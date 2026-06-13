"""pipeline.seats.editor.card_wiring — Editor per-card behavioral context.

Per architecture v7.0.13 §1 (Card Runtime Wiring Amendment — DRAFT).
Editor's clarity review reads applicant-side voice/tone defaults +
admin-risk register from the active CIC and reviewer-pov red flags +
reviewer profile + section patterns from the active CLC. Projects the
Editor-relevant subset of a :class:`CardRuntimeContext` into a frozen
:class:`EditorCardView` consumed by Editor's prompt assembly.

Field roster mirrors ``SEAT_CARD_FIELD_DEPENDENCIES["Editor"]`` in
:mod:`pipeline.cards.seat_dependencies` — if a field is added or removed
there, this module's view must rev correspondingly.

What Editor reads from each axis:

  * **CIC (applicant side):**
      - ``register_defaults`` — voice / tone / narrative-register baseline
        the draft must match.
      - ``dialect_routing_table`` — confirms the draft's funder-dialect
        target aligns with the CIC's routing rules.
      - ``admin_risk_term_register`` — Editor flags occurrences of these
        terms in the draft for operator approval (no silent rewrites
        per Law 4).

  * **CLC (funder side):**
      - ``common_red_flags`` — adversarial-probe items the reviewer
        actively looks for; Editor calls them out as edit suggestions.
      - ``reviewer_profile_typical`` — reviewer types + priorities +
        common-red-flags-from-reviewer-pov; informs clarity edits.
      - ``narrative_section_patterns`` — typical section names + word
        counts; Editor checks each section against the funder's expected
        shape.

Editor's existing v1 envelope (``editor-envelope.v1``) is NOT modified at
this amendment; the card-context is injected at the prompt-assembly layer
upstream of the envelope.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from pipeline.cards.runtime_context import CardRuntimeContext


@dataclass(frozen=True, kw_only=True, slots=True)
class EditorCardView:
    """Editor-relevant projection of a :class:`CardRuntimeContext`."""

    # CIC-derived (applicant side)
    cic_slug: str
    register_defaults: Mapping[str, Any]
    dialect_routing_table: tuple[Mapping[str, Any], ...]
    admin_risk_term_register: tuple[Mapping[str, Any], ...]

    # CLC-derived (funder side)
    clc_slug: str
    common_red_flags: tuple[Mapping[str, Any], ...]
    reviewer_profile_typical: Mapping[str, Any]
    narrative_section_patterns: tuple[Mapping[str, Any], ...]


def build_editor_card_view(context: CardRuntimeContext) -> EditorCardView:
    """Project the Editor-relevant subset out of a CardRuntimeContext.

    Pure function; no side effects, no I/O.
    """

    cic = context.cic
    clc = context.clc
    return EditorCardView(
        cic_slug=cic.slug,
        register_defaults=cic.register_defaults,
        dialect_routing_table=cic.dialect_routing_table,
        admin_risk_term_register=cic.admin_risk_term_register,
        clc_slug=clc.slug,
        common_red_flags=clc.common_red_flags,
        reviewer_profile_typical=clc.reviewer_profile_typical,
        narrative_section_patterns=clc.narrative_section_patterns,
    )


__all__ = [
    "EditorCardView",
    "build_editor_card_view",
]
