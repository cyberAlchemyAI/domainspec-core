"""Tests for pipeline.seats.scribe.provider_anthropic.

Covers: AnthropicBinding / AnthropicResponse shape invariants, token estimate,
call orchestration with injected seams, E-028 retry discipline, payload ceiling,
BYOK load path, semantic 4xx behavior, 2xx parse behavior.
"""

from __future__ import annotations

import hashlib
import json
import urllib.error

import pytest

from pipeline.seats.scribe.provider_anthropic import (
    ANTHROPIC_MESSAGES_URL,
    AnthropicBinding,
    AnthropicBYOKMissing,
    AnthropicPayloadCeiling,
    AnthropicProviderMalformed,
    AnthropicResponse,
    AnthropicSemanticFailure,
    AnthropicTransportFailure,
    _parse_anthropic_2xx_response,
    call_anthropic_scribe,
    estimate_prompt_tokens,
    load_scribe_binding_from_router_mapping,
)


def _ok_binding() -> AnthropicBinding:
    return AnthropicBinding(
        primary_model_id="claude-sonnet-4-6",
        escalation_model_id="claude-opus-4-6",
    )


def _ok_response_body(model: str = "claude-sonnet-4-6") -> bytes:
    return json.dumps(
        {
            "model": model,
            "content": [{"type": "text", "text": "hello world"}],
            "id": "msg_01",
            "stop_reason": "end_turn",
        }
    ).encode("utf-8")


# ---------- Binding shape ----------


def test_binding_constructs_ok() -> None:
    b = _ok_binding()
    assert b.primary_model_id == "claude-sonnet-4-6"
    assert b.escalation_model_id == "claude-opus-4-6"
    assert b.max_tokens == 64000
    assert b.prompt_token_ceiling == 180_000


def test_binding_is_frozen() -> None:
    b = _ok_binding()
    with pytest.raises((AttributeError, Exception)):
        b.primary_model_id = "other"  # type: ignore[misc]


def test_binding_rejects_empty_primary() -> None:
    with pytest.raises(ValueError, match="primary_model_id"):
        AnthropicBinding(primary_model_id="", escalation_model_id="x")


def test_binding_rejects_empty_escalation() -> None:
    with pytest.raises(ValueError, match="escalation_model_id"):
        AnthropicBinding(primary_model_id="x", escalation_model_id="")


def test_binding_rejects_nonpositive_max_tokens() -> None:
    with pytest.raises(ValueError, match="max_tokens"):
        AnthropicBinding(primary_model_id="x", escalation_model_id="y", max_tokens=0)


def test_binding_rejects_nonpositive_ceiling() -> None:
    with pytest.raises(ValueError, match="ceiling"):
        AnthropicBinding(
            primary_model_id="x", escalation_model_id="y", prompt_token_ceiling=-1
        )


# ---------- AnthropicResponse shape ----------


def test_response_ok() -> None:
    body = _ok_response_body()
    sha = hashlib.sha3_512(body).hexdigest()
    r = AnthropicResponse(
        landed_model_id="claude-sonnet-4-6",
        text_body="hi",
        prompt_token_estimate=12,
        response_sha3_512=sha,
        raw_response_canonical_json_bytes=body,
    )
    assert r.landed_model_id == "claude-sonnet-4-6"


def test_response_rejects_short_sha() -> None:
    with pytest.raises(ValueError, match="128-hex"):
        AnthropicResponse(
            landed_model_id="x",
            text_body="y",
            prompt_token_estimate=1,
            response_sha3_512="abc",
            raw_response_canonical_json_bytes=b"{}",
        )


def test_response_rejects_uppercase_sha() -> None:
    sha = "A" * 128
    with pytest.raises(ValueError, match="lowercase"):
        AnthropicResponse(
            landed_model_id="x",
            text_body="y",
            prompt_token_estimate=1,
            response_sha3_512=sha,
            raw_response_canonical_json_bytes=b"{}",
        )


# ---------- Token estimate ----------


def test_estimate_prompt_tokens_is_chars_over_3_7() -> None:
    assert estimate_prompt_tokens("") == 0
    # 37 chars / 3.7 = 10.0
    assert estimate_prompt_tokens("x" * 37) == 10


def test_estimate_prompt_tokens_large() -> None:
    # Sanity: 3700 chars / 3.7 = 1000
    assert estimate_prompt_tokens("x" * 3700) == 1000


# ---------- _parse_anthropic_2xx_response ----------


