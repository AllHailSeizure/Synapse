---
name: finishing-branches
description: >-
  Close out a development branch after implementation. Use when work is
  complete and tests pass — verify, confirm base branch, push, and open a PR
  with a one-line heads-up. Merge and discard stay user-initiated.
---

# Finishing Branches

Verify → confirm base → push and open PR. Do not present a multi-option
integration menu. Do not merge or discard unless the user explicitly asks.

## 1. Verify tests

Run the project's normal suite for this work (`verification`).

Failing → report failures and stop. Do not open a PR on red.

## 2. Confirm base branch

Base = whatever this work forked from (plan, conversation, upstream). If
unsure, ask once with your best guess. Wrong-base merges are expensive.

## 3. Push and open PR

```bash
git push -u origin HEAD
```

Detached HEAD: `git push origin HEAD:refs/heads/<new-branch>` then open the PR
from that branch.

Create the PR with `gh pr create` (or the forge's CLI), following the repo
template if present. Report the URL.

One-line heads-up to the user, e.g.:

> Pushed and opened PR: <url> (base: <branch>)

Keep the worktree if one exists — PR feedback lands there.

## 4. Stacked PRs

Never auto-merge. Never merge a stack out of order. Push/PR only; the user
owns merge timing.

## Merge (user-initiated only)

When the user explicitly asks to merge locally:

1. Checkout base, pull, merge the feature branch
2. Run tests on the merged result
3. Failures → stop, leave branch/worktree; investigate
4. Green → optional worktree cleanup (below); `git branch -d` when safe

## Discard (user-initiated only)

Only on an explicit discard request. Confirm the branch name and that commits
will be lost. Then:

```bash
# from main repo root, outside the worktree
git worktree remove "$WORKTREE_PATH"   # if you own it under .worktrees/ or worktrees/
git branch -D <feature-branch>
```

No typed magic word required beyond a clear yes to the confirmation.

## Worktree cleanup

| Workspace | Cleanup |
|-----------|---------|
| Normal repo (`GIT_DIR == GIT_COMMON`) | Nothing |
| Under `.worktrees/` or `worktrees/` after merge/discard | `git worktree remove` + prune |
| Harness-managed / other path | Leave it; use harness exit if any |
| After PR opened | **Keep** worktree |

## Don't

- Block on a 3-option merge/PR/keep menu
- Merge or discard without an explicit ask
- Force-push to fix a rejected push
- Assume base is `main` without checking
- Auto-merge stacked PRs
