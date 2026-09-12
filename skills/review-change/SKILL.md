---
name: review-change
description: Review a diff, branch, commit, or GitHub pull request through one fresh-context high-effort subagent pass for material correctness, maintainability, risk, and test problems. Use when review is explicitly requested or covered by trusted nightly standing authorization; not merely because a PR exists.
---

# Review a change

Apply [clarify-requirements](../clarify-requirements/SKILL.md) to the task's
requirements first; reuse the established requirements for the same scope.

Run independently from implementation. The coordinating agent must delegate the
review exactly once through supported subagent controls with no inherited
conversation and a self-contained prompt. In Codex, use `spawn_agent` with
`fork_turns: "none"`; do not use `create_thread`. On another supported host, use
its isolated-context subagent facility. Never create a user-visible task, thread,
or chat for code review, and never review in the implementation context.
If fresh-context subagent controls are unavailable, report that the requested
review cannot be run; do not silently fall back to either behavior. A subagent
explicitly delegated this review performs it directly and must not delegate again.
Use actual high effort through supported controls; if that cannot be applied,
report the limitation instead of silently substituting another effort level.

For explicitly enabled nightly work, apply
[standing authorization](../nightly-implement/references/authorization.md).
Require a new fresh-context subagent with self-contained scope, allowed GitHub
writes and actual high effort on the setup-selected/default model; never inherit
implementation history or resume an earlier reviewer. The saved opt-in accepts
starting review and posting/clean-readiness actions without another prompt.
Recheck current head,
required checks and independent verification coverage before marking ready; a
clean review alone is insufficient. Missing capabilities, unresolved findings or
ambiguity leave a draft and return a handoff. The nightly workflow is the sole
exception to the interactive stop-after-one-pass rule below.

In Codex, run every `gh` command—and any `mad-skills` command that reaches
GitHub—outside the sandbox with escalation from the outset.

1. Load effective policy and repository guidance. Offer `mad-skills init` when
   configuration is absent; use `light` for this task if declined. Determine the
   reviewed ref, then use authenticated `gh` to check whether its branch is the
   head of an open PR. If so, treat that PR as the review target and load its
   description, any linked issue, diff, existing review comments, and checks.
2. Inspect relevant surrounding code and tests; do not review the diff in isolation.
3. Prioritize correctness, data loss, security, compatibility, architectural
   inconsistency, unnecessary complexity, maintainability, and important missing
   tests. Ignore cosmetic preferences unless they obscure a material problem.
4. Require evidence for every finding. Include the affected path and tight line
   range, consequence, triggering conditions, and a practical fix direction.
5. Order findings by severity. State residual testing gaps and assumptions.
   “No significant issues found” is valid; never manufacture criticism.
   When policy requires a well-specified PR, report a title or body that is not a
   standalone change contract as a merge-blocking workflow gap.
6. Do not edit code as part of review.
7. If the reviewed branch has an open PR and the review scope meets the 95%
   confidence threshold, the request to review authorizes posting the feedback
   there without another approval step. Post actionable findings as inline review
   comments when they can be anchored to the current diff, and post
   any remaining findings, assumptions, testing gaps, or no-findings result in a
   PR review comment. Also present the result locally and return the PR URL. If no
   open PR exists, present the feedback locally only. Do not approve, request
   changes, merge, mark ready, or otherwise change PR state during interactive
   review without a separate explicit request.
8. For interactive work, end after this single review pass whether it finds issues
   or not. Do not edit or remediate code, start another review, mark the PR ready,
   or take a suggested next action. Return control to the user. For explicitly
   enabled nightly work only, return the findings to `nightly-implement`; its
   standing authorization may drive bounded remediation, another fresh review,
   and the clean transition to ready.
