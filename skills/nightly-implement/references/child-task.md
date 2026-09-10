# Fresh verification or review request

Create a new separate task through supported Codex controls. Fill every field
below with current values from trusted setup and observed Git state. Pass plain
prose in the task's prompt. Do not fork a conversation, resume the previous
reviewer, or assume parent permissions. Select the exact current branch/ref using
supported task target controls; for a Git project use an isolated worktree. Resolve
the real thread ID after asynchronous setup before continuing or waiting on it.

> This is an explicitly authorized fresh [verification/code-review] task for
> [project ID, host, canonical project path, GitHub repository] and issue [URL].
> The user enabled this project's nightly implementation workflow during setup
> [setup record]. Authority is limited to this issue's accepted
> scope: [self-contained outcome, constraints, acceptance criteria].
>
> Apply [verify-issue/review-change]. Independently read [issue URL and PR URL if
> available], repository guidance, the diff from [base SHA] to [head SHA/branch],
> [test/check evidence] and [independent verification evidence for review]. Include
> [post-merge checks, evidence required, triggers and responsible roles] separately
> under [acceptance stages](../../verify-issue/SKILL.md#acceptance-stages). Do not
> rely on implementation conversation or treat implementation claims as evidence.
> Confirm you are inspecting the specified commit; report if the remote head moves.
>
> Model: [setup-selected model or resolved configured default]. Task controls
> must use [high for code review; recorded setup effort for verification]. Confirm
> actual settings and workspace-write environment; report inability to verify or
> apply them. Implementation and remediation are medium in separate turns; do
> not edit code here. Temporary approvals in the parent are not permissions here.
>
> Standing authorization covers in-scope inspection, required safe environment
> setup/tests/checks, requirements assessment and summary without an added approval
> gate, and gh comments
> on [exact issue/PR]. For verification, post findings and apply configured
> [in-progress → verified] labels only if all material acceptance criteria pass;
> leave verified unapplied while any post-merge criterion is pending. Report a
> pre-merge pass separately; documented post-merge checks alone do not block a PR.
> For review, post inline/summary feedback using COMMENT, then mark the draft PR
> ready only after independently checking current-head tests, required checks,
> verification coverage, fresh high-effort review, and no material finding or
> ambiguity. Label names: [resolved mapping]. No approval/request-changes review,
> merge, deployment, issue closure, permission expansion, or unrelated writes.
>
> A material ambiguity, unavailable permission/capability, or execution failure
> requires a blocked/failed handoff; do not ask an unattended question or claim a
> stage passed. Report exact unapplied GitHub writes in your result if posting
> fails. Preserve draft state on uncertainty and return evidence, findings,
> reviewed commit, actual model/effort, and task ID to the implementation task.

Where supported, `create_thread` accepts the resolved project, a worktree target
from the exact implementation branch/ref, and `thinking: "high"` for code review.
Verify the ref exists on the destination host; push it first if needed within the
saved authority. Pass an explicit
`model` only when setup explicitly selected one; otherwise use the configured
default and verify it matches setup. If defaults differ by task/host, stop for
interactive setup. A follow-up implementation/fix turn uses the existing task
with `thinking: "medium"`; every re-review still creates a new high-effort task.
Read the current tool schema; these names describe supported app controls, not a
shell API or permission workaround. An unavailable control blocks setup/run.
