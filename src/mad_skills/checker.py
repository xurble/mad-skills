from __future__ import annotations

import shlex
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from mad_skills.configuration import EffectiveConfig, github_workflow_enabled, resolve_project
from mad_skills.errors import MadSkillsError
from mad_skills.github import mismatched_repository_settings, missing_labels, require_gh
from mad_skills.installer import TARGET_PATHS
from mad_skills.paths import find_toolkit_root
from mad_skills.validation import validate_skill


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    message: str

    def render(self) -> str:
        return f"{self.severity.upper():7} {self.code}: {self.message}"


@dataclass(frozen=True)
class CheckResult:
    findings: tuple[Finding, ...]

    @property
    def status(self) -> str:
        if any(item.severity == "error" for item in self.findings):
            return "NOT READY"
        if any(item.severity == "warning" for item in self.findings):
            return "READY WITH WARNINGS"
        return "READY"


def check_project(
    start: Path | None = None,
    *,
    full: bool = False,
    home: Path | None = None,
    toolkit_root: Path | None = None,
    check_github: bool = True,
) -> CheckResult:
    root = toolkit_root or find_toolkit_root()
    findings: list[Finding] = []
    try:
        effective = resolve_project(start, root)
    except MadSkillsError as exc:
        return CheckResult((Finding("error", "config", str(exc)),))

    actual_home = (home or Path.home()).expanduser().resolve()
    _check_installation(effective, root, actual_home, findings)
    _check_guidance(effective, findings)
    _check_commands(effective, findings)
    _check_local_skills(effective, root, findings)
    _check_decisions(effective, findings)
    _check_policy(effective, full, findings)
    if check_github and github_workflow_enabled(effective.data["github"]):
        _check_github(effective, findings, check_remote=True)
    if full:
        _run_full_check(effective, findings)
    findings.sort(key=lambda item: ({"error": 0, "warning": 1, "info": 2}[item.severity], item.code))
    return CheckResult(tuple(findings))


def _check_installation(effective: EffectiveConfig, toolkit_root: Path, home: Path, findings: list[Finding]) -> None:
    for target_name, relative in TARGET_PATHS.items():
        missing = []
        for skill in effective.skills:
            expected = toolkit_root / "skills" / skill
            installed = home / relative / skill
            if not installed.is_symlink() or installed.resolve(strict=False) != expected.resolve():
                missing.append(skill)
        if missing:
            severity = "error" if target_name == "codex" else "warning"
            findings.append(
                Finding(
                    severity,
                    f"install.{target_name}",
                    f"{len(missing)} resolved skill(s) are not linked correctly; run "
                    f"'mad-skills install --target {target_name}'",
                )
            )


def _check_guidance(effective: EffectiveConfig, findings: list[Finding]) -> None:
    if not effective.configured:
        findings.append(
            Finding(
                "warning",
                "config.missing",
                "No .agent/config.yaml; passive guidance uses light/general and "
                "action skills will offer initialization",
            )
        )
        return
    agents = effective.repo_root / "AGENTS.md"
    if not agents.is_file() or not agents.read_text(encoding="utf-8").strip():
        findings.append(Finding("error", "guidance.agents", "AGENTS.md is missing or empty"))
    claude = effective.repo_root / "CLAUDE.md"
    if not claude.is_file():
        findings.append(Finding("warning", "guidance.claude", "CLAUDE.md import shim is missing"))
    elif "@AGENTS.md" not in claude.read_text(encoding="utf-8"):
        findings.append(Finding("warning", "guidance.claude", "CLAUDE.md does not import AGENTS.md"))


def _check_commands(effective: EffectiveConfig, findings: list[Finding]) -> None:
    for name, command in effective.data.get("commands", {}).items():
        try:
            parts = shlex.split(command)
        except ValueError as exc:
            findings.append(Finding("error", f"command.{name}", f"cannot parse command: {exc}"))
            continue
        executable = next((part for part in parts if "=" not in part or part.startswith("./")), None)
        if not executable:
            findings.append(Finding("error", f"command.{name}", "command has no executable"))
            continue
        if "/" in executable:
            candidate = (effective.repo_root / executable).resolve()
            if not candidate.exists():
                findings.append(Finding("error", f"command.{name}", f"configured path does not exist: {executable}"))
        elif shutil.which(executable) is None:
            findings.append(Finding("error", f"command.{name}", f"executable is not on PATH: {executable}"))


