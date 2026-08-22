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

Every rigorous project must configure `commands.check` and enable GitHub issues.

## GitHub

GitHub workflows require `gh`. The default semantic labels are configurable:

```yaml
github:
  use_issues: true
  labels:
    bug: defect
    enhancement: improvement
    actionable: ready-for-agent
```

The full managed set covers bug, enhancement, actionable, needs-investigation,
blocked, high-risk, in-progress, and verified. Technology labels are optional
additional mapping entries.

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

