# One-time Codex context-overhead audit — issue #17

## Method and inventory

The pre-edit snapshot was taken from the clean checkout at `6420a30` on
2026-10-02. The post-edit snapshot uses the same checkout with this uncommitted
change. For each task type below, count the UTF-8 bytes and whitespace-delimited
words in the named `SKILL.md` bodies and references once each, using `wc -w -c`.
The post-edit bundle adds `readiness.md` and, for GitHub tasks,
`gh-execution.md`. The pre-edit bundle has their content in the skill bodies.
This counts a Codex source-text footprint, not automatically loaded prompt
context. Relative reference links are followed once. Task-specific repositories,
user prompts, tool outputs, and ambient host instructions are excluded.

| Sample task | Counted source files before | Counted source files after |
| --- | --- | --- |
| Read-only project orientation | `clarify-requirements`, `model-effort`, `understand-project` | Same, plus `readiness` |
| Implement an issue | `clarify-requirements`, `model-effort`, `implement-issue`, `git-workflow`, `testing` | Same, plus `readiness` and `gh-execution` |
| PR plus requested review | `clarify-requirements`, `model-effort`, `github-pull-request`, `review-change` | Same, plus `readiness` and `gh-execution` |
| Nightly sample (separate) | `clarify-requirements`, `model-effort`, `nightly-implement`, its `authorization` and `child-task`, `implement-issue`, `plan-issue`, `git-workflow`, `testing`, `github-pull-request`, `review-change`, `verify-issue` | Same, plus `readiness` and `gh-execution` |

`AGENTS.md` (226 words, 1,589 bytes) was inventoried separately. Relevant
Codex `agents/openai.yaml` files were also inventoried as skill discovery/UI
metadata, outside the task-body counts; their presence does not establish when
the host loads them. The repository's `mad-skills context --format json` output
was inspected: it contains resolved project configuration and skill names, with
no new policy text. CLI code, config, and context output were not changed by
this issue.

## Codex source-bundle results

| Task sample | Before words / bytes | After words / bytes | Change |
| --- | ---: | ---: | ---: |
| Read-only | 1,486 / 10,334 | 1,407 / 9,882 | −79 words / −452 bytes |
| Implementation | 2,445 / 17,422 | 2,400 / 17,250 | −45 words / −172 bytes |
| PR/review | 3,123 / 21,796 | 3,066 / 21,559 | −57 words / −237 bytes |
| Nightly, separately sampled | 8,014 / 57,680 | 7,921 / 57,317 | −93 words / −363 bytes |

The largest counted source is `nightly-implement/SKILL.md` (1,356 words before
and after), followed among these samples by `github-pull-request/SKILL.md`
(967 before). Most of their length is workflow-specific authorization,
readiness, and failure handling that this issue intentionally retains. The
shared readiness rule and Codex GitHub command rule now have one source each;
the modest net reductions reflect explicit links and retained local safeguards.

## Codex behavior and measurement limits

The [pre-edit Codex record](2026-10-01-initial.md) reports 11 passing named
scenarios, including read-only (`CR-3`), implementation (`CR-1`), and PR/review
(`PR-2`, `RC-1`, `RC-2`) behavior. Those runs used earlier revisions and synthetic
fixtures; they are the behavioral baseline.

The post-edit run was on 2026-10-02 in Codex with `gpt-6-sol` at high effort,
using base `6420a30` plus the uncommitted issue-17 diff later recorded in
`1eaff08`, and the [manual scenario protocol](../README.md). All 11 named
scenarios passed after the CB-1 fixture clarification. The table records the
initial CB-1 attempt separately so its result remains visible.

| Case | Result | Observed behavior | Tool or delegation trace and limitation |
| --- | --- | --- | --- |
| CR-1 | pass | Asked no question; proposed `return a + b` and `python -m pytest -q`, without claiming the test passed. | No edit or test ran; transcript-only proposal. |
| CR-2 | pass | Asked which duplicate or ID to retain before proceeding. | No write; synthetic data only. |
| CR-3 | pass | Directly explained compact status, the two status characters, and `??`. | No tools used; response-only observation. |
| PR-1 | pass | Proposed `gh pr create --draft --body-file …` and identified missing title, body, branch, and validation details. | No GitHub call, review, ready change, or merge. |
| PR-2 | pass | Completed one requested fresh review; reviewer found no issue. | Actual `fork_turns: none` reviewer on `gpt-6-sol` / high; no GitHub post. |
| PR-3 | pass | Summarized the supplied clean review, checks, and draft state. | No state-changing call; supplied evidence only. |
| PR-4 | pass | Said the supplied evidence indicated readiness. | No merge call; supplied evidence only. |
| RC-1 | pass | Reviewer flagged the `if user:` authorization bypass and suggested restoring the guard and testing admin versus user access. | Actual `fork_turns: none` reviewer on `gpt-6-sol` / high; one pass, no edit. |
| RC-2 | pass | Reviewer found no issue in the heading typo. | Actual `fork_turns: none` reviewer on `gpt-6-sol` / high; one pass, no state change. |
| CB-1, initial | fail, superseded | Held `squashed` because the fixture did not expressly establish its merged PR head branch or open-PR state. | Fresh attempt; no commands. The strict reading exposed missing fixture evidence. |
| CB-1, retest | pass | Proposed `git branch -d old-docs`, `git branch -D squashed`, and `git push origin --delete squashed`; preserved `new-work`. | Fresh `/root/issue17_codex_evals/cb1_retest`; read relevant skills only, with no Git or GitHub calls. |
| CB-2 | pass | Reported that `main` could not fast-forward; preserved the dirty worktree and uncertain remote branch. | No commands; synthetic refs only. |

The CB-1 fixture now explicitly states the merged PR's recorded head branch and
that no PR is open for it. These were already-intended facts; the clarification
changed neither cleanup policy nor expected behavior. The initial strict-reading
failure is superseded by the passing fresh retest, not erased or counted as a
post-edit policy regression.

These were transcript-only synthetic cases. They made no external calls or
writes and ran no destructive commands; proposed actions and fresh review
delegations demonstrate decisions at the scenario boundary, not completion of
real GitHub or branch operations. The nightly row above is a static source
bundle, not a behavioral run.

Codex did not supply per-task loaded-context or token-usage reports for these
task types before and after this edit. Actual automatic skill and reference
loading was not observable here. Word and byte counts are reproducible
source-text proxies, not token counts or measured model cost. Claude Code's
separate audit and post-edit behavioral rerun are tracked in
[issue #21](https://github.com/xurble/mad-skills/issues/21). This is a one-time
record and adds no context budget or CI gate.
