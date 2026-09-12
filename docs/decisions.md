# Decision log

## 2026-09-12 — Keep interactive implementation and review user-directed

**Decision:**

Treat each interactive request as an action boundary. `fix` or `implement` runs
implementation and testing at medium effort where supported. Adding `open a PR`
adds PR creation only. Adding `review` adds exactly one high-effort fresh-context
subagent review. After that pass, return control without remediation, re-review,
or a readiness transition. Do not create a separate user-visible task, thread, or
chat for code review. Independent verification remains a separate fresh task.
Explicitly enabled unattended nightly work is the sole exception: it may run its
bounded remediation/re-review/readiness loop, but every review remains a subagent
inside the scheduled task.

**Context:**

Fresh review execution varied by computer because the workflow described a
separate task without fixing the coordination mechanism. The owner wants review
results returned through the task where the work is already being coordinated,
while still withholding implementation history from the reviewer. When working
interactively, the owner also wants to decide what follows each implementation,
PR creation, and review result.

**Rationale:**

A subagent with no inherited conversation preserves reviewer independence and
keeps review orchestration consistent without adding another sidebar task. An
explicit one-level delegation rule prevents recursive review delegation. Literal
action boundaries keep the user in control and prevent a request from silently
growing into a fix/review loop.

**Alternatives considered:**

- Create a new task for every review: rejected because it exposes host-dependent
  behavior and moves the review cycle out of the current task.
- Review directly in the implementation context: rejected because implementation
  history weakens the intended fresh-context check.
- Automatically remediate review findings and re-review interactively: rejected
  because the user wants to decide the next action after seeing every review.

**Consequences and constraints:**

- Direct review requests and nightly review rounds use fresh-context subagents at
  high effort. Interactive implementation and remediation prefer medium effort
  but stay in the current task rather than creating another context for effort.
- A review subagent receives a self-contained target, scope, evidence, permissions,
  and stopping rules, and performs the review without delegating again.
- Interactive PRs remain draft when readiness gates are pending. A clean review
  does not mark one ready without a subsequent explicit instruction.
- Nightly may remediate and repeat reviews under its saved authorization, but it
  does so within one scheduled task and never produces extra review chats.
- If supported subagent controls cannot provide a fresh context, the workflow
  reports the limitation instead of creating a new chat or self-reviewing.
- This supersedes only the code-review execution mechanism in the 2026-09-08
  decision; verification continues to use a separate fresh task.

## 2026-09-09 — Activate nightly tasks without a setup trial

**Decision:**

After explicit one-project authorization and prerequisite/configuration checks,
`setup-nightly` activates the scheduled task directly. Setup does not require a
designated test issue, Run now execution, remediation exercise, or other
supervised trial.

**Context:**

The full implementation-through-review trial made initial setup burdensome. The
owner prefers to complete setup once and troubleshoot from a real overnight run
if an environmental, permission, or tool-control failure occurs.

**Rationale:**

The saved authorization, one-issue bound, no-merge rule, prerequisite inspection,
configuration readback, and failed/blocked handoff continue to limit unattended
work. A mandatory end-to-end rehearsal adds substantial setup cost without being
required by the owner for this personal toolkit.

**Alternatives considered:**

- Keep the supervised trial as a hard activation gate: rejected because its setup
  cost outweighs the desired assurance.
- Make the trial optional: rejected because setup should finish and leave the
  active schedule without another decision or execution step.

**Consequences and constraints:**

- The first scheduled run may reveal permission or environment failures that a
  trial would have caught earlier.
- Such failures use the existing failed/blocked handoff and never permit broader
  access, skipped checks, a second issue, merge, deployment, or issue closure.
- Setup still verifies task identity, schedule/timezone, model/effort settings,
  authorization text, and configured persistent permissions before reporting
  readiness.

## 2026-09-08 — Scope unattended authorization to one Codex project task

**Status:** Superseded in part by the 2026-09-09 decision removing the setup-trial
activation gate and the 2026-09-12 decision moving code reviews from new tasks to
subagents.

**Decision:**

Add explicit per-project nightly setup and execution skills. Store standing
authorization and trial evidence in trusted Codex scheduled-task instructions;
leave scheduling, permissions, task controls and history to Codex. Implement and
remediate at medium effort, and review in new independent tasks at high effort
using the selected model or configured default. Never merge automatically.

**Context:**

Interactive approval and review-offer gates, plus questions raised by new material
ambiguity, can otherwise stop unattended issue work. A reusable skill needs both
scoped authority and proven tool permissions;
an actionable issue or an approval-suppression setting supplies neither alone.

**Rationale:**

One explicitly selected project and at most one issue per run bound the authority.
A supervised trial, including remediation and fresh review in actual scheduled
and child environments, establishes that required actions succeed without human
responses. Current-diff checks, verification and review remain mandatory.

