"""pipeline.seats.scribe.provider_anthropic — seat-local BYOK Anthropic binding.

Spec card: ``pipeline/engineering/spec_cards/section_07_scribe_round_3_seat_entry_and_wiring.md``
OQ-1 resolution: seat-local for v0.1.0 (no ``pipeline/providers/`` package yet);
refactor to ``pipeline.providers.anthropic`` deferred to v0.1.1.

Disciplines applied:

- E-017 injected-seam: ``AnthropicCallCallable`` Protocol + ``HttpPostCallable``
  Protocol + ``ClockFn`` + ``SleepFn``. Production wires stdlib ``urllib.request``
  + ``time.time`` + ``time.sleep``; tests inject deterministic stubs.
- V1 inline-literal rebind-resistance: transport cap ``120.0`` seconds,
  single-shot retry, ``30`` second health-check, ``max_tokens=64000`` all
  pinned at dispatch. Module-level constants exist for reading, never
  consulted at runtime.
- E-027 payload-size pre-check: ``prompt_token_estimate =
  len(compiled_prompt) / 3.7``; logged to SFR-hook; does NOT fail-closed
  at the binding layer (§F.1 exempt decision is POST-gate concern).
- E-028 transport-retry: single retry on connection-level failures only
  (``urllib.error.URLError``, 5xx, ``TimeoutError``); semantic 4xx with
  structured body never retries.
- A-v1-02 trust model: provider-reported ``model`` field in the response
  is captured as ``landed_model_id``; the binding does NOT second-guess.
"""

from __future__ import annotations

import hashlib
import json
import time
import urllib.error  # Exception classes only — call site moved to provider_boundary.
from dataclasses import dataclass
from typing import Any, Callable, Final, Mapping, Protocol

from pipeline.orchestrator.provider_boundary import (
    OutboundCallable as _OutboundCallable,
)

# -- Constants (human-readable; NOT consulted at runtime; V1 discipline). --
TRANSPORT_CAP_SECONDS: Final[float] = 120.0
TRANSPORT_RETRY_HEALTH_CHECK_SECONDS: Final[float] = 30.0
DEFAULT_MAX_TOKENS: Final[int] = 64000
ANTHROPIC_MESSAGES_URL: Final[str] = "https://api.anthropic.com/v1/messages"
ANTHROPIC_API_VERSION: Final[str] = "2023-06-01"
TOKEN_ESTIMATE_CHARS_PER_TOKEN: Final[float] = 3.7

# -- Failure-code strings. --
F_SCRIBE_BYOK_MISSING: Final[str] = "F-SCRIBE-BYOK-MISSING"
F_SCRIBE_TRANSPORT_FAILURE: Final[str] = "F-SCRIBE-TRANSPORT-FAILURE"
F_SCRIBE_SEMANTIC_FAILURE: Final[str] = "F-SCRIBE-SEMANTIC-FAILURE"
F_SCRIBE_PAYLOAD_CEILING: Final[str] = "F-SCRIBE-PAYLOAD-CEILING"
F_SCRIBE_PROVIDER_MALFORMED: Final[str] = "F-SCRIBE-PROVIDER-MALFORMED"


# -- Exceptions. --


class AnthropicBYOKMissing(RuntimeError):
    """BYOK key absent from keystore. F-SCRIBE-BYOK-MISSING."""


class AnthropicTransportFailure(RuntimeError):
    """Network-class failure after single-shot retry. F-SCRIBE-TRANSPORT-FAILURE."""


class AnthropicSemanticFailure(RuntimeError):
    """4xx response with structured body; never retried. F-SCRIBE-SEMANTIC-FAILURE."""


class AnthropicPayloadCeiling(RuntimeError):
    """Estimated prompt tokens exceed ceiling. F-SCRIBE-PAYLOAD-CEILING."""


class AnthropicProviderMalformed(RuntimeError):
    """Provider returned non-JSON or missing required fields. F-SCRIBE-PROVIDER-MALFORMED."""


# -- E-017 Protocols. --


class ClockFn(Protocol):
    def __call__(self) -> float: ...


class SleepFn(Protocol):
    def __call__(self, seconds: float, /) -> None: ...


