---
name: github-pull-request
description: Create a concise GitHub pull request linked to its issue after implementation is ready. Use when the user directly asks to open or create a PR, or when a rigorous workflow reaches its approved PR step.
---

# Create a GitHub pull request

1. Load effective policy. Offer `mad-skills init` when configuration is absent;
   use `light` for this task if declined. Require installed, authenticated `gh`;
   stop and ask for setup if unavailable. Do not use another GitHub integration.
2. Inspect branch, status, commits, final diff, linked issue, migrations, checks,
   and remote state. Do not include unrelated changes.
3. Stop if required tests or `commands.check` failed, if the branch is not pushed,
   or if a rigorous issue/plan is missing. Report the exact blocker.
4. Prepare a concise body containing outcome, implementation summary, important
   decisions, migrations/data/security implications, tests and verification,
   known risks, and `Closes #N` for the linked issue.
5. A direct request authorizes PR creation. Use a body file with `gh pr create` and
   return the URL. Create a draft when verification/review remains outstanding;
   mark ready only when policy requirements are satisfied.
6. Never merge automatically. Issue closure occurs through the merged linked PR
   or a separate explicit user request.
