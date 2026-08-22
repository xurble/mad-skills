# mad-skills Specification

**Status:** Normative  
**Configuration version:** 1  
**Primary agent:** Codex  
**Compatible agent:** Claude Code  
**Supported hosts:** macOS and Windows Subsystem for Linux (WSL)

This document defines `mad-skills` as an established personal engineering
toolkit. It is the source of truth for product behavior, policy, distribution,
and future evolution. The root bootstrap document records the project's origin
and is retained only as historical source material.

The words **must**, **should**, and **may** express required, recommended, and
optional behavior respectively.

## 1. Purpose

`mad-skills` provides reusable Agent Skills, project profiles, deterministic
checks, and small project-specific configuration for software work across a
personal portfolio.

It must make agent-assisted development safer and more consistent without
forcing the same amount of process onto every repository. A small hobby project
must remain lightweight, while an important or high-risk project can require
issues, planning, tests, independent verification, review, and pull requests.

The product, repository, Python package, and command-line program are all named
`mad-skills`.

## 2. Product principles

- Shared workflows live in this repository and improve centrally.
- Project facts and conventions remain in each project's `AGENTS.md`,
  `.agent/config.yaml`, documentation, and local skills.
- Codex is the reference agent. Claude Code compatibility must not complicate
  the Codex-first design.
- Native agent mechanisms are preferred over custom infrastructure.
- Deterministic software checks objective facts; skills handle judgment.
- Profiles establish minimum ceremony, and task risk can increase it.
- Natural-language requests are first-class; users need not name a skill.
- Existing repositories adopt the toolkit incrementally.
- The toolkit stays small enough to maintain as part of ordinary project work.

## 3. Scope and non-goals

The toolkit includes:

- shared general and technology-specific skills;
- `light`, `normal`, and `rigorous` profiles;
- additive skill bundles;
- a strict, versioned project configuration schema;
- installation and discovery for Codex and Claude Code;
- deterministic toolkit and repository checks;
- GitHub issue and pull-request workflows using `gh`;
- guidance for project adoption, local skills, and consequential decisions.

The toolkit does not provide:

- enterprise change management or mandatory release management;
- a package manager, workflow engine, agent harness, or marketplace;
- complex automatic multi-agent orchestration;
- native Windows support outside WSL;
- mandatory issues, plans, pull requests, TDD, or decision records for trivial
  work;
- one prescribed application architecture for all projects;
- plugin-based distribution in version 1.

## 4. Architecture

The system has four layers:

1. `skills/` contains reusable Agent Skills.
2. `config/`, `profiles/`, and `bundles/` define shared defaults and policy.
3. A consuming repository's `.agent/config.yaml` contains legitimate project
   overrides.
4. Its `AGENTS.md`, documentation, decisions, and local skills contain
   repository-specific knowledge.

Configuration resolves in this order:

```text
shared defaults -> selected profile -> project configuration
```

The repository layout is:

```text
mad-skills/
  .agent/config.yaml
  AGENTS.md
  CLAUDE.md
  README.md
  CHANGELOG.md
  LICENSE
  pyproject.toml
  uv.lock
  bundles/
  config/
  docs/
  examples/
  profiles/
  scripts/
  skills/
  src/
  templates/
  tests/
```

The project and GitHub remain the durable sources of truth. The CLI does not
maintain a separate workflow state database.

## 5. Runtime and host support

The CLI must support Python 3.11 or newer and use `uv` for environment,
dependency, and tool management.

Supported hosts are:

- macOS;
- WSL on Windows.

Native Windows is not supported. Shared Python code must remain portable across
the supported hosts. Platform-specific commands belong in project configuration
or documented project guidance rather than hidden assumptions in shared skills.

## 6. Distribution and updates

This Git checkout is the single source of truth. Installation creates absolute,
user-scope symlinks for every shared skill:

- `~/.agents/skills/<skill>` for Codex;
- `~/.claude/skills/<skill>` for Claude Code.

The CLI is installed into an editable `uv` tool environment. Skill links and the
CLI therefore continue to use the checked-out source after updates.

Installation must be idempotent. It must inspect all destinations before making
changes and stop on an unmanaged name conflict rather than overwrite or adopt the
path silently. Installation should be tested against temporary destinations
before the live user-scope installation is changed.

Updates use normal Git operations, normally `git pull`. There is no custom update
command, release pinning system, or second distribution lifecycle in version 1.

## 7. Agent and repository integration

`AGENTS.md` is the authoritative repository-specific instruction file. It should
remain concise and describe:

- what the project is;
- its important technology and directories;
- canonical development, test, and check commands;
- material conventions and dangerous areas;
- where specifications and decisions live.

Generic workflows belong in shared skills, not duplicated into every project.

Claude Code compatibility uses a minimal root `CLAUDE.md` containing:

```text
@AGENTS.md
```

Repository-local skills may coexist with shared skills. They should extend or
compose shared behavior rather than copy shared skills for routine editing.

## 8. Project profiles

Every configured project selects one profile. A profile sets the minimum
workflow depth; task risk may raise it.

### `light`

Use for experiments, small scripts, prototypes, and low-risk maintenance.

Typical flow:

```text
understand -> implement -> relevant checks -> inspect diff -> finish
```

Issues, written plans, pull requests, and independent review are optional unless
task risk requires them.

### `normal`

Use for active personal projects where regressions matter.

Typical flow:

```text
understand -> durable issue when useful -> implement -> test -> verify
-> fresh review for meaningful changes
```

Meaningful behavior changes normally receive tests. Bug fixes normally receive
regression coverage. Issues, plans, and pull requests follow project policy and
the significance of the task.

### `rigorous`

Use for production-facing, security-sensitive, financially consequential, or
otherwise important projects.

Every non-trivial task requires:

1. a durable issue;
2. an implementation-ready contract with acceptance criteria;
3. a written plan presented to the user, then posted to the issue after approval;
4. implementation on a pull-request branch;
5. proportionate tests and the configured full check;
6. verification against the issue in a separate fresh task;
7. code review in another separate fresh task;
8. a pull request linked with `Closes #N`.

Trivial changes remain exempt from ceremony that adds no safety.

## 9. Task risk

The implementer must infer and state task risk. It asks the user only when a real
ambiguity would change the workflow.

The following areas are high risk by default:

- authentication and authorization;
- payments;
- destructive migrations;
- production data;
- synchronization semantics;
- security boundaries.

Projects may add domain-specific risk mappings. A high-risk task always uses the
planning, testing, fresh verification, and fresh review expectations of the
rigorous profile. GitHub-specific steps apply only when the repository uses
GitHub.

## 10. Project configuration

Project configuration lives at `.agent/config.yaml` and conforms to
`config/project-config.schema.json`.

The schema is strict. Unknown keys fail validation. `extensions` is the only
escape hatch for project metadata that the toolkit does not interpret.

Supported project types are:

```text
general
python
django
ios
```

Supported profiles are:

```text
light
normal
rigorous
```

`project.type` selects its base bundle. `project.extra_bundles` adds bundles; it
never removes the `general` bundle or its safety workflows.

Commands remain explicit shell strings:

```yaml
commands:
  dev: ./scripts/dev
  test: ./scripts/test
  check: ./scripts/check
```

Projects should reuse their existing canonical tooling when wrappers provide no
benefit. Native Xcode and `xcodebuild` commands are valid for iOS projects.

Every rigorous project must configure `commands.check` and enable GitHub issues.
An ordinary repository check validates that configured commands resolve without
executing them. A full check explicitly executes `commands.check`.

## 11. Initialization and unconfigured repositories

`mad-skills init` adopts a repository interactively. It must:

1. inspect repository structure, languages, and existing guidance;
2. suggest a project type and profile;
3. preserve useful existing instructions;
4. propose a concise `AGENTS.md` when one is missing;
5. propose `.agent/config.yaml` and a `CLAUDE.md` import shim;
6. identify canonical test and check commands;
7. inspect configured GitHub labels and ask before creating missing ones;
8. preview changes and ask before writing.

Initialization does not create an empty decision log. A log begins only when a
real decision is worth preserving.

An unconfigured repository remains usable. Passive skills assume `light` and
general guidance. On the first action workflow, the skill offers
`mad-skills init`. If the user declines, the current task proceeds with `light`
policy and does not persist a preference.

## 12. Bundles

The `general` bundle is always present and contains:

```text
understand-project
specify-existing-project
repo-health
open-bug
open-enhancement
create-agent-issue
plan-issue
implement-issue
verify-issue
review-change
systematic-debugging
testing
record-decision
git-workflow
github-pull-request
```

Technology bundles are additive:

```text
python = general + python-development
django = general + python-development + django-development
ios = general + ios-development
```

New first-class project types must include `general` and should be added only
after repeated real-project use demonstrates a distinct body of reusable
guidance.

## 13. Shared skill contracts

