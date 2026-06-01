"""pipeline.orchestrator.provider_boundary — F-CLASS-* outbound boundary wrapper.

Companion code for §4 v2.x.5 amendment (LOCKED 2026-05-16 row 232).

Closes CC-007 — seat-local provider HTTP egress sovereignty bypass — by
wrapping every cloud-routable HTTP POST with the existing F-CLASS-* PRE/POST
predicate chain. The wrapper is wired at each seat's subprocess wire-up so
that ``stdlib_http_post`` / ``_ProductionHTTPCaller`` paths are deleted from
seat-local provider modules and replaced with the wrapped callable.

Public surface
--------------

- :data:`ClassificationContext` — frozen per-call classification proof; mirrors
  the router's local ``ClassificationContext`` shape so seat subprocesses can
  construct it from envelope JSON without importing ``pipeline.orchestrator.router``.
- :class:`OutboundCallable` — unified Protocol (bytes body + ``tuple[int, bytes]``
  return) covering both the Anthropic/Google ``HttpPostCallable`` shape and the
  Groq ``HTTPCaller.post_json`` shape (OD-3 unification).
- :class:`OutboundBoundaryRefusedError` — typed exception raised on PRE or POST
  refusal (mirrors ``router.ClassificationBoundaryError`` shape per OD-2).
- :func:`enforce_outbound_boundary` — wrapper factory; composes PRE→inner→POST.
- :func:`stdlib_urlopen_caller` — sole permitted ``urllib.request.urlopen`` call
  site in ``pipeline/`` (R-NO-DIRECT-PROVIDER-HTTP allowlist anchor).
- Module-level constants: the three sub-tag failure-code strings + additional
  sub-tags introduced by Cycle 1/2 fold-ins (RT-01/04/05/07/14/18 + Cycle 2
  DC/RT-C2 closures).

Cycle 1 + Cycle 2 fold-ins
--------------------------

Per amendment §11.1 / §12.4 / §12.5 the wrapper includes runtime guards
beyond the bare PRE/POST predicate composition:

- **PRE-2a (RT-01)** — runtime identity pin: ``inner is _CANONICAL_STDLIB_URLOPEN_CALLER``.
- **PRE-2b (RT-07)** — posture cross-check against the operator-signed register.
- **PRE-2c (RT-05)** — sha3-512 payload commitment match.
- **PRE-2d (RT-04)** — raw-bytes scan against signed-register classified values.
- **POST (RT-18 / §12.5)** — process-wide atomic invocation counter + thread-local
  ``_INSIDE_WRAPPER`` flag to detect direct calls of ``stdlib_urlopen_caller``
  outside the wrapper.
- **DC-CYCLE2-02** — ``stdlib_urlopen_caller`` refuses non-https URL schemes.

Threat model bounding
---------------------

Bounded under v7 LOCKED A1 (single-client) + A4 (operator-trusted preflight
envelope). Multi-tenant promotion lands at Stage-5 Sovereign Node commons.
Dynamic-import / monkey-patch evasion shapes are bounded per amendment §3.4 +
§12.4; the runtime identity pin + Cedar second layer close most paths.

This module IS the AST-lint allowlist anchor for ``urllib.request.urlopen``;
any other call to that primitive inside ``pipeline/`` is a
``R-NO-DIRECT-PROVIDER-HTTP.urlopen`` violation.
"""

from __future__ import annotations

import hashlib
import json
import threading
import unicodedata
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Final, Literal, Mapping, Protocol, runtime_checkable

# Compose the existing F-CLASS-* predicate chain. These imports are required
# for the wrapper to delegate to the canonical gate functions rather than
# redefining them.
from pipeline.logician.gates.f_class_outbound_boundary import (
    ClassifiedValue,
    SlotPosition,
    check_class_cloud_received_confidential,
    check_class_cloud_received_opaque_slot_filled,
    check_class_high_stakes_flag_leak,
    check_class_slot_id_non_opaque,
)
from pipeline.logician.gates.f_class_routing_indeterminate import (
    CallInput,
    check_class_routing_indeterminate,
)

