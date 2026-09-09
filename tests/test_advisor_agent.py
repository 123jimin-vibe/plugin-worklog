"""Packaging checks for the shared worklog advisor agent."""

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugin"
AGENT = PLUGIN / "agents/worklog-advisor.md"


class AdvisorAgentTests(unittest.TestCase):
    def test_agent_is_shared_by_claude_plugin_and_pi_package(self):
        claude_manifest = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        pi_manifest = json.loads((PLUGIN / "package.json").read_text(encoding="utf-8"))

        self.assertEqual(claude_manifest["name"], "worklog")
        self.assertEqual(pi_manifest["name"], "worklog")
        self.assertIn("./agents", pi_manifest["pi"]["subagents"]["agents"])
        self.assertIn("./skills", pi_manifest["pi"]["skills"])
        self.assertTrue(AGENT.is_file())


if __name__ == "__main__":
    unittest.main()
