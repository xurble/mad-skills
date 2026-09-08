---
name: setup-nightly
description: Explicitly enable, update, or pause nightly issue implementation for one selected project using a Codex scheduled task. Check persistent permissions and run a supervised trial before enabling unattended work; never opt in projects during installation.
---

# Set up one project's nightly implementation

Apply [clarify-requirements](../clarify-requirements/SKILL.md) interactively.
This skill requires supported Codex app scheduling and fresh-task controls;
other hosts may read the skills but must not invent a scheduler or Claude fallback.
Read [setup and trial checks](references/setup-checks.md) and the
[saved task template](references/scheduled-task.md).

1. Resolve exactly one explicitly selected saved project using Codex's project
   inventory. Confirm its canonical path, host, Git remote/repository, nightly
   local time and IANA timezone, optional model choice, and approved trial issue
   or designated test scope. Do not discover/enable other projects automatically.
   Explicitly request standalone project runs and separate verification/review
   tasks as part of the opt-in; a thread heartbeat is not this workflow.
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
   project/selection/workflow/stop field, chosen time/timezone, model provenance,
   permissions and trial scope. Present this concrete authorization and task
   configuration for approval before the first trial or activating wider scope.
   On repeat setup, reuse settled authorization; confirm material expansions.
5. Use supported app controls to create/update **one paused standalone** task on
   that project. Use `list_projects` IDs and `automation_update` with cron kind,
   local execution, the approved schedule, and actual `reasoningEffort: medium`.
   For updates use its resolved ID and full preserved fields. When model is
   omitted by the user, use the configured default; if a required model field
   needs a concrete value, resolve and record that default through supported
   settings rather than choosing another. Validate both medium and high support
   on the actual host; unsupported/unavailable values stop setup.
6. Verify schedule/timezone semantics in the app, including daylight-saving
   behavior. If the available control cannot represent the selected timezone,
   report that and resolve it interactively; do not silently schedule UTC or the
   host's timezone. Read back project binding, paused state, schedule, model and
   effort. A prompt saying “medium” or a successful create call alone is not proof.
7. Run the supervised trial using the actual paused scheduled task's supported
   Run now control and its saved trial-scope instructions. Exercise fresh child
   tasks and a remediation round as specified in setup checks. Fix permissions
   interactively, then repeat the affected path without human responses. A
   successful interactive parent turn or simulated command log is insufficient.
   Unsupported Run now, child controls, effort inspection, or unresolved trial
   failures keep the task paused and the project **not ready**.
8. Save trial evidence in trusted setup instructions/run records. After the whole
   expected path passes unattended, replace the trial scope with the approved
   production selection rule and activate this same task ID. Read back its full
   configuration and report the project, schedule/timezone, model/default source,
   medium implementation/high review settings, authorization, trial evidence,
   task ID and readiness. An update invalidating tested prerequisites requires
   another trial before activation. Repeating unchanged setup reuses valid trial
   evidence and updates the existing task without duplicating it.

For a pause request, locate the existing task by the same identity checks and
pause it through Codex controls. Pausing stops future scheduled runs; it does not
cancel an already running task, merge/close a PR, or remove branches/worktrees.
Never claim cancellation of in-flight work from pausing the schedule alone.
