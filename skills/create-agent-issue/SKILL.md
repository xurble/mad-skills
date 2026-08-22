---
name: create-agent-issue
description: Turn an existing GitHub issue or user request into an implementation-ready agent contract grounded in the current repository. Use when asked to refine, promote, specify, or make an issue actionable for a fresh implementation task.
---

# Create an agent-actionable issue

In Codex, run every `gh` command—and any `mad-skills` command that reaches
GitHub—outside the sandbox with escalation from the outset.

1. Load effective policy with `mad-skills context --format json`. Offer project
   initialization if missing.
2. Require installed, authenticated `gh`. Load the issue body, labels, and
   comments; do not rely on the authoring conversation.
3. Inspect `AGENTS.md`, relevant code, tests, architecture, and existing patterns
   without editing code.
4. Produce a self-contained contract using
   `<resolved.toolkit_root>/templates/agent-actionable-issue.md`:
   - outcome and current context;
   - in-scope behavior and non-goals;
   - observable acceptance criteria;
   - relevant components and patterns, without over-prescribing implementation;
   - `low`, `normal`, or `high` risk and why;
   - migrations, data safety, security, compatibility, and rollback where relevant;
   - expected verification and unresolved questions.
5. For `rigorous` or high-risk work, make tests, rollback/data safety, migration,
   and security expectations explicit. Stop if a material product decision is
   unresolved instead of inventing it.
6. Show the complete proposed replacement before mutating GitHub. After approval,
   update the issue body with `gh issue edit --body-file` and apply the configured
   `actionable` and, when justified, `high-risk` labels.
7. Return the issue URL and a concise readiness summary.
