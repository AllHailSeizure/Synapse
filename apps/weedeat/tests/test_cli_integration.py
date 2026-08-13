from __future__ import annotations

import contextlib
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from apps.weedeat.cli import run


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=True,
    )
    return result.stdout.strip()


class RunIntegrationTest(unittest.TestCase):
    @patch("apps.weedeat.scan.gh_pr_heads", return_value=(set(), False))
    @patch("apps.weedeat.tui.review")
    def test_headless_run_prints_remainder_without_launching_tui(
        self, review, _pr_heads
    ) -> None:
        fake_stdout = Mock(wraps=sys.stdout)
        fake_stdout.isatty.return_value = False
        output = io.StringIO()
        fake_stdout.write.side_effect = output.write
        fake_stdout.flush.side_effect = lambda: None

        with patch("sys.stdout", fake_stdout):
            self.assertEqual(run(str(Path.cwd()), no_fetch=True), 0)

        self.assertIn("Remainder (", output.getvalue())
        review.assert_not_called()

    def test_safe_worktree_and_branch_are_pruned_but_unmerged_work_is_kept(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            remote = base / "remote.git"
            repo = base / "repo"
            safe_tree = base / "safe-tree"
            hold_tree = base / "hold-tree"

            subprocess.run(["git", "init", "--bare", str(remote)], check=True,
                           capture_output=True)
            subprocess.run(["git", "init", "-b", "main", str(repo)], check=True,
                           capture_output=True)
            git(repo, "config", "user.email", "weedeat@example.invalid")
            git(repo, "config", "user.name", "Weedeat Test")
            (repo / "README.md").write_text("root\n", encoding="utf-8")
            git(repo, "add", "README.md")
            git(repo, "commit", "-m", "root")
            git(repo, "remote", "add", "origin", str(remote))
            git(repo, "push", "-u", "origin", "main")

            git(repo, "switch", "-c", "merged")
            (repo / "merged.txt").write_text("merged\n", encoding="utf-8")
            git(repo, "add", "merged.txt")
            git(repo, "commit", "-m", "merged work")
            git(repo, "push", "-u", "origin", "merged")
            git(repo, "switch", "main")
            git(repo, "merge", "--ff-only", "merged")
            git(repo, "worktree", "add", str(safe_tree), "merged")

            git(repo, "worktree", "add", "-b", "unmerged", str(hold_tree), "main")
            (hold_tree / "unmerged.txt").write_text("keep me\n", encoding="utf-8")
            git(hold_tree, "add", "unmerged.txt")
            git(hold_tree, "commit", "-m", "unmerged work")

            def pr_heads(state: str, _limit: int) -> tuple[set[str], bool]:
                return ({"merged"} if state == "merged" else set(), True)

            with patch("apps.weedeat.scan.gh_pr_heads", side_effect=pr_heads):
                dry_output = io.StringIO()
                with contextlib.redirect_stdout(dry_output):
                    self.assertEqual(run(str(repo), no_fetch=True, dry_run=True), 0)
                self.assertIn("worktree `merged`", dry_output.getvalue())
                self.assertIn("[HOLD] `unmerged`", dry_output.getvalue())
                self.assertTrue(safe_tree.exists())

                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(run(str(repo), no_fetch=True), 0)

            worktrees = git(repo, "worktree", "list", "--porcelain")
            branches = git(repo, "branch", "--format=%(refname:short)").splitlines()
            self.assertNotIn(str(safe_tree), worktrees)
            self.assertNotIn("merged", branches)
            self.assertIn(str(hold_tree).replace("\\", "/"), worktrees)
            self.assertIn("unmerged", branches)


if __name__ == "__main__":
    unittest.main()
