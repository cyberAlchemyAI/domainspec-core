"""F-CLASS-NEW-FACT-UNCLASSIFIED — PRE per-cycle Intake INCREMENTAL gate.

Per architecture v7.0.7 §3.6 (incremental-classification fail-closed
default).

After white-glove Classification Review completes once at onboarding,
new facts continue to enter via Intake INCREMENTAL mode. Per §3.6 the
discipline is:

  1. Default to confidential — every new fact extracted by Intake
     INCREMENTAL is tagged ``class: confidential`` AND ``locked_by:
     pending_operator_review`` at write time.
  2. Operator review queue — newly-ingested facts surface for operator
     classification on next pass.
  3. Per-grant pre-flight check — before each grant cycle's Scout /
     Scribe sees the fact, the pipeline confirms operator-classified
     post-ingest. Unclassified facts STOP the cycle until reviewed.

This gate fires PRE per-cycle: it scans the per-cycle fact-consumption
manifest for any fact still tagged ``confidential`` AND
``pending_operator_review`` and fail-closes if any pipeline consumer
intends to read such a fact during the cycle.

Bypass: M13 (audited; admin-risk MEDIUM — operator must classify the
fact OR drop it from the cycle).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final, Optional, Sequence


F_CLASS_NEW_FACT_UNCLASSIFIED: Final[str] = "F-CLASS-NEW-FACT-UNCLASSIFIED"

PENDING_OPERATOR_REVIEW: Final[str] = "pending_operator_review"
CLASS_CONFIDENTIAL: Final[str] = "confidential"


@dataclass(frozen=True, kw_only=True)
class IncrementalFact:
    """One Intake INCREMENTAL-mode fact tagged at extraction time.

    `class_name` is the classification value persisted by Intake when
    it wrote the fact to the operator review queue. `locked_by` is the
    classification register lock indicator; an unreviewed fact carries
    `locked_by="pending_operator_review"` per §3.6 step 1.
    """

    fact_id: str
    class_name: str
    locked_by: str
    will_be_consumed_this_cycle: bool


@dataclass(frozen=True, kw_only=True)
class NewFactUnclassifiedResult:
    """Result of F-CLASS-NEW-FACT-UNCLASSIFIED check."""

    success: bool
    failure_code: Optional[str]
    detail: str
    blocked_fact_ids: tuple[str, ...] = field(default_factory=tuple)


def check_class_new_fact_unclassified(
    *,
    facts: Sequence[IncrementalFact],
) -> NewFactUnclassifiedResult:
    """PRE per-cycle: no pending-review fact may be consumed.

    Identifies facts that are simultaneously:

    * tagged ``class: confidential``,
    * locked by ``pending_operator_review``,
    * scheduled for cycle consumption,

    and fail-closes the cycle entry until operator classifies. Per §3.6
    step 4: a fact's class can only DROP (more sensitive → less) by
    explicit operator action; the gate never silently downgrades
    ``confidential`` to ``shareable``.

    Returns
    -------
    NewFactUnclassifiedResult. PASS when no consumed fact is in
    pending-review state. FAIL when any consumed fact still awaits
    operator classification.
    """
    blocked: list[str] = []
    for fact in facts:
        if not fact.will_be_consumed_this_cycle:
            continue
        if fact.class_name != CLASS_CONFIDENTIAL:
            continue
        if fact.locked_by != PENDING_OPERATOR_REVIEW:
            continue
        blocked.append(fact.fact_id)

    if blocked:
        return NewFactUnclassifiedResult(
            success=False,
            failure_code=F_CLASS_NEW_FACT_UNCLASSIFIED,
            detail=(
                f"{len(blocked)} Intake INCREMENTAL fact(s) still tagged "
                f"confidential + locked_by=pending_operator_review and "
                f"scheduled for cycle consumption: "
                f"{', '.join(blocked[:5])}"
                + (f" (+{len(blocked) - 5} more)" if len(blocked) > 5 else "")
                + " — fail-closed per §3.6; operator must classify before "
                "cycle proceeds (M13 audited bypass available)"
            ),
            blocked_fact_ids=tuple(blocked[:5]),
        )

    return NewFactUnclassifiedResult(
        success=True,
        failure_code=None,
        detail=(
            f"no pending-review facts among {len(facts)} cycle inputs; "
            "every consumed fact has been operator-classified post-ingest"
        ),
    )


__all__ = [
    "CLASS_CONFIDENTIAL",
    "F_CLASS_NEW_FACT_UNCLASSIFIED",
    "IncrementalFact",
    "NewFactUnclassifiedResult",
    "PENDING_OPERATOR_REVIEW",
    "check_class_new_fact_unclassified",
]