Every shared skill uses a `SKILL.md` file with only `name` and `description` in
frontmatter. Codex-specific UI metadata belongs in `agents/openai.yaml`.
Descriptions must be concise and precise enough for reliable implicit
activation.

### Project understanding and specification

- `understand-project` inspects and explains an unfamiliar repository without
  changing it. It identifies architecture, canonical commands, local guidance,
  and adoption opportunities.
- `specify-existing-project` derives an as-built behavioral and product
  specification when documentation is missing or stale. It treats implementation
  as evidence rather than unquestionable intent, distinguishes observed behavior
  from inferred intent and suspected defects, and raises every material ambiguity
  as a numbered assumption for user clarification before finalizing the document.
- `repo-health` deterministically reports whether a repository is correctly wired
  into `mad-skills` and returns an actionable readiness result.

### Durable work capture

- `open-bug` creates a concise issue for a grounded suspected or confirmed defect.
- `open-enhancement` creates a concise issue for a grounded feature, improvement,
  refactor, or future idea.
- A direct request to open either kind of issue creates it immediately when the
  available facts are sufficient.
- `create-agent-issue` refines an existing issue into a standalone implementation
  contract with scope, constraints, acceptance criteria, and verification notes.
  A substantial issue-body replacement is previewed before it is applied.
- `plan-issue` investigates without changing code, presents a practical plan
  first, and posts it as an issue comment only after approval.

### Implementation, verification, and review

- `implement-issue` works from explicit acceptance criteria, applies the selected
  profile and task risk, preserves unrelated changes, tests proportionately, and
  reports evidence.
- `verify-issue` runs in a separate fresh task, checks the completed change against
  every acceptance criterion, presents its finding first, and posts the approved
  result and label changes afterward.
- `review-change` runs in a separate fresh task and reviews correctness,
  maintainability, complexity, likely defects, data-loss or security risk,
  architecture, and important missing tests. It presents findings first and posts
  a pull-request review only after approval. “No significant issues found” is a
  valid result.
- Verification and review are different responsibilities and do not substitute
  for each other.

Fresh verification and review are separate Codex or Claude Code tasks. They are
not automatically delegated to a subagent from the implementation conversation.

### Engineering practice

- `systematic-debugging` reproduces a failure where possible, gathers evidence,
  identifies the failing boundary, tests hypotheses, finds root cause, makes the
  smallest appropriate fix, adds useful regression coverage, and verifies it.
- `testing` selects proportionate tests using existing project conventions. It
  does not mandate TDD or brittle framework-internal tests.
- `record-decision` records only significant choices with meaningful alternatives,
  reversal cost, compatibility constraints, or context future maintainers would
  otherwise lose.
- `git-workflow` inspects status, preserves unrelated work, prevents secret
  commits, encourages focused commits, and uses worktrees when parallel or risky
  work makes them useful.
- `github-pull-request` creates a concise PR covering outcome, implementation,
  known rationale, important decisions, migrations, security implications,
  tests, and risks. It links an existing issue for issue-driven work, but a PR
  request alone neither requires nor authorizes creating one.

### Technology guidance

- `python-development` favors conventional Python, useful typing, existing
  dependency tooling, small abstractions, proportionate tests, and appropriate
  logging.
- `django-development` favors Django-native facilities and existing project
  patterns without forcing DRF, service layers, or one architecture.
- `ios-development` inspects platform availability, SwiftUI or UIKit, concurrency,
  persistence, navigation, packages, build configuration, and tests without
  forcing MVVM, coordinators, or clean architecture.

## 14. GitHub workflow

GitHub Issues are the durable work record when enabled. `gh` is the only supported
GitHub client. Every GitHub workflow must stop and ask the user to install `gh` or
authenticate it when the required state is missing; it must not fall back to a
connector or an alternative client.

The standard semantic labels are:

```text
bug
enhancement
agent-actionable
needs-investigation
blocked
high-risk
in-progress
verified
```

Projects may map these semantics to different label names. Initialization checks
for missing configured labels and asks before creating them.

The normal lifecycle is:

```text
capture issue -> make actionable -> approve plan -> in-progress
-> implement -> verify -> review -> pull request -> merge
```

Workflow labels progress from `agent-actionable` to `in-progress` to `verified`.
Classification labels such as `bug` or `enhancement` remain in place. Failed or
uncertain verification never applies `verified`.

Verification never closes an issue. An issue closes only when:

- a merged pull request contains `Closes #N`; or
- the user explicitly asks for closure.

## 15. Invocation and mutation authority

