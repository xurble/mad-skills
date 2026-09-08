from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from mad_skills.cli import main
from mad_skills.errors import MadSkillsError
from mad_skills.nightly import nightly_candidate, oldest_actionable
from tests.conftest import write_project_config

LABELS = {"actionable": "ready, please", "blocked": "needs decision", "in_progress": "doing", "verified": "done"}


def issue(number: int, created: str = "2026-08-01T12:00:00Z", **overrides: object) -> dict:
    return {
        "number": number,
        "created_at": created,
        "state": "open",
        "labels": [{"name": LABELS["actionable"]}],
        "html_url": f"https://github.com/example/project/issues/{number}",
        **overrides,
    }


@pytest.fixture
def gh_project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    write_project_config(
        tmp_path,
        """project:
  type: general
  profile: normal
github:
  use_issues: true
  labels:
    actionable: 'ready, please'
    blocked: needs decision
    in_progress: doing
    verified: done
""",
    )
    executable_dir = tmp_path / "bin"
    executable_dir.mkdir()
    executable = executable_dir / "gh"
    executable.write_text(
        f"#!{sys.executable}\n"
        """import json, os, sys
from pathlib import Path
args = sys.argv[1:]
with Path(os.environ['NIGHTLY_GH_LOG']).open('a') as log:
    log.write(json.dumps(args) + '\\n')
if args == ['auth', 'status']:
    sys.exit(int(os.environ.get('NIGHTLY_AUTH_EXIT', '0')))
if os.environ.get('NIGHTLY_GH_FAIL'):
    print('test permission denied', file=sys.stderr)
    sys.exit(1)
if args[:2] == ['pr', 'list']:
    print(os.environ.get('NIGHTLY_PRS', '[]'))
elif args[0] == 'api':
    print(os.environ.get('NIGHTLY_ISSUES', '[[]]'))
else:
    sys.exit('unexpected gh write or command: ' + repr(args))
""",
        encoding="utf-8",
    )
    executable.chmod(0o755)
    monkeypatch.setenv("PATH", f"{executable_dir}{os.pathsep}{os.environ.get('PATH', '')}")
    monkeypatch.setenv("NIGHTLY_GH_LOG", str(tmp_path / "calls.jsonl"))
    return tmp_path


def test_selection_uses_creation_time_then_number_across_all_pages() -> None:
    later = [issue(number, "2026-09-01T00:00:00Z") for number in range(1, 151)]
    result = oldest_actionable(
        [later[:100], later[100:], [issue(400), issue(300), issue(200, "2026-08-01T13:00:00+01:00")]],
        LABELS,
    )
    assert result == {"number": 200, "url": issue(200)["html_url"], "created_at": "2026-08-01T13:00:00+01:00"}


@pytest.mark.parametrize("excluded_label", ["blocked", "in_progress"])
def test_excludes_workflow_states_even_when_also_actionable(excluded_label: str) -> None:
    excluded = issue(1, labels=[{"name": LABELS["actionable"]}, {"name": LABELS[excluded_label]}])
    assert oldest_actionable([[excluded, issue(2)]], LABELS)["number"] == 2


def test_excludes_closed_issues_prs_and_other_labels_without_mutating_inputs() -> None:
    pages = [[issue(1, state="closed"), issue(2, pull_request={}), issue(3, labels=[{"name": "enhancement"}])]]
    before = json.dumps(pages)
    assert oldest_actionable(pages, LABELS) is None
    assert json.dumps(pages) == before


@pytest.mark.parametrize("bad", [None, {}, [None], [[None]], [[issue(1, created_at="invalid")]],
                                 [[issue(1, created_at="2026-01-01")]], [[issue(True)]]])
def test_malformed_issue_data_fails_closed(bad: object) -> None:
    with pytest.raises(MadSkillsError, match="Unexpected response"):
        oldest_actionable(bad, LABELS)


@pytest.mark.parametrize("author,draft", [("person", False), ("dependabot[bot]", True), ("person", True)])
def test_any_open_pr_skips_before_reading_issues(
    gh_project: Path, monkeypatch: pytest.MonkeyPatch, author: str, draft: bool
) -> None:
    monkeypatch.setenv("NIGHTLY_PRS", json.dumps([{"number": 1, "author": author, "isDraft": draft}]))
    monkeypatch.setenv("NIGHTLY_ISSUES", "this must not be read")
    assert nightly_candidate(gh_project) == {"status": "skip", "reason": "open_pr", "issue": None}
    calls = [json.loads(line) for line in (gh_project / "calls.jsonl").read_text().splitlines()]
    assert calls == [["auth", "status"], ["pr", "list", "--state", "open", "--limit", "1", "--json", "number,url"]]


def test_cli_returns_one_candidate_from_paginated_custom_labels(
    gh_project: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    monkeypatch.setenv("NIGHTLY_ISSUES", json.dumps([[issue(8)], [issue(7)]]))
    assert main(["nightly-candidate", str(gh_project)]) == 0
    assert json.loads(capsys.readouterr().out)["issue"]["number"] == 7
    calls = [json.loads(line) for line in (gh_project / "calls.jsonl").read_text().splitlines()]
    assert len(calls) == 3
    assert calls[-1] == [
        "api", "--method", "GET", "repos/{owner}/{repo}/issues",
        "-f", "state=open", "-f", "sort=created", "-f", "direction=asc",
        "-F", "per_page=100", "--paginate", "--slurp",
    ]


def test_no_eligible_issue_is_a_successful_skip(gh_project: Path) -> None:
    assert nightly_candidate(gh_project) == {"status": "skip", "reason": "no_actionable_issue", "issue": None}


@pytest.mark.parametrize("env,value", [("NIGHTLY_GH_FAIL", "1"), ("NIGHTLY_PRS", "null"),
                                       ("NIGHTLY_PRS", "invalid"), ("NIGHTLY_ISSUES", "{}"),
                                       ("NIGHTLY_AUTH_EXIT", "1")])
def test_cli_read_failures_return_error_not_a_skip_or_second_attempt(
    gh_project: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture, env: str, value: str
) -> None:
    monkeypatch.setenv(env, value)
    assert main(["nightly-candidate", str(gh_project)]) == 2
    output = capsys.readouterr()
    assert output.out == ""
    assert output.err.startswith("ERROR:")


@pytest.mark.parametrize("config", ["project: {type: general}", "github: {use_issues: false}",
                                    "github: {use_issues: true, labels: {blocked: agent-actionable}}",
                                    "github: {use_issues: true, labels: {verified: ' '}}"])
def test_missing_or_conflicting_configuration_stops_before_gh(
    gh_project: Path, config: str
) -> None:
    write_project_config(gh_project, config)
    with pytest.raises(MadSkillsError):
        nightly_candidate(gh_project)
    assert not (gh_project / "calls.jsonl").exists()


def test_unconfigured_project_does_not_opt_in(tmp_path: Path) -> None:
    with pytest.raises(MadSkillsError, match="requires project configuration"):
        nightly_candidate(tmp_path)
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("failure", [OSError("unavailable"), subprocess.TimeoutExpired("gh", 120)])
def test_process_failures_are_actionable(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, failure: Exception) -> None:
    from mad_skills.nightly import _read_gh

    def fail(*args: object, **kwargs: object) -> None:
        raise failure

    monkeypatch.setattr(subprocess, "run", fail)
    with pytest.raises(MadSkillsError, match="Cannot read nightly candidates"):
        _read_gh(tmp_path, ["pr", "list"])
