"""Command-line entry points for the weedeat worktree cleanup app."""

from __future__ import annotations

import argparse
import json
import sys

from apps.weedeat.scan import repo_root, run_survey
from apps.weedeat.prune import prune_branch, prune_worktree


REMAINDER_TIERS = ("STALE", "REVIEW", "HOLD")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="weedeat")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="emit the worktree survey as JSON")
    scan_parser.add_argument(
        "--no-fetch", action="store_true", help="skip git fetch --prune"
    )

    run_parser = subparsers.add_parser("run", help="prune safe entries and review the rest")
    run_parser.add_argument(
        "--no-fetch", action="store_true", help="skip git fetch --prune"
    )
    run_parser.add_argument(
        "--dry-run", action="store_true", help="show actions without changing Git state"
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = repo_root()
    if not root:
        print("Not inside a git repository.", file=sys.stderr)
        return 1

    if args.command == "scan":
        result = run_survey(root, no_fetch=args.no_fetch)
        json.dump(result, sys.stdout, indent=2)
        return 0

    return run(root, no_fetch=args.no_fetch, dry_run=args.dry_run)


def run(root: str, no_fetch: bool = False, dry_run: bool = False) -> int:
    result = run_survey(root, no_fetch=no_fetch)
    auto = [entry for entry in result["worktrees"] if entry["tier"] == "SAFE"]
    auto_worktree_branches = {entry["branch"] for entry in auto if entry["branch"]}
    auto_branches = [
        entry for entry in result["branches"]
        if entry["merged"] and not entry["unpushed"]
        and (not entry["checked_out"] or entry["branch"] in auto_worktree_branches)
    ]
    remainder = [
        entry for entry in result["worktrees"] if entry["tier"] in REMAINDER_TIERS
    ]

    if dry_run:
        print("Would prune:")
        for entry in auto:
            print(f"- worktree `{entry['branch'] or '(detached)'}` at {entry['path']}")
        for entry in auto_branches:
            print(f"- branch `{entry['branch']}` after its worktree is removed")
        print_remainder(remainder)
        return 0

    for entry in auto:
        success, message = prune_worktree(root, entry)
        print_prune_result("worktree", entry["branch"] or entry["path"], success, message)

    # Worktree removal changes branch eligibility. Re-check attachment after the
    # safe pass so a branch that was checked out only there can now be deleted.
    refreshed = run_survey(root, no_fetch=True)
    refreshed_branches = {entry["branch"]: entry for entry in refreshed["branches"]}
    for candidate in auto_branches:
        refreshed_entry = refreshed_branches.get(candidate["branch"])
        if refreshed_entry is None or refreshed_entry["checked_out"]:
            continue
        entry = {**candidate, "checked_out": False}
        success, message = prune_branch(root, entry)
        print_prune_result("branch", entry["branch"], success, message)

    reviewable = [entry for entry in remainder if not entry.get("locked")]
    if reviewable and sys.stdout.isatty():
        from apps.weedeat.tui import review

        review(root, reviewable)
    else:
        print_remainder(remainder)
    return 0


def print_prune_result(kind: str, label: str, success: bool, message: str) -> None:
    status = "pruned" if success else "failed"
    print(f"{status}: {kind} `{label}` - {message}")


def print_remainder(remainder: list[dict]) -> None:
    print("\n# Worktree cleanup remainder")
    print(f"\n{len(remainder)} worktrees need manual review.")
    for tier in REMAINDER_TIERS:
        rows = [entry for entry in remainder if entry["tier"] == tier]
        if not rows:
            continue
        print(f"\n## {tier} ({len(rows)})")
        for entry in rows:
            label = entry["branch"] or "(detached)"
            print(f"- `{label}` - {entry['reason']}")
            print(f"    {entry['path']}")
            if entry.get("dirty"):
                shown = ", ".join(entry["dirty"][:4])
                more = (
                    f" +{len(entry['dirty']) - 4} more"
                    if len(entry["dirty"]) > 4 else ""
                )
                print(f"    uncommitted: {shown}{more}")
