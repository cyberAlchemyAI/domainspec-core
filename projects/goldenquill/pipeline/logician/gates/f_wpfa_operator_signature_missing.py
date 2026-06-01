"""F-WPFA-OPERATOR-SIGNATURE-MISSING — PRE-PDF-emit gate. [§5.1.WPFA.8]

Trigger: buyer-facing PDF emission attempted without
``signed_by_operator_ed25519`` set on the source receipt.

This is the structural attestation boundary. M13 NOT permitted per OQ-E
default — it is not applicable to draft handoff artifact, but required / blocking for final FIT Farms submission packet.

Sub-tag: ``.pdf_emission_without_attestation``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional


F_WPFA_OPERATOR_SIGNATURE_MISSING: Final[str] = "F-WPFA-OPERATOR-SIGNATURE-MISSING"


@dataclass(frozen=True, kw_only=True)
class OperatorSignatureMissingResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    sub_tag: Optional[str] = None

    # Stage-aware fields (Consulting Node Doctrine)
    has_findings: bool = False
    blocking: bool = True
    advisory_only: bool = False
    requires_handoff_disclosure: bool = False


from pipeline.logician.types import OutputType, GateStage, ArtifactType, FINAL_OR_SUBMISSION_STAGES, THIRD_PARTY_FINAL_BLOCKED_ARTIFACTS, THIRD_PARTY_HANDOFF_ARTIFACTS

def check_f_wpfa_operator_signature_missing(
    *,
    signed_by_operator_ed25519: Optional[str],
    target_artifact: str = "pdf",
    output_type: OutputType = "FIT_FARMS_SUBMISSION_PACKET",
    stage: GateStage = "final_export_attempt",
    artifact_type: ArtifactType = "pdf",
) -> OperatorSignatureMissingResult:
    """PRE-PDF-emit: signed_by_operator_ed25519 must be non-None.

    Verifies presence + well-formedness only. Cryptographic verification
    happens at the Cedar policy layer (``cycle_receipt_operator_attestation``)
    and the Cycle Accountant emission code path; this gate is defense-in-
    depth at the PRE-PDF-emit boundary.
    """
    is_pdf_like = target_artifact == "pdf" or artifact_type in THIRD_PARTY_FINAL_BLOCKED_ARTIFACTS or artifact_type in THIRD_PARTY_HANDOFF_ARTIFACTS
    if not is_pdf_like:
        # The gate is scoped to buyer-facing PDF only. Internal-only emission
        # paths skip this gate (they are internal/unsigned).
        return OperatorSignatureMissingResult(
            success=True,
            failure_code=None,
            detail=(
                f"target_artifact={target_artifact!r} / artifact_type={artifact_type!r} "
                "is not PDF-like — gate not applicable"
            ),
            has_findings=False,
            blocking=False,
        )

    has_findings = signed_by_operator_ed25519 is None or not (
        isinstance(signed_by_operator_ed25519, str)
        and len(signed_by_operator_ed25519) == 128
        and all(c in "0123456789abcdef" for c in signed_by_operator_ed25519.lower())
    )

    blocking = has_findings
    advisory_only = False
    requires_handoff_disclosure = False

    if has_findings:
        if output_type == "THIRD_PARTY_DRAFT_DELIVERABLE":
            # For third party drafts, we do not require operator signature on the draft handoff PDF.
            # But if they try to generate a final submission PDF, we block it entirely because FIT Farms doesn't authorize third-party submissions.
            if artifact_type in THIRD_PARTY_FINAL_BLOCKED_ARTIFACTS or stage in FINAL_OR_SUBMISSION_STAGES:
                blocking = True
            else:
                blocking = False
                advisory_only = True
                requires_handoff_disclosure = True
        else:
            if stage in ("draft_generation", "draft_review"):
                blocking = False
                advisory_only = True

    if not has_findings:
        return OperatorSignatureMissingResult(
            success=True,
            failure_code=None,
            detail="operator attestation present and well-formed",
            has_findings=False,
            blocking=False,
        )

    if signed_by_operator_ed25519 is None:
        return OperatorSignatureMissingResult(
            success=False,
            failure_code=F_WPFA_OPERATOR_SIGNATURE_MISSING,
            sub_tag="pdf_emission_without_attestation",
            detail=(
                "buyer-facing PDF emission attempted without operator "
                "attestation (signed_by_operator_ed25519 is None) — "
                "structural attestation boundary"
            ),
            has_findings=has_findings,
            blocking=blocking,
            advisory_only=advisory_only,
            requires_handoff_disclosure=requires_handoff_disclosure,
        )
    else:
        return OperatorSignatureMissingResult(
            success=False,
            failure_code=F_WPFA_OPERATOR_SIGNATURE_MISSING,
            sub_tag="pdf_emission_without_attestation",
            detail=(
                "signed_by_operator_ed25519 must be 128-char lowercase hex"
            ),
            has_findings=has_findings,
            blocking=blocking,
            advisory_only=advisory_only,
            requires_handoff_disclosure=requires_handoff_disclosure,
        )


__all__ = [
    "F_WPFA_OPERATOR_SIGNATURE_MISSING",
    "OperatorSignatureMissingResult",
    "check_f_wpfa_operator_signature_missing",
]
