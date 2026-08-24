---
name: verify-issue
description: Independently verify a completed change against its PR, GitHub issue, or supplied acceptance criteria in a separate fresh task. Use when asked to check acceptance criteria, validate an implementation, or determine whether a change is ready after implementation.
---

# Verify a change

Run this workflow in a task separate from implementation.

In Codex, run every `gh` command—and any `mad-skills` command that reaches
GitHub—outside the sandbox with escalation from the outset.

1. Load policy with `mad-skills context --format json`. Offer `mad-skills init`
   when configuration is absent; use `light` for this task if declined. Require
   authenticated `gh` for a GitHub issue or PR.
2. Read the authoritative contract, `AGENTS.md`, decisions, final diff, relevant
   code, and available test results. For issue-driven work, read the issue and
   material comments. For an existing PR, use its standalone specification as the
   accepted final scope. When there is no GitHub artifact, require the user to
   supply the accepted specification and acceptance criteria explicitly in this
   fresh task. Reconstruct the contract independently; do not rely on the
   implementation conversation.
3. For every acceptance criterion classify `verified`, `failed`, or `unable to
   verify`, citing code, test, or observed-behavior evidence.
4. Check missing behavior, regressions, edge cases, scope creep, debug artifacts,
   migration/data safety, security boundaries, and test adequacy proportionate to
   risk. Run safe focused checks; run `mad-skills check --full` when policy requires.
5. Do not repeat implementation claims as evidence and do not edit code.
6. Present the complete verification result before changing GitHub. When a source
   issue or PR exists, comment the result there only after approval. Only for an
   issue-driven change whose material criteria all pass, remove `in-progress` and
   apply `verified`; otherwise do not change issue labels. For issue-less work
   verified before PR creation, return the result locally for the PR handoff.
7. Never merge a PR or close an issue. Issue closure occurs only through a merged
   linked PR or the user's explicit request.
