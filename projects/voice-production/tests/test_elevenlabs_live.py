from __future__ import annotations

import json
import sys
import unittest
from datetime import UTC, datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from voice_production.elevenlabs_live import (  # noqa: E402
    DirectTtsRequest,
    LiveRequestInvalid,
    ProviderRequestFailed,
    TransportResponse,
    synthesize_direct_tts,
)
from voice_production.canonical import canonical_loads, require_valid_envelope  # noqa: E402
from run_elevenlabs_audition import (  # noqa: E402
    AuditionConfigError,
    _require_current_authorization_date,
    build_receipt_artifact,
)


TEXT = "Your Light has arrived."
TEXT_SHA256 = "768821ed4f61a7283400cb9d17fc84d780fc97d1e0009e499dc742faeb6f9d64"
VOICE_ID = "SAz9YHcvj6GT2YYXdXww"
FAKE_KEY = b"test-key-material-never-returned"
FAKE_MP3 = b"ID3\x04\x00\x00\x00\x00\x00\x15" + (b"audio" * 30)


def request(**changes: object) -> DirectTtsRequest:
    values: dict[str, object] = {
        "segment_id": "segment-005",
        "speaker": "SYSTEM",
        "exact_text": TEXT,
        "exact_text_sha256": TEXT_SHA256,
        "voice_id": VOICE_ID,
        "voice_label": "River - connectivity only",
        "seed": 230823,
    }
    values.update(changes)
    return DirectTtsRequest(**values)  # type: ignore[arg-type]


