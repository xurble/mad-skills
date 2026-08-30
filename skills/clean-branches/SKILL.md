---
name: clean-branches
description: Clean obsolete Git branches and synchronize the primary branch. Use when explicitly asked to prune merged local or remote branches while syncing main or the default branch, including branches left unmerged by squash merges.
---

# Sync the primary branch and clean obsolete branches

1. Inspect the repository root, status, current branch, worktrees, remotes, and
   the remote's primary branch. Scope remote cleanup to `origin` unless the user
   names another remote. Preserve uncommitted work and do not switch branches
   when that would disturb it.
2. Fetch and prune the scoped remote, then bring the local primary branch to its
   remote tip with a fast-forward-only update. Never reset it, rewrite history,
   or force-push. If it cannot fast-forward, stop and report the divergence.
3. Exclude the primary branch, the current branch, remote HEAD, protected
   branches, and every branch checked out in any worktree. Treat local and
   remote refs independently: evidence that one is obsolete does not prove the
   other ref is safe to delete when their tips differ.
4. Classify a candidate as safely obsolete only when its exact tip is either:
   - an ancestor of the updated remote primary branch; or
   - the recorded head commit of a merged pull request for that exact repository
     and head branch.

   Use `gh` when available to verify squash merges. A matching branch name or a
   closed, unmerged pull request is not sufficient. Skip candidates with an open
   pull request, commits added after the merged pull request, missing merge
   evidence, or ambiguous repository ownership.
5. Show the exact local and remote deletion sets before mutating them. A direct
   request to run this skill authorizes deletion of only the verified set; if
   the skill was selected without an explicit cleanup request, ask for approval
   first. Never remove a worktree or delete an uncertain branch.
6. Delete ordinary merged local branches with `git branch -d`. Use
   `git branch -D` only for a locally verified squash-merged branch whose exact
   tip passed the pull-request check. Delete a verified remote branch with
   `git push <remote> --delete <branch>`, then fetch with pruning again.
7. Reinspect status, the primary branch and its upstream, worktrees, and
   remaining branches. Report what was synchronized, each local and remote
   branch deleted, and every candidate skipped with its reason.
