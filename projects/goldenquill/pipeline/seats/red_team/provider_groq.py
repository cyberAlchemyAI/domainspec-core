"""pipeline.seats.red_team.provider_groq — Groq GPT-OSS-120B provider binding.

Per `router.yaml` (2026-04-19 update): Red Team primary =
``groq/openai/gpt-oss-120b`` (OpenAI-OSS family); fallback =
``anthropic/claude-haiku-4-5``; escalation = ``openai/gpt-5.1`` for
LOCK-sealed-tier audits.

R3 ships the provider as a thin HTTP wrapper around Groq's OpenAI-
compatible chat-completions API. The real network call lives behind
``# pragma: no cover`` — tests inject deterministic stubs via the
``OutboundCallable`` Protocol (bytes body + bytes response — unified
shape per §4 v2.x.5 LOCKED 2026-05-16 row 232 + §4 v2.x.6 fixture-
migration sweep 2026-05-16). Same E-017 seam discipline as Judge R3
(`pipeline.seats.judge.provider_google`).

Failure-code surface (4 codes):

- ``F_RT_PROVIDER_TRANSPORT_FAIL`` — connection / timeout / 5xx errors.
- ``F_RT_PROVIDER_AUTH_FAIL`` — 401 / 403 (BYOK key invalid or revoked).
- ``F_RT_PROVIDER_RATE_LIMITED`` — 429 (caller's responsibility to back off).
- ``F_RT_PROVIDER_PARSE_FAIL`` — model returned non-JSON or malformed JSON.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Final, Mapping

from pipeline.orchestrator.provider_boundary import (
    OutboundCallable as _OutboundCallable,
)


F_RT_PROVIDER_TRANSPORT_FAIL: Final[str] = "F-RT-PROVIDER-TRANSPORT-FAIL"
F_RT_PROVIDER_AUTH_FAIL: Final[str] = "F-RT-PROVIDER-AUTH-FAIL"
F_RT_PROVIDER_RATE_LIMITED: Final[str] = "F-RT-PROVIDER-RATE-LIMITED"
F_RT_PROVIDER_PARSE_FAIL: Final[str] = "F-RT-PROVIDER-PARSE-FAIL"


GROQ_DEFAULT_BASE_URL: Final[str] = "https://api.groq.com/openai/v1"
GROQ_DEFAULT_MODEL: Final[str] = "openai/gpt-oss-120b"
GROQ_DEFAULT_TIMEOUT_SEC: Final[float] = 60.0
GROQ_DEFAULT_MAX_TOKENS: Final[int] = 4000

assert GROQ_DEFAULT_MODEL == "openai/gpt-oss-120b", (
    "GROQ_DEFAULT_MODEL rebound; refusing to load"
)
assert GROQ_DEFAULT_TIMEOUT_SEC == 60.0, (
    "GROQ_DEFAULT_TIMEOUT_SEC rebound; refusing to load"
)


# ---------------------------------------------------------------------------
# E-017 seam: OutboundCallable Protocol
# ---------------------------------------------------------------------------
#
# Per §4 v2.x.5 LOCKED 2026-05-16 row 232 (CC-007 closure) + §4 v2.x.6
# fixture-migration sweep 2026-05-16: this seat consumes the unified
# ``OutboundCallable`` Protocol (bytes body + bytes response) defined at
# ``pipeline.orchestrator.provider_boundary``. Production wire-up at
# ``pipeline/seats/red_team/seat.py`` binds
# ``enforce_outbound_boundary(stdlib_urlopen_caller, ...)``; tests inject
# stubs matching the Protocol byte-for-byte.
#
# Historical note: the prior dual-path support (legacy ``HTTPCaller`` with
# dict body + str response, plus an XOR check in ``call_groq``) was
# preserved at §4 v2.x.5 LANDING as a documentary back-compat seam for
# existing test fixtures. The §4 v2.x.6 fixture-migration sweep retired
# the legacy Protocol after migrating ~30 test call sites in
# ``tests/seats/red_team/{test_r3_seat_provider_wiring,test_whole_section_capstone}.py``
# to the unified Protocol shape.

#: Unified OutboundCallable alias — sole supported seam shape.
OutboundCallable = _OutboundCallable


@dataclass(frozen=True, kw_only=True, slots=True)
class GroqProviderResult:
    """Deterministic result of a Groq invocation."""

    status_code: int
    raw_text: str
    parsed: dict
    failure_code: str | None
    failure_detail: str | None
    family: str = "OpenAI-OSS"
    model: str = GROQ_DEFAULT_MODEL


def _build_headers(*, api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def _build_request_body(
    *,
    model: str,
    system_prompt: str,
    user_prompt: str,
    max_tokens: int,
) -> dict[str, object]:
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.2,  # low — Red Team needs deterministic-ish prosecution
    }


def call_groq(
    *,
    http_post: "OutboundCallable",
    api_key: str,
    system_prompt: str,
    user_prompt: str,
    model: str = GROQ_DEFAULT_MODEL,
    base_url: str = GROQ_DEFAULT_BASE_URL,
    timeout_sec: float = GROQ_DEFAULT_TIMEOUT_SEC,
    max_tokens: int = GROQ_DEFAULT_MAX_TOKENS,
) -> GroqProviderResult:
    """Call Groq's chat-completions endpoint and return a structured result.

    Per §4 v2.x.5 LOCKED 2026-05-16 row 232 (CC-007 closure) + §4 v2.x.6
    fixture-migration sweep 2026-05-16:

    - Production wire-up at ``pipeline/seats/red_team/seat.py`` binds
      ``http_post=enforce_outbound_boundary(stdlib_urlopen_caller, ...)``
      (unified ``OutboundCallable`` shape — bytes body + bytes response).
    - Test fixtures inject deterministic stubs matching the
      ``OutboundCallable`` Protocol byte-for-byte.
    - The prior dual-path (legacy ``http_caller: HTTPCaller`` accepting
      dict body + str response) was retired at the §4 v2.x.6 sweep after
      migrating ~30 test call sites in
      ``tests/seats/red_team/{test_r3_seat_provider_wiring,test_whole_section_capstone}.py``
      to the unified Protocol shape. ``call_groq`` now accepts a single
      ``http_post`` parameter (required) and the XOR check is gone.
    """
    if not isinstance(api_key, str) or not api_key.strip():
        return GroqProviderResult(
            status_code=0,
            raw_text="",
            parsed={},
            failure_code=F_RT_PROVIDER_AUTH_FAIL,
            failure_detail="api_key empty",
        )
    headers = _build_headers(api_key=api_key)
    body = _build_request_body(
        model=model,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        max_tokens=max_tokens,
    )
    # OD-3 unification: encode dict → bytes once before invocation, then
    # decode bytes → str after. The wrapper at provider_boundary.py operates
    # on bytes; the post-decode is local.
    body_bytes = json.dumps(body, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )
    try:
        status_code, raw_bytes = http_post(
            url=f"{base_url}/chat/completions",
            headers=headers,
            body=body_bytes,
            timeout_seconds=timeout_sec,
        )
        raw_text = raw_bytes.decode("utf-8", errors="replace")
    except Exception as e:
        return GroqProviderResult(
            status_code=0,
            raw_text="",
            parsed={},
            failure_code=F_RT_PROVIDER_TRANSPORT_FAIL,
            failure_detail=f"{type(e).__name__}: {str(e)[:200]}",
        )

    if status_code in (401, 403):
        return GroqProviderResult(
            status_code=status_code,
            raw_text=raw_text[:500],
            parsed={},
            failure_code=F_RT_PROVIDER_AUTH_FAIL,
            failure_detail=f"HTTP {status_code} (BYOK key invalid)",
        )
    if status_code == 429:
        return GroqProviderResult(
            status_code=status_code,
            raw_text=raw_text[:500],
            parsed={},
            failure_code=F_RT_PROVIDER_RATE_LIMITED,
            failure_detail=f"HTTP 429 — caller back off",
        )
    if status_code >= 500:
        return GroqProviderResult(
            status_code=status_code,
            raw_text=raw_text[:500],
            parsed={},
            failure_code=F_RT_PROVIDER_TRANSPORT_FAIL,
            failure_detail=f"HTTP {status_code} server error",
        )
    if status_code != 200:
        return GroqProviderResult(
            status_code=status_code,
            raw_text=raw_text[:500],
            parsed={},
            failure_code=F_RT_PROVIDER_TRANSPORT_FAIL,
            failure_detail=f"unexpected HTTP {status_code}",
        )

    try:
        parsed = json.loads(raw_text)
    except Exception as e:
        return GroqProviderResult(
            status_code=status_code,
            raw_text=raw_text[:500],
            parsed={},
            failure_code=F_RT_PROVIDER_PARSE_FAIL,
            failure_detail=f"top-level JSON parse fail: {type(e).__name__}: {str(e)[:200]}",
        )

    return GroqProviderResult(
        status_code=status_code,
        raw_text=raw_text,
        parsed=parsed,
        failure_code=None,
        failure_detail=None,
    )


def extract_message_content(provider_result: GroqProviderResult) -> str | None:
    """Pull the model's message content from a successful Groq response.

    Returns ``None`` if the response shape is malformed.
    """
    if provider_result.failure_code is not None:
        return None
    try:
        choices = provider_result.parsed.get("choices", [])
        if not choices:
            return None
        return choices[0].get("message", {}).get("content")
    except (AttributeError, IndexError, KeyError, TypeError):  # pragma: no cover
        return None


def strip_fences(s: str) -> str:
    """Strip markdown fences from model output (matches orchestrator-CLI line 161-168)."""
    s = s.strip()
    if s.startswith("```"):
        first_nl = s.find("\n")
        s = s[first_nl + 1:] if first_nl > 0 else s[3:]
        if s.endswith("```"):
            s = s[:-3]
    return s.strip()


def extract_json_from_content(content: str) -> dict | None:
    """Extract a JSON object from the model's text content.

    Uses raw_decode to allow trailing prose. Returns ``None`` on parse failure.
    """
    if not content:
        return None
    t = strip_fences(content)
    start = t.find("{")
    if start < 0:
        return None
    try:
        decoder = json.JSONDecoder()
        obj, _ = decoder.raw_decode(t[start:])
        return obj if isinstance(obj, dict) else None
    except (ValueError, json.JSONDecodeError):
        return None


# ---------------------------------------------------------------------------
# Production HTTP wiring
# ---------------------------------------------------------------------------
#
# Per §4 v2.x.5 LOCKED 2026-05-16 row 232 (CC-007 closure):
#
#   - ``_ProductionHTTPCaller`` class — DELETED.
#   - ``make_production_http_caller()`` function — DELETED.
#
# Production wire-up at ``pipeline/seats/red_team/seat.py:269`` now binds:
#
#     http_post = enforce_outbound_boundary(
#         stdlib_urlopen_caller,
#         classification_context=ClassificationContext.from_envelope_json(
#             envelope.classification_context_json
#         ),
#         posture=envelope.posture,
#         operator_signed_register=load_signed_register(),
#     )
#
# and ``call_groq`` is invoked with ``http_post=http_post`` (OutboundCallable
# shape — bytes body + bytes response). The sole permitted urllib call site
# in ``pipeline/`` is ``provider_boundary.stdlib_urlopen_caller``.


def read_groq_api_key_from_env() -> str:  # pragma: no cover
    """Read Groq API key from BYOK env vars (per §1 keys.py discipline).

    Operator MUST hold this key (BYOK). Read at seat-subprocess time, not
    at module-load (V1 cache-leakage discipline).
    """
    return os.environ.get("GROQ_API_KEY", "")


__all__ = [
    "F_RT_PROVIDER_TRANSPORT_FAIL",
    "F_RT_PROVIDER_AUTH_FAIL",
    "F_RT_PROVIDER_RATE_LIMITED",
    "F_RT_PROVIDER_PARSE_FAIL",
    "GROQ_DEFAULT_BASE_URL",
    "GROQ_DEFAULT_MODEL",
    "GROQ_DEFAULT_TIMEOUT_SEC",
    "GROQ_DEFAULT_MAX_TOKENS",
    "OutboundCallable",
    "GroqProviderResult",
    "call_groq",
    "extract_message_content",
    "extract_json_from_content",
    "strip_fences",
    "read_groq_api_key_from_env",
]