# ---------------------------------------------------------------------------
# Sub-tag failure-code strings (OD-1: sub-tag extensions on existing F-CLASS-*
# top-level primitives; the family roster stays at sixteen — no new top-level
# row).
# ---------------------------------------------------------------------------

#: PRE refusal — wrapper invoked with classification_context=None under a
#: posture that would otherwise have permitted egress. Structural; no M13.
F_CLASS_OUTBOUND_BOUNDARY_MISSING_CONTEXT: Final[str] = (
    "F-CLASS-ROUTING-INDETERMINATE.outbound_boundary_missing_context"
)

#: PRE refusal — Local-Only posture / confidential input / split-context
#: allow-list miss / non-https URL scheme. M13_AUDITED_HIGH.
F_CLASS_OUTBOUND_BOUNDARY_CLASSIFICATION_DENY: Final[str] = (
    "F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.outbound_boundary_classification_deny"
)

#: POST refusal — response bytes contain a tagged Confidential literal /
#: opaque-slot pattern / high-stakes-token. Response bytes discarded.
F_CLASS_OUTBOUND_BOUNDARY_POST_DRIFT: Final[str] = (
    "F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.outbound_boundary_post_drift"
)

# -- Cycle 1 RT-fold-in sub-tags (still on existing top-level rows). --

#: RT-01 — runtime identity pin: ``inner is not _CANONICAL_STDLIB_URLOPEN_CALLER``.
F_CLASS_OUTBOUND_BOUNDARY_RUNTIME_INTEGRITY_FAIL: Final[str] = (
    "F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.outbound_boundary_runtime_integrity_fail"
)

#: RT-05 — body sha3-512 mismatches the envelope's payload_sha3_512_commitment.
F_CLASS_OUTBOUND_BOUNDARY_PAYLOAD_COMMITMENT_MISMATCH: Final[str] = (
    "F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.outbound_boundary_payload_commitment_mismatch"
)

#: RT-07 — envelope posture differs from operator-signed register posture.
F_CLASS_OUTBOUND_BOUNDARY_POSTURE_MISMATCH: Final[str] = (
    "F-CLASS-POSTURE-MID-CYCLE-CHANGE.outbound_boundary_posture_mismatch"
)

#: RT-18 — wrapper never invoked under a cloud-routable posture.
F_CLASS_OUTBOUND_BOUNDARY_NEVER_INVOKED: Final[str] = (
    "F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.outbound_boundary_never_invoked"
)

#: §12.5 RT-C2-03 — ``stdlib_urlopen_caller`` invoked outside the wrapper.
F_CLASS_OUTBOUND_BOUNDARY_NEVER_INVOKED_DIRECT_CALL: Final[str] = (
    "F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.outbound_boundary_never_invoked.direct_call"
)

#: §12.6 RT-C2-04 — Cedar policy failed to load at startup; second-layer
#: defense unavailable; fail-closed.
F_CLASS_OUTBOUND_BOUNDARY_CEDAR_LOAD_FAILURE: Final[str] = (
    "F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.cedar_load_failure"
)

#: §12.3 RT-C2-01 — signed-register file invalid / sig verification failed.
F_CLASS_REGISTER_SIGNATURE_INVALID_SIGNED_FILE_INVALID: Final[str] = (
    "F-CLASS-REGISTER-SIGNATURE-INVALID.signed_file_invalid"
)


# ---------------------------------------------------------------------------
# Posture literal — exact closed set per architecture v7.0.10 (the three
# canonical postures; the Sanitized / opaque-slot posture is deprecated).
# ---------------------------------------------------------------------------

Posture = Literal["frontier_eligible", "split_context_hybrid", "local_only_sovereign"]

_VALID_POSTURES: Final[frozenset[str]] = frozenset(
    {"frontier_eligible", "split_context_hybrid", "local_only_sovereign"}
)


