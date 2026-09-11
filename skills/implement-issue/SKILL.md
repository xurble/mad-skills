---
name: implement-issue
description: Implement an actionable GitHub issue against explicit acceptance criteria using project profile and task risk to select workflow depth. Use when the user asks to implement, fix, or build a specific issue in the current repository.
---

# Implement an issue

Apply [clarify-requirements](../clarify-requirements/SKILL.md) to the task's
requirements first; reuse the established requirements for the same scope.

For explicitly enabled nightly work, apply
[standing authorization](../nightly-implement/references/authorization.md).
It covers routine scope/plan approval, focused commits, GitHub writes, separate
verification/review, and remediation without additional prompts. Required
artifacts, checks and independent assessments still occur. Follow
`nightly-implement` for effort controls, clarification screening before claiming,
bounded review rounds and blocked/failed draft handoffs. Missing configuration or
capabilities stop the run; material ambiguity returns an unclaimed candidate to
investigation and continues authorized screening, or stops an already claimed
issue with a blocked handoff. Do not ask unattended setup/clarification questions.

In Codex, run every `gh` command—and any `mad-skills` command that reaches
GitHub—outside the sandbox with escalation from the outset.

1. Load `mad-skills context --format json`. If unconfigured, ask whether to run
   `mad-skills init`; if declined, use `light` for this task.
2. Require installed, authenticated `gh`. Load the issue and comments. Resolve
   unclear outcomes or material requirements through focused questions until
   requirements confidence reaches 95% before changing code or workflow labels.
3. Read `AGENTS.md`, relevant docs and decisions, repository status, current code,
   and tests before editing. Preserve unrelated work.
4. Classify risk as `low`, `normal`, or `high` and state the evidence. Reassess
   requirements confidence if the findings change material constraints or scope,
   and ask only if it falls below 95%. High risk always uses rigorous safety.
5. Enforce effective policy:
   - rigorous non-trivial work needs an approved written plan, tests, a full
     check, later fresh verification, and a standalone well-specified draft PR
     that offers fresh review before it is marked ready; the issue is this
     workflow's input, not a universal prerequisite;
   - normal meaningful changes normally need tests and later fresh review;
   - light work uses focused checks and a final diff inspection.
6. After determining the issue is actionable, replace configured
   `actionable`/`verified` workflow labels with `in-progress`. Preserve `bug`,
   `enhancement`, and `high-risk` classification labels.
7. Use a focused branch when a PR is required. Use a worktree for parallel work,
   unrelated dirty changes, substantial tasks, or risky experiments; never stash
   or overwrite unrelated work silently.
8. Implement only the issue scope, follow existing patterns, and add or update
   proportionate tests. Run focused checks while iterating and `commands.check`
   before completion when required.
9. Inspect the final diff for scope, debug artifacts, secrets, migrations, and
   acceptance coverage. Do not claim checks that did not run.
10. Hand off the issue, diff, checks, risks, and remaining work. Do not self-verify
    or self-review. Rigorous verification uses a separate fresh `verify-issue`
    task; after draft PR creation, offer a separate fresh `review-change` task and
    wait for the user's acceptance.
