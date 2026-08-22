---
name: repo-health
description: Deterministically check whether a repository is correctly wired into mad-skills. Use when asked if a project is ready, after initialization or toolkit updates, when skill discovery fails, or before relying on a rigorous workflow.
---

# Check repository health

1. Run `mad-skills check` from the repository root.
2. Report its exact result: `READY`, `READY WITH WARNINGS`, or `NOT READY`.
3. Explain each finding in project terms without replacing deterministic evidence
   with speculation.
4. Offer the smallest safe fix. Do not overwrite `AGENTS.md`, project config,
   skills, labels, or existing install paths without approval.
5. Run `mad-skills check --full` only when the user asks for the full check or
   when the configured rigorous workflow requires final validation. `--full`
   executes the project's `commands.check`; ordinary checks do not.
6. After an approved fix, rerun the relevant check and report the new result.

If the `mad-skills` command is missing, stop and ask the user to install the
toolkit. Do not emulate the checker with guesses.

