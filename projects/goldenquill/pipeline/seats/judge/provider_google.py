"""pipeline.seats.judge.provider_google — seat-local BYOK Google Gemini binding.

Spec card: ``pipeline/engineering/spec_cards/section_09_judge_round_3_seat_entry_and_sfr.md``
Mirrors the seat-local pattern Scribe R3 used for ``provider_anthropic.py``;
refactor to ``pipeline.providers.google`` deferred to v0.1.1.

Disciplines applied:

- E-017 injected-seam: ``GoogleCallCallable`` Protocol + ``HttpPostCallable``
  Protocol + ``ClockFn`` + ``SleepFn``. Production wires stdlib
  ``urllib.request`` + ``time.time`` + ``time.sleep``; tests inject
  deterministic stubs.
- V1 inline-literal rebind-resistance: transport cap ``120.0`` seconds,
  single-shot retry, ``30`` second health-check, ``max_output_tokens=8192``
  all inlined at dispatch. Module-level constants exist for reading,
  never consulted at runtime.
- E-027 payload-size pre-check: ``prompt_token_estimate =
  len(compiled_prompt) / 3.7``; raises :class:`GooglePayloadCeiling` when
  over the binding's ceiling.
- E-028 transport-retry: single retry on connection-class failures only
  (``urllib.error.URLError``, 5xx, ``TimeoutError``, ``OSError``); semantic
  4xx never retries.
- A-v1-02 trust model: provider-reported ``modelVersion`` field in the
  response is captured as ``landed_model_id``; the binding does NOT
  second-guess.
- Cross-family enforcement (F_PIPE_08 defense-in-depth): the binding
  loader refuses to construct a :class:`GoogleBinding` whose primary
  is not a ``google/`` row in ``router.yaml``. The seat itself rejects
  envelopes whose Scribe-landed family is ``google`` via a separate
  PRE-gate check.
"""

from __future__ import annotations

import hashlib
import json
import urllib.error  # Exception classes only — call site moved to provider_boundary.
from dataclasses import dataclass
from typing import Any, Final, Mapping, Protocol

from pipeline.orchestrator.provider_boundary import (
    OutboundCallable as _OutboundCallable,
)


# -- Constants (human-readable; NOT consulted at runtime; V1 discipline). --
TRANSPORT_CAP_SECONDS: Final[float] = 120.0
TRANSPORT_RETRY_HEALTH_CHECK_SECONDS: Final[float] = 30.0
DEFAULT_MAX_OUTPUT_TOKENS: Final[int] = 8192
GOOGLE_GENERATE_CONTENT_URL_TEMPLATE: Final[str] = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
)
TOKEN_ESTIMATE_CHARS_PER_TOKEN: Final[float] = 3.7

# -- Failure-code strings. --
F_JUDGE_BYOK_MISSING: Final[str] = "F-JUDGE-BYOK-MISSING"
F_JUDGE_TRANSPORT_FAILURE: Final[str] = "F-JUDGE-TRANSPORT-FAILURE"
F_JUDGE_SEMANTIC_FAILURE: Final[str] = "F-JUDGE-SEMANTIC-FAILURE"
F_JUDGE_PAYLOAD_CEILING: Final[str] = "F-JUDGE-PAYLOAD-CEILING"
F_JUDGE_PROVIDER_MALFORMED: Final[str] = "F-JUDGE-PROVIDER-MALFORMED"


# -- Exceptions. --


class GoogleBYOKMissing(RuntimeError):
    """BYOK key absent from keystore. F-JUDGE-BYOK-MISSING."""


class GoogleTransportFailure(RuntimeError):
    """Network-class failure after single-shot retry. F-JUDGE-TRANSPORT-FAILURE."""


class GoogleSemanticFailure(RuntimeError):
    """4xx response with structured body; never retried. F-JUDGE-SEMANTIC-FAILURE."""


class GooglePayloadCeiling(RuntimeError):
    """Estimated prompt tokens exceed ceiling. F-JUDGE-PAYLOAD-CEILING."""


class GoogleProviderMalformed(RuntimeError):
    """Provider returned non-JSON or missing required fields. F-JUDGE-PROVIDER-MALFORMED."""


# -- E-017 Protocols. --


class ClockFn(Protocol):
    def __call__(self) -> float: ...


class SleepFn(Protocol):
    def __call__(self, seconds: float, /) -> None: ...


