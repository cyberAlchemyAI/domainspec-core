"""pipeline.cards.runtime_context — Card runtime context for seat injection.

Per architecture v7.0.13 §1 (Card Runtime Wiring Amendment — DRAFT, paired
with this commit). Lifts the v7.0.11 §5 v0.2-first-wave deferral of seat
runtime context injection (§18.16.B blueprint section). Cards now carry
behavioral semantics into Scout / Scribe / Judge / Editor at runtime via
the :class:`CardRuntimeContext` primitive defined here.

What this module provides:

  * :class:`CardRuntimeContext` — immutable pair-of-cards container holding
    one parsed :class:`CICCard` and one parsed :class:`CLCCard` plus the
    on-disk paths the cards were loaded from. Built once per cycle from
    the active applicant CIC + funder CLC pair.
  * :func:`build_card_runtime_context` — convenience constructor that
    loads both cards through the existing loader preflight (schema +
    lifecycle + coupling + manifest membership) and constructs the
    context.

Each consuming seat has a per-seat ``card_wiring.py`` module that projects
the relevant subset of card fields out of this context (see
``pipeline/seats/{scribe,editor,judge}/card_wiring.py`` and
``pipeline/scout/card_wiring.py``).

Discipline:

  * **Frozen, kw-only dataclass** — A12 mandate; rebind-resistance.
  * **No org-private data crossing into this module** — CardRuntimeContext
    carries workspace-shared card content only. Per-org data lives in
    PROJECT_CONTEXT / KFR; never injected here. F-CARDS-PRIVATE-DATA-IN-CARD
    fail-closes any attempt to populate confidential fields into a card.
  * **Single-track CLC only at v0.2 first wave landing.** Multi-track CLC
    (§18.6 v2 Option A track_a/track_b shape) graduates LIVE at v0.2
    second wave; current loader fails closed before reaching this module
    for multi-track CLCs.

This module is the architectural primitive blueprint §18.16.B step 1
("Add CardRuntimeContext object"). The seat-by-seat injection steps
(§18.16.B steps 2-5) live in the per-seat card_wiring.py modules.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from pipeline.cards.loader import load_card
from pipeline.cards.models import CICCard, CLCCard


@dataclass(frozen=True, kw_only=True, slots=True)
class CardRuntimeContext:
    """Active CIC + CLC card pair driving one cycle's seat behavior.

    Built once per cycle by :func:`build_card_runtime_context` from the
    operator-active CIC slug + funder-opportunity-derived CLC slug.
    Consumed by Scribe / Scout / Judge / Editor via their per-seat
    ``card_wiring.py`` modules.

    Per Law 3 (Org Isolation): a single ``CardRuntimeContext`` is
    bound to one cycle for one org. Cross-org reuse is structurally
    impossible because cards carry workspace-shared knowledge only
    (F-CARDS-PRIVATE-DATA-IN-CARD enforces no org binding at load
    time); the per-cycle runtime substrate is org-scoped elsewhere.
    """

    cic: CICCard
    clc: CLCCard
    cic_path: str
    clc_path: str

    def __post_init__(self) -> None:
        if self.cic.card_axis != "CIC":
            raise ValueError(
                f"CardRuntimeContext.cic must be a CIC card; got card_axis={self.cic.card_axis!r}"
            )
        if self.clc.card_axis != "CLC":
            raise ValueError(
                f"CardRuntimeContext.clc must be a CLC card; got card_axis={self.clc.card_axis!r}"
            )
        if not self.cic_path:
            raise ValueError("CardRuntimeContext.cic_path must be non-empty")
        if not self.clc_path:
            raise ValueError("CardRuntimeContext.clc_path must be non-empty")


def build_card_runtime_context(
    *,
    cic_path: str,
    clc_path: str,
    environment: str = "production",
    manifest_path: Optional[str] = None,
) -> CardRuntimeContext:
    """Load a CIC + CLC card pair via the loader and return a runtime context.

    Args:
        cic_path: Filesystem path to the CIC card YAML.
        clc_path: Filesystem path to the CLC card YAML.
        environment: "production" (full preflight including manifest gate)
            or "development" (skips manifest gate; cards still validate
            schema + lifecycle + coupling).
        manifest_path: Optional manifest override. Defaults to the resolved
            ``pipeline/cards/registry.yaml`` per the loader's standard
            resolution rule.

    Raises:
        Re-raises any preflight failure from :func:`pipeline.cards.loader.load_card`:
        :class:`CardSchemaError`, :class:`CardLifecycleError`,
        :class:`CardCouplingError`, or :class:`CardManifestMembershipError`.
        Raises :class:`ValueError` if the loaded cards do not match the
        expected axis at each slot.
    """

    cic_loaded = load_card(
        path=cic_path,
        environment=environment,  # type: ignore[arg-type]
        manifest_path=manifest_path,
    )
    clc_loaded = load_card(
        path=clc_path,
        environment=environment,  # type: ignore[arg-type]
        manifest_path=manifest_path,
    )

    cic_card = cic_loaded.card
    clc_card = clc_loaded.card
    if not isinstance(cic_card, CICCard):
        raise ValueError(
            f"build_card_runtime_context: cic_path={cic_path!r} did not load as CIC card; "
            f"got {type(cic_card).__name__}"
        )
    if not isinstance(clc_card, CLCCard):
        raise ValueError(
            f"build_card_runtime_context: clc_path={clc_path!r} did not load as CLC card; "
            f"got {type(clc_card).__name__}"
        )

    return CardRuntimeContext(
        cic=cic_card,
        clc=clc_card,
        cic_path=cic_loaded.card_path,
        clc_path=clc_loaded.card_path,
    )


__all__ = [
    "CardRuntimeContext",
    "build_card_runtime_context",
]
