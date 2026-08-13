"""Guarded Git mutations used by weedeat's automatic safe-tier pass."""

from __future__ import annotations

import subprocess


def _run(root: str, *args: str) -> tuple[bool, str]:
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )
    message = (result.stdout if result.returncode == 0 else result.stderr).strip()
    if not message:
        message = "completed" if result.returncode == 0 else "git command failed"
    return result.returncode == 0, message


def prune_worktree(root: str, entry: dict) -> tuple[bool, str]:
    """Remove an automatically classified SAFE worktree."""
    assert entry["tier"] == "SAFE", "automatic pruning requires a SAFE worktree"
    return _run(root, "worktree", "remove", "--force", entry["path"])


def prune_branch(root: str, entry: dict) -> tuple[bool, str]:
    """Delete a merged, unattached local branch with nothing unpushed."""
    assert entry["merged"], "automatic pruning requires a merged branch"
    assert not entry["unpushed"], "automatic pruning rejects unpushed commits"
    assert not entry["checked_out"], "automatic pruning rejects checked-out branches"
    return _run(root, "branch", "-D", entry["branch"])


def prune_reviewed_worktree(root: str, entry: dict) -> tuple[bool, str]:
    """Remove a non-safe worktree after an explicit interactive confirmation."""
    assert entry["tier"] in ("STALE", "REVIEW", "HOLD")
    assert not entry.get("locked"), "locked worktrees are never deletion candidates"
    return _run(root, "worktree", "remove", "--force", entry["path"])


def prune_reviewed_branch(root: str, branch: str) -> tuple[bool, str]:
    """Delete a branch after its non-safe worktree was explicitly confirmed."""
    assert branch, "detached worktrees have no branch to delete"
    return _run(root, "branch", "-D", branch)
