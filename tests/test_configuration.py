from __future__ import annotations

from pathlib import Path

import pytest

from mad_skills.configuration import load_yaml, resolve_project, validate_project_data
from mad_skills.errors import MadSkillsError
from tests.conftest import write_project_config


def test_unconfigured_project_uses_light_general(tmp_path: Path, toolkit_root: Path) -> None:
    effective = resolve_project(tmp_path, toolkit_root)

    assert effective.configured is False
    assert effective.data["project"] == {
        "type": "general",
        "profile": "light",
        "extra_bundles": [],
    }
    assert effective.bundles == ("general",)
    assert "implement-issue" in effective.skills
    assert effective.data["verification"]["full_check_required"] is False
    assert effective.data["git"]["conventional_commits"] is True
    assert effective.data["github"]["merge_method"] == "squash"
    assert effective.data["github"]["delete_branch_on_merge"] is True


def test_django_type_adds_general_python_and_django_skills(tmp_path: Path, toolkit_root: Path) -> None:
    write_project_config(
        tmp_path,
        """project:
  type: django
  profile: normal
""",
    )

    effective = resolve_project(tmp_path, toolkit_root)

    assert effective.bundles == ("general", "django")
    assert "python-development" in effective.skills
    assert "django-development" in effective.skills
    assert effective.data["testing"]["meaningful_changes_require_tests"] is True


def test_extra_bundles_are_additive(tmp_path: Path, toolkit_root: Path) -> None:
    write_project_config(
        tmp_path,
        """project:
  type: ios
  profile: normal
  extra_bundles:
    - python
ios:
  project: Example.xcodeproj
  scheme: Example
""",
    )

    effective = resolve_project(tmp_path, toolkit_root)

    assert effective.bundles == ("general", "ios", "python")
    assert "ios-development" in effective.skills
    assert "python-development" in effective.skills


def test_unknown_configuration_key_fails(tmp_path: Path, toolkit_root: Path) -> None:
    write_project_config(
        tmp_path,
        """project:
  type: general
  profile: light
mispelled: true
""",
    )

    with pytest.raises(MadSkillsError, match="Additional properties"):
        resolve_project(tmp_path, toolkit_root)


def test_extensions_are_allowed(toolkit_root: Path) -> None:
    data = {
        "project": {"type": "general", "profile": "light"},
        "extensions": {"example": {"anything": True}},
    }

    assert validate_project_data(data, toolkit_root) == []


def test_rigorous_requires_check_and_github(toolkit_root: Path) -> None:
    data = {"project": {"type": "django", "profile": "rigorous"}}

    errors = validate_project_data(data, toolkit_root)

    assert any("commands" in error for error in errors)
    assert any("github" in error for error in errors)


def test_rigorous_profile_allows_work_without_an_issue(tmp_path: Path, toolkit_root: Path) -> None:
    path = write_project_config(
        tmp_path,
        """project:
  type: django
  profile: rigorous
commands:
  check: ./scripts/check
github:
  use_issues: true
  require_issue_for_nontrivial_work: false
""",
    )

    errors = validate_project_data(load_yaml(path), toolkit_root)

    assert errors == []
    effective = resolve_project(tmp_path, toolkit_root)
    assert effective.data["github"]["require_issue_for_nontrivial_work"] is False
    assert effective.data["github"]["require_pull_request_for_nontrivial_work"] is True
    assert effective.data["github"]["require_well_specified_pull_request_for_nontrivial_work"] is True
    assert effective.data["github"]["open_pull_requests_as_draft_until_reviewed"] is True


@pytest.mark.parametrize(
    ("setting", "message"),
    [
        (
            "require_pull_request_for_nontrivial_work",
            "github.require_pull_request_for_nontrivial_work cannot be false for rigorous",
        ),
        (
            "require_well_specified_pull_request_for_nontrivial_work",
            "github.require_well_specified_pull_request_for_nontrivial_work cannot be false for rigorous",
        ),
        (
            "open_pull_requests_as_draft_until_reviewed",
            "github.open_pull_requests_as_draft_until_reviewed cannot be false for rigorous",
        ),
    ],
)
def test_rigorous_profile_cannot_disable_required_pr_gate(
    tmp_path: Path, toolkit_root: Path, setting: str, message: str
) -> None:
    path = write_project_config(
        tmp_path,
        f"""project:
  type: django
  profile: rigorous
commands:
  check: ./scripts/check
github:
  use_issues: true
  {setting}: false
""",
    )

    errors = validate_project_data(load_yaml(path), toolkit_root)

    assert message in errors


def test_context_includes_source_locations(tmp_path: Path, toolkit_root: Path) -> None:
    effective = resolve_project(tmp_path, toolkit_root)

    resolved = effective.serializable()["resolved"]
    assert resolved["toolkit_root"] == str(toolkit_root)
    assert resolved["repo_root"] == str(tmp_path)
