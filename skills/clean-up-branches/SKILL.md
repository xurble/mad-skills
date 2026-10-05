---
name: clean-up-branches
description: Clean up obsolete Git branches and linked worktrees, and synchronize the primary branch. Use when explicitly asked to clean up, prune, or remove merged local or remote branches or worktrees while syncing main or the default branch, including branches left unmerged by squash merges.
---

# Clean up Git branches and worktrees, and sync the primary branch

Apply [clarify-requirements](../clarify-requirements/SKILL.md) to the task's
requirements first; reuse the established requirements for the same scope.
Apply the shared [Codex GitHub command rule](../github-pull-request/references/gh-execution.md)
when checking pull requests with `gh`.

1. Inspect the repository root, status, current branch, worktrees, remotes, and
   the remote's primary branch. Scope remote cleanup to `origin` unless the user
   names another remote. Preserve uncommitted work and do not switch branches
   when that would disturb it.
2. Fetch and prune the scoped remote, then bring the local primary branch to its
   remote tip with a fast-forward-only update. Never reset it, rewrite history,
   or force-push. If it cannot fast-forward, stop and report the divergence.
3. Exclude the primary branch, the current branch and worktree, remote HEAD, and
   protected branches. A branch checked out in another worktree is eligible only
   when that worktree is clean and its exact tip passes the merge test below;
   remove the worktree before deleting the branch. Treat worktrees and local and
   remote refs independently: evidence that one is obsolete does not prove
   another is safe to remove when their tips differ.
4. Classify a candidate as safely obsolete only when its exact tip is either:
   - an ancestor of the updated remote primary branch; or
   - the recorded head commit, or an ancestor of it, of a merged pull request
     in that exact repository whose merge reached the primary branch.

   Use `gh` when available to verify squash merges. Look up pull requests
   containing the candidate's tip with
   `gh api repos/<owner>/<repo>/commits/<tip>/pulls`, keeping only those with
   `merged_at` set, `base.ref` equal to the primary branch, and
   `merge_commit_sha` an ancestor of the updated remote primary branch. Fetch
   each recorded head with `git fetch <remote> refs/pull/<N>/head`, confirm it
   equals `head.sha`, and require `git merge-base --is-ancestor <tip> <head.sha>`;
   one qualifying pull request suffices. Do not check out pull requests. A local
   branch may qualify under any name. A remote branch qualifies through a pull
   request only when it equals `head.ref` and `head.repo.full_name` is the
   scoped remote's repository.

   A matching branch name or a closed, unmerged pull request is not sufficient.
   Skip candidates with an open pull request using them as head or base,
   commits added after the merged pull request head, missing merge evidence, or
   ambiguous repository ownership.
5. Show the exact worktree removal and local and remote branch deletion sets
   before mutating them. A direct request with scope meeting the 95% confidence
   threshold authorizes removal of only the verified set; if the skill was
   selected without an explicit cleanup request, ask for approval first. Never
   remove a dirty or uncertain worktree or delete an uncertain branch.
6. Remove a verified linked worktree with `git worktree remove <path>` without
   force, then delete its branch. Delete ordinary merged local branches with
   `git branch -d`. Use
   `git branch -D` only for a locally verified squash-merged branch whose exact
   tip passed the pull-request check. Delete a verified remote branch with
   `git push <remote> --delete <branch>`, then fetch with pruning again.
7. Reinspect status, the primary branch and its upstream, worktrees, and
   remaining branches. Report what was synchronized, each worktree removed,
   each local and remote branch deleted with its evidence, and every candidate
   skipped with its reason. For a branch deleted through a pull request, give
   its deleted tip SHA and `refs/pull/<N>/head` as recovery points.
