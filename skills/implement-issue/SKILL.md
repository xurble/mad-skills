---
name: implement-issue
description: Implement an actionable GitHub issue against explicit acceptance criteria using project profile and task risk to select workflow depth. Use when the user asks to implement, fix, or build a specific issue in the current repository.
---

# Implement an issue

In Codex, run every `gh` command—and any `mad-skills` command that reaches
GitHub—outside the sandbox with escalation from the outset.

1. Load `mad-skills context --format json`. If unconfigured, ask whether to run
   `mad-skills init`; if declined, use `light` for this task.
2. Require installed, authenticated `gh`. Load the issue and comments. Stop if it
   lacks a clear outcome or material requirements remain unresolved.
3. Read `AGENTS.md`, relevant docs and decisions, repository status, current code,
   and tests before editing. Preserve unrelated work.
4. Classify risk as `low`, `normal`, or `high` and state the evidence. Ask only
   when ambiguity changes the workflow. High risk always uses rigorous safety.
5. Enforce effective policy:
   - rigorous non-trivial work needs an issue, approved written plan, PR, tests,
     full check, and later fresh verification and review;
   - normal meaningful changes normally need tests and later fresh review;
   - light work uses focused checks and a final diff inspection.
6. After confirming actionability, replace configured `actionable`/`verified`
   workflow labels with `in-progress`. Preserve `bug`, `enhancement`, and
   `high-risk` classification labels.
7. Use a focused branch when a PR is required. Use a worktree for parallel work,
   unrelated dirty changes, substantial tasks, or risky experiments; never stash
   or overwrite unrelated work silently.
8. Implement only the issue scope, follow existing patterns, and add or update
   proportionate tests. Run focused checks while iterating and `commands.check`
   before completion when required.
9. Inspect the final diff for scope, debug artifacts, secrets, migrations, and
   acceptance coverage. Do not claim checks that did not run.
10. Hand off the issue, diff, checks, risks, and remaining work. Do not self-verify
    or self-review: rigorous completion requires separate fresh tasks using
    `verify-issue` and `review-change`.
