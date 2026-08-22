---
name: verify-issue
description: Independently verify a completed change against its GitHub issue in a separate fresh task. Use when asked to check acceptance criteria, validate an implementation, or determine whether an issue is ready after implementation.
---

# Verify an issue

Run this workflow in a task separate from implementation.

In Codex, run every `gh` command—and any `mad-skills` command that reaches
GitHub—outside the sandbox with escalation from the outset.

1. Load policy with `mad-skills context --format json`. Offer `mad-skills init`
   when configuration is absent; use `light` for this task if declined. Require
   authenticated `gh` for a GitHub issue.
2. Read the issue, material comments, `AGENTS.md`, decisions, final diff, relevant
   code, and available test results. Reconstruct the contract independently.
3. For every acceptance criterion classify `verified`, `failed`, or `unable to
   verify`, citing code, test, or observed-behavior evidence.
4. Check missing behavior, regressions, edge cases, scope creep, debug artifacts,
   migration/data safety, security boundaries, and test adequacy proportionate to
   risk. Run safe focused checks; run `mad-skills check --full` when policy requires.
5. Do not repeat implementation claims as evidence and do not edit code.
6. Present the complete verification result before changing GitHub. After approval:
   - if all material criteria are verified, comment the result, remove
     `in-progress`, and apply `verified`;
   - otherwise comment only the approved result and do not apply `verified`.
7. Never close the issue. Closure occurs only through a merged linked PR or the
   user's explicit request.
