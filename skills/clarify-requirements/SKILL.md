---
name: clarify-requirements
description: Clarify requirements to at least 95% confidence before proceeding. Use for requirements capture, bug reports and investigation, issue refinement or planning, specifications, implementation, and any instruction to do work after a discussion, even when the user does not explicitly ask for questions.
---

# Clarify requirements before proceeding

Read the shared [requirements readiness rule](references/readiness.md) before
assessing or acting on requirements. It governs practical convergence, material
questions, defaults, pending answers, and reuse of settled requirements.

Apply the shared [model and effort policy](references/model-effort.md) before
substantive work in each requested engineering stage.

For an explicitly enabled nightly run, first apply
[standing authorization](../nightly-implement/references/authorization.md).
Still assess confidence and record the requirements summary. New material
ambiguity before claiming a candidate uses authorized nightly clarification
screening: return it to needs-investigation and continue selection. After claiming,
stop dependent work with the nightly blocked handoff instead of an unattended
question. Outside this mode, the interactive steps below apply.

For interactive engineering work, interpret requested actions compositionally
and do not expand them into later workflow stages. `fix` or `implement` means
make the change and run proportionate tests at the selected model and effort.
Adding `open a PR` adds PR creation only. Adding `review` adds exactly
one fresh-context subagent review pass with the resolved model explicitly
(Codex Sol/high by default); never inherit the parent model. After the last requested
action—especially every review—stop and return control; do not automatically
remediate, re-review, verify, mark ready, merge, or offer the next action.
Explicitly enabled unattended nightly work is the sole exception to this stopping
rule, and its reviews must still use subagents within the scheduled task rather
than new user-visible tasks.

For bug work, distinguish observed from expected behavior and whether the
requested deliverable is capture, diagnosis, or a fix. Keep the requirements
summary proportional to the task.
