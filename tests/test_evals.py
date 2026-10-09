from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import pytest

CASES = {
    "clarify-requirements": ("CR-1", "CR-2", "CR-3"),
    "github-pull-request": ("PR-1", "PR-2", "PR-3", "PR-4"),
    "review-change": ("RC-1", "RC-2"),
    "clean-up-branches": ("CB-1", "CB-2"),
}


def test_manual_eval_scenarios_have_observable_contract(toolkit_root: Path) -> None:
    scenarios = toolkit_root / "evals" / "scenarios"
    assert {path.stem for path in scenarios.glob("*.md")} == set(CASES)

    for skill, case_ids in CASES.items():
        text = (scenarios / f"{skill}.md").read_text(encoding="utf-8")
        for case_id in case_ids:
            section = text.split(f"## {case_id} — ", 1)[1].split("\n## ", 1)[0]
            for field in ("**Fixture:**", "**Prompt:**", "**Expected:**", "**Prohibited:**", "**Evidence:**"):
                assert field in section, (skill, case_id, field)


def test_manual_eval_protocol_and_results_do_not_claim_unrun_pass(toolkit_root: Path) -> None:
    evals = toolkit_root / "evals"
    readme = (evals / "README.md").read_text(encoding="utf-8")
    template = (evals / "results" / "TEMPLATE.md").read_text(encoding="utf-8")
    results = (evals / "results" / "2026-10-01-initial.md").read_text(encoding="utf-8")

    assert "same case text" in readme
    assert "not a CI gate" in readme
    assert "Codex or Claude Code" in readme
    assert "uncontrolled / host default" in readme
    assert "authoritative high-effort verification or review readiness gate" in readme
    assert "| Model | Effort |" in template
    rows = [line.split(" | ") for line in results.splitlines() if line.startswith("| ") and " | 2026-" in line]
    recorded = {(row[0].removeprefix("| "), row[1]): row[4] for row in rows}
    for case_ids in CASES.values():
        for case_id in case_ids:
            for host in ("Codex", "Claude Code"):
                assert recorded.get((case_id, host)) in {"pass", "fail", "unrun"}, (case_id, host)


def test_claude_runner_parses_every_case_and_links_reviewer_agent(toolkit_root: Path) -> None:
    spec = importlib.util.spec_from_file_location("claude_runner", toolkit_root / "evals" / "claude_runner.py")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)

    cases = runner.parse_cases()

    assert [case[0] for case in cases] == [case_id for ids in CASES.values() for case_id in ids]
    assert all(fixture and prompt for _, _, fixture, prompt in cases)
    workflows = list(CASES)
    other_skills = {path.name for path in (toolkit_root / "skills").iterdir() if path.is_dir()} - set(workflows)
    assert set(runner.ORDER) == set(workflows)
    assert other_skills
    for case_id, *_ in cases:
        transcript = runner.build_command(case_id, "synthetic prompt")
        assert "--restricted" not in transcript  # it hides the project skills under test
        assert "--strict-mcp-config" in transcript
        # Without --restricted, this alone keeps user hooks, plugins, skills, and settings out.
        assert transcript[transcript.index("--setting-sources") + 1] == "project"
        assert transcript[transcript.index("--model") + 1] == runner.MODEL == "claude-opus-5-5"
        assert transcript[transcript.index("--effort") + 1] == "high"
        assert transcript[transcript.index("--permission-mode") + 1] == "dontAsk"
        expected_tools = runner.CR1_READ_ONLY_TOOLS if case_id == "CR-1" else runner.READ_ONLY_TOOLS
        tools = transcript[transcript.index("--tools") + 1].split(",")
        assert tools == list(expected_tools)
        assert "Skill" in tools
        assert not {"Bash", "Edit", "Write", "NotebookEdit", "WebFetch", "WebSearch"} & set(tools)
        allowed = transcript[transcript.index("--allowedTools") + 1 : transcript.index("--disallowedTools")]
        denied = transcript[transcript.index("--disallowedTools") + 1 :]
        # Read stays out of the allowlist so dontAsk denies reads outside the fixture.
        assert allowed == [f"Skill({name})" for name in runner.ORDER]
        assert {"Bash", "Edit", "Write", "NotebookEdit", "WebFetch", "WebSearch", "mcp__*"} <= set(denied)
        assert {f"Skill({name})" for name in other_skills} <= set(denied)
        assert not {f"Skill({name})" for name in workflows} & set(denied)
        assert ("Agent" in denied) == (case_id == "CR-1")
    assert (toolkit_root / "claude-agents" / "mad-skills-reviewer.md").is_file()
    readme = (toolkit_root / "evals" / "README.md").read_text(encoding="utf-8")
    assert "evals/claude_runner.py" in readme
    assert "`mad-skills-reviewer`" in readme
    assert "all cases (including CR-1) transcript-only with read-only tools" in readme
    assert "not an executed test" in readme


