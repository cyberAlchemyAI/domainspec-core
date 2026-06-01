"""Tests for pipeline.seats.scribe.dialect — §7.8 + §7.2 Law 5."""

from __future__ import annotations

import pytest

from pipeline.seats.scribe.dialect import (
    DIALECT_IDENTITY_PROXY_TABLE,
    DIALECT_VOCABULARY,
    detect_dialect_drift,
    detect_dialect_induced_identity,
    select_default_dialect,
)
from pipeline.seats.scribe.types import IdentityClaim


# ---------------------------------------------------------------------------
# DIALECT_VOCABULARY shape
# ---------------------------------------------------------------------------


class TestDialectVocabulary:
    def test_four_dialects(self) -> None:
        assert set(DIALECT_VOCABULARY.keys()) == {
            "conservative",
            "centrist",
            "progressive",
            "soul_fire",
        }

    def test_values_are_frozensets(self) -> None:
        for v in DIALECT_VOCABULARY.values():
            assert isinstance(v, frozenset)
            assert all(isinstance(p, str) and p.strip() for p in v)

    def test_no_phrase_overlap_between_dialects(self) -> None:
        pairs = [
            ("conservative", "centrist"),
            ("conservative", "progressive"),
            ("conservative", "soul_fire"),
            ("centrist", "progressive"),
            ("centrist", "soul_fire"),
            ("progressive", "soul_fire"),
        ]
        for a, b in pairs:
            intersect = DIALECT_VOCABULARY[a] & DIALECT_VOCABULARY[b]
            assert intersect == frozenset(), f"{a}∩{b} = {intersect!r}"


# ---------------------------------------------------------------------------
# detect_dialect_drift
# ---------------------------------------------------------------------------


class TestDetectDialectDrift:
    def test_pure_declared_dialect_no_drift(self) -> None:
        text = "Our focus is production efficiency and return on investment."
        assert detect_dialect_drift(text, "conservative") == ()

    def test_progressive_phrase_in_conservative_draft(self) -> None:
        text = (
            "Production efficiency drives our project, and we center equity "
            "in hiring."
        )
        drift = detect_dialect_drift(text, "conservative")
        assert "equity" in drift

    def test_case_insensitive_match(self) -> None:
        text = "Our focus is EQUITY and food sovereignty."
        drift = detect_dialect_drift(text, "conservative")
        assert "equity" in drift
        assert "food sovereignty" in drift

    def test_no_drift_in_empty_text(self) -> None:
        assert detect_dialect_drift("", "progressive") == ()

    def test_duplicate_phrases_deduped(self) -> None:
        text = "equity equity equity"
        drift = detect_dialect_drift(text, "conservative")
        assert drift.count("equity") == 1

    def test_soul_fire_phrase_in_centrist(self) -> None:
        text = "We center ancestral knowledge in our curriculum."
        drift = detect_dialect_drift(text, "centrist")
        assert "ancestral knowledge" in drift

    def test_declared_dialect_phrases_not_reported(self) -> None:
        text = "Equity is our guiding value and food sovereignty our mission."
        drift = detect_dialect_drift(text, "progressive")
        assert drift == ()

    def test_invalid_dialect_raises(self) -> None:
        with pytest.raises(ValueError, match="declared_dialect"):
            detect_dialect_drift("text", "bogus")  # type: ignore[arg-type]

    def test_non_string_returns_empty(self) -> None:
        assert detect_dialect_drift(None, "conservative") == ()  # type: ignore[arg-type]

    def test_document_order_across_dialects(self) -> None:
        # Phrases from multiple non-declared dialects should all appear.
        text = (
            "Our return on investment is strong, our community resilience "
            "is proven, and equity is non-negotiable."
        )
        drift = detect_dialect_drift(text, "soul_fire")
        assert set(drift) >= {"return on investment", "community resilience", "equity"}


# ---------------------------------------------------------------------------
# DIALECT_IDENTITY_PROXY_TABLE + detect_dialect_induced_identity
# ---------------------------------------------------------------------------


