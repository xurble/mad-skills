from __future__ import annotations

from pathlib import Path

import pytest

from mad_skills.errors import MadSkillsError
from mad_skills.installer import claude_agent_files, install, skill_directories


def test_install_all_links_every_skill_and_is_idempotent(tmp_path: Path, toolkit_root: Path) -> None:
    skills = skill_directories(toolkit_root)
    agents = claude_agent_files(toolkit_root)

    first = install("all", home=tmp_path, toolkit_root=toolkit_root)
    second = install("all", home=tmp_path, toolkit_root=toolkit_root)

    assert len(first) == len(skills) * 2 + len(agents)
    assert all(action.state == "create" for action in first)
    assert all(action.state == "current" for action in second)
    for scope in (".agents/skills", ".claude/skills"):
        for skill in skills:
            link = tmp_path / scope / skill.name
            assert link.is_symlink()
            assert link.resolve() == skill.resolve()


def test_conflict_stops_before_creating_any_links(tmp_path: Path, toolkit_root: Path) -> None:
    conflict = tmp_path / ".agents/skills/open-bug"
    conflict.mkdir(parents=True)

    with pytest.raises(MadSkillsError, match="unmanaged paths"):
        install("all", home=tmp_path, toolkit_root=toolkit_root)

    assert not (tmp_path / ".claude/skills/testing").exists()
    assert not (tmp_path / ".agents/skills/testing").exists()


def test_broken_or_foreign_symlink_is_a_conflict(tmp_path: Path, toolkit_root: Path) -> None:
    destination = tmp_path / ".agents/skills/testing"
    destination.parent.mkdir(parents=True)
    destination.symlink_to(tmp_path / "missing")

    with pytest.raises(MadSkillsError, match="testing"):
        install("codex", home=tmp_path, toolkit_root=toolkit_root)


def test_non_directory_scope_parent_is_a_conflict(tmp_path: Path, toolkit_root: Path) -> None:
    (tmp_path / ".agents").write_text("not a directory", encoding="utf-8")

    with pytest.raises(MadSkillsError, match=r"\.agents"):
        install("codex", home=tmp_path, toolkit_root=toolkit_root)


def test_claude_install_links_reviewer_agent_but_codex_does_not(tmp_path: Path, toolkit_root: Path) -> None:
    reviewer = toolkit_root / "claude-agents/mad-skills-reviewer.md"
    assert reviewer in claude_agent_files(toolkit_root)

    install("codex", home=tmp_path / "codex", toolkit_root=toolkit_root)
    install("claude", home=tmp_path / "claude", toolkit_root=toolkit_root)

    assert not (tmp_path / "codex/.claude").exists()
    link = tmp_path / "claude/.claude/agents/mad-skills-reviewer.md"
    assert link.is_symlink()
    assert link.resolve() == reviewer.resolve()


def test_unmanaged_agent_file_is_a_conflict_and_is_preserved(tmp_path: Path, toolkit_root: Path) -> None:
    existing = tmp_path / ".claude/agents/mad-skills-reviewer.md"
    existing.parent.mkdir(parents=True)
    existing.write_text("user agent", encoding="utf-8")

    with pytest.raises(MadSkillsError, match="mad-skills-reviewer.md"):
        install("claude", home=tmp_path, toolkit_root=toolkit_root)

    assert existing.read_text(encoding="utf-8") == "user agent"
    assert not (tmp_path / ".claude/skills/testing").exists()
