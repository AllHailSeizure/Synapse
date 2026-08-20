"""Pending-spec discovery and the versioned interview-question contract."""

from __future__ import annotations

import json
import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path


PENDING_NAME = re.compile(
    r"^(?P<stem>.+) \(PENDING\)(?P<blocked> \(BLOCKED\))?\.md$"
)
DATE_PREFIX = re.compile(r"^\d{4}-\d{2}-\d{2} - ")


class QuestionFileError(ValueError):
    """Raised when a sibling questions file cannot be safely interviewed."""


class SpecStateError(RuntimeError):
    """Raised when a pending spec cannot be safely transitioned."""


@dataclass(frozen=True)
class PendingSpec:
    path: Path
    label: str
    blocked: bool = False

    @property
    def questions_path(self) -> Path:
        return self.path.with_suffix(".questions.json")


@dataclass(frozen=True)
class Option:
    label: str
    description: str = ""


@dataclass(frozen=True)
class Question:
    id: str
    prompt: str
    options: tuple[Option, ...] = ()
    recommendation: str | None = None


def find_pending_specs(root: str | Path) -> list[PendingSpec]:
    specs_dir = Path(root) / ".synapse" / "specs"
    if not specs_dir.is_dir():
        return []

    found = []
    for path in specs_dir.iterdir():
        if not path.is_file():
            continue
        match = PENDING_NAME.match(path.name)
        if match is None:
            continue
        label = DATE_PREFIX.sub("", match.group("stem"))
        found.append(PendingSpec(path, label, bool(match.group("blocked"))))
    return sorted(found, key=lambda spec: (spec.label.casefold(), spec.path.name))


def load_questions(spec: PendingSpec) -> list[Question]:
    path = spec.questions_path
    if not path.is_file():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise QuestionFileError(f"{path.name} must contain valid JSON: {error}") from error

    if not isinstance(payload, dict):
        raise QuestionFileError(f"{path.name} must contain a JSON object")
    if type(payload.get("version")) is not int or payload["version"] != 1:
        raise QuestionFileError(f"{path.name} must use question format version 1")
    if payload.get("spec") != spec.path.name:
        raise QuestionFileError(
            f"{path.name} spec must match {spec.path.name!r}"
        )
    raw_questions = payload.get("questions")
    if not isinstance(raw_questions, list):
        raise QuestionFileError(f"{path.name} questions must be an array")

    questions = []
    ids: set[str] = set()
    for index, raw in enumerate(raw_questions, start=1):
        where = f"{path.name} question {index}"
        if not isinstance(raw, dict):
            raise QuestionFileError(f"{where} must be an object")
        question_id = _required_text(raw.get("id"), f"{where} id")
        if question_id in ids:
            raise QuestionFileError(f"{where} has duplicate id {question_id!r}")
        ids.add(question_id)
        prompt = _required_text(raw.get("prompt"), f"{where} prompt")

        raw_options = raw.get("options", [])
        if not isinstance(raw_options, list):
            raise QuestionFileError(f"{where} options must be an array")
        options = []
        labels: set[str] = set()
        for option_index, raw_option in enumerate(raw_options, start=1):
            option_where = f"{where} option {option_index}"
            if not isinstance(raw_option, dict):
                raise QuestionFileError(f"{option_where} must be an object")
            label = _required_text(raw_option.get("label"), f"{option_where} label")
            if label in labels:
                raise QuestionFileError(f"{option_where} duplicates label {label!r}")
            labels.add(label)
            description = raw_option.get("description", "")
            if not isinstance(description, str):
                raise QuestionFileError(f"{option_where} description must be text")
            options.append(Option(label, description.strip()))

        recommendation = raw.get("recommendation")
        if recommendation is not None:
            recommendation = _required_text(recommendation, f"{where} recommendation")
            if options and recommendation not in labels:
                raise QuestionFileError(
                    f"{where} recommendation must match an option label"
                )
        questions.append(Question(question_id, prompt, tuple(options), recommendation))
    return questions


def approve_spec(
    spec: PendingSpec,
    answers: list[tuple[Question, str]],
    remarks: str,
) -> Path:
    """Append completed interview answers and atomically transition the spec."""
    if not spec.path.is_file():
        raise SpecStateError(f"{spec.path.name} no longer exists")
    try:
        original = spec.path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise SpecStateError(f"Could not read {spec.path.name}: {error}") from error

    lines = original.splitlines()
    if not lines or not lines[0].startswith("# ") or "(PENDING)" not in lines[0]:
        raise SpecStateError(f"{spec.path.name} title is not marked PENDING")
    lines[0] = lines[0].replace("(PENDING)", "(APPROVED)", 1)
    approved_name = spec.path.name.replace(" (PENDING)", " (APPROVED)", 1)
    if approved_name == spec.path.name:
        raise SpecStateError(f"{spec.path.name} filename is not marked PENDING")
    approved_path = spec.path.with_name(approved_name)
    if approved_path.exists():
        raise SpecStateError(f"{approved_path.name} already exists")

    body = "\n".join(lines).rstrip()
    interview = ["", "", "## Spec interview", ""]
    if answers:
        for question, answer in answers:
            interview.append(f"- **{_single_line(question.prompt)}** {_single_line(answer)}")
    else:
        interview.append("No feature questions were recorded.")
    interview.extend(("", "- **Approval:** accepted", f"- **Remarks:** {_single_line(remarks)}", ""))
    updated = body + "\n".join(interview)

    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            newline="\n",
            dir=spec.path.parent,
            prefix=".todo-",
            suffix=".tmp",
            delete=False,
        ) as handle:
            handle.write(updated)
            handle.flush()
            os.fsync(handle.fileno())
            temporary = Path(handle.name)
        spec.path.rename(approved_path)
        try:
            os.replace(temporary, approved_path)
        except OSError:
            approved_path.rename(spec.path)
            raise
        temporary = None
    except OSError as error:
        raise SpecStateError(f"Could not approve {spec.path.name}: {error}") from error
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return approved_path


def _required_text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise QuestionFileError(f"{field} must be non-empty text")
    return value.strip()


def _single_line(value: str) -> str:
    return " ".join(value.split())
