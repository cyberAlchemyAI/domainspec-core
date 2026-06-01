"""F-LOGICIAN-FACT-NEEDED-REQUIRED — PRE on SP0 sign-out (HARD_BLOCK).

Per architecture v7.0.4 §3.2 (J-04 / RT-08 closure).

If a KFR fact tagged ``required_for_funder`` matches the current RFA
AND the fact is in NEEDED state at SP0 sign-out, the pipeline HALTS at
SP0 and cannot advance to KGIE. Operator must either fill the fact in
full schema OR remove the funder from the in-flight grant cycle.

Closes the silent-skip path where Scribe might draft against an
absent required fact (either fabricating or shipping a ``[NEEDED]``
token; the existing F-PRE-15 catches the ``[NEEDED]`` token but not
silent fabrication when Scribe rephrases around the gap).

Severity: HARD_BLOCK. No M13 bypass — the gate exists explicitly to
prevent fabrication-by-omission. Operator must resolve at the source
(populate the fact OR drop the funder).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final, Mapping, Optional, Sequence


F_LOGICIAN_FACT_NEEDED_REQUIRED: Final[str] = "F-LOGICIAN-FACT-NEEDED-REQUIRED"

# Canonical NEEDED-state markers per §3 SP0 surface.
NEEDED_STATUS_VALUES: Final[frozenset[str]] = frozenset({
    "NEEDED",
    "needed",
})


@dataclass(frozen=True, kw_only=True)
class NeededFactGap:
    """One NEEDED-state required-for-funder fact surfaced at SP0."""

    fact_id: str
    what: str
    required_for_funder: str


@dataclass(frozen=True, kw_only=True)
class FactNeededRequiredResult:
    """Result of F-LOGICIAN-FACT-NEEDED-REQUIRED check."""

    success: bool
    failure_code: Optional[str]
    detail: str
    gaps: tuple[NeededFactGap, ...] = ()

    # Stage-aware fields (Consulting Node Doctrine)
    has_findings: bool = False
    blocking: bool = True
    advisory_only: bool = False
    requires_handoff_disclosure: bool = False


def _is_needed(fact: Mapping[str, Any]) -> bool:
    status = fact.get("status")
    if isinstance(status, str) and status.strip() in NEEDED_STATUS_VALUES:
        return True
    return False


def _required_for_match(
    fact: Mapping[str, Any],
    rfa_funder_id: str,
) -> bool:
    raw = fact.get("required_for_funder")
    if isinstance(raw, str):
        return raw.strip() == rfa_funder_id
    if isinstance(raw, Sequence):
        return any(
            isinstance(item, str) and item.strip() == rfa_funder_id
            for item in raw
        )
    return False


from pipeline.logician.types import OutputType, GateStage, ArtifactType, FINAL_OR_SUBMISSION_STAGES

def check_fact_needed_required(
    *,
    kfr_facts: Sequence[Mapping[str, Any]],
    current_rfa_funder_id: str,
    output_type: OutputType = "FIT_FARMS_SUBMISSION_PACKET",
    stage: GateStage = "final_export_attempt",
    artifact_type: ArtifactType = "pdf",
) -> FactNeededRequiredResult:
    """PRE-SP0-sign-out gate: HARD_BLOCK on required-for-funder NEEDED facts.

    Parameters
    ----------
    kfr_facts
        Sequence of KFR fact entries (already-parsed YAML mappings).
        Each entry contributes a NEEDED gap iff its ``status`` is
        NEEDED AND its ``required_for_funder`` field includes the
        current RFA's funder_id.
    current_rfa_funder_id
        Identifier of the funder for the in-flight grant cycle. Empty
        / missing fail-closes — SP0 must run against a known funder.

    Returns
    -------
    FactNeededRequiredResult. Passes when zero NEEDED gaps match the
    current RFA. Fails (HARD_BLOCK) listing every offending fact.
    """
    funder_id = current_rfa_funder_id.strip()
    if not funder_id:
        return FactNeededRequiredResult(
            success=False,
            failure_code=F_LOGICIAN_FACT_NEEDED_REQUIRED,
            detail=(
                "current_rfa_funder_id empty — SP0 cannot sign out without "
                "a known funder_id (fail-closed)"
            ),
        )

    gaps: list[NeededFactGap] = []
    for fact in kfr_facts:
        if not isinstance(fact, Mapping):
            continue
        if not _is_needed(fact):
            continue
        if not _required_for_match(fact, funder_id):
            continue
        fact_id = str(fact.get("id", "")).strip() or "<unidentified>"
        what = str(fact.get("what", "")).strip()
        gaps.append(NeededFactGap(
            fact_id=fact_id,
            what=what,
            required_for_funder=funder_id,
        ))

    if gaps:
        gap_labels = ", ".join(
            f"{g.fact_id} ({g.what!r})" if g.what else g.fact_id
            for g in gaps
        )

        has_findings = True
        blocking = True
        advisory_only = False
        requires_handoff_disclosure = False

        if output_type == "THIRD_PARTY_DRAFT_DELIVERABLE":
            if stage not in FINAL_OR_SUBMISSION_STAGES:
                blocking = False
                advisory_only = True
                requires_handoff_disclosure = True
        else:
            # FIT_FARMS_SUBMISSION_PACKET
            if stage in ("draft_generation", "draft_review"):
                blocking = False
                advisory_only = True

        return FactNeededRequiredResult(
            success=False,
            failure_code=F_LOGICIAN_FACT_NEEDED_REQUIRED,
            detail=(
                f"{len(gaps)} required-for-funder fact(s) in NEEDED state "
                f"at SP0 sign-out for funder_id={funder_id!r}: {gap_labels} "
                f"— {'HARD_BLOCK' if blocking else 'ADVISORY (draft-permissive)'}"
            ),
            gaps=tuple(gaps),
            has_findings=has_findings,
            blocking=blocking,
            advisory_only=advisory_only,
            requires_handoff_disclosure=requires_handoff_disclosure,
        )

    return FactNeededRequiredResult(
        success=True,
        failure_code=None,
        detail=(
            f"no required-for-funder facts in NEEDED state for "
            f"funder_id={funder_id!r}"
        ),
        has_findings=False,
        blocking=False,
        advisory_only=False,
        requires_handoff_disclosure=False,
    )


__all__ = [
    "F_LOGICIAN_FACT_NEEDED_REQUIRED",
    "NEEDED_STATUS_VALUES",
    "FactNeededRequiredResult",
    "NeededFactGap",
    "check_fact_needed_required",
]
