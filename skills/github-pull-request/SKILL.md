---
name: github-pull-request
description: Create a well-specified draft GitHub pull request, offer fresh-context review, mark it ready after the review cycle, or merge it on explicit request. Link an existing issue only when the work is issue-driven. Use when the user asks to open, create, ready, or merge a PR, or when a rigorous workflow reaches its PR gate.
---

# Create or merge a GitHub pull request

In Codex, run every `gh` command—and any `mad-skills` command that reaches
GitHub—outside the sandbox with escalation from the outset.

1. Load effective policy. Offer `mad-skills init` when configuration is absent;
   use `light` for this task if declined. Require installed, authenticated `gh`;
   stop and ask for setup if unavailable. Do not use another GitHub integration.
2. Inspect branch, status, commits, final diff, any existing linked issue,
   migrations, checks, task risk, and remote state. High-risk work uses rigorous
   safety in every profile. Do not include unrelated changes. When
   `git.conventional_commits` is enabled, require introduced commit messages and
   the PR title to use Conventional Commits; do not rewrite history without
   explicit authorization.
3. Stop if required tests or `commands.check` failed, if the branch is not pushed,
   or if policy-required planning or verification is missing. A missing fresh code
   review does not block draft PR creation; it keeps the PR in draft. Report other
   exact blockers. Never create or require an issue merely because the user
   requested a PR; treat a missing issue as a blocker only when effective project
   policy explicitly requires one.
4. When policy requires a well-specified PR or task risk is high, make its title
   and body a standalone change contract that does not depend on the originating
   chat or an issue. State the desired outcome and motivation, scope and material
   non-goals, observable acceptance criteria, what changed, important decisions,
   validation evidence, and relevant migrations, data/security implications,
   rollout, and known risks. Keep inapplicable sections out and do not invent
   rationale. For issue-driven work, include `Closes #N`, but consolidate the
   accepted final specification in the PR instead of making reviewers reconstruct
   it from the issue history.
5. Confirm the repository supports `github.merge_method` and
   `github.delete_branch_on_merge`. The defaults are squash-only merging, a
   Conventional-Commit PR title plus description for the squash commit, and
   automatic remote branch deletion. Report drift and offer `mad-skills
   setup-github`; do not silently change repository settings during PR creation.
6. A direct request authorizes PR creation. Use a body file and return the URL.
   Open with `gh pr create --draft` and offer a fresh-context code review when task
   risk is high, or when the change is non-trivial and either policy sets
   `github.open_pull_requests_as_draft_until_reviewed` or effective policy requires
   separate review. Do not start that review automatically. Otherwise create the
   PR in the non-draft state allowed by effective policy; trivial work does not
   inherit a profile's non-trivial review gate.
7. When the user accepts the review offer, use `review-change` in a separate fresh
   task. Keep the PR draft while material findings remain. After fixes, repeat
   relevant checks and fresh review against the current diff. When the cycle has
   no unresolved material findings, mark the PR ready with `gh pr ready` and
   report the transition. If the user declines or does not accept the offer, leave
   the PR draft.
8. Never merge automatically. When the user separately asks to merge, use the
   PR as the merge gate: reload its current title, body, diff, checks, and reviews,
   and stop if hard evidence is missing or the PR does not meet the standalone
   specification requirement imposed by effective policy or high task risk. A
   direct request to skip AI review, mark ready, or merge an unreviewed draft
   explicitly overrides only the fresh-review gate: call out the skipped review,
   never claim it happened, and mark ready if GitHub requires it before using the
   configured merge method. Default to squash. Let GitHub delete the remote branch
   after merge, and do not delete a local branch without explicit authorization.
   Issue closure occurs through the merged linked PR or a separate explicit user
   request.
