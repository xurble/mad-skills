from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from mad_skills.errors import MadSkillsError


@dataclass(frozen=True)
class LabelDefinition:
    color: str
    description: str


LABEL_DEFINITIONS = {
    "bug": LabelDefinition("d73a4a", "Something is not working"),
    "enhancement": LabelDefinition("a2eeef", "New feature or improvement"),
    "actionable": LabelDefinition("0e8a16", "Ready for an implementation agent"),
    "needs_investigation": LabelDefinition("fbca04", "More evidence or diagnosis is needed"),
    "blocked": LabelDefinition("b60205", "Blocked on a decision or dependency"),
    "high_risk": LabelDefinition("b60205", "Requires rigorous risk handling"),
    "in_progress": LabelDefinition("1d76db", "Implementation is in progress"),
    "verified": LabelDefinition("0e8a16", "Acceptance criteria were independently verified"),
}


def require_gh(repo_root: Path) -> None:
    if not shutil.which("gh"):
        raise MadSkillsError("GitHub support requires the gh CLI. Install gh, run 'gh auth login', and retry.")
    result = subprocess.run(
        ["gh", "auth", "status"],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
        timeout=15,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise MadSkillsError(f"gh is not authenticated. Run 'gh auth login' and retry. {detail}")


def existing_labels(repo_root: Path) -> set[str]:
    require_gh(repo_root)
    result = subprocess.run(
        ["gh", "label", "list", "--limit", "1000", "--json", "name"],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise MadSkillsError(f"Cannot read GitHub labels for this repository: {detail}")
    try:
        return {entry["name"] for entry in json.loads(result.stdout)}
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        raise MadSkillsError(f"Unexpected response from gh label list: {exc}") from exc


def missing_labels(repo_root: Path, github_config: dict[str, Any]) -> list[tuple[str, LabelDefinition]]:
    current = existing_labels(repo_root)
    configured = github_config.get("labels", {})
    result = []
    for semantic_name, definition in LABEL_DEFINITIONS.items():
        label_name = configured.get(semantic_name)
        if label_name and label_name not in current:
            result.append((label_name, definition))
    return result


def create_labels(repo_root: Path, labels: list[tuple[str, LabelDefinition]]) -> None:
    for name, definition in labels:
        result = subprocess.run(
            [
                "gh",
                "label",
                "create",
                name,
                "--color",
                definition.color,
                "--description",
                definition.description,
            ],
            cwd=repo_root,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip()
            raise MadSkillsError(f"Could not create GitHub label {name!r}: {detail}")
