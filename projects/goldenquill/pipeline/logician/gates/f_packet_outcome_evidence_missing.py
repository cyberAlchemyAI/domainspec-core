"""F-PACKET-OUTCOME-EVIDENCE-MISSING — PRE-emission + PRE-load gate.
[§4 v2.x.y.1 row 17, LIVE]

outcome.status != "PENDING" REQUIRES outcome.outcome_evidence_span_ids
non-empty AND every span_id resolvable AND from same cycle as packet.cycle_id.

Schema-layer invariant covers the non-empty case; predicate body adds
resolvability + cross-cycle check (sub-tag .evidence_span_from_different_cycle).

Blueprint authority:
    - section_04_v2_x_y_1_packet_bodies_amendment.md §4.v2.x.y.1.1.17
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Iterable, Mapping, Optional


F_PACKET_OUTCOME_EVIDENCE_MISSING: Final[str] = "F-PACKET-OUTCOME-EVIDENCE-MISSING"


@dataclass(frozen=True, kw_only=True)
class OutcomeEvidenceMissingResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    sub_tag: Optional[str] = None


def check_f_packet_outcome_evidence_missing(
    *,
    packet_outcome_status: str,
    outcome_evidence_span_ids: tuple[str, ...],
    packet_cycle_id: str,
    resolvable_span_ids: Iterable[str],
    span_to_cycle: Mapping[str, str] | None = None,
) -> OutcomeEvidenceMissingResult:
    """Non-PENDING: evidence non-empty + resolvable + same cycle."""
    if packet_outcome_status == "PENDING":
        if outcome_evidence_span_ids:
            return OutcomeEvidenceMissingResult(
                success=False,
                failure_code=F_PACKET_OUTCOME_EVIDENCE_MISSING,
                detail="PENDING packet must have empty outcome_evidence_span_ids",
            )
        return OutcomeEvidenceMissingResult(
            success=True,
            failure_code=None,
            detail="PENDING packet correctly has no outcome evidence",
        )
    # Non-PENDING — require non-empty + resolvable + same cycle
    if not outcome_evidence_span_ids:
        return OutcomeEvidenceMissingResult(
            success=False,
            failure_code=F_PACKET_OUTCOME_EVIDENCE_MISSING,
            sub_tag="evidence_empty",
            detail=(
                f"outcome.status={packet_outcome_status!r} requires non-empty "
                "outcome_evidence_span_ids"
            ),
        )
    resolvable_set = set(resolvable_span_ids)
    for sid in outcome_evidence_span_ids:
        if sid not in resolvable_set:
            return OutcomeEvidenceMissingResult(
                success=False,
                failure_code=F_PACKET_OUTCOME_EVIDENCE_MISSING,
                sub_tag="evidence_span_unresolvable",
                detail=f"outcome evidence span_id {sid!r} not in Logfire export",
            )
        if span_to_cycle is not None:
            span_cycle = span_to_cycle.get(sid)
            if span_cycle is not None and span_cycle != packet_cycle_id:
                return OutcomeEvidenceMissingResult(
                    success=False,
                    failure_code=F_PACKET_OUTCOME_EVIDENCE_MISSING,
                    sub_tag="evidence_span_from_different_cycle",
                    detail=(
                        f"evidence span_id {sid!r} parent cycle "
                        f"{span_cycle!r} != packet.cycle_id "
                        f"{packet_cycle_id!r}"
                    ),
                )
    return OutcomeEvidenceMissingResult(
        success=True,
        failure_code=None,
        detail=(
            f"outcome.status={packet_outcome_status!r} evidence: "
            f"{len(outcome_evidence_span_ids)} resolvable same-cycle span_ids"
        ),
    )


predicate_outcome_evidence_missing = check_f_packet_outcome_evidence_missing


__all__ = [
    "F_PACKET_OUTCOME_EVIDENCE_MISSING",
    "OutcomeEvidenceMissingResult",
    "check_f_packet_outcome_evidence_missing",
    "predicate_outcome_evidence_missing",
]
