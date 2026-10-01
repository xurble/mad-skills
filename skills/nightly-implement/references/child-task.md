# Fresh verification task or review subagent request

For verification, create a new separate task through supported Codex controls.
Select the exact current branch/ref using supported task target controls; for a
Git project use an isolated worktree, and resolve its real thread ID after
asynchronous setup before continuing or waiting on it.

For code review, spawn a fresh-context subagent within the current scheduled task
using supported subagent controls with no inherited turns. In Codex, use
`spawn_agent` with `fork_turns: "none"`, the saved `model` explicitly
(`gpt-6-sol` unless the user selected another model at setup), and
`reasoning_effort: "high"`.
Never omit the model or inherit the parent model, even if the parent runs Astra;
stop if the saved model cannot be applied. Do not use
`create_thread`. Never create
a new user-visible task, thread, or chat for review. A review subagent performs
the review directly and must not delegate again.

For either operation, fill every field below with current values from trusted
setup and observed Git state. Pass plain prose in the task or subagent prompt. Do
not resume a previous verifier/reviewer or assume parent permissions.

> This is an explicitly authorized fresh [verification task/code-review subagent] for
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
> Model: [model saved at setup, with explicit user selection or Codex Sol default
> provenance]. Task controls must use high effort for this verification or
> review stage. Confirm
> actual settings and workspace-write environment; report inability to verify or
> apply them. Implementation and remediation use medium in separate turns; do
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
> verification coverage, fresh review at high effort, and no material finding or
> ambiguity. Label names: [resolved mapping]. No approval/request-changes review,
> merge, deployment, issue closure, permission expansion, or unrelated writes.
>
> A material ambiguity, unavailable permission/capability, or execution failure
> requires a blocked/failed handoff; do not ask an unattended question or claim a
> stage passed. Report exact unapplied GitHub writes in your result if posting
> fails. Preserve draft state on uncertainty and return evidence, findings,
> reviewed commit, actual model/effort, and task or subagent ID to the implementation task.

For verification, supported task creation accepts the resolved project and a
worktree target from the exact implementation branch/ref. Pass the saved model
and high effort through every verifier's task creation controls. For review,
supported subagent creation must disable inherited turns and apply high effort.
Verify the
ref is available in the shared workspace or push it first if needed within saved
authority. Pass the saved model explicitly through supported controls. If the
selected model differs by execution context or host, stop for
interactive setup. A follow-up
implementation/fix turn uses medium effort through supported controls.
Every re-review spawns a new fresh-context subagent at high effort. Read the
current tool schemas;
these names describe supported controls, not a shell API or permission workaround.
An unavailable control blocks setup/run rather than permitting a fallback to a
new review chat or implementation-context self-review.