# ---------------------------------------------------------------------------
# ClassificationContext mirror (lives here so seat subprocesses don't import
# pipeline.orchestrator.router, which has yaml + filesystem side-effects).
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class ClassificationContext:
    """Per-call proof that cloud routing is allowed for the exact payload.

    Mirrors the router's local shape one-for-one; the extra ``cycle_id`` and
    ``payload_sha3_512_commitment`` fields are Cycle-1 RT-05 fold-ins for
    cross-cycle replay defense.
    """

    inputs: tuple[CallInput, ...]
    classified_values: tuple[ClassifiedValue, ...] = field(default_factory=tuple)
    slot_positions: tuple[SlotPosition, ...] = field(default_factory=tuple)
    high_stakes_flag_values: tuple[str, ...] = field(default_factory=tuple)
    post_fill_draft: bool = False

    # RT-05 fold-in — cross-cycle replay defense.
    cycle_id: str = ""
    payload_sha3_512_commitment: str = ""

    @classmethod
    def from_envelope_json(cls, json_str: str) -> "ClassificationContext":
        """Decode envelope-encoded JSON into a frozen ClassificationContext.

        Raises ValueError on malformed JSON or missing required keys. Under
        Local-Only / Sovereign posture the orchestrator MUST still emit a
        syntactically-valid JSON (empty ``inputs`` array is acceptable —
        wrapper refuses unconditionally on Local-Only posture).
        """
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as exc:
            raise ValueError(f"classification_context_json malformed: {exc}") from exc
        if not isinstance(data, dict):
            raise ValueError("classification_context_json must decode to a JSON object")

        inputs_raw = data.get("inputs", [])
        if not isinstance(inputs_raw, list):
            raise ValueError("classification_context_json.inputs must be a list")
        inputs: tuple[CallInput, ...] = tuple(
            CallInput(
                field_path=str(item["field_path"]),
                class_name=str(item["class_name"]),
                locked_by=str(item.get("locked_by", "operator")),
            )
            for item in inputs_raw
            if isinstance(item, dict) and "field_path" in item and "class_name" in item
        )

        classified_raw = data.get("classified_values", [])
        classified: tuple[ClassifiedValue, ...] = tuple(
            ClassifiedValue(
                value=str(item["value"]),
                class_name=str(item["class_name"]),
                field_path=str(item.get("field_path", "")),
            )
            for item in classified_raw
            if isinstance(item, dict) and "value" in item and "class_name" in item
        )

        slot_raw = data.get("slot_positions", [])
        slots: tuple[SlotPosition, ...] = tuple(
            SlotPosition(
                slot_id=str(item["slot_id"]),
                pre_marker=str(item.get("pre_marker", "")),
                post_marker=str(item.get("post_marker", "")),
            )
            for item in slot_raw
            if isinstance(item, dict) and "slot_id" in item
        )

        flags_raw = data.get("high_stakes_flag_values", [])
        flags: tuple[str, ...] = tuple(str(x) for x in flags_raw)

        return cls(
            inputs=inputs,
            classified_values=classified,
            slot_positions=slots,
            high_stakes_flag_values=flags,
            post_fill_draft=bool(data.get("post_fill_draft", False)),
            cycle_id=str(data.get("cycle_id", "")),
            payload_sha3_512_commitment=str(data.get("payload_sha3_512_commitment", "")),
        )


# ---------------------------------------------------------------------------
# OutboundCallable Protocol — unifies Anthropic/Google HttpPostCallable
# (bytes body) and Groq HTTPCaller.post_json (dict body) per OD-3.
# Groq's call_groq body encodes dict → bytes once before invocation.
# ---------------------------------------------------------------------------


