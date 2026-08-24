from __future__ import annotations

import hashlib
import json
import math
import struct
import subprocess
import sys
import tempfile
import unittest
import wave
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from master_elevenlabs_audition import (  # noqa: E402
    DEFAULT_CHROMIUM,
    DEFAULT_NODE,
    DEFAULT_PLAYWRIGHT_MODULE,
    RENDER_SCRIPT,
    build_master_receipt_artifact,
    load_mastering_profile,
)
from voice_production.canonical import (  # noqa: E402
    canonical_loads,
    require_valid_envelope,
)


PROFILE = (
    REPOSITORY_ROOT
    / "projects/lucifers-lights/factory/voice/lucifers-lights-halo-v1.json"
)
PROFILE_V2 = (
    REPOSITORY_ROOT
    / "projects/lucifers-lights/factory/voice/lucifers-lights-halo-v2.json"
)
PROFILE_V3 = (
    REPOSITORY_ROOT
    / "projects/lucifers-lights/factory/voice/lucifers-lights-slow-dark-v3.json"
)


class MasteringTests(unittest.TestCase):
    def test_profile_is_closed_and_local_only(self) -> None:
        profile, payload = load_mastering_profile(PROFILE)
        self.assertEqual(profile["identity"]["profile_id"], "lucifers-lights-halo-v1")
        self.assertFalse(profile["authority"]["publication"])
        self.assertEqual(profile["authority"]["canonical_cast_effect"], "none")
        self.assertEqual(hashlib.sha256(payload).hexdigest(), hashlib.sha256(PROFILE.read_bytes()).hexdigest())
        profile_v2, _ = load_mastering_profile(PROFILE_V2)
        self.assertEqual(profile_v2["dynamics"]["target_rms_dbfs"], -18)
        self.assertEqual(profile_v2["reverb"]["wet_db"], -16.5)
        profile_v3, _ = load_mastering_profile(PROFILE_V3)
        self.assertEqual(profile_v3["performance"]["playback_rate"], 0.95)
        self.assertEqual(profile_v3["tone"]["high_shelf_gain_db"], -1.0)

    def test_master_receipt_bytes_are_canonical(self) -> None:
        receipt, payload = build_master_receipt_artifact({"status": "test-only"})
        self.assertFalse(payload.endswith(b"\n"))
        parsed = canonical_loads(payload)
        self.assertEqual(parsed, receipt)
        require_valid_envelope(parsed)

    def test_pinned_browser_renderer_is_deterministic_24bit_stereo(self) -> None:
        for path in (DEFAULT_NODE, DEFAULT_PLAYWRIGHT_MODULE, DEFAULT_CHROMIUM):
            if not path.exists():
                self.skipTest(f"shared browser runtime is unavailable: {path}")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.wav"
            outputs = [root / "first.wav", root / "second.wav"]
            sample_rate = 44_100
            frames = bytearray()
            for index in range(sample_rate // 5):
                envelope = max(0.0, 1.0 - index / (sample_rate // 5))
                sample = int(
                    0.35
                    * envelope
                    * math.sin(2 * math.pi * 330 * index / sample_rate)
                    * 32767
                )
                frames.extend(struct.pack("<h", sample))
            with wave.open(str(source), "wb") as stream:
                stream.setnchannels(1)
                stream.setsampwidth(2)
                stream.setframerate(sample_rate)
                stream.writeframes(bytes(frames))

            observations = []
            for output in outputs:
                completed = subprocess.run(
                    [
                        str(DEFAULT_NODE),
                        str(RENDER_SCRIPT),
                        str(source),
                        str(output),
                        str(PROFILE_V3),
                        str(DEFAULT_PLAYWRIGHT_MODULE),
                        str(DEFAULT_CHROMIUM),
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                observations.append(json.loads(completed.stdout))
                with wave.open(str(output), "rb") as stream:
                    self.assertEqual(stream.getnchannels(), 2)
                    self.assertEqual(stream.getsampwidth(), 3)
                    self.assertEqual(stream.getframerate(), 48_000)
                    self.assertGreater(stream.getnframes(), 48_000)
            self.assertEqual(outputs[0].read_bytes(), outputs[1].read_bytes())
            self.assertEqual(observations[0]["metrics"], observations[1]["metrics"])
            metrics = observations[0]["metrics"]
            self.assertEqual(metrics["playback_rate"], 0.95)
            self.assertAlmostEqual(metrics["pitch_shift_cents"], -88.8, places=1)
            self.assertAlmostEqual(metrics["pitch_shift_semitones"], -0.888, places=3)
            self.assertAlmostEqual(
                metrics["performed_source_duration_seconds"], 0.2 / 0.95, places=4
            )
            self.assertAlmostEqual(
                metrics["duration_seconds"], 0.2 / 0.95 + 1.7, delta=1 / 48_000
            )

            ceiling_profile = json.loads(PROFILE_V2.read_text(encoding="utf-8"))
            ceiling_profile["dynamics"]["target_rms_dbfs"] = -10
            ceiling_profile["dynamics"]["max_makeup_db"] = 6
            ceiling_profile_path = root / "ceiling-profile.json"
            ceiling_profile_path.write_text(
                json.dumps(ceiling_profile), encoding="utf-8"
            )
            ceiling_source = root / "ceiling-source.wav"
            ceiling_frames = bytearray()
            for index in range(sample_rate // 5):
                if index == 256:
                    sample = int(0.99 * 32767)
                else:
                    sample = int(
                        0.02
                        * math.sin(2 * math.pi * 330 * index / sample_rate)
                        * 32767
                    )
                ceiling_frames.extend(struct.pack("<h", sample))
            with wave.open(str(ceiling_source), "wb") as stream:
                stream.setnchannels(1)
                stream.setsampwidth(2)
                stream.setframerate(sample_rate)
                stream.writeframes(bytes(ceiling_frames))
            ceiling_output = root / "ceiling.wav"
            completed = subprocess.run(
                [
                    str(DEFAULT_NODE),
                    str(RENDER_SCRIPT),
                    str(ceiling_source),
                    str(ceiling_output),
                    str(ceiling_profile_path),
                    str(DEFAULT_PLAYWRIGHT_MODULE),
                    str(DEFAULT_CHROMIUM),
                ],
                check=True,
                capture_output=True,
                text=True,
                timeout=60,
            )
            ceiling_metrics = json.loads(completed.stdout)["metrics"]
            self.assertTrue(ceiling_metrics["ceiling_limited"])
            self.assertGreater(ceiling_metrics["applied_master_gain_db"], 0)
            self.assertAlmostEqual(ceiling_metrics["peak_dbfs"], -1.5, places=5)
            self.assertLess(ceiling_metrics["rms_dbfs"], -10)


if __name__ == "__main__":
    unittest.main()
