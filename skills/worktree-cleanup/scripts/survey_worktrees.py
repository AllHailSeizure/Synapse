#!/usr/bin/env python3
"""Survey every git worktree and branch in this repo and classify removal safety.

Read-only by design: this prints findings and the commands that would act on
them. It never runs a removal itself, because the destructive step needs a human
who can recognize which parked WIP still matters.

Repo-specific knowledge (where worktrees live, which uncommitted paths carry no
work) comes from `.synapse/weedeat.toml`. Without it the survey runs on generic
defaults, which is correct but treats every uncommitted file as real work.

Usage:
    python scripts/survey_worktrees.py [--json out.json] [--no-fetch]
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

DEFAULT_CONTAINERS = [".claude/worktrees", ".worktrees", "worktrees"]

# Worktrees other tools create and may be actively using. Reported, never
# proposed for removal. Tool-level rather than repo-level, so it holds up as a
# default anywhere.
DEFAULT_FOREIGN = [".cursor", ".codex", ".vscode"]

DEFAULT_PROTECTED = ["master", "main"]


def git(*args: str, cwd: str | None = None) -> str:
    return _git_raw(*args, cwd=cwd).strip()


def _git_raw(*args: str, cwd: str | None = None) -> str:
    """Unstripped output.

    `git status --porcelain` encodes state in fixed columns, and its first line
    often begins with a space (` M file`). Stripping the whole blob eats that
    space and shifts the filename by one character, so status parsing uses this.
    """
    result = subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )
    return result.stdout


def repo_root() -> str:
    return git("rev-parse", "--show-toplevel")


def load_config(root: str) -> dict:
    """Read `[worktrees]` out of .synapse/weedeat.toml. Absent file is not an error."""
    path = Path(root) / ".synapse" / "weedeat.toml"
    if not path.is_file():
        return {}
    try:
        import tomllib
    except ImportError:
        print(f"{path} found but this Python has no tomllib (needs 3.11+); "
              "continuing on generic defaults.", file=sys.stderr)
        return {}
    try:
        return tomllib.loads(path.read_text(encoding="utf-8")).get("worktrees", {})
    except (tomllib.TOMLDecodeError, OSError) as exc:
        print(f"Could not read {path}: {exc}; continuing on generic defaults.",
              file=sys.stderr)
        return {}


def list_worktrees(root: str) -> list[dict]:
    """Parse `git worktree list --porcelain` into records."""
    out = git("worktree", "list", "--porcelain", cwd=root)
    trees, current = [], {}
    for line in out.splitlines():
        if not line.strip():
            if current:
                trees.append(current)
                current = {}
            continue
        key, _, value = line.partition(" ")
        if key == "worktree":
            current["path"] = value
        elif key == "branch":
            current["branch"] = value.replace("refs/heads/", "")
        elif key == "HEAD":
            current["head"] = value
        elif key == "detached":
            current["detached"] = True
        elif key == "locked":
            current["locked"] = True
    if current:
        trees.append(current)
    return trees


def real_dirt(path: str, noise_suffixes: tuple[str, ...],
              noise_dirs: tuple[str, ...]) -> list[str]:
    """Uncommitted files in a worktree, excluding configured regenerable noise."""
    if not os.path.isdir(path):
        return []
    out = _git_raw("status", "--porcelain", cwd=path)
    dirt = []
    for line in out.splitlines():
        if len(line) < 4:
            continue
        name = line[3:].strip().strip('"')
        # Renames report "old -> new"; the destination is what exists on disk.
        if " -> " in name:
            name = name.split(" -> ", 1)[1]
        if noise_suffixes and name.endswith(noise_suffixes):
            continue
        if any(name.startswith(d) for d in noise_dirs):
            continue
        dirt.append(name)
    return dirt


def unpushed_count(root: str, ref: str) -> int:
    """Commits on `ref` that exist on no origin branch — unrecoverable if deleted."""
    if not ref:
        return 0
    out = git("rev-list", "--count", ref, "--not", "--remotes=origin", cwd=root)
    return int(out) if out.isdigit() else 0


def gh_pr_heads(state: str, limit: int) -> tuple[set[str], bool]:
    result = subprocess.run(
        ["gh", "pr", "list", "--state", state, "--limit", str(limit),
         "--json", "headRefName", "-q", ".[].headRefName"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if result.returncode != 0:
        return set(), False
    return {b.strip() for b in result.stdout.split() if b.strip()}, True


def orphan_dirs(root: str, containers: list[str], registered: set[str]) -> list[str]:
    """Directories that look like worktrees but git no longer tracks as such.

    These are full checkouts consuming disk with no git registration, usually
    left when a worktree was pruned without removing its directory.
    """
    found = []
    for container in containers:
        base = Path(root) / container
        if not base.is_dir():
            continue
        for child in sorted(base.iterdir()):
            if not child.is_dir():
                continue
            resolved = str(child.resolve()).replace("\\", "/")
            if resolved not in registered:
                found.append(f"{container}/{child.name}")
    return found


def classify(tree: dict, root: str, merged: set[str], open_heads: set[str],
             have_gh: bool, foreign_markers: list[str],
             noise_suffixes: tuple[str, ...], noise_dirs: tuple[str, ...]) -> dict:
    path = tree.get("path", "")
    branch = tree.get("branch", "")
    norm = path.replace("\\", "/")
    is_main = os.path.normcase(os.path.abspath(path)) == os.path.normcase(os.path.abspath(root))
    foreign = any(m in norm for m in foreign_markers)

    dirt = real_dirt(path, noise_suffixes, noise_dirs)
    unpushed = unpushed_count(root, branch or tree.get("head", ""))
    is_merged = branch in merged if have_gh else False
    is_open = branch in open_heads

    if is_main:
        tier, why = "MAIN", "primary checkout"
    elif tree.get("locked"):
        tier, why = "HOLD", "worktree is locked"
    elif is_open:
        tier, why = "HOLD", "branch has an open PR"
    elif dirt or unpushed:
        bits = []
        if dirt:
            bits.append(f"{len(dirt)} uncommitted file(s)")
        if unpushed:
            bits.append(f"{unpushed} unpushed commit(s)")
        tier = "REVIEW" if is_merged else "HOLD"
        why = " + ".join(bits) + (" despite merged PR" if is_merged else "")
    elif is_merged:
        tier, why = "SAFE", "PR merged, tree clean, nothing unpushed"
    elif not have_gh:
        tier, why = "UNKNOWN", "gh unavailable - merge status not checked"
    else:
        tier, why = "STALE", "no merged PR, no open PR, nothing uncommitted"

    if foreign and tier in ("SAFE", "STALE", "REVIEW"):
        tier, why = "FOREIGN", f"{why} (owned by another tool - report only)"

    return {
        "path": path, "branch": branch, "tier": tier, "reason": why,
        "dirty": dirt, "unpushed": unpushed, "merged": is_merged,
        "detached": tree.get("detached", False), "locked": tree.get("locked", False),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", help="also write the full survey to this path")
    parser.add_argument("--no-fetch", action="store_true", help="skip git fetch --prune")
    args = parser.parse_args()

    # The Windows console defaults to a codepage that mangles non-ASCII output.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    root = repo_root()
    if not root:
        print("Not inside a git repository.", file=sys.stderr)
        return 1

    cfg = load_config(root)
    containers = list(cfg.get("containers", DEFAULT_CONTAINERS))
    foreign_markers = list(cfg.get("foreign_markers", DEFAULT_FOREIGN))
    noise_suffixes = tuple(cfg.get("noise_suffixes", []))
    noise_dirs = tuple(cfg.get("noise_dirs", [])) or tuple(
        c if c.endswith("/") else c + "/" for c in containers)
    protected = set(cfg.get("protected_branches", DEFAULT_PROTECTED))

    if not args.no_fetch:
        print("Fetching origin (pruning deleted remote branches)...", file=sys.stderr)
        git("fetch", "origin", "--prune", cwd=root)

    merged, have_gh = gh_pr_heads("merged", 500)
    open_heads = gh_pr_heads("open", 300)[0] if have_gh else set()
    trees = list_worktrees(root)
    registered = {str(Path(t["path"]).resolve()).replace("\\", "/")
                  for t in trees if t.get("path")}

    surveyed = [classify(t, root, merged, open_heads, have_gh, foreign_markers,
                         noise_suffixes, noise_dirs) for t in trees]
    orphans = orphan_dirs(root, containers, registered)

    local = [b for b in git("for-each-ref", "--format=%(refname:short)",
                            "refs/heads", cwd=root).splitlines() if b]
    attached = {s["branch"] for s in surveyed if s["branch"]}
    branch_rows = []
    for branch in local:
        if branch in protected:
            continue
        branch_rows.append({
            "branch": branch,
            "merged": branch in merged,
            "open_pr": branch in open_heads,
            "unpushed": unpushed_count(root, branch),
            "checked_out": branch in attached,
        })

    tiers: dict[str, list[dict]] = {}
    for entry in surveyed:
        tiers.setdefault(entry["tier"], []).append(entry)

    print("\n# Worktree cleanup survey\n")
    print(f"{len(surveyed)} worktrees, {len(local)} local branches, "
          f"{len(orphans)} orphaned directories.")
    if not cfg:
        print("\n> No `.synapse/weedeat.toml` in this repo - running on generic "
              "defaults. Every uncommitted file counts as real work, so worktrees "
              "dirty only with regenerated files will read as HOLD.")
    if not have_gh:
        print("\n> `gh` unavailable - merge status could not be checked, so nothing "
              "is classified SAFE. Everything needs manual review.")

    for tier in ("SAFE", "STALE", "REVIEW", "HOLD", "FOREIGN", "UNKNOWN", "MAIN"):
        rows = tiers.get(tier, [])
        if not rows:
            continue
        print(f"\n## {tier} ({len(rows)})")
        for row in rows:
            label = row["branch"] or "(detached)"
            print(f"- `{label}` - {row['reason']}")
            print(f"    {row['path']}")
            if row["dirty"]:
                shown = ", ".join(row["dirty"][:4])
                more = f" +{len(row['dirty']) - 4} more" if len(row["dirty"]) > 4 else ""
                print(f"    uncommitted: {shown}{more}")

    if orphans:
        print(f"\n## ORPHANED DIRECTORIES ({len(orphans)})")
        print("Full checkouts on disk that git no longer registers as worktrees.")
        for name in orphans:
            print(f"- `{name}`")

    deletable = [b for b in branch_rows
                 if b["merged"] and not b["unpushed"] and not b["checked_out"]]
    keepers = [b for b in branch_rows if not b["merged"] and not b["open_pr"]]
    print("\n## BRANCHES")
    print(f"- {len(deletable)} merged, not checked out, nothing unpushed - deletable")
    print(f"- {len(keepers)} with no merged PR and no open PR - need a look before deleting")
    for row in keepers:
        flag = f" ({row['unpushed']} unpushed)" if row["unpushed"] else ""
        print(f"    - `{row['branch']}`{flag}")

    if args.json:
        Path(args.json).write_text(json.dumps(
            {"worktrees": surveyed, "orphan_dirs": orphans, "branches": branch_rows,
             "gh_available": have_gh, "configured": bool(cfg)}, indent=2),
            encoding="utf-8")
        print(f"\nFull survey written to {args.json}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
