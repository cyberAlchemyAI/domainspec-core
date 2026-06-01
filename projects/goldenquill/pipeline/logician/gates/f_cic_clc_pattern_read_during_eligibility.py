"""F-CIC-CLC-PATTERN-READ-DURING-ELIGIBILITY — runtime read-path gate.

Per blueprint §4 v2.x card-hardening §4.X.1.8. Extends v7.0.8's existing
F-CIC-CLC-COUPLING-VIOLATION family — family prefix F-CIC-CLC-* (not F-CARDS-*)
preserves orthogonality-discipline ancestry per architecture v7.0.11 §1.6 #7.

Fires when Scout, Scribe, Judge, or eligibility-evaluation code attempts to
read matrix card fields or any historical-pattern field during opportunity
eligibility evaluation, fit gating, opportunity exclusion, or ranking
suppression.

Allowed reader during v1.x matrix phase: Archivist, retrospectively, via
explicit allowed_runtime_readers registry in matrix card bodies.

Possible future reader after explicit amendment: Match DB advisory layer, if
and only if result is labeled as non-binding suggestion in audit log AND
cannot suppress or exclude opportunities.

Predicate body graduates LIVE at v0.2 first wave (or earlier if v1.x matrix
phase begins).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Literal


GATE_ID: Final[str] = "F-CIC-CLC-PATTERN-READ-DURING-ELIGIBILITY"


ALLOWED_READERS_RETROSPECTIVE: Final[frozenset[str]] = frozenset({"Archivist"})

FORBIDDEN_READERS_DURING_ELIGIBILITY: Final[frozenset[str]] = frozenset({
    "Scout", "Scribe", "Judge", "Logician_as_evaluator",
})

ELIGIBILITY_READ_CONTEXTS: Final[frozenset[str]] = frozenset({
    "eligibility_evaluation",
    "fit_gating",
    "opportunity_ranking",
    "opportunity_exclusion",
})


@dataclass(frozen=True, kw_only=True)
class GateOutcome:
    passed: bool
    message: str


def evaluate(
    *,
    reader_identity: Literal["Scout", "Scribe", "Judge", "Logician_as_evaluator", "Archivist", "MatchDB"],
    read_context: Literal[
        "eligibility_evaluation", "fit_gating", "opportunity_ranking",
        "opportunity_exclusion", "retrospective_lesson",
    ],
    card_axis: Literal["CIC", "CLC", "MATRIX"],
    field_path: str,
) -> GateOutcome:
    """Evaluate the gate.

    DRAFT predicate body. Raises NotImplementedError until v0.2 first wave (or
    earlier if v1.x matrix phase begins). The constant sets ALLOWED_READERS_*
    and FORBIDDEN_READERS_* are LIVE at v7.0.11 LOCK.
    """

    raise NotImplementedError(
        f"{GATE_ID} predicate body graduates LIVE at v0.2 first wave (or earlier "
        f"if v1.x matrix phase begins) per architecture v7.0.11 §5."
    )
