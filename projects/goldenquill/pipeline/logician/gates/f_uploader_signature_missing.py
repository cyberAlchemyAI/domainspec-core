"""F-UPLOADER-SIGNATURE-MISSING — PRE-gate.

Per Blueprint §12.9.4 + §4 v2.7 amendment. Operator sign-off must be
present on the input bundle before Uploader will assemble a package.

This module is the **Logician-side surface** for the predicate. It owns
exactly one failure code (PRE-31 / SIGNATURE-MISSING). Per the §4 v2.2
``_protocols.py`` pattern (E-017 injected-callable), the presence check
itself is a Protocol-typed dependency injected into ``check_uploader_
signature_missing``. Production binds to the seat-side
``_check_signature_presence`` from
``pipeline/orchestrator/seats/uploader.py`` via the
``_uploader_defaults`` registry; tests inject mocks.

This module imports only ``_uploader_protocols`` and ``_uploader_defaults``
— **zero direct imports from ``pipeline.orchestrator.seats.uploader``**.

Bypass: M13.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from pipeline.logician.gates._uploader_defaults import (
    get_default_signature_presence_check,
)
from pipeline.logician.gates._uploader_protocols import SignaturePresenceCheck


F_UPLOADER_SIGNATURE_MISSING: str = "F-UPLOADER-SIGNATURE-MISSING"


@dataclass(frozen=True, kw_only=True)
class SignatureMissingResult:
    """Result of F-UPLOADER-SIGNATURE-MISSING check."""

    success: bool
    failure_code: Optional[str]
    detail: str


def check_uploader_signature_missing(
    *,
    uploader_input: object,
    submission_bundle_bytes: bytes = b"",
    check: Optional[SignaturePresenceCheck] = None,
) -> SignatureMissingResult:
    """PRE-gate (PRE-31): only emits F-UPLOADER-SIGNATURE-MISSING.

    Parameters
    ----------
    uploader_input
        The Uploader input bundle (duck-typed; concrete shape from
        ``pipeline.orchestrator.seats.uploader.UploaderInput``).
    submission_bundle_bytes
        Reserved for backwards-compatibility with the v2.7-pre interface.
        Unused by this surface — presence is the only concern; hash
        validation belongs to PRE-32 (SIGNATURE-MISMATCH).
    check
        Injected ``SignaturePresenceCheck`` callable. When ``None``, the
        seat-side ``_check_signature_presence`` predicate is bound via
        the ``_uploader_defaults`` registry (lazy, idempotent).
    """
    presence_check = check or get_default_signature_presence_check()
    if presence_check(uploader_input):
        return SignatureMissingResult(
            success=True,
            failure_code=None,
            detail="operator signature present",
        )
    return SignatureMissingResult(
        success=False,
        failure_code=F_UPLOADER_SIGNATURE_MISSING,
        detail="operator signature absent on submission bundle",
    )
