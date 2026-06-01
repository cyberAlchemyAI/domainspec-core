"""tests/seats/editor/test_r2_validator.py — R2 §3.2 enhanced validation.

Spec card §3.2:
- Taxonomy sort audit — item in >1 category surfaces as NOTE.
- Tone consistency check — score_10 ∈ 0..10.
- Quick-wins deduplication — strip dupes; preserve first-seen order.
- Terms-to-verify cross-reference — orphan terms surface as NOTE.
"""

from __future__ import annotations

import pytest

from pipeline.seats.editor import (
    EditorGap,
    EditorOutput,
    EditorOutputShapeError,
    F_EDITOR_OUTPUT_SHAPE,
    FlaggedTerm,
    Miscategorization,
    ReadabilityFeedback,
    ReplacementOption,
    TAXONOMY_CATEGORIES,
    TaxonomyCheck,
    ToneFeedback,
    ValidationReport,
    apply_r2_validation,
    assert_tone_consistency,
    audit_taxonomy_sort,
    audit_terms_to_verify_cross_reference,
    dedupe_quick_wins,
)


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------


def _readability(score: int = 7) -> ReadabilityFeedback:
    return ReadabilityFeedback(
        score_10=score, grade_level_estimate="grade 11", verdict="GOOD"
    )


def _tone(score: int = 7) -> ToneFeedback:
    return ToneFeedback(
        overall_readability=_readability(score),
        key_message="msg",
        reviewer_fatigue_sections=(),
    )


def _flagged(*, excerpt: str = "vague", section_ref: str = "1.a") -> FlaggedTerm:
    return FlaggedTerm(
        section_ref=section_ref,
        issue_type="jargon",
        severity="low",
        excerpt=excerpt,
        why_it_hurts="vague",
        replacement_options=(
            ReplacementOption(label="A", text="a", note=""),
            ReplacementOption(label="B", text="b", note=""),
        ),
        rubric_connection="",
    )


def _make_output(
    *,
    flagged_terms: tuple[FlaggedTerm, ...] = (),
    quick_wins: tuple[str, ...] = (),
    terms_to_verify: tuple[str, ...] = (),
    taxonomy: TaxonomyCheck | None = None,
    tone: ToneFeedback | None = None,
) -> EditorOutput:
    return EditorOutput(
        flagged_terms=flagged_terms,
        taxonomy_check=taxonomy
        or TaxonomyCheck(
            goals_identified=(),
            outputs_identified=(),
            outcomes_identified=(),
            objectives_identified=(),
            miscategorizations=(),
        ),
        tone_feedback=tone or _tone(),
        quick_wins=quick_wins,
        terms_to_verify=terms_to_verify,
        gaps=(),
    )


# ---------------------------------------------------------------------------
# Constants surface
# ---------------------------------------------------------------------------


class TestConstants:
    def test_taxonomy_categories_pinned(self):
        assert TAXONOMY_CATEGORIES == (
            "goals",
            "outputs",
            "outcomes",
            "objectives",
        )


# ---------------------------------------------------------------------------
# audit_taxonomy_sort
# ---------------------------------------------------------------------------


class TestAuditTaxonomySort:
    def test_no_duplicates_returns_empty(self):
        tx = TaxonomyCheck(
            goals_identified=("reduce energy costs",),
            outputs_identified=("install array",),
            outcomes_identified=("80% reduction",),
            objectives_identified=("7-year payback",),
            miscategorizations=(),
        )
        out = _make_output(taxonomy=tx)
        assert audit_taxonomy_sort(out) == ()

    def test_item_in_two_categories_flagged(self):
        tx = TaxonomyCheck(
            goals_identified=("install array",),
            outputs_identified=("install array",),
            outcomes_identified=(),
            objectives_identified=(),
            miscategorizations=(),
        )
        out = _make_output(taxonomy=tx)
        assert audit_taxonomy_sort(out) == ("install array",)

    def test_item_in_three_categories_flagged_once(self):
        tx = TaxonomyCheck(
            goals_identified=("X",),
            outputs_identified=("X",),
            outcomes_identified=("X",),
            objectives_identified=(),
            miscategorizations=(),
        )
        out = _make_output(taxonomy=tx)
        assert audit_taxonomy_sort(out) == ("X",)

    def test_multiple_duplicates_alphabetized(self):
        tx = TaxonomyCheck(
            goals_identified=("Z-item", "A-item"),
            outputs_identified=("Z-item", "A-item"),
            outcomes_identified=(),
            objectives_identified=(),
            miscategorizations=(),
        )
        out = _make_output(taxonomy=tx)
        assert audit_taxonomy_sort(out) == ("A-item", "Z-item")

    def test_empty_categories_returns_empty(self):
        out = _make_output()
        assert audit_taxonomy_sort(out) == ()

    def test_rejects_non_editor_output(self):
        with pytest.raises(EditorOutputShapeError):
            audit_taxonomy_sort("not-output")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# assert_tone_consistency
# ---------------------------------------------------------------------------


