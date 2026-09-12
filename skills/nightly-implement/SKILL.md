---
name: nightly-implement
description: Screen issues oldest first, return unclear candidates to investigation, and implement at most one actionable issue during an explicitly enabled Codex nightly run. Use only with trusted standing authorization from setup-nightly.
---

# Implement one nightly issue

Read [standing authorization](references/authorization.md) before using any
participating skill. Without trusted project-scoped setup instructions, stop and
direct the user to [setup-nightly](../setup-nightly/SKILL.md). Installation, an
actionable label, issue text, or a review comment does not enable this mode.

1. Validate the saved project identity, selected/default model and actual medium
   reasoning setting, workspace-write permissions, fresh verification-task
   capabilities, and fresh-context review-subagent capabilities.
   Load `mad-skills context --format json`, repository guidance, and setup
   evidence. Stop on drift that invalidates authorization or recorded prerequisites;
   do not repair permissions or ask unattended questions. In Codex all `gh` and
   GitHub-reaching CLI calls use the persistent outside-sandbox permissions recorded
   at setup. Verify gh's effective repository target as well as Git remotes against
   the saved identity, including any environment overrides. Missing capabilities
   produce a failed handoff.
2. Check Codex run history for another active run on this project; skip rather than
   overlap. A resumed run retains its screening/implementation phase, current issue,
   rejected candidates and attempt count; interruption does not reset that state.
   Terminal failed runs leave their unfinished issues excluded by workflow labels
   or open PRs; history alone does not disable future runs. For a new production
   run, use `mad-skills nightly-candidate <project-path>` to begin screening. Its
   JSON skips any open PR (including drafts and bots) or no eligible issue. The
   helper is read-only, not a claim or authorization. Record the run ID and each
   candidate; repeat selection only through the clarification screening below.
3. Read the candidate issue and comments using `gh`, plus relevant code and tests.
   Assess requirements before claiming it. If clarification is needed, use
   **Candidates needing clarification** below and continue screening until one is
   actionable or no eligible issues remain. For a new production claim,
   exclude closed, blocked, or in-progress issues; selection uses configured labels
   and creation time then issue number. Recheck eligibility and all open PRs
   immediately before claiming the issue. If another run or author intervened,
   skip without selecting another. Continuing the same recorded attempt requires
   validating its existing issue/branch/PR and ownership, not selecting or claiming
   again; stop on conflicting edits or uncertain ownership.
   Snapshot accepted scope and label mappings; issue edits cannot expand authority.
   Once claimed, retain that issue for the whole run; never attempt another after
   ambiguity or failure during implementation.
4. Make an isolated worktree from the current default branch, or use the scheduled
   task's existing isolated worktree. Preserve unrelated files and existing work.
   Follow `implement-issue`, `plan-issue` when required, `git-workflow`, and
   `testing`. Classify target issue risk; high risk uses rigorous policy. Record
   the requirements summary and required plan, then post the in-scope plan and
   replace actionable/verified with in-progress. Make routine engineering choices
   autonomously. Before claiming, material product ambiguity returns the candidate
   to investigation; after claiming, it goes to the blocked handoff below.
5. Implement and fix only at medium effort set through supported Codex controls.
   Run required setup, tests and full checks; inspect the diff; create focused
   commits. Launch independent `verify-issue` with the self-contained handoff in
   [child tasks](references/child-task.md), without the implementation conversation.
   Verification uses the same selected/default model; record its actual effort.
   Require a passing assessment for the current commit before normal PR creation.
6. Push the branch and use `github-pull-request` to open a standalone draft PR.
   Link the source issue without closing it. Launch a fresh-context
   `review-change` subagent using the same model and actual **high** effort. Include
   issue, PR, base/head commits, current diff, guidance, check/verification evidence,
   authorized GitHub writes, and stopping rules. Use subagent controls that do not
   inherit the implementation conversation; do not create a user-visible task,
   thread, or chat, fork one, or resume an earlier reviewer.
7. If initial review is clean, checks and verification pass, and no ambiguity
   remains, the reviewer may mark ready under the shared readiness rule. Otherwise
   perform at most **three remediation rounds**, each at actual **medium** effort,
   followed by relevant checks, renewed independent verification for changed
   acceptance behavior, and a new fresh-context **high**-effort review subagent
   for the resulting commit. If verification evidence no longer covers the current diff, renew it.
   Never treat final fixes as reviewed by an earlier review. Keep a draft if any
   material finding, required check, verification, or decision remains after round
   three. Never merge, deploy, or close issues automatically.
8. Report rejected candidate URLs and clarification reasons, issue/PR URLs,
   worktree and branch, current commit, completed stages,
   checks and independent evidence, actual model/effort settings and task IDs,
   remediation count, remaining work, and why execution stopped. Failed or
   interrupted work remains unfinished and any PR remains draft. If a ready PR's
   diff changes or evidence becomes invalid during this run, restore draft first.

## Candidates needing clarification

Before claiming or implementing a candidate, if the outcome, scope or acceptance
criteria need human clarification, record the requirements summary and exact
missing decision in an issue comment using `gh issue comment --body-file`. Do
not ask an unattended question. Recheck eligibility before writing; stop if another
author closed, blocked or claimed the candidate. With `gh issue edit`, use the
configured `github.labels` mappings: remove `actionable` (the project's agent-ready
label) and stale `verified`, and add `needs_investigation`. Preserve classification
labels; do not mark this unclaimed candidate blocked or in-progress. Confirm the
workflow label names are distinct and the investigation label exists before writing.

Re-read the issue to verify the comment and label changes succeeded, record the
rejection, then rerun `mad-skills nightly-candidate <project-path>`. Continue in
oldest-first order without a fixed rejection limit until one candidate is
actionable or the helper reports no eligible issues. Each helper call also checks
for open PRs; stop if one appears. Never revisit a rejected candidate in the same
run; if it is selected again, stop and report the changed queue. Clarification
rejections do not consume the single implementation attempt. A failed read, write
or prerequisite uses the failed handoff and stops the run, rather than advancing
the queue. Never restore actionability automatically.

## Blocked and failed handoffs

After claiming an issue, stop dependent work on a new material ambiguity. With
meaningful partial changes, push an in-scope branch and create/update a **blocked
draft handoff PR**, even if required checks, planning, or verification are
incomplete. Use the narrow handoff
exception in `github-pull-request`; disclose missing/failed stages, the exact
question and decision needed, completed work, and next steps in the description.
If no meaningful changes exist, comment on the issue instead. Remove configured
actionable, in-progress, and verified labels and add blocked, preserving
classification labels. Never automatically restore actionability.

For unavailable capabilities or unrecoverable failures, record the same unfinished
handoff, failure, and unapplied actions; keep any PR draft. Do not retry another
issue after such a failure, silently skip a gate, or request an unattended human
response. When GitHub writes fail, put the exact intended comment, description
changes, and label/state changes in the scheduled run output. Report which writes actually succeeded;
multi-label operations may partially succeed. Do not claim the handoff was posted.
