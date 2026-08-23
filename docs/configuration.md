# Configuration

Project configuration lives at `.agent/config.yaml`. The JSON Schema is
`config/project-config.schema.json`; unknown keys fail validation, while
`extensions` is the explicit escape hatch for project metadata not interpreted by
the toolkit.

## Minimal configuration

```yaml
version: 1
project:
  type: django
  profile: normal
github:
  use_issues: true
commands:
  test: ./scripts/test
  check: ./scripts/check
```

Supported types are `general`, `python`, `django`, and `ios`. Supported profiles
are `light`, `normal`, and `rigorous`. Add mixed guidance with:

```yaml
project:
  type: ios
  profile: normal
  extra_bundles:
    - python
```

Bundle selection is additive; it cannot remove `general` safety workflows.

## Commands

`commands.dev`, `commands.test`, and `commands.check` are shell strings. Ordinary
`mad-skills check` verifies that their executables or paths resolve but does not
run them. `mad-skills check --full` explicitly executes `commands.check`.

Every rigorous project must configure `commands.check` and enable its GitHub
workflow. Issues remain available for backlog work, but a rigorous PR does not
require an issue. The rigorous merge gate is a standalone, well-specified PR.

## GitHub

GitHub workflows require `gh`. The default semantic labels are configurable:

```yaml
github:
  use_issues: true
  require_issue_for_nontrivial_work: false
  require_pull_request_for_nontrivial_work: true
  require_well_specified_pull_request_for_nontrivial_work: true
  open_pull_requests_as_draft_until_reviewed: true
  merge_method: squash
  squash_merge_commit_message: pr-title-description
  delete_branch_on_merge: true
  labels:
    bug: defect
    enhancement: improvement
    actionable: ready-for-agent
```

The full managed set covers bug, enhancement, actionable, needs-investigation,
blocked, high-risk, in-progress, and verified. Technology labels are optional
additional mapping entries.

`require_issue_for_nontrivial_work` is independently configurable and defaults to
false in every profile. Rigorous projects require a PR whose title and body stand
alone as the final change specification; an existing issue is linked when it
actually drove the work. They open that PR as a draft, offer a fresh-context code
review, and mark it ready after the accepted review cycle completes. An explicit
developer override may bypass the AI-review gate.

Normal projects also open non-trivial PRs as drafts because their default policy
requires separate review. High-risk work uses the rigorous draft gate in every
profile. A project may enable required PRs while leaving `use_issues` false;
repository checks and `mad-skills setup-github` still manage PR settings, while
issue-label management remains disabled.

`merge_method` selects the only enabled GitHub merge method. The defaults use a
Conventional-Commit PR title plus the PR description for the squash commit and
delete the remote head branch after merge. Apply or repair the settings and
labels with `mad-skills setup-github`. In Codex, run that command and other `gh`
work outside the sandbox with escalation from the outset.

Conventional Commits are enabled by default and can be overridden per project:

```yaml
git:
  conventional_commits: true
```

## Decisions and risk

Decision logs are not created empty. Configure a path when the first real decision
is worth preserving:

```yaml
decisions:
  log: docs/decisions.md
```

Project risk mappings supplement the shared high-risk defaults:

```yaml
risk:
  registrations: high
  report_exports: normal
```

Inspect the complete effective policy with `mad-skills context`.
