"""tests/seats/editor/test_types.py — R1 type-shape coverage.

Per spec card §7 (Test surface for §8 Editor R1+R2 combined):
- Every frozen dataclass constructible with the full documented field set.
- Closed-set Literals reject invalid values via __post_init__.
- 2-3 invariant on FlaggedTerm.replacement_options is **NOT** enforced at
  __post_init__ (validator-enforced per spec card §4 decision 5).
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from pipeline.seats.editor import (
    Dialect,
    EditorGap,
    EditorInput,
    EditorOutput,
    EditorSkillInvocation,
    FlaggedTerm,
    Miscategorization,
    ReadabilityFeedback,
    ReplacementOption,
    TaxonomyCheck,
    ToneFeedback,
)


UTC = timezone.utc


def _make_replacement(label: str = "A", text: str = "rewrite", note: str = "") -> ReplacementOption:
    return ReplacementOption(label=label, text=text, note=note)


def _make_flagged_term(
    *,
    replacement_options=None,
    section_ref: str = "1.a",
    issue_type: str = "jargon",
    severity: str = "medium",
    excerpt: str = "utilizes",
    why: str = "vague",
    rubric_connection: str = "",
) -> FlaggedTerm:
    if replacement_options is None:
        replacement_options = (_make_replacement("A"), _make_replacement("B"))
    return FlaggedTerm(
        section_ref=section_ref,
        issue_type=issue_type,  # type: ignore[arg-type]
        severity=severity,  # type: ignore[arg-type]
        excerpt=excerpt,
        why_it_hurts=why,
        replacement_options=replacement_options,
        rubric_connection=rubric_connection,
    )


def _make_readability(score_10: int = 7) -> ReadabilityFeedback:
    return ReadabilityFeedback(
        score_10=score_10, grade_level_estimate="grade 11", verdict="GOOD"
    )


def _make_tone(score_10: int = 7) -> ToneFeedback:
    return ToneFeedback(
        overall_readability=_make_readability(score_10=score_10),
        key_message="Plain summary",
        reviewer_fatigue_sections=(),
    )


def _make_taxonomy() -> TaxonomyCheck:
    return TaxonomyCheck(
        goals_identified=(),
        outputs_identified=(),
        outcomes_identified=(),
        objectives_identified=(),
        miscategorizations=(),
    )


def _make_editor_output(*, flagged_terms=None, quick_wins=()) -> EditorOutput:
    if flagged_terms is None:
        flagged_terms = (_make_flagged_term(),)
    return EditorOutput(
        flagged_terms=flagged_terms,
        taxonomy_check=_make_taxonomy(),
        tone_feedback=_make_tone(),
        quick_wins=quick_wins,
        terms_to_verify=(),
        gaps=(),
    )


def _make_editor_input(
    *, section_drafts=None, dialect: str = "centrist"
) -> EditorInput:
    if section_drafts is None:
        section_drafts = (
            {"section_name": "1.a", "section_order": 1, "body_text": "draft body."},
        )
    return EditorInput(
        section_drafts=section_drafts,
        rfa_excerpt="Rfa excerpt.",
        dialect=dialect,  # type: ignore[arg-type]
        session_id="sess-1",
        org_slug="mycosymbiotics",
    )


# ---------------------------------------------------------------------------
# ReplacementOption
# ---------------------------------------------------------------------------


class TestReplacementOption:
    def test_accepts_valid_label_text_note(self):
        opt = ReplacementOption(label="A", text="rewrite", note="strongest")
        assert opt.label == "A"
        assert opt.text == "rewrite"
        assert opt.note == "strongest"

    def test_rejects_invalid_label_d(self):
        with pytest.raises(ValueError, match="label"):
            ReplacementOption(label="D", text="x", note="")  # type: ignore[arg-type]

    def test_rejects_empty_text(self):
        with pytest.raises(ValueError, match="text"):
            ReplacementOption(label="A", text="", note="")

    def test_rejects_whitespace_only_text(self):
        with pytest.raises(ValueError, match="text"):
            ReplacementOption(label="A", text="   ", note="")

    def test_note_may_be_empty(self):
        opt = ReplacementOption(label="B", text="x", note="")
        assert opt.note == ""

    def test_note_must_be_string(self):
        with pytest.raises(ValueError, match="note"):
            ReplacementOption(label="A", text="x", note=123)  # type: ignore[arg-type]

    def test_frozen_field_rejects_setattr(self):
        from dataclasses import FrozenInstanceError

        opt = ReplacementOption(label="A", text="x", note="")
        with pytest.raises((FrozenInstanceError, AttributeError)):
            opt.label = "C"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# FlaggedTerm
# ---------------------------------------------------------------------------


class TestFlaggedTerm:
    def test_accepts_full_field_set(self):
        ft = _make_flagged_term(rubric_connection="op efficiency")
        assert ft.section_ref == "1.a"
        assert ft.issue_type == "jargon"
        assert ft.severity == "medium"
        assert len(ft.replacement_options) == 2

    def test_rejects_invalid_issue_type(self):
        with pytest.raises(ValueError, match="issue_type"):
            _make_flagged_term(issue_type="climate_nostalgia")

    def test_rejects_invalid_severity(self):
        with pytest.raises(ValueError, match="severity"):
            _make_flagged_term(severity="catastrophic")

    def test_rejects_empty_section_ref(self):
        with pytest.raises(ValueError, match="section_ref"):
            _make_flagged_term(section_ref="   ")

    def test_rejects_empty_excerpt(self):
        with pytest.raises(ValueError, match="excerpt"):
            _make_flagged_term(excerpt="")

    def test_rejects_empty_why(self):
        with pytest.raises(ValueError, match="why_it_hurts"):
            _make_flagged_term(why="   ")

    def test_admits_zero_replacement_options_for_validator_enforcement(self):
        # Spec card §4 decision 5 — validator enforces 2-3 invariant
        ft = _make_flagged_term(replacement_options=())
        assert len(ft.replacement_options) == 0

    def test_admits_four_replacement_options_for_validator_enforcement(self):
        opts = tuple(_make_replacement(lbl, f"text-{lbl}") for lbl in ("A", "B", "C"))
        opts = opts + (_make_replacement("A", "duplicate-label-allowed-at-shape"),)
        ft = _make_flagged_term(replacement_options=opts)
        assert len(ft.replacement_options) == 4

    def test_replacement_options_must_be_tuple(self):
        with pytest.raises(ValueError, match="replacement_options"):
            _make_flagged_term(replacement_options=[_make_replacement()])  # type: ignore[arg-type]

    def test_rubric_connection_must_be_string(self):
        with pytest.raises(ValueError, match="rubric_connection"):
            FlaggedTerm(
                section_ref="1.a",
                issue_type="jargon",
                severity="low",
                excerpt="x",
                why_it_hurts="y",
                replacement_options=(_make_replacement(), _make_replacement("B")),
                rubric_connection=None,  # type: ignore[arg-type]
            )


# ---------------------------------------------------------------------------
# Miscategorization + TaxonomyCheck
# ---------------------------------------------------------------------------


class TestMiscategorization:
    def test_accepts_full_set(self):
        m = Miscategorization(
            excerpt="Our goal is to install...",
            stated_as="goal",
            should_be="output",
            why="installation is a deliverable",
        )
        assert m.stated_as == "goal"

    @pytest.mark.parametrize(
        "field", ["excerpt", "stated_as", "should_be", "why"],
    )
    def test_rejects_empty_field(self, field: str):
        kwargs = dict(excerpt="x", stated_as="y", should_be="z", why="w")
        kwargs[field] = "   "
        with pytest.raises(ValueError, match=field):
            Miscategorization(**kwargs)


class TestTaxonomyCheck:
    def test_accepts_empty_categories(self):
        tx = _make_taxonomy()
        assert tx.goals_identified == ()

    def test_rejects_non_tuple_category(self):
        with pytest.raises(ValueError, match="goals_identified"):
            TaxonomyCheck(
                goals_identified=["g"],  # type: ignore[arg-type]
                outputs_identified=(),
                outcomes_identified=(),
                objectives_identified=(),
                miscategorizations=(),
            )

    def test_rejects_empty_string_in_category(self):
        with pytest.raises(ValueError, match="goals_identified"):
            TaxonomyCheck(
                goals_identified=("",),
                outputs_identified=(),
                outcomes_identified=(),
                objectives_identified=(),
                miscategorizations=(),
            )

    def test_miscategorizations_must_be_tuple(self):
        with pytest.raises(ValueError, match="miscategorizations"):
            TaxonomyCheck(
                goals_identified=(),
                outputs_identified=(),
                outcomes_identified=(),
                objectives_identified=(),
                miscategorizations=[],  # type: ignore[arg-type]
            )


# ---------------------------------------------------------------------------
# ReadabilityFeedback + ToneFeedback
# ---------------------------------------------------------------------------


class TestReadabilityFeedback:
    def test_accepts_score_in_range(self):
        r = _make_readability(7)
        assert r.score_10 == 7

    @pytest.mark.parametrize("score", [-1, 11, 100, 50])
    def test_rejects_score_out_of_range(self, score: int):
        with pytest.raises(ValueError, match="score_10"):
            _make_readability(score)

    def test_rejects_bool_score(self):
        with pytest.raises(ValueError, match="score_10"):
            ReadabilityFeedback(
                score_10=True,  # type: ignore[arg-type]
                grade_level_estimate="g",
                verdict="ok",
            )

    def test_requires_non_empty_grade_level_estimate(self):
        with pytest.raises(ValueError, match="grade_level_estimate"):
            ReadabilityFeedback(score_10=5, grade_level_estimate="", verdict="ok")

    def test_requires_non_empty_verdict(self):
        with pytest.raises(ValueError, match="verdict"):
            ReadabilityFeedback(score_10=5, grade_level_estimate="g", verdict=" ")


class TestToneFeedback:
    def test_accepts_full_set(self):
        t = _make_tone(8)
        assert t.overall_readability.score_10 == 8

    def test_rejects_non_readability(self):
        with pytest.raises(ValueError, match="overall_readability"):
            ToneFeedback(
                overall_readability="not-a-feedback",  # type: ignore[arg-type]
                key_message="x",
                reviewer_fatigue_sections=(),
            )

    def test_rejects_empty_key_message(self):
        with pytest.raises(ValueError, match="key_message"):
            ToneFeedback(
                overall_readability=_make_readability(),
                key_message=" ",
                reviewer_fatigue_sections=(),
            )

    def test_rejects_non_tuple_fatigue(self):
        with pytest.raises(ValueError, match="reviewer_fatigue_sections"):
            ToneFeedback(
                overall_readability=_make_readability(),
                key_message="x",
                reviewer_fatigue_sections=["section"],  # type: ignore[arg-type]
            )

    def test_rejects_empty_fatigue_entry(self):
        with pytest.raises(ValueError, match="reviewer_fatigue_sections"):
            ToneFeedback(
                overall_readability=_make_readability(),
                key_message="x",
                reviewer_fatigue_sections=("",),
            )


# ---------------------------------------------------------------------------
# EditorGap
# ---------------------------------------------------------------------------


class TestEditorGap:
    def test_accepts_full_set(self):
        g = EditorGap(
            section_ref="1.a", issue="missing data", action_needed="add metric"
        )
        assert g.action_needed == "add metric"

    @pytest.mark.parametrize("field", ["section_ref", "issue", "action_needed"])
    def test_rejects_empty_field(self, field: str):
        kwargs = dict(section_ref="s", issue="i", action_needed="a")
        kwargs[field] = "   "
        with pytest.raises(ValueError, match=field):
            EditorGap(**kwargs)


# ---------------------------------------------------------------------------
# EditorInput
# ---------------------------------------------------------------------------


class TestEditorInput:
    def test_accepts_minimal_full_set(self):
        inp = _make_editor_input()
        assert len(inp.section_drafts) == 1
        assert inp.dialect == "centrist"

    def test_rejects_empty_drafts(self):
        with pytest.raises(ValueError, match="section_drafts"):
            EditorInput(
                section_drafts=(),
                rfa_excerpt="",
                dialect="centrist",
                session_id="s",
                org_slug="o",
            )

    def test_rejects_non_tuple_drafts(self):
        with pytest.raises(ValueError, match="section_drafts"):
            EditorInput(
                section_drafts=[  # type: ignore[arg-type]
                    {"section_name": "x", "section_order": 1, "body_text": "y"}
                ],
                rfa_excerpt="",
                dialect="centrist",
                session_id="s",
                org_slug="o",
            )

    def test_rejects_invalid_dialect(self):
        with pytest.raises(ValueError, match="dialect"):
            _make_editor_input(dialect="hard_left")

    def test_rejects_drafts_missing_required_field(self):
        with pytest.raises(ValueError, match="section_drafts"):
            _make_editor_input(
                section_drafts=({"section_name": "x", "section_order": 1},)
            )

    def test_rejects_non_mapping_draft(self):
        with pytest.raises(ValueError, match="section_drafts"):
            _make_editor_input(section_drafts=("not-a-dict",))  # type: ignore[arg-type]

    def test_rejects_empty_session_id(self):
        with pytest.raises(ValueError, match="session_id"):
            EditorInput(
                section_drafts=(
                    {"section_name": "x", "section_order": 1, "body_text": "y"},
                ),
                rfa_excerpt="",
                dialect="centrist",
                session_id=" ",
                org_slug="o",
            )

    def test_rejects_empty_org_slug(self):
        with pytest.raises(ValueError, match="org_slug"):
            EditorInput(
                section_drafts=(
                    {"section_name": "x", "section_order": 1, "body_text": "y"},
                ),
                rfa_excerpt="",
                dialect="centrist",
                session_id="s",
                org_slug=" ",
            )

    def test_rejects_non_string_rfa(self):
        with pytest.raises(ValueError, match="rfa_excerpt"):
            EditorInput(
                section_drafts=(
                    {"section_name": "x", "section_order": 1, "body_text": "y"},
                ),
                rfa_excerpt=None,  # type: ignore[arg-type]
                dialect="centrist",
                session_id="s",
                org_slug="o",
            )


# ---------------------------------------------------------------------------
# EditorSkillInvocation
# ---------------------------------------------------------------------------


class TestEditorSkillInvocation:
    def test_accepts_tz_aware_invocation(self):
        inv = EditorSkillInvocation(
            draft_markdown="# x\n\nbody",
            rfa_excerpt="rfa",
            dialect="centrist",
            session_id="s",
            org_slug="o",
            invocation_at_utc=datetime(2026, 4, 29, 12, 0, tzinfo=UTC),
        )
        assert inv.invocation_at_utc.tzinfo is not None

    def test_rejects_naive_clock(self):
        with pytest.raises(ValueError, match="timezone"):
            EditorSkillInvocation(
                draft_markdown="x",
                rfa_excerpt="",
                dialect="centrist",
                session_id="s",
                org_slug="o",
                invocation_at_utc=datetime(2026, 4, 29, 12, 0),
            )

    def test_rejects_empty_draft(self):
        with pytest.raises(ValueError, match="draft_markdown"):
            EditorSkillInvocation(
                draft_markdown=" ",
                rfa_excerpt="",
                dialect="centrist",
                session_id="s",
                org_slug="o",
                invocation_at_utc=datetime.now(tz=UTC),
            )

    def test_rejects_invalid_dialect(self):
        with pytest.raises(ValueError, match="dialect"):
            EditorSkillInvocation(
                draft_markdown="x",
                rfa_excerpt="",
                dialect="hard_left",  # type: ignore[arg-type]
                session_id="s",
                org_slug="o",
                invocation_at_utc=datetime.now(tz=UTC),
            )

    def test_rejects_non_string_rfa(self):
        with pytest.raises(ValueError, match="rfa_excerpt"):
            EditorSkillInvocation(
                draft_markdown="x",
                rfa_excerpt=42,  # type: ignore[arg-type]
                dialect="centrist",
                session_id="s",
                org_slug="o",
                invocation_at_utc=datetime.now(tz=UTC),
            )

    def test_rejects_empty_session_id(self):
        with pytest.raises(ValueError, match="session_id"):
            EditorSkillInvocation(
                draft_markdown="x",
                rfa_excerpt="",
                dialect="centrist",
                session_id="",
                org_slug="o",
                invocation_at_utc=datetime.now(tz=UTC),
            )

    def test_rejects_empty_org_slug(self):
        with pytest.raises(ValueError, match="org_slug"):
            EditorSkillInvocation(
                draft_markdown="x",
                rfa_excerpt="",
                dialect="centrist",
                session_id="s",
                org_slug=" ",
                invocation_at_utc=datetime.now(tz=UTC),
            )


# ---------------------------------------------------------------------------
# EditorOutput
# ---------------------------------------------------------------------------


class TestEditorOutput:
    def test_accepts_minimal_set(self):
        out = _make_editor_output()
        assert isinstance(out.flagged_terms, tuple)

    def test_rejects_non_tuple_flagged(self):
        with pytest.raises(ValueError, match="flagged_terms"):
            EditorOutput(
                flagged_terms=[_make_flagged_term()],  # type: ignore[arg-type]
                taxonomy_check=_make_taxonomy(),
                tone_feedback=_make_tone(),
                quick_wins=(),
                terms_to_verify=(),
                gaps=(),
            )

    def test_rejects_non_flagged_term_in_flagged(self):
        with pytest.raises(ValueError, match="flagged_terms"):
            EditorOutput(
                flagged_terms=("not-a-term",),  # type: ignore[arg-type]
                taxonomy_check=_make_taxonomy(),
                tone_feedback=_make_tone(),
                quick_wins=(),
                terms_to_verify=(),
                gaps=(),
            )

    def test_rejects_non_taxonomy(self):
        with pytest.raises(ValueError, match="taxonomy_check"):
            EditorOutput(
                flagged_terms=(),
                taxonomy_check="not-a-tx",  # type: ignore[arg-type]
                tone_feedback=_make_tone(),
                quick_wins=(),
                terms_to_verify=(),
                gaps=(),
            )

    def test_rejects_non_tone_feedback(self):
        with pytest.raises(ValueError, match="tone_feedback"):
            EditorOutput(
                flagged_terms=(),
                taxonomy_check=_make_taxonomy(),
                tone_feedback="not-a-tone",  # type: ignore[arg-type]
                quick_wins=(),
                terms_to_verify=(),
                gaps=(),
            )

    def test_rejects_empty_quick_wins_entry(self):
        with pytest.raises(ValueError, match="quick_wins"):
            EditorOutput(
                flagged_terms=(),
                taxonomy_check=_make_taxonomy(),
                tone_feedback=_make_tone(),
                quick_wins=("",),
                terms_to_verify=(),
                gaps=(),
            )

    def test_rejects_empty_term_entry(self):
        with pytest.raises(ValueError, match="terms_to_verify"):
            EditorOutput(
                flagged_terms=(),
                taxonomy_check=_make_taxonomy(),
                tone_feedback=_make_tone(),
                quick_wins=(),
                terms_to_verify=(" ",),
                gaps=(),
            )

    def test_rejects_non_tuple_quick_wins(self):
        with pytest.raises(ValueError, match="quick_wins"):
            EditorOutput(
                flagged_terms=(),
                taxonomy_check=_make_taxonomy(),
                tone_feedback=_make_tone(),
                quick_wins=["a"],  # type: ignore[arg-type]
                terms_to_verify=(),
                gaps=(),
            )

    def test_rejects_non_tuple_terms(self):
        with pytest.raises(ValueError, match="terms_to_verify"):
            EditorOutput(
                flagged_terms=(),
                taxonomy_check=_make_taxonomy(),
                tone_feedback=_make_tone(),
                quick_wins=(),
                terms_to_verify=["t"],  # type: ignore[arg-type]
                gaps=(),
            )

    def test_rejects_non_tuple_gaps(self):
        with pytest.raises(ValueError, match="gaps"):
            EditorOutput(
                flagged_terms=(),
                taxonomy_check=_make_taxonomy(),
                tone_feedback=_make_tone(),
                quick_wins=(),
                terms_to_verify=(),
                gaps=[],  # type: ignore[arg-type]
            )


# ---------------------------------------------------------------------------
# Public surface: __all__ leakage / membership
# ---------------------------------------------------------------------------


class TestPublicSurface:
    def test_init_all_includes_required_symbols(self):
        from pipeline.seats import editor as mod

        required = {
            "EditorInput",
            "EditorOutput",
            "FlaggedTerm",
            "ReplacementOption",
            "TaxonomyCheck",
            "ToneFeedback",
            "EditorGap",
            "ReadabilityFeedback",
            "Miscategorization",
            "EditorSkillInvocation",
            "Dialect",
            "IssueType",
            "Severity",
            "ReplacementLabel",
            "SkillLauncher",
            "SkillSubprocessResult",
            "invoke_editor_adapter",
            "parse_skill_output",
            "validate_editor_output_shape",
            "F_EDITOR_OUTPUT_SHAPE",
            "F_EDITOR_REWROTE_INSTEAD_OF_FLAGGED",
            "F_EDITOR_SINGLE_REPLACEMENT",
            "F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON",
            "F_EDITOR_SKILL_SUBPROCESS_FAIL",
            "F_EDITOR_SKILL_TIMEOUT",
            "EditorOutputShapeError",
            "EditorRewroteInsteadOfFlaggedError",
            "EditorSingleReplacementError",
            "EditorSkillSubprocessFail",
            "EditorSkillOutputMalformedJson",
            "EditorSkillTimeout",
            "EditorEnvelope",
            "EditorSeatResult",
            "EditorEnvelopeMalformed",
            "EditorGateFailed",
            "ClockFn",
            "PreGateCallable",
            "PostGateCallable",
            "decode_envelope",
            "encode_result",
            "run_seat",
            "default_cross_org_pre_gate",
            "default_noop_post_gate",
            "ENVELOPE_VERSION_V1",
            "RESULT_VERSION_V1",
            "EXIT_OK",
            "EXIT_INTERNAL_ERROR",
            "EXIT_GATE_FAIL",
            "F_EDITOR_ENVELOPE_MALFORMED",
            "F_EDITOR_ORG_CROSS_REF",
            # R2 surface
            "TAXONOMY_CATEGORIES",
            "ValidationReport",
            "apply_r2_validation",
            "assert_tone_consistency",
            "audit_taxonomy_sort",
            "audit_terms_to_verify_cross_reference",
            "dedupe_quick_wins",
            "BLUEPRINT_DEPS",
        }
        exposed = set(mod.__all__)
        missing = required - exposed
        assert not missing, f"missing from __all__: {sorted(missing)}"

    def test_no_private_in_all(self):
        from pipeline.seats import editor as mod

        for name in mod.__all__:
            assert not name.startswith("_"), f"private leaked in __all__: {name!r}"

    def test_blueprint_deps_present(self):
        from pipeline.seats.editor import BLUEPRINT_DEPS

        assert "section_07_scribe.md" in BLUEPRINT_DEPS
        assert "skills/editor/SKILL.md" in BLUEPRINT_DEPS
