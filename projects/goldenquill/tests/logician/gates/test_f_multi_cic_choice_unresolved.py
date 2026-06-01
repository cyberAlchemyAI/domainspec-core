"""Unit tests for F-MULTI-CIC-CHOICE-UNRESOLVED.

Per architecture v7.0.8 §4.3 + §7 (LOCKED 2026-05-08, Cycle-1 RT-04 fix).
"""

from __future__ import annotations

from pipeline.logician.gates.f_multi_cic_choice_unresolved import (
    GATE_ID,
    PRE_GATE_ORDER,
    SELECT_ONE_PRIMITIVES,
    run,
)


# ---------------------------------------------------------------------------
# Reader fixtures
# ---------------------------------------------------------------------------


def _primitives_reader(per_primitive: dict[str, dict[str, str]]):
    """Returns ``{cic_id: value}`` for each primitive."""

    def _r(cic_active: list[str], primitive_name: str) -> dict[str, str]:
        per_cic = per_primitive.get(primitive_name, {})
        return {cic: per_cic[cic] for cic in cic_active if cic in per_cic}

    return _r


def _override_reader(per_grant: dict[tuple[str, str, str], str | None]):
    def _r(org_slug: str, grant_id: str, primitive_name: str):
        return per_grant.get((org_slug, grant_id, primitive_name))

    return _r


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


def test_gate_id() -> None:
    assert GATE_ID == "F-MULTI-CIC-CHOICE-UNRESOLVED"


def test_pre_gate_order() -> None:
    assert PRE_GATE_ORDER == 6.7


def test_select_one_primitives_pinned() -> None:
    """v7.0.8 §7's primitive-to-mode mapping for select-one mode."""
    assert "language_register" in SELECT_ONE_PRIMITIVES
    assert "narrative_voice" in SELECT_ONE_PRIMITIVES
    assert "tone" in SELECT_ONE_PRIMITIVES


# ---------------------------------------------------------------------------
# Single-CIC org → no-op (gate inapplicable)
# ---------------------------------------------------------------------------


def test_single_cic_passes_silently() -> None:
    r = run(
        org_slug="solo",
        grant_id="g1",
        cic_active=["educator"],
        cic_primitives_reader=_primitives_reader({}),
        match_override_reader=_override_reader({}),
    )
    assert r.passed is True
    assert r.findings == ()


def test_empty_cic_passes_silently() -> None:
    """Empty cic_active is F-CIC-CLC-MATCH-NULL territory; this gate stays silent."""
    r = run(
        org_slug="empty",
        grant_id="g1",
        cic_active=[],
        cic_primitives_reader=_primitives_reader({}),
        match_override_reader=_override_reader({}),
    )
    assert r.passed is True


def test_invalid_cic_passes_silently() -> None:
    """Invalid CIC IDs are F-CIC-CLC-MATCH-NULL territory; no double-fire."""
    r = run(
        org_slug="bad",
        grant_id="g1",
        cic_active=["not_a_real_cic"],
        cic_primitives_reader=_primitives_reader({}),
        match_override_reader=_override_reader({}),
    )
    assert r.passed is True


# ---------------------------------------------------------------------------
# Multi-CIC, all primitives identical → pass
# ---------------------------------------------------------------------------


def test_multi_cic_identical_values_passes() -> None:
    r = run(
        org_slug="dual",
        grant_id="g1",
        cic_active=["educator", "food_systems"],
        cic_primitives_reader=_primitives_reader(
            {
                "language_register": {
                    "educator": "plainspoken",
                    "food_systems": "plainspoken",
                },
                "narrative_voice": {
                    "educator": "first_person",
                    "food_systems": "first_person",
                },
                "tone": {
                    "educator": "warm",
                    "food_systems": "warm",
                },
            }
        ),
        match_override_reader=_override_reader({}),
    )
    assert r.passed is True


# ---------------------------------------------------------------------------
# Multi-CIC, primitives differ, no override → fail
# ---------------------------------------------------------------------------


