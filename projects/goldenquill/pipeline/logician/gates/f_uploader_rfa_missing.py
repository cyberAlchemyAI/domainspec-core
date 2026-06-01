"""F-UPLOADER-RFA-MISSING — PRE-gate.

Per Blueprint §12.9.5 + §4 v2.7 amendment. Law 1 enforcement. The
``RfaExtractedRecord`` must be present on the input bundle AND its
``rfa_content_sha3_512`` must match the session manifest pin. Either fault
blocks Uploader assembly — without a verified RFA, every downstream Law 1
trace is broken.

Fail-closed. No file I/O — the manifest pin is read by an injected
``ManifestPinReaderCallable``. Bypass: M13.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol, runtime_checkable


F_UPLOADER_RFA_MISSING: str = "F-UPLOADER-RFA-MISSING"


@runtime_checkable
class _RfaRecord(Protocol):
    rfa_content_sha3_512: str


@runtime_checkable
class ManifestPinReaderCallable(Protocol):
    """Returns the session-manifest-pinned RFA SHA3-512 for `run_id`."""

    def __call__(self, run_id: str) -> Optional[str]: ...


@dataclass(frozen=True, kw_only=True)
class RfaMissingResult:
    """Result of F-UPLOADER-RFA-MISSING check."""

    success: bool
    failure_code: Optional[str]
    reason_tag: Optional[str]  # "rfa_record_absent" | "rfa_pin_absent" | "rfa_hash_mismatch"
    detail: str


def check_uploader_rfa_missing(
    *,
    run_id: str,
    rfa: Optional[_RfaRecord],
    manifest_pin_reader: ManifestPinReaderCallable,
) -> RfaMissingResult:
    """PRE-gate: RFA present AND hash matches session manifest pin."""
    if rfa is None:
        return RfaMissingResult(
            success=False,
            failure_code=F_UPLOADER_RFA_MISSING,
            reason_tag="rfa_record_absent",
            detail="UploaderInput.rfa_extracted_record is None",
        )
    try:
        pinned = manifest_pin_reader(run_id)
    except Exception as exc:
        return RfaMissingResult(
            success=False,
            failure_code=F_UPLOADER_RFA_MISSING,
            reason_tag="rfa_pin_absent",
            detail=f"manifest_pin_reader raised for run_id={run_id!r}: {exc!r}",
        )
    if pinned is None:
        return RfaMissingResult(
            success=False,
            failure_code=F_UPLOADER_RFA_MISSING,
            reason_tag="rfa_pin_absent",
            detail=f"session manifest has no RFA pin for run_id={run_id!r}",
        )
    if rfa.rfa_content_sha3_512 != pinned:
        return RfaMissingResult(
            success=False,
            failure_code=F_UPLOADER_RFA_MISSING,
            reason_tag="rfa_hash_mismatch",
            detail=(
                f"RFA hash {rfa.rfa_content_sha3_512[:32]}... does not match "
                f"session manifest pin {pinned[:32]}..."
            ),
        )
    return RfaMissingResult(
        success=True,
        failure_code=None,
        reason_tag=None,
        detail="RFA present and hash matches session manifest pin",
    )
