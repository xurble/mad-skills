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
    transcript = runner.build_command("PR-2", "synthetic prompt")
    assert "--restricted" in transcript
    assert transcript[transcript.index("--permission-mode") + 1] == "dontAsk"
    assert "Bash" not in transcript[transcript.index("--tools") + 1].split(",")
    assert "Bash" in transcript[transcript.index("--disallowedTools") + 1 :]
    assert "mcp__*" in transcript[transcript.index("--disallowedTools") + 1 :]
    assert (toolkit_root / "claude-agents" / "mad-skills-reviewer.md").is_file()
    readme = (toolkit_root / "evals" / "README.md").read_text(encoding="utf-8")
    assert "evals/claude_runner.py" in readme
    assert "`mad-skills-reviewer`" in readme


def test_claude_runner_scrubs_credentials_and_limits_cr1_to_fixture(toolkit_root: Path, tmp_path: Path) -> None:
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
    env = runner.build_env("PR-2", tmp_path, host_env)
    assert set(env) == {"PATH", "HOME", "TMPDIR"}
    assert env["PATH"] == "/usr/bin"
    # A Bash wrapper such as `env gh ...` cannot run in transcript cases.
    transcript = runner.build_command("PR-2", "synthetic prompt")
    assert "Bash" not in transcript[transcript.index("--tools") + 1].split(",")

    cr1 = runner.build_command("CR-1", "synthetic prompt")
    allowed = cr1[cr1.index("--allowedTools") + 1 : cr1.index("--disallowedTools")]
    assert "Edit(./calc.py)" in allowed
    assert [rule for rule in allowed if rule.startswith("Bash(")] == [
        "Bash(.venv/bin/python -m pytest test_calc.py::test_add)"
    ]
    assert "acceptEdits" not in cr1
    cr1_env = runner.build_env("CR-1", tmp_path, host_env)
    assert cr1_env["PATH"].startswith(str(tmp_path / ".venv" / "bin"))
    assert "GH_TOKEN" not in cr1_env
