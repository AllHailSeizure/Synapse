"""Command-line entry points for the weedeat worktree cleanup app."""

from __future__ import annotations

import argparse
import json
import sys

from apps.weedeat.scan import repo_root, run_survey


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

    raise NotImplementedError("weedeat run is added by the auto-prune task")
