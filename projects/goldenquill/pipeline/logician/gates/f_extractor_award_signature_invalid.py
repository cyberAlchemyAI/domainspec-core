"""F-EXTRACTOR-AWARD-SIGNATURE-INVALID — PRE on AWARD_INGEST (Law 5, P0).

Per architecture v7.0.4 §5.3.

When Intake's AWARD_INGEST mode is invoked, two pre-extraction
verifications fire BEFORE any ``proposal_commitments.yaml`` row is
written:

* ``F-EXTRACTOR-AWARD-SIGNATURE-INVALID.proposal`` — won-proposal
  artifact's operator ``SignedClaimEvidenceMap`` Ed25519 signature
  must verify (per existing Section 4 §4.5 verify_claim_evidence_map
  discipline).

* ``F-EXTRACTOR-AWARD-SIGNATURE-INVALID.award`` — award document
  signature, where present, must verify against the funder's
  published signing key (operator-curated per
  ``vault_shared/funders/<funder_id>/signing_keys.yaml``). Where the
  funder does not publish signing keys, operator confirms the document
  path via attestation flag at the CLI invocation; the gate accepts
  unsigned-with-attestation as PASS for the award leg.

Both legs fail-closed; on any failure AWARD_INGEST refuses the
operation and writes the relevant sub-code to the admin-risk ledger
at HIGH severity.

Bypass: M13 (audited operator override; HIGH severity admin-risk entry).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional

from pipeline.logician.gates._protocols import SignatureVerifyCallable


F_EXTRACTOR_AWARD_SIGNATURE_INVALID: Final[str] = (
    "F-EXTRACTOR-AWARD-SIGNATURE-INVALID"
)
F_EXTRACTOR_AWARD_SIGNATURE_INVALID_PROPOSAL: Final[str] = (
    "F-EXTRACTOR-AWARD-SIGNATURE-INVALID.proposal"
)
F_EXTRACTOR_AWARD_SIGNATURE_INVALID_AWARD: Final[str] = (
    "F-EXTRACTOR-AWARD-SIGNATURE-INVALID.award"
)


@dataclass(frozen=True, kw_only=True)
class AwardSignatureLeg:
    """One pre-extraction signature verification leg.

    For the proposal leg: signature/message_bytes/public_key are the
    operator-signed SignedClaimEvidenceMap of the won-proposal artifact.

    For the award leg: signature/message_bytes/public_key are the
    funder's signature over the award document. If the funder does not
    publish signing keys, supply ``unsigned_with_attestation=True``
    instead and leave the signature fields as empty bytes — the gate
    treats the leg as PASS by operator attestation.
    """

    signature: bytes
    message_bytes: bytes
    public_key: bytes
    unsigned_with_attestation: bool = False


@dataclass(frozen=True, kw_only=True)
class AwardSignatureResult:
    """Result of F-EXTRACTOR-AWARD-SIGNATURE-INVALID check."""

    success: bool
    failure_code: Optional[str]
    detail: str
    proposal_verified: bool = False
    award_verified: bool = False
    award_unsigned_attested: bool = False


def _verify_leg(
    leg: AwardSignatureLeg,
    signature_verify: SignatureVerifyCallable,
) -> tuple[bool, Optional[str]]:
    """Returns (verified, error_str).

    error_str is None when verification raised no exception.
    """
    try:
        result = signature_verify(
            leg.message_bytes, leg.signature, leg.public_key
        )
    except Exception as exc:  # noqa: BLE001 — fail-closed, capture class
        return False, f"{type(exc).__name__}: {exc}"
    return result is True, None


def check_extractor_award_signature_invalid(
    *,
    proposal_leg: AwardSignatureLeg,
    award_leg: AwardSignatureLeg,
    signature_verify: SignatureVerifyCallable,
) -> AwardSignatureResult:
    """PRE-AWARD_INGEST gate: proposal + award signature verification.

    Parameters
    ----------
    proposal_leg
        Won-proposal SignedClaimEvidenceMap signature material.
        ``unsigned_with_attestation`` is FORBIDDEN on the proposal leg
        — the operator-signed map is mandatory per Section 4 §4.5; the
        gate fails-closed if the field is set.
    award_leg
        Funder-signed award document signature material. When the
        funder does not publish signing keys, supply
        ``unsigned_with_attestation=True`` to record operator
        attestation; the leg PASSes by attestation.
    signature_verify
        Injected Ed25519 verifier per :class:`SignatureVerifyCallable`.

    Returns
    -------
    AwardSignatureResult. Success requires PROPOSAL verified AND
    (AWARD verified OR AWARD attested-unsigned).
    """
    if proposal_leg.unsigned_with_attestation:
        return AwardSignatureResult(
            success=False,
            failure_code=F_EXTRACTOR_AWARD_SIGNATURE_INVALID_PROPOSAL,
            detail=(
                "proposal leg may not use unsigned_with_attestation — "
                "won-proposal SignedClaimEvidenceMap is mandatory per "
                "Section 4 §4.5 verify_claim_evidence_map discipline"
            ),
        )

    proposal_ok, proposal_err = _verify_leg(proposal_leg, signature_verify)
    if not proposal_ok:
        return AwardSignatureResult(
            success=False,
            failure_code=F_EXTRACTOR_AWARD_SIGNATURE_INVALID_PROPOSAL,
            detail=(
                "won-proposal SignedClaimEvidenceMap Ed25519 verification "
                "failed"
                + (f" — {proposal_err}" if proposal_err else "")
            ),
            proposal_verified=False,
        )

    if award_leg.unsigned_with_attestation:
        return AwardSignatureResult(
            success=True,
            failure_code=None,
            detail=(
                "proposal verified; award leg passed by operator "
                "attestation (funder publishes no signing keys)"
            ),
            proposal_verified=True,
            award_verified=False,
            award_unsigned_attested=True,
        )

    award_ok, award_err = _verify_leg(award_leg, signature_verify)
    if not award_ok:
        return AwardSignatureResult(
            success=False,
            failure_code=F_EXTRACTOR_AWARD_SIGNATURE_INVALID_AWARD,
            detail=(
                "award document Ed25519 verification failed against "
                "funder's published signing key"
                + (f" — {award_err}" if award_err else "")
            ),
            proposal_verified=True,
            award_verified=False,
        )

    return AwardSignatureResult(
        success=True,
        failure_code=None,
        detail=(
            "proposal SignedClaimEvidenceMap verified; award document "
            "signature verified against funder's published signing key"
        ),
        proposal_verified=True,
        award_verified=True,
    )


__all__ = [
    "F_EXTRACTOR_AWARD_SIGNATURE_INVALID",
    "F_EXTRACTOR_AWARD_SIGNATURE_INVALID_AWARD",
    "F_EXTRACTOR_AWARD_SIGNATURE_INVALID_PROPOSAL",
    "AwardSignatureLeg",
    "AwardSignatureResult",
    "check_extractor_award_signature_invalid",
]
