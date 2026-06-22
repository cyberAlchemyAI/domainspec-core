import json
import tempfile
import unittest
from pathlib import Path

from poker_agent_arena.constants import FORBIDDEN_PUBLIC_FIELDS, PROJECT_ROOT
from poker_agent_arena.games.kuhn import KuhnGame
from poker_agent_arena.protocol.validation import find_forbidden_fields, parse_agent_output
from poker_agent_arena.runner.match import replay_to_dir, run_eval


class LocalArenaCliTests(unittest.TestCase):
    def setUp(self):
        (PROJECT_ROOT / ".tmp").mkdir(exist_ok=True)

    def test_decision_envelope_does_not_expose_forbidden_fields(self):
        game = KuhnGame("match-test", "hand-test", "seed-handle", "raw-seed")
        envelope = game.decision_envelope(0, 5000)
        self.assertEqual([], find_forbidden_fields(envelope))
        text = json.dumps(envelope)
        for forbidden in FORBIDDEN_PUBLIC_FIELDS:
            self.assertNotIn(forbidden, text)

    def test_parse_invalid_agent_output(self):
        parsed = parse_agent_output("I call\n")
        self.assertEqual("invalid", parsed.status)
        self.assertEqual("prose_before_json", parsed.event_code)
        parsed = parse_agent_output('{"a": 1} {"b": 2}\n')
        self.assertEqual("invalid", parsed.status)
        self.assertEqual("extra_json_object", parsed.event_code)

    def test_eval_and_replay_clean_agents(self):
        with tempfile.TemporaryDirectory(dir=PROJECT_ROOT / ".tmp") as tmp:
            out = Path(tmp) / "clean"
            result = run_eval(
                str(PROJECT_ROOT / "examples/agents/check_call.py"),
                str(PROJECT_ROOT / "examples/agents/legal_random.py"),
                out,
                max_hands=2,
            )
            self.assertTrue(result.ok)
            replay_report = replay_to_dir(out / "private-transcript.jsonl", out / "replay")
            self.assertTrue(replay_report["ok"])
            public_text = (out / "replay/public-replay.json").read_text()
            self.assertNotIn("raw_seed", public_text)
            self.assertNotIn("deck_order", public_text)

    def test_timeout_agent_records_timeout_and_fallback(self):
        with tempfile.TemporaryDirectory(dir=PROJECT_ROOT / ".tmp") as tmp:
            out = Path(tmp) / "timeout"
            result = run_eval(
                str(PROJECT_ROOT / "examples/agents/timeout.py"),
                str(PROJECT_ROOT / "examples/agents/check_call.py"),
                out,
                decision_timeout_ms=50,
                process_kill_after_ms=100,
                max_hands=1,
            )
            self.assertTrue(result.ok)
            agent_a = result.diagnostics["agents"]["agent_a"]
            self.assertGreater(agent_a["timeout_rate"], 0)
            self.assertGreater(agent_a["fallback_count"], 0)


if __name__ == "__main__":
    unittest.main()
