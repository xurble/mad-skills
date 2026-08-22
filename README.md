# mad-skills

`mad-skills` is a personal, version-controlled toolkit of reusable Agent Skills,
project profiles, and deterministic repository checks for Codex and Claude Code.

The toolkit is intentionally small: shared workflows live here, while each
project keeps its own facts and conventions in `AGENTS.md` and optional
`.agent/config.yaml`.

## Quick start

Requirements: macOS or WSL, Git, and [uv](https://docs.astral.sh/uv/).

```bash
git clone <repository-url> mad-skills
cd mad-skills
./scripts/install --target all
```

This installs the `mad-skills` command in an editable uv tool environment and
links every shared skill into:

- `~/.agents/skills` for Codex;
- `~/.claude/skills` for Claude Code.

The links continue to point at this checkout, so a normal `git pull` updates the
skills everywhere. The installer is safe to rerun and stops on unmanaged name
conflicts.

## Adopt a project

From a project repository:

```bash
mad-skills init
mad-skills check
```

Initialization inspects the repository, proposes a project type and rigor
profile, previews the files it would create, and asks before writing. Projects
without configuration remain usable: passive guidance assumes `light`, while
action workflows offer to initialize the project on first use.

The supported profiles are `light`, `normal`, and `rigorous`. Supported project
types are `general`, `python`, `django`, and `ios`; a type selects its matching
bundle automatically.

## Commands

```text
mad-skills init                    Configure the current project
mad-skills context                Show effective project policy
mad-skills check [--full]         Check project wiring; optionally run commands.check
mad-skills validate               Validate the toolkit
mad-skills validate-project       Validate one project configuration
mad-skills list-skills            List shared skills
mad-skills install --target ...   Install Codex/Claude skill links
mad-skills setup-github           Apply configured merge settings and labels with gh
mad-skills setup-github-labels    Create missing configured labels with gh
```

GitHub workflows deliberately require the `gh` CLI. They stop with an actionable
message when `gh` is missing or unauthenticated. In Codex, run every command that
reaches GitHub outside the sandbox with escalation from the outset.

## Documentation

- [Specification](docs/specification.md)
- [Architecture](docs/architecture.md)
- [Adding a project](docs/adding-a-project.md)
- [Configuration](docs/configuration.md)
- [Issue workflow](docs/issue-workflow.md)
- [Creating skills](docs/creating-skills.md)
- [Promoting local skills](docs/promoting-local-skills.md)
- [Updating skills](docs/updating-skills.md)

## Development

```bash
uv sync --dev
uv run mad-skills validate
uv run pytest
uv run ruff check .
```