def test_parse_2xx_ok() -> None:
    r = _parse_anthropic_2xx_response(
        resp_bytes=_ok_response_body(), prompt_token_estimate=42
    )
    assert r.landed_model_id == "claude-sonnet-4-6"
    assert r.text_body == "hello world"
    assert r.prompt_token_estimate == 42


def test_parse_2xx_concatenates_multi_block() -> None:
    body = json.dumps(
        {
            "model": "m",
            "content": [
                {"type": "text", "text": "alpha "},
                {"type": "text", "text": "beta"},
            ],
        }
    ).encode()
    r = _parse_anthropic_2xx_response(resp_bytes=body, prompt_token_estimate=1)
    assert r.text_body == "alpha beta"


def test_parse_2xx_rejects_nonjson() -> None:
    # Sanitization (Scribe R3 narrow-fix 2026-04-29): JSONDecodeError .msg
    # content must NOT leak into the ProviderMalformed message — only the
    # class name + body hash + length.
    body = b"not json with secret /op/path content"
    with pytest.raises(AnthropicProviderMalformed) as excinfo:
        _parse_anthropic_2xx_response(resp_bytes=body, prompt_token_estimate=0)
    msg = str(excinfo.value)
    assert "non-JSON 2xx body" in msg
    assert "exception_class=JSONDecodeError" in msg
    assert "body_sha3_256_prefix16=" in msg
    assert f"body_len_bytes={len(body)}" in msg
    # Defense-in-depth: raw body must not leak.
    assert b"secret /op/path content".decode() not in msg


def test_parse_2xx_rejects_missing_model() -> None:
    body = json.dumps({"content": [{"type": "text", "text": "x"}]}).encode()
    with pytest.raises(AnthropicProviderMalformed, match="model"):
        _parse_anthropic_2xx_response(resp_bytes=body, prompt_token_estimate=0)


def test_parse_2xx_rejects_empty_content() -> None:
    body = json.dumps({"model": "m", "content": []}).encode()
    with pytest.raises(AnthropicProviderMalformed, match="content"):
        _parse_anthropic_2xx_response(resp_bytes=body, prompt_token_estimate=0)


def test_parse_2xx_rejects_all_nontext_blocks() -> None:
    body = json.dumps(
        {"model": "m", "content": [{"type": "tool_use", "id": "x"}]}
    ).encode()
    with pytest.raises(AnthropicProviderMalformed, match="no text"):
        _parse_anthropic_2xx_response(resp_bytes=body, prompt_token_estimate=0)


def test_parse_2xx_rejects_toplevel_list() -> None:
    body = b"[]"
    with pytest.raises(AnthropicProviderMalformed, match="not object"):
        _parse_anthropic_2xx_response(resp_bytes=body, prompt_token_estimate=0)


# ---------- call_anthropic_scribe orchestration ----------


class _ClockStub:
    def __init__(self, values: list[float]) -> None:
        self._values = list(values)

    def __call__(self) -> float:
        if self._values:
            return self._values.pop(0)
        return 0.0


class _SleepStub:
    def __init__(self) -> None:
        self.calls: list[float] = []

    def __call__(self, seconds: float, /) -> None:
        self.calls.append(seconds)


def _fake_key_retrieve_ok(*, org_slug: str, key_id: str) -> bytes:
    assert key_id == "anthropic"
    return b"sk-ant-test"


def _fake_key_retrieve_empty(*, org_slug: str, key_id: str) -> bytes:
    return b""


def _fake_key_retrieve_raise(*, org_slug: str, key_id: str) -> bytes:
    raise OSError("keychain locked")


def _fake_key_retrieve_nonascii(*, org_slug: str, key_id: str) -> bytes:
    return "sk-αντ".encode("utf-8")


def test_call_happy_path() -> None:
    def http_post(*, url, headers, body, timeout_seconds):
        assert url == ANTHROPIC_MESSAGES_URL
        assert headers["x-api-key"] == "sk-ant-test"
        assert headers["anthropic-version"] == "2023-06-01"
        parsed = json.loads(body)
        assert parsed["max_tokens"] == 64000
        assert parsed["messages"][0]["content"] == "compiled-prompt"
        return 200, _ok_response_body()

    sleep = _SleepStub()
    r = call_anthropic_scribe(
        binding=_ok_binding(),
        compiled_prompt="compiled-prompt",
        org_slug="test_org",
        key_retrieve=_fake_key_retrieve_ok,
        http_post=http_post,
        clock=_ClockStub([0.0, 0.5]),
        sleep=sleep,
    )
    assert r.landed_model_id == "claude-sonnet-4-6"
    assert r.text_body == "hello world"
    assert sleep.calls == []


