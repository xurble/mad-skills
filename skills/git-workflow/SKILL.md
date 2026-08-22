---
name: git-workflow
description: Apply safe Git practices while implementing or preparing a change. Use for branch, worktree, staging, commit, diff, and handoff decisions, especially with dirty worktrees, parallel tasks, or changes intended for a pull request.
---

# Use Git safely

1. Inspect repository root, current branch, status, and relevant diff before acting.
2. Treat existing modifications and untracked files as user work. Do not discard,
   overwrite, stage, or reformat unrelated changes.
3. Use a focused branch when policy requires a PR. Use the configured branch
   prefix when non-empty; otherwise follow the host or repository convention.
4. Use a worktree when parallel work, unrelated dirty changes, substantial scope,
   or risky experimentation makes isolation useful. Do not require it for an
   ordinary clean change.
5. Never commit secrets. Stage explicit logical paths rather than broad unrelated
   sets. Create focused, understandable commits only when the user requests them.
6. Inspect the final diff and status. Report unstaged, untracked, or unrelated
   work clearly.
7. Never force-push, rewrite history, delete branches/worktrees, or perform a
   destructive reset without explicit authorization and verified targets.