class ElevenLabsLiveTests(unittest.TestCase):
    def test_authorization_date_uses_declared_civil_timezone(self) -> None:
        boundary = datetime(2026, 8, 23, 23, 30, tzinfo=UTC)
        _require_current_authorization_date(
            "2026-08-24", "Europe/London", now_utc=boundary
        )
        with self.assertRaisesRegex(AuditionConfigError, "not current"):
            _require_current_authorization_date(
                "2026-08-23", "Europe/London", now_utc=boundary
            )
        with self.assertRaisesRegex(AuditionConfigError, "unknown"):
            _require_current_authorization_date(
                "2026-08-24", "Mars/Olympus_Mons", now_utc=boundary
            )

    def test_live_receipt_bytes_are_canonical_without_a_trailing_suffix(self) -> None:
        receipt, payload = build_receipt_artifact({"status": "test-only"})
        self.assertEqual(payload[-1:], b"}")
        self.assertFalse(payload.endswith(b"\n"))
        parsed = canonical_loads(payload)
        self.assertEqual(parsed, receipt)
        require_valid_envelope(parsed)

    def test_one_bounded_request_consumes_secret_and_returns_redacted_audio(self) -> None:
        calls: list[dict[str, object]] = []

        def consume(request_digest, callback):
            calls.append({"kind": "secret", "request_digest": request_digest})
            callback(memoryview(FAKE_KEY))
            return {"digest": "a" * 64}

        def transport(url, headers, body, timeout):
            calls.append(
                {
                    "kind": "transport",
                    "url": url,
                    "headers": dict(headers),
                    "body": body,
                    "timeout": timeout,
                }
            )
            return TransportResponse(
                status_code=200,
                headers={
                    "content-type": "audio/mpeg",
                    "request-id": "provider-request-1",
                    "character-cost": "23",
                },
                body=FAKE_MP3,
            )

        result = synthesize_direct_tts(
            request(), secret_consumer=consume, transport=transport
        )
        self.assertEqual([item["kind"] for item in calls], ["secret", "transport"])
        sent = calls[1]
        self.assertEqual(sent["headers"]["xi-api-key"], FAKE_KEY.decode("ascii"))
        self.assertEqual(
            json.loads(sent["body"]),
            {
                "language_code": "en",
                "model_id": "eleven_v3",
                "seed": 230823,
                "text": TEXT,
                "voice_settings": {
                    "similarity_boost": 0.75,
                    "stability": 0.5,
                    "style": 0.0,
                    "use_speaker_boost": True,
                },
            },
        )
        self.assertEqual(result.audio_bytes, FAKE_MP3)
        self.assertEqual(result.character_cost, 23)
        rendered = json.dumps(result.safe_summary(), sort_keys=True)
        self.assertNotIn(TEXT, rendered)
        self.assertNotIn(FAKE_KEY.decode("ascii"), rendered)

    def test_request_digest_rebinds_effect_inputs(self) -> None:
        baseline = request().request_digest
        self.assertNotEqual(baseline, request(seed=230824).request_digest)
        self.assertNotEqual(
            baseline,
            request(voice_id="JBFqnCBsd6RMkjVDRZzb").request_digest,
        )
        self.assertNotEqual(baseline, request(stability=1.0).request_digest)
        self.assertNotEqual(baseline, request(speed=0.9).request_digest)
        self.assertNotEqual(
            baseline,
            request(previous_text="The prior line.").request_digest,
        )

    def test_multilingual_v2_context_omits_unsupported_language_code(self) -> None:
        contextual = request(
            model_id="eleven_multilingual_v2",
            language_code=None,
            previous_text="The phone burned with a white flame.",
            next_text="That was me. Memorable? Absolutely.",
            seed=None,
            speed=0.9,
        )
        self.assertEqual(
            contextual.body,
            {
                "model_id": "eleven_multilingual_v2",
                "next_text": "That was me. Memorable? Absolutely.",
                "previous_text": "The phone burned with a white flame.",
                "text": TEXT,
                "voice_settings": {
                    "similarity_boost": 0.75,
                    "speed": 0.9,
                    "stability": 0.5,
                    "style": 0.0,
                    "use_speaker_boost": True,
                },
            },
        )

    def test_multilingual_v2_rejects_language_code_before_secret_resolution(self) -> None:
        with self.assertRaisesRegex(LiveRequestInvalid, "language_code must be null"):
            request(model_id="eleven_multilingual_v2")

    def test_speed_outside_provider_range_is_rejected(self) -> None:
        with self.assertRaisesRegex(LiveRequestInvalid, "speed must be null"):
            request(speed=0.69)

    def test_invalid_request_fails_before_secret_resolution(self) -> None:
        calls = 0

        def consume(_request_digest, _callback):
            nonlocal calls
            calls += 1
            return {}

        with self.assertRaisesRegex(LiveRequestInvalid, "does not match"):
            invalid = request(exact_text_sha256="0" * 64)
            synthesize_direct_tts(invalid, secret_consumer=consume)
        self.assertEqual(calls, 0)

    def test_provider_error_is_reduced_to_safe_status(self) -> None:
        def consume(_request_digest, callback):
            callback(memoryview(FAKE_KEY))
            return {}

        def transport(_url, _headers, _body, _timeout):
            return TransportResponse(
                status_code=401,
                headers={"content-type": "application/json"},
                body=b'{"detail":{"status":"invalid_api_key","message":"private"}}',
            )

        with self.assertRaisesRegex(
            ProviderRequestFailed, r"HTTP 401 \(invalid_api_key\)"
        ) as raised:
            synthesize_direct_tts(
                request(), secret_consumer=consume, transport=transport
            )
        self.assertNotIn("private", str(raised.exception))

    def test_non_mp3_success_response_is_rejected(self) -> None:
        def consume(_request_digest, callback):
            callback(memoryview(FAKE_KEY))
            return {}

        def transport(_url, _headers, _body, _timeout):
            return TransportResponse(
                status_code=200,
                headers={"content-type": "application/json"},
                body=b"{}",
            )

        with self.assertRaisesRegex(ProviderRequestFailed, "invalid_mp3_response"):
            synthesize_direct_tts(
                request(), secret_consumer=consume, transport=transport
            )


if __name__ == "__main__":
    unittest.main()
