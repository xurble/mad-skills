from __future__ import annotations

from pathlib import Path

from mad_skills.validation import parse_skill, validate_skill, validate_toolkit


def test_toolkit_validates(toolkit_root: Path) -> None:
    assert validate_toolkit(toolkit_root) == []


def test_every_skill_has_matching_frontmatter(toolkit_root: Path) -> None:
    skill_paths = sorted((toolkit_root / "skills").iterdir())

    assert len(skill_paths) == 20
    for skill_path in skill_paths:
        name, description = parse_skill(skill_path)
        assert name == skill_path.name
        assert len(description) >= 20


def test_general_bundle_includes_reverse_specification(toolkit_root: Path) -> None:
    from mad_skills.configuration import resolve_bundles

    _, skills = resolve_bundles(["general"], toolkit_root)

    assert "specify-existing-project" in skills


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