#: Per §4 v2.x.5 LOCKED 2026-05-16 row 232 (CC-007 closure), HttpPostCallable
#: is now an alias of the unified ``OutboundCallable`` Protocol exported by
#: ``pipeline.orchestrator.provider_boundary``. Production wire-up at
#: ``pipeline/seats/judge/seat.py`` binds
#: ``enforce_outbound_boundary(stdlib_urlopen_caller, ...)`` and passes the
#: wrapped callable into ``call_google_judge``. The seat-local
#: ``stdlib_http_post`` urllib call site has been DELETED per OD-1 + §4.2.
HttpPostCallable = _OutboundCallable


class KeyRetrieveCallable(Protocol):
    """Retrieve BYOK Google key for given org slug. Returns bytes."""

    def __call__(self, *, org_slug: str, key_id: str) -> bytes: ...


class GoogleCallCallable(Protocol):
    """Full Judge-Google call seam. seat.py injects this."""

    def __call__(
        self,
        *,
        binding: "GoogleBinding",
        compiled_prompt: str,
        org_slug: str,
    ) -> "GoogleResponse": ...


# -- Shapes. --


@dataclass(frozen=True, kw_only=True, slots=True)
class GoogleBinding:
    """Router-yaml-derived Judge binding. Frozen; constructed by
    :func:`load_judge_binding_from_router_mapping`.

    NOTE: ``max_output_tokens`` is carried for telemetry; runtime call
    inlines the literal ``8192`` (V1 rebind-resistance).
    """

    primary_model_id: str
    fallback_model_id: str
    max_output_tokens: int = DEFAULT_MAX_OUTPUT_TOKENS
    prompt_token_ceiling: int = 1_000_000  # Gemini 2.5 Pro context window

    def __post_init__(self) -> None:
        if not self.primary_model_id:
            raise ValueError("primary_model_id must be non-empty")
        if not self.fallback_model_id:
            raise ValueError("fallback_model_id must be non-empty")
        if self.max_output_tokens <= 0:
            raise ValueError("max_output_tokens must be positive")
        if self.prompt_token_ceiling <= 0:
            raise ValueError("prompt_token_ceiling must be positive")


@dataclass(frozen=True, kw_only=True, slots=True)
class GoogleResponse:
    """Captured Google response. landed_model_id is provider-reported (A-v1-02)."""

    landed_model_id: str
    text_body: str
    prompt_token_estimate: int
    response_sha3_512: str
    raw_response_canonical_json_bytes: bytes

    def __post_init__(self) -> None:
        if not self.landed_model_id:
            raise ValueError("landed_model_id must be non-empty")
        if len(self.response_sha3_512) != 128:
            raise ValueError(
                f"response_sha3_512 must be 128-hex chars; got "
                f"{len(self.response_sha3_512)}"
            )
        if self.response_sha3_512 != self.response_sha3_512.lower():
            raise ValueError("response_sha3_512 must be lowercase hex")


# -- Token estimate (E-027 discipline at binding layer). --


def estimate_prompt_tokens(compiled_prompt: str) -> int:
    """Len / 3.7 rounded down. Inline literal at dispatch; module constant for reading."""
    return int(len(compiled_prompt) / 3.7)


# -- Production HTTP POST. Stdlib only. --


# Per §4 v2.x.5 LOCKED 2026-05-16 row 232 (CC-007 closure), the seat-local
# ``stdlib_http_post`` function has been DELETED. The sole permitted
# ``urllib.request.urlopen`` call site in ``pipeline/`` is now
# ``pipeline.orchestrator.provider_boundary.stdlib_urlopen_caller``, wrapped
# by ``enforce_outbound_boundary(...)`` at seat subprocess wire-up.


# -- Call orchestration with E-028 single-shot transport retry. --


