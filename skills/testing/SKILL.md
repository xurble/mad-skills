---
name: testing
description: Select, add, and run proportionate tests for a code change using project conventions, profile, and task risk. Use during feature work, bug fixes, refactors, verification, or when deciding what evidence is sufficient before completion.
---

# Test proportionately

1. Load policy with `mad-skills context --format json`; passive use without
   configuration assumes `light`.
2. Inspect existing test organization, fixtures, tooling, and canonical commands.
   Reuse project style rather than importing a preferred framework.
3. Classify risk. High-risk work uses rigorous expectations in any project.
4. Apply profile defaults:
   - `light`: test meaningful logic where useful; do not force coverage for trivial changes;
   - `normal`: meaningful behavior changes normally need tests and bug fixes need regression coverage;
   - `rigorous`: non-trivial behavior changes require tests, focused iteration,
     and canonical validation unless genuinely impossible.
5. Prefer observable behavior and stable boundaries. Avoid brittle tests of
   framework internals or duplicate tests that add no confidence.
6. Run focused tests while iterating, then the configured canonical check when
   required. Report exact commands, outcomes, skipped checks, and limitations.

TDD is optional. Evidence and regression protection are not.

