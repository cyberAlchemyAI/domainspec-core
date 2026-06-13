"""Integration tests — all 4 runtime seats wired off a single CIC×CLC pair.

Per architecture v7.0.13 §1 (Card Runtime Wiring Amendment — DRAFT) +
blueprint §18.16.B. Verifies the full v0.2 first wave wiring chain:

  build_card_runtime_context()
      ↓
  CardRuntimeContext (cic + clc parsed cards)
      ↓
  build_{scout,scribe,editor,judge}_card_view()
      ↓
  per-seat behavioral context

The fixture pair is the canonical Phase A v7.0.11 LOCK pair —
food_systems CIC + operating_capacity CLC.
"""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CIC_PATH = REPO_ROOT / "pipeline" / "cards" / "CIC" / "food_systems.yaml"
CLC_PATH = REPO_ROOT / "pipeline" / "cards" / "CLC" / "operating_capacity.yaml"


def test_full_v02_first_wave_wiring_chain_food_systems_x_operating_capacity():
    """Loader → CardRuntimeContext → 4 seat views, all from a single pair."""

    from pipeline.cards.runtime_context import build_card_runtime_context
    from pipeline.scout.card_wiring import build_scout_card_view
    from pipeline.seats.scribe.card_wiring import build_scribe_card_view
    from pipeline.seats.editor.card_wiring import build_editor_card_view
    from pipeline.seats.judge.card_wiring import build_judge_card_view

    ctx = build_card_runtime_context(
        cic_path=str(CIC_PATH),
        clc_path=str(CLC_PATH),
        environment="production",
    )

    scout_view = build_scout_card_view(ctx)
    scribe_view = build_scribe_card_view(ctx)
    editor_view = build_editor_card_view(ctx)
    judge_view = build_judge_card_view(ctx)

    # Every view sees the same active CIC × CLC pair.
    for view in (scout_view, scribe_view, editor_view, judge_view):
        assert view.cic_slug == "food_systems"
        assert view.clc_slug == "operating_capacity"

    # Each seat surfaces the fields its dependency declaration claims.
    assert scout_view.search_vocabulary  # Scout reads search_vocabulary
    assert scribe_view.register_defaults  # Scribe reads register_defaults
    assert editor_view.common_red_flags  # Editor reads CLC red flags
    assert judge_view.underwriting_criteria  # Judge reads CLC underwriting


def test_shared_field_consistency_across_seats():
    """Fields read by multiple seats must come from the same card body —
    confirms each seat's view is a pure projection of the same context."""

    from pipeline.cards.runtime_context import build_card_runtime_context
    from pipeline.seats.scribe.card_wiring import build_scribe_card_view
    from pipeline.seats.editor.card_wiring import build_editor_card_view

    ctx = build_card_runtime_context(
        cic_path=str(CIC_PATH),
        clc_path=str(CLC_PATH),
        environment="production",
    )

    scribe_view = build_scribe_card_view(ctx)
    editor_view = build_editor_card_view(ctx)

    # Scribe + Editor both read CIC register_defaults — must be identical.
    assert scribe_view.register_defaults == editor_view.register_defaults
    # Scribe + Editor both read CIC admin_risk_term_register — must match.
    assert scribe_view.admin_risk_term_register == editor_view.admin_risk_term_register
    # Scribe + Editor both read CIC dialect_routing_table — must match.
    assert scribe_view.dialect_routing_table == editor_view.dialect_routing_table


def test_judge_and_scout_share_underwriting_criteria_field():
    """Scout (funder-side classification) and Judge (rubric scoring) both
    read CLC underwriting_criteria — same source."""

    from pipeline.cards.runtime_context import build_card_runtime_context
    from pipeline.scout.card_wiring import build_scout_card_view
    from pipeline.seats.judge.card_wiring import build_judge_card_view

    ctx = build_card_runtime_context(
        cic_path=str(CIC_PATH),
        clc_path=str(CLC_PATH),
        environment="production",
    )
    scout_view = build_scout_card_view(ctx)
    judge_view = build_judge_card_view(ctx)
    assert scout_view.underwriting_criteria == judge_view.underwriting_criteria


def test_loaded_card_runtime_registered_seats_matches_view_consumers():
    """The loader's runtime_registered_seats roster must include exactly the
    seats whose views build successfully without ValueError or missing data."""

    from pipeline.cards.loader import load_card
    from pipeline.cards.runtime_context import build_card_runtime_context
    from pipeline.scout.card_wiring import build_scout_card_view
    from pipeline.seats.scribe.card_wiring import build_scribe_card_view
    from pipeline.seats.editor.card_wiring import build_editor_card_view
    from pipeline.seats.judge.card_wiring import build_judge_card_view

    cic_loaded = load_card(path=str(CIC_PATH), environment="production")
    clc_loaded = load_card(path=str(CLC_PATH), environment="production")

    # The four v0.2 first wave runtime seats must appear in both axes.
    expected = {"Scout", "Scribe", "Editor", "Judge"}
    assert expected <= set(cic_loaded.runtime_registered_seats)
    assert expected <= set(clc_loaded.runtime_registered_seats)

    # And each view must build successfully from the corresponding context.
    ctx = build_card_runtime_context(
        cic_path=str(CIC_PATH),
        clc_path=str(CLC_PATH),
        environment="production",
    )
    assert build_scout_card_view(ctx) is not None
    assert build_scribe_card_view(ctx) is not None
    assert build_editor_card_view(ctx) is not None
    assert build_judge_card_view(ctx) is not None