def call_google_judge(
    *,
    binding: GoogleBinding,
    compiled_prompt: str,
    org_slug: str,
    key_retrieve: KeyRetrieveCallable,
    http_post: HttpPostCallable,
    clock: ClockFn,
    sleep: SleepFn,
) -> GoogleResponse:
    """Single Judge-Google call with transport retry discipline.

    Raises:
        GoogleBYOKMissing: key_retrieve returned b"" or raised.
        GooglePayloadCeiling: estimated tokens > binding.prompt_token_ceiling.
        GoogleTransportFailure: two consecutive connection-class failures.
        GoogleSemanticFailure: 4xx with structured body.
        GoogleProviderMalformed: non-JSON 2xx or missing required fields.
    """
    prompt_token_estimate = estimate_prompt_tokens(compiled_prompt)
    if prompt_token_estimate > binding.prompt_token_ceiling:
        raise GooglePayloadCeiling(
            f"{F_JUDGE_PAYLOAD_CEILING}: estimated {prompt_token_estimate} tokens "
            f"exceeds ceiling {binding.prompt_token_ceiling}"
        )

    try:
        key_bytes = key_retrieve(org_slug=org_slug, key_id="google")
    except Exception as exc:
        raise GoogleBYOKMissing(
            f"{F_JUDGE_BYOK_MISSING}: keystore retrieve failed for org={org_slug}; "
            f"exception_class={type(exc).__name__}"
        ) from exc
    if not key_bytes:
        raise GoogleBYOKMissing(
            f"{F_JUDGE_BYOK_MISSING}: empty key returned for org={org_slug}"
        )
    try:
        api_key = key_bytes.decode("ascii")
    except UnicodeDecodeError as exc:
        raise GoogleBYOKMissing(
            f"{F_JUDGE_BYOK_MISSING}: key is not ASCII-decodable for org={org_slug}"
        ) from exc

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{binding.primary_model_id}:generateContent"
    )
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": compiled_prompt}],
            }
        ],
        "generationConfig": {
            "maxOutputTokens": 8192,
            "temperature": 0.0,
        },
    }
    body_bytes = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )
    headers = {
        "content-type": "application/json",
        "x-goog-api-key": api_key,
    }

    t_start = clock()
    attempts = 0
    last_transport_exc: BaseException | None = None
    while attempts < 2:
        attempts += 1
        elapsed = clock() - t_start
        remaining = 120.0 - elapsed
        if remaining <= 0:
            raise GoogleTransportFailure(
                f"{F_JUDGE_TRANSPORT_FAILURE}: 120s wall-clock cap exceeded before "
                f"attempt {attempts}"
            )
        try:
            status, resp_bytes = http_post(
                url=url,
                headers=headers,
                body=body_bytes,
                timeout_seconds=min(remaining, 90.0),
            )
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_transport_exc = exc
            if attempts >= 2:
                break
            sleep(30.0)
            continue

        if 400 <= status < 500:
            body_digest = hashlib.sha3_256(resp_bytes).hexdigest()[:16]
            raise GoogleSemanticFailure(
                f"{F_JUDGE_SEMANTIC_FAILURE}: HTTP {status}; "
                f"body_sha3_256_prefix16={body_digest}; "
                f"body_len_bytes={len(resp_bytes)}"
            )
        if status >= 500:
            last_transport_exc = RuntimeError(f"HTTP {status}")
            if attempts >= 2:
                break
            sleep(30.0)
            continue

        return _parse_google_2xx_response(
            resp_bytes=resp_bytes,
            prompt_token_estimate=prompt_token_estimate,
            primary_model_id=binding.primary_model_id,
        )

    last_class = (
        type(last_transport_exc).__name__ if last_transport_exc is not None else "unknown"
    )
    raise GoogleTransportFailure(
        f"{F_JUDGE_TRANSPORT_FAILURE}: two consecutive transport-class failures; "
        f"last_exception_class={last_class}"
    )


