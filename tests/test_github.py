from __future__ import annotations

import os
from pathlib import Path

import pytest

from mad_skills.errors import MadSkillsError
from mad_skills.github import create_labels, missing_labels, require_gh


def make_fake_gh(directory: Path) -> Path:
    script = directory / "gh"
    script.write_text(
        """#!/bin/sh
set -eu
if [ "$1" = "auth" ]; then
  exit 0
fi
if [ "$1" = "label" ] && [ "$2" = "list" ]; then
  echo '[{"name":"bug"}]'
  exit 0
fi
if [ "$1" = "label" ] && [ "$2" = "create" ]; then
  echo "$3" >> "$FAKE_GH_LOG"
  exit 0
fi
exit 1
""",
        encoding="utf-8",
    )
    script.chmod(0o755)
    return script


def test_missing_gh_stops_with_setup_instruction(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PATH", "")

    with pytest.raises(MadSkillsError, match="Install gh"):
        require_gh(tmp_path)


def test_label_detection_and_creation(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    executable_dir = tmp_path / "bin"
    executable_dir.mkdir()
    make_fake_gh(executable_dir)
    log = tmp_path / "created.log"
    monkeypatch.setenv("PATH", f"{executable_dir}{os.pathsep}{os.environ.get('PATH', '')}")
    monkeypatch.setenv("FAKE_GH_LOG", str(log))
    github_config = {
        "labels": {
            "bug": "bug",
            "enhancement": "enhancement",
            "actionable": "agent-actionable",
        }
    }

    missing = missing_labels(tmp_path, github_config)
    create_labels(tmp_path, missing)

    assert [name for name, _ in missing] == ["enhancement", "agent-actionable"]
    assert log.read_text(encoding="utf-8").splitlines() == ["enhancement", "agent-actionable"]
