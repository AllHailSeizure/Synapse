from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from apps.todo.domain import QuestionFileError, find_pending_specs, load_questions


class PendingSpecInventoryTest(unittest.TestCase):
    def test_missing_specs_directory_is_an_empty_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual(find_pending_specs(Path(temp)), [])

    def test_only_pending_specs_are_listed_with_short_sorted_labels(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            specs = root / ".synapse" / "specs"
            specs.mkdir(parents=True)
            for name in (
                "2026-08-19 - Zebra (PENDING).md",
                "2026-08-18 - Alpha (PENDING) (BLOCKED).md",
                "2026-08-17 - Done (APPROVED).md",
                "2026-08-16 - Shipped (IMPLEMENTED).md",
                "2026-08-15 - Dropped (CLOSED).md",
                "notes.md",
            ):
                (specs / name).write_text(f"# {name}\n", encoding="utf-8")

            found = find_pending_specs(root)

            self.assertEqual([item.label for item in found], ["Alpha", "Zebra"])
            self.assertEqual(found[0].path.name, "2026-08-18 - Alpha (PENDING) (BLOCKED).md")
            self.assertTrue(found[0].blocked)


class QuestionFileTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        specs = self.root / ".synapse" / "specs"
        specs.mkdir(parents=True)
        self.path = specs / "2026-08-19 - Feature (PENDING).md"
        self.path.write_text("# 2026-08-19: Feature (PENDING)\n", encoding="utf-8")
        self.spec = find_pending_specs(self.root)[0]

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_questions(self, payload: object) -> None:
        self.spec.questions_path.write_text(json.dumps(payload), encoding="utf-8")

    def test_missing_questions_file_means_no_feature_questions(self) -> None:
        self.assertEqual(load_questions(self.spec), [])

    def test_empty_questions_array_is_valid(self) -> None:
        self.write_questions({
            "version": 1,
            "spec": self.path.name,
            "questions": [],
        })

        self.assertEqual(load_questions(self.spec), [])

    def test_valid_questions_preserve_options_and_recommendation(self) -> None:
        self.write_questions({
            "version": 1,
            "spec": self.path.name,
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
        })

        questions = load_questions(self.spec)

        self.assertEqual([question.id for question in questions], ["audience", "name"])
        self.assertEqual(questions[0].options[0].label, "Maintainers")
        self.assertEqual(questions[0].recommendation, "Maintainers")
        self.assertEqual(questions[1].options, ())

    def test_invalid_json_is_rejected(self) -> None:
        self.spec.questions_path.write_text("{", encoding="utf-8")

        with self.assertRaisesRegex(QuestionFileError, "valid JSON"):
            load_questions(self.spec)

    def test_wrong_spec_reference_is_rejected(self) -> None:
        self.write_questions({"version": 1, "spec": "other.md", "questions": []})

        with self.assertRaisesRegex(QuestionFileError, "must match"):
            load_questions(self.spec)

    def test_duplicate_ids_and_unknown_recommendations_are_rejected(self) -> None:
        self.write_questions({
            "version": 1,
            "spec": self.path.name,
            "questions": [
                {"id": "same", "prompt": "First?"},
                {
                    "id": "same",
                    "prompt": "Second?",
                    "options": [{"label": "A"}],
                    "recommendation": "B",
                },
            ],
        })

        with self.assertRaises(QuestionFileError):
            load_questions(self.spec)


if __name__ == "__main__":
    unittest.main()