@runtime_checkable
class OutboundCallable(Protocol):
    """Unified production HTTP POST seam (OD-3).

    Body is bytes; return is ``(status, response_bytes)``. The caller
    (provider module) encodes dict→bytes once before invocation. The wrapper
    composes PRE-gates → ``inner`` → POST-gates while preserving this shape.
    """

    def __call__(
        self,
        *,
        url: str,
        headers: Mapping[str, str],
        body: bytes,
        timeout_seconds: float,
    ) -> tuple[int, bytes]: ...


# ---------------------------------------------------------------------------
# Typed refusal exception (mirrors router.ClassificationBoundaryError per OD-2).
# Callers that already catch ClassificationBoundaryError can catch this with
# the same handler.
# ---------------------------------------------------------------------------


class OutboundBoundaryRefusedError(RuntimeError):
    """PRE-gate refused egress OR POST-gate detected drift.

    Carries:
      - ``failure_code`` — the F-CLASS-* sub-tag string (one of the module constants).
      - ``detail`` — human-readable explanation (NO Confidential content per Law 3).
    """

    def __init__(self, failure_code: str, detail: str) -> None:
        self.failure_code = failure_code
        self.detail = detail
        super().__init__(f"{failure_code}: {detail}")


# ---------------------------------------------------------------------------
# Process-wide invocation counter (RT-18 + §12.5 RT-C2-03 fold-in).
# Replaces an earlier thread-local design; ``threading.Lock``-guarded int
# counter at module scope. Incremented inside the wrapper on successful
# POST-gate clearance.
# ---------------------------------------------------------------------------

_INVOCATION_COUNTER_LOCK: threading.Lock = threading.Lock()
_PROCESS_OUTBOUND_BOUNDARY_INVOCATION_COUNT_ATOMIC: int = 0

#: Thread-local flag set by the wrapper before calling ``inner``; read by
#: ``stdlib_urlopen_caller`` to detect direct invocations outside the wrapper.
_INSIDE_WRAPPER: threading.local = threading.local()


def _get_invocation_count() -> int:
    """Read the process-wide invocation count atomically."""
    with _INVOCATION_COUNTER_LOCK:
        return _PROCESS_OUTBOUND_BOUNDARY_INVOCATION_COUNT_ATOMIC


def _increment_invocation_count() -> None:
    """Increment the process-wide invocation count atomically."""
    global _PROCESS_OUTBOUND_BOUNDARY_INVOCATION_COUNT_ATOMIC
    with _INVOCATION_COUNTER_LOCK:
        _PROCESS_OUTBOUND_BOUNDARY_INVOCATION_COUNT_ATOMIC += 1


def reset_invocation_count_for_tests() -> None:
    """Test-only helper to reset the counter between cases."""
    global _PROCESS_OUTBOUND_BOUNDARY_INVOCATION_COUNT_ATOMIC
    with _INVOCATION_COUNTER_LOCK:
        _PROCESS_OUTBOUND_BOUNDARY_INVOCATION_COUNT_ATOMIC = 0


# ---------------------------------------------------------------------------
# The canonical urllib call site. Sole permitted ``urllib.request.urlopen``
# invocation in ``pipeline/`` (R-NO-DIRECT-PROVIDER-HTTP allowlist anchor).
# ---------------------------------------------------------------------------


