---
name: review-change
description: Review a diff, branch, commit, or GitHub pull request in a separate fresh task for material correctness, maintainability, risk, and test problems. Use only when the user directly requests review or accepts an offered rigorous PR review; do not start merely because a PR exists.
---

# Review a change

Run independently from implementation.

In Codex, run every `gh` command—and any `mad-skills` command that reaches
GitHub—outside the sandbox with escalation from the outset.

1. Load effective policy and repository guidance. Offer `mad-skills init` when
   configuration is absent; use `light` for this task if declined. For a PR,
   require authenticated `gh` and load its description, any linked issue, diff,
   and checks.
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
7. Present findings locally first. After user approval, post a PR review with
   `gh pr review --comment --body-file`; do not approve, request changes, merge,
   or otherwise change PR state without a separate explicit request.
8. Report the review cycle complete only when the current diff has no unresolved
   material findings. If fixes change the diff, require a fresh review pass before
   reporting completion. Hand the result back to the PR workflow; do not mark the
   PR ready from the review task.
