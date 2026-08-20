from __future__ import annotations

import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from apps.todo.cli import main, repo_root, run


def tty_stream() -> Mock:
    stream = Mock()
    stream.isatty.return_value = True
    return stream


class CliTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def add_spec(self, name: str = "Feature") -> Path:
        specs = self.root / ".synapse" / "specs"
        specs.mkdir(parents=True, exist_ok=True)
        path = specs / f"2026-08-19 - {name} (PENDING).md"
        path.write_text(f"# 2026-08-19: {name} (PENDING)\n", encoding="utf-8")
        return path

    def test_empty_inventory_is_clear_and_successful(self) -> None:
        output = io.StringIO()

        code = run(self.root, list_only=True, stdout=output)

        self.assertEqual(code, 0)
        self.assertEqual(output.getvalue(), "TODO\n\nNo pending specs.\n")

    def test_list_only_prints_numbered_spec_rows(self) -> None:
        self.add_spec("Zebra")
        self.add_spec("Alpha")
        output = io.StringIO()

        code = run(self.root, list_only=True, stdout=output)

        self.assertEqual(code, 0)
        self.assertIn("1. SPEC: Alpha", output.getvalue())
        self.assertIn("2. SPEC: Zebra", output.getvalue())

    def test_non_interactive_run_refuses_interview_without_mutation(self) -> None:
        pending = self.add_spec()
        output = io.StringIO()
        errors = io.StringIO()
        stdin = Mock()
        stdin.isatty.return_value = False

        code = run(self.root, stdin=stdin, stdout=output, stderr=errors)

        self.assertEqual(code, 2)
        self.assertIn("interactive terminal", errors.getvalue())
        self.assertTrue(pending.exists())

    def test_selected_spec_runs_interview(self) -> None:
        pending = self.add_spec()
        answers = iter(("1", "y", "none"))
        output = io.StringIO()
        output.isatty = lambda: True  # type: ignore[attr-defined]
        stdin = tty_stream()

        code = run(
            self.root,
            input_fn=lambda _prompt="": next(answers),
            stdin=stdin,
            stdout=output,
            stderr=io.StringIO(),
        )

        self.assertEqual(code, 0)
        self.assertFalse(pending.exists())
        self.assertTrue(pending.with_name(pending.name.replace("PENDING", "APPROVED")).exists())

    def test_corrupt_question_file_refuses_selected_interview(self) -> None:
        pending = self.add_spec()
        pending.with_suffix(".questions.json").write_text("{", encoding="utf-8")
        answers = iter(("1",))
        output = io.StringIO()
        output.isatty = lambda: True  # type: ignore[attr-defined]
        errors = io.StringIO()

        code = run(
            self.root,
            input_fn=lambda _prompt="": next(answers),
            stdin=tty_stream(),
            stdout=output,
            stderr=errors,
        )

        self.assertEqual(code, 1)
        self.assertIn("valid JSON", errors.getvalue())
        self.assertTrue(pending.exists())

    def test_spec_vanishing_after_selection_is_reported(self) -> None:
        pending = self.add_spec()
        output = io.StringIO()
        output.isatty = lambda: True  # type: ignore[attr-defined]
        errors = io.StringIO()

        def select(_prompt: str = "") -> str:
            pending.unlink()
            return "1"

        code = run(
            self.root,
            input_fn=select,
            stdin=tty_stream(),
            stdout=output,
            stderr=errors,
        )

        self.assertEqual(code, 1)
        self.assertIn("no longer exists", errors.getvalue())

    @patch("apps.todo.cli.repo_root")
    @patch("apps.todo.cli.run", return_value=0)
    def test_main_discovers_git_root(self, run_cli, discover) -> None:
        discover.return_value = self.root

        self.assertEqual(main(["--list"]), 0)

        run_cli.assert_called_once_with(self.root, list_only=True)


class RepoRootTest(unittest.TestCase):
    def test_repo_root_discovers_parent_repository(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(
                ["git", "init", "-b", "main", str(root)],
                check=True,
                capture_output=True,
            )
            child = root / "nested"
            child.mkdir()

            self.assertEqual(repo_root(child), root.resolve())

    def test_repo_root_returns_none_outside_git(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            self.assertIsNone(repo_root(Path(temp)))


if __name__ == "__main__":
    unittest.main()
