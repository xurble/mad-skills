---
name: plan-issue
description: Investigate an existing GitHub issue and produce a practical implementation plan without changing code. Use when asked to plan an issue, especially before non-trivial rigorous or high-risk implementation.
---

# Plan an issue

Apply [clarify-requirements](../clarify-requirements/SKILL.md) to the task's
requirements first; reuse the established requirements for the same scope.

For explicitly enabled nightly work, apply
[standing authorization](../nightly-implement/references/authorization.md).
It approves an in-scope required plan and its issue comment without a new prompt;
still write and record the plan. Material ambiguity before claiming uses authorized
nightly clarification screening; after claiming, use the blocked handoff.
Interactive plan approval and posting behavior below remains unchanged.

In Codex, run every `gh` command—and any `mad-skills` command that reaches
GitHub—outside the sandbox with escalation from the outset.

1. Load policy with `mad-skills context --format json`; offer initialization if
   configuration is absent.
2. Require installed, authenticated `gh`. Read the issue and all material
   comments. Determine whether the desired outcome and acceptance criteria are
   actionable.
3. Read `AGENTS.md`, decisions, relevant code and tests. Inspect repository status
   but do not edit code or change issue status.
4. Identify current architecture, patterns to reuse, likely files and modules,
   data/migration/API/UI implications, test changes, risks, and open questions.
5. State the inferred task risk. Treat high risk as rigorous regardless of project
   profile. Resolve material requirements through focused questions until
   requirements confidence reaches 95% before finalizing the plan.
6. Present a sequenced plan detailed enough for a fresh implementation task but
   avoid speculative line-by-line prescriptions.
7. Show the plan locally first. After user approval, post it as a GitHub issue
   comment using `gh issue comment --body-file`; do not rewrite the issue body.
