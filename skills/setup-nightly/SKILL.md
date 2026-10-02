---
name: setup-nightly
description: Explicitly enable, update, or pause nightly issue implementation for one selected project using a Codex scheduled task. Check configuration and persistent permissions before activation; never opt in projects during installation.
---

# Set up one project's nightly implementation

Apply [clarify-requirements](../clarify-requirements/SKILL.md) interactively.
This skill requires supported Codex app scheduling, fresh verification-task
controls, and fresh-context review-subagent controls;
other hosts may read the skills but must not invent a scheduler or Claude fallback.
Read [setup checks](references/setup-checks.md) and the
[saved task template](references/scheduled-task.md).
Apply the shared [Codex GitHub command rule](../github-pull-request/references/gh-execution.md)
to setup's `gh` checks; retain the approved persistent-permission requirements
for the scheduled run.

1. Resolve exactly one explicitly selected saved project using Codex's project
   inventory. Confirm its canonical path, host, Git remote/repository, nightly
   local time and IANA timezone, and optional model choice. Default to Codex Sol
   when the user has not chosen a model. Do not discover or
   enable other projects automatically.
   Explicitly request standalone project runs, separate verification tasks, and
   fresh-context review subagents as part of the opt-in; a thread heartbeat is
   not this workflow.
2. Load effective project configuration and required commands/labels. Complete
   every prerequisite in the setup checks. Present missing prerequisites with
   their exact resolution; use supported Codex controls for any approved permission
   changes, respect managed policy, and never silently broaden access. Require
   `gh`; in Codex use approved outside-sandbox execution from the outset.
3. Inspect existing Codex scheduled tasks, including paused ones, by project ID,
   canonical repository/path, and the `mad-skills nightly` marker in their prompt.
   Use the recorded task ID when available and verify its identity. Read existing
   automation records as supported by the app (currently
   `$CODEX_HOME/automations/*/automation.toml`) and use the app's view control.
   An inaccessible inventory or multiple matches is a blocker: resolve it
   interactively, never create a likely duplicate. Preserve unrelated settings
   including notification preferences. Never write automation TOML directly.
4. Prepare the complete saved instructions from the template, filling every
   project/selection/workflow/stop field, chosen time/timezone, exact model ID
   and provenance (explicit setup selection or Codex Sol default), and fixed
   stage efforts (high for screening, planning, verification and review; medium
   for implementation, fixes and remediation), plus permission settings. Present
   this concrete authorization and task
   configuration for approval before activation. On repeat setup, reuse settled
   authorization; confirm material expansions.
5. Verify schedule/timezone semantics in the app, including daylight-saving
   behavior. If the available control cannot represent the selected timezone,
   report that and resolve it interactively; do not silently schedule UTC or the
   host's timezone.
6. For an enable/setup request, use supported app controls to create/update **one
   active standalone** task on that project. A settings-only update preserves the
   existing paused/active state unless the user requests activation. Use
   `list_projects` IDs and `automation_update` with cron kind, local execution,
   the approved schedule, and actual `reasoningEffort: medium`.
   For updates use its resolved ID and full preserved fields. When model is
   omitted by the user, select Codex Sol through supported settings and record
   it explicitly. Validate both medium and high support
   on the actual host; unsupported/unavailable values stop setup.
7. Read back project binding, intended active/paused state, schedule, timezone,
   exact model ID and provenance, scheduled-task medium effort, saved high/medium
   stage effort mapping and full prompt. A prompt saying “medium” or a
   successful create call alone is not proof. If the readback differs materially,
   pause the task and report the exact
   mismatch. Otherwise report the project, schedule/timezone, exact model/default
   source, high screening/planning/verification/review and medium
   implementation/fixes/remediation settings, authorization, setup evidence,
   task ID and readiness. Do not require or launch a supervised trial; activation
   completes setup, and failures from a later scheduled run use the normal
   failed/blocked handoff for interactive troubleshooting.

For a pause request, locate the existing task by the same identity checks and
pause it through Codex controls. Pausing stops future scheduled runs; it does not
cancel an already running task, merge/close a PR, or remove branches/worktrees.
Never claim cancellation of in-flight work from pausing the schedule alone.
