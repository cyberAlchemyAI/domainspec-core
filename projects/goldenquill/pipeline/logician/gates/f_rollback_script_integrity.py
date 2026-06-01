"""F-ROLLBACK-SCRIPT-INTEGRITY (F-AMDT-05) — PRE-gate on rollback-script execution.

Every amendment with a rollback script carries an implicit trust claim: "if this
amendment fails, run this script to revert." A tampered rollback script could
corrupt pipeline state under the authority of the original amendment's audit
evidence. This gate verifies two integrity properties before any rollback
script executes:

1. **Signature integrity.** The script's Ed25519 signature is valid against
   the pinned public key. Verified via the injected
   :class:`SignatureVerifyCallable` — the gate never imports cryptography
   primitives.
2. **Ledger-pin integrity.** The ledger hash at the current ``lock_history``
   head matches the script's pinned ``ledger_hash_at_pin``. This binds the
   script to the lock-history state it was authored against; a ledger that
   has advanced since script authorship invalidates the script (new locks
   may change the invariants the script's rollback depends on).

The gate fires as a PRE-gate on the *execution request*, not on registration
— registration is a write event that belongs to a separate amendment-review
path; execution is the risk surface.

Blueprint anchor: ``pipeline/blueprint/v0.1/section_04_logician.md`` v2.1
(parent LOCK); v2.2 wave-3 delta row for F-AMDT-05.

Semantics (spec card v1, 2026-04-20):

* ``script_path`` missing / not a string / empty → FAIL (structural).
* ``script_bytes`` not a ``bytes`` instance → FAIL (caller-contract violation).
* ``signature`` not a ``bytes`` instance → FAIL.
* ``public_key`` not a ``bytes`` instance → FAIL.
* ``signature_verify`` returns not ``True`` (anything other than strict
  ``is True``) → FAIL with ``check_failed: "signature"``.
* ``signature_verify`` raises → FAIL fail-closed with ``reader_error``.
* ``script_metadata_reader`` raises → FAIL fail-closed.
* Metadata return is not a ``dict`` → FAIL.
* Metadata missing ``ledger_hash_at_pin`` OR value is not a non-empty ``str``
  → FAIL with ``check_failed: "ledger_hash"`` (pin-absent is a ledger-hash
  failure class, not a separate reason).
* ``ledger_hash_reader`` raises → FAIL fail-closed.
* ``ledger_hash_reader()`` return is not a ``str`` → FAIL.
* Exact string-equality comparison between live ledger hash and pinned hash.
  Mismatch → FAIL with ``check_failed: "ledger_hash"``.
* Both signature and ledger-hash checks fail independently → FAIL with
  ``check_failed: "both"``. Evaluation is short-circuit-free: both checks
  always run so the failure record is complete for operator triage.
* PASS only when signature is ``True`` AND live ledger hash == pinned hash.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional

from pipeline.logician.gates._protocols import (
    LedgerHashReaderCallable,
    ScriptMetadataReaderCallable,
    SignatureVerifyCallable,
)


F_AMDT_05: Final[str] = "F-AMDT-05"


_CHECK_SIGNATURE: Final[str] = "signature"
_CHECK_LEDGER_HASH: Final[str] = "ledger_hash"
_CHECK_BOTH: Final[str] = "both"

_REASON_SCRIPT_PATH_INVALID: Final[str] = "script_path_invalid"
_REASON_SCRIPT_BYTES_NOT_BYTES: Final[str] = "script_bytes_not_bytes"
_REASON_SIGNATURE_NOT_BYTES: Final[str] = "signature_not_bytes"
_REASON_PUBLIC_KEY_NOT_BYTES: Final[str] = "public_key_not_bytes"
_REASON_SIGNATURE_INVALID: Final[str] = "signature_verify_returned_false"
_REASON_SIGNATURE_VERIFY_RAISED: Final[str] = "signature_verify_raised"
_REASON_METADATA_READER_RAISED: Final[str] = "script_metadata_reader_raised"
_REASON_METADATA_NOT_DICT: Final[str] = "script_metadata_not_dict"
_REASON_LEDGER_HASH_PIN_MISSING: Final[str] = "ledger_hash_at_pin_missing_or_empty"
_REASON_LEDGER_READER_RAISED: Final[str] = "ledger_hash_reader_raised"
_REASON_LEDGER_LIVE_NOT_STR: Final[str] = "ledger_hash_live_not_str"
_REASON_LEDGER_HASH_MISMATCH: Final[str] = "ledger_hash_live_mismatches_pin"
_REASON_BOTH_FAILED: Final[str] = "signature_and_ledger_hash_both_failed"


@dataclass(frozen=True, kw_only=True)
class RollbackScriptIntegrityDetail:
    """Structured failure / pass record.

    ``reason_tag`` is always populated. ``check_failed`` is one of
    ``"signature"``, ``"ledger_hash"``, ``"both"`` for primary-path failures,
    or an empty string for structural pre-check failures that do not reach
    either substantive check. ``reader_error`` is non-empty only for
    fail-closed reader/verifier exceptions.
    """

    reason_tag: str
    check_failed: str
    reader_error: Optional[str]
    script_path: str


@dataclass(frozen=True, kw_only=True)
class RollbackScriptIntegrityResult:
    success: bool
    failure_code: Optional[str]
    detail: Optional[RollbackScriptIntegrityDetail]


def _fail(
    *,
    reason_tag: str,
    check_failed: str,
    script_path: str,
    reader_error: Optional[str] = None,
) -> RollbackScriptIntegrityResult:
    return RollbackScriptIntegrityResult(
        success=False,
        failure_code=F_AMDT_05,
        detail=RollbackScriptIntegrityDetail(
            reason_tag=reason_tag,
            check_failed=check_failed,
            reader_error=reader_error,
            script_path=script_path,
        ),
    )


def _ok(*, script_path: str) -> RollbackScriptIntegrityResult:
    return RollbackScriptIntegrityResult(
        success=True,
        failure_code=None,
        detail=RollbackScriptIntegrityDetail(
            reason_tag="ok",
            check_failed="",
            reader_error=None,
            script_path=script_path,
        ),
    )


def _clip_error(exc: BaseException) -> str:
    """Produce a ≤500-char error tag for ``reader_error`` records.

    Format: ``"{ExcClassName}: {str(exc)}"`` truncated at 500 bytes to keep
    the session-log row bounded. Truncation is plain slicing (not UTF-8
    aware) — callers tolerate non-canonical bytes because this value is
    advisory, not canonical.
    """

    return f"{type(exc).__name__}: {exc}"[:500]


def check_rollback_script_integrity(
    *,
    script_path: str,
    script_bytes: bytes,
    signature: bytes,
    public_key: bytes,
    signature_verify: SignatureVerifyCallable,
    ledger_hash_reader: LedgerHashReaderCallable,
    script_metadata_reader: ScriptMetadataReaderCallable,
) -> RollbackScriptIntegrityResult:
    """PRE-gate F-ROLLBACK-SCRIPT-INTEGRITY (F-AMDT-05).

    Verifies that a rollback script is authentic (valid Ed25519 signature
    under the pinned public key) AND that the ledger has not advanced since
    the script was authored (live ledger hash matches the script's pinned
    ``ledger_hash_at_pin`` metadata).

    Both checks run unconditionally — signature failure does not short-
    circuit the ledger check, and vice versa. This ensures the failure
    record is complete for operator triage when an adversary may have
    tampered with both the signature and the pinned hash independently.

    Returns a :class:`RollbackScriptIntegrityResult` with ``success=True``
    iff both checks PASS. Otherwise ``success=False`` with a
    :class:`RollbackScriptIntegrityDetail` describing which check(s) failed
    and why.
    """

    if not isinstance(script_path, str) or script_path == "":
        return _fail(
            reason_tag=_REASON_SCRIPT_PATH_INVALID,
            check_failed="",
            script_path=script_path if isinstance(script_path, str) else "",
        )

    if not isinstance(script_bytes, bytes):
        return _fail(
            reason_tag=_REASON_SCRIPT_BYTES_NOT_BYTES,
            check_failed="",
            script_path=script_path,
        )

    if not isinstance(signature, bytes):
        return _fail(
            reason_tag=_REASON_SIGNATURE_NOT_BYTES,
            check_failed="",
            script_path=script_path,
        )

    if not isinstance(public_key, bytes):
        return _fail(
            reason_tag=_REASON_PUBLIC_KEY_NOT_BYTES,
            check_failed="",
            script_path=script_path,
        )

    # Signature check. Run first but DO NOT short-circuit on failure —
    # the operator needs both check outcomes in the record.
    signature_ok = False
    signature_reason: Optional[str] = None
    signature_reader_error: Optional[str] = None
    try:
        raw = signature_verify(script_bytes, signature, public_key)
    except Exception as exc:
        signature_reason = _REASON_SIGNATURE_VERIFY_RAISED
        signature_reader_error = f"signature_verify: {_clip_error(exc)}"
    else:
        if raw is True:
            signature_ok = True
        else:
            signature_reason = _REASON_SIGNATURE_INVALID

    # Ledger-hash check. Runs unconditionally.
    ledger_ok = False
    ledger_reason: Optional[str] = None
    ledger_reader_error: Optional[str] = None

    pinned_hash: Optional[str] = None
    try:
        metadata = script_metadata_reader(script_path)
    except Exception as exc:
        ledger_reason = _REASON_METADATA_READER_RAISED
        ledger_reader_error = f"script_metadata_reader: {_clip_error(exc)}"
    else:
        if not isinstance(metadata, dict):
            ledger_reason = _REASON_METADATA_NOT_DICT
        else:
            raw_pin = metadata.get("ledger_hash_at_pin")
            if not isinstance(raw_pin, str) or raw_pin == "":
                ledger_reason = _REASON_LEDGER_HASH_PIN_MISSING
            else:
                pinned_hash = raw_pin

    if ledger_reason is None and pinned_hash is not None:
        try:
            live_hash = ledger_hash_reader()
        except Exception as exc:
            ledger_reason = _REASON_LEDGER_READER_RAISED
            ledger_reader_error = f"ledger_hash_reader: {_clip_error(exc)}"
        else:
            if not isinstance(live_hash, str):
                ledger_reason = _REASON_LEDGER_LIVE_NOT_STR
            elif live_hash != pinned_hash:
                ledger_reason = _REASON_LEDGER_HASH_MISMATCH
            else:
                ledger_ok = True

    if signature_ok and ledger_ok:
        return _ok(script_path=script_path)

    # Compose final record. If both substantive checks failed, merge into a
    # "both" record carrying the first non-empty reader_error (if any) and
    # a combined reason_tag.
    if not signature_ok and not ledger_ok:
        combined_reader_error = signature_reader_error or ledger_reader_error
        return _fail(
            reason_tag=_REASON_BOTH_FAILED,
            check_failed=_CHECK_BOTH,
            script_path=script_path,
            reader_error=combined_reader_error,
        )

    if not signature_ok:
        # Signature failure; ledger may have passed.
        return _fail(
            reason_tag=signature_reason or _REASON_SIGNATURE_INVALID,
            check_failed=_CHECK_SIGNATURE,
            script_path=script_path,
            reader_error=signature_reader_error,
        )

    # Ledger failure; signature must have passed.
    return _fail(
        reason_tag=ledger_reason or _REASON_LEDGER_HASH_MISMATCH,
        check_failed=_CHECK_LEDGER_HASH,
        script_path=script_path,
        reader_error=ledger_reader_error,
    )