def test_multi_cic_differing_voice_no_override_fails() -> None:
    r = run(
        org_slug="dual",
        grant_id="g1",
        cic_active=["educator", "food_systems"],
        cic_primitives_reader=_primitives_reader(
            {
                "language_register": {
                    "educator": "academic_formal",
                    "food_systems": "agricultural_plainspoken",
                },
                "narrative_voice": {
                    "educator": "third_person",
                    "food_systems": "third_person",
                },
                "tone": {
                    "educator": "warm",
                    "food_systems": "warm",
                },
            }
        ),
        match_override_reader=_override_reader({}),
    )
    assert r.passed is False
    assert any(f.primitive_name == "language_register" for f in r.findings)


def test_multi_cic_all_three_primitives_differ_three_findings() -> None:
    r = run(
        org_slug="dual",
        grant_id="g1",
        cic_active=["educator", "cooperative"],
        cic_primitives_reader=_primitives_reader(
            {
                "language_register": {
                    "educator": "formal",
                    "cooperative": "casual",
                },
                "narrative_voice": {
                    "educator": "third_person",
                    "cooperative": "first_person_plural",
                },
                "tone": {
                    "educator": "neutral",
                    "cooperative": "warm",
                },
            }
        ),
        match_override_reader=_override_reader({}),
    )
    assert r.passed is False
    primitive_names = {f.primitive_name for f in r.findings}
    assert primitive_names == {"language_register", "narrative_voice", "tone"}


# ---------------------------------------------------------------------------
# Multi-CIC, primitives differ, override set → pass
# ---------------------------------------------------------------------------


def test_multi_cic_with_override_passes() -> None:
    r = run(
        org_slug="dual",
        grant_id="g1",
        cic_active=["educator", "food_systems"],
        cic_primitives_reader=_primitives_reader(
            {
                "language_register": {
                    "educator": "academic_formal",
                    "food_systems": "agricultural_plainspoken",
                },
                "narrative_voice": {
                    "educator": "third_person",
                    "food_systems": "third_person",
                },
                "tone": {
                    "educator": "warm",
                    "food_systems": "warm",
                },
            }
        ),
        match_override_reader=_override_reader(
            {("dual", "g1", "language_register"): "academic_formal"}
        ),
    )
    assert r.passed is True


def test_multi_cic_partial_override_partial_fail() -> None:
    """Override one of two unresolved primitives — the other still fails."""
    r = run(
        org_slug="dual",
        grant_id="g1",
        cic_active=["educator", "cooperative"],
        cic_primitives_reader=_primitives_reader(
            {
                "language_register": {
                    "educator": "formal",
                    "cooperative": "casual",
                },
                "narrative_voice": {
                    "educator": "third_person",
                    "cooperative": "first_person_plural",
                },
                "tone": {
                    "educator": "neutral",
                    "cooperative": "neutral",
                },
            }
        ),
        match_override_reader=_override_reader(
            {("dual", "g1", "language_register"): "formal"}
        ),
    )
    assert r.passed is False
    primitive_names = {f.primitive_name for f in r.findings}
    assert primitive_names == {"narrative_voice"}


def test_empty_string_override_treated_as_unset() -> None:
    """Empty-string override doesn't count as a resolution."""
    r = run(
        org_slug="dual",
        grant_id="g1",
        cic_active=["educator", "food_systems"],
        cic_primitives_reader=_primitives_reader(
            {
                "language_register": {
                    "educator": "formal",
                    "food_systems": "plainspoken",
                },
                "narrative_voice": {"educator": "x", "food_systems": "x"},
                "tone": {"educator": "x", "food_systems": "x"},
            }
        ),
        match_override_reader=_override_reader(
            {("dual", "g1", "language_register"): ""}
        ),
    )
    assert r.passed is False


# ---------------------------------------------------------------------------
# Detail field
# ---------------------------------------------------------------------------


def test_finding_detail_includes_match_overrides_path() -> None:
    """Detail must explain how to fix — operator needs the path."""
    r = run(
        org_slug="dual",
        grant_id="g1",
        cic_active=["educator", "cooperative"],
        cic_primitives_reader=_primitives_reader(
            {
                "language_register": {
                    "educator": "formal",
                    "cooperative": "casual",
                },
                "narrative_voice": {"educator": "x", "cooperative": "x"},
                "tone": {"educator": "x", "cooperative": "x"},
            }
        ),
        match_override_reader=_override_reader({}),
    )
    assert r.passed is False
    finding = next(f for f in r.findings if f.primitive_name == "language_register")
    assert "match_overrides" in finding.detail
    assert "PROJECT_CONTEXT" in finding.detail
