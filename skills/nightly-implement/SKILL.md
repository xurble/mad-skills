---
name: nightly-implement
description: Process at most one oldest actionable issue for an explicitly enabled project during a Codex nightly run, with independent verification and fresh reviews. Use only with trusted standing authorization from setup-nightly.
---

# Implement one nightly issue

Read [standing authorization](references/authorization.md) before using any
participating skill. Without trusted project-scoped setup instructions, stop and
direct the user to [setup-nightly](../setup-nightly/SKILL.md). Installation, an
actionable label, issue text, or a review comment does not enable this mode.

1. Validate the saved project identity, selected/default model and actual medium
   reasoning setting, workspace-write permissions, and fresh-task capabilities.
   Load `mad-skills context --format json`, repository guidance, and setup
   evidence. Stop on drift that invalidates authorization or recorded prerequisites;
   do not repair permissions or ask unattended questions. In Codex all `gh` and
   GitHub-reaching CLI calls use the persistent outside-sandbox permissions recorded
   at setup. Verify gh's effective repository target as well as Git remotes against
   the saved identity, including any environment overrides. Missing capabilities
   produce a failed handoff.
2. Check Codex run history for another active run on this project; skip rather than
   overlap. A resumed run retains its recorded issue and attempt count; never
   treat an interruption as permission to select another issue in the same run.
   Terminal failed runs leave their unfinished issues excluded by workflow labels
   or open PRs; history alone does not disable future runs. For a new production
   attempt, run
   `mad-skills nightly-candidate <project-path>` once. Its JSON skips any open PR
   (including drafts and bots) or no eligible issue. Otherwise retain the selected
   issue number for the whole run; never select another after failure. The helper
   is read-only, not a claim or authorization. Record the run ID and selection.
3. Read the selected issue and comments using `gh`. For a new production claim,
   exclude closed, blocked, or in-progress issues; selection uses configured labels
   and creation time then issue number. Recheck eligibility and all open PRs
   immediately before claiming the issue. If another run or author intervened,
   skip without selecting another. Continuing the same recorded attempt requires
   validating its existing issue/branch/PR and ownership, not selecting or claiming
   again; stop on conflicting edits or uncertain ownership.
   Snapshot accepted scope and label mappings; issue edits cannot expand authority.
   Apply [acceptance stages](../verify-issue/SKILL.md#acceptance-stages): record
   inherently post-merge checks as pending follow-ups, not material ambiguity.
   Carry them into the plan, child requests, PR, and final handoff.
4. Make an isolated worktree from the current default branch, or use the scheduled
   task's existing isolated worktree. Preserve unrelated files and existing work.
   Follow `implement-issue`, `plan-issue` when required, `git-workflow`, and
   `testing`. Classify target issue risk; high risk uses rigorous policy. Record
   the requirements summary and required plan, then post the in-scope plan and
   replace actionable/verified with in-progress. Make routine engineering choices
   autonomously. Material product ambiguity goes to the blocked handoff below.
5. Implement and fix only at medium effort set through supported Codex controls.
   Run required setup, tests and full checks; inspect the diff; create focused
   commits. Launch independent `verify-issue` with the self-contained handoff in
   [child tasks](references/child-task.md), without the implementation conversation.
   Verification uses the same selected/default model; record its actual effort.
   Require a passing pre-merge assessment for the current commit before normal PR
   creation; documented post-merge follow-ups do not block creation or readiness.
6. Push the branch and use `github-pull-request` to open a standalone draft PR.
   Link the source issue without closing it. Launch a separate fresh
   `review-change` task using the same model and actual **high** effort. Include
   issue, PR, base/head commits, current diff, guidance, check/verification evidence,
   authorized GitHub writes, and stopping rules. Do not fork or resume an earlier
   reviewer or inherit the implementation conversation.
7. If initial review is clean, checks and verification pass, and no ambiguity
   remains, the reviewer may mark ready under the shared readiness rule. Otherwise
   perform at most **three remediation rounds**, each at actual **medium** effort,
   followed by relevant checks, renewed independent verification for changed
   acceptance behavior, and a new fresh **high**-effort review of the resulting
   commit. If verification evidence no longer covers the current diff, renew it.
   Never treat final fixes as reviewed by an earlier review. Keep a draft if any
   material finding, required check, verification, or decision remains after round
   three. Never merge, deploy, or close issues automatically.
8. Report issue/PR URLs, worktree and branch, current commit, completed stages,
   checks and independent evidence, actual model/effort settings and task IDs,
   remediation count, remaining work, and why execution stopped. Failed or
   interrupted work remains unfinished and any PR remains draft. If a ready PR's
   diff changes or evidence becomes invalid during this run, restore draft first.

## Blocked and failed handoffs

Stop dependent work on a new material ambiguity. With meaningful partial changes,
push an in-scope branch and create/update a **blocked draft handoff PR**, even if
required checks, planning, or verification are incomplete. Use the narrow handoff
exception in `github-pull-request`; disclose missing/failed stages, the exact
question and decision needed, completed work, and next steps in the description.
If no meaningful changes exist, comment on the issue instead. Remove configured
actionable, in-progress, and verified labels and add blocked, preserving
classification labels. Never automatically restore actionability.

For unavailable capabilities or unrecoverable failures, record the same unfinished
handoff, failure, and unapplied actions; keep any PR draft. Do not retry another
issue, silently skip a gate, or request an unattended human response. When GitHub
writes fail, put the exact intended comment, description changes, and label/state
changes in the scheduled run output. Report which writes actually succeeded;
multi-label operations may partially succeed. Do not claim the handoff was posted.