def test_claude_runner_scrubs_credentials_and_cr1_setup_is_transcript_only(
    toolkit_root: Path, tmp_path: Path, monkeypatch
) -> None:
    spec = importlib.util.spec_from_file_location("claude_runner", toolkit_root / "evals" / "claude_runner.py")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)

    host_env = {
        "PATH": "/usr/bin",
        "HOME": "/Users/example",
        "GH_TOKEN": "secret",
        "ANTHROPIC_API_KEY": "secret",
        "AWS_SECRET_ACCESS_KEY": "secret",
        "CLAUDE_CODE_OAUTH_TOKEN": "secret",
    }
    host_env["USER"] = "example"
    env = runner.build_env(tmp_path, host_env)
    assert set(env) == {"PATH", "HOME", "USER", "TMPDIR"}
    assert env["PATH"] == "/usr/bin"
    assert all(key not in env for key in ("GH_TOKEN", "ANTHROPIC_API_KEY", "AWS_SECRET_ACCESS_KEY"))

    source = tmp_path / "source"
    (source / "skills").mkdir(parents=True)
    (source / "claude-agents").mkdir()
    monkeypatch.setattr(runner, "ROOT", source)

    def unexpected_execution(*args, **kwargs):
        raise AssertionError("fixture setup must not execute commands")

    monkeypatch.setattr(runner.subprocess, "run", unexpected_execution)
    work = tmp_path / "cr1"
    runner.build_fixture("CR-1", work)
    assert sorted(path.name for path in work.iterdir()) == [".claude"]
    assert not any((work / name).exists() for name in ("calc.py", "test_calc.py", ".venv", ".git"))


@pytest.mark.parametrize("requested", [("PR_2",), ("PR-1", "PR_2"), ("",)])
def test_claude_runner_rejects_unknown_cases_before_setup(
    toolkit_root: Path, tmp_path: Path, monkeypatch, capsys, requested: tuple[str, ...]
) -> None:
    spec = importlib.util.spec_from_file_location("claude_runner", toolkit_root / "evals" / "claude_runner.py")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)

    def unexpected_execution(*args, **kwargs):
        raise AssertionError("invalid cases must not start Claude or set up a fixture")

    monkeypatch.setattr(runner.subprocess, "run", unexpected_execution)
    monkeypatch.setattr(runner, "build_fixture", unexpected_execution)
    output = tmp_path / "output"
    assert runner.main([str(output), *requested]) != 0
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "unknown case ID" in captured.err
    assert repr(requested[-1]) in captured.err
    assert "Available cases:" in captured.err
    assert "PR-2" in captured.err
    assert not output.exists()