**Alternatives considered:**

- A central runner or toolkit permission registry: rejected as duplicate native
  infrastructure and an additional security boundary.
- Remove interactive gates globally or treat issue text as authorization:
  rejected because scope could expand without explicit opt-in.
- Use prompt-only effort instructions or choose another model automatically:
  rejected because neither honors the selected model and actual execution policy.

**Consequences and constraints:**

- This narrowly qualifies the 2026-08-23 prohibition on automatically launching
  review: explicit nightly opt-in accepts the offer in advance; ordinary
  interactive workflows retain that gate.
- No project is enabled during installation. Repeated setup updates the same
  paused/active task and cannot claim ready until its full trial passes.
- New material ambiguities produce blocked draft/issue handoffs; partial draft
  handoffs disclose incomplete checks without weakening ready requirements.
- Required runtime capabilities or permissions may be unavailable. Report that
  limitation and keep setup paused instead of inventing unsupported controls.
- The only new CLI behavior is deterministic read-only issue selection.

## 2026-08-29 — Bundle the Django preview helper inside its skill

**Decision:**

Ship `mad_skills_django_preview` as a Python resource inside the
`preview-django-page` skill. Add the resource directory to `PYTHONPATH` only for
the local preview server; do not publish it or add it to the toolkit's runtime
package.

**Context:**

Django templates need the project's rendering stack for useful browser previews,
but consuming projects should not gain a production dependency or maintain a
preview view for every page. Installed skills are symlinked directly to this
checkout, so their resources already share the toolkit's update lifecycle.

**Rationale:**

A skill resource keeps the workflow and helper version together, remains
immediately available to installed consumers, and disappears from importability
when the preview server is not launched with the temporary path. A consuming
project needs only a small flag-gated URL integration while retaining its normal
settings, middleware, template loaders, context processors, and static serving.

**Alternatives considered:**

- Publish a separate development dependency. Rejected because it adds a second
  release and installation lifecycle for a personal source-of-truth toolkit.
- Put the helper in `src/mad_skills`. Rejected because it would make Django
  preview code part of the general CLI package and its ordinary import path.
- Add project-specific preview views or scenarios. Rejected because it repeats
  infrastructure for each consuming project and page.

**Consequences and constraints:**

- Preview server commands must prepend the skill's `resources` directory to
  `PYTHONPATH` and bind to loopback.
- Consuming projects must explicitly approve the small development URL and
  setting integration; the skill cannot modify it silently.
- The helper supports Django 5.2 and 6.x while those versions fit the toolkit's
  Python support, and tests resolve both through the development lock.
- The helper remains a trusted development tool, not a sandbox for malicious
  middleware, context processors, templates, tags, or dependencies.

## 2026-08-23 — Use pull requests as the rigorous delivery contract

**Status:** Superseded in part by the 2026-09-12 decision requiring explicit
interactive actions and a stop after each review pass.

**Decision:**

For rigorous non-trivial work, use a standalone, well-specified pull request as
the durable delivery contract and merge gate. An issue is optional and is linked
only when it drove the work. Open the pull request as a draft while fresh AI
review is pending, and mark it ready after the accepted review cycle completes.
The developer may explicitly override only the AI-review gate.

**Context:**

This toolkit serves primarily one-person projects. Requiring an issue for work
already specified and approved in conversation duplicated the change contract
without adding corresponding safety. The workflow still needs a durable record
of final scope and a visible indication that independent review is pending.

**Rationale:**

A standalone pull request keeps the accepted outcome, motivation, scope,
acceptance criteria, implementation, validation, and risks beside the exact diff
being merged. Draft state provides a lightweight, visible review gate without
requiring workflow orchestration. Issues remain useful as a backlog and retain
their normal closing relationship when they are the source of the work.

**Alternatives considered:**

- Require an issue for every rigorous change. Rejected because it duplicates an
  already accepted specification and adds ceremony to issue-less work.
- Start fresh AI review automatically when a draft pull request is created.
  Rejected because review should begin only after explicit user acceptance.
- Make AI review impossible to bypass. Rejected because the developer retains
  final authority in a personal toolkit; any override must be explicit and the
  skipped review must be disclosed.

**Consequences and constraints:**

- Rigorous pull requests must stand alone and not depend on chat or issue history.
- Existing issues are linked and closed only when they actually drove the work.
- A draft rigorous pull request represents pending fresh AI review.
- Material findings keep the pull request in draft and require another fresh
  review after remediation.
- An explicit override bypasses only the AI-review gate, not other required
  planning, verification, tests, or repository checks.
- The workflow must not automatically launch review or merge pull requests.
