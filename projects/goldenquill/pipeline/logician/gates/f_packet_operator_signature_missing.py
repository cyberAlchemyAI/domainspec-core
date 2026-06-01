"""F-PACKET-OPERATOR-SIGNATURE-MISSING — PRE-load gate. [§4 v2.x.y.1 row 14, LIVE]

packet.outcome.status != "PENDING" REQUIRES packet.operator_signature_ed25519
non-None. Defensive symmetry sub-tag .signature_present_for_pending per
Cycle 2 RT-C2-02 fold-in: PENDING REQUIRES operator_signature_ed25519 None.

Schema-layer invariant 16 enforces at construction; predicate body is the
runtime failure-code surface.

Blueprint authority:
    - section_04_v2_x_y_1_packet_bodies_amendment.md §4.v2.x.y.1.1.14
    - section_16_reflection_packet.md §16.3 emit + backfill discipline
    - section_16_reflection_packet.md §16.10.2 RT-C2-02 fold-in
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional


F_PACKET_OPERATOR_SIGNATURE_MISSING: Final[str] = "F-PACKET-OPERATOR-SIGNATURE-MISSING"


@dataclass(frozen=True, kw_only=True)
class OperatorSignatureMissingResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    sub_tag: Optional[str] = None


def check_f_packet_operator_signature_missing(
    *,
    packet_outcome_status: str,
    packet_operator_signature: str | None,
) -> OperatorSignatureMissingResult:
    """PRE-load: non-PENDING requires sig; PENDING forbids sig."""
    if packet_outcome_status not in {"PENDING", "AWARDED", "DECLINED", "NO_DECISION"}:
        return OperatorSignatureMissingResult(
            success=False,
            failure_code=F_PACKET_OPERATOR_SIGNATURE_MISSING,
            detail=f"packet_outcome_status {packet_outcome_status!r} unknown",
        )
    if packet_outcome_status == "PENDING":
        if packet_operator_signature is not None:
            return OperatorSignatureMissingResult(
                success=False,
                failure_code=F_PACKET_OPERATOR_SIGNATURE_MISSING,
                sub_tag="signature_present_for_pending",
                detail=(
                    "outcome.status='PENDING' forbids non-None "
                    "operator_signature_ed25519 (defensive symmetry per "
                    "RT-C2-02 fold-in)"
                ),
            )
        return OperatorSignatureMissingResult(
            success=True,
            failure_code=None,
            detail="PENDING packet with None operator signature (correct)",
        )
    # Non-PENDING
    if packet_operator_signature is None:
        return OperatorSignatureMissingResult(
            success=False,
            failure_code=F_PACKET_OPERATOR_SIGNATURE_MISSING,
            sub_tag="missing_for_outcome",
            detail=(
                f"outcome.status={packet_outcome_status!r} REQUIRES "
                "operator_signature_ed25519 non-None"
            ),
        )
    return OperatorSignatureMissingResult(
        success=True,
        failure_code=None,
        detail=f"{packet_outcome_status} packet carries operator signature (correct)",
    )


predicate_operator_signature_missing = check_f_packet_operator_signature_missing


__all__ = [
    "F_PACKET_OPERATOR_SIGNATURE_MISSING",
    "OperatorSignatureMissingResult",
    "check_f_packet_operator_signature_missing",
    "predicate_operator_signature_missing",
]
