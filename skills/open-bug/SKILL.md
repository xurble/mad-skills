---
name: open-bug
description: Create a durable GitHub issue for a suspected or confirmed defect. Use when the user directly asks to open, file, capture, or record a bug for later investigation or implementation; do not create an issue from tentative discussion alone.
---

# Open a bug

1. Run `mad-skills context --format json`. If `.agent/config.yaml` is absent,
   offer `mad-skills init`; if declined, use `light` for this task.
2. Require `gh` and run `gh auth status`. If either fails, stop and ask the user
   to install or authenticate `gh`. Do not use another GitHub integration.
3. Capture only supported facts:
   - concise title;
   - `confirmed defect`, `suspected defect`, or `needs investigation`;
   - observed and expected behavior;
   - reproduction, environment, evidence, impact, workaround, and unknowns;
   - possible data-loss or security implications;
   - observable acceptance criteria where the expected outcome is known.
4. Never invent reproduction steps, evidence, severity, or root cause. Ask only
   when a missing answer would materially change the record; otherwise write
   `Unknown` or preserve the uncertainty.
5. Read the issue template from
   `<resolved.toolkit_root>/templates/bug-issue.md`. Scale detail to profile and
   risk; keep `light` issues short.
6. Write the body to a temporary file and create the issue with `gh issue create
   --body-file`. Apply configured `bug`; use `needs-investigation` and
   `high-risk` only when supported.
7. Because the user's direct request authorizes creation, do not add a redundant
   preview step when the issue is sufficiently grounded. Return the issue URL
   and summarize preserved unknowns.

