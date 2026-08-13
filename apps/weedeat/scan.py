"""Deterministic worktree and branch survey used by every weedeat frontend."""

from __future__ import annotations

import os
import subprocess
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


def read_manifest(root: str) -> dict[str, dict[str, list[str]]]:
    """Parse `.synapse/weedeat.md` into {section: {key: [values]}}.

    Only this tool's own file is read. It needs nothing from `identity.md` —
    the survey works off local refs and the PR list, not a baseline branch —
    and nothing at all from `bandaids.md`. There is no fallback to a root
    SYNAPSE.md: a stale file nobody remembers is worse than clean defaults.

    Sections are `## Heading`, entries are `key: value`. Repeated keys
    accumulate. Code fences are skipped, so the fenced and bare styles both
    parse the same.
    """
    path = Path(root) / ".synapse" / "weedeat.md"
    if not path.is_file():
        return {}
    sections: dict[str, dict[str, list[str]]] = {}
    current: str | None = None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            continue
        if stripped.startswith("## "):
            current = stripped[3:].strip().lower()
            sections.setdefault(current, {})
            continue
        if current is None or stripped.startswith("#") or ":" not in stripped:
            continue
        key, _, value = stripped.partition(":")
        key, value = key.strip().lower(), value.strip()
        # Prose in a section reads as a key when it happens to contain a colon;
        # a real entry key is a single bare word.
        if key and value and " " not in key:
            sections[current].setdefault(key, []).append(value)
    return sections


def csv(section: dict, key: str, default: list[str] | None = None) -> list[str]:
    values = section.get(key)
    if not values:
        return list(default) if default is not None else []
    return [item.strip() for item in values[-1].split(",") if item.strip()]


def worktrees_config(manifest: dict) -> dict:
    """The `## Worktrees` section of .synapse/weedeat.md, shaped for the survey."""
    section = manifest.get("worktrees", {})
    if not section:
        return {}
    return {
        "containers": csv(section, "containers", DEFAULT_CONTAINERS),
        "foreign_markers": csv(section, "foreign", DEFAULT_FOREIGN),
        "noise_suffixes": csv(section, "noise-suffixes"),
        "noise_dirs": csv(section, "noise-dirs"),
        "protected_branches": csv(section, "protected", DEFAULT_PROTECTED),
    }


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


def run_survey(root: str, no_fetch: bool = False) -> dict:
    """Build the complete deterministic survey without rendering a report."""
    cfg = worktrees_config(read_manifest(root))
    containers = list(cfg.get("containers", DEFAULT_CONTAINERS))
    foreign_markers = list(cfg.get("foreign_markers", DEFAULT_FOREIGN))
    noise_suffixes = tuple(cfg.get("noise_suffixes", []))
    noise_dirs = tuple(cfg.get("noise_dirs", [])) or tuple(
        c if c.endswith("/") else c + "/" for c in containers)
    protected = set(cfg.get("protected_branches", DEFAULT_PROTECTED))

    if not no_fetch:
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

    return {
        "worktrees": surveyed,
        "orphan_dirs": orphans,
        "branches": branch_rows,
        "gh_available": have_gh,
        "configured": bool(cfg),
    }
