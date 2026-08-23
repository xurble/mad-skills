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
task always uses rigorous planning, testing, verification, and review expectations.
For rigorous non-trivial work, a standalone well-specified PR is the merge gate.
Issues capture future or otherwise tracked work and are not a prerequisite for a
PR. The PR opens as a draft to expose that fresh AI review is pending; review is
offered rather than started automatically, and an explicit developer override may
bypass that advisory gate. Trivial work remains exempt from plan and PR ceremony.

The CLI checks objective facts—schema, paths, installation, labels, and commands.
Skills handle judgment—risk classification, issue quality, implementation, and
review. The project and GitHub remain sources of truth; there is no workflow engine.

## Portability

Skills use the common `SKILL.md` format with only `name` and `description` in
frontmatter. Codex UI metadata lives in `agents/openai.yaml`. Projects use
`AGENTS.md` as authoritative guidance and a one-line `CLAUDE.md` import shim.

Supported environments are macOS and WSL. Native Windows is not a v1 target.
