from __future__ import annotations

import importlib.util
from pathlib import Path

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
    for case_id, *_ in cases:
        transcript = runner.build_command(case_id, "synthetic prompt")
        assert "--restricted" in transcript
        assert transcript[transcript.index("--permission-mode") + 1] == "dontAsk"
        assert transcript[transcript.index("--tools") + 1].split(",") == list(runner.READ_ONLY_TOOLS)
        allowed = transcript[transcript.index("--allowedTools") + 1 : transcript.index("--disallowedTools")]
        denied = transcript[transcript.index("--disallowedTools") + 1 :]
        assert allowed == list(runner.READ_ONLY_TOOLS)
        assert {"Bash", "Edit", "Write", "NotebookEdit", "WebFetch", "WebSearch", "mcp__*"} <= set(denied)
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
    env = runner.build_env(tmp_path, host_env)
    assert set(env) == {"PATH", "HOME", "TMPDIR"}
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
