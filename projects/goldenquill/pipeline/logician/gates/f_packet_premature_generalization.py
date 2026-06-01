"""F-PACKET-PREMATURE-GENERALIZATION — PRE-emission gate. [§4 v2.x.y.1 row 7, LIVE]

For every ProposedLesson in packet.lessons_proposed: frequency == 1
REQUIRES severity == "HIGH". Operator SP0 override surface: per-grant SP0
may relax this rule with HIGH-severity admin-risk ledger entry.

Schema-layer invariant 10 enforces at construction; predicate body is the
runtime failure-code surface + SP0 override path.

Blueprint authority:
    - section_04_v2_x_y_1_packet_bodies_amendment.md §4.v2.x.y.1.1.7
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final, Iterable, Optional


F_PACKET_PREMATURE_GENERALIZATION: Final[str] = "F-PACKET-PREMATURE-GENERALIZATION"


@dataclass(frozen=True, kw_only=True)
class PrematureGeneralizationResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    sub_tag: Optional[str] = None


def check_f_packet_premature_generalization(
    *,
    lessons_proposed: Iterable[Any],
    operator_sp0_grant: bool = False,
) -> PrematureGeneralizationResult:
    """PRE-emission: lessons with frequency==1 require severity==HIGH."""
    violations: list[str] = []
    for i, lesson in enumerate(lessons_proposed):
        freq = getattr(lesson, "frequency", None)
        sev = getattr(lesson, "severity", None)
        lid = getattr(lesson, "lesson_id", f"<index {i}>")
        if freq == 1 and sev != "HIGH":
            violations.append(f"{lid!r}")
    if violations and not operator_sp0_grant:
        return PrematureGeneralizationResult(
            success=False,
            failure_code=F_PACKET_PREMATURE_GENERALIZATION,
            sub_tag="frequency_one_no_severity",
            detail=(
                f"lessons with frequency==1 require severity==HIGH: "
                f"{violations!r}"
            ),
        )
    if violations and operator_sp0_grant:
        # SP0 override path — admin-risk ledger entry expected upstream
        return PrematureGeneralizationResult(
            success=True,
            failure_code=None,
            detail=(
                f"operator SP0 grant relaxes premature-generalization rule "
                f"for {violations!r}; admin-risk ledger HIGH severity entry "
                f"expected"
            ),
        )
    return PrematureGeneralizationResult(
        success=True,
        failure_code=None,
        detail="no premature-generalization violations",
    )


predicate_premature_generalization = check_f_packet_premature_generalization


__all__ = [
    "F_PACKET_PREMATURE_GENERALIZATION",
    "PrematureGeneralizationResult",
    "check_f_packet_premature_generalization",
    "predicate_premature_generalization",
]
