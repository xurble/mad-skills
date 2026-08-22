# Promote a local skill

Repository-local skills belong in `.agents/skills` for Codex and `.claude/skills`
for Claude Code. Use the same `SKILL.md` source when both harnesses need it.

Promote a local workflow only after repeated successful use:

1. Identify the reusable user goal and concrete examples.
2. Remove project names, absolute paths, commands, and architecture assumptions.
3. Move legitimate project facts into `.agent/config.yaml`, `AGENTS.md`, or project
   documentation.
4. Add and validate the central skill.
5. Test it against the original project and at least one differing context.
6. Remove the local copy and rely on the central symlinked skill.

Do not shadow a shared skill with the same name. Codex does not merge duplicates,
and Claude gives personal skills precedence over project skills. Extend under a
distinct, project-specific name or improve the central skill.

