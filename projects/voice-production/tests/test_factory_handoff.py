from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


STAGING_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(STAGING_ROOT))

from voice_production.compiler_config import (  # noqa: E402
    compiler_config_from_json_bytes,
)
from voice_production.factory_handoff import (  # noqa: E402
    FactoryHandoffError,
    validate_factory_handoff,
)


SOURCE_PATH = REPOSITORY_ROOT / (
    "projects/lucifers-lights/drafts/graphic-novel/chapter-01/audio/"
    "elevenlabs-voiceover-studio.csv"
)
CONFIG_PATH = (
    REPOSITORY_ROOT / "projects/lucifers-lights/factory/voice/chapter-01.json"
)
HANDOFF_PATH = REPOSITORY_ROOT / (
    "projects/lucifers-lights/development/chapter-factory-runs/"
    "chapter-01-pilot/voice-handoff.json"
)


class FactoryHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source_bytes = SOURCE_PATH.read_bytes()
        cls.config_bytes = CONFIG_PATH.read_bytes()
        cls.handoff_bytes = HANDOFF_PATH.read_bytes()
        cls.config = compiler_config_from_json_bytes(cls.config_bytes)

    def validate(self, handoff_bytes: bytes, *, source_bytes: bytes | None = None):
        return validate_factory_handoff(
            handoff_bytes,
            handoff_path=HANDOFF_PATH,
            repository_root=REPOSITORY_ROOT,
            source_path=SOURCE_PATH,
            source_bytes=self.source_bytes if source_bytes is None else source_bytes,
            compiler_config_path=CONFIG_PATH,
            compiler_config_bytes=self.config_bytes,
            compiler_config=self.config,
        )

    def test_exact_factory_handoff_admits_only_local_compile(self) -> None:
        admission = self.validate(self.handoff_bytes)
        self.assertEqual(admission.project_id, "lucifers-lights")
        self.assertEqual(admission.chapter_id, "LL-CH1")
        self.assertEqual(admission.run_id, "LL-CF-CH01-PILOT")
        self.assertEqual(admission.source_sha256, self.config.expected_source_sha256)

    def test_source_byte_drift_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            FactoryHandoffError,
            "voice source digest does not match CLI bytes",
        ):
            self.validate(self.handoff_bytes, source_bytes=self.source_bytes + b"\n")

    def test_external_effect_or_binding_drift_is_rejected(self) -> None:
        cases = (
            (
                "external-effect",
                lambda handoff: handoff["external_effects"].__setitem__(
                    "provider", True
                ),
                "permits an external effect",
            ),
            (
                "chapter-run",
                lambda handoff: handoff.__setitem__("chapter_run_digest", "0" * 64),
                "chapter run digest does not match handoff",
            ),
            (
                "sync-disposition",
                lambda handoff: handoff["sync_disposition"].__setitem__(
                    "sha256", "0" * 64
                ),
                "sync disposition digest drift",
            ),
        )
        original = json.loads(self.handoff_bytes)
        for name, mutate, message in cases:
            with self.subTest(name=name):
                changed = copy.deepcopy(original)
                mutate(changed)
                with self.assertRaisesRegex(FactoryHandoffError, message):
                    self.validate(json.dumps(changed).encode("utf-8"))


if __name__ == "__main__":
    unittest.main()
