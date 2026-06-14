"""pipeline.scout.card_wiring — Scout per-card behavioral context.

Per architecture v7.0.13 §1 (Card Runtime Wiring Amendment — DRAFT) +
blueprint §18.16.B step 2 ("Inject CIC context into Scout"). Projects
the Scout-relevant subset of a :class:`CardRuntimeContext` into a frozen
:class:`ScoutCardView` consumed by Scout's DISCOVER + VERIFY stages.

Field roster mirrors ``SEAT_CARD_FIELD_DEPENDENCIES["Scout"]`` in
:mod:`pipeline.cards.seat_dependencies` — if a field is added or removed
there, this module's view must rev correspondingly.

What Scout reads from each axis:

  * **CIC (applicant side):**
      - ``search_vocabulary`` — core_terms + synonym_map +
        funder_program_keywords + disqualifier_terms; expands DISCOVER
        queries across channels A-F.
      - ``evidence_signals`` — applicant-side signal kinds Scout uses to
        screen candidates for early-stage fit.
      - ``kfr_fact_classes`` — applicant fact classes Scout cross-
        references against PROJECT_CONTEXT to surface gaps.
      - ``admin_risk_term_register`` — terms Scout flags in opportunity
        descriptions for downstream Law 4 review.

  * **CLC (funder side):**
      - ``underwriting_criteria`` — used at VERIFY stage to classify
        opportunity funding mechanism (which CLC the opportunity belongs
        to per architecture v7.0.11 §1.6 + §6.1 opportunity-driven match
        logic).

Note: Scout lives at ``pipeline/scout/`` (not under ``pipeline/seats/``)
for historical reasons — the run.py + discover.py + verify_stage.py +
review_stage.py composition pattern predates the seats/ subtree. The
card_wiring module sits alongside as a peer of run.py.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from pipeline.cards.runtime_context import CardRuntimeContext


@dataclass(frozen=True, kw_only=True, slots=True)
class ScoutCardView:
    """Scout-relevant projection of a :class:`CardRuntimeContext`."""

    # CIC-derived (applicant side)
    cic_slug: str
    search_vocabulary: Mapping[str, Any]
    evidence_signals: tuple[Mapping[str, Any], ...]
    kfr_fact_classes: tuple[Mapping[str, Any], ...]
    admin_risk_term_register: tuple[Mapping[str, Any], ...]

    # CLC-derived (funder side)
    clc_slug: str
    underwriting_criteria: tuple[Mapping[str, Any], ...]


def build_scout_card_view(context: CardRuntimeContext) -> ScoutCardView:
    """Project the Scout-relevant subset out of a CardRuntimeContext.

    Pure function; no side effects, no I/O.
    """

    cic = context.cic
    clc = context.clc
    return ScoutCardView(
        cic_slug=cic.slug,
        search_vocabulary=cic.search_vocabulary,
        evidence_signals=cic.evidence_signals,
        kfr_fact_classes=cic.kfr_fact_classes,
        admin_risk_term_register=cic.admin_risk_term_register,
        clc_slug=clc.slug,
        underwriting_criteria=clc.underwriting_criteria,
    )


__all__ = [
    "ScoutCardView",
    "build_scout_card_view",
]
