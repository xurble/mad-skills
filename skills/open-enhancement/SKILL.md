---
name: open-enhancement
description: Create a durable GitHub issue for a feature, improvement, refactor, or future idea. Use when the user directly asks to open, file, capture, or record an enhancement; do not create an issue from speculative conversation alone.
---

# Open an enhancement

In Codex, run every `gh` command—and any `mad-skills` command that reaches
GitHub—outside the sandbox with escalation from the outset.

1. Run `mad-skills context --format json`. Offer `mad-skills init` when project
   configuration is absent; use `light` for this task if declined.
2. Require an installed and authenticated `gh` CLI. Stop with the needed setup
   instruction if unavailable; do not fall back to a connector.
3. Capture the desired outcome, motivation, current limitation, benefit, scope,
   useful non-goals, rough acceptance criteria, dependencies, constraints, and
   material unknowns.
4. Do not force implementation details before repository investigation makes
   them necessary. Distinguish feature, improvement, and refactor accurately.
5. Read `<resolved.toolkit_root>/templates/enhancement-issue.md`; scale detail to
   the effective profile.
6. Write the body to a temporary file and create it with `gh issue create
   --body-file`, applying the configured `enhancement` label.
7. A direct request authorizes creation without another confirmation. Return the
   issue URL and note any unresolved questions.