Skills may activate implicitly from ordinary language. A clear imperative such as
“open an issue for this” or “create a PR” authorizes the smallest corresponding
mutation in the named repository. Explicit `$skill-name` syntax is optional.

Tentative discussion, brainstorming, or ambiguous language does not authorize a
mutation. The agent must ask before changing durable external state when intent is
unclear. Preview and approval requirements defined by a skill still apply even
when activation is implicit.

## 16. CLI contract

The public command surface is:

```text
mad-skills init
mad-skills context [--format text|json]
mad-skills check [--full]
mad-skills validate
mad-skills validate-project
mad-skills list-skills
mad-skills install --target codex|claude|all
mad-skills setup-github-labels
```

Command behavior:

- `init` performs interactive project adoption with previews.
- `context` displays the effective merged policy, bundles, and skills.
- `check` validates project wiring without running the configured full command.
- `check --full` additionally executes `commands.check`.
- `validate` checks the toolkit's own structure and cross-references.
- `validate-project` validates a project configuration against the schema and
  policy invariants.
- `list-skills` lists discoverable shared skills.
- `install` installs user-scope skill links and the editable CLI.
- `setup-github-labels` uses `gh` to create missing configured labels after
  confirmation.

Objective checks should return concise results such as `READY`,
`READY WITH WARNINGS`, `NOT READY`, or `VALID`, together with actionable findings.

## 17. Deterministic validation

Software must validate objective facts wherever practical, including:

- schema conformance and policy invariants;
- skill structure and metadata;
- profile and bundle references;
- missing or duplicate skills;
- configured command resolution;
- installation destinations and symlinks;
- GitHub CLI availability, authentication, and configured labels;
- repository integration files.

The toolkit's canonical development checks are:

```bash
uv run ruff check .
uv run pytest
uv run mad-skills validate
mad-skills check
```

Skills must not replace a deterministic check with subjective inspection when the
fact is machine-verifiable.

## 18. Local skills and promotion

A repository-local skill is appropriate for project-specific domain workflows.
It should be promoted into `mad-skills` only after repeated use demonstrates
general value.

Promotion must:

1. remove project-specific assumptions;
2. move legitimate variability into project context or configuration;
3. test the shared form against the originating project;
4. switch the project to the central skill;
5. avoid retaining an edited local copy.

Hypothetical skills are not added preemptively.

## 19. Decision records

Consequential design choices should be recorded when they have meaningful
alternatives, high reversal cost, compatibility constraints, or rationale likely
to disappear from chat history. Routine implementation choices do not require a
decision record.

The decision-log location is project-configurable. No project or initializer
creates an empty log merely to satisfy a template.

## 20. Future evolution

Future work must preserve the following rules:

- Improve existing shared skills before creating overlapping ones.
- Add a project type only after proven repeated use and include `general` in its
  bundle.
- Keep skill descriptions concise so implicit activation remains predictable.
- Move detailed or conditional guidance into skill references rather than making
  every `SKILL.md` large.
- Add scripts only for deterministic, repeatable operations.
- Test changes on both supported host families when portability is affected.
- Version any incompatible configuration change and provide a migration path.
- Retain `gh` as the only GitHub client until this specification is deliberately
  revised.
- Keep fresh verification and review as separate user-visible tasks.
- Do not add plugins, release pinning, hooks, MCP integrations, or orchestration
  until demonstrated need outweighs the added lifecycle and maintenance cost.
- Record consequential changes to these contracts in the decision log and update
  this specification in the same change.

## 21. Acceptance criteria

`mad-skills` conforms to this specification when:

- a user can install it safely for Codex, Claude Code, or both;
- shared skill improvements propagate from the checkout without copying files;
- a repository can adopt it interactively or use passive light guidance before
  configuration;
- all project configuration is strictly validated and effective policy is
  inspectable;
- general, Python, Django, and iOS projects resolve the correct additive skills;
- high-risk tasks receive rigorous safety regardless of project profile;
- clear natural-language commands invoke the relevant skill safely;
- GitHub operations use `gh`, preserve approval boundaries, and follow the label
  and closure lifecycle;
- a fresh task can implement an actionable issue without the originating chat;
- separate fresh tasks can verify the specification and review the code;
- an inherited project can be specified from implementation while surfacing
  uncertain intent as explicit assumptions;
- deterministic validation catches malformed skills, configuration, bundles,
  installation, and repository wiring;
- small projects retain low ceremony and important projects gain proportionate
  planning, testing, verification, and review;
- toolkit tests, lint, validation, and repository health checks pass.