def stdlib_urlopen_caller(
    *,
    url: str,
    headers: Mapping[str, str],
    body: bytes,
    timeout_seconds: float,
) -> tuple[int, bytes]:
    """Sole permitted urllib.request.urlopen call site in pipeline/.

    Production seats wire ``enforce_outbound_boundary(stdlib_urlopen_caller,
    ...)`` at subprocess wire-up; the wrapped callable runs the F-CLASS
    PRE/POST gates around the urllib egress.

    DC-CYCLE2-02 fold-in: refuses non-https URL schemes structurally. This is
    defense-in-depth against (a) misconfigured router.yaml endpoints,
    (b) header-injection attacks that mutate the URL field, (c) future
    provider adapters that fail to enforce https.

    §12.5 RT-C2-03 fold-in: refuses direct invocation outside the wrapper
    via the ``_INSIDE_WRAPPER`` thread-local flag.
    """
    # §12.5 RT-C2-03: detect direct calls outside the wrapper.
    if not getattr(_INSIDE_WRAPPER, "active", False):
        raise OutboundBoundaryRefusedError(
            F_CLASS_OUTBOUND_BOUNDARY_NEVER_INVOKED_DIRECT_CALL,
            "stdlib_urlopen_caller invoked outside enforce_outbound_boundary wrapper; "
            "direct calls are forbidden under v7.0.10 §1.3",
        )

    # DC-CYCLE2-02: structural https-only.
    if not url.startswith("https://"):
        raise OutboundBoundaryRefusedError(
            F_CLASS_OUTBOUND_BOUNDARY_CLASSIFICATION_DENY,
            f"stdlib_urlopen_caller refused non-https scheme: {url[:64]!r}",
        )

    req = urllib.request.Request(
        url, data=body, headers=dict(headers), method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_seconds) as resp:  # noqa: S310
            return int(resp.status), resp.read()
    except urllib.error.HTTPError as exc:
        return int(exc.code), exc.read() or b""


# Capture the canonical identity at module load. The wrapper compares
# ``inner is _CANONICAL_STDLIB_URLOPEN_CALLER`` (RT-01 + §12.4 fold-in);
# monkey-patching the public symbol does NOT mutate this captured identity.
_CANONICAL_STDLIB_URLOPEN_CALLER: Final[OutboundCallable] = stdlib_urlopen_caller


# ---------------------------------------------------------------------------
# PRE / POST helper composition. The wrapper delegates to these instead of
# inlining the predicate chain.
# ---------------------------------------------------------------------------


def _scan_payload_text_for_classified(
    body_text: str, classified_values: tuple[ClassifiedValue, ...]
) -> ClassifiedValue | None:
    """Substring-match scan of payload text against classified literals.

    NFC-normalises both sides before comparison; v0.2 hardening will replace
    this with a token-aware scan (RT-10/11 deferred dispositions). Returns
    the first hit (if any) for diagnostic; raises nothing.
    """
    haystack = unicodedata.normalize("NFC", body_text)
    for cv in classified_values:
        if cv.class_name in {"confidential", "operator_flagged"}:
            needle = unicodedata.normalize("NFC", cv.value)
            if needle and needle in haystack:
                return cv
    return None


def _scan_payload_text_for_flags(body_text: str, flags: tuple[str, ...]) -> str | None:
    """Substring-match scan for high-stakes flag literals."""
    for flag in flags:
        if flag and flag in body_text:
            return flag
    return None