#: HttpPostCallable Protocol — preserved as a public name for backward
#: compatibility with test fixtures that inject stubs via the same name.
#: Per §4 v2.x.5 LOCKED 2026-05-16 row 232, this is now an alias of the
#: unified ``OutboundCallable`` Protocol exported by
#: ``pipeline.orchestrator.provider_boundary``. Production wire-up at
#: ``pipeline/seats/scribe/seat.py`` binds
#: ``enforce_outbound_boundary(stdlib_urlopen_caller, ...)`` and passes the
#: wrapped callable into ``call_anthropic_scribe``; the seat-local
#: ``stdlib_http_post`` urllib call site has been DELETED per OD-1 + §4.1.
HttpPostCallable = _OutboundCallable


class KeyRetrieveCallable(Protocol):
    """Retrieve BYOK Anthropic key for given org slug. Returns bytes (not SecretBytes)."""

    def __call__(self, *, org_slug: str, key_id: str) -> bytes: ...


class AnthropicCallCallable(Protocol):
    """Full Scribe-Anthropic call seam. seat.py injects this."""

    def __call__(
        self,
        *,
        binding: "AnthropicBinding",
        compiled_prompt: str,
        org_slug: str,
    ) -> "AnthropicResponse": ...


# -- Shapes. --


@dataclass(frozen=True, kw_only=True, slots=True)
class AnthropicBinding:
    """Router-yaml-derived Scribe binding. Frozen; constructed by load_scribe_binding.

    NOTE: ``max_tokens`` is carried for telemetry; runtime call inlines the
    literal ``64000`` (V1 rebind-resistance).
    """

    primary_model_id: str
    escalation_model_id: str
    max_tokens: int = DEFAULT_MAX_TOKENS
    prompt_token_ceiling: int = 180_000  # Anthropic context window floor

    def __post_init__(self) -> None:
        if not self.primary_model_id:
            raise ValueError("primary_model_id must be non-empty")
        if not self.escalation_model_id:
            raise ValueError("escalation_model_id must be non-empty")
        if self.max_tokens <= 0:
            raise ValueError("max_tokens must be positive")
        if self.prompt_token_ceiling <= 0:
            raise ValueError("prompt_token_ceiling must be positive")


@dataclass(frozen=True, kw_only=True, slots=True)
class AnthropicResponse:
    """Captured Anthropic response. landed_model_id is provider-reported (A-v1-02)."""

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
                f"response_sha3_512 must be 128-hex chars; got {len(self.response_sha3_512)}"
            )
        if self.response_sha3_512 != self.response_sha3_512.lower():
            raise ValueError("response_sha3_512 must be lowercase hex")


# -- Token estimate (E-027 discipline at binding layer). --


def estimate_prompt_tokens(compiled_prompt: str) -> int:
    """Len / 3.7 rounded down. Inline literal at dispatch; module constant for reading."""
    return int(len(compiled_prompt) / 3.7)


# -- Production HTTP POST. --
#
# Per §4 v2.x.5 LOCKED 2026-05-16 row 232 (CC-007 closure), the seat-local
# ``stdlib_http_post`` function has been DELETED. The sole permitted
# ``urllib.request.urlopen`` call site in ``pipeline/`` is now
# ``pipeline.orchestrator.provider_boundary.stdlib_urlopen_caller``, wrapped
# by ``enforce_outbound_boundary(...)`` at seat subprocess wire-up. Tests
# that previously parametrized over ``stdlib_http_post`` continue to work by
# injecting stub ``HttpPostCallable`` implementations directly.


# -- Call orchestration with E-028 single-shot transport retry. --


