"""Tests for pipeline.cards.runtime_context — CardRuntimeContext + loader.

Per architecture v7.0.13 §1 (Card Runtime Wiring Amendment — DRAFT).
Verifies the v0.2 first wave wiring landing surfaces the active CIC + CLC
pair to the four runtime seats via the LIVE loader body and the
:class:`CardRuntimeContext` primitive.
"""

from __future__ import annotations

from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
CIC_PATH = REPO_ROOT / "pipeline" / "cards" / "CIC" / "food_systems.yaml"
CLC_PATH = REPO_ROOT / "pipeline" / "cards" / "CLC" / "operating_capacity.yaml"


def test_build_card_runtime_context_loads_cic_and_clc():
    from pipeline.cards.runtime_context import (
        CardRuntimeContext,
        build_card_runtime_context,
    )
    from pipeline.cards.models import CICCard, CLCCard

    ctx = build_card_runtime_context(
        cic_path=str(CIC_PATH),
        clc_path=str(CLC_PATH),
        environment="production",
    )
    assert isinstance(ctx, CardRuntimeContext)
    assert isinstance(ctx.cic, CICCard)
    assert isinstance(ctx.clc, CLCCard)
    assert ctx.cic.slug == "food_systems"
    assert ctx.clc.slug == "operating_capacity"
    assert ctx.cic_path.endswith("food_systems.yaml")
    assert ctx.clc_path.endswith("operating_capacity.yaml")


def test_card_runtime_context_is_frozen():
    """A12 mandate: CardRuntimeContext is frozen and rebind-resistant."""

    from pipeline.cards.runtime_context import build_card_runtime_context

    ctx = build_card_runtime_context(
        cic_path=str(CIC_PATH),
        clc_path=str(CLC_PATH),
        environment="production",
    )
    with pytest.raises(Exception):
        ctx.cic = None  # type: ignore[misc]


def test_card_runtime_context_rejects_swapped_axes():
    """The loader axis-detection upstream prevents the swap path, but the
    constructor still asserts the invariant for defense-in-depth."""

    from pipeline.cards.runtime_context import CardRuntimeContext
    from pipeline.cards.loader import load_card

    cic_loaded = load_card(path=str(CIC_PATH), environment="production")
    clc_loaded = load_card(path=str(CLC_PATH), environment="production")

    # Swap axes: this MUST raise.
    with pytest.raises(ValueError):
        CardRuntimeContext(
            cic=clc_loaded.card,  # type: ignore[arg-type]
            clc=cic_loaded.card,  # type: ignore[arg-type]
            cic_path=clc_loaded.card_path,
            clc_path=cic_loaded.card_path,
        )


def test_loaded_card_namespace_resolves_correctly():
    """The loader's namespace step (§1.9) produces the canonical
    ``cards:cic:<slug>`` / ``cards:clc:<slug>`` shape."""

    from pipeline.cards.loader import load_card

    cic_loaded = load_card(path=str(CIC_PATH), environment="production")
    clc_loaded = load_card(path=str(CLC_PATH), environment="production")

    assert cic_loaded.namespace == "cards:cic:food_systems"
    assert clc_loaded.namespace == "cards:clc:operating_capacity"


def test_loaded_card_runtime_registered_seats_includes_v02_first_wave_seats():
    """v0.2 first wave: Scout / Scribe / Editor / Judge all register as
    consuming seats for both CIC and CLC cards."""

    from pipeline.cards.loader import load_card

    cic_loaded = load_card(path=str(CIC_PATH), environment="production")
    for seat in ("Scout", "Scribe", "Editor", "Judge"):
        assert seat in cic_loaded.runtime_registered_seats, (
            f"{seat} expected in CIC runtime_registered_seats; got "
            f"{cic_loaded.runtime_registered_seats!r}"
        )

    clc_loaded = load_card(path=str(CLC_PATH), environment="production")
    for seat in ("Scout", "Scribe", "Editor", "Judge"):
        assert seat in clc_loaded.runtime_registered_seats, (
            f"{seat} expected in CLC runtime_registered_seats; got "
            f"{clc_loaded.runtime_registered_seats!r}"
        )


def test_loaded_card_canonical_hash_matches_lifecycle_content_hash():
    """The loader's canonical-bytes SHA-256 matches the lifecycle
    content_hash invariant verified during preflight."""

    from pipeline.cards.loader import load_card

    cic_loaded = load_card(path=str(CIC_PATH), environment="production")
    declared = cic_loaded.card.lifecycle.content_hash  # type: ignore[attr-defined]
    assert declared == f"sha256:{cic_loaded.canonical_bytes_sha256}"
