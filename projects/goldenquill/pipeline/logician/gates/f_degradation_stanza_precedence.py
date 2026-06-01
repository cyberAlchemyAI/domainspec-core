"""F-DEGRADATION-STANZA-PRECEDENCE (F-AMDT-11) — two-tooth PRE-gate.

EN-003 Cycle 4 Red Team finding C4-NEW-03 has two teeth:

**Tooth (a) — stanza precedence.** Operator sign-off stanzas written in
response to F-AMDT-08 (Committee-Degradation-Timeout) SUSPEND / ESCALATE
tiers may carry a ``TARGET_DATE`` directive, a ``FRESH_ARCHITECTURAL_THESIS``
directive, both, or neither. Text-level closure left "both" and "neither"
ambiguous. This gate resolves the ambiguity mechanically:

  - only ``FRESH_ARCHITECTURAL_THESIS`` → PASS (ESCALATE-tier resolution).
  - only ``TARGET_DATE`` → PASS (SUSPEND-tier resolution).
  - both → PASS with ``F-AMDT-11-PRECEDENCE-MIXED`` event; the stronger
    directive (FRESH_ARCHITECTURAL_THESIS) wins; TARGET_DATE is ignored.
  - neither → FAIL ``F-AMDT-11-PRECEDENCE-EMPTY`` (malformed stanza).

**Tooth (b) — READ-ONLY deadlock carve-out.** F-AMDT-08 ESCALATE tier
requires a fresh architectural Thesis to exit READ-ONLY, but sealing a
fresh Thesis is itself a LOCK operation. Code-LOCKs remain blocked under
READ-ONLY; architectural-Thesis LOCKs carve out a narrow bypass:

  - ``lock_class: "architectural_thesis"``,
  - target path matches the architecture-file regex, and
  - row bytes carry a valid operator Ed25519 signature.

All three must hold to grant a carve-out
(``F-AMDT-11-CARVEOUT-GRANTED`` emitted). Any one missing → FAIL
``F-AMDT-11-DEADLOCK-CARVEOUT-VIOLATION``. Code LOCKs under SUSPEND /
ESCALATE tiers are denied carve-out (expected — they remain subject to
READ-ONLY per F-AMDT-08).

The precedence enumeration and the architecture-path regex are
**inline literals**, not module constants. Rebind-resistance tests
verify the gate's behaviour does not change under module-namespace
mutation.

Blueprint anchor: ``pipeline/blueprint/v0.1/section_04_logician.md`` v2.1
(parent LOCK); v2.2 wave-3 delta rows for F-AMDT-11.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Final, Optional

from pipeline.logician.gates._protocols import (
    SignatureVerifyCallable,
    StanzaReaderCallable,
)


F_AMDT_11: Final[str] = "F-AMDT-11"
F_AMDT_11_PRECEDENCE_EMPTY: Final[str] = "F-AMDT-11-PRECEDENCE-EMPTY"
F_AMDT_11_DEADLOCK_CARVEOUT_VIOLATION: Final[str] = "F-AMDT-11-DEADLOCK-CARVEOUT-VIOLATION"
F_AMDT_11_READER_FAIL: Final[str] = "F-AMDT-11-READER-FAIL"

EVENT_PRECEDENCE_MIXED: Final[str] = "F-AMDT-11-PRECEDENCE-MIXED"
EVENT_CARVEOUT_GRANTED: Final[str] = "F-AMDT-11-CARVEOUT-GRANTED"

EVENT_KIND_STANZA: Final[str] = "stanza_check"
EVENT_KIND_PROMOTION: Final[str] = "lock_promotion_under_readonly"

_TIER_PASS: Final[str] = "pass"
_TIER_WARN: Final[str] = "warn"
_TIER_SUSPEND: Final[str] = "suspend"
_TIER_ESCALATE: Final[str] = "escalate"
_VALID_TIERS: Final[frozenset] = frozenset({_TIER_PASS, _TIER_WARN, _TIER_SUSPEND, _TIER_ESCALATE})

_LOCK_CLASS_ARCHITECTURAL: Final[str] = "architectural_thesis"


_REASON_INVALID_EVENT_KIND: Final[str] = "invalid_event_kind"
_REASON_INVALID_TODAY_ISO: Final[str] = "invalid_today_iso"
_REASON_INVALID_TIER: Final[str] = "invalid_tier"
_REASON_STAGED_ROW_NOT_DICT: Final[str] = "staged_row_not_dict"
_REASON_PUBLIC_KEY_NOT_BYTES: Final[str] = "public_key_not_bytes"
_REASON_STANZA_READER_RAISED: Final[str] = "stanza_reader_raised"
_REASON_STANZA_READER_NOT_STR_OR_NONE: Final[str] = "stanza_reader_return_invalid"
_REASON_STANZA_ABSENT_OK: Final[str] = "stanza_absent_no_op"
_REASON_STANZA_FRESH_ONLY: Final[str] = "stanza_fresh_architectural_thesis"
_REASON_STANZA_TARGET_ONLY: Final[str] = "stanza_target_date_only"
_REASON_STANZA_BOTH_FRESH_WINS: Final[str] = "stanza_both_fresh_wins"
_REASON_STANZA_EMPTY: Final[str] = "stanza_neither_directive_present"
_REASON_TIER_NOT_SUSPEND_OR_ESCALATE: Final[str] = "tier_not_suspend_or_escalate_no_op"
_REASON_LOCK_CLASS_NOT_ARCHITECTURAL: Final[str] = "lock_class_not_architectural_thesis"
_REASON_MODULE_PATH_NOT_STR: Final[str] = "module_path_not_str"
_REASON_MODULE_PATH_NOT_ARCHITECTURE: Final[str] = "module_path_not_architecture_file"
_REASON_SIGNED_ROW_BYTES_NOT_BYTES: Final[str] = "signed_row_bytes_not_bytes"
_REASON_OPERATOR_SIGNATURE_NOT_BYTES: Final[str] = "operator_signature_not_bytes"
_REASON_SIGNATURE_VERIFY_RAISED: Final[str] = "signature_verify_raised"
_REASON_SIGNATURE_INVALID: Final[str] = "signature_verify_returned_false"
_REASON_CARVEOUT_GRANTED_OK: Final[str] = "carveout_granted"


@dataclass(frozen=True, kw_only=True)
class StanzaPrecedenceDetail:
    """Structured result detail for both event kinds."""

    reason_tag: str
    event_kind: str
    emitted_event: str
    has_fresh: bool
    has_target: bool
    lock_class: str
    module_path: str
    reader_error: Optional[str]


@dataclass(frozen=True, kw_only=True)
class StanzaPrecedenceResult:
    success: bool
    failure_code: Optional[str]
    detail: StanzaPrecedenceDetail


def _clip_error(exc: BaseException) -> str:
    return f"{type(exc).__name__}: {exc}"[:500]


def _fail(
    *,
    failure_code: str,
    reason_tag: str,
    event_kind: str,
    has_fresh: bool = False,
    has_target: bool = False,
    lock_class: str = "",
    module_path: str = "",
    reader_error: Optional[str] = None,
) -> StanzaPrecedenceResult:
    return StanzaPrecedenceResult(
        success=False,
        failure_code=failure_code,
        detail=StanzaPrecedenceDetail(
            reason_tag=reason_tag,
            event_kind=event_kind,
            emitted_event="",
            has_fresh=has_fresh,
            has_target=has_target,
            lock_class=lock_class,
            module_path=module_path,
            reader_error=reader_error,
        ),
    )


def _ok(
    *,
    reason_tag: str,
    event_kind: str,
    emitted_event: str = "",
    has_fresh: bool = False,
    has_target: bool = False,
    lock_class: str = "",
    module_path: str = "",
) -> StanzaPrecedenceResult:
    return StanzaPrecedenceResult(
        success=True,
        failure_code=None,
        detail=StanzaPrecedenceDetail(
            reason_tag=reason_tag,
            event_kind=event_kind,
            emitted_event=emitted_event,
            has_fresh=has_fresh,
            has_target=has_target,
            lock_class=lock_class,
            module_path=module_path,
            reader_error=None,
        ),
    )


def check_degradation_stanza_precedence(
    *,
    event_kind: str,
    today_iso: str,
    f_amdt_08_tier: str,
    stanza_reader: StanzaReaderCallable,
    signature_verify: SignatureVerifyCallable,
    operator_public_key: bytes,
    staged_row: Optional[dict] = None,
) -> StanzaPrecedenceResult:
    """PRE-gate F-DEGRADATION-STANZA-PRECEDENCE (F-AMDT-11)."""

    if event_kind not in (EVENT_KIND_STANZA, EVENT_KIND_PROMOTION):
        return _fail(
            failure_code=F_AMDT_11_READER_FAIL,
            reason_tag=_REASON_INVALID_EVENT_KIND,
            event_kind=str(event_kind) if isinstance(event_kind, str) else "",
        )

    if not isinstance(today_iso, str) or today_iso == "":
        return _fail(
            failure_code=F_AMDT_11_READER_FAIL,
            reason_tag=_REASON_INVALID_TODAY_ISO,
            event_kind=event_kind,
        )

    if not isinstance(f_amdt_08_tier, str) or f_amdt_08_tier not in _VALID_TIERS:
        return _fail(
            failure_code=F_AMDT_11_READER_FAIL,
            reason_tag=_REASON_INVALID_TIER,
            event_kind=event_kind,
        )

    if not isinstance(operator_public_key, bytes):
        return _fail(
            failure_code=F_AMDT_11_READER_FAIL,
            reason_tag=_REASON_PUBLIC_KEY_NOT_BYTES,
            event_kind=event_kind,
        )

    if event_kind == EVENT_KIND_STANZA:
        return _check_stanza(
            today_iso=today_iso,
            stanza_reader=stanza_reader,
        )

    # event_kind == EVENT_KIND_PROMOTION
    return _check_promotion(
        tier=f_amdt_08_tier,
        staged_row=staged_row,
        signature_verify=signature_verify,
        operator_public_key=operator_public_key,
    )


def _check_stanza(
    *,
    today_iso: str,
    stanza_reader: StanzaReaderCallable,
) -> StanzaPrecedenceResult:
    try:
        stanza = stanza_reader(today_iso)
    except Exception as exc:
        return _fail(
            failure_code=F_AMDT_11_READER_FAIL,
            reason_tag=_REASON_STANZA_READER_RAISED,
            event_kind=EVENT_KIND_STANZA,
            reader_error=f"stanza_reader: {_clip_error(exc)}",
        )

    if stanza is None:
        return _ok(
            reason_tag=_REASON_STANZA_ABSENT_OK,
            event_kind=EVENT_KIND_STANZA,
        )

    if not isinstance(stanza, str):
        return _fail(
            failure_code=F_AMDT_11_READER_FAIL,
            reason_tag=_REASON_STANZA_READER_NOT_STR_OR_NONE,
            event_kind=EVENT_KIND_STANZA,
        )

    has_fresh = "FRESH_ARCHITECTURAL_THESIS" in stanza
    has_target = "TARGET_DATE:" in stanza

    # Inline-literal precedence enumeration — FRESH_ARCHITECTURAL_THESIS > TARGET_DATE.
    if has_fresh and has_target:
        return _ok(
            reason_tag=_REASON_STANZA_BOTH_FRESH_WINS,
            event_kind=EVENT_KIND_STANZA,
            emitted_event=EVENT_PRECEDENCE_MIXED,
            has_fresh=True,
            has_target=True,
        )
    if has_fresh:
        return _ok(
            reason_tag=_REASON_STANZA_FRESH_ONLY,
            event_kind=EVENT_KIND_STANZA,
            has_fresh=True,
        )
    if has_target:
        return _ok(
            reason_tag=_REASON_STANZA_TARGET_ONLY,
            event_kind=EVENT_KIND_STANZA,
            has_target=True,
        )
    return _fail(
        failure_code=F_AMDT_11_PRECEDENCE_EMPTY,
        reason_tag=_REASON_STANZA_EMPTY,
        event_kind=EVENT_KIND_STANZA,
    )


def _check_promotion(
    *,
    tier: str,
    staged_row: Optional[dict],
    signature_verify: SignatureVerifyCallable,
    operator_public_key: bytes,
) -> StanzaPrecedenceResult:
    if tier not in (_TIER_SUSPEND, _TIER_ESCALATE):
        return _ok(
            reason_tag=_REASON_TIER_NOT_SUSPEND_OR_ESCALATE,
            event_kind=EVENT_KIND_PROMOTION,
        )

    if not isinstance(staged_row, dict):
        return _fail(
            failure_code=F_AMDT_11_READER_FAIL,
            reason_tag=_REASON_STAGED_ROW_NOT_DICT,
            event_kind=EVENT_KIND_PROMOTION,
        )

    raw_class = staged_row.get("lock_class", "")
    lock_class = raw_class if isinstance(raw_class, str) else ""

    if lock_class != _LOCK_CLASS_ARCHITECTURAL:
        return _fail(
            failure_code=F_AMDT_11_DEADLOCK_CARVEOUT_VIOLATION,
            reason_tag=_REASON_LOCK_CLASS_NOT_ARCHITECTURAL,
            event_kind=EVENT_KIND_PROMOTION,
            lock_class=lock_class,
        )

    raw_path = staged_row.get("module_path", "")
    if not isinstance(raw_path, str):
        return _fail(
            failure_code=F_AMDT_11_DEADLOCK_CARVEOUT_VIOLATION,
            reason_tag=_REASON_MODULE_PATH_NOT_STR,
            event_kind=EVENT_KIND_PROMOTION,
            lock_class=lock_class,
        )
    module_path = raw_path

    # Inline-literal architecture-file regex — tooth (b) carve-out scope.
    if not re.match(
        r"^pipeline/architecture/v[0-9]+(\.[0-9]+)?/("
        r"tilth_architecture_locked_v.*\.md"
        r"|architecture_v.*_amendment\.md"
        r")$",
        module_path,
    ):
        return _fail(
            failure_code=F_AMDT_11_DEADLOCK_CARVEOUT_VIOLATION,
            reason_tag=_REASON_MODULE_PATH_NOT_ARCHITECTURE,
            event_kind=EVENT_KIND_PROMOTION,
            lock_class=lock_class,
            module_path=module_path,
        )

    raw_bytes = staged_row.get("signed_row_bytes", b"")
    if not isinstance(raw_bytes, bytes):
        return _fail(
            failure_code=F_AMDT_11_DEADLOCK_CARVEOUT_VIOLATION,
            reason_tag=_REASON_SIGNED_ROW_BYTES_NOT_BYTES,
            event_kind=EVENT_KIND_PROMOTION,
            lock_class=lock_class,
            module_path=module_path,
        )

    raw_sig = staged_row.get("operator_signature", b"")
    if not isinstance(raw_sig, bytes):
        return _fail(
            failure_code=F_AMDT_11_DEADLOCK_CARVEOUT_VIOLATION,
            reason_tag=_REASON_OPERATOR_SIGNATURE_NOT_BYTES,
            event_kind=EVENT_KIND_PROMOTION,
            lock_class=lock_class,
            module_path=module_path,
        )

    try:
        sig_raw = signature_verify(raw_bytes, raw_sig, operator_public_key)
    except Exception as exc:
        return _fail(
            failure_code=F_AMDT_11_READER_FAIL,
            reason_tag=_REASON_SIGNATURE_VERIFY_RAISED,
            event_kind=EVENT_KIND_PROMOTION,
            lock_class=lock_class,
            module_path=module_path,
            reader_error=f"signature_verify: {_clip_error(exc)}",
        )

    if sig_raw is not True:
        return _fail(
            failure_code=F_AMDT_11_DEADLOCK_CARVEOUT_VIOLATION,
            reason_tag=_REASON_SIGNATURE_INVALID,
            event_kind=EVENT_KIND_PROMOTION,
            lock_class=lock_class,
            module_path=module_path,
        )

    return _ok(
        reason_tag=_REASON_CARVEOUT_GRANTED_OK,
        event_kind=EVENT_KIND_PROMOTION,
        emitted_event=EVENT_CARVEOUT_GRANTED,
        lock_class=lock_class,
        module_path=module_path,
    )
