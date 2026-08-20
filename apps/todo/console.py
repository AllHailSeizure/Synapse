"""Terminal interview for a selected pending spec."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable, TextIO

from apps.todo.domain import PendingSpec, Question, approve_spec, load_questions


InputFn = Callable[[str], str]


def run_interview(
    spec: PendingSpec,
    *,
    input_fn: InputFn | None = None,
    output: TextIO | None = None,
) -> Path | None:
    ask = input_fn or input
    stream = output or sys.stdout
    questions = load_questions(spec)
    answers: list[tuple[Question, str]] = []

    print(f"SPEC: {spec.label}", file=stream)
    print(file=stream)
    try:
        for number, question in enumerate(questions, start=1):
            print(f"{number}. {question.prompt}", file=stream)
            for option_number, option in enumerate(question.options, start=1):
                suffix = f" — {option.description}" if option.description else ""
                print(f"   {option_number}. {option.label}{suffix}", file=stream)
            if question.recommendation:
                print(f"   Recommended: {question.recommendation}", file=stream)
            answers.append((question, _answer(question, ask, stream)))
            print(file=stream)

        accepted = ask("Approve this spec? [y/N] ").strip().casefold()
        if accepted not in ("y", "yes"):
            print("Interview ended. Spec remains PENDING.", file=stream)
            return None
        remarks = _required_input("Remarks (enter 'none' if none): ", ask)
    except (EOFError, KeyboardInterrupt, StopIteration):
        print("\nInterview aborted. Spec remains PENDING.", file=stream)
        return None

    approved = approve_spec(spec, answers, remarks)
    print(f"Approved: {approved.name}", file=stream)
    return approved


def _answer(question: Question, ask: InputFn, output: TextIO) -> str:
    while True:
        raw = ask("Answer: ").strip()
        if not raw and question.recommendation:
            return question.recommendation
        if question.options:
            if raw.isdigit():
                index = int(raw) - 1
                if 0 <= index < len(question.options):
                    return question.options[index].label
            match = next(
                (
                    option.label
                    for option in question.options
                    if option.label.casefold() == raw.casefold()
                ),
                None,
            )
            if match:
                return match
            print("Choose an option number or label.", file=output)
            continue
        if raw:
            return raw
        print("Answer cannot be empty.", file=output)


def _required_input(prompt: str, ask: InputFn) -> str:
    while True:
        value = ask(prompt).strip()
        if value:
            return value
