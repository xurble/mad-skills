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
using `6420a30` plus the uncommitted issue-17 diff and the
[manual scenario protocol](../README.md). All 11 named scenarios passed after
the CB-1 fixture clarification:

| Post-edit Codex scenarios | Result | Observation |
| --- | --- | --- |
| CR-1–CR-3 | 3/3 pass | The implementation, material-question, and read-only boundaries matched their contracts. |
| PR-1–PR-4 | 4/4 pass | The action boundaries held; PR-2 used an actual fresh reviewer. |
| RC-1–RC-2 | 2/2 pass | Both cases used actual fresh reviewers and stopped at the requested review boundary. |
| CB-1–CB-2 | 2/2 pass | Exact-tip cleanup decisions matched the clarified CB-1 fixture and the dirty/divergent CB-2 fixture. |

The first CB-1 attempt did not satisfy the expected deletion set under a strict
reading: the fixture did not expressly identify `squashed` as the merged PR's
recorded head branch or state that no PR remained open for it. This was
investigated as missing fixture evidence. The fixture now states those
already-intended facts explicitly; it does not change the cleanup policy or
expected behavior. The original result is superseded by the passing rerun, not
counted as a post-edit policy regression.

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
