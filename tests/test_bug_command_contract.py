from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BugCommandContractTest(unittest.TestCase):
    def test_cursor_command_runs_the_script(self) -> None:
        command = (ROOT / "commands" / "bug.md").read_text(encoding="utf-8")
        self.assertIn("commands/bug.mjs", command)
        self.assertNotIn("bug-capture", command)
        self.assertIn("Do not diagnose", command)

    def test_patch_command_runs_the_script(self) -> None:
        command = (ROOT / "commands" / "patch.md").read_text(encoding="utf-8")
        self.assertIn("commands/patch.mjs", command)
        self.assertIn("@fastpatch", command)
        self.assertNotIn("bug-capture", command)
        self.assertIn("Do not diagnose", command)

    def test_capture_is_not_a_skill(self) -> None:
        self.assertFalse((ROOT / "skills" / "bug" / "SKILL.md").exists())
        self.assertFalse((ROOT / "skills" / "bug-capture" / "SKILL.md").exists())

    def test_agents_and_briefing_do_not_route_capture(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        briefing = (ROOT / "hooks" / "synapse-briefing.md").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("`bug-capture`", agents)
        self.assertNotIn("$bug", agents)
        self.assertNotIn("bug-capture", briefing)
        self.assertNotIn("$bug", briefing)


if __name__ == "__main__":
    unittest.main()
