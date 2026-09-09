# Setup prerequisites

Record the observed configuration for every check. Unknown required settings are
not a pass, but setup does not execute a trial run to prove the workflow. The first
scheduled run may expose an environmental or permission failure; preserve its
normal failed/blocked handoff for interactive troubleshooting.

## Preflight

- Project: one explicitly selected saved Git project, canonical path and GitHub
  remote match; installed current skills/CLI; valid `mad-skills context`; GitHub
  issues enabled; configured setup, test and full-check commands. Use
  `mad-skills check` and inspect its findings rather than only its exit code.
- GitHub: installed/authenticated `gh`, actual repository read/write access,
  distinct configured actionable/blocked/in-progress/verified labels, and all
  required classification labels present. Check `gh label list`; resolve missing
  labels during interactive setup with `mad-skills setup-github-labels`. Check Git
  fetch and push authentication separately; `gh auth status` alone is insufficient.
  Verify gh's effective repository target matches the approved repository,
  including host/repository environment overrides.
- Codex: supported inventory/view/create/update/pause controls for one
  standalone project task, fresh verification/review task creation and waiting,
  a way to select the current reviewed branch/commit, and inspect actual task
  model/effort/environment. The selected model or resolved configured default
  supports medium and high on that host. Never select a new model to get an effort.
- Schedule: selected local time and IANA timezone are representable; verify the
  app's next runs and daylight-saving behavior. Local execution requires the
  computer and app available. Codex owns scheduling and history; no toolkit cron,
  daemon, or central runner. Read current app schemas instead of inventing fields.
- Permissions: inspect effective scheduled **and child** workspace-write sandbox
  and approval policy, including managed requirements. Check actual writable
  project/worktree locations, the shared Git metadata behind `.git` files, cache,
  dependency, build and temp locations. Check necessary network access to GitHub,
  remotes and dependency registries, credentials, and project setup/test commands.
  Required Git/GitHub/dependency/test operations must have persistent supported
  permissions in each environment. One-off approval or `approval_policy=never`
  does not grant access. Fix restrictions only through supported interactive Codex
  controls; do not write a toolkit permission registry or silently enable full
  access. Managed denials are blockers, not invitations to work around them.

After preflight, activate the task and verify its saved identity, recurrence,
timezone, model, medium effort and full authorization prompt through app readback.
Do not use Run now, a designated test issue, or a simulated workflow as an
activation gate. If a later scheduled run encounters a permission denial,
unavailable child control, failed command or other unmet prerequisite, it must
leave the ordinary failed/blocked handoff rather than broadening permissions,
skipping a stage or selecting a second issue.

Codex behavior references (consult current docs and runtime schemas during setup):
[scheduled tasks](https://learn.chatgpt.com/docs/automations?surface=app) and
[agent permissions](https://developers.openai.com/codex/permissions).
