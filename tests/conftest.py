from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def toolkit_root() -> Path:
    return Path(__file__).resolve().parents[1]


def write_project_config(repo: Path, content: str) -> Path:
    path = repo / ".agent/config.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path
