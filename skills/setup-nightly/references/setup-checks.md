# Prerequisites and supervised trial

Record observed evidence for every check. Unknown is not a pass. Setup remains
interactive until all permissions and stages are proven; the trial itself must
complete without human responses after configuration is resolved.

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
- Codex: supported inventory/view/create/update/pause/run-now controls for one
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

## Trial procedure

1. Obtain approval of a concrete exact issue or designated test scope and the
   expected writes, including a deliberate review finding/remediation scenario.
   Use an isolated worktree in the selected project's actual scheduled environment.
   Never introduce a deliberate defect into unrelated production code. Use an
   approved test fixture with a genuine detectable defect/omission, or a pending
   test-scope acceptance item, to exercise the remediation path.
2. Create/update the intended task **paused**, with its full authorization, actual
   medium setting and narrow trial override. Launch it through supported Run now;
   inspect the resulting run's sandbox, approval policy and settings. If the host
   cannot run a paused task without enabling future runs, leave setup blocked
   until a supported supervised control is available. Do not claim an ordinary
   interactive chat tests the actual scheduled environment.
3. Exercise inspection and dependency setup, isolated worktree/branch, requirements
   assessment/summary and plan approval without prompts, plan posting,
   edits, tests/checks, focused commit, push, new independent verification and
   result posting/labels, draft PR creation, new high-effort review and comments.
   Ensure each fresh task receives the self-contained authorization and actual
   persistent permissions. Confirm real tool results and stage transitions.
4. Exercise at least one medium-effort remediation turn with a new commit, renewed
   checks/verification, and a **new** high-effort reviewer with no previous context.
   Demonstrate that stale review cannot mark final fixes ready. After clean
   current-head evidence, exercise the authorized ready transition. Never merge
   or close the trial issue automatically. Keep the trial PR available for human
   handling; it will correctly cause later production runs to skip while open.
5. If any operation prompts, fails, or has unverifiable settings, keep the task
   paused. Record the exact command/capability, environment and gate. Resolve it
   interactively and rerun the affected full path without human responses. For a
   retry, explicitly authorize only the recorded trial issue/PR and remaining
   stages in the trial instructions; unrelated open PRs still block the trial.
   Do not reset production attempt counts or select another issue. Record
   actual run/child IDs, settings, commands/results, commits and transitions.
   Unresolved failures or unexercised stages prevent readiness claims.
6. Once the complete expected path passes, store the evidence with trusted setup
   instructions/run history and activate the same task with approved production
   scope. Recheck identity, recurrence/timezone, model and medium effort after the
   update. A permission, host, model, path, workflow or command change that
   invalidates the trial requires revalidation before reactivation.

## Additional controlled workflow scenarios

In a designated test repository exercise: repeated setup (one task ID), custom
labels and tied creation dates, open draft/bot PR skipping, no issue, clean first
review, ambiguity before changes (issue comment) and after changes (draft PR with
incomplete checks disclosed), three exhausted fix rounds, failed commands,
interruption, denied GitHub writes and exact unapplied handoff output. Check
classification preservation, blocked labels, no automatic actionability restore,
one issue per run, fresh final review, no merge/closure, and unchanged interactive
gates when opt-in is absent. Unit tests can cover deterministic selectors; scenario
transcripts and successful real tool results establish agent behavior. Never
present mocked tests or a prose walkthrough as a successful unattended trial.

Codex behavior references (consult current docs and runtime schemas during setup):
[scheduled tasks](https://learn.chatgpt.com/docs/automations?surface=app) and
[agent permissions](https://developers.openai.com/codex/permissions).
