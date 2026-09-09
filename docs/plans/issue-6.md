# Issue #6 implementation plan

Historical note: the supervised-trial activation gate in this original plan was
superseded by the 2026-09-09 decision in `docs/decisions.md`.

Implement the accepted issue contract as two shared skills, with Codex owning
scheduling, task controls, permissions, and run history. Risk is high because
standing authorization permits unattended code and GitHub writes. No application
migration, central runner, automatic merge, or installation-time opt-in is added.

1. Add a read-only `nightly-candidate` CLI command using authenticated `gh` and
   effective label mappings. Skip any open PR; inspect all pages of open issues,
   exclude blocked/in-progress issues, and select by creation time then number.
2. Add `setup-nightly` with explicit one-project opt-in, idempotent app task
   updates, selected/default model validation, persistent permission checks,
   and a supervised implementation-through-remediation trial before activation.
3. Add `nightly-implement` and reusable saved-task/child-task instructions. Bound
   execution to one issue, isolated worktrees, medium implementation/fix turns,
   independent verification, high-effort fresh reviews, and three fix rounds.
4. Audit all seven participating skills. Add a shared standing-authorization
   exception for routine gates, preserve required evidence and interactive
   behavior, and allow clearly disclosed blocked draft handoffs.
5. Update metadata, bundles, workflow docs, specification, and decision log.
   Test deterministic boundaries and exercise realistic workflow scenarios.
6. Run toolkit validation, pytest, Ruff, the canonical check, final diff inspection,
   and fresh independent verification. Prepare a draft PR with validation limits
   disclosed and offer fresh code review before readiness.

Live scheduled/child-task trials require an explicitly designated project and
issue/test scope, supported task controls, and its actual persistent permissions.
Local or simulated tests cannot establish that deployment prerequisite. Any live
stages not exercised must remain recorded as unverified; do not enable a project
or claim unattended readiness from this implementation alone.
