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
verification, review subagents, and remediation without additional prompts.
Required artifacts, checks and independent assessments still occur. Follow
`nightly-implement` for effort controls, clarification screening before claiming,
bounded review rounds and blocked/failed draft handoffs. Missing configuration or
capabilities stop the run; material ambiguity returns an unclaimed candidate to
investigation and continues authorized screening, or stops an already claimed
issue with a blocked handoff. Do not ask unattended setup/clarification questions.

In Codex, run every `gh` command—and any `mad-skills` command that reaches
GitHub—outside the sandbox with escalation from the outset.

For interactive work, treat the user's requested actions as the execution
boundary and prefer actual medium effort through supported controls. Keep
implementation in the current task; do not create another task or subagent merely
to change its effort, and continue at the current effort with disclosure if medium
cannot be applied:

- `fix` or `implement` authorizes implementation and proportionate testing, not
  verification, PR creation, review, readiness changes, or merge;
- adding `open a PR` also authorizes PR creation, but not review;
- adding `review` also authorizes exactly one fresh-context high-effort review
  pass after the requested implementation and PR work.

Workflow policy may identify evidence or review still required before readiness
or merge, but it does not expand the current interactive request. Stop after the
last requested action and let the user choose the next one. Explicitly enabled
nightly work is the sole exception and follows its authorized unattended loop.

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
5. Enforce effective policy without adding unrequested interactive actions:
   - rigorous non-trivial work needs a written plan, tests, and a full check. A
     direct fix/implement request with 95% requirements confidence authorizes the
     in-scope plan; present it concisely without adding a confirmation gate. Fresh
     verification, a standalone well-specified draft PR, and fresh
     review remain gates before readiness or merge but run only when requested;
     the issue is this workflow's input, not a universal prerequisite;
   - normal meaningful changes normally need tests and a fresh review before
     readiness, but the review runs only when requested;
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
    or self-review, offer or start an unrequested review, create an unrequested
    PR, or continue into remediation. If review was explicitly included, delegate
    one fresh-context high-effort `review-change` pass and stop after its result.
