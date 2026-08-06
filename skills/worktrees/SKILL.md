---
name: worktrees
description: >-
  Isolated git worktrees for feature work. Use when starting work that needs
  isolation from the current workspace, when the tree is dirty or conflicts
  with the task, or before executing a multi-step implementation plan.
---

# Worktrees

Keep implementation off the user's active checkout when isolation helps.
Detect existing isolation first. Prefer native harness worktree tools. Fall
back to `git worktree` only when no native tool exists.

## Step 0: Detect existing isolation

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

Submodule guard — `GIT_DIR != GIT_COMMON` is also true inside submodules:

```bash
git rev-parse --show-superproject-working-tree 2>/dev/null
```

| State | Action |
|-------|--------|
| Linked worktree (not submodule) | Use it. Do not nest another. |
| Submodule or normal checkout | Continue to create (with consent if needed) |
| User already declared preference | Honor it; don't re-ask |
| User declines isolation | Work in place |

Consent prompt when preference is unknown:

> Would you like an isolated worktree? It keeps your current branch untouched.

## Step 1: Create

### 1a. Native tool (preferred)

If the harness exposes worktree creation (`EnterWorktree`, `/worktree`,
`--worktree`, etc.), use it. Skipping native tools creates state the harness
cannot manage.

### 1b. Git fallback

Only when no native tool exists.

**Directory priority:** explicit user preference → existing `.worktrees/` →
existing `worktrees/` → default `.worktrees/`.

**Must be gitignored** before creating:

```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

If not ignored: add to `.gitignore`, commit that change, then proceed.

```bash
path="$LOCATION/$BRANCH_NAME"
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

Sandbox/permission failure → report it, work in place instead.

## Step 2: Setup + baseline

Run project setup if needed (`npm install`, `cargo build`, `pip install`,
`poetry install`, `go mod download`).

Run the project's normal test command once. Failures → report and ask whether
to proceed or investigate. Pass → ready.

```
Worktree ready at <path> on <branch>
Baseline: <pass | fail summary>
```

## Quick reference

| Situation | Action |
|-----------|--------|
| Already in linked worktree | Skip creation |
| Native tool available | Use it |
| No native tool | `git worktree add` under ignored dir |
| Dir not ignored | Fix `.gitignore` first |
| Create blocked | Work in place |
| Baseline fails | Report + ask |
