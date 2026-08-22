# Issue workflow

GitHub is the durable record for tracked work and `gh` is the only supported
GitHub client.

```text
open-bug / open-enhancement
  → create-agent-issue
  → plan-issue when required
  → implement-issue
  → separate verify-issue
  → separate review-change
  → pull request
  → merge closes the linked issue
```

Direct natural-language requests such as “open an issue” or “create a PR” authorize
the corresponding action; skill syntax is optional. Ambiguous discussion never
authorizes a mutation.

Bug and enhancement capture creates an issue immediately when facts are sufficient.
Converting an existing issue into an implementation contract always previews the
replacement body first. Planning, verification, and PR review also present their
result locally before posting an approved comment or review.

Workflow labels change from `agent-actionable` to `in-progress` to `verified`.
Classification labels remain. Failed or uncertain verification never applies
`verified`. Verification never closes an issue: only a merged PR containing
`Closes #N` or an explicit user request does so.

Rigorous non-trivial work requires an issue, approved plan, tests, PR, full check,
fresh verification, and fresh review. High-risk work uses these safety expectations
in every profile. Fresh work means a separate Codex or Claude task, not the
implementation conversation.