def _enforce_pre(
    *,
    classification_context: ClassificationContext,
    posture: Posture,
    body: bytes,
    operator_signed_register: Mapping[str, Any] | None,
) -> None:
    """PRE-gate predicate chain. Raises OutboundBoundaryRefusedError on refusal.

    Order of checks mirrors router._enforce_cloud_boundary_pre:
    1. check_class_routing_indeterminate (input class enum legality)
    2. blocking-class scan on inputs (confidential / operator_flagged)
    3. check_class_slot_id_non_opaque (defense-in-depth)
    4. check_class_cloud_received_confidential (payload literal scan)
    5. check_class_high_stakes_flag_leak
    6. (split_context_hybrid only) allow-list + leak scan deferred to v0.2
    7. RT-04 raw-bytes scan against signed register's classified_values
    """
    # PRE-3.1 — routing indeterminate (illegal class_name) when inputs are
    # provided. Empty-inputs is acceptable under Local-Only style stubs where
    # the wrapper's earlier Local-Only refusal already short-circuits.
    if classification_context.inputs:
        routing_result = check_class_routing_indeterminate(
            inputs=list(classification_context.inputs)
        )
        if not routing_result.success:
            raise OutboundBoundaryRefusedError(
                "F-CLASS-ROUTING-INDETERMINATE",
                routing_result.detail,
            )

    # PRE-3.2 — blocking-class scan on inputs.
    for inp in classification_context.inputs:
        if inp.class_name in {"confidential", "operator_flagged"}:
            raise OutboundBoundaryRefusedError(
                F_CLASS_OUTBOUND_BOUNDARY_CLASSIFICATION_DENY,
                f"input class={inp.class_name} forbids cloud egress "
                f"(field_path={inp.field_path})",
            )

    # PRE-3.3 — opaque slot id defense-in-depth on the body bytes.
    body_text = body.decode("utf-8", errors="replace")
    slot_result = check_class_slot_id_non_opaque(cloud_routed_prompt=body_text)
    if not slot_result.success:
        raise OutboundBoundaryRefusedError(
            "F-CLASS-SLOT-ID-NON-OPAQUE",
            slot_result.detail,
        )

    # PRE-3.4 — classified-value scan on the body bytes.
    confidential_result = check_class_cloud_received_confidential(
        cloud_routed_payload=body_text,
        classified_values=list(classification_context.classified_values),
    )
    if not confidential_result.success:
        raise OutboundBoundaryRefusedError(
            "F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL",
            confidential_result.detail,
        )

    # PRE-3.5 — high-stakes flag leak on the body bytes.
    flag_result = check_class_high_stakes_flag_leak(
        cloud_routed_payload=body_text,
        high_stakes_flag_values=list(classification_context.high_stakes_flag_values),
    )
    if not flag_result.success:
        raise OutboundBoundaryRefusedError(
            "F-CLASS-HIGH-STAKES-FLAG-LEAK",
            flag_result.detail,
        )

    # PRE-2d (RT-04 fold-in) — raw-bytes scan against operator-signed register's
    # classified values. Source of truth = signed register, NOT envelope (which
    # the wrapper treats as untrusted). When operator_signed_register is None
    # (test or no-register deployment) this layer is skipped under v7 A1+A4.
    if operator_signed_register is not None:
        register_classified = _extract_register_classified_values(
            operator_signed_register
        )
        hit = _scan_payload_text_for_classified(body_text, register_classified)
        if hit is not None:
            raise OutboundBoundaryRefusedError(
                F_CLASS_OUTBOUND_BOUNDARY_CLASSIFICATION_DENY,
                f"operator-signed-register classified literal in payload "
                f"(field_path={hit.field_path}, class_name={hit.class_name})",
            )


def _enforce_post(
    *,
    classification_context: ClassificationContext,
    response_bytes: bytes,
) -> None:
    """POST-gate predicate chain. Raises OutboundBoundaryRefusedError on drift."""
    response_text = response_bytes.decode("utf-8", errors="replace")

    # POST-1 — confidential literal in response.
    confidential_result = check_class_cloud_received_confidential(
        cloud_routed_payload=response_text,
        classified_values=list(classification_context.classified_values),
    )
    if not confidential_result.success:
        raise OutboundBoundaryRefusedError(
            F_CLASS_OUTBOUND_BOUNDARY_POST_DRIFT,
            confidential_result.detail,
        )

    # POST-2 — opaque-slot pattern in response (defense-in-depth; v7.0.10 §2.2
    # — the opaque-slot mechanism is deprecated; firing here is bug-class).
    slot_filled_result = check_class_cloud_received_opaque_slot_filled(
        cloud_routed_payload=response_text,
        slot_positions=list(classification_context.slot_positions),
    )
    if not slot_filled_result.success:
        raise OutboundBoundaryRefusedError(
            "F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED",
            slot_filled_result.detail,
        )

    # POST-3 — high-stakes literal in response.
    flag_result = check_class_high_stakes_flag_leak(
        cloud_routed_payload=response_text,
        high_stakes_flag_values=list(classification_context.high_stakes_flag_values),
    )
    if not flag_result.success:
        raise OutboundBoundaryRefusedError(
            "F-CLASS-HIGH-STAKES-FLAG-LEAK",
            flag_result.detail,
        )


