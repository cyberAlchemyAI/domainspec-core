"""Regression tests for the v7.0.10 three-posture UX flip in
`pipeline.orchestrator.classification_review` + `pipeline.cli.tilth_review_classify`.

Per architecture v7.0.10 LOCKED 2026-05-11 §1.4 — Classification Review
step 3 + step 4 amended to add a deployment-level posture selection
(``selected_posture`` field; one of ``frontier_eligible`` /
``split_context_hybrid`` / ``local_only_sovereign``) alongside the per-field
4-class register. The signed register attests to BOTH per-field
classifications AND the selected posture.

These tests cover:

1. The exported posture constants + descriptions + display labels.
2. ``validate_posture`` accepts the three permitted postures.
3. ``validate_posture`` rejects the deprecated ``sanitized`` posture with
   a pointed error message naming v7.0.10.
4. ``validate_posture`` rejects unknown posture values.
5. The CLI surfaces the three-posture menu rendering.
6. ``InvalidPostureValue`` is a distinct exception class with the expected
   ``code`` attribute.
"""

from __future__ import annotations

import pytest

from pipeline.orchestrator.classification_review import (
    DEPRECATED_POSTURE_SANITIZED,
    InvalidPostureValue,
    PERMITTED_POSTURES,
    POSTURE_DESCRIPTIONS,
    POSTURE_DISPLAY_LABELS,
    POSTURE_FRONTIER_ELIGIBLE,
    POSTURE_LOCAL_ONLY_SOVEREIGN,
    POSTURE_SPLIT_CONTEXT_HYBRID,
    validate_posture,
)


# ---------------------------------------------------------------------------
# Posture vocabulary contract
# ---------------------------------------------------------------------------


def test_posture_constants_have_expected_values() -> None:
    assert POSTURE_FRONTIER_ELIGIBLE == "frontier_eligible"
    assert POSTURE_SPLIT_CONTEXT_HYBRID == "split_context_hybrid"
    assert POSTURE_LOCAL_ONLY_SOVEREIGN == "local_only_sovereign"


def test_permitted_postures_is_exactly_three() -> None:
    assert PERMITTED_POSTURES == frozenset(
        {
            POSTURE_FRONTIER_ELIGIBLE,
            POSTURE_SPLIT_CONTEXT_HYBRID,
            POSTURE_LOCAL_ONLY_SOVEREIGN,
        }
    )
    assert len(PERMITTED_POSTURES) == 3


def test_deprecated_sanitized_is_not_in_permitted() -> None:
    """The v7.0.7 'Sanitized' posture is deprecated; the constant is exported
    so callers can detect attempts to set the field to the legacy value."""
    assert DEPRECATED_POSTURE_SANITIZED == "sanitized"
    assert DEPRECATED_POSTURE_SANITIZED not in PERMITTED_POSTURES


def test_display_labels_match_customer_facing_v7_0_10_wording() -> None:
    assert POSTURE_DISPLAY_LABELS[POSTURE_FRONTIER_ELIGIBLE] == "Frontier-Eligible"
    assert (
        POSTURE_DISPLAY_LABELS[POSTURE_SPLIT_CONTEXT_HYBRID]
        == "Split-Context Hybrid"
    )
    assert (
        POSTURE_DISPLAY_LABELS[POSTURE_LOCAL_ONLY_SOVEREIGN]
        == "Local-Only / Sovereign"
    )


def test_descriptions_cover_all_three_postures() -> None:
    assert set(POSTURE_DESCRIPTIONS) == PERMITTED_POSTURES
    # Each description is a non-empty paragraph (rough sanity check).
    for value, description in POSTURE_DESCRIPTIONS.items():
        assert isinstance(description, str)
        assert len(description) > 50, (
            f"description for {value} is too short to be informative: "
            f"{description!r}"
        )


def test_local_only_description_mentions_under_validation() -> None:
    """v7.0.10 §1.1 — Local-Only posture carries an under-validation caveat."""
    description = POSTURE_DESCRIPTIONS[POSTURE_LOCAL_ONLY_SOVEREIGN]
    assert (
        "under validation" in description.lower()
        or "under-validation" in description.lower()
        or "performance-dependent" in description.lower()
    )


def test_split_context_description_mentions_no_slot_round_trip() -> None:
    """v7.0.10 §1.1 — Split-Context Hybrid explicitly says 'no opaque-slot round-trip'."""
    description = POSTURE_DESCRIPTIONS[POSTURE_SPLIT_CONTEXT_HYBRID]
    assert "no opaque-slot" in description.lower() or "no slot" in description.lower()


# ---------------------------------------------------------------------------
# validate_posture
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "posture",
    [
        POSTURE_FRONTIER_ELIGIBLE,
        POSTURE_SPLIT_CONTEXT_HYBRID,
        POSTURE_LOCAL_ONLY_SOVEREIGN,
    ],
)
def test_validate_posture_accepts_permitted_values(posture: str) -> None:
    assert validate_posture(posture) == posture


def test_validate_posture_accepts_none() -> None:
    """Legacy v7.0.7-era callers that pre-date posture selection pass None."""
    assert validate_posture(None) is None


def test_validate_posture_normalizes_whitespace_and_case() -> None:
    assert validate_posture("  Frontier_Eligible  ") == POSTURE_FRONTIER_ELIGIBLE
    assert (
        validate_posture("SPLIT_CONTEXT_HYBRID") == POSTURE_SPLIT_CONTEXT_HYBRID
    )


def test_validate_posture_rejects_deprecated_sanitized() -> None:
    """The deprecated v7.0.7 'sanitized' posture raises with a v7.0.10-naming error."""
    with pytest.raises(InvalidPostureValue) as exc_info:
        validate_posture("sanitized")
    message = str(exc_info.value)
    assert "DEPRECATED" in message
    assert "v7.0.10" in message
    assert "2026-05-11" in message
    # And it tells the operator the permitted values
    assert "frontier_eligible" in message
    assert "split_context_hybrid" in message
    assert "local_only_sovereign" in message


def test_validate_posture_rejects_unknown_value() -> None:
    with pytest.raises(InvalidPostureValue):
        validate_posture("aggressive_routing")


def test_validate_posture_rejects_non_string() -> None:
    with pytest.raises(InvalidPostureValue):
        validate_posture(42)  # type: ignore[arg-type]


def test_invalid_posture_value_has_failure_code_attribute() -> None:
    exc = InvalidPostureValue("test")
    assert exc.code == "F-CLASSIFICATION-REVIEW-INVALID-POSTURE"


# ---------------------------------------------------------------------------
# CLI posture menu rendering
# ---------------------------------------------------------------------------


def test_cli_render_posture_menu_lists_three_postures() -> None:
    """The CLI's posture-menu rendering surfaces all three postures (step 3)."""
    from pipeline.cli.tilth_review_classify import _render_posture_menu

    rendered = _render_posture_menu()
    assert "Frontier-Eligible" in rendered
    assert "Split-Context Hybrid" in rendered
    assert "Local-Only / Sovereign" in rendered
    # Includes the v7.0.10 deprecation footnote so operators see the
    # historical context inline.
    assert "Sanitized" in rendered
    assert "DEPRECATED" in rendered
    # Surfaces the under-validation notice for Local-Only.
    assert "under-validation" in rendered or "under validation" in rendered


def test_cli_render_posture_menu_includes_v7_0_10_authority_pointer() -> None:
    from pipeline.cli.tilth_review_classify import _render_posture_menu

    rendered = _render_posture_menu()
    assert "v7.0.10" in rendered or "§1.4" in rendered