def test_claude_runner_rejects_empty_case_set(toolkit_root: Path, tmp_path: Path, monkeypatch, capsys) -> None:
    spec = importlib.util.spec_from_file_location("claude_runner", toolkit_root / "evals" / "claude_runner.py")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    monkeypatch.setattr(runner, "parse_cases", lambda: [])
    output = tmp_path / "output"

    assert runner.main([str(output)]) != 0
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "no eval cases are available" in captured.err
    assert not output.exists()


@pytest.mark.parametrize(
    ("codes", "expected_status"),
    [({"CR-1": 7}, 1), ({"CR-1": 0, "CR-2": 7, "CR-3": 0}, 1), ({"CR-1": 0, "CR-2": 0}, 0)],
)
def test_claude_runner_reports_every_case_and_propagates_failures(
    toolkit_root: Path, tmp_path: Path, monkeypatch, capsys, codes: dict[str, int], expected_status: int
) -> None:
    spec = importlib.util.spec_from_file_location("claude_runner", toolkit_root / "evals" / "claude_runner.py")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    cases = [(case_id, "", "", "") for case_id in codes]
    monkeypatch.setattr(runner, "parse_cases", lambda: cases)

    def unexpected_execution(*args, **kwargs):
        raise AssertionError("test cases must not start Claude")

    monkeypatch.setattr(runner.subprocess, "run", unexpected_execution)
    completed: set[str] = set()

    def fake_run_case(case: tuple[str, str, str, str], output: Path) -> tuple[str, int]:
        case_id = case[0]
        trace = output / case_id / "trace.jsonl"
        trace.parent.mkdir(parents=True)
        trace.write_text(f"evidence for {case_id}\n", encoding="utf-8")
        completed.add(case_id)
        return case_id, codes[case_id]

    monkeypatch.setattr(runner, "run_case", fake_run_case)
    output = tmp_path / "output"
    assert runner.main([str(output)]) == expected_status
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out.splitlines() == [
        f"{case_id}: exit {code}; trace {output / case_id / 'trace.jsonl'}" for case_id, code in codes.items()
    ]
    assert completed == set(codes)
    for case_id in codes:
        assert (output / case_id / "trace.jsonl").read_text(encoding="utf-8") == f"evidence for {case_id}\n"


@pytest.mark.parametrize(
    ("failure", "expected_code", "diagnostic"),
    [
        (subprocess.TimeoutExpired(["claude"], 1800), 124, "timed out after 1800s"),
        (FileNotFoundError(2, "No such file or directory", "claude"), 127, "could not start Claude"),
    ],
)
def test_claude_runner_records_launch_errors_and_timeouts_per_case(
    toolkit_root: Path, tmp_path: Path, monkeypatch, capsys, failure: Exception, expected_code: int, diagnostic: str
) -> None:
    spec = importlib.util.spec_from_file_location("claude_runner", toolkit_root / "evals" / "claude_runner.py")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    monkeypatch.setattr(runner, "parse_cases", lambda: [(case_id, "", "", "") for case_id in ("CR-1", "CR-2", "CR-3")])
    monkeypatch.setattr(runner, "build_fixture", lambda case_id, work: work.mkdir(parents=True))

    def fake_run(command, *, stdout, **kwargs):
        if stdout.name.endswith("CR-2/trace.jsonl"):
            raise failure
        stdout.write("ok\n")
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(runner.subprocess, "run", fake_run)
    output = tmp_path / "output"

    assert runner.main([str(output)]) == 1
    captured = capsys.readouterr()
    assert captured.out.splitlines() == [
        f"CR-1: exit 0; trace {output / 'CR-1' / 'trace.jsonl'}",
        f"CR-2: exit {expected_code}; trace {output / 'CR-2' / 'trace.jsonl'}",
        f"CR-3: exit 0; trace {output / 'CR-3' / 'trace.jsonl'}",
    ]
    assert diagnostic in (output / "CR-2" / "trace.jsonl").read_text(encoding="utf-8")
    assert (output / "CR-3" / "trace.jsonl").read_text(encoding="utf-8") == "ok\n"
