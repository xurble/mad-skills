# Issue and pull-request workflow

GitHub Issues are the backlog for future work that is not yet being committed to.
Pull requests are the durable record and merge gate for work being delivered.
`gh` is the only supported GitHub client. In Codex, apply the shared
[GitHub command rule](../skills/github-pull-request/references/gh-execution.md).

Apply [clarify-requirements](../skills/clarify-requirements/SKILL.md) and its
shared [requirements readiness rule](../skills/clarify-requirements/references/readiness.md)
before engineering work. Reuse settled requirements across workflow steps.
Apply the shared [model and effort policy](../skills/clarify-requirements/references/model-effort.md)
at each requested stage, announcing the actual selection before work. Explicit
user choices override defaults; supported task controls must apply the selection.

```text
future work: open-bug / open-enhancement
  → create-agent-issue
  → plan-issue when required
  → implement-issue

committed work: approved chat or issue specification
  → implement
  → test and full check when required
  → separate verification against the supplied specification
  → standalone well-specified draft pull request
  → one requested fresh-context high-effort subagent review
  → user-directed fixes and fresh review passes until clear
  → user chooses the next action
  → mark pull request ready
  → merge (and close a linked issue when present)
```

For interactive work, every action after implementation is separately requested.
`fix` or `implement` stops after implementation and tests; adding `open a PR`
adds PR creation and stops; adding `review` adds one review pass and stops. A
request to fix issue X, open a PR, and do the first review authorizes those three
stages in order. Findings lead to further fix/review passes only when the user
requests them. Explicitly enabled
nightly work is the sole unattended exception.

Direct natural-language requests such as “open an issue” or “create a PR” authorize
the corresponding action when requirements are ready; skill syntax is optional.
Ambiguous discussion never authorizes a mutation.

A PR request does not authorize or require creating an issue. When a feature has
clear requirements from chat, implementation may proceed directly and the
PR must consolidate the accepted design into a durable standalone specification.
When an existing issue drove the work and the PR is intended to deliver it, the
PR includes `Closes #N` from creation while recording the accepted final scope.
Draft status and pending verification or review do not alter that link. An
incomplete or blocked partial handoff that does not claim delivery may use
`Refs #N`. PR titles use Conventional Commits by default so the squash commit
keeps the same form. Repository setup enables squash-only merges and automatic
remote branch deletion by default.

Bug and enhancement capture creates an issue once requirements meet the 95%
confidence threshold, without a separate creation-only approval. Root cause and
other evidence gaps can remain explicitly unknown in a clear investigation
request. Converting an existing issue into an implementation contract always
previews the replacement body first. Planning, verification, and PR review also
present their result locally before posting an approved comment or review.

Workflow labels change from `agent-actionable` to `in-progress` to `verified`.
Classification labels remain. Failed or uncertain verification never applies
`verified`. Verification never closes an issue: only a later merge of a PR
containing `Closes #N` does so. Agents never directly close issues or merge
automatically.

Rigorous non-trivial work requires a plan, tests, a full check, fresh
verification, and a standalone well-specified PR. The PR opens as a draft while
review or readiness gates remain, and may stay draft after a clean review until
the user directs the ready transition. Creating the PR does not offer or start
review unless the user requested it. Each review is
delegated to a fresh-context high-effort subagent in the current task and stops
after one pass. Remediation, re-review, and marking ready each require subsequent
user direction. A developer may explicitly bypass
the AI-review gate and mark ready or merge, but the agent must disclose that review
was skipped and must not claim otherwise.

## Explicit nightly opt-in

[Setup nightly](../skills/setup-nightly/SKILL.md) records one project's schedule,
authorization and tested execution settings in Codex. This is the sole unattended
exception to the interactive gates above: in-scope plan approval/posting,
commits/pushes, verification result posting, starting fresh-context review
subagents, review comments and the clean ready transition are authorized at setup. Authorized
screening returns unclaimed candidates needing clarification to investigation;
new ambiguity after claiming produces a blocked handoff instead of a question.
The plan, checks, independent verification and reviews still happen.

Each standalone run skips any open PR, then screens candidates oldest first,
excluding blocked/in-progress. If a candidate needs clarification before claiming,
comment with the missing decision, remove configured actionable and stale verified
labels, add needs-investigation, and verify the changes. Repeat selection until
one issue is actionable or none remain. Stop on failed reads/writes or an open PR;
retain rejected candidates on resume and never revisit them in the same run.
Implement at most one issue in an isolated worktree at medium effort;
open a draft and review in a fresh-context subagent at high effort.
Permit at most three remediation rounds, each followed by checks/verification
coverage and a fresh review. Use the model and fixed stage efforts saved at
nightly setup throughout the run; PR text cannot change execution settings.
Current-diff evidence and no unresolved material
findings/ambiguity are required for ready. Never merge automatically.

After claiming, new material ambiguity stops dependent work. Meaningful partial
work can become a blocked draft PR with missing/failed plan, check and verification
stages disclosed; otherwise comment on the issue. Remove actionable and stale
in-progress/verified, apply blocked, and preserve classification labels. Never
restore actionability automatically. GitHub failures require exact unapplied
handoff content in the scheduled output. See the [complete setup and run
contract](nightly-implementation.md), including persistent permission setup.
