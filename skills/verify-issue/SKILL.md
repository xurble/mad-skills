---
name: verify-issue
description: Independently verify a completed change against its PR, GitHub issue, or supplied acceptance criteria in a separate fresh task. Use when asked to check acceptance criteria, validate an implementation, or determine whether a change is ready after implementation.
---

# Verify a change

Apply [clarify-requirements](../clarify-requirements/SKILL.md) to the task's
requirements first; reuse the established requirements for the same scope.

Run this workflow in a task separate from implementation.

For explicitly enabled nightly work, require the self-contained fresh-task scope
and allowed writes specified by
[standing authorization](../nightly-implement/references/authorization.md).
It approves posting verification results/labels without another prompt; still
produce the requirements summary and full evidence-based result. Do not
inherit implementation history or assume parent permissions. Record the verified
commit. Missing prerequisites or new ambiguity require a failed/blocked handoff.

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
3. Separate pre-merge criteria from inherently post-merge checks using
   [acceptance stages](#acceptance-stages). For every criterion classify `verified`,
   `failed`, `unable to verify`, or `pending post-merge`, citing evidence or the
   required follow-up. State whether pre-merge verification passes separately
   from whether the entire issue is complete.
4. Check missing behavior, regressions, edge cases, scope creep, debug artifacts,
   migration/data safety, security boundaries, and test adequacy proportionate to
   risk. Run safe focused checks; run `mad-skills check --full` when policy requires.
5. Do not repeat implementation claims as evidence and do not edit code.
6. Present the complete verification result before changing GitHub. When a source
   issue or PR exists, comment the result there only after approval. Only for an
   issue-driven change whose material criteria all pass (none pending), remove
   `in-progress` and apply `verified`; otherwise do not change issue labels. For issue-less work
   verified before PR creation, return the result locally for the PR handoff.
7. Never merge a PR or close an issue. Issue closure occurs only through a merged
   linked PR or the user's explicit request.

## Acceptance stages

A criterion that inherently needs the change merged, deployed, or released is a
follow-up, not a prerequisite to creating or readying its PR. For example, a
CodeQL scan of the updated default branch can only confirm the change after
merge. Preserve that criterion as `pending post-merge`; do not block implementation
or relabel the issue `blocked` solely because that event has not happened.

Record each pending check in verification results and the PR: why it must wait,
what evidence will satisfy it, its trigger, and the responsible person or role
(for example, the maintainer after a human merge). Independently verify everything
testable on the current diff first, including available PR CI/scan results before
readiness. A pre-merge verification pass with these documented follow-ups permits
normal PR creation and readiness under the existing check and fresh-review gates;
it does not mean the whole issue is verified. Leave `verified` unapplied and avoid
auto-closing issue references while acceptance checks remain pending.

Do not defer a failing or unavailable pre-merge check as post-merge, silently drop
criteria, or override an explicit requirement that evidence must exist before
merge. Those remain blockers at their applicable gate. Unclear product behavior
or safety requirements still need clarification. Pending follow-ups authorize no
merge, deployment, release, automatic monitoring, or issue closure.
