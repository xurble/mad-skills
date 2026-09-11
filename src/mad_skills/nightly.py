"""Read-only issue selection. Scheduling and execution belong to Codex."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

from mad_skills.configuration import resolve_project
from mad_skills.errors import MadSkillsError
from mad_skills.github import require_gh


def _read_gh(repo_root: Path, arguments: list[str]) -> Any:
    try:
        result = subprocess.run(
            ["gh", *arguments], cwd=repo_root, capture_output=True, text=True, check=False, timeout=120
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise MadSkillsError(f"Cannot read nightly candidates with gh: {exc}") from exc
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        raise MadSkillsError(f"Cannot read nightly candidates with gh: {detail}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise MadSkillsError(f"Unexpected response from gh: {exc}") from exc


def oldest_actionable(pages: Any, labels: dict[str, str]) -> dict[str, Any] | None:
    """Select across every REST page, excluding PRs and non-eligible issues."""
    candidates = []
    try:
        if not isinstance(pages, list) or any(not isinstance(page, list) for page in pages):
            raise ValueError("expected paginated issue arrays")
        for page in pages:
            for issue in page:
                if "pull_request" in issue or issue["state"] != "open":
                    continue
                names = {label["name"] for label in issue["labels"]}
                if labels["actionable"] not in names or names.intersection(
                    {labels["blocked"], labels["in_progress"]}
                ):
                    continue
                created = datetime.fromisoformat(issue["created_at"].replace("Z", "+00:00"))
                if created.tzinfo is None or type(issue["number"]) is not int or issue["number"] < 1:
                    raise ValueError("expected a timezone-aware creation date and positive issue number")
                candidates.append((created, issue["number"], issue))
        if not candidates:
            return None
        issue = min(candidates, key=lambda candidate: candidate[:2])[2]
        return {"number": issue["number"], "url": issue["html_url"], "created_at": issue["created_at"]}
    except (KeyError, TypeError, ValueError, AttributeError) as exc:
        raise MadSkillsError(f"Unexpected response from gh issues: {exc}") from exc


def nightly_candidate(path: Path) -> dict[str, Any]:
    effective = resolve_project(path)
    github = effective.data["github"]
    if not effective.configured or not github.get("use_issues"):
        raise MadSkillsError("Nightly selection requires project configuration with github.use_issues enabled")
    labels = github["labels"]
    workflow_names = [
        labels.get(key) for key in ("actionable", "needs_investigation", "blocked", "in_progress", "verified")
    ]
    if any(not isinstance(name, str) or not name.strip() for name in workflow_names):
        raise MadSkillsError("Nightly selection requires non-empty workflow label mappings")
    if len(set(workflow_names)) != len(workflow_names):
        raise MadSkillsError("Nightly workflow labels must have distinct names")
    require_gh(effective.repo_root)
    prs = _read_gh(effective.repo_root, ["pr", "list", "--state", "open", "--limit", "1", "--json", "number,url"])
    if not isinstance(prs, list):
        raise MadSkillsError("Unexpected response from gh pr list: expected an array")
    if prs:
        return {"status": "skip", "reason": "open_pr", "issue": None}
    pages = _read_gh(
        effective.repo_root,
        [
            "api", "--method", "GET", "repos/{owner}/{repo}/issues",
            "-f", "state=open", "-f", "sort=created", "-f", "direction=asc",
            "-F", "per_page=100", "--paginate", "--slurp",
        ],
    )
    issue = oldest_actionable(pages, labels)
    if issue is None:
        return {"status": "skip", "reason": "no_actionable_issue", "issue": None}
    return {"status": "candidate", "reason": None, "issue": issue}