def _mk_claim(claim: str = "marginalized-community") -> IdentityClaim:
    return IdentityClaim(
        claim=claim,
        source_field_in_project_context="company.sda_status",
        rfa_priority_points=0,
    )


class TestDialectIdentityProxyTable:
    def test_conservative_and_centrist_are_empty(self) -> None:
        assert DIALECT_IDENTITY_PROXY_TABLE["conservative"] == {}
        assert DIALECT_IDENTITY_PROXY_TABLE["centrist"] == {}

    def test_progressive_entries_present(self) -> None:
        progressive = DIALECT_IDENTITY_PROXY_TABLE["progressive"]
        assert "historically marginalized" in progressive
        assert progressive["historically marginalized"] == "marginalized-community"

    def test_soul_fire_entries_present(self) -> None:
        sf = DIALECT_IDENTITY_PROXY_TABLE["soul_fire"]
        assert "ancestral knowledge" in sf
        assert sf["ancestral knowledge"] == "ancestral-knowledge"
        assert "indigenous knowledge" in sf
        assert sf["indigenous knowledge"] == "indigenous-practitioner"


class TestDetectDialectInducedIdentity:
    def test_no_proxy_no_violation(self) -> None:
        assert (
            detect_dialect_induced_identity("any text", "conservative", ()) == ()
        )

    def test_empty_text_no_violation(self) -> None:
        assert detect_dialect_induced_identity("", "progressive", ()) == ()

    def test_proxy_phrase_without_claim_is_violation(self) -> None:
        text = "We serve historically marginalized producers in our region."
        violations = detect_dialect_induced_identity(text, "progressive", ())
        assert violations == ("historically marginalized",)

    def test_proxy_phrase_with_matching_claim_cleared(self) -> None:
        text = "We serve historically marginalized producers in our region."
        claims = (_mk_claim("marginalized-community"),)
        violations = detect_dialect_induced_identity(text, "progressive", claims)
        assert violations == ()

    def test_soul_fire_grandmother_requires_ancestral_claim(self) -> None:
        text = "My grandmother taught me to farm with intention."
        violations = detect_dialect_induced_identity(text, "soul_fire", ())
        assert "my grandmother taught me" in violations

    def test_soul_fire_grandmother_cleared_by_ancestral_claim(self) -> None:
        text = "My grandmother taught me to farm."
        claims = (_mk_claim("ancestral-knowledge keeper"),)
        violations = detect_dialect_induced_identity(text, "soul_fire", claims)
        assert violations == ()

    def test_case_insensitive(self) -> None:
        text = "HISTORICALLY MARGINALIZED producers."
        violations = detect_dialect_induced_identity(text, "progressive", ())
        assert violations == ("historically marginalized",)

    def test_multiple_violations_collected(self) -> None:
        text = (
            "My grandmother taught me, and elder wisdom guides our work, "
            "with indigenous knowledge at the center."
        )
        violations = detect_dialect_induced_identity(text, "soul_fire", ())
        assert set(violations) >= {
            "my grandmother taught me",
            "elder wisdom",
            "indigenous knowledge",
        }

    def test_partial_claim_match_still_clears(self) -> None:
        # implied_label is substring of claim text → cleared
        text = "We are first-generation growers."
        claims = (_mk_claim("first-generation farmer household"),)
        violations = detect_dialect_induced_identity(text, "progressive", claims)
        assert violations == ()

    def test_invalid_dialect_raises(self) -> None:
        with pytest.raises(ValueError, match="declared_dialect"):
            detect_dialect_induced_identity("x", "bogus", ())  # type: ignore[arg-type]

    def test_non_string_returns_empty(self) -> None:
        assert detect_dialect_induced_identity(None, "progressive", ()) == ()  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# select_default_dialect
# ---------------------------------------------------------------------------


class TestSelectDefaultDialect:
    def test_returns_conservative(self) -> None:
        assert select_default_dialect() == "conservative"
