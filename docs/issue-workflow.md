# Issue and pull-request workflow

GitHub Issues are the backlog for future work that is not yet being committed to.
Pull requests are the durable record and merge gate for work being delivered.
`gh` is the only supported GitHub client. In Codex, every direct `gh` command and
every `mad-skills` command that reaches GitHub runs outside the sandbox with
escalation from the outset.

Apply [clarify-requirements](../skills/clarify-requirements/SKILL.md) before
proceeding with requirements capture, investigation, planning, implementation, or
a request to act after discussion. Use the discussion and repository evidence,
ask focused questions whenever requirements confidence is below 95%, then present
a concise summary and wait for explicit confirmation. Read-only investigation
may continue while answers or confirmation are pending; edits, issue creation,
and other mutations wait. Reuse confirmed requirements across workflow steps,
reopening clarification only for material scope changes or new ambiguity.

```text
future work: open-bug / open-enhancement
  → create-agent-issue
  → plan-issue when required
  → implement-issue

committed work: approved chat or issue specification
  → implement
  → test and full check when required
  → separate verification against the supplied specification
  → standalone well-specified draft pull request
  → offer separate fresh-context review
  → accepted review cycle completes
  → mark pull request ready
  → merge (and close a linked issue when present)
```

Direct natural-language requests such as “open an issue” or “create a PR” authorize
the corresponding action within confirmed requirements; skill syntax is optional.
The initial request does not replace confirmation of the requirements summary.
Ambiguous discussion never authorizes a mutation.

A PR request does not authorize or require creating an issue. When a feature has
confirmed requirements from chat, implementation may proceed directly and the
PR must consolidate the accepted design into a durable standalone specification.
When an existing issue drove the work, the PR retains the issue link and closing
syntax while still recording the accepted final scope. PR titles use Conventional
Commits by default so the squash commit keeps the same form. Repository setup
enables squash-only merges and automatic remote branch deletion by default.

Bug and enhancement capture creates an issue after requirements confirmation,
without a second creation-only approval. Root cause and other evidence gaps can
remain explicitly unknown in a confirmed investigation request. Converting an
existing issue into an implementation contract always previews the replacement
body first. Planning, verification, and PR review also present their
result locally before posting an approved comment or review.

Workflow labels change from `agent-actionable` to `in-progress` to `verified`.
Classification labels remain. Failed or uncertain verification never applies
`verified`. Verification never closes an issue: only a merged PR containing
`Closes #N` or an explicit user request does so.

Rigorous non-trivial work requires an approved plan, tests, a full check, fresh
verification, and a standalone well-specified PR. The PR opens as a draft so its
state visibly records that fresh AI code review has not completed. Creating the PR
offers that review but never starts it automatically. When accepted, the review
runs in a separate Codex or Claude task; the PR is marked ready after all material
findings against the current diff are resolved. A developer may explicitly bypass
the AI-review gate and mark ready or merge, but the agent must disclose that review
was skipped and must not claim otherwise.

## Explicit nightly opt-in

[Setup nightly](../skills/setup-nightly/SKILL.md) records one project's schedule,
authorization and tested execution settings in Codex. This is the sole unattended
exception to the interactive gates above: routine summary confirmation, in-scope
plan approval/posting, commits/pushes, verification result posting, accepting the
fresh-review offer, review comments and the clean ready transition are authorized
at setup. The plan, checks, independent verification and reviews still happen.

Each standalone run skips any open PR, then selects at most one oldest actionable
issue excluding blocked/in-progress. Implement in an isolated worktree at medium;
open a draft and review in a separate new high-effort task. Permit at most three
medium-effort remediation rounds, each followed by checks/verification coverage
and a fresh high-effort review. Current-diff evidence and no unresolved material
findings/ambiguity are required for ready. Never merge automatically.

New material ambiguity stops dependent work. Meaningful partial work can become
a blocked draft PR with missing/failed plan, check and verification stages
disclosed; otherwise comment on the issue. Remove actionable and stale
in-progress/verified, apply blocked, and preserve classification labels. Never
restore actionability automatically. GitHub failures require exact unapplied
handoff content in the scheduled output. See the [complete setup and run
contract](nightly-implementation.md), including persistent permissions and trial.
