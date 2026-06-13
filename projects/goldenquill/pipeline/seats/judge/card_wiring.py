"""pipeline.seats.judge.card_wiring — Judge per-card behavioral context.

Per architecture v7.0.13 §1 (Card Runtime Wiring Amendment — DRAFT) +
blueprint §18.16.B step 4 ("Inject CLC underwriting into Judge"). Projects
the Judge-relevant subset of a :class:`CardRuntimeContext` into a frozen
:class:`JudgeCardView` consumed by Judge's rubric assembly.

Field roster mirrors ``SEAT_CARD_FIELD_DEPENDENCIES["Judge"]`` in
:mod:`pipeline.cards.seat_dependencies` — if a field is added or removed
there, this module's view must rev correspondingly.

What Judge reads from each axis:

  * **CIC (applicant side):**
      - ``capacity_signals_required`` — applicant-side signals Judge
        verifies the draft demonstrates (SAM.gov registration, key
        personnel identified, etc.).
      - ``compliance_burdens`` — applicable frameworks (2 CFR 200,
        program-specific regs); Judge checks the draft addresses each.

  * **CLC (funder side):**
      - ``underwriting_criteria`` — the actual evaluation rubric the
        funder uses; Judge scores against each criterion.
      - ``scoring_weight_patterns`` — qualitative weight tiers per
        criterion in typical funder rubrics; informs Judge's per-
        dimension scoring.
      - ``evidence_weights`` — kind-by-kind weight + rationale for
        evidence the funder cares most about.
      - ``reviewer_profile_typical`` — reviewer types + priorities +
        common-red-flags-from-reviewer-pov; informs Judge's adversarial
        scoring stance.
      - ``common_red_flags`` — funder-side red-flag probes Judge
        explicitly tests the draft against.

Judge's existing v1 envelope (``judge-envelope.v1``) is NOT modified at
this amendment; the card-context is injected at the rubric-assembly layer
upstream of the envelope.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from pipeline.cards.runtime_context import CardRuntimeContext


@dataclass(frozen=True, kw_only=True, slots=True)
class JudgeCardView:
    """Judge-relevant projection of a :class:`CardRuntimeContext`."""

    # CIC-derived (applicant side)
    cic_slug: str
    capacity_signals_required: tuple[Mapping[str, Any], ...]
    compliance_burdens: tuple[Mapping[str, Any], ...]

    # CLC-derived (funder side)
    clc_slug: str
    underwriting_criteria: tuple[Mapping[str, Any], ...]
    scoring_weight_patterns: tuple[Mapping[str, Any], ...]
    evidence_weights: Mapping[str, Any]
    reviewer_profile_typical: Mapping[str, Any]
    common_red_flags: tuple[Mapping[str, Any], ...]


def build_judge_card_view(context: CardRuntimeContext) -> JudgeCardView:
    """Project the Judge-relevant subset out of a CardRuntimeContext.

    Pure function; no side effects, no I/O.
    """

    cic = context.cic
    clc = context.clc
    return JudgeCardView(
        cic_slug=cic.slug,
        capacity_signals_required=cic.capacity_signals_required,
        compliance_burdens=cic.compliance_burdens,
        clc_slug=clc.slug,
        underwriting_criteria=clc.underwriting_criteria,
        scoring_weight_patterns=clc.scoring_weight_patterns,
        evidence_weights=clc.evidence_weights,
        reviewer_profile_typical=clc.reviewer_profile_typical,
        common_red_flags=clc.common_red_flags,
    )


__all__ = [
    "JudgeCardView",
    "build_judge_card_view",
]
