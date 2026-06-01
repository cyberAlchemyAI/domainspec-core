"""F-UPLOADER-SIGNATURE-MISMATCH — PRE-gate.

Per Blueprint §12.9.5 + §4 v2.7 amendment. Distinct from
F-UPLOADER-SIGNATURE-MISSING (presence) — fires when the operator did sign
but the bundle bytes have changed since signing.

This module is the **Logician-side surface** for the predicate. It owns
exactly one failure code (PRE-32 / SIGNATURE-MISMATCH). Per the §4 v2.2
``_protocols.py`` pattern (E-017 injected-callable), the hash check is a
Protocol-typed dependency injected into ``check_uploader_signature_
mismatch``. Production binds to the seat-side ``_check_signature_hash``
from ``pipeline/orchestrator/seats/uploader.py`` via the
``_uploader_defaults`` registry; tests inject mocks.

This module imports only ``_uploader_protocols`` and ``_uploader_defaults``
— **zero direct imports from ``pipeline.orchestrator.seats.uploader``**.

Surface discipline: this gate ONLY emits MISMATCH. When the signature is
absent (no presence), this surface returns PASS — that condition is the
PRE-31 surface's responsibility. The presence-check is invoked first via
the same Protocol Defaults registry to discriminate.

Bypass: M13.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from pipeline.logician.gates._uploader_defaults import (
    get_default_signature_hash_check,
    get_default_signature_presence_check,
)
from pipeline.logician.gates._uploader_protocols import (
    SignatureHashCheck,
    SignaturePresenceCheck,
)


F_UPLOADER_SIGNATURE_MISMATCH: str = "F-UPLOADER-SIGNATURE-MISMATCH"


@dataclass(frozen=True, kw_only=True)
class SignatureMismatchResult:
    """Result of F-UPLOADER-SIGNATURE-MISMATCH check."""

    success: bool
    failure_code: Optional[str]
    detail: str


def check_uploader_signature_mismatch(
    *,
    uploader_input: object,
    submission_bundle_bytes: bytes,
    check: Optional[SignatureHashCheck] = None,
    presence_check: Optional[SignaturePresenceCheck] = None,
) -> SignatureMismatchResult:
    """PRE-gate (PRE-32): only emits F-UPLOADER-SIGNATURE-MISMATCH.

    Parameters
    ----------
    uploader_input
        The Uploader input bundle (duck-typed).
    submission_bundle_bytes
        The on-disk bytes of the SubmissionBundle being assembled. Hashed
        by the injected ``check`` to compare against the operator
        signature's pinned hash.
    check
        Injected ``SignatureHashCheck`` callable. When ``None``, the
        seat-side ``_check_signature_hash`` predicate is bound via the
        ``_uploader_defaults`` registry.
    presence_check
        Injected ``SignaturePresenceCheck`` callable used to discriminate
        ABSENT (handled by PRE-31) from MISMATCH (handled here). When
        ``None``, the seat-side default is bound.
    """
    presence_callable = presence_check or get_default_signature_presence_check()
    if not presence_callable(uploader_input):
        # ABSENT — PRE-31 surface owns this; PASS here per §12.9.5
        # audit-trail-clarity rule.
        return SignatureMismatchResult(
            success=True,
            failure_code=None,
            detail=(
                "no signature present (presence is the SIGNATURE-MISSING "
                "surface's responsibility)"
            ),
        )
    hash_check = check or get_default_signature_hash_check()
    if hash_check(uploader_input, submission_bundle_bytes):
        return SignatureMismatchResult(
            success=True,
            failure_code=None,
            detail="operator signature hash matches bundle bytes",
        )
    return SignatureMismatchResult(
        success=False,
        failure_code=F_UPLOADER_SIGNATURE_MISMATCH,
        detail="signature hash mismatch — bundle modified after operator sign-off",
    )
