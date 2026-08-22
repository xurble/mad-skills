from __future__ import annotations

from pathlib import Path

from mad_skills.checker import check_project
from mad_skills.installer import install
from tests.conftest import write_project_config


def configure_ready_project(repo: Path) -> None:
    write_project_config(
        repo,
        """project:
  type: general
  profile: normal
commands:
  check: ./scripts/check
github:
  use_issues: false
""",
    )
    (repo / "AGENTS.md").write_text("# Project\n", encoding="utf-8")
    (repo / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
    scripts = repo / "scripts"
    scripts.mkdir()
    check = scripts / "check"
    check.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    check.chmod(0o755)


def test_ready_project(tmp_path: Path, toolkit_root: Path) -> None:
    repo = tmp_path / "repo"
    home = tmp_path / "home"
    repo.mkdir()
    configure_ready_project(repo)
    install("all", home=home, toolkit_root=toolkit_root)

    result = check_project(repo, home=home, toolkit_root=toolkit_root, check_github=False)

    assert result.status == "READY"
    assert result.findings == ()


def test_full_check_executes_canonical_command(tmp_path: Path, toolkit_root: Path) -> None:
    repo = tmp_path / "repo"
    home = tmp_path / "home"
    repo.mkdir()
    configure_ready_project(repo)
    install("all", home=home, toolkit_root=toolkit_root)

    result = check_project(
        repo,
        full=True,
        home=home,
        toolkit_root=toolkit_root,
        check_github=False,
    )

    assert result.status == "READY"


def test_unconfigured_project_is_ready_with_warning(tmp_path: Path, toolkit_root: Path) -> None:
    home = tmp_path / "home"
    repo = tmp_path / "repo"
    repo.mkdir()
    install("all", home=home, toolkit_root=toolkit_root)

    result = check_project(repo, home=home, toolkit_root=toolkit_root, check_github=False)

    assert result.status == "READY WITH WARNINGS"
    assert any(finding.code == "config.missing" for finding in result.findings)


def test_missing_command_is_not_ready(tmp_path: Path, toolkit_root: Path) -> None:
    home = tmp_path / "home"
    repo = tmp_path / "repo"
    repo.mkdir()
    configure_ready_project(repo)
    (repo / "scripts/check").unlink()
    install("all", home=home, toolkit_root=toolkit_root)

    result = check_project(repo, home=home, toolkit_root=toolkit_root, check_github=False)

    assert result.status == "NOT READY"
    assert any(finding.code == "command.check" for finding in result.findings)
