---
name: understand-project
description: Inspect and explain an unfamiliar, inherited, or neglected repository without changing it. Use when orienting to a project, finding its architecture and canonical commands, auditing AGENTS.md, or preparing incremental mad-skills adoption.
---

# Understand a project

1. Run `mad-skills context --format json`. If the project is unconfigured, use
   `light`/`general` for this read-only task and mention that `mad-skills init`
   can configure it later.
2. Read the active `AGENTS.md` chain and concise repository documentation before
   exploring broadly. Treat checked-in instructions as authoritative project
   facts.
3. Inspect repository status and structure. Preserve unrelated work and do not
   edit files.
4. Identify, with evidence:
   - language, framework, dependency and project tooling;
   - entry points and important directories;
   - build, run, test, lint, type-check, migration, and canonical check commands;
   - architecture and recurring implementation patterns;
   - persistence, external integrations, deployment, and risky boundaries;
   - existing issues, specs, decisions, and repository-local skills.
5. Distinguish confirmed facts from inference and unknowns. Do not infer commands
   merely from ecosystem convention when the repository provides no evidence.
6. Report a compact project map, reliable commands, risks, documentation gaps,
   and the smallest useful next adoption step.

Do not rewrite documentation automatically. If `AGENTS.md` is absent or stale,
propose precise changes and wait for approval.

