"""pipeline.seats.red_team.sfr_emitter — SFR three-block markdown emitter.

Per architecture §F.1 (A3 amendment, LOCKED v7 2026-04-19), every Red Team
verdict is serialized as a Semi-Formal Reasoning three-block certificate:

1. **Premises** — explicit facts + citations.
2. **Execution trace** — ordered steps citing premises by ID.
3. **Conclusion** — derives only from declared premises + trace.

The Logician's SFR parser (implemented by §6 Operating Envelope per A3) is
the canonical structural validator; this module is the *emitter* — it takes
a :class:`pipeline.seats.red_team.types.RedTeamVerdict` and produces the
markdown payload that the parser will consume.

R1 ships only the deterministic emitter (pure stdlib, no LLM, no network).
R3 wires the emitter into :mod:`pipeline.seats.red_team.seat` for subprocess
output assembly.

The emitter is line-oriented and parser-friendly: each block has a fixed
heading (``## Premises``, ``## Execution trace``, ``## Conclusion``); each
premise is ``- P{n}: {citation} — {fact}``; each step is
``- T{n}: {premise refs} → {inference}``. The conclusion carries
``recommendation:`` + ``total_score:`` + ``residuals:`` lines so the parser
can extract them deterministically.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from pipeline.seats.red_team.types import (
    RedTeamCriterionScore,
    RedTeamVerdict,
    Weakness,
)


# ---------------------------------------------------------------------------
# Block headings (V1 inline-literal pattern)
# ---------------------------------------------------------------------------

PREMISES_HEADING: Final[str] = "## Premises"
TRACE_HEADING: Final[str] = "## Execution trace"
CONCLUSION_HEADING: Final[str] = "## Conclusion"

assert PREMISES_HEADING == "## Premises", "PREMISES_HEADING rebound; refusing to load"
assert TRACE_HEADING == "## Execution trace", "TRACE_HEADING rebound; refusing to load"
assert CONCLUSION_HEADING == "## Conclusion", "CONCLUSION_HEADING rebound; refusing to load"


# ---------------------------------------------------------------------------
# Premise / Step shapes — internal-only (the emitter composes from
# RedTeamVerdict; callers never construct premises directly).
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class _Premise:
    """A single SFR premise. ID assigned 1-indexed at emission time."""

    citation: str  # e.g. "RUBRIC:need:medium" or "DRAFT:project_description:p3:abc1234..."
    fact: str  # human-readable premise body


@dataclass(frozen=True, kw_only=True, slots=True)
class _Step:
    """A single SFR execution-trace step. ID assigned 1-indexed at emission."""

    premise_refs: tuple[int, ...]  # 1-indexed P-IDs this step cites
    inference: str  # named inference rule + brief justification

    def __post_init__(self) -> None:
        if len(self.premise_refs) == 0:
            raise ValueError(
                "Step must reference at least one premise (floating reasoning "
                "is rejected by F-RT-VERDICT-CERT-MALFORMED.step_without_premise_reference)"
            )
        for ref in self.premise_refs:
            if not isinstance(ref, int) or ref < 1:
                raise ValueError(
                    f"premise_refs must be 1-indexed positive ints; got {ref!r}"
                )


# ---------------------------------------------------------------------------
# Emitter helpers
# ---------------------------------------------------------------------------


def _format_premise(idx: int, premise: _Premise) -> str:
    return f"- P{idx}: [{premise.citation}] — {premise.fact}"


def _format_step(idx: int, step: _Step) -> str:
    refs = ", ".join(f"P{r}" for r in step.premise_refs)
    return f"- T{idx}: ({refs}) → {step.inference}"


def _compose_premises_for_criterion(
    crit: RedTeamCriterionScore,
    rubric_id: str,
    section_pointer: str | None,
) -> tuple[_Premise, _Premise]:
    """Two premises per criterion: rubric-tier citation + draft-evidence citation."""
    p_rubric = _Premise(
        citation=f"RUBRIC:{rubric_id}:{crit.criterion_id}:{crit.tier_matched[:32]}",
        fact=f"{crit.criterion_name} tier-language: {crit.tier_matched}",
    )
    pointer = section_pointer or "DRAFT:section_unknown"
    p_evidence = _Premise(
        citation=f"{pointer}:{crit.criterion_id}",
        fact=f"Evidence cited for {crit.criterion_name}: {crit.evidence}",
    )
    return p_rubric, p_evidence


def _compose_step_for_criterion(
    crit: RedTeamCriterionScore,
    rubric_premise_id: int,
    evidence_premise_id: int,
) -> _Step:
    """One step per criterion: rubric + evidence ⇒ score."""
    return _Step(
        premise_refs=(rubric_premise_id, evidence_premise_id),
        inference=(
            f"by rubric-tier-language match + claim-without-evidence anti-pattern "
            f"⇒ {crit.criterion_id} = {crit.score}/{crit.max_points}"
        ),
    )


def _compose_premise_for_weakness(weakness: Weakness, idx: int) -> _Premise:
    return _Premise(
        citation=f"DRAFT:weakness_{idx}",
        fact=f"[{weakness.severity}] {weakness.claim}",
    )


def _compose_step_for_weakness(weakness_premise_id: int, weakness: Weakness) -> _Step:
    return _Step(
        premise_refs=(weakness_premise_id,),
        inference=(
            f"by reviewer-margin-comment anti-pattern ⇒ {weakness.what_a_reviewer_would_say}"
        ),
    )


# ---------------------------------------------------------------------------
# Public emitter
# ---------------------------------------------------------------------------


def emit_sfr_certificate(
    *,
    verdict: RedTeamVerdict,
    section_pointer_hint: str | None = None,
) -> str:
    """Compose the SFR three-block markdown for a :class:`RedTeamVerdict`.

    Args:
        verdict: the authoritative Red Team verdict.
        section_pointer_hint: optional draft-section pointer prefix (e.g.
            ``"DRAFT:project_description:p3:abc1234"``). When ``None``,
            the emitter uses the criterion_id-keyed default pointer.

    Returns:
        Markdown string with three line-oriented blocks.
    """
    premises: list[_Premise] = []
    steps: list[_Step] = []

    # Per-criterion: 2 premises (rubric tier + draft evidence) + 1 step (score).
    for crit in verdict.criteria:
        p_rubric, p_evidence = _compose_premises_for_criterion(
            crit=crit,
            rubric_id=verdict.rubric_id,
            section_pointer=section_pointer_hint,
        )
        premises.append(p_rubric)
        rubric_id_local = len(premises)
        premises.append(p_evidence)
        evidence_id_local = len(premises)
        steps.append(
            _compose_step_for_criterion(
                crit=crit,
                rubric_premise_id=rubric_id_local,
                evidence_premise_id=evidence_id_local,
            )
        )

    # Per-weakness: 1 premise (the cited claim) + 1 step (reviewer-margin inference).
    for weakness_idx, weakness in enumerate(verdict.attack_memo.top_weaknesses, start=1):
        p_weakness = _compose_premise_for_weakness(weakness, idx=weakness_idx)
        premises.append(p_weakness)
        weakness_premise_id = len(premises)
        steps.append(
            _compose_step_for_weakness(
                weakness_premise_id=weakness_premise_id, weakness=weakness
            )
        )

    # Conclusion derivation: cite total = sum-of-criteria-scores + recommendation
    # backed by attack_memo.overall_verdict.
    lines: list[str] = []
    lines.append(PREMISES_HEADING)
    lines.append("")
    for idx, premise in enumerate(premises, start=1):
        lines.append(_format_premise(idx, premise))
    lines.append("")
    lines.append(TRACE_HEADING)
    lines.append("")
    for idx, step in enumerate(steps, start=1):
        lines.append(_format_step(idx, step))
    lines.append("")
    lines.append(CONCLUSION_HEADING)
    lines.append("")
    lines.append(f"recommendation: {verdict.recommendation}")
    lines.append(f"total_score: {verdict.total_score}/{verdict.max_score}")
    lines.append("residuals:")
    for weakness_idx, weakness in enumerate(verdict.attack_memo.top_weaknesses, start=1):
        # Each residual cites a step (the per-weakness step). Step numbering:
        # criteria-steps come first (1..N_criteria), then weakness-steps
        # (N_criteria+1..N_criteria+N_weaknesses).
        step_id = len(verdict.criteria) + weakness_idx
        lines.append(f"  - T{step_id}: [{weakness.severity}] {weakness.claim}")
    lines.append("")
    lines.append(f"overall_verdict: {verdict.attack_memo.overall_verdict}")
    return "\n".join(lines)


def parse_recommendation_from_sfr(sfr_markdown: str) -> str | None:
    """Lightweight parser-side helper — extracts ``recommendation: <value>``.

    R1 helper for tests; R3's full SFR parser lives in §6 Operating Envelope.
    Returns ``None`` if the recommendation line is absent.
    """
    for line in sfr_markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("recommendation:"):
            value = stripped.split(":", 1)[1].strip()
            return value or None
    return None


def parse_total_score_from_sfr(sfr_markdown: str) -> tuple[int, int] | None:
    """Lightweight parser-side helper — extracts ``total_score: N/M``.

    Returns ``(N, M)`` or ``None`` if the line is absent or malformed.
    """
    for line in sfr_markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("total_score:"):
            value = stripped.split(":", 1)[1].strip()
            if "/" not in value:
                return None
            num_str, den_str = value.split("/", 1)
            try:
                return int(num_str), int(den_str)
            except ValueError:
                return None
    return None


__all__ = [
    "PREMISES_HEADING",
    "TRACE_HEADING",
    "CONCLUSION_HEADING",
    "emit_sfr_certificate",
    "parse_recommendation_from_sfr",
    "parse_total_score_from_sfr",
]
