from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


class SpecWriterContractTest(unittest.TestCase):
    def test_writing_specs_emits_pending_spec_and_versioned_questions(self) -> None:
        skill = (ROOT / "skills" / "writing-specs" / "SKILL.md").read_text(
            encoding="utf-8"
        )

        self.assertIn(".questions.json", skill)
        self.assertIn('"version": 1', skill)
        self.assertIn('"spec":', skill)
        self.assertIn('"questions":', skill)
        self.assertIn("feature-defining", skill)
        self.assertIn("TODO", skill)

    def test_writing_specs_stops_before_interview_approval_or_implementation(self) -> None:
        skill = (ROOT / "skills" / "writing-specs" / "SKILL.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("Do not conduct the interview in chat", skill)
        self.assertIn("Do not mark the spec `APPROVED`", skill)
        self.assertIn("Do not start a plan or implementation", skill)

    def test_registered_spec_writer_has_the_same_authority_boundary(self) -> None:
        agent_path = ROOT / ".codex" / "agents" / "synapse" / "spec-writer.toml"
        self.assertTrue(agent_path.is_file())
        agent = agent_path.read_text(encoding="utf-8")

        self.assertIn('name = "spec-writer"', agent)
        self.assertIn("PENDING", agent)
        self.assertIn("questions", agent)
        self.assertIn("Do not run the interview", agent)
        self.assertIn("Do not approve", agent)
        self.assertIn("Do not implement", agent)

    def test_codex_guidance_publishes_the_spec_writer(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        briefing = (ROOT / "hooks" / "synapse-briefing.md").read_text(encoding="utf-8")

        self.assertIn("spec-writer", agents)
        self.assertIn("spec-writer", briefing)


if __name__ == "__main__":
    unittest.main()