def _check_local_skills(effective: EffectiveConfig, toolkit_root: Path, findings: list[Finding]) -> None:
    shared = {path.name for path in (toolkit_root / "skills").iterdir() if path.is_dir()}
    for relative in (Path(".agents/skills"), Path(".claude/skills")):
        directory = effective.repo_root / relative
        if not directory.is_dir():
            continue
        for skill in sorted(path for path in directory.iterdir() if path.is_dir()):
            for issue in validate_skill(skill, require_metadata=False):
                findings.append(Finding("error", "local-skill.invalid", issue.render(effective.repo_root)))
            if skill.name in shared and skill.resolve() != (toolkit_root / "skills" / skill.name).resolve():
                findings.append(
                    Finding(
                        "warning",
                        "local-skill.shadow",
                        f"{skill} duplicates shared skill {skill.name}; extend it under a distinct name",
                    )
                )


def _check_decisions(effective: EffectiveConfig, findings: list[Finding]) -> None:
    log = effective.data.get("decisions", {}).get("log")
    if log and not (effective.repo_root / log).is_file():
        findings.append(Finding("error", "decisions.log", f"configured decision log is missing: {log}"))


def _check_policy(effective: EffectiveConfig, full: bool, findings: list[Finding]) -> None:
    profile = effective.data["project"]["profile"]
    if profile == "rigorous":
        required = {
            "github.require_pull_request_for_nontrivial_work": effective.data["github"].get(
                "require_pull_request_for_nontrivial_work"
            ),
            "github.require_well_specified_pull_request_for_nontrivial_work": effective.data["github"].get(
                "require_well_specified_pull_request_for_nontrivial_work"
            ),
            "github.open_pull_requests_as_draft_until_reviewed": effective.data["github"].get(
                "open_pull_requests_as_draft_until_reviewed"
            ),
            "planning.required_for_nontrivial_work": effective.data["planning"].get("required_for_nontrivial_work"),
            "verification.fresh_context_for_nontrivial_work": effective.data["verification"].get(
                "fresh_context_for_nontrivial_work"
            ),
            "verification.separate_review_for_nontrivial_work": effective.data["verification"].get(
                "separate_review_for_nontrivial_work"
            ),
            "verification.full_check_required": effective.data["verification"].get("full_check_required"),
        }
        for key, value in required.items():
            if not value:
                findings.append(Finding("error", "policy.rigorous", f"rigorous policy requires {key}"))
        if not full:
            findings.append(Finding("warning", "check.full", "Rigorous project has not run commands.check; use --full"))


def _check_github(effective: EffectiveConfig, findings: list[Finding], *, check_remote: bool) -> None:
    try:
        require_gh(effective.repo_root)
        if check_remote:
            if effective.data["github"].get("use_issues"):
                missing = missing_labels(effective.repo_root, effective.data["github"])
                if missing:
                    names = ", ".join(name for name, _ in missing)
                    findings.append(
                        Finding(
                            "error",
                            "github.labels",
                            f"missing configured labels: {names}; run 'mad-skills setup-github'",
                        )
                    )
            mismatches = mismatched_repository_settings(effective.repo_root, effective.data["github"])
            if mismatches:
                findings.append(
                    Finding(
                        "error",
                        "github.settings",
                        "; ".join(mismatches) + "; run 'mad-skills setup-github'",
                    )
                )
    except (MadSkillsError, subprocess.TimeoutExpired) as exc:
        findings.append(Finding("error", "github.gh", str(exc)))


def _run_full_check(effective: EffectiveConfig, findings: list[Finding]) -> None:
    command = effective.data.get("commands", {}).get("check")
    if not command:
        findings.append(Finding("warning", "check.full", "No commands.check is configured"))
        return
    result = subprocess.run(command, cwd=effective.repo_root, shell=True, check=False)
    if result.returncode != 0:
        findings.append(Finding("error", "check.command", f"commands.check exited with status {result.returncode}"))
