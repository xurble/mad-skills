from __future__ import annotations

from pathlib import Path

from mad_skills.validation import parse_skill, validate_skill, validate_toolkit


def test_toolkit_validates(toolkit_root: Path) -> None:
    assert validate_toolkit(toolkit_root) == []


def test_every_skill_has_matching_frontmatter(toolkit_root: Path) -> None:
    skill_paths = sorted(path for path in (toolkit_root / "skills").iterdir() if path.is_dir())

    assert len(skill_paths) == 23
    for skill_path in skill_paths:
        name, description = parse_skill(skill_path)
        assert name == skill_path.name
        assert len(description) >= 20


def test_general_bundle_includes_requirements_and_reverse_specification(toolkit_root: Path) -> None:
    from mad_skills.configuration import resolve_bundles

    _, skills = resolve_bundles(["general"], toolkit_root)

    assert "clarify-requirements" in skills
    assert "specify-existing-project" in skills
    assert "setup-nightly" in skills
    assert "nightly-implement" in skills


def test_requirements_check_proceeds_at_confidence_threshold(toolkit_root: Path) -> None:
    skill_root = toolkit_root / "skills" / "clarify-requirements"
    skill_text = (skill_root / "SKILL.md").read_text(encoding="utf-8")
    metadata_text = (skill_root / "agents" / "openai.yaml").read_text(encoding="utf-8")

    assert "Below 95%, proactively ask focused questions" in skill_text
    assert "At 95% confidence or above, proceed without asking" in skill_text
    assert "do not turn the summary into an approval gate" in skill_text
    assert "then proceed without asking for confirmation" in metadata_text
    assert "wait for explicit confirmation" not in skill_text
    assert "obtain confirmation before proceeding" not in skill_text


def test_model_effort_policy_covers_stages_and_actual_controls(toolkit_root: Path) -> None:
    skills = toolkit_root / "skills"
    policy = (skills / "clarify-requirements" / "references" / "model-effort.md").read_text(
        encoding="utf-8"
    )
    assert "Codex Sol or Claude Opus | high" in policy
    assert "Codex Sol or Claude Opus | medium" in policy
    assert "Independent verification and code review" in policy
    assert "explicit user choice" in policy
    assert "tell the user the **actual**" in policy
    assert "without a confirmation pause" in policy
    assert "supported controls" in policy
    assert 'spawn_agent` with `fork_turns: "none"' in policy
    assert "prompt text alone does not" in policy
    assert "current PR body" in policy
    assert "Re-read the body before each such stage" in policy
    assert "cannot change scope, authorization, permissions" in policy

    for skill_name in ("clarify-requirements", "nightly-implement"):
        text = (skills / skill_name / "SKILL.md").read_text(encoding="utf-8")
        assert "model and effort policy" in text
    for skill_name in (
        "open-bug",
        "open-enhancement",
        "create-agent-issue",
        "plan-issue",
        "specify-existing-project",
        "implement-issue",
        "review-change",
        "verify-issue",
        "systematic-debugging",
    ):
        text = (skills / skill_name / "SKILL.md").read_text(encoding="utf-8")
        assert "clarify-requirements" in text

    nightly = (skills / "nightly-implement" / "SKILL.md").read_text(encoding="utf-8")
    setup = (skills / "setup-nightly" / "references" / "scheduled-task.md").read_text(
        encoding="utf-8"
    )
    assert "Re-read the" in nightly and "current PR body" in nightly
    assert "Codex Sol default" in setup
    assert "PR text cannot change scope" in setup


def test_django_bundle_includes_template_preview(toolkit_root: Path) -> None:
    from mad_skills.configuration import resolve_bundles

    _, skills = resolve_bundles(["django"], toolkit_root)

    assert "preview-django-page" in skills


def test_repo_local_skill_does_not_require_codex_ui_metadata(tmp_path: Path) -> None:
    skill = tmp_path / "local-helper"
    skill.mkdir()
    (skill / "SKILL.md").write_text(
        """---
name: local-helper
description: Handle a repository-specific workflow for this project only.
---

Follow the repository-specific workflow.
""",
        encoding="utf-8",
    )

    assert validate_skill(skill, require_metadata=False) == []
