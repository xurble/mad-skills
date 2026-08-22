from __future__ import annotations

from pathlib import Path

import pytest

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


def test_rigorous_initialization_requires_check_command(tmp_path: Path) -> None:
    with pytest.raises(MadSkillsError, match="requires --check-command"):
        propose_initialization(
            tmp_path,
            project_type="django",
            profile="rigorous",
            use_github=True,
        )