def _parse_google_2xx_response(
    *, resp_bytes: bytes, prompt_token_estimate: int, primary_model_id: str
) -> GoogleResponse:
    try:
        parsed = json.loads(resp_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        body_digest = hashlib.sha3_256(resp_bytes).hexdigest()[:16]
        raise GoogleProviderMalformed(
            f"{F_JUDGE_PROVIDER_MALFORMED}: non-JSON 2xx body; "
            f"exception_class={type(exc).__name__}; "
            f"body_sha3_256_prefix16={body_digest}; "
            f"body_len_bytes={len(resp_bytes)}"
        ) from exc
    if not isinstance(parsed, dict):
        raise GoogleProviderMalformed(
            f"{F_JUDGE_PROVIDER_MALFORMED}: top-level is not object"
        )
    candidates = parsed.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        raise GoogleProviderMalformed(
            f"{F_JUDGE_PROVIDER_MALFORMED}: missing or empty 'candidates' array"
        )
    first = candidates[0]
    if not isinstance(first, dict):
        raise GoogleProviderMalformed(
            f"{F_JUDGE_PROVIDER_MALFORMED}: candidates[0] is not object"
        )
    content = first.get("content")
    if not isinstance(content, dict):
        raise GoogleProviderMalformed(
            f"{F_JUDGE_PROVIDER_MALFORMED}: missing or non-object 'content'"
        )
    parts = content.get("parts")
    if not isinstance(parts, list) or not parts:
        raise GoogleProviderMalformed(
            f"{F_JUDGE_PROVIDER_MALFORMED}: missing or empty 'parts' array"
        )
    text_parts: list[str] = []
    for part in parts:
        if not isinstance(part, dict):
            continue
        text = part.get("text")
        if isinstance(text, str):
            text_parts.append(text)
    text_body = "".join(text_parts)
    if not text_body:
        raise GoogleProviderMalformed(
            f"{F_JUDGE_PROVIDER_MALFORMED}: no text content in response"
        )
    # Provider-reported model identifier. Gemini API typically returns
    # ``modelVersion`` at the top level (e.g., "gemini-2.5-pro-002").
    # Fall back to the request's primary_model_id when absent — A-v1-02
    # trust model: the binding does not invent values, but the seat needs
    # a non-empty landed_model_id to construct GoogleResponse.
    landed_model_id = parsed.get("modelVersion")
    if not isinstance(landed_model_id, str) or not landed_model_id:
        landed_model_id = primary_model_id
    canonical_json_bytes = json.dumps(
        parsed, separators=(",", ":"), ensure_ascii=False, sort_keys=True
    ).encode("utf-8")
    response_sha3_512 = hashlib.sha3_512(canonical_json_bytes).hexdigest()
    return GoogleResponse(
        landed_model_id=landed_model_id,
        text_body=text_body,
        prompt_token_estimate=prompt_token_estimate,
        response_sha3_512=response_sha3_512,
        raw_response_canonical_json_bytes=canonical_json_bytes,
    )


# -- Binding loader from router.yaml. --


def load_judge_binding_from_router_mapping(
    router_mapping: Mapping[str, Any],
) -> GoogleBinding:
    """Parse router.yaml-shaped mapping → :class:`GoogleBinding`.

    Expects the shape under key path ``tilth.judge.{primary,fallback}``.
    Refuses to construct a binding whose primary is not a ``google/*``
    row — F_PIPE_08 cross-family defense-in-depth at load time.
    """
    tilth = router_mapping.get("tilth")
    if not isinstance(tilth, Mapping):
        raise ValueError("router mapping missing 'tilth' section")
    judge = tilth.get("judge")
    if not isinstance(judge, Mapping):
        raise ValueError("router mapping missing 'tilth.judge' section")
    primary = judge.get("primary")
    fallback = judge.get("fallback")
    if not isinstance(primary, str) or not primary.startswith("google/"):
        raise ValueError(
            f"tilth.judge.primary must be google/* binding (cross-family "
            f"discipline); got {primary!r}"
        )
    if not isinstance(fallback, str) or not fallback:
        raise ValueError(
            f"tilth.judge.fallback must be non-empty string; got {fallback!r}"
        )
    fallback_id = fallback.split("/", 1)[1] if "/" in fallback else fallback
    return GoogleBinding(
        primary_model_id=primary.split("/", 1)[1],
        fallback_model_id=fallback_id,
    )


__all__ = [
    # Shapes
    "GoogleBinding",
    "GoogleResponse",
    # Callables / Protocols (E-017)
    "ClockFn",
    "SleepFn",
    "HttpPostCallable",
    "KeyRetrieveCallable",
    "GoogleCallCallable",
    # Entry points
    "call_google_judge",
    "load_judge_binding_from_router_mapping",
    "estimate_prompt_tokens",
    # Exceptions
    "GoogleBYOKMissing",
    "GoogleTransportFailure",
    "GoogleSemanticFailure",
    "GooglePayloadCeiling",
    "GoogleProviderMalformed",
    # Failure-code constants
    "F_JUDGE_BYOK_MISSING",
    "F_JUDGE_TRANSPORT_FAILURE",
    "F_JUDGE_SEMANTIC_FAILURE",
    "F_JUDGE_PAYLOAD_CEILING",
    "F_JUDGE_PROVIDER_MALFORMED",
]
