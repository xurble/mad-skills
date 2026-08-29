# Repository guidance

## Purpose

This repository is the source of truth for the `mad-skills` personal Agent
Skills toolkit. Shared behavior belongs in reusable skills or policy data;
consuming repositories supply project facts through `AGENTS.md` and
`.agent/config.yaml`.

## Structure

- `skills/`: reusable Agent Skills; each requires `SKILL.md` and Codex metadata.
- `src/mad_skills/`: deterministic CLI, configuration, installation, and checks.
- `profiles/`, `bundles/`, `config/`: shared policy data and schema.
- `templates/`: issue and decision templates used by workflows.
- `docs/`: adoption and maintenance documentation.
- `tests/`: CLI and integration tests.

## Working rules

- Keep `SKILL.md` files concise and focused on one user goal.
- Put deterministic facts in the CLI rather than asking an agent to infer them.
- Never require a consuming project to edit a shared skill.
- Preserve Codex and Claude Code compatibility; use only `name` and
  `description` in `SKILL.md` frontmatter.
- GitHub-writing workflows require `gh`; do not add hidden API or connector
  fallbacks.
- Keep installation idempotent and non-destructive.
- Do not add workflow orchestration, automatic merging, or enterprise process.

## Verification

Run:

```bash
uv run mad-skills validate
uv run pytest
uv run ruff check .
```

Inspect `git diff` and preserve unrelated user work before finishing.

## Environment

The gh command should be installed and authenticated.  It needs to run outside the sandbox

