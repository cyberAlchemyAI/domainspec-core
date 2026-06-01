"""Round-3 tests for ``pipeline.seats.judge.provider_google``.

Covers BYOK loading, payload-ceiling pre-check, transport retry semantics,
semantic-4xx + 5xx routing, response parsing, and router-yaml binding
loader cross-family discipline.
"""
from __future__ import annotations

import json
import urllib.error
from typing import Any, Mapping

import pytest

from pipeline.seats.judge.provider_google import (
    DEFAULT_MAX_OUTPUT_TOKENS,
    F_JUDGE_BYOK_MISSING,
    F_JUDGE_PAYLOAD_CEILING,
    F_JUDGE_PROVIDER_MALFORMED,
    F_JUDGE_SEMANTIC_FAILURE,
    F_JUDGE_TRANSPORT_FAILURE,
    GoogleBYOKMissing,
    GoogleBinding,
    GooglePayloadCeiling,
    GoogleProviderMalformed,
    GoogleResponse,
    GoogleSemanticFailure,
    GoogleTransportFailure,
    call_google_judge,
    estimate_prompt_tokens,
    load_judge_binding_from_router_mapping,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _key_retrieve_ok(*, org_slug: str, key_id: str) -> bytes:
    return b"AIza-test-key"


def _key_retrieve_empty(*, org_slug: str, key_id: str) -> bytes:
    return b""


def _key_retrieve_raises(*, org_slug: str, key_id: str) -> bytes:
    raise RuntimeError("keystore down")


def _key_retrieve_non_ascii(*, org_slug: str, key_id: str) -> bytes:
    return "AIza-é".encode("utf-8")


def _make_clock(start: float = 1000.0):
    state = {"t": start}

    def _now() -> float:
        return state["t"]

    def _advance(delta: float) -> None:
        state["t"] += delta

    return _now, _advance


def _make_sleep_recorder():
    sleeps: list[float] = []

    def _sleep(seconds: float, /) -> None:
        sleeps.append(seconds)

    return _sleep, sleeps


def _ok_response_bytes() -> bytes:
    return json.dumps(
        {
            "candidates": [
                {
                    "content": {
                        "parts": [{"text": '{"score": 7, "ok": true}'}],
                        "role": "model",
                    },
                    "finishReason": "STOP",
                    "index": 0,
                }
            ],
            "modelVersion": "gemini-2.5-pro-002",
        }
    ).encode("utf-8")


def _make_http_post_returning(
    status: int, body: bytes
):
    calls: list[Mapping[str, Any]] = []

    def _post(*, url, headers, body, timeout_seconds):
        calls.append(
            {
                "url": url,
                "headers": dict(headers),
                "body": body,
                "timeout_seconds": timeout_seconds,
            }
        )
        return status, body if False else _ok_response_bytes() if status == 200 else b""

    return _post, calls


# ---------------------------------------------------------------------------
# GoogleBinding shape
# ---------------------------------------------------------------------------


class TestGoogleBinding:
    def test_construct_default_max_tokens(self) -> None:
        b = GoogleBinding(
            primary_model_id="gemini-2.5-pro",
            fallback_model_id="qwen3-32b",
        )
        assert b.max_output_tokens == DEFAULT_MAX_OUTPUT_TOKENS
        assert b.prompt_token_ceiling == 1_000_000

    def test_empty_primary_rejected(self) -> None:
        with pytest.raises(ValueError, match="primary_model_id"):
            GoogleBinding(primary_model_id="", fallback_model_id="x")

    def test_empty_fallback_rejected(self) -> None:
        with pytest.raises(ValueError, match="fallback_model_id"):
            GoogleBinding(primary_model_id="x", fallback_model_id="")

    def test_zero_max_tokens_rejected(self) -> None:
        with pytest.raises(ValueError, match="max_output_tokens"):
            GoogleBinding(
                primary_model_id="x",
                fallback_model_id="y",
                max_output_tokens=0,
            )

    def test_zero_ceiling_rejected(self) -> None:
        with pytest.raises(ValueError, match="prompt_token_ceiling"):
            GoogleBinding(
                primary_model_id="x",
                fallback_model_id="y",
                prompt_token_ceiling=0,
            )


# ---------------------------------------------------------------------------
# GoogleResponse shape
# ---------------------------------------------------------------------------


class TestGoogleResponse:
    def test_construct_ok(self) -> None:
        resp = GoogleResponse(
            landed_model_id="gemini-2.5-pro",
            text_body="hello",
            prompt_token_estimate=10,
            response_sha3_512="a" * 128,
            raw_response_canonical_json_bytes=b"{}",
        )
        assert resp.landed_model_id == "gemini-2.5-pro"

    def test_short_sha_rejected(self) -> None:
        with pytest.raises(ValueError, match="response_sha3_512"):
            GoogleResponse(
                landed_model_id="g",
                text_body="x",
                prompt_token_estimate=1,
                response_sha3_512="abc",
                raw_response_canonical_json_bytes=b"",
            )

    def test_uppercase_sha_rejected(self) -> None:
        with pytest.raises(ValueError, match="lowercase"):
            GoogleResponse(
                landed_model_id="g",
                text_body="x",
                prompt_token_estimate=1,
                response_sha3_512="A" * 128,
                raw_response_canonical_json_bytes=b"",
            )

    def test_empty_landed_model_rejected(self) -> None:
        with pytest.raises(ValueError, match="landed_model_id"):
            GoogleResponse(
                landed_model_id="",
                text_body="x",
                prompt_token_estimate=1,
                response_sha3_512="a" * 128,
                raw_response_canonical_json_bytes=b"",
            )


# ---------------------------------------------------------------------------
# estimate_prompt_tokens
# ---------------------------------------------------------------------------


class TestEstimateTokens:
    def test_zero_length(self) -> None:
        assert estimate_prompt_tokens("") == 0

    def test_typical(self) -> None:
        # 37 chars / 3.7 = 10
        assert estimate_prompt_tokens("a" * 37) == 10

    def test_floor(self) -> None:
        # 36 chars / 3.7 = 9.72 → 9
        assert estimate_prompt_tokens("a" * 36) == 9


# ---------------------------------------------------------------------------
# load_judge_binding_from_router_mapping
# ---------------------------------------------------------------------------


class TestLoadBinding:
    def test_happy_path(self) -> None:
        mapping = {
            "tilth": {
                "judge": {
                    "primary": "google/gemini-2.5-pro",
                    "fallback": "groq/qwen/qwen3-32b",
                }
            }
        }
        binding = load_judge_binding_from_router_mapping(mapping)
        assert binding.primary_model_id == "gemini-2.5-pro"
        assert binding.fallback_model_id == "qwen/qwen3-32b"

    def test_missing_tilth_rejected(self) -> None:
        with pytest.raises(ValueError, match="tilth"):
            load_judge_binding_from_router_mapping({})

    def test_missing_judge_rejected(self) -> None:
        with pytest.raises(ValueError, match="judge"):
            load_judge_binding_from_router_mapping({"tilth": {}})

    def test_non_google_primary_rejected(self) -> None:
        # Cross-family discipline: refuse anthropic/openai/groq primaries.
        mapping = {
            "tilth": {
                "judge": {
                    "primary": "anthropic/claude-opus-4-7",
                    "fallback": "x",
                }
            }
        }
        with pytest.raises(ValueError, match="google"):
            load_judge_binding_from_router_mapping(mapping)

    def test_non_string_primary_rejected(self) -> None:
        mapping = {
            "tilth": {"judge": {"primary": 42, "fallback": "x"}}
        }
        with pytest.raises(ValueError, match="google"):
            load_judge_binding_from_router_mapping(mapping)

    def test_missing_fallback_rejected(self) -> None:
        mapping = {
            "tilth": {
                "judge": {"primary": "google/gemini-2.5-pro", "fallback": ""}
            }
        }
        with pytest.raises(ValueError, match="fallback"):
            load_judge_binding_from_router_mapping(mapping)

    def test_fallback_without_slash(self) -> None:
        mapping = {
            "tilth": {
                "judge": {
                    "primary": "google/gemini-2.5-pro",
                    "fallback": "qwen3-32b",
                }
            }
        }
        binding = load_judge_binding_from_router_mapping(mapping)
        assert binding.fallback_model_id == "qwen3-32b"


# ---------------------------------------------------------------------------
# call_google_judge — happy path + error paths
# ---------------------------------------------------------------------------


def _make_binding() -> GoogleBinding:
    return GoogleBinding(
        primary_model_id="gemini-2.5-pro",
        fallback_model_id="qwen3-32b",
    )


class TestCallGoogleHappyPath:
    def test_returns_response(self) -> None:
        clock, _ = _make_clock()
        sleep, sleeps = _make_sleep_recorder()
        captured: list[Any] = []

        def _post(*, url, headers, body, timeout_seconds):
            captured.append((url, dict(headers), body, timeout_seconds))
            return 200, _ok_response_bytes()

        resp = call_google_judge(
            binding=_make_binding(),
            compiled_prompt="hello world",
            org_slug="acme",
            key_retrieve=_key_retrieve_ok,
            http_post=_post,
            clock=clock,
            sleep=sleep,
        )
        assert resp.landed_model_id == "gemini-2.5-pro-002"
        assert "score" in resp.text_body
        assert resp.prompt_token_estimate == int(len("hello world") / 3.7)
        assert sleeps == []
        url, headers, body, timeout = captured[0]
        assert "gemini-2.5-pro" in url
        assert headers["x-goog-api-key"] == "AIza-test-key"
        assert headers["content-type"] == "application/json"

    def test_landed_model_falls_back_to_request(self) -> None:
        clock, _ = _make_clock()
        sleep, _ = _make_sleep_recorder()

        def _post(*, url, headers, body, timeout_seconds):
            return 200, json.dumps(
                {
                    "candidates": [
                        {
                            "content": {
                                "parts": [{"text": "result"}],
                                "role": "model",
                            }
                        }
                    ]
                    # NOTE: no modelVersion field
                }
            ).encode("utf-8")

        resp = call_google_judge(
            binding=_make_binding(),
            compiled_prompt="x",
            org_slug="acme",
            key_retrieve=_key_retrieve_ok,
            http_post=_post,
            clock=clock,
            sleep=sleep,
        )
        assert resp.landed_model_id == "gemini-2.5-pro"


class TestCallGoogleByokFailures:
    def test_empty_key(self) -> None:
        clock, _ = _make_clock()
        sleep, _ = _make_sleep_recorder()

        def _post(*, url, headers, body, timeout_seconds):
            raise AssertionError("should not be reached")

        with pytest.raises(GoogleBYOKMissing, match=F_JUDGE_BYOK_MISSING):
            call_google_judge(
                binding=_make_binding(),
                compiled_prompt="x",
                org_slug="acme",
                key_retrieve=_key_retrieve_empty,
                http_post=_post,
                clock=clock,
                sleep=sleep,
            )

    def test_keystore_raises(self) -> None:
        clock, _ = _make_clock()
        sleep, _ = _make_sleep_recorder()

        def _post(*, url, headers, body, timeout_seconds):
            raise AssertionError("should not be reached")

        with pytest.raises(GoogleBYOKMissing, match="keystore retrieve"):
            call_google_judge(
                binding=_make_binding(),
                compiled_prompt="x",
                org_slug="acme",
                key_retrieve=_key_retrieve_raises,
                http_post=_post,
                clock=clock,
                sleep=sleep,
            )

    def test_non_ascii_key(self) -> None:
        clock, _ = _make_clock()
        sleep, _ = _make_sleep_recorder()

        def _post(*, url, headers, body, timeout_seconds):
            raise AssertionError("should not be reached")

        with pytest.raises(GoogleBYOKMissing, match="ASCII"):
            call_google_judge(
                binding=_make_binding(),
                compiled_prompt="x",
                org_slug="acme",
                key_retrieve=_key_retrieve_non_ascii,
                http_post=_post,
                clock=clock,
                sleep=sleep,
            )


class TestCallGooglePayloadCeiling:
    def test_over_ceiling_rejected(self) -> None:
        clock, _ = _make_clock()
        sleep, _ = _make_sleep_recorder()

        def _post(*, url, headers, body, timeout_seconds):
            raise AssertionError("should not be reached")

        binding = GoogleBinding(
            primary_model_id="g",
            fallback_model_id="f",
            prompt_token_ceiling=10,
        )
        with pytest.raises(GooglePayloadCeiling, match=F_JUDGE_PAYLOAD_CEILING):
            call_google_judge(
                binding=binding,
                compiled_prompt="x" * 100,  # ~27 tokens > ceiling 10
                org_slug="acme",
                key_retrieve=_key_retrieve_ok,
                http_post=_post,
                clock=clock,
                sleep=sleep,
            )


class TestCallGoogleSemantic4xx:
    def test_400_does_not_retry(self) -> None:
        clock, _ = _make_clock()
        sleep, sleeps = _make_sleep_recorder()
        call_count = [0]

        def _post(*, url, headers, body, timeout_seconds):
            call_count[0] += 1
            return 400, b'{"error":"bad request"}'

        with pytest.raises(GoogleSemanticFailure, match=F_JUDGE_SEMANTIC_FAILURE):
            call_google_judge(
                binding=_make_binding(),
                compiled_prompt="x",
                org_slug="acme",
                key_retrieve=_key_retrieve_ok,
                http_post=_post,
                clock=clock,
                sleep=sleep,
            )
        assert call_count[0] == 1
        assert sleeps == []

    def test_403_body_digest_in_message(self) -> None:
        clock, _ = _make_clock()
        sleep, _ = _make_sleep_recorder()

        def _post(*, url, headers, body, timeout_seconds):
            return 403, b'{"error":"forbidden"}'

        with pytest.raises(GoogleSemanticFailure) as ei:
            call_google_judge(
                binding=_make_binding(),
                compiled_prompt="x",
                org_slug="acme",
                key_retrieve=_key_retrieve_ok,
                http_post=_post,
                clock=clock,
                sleep=sleep,
            )
        assert "body_sha3_256_prefix16" in str(ei.value)
        # Body content NOT in message — digest only.
        assert "forbidden" not in str(ei.value)


class TestCallGoogleTransport5xx:
    def test_500_retries_once_then_succeeds(self) -> None:
        clock, advance = _make_clock()
        sleep, sleeps = _make_sleep_recorder()
        statuses = [500, 200]

        def _post(*, url, headers, body, timeout_seconds):
            advance(0.1)
            status = statuses.pop(0)
            return status, _ok_response_bytes() if status == 200 else b"err"

        resp = call_google_judge(
            binding=_make_binding(),
            compiled_prompt="x",
            org_slug="acme",
            key_retrieve=_key_retrieve_ok,
            http_post=_post,
            clock=clock,
            sleep=sleep,
        )
        assert resp.landed_model_id
        assert sleeps == [30.0]

    def test_500_two_consecutive_raises_transport(self) -> None:
        clock, advance = _make_clock()
        sleep, sleeps = _make_sleep_recorder()

        def _post(*, url, headers, body, timeout_seconds):
            advance(0.1)
            return 503, b"down"

        with pytest.raises(GoogleTransportFailure, match=F_JUDGE_TRANSPORT_FAILURE):
            call_google_judge(
                binding=_make_binding(),
                compiled_prompt="x",
                org_slug="acme",
                key_retrieve=_key_retrieve_ok,
                http_post=_post,
                clock=clock,
                sleep=sleep,
            )
        assert sleeps == [30.0]

    def test_url_error_retries(self) -> None:
        clock, advance = _make_clock()
        sleep, sleeps = _make_sleep_recorder()
        attempts = [0]

        def _post(*, url, headers, body, timeout_seconds):
            attempts[0] += 1
            advance(0.1)
            if attempts[0] == 1:
                raise urllib.error.URLError("connection refused")
            return 200, _ok_response_bytes()

        resp = call_google_judge(
            binding=_make_binding(),
            compiled_prompt="x",
            org_slug="acme",
            key_retrieve=_key_retrieve_ok,
            http_post=_post,
            clock=clock,
            sleep=sleep,
        )
        assert resp.landed_model_id
        assert sleeps == [30.0]

    def test_two_url_errors_raises_transport_with_class_only(self) -> None:
        clock, advance = _make_clock()
        sleep, _ = _make_sleep_recorder()

        def _post(*, url, headers, body, timeout_seconds):
            advance(0.1)
            raise urllib.error.URLError("connection refused secret-host.local")

        with pytest.raises(GoogleTransportFailure) as ei:
            call_google_judge(
                binding=_make_binding(),
                compiled_prompt="x",
                org_slug="acme",
                key_retrieve=_key_retrieve_ok,
                http_post=_post,
                clock=clock,
                sleep=sleep,
            )
        # Sanitization: class name only, not the host string.
        assert "URLError" in str(ei.value)
        assert "secret-host.local" not in str(ei.value)

    def test_timeout_then_success(self) -> None:
        clock, advance = _make_clock()
        sleep, sleeps = _make_sleep_recorder()
        attempts = [0]

        def _post(*, url, headers, body, timeout_seconds):
            attempts[0] += 1
            advance(0.1)
            if attempts[0] == 1:
                raise TimeoutError("read timeout")
            return 200, _ok_response_bytes()

        resp = call_google_judge(
            binding=_make_binding(),
            compiled_prompt="x",
            org_slug="acme",
            key_retrieve=_key_retrieve_ok,
            http_post=_post,
            clock=clock,
            sleep=sleep,
        )
        assert resp.landed_model_id
        assert sleeps == [30.0]

    def test_120s_wall_clock_cap_exceeded(self) -> None:
        clock, advance = _make_clock()
        sleep, sleeps = _make_sleep_recorder()
        attempts = [0]

        def _post(*, url, headers, body, timeout_seconds):
            attempts[0] += 1
            advance(0.1)
            if attempts[0] == 1:
                # Force the wall clock past 120s before retry.
                advance(125.0)
                raise urllib.error.URLError("first failure")
            raise AssertionError("should not retry past wall-clock cap")

        with pytest.raises(GoogleTransportFailure, match="120s wall-clock"):
            call_google_judge(
                binding=_make_binding(),
                compiled_prompt="x",
                org_slug="acme",
                key_retrieve=_key_retrieve_ok,
                http_post=_post,
                clock=clock,
                sleep=sleep,
            )


# ---------------------------------------------------------------------------
# 2xx parsing failures (GoogleProviderMalformed)
# ---------------------------------------------------------------------------


class TestParseProviderMalformed:
    def _make_post(self, body: bytes):
        def _post(*, url, headers, body, timeout_seconds):
            return 200, body  # type: ignore[misc]

        return _post

    def _call(self, body: bytes):
        clock, _ = _make_clock()
        sleep, _ = _make_sleep_recorder()

        def _post(*, url, headers, body, timeout_seconds):
            return 200, body if isinstance(body, bytes) else b""

        # Capture body in closure
        captured_body = body

        def _post_real(*, url, headers, body, timeout_seconds):
            return 200, captured_body

        return call_google_judge(
            binding=_make_binding(),
            compiled_prompt="x",
            org_slug="acme",
            key_retrieve=_key_retrieve_ok,
            http_post=_post_real,
            clock=clock,
            sleep=sleep,
        )

    def test_non_json_2xx(self) -> None:
        with pytest.raises(GoogleProviderMalformed, match=F_JUDGE_PROVIDER_MALFORMED):
            self._call(b"not json at all")

    def test_top_level_not_object(self) -> None:
        with pytest.raises(GoogleProviderMalformed, match="top-level"):
            self._call(b'["array", "not", "object"]')

    def test_missing_candidates(self) -> None:
        with pytest.raises(GoogleProviderMalformed, match="candidates"):
            self._call(b'{"modelVersion": "x"}')

    def test_empty_candidates(self) -> None:
        with pytest.raises(GoogleProviderMalformed, match="candidates"):
            self._call(b'{"candidates": []}')

    def test_candidates_not_object(self) -> None:
        with pytest.raises(GoogleProviderMalformed, match="candidates\\[0\\]"):
            self._call(b'{"candidates": ["string"]}')

    def test_missing_content(self) -> None:
        with pytest.raises(GoogleProviderMalformed, match="content"):
            self._call(b'{"candidates": [{}]}')

    def test_missing_parts(self) -> None:
        with pytest.raises(GoogleProviderMalformed, match="parts"):
            self._call(b'{"candidates": [{"content": {}}]}')

    def test_empty_parts(self) -> None:
        with pytest.raises(GoogleProviderMalformed, match="parts"):
            self._call(
                b'{"candidates": [{"content": {"parts": []}}]}'
            )

    def test_no_text_in_parts(self) -> None:
        with pytest.raises(GoogleProviderMalformed, match="no text content"):
            self._call(
                b'{"candidates": [{"content": {"parts": [{"image": "x"}]}}]}'
            )

    def test_non_dict_part_skipped(self) -> None:
        # A non-dict part should be silently skipped — only fails if
        # ALL parts have no text.
        body = json.dumps(
            {
                "candidates": [
                    {
                        "content": {
                            "parts": [
                                "string-part",
                                {"text": "valid"},
                            ]
                        }
                    }
                ]
            }
        ).encode("utf-8")
        clock, _ = _make_clock()
        sleep, _ = _make_sleep_recorder()

        def _post(*, url, headers, body, timeout_seconds):
            return 200, body  # type: ignore[misc]

        captured_body = body

        def _post_real(*, url, headers, body, timeout_seconds):
            return 200, captured_body

        resp = call_google_judge(
            binding=_make_binding(),
            compiled_prompt="x",
            org_slug="acme",
            key_retrieve=_key_retrieve_ok,
            http_post=_post_real,
            clock=clock,
            sleep=sleep,
        )
        assert resp.text_body == "valid"
