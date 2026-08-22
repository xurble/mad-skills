# Create a shared skill

Add a shared skill only after a concrete workflow has proved reusable.

1. Give it one recognizable user goal and a lowercase hyphenated name.
2. Create `skills/<name>/SKILL.md` with only `name` and `description` frontmatter.
3. Put all trigger wording in the description. Keep the body imperative and under
   500 lines.
4. Add deterministic scripts, focused references, or output assets only when they
   reduce repeated work or ambiguity.
5. Generate matching Codex UI metadata at `agents/openai.yaml`.
6. Add it to the smallest appropriate bundle.
7. Run `mad-skills validate` and forward-test realistic prompts in a consuming
   repository.

Do not add a per-skill README, copy shared policy into every body, or bake in a
consuming project's assumptions. Prefer project config, `AGENTS.md`, and runtime
inspection.