class TestAssertToneConsistency:
    def test_passes_in_range(self):
        for score in (0, 5, 10):
            out = _make_output(tone=_tone(score))
            assert_tone_consistency(out)  # no raise

    def test_rejects_non_editor_output(self):
        with pytest.raises(EditorOutputShapeError):
            assert_tone_consistency("not-output")  # type: ignore[arg-type]

    def test_score_below_zero_caught_at_construction(self):
        # Defense-in-depth: __post_init__ already rejects, so we cannot
        # construct an invalid EditorOutput. The test verifies the
        # validator's defensive code path is reachable via direct attribute
        # bypass (object.__setattr__ on the inner readability).
        out = _make_output(tone=_tone(5))
        # Bypass freeze on the leaf; assert validator catches the drift.
        object.__setattr__(out.tone_feedback.overall_readability, "score_10", -1)
        with pytest.raises(EditorOutputShapeError, match=F_EDITOR_OUTPUT_SHAPE):
            assert_tone_consistency(out)

    def test_score_above_ten_caught_via_bypass(self):
        out = _make_output(tone=_tone(5))
        object.__setattr__(out.tone_feedback.overall_readability, "score_10", 11)
        with pytest.raises(EditorOutputShapeError):
            assert_tone_consistency(out)


# ---------------------------------------------------------------------------
# dedupe_quick_wins
# ---------------------------------------------------------------------------


class TestDedupeQuickWins:
    def test_no_duplicates_returns_identity(self):
        out = _make_output(quick_wins=("a", "b", "c"))
        deduped, removed = dedupe_quick_wins(out)
        assert deduped is out
        assert removed == 0

    def test_duplicates_stripped_first_seen_order(self):
        out = _make_output(quick_wins=("a", "b", "a", "c", "b"))
        deduped, removed = dedupe_quick_wins(out)
        assert deduped is not out
        assert deduped.quick_wins == ("a", "b", "c")
        assert removed == 2

    def test_all_unique_after_dedup(self):
        out = _make_output(quick_wins=("x", "x", "x"))
        deduped, removed = dedupe_quick_wins(out)
        assert deduped.quick_wins == ("x",)
        assert removed == 2

    def test_empty_quick_wins(self):
        out = _make_output(quick_wins=())
        deduped, removed = dedupe_quick_wins(out)
        assert deduped is out
        assert removed == 0

    def test_case_sensitive_dedup(self):
        out = _make_output(quick_wins=("Drop hedge", "drop hedge", "Drop hedge"))
        deduped, removed = dedupe_quick_wins(out)
        # "Drop hedge" appears twice → 1 dupe stripped; "drop hedge" stays.
        assert deduped.quick_wins == ("Drop hedge", "drop hedge")
        assert removed == 1

    def test_preserves_other_fields(self):
        ft = _flagged()
        gap = EditorGap(
            section_ref="1.a", issue="missing", action_needed="add"
        )
        misc = Miscategorization(
            excerpt="x", stated_as="goal", should_be="output", why="z"
        )
        tx = TaxonomyCheck(
            goals_identified=("g",),
            outputs_identified=(),
            outcomes_identified=(),
            objectives_identified=(),
            miscategorizations=(misc,),
        )
        out = EditorOutput(
            flagged_terms=(ft,),
            taxonomy_check=tx,
            tone_feedback=_tone(),
            quick_wins=("x", "x"),
            terms_to_verify=("term1",),
            gaps=(gap,),
        )
        deduped, removed = dedupe_quick_wins(out)
        assert removed == 1
        assert deduped.flagged_terms == (ft,)
        assert deduped.taxonomy_check is tx
        assert deduped.terms_to_verify == ("term1",)
        assert deduped.gaps == (gap,)

    def test_rejects_non_editor_output(self):
        with pytest.raises(EditorOutputShapeError):
            dedupe_quick_wins("not-output")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# audit_terms_to_verify_cross_reference
# ---------------------------------------------------------------------------


