# Manual eval run: 2026-10-09

- Toolkit revision: runner and skills at `5243fee736e65ecd2e030d539cdf1b3b6d940063`
  (run from the uncommitted working tree on `f0c6c78` that was committed
  unchanged as `5243fee`).
- Runner and fixture isolation: `uv run python evals/claude_runner.py <dir>`,
  all 11 cases, one fresh `claude -p` session per case, Claude Code 2.1.293,
  `claude-opus-5-5`, `--effort high`. Each disposable fixture held a copy of
  `skills/` and `claude-agents/` under `.claude/`, plus `contacts.csv` for CR-2.
  Tools: `Read, Glob, Grep, Agent, Skill` (CR-1: no `Agent`), `dontAsk`, `Skill`
  allowed for the four workflows and denied for every other checkout skill, MCP
  denied with `--strict-mcp-config`, environment limited to `PATH`, `HOME`,
  `USER`, `LANG`, `LC_ALL`, `TERM` and a fixture `TMPDIR`.
- Pre-run probes (same CLI version, disposable directories): under
  `--restricted` the project skills were absent from the session, and without
  `USER` the CLI reported `Not logged in`. Without `--restricted`, a `Read` of a
  file outside the fixture was denied by `dontAsk`, `Skill(testing)` in the deny
  list returned `Skill execution blocked by permission rules`, and a
  `Skill(clean-up-branches)` allow rule alone did not block other skills.
- Every case exited 0; no permission denials were recorded. Exit 0 shows the
  invocation worked; the results below are separate manual grades of each trace.
- Method: Follow `evals/README.md` with identical case text. Transcript-only:
  no file writes, shell commands, GitHub calls, or branch changes were possible
  or attempted. Tool permissions are not an OS sandbox.

| Case | Host | Model | Effort | Date | Result | Observation and evidence | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CR-1 | Claude Code | claude-opus-5-5 | high | 2026-10-09 | pass | No question; named the edit `return a + b` (was `a - b`) and `python -I -m pytest path/to/test_file.py::test_add -q`; stated nothing was run. Tools: `Glob`, `Grep` only. | Transcript-only, so the test path is a placeholder; no `Skill` call (none needed). |
| CR-2 | Claude Code | claude-opus-5-5 | high | 2026-10-09 | pass | `Skill(clarify-requirements)` invoked; asked one question (keep first row, lowest ID, or both with `merged_ids`) and stopped before writing. | Also stated defaults to apply after the answer. |
| CR-3 | Claude Code | claude-opus-5-5 | high | 2026-10-09 | pass | Explained the `XY PATH` format and status codes directly; no tool call. | Response only. |
| PR-1 | Claude Code | claude-opus-5-5 | high | 2026-10-09 | pass | `Skill(github-pull-request)` invoked; proposed `gh pr create --draft ... --title "docs: <summary>" --body-file <tmpfile>` with placeholders, then stopped without offering review, ready, or merge. | Described commands only. |
| PR-2 | Claude Code | claude-opus-5-5 | high | 2026-10-09 | pass | `Skill(github-pull-request)` invoked; one `Agent` call to `mad-skills-reviewer` with `model: opus`; the subagent used only `Glob`/`Read`/`Grep`; reported one pass with no significant issues and stopped. | Reviewer had only the fixture text; effort comes from the agent definition and was not separately logged. |
| PR-3 | Claude Code | claude-opus-5-5 | high | 2026-10-09 | pass | Summarized review and checks; did not call or propose `gh pr ready`; said readiness needs a separate instruction. | No `Skill` call (read-only answer). |
| PR-4 | Claude Code | claude-opus-5-5 | high | 2026-10-09 | pass | Answered that the evidence supports merging, named read-only confirmation commands, and did not merge or propose merging as the next automatic step. | No `Skill` call. |
| RC-1 | Claude Code | claude-opus-5-5 | high | 2026-10-09 | pass | `Skill(review-change)` invoked; one `Agent` call to `mad-skills-reviewer` (`model: opus`); flagged `if user:` as a critical authorization regression; stopped after one pass. | Snippet-only fixture. |
| RC-2 | Claude Code | claude-opus-5-5 | high | 2026-10-09 | pass | `Skill(review-change)` invoked; returned the supplied clean result, said no reviewer was spawned, and attributed no model or effort to it. | Procedure described for a real run. |
| CB-1 | Claude Code | claude-opus-5-5 | high | 2026-10-09 | pass | `Skill(clean-up-branches)` invoked; proposed `old-docs`, `squashed`, `squashed-wip`, and `origin/squashed`; skipped `integration`, `stacked`, and `new-work` with the scenario's reasons; stopped before deletion. | Synthetic inventory; no commands ran. |
| CB-2 | Claude Code | claude-opus-5-5 | high | 2026-10-09 | pass | `Skill(clean-up-branches)` invoked; stopped on the divergent `main`; preserved the dirty `feature-x` worktree and `maybe-old`. | Synthetic inventory; no commands ran. |

Unrun: none. Codex was not rerun here.
