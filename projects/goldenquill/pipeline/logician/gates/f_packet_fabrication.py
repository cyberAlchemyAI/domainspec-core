"""F-PACKET-FABRICATION — POST-emission + POST-load gate. [§4 v2.x.y.1 row 3, LIVE]

Aggregated counts in packet.gate_pass_counts + packet.score_signals +
packet.outcome cross-checked against Logfire span-tree aggregates for the
cycle. Detail names the divergent count/score.

Blueprint authority:
    - section_04_v2_x_y_1_packet_bodies_amendment.md §4.v2.x.y.1.1.3
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final, Mapping, Optional


F_PACKET_FABRICATION: Final[str] = "F-PACKET-FABRICATION"


@dataclass(frozen=True, kw_only=True)
class FabricationResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    sub_tag: Optional[str] = None


def check_f_packet_fabrication(
    *,
    packet_gate_pass_counts: Mapping[str, int],
    packet_score_signals: Mapping[str, Any],
    packet_outcome: Mapping[str, Any],
    span_tree_aggregates: Mapping[str, int],
    kfr_funder_outcome: Mapping[str, Any] | None = None,
) -> FabricationResult:
    """POST-emission + POST-load: packet aggregates match Logfire counts."""
    if not isinstance(packet_gate_pass_counts, Mapping):
        return FabricationResult(
            success=False,
            failure_code=F_PACKET_FABRICATION,
            detail="packet_gate_pass_counts must be Mapping",
        )
    if not isinstance(span_tree_aggregates, Mapping):
        return FabricationResult(
            success=False,
            failure_code=F_PACKET_FABRICATION,
            detail="span_tree_aggregates must be Mapping",
        )
    # Gate-pass-count cross-check — packet counts <= span-tree counts
    for fam in (
        "f_class_pass",
        "f_class_fail",
        "f_archivist_pass",
        "f_archivist_fail",
        "f_reflection_pass",
        "f_reflection_fail",
        "f_packet_pass",
        "f_packet_fail",
    ):
        packet_n = packet_gate_pass_counts.get(fam, 0)
        span_n = span_tree_aggregates.get(fam, 0)
        if not isinstance(packet_n, int) or isinstance(packet_n, bool):
            return FabricationResult(
                success=False,
                failure_code=F_PACKET_FABRICATION,
                sub_tag="gate_count_mismatch",
                detail=f"packet.gate_pass_counts.{fam} must be int",
            )
        if packet_n > span_n:
            return FabricationResult(
                success=False,
                failure_code=F_PACKET_FABRICATION,
                sub_tag="gate_count_mismatch",
                detail=(
                    f"packet.gate_pass_counts.{fam}={packet_n} exceeds "
                    f"span-tree aggregate {span_n}"
                ),
            )
    # judge_score must match most-recent recorded
    judge_score_pkt = packet_score_signals.get("judge_score")
    judge_score_span = span_tree_aggregates.get("most_recent_judge_score")
    if (
        judge_score_pkt is not None
        and judge_score_span is not None
        and judge_score_pkt != judge_score_span
    ):
        return FabricationResult(
            success=False,
            failure_code=F_PACKET_FABRICATION,
            sub_tag="score_mismatch",
            detail=(
                f"packet.score_signals.judge_score={judge_score_pkt} != "
                f"span-tree most_recent_judge_score={judge_score_span}"
            ),
        )
    # Outcome cross-check against KFR if BACKFILL packet
    if kfr_funder_outcome is not None and packet_outcome.get("status") in {
        "AWARDED",
        "DECLINED",
        "NO_DECISION",
    }:
        pkt_amount = packet_outcome.get("award_amount_minor_units")
        kfr_amount = kfr_funder_outcome.get("award_amount_minor_units")
        if (
            pkt_amount is not None
            and kfr_amount is not None
            and pkt_amount != kfr_amount
        ):
            return FabricationResult(
                success=False,
                failure_code=F_PACKET_FABRICATION,
                sub_tag="score_mismatch",
                detail=(
                    f"packet.outcome.award_amount={pkt_amount} != "
                    f"KFR funder-outcome ledger={kfr_amount}"
                ),
            )
    return FabricationResult(
        success=True,
        failure_code=None,
        detail="packet aggregates consistent with Logfire span tree",
    )


predicate_fabrication = check_f_packet_fabrication


__all__ = [
    "F_PACKET_FABRICATION",
    "FabricationResult",
    "check_f_packet_fabrication",
    "predicate_fabrication",
]
