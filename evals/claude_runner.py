"""Run the manual scenarios on Claude Code, one fresh `claude -p` session per case.

Usage: uv run python evals/claude_runner.py OUTPUT_DIR [CASE_ID ...]

Each case runs in a disposable directory under OUTPUT_DIR whose `.claude/skills`
and `.claude/agents` link to this checkout. GitHub and destructive Git commands
are disallowed. Traces are written for manual grading; nothing here judges them.
"""

from __future__ import annotations

import os
import re
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
    "You must stop before any external write or destructive command. Act as you normally would "
    "with the skills available to you.\n\n"
)
DISALLOWED = (
    "Bash(gh:*)",
    "Bash(git push:*)",
    "Bash(git branch:*)",
    "Bash(git reset:*)",
    "Bash(git worktree:*)",
    "Bash(rm:*)",
)
# CR-1 is the only case whose fixture authorizes edits and a test run.
CR1_ALLOWED = ("Bash(.venv/bin/python -m pytest:*)", "Bash(python -m pytest:*)", "Bash(pytest:*)")


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
    (work / ".claude" / "skills").symlink_to(ROOT / "skills", target_is_directory=True)
    (work / ".claude" / "agents").symlink_to(ROOT / "claude-agents", target_is_directory=True)
    if case_id == "CR-1":
        (work / "calc.py").write_text("def add(a, b):\n    return a - b\n")
        (work / "test_calc.py").write_text("from calc import add\n\n\ndef test_add():\n    assert add(2, 3) == 5\n")
        (work / ".gitignore").write_text(".venv/\n.claude/\n")
        subprocess.run(["uv", "venv", "-q", ".venv"], cwd=work, check=True)
        subprocess.run(["uv", "pip", "install", "-q", "--python", ".venv", "pytest"], cwd=work, check=True)
        for command in (
            ["git", "init", "-q"],
            ["git", "add", "."],
            ["git", "-c", "user.name=Eval", "-c", "user.email=eval@example.invalid", "commit", "-qm", "fixture"],
        ):
            subprocess.run(command, cwd=work, check=True)
    elif case_id == "CR-2":
        (work / "contacts.csv").write_text(
            "id,email\n101,alex@example.invalid\n102,alex@example.invalid\n103,sam@example.invalid\n"
        )


def run_case(case: tuple[str, str, str, str], output: Path) -> tuple[str, int]:
    case_id, preamble, fixture, prompt = case
    case_dir = output / case_id
    work = case_dir / "work"
    build_fixture(case_id, work)
    text = f"{NOTICE}{preamble}\n\nFixture: {fixture}\n\nPrompt: {prompt}\n"
    (case_dir / "prompt.txt").write_text(text)
    command = [
        "claude", "-p", text,
        "--model", MODEL,
        "--effort", "high",
        "--setting-sources", "project",
        "--output-format", "stream-json", "--verbose",
        "--disallowedTools", *DISALLOWED,
    ]  # fmt: skip
    env = dict(os.environ)
    if case_id == "CR-1":
        command += ["--permission-mode", "acceptEdits", "--allowedTools", *CR1_ALLOWED]
        env["PATH"] = f"{work / '.venv' / 'bin'}{os.pathsep}{env['PATH']}"
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