def call_anthropic_scribe(
    *,
    binding: AnthropicBinding,
    compiled_prompt: str,
    org_slug: str,
    key_retrieve: KeyRetrieveCallable,
    http_post: HttpPostCallable,
    clock: ClockFn,
    sleep: SleepFn,
) -> AnthropicResponse:
    """Single Scribe-Anthropic call with transport retry discipline.

    Raises:
        AnthropicBYOKMissing: key_retrieve returned b"" or raised.
        AnthropicPayloadCeiling: estimated tokens > binding.prompt_token_ceiling.
        AnthropicTransportFailure: two consecutive connection-class failures.
        AnthropicSemanticFailure: 4xx with structured body.
        AnthropicProviderMalformed: non-JSON 2xx or missing required fields.
    """
    # Payload-size pre-check (E-027).
    prompt_token_estimate = estimate_prompt_tokens(compiled_prompt)
    if prompt_token_estimate > binding.prompt_token_ceiling:
        raise AnthropicPayloadCeiling(
            f"{F_SCRIBE_PAYLOAD_CEILING}: estimated {prompt_token_estimate} tokens "
            f"exceeds ceiling {binding.prompt_token_ceiling}"
        )

    # BYOK load.
    try:
        key_bytes = key_retrieve(org_slug=org_slug, key_id="anthropic")
    except Exception as exc:
        # Sanitization (Scribe R3 narrow-fix 2026-04-29): class name only;
        # the underlying keystore exception may carry filesystem paths /
        # keystore identifiers that would leak via stderr.
        raise AnthropicBYOKMissing(
            f"{F_SCRIBE_BYOK_MISSING}: keystore retrieve failed for org={org_slug}; "
            f"exception_class={type(exc).__name__}"
        ) from exc
    if not key_bytes:
        raise AnthropicBYOKMissing(
            f"{F_SCRIBE_BYOK_MISSING}: empty key returned for org={org_slug}"
        )
    try:
        api_key = key_bytes.decode("ascii")
    except UnicodeDecodeError as exc:
        raise AnthropicBYOKMissing(
            f"{F_SCRIBE_BYOK_MISSING}: key is not ASCII-decodable for org={org_slug}"
        ) from exc

    # Build request body.
    payload = {
        "model": binding.primary_model_id,
        "max_tokens": 64000,  # inline literal; V1 rebind-resistance
        "messages": [{"role": "user", "content": compiled_prompt}],
    }
    body_bytes = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )
    headers = {
        "content-type": "application/json",
        "anthropic-version": "2023-06-01",  # inline literal
        "x-api-key": api_key,
    }

    # E-028 transport retry: one retry on connection-class failure, 120s cap total.
    t_start = clock()
    attempts = 0
    last_transport_exc: BaseException | None = None
    while attempts < 2:
        attempts += 1
        elapsed = clock() - t_start
        remaining = 120.0 - elapsed  # inline literal cap
        if remaining <= 0:
            raise AnthropicTransportFailure(
                f"{F_SCRIBE_TRANSPORT_FAILURE}: 120s wall-clock cap exceeded before "
                f"attempt {attempts}"
            )
        try:
            status, resp_bytes = http_post(
                url=ANTHROPIC_MESSAGES_URL,
                headers=headers,
                body=body_bytes,
                timeout_seconds=min(remaining, 90.0),
            )
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_transport_exc = exc
            if attempts >= 2:
                break
            sleep(30.0)  # inline literal health-check
            continue

        # Semantic 4xx never retries (E-028).
        if 400 <= status < 500:
            # Sanitization (Scribe R3 committee narrow-fix 2026-04-29):
            # surface only the response body's SHA-3-256 prefix + length, not
            # the raw bytes — defense-in-depth against accidental egress of
            # any echoed prompt/account-id from the provider error envelope
            # via the seat's structured-stderr line that crosses the
            # subprocess boundary.
            body_digest = hashlib.sha3_256(resp_bytes).hexdigest()[:16]
            raise AnthropicSemanticFailure(
                f"{F_SCRIBE_SEMANTIC_FAILURE}: HTTP {status}; "
                f"body_sha3_256_prefix16={body_digest}; "
                f"body_len_bytes={len(resp_bytes)}"
            )
        # 5xx retryable once.
        if status >= 500:
            last_transport_exc = RuntimeError(f"HTTP {status}")
            if attempts >= 2:
                break
            sleep(30.0)
            continue

        # 2xx path.
        return _parse_anthropic_2xx_response(
            resp_bytes=resp_bytes,
            prompt_token_estimate=prompt_token_estimate,
        )

    # Sanitization (Scribe R3 committee narrow-fix 2026-04-29): surface only
    # the exception class name, not its repr — defense-in-depth against
    # urllib.error embedded URL / response-body strings leaking via stderr.
    last_class = (
        type(last_transport_exc).__name__ if last_transport_exc is not None else "unknown"
    )
    raise AnthropicTransportFailure(
        f"{F_SCRIBE_TRANSPORT_FAILURE}: two consecutive transport-class failures; "
        f"last_exception_class={last_class}"
    )


