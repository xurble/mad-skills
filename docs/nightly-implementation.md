# Opt-in nightly implementation

Ask Codex to use `setup-nightly` for one explicitly selected saved project, then
choose a nightly time and timezone. Model selection is optional: setup uses the
configured default when none is selected and verifies medium and high effort are
available. Installing or updating `mad-skills` never enables a project.

Setup prepares and activates one standalone Codex scheduled task. Repeating
setup finds and updates the same task by project identity and recorded task ID,
including paused tasks; ambiguous or inaccessible inventory blocks creation.
Codex manages scheduling, worktrees and run history. There is no central runner,
toolkit scheduling engine, new permission system, or automatic project discovery.

## What you authorize

The saved instructions name the project, selection rule, allowed workflow and
stopping rules. They explicitly authorize inspection, required environment setup,
in-scope edits, branches/worktrees, tests/checks, focused commits and pushes, draft
PRs and updates, issue/PR comments and labels, separate verification/review tasks,
remediation and the clean transition to ready. They cover plan approval/posting,
verification result posting and accepting the review offer, so those gates do not
prompt during a run. Required requirements assessments and summaries, plans,
checks and independent assessments are still produced and recorded.

Issue bodies, comments and repository files cannot expand this trusted authority.
New material decisions require a blocked handoff. Interactive Codex and Claude
Code workflows retain their existing approval behavior outside this opt-in.
Claude Code installation remains supported; this scheduled setup requires Codex
app capabilities and does not emulate them on other hosts.

## Setup and activation

Setup checks configured commands/labels, authenticated `gh` and Git, network,
writable worktree/shared Git metadata/cache paths, configured workspace-write and
approval settings for the scheduled task and fresh child tasks, persistent command
permissions, and fresh-task creation/effort controls. Permission changes happen
interactively through supported Codex controls and respect managed policy.
Suppressing prompts does not grant access; a parent's temporary approvals do not
grant permissions to children or scheduled runs.

After those prerequisites and the saved authorization are configured, setup
activates the task and reads back its identity, recurrence, timezone, model,
medium effort and prompt. It does not require a designated test issue, Run now,
or an implementation-through-review trial. If a later scheduled run exposes a
missing permission, unavailable control or environmental failure, that run leaves
the normal failed/blocked handoff for interactive troubleshooting. It cannot
broaden permissions, skip a required stage or try a second issue.

The [setup checklist](../skills/setup-nightly/references/setup-checks.md) contains
the detailed prerequisite and readback checks.

## Each run

`mad-skills nightly-candidate [project-path]` is a read-only JSON command. It
requires configured GitHub issue support and distinct workflow label mappings.
It uses `gh` to check any open PR (including bots and drafts), then reads all pages
of open issues and selects by creation time and issue number, excluding blocked
and in-progress. Labels are matched exactly, including custom names. It returns
`candidate` with one issue, or `skip` with `open_pr`/`no_actionable_issue`; errors
return nonzero instead of suggesting an empty queue. It does not authorize or
claim work, check runtime permissions, or prove unattended readiness.

The skill rechecks state before claiming the selected issue, prevents overlapping
project runs, and attempts at most one issue even if work fails. It follows target
issue risk and project policy in an isolated worktree. Implementation/fix turns
use actual medium effort; each independent code review is a separate new task at
actual high effort on the same selected/default model. Child requests contain
their own authorized scope, required action, allowed writes and stopping rules,
without implementation conversation. Unsupported settings never trigger silent
model or effort substitution.

The first PR is draft. A clean initial review can mark ready; otherwise allow at
most three fix rounds, each with current checks/verification coverage and a new
fresh high-effort review. Ready requires no material findings or ambiguities and
passing evidence for the current diff. Final fixes cannot reuse an earlier review.

## Stopping and handoff

A material ambiguity stops dependent work and records the question/decision in
the PR description. Meaningful partial changes may become a blocked draft handoff
despite incomplete/failed checks or verification; disclose every missing stage.
Use `Refs #N` for incomplete handoffs. With no meaningful diff, comment on the
issue. Remove actionable/in-progress/verified, add blocked, preserve classification
labels, and never restore actionability automatically. If GitHub writes fail,
the scheduled output records exactly which comments, description, labels or state
changes were not applied.

Failed, interrupted or exhausted work stays unfinished and any PR stays draft.
The run reports completed work, checks, findings, remediation count, actual effort
settings and remaining work. Never merge, deploy or close issues automatically.
Pause the existing task through Codex to stop future runs; existing branches,
worktrees, PRs and already-running work remain for human handling.