def _extract_register_classified_values(
    register: Mapping[str, Any],
) -> tuple[ClassifiedValue, ...]:
    """Pull ClassifiedValue tuples out of the signed register's payload shape.

    The signed register is a dict shaped per ``signed_register_loader``:
        {"register": {"entries": [{"field_path": ..., "value": ...,
                                   "class_name": ...}, ...]},
         "signature": {...}}
    """
    entries = []
    payload = register.get("register", {})
    raw_entries = payload.get("entries", [])
    for item in raw_entries:
        if not isinstance(item, dict):
            continue
        class_name = str(item.get("class_name", ""))
        if class_name not in {"confidential", "operator_flagged"}:
            continue
        entries.append(
            ClassifiedValue(
                value=str(item.get("value", "")),
                class_name=class_name,
                field_path=str(item.get("field_path", "")),
            )
        )
    return tuple(entries)


# ---------------------------------------------------------------------------
# enforce_outbound_boundary — the wrapper factory.
# ---------------------------------------------------------------------------


def enforce_outbound_boundary(
    inner: OutboundCallable,
    *,
    classification_context: ClassificationContext | None,
    posture: Posture,
    operator_signed_register: Mapping[str, Any] | None = None,
    register_posture: Posture | None = None,
) -> OutboundCallable:
    """Wrap an HTTP POST callable with F-CLASS PRE/POST outbound-boundary gates.

    Behavior:
      1. PRE-1: if posture == "local_only_sovereign", refuse unconditionally
         (cloud egress structurally absent under Local-Only; firing = bug-class).
      2. PRE-2: if classification_context is None, refuse with
         F-CLASS-ROUTING-INDETERMINATE.outbound_boundary_missing_context.
      3. PRE-2a (RT-01): identity pin — refuse if
         ``inner is not _CANONICAL_STDLIB_URLOPEN_CALLER`` AND
         operator_signed_register is not None (production binding). Tests pass
         operator_signed_register=None to skip identity-pin for stub callers.
      4. PRE-2b (RT-07): refuse if envelope posture differs from
         operator-signed register posture.
      5. PRE-2c (RT-05): if classification_context.payload_sha3_512_commitment is
         non-empty, verify sha3-512(body) matches.
      6. PRE-3..N (composed): existing F-CLASS predicate chain.
      7. INVOKE: call ``inner(url=..., headers=..., body=..., timeout_seconds=...)``.
      8. POST: classified-value / slot-filled / high-stakes-flag scan on response.
      9. PRE refusal → raise OutboundBoundaryRefusedError (no urllib call).
     10. POST refusal → raise OutboundBoundaryRefusedError with the post-drift
         sub-tag (response bytes discarded).

    Returns a NEW OutboundCallable preserving the inner's Protocol shape.
    """
    if posture not in _VALID_POSTURES:
        raise OutboundBoundaryRefusedError(
            "F-CLASS-ROUTING-INDETERMINATE",
            f"unrecognized posture: {posture!r}",
        )

    def wrapped(
        *,
        url: str,
        headers: Mapping[str, str],
        body: bytes,
        timeout_seconds: float,
    ) -> tuple[int, bytes]:
        # PRE-1: Local-Only posture refuses cloud egress structurally.
        if posture == "local_only_sovereign":
            raise OutboundBoundaryRefusedError(
                F_CLASS_OUTBOUND_BOUNDARY_CLASSIFICATION_DENY,
                "outbound HTTP attempted under Local-Only / Sovereign posture; "
                "cloud egress is structurally absent",
            )

        # PRE-2: missing classification context.
        if classification_context is None:
            raise OutboundBoundaryRefusedError(
                F_CLASS_OUTBOUND_BOUNDARY_MISSING_CONTEXT,
                "outbound HTTP attempted without classification_context; "
                "fail-closed per v7.0.10 §1.3",
            )

        # PRE-2a (RT-01 + §12.4): runtime identity pin. Enforced only when
        # operator_signed_register is provided (production binding); test
        # fixtures with operator_signed_register=None skip this layer so they
        # can inject stub callers.
        if operator_signed_register is not None:
            if inner is not _CANONICAL_STDLIB_URLOPEN_CALLER:
                raise OutboundBoundaryRefusedError(
                    F_CLASS_OUTBOUND_BOUNDARY_RUNTIME_INTEGRITY_FAIL,
                    "inner callable is not the canonical stdlib_urlopen_caller; "
                    "monkey-patch or wrapper-bypass detected",
                )

        # PRE-2b (RT-07): posture cross-check against signed register.
        if register_posture is not None and posture != register_posture:
            raise OutboundBoundaryRefusedError(
                F_CLASS_OUTBOUND_BOUNDARY_POSTURE_MISMATCH,
                f"envelope posture={posture!r} != register posture="
                f"{register_posture!r}; posture forgery detected",
            )

        # PRE-2c (RT-05): payload sha3-512 commitment match.
        commitment = classification_context.payload_sha3_512_commitment
        if commitment:
            actual = hashlib.sha3_512(body).hexdigest()
            if actual != commitment.lower():
                raise OutboundBoundaryRefusedError(
                    F_CLASS_OUTBOUND_BOUNDARY_PAYLOAD_COMMITMENT_MISMATCH,
                    "body sha3-512 differs from payload_sha3_512_commitment; "
                    "cross-cycle replay attempt detected",
                )

        # PRE-3..N: existing F-CLASS predicate chain composition.
        _enforce_pre(
            classification_context=classification_context,
            posture=posture,
            body=body,
            operator_signed_register=operator_signed_register,
        )

        # INVOKE with thread-local _INSIDE_WRAPPER flag set so direct calls
        # to stdlib_urlopen_caller from worker threads are caught.
        _INSIDE_WRAPPER.active = True
        try:
            status, response_bytes = inner(
                url=url,
                headers=headers,
                body=body,
                timeout_seconds=timeout_seconds,
            )
        finally:
            _INSIDE_WRAPPER.active = False

        # POST: classified-value / slot-filled / high-stakes-flag scan.
        _enforce_post(
            classification_context=classification_context,
            response_bytes=response_bytes,
        )

        # RT-18 + §12.5: increment process-wide invocation counter on success.
        _increment_invocation_count()

        return status, response_bytes

    return wrapped


