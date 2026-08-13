from __future__ import annotations

import unittest
from unittest.mock import patch

from apps.weedeat.tui import ConfirmDelete, DiffScreen, WeedeatApp, WorktreeItem


ENTRY = {
    "branch": "topic",
    "tier": "STALE",
    "reason": "no merged PR",
    "path": "tree",
    "locked": False,
}


class TuiInteractionTest(unittest.IsolatedAsyncioTestCase):
    async def test_diff_opens_and_escape_returns_to_list(self) -> None:
        with patch("apps.weedeat.tui.review_base", return_value="main"), patch(
            "apps.weedeat.tui.branch_diff", return_value="example diff"
        ):
            app = WeedeatApp("repo", [ENTRY])
            async with app.run_test() as pilot:
                await pilot.press("d")
                self.assertIsInstance(app.screen, DiffScreen)
                self.assertIn("example diff", app.screen.query_one("#diff-body").content)
                await pilot.press("escape")
                self.assertIsInstance(app.screen.query_one(WorktreeItem), WorktreeItem)

    async def test_decline_keeps_row_and_confirm_deletes_it(self) -> None:
        with patch("apps.weedeat.tui.review_base", return_value="main"), patch(
            "apps.weedeat.tui.prune_reviewed_worktree", return_value=(True, "removed")
        ) as remove_tree, patch(
            "apps.weedeat.tui.prune_reviewed_branch", return_value=(True, "deleted")
        ) as remove_branch:
            app = WeedeatApp("repo", [ENTRY])
            async with app.run_test() as pilot:
                await pilot.press("x")
                self.assertIsInstance(app.screen, ConfirmDelete)
                await pilot.press("n")
                self.assertEqual(len(app.query(WorktreeItem)), 1)
                remove_tree.assert_not_called()

                await pilot.press("x")
                await pilot.press("y")
                await pilot.pause()
                self.assertEqual(len(app.query(WorktreeItem)), 0)
                remove_tree.assert_called_once_with("repo", ENTRY)
                remove_branch.assert_called_once_with("repo", "topic")

    async def test_locked_entry_is_not_offered(self) -> None:
        locked = {**ENTRY, "tier": "HOLD", "locked": True}
        with patch("apps.weedeat.tui.review_base", return_value="main"):
            app = WeedeatApp("repo", [locked])
            async with app.run_test():
                self.assertEqual(len(app.query(WorktreeItem)), 0)


if __name__ == "__main__":
    unittest.main()