def test_call_payload_ceiling() -> None:
    def http_post(**_: object) -> tuple[int, bytes]:
        raise AssertionError("http should not be called when ceiling exceeds")

    b = AnthropicBinding(
        primary_model_id="x", escalation_model_id="y", prompt_token_ceiling=5
    )
    with pytest.raises(AnthropicPayloadCeiling):
        call_anthropic_scribe(
            binding=b,
            compiled_prompt="x" * 1000,
            org_slug="o",
            key_retrieve=_fake_key_retrieve_ok,
            http_post=http_post,
            clock=_ClockStub([0.0]),
            sleep=_SleepStub(),
        )


def test_call_byok_missing_empty() -> None:
    def http_post(**_: object) -> tuple[int, bytes]:
        raise AssertionError("http should not be called when key missing")

    with pytest.raises(AnthropicBYOKMissing, match="empty key"):
        call_anthropic_scribe(
            binding=_ok_binding(),
            compiled_prompt="p",
            org_slug="o",
            key_retrieve=_fake_key_retrieve_empty,
            http_post=http_post,
            clock=_ClockStub([0.0]),
            sleep=_SleepStub(),
        )


def test_call_byok_missing_raise() -> None:
    """Sanitization (Scribe R3 narrow-fix 2026-04-29): the keystore exception
    .args content (e.g. ``"keychain locked"``) must NOT leak into the
    AnthropicBYOKMissing message — only the exception class name."""

    def http_post(**_: object) -> tuple[int, bytes]:
        raise AssertionError("http should not be called when key retrieve raises")

    with pytest.raises(AnthropicBYOKMissing) as excinfo:
        call_anthropic_scribe(
            binding=_ok_binding(),
            compiled_prompt="p",
            org_slug="o",
            key_retrieve=_fake_key_retrieve_raise,
            http_post=http_post,
            clock=_ClockStub([0.0]),
            sleep=_SleepStub(),
        )
    msg = str(excinfo.value)
    assert "retrieve failed" in msg
    assert "exception_class=OSError" in msg
    # Defense-in-depth: keystore exception .args content must not leak.
    assert "keychain locked" not in msg


def test_call_byok_nonascii() -> None:
    def http_post(**_: object) -> tuple[int, bytes]:
        raise AssertionError("http should not be called")

    with pytest.raises(AnthropicBYOKMissing, match="ASCII"):
        call_anthropic_scribe(
            binding=_ok_binding(),
            compiled_prompt="p",
            org_slug="o",
            key_retrieve=_fake_key_retrieve_nonascii,
            http_post=http_post,
            clock=_ClockStub([0.0]),
            sleep=_SleepStub(),
        )


def test_call_semantic_4xx_never_retries() -> None:
    calls = {"n": 0}
    response_body = (
        b'{"type":"error","error":{"type":"invalid_request_error",'
        b'"message":"sensitive operator data echo"}}'
    )

    def http_post(**_: object) -> tuple[int, bytes]:
        calls["n"] += 1
        return 400, response_body

    # Sanitization (Scribe R3 narrow-fix 2026-04-29): exception carries SHA
    # prefix + length, NOT the raw response body.
    with pytest.raises(AnthropicSemanticFailure) as excinfo:
        call_anthropic_scribe(
            binding=_ok_binding(),
            compiled_prompt="p",
            org_slug="o",
            key_retrieve=_fake_key_retrieve_ok,
            http_post=http_post,
            clock=_ClockStub([0.0, 0.1]),
            sleep=_SleepStub(),
        )
    msg = str(excinfo.value)
    assert "HTTP 400" in msg
    assert "body_sha3_256_prefix16=" in msg
    assert f"body_len_bytes={len(response_body)}" in msg
    # Defense-in-depth: raw error body must NOT leak via the exception
    # message — only its hash + length.
    assert b"sensitive operator data echo".decode() not in msg
    assert calls["n"] == 1  # no retry


def test_call_5xx_retries_once_then_fails() -> None:
    calls = {"n": 0}

    def http_post(**_: object) -> tuple[int, bytes]:
        calls["n"] += 1
        return 503, b"service unavailable"

    sleep = _SleepStub()
    with pytest.raises(AnthropicTransportFailure):
        call_anthropic_scribe(
            binding=_ok_binding(),
            compiled_prompt="p",
            org_slug="o",
            key_retrieve=_fake_key_retrieve_ok,
            http_post=http_post,
            clock=_ClockStub([0.0, 1.0, 2.0, 3.0]),
            sleep=sleep,
        )
    assert calls["n"] == 2  # one retry
    assert sleep.calls == [30.0]


