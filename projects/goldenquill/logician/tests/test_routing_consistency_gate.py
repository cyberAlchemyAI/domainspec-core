"""Unit tests for logician.gates.routing_consistency_gate.

Each test writes minimal router.yaml + routing.yaml pairs into a tmp
workspace, sets QUILL_WORKSPACE, reloads the gate, and asserts on findings.
"""
from __future__ import annotations

import importlib
import os
import shutil
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))


MATCHED_ROUTER = """\
version: 1
tilth:
  scribe:
    primary: anthropic/claude-sonnet-4-6
  judge:
    primary: groq/qwen/qwen3-32b
  editor:
    primary: groq/llama-3.3-70b-versatile
  red_team:
    primary: groq/openai/gpt-oss-120b
  scout:
    primary: ollama/mistral:7b
  logician:
    primary: none
    implementation: python + cedar-policy
"""

MATCHED_ROUTING = """\
version: "0.1"
active_tier: tier_8gb
seats:
  scribe:
    tier_8gb: {provider: anthropic, model: claude-sonnet-4-6, family: anthropic}
  judge:
    tier_8gb: {provider: groq, model: "qwen/qwen3-32b", family: alibaba}
  editor:
    tier_8gb: {provider: groq, model: llama-3.3-70b-versatile, family: meta}
  red_team:
    tier_8gb: {provider: groq, model: "openai/gpt-oss-120b", family: openai_oss}
  scout:
    tier_8gb: {provider: ollama, model: "mistral:7b", family: mistral}
  logician:
    implementation: python_deterministic
    path: pipeline/orchestrator/logician.py
"""


class RoutingConsistencyGateTestBase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="rcg_test_"))
        self.workspace = self.tmp / "GoldenQuill"
        (self.workspace / "pipeline" / "orchestrator").mkdir(parents=True)
        self._orig_env = dict(os.environ)
        os.environ["QUILL_WORKSPACE"] = str(self.workspace)
        if "logician.gates.routing_consistency_gate" in sys.modules:
            del sys.modules["logician.gates.routing_consistency_gate"]
        import logician.gates.routing_consistency_gate as gate  # noqa: E402
        importlib.reload(gate)
        # Ensure it read our QUILL_WORKSPACE
        gate.WORKSPACE = self.workspace
        gate.ROUTER_YAML = self.workspace / "router.yaml"
        gate.ROUTING_YAML = self.workspace / "pipeline" / "orchestrator" / "routing.yaml"
        self.gate = gate

    def tearDown(self) -> None:
        os.environ.clear()
        os.environ.update(self._orig_env)
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write_pair(self, router: str, routing: str) -> None:
        (self.workspace / "router.yaml").write_text(router)
        (self.workspace / "pipeline" / "orchestrator" / "routing.yaml").write_text(routing)


class TestMatched(RoutingConsistencyGateTestBase):
    def test_matched_pair_is_ok(self):
        self.write_pair(MATCHED_ROUTER, MATCHED_ROUTING)
        r = self.gate.run()
        self.assertEqual(r.severity, "OK", msg=r.findings)
        self.assertEqual(r.findings, [])
        # All six seats checked
        self.assertEqual(set(r.seats_checked),
                         {"scribe", "judge", "editor", "red_team", "scout", "logician"})


class TestModelMismatch(RoutingConsistencyGateTestBase):
    def test_model_string_mismatch_errors(self):
        bad = MATCHED_ROUTER.replace("groq/qwen/qwen3-32b", "groq/qwen-3-32b")
        self.write_pair(bad, MATCHED_ROUTING)
        r = self.gate.run()
        self.assertEqual(r.severity, "ERROR")
        mismatches = [f for f in r.findings if f.rule == "model_string_mismatch"]
        self.assertEqual(len(mismatches), 1)
        self.assertIn("judge", mismatches[0].detail)


class TestSeatMissing(RoutingConsistencyGateTestBase):
    def test_seat_only_in_routing_errors(self):
        # Drop red_team from router.yaml
        router = MATCHED_ROUTER.replace(
            "  red_team:\n    primary: groq/openai/gpt-oss-120b\n", "")
        self.write_pair(router, MATCHED_ROUTING)
        r = self.gate.run()
        self.assertEqual(r.severity, "ERROR")
        missing = [f for f in r.findings
                   if f.rule == "seat_missing_in_router_yaml"]
        self.assertEqual(len(missing), 1)
        self.assertIn("red_team", missing[0].detail)

    def test_seat_only_in_router_errors(self):
        routing = MATCHED_ROUTING.replace(
            '  red_team:\n    tier_8gb: {provider: groq, model: "openai/gpt-oss-120b", family: openai_oss}\n',
            "")
        self.write_pair(MATCHED_ROUTER, routing)
        r = self.gate.run()
        self.assertEqual(r.severity, "ERROR")
        missing = [f for f in r.findings
                   if f.rule == "seat_missing_in_routing_yaml"]
        self.assertEqual(len(missing), 1)


class TestFileMissing(RoutingConsistencyGateTestBase):
    def test_missing_router_errors(self):
        (self.workspace / "pipeline" / "orchestrator" / "routing.yaml").write_text(MATCHED_ROUTING)
        r = self.gate.run()
        self.assertEqual(r.severity, "ERROR")
        self.assertTrue(any(f.rule == "router_yaml_missing" for f in r.findings))

    def test_missing_routing_errors(self):
        (self.workspace / "router.yaml").write_text(MATCHED_ROUTER)
        r = self.gate.run()
        self.assertEqual(r.severity, "ERROR")
        self.assertTrue(any(f.rule == "routing_yaml_missing" for f in r.findings))


if __name__ == "__main__":
    unittest.main(verbosity=2)
