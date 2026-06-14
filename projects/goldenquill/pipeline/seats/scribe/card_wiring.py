"""pipeline.seats.scribe.card_wiring — Scribe per-card behavioral context.

Per architecture v7.0.13 §1 (Card Runtime Wiring Amendment — DRAFT) +
blueprint §18.16.B step 3 ("Inject CIC/CLC context into Scribe"). Projects
the Scribe-relevant subset of a :class:`CardRuntimeContext` into a frozen
:class:`ScribeCardView` consumed by Scribe's prompt assembly.

Field roster mirrors ``SEAT_CARD_FIELD_DEPENDENCIES["Scribe"]`` in
:mod:`pipeline.cards.seat_dependencies` — if a field is added or removed
there, this module's view must rev correspondingly. The
``R-CARDS-SEAT-DEPS-DRIFT`` AST-lint rule (v0.2 second-wave) cross-checks
this contract.

What Scribe reads from each axis:

  * **CIC (applicant side):**
      - ``register_defaults`` — language register, narrative voice, tone,
        sub-registers; selects per-section dialect.
      - ``dialect_routing_table`` — funder-political-axis → Scribe-dialect
        mapping; drives Law 4 funder dialect code-switching.
      - ``admin_risk_term_register`` — flagged terms + severity +
        substitution candidates; Scribe surfaces flagged terms in
        ``AdminRiskFlag`` outputs for operator approval.
      - ``narrative_sections_typical`` — applicant-side baseline of
        sections the proposal is expected to cover.

  * **CLC (funder side):**
      - ``narrative_section_patterns`` — funder-side section names +
        typical word counts; Scribe aligns section ordering to the
        funder's rubric anatomy.
      - ``evidence_weights`` — which evidence kinds the funder weights
        most heavily; Scribe ensures the draft cites accordingly.
      - ``budget_structure_conventions`` — funder budget category
        conventions (direct cost categories, indirect treatment, match
        rules); Scribe drafts budget narrative against these.

Scribe's existing v1 envelope (``scribe-envelope.v1``) is NOT modified at
this amendment; the card-context is injected at the prompt-assembly layer
upstream of the envelope. v0.2 second-wave envelope rev (``scribe-envelope.v2``)
will carry the active CIC/CLC slugs explicitly for downstream audit; at
v0.2 first wave the wiring layer composes the prompt directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from pipeline.cards.runtime_context import CardRuntimeContext


@dataclass(frozen=True, kw_only=True, slots=True)
class ScribeCardView:
    """Scribe-relevant projection of a :class:`CardRuntimeContext`.

    Frozen + kw-only + slots per A12 mandate; rebind-resistant.
    """

    # CIC-derived (applicant side)
    cic_slug: str
    register_defaults: Mapping[str, Any]
    dialect_routing_table: tuple[Mapping[str, Any], ...]
    admin_risk_term_register: tuple[Mapping[str, Any], ...]
    narrative_sections_typical: tuple[str, ...]

    # CLC-derived (funder side)
    clc_slug: str
    narrative_section_patterns: tuple[Mapping[str, Any], ...]
    evidence_weights: Mapping[str, Any]
    budget_structure_conventions: Mapping[str, Any]


def build_scribe_card_view(context: CardRuntimeContext) -> ScribeCardView:
    """Project the Scribe-relevant subset out of a CardRuntimeContext.

    Pure function; no side effects, no I/O. The returned ScribeCardView
    is frozen and safe to retain across the prompt-assembly call chain.
    """

    cic = context.cic
    clc = context.clc
    return ScribeCardView(
        cic_slug=cic.slug,
        register_defaults=cic.register_defaults,
        dialect_routing_table=cic.dialect_routing_table,
        admin_risk_term_register=cic.admin_risk_term_register,
        narrative_sections_typical=cic.narrative_sections_typical,
        clc_slug=clc.slug,
        narrative_section_patterns=clc.narrative_section_patterns,
        evidence_weights=clc.evidence_weights,
        budget_structure_conventions=clc.budget_structure_conventions,
    )


__all__ = [
    "ScribeCardView",
    "build_scribe_card_view",
]
