# Architecture

`mad-skills` separates reusable workflows from project facts.

## Layers

1. `skills/` contains shared Agent Skills. A consuming project never edits them.
2. `config/`, `profiles/`, and `bundles/` define shared defaults and policy.
3. `.agent/config.yaml` contains legitimate project overrides.
4. `AGENTS.md`, project documentation, decisions, and local skills contain
   repository-specific knowledge.

The Python CLI resolves configuration in this order:

```text
defaults → selected profile → project configuration
```

`project.type` selects an additive bundle; `project.extra_bundles` may add more.
Bundle includes are resolved before their own skills, duplicates are removed, and
`general` remains part of every supported first-class type.

## Distribution

The checkout is the source of truth. `mad-skills install` creates absolute,
user-scope skill symlinks for Codex and Claude Code. Existing unmanaged paths are
never replaced. An editable uv tool install keeps the CLI pointed at this source
tree. A normal Git pull therefore updates both instructions and tooling.

Plugins are deliberately out of scope for v1: this is a personal toolkit, and a
plugin release/cache lifecycle would weaken immediate propagation and add a second
distribution model.

## Policy and risk

Profiles establish minimum workflow depth. Task risk can raise it: a high-risk
task always uses rigorous planning, testing, verification, and review expectations
as readiness gates, without adding unrequested interactive actions.
For rigorous non-trivial work, a standalone well-specified PR is the merge gate.
Issues capture future or otherwise tracked work and are not a prerequisite for a
PR. The PR opens as a draft to expose that fresh AI review is pending; review is
run only when explicitly requested. Each interactive review performs one
fresh-context subagent pass at the selected effort (high by default), then
returns control without remediation,
re-review, or a readiness transition. Interactive implementation and fixes use
medium effort by default. An explicit developer override may bypass the advisory review gate.
Trivial work remains exempt from plan and PR ceremony.

The shared [model and effort policy](../skills/clarify-requirements/references/model-effort.md)
selects Codex Sol or Claude Opus at high effort for capture, planning,
verification and review, and medium effort for implementation and fixes. An
explicit user choice overrides the corresponding default. Each stage announces
its actual settings before work and applies them through supported controls.

The CLI checks objective facts—schema, paths, installation, labels, and commands.
Skills handle judgment—risk classification, issue quality, implementation, and
review. The project and GitHub remain sources of truth; there is no workflow engine.

## Opt-in scheduled work

`setup-nightly` and `nightly-implement` provide a bounded exception to interactive
approval and review-offer gates. Trusted Codex task instructions carry explicit
authorization for one project and one selected issue per run. Codex owns schedules,
task model/effort controls, permissions, worktrees and run history. The CLI adds
only read-only deterministic candidate selection; it never runs a workflow,
stores permission grants, or enables schedules during installation.

Required evidence and independent assessments remain mandatory. Implementation
and fixes use medium effort; requirements screening, planning, verification and
fresh-context code-review subagents use high effort on the saved model (user-selected
or Codex Sol default). Setup inspects required configuration and persistent
permissions, then
activates the task without a trial run; operational failures are handled by the
scheduled run's failed/blocked handoff. See the [nightly contract](nightly-implementation.md).
Other hosts keep interactive skills.

## Portability

Skills use the common `SKILL.md` format with only `name` and `description` in
frontmatter. Codex UI metadata lives in `agents/openai.yaml`. Projects use
`AGENTS.md` as authoritative guidance and a one-line `CLAUDE.md` import shim.

Supported environments are macOS and WSL. Native Windows is not a v1 target.
