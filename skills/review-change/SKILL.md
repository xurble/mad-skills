---
name: review-change
description: Review a diff, branch, commit, or GitHub pull request in a separate fresh task for material correctness, maintainability, risk, and test problems. Use when asked for code review or when rigorous policy requires independent review.
---

# Review a change

Run independently from implementation.

1. Load effective policy and repository guidance. Offer `mad-skills init` when
   configuration is absent; use `light` for this task if declined. For a PR,
   require authenticated `gh` and load its issue, description, diff, and checks.
2. Inspect relevant surrounding code and tests; do not review the diff in isolation.
3. Prioritize correctness, data loss, security, compatibility, architectural
   inconsistency, unnecessary complexity, maintainability, and important missing
   tests. Ignore cosmetic preferences unless they obscure a material problem.
4. Require evidence for every finding. Include the affected path and tight line
   range, consequence, triggering conditions, and a practical fix direction.
5. Order findings by severity. State residual testing gaps and assumptions.
   “No significant issues found” is valid; never manufacture criticism.
6. Do not edit code as part of review.
7. Present findings locally first. After user approval, post a PR review with
   `gh pr review --comment --body-file`; do not approve, request changes, merge,
   or otherwise change PR state without a separate explicit request.
