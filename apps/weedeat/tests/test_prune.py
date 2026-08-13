from __future__ import annotations

import unittest
from unittest.mock import patch

from apps.weedeat.prune import prune_branch, prune_worktree


class PruneGuardsTest(unittest.TestCase):
    @patch("apps.weedeat.prune.subprocess.run")
    def test_worktree_rejects_every_non_safe_tier(self, run) -> None:
        for tier in ("STALE", "REVIEW", "HOLD", "FOREIGN", "MAIN", "UNKNOWN"):
            with self.subTest(tier=tier), self.assertRaises(AssertionError):
                prune_worktree("repo", {"tier": tier, "path": "tree"})
        run.assert_not_called()

    @patch("apps.weedeat.prune.subprocess.run")
    def test_branch_rejects_ineligible_state(self, run) -> None:
        cases = [
            {"branch": "topic", "merged": False, "unpushed": 0, "checked_out": False},
            {"branch": "topic", "merged": True, "unpushed": 1, "checked_out": False},
            {"branch": "topic", "merged": True, "unpushed": 0, "checked_out": True},
        ]
        for entry in cases:
            with self.subTest(entry=entry), self.assertRaises(AssertionError):
                prune_branch("repo", entry)
        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
