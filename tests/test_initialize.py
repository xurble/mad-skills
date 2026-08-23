from __future__ import annotations

from pathlib import Path

import pytest

from mad_skills.cli import main
from mad_skills.configuration import load_yaml, validate_project_data
from mad_skills.errors import MadSkillsError
from mad_skills.initialize import (
    detect_project,
    initialize_interactive,
    propose_initialization,
)


def test_detects_django_and_existing_commands(tmp_path: Path) -> None:
    (tmp_path / "manage.py").write_text("", encoding="utf-8")
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    (scripts / "check").write_text("#!/bin/sh\n", encoding="utf-8")

    detected = detect_project(tmp_path)

    assert detected.project_type == "django"
    assert detected.commands == {"check": "./scripts/check"}


def test_detects_ios_project(tmp_path: Path) -> None:
    (tmp_path / "Sample.xcodeproj").mkdir()

    detected = detect_project(tmp_path)

    assert detected.project_type == "ios"
    assert detected.ios == {"project": "Sample.xcodeproj", "scheme": "Sample"}


def test_initialization_writes_config_guidance_and_claude_shim(tmp_path: Path, toolkit_root: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("[project]\nname='sample'\n", encoding="utf-8")

    proposals = initialize_interactive(
        tmp_path,
        project_type="python",
        profile="light",
        use_github=False,
        assume_yes=True,
    )

    assert len(proposals) == 3
    config = load_yaml(tmp_path / ".agent/config.yaml")
    assert validate_project_data(config, toolkit_root) == []
    assert config["project"] == {"type": "python", "profile": "light"}
    assert config["git"] == {"conventional_commits": True}
    assert config["github"] == {
        "enabled": False,
        "use_issues": False,
        "merge_method": "squash",
        "squash_merge_commit_message": "pr-title-description",
        "delete_branch_on_merge": True,
    }
    assert "Type: `python`" in (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    assert (tmp_path / "CLAUDE.md").read_text(encoding="utf-8") == "@AGENTS.md\n"


def test_existing_agents_is_preserved(tmp_path: Path) -> None:
    agents = tmp_path / "AGENTS.md"
    agents.write_text("Keep me\n", encoding="utf-8")

    proposals = propose_initialization(
        tmp_path,
        project_type="general",
        profile="light",
        use_github=False,
    )

    assert agents not in {proposal.path for proposal in proposals}
    assert agents.read_text(encoding="utf-8") == "Keep me\n"


def test_initialization_can_enable_github_without_issues(
    tmp_path: Path, toolkit_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("mad_skills.initialize.require_gh", lambda repo_root: None)
    monkeypatch.setattr("mad_skills.initialize.mismatched_repository_settings", lambda repo_root, config: [])
    monkeypatch.setattr(
        "mad_skills.initialize.missing_labels",
        lambda repo_root, config: pytest.fail("PR-only initialization should not inspect issue labels"),
    )
    proposals = initialize_interactive(
        tmp_path,
        project_type="general",
        profile="light",
        use_github=True,
        use_issues=False,
        assume_yes=True,
    )

    assert len(proposals) == 3
    config = load_yaml(tmp_path / ".agent/config.yaml")
    assert validate_project_data(config, toolkit_root) == []
    assert config["github"]["enabled"] is True
    assert config["github"]["use_issues"] is False


def test_rigorous_initialization_requires_check_command(tmp_path: Path) -> None:
    with pytest.raises(MadSkillsError) as error:
        propose_initialization(
            tmp_path,
            project_type="django",
            profile="rigorous",
            use_github=True,
        )

    message = str(error.value)
    assert "project check command" in message
    assert "validates the repository before a change is accepted" in message
    assert "--check-command './scripts/check'" in message


def test_check_command_option_without_value_has_actionable_error(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as error:
        main(["init", "--check-command"])

    assert error.value.code == 2
    assert "--check-command needs the project validation command as its value" in capsys.readouterr().err


def test_github_initialization_applies_standard_repository_settings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    configured = []
    monkeypatch.setattr("mad_skills.initialize.require_gh", lambda repo_root: None)
    monkeypatch.setattr("mad_skills.initialize.missing_labels", lambda repo_root, config: [])
    monkeypatch.setattr(
        "mad_skills.initialize.mismatched_repository_settings",
        lambda repo_root, config: ["squash merges should be enabled"],
    )
    monkeypatch.setattr(
        "mad_skills.initialize.configure_repository",
        lambda repo_root, config: configured.append((repo_root, config)),
    )

    initialize_interactive(
        tmp_path,
        project_type="general",
        profile="light",
        use_github=True,
        assume_yes=True,
    )

    assert len(configured) == 1
    assert configured[0][0] == tmp_path
    assert configured[0][1]["merge_method"] == "squash"
    assert configured[0][1]["delete_branch_on_merge"] is True


def test_setup_github_command_applies_configured_settings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config_path = tmp_path / ".agent/config.yaml"
    config_path.parent.mkdir()
    config_path.write_text(
        """project:
  type: general
  profile: light
github:
  use_issues: true
""",
        encoding="utf-8",
    )
    configured = []
    monkeypatch.setattr(
        "mad_skills.cli.mismatched_repository_settings",
        lambda repo_root, config: ["squash merges should be enabled"],
    )
    monkeypatch.setattr("mad_skills.cli.missing_labels", lambda repo_root, config: [])
    monkeypatch.setattr(
        "mad_skills.cli.configure_repository",
        lambda repo_root, config: configured.append((repo_root, config)),
    )

    result = main(["setup-github", str(tmp_path), "--yes"])

    assert result == 0
    assert len(configured) == 1
    assert configured[0][1]["merge_method"] == "squash"


def test_setup_github_supports_pr_only_projects(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    config_path = tmp_path / ".agent/config.yaml"
    config_path.parent.mkdir()
    config_path.write_text(
        """project:
  type: general
  profile: light
github:
  enabled: true
  use_issues: false
""",
        encoding="utf-8",
    )
    configured = []
    monkeypatch.setattr(
        "mad_skills.cli.mismatched_repository_settings",
        lambda repo_root, config: ["squash merges should be enabled"],
    )
    monkeypatch.setattr(
        "mad_skills.cli.missing_labels",
        lambda repo_root, config: pytest.fail("PR-only setup should not inspect issue labels"),
    )
    monkeypatch.setattr(
        "mad_skills.cli.configure_repository",
        lambda repo_root, config: configured.append((repo_root, config)),
    )

    result = main(["setup-github", str(tmp_path), "--yes"])

    assert result == 0
    assert len(configured) == 1
