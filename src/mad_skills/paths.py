from __future__ import annotations

import os
import subprocess
from pathlib import Path

from mad_skills.errors import MadSkillsError

PROJECT_CONFIG = Path(".agent/config.yaml")


def find_repo_root(start: Path | None = None) -> Path:
    candidate = (start or Path.cwd()).resolve()
    if candidate.is_file():
        candidate = candidate.parent
    result = subprocess.run(
        ["git", "-C", str(candidate), "rev-parse", "--show-toplevel"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0 and result.stdout.strip():
        return Path(result.stdout.strip()).resolve()
    return candidate


def find_toolkit_root() -> Path:
    override = os.environ.get("MAD_SKILLS_HOME")
    if override:
        candidate = Path(override).expanduser().resolve()
        if _looks_like_toolkit(candidate):
            return candidate
        raise MadSkillsError(f"MAD_SKILLS_HOME is not a mad-skills checkout: {candidate}")

    for candidate in Path(__file__).resolve().parents:
        if _looks_like_toolkit(candidate):
            return candidate
    raise MadSkillsError(
        "Cannot locate the mad-skills checkout. Install it with uv in editable mode or set MAD_SKILLS_HOME."
    )


def _looks_like_toolkit(path: Path) -> bool:
    return (path / "config/defaults.yaml").is_file() and (path / "profiles").is_dir() and (path / "skills").is_dir()
