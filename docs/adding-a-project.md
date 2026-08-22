# Add a project

## Quick adoption

From the repository root:

```bash
mad-skills init
mad-skills check
```

Initialization detects a likely project type and existing `scripts/dev`,
`scripts/test`, and `scripts/check` commands. It asks for the profile and GitHub
preference, previews every proposed file, and writes only after approval.

If `AGENTS.md` is missing, initialization proposes a concise fact-based starting
point. It never replaces an existing file. It also creates `CLAUDE.md` containing
`@AGENTS.md` when absent.

GitHub-backed initialization requires installed, authenticated `gh`, checks the
configured standard labels, and asks before creating missing labels.

## Adoption levels

- Level 0: leave the project untouched; passive skills use `light`/`general`.
- Level 1: add or improve `AGENTS.md` and the Claude import shim.
- Level 2: add `.agent/config.yaml` and reliable canonical commands.
- Level 3: enable issues, decisions, specs, and local skills where they add value.

For an old repository, run `$understand-project` before initialization. Preserve
useful local guidance; remove generic procedures only after their shared skill is
available. Adoption should return quickly to real project work.

When an inherited project has no trustworthy specification, run
`$specify-existing-project` after orientation. It reconstructs a traceable
current-state draft from implementation and tests, then raises numbered assumptions
for clarification before writing the final specification.

## New projects

Create the project normally, add concise repository guidance, initialize
`mad-skills`, and make the real build/test/check commands reliable. Do not scaffold
application architecture merely for the agent.
