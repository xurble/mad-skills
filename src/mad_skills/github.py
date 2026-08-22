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

MERGE_METHOD_FIELDS = {
    "merge": "mergeCommitAllowed",
    "squash": "squashMergeAllowed",
    "rebase": "rebaseMergeAllowed",
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


def repository_settings(repo_root: Path) -> dict[str, bool]:
    require_gh(repo_root)
    fields = [*MERGE_METHOD_FIELDS.values(), "deleteBranchOnMerge"]
    result = subprocess.run(
        ["gh", "repo", "view", "--json", ",".join(fields)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise MadSkillsError(f"Cannot read GitHub repository settings: {detail}")
    try:
        data = json.loads(result.stdout)
        return {field: data[field] for field in fields}
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        raise MadSkillsError(f"Unexpected response from gh repo view: {exc}") from exc


def mismatched_repository_settings(repo_root: Path, github_config: dict[str, Any]) -> list[str]:
    actual = repository_settings(repo_root)
    merge_method = github_config.get("merge_method", "squash")
    mismatches = []
    for method, field in MERGE_METHOD_FIELDS.items():
        expected = method == merge_method
        if actual[field] is not expected:
            state = "enabled" if expected else "disabled"
            mismatches.append(f"{method} merges should be {state}")
    expected_deletion = github_config.get("delete_branch_on_merge", True)
    if actual["deleteBranchOnMerge"] is not expected_deletion:
        state = "enabled" if expected_deletion else "disabled"
        mismatches.append(f"automatic branch deletion should be {state}")
    return mismatches


def configure_repository(repo_root: Path, github_config: dict[str, Any]) -> None:
    require_gh(repo_root)
    merge_method = github_config.get("merge_method", "squash")
    arguments = ["gh", "repo", "edit"]
    for method, flag in (
        ("merge", "--enable-merge-commit"),
        ("squash", "--enable-squash-merge"),
        ("rebase", "--enable-rebase-merge"),
    ):
        arguments.append(f"{flag}={'true' if method == merge_method else 'false'}")
    arguments.append(
        f"--delete-branch-on-merge={'true' if github_config.get('delete_branch_on_merge', True) else 'false'}"
    )
    if merge_method == "squash":
        message = github_config.get("squash_merge_commit_message", "pr-title-description")
        arguments.append(f"--squash-merge-commit-message={message}")
    result = subprocess.run(
        arguments,
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise MadSkillsError(f"Could not configure GitHub repository settings: {detail}")
