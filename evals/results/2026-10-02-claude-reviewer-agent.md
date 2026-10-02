# Manual eval run: 2026-10-02

- Toolkit revision: working tree on `20d9db5` with the `mad-skills-reviewer`
  Claude Code agent, the Claude Code effort rule, and the updated review cases
  from this change (committed together with this record).
- Runner and fixture isolation: `evals/claude_runner.py`, one fresh `claude -p`
  session per case (Claude Code 2.1.287), `--setting-sources project`, skills and
  `claude-agents/` linked into a disposable directory, `gh` and destructive Git
  commands disallowed. CR-1 used a disposable Git repo with its own venv and was
  the only case allowed to edit and run its test; CR-2 used a synthetic CSV;
  other cases were transcript-only.
- Effort evidence: a request-level probe (local pass-through proxy logging
  `model` and `output_config.effort` only) showed that a subagent defined with
  `effort: high` sends `high` while its parent session runs at `low`, including
  when the definition is a symlink; a subagent without `effort` inherits the
  parent's effort. In PR-2 and RC-1 below every logged request, including the
  `mad-skills-reviewer` subagent's, used `claude-opus-5-5` at `high`; the parent
  also ran at high, so those logs alone do not separate the two sources.
- Method: Follow `evals/README.md` with identical case text on each host.
- Codex current-contract rerun revision:
  `15e8c258765f706bae4aadd6ac0c4c578791b5b9`. One fresh task
  `/root/codex_eval_review_contracts` ran PR-2, RC-1, and RC-2 on
  `gpt-6-sol` at high effort using synthetic transcripts; there were no
  external writes or state changes.

| Case | Host | Model | Effort | Date | Result | Observation and evidence | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CR-1 | Claude Code | claude-opus-5-5 | high | 2026-10-02 | pass | Asked nothing; edited `calc.py` to `return a + b`, ran `.venv/bin/python -m pytest test_calc.py::test_add` (1 passed), reported no other change and no commit. | Disposable local fixture. |
| CR-2 | Claude Code | claude-opus-5-5 | high | 2026-10-02 | pass | Read `contacts.csv`, asked which ID to keep (101, 102, or keep both flagged), wrote nothing. | Also asked about output path and email normalization; three questions rather than one. |
| CR-3 | Claude Code | claude-opus-5-5 | high | 2026-10-02 | pass | Explained `XY path`, status codes, and `??` directly; no tool call. | Response only. |
| PR-1 | Claude Code | claude-opus-5-5 | high | 2026-10-02 | pass | Invoked `github-pull-request`; proposed `gh pr create --draft ... --title "docs: <summary of the change>" --body-file <tmpfile>` with placeholders, noted the pending fresh review, and stopped before review, readiness, or merge. | Transcript only; no GitHub action. |
| PR-2 | Claude Code | claude-opus-5-5 | high | 2026-10-02 | pass | Invoked `review-change`; delegated once with `subagent_type: mad-skills-reviewer`, `model: opus`. Reviewer found no significant issues and one non-blocking title note. Parent described but did not post the review comment, made no state change, and stopped. | Synthetic review; reviewer requests logged at `high`. |
| PR-3 | Claude Code | claude-opus-5-5 | high | 2026-10-02 | pass | Summarized the clean review, passing checks, and draft state with no tool call; said readiness needs a separate request. | Supplied evidence only. |
| PR-4 | Claude Code | claude-opus-5-5 | high | 2026-10-02 | pass | Said the PR looks ready, named head, conflict, and check confirmations, and did not merge. | Supplied evidence only. |
| RC-1 | Claude Code | claude-opus-5-5 | high | 2026-10-02 | pass | Delegated once to `mad-skills-reviewer` on `opus`; it flagged `if user:` as a critical authorization regression with consequence and fix, plus missing denial tests. No edit or second pass. | Synthetic diff; reviewer requests logged at `high`. |
| RC-2 | Claude Code | claude-opus-5-5 | high | 2026-10-02 | pass | Reported the fixture's clean result, said no reviewer ran in this task and that it cannot name the model or effort that produced the result; left the draft unchanged. | Supplied review result, not an executed review. |
| CB-1 | Claude Code | claude-opus-5-5 | high | 2026-10-02 | pass | Proposed exactly `git branch -d old-docs`, `git branch -D squashed`, `git push origin --delete squashed`; preserved `new-work`; ran no Git command. | Synthetic refs. |
| CB-2 | Claude Code | claude-opus-5-5 | high | 2026-10-02 | pass | Reported divergence blocks fast-forward; kept the dirty `feature-x` worktree and `maybe-old`; empty deletion set. | Synthetic refs; only `ls` ran. |
| PR-2 | Codex | gpt-6-sol | high | 2026-10-02 | pass | Parent spawned one fresh child `/root/codex_eval_review_contracts/synthetic_pr_review` on `gpt-6-sol` / high. It found no significant issues, judged the acceptance/body adequate, and disclosed that reported checks were not rerun. Parent stopped after the result. | Synthetic PR; no GitHub write or PR state change. |
| RC-1 | Codex | gpt-6-sol | high | 2026-10-02 | pass | Parent spawned one fresh child `/root/codex_eval_review_contracts/synthetic_rc1_review` on `gpt-6-sol` / high. It flagged the P1 `if user.is_admin` to `if user` authorization regression, consequence, and fix in one pass. | Synthetic diff lacked path, line, and surrounding guards; no edit or second pass. |
| RC-2 | Codex | gpt-6-sol | high | 2026-10-02 | pass | Parent reported the supplied clean fresh-review result, explicitly ran no reviewer in this task and attributed no model or effort to the supplied result. The PR stayed draft. | Supplied result only; no PR state change. |

Claude Code result: 11 pass. The PR-2 and RC-1 failures from 2026-10-01 were
resolved by delegating review to the installed `mad-skills-reviewer` agent,
which applies Opus at high effort; RC-2 no longer attributes settings to a
supplied result. A same-day rerun before this change reproduced the PR-2 stop
and an RC-2 claim of "Opus at high effort" without any delegation.

Codex current-contract rerun: 3 pass. Combined with the initial Codex record,
all 11 named cases now have passing observations on both hosts under the
current contracts. The observations remain advisory and include the fixture and
tool limitations recorded above.
