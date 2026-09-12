# Fresh verification task or review subagent request

For verification, create a new separate task through supported Codex controls.
Select the exact current branch/ref using supported task target controls; for a
Git project use an isolated worktree, and resolve its real thread ID after
asynchronous setup before continuing or waiting on it.

For code review, spawn a fresh-context subagent within the current scheduled task
using supported subagent controls with no inherited turns. In Codex, use
`spawn_agent` with `fork_turns: "none"`; do not use `create_thread`. Never create
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
> [test/check evidence] and [independent verification evidence for review]. Do not
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
> [in-progress → verified] labels only if all material acceptance criteria pass.
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
> reviewed commit, actual model/effort, and task or subagent ID to the implementation task.

For verification, supported task creation accepts the resolved project and a
worktree target from the exact implementation branch/ref. For review, supported
subagent creation must disable inherited turns and apply `high` effort. Verify the
ref is available in the shared workspace or push it first if needed within saved
authority. Pass an explicit model only when setup explicitly selected one;
otherwise use the configured default and verify it matches setup. If defaults
differ by execution context or host, stop for interactive setup. A follow-up
implementation/fix turn uses the existing task at medium effort; every re-review
spawns a new fresh-context high-effort subagent. Read the current tool schemas;
these names describe supported controls, not a shell API or permission workaround.
An unavailable control blocks setup/run rather than permitting a fallback to a
new review chat or implementation-context self-review.