def test_call_5xx_then_2xx_succeeds() -> None:
    responses: list[tuple[int, bytes]] = [
        (503, b"down"),
        (200, _ok_response_body()),
    ]
    calls = {"n": 0}

    def http_post(**_: object) -> tuple[int, bytes]:
        calls["n"] += 1
        return responses.pop(0)

    sleep = _SleepStub()
    r = call_anthropic_scribe(
        binding=_ok_binding(),
        compiled_prompt="p",
        org_slug="o",
        key_retrieve=_fake_key_retrieve_ok,
        http_post=http_post,
        clock=_ClockStub([0.0, 1.0, 2.0]),
        sleep=sleep,
    )
    assert calls["n"] == 2
    assert sleep.calls == [30.0]
    assert r.text_body == "hello world"


def test_call_urlerror_retries_once_then_fails() -> None:
    calls = {"n": 0}

    def http_post(**_: object) -> tuple[int, bytes]:
        calls["n"] += 1
        raise urllib.error.URLError("dns fail with sensitive hostname")

    # Sanitization (Scribe R3 narrow-fix 2026-04-29): TransportFailure
    # carries only the exception class name, NOT the URLError repr.
    with pytest.raises(AnthropicTransportFailure) as excinfo:
        call_anthropic_scribe(
            binding=_ok_binding(),
            compiled_prompt="p",
            org_slug="o",
            key_retrieve=_fake_key_retrieve_ok,
            http_post=http_post,
            clock=_ClockStub([0.0, 1.0, 2.0]),
            sleep=_SleepStub(),
        )
    msg = str(excinfo.value)
    assert "two consecutive transport-class failures" in msg
    assert "last_exception_class=URLError" in msg
    # Defense-in-depth: hostname / URL string must NOT leak.
    assert "dns fail with sensitive hostname" not in msg
    assert calls["n"] == 2


def test_call_timeout_error_retries_once() -> None:
    calls = {"n": 0}

    def http_post(**_: object) -> tuple[int, bytes]:
        calls["n"] += 1
        raise TimeoutError("read timeout")

    with pytest.raises(AnthropicTransportFailure):
        call_anthropic_scribe(
            binding=_ok_binding(),
            compiled_prompt="p",
            org_slug="o",
            key_retrieve=_fake_key_retrieve_ok,
            http_post=http_post,
            clock=_ClockStub([0.0, 1.0, 2.0]),
            sleep=_SleepStub(),
        )
    assert calls["n"] == 2


def test_call_wallclock_cap_prevents_second_attempt() -> None:
    def http_post(**_: object) -> tuple[int, bytes]:
        raise urllib.error.URLError("x")

    # clock returns 0.0 for pre-attempt1 check, then 130.0 for pre-attempt2 check.
    with pytest.raises(AnthropicTransportFailure):
        call_anthropic_scribe(
            binding=_ok_binding(),
            compiled_prompt="p",
            org_slug="o",
            key_retrieve=_fake_key_retrieve_ok,
            http_post=http_post,
            clock=_ClockStub([0.0, 130.0]),
            sleep=_SleepStub(),
        )


# ---------- load_scribe_binding_from_router_mapping ----------


def test_load_binding_happy() -> None:
    router = {
        "tilth": {
            "scribe": {
                "primary": "anthropic/claude-sonnet-4-6",
                "escalation": "anthropic/claude-opus-4-6",
            }
        }
    }
    b = load_scribe_binding_from_router_mapping(router)
    assert b.primary_model_id == "claude-sonnet-4-6"
    assert b.escalation_model_id == "claude-opus-4-6"


def test_load_binding_missing_tilth() -> None:
    with pytest.raises(ValueError, match="tilth"):
        load_scribe_binding_from_router_mapping({})


def test_load_binding_missing_scribe() -> None:
    with pytest.raises(ValueError, match="scribe"):
        load_scribe_binding_from_router_mapping({"tilth": {}})


def test_load_binding_rejects_non_anthropic_primary() -> None:
    router = {
        "tilth": {
            "scribe": {
                "primary": "groq/qwen",
                "escalation": "anthropic/claude-opus-4-6",
            }
        }
    }
    with pytest.raises(ValueError, match="primary"):
        load_scribe_binding_from_router_mapping(router)


def test_load_binding_rejects_non_anthropic_escalation() -> None:
    router = {
        "tilth": {
            "scribe": {
                "primary": "anthropic/claude-sonnet-4-6",
                "escalation": "groq/qwen",
            }
        }
    }
    with pytest.raises(ValueError, match="escalation"):
        load_scribe_binding_from_router_mapping(router)
