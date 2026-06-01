"""F-PACKET-SPAN-PROVENANCE-MISSING — PRE-emission gate. [§4 v2.x.y.1 row 8, LIVE]

Body mirrors ``check_f_wpfa_span_provenance_missing`` byte-for-byte +
extends with the ``.span_id_from_different_cycle`` sub-tag per Cycle 1
RT-08 fold-in.

**RESOLVES §17 v1 §6.5 forward-reference at the v0.2 first wave LOCK.**

Blueprint authority:
    - section_04_v2_x_y_1_packet_bodies_amendment.md §4.v2.x.y.1.1.8
    - section_17_watts_per_funding_action.md §17.6 (forward-reference resolved)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Iterable, Mapping, Optional


F_PACKET_SPAN_PROVENANCE_MISSING: Final[str] = "F-PACKET-SPAN-PROVENANCE-MISSING"

# Minimum claim keys every ReflectionPacket MUST map. v0.2 first wave.
_REQUIRED_CLAIM_KEYS_V0_2: Final[frozenset[str]] = frozenset(
    {
        "gate_pass_counts.f_packet_pass",
        "gate_pass_counts.f_packet_fail",
        "gate_pass_counts.f_logician_total_pass",
        "gate_pass_counts.f_logician_total_fail",
        "score_signals.judge_score",
        "score_signals.red_team_score",
        "outcome.status",
    }
)


@dataclass(frozen=True, kw_only=True)
class SpanProvenanceMissingResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    sub_tag: Optional[str] = None
    missing_claim_keys: tuple[str, ...] = ()


def check_f_packet_span_provenance_missing(
    *,
    per_claim_span_ids: Mapping[str, tuple[str, ...]],
    resolvable_span_ids: Iterable[str],
    packet_cycle_id: str,
    span_to_cycle: Mapping[str, str] | None = None,
    required_claim_keys: frozenset[str] = _REQUIRED_CLAIM_KEYS_V0_2,
) -> SpanProvenanceMissingResult:
    """PRE-emission: every required claim key maps to >=1 resolvable, same-cycle span_id.

    ``span_to_cycle`` maps span_id → cycle_id for cross-cycle detection
    (sub-tag ``.span_id_from_different_cycle`` per RT-08 fold-in). When
    None, the cross-cycle check is skipped (v0.2 callers can opt out).
    """
    if not isinstance(per_claim_span_ids, Mapping):
        return SpanProvenanceMissingResult(
            success=False,
            failure_code=F_PACKET_SPAN_PROVENANCE_MISSING,
            sub_tag="claim_key_unmapped",
            detail="per_claim_span_ids must be a Mapping",
        )
    resolvable_set = set(resolvable_span_ids)
    missing_required = sorted(
        k for k in required_claim_keys if k not in per_claim_span_ids
    )
    if missing_required:
        return SpanProvenanceMissingResult(
            success=False,
            failure_code=F_PACKET_SPAN_PROVENANCE_MISSING,
            sub_tag="claim_key_unmapped",
            detail=(
                f"required claim keys absent from per_claim_span_ids: "
                f"{missing_required!r}"
            ),
            missing_claim_keys=tuple(missing_required),
        )
    for ckey, sids in per_claim_span_ids.items():
        if not isinstance(sids, tuple) or not sids:
            return SpanProvenanceMissingResult(
                success=False,
                failure_code=F_PACKET_SPAN_PROVENANCE_MISSING,
                sub_tag="no_trace_id",
                detail=f"claim {ckey!r} maps to empty span_ids tuple",
                missing_claim_keys=(ckey,),
            )
        for s in sids:
            if not isinstance(s, str) or not s:
                return SpanProvenanceMissingResult(
                    success=False,
                    failure_code=F_PACKET_SPAN_PROVENANCE_MISSING,
                    sub_tag="no_trace_id",
                    detail=f"claim {ckey!r} contains empty/non-str span_id",
                    missing_claim_keys=(ckey,),
                )
            if s not in resolvable_set:
                return SpanProvenanceMissingResult(
                    success=False,
                    failure_code=F_PACKET_SPAN_PROVENANCE_MISSING,
                    sub_tag="trace_id_unresolvable_in_logfire",
                    detail=(
                        f"claim {ckey!r} span_id {s!r} not present in "
                        "Logfire export"
                    ),
                    missing_claim_keys=(ckey,),
                )
            # RT-08 fold-in — cross-cycle detection
            if span_to_cycle is not None:
                span_cycle = span_to_cycle.get(s)
                if span_cycle is not None and span_cycle != packet_cycle_id:
                    return SpanProvenanceMissingResult(
                        success=False,
                        failure_code=F_PACKET_SPAN_PROVENANCE_MISSING,
                        sub_tag="span_id_from_different_cycle",
                        detail=(
                            f"claim {ckey!r} span_id {s!r} parent cycle "
                            f"{span_cycle!r} != packet.cycle_id "
                            f"{packet_cycle_id!r}"
                        ),
                        missing_claim_keys=(ckey,),
                    )
    return SpanProvenanceMissingResult(
        success=True,
        failure_code=None,
        detail=(
            "all required claim keys map to resolvable Logfire span_ids "
            "from the packet's own cycle"
        ),
    )


predicate_span_provenance_missing = check_f_packet_span_provenance_missing


__all__ = [
    "F_PACKET_SPAN_PROVENANCE_MISSING",
    "SpanProvenanceMissingResult",
    "check_f_packet_span_provenance_missing",
    "predicate_span_provenance_missing",
]
