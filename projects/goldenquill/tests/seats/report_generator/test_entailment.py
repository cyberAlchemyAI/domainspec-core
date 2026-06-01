"""Tests for ``pipeline.orchestrator.seats.report_generator._entailment``.

Per RT-1a closure (semantic entailment) + RT-C2-10 closure
(verbatim-or-paraphrase-flag contract). Deterministic-Python; no LLM.
"""
from __future__ import annotations

from decimal import Decimal

import pytest

from pipeline.orchestrator.seats.report_generator._entailment import (
    NarrativeEntailmentResult,
    NumericEntailmentResult,
    check_narrative_entailment,
    check_numeric_entailment,
)


class TestNumericEntailment:
    def test_decimal_exact_match_passes(self):
        r = check_numeric_entailment(claim_value=Decimal("50"), source_value=Decimal("50"))
        assert r.success
        assert "exact-Decimal-match" in r.detail

    def test_decimal_different_scales_equal(self):
        # Decimal("1.0") == Decimal("1.00") numerically
        r = check_numeric_entailment(claim_value=Decimal("1.0"), source_value=Decimal("1.00"))
        assert r.success

    def test_decimal_mismatch_fails(self):
        r = check_numeric_entailment(claim_value=Decimal("50"), source_value=Decimal("51"))
        assert not r.success
        assert "Decimal-mismatch" in r.detail

    def test_float_claim_raises(self):
        with pytest.raises(TypeError, match="float comparison"):
            check_numeric_entailment(claim_value=0.1, source_value=Decimal("0.1"))

    def test_float_source_raises(self):
        with pytest.raises(TypeError, match="float comparison"):
            check_numeric_entailment(claim_value=Decimal("0.1"), source_value=0.1)


class TestNarrativeEntailmentVerbatim:
    def test_exact_sentence_passes_verbatim(self):
        r = check_narrative_entailment(
            claim_text="The project delivered 50 workshops.",
            source_texts=(
                "In Q3 the project delivered 50 workshops to 200 farmers across PA.",
            ),
        )
        assert r.success
        assert r.path == "verbatim"
        assert r.matched_source_idx == 0

    def test_normalized_whitespace_match(self):
        r = check_narrative_entailment(
            claim_text="  the   project delivered   50 workshops  ",
            source_texts=("In Q3 the project delivered 50 workshops to farmers.",),
        )
        assert r.success
        assert r.path == "verbatim"

    def test_case_insensitive_match(self):
        r = check_narrative_entailment(
            claim_text="Project Delivered Workshops",
            source_texts=("the project delivered workshops in pa",),
        )
        assert r.success
        assert r.path == "verbatim"


class TestNarrativeEntailmentParaphraseFlag:
    def test_paraphrase_flag_bypasses_verbatim(self):
        r = check_narrative_entailment(
            claim_text="Adapted workshop format to virtual delivery.",
            source_texts=("Field notes: pivoted in-person to online due to weather.",),
            editor_approved_paraphrase=True,
        )
        assert r.success
        assert r.path == "editor_approved_paraphrase"


class TestNarrativeEntailmentNgramAdvisory:
    def test_high_overlap_ngram_advisory_passes(self):
        # Claim shares most content tokens with source but is not verbatim.
        r = check_narrative_entailment(
            claim_text="project delivered farmers workshops pennsylvania training",
            source_texts=(
                "the project delivered training workshops to farmers in pennsylvania",
            ),
        )
        # High overlap → advisory pass (above 0.6 threshold default)
        assert r.success
        assert r.path == "ngram_advisory_only"
        assert r.ngram_overlap_ratio >= 0.6

    def test_low_overlap_fails(self):
        r = check_narrative_entailment(
            claim_text="Pigs flew over the moon.",
            source_texts=("The project delivered workshops to farmers in PA.",),
        )
        assert not r.success
        assert r.path == "ngram_advisory_only"

    def test_empty_source_fails(self):
        r = check_narrative_entailment(
            claim_text="hello world",
            source_texts=(),
        )
        assert not r.success

    def test_empty_claim_after_normalization_fails(self):
        r = check_narrative_entailment(
            claim_text="...",
            source_texts=("In Q3 the project delivered 50 workshops.",),
        )
        assert not r.success


class TestNarrativeEntailmentResultDataclass:
    def test_frozen(self):
        r = NarrativeEntailmentResult(
            success=True,
            path="verbatim",
            matched_source_idx=0,
            ngram_overlap_ratio=1.0,
            detail="x",
        )
        with pytest.raises(Exception):
            r.success = False  # type: ignore[misc]