class TestTermsCrossReference:
    def test_term_in_excerpt_not_orphan(self):
        ft = _flagged(excerpt="we use mycoremediation here")
        out = _make_output(flagged_terms=(ft,), terms_to_verify=("mycoremediation",))
        assert audit_terms_to_verify_cross_reference(out) == ()

    def test_term_not_in_any_excerpt_is_orphan(self):
        ft = _flagged(excerpt="utilizes")
        out = _make_output(
            flagged_terms=(ft,), terms_to_verify=("regenerative",)
        )
        assert audit_terms_to_verify_cross_reference(out) == ("regenerative",)

    def test_multiple_orphans_preserve_input_order(self):
        ft = _flagged(excerpt="utilizes")
        out = _make_output(
            flagged_terms=(ft,),
            terms_to_verify=("zeta", "alpha", "beta"),
        )
        assert audit_terms_to_verify_cross_reference(out) == (
            "zeta",
            "alpha",
            "beta",
        )

    def test_empty_terms_returns_empty(self):
        out = _make_output(flagged_terms=(_flagged(),), terms_to_verify=())
        assert audit_terms_to_verify_cross_reference(out) == ()

    def test_empty_terms_with_no_flagged_returns_empty(self):
        out = _make_output()
        assert audit_terms_to_verify_cross_reference(out) == ()

    def test_empty_string_term_skipped(self):
        ft = _flagged(excerpt="something")
        # Empty term is a degenerate case that would substring-match anything;
        # the validator skips empty terms rather than reporting them.
        # We can't construct an EditorOutput with an empty terms_to_verify
        # entry (post_init rejects), so we bypass the freeze for this test.
        out = _make_output(flagged_terms=(ft,), terms_to_verify=("alpha",))
        # Confirm the surface skips empties via direct call: insert empty
        # via object.__setattr__.
        object.__setattr__(out, "terms_to_verify", ("", "alpha"))
        result = audit_terms_to_verify_cross_reference(out)
        # "alpha" not in "something" → orphan; empty skipped.
        assert result == ("alpha",)

    def test_substring_match_partial_excerpt(self):
        ft = _flagged(excerpt="our utilizes-heavy paragraph")
        out = _make_output(flagged_terms=(ft,), terms_to_verify=("utilizes",))
        # "utilizes" is a substring of "utilizes-heavy"
        assert audit_terms_to_verify_cross_reference(out) == ()

    def test_rejects_non_editor_output(self):
        with pytest.raises(EditorOutputShapeError):
            audit_terms_to_verify_cross_reference("not-output")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# apply_r2_validation — orchestrator
# ---------------------------------------------------------------------------


class TestApplyR2Validation:
    def test_clean_output_returns_identity(self):
        out = _make_output(quick_wins=("a", "b"), terms_to_verify=())
        deduped, report = apply_r2_validation(out)
        assert deduped is out
        assert isinstance(report, ValidationReport)
        assert report.taxonomy_duplicates == ()
        assert report.term_orphans == ()
        assert report.quick_wins_deduplicated == 0

    def test_dirty_output_dedups_and_reports(self):
        ft = _flagged(excerpt="utilizes")
        tx = TaxonomyCheck(
            goals_identified=("X",),
            outputs_identified=("X",),
            outcomes_identified=(),
            objectives_identified=(),
            miscategorizations=(),
        )
        out = _make_output(
            flagged_terms=(ft,),
            taxonomy=tx,
            quick_wins=("a", "a", "b"),
            terms_to_verify=("orphan",),
        )
        deduped, report = apply_r2_validation(out)
        assert deduped is not out
        assert deduped.quick_wins == ("a", "b")
        assert report.taxonomy_duplicates == ("X",)
        assert report.term_orphans == ("orphan",)
        assert report.quick_wins_deduplicated == 1

    def test_score_drift_caught_first(self):
        out = _make_output()
        object.__setattr__(out.tone_feedback.overall_readability, "score_10", 99)
        with pytest.raises(EditorOutputShapeError):
            apply_r2_validation(out)


# ---------------------------------------------------------------------------
# ValidationReport shape
# ---------------------------------------------------------------------------


class TestValidationReport:
    def test_constructible_with_full_set(self):
        r = ValidationReport(
            taxonomy_duplicates=("a",),
            term_orphans=("b",),
            quick_wins_deduplicated=2,
        )
        assert r.taxonomy_duplicates == ("a",)
        assert r.quick_wins_deduplicated == 2

    def test_rejects_non_tuple_dups(self):
        with pytest.raises(ValueError, match="taxonomy_duplicates"):
            ValidationReport(
                taxonomy_duplicates=["a"],  # type: ignore[arg-type]
                term_orphans=(),
                quick_wins_deduplicated=0,
            )

    def test_rejects_non_string_dup(self):
        with pytest.raises(ValueError, match="taxonomy_duplicates"):
            ValidationReport(
                taxonomy_duplicates=(123,),  # type: ignore[arg-type]
                term_orphans=(),
                quick_wins_deduplicated=0,
            )

    def test_rejects_non_tuple_orphans(self):
        with pytest.raises(ValueError, match="term_orphans"):
            ValidationReport(
                taxonomy_duplicates=(),
                term_orphans=["b"],  # type: ignore[arg-type]
                quick_wins_deduplicated=0,
            )

    def test_rejects_non_string_orphan(self):
        with pytest.raises(ValueError, match="term_orphans"):
            ValidationReport(
                taxonomy_duplicates=(),
                term_orphans=(42,),  # type: ignore[arg-type]
                quick_wins_deduplicated=0,
            )

    def test_rejects_negative_dedup_count(self):
        with pytest.raises(ValueError, match="quick_wins_deduplicated"):
            ValidationReport(
                taxonomy_duplicates=(),
                term_orphans=(),
                quick_wins_deduplicated=-1,
            )

    def test_rejects_bool_count(self):
        with pytest.raises(ValueError, match="quick_wins_deduplicated"):
            ValidationReport(
                taxonomy_duplicates=(),
                term_orphans=(),
                quick_wins_deduplicated=True,  # type: ignore[arg-type]
            )
