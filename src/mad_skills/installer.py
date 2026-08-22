from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from mad_skills.errors import MadSkillsError
from mad_skills.paths import find_toolkit_root

TARGET_PATHS = {
    "codex": Path(".agents/skills"),
    "claude": Path(".claude/skills"),
}


@dataclass(frozen=True)
class LinkAction:
    source: Path
    target: Path
    state: str


def skill_directories(toolkit_root: Path | None = None) -> list[Path]:
    root = toolkit_root or find_toolkit_root()
    return sorted(path for path in (root / "skills").iterdir() if path.is_dir() and (path / "SKILL.md").is_file())


def target_names(target: str) -> list[str]:
    if target == "all":
        return ["codex", "claude"]
    if target not in TARGET_PATHS:
        raise MadSkillsError(f"Unknown install target: {target}")
    return [target]


def plan_install(
    target: str,
    *,
    home: Path | None = None,
    toolkit_root: Path | None = None,
) -> list[LinkAction]:
    actual_home = (home or Path.home()).expanduser().resolve()
    actions: list[LinkAction] = []
    conflicts: list[Path] = []
    for target_name in target_names(target):
        destination = actual_home / TARGET_PATHS[target_name]
        for candidate in (destination.parent, destination):
            if candidate.exists() and not candidate.is_dir():
                conflicts.append(candidate)
        for source in skill_directories(toolkit_root):
            link = destination / source.name
            if link.is_symlink():
                try:
                    resolved = link.resolve(strict=True)
                except OSError:
                    resolved = link.resolve(strict=False)
                if resolved == source.resolve():
                    actions.append(LinkAction(source, link, "current"))
                else:
                    conflicts.append(link)
            elif link.exists():
                conflicts.append(link)
            else:
                actions.append(LinkAction(source, link, "create"))
    if conflicts:
        rendered = "\n  - ".join(str(path) for path in conflicts)
        raise MadSkillsError(
            "Installation stopped; these unmanaged paths would conflict:\n"
            f"  - {rendered}\n"
            "Move or remove them explicitly, then rerun the installer."
        )
    return actions


def install(
    target: str,
    *,
    home: Path | None = None,
    toolkit_root: Path | None = None,
) -> list[LinkAction]:
    actions = plan_install(target, home=home, toolkit_root=toolkit_root)
    for action in actions:
        if action.state == "current":
            continue
        action.target.parent.mkdir(parents=True, exist_ok=True)
        action.target.symlink_to(action.source.resolve(), target_is_directory=True)
    return actions
