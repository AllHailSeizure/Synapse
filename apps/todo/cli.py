"""Command-line entrypoint for pending spec interviews."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Callable, TextIO

from apps.todo.console import run_interview
from apps.todo.domain import (
    PendingSpec,
    QuestionFileError,
    SpecStateError,
    find_pending_specs,
)


InputFn = Callable[[str], str]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="TODO",
        description="List pending Synapse specs and complete their interviews.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_only",
        help="list pending specs without starting an interview",
    )
    return parser


def repo_root(cwd: str | Path | None = None) -> Path | None:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0 or not result.stdout.strip():
        return None
    return Path(result.stdout.strip()).resolve()


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = repo_root()
    if root is None:
        print("Not inside a git repository.", file=sys.stderr)
        return 1
    return run(root, list_only=args.list_only)


def run(
    root: str | Path,
    *,
    list_only: bool = False,
    input_fn: InputFn | None = None,
    stdin: TextIO | None = None,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    input_stream = sys.stdin if stdin is None else stdin
    output = sys.stdout if stdout is None else stdout
    errors = sys.stderr if stderr is None else stderr
    specs = find_pending_specs(root)

    print("TODO", file=output)
    print(file=output)
    if not specs:
        print("No pending specs.", file=output)
        return 0
    for number, spec in enumerate(specs, start=1):
        print(f"{number}. SPEC: {spec.label}", file=output)

    if list_only:
        return 0
    if not input_stream.isatty() or not output.isatty():
        print(
            "A spec interview requires an interactive terminal; use --list to list only.",
            file=errors,
        )
        return 2

    ask = input_fn or input
    try:
        selected = _select(specs, ask, output)
    except (EOFError, KeyboardInterrupt, StopIteration):
        print("\nSelection aborted.", file=errors)
        return 130
    if selected is None:
        return 0
    if not selected.path.is_file():
        print(f"{selected.path.name} no longer exists.", file=errors)
        return 1

    try:
        run_interview(selected, input_fn=ask, output=output)
    except (QuestionFileError, SpecStateError) as error:
        print(f"Cannot interview {selected.label}: {error}", file=errors)
        return 1
    return 0


def _select(
    specs: list[PendingSpec], ask: InputFn, output: TextIO
) -> PendingSpec | None:
    while True:
        raw = ask("Select a SPEC number (or q): ").strip()
        if raw.casefold() in ("q", "quit", "exit"):
            return None
        if raw.isdigit():
            index = int(raw) - 1
            if 0 <= index < len(specs):
                return specs[index]
        print(f"Choose a number from 1 to {len(specs)}, or q.", file=output)
