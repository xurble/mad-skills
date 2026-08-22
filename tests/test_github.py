from __future__ import annotations

import os
from pathlib import Path

import pytest

from mad_skills.errors import MadSkillsError
from mad_skills.github import (
    configure_repository,
    create_labels,
    mismatched_repository_settings,
    missing_labels,
    require_gh,
)


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
if [ "$1" = "repo" ] && [ "$2" = "view" ]; then
  if [ -n "${FAKE_GH_SETTINGS:-}" ]; then
    echo "$FAKE_GH_SETTINGS"
  else
    echo '{"mergeCommitAllowed":false,"squashMergeAllowed":true,"rebaseMergeAllowed":false,"deleteBranchOnMerge":true}'
  fi
  exit 0
fi
if [ "$1" = "repo" ] && [ "$2" = "edit" ]; then
  echo "$*" > "$FAKE_GH_LOG"
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


def test_repository_settings_are_detected_and_configured(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    executable_dir = tmp_path / "bin"
    executable_dir.mkdir()
    make_fake_gh(executable_dir)
    log = tmp_path / "repo-edit.log"
    monkeypatch.setenv("PATH", f"{executable_dir}{os.pathsep}{os.environ.get('PATH', '')}")
    monkeypatch.setenv("FAKE_GH_LOG", str(log))
    monkeypatch.setenv(
        "FAKE_GH_SETTINGS",
        '{"mergeCommitAllowed":true,"squashMergeAllowed":false,'
        '"rebaseMergeAllowed":true,"deleteBranchOnMerge":false}',
    )
    github_config = {
        "merge_method": "squash",
        "squash_merge_commit_message": "pr-title-description",
        "delete_branch_on_merge": True,
    }

    mismatches = mismatched_repository_settings(tmp_path, github_config)
    configure_repository(tmp_path, github_config)

    assert mismatches == [
        "merge merges should be disabled",
        "squash merges should be enabled",
        "rebase merges should be disabled",
        "automatic branch deletion should be enabled",
    ]
    arguments = log.read_text(encoding="utf-8")
    assert "--enable-merge-commit=false" in arguments
    assert "--enable-squash-merge=true" in arguments
    assert "--enable-rebase-merge=false" in arguments
    assert "--delete-branch-on-merge=true" in arguments
    assert "--squash-merge-commit-message=pr-title-description" in arguments
