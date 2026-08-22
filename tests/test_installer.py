from __future__ import annotations

from pathlib import Path

import pytest

from mad_skills.errors import MadSkillsError
from mad_skills.installer import install, skill_directories


def test_install_all_links_every_skill_and_is_idempotent(tmp_path: Path, toolkit_root: Path) -> None:
    skills = skill_directories(toolkit_root)

    first = install("all", home=tmp_path, toolkit_root=toolkit_root)
    second = install("all", home=tmp_path, toolkit_root=toolkit_root)

    assert len(first) == len(skills) * 2
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