__all__ = [
    # Sub-tag failure-code strings.
    "F_CLASS_OUTBOUND_BOUNDARY_MISSING_CONTEXT",
    "F_CLASS_OUTBOUND_BOUNDARY_CLASSIFICATION_DENY",
    "F_CLASS_OUTBOUND_BOUNDARY_POST_DRIFT",
    "F_CLASS_OUTBOUND_BOUNDARY_RUNTIME_INTEGRITY_FAIL",
    "F_CLASS_OUTBOUND_BOUNDARY_PAYLOAD_COMMITMENT_MISMATCH",
    "F_CLASS_OUTBOUND_BOUNDARY_POSTURE_MISMATCH",
    "F_CLASS_OUTBOUND_BOUNDARY_NEVER_INVOKED",
    "F_CLASS_OUTBOUND_BOUNDARY_NEVER_INVOKED_DIRECT_CALL",
    "F_CLASS_OUTBOUND_BOUNDARY_CEDAR_LOAD_FAILURE",
    "F_CLASS_REGISTER_SIGNATURE_INVALID_SIGNED_FILE_INVALID",
    # Types.
    "Posture",
    "ClassificationContext",
    "OutboundCallable",
    "OutboundBoundaryRefusedError",
    # Wrapper + canonical caller.
    "enforce_outbound_boundary",
    "stdlib_urlopen_caller",
    # Test helpers + introspection.
    "reset_invocation_count_for_tests",
]
