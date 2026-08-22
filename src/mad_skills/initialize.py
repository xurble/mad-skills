from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import yaml

from mad_skills.configuration import load_yaml
from mad_skills.errors import MadSkillsError
from mad_skills.github import create_labels, missing_labels, require_gh
from mad_skills.paths import PROJECT_CONFIG, find_repo_root, find_toolkit_root

Prompt = Callable[[str], str]


@dataclass(frozen=True)
class ProjectDetection:
    project_type: str
    commands: dict[str, str]
    ios: dict[str, str] | None


@dataclass(frozen=True)
class ProposedFile:
    path: Path
    content: str


def detect_project(repo_root: Path) -> ProjectDetection:
    commands = {}
    for name in ("dev", "test", "check"):
        script = repo_root / "scripts" / name
        if script.is_file():
            commands[name] = f"./scripts/{name}"

    workspaces = sorted(repo_root.glob("*.xcworkspace"))
    projects = sorted(repo_root.glob("*.xcodeproj"))
    if workspaces or projects:
        container = workspaces[0] if workspaces else projects[0]
        key = "workspace" if workspaces else "project"
        return ProjectDetection(
            "ios",
            commands,
            {key: container.name, "scheme": container.stem},
        )
    if (repo_root / "manage.py").is_file() or any(repo_root.glob("*/settings.py")):
        return ProjectDetection("django", commands, None)
    if any((repo_root / name).is_file() for name in ("pyproject.toml", "setup.py", "requirements.txt")):
        return ProjectDetection("python", commands, None)
    return ProjectDetection("general", commands, None)


def propose_initialization(
    repo_root: Path,
    *,
    project_type: str,
    profile: str,
    use_github: bool,
    check_command: str | None = None,
    ios: dict[str, str] | None = None,
) -> list[ProposedFile]:
    config: dict = {
        "version": 1,
        "project": {"type": project_type, "profile": profile},
    }
    detected = detect_project(repo_root)
    commands = dict(detected.commands)
    if check_command:
        commands["check"] = check_command
    if commands:
        config["commands"] = commands
    config["github"] = {"use_issues": use_github}
    if project_type == "ios":
        config["ios"] = ios or detected.ios
        if not config["ios"]:
            raise MadSkillsError("iOS initialization needs a project/workspace and scheme")
    if profile == "rigorous" and "check" not in commands:
        raise MadSkillsError("A rigorous project requires --check-command or an existing scripts/check")

    proposals = [
        ProposedFile(
            repo_root / PROJECT_CONFIG,
            yaml.safe_dump(config, sort_keys=False, allow_unicode=True),
        )
    ]
    if not (repo_root / "AGENTS.md").exists():
        proposals.append(ProposedFile(repo_root / "AGENTS.md", render_agents(repo_root, project_type, commands)))
    if not (repo_root / "CLAUDE.md").exists():
        proposals.append(ProposedFile(repo_root / "CLAUDE.md", "@AGENTS.md\n"))
    return proposals


def render_agents(repo_root: Path, project_type: str, commands: dict[str, str]) -> str:
    directories = [name for name in ("app", "apps", "src", "tests", "docs", "scripts") if (repo_root / name).is_dir()]
    lines = [
        "# Repository guidance",
        "",
        "## Project",
        "",
        f"- Name: `{repo_root.name}`",
        f"- Type: `{project_type}`",
    ]
    if directories:
        lines.extend(["- Important directories: " + ", ".join(f"`{item}/`" for item in directories)])
    if commands:
        lines.extend(["", "## Commands", ""])
        lines.extend(f"- `{name}`: `{command}`" for name, command in commands.items())
    lines.extend(
        [
            "",
            "## Conventions and risky areas",
            "",
            "Add only repository-specific rules confirmed by the project. Keep reusable workflows in mad-skills.",
            "",
        ]
    )
    return "\n".join(lines)


def write_proposals(proposals: list[ProposedFile]) -> None:
    for proposal in proposals:
        proposal.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = proposal.path.with_name(f".{proposal.path.name}.mad-skills.tmp")
        temporary.write_text(proposal.content, encoding="utf-8")
        os.replace(temporary, proposal.path)


def initialize_interactive(
    start: Path | None = None,
    *,
    project_type: str | None = None,
    profile: str | None = None,
    use_github: bool | None = None,
    check_command: str | None = None,
    assume_yes: bool = False,
    prompt: Prompt = input,
) -> list[ProposedFile]:
    repo_root = find_repo_root(start)
    config_path = repo_root / PROJECT_CONFIG
    if config_path.exists():
        raise MadSkillsError(f"Project is already configured: {config_path}")
    detection = detect_project(repo_root)
    selected_type = project_type or _choose(
        prompt,
        f"Project type [general/python/django/ios] ({detection.project_type}): ",
        detection.project_type,
        {"general", "python", "django", "ios"},
        assume_yes,
    )
    suggested_profile = "normal" if selected_type in {"django", "ios"} else "light"
    selected_profile = profile or _choose(
        prompt,
        f"Profile [light/normal/rigorous] ({suggested_profile}): ",
        suggested_profile,
        {"light", "normal", "rigorous"},
        assume_yes,
    )
    github_enabled = use_github
    if github_enabled is None:
        github_enabled = False if assume_yes else _yes(prompt("Use GitHub issues? [y/N]: "))
    pending_labels = []
    if github_enabled:
        require_gh(repo_root)
        defaults = load_yaml(find_toolkit_root() / "config/defaults.yaml")
        pending_labels = missing_labels(repo_root, defaults["github"])

    proposals = propose_initialization(
        repo_root,
        project_type=selected_type,
        profile=selected_profile,
        use_github=github_enabled,
        check_command=check_command,
        ios=detection.ios,
    )
    if not assume_yes:
        print(render_preview(proposals, repo_root))
        if not _yes(prompt("Write these files? [y/N]: ")):
            raise MadSkillsError("Initialization cancelled; no files were written")
    write_proposals(proposals)

    if pending_labels and (assume_yes or _yes(prompt(f"Create {len(pending_labels)} missing labels? [y/N]: "))):
        create_labels(repo_root, pending_labels)
    return proposals


def render_preview(proposals: list[ProposedFile], repo_root: Path) -> str:
    sections = []
    for proposal in proposals:
        sections.append(f"--- {proposal.path.relative_to(repo_root)} ---\n{proposal.content.rstrip()}")
    return "\n\n".join(sections)


def _choose(
    prompt: Prompt,
    message: str,
    default: str,
    choices: set[str],
    assume_yes: bool,
) -> str:
    value = default if assume_yes else (prompt(message).strip() or default)
    if value not in choices:
        raise MadSkillsError(f"Expected one of {', '.join(sorted(choices))}; got {value!r}")
    return value


def _yes(value: str) -> bool:
    return value.strip().lower() in {"y", "yes"}
