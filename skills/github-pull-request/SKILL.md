---
name: github-pull-request
description: Create a concise GitHub pull request after implementation is ready, linking an existing issue when the work is issue-driven. Use when the user directly asks to open or create a PR, or when a rigorous workflow reaches its approved PR step.
---

# Create a GitHub pull request

In Codex, run every `gh` command—and any `mad-skills` command that reaches
GitHub—outside the sandbox with escalation from the outset.

1. Load effective policy. Offer `mad-skills init` when configuration is absent;
   use `light` for this task if declined. Require installed, authenticated `gh`;
   stop and ask for setup if unavailable. Do not use another GitHub integration.
2. Inspect branch, status, commits, final diff, any existing linked issue,
   migrations, checks, and remote state. Do not include unrelated changes. When
   `git.conventional_commits` is enabled, require introduced commit messages and
   the PR title to use Conventional Commits; do not rewrite history without
   explicit authorization.
3. Stop if required tests or `commands.check` failed, if the branch is not pushed,
   or if other policy-required planning, verification, or review is missing.
   Report the exact blocker. Do not create or require an issue merely because the
   user requested a PR; treat a missing issue as a blocker only when effective
   project policy independently requires one.
4. Prepare a concise body containing the outcome, what changed, why when known,
   important decisions, migrations/data/security implications, tests and
   verification, and known risks. For issue-driven work, include `Closes #N` for
   the existing linked issue. Otherwise let the PR title and body be the durable
   record; do not invent a rationale or issue reference.
5. Confirm the repository supports `github.merge_method` and
   `github.delete_branch_on_merge`. The defaults are squash-only merging, a
   Conventional-Commit PR title plus description for the squash commit, and
   automatic remote branch deletion. Report drift and offer `mad-skills
   setup-github`; do not silently change repository settings during PR creation.
6. A direct request authorizes PR creation. Use a body file with `gh pr create`
   and return the URL. Create a draft when verification/review remains
   outstanding; mark ready only when policy requirements are satisfied.
7. Never merge automatically. When the user separately asks to merge, use the
   configured method; default to squash. Let GitHub delete the remote branch
   after merge, and do not delete a local branch without explicit authorization.
   Issue closure occurs through the merged linked PR or a separate explicit user
   request.