def _parse_anthropic_2xx_response(
    *, resp_bytes: bytes, prompt_token_estimate: int
) -> AnthropicResponse:
    try:
        parsed = json.loads(resp_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        # Sanitization (Scribe R3 narrow-fix 2026-04-29): class name only;
        # JSONDecodeError messages can carry response-body snippets.
        body_digest = hashlib.sha3_256(resp_bytes).hexdigest()[:16]
        raise AnthropicProviderMalformed(
            f"{F_SCRIBE_PROVIDER_MALFORMED}: non-JSON 2xx body; "
            f"exception_class={type(exc).__name__}; "
            f"body_sha3_256_prefix16={body_digest}; "
            f"body_len_bytes={len(resp_bytes)}"
        ) from exc
    if not isinstance(parsed, dict):
        raise AnthropicProviderMalformed(
            f"{F_SCRIBE_PROVIDER_MALFORMED}: top-level is not object"
        )
    landed_model_id = parsed.get("model")
    if not isinstance(landed_model_id, str) or not landed_model_id:
        raise AnthropicProviderMalformed(
            f"{F_SCRIBE_PROVIDER_MALFORMED}: missing 'model' field"
        )
    content = parsed.get("content")
    if not isinstance(content, list) or not content:
        raise AnthropicProviderMalformed(
            f"{F_SCRIBE_PROVIDER_MALFORMED}: missing or empty 'content' array"
        )
    # Concatenate all text blocks (Anthropic returns list of content blocks).
    text_parts: list[str] = []
    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") == "text":
            text = block.get("text")
            if isinstance(text, str):
                text_parts.append(text)
    text_body = "".join(text_parts)
    if not text_body:
        raise AnthropicProviderMalformed(
            f"{F_SCRIBE_PROVIDER_MALFORMED}: no text content in response"
        )
    canonical_json_bytes = json.dumps(
        parsed, separators=(",", ":"), ensure_ascii=False, sort_keys=True
    ).encode("utf-8")
    response_sha3_512 = hashlib.sha3_512(canonical_json_bytes).hexdigest()
    return AnthropicResponse(
        landed_model_id=landed_model_id,
        text_body=text_body,
        prompt_token_estimate=prompt_token_estimate,
        response_sha3_512=response_sha3_512,
        raw_response_canonical_json_bytes=canonical_json_bytes,
    )


# -- Binding loader from router.yaml. --


def load_scribe_binding_from_router_mapping(
    router_mapping: Mapping[str, Any],
) -> AnthropicBinding:
    """Parse router.yaml-shaped mapping → AnthropicBinding.

    Expects the shape under key path ``tilth.scribe.{primary,escalation}``.
    Stays close to router.yaml actual structure.
    """
    tilth = router_mapping.get("tilth")
    if not isinstance(tilth, Mapping):
        raise ValueError("router mapping missing 'tilth' section")
    scribe = tilth.get("scribe")
    if not isinstance(scribe, Mapping):
        raise ValueError("router mapping missing 'tilth.scribe' section")
    primary = scribe.get("primary")
    escalation = scribe.get("escalation")
    if not isinstance(primary, str) or not primary.startswith("anthropic/"):
        raise ValueError(
            f"tilth.scribe.primary must be anthropic/* binding; got {primary!r}"
        )
    if not isinstance(escalation, str) or not escalation.startswith("anthropic/"):
        raise ValueError(
            f"tilth.scribe.escalation must be anthropic/* binding; got {escalation!r}"
        )
    return AnthropicBinding(
        primary_model_id=primary.split("/", 1)[1],
        escalation_model_id=escalation.split("/", 1)[1],
    )


__all__ = [
    # Shapes
    "AnthropicBinding",
    "AnthropicResponse",
    # Callables / Protocols (E-017)
    "ClockFn",
    "SleepFn",
    "HttpPostCallable",
    "KeyRetrieveCallable",
    "AnthropicCallCallable",
    # Entry points
    "call_anthropic_scribe",
    "load_scribe_binding_from_router_mapping",
    "estimate_prompt_tokens",
    # Exceptions
    "AnthropicBYOKMissing",
    "AnthropicTransportFailure",
    "AnthropicSemanticFailure",
    "AnthropicPayloadCeiling",
    "AnthropicProviderMalformed",
    # Failure-code constants
    "F_SCRIBE_BYOK_MISSING",
    "F_SCRIBE_TRANSPORT_FAILURE",
    "F_SCRIBE_SEMANTIC_FAILURE",
    "F_SCRIBE_PAYLOAD_CEILING",
    "F_SCRIBE_PROVIDER_MALFORMED",
]
