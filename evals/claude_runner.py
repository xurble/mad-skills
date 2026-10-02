"""Run the manual scenarios on Claude Code, one fresh `claude -p` session per case.

Usage: uv run python evals/claude_runner.py OUTPUT_DIR [CASE_ID ...]

Each case runs in a disposable directory under OUTPUT_DIR with a copy of this
checkout's skills and Claude agents. Every case is transcript-only and has
read-only tools. Traces are for manual grading. This is tool-permission
containment, not an OS sandbox.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "evals" / "scenarios"
ORDER = ("clarify-requirements", "github-pull-request", "review-change", "clean-up-branches")
MODEL = "claude-opus-5-5"
NOTICE = (
    "This is an advisory behavioral eval. The supplied fixture and any transcript are synthetic. "
    "Describe any edit or test you would perform, but do not execute it. "
    "You must stop before any external write or destructive command. "
    "Act as you normally would with the skills available to you.\n\n"
)
READ_ONLY_TOOLS = ("Read", "Glob", "Grep", "Agent")
TRANSCRIPT_DENIED = ("Bash", "Edit", "Write", "NotebookEdit", "WebFetch", "WebSearch", "mcp__*")
SAFE_ENV_KEYS = ("PATH", "HOME", "LANG", "LC_ALL", "TERM")


def parse_cases(scenarios: Path = SCENARIOS) -> list[tuple[str, str, str, str]]:
    cases = []
    for name in ORDER:
        head, *sections = re.split(r"^## ", (scenarios / f"{name}.md").read_text(encoding="utf-8"), flags=re.M)
        preamble = "\n".join(head.splitlines()[1:]).strip()
        for section in sections:
            title, body = section.split("\n", 1)
            fixture = re.search(r"\*\*Fixture:\*\*(.*?)\n\*\*Prompt:\*\*", body, re.S)
            prompt = re.search(r"\*\*Prompt:\*\*(.*?)\n\*\*Expected:\*\*", body, re.S)
            if not (fixture and prompt):
                raise ValueError(f"{name}: {title} lacks Fixture or Prompt")
            cases.append((title.split(" ")[0], preamble, fixture.group(1).strip(), prompt.group(1).strip()))
    return cases


def build_fixture(case_id: str, work: Path) -> None:
    (work / ".claude").mkdir(parents=True)
    shutil.copytree(ROOT / "skills", work / ".claude" / "skills")
    shutil.copytree(ROOT / "claude-agents", work / ".claude" / "agents")
    if case_id == "CR-2":
        (work / "contacts.csv").write_text(
            "id,email\n101,alex@example.invalid\n102,alex@example.invalid\n103,sam@example.invalid\n"
        )


def build_command(case_id: str, text: str) -> list[str]:
    return [
        "claude", "-p", text,
        "--model", MODEL,
        "--effort", "high",
        "--restricted",
        "--permission-mode", "dontAsk",
        "--setting-sources", "project",
        "--output-format", "stream-json", "--verbose",
        "--tools", ",".join(READ_ONLY_TOOLS),
        "--allowedTools", *READ_ONLY_TOOLS,
        "--disallowedTools", *TRANSCRIPT_DENIED,
    ]  # fmt: skip


def build_env(work: Path, host_env: dict[str, str]) -> dict[str, str]:
    env = {key: host_env[key] for key in SAFE_ENV_KEYS if key in host_env}
    env["TMPDIR"] = str(work / "tmp")
    return env


def run_case(case: tuple[str, str, str, str], output: Path) -> tuple[str, int]:
    case_id, preamble, fixture, prompt = case
    case_dir = output / case_id
    work = case_dir / "work"
    build_fixture(case_id, work)
    (work / "tmp").mkdir()
    text = f"{NOTICE}{preamble}\n\nFixture: {fixture}\n\nPrompt: {prompt}\n"
    (case_dir / "prompt.txt").write_text(text)
    command = build_command(case_id, text)
    env = build_env(work, dict(os.environ))
    with open(case_dir / "trace.jsonl", "w") as trace:
        result = subprocess.run(
            command, cwd=work, env=env, stdin=subprocess.DEVNULL, stdout=trace, stderr=subprocess.STDOUT, timeout=1800
        )
    return case_id, result.returncode


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    output = Path(argv[0]).resolve()
    selected = set(argv[1:])
    cases = [case for case in parse_cases() if not selected or case[0] in selected]
    if output.exists() and any(output.iterdir()):
        print(f"{output} is not empty; choose a new output directory")
        return 2
    with ThreadPoolExecutor(max_workers=6) as pool:
        for case_id, code in pool.map(lambda case: run_case(case, output), cases):
            print(f"{case_id}: exit {code}; trace {output / case_id / 'trace.jsonl'}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
