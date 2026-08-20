from __future__ import annotations

import json
import io
import tempfile
import unittest
from pathlib import Path

from apps.todo.console import run_interview
from apps.todo.domain import SpecStateError, approve_spec, find_pending_specs


def inputs(*values: str):
    iterator = iter(values)
    return lambda _prompt="": next(iterator)


class InterviewTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        specs = self.root / ".synapse" / "specs"
        specs.mkdir(parents=True)
        self.pending = specs / "2026-08-19 - Feature (PENDING).md"
        self.pending.write_text(
            "# 2026-08-19: Feature (PENDING)\n\n## Intent\nSomething useful.\n",
            encoding="utf-8",
        )
        self.spec = find_pending_specs(self.root)[0]

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_questions(self) -> None:
        self.spec.questions_path.write_text(json.dumps({
            "version": 1,
            "spec": self.pending.name,
            "questions": [
                {
                    "id": "audience",
                    "prompt": "Who can run it?",
                    "options": [
                        {"label": "Maintainers", "description": "Smallest scope."},
                        {"label": "Everyone", "description": "Broad access."},
                    ],
                    "recommendation": "Maintainers",
                },
                {"id": "name", "prompt": "What should it be called?"},
            ],
        }), encoding="utf-8")

    def test_completed_interview_appends_answers_and_approves(self) -> None:
        self.write_questions()
        output = io.StringIO()

        approved = run_interview(
            self.spec,
            input_fn=inputs("1", "TODO", "y", "none"),
            output=output,
        )

        self.assertIsNotNone(approved)
        assert approved is not None
        self.assertFalse(self.pending.exists())
        self.assertEqual(approved.name, "2026-08-19 - Feature (APPROVED).md")
        content = approved.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("# 2026-08-19: Feature (APPROVED)"))
        self.assertIn("## Spec interview", content)
        self.assertIn("**Who can run it?** Maintainers", content)
        self.assertIn("**What should it be called?** TODO", content)
        self.assertIn("**Remarks:** none", content)
        self.assertIn("Recommended: Maintainers", output.getvalue())

    def test_missing_questions_file_runs_closer_only(self) -> None:
        approved = run_interview(
            self.spec,
            input_fn=inputs("y", "Looks right"),
            output=io.StringIO(),
        )

        assert approved is not None
        content = approved.read_text(encoding="utf-8")
        self.assertIn("No feature questions were recorded.", content)
        self.assertIn("**Remarks:** Looks right", content)

    def test_declining_closer_leaves_pending_spec_untouched(self) -> None:
        before = self.pending.read_text(encoding="utf-8")

        result = run_interview(
            self.spec,
            input_fn=inputs("n"),
            output=io.StringIO(),
        )

        self.assertIsNone(result)
        self.assertTrue(self.pending.exists())
        self.assertEqual(self.pending.read_text(encoding="utf-8"), before)

    def test_abort_mid_interview_leaves_pending_spec_untouched(self) -> None:
        self.write_questions()
        before = self.pending.read_text(encoding="utf-8")

        result = run_interview(
            self.spec,
            input_fn=inputs("1"),
            output=io.StringIO(),
        )

        self.assertIsNone(result)
        self.assertTrue(self.pending.exists())
        self.assertEqual(self.pending.read_text(encoding="utf-8"), before)

    def test_blank_option_answer_uses_the_recommendation(self) -> None:
        self.write_questions()

        approved = run_interview(
            self.spec,
            input_fn=inputs("", "TODO", "y", "none"),
            output=io.StringIO(),
        )

        assert approved is not None
        self.assertIn(
            "**Who can run it?** Maintainers",
            approved.read_text(encoding="utf-8"),
        )


class ApprovalStateTest(unittest.TestCase):
    def test_vanished_spec_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            specs = root / ".synapse" / "specs"
            specs.mkdir(parents=True)
            pending = specs / "Feature (PENDING).md"
            pending.write_text("# Feature (PENDING)\n", encoding="utf-8")
            spec = find_pending_specs(root)[0]
            pending.unlink()

            with self.assertRaisesRegex(SpecStateError, "no longer exists"):
                approve_spec(spec, [], "none")

    def test_mismatched_title_is_refused_without_rename(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            specs = root / ".synapse" / "specs"
            specs.mkdir(parents=True)
            pending = specs / "Feature (PENDING).md"
            pending.write_text("# Feature\n", encoding="utf-8")
            spec = find_pending_specs(root)[0]

            with self.assertRaisesRegex(SpecStateError, "title"):
                approve_spec(spec, [], "none")

            self.assertTrue(pending.exists())

    def test_blocked_marker_is_preserved_during_approval(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            specs = root / ".synapse" / "specs"
            specs.mkdir(parents=True)
            pending = specs / "Feature (PENDING) (BLOCKED).md"
            pending.write_text("# Feature (PENDING) (BLOCKED)\n", encoding="utf-8")
            spec = find_pending_specs(root)[0]

            approved = approve_spec(spec, [], "none")

            self.assertEqual(approved.name, "Feature (APPROVED) (BLOCKED).md")
            self.assertTrue(
                approved.read_text(encoding="utf-8").startswith(
                    "# Feature (APPROVED) (BLOCKED)"
                )
            )


if __name__ == "__main__":
    unittest.main()
