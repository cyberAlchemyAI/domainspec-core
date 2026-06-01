"""F-PACKET-EVAL-ONLY-GROUNDED — PRE-emission gate. [§4 v2.x.y.1 row 6, LIVE]

packet.grounding_signal_classes MUST contain at least one of the six
non-LLM-eval-only classes. Sibling at artifact-validity layer to
F-REFLECTION-EVAL-ONLY-GROUNDED at producer-side (§4 v2.x.2).

Blueprint authority:
    - section_04_v2_x_y_1_packet_bodies_amendment.md §4.v2.x.y.1.1.6
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional


F_PACKET_EVAL_ONLY_GROUNDED: Final[str] = "F-PACKET-EVAL-ONLY-GROUNDED"

_NON_LLM_EVAL_CLASSES: Final[frozenset[str]] = frozenset(
    {
        "external_funder_outcome",
        "operator_approval",
        "logician_gate_outcome",
        "kfr_drift_event",
        "admin_risk_event",
        "match_db_outcome",
    }
)


@dataclass(frozen=True, kw_only=True)
class EvalOnlyGroundedResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    sub_tag: Optional[str] = None


def check_f_packet_eval_only_grounded(
    *,
    grounding_signal_classes: frozenset[str],
) -> EvalOnlyGroundedResult:
    """PRE-emission: at least one non-LLM-eval-only signal class present."""
    if not isinstance(grounding_signal_classes, (frozenset, set)):
        return EvalOnlyGroundedResult(
            success=False,
            failure_code=F_PACKET_EVAL_ONLY_GROUNDED,
            detail=(
                f"grounding_signal_classes must be frozenset[str], got "
                f"{type(grounding_signal_classes).__name__}"
            ),
        )
    if not grounding_signal_classes:
        return EvalOnlyGroundedResult(
            success=False,
            failure_code=F_PACKET_EVAL_ONLY_GROUNDED,
            detail="grounding_signal_classes empty",
        )
    intersection = grounding_signal_classes & _NON_LLM_EVAL_CLASSES
    if intersection:
        return EvalOnlyGroundedResult(
            success=True,
            failure_code=None,
            detail=(
                "grounding_signal_classes contains at least one non-LLM-"
                f"eval-only signal: {sorted(intersection)!r}"
            ),
        )
    return EvalOnlyGroundedResult(
        success=False,
        failure_code=F_PACKET_EVAL_ONLY_GROUNDED,
        sub_tag="llm_eval_only_grounding",
        detail=(
            "grounding_signal_classes is a subset of LLM-eval-only classes; "
            "at least one non-LLM-eval-only class required per §16.2.3 inv 11"
        ),
    )


predicate_eval_only_grounded = check_f_packet_eval_only_grounded


__all__ = [
    "F_PACKET_EVAL_ONLY_GROUNDED",
    "EvalOnlyGroundedResult",
    "check_f_packet_eval_only_grounded",
    "predicate_eval_only_grounded",
]
