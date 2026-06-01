"""Round-3 tests for ``pipeline.seats.judge.logician_wiring``.

Covers PRE/POST-gate assemblers + their internal predicates:

- PRE: ``F-JUDGE-CROSS-FAMILY-COLLISION`` + ``F-JUDGE-ORG-CROSS-REF``.
- POST: ``F-JUDGE-RUBRIC-MALFORMED`` + ``F-JUDGE-RUBRIC-HASH-DRIFT`` +
  ``F-JUDGE-CRITERION-MISSING`` + ``F-JUDGE-SCORE-OUT-OF-BOUND`` +
  ``F-JUDGE-EVIDENCE-NOT-IN-DRAFT`` (Law 5).
"""
from __future__ import annotations

from datetime import datetime, timezone
from types import MappingProxyType
from typing import Any, Mapping

import pytest

from pipeline.seats.judge.logician_wiring import (
    JudgePostGateAssembly,
    JudgePreGateAssembly,
    _check_coverage,
    _check_evidence_in_drafts,
    _check_score_bounds,
    assemble_judge_post_gate,
    assemble_judge_pre_gate,
)
from pipeline.seats.judge.seat import (
    F_JUDGE_CROSS_FAMILY_COLLISION,
    F_JUDGE_ORG_CROSS_REF,
    JudgeEnvelope,
    JudgeGateFailed,
)
from pipeline.seats.judge.types import (
    CriterionScore,
    F_JUDGE_CRITERION_MISSING,
    F_JUDGE_EVIDENCE_NOT_IN_DRAFT,
    F_JUDGE_RUBRIC_HASH_DRIFT,
    F_JUDGE_RUBRIC_MALFORMED,
    F_JUDGE_SCORE_OUT_OF_BOUND,
    JudgeOutput,
    JudgeVerdict,
    ResponsivenessMap,
    Rubric,
    RubricCriterion,
    RubricSubCriterion,
)


_FIXED_NOW = datetime(2026, 4, 30, 12, 0, tzinfo=timezone.utc)
_RFA_HASH = "b" * 128
_RUBRIC_HASH = "c" * 64
_SHELL_HASH = "a" * 128


def _make_envelope(
    *, scribe_family: str = "anthropic", org: str = "fit_farms_llc"
) -> JudgeEnvelope:
    return JudgeEnvelope(
        envelope_version="judge-envelope.v1",
        run_id="r1",
        org_slug=org,
        iteration_number=0,
        program_code="VAPG",
        rubric_path="/r.json",
        rfa_content_sha3_512=_RFA_HASH,
        rfa_scope_summary="scope",
        scribe_provider_family=scribe_family,
        section_drafts_blob=({"section_name": "S"},),
        compiled_prompt_shell_sha3_512=_SHELL_HASH,
        project_context={"applicant_name": "FIT Farms"},
        envelope_emitted_at_utc=_FIXED_NOW,
    )


def _build_rubric() -> Rubric:
    crit_b = RubricCriterion(
        id="b",
        name="Personnel",
        max_points=20,
        scorer="review_panel",
        subcriteria=(),
        must_address=("qualifications",),
        tiers=(MappingProxyType({"points": 20, "description": "Strong"}),),
    )
    return Rubric(
        program_code="VAPG",
        funder="USDA",
        nofo_number="X",
        max_score=100,
        min_score=50,
        criteria=(crit_b,),
        rubric_sha256=_RUBRIC_HASH,
        loaded_at_utc=_FIXED_NOW,
    )


def _build_rubric_with_subs() -> Rubric:
    sub_a_i = RubricSubCriterion(
        id="a.i", name="i", max_points=10, must_address=(), tiers=()
    )
    sub_a_ii = RubricSubCriterion(
        id="a.ii", name="ii", max_points=10, must_address=(), tiers=()
    )
    crit_a = RubricCriterion(
        id="a",
        name="Venture",
        max_points=20,
        scorer="review_panel",
        subcriteria=(sub_a_i, sub_a_ii),
        must_address=(),
        tiers=(),
    )
    return Rubric(
        program_code="VAPG",
        funder="USDA",
        nofo_number="X",
        max_score=100,
        min_score=50,
        criteria=(crit_a,),
        rubric_sha256=_RUBRIC_HASH,
        loaded_at_utc=_FIXED_NOW,
    )


def _build_verdict(
    rubric: Rubric, scores: tuple[CriterionScore, ...], *, total: int, max_total: int
) -> JudgeVerdict:
    jo = JudgeOutput(
        criterion_scores=scores,
        total_score=total,
        max_total=max_total,
        rubric_sha256=rubric.rubric_sha256,
        rfa_content_sha3_512=_RFA_HASH,
        scored_at_utc=_FIXED_NOW,
    )
    return JudgeVerdict(
        judge_output=jo,
        rubric_program_code=rubric.program_code,
        responsiveness_map=ResponsivenessMap(entries=()),
        assembled_at_utc=_FIXED_NOW,
    )


class _FakeDraft:
    def __init__(self, body: str = "FIT Farms grows mushrooms."):
        self.section_name = "S"
        self.section_order = 1
        self.body_text = body
        self.claim_evidence_map: tuple = ()


# ---------------------------------------------------------------------------
# Result shapes
# ---------------------------------------------------------------------------


class TestPreGateAssemblyShape:
    def test_constructs_with_codes(self):
        a = JudgePreGateAssembly(
            run_id="r", org_slug="o", codes_checked=("F-A", "F-B")
        )
        assert a.codes_checked == ("F-A", "F-B")


class TestPostGateAssemblyShape:
    def test_constructs_with_codes(self):
        a = JudgePostGateAssembly(
            run_id="r", org_slug="o", codes_checked=("F-A",)
        )
        assert a.codes_checked == ("F-A",)


# ---------------------------------------------------------------------------
# PRE-gate assembler
# ---------------------------------------------------------------------------


def _no_foreign_orgs(*, envelope_org_slug, section_drafts_blob, project_context):
    return ()


class TestAssembleJudgePreGate:
    def test_happy_path(self):
        env = _make_envelope()
        result = assemble_judge_pre_gate(
            envelope=env, cedar_cross_org_check=_no_foreign_orgs
        )
        assert F_JUDGE_CROSS_FAMILY_COLLISION in result.codes_checked
        assert F_JUDGE_ORG_CROSS_REF in result.codes_checked

    def test_cross_family_google_rejected(self):
        env = _make_envelope(scribe_family="google")
        with pytest.raises(JudgeGateFailed) as exc:
            assemble_judge_pre_gate(
                envelope=env, cedar_cross_org_check=_no_foreign_orgs
            )
        assert exc.value.failure_code == F_JUDGE_CROSS_FAMILY_COLLISION
        assert exc.value.evidence["scribe_provider_family"] == "google"
        assert exc.value.evidence["judge_own_family"] == "google"

    def test_other_families_pass(self):
        for family in ("anthropic", "openai", "groq", "alibaba"):
            env = _make_envelope(scribe_family=family)
            result = assemble_judge_pre_gate(
                envelope=env, cedar_cross_org_check=_no_foreign_orgs
            )
            assert isinstance(result, JudgePreGateAssembly)

    def test_cedar_foreign_org_rejected(self):
        def _has_foreign(*, envelope_org_slug, section_drafts_blob, project_context):
            return ("other_org",)

        env = _make_envelope()
        with pytest.raises(JudgeGateFailed) as exc:
            assemble_judge_pre_gate(envelope=env, cedar_cross_org_check=_has_foreign)
        assert exc.value.failure_code == F_JUDGE_ORG_CROSS_REF
        assert exc.value.evidence["foreign_slugs"] == ["other_org"]

    def test_cross_family_check_runs_before_cedar(self):
        """PRE-gate check ordering: cross-family fires before cedar."""
        called: list[str] = []

        def _track_cedar(*, envelope_org_slug, section_drafts_blob, project_context):
            called.append("cedar")
            return ()

        env = _make_envelope(scribe_family="google")
        with pytest.raises(JudgeGateFailed) as exc:
            assemble_judge_pre_gate(envelope=env, cedar_cross_org_check=_track_cedar)
        assert exc.value.failure_code == F_JUDGE_CROSS_FAMILY_COLLISION
        # Cedar should NOT have run.
        assert called == []


# ---------------------------------------------------------------------------
# POST-gate predicates
# ---------------------------------------------------------------------------


class TestCheckEvidenceInDrafts:
    def test_happy_quote_in_draft(self):
        rubric = _build_rubric()
        cs = CriterionScore(
            criterion_id="b",
            score=18,
            evidence_quote="grows mushrooms",
            confidence=0.9,
            rationale="r",
        )
        v = _build_verdict(rubric, (cs,), total=18, max_total=20)
        bad = _check_evidence_in_drafts(v, (_FakeDraft("FIT Farms grows mushrooms in 50 acres."),))
        assert bad == ()

    def test_quote_not_in_draft(self):
        rubric = _build_rubric()
        cs = CriterionScore(
            criterion_id="b",
            score=18,
            evidence_quote="something not present",
            confidence=0.9,
            rationale="r",
        )
        v = _build_verdict(rubric, (cs,), total=18, max_total=20)
        bad = _check_evidence_in_drafts(v, (_FakeDraft("totally other text"),))
        assert bad == ("b",)

    def test_empty_drafts_means_all_unsourced(self):
        rubric = _build_rubric()
        cs = CriterionScore(
            criterion_id="b",
            score=18,
            evidence_quote="anything",
            confidence=0.9,
            rationale="r",
        )
        v = _build_verdict(rubric, (cs,), total=18, max_total=20)
        bad = _check_evidence_in_drafts(v, ())
        assert bad == ("b",)

    def test_blank_quote_marks_unsourced(self):
        # CriterionScore allows non-empty evidence_quote; bypass via fake.
        class _Score:
            criterion_id = "b"
            evidence_quote = "   "

        class _JO:
            criterion_scores = (_Score(),)

        class _V:
            judge_output = _JO()

        bad = _check_evidence_in_drafts(_V(), (_FakeDraft("anything"),))
        assert bad == ("b",)

    def test_multiple_drafts_any_match_passes(self):
        rubric = _build_rubric()
        cs = CriterionScore(
            criterion_id="b",
            score=18,
            evidence_quote="needle",
            confidence=0.9,
            rationale="r",
        )
        v = _build_verdict(rubric, (cs,), total=18, max_total=20)
        drafts = (_FakeDraft("hay"), _FakeDraft("needle in haystack"))
        bad = _check_evidence_in_drafts(v, drafts)
        assert bad == ()


class TestCheckScoreBounds:
    def test_in_bounds(self):
        rubric = _build_rubric()
        cs = CriterionScore(
            criterion_id="b",
            score=18,
            evidence_quote="x",
            confidence=0.9,
            rationale="r",
        )
        v = _build_verdict(rubric, (cs,), total=18, max_total=20)
        assert _check_score_bounds(v, rubric) == ()

    def test_score_above_max(self):
        rubric = _build_rubric()
        # Bypass CriterionScore.__post_init__ to inject overflow.
        score_obj = CriterionScore(
            criterion_id="b",
            score=20,
            evidence_quote="x",
            confidence=0.9,
            rationale="r",
        )
        # Trick: object with same shape but score above max
        class _Score:
            criterion_id = "b"
            score = 25
            evidence_quote = "x"
            confidence = 0.9
            rationale = "r"

        class _JO:
            criterion_scores = (_Score(),)

        class _V:
            judge_output = _JO()

        assert _check_score_bounds(_V(), rubric) == ("b",)

    def test_unknown_id_skipped(self):
        rubric = _build_rubric()
        # Score for an unknown criterion id is skipped (coverage layer
        # handles it instead of bound layer).
        class _Score:
            criterion_id = "nonexistent"
            score = 5
            evidence_quote = "x"
            confidence = 0.9
            rationale = "r"

        class _JO:
            criterion_scores = (_Score(),)

        class _V:
            judge_output = _JO()

        assert _check_score_bounds(_V(), rubric) == ()


class TestCheckCoverage:
    def test_parent_covered(self):
        rubric = _build_rubric()
        cs = CriterionScore(
            criterion_id="b",
            score=18,
            evidence_quote="x",
            confidence=0.9,
            rationale="r",
        )
        v = _build_verdict(rubric, (cs,), total=18, max_total=20)
        assert _check_coverage(v, rubric) == ()

    def test_parent_uncovered_no_subs(self):
        rubric = _build_rubric()
        # No score at all for parent 'b'; pass an unrelated score id.
        class _Score:
            criterion_id = "z"
            score = 5
            evidence_quote = "x"
            confidence = 0.9
            rationale = "r"

        class _JO:
            criterion_scores = (_Score(),)

        class _V:
            judge_output = _JO()

        bad = _check_coverage(_V(), rubric)
        assert "b" in bad

    def test_all_subs_covered(self):
        rubric = _build_rubric_with_subs()
        cs1 = CriterionScore(
            criterion_id="a.i",
            score=8,
            evidence_quote="x",
            confidence=0.9,
            rationale="r",
        )
        cs2 = CriterionScore(
            criterion_id="a.ii",
            score=9,
            evidence_quote="x",
            confidence=0.9,
            rationale="r",
        )
        v = _build_verdict(rubric, (cs1, cs2), total=17, max_total=20)
        assert _check_coverage(v, rubric) == ()

    def test_partial_sub_coverage_flagged(self):
        rubric = _build_rubric_with_subs()
        cs1 = CriterionScore(
            criterion_id="a.i",
            score=8,
            evidence_quote="x",
            confidence=0.9,
            rationale="r",
        )
        v = _build_verdict(rubric, (cs1,), total=8, max_total=10)
        bad = _check_coverage(v, rubric)
        assert "a" in bad

    def test_parent_and_sub_both_covered_flagged(self):
        rubric = _build_rubric_with_subs()
        cs_parent = CriterionScore(
            criterion_id="a",
            score=15,
            evidence_quote="x",
            confidence=0.9,
            rationale="r",
        )
        cs_sub = CriterionScore(
            criterion_id="a.i",
            score=8,
            evidence_quote="x",
            confidence=0.9,
            rationale="r",
        )
        v = _build_verdict(rubric, (cs_parent, cs_sub), total=23, max_total=30)
        bad = _check_coverage(v, rubric)
        assert "a" in bad


# ---------------------------------------------------------------------------
# POST-gate assembler
# ---------------------------------------------------------------------------


def _ok_recompute(*, rubric_path: str) -> str:
    return _RUBRIC_HASH


class TestAssembleJudgePostGate:
    def test_happy_path(self):
        env = _make_envelope()
        rubric = _build_rubric()
        cs = CriterionScore(
            criterion_id="b",
            score=18,
            evidence_quote="grows mushrooms",
            confidence=0.9,
            rationale="r",
        )
        verdict = _build_verdict(rubric, (cs,), total=18, max_total=20)
        result = assemble_judge_post_gate(
            envelope=env,
            judge_verdict=verdict,
            rubric=rubric,
            section_drafts=(_FakeDraft("FIT Farms grows mushrooms."),),
            rubric_hash_recompute=_ok_recompute,
        )
        assert F_JUDGE_RUBRIC_MALFORMED in result.codes_checked
        assert F_JUDGE_RUBRIC_HASH_DRIFT in result.codes_checked
        assert F_JUDGE_CRITERION_MISSING in result.codes_checked
        assert F_JUDGE_SCORE_OUT_OF_BOUND in result.codes_checked
        assert F_JUDGE_EVIDENCE_NOT_IN_DRAFT in result.codes_checked

    def test_rubric_malformed_zero_max_score(self):
        env = _make_envelope()
        # Use a rubric with degenerate max_score (must use object.__new__
        # because Rubric.__post_init__ would reject construction-time).
        rubric = _build_rubric()
        bad_rubric = object.__new__(Rubric)
        for fname in (
            "program_code",
            "funder",
            "nofo_number",
            "min_score",
            "criteria",
            "rubric_sha256",
            "loaded_at_utc",
        ):
            object.__setattr__(bad_rubric, fname, getattr(rubric, fname))
        object.__setattr__(bad_rubric, "max_score", 0)
        cs = CriterionScore(
            criterion_id="b",
            score=18,
            evidence_quote="grows mushrooms",
            confidence=0.9,
            rationale="r",
        )
        verdict = _build_verdict(rubric, (cs,), total=18, max_total=20)
        with pytest.raises(JudgeGateFailed) as exc:
            assemble_judge_post_gate(
                envelope=env,
                judge_verdict=verdict,
                rubric=bad_rubric,
                section_drafts=(_FakeDraft("grows mushrooms"),),
                rubric_hash_recompute=_ok_recompute,
            )
        assert exc.value.failure_code == F_JUDGE_RUBRIC_MALFORMED

    def test_rubric_hash_drift(self):
        env = _make_envelope()
        rubric = _build_rubric()
        cs = CriterionScore(
            criterion_id="b",
            score=18,
            evidence_quote="grows mushrooms",
            confidence=0.9,
            rationale="r",
        )
        verdict = _build_verdict(rubric, (cs,), total=18, max_total=20)

        def _drifted(*, rubric_path: str) -> str:
            return "d" * 64

        with pytest.raises(JudgeGateFailed) as exc:
            assemble_judge_post_gate(
                envelope=env,
                judge_verdict=verdict,
                rubric=rubric,
                section_drafts=(_FakeDraft("grows mushrooms"),),
                rubric_hash_recompute=_drifted,
            )
        assert exc.value.failure_code == F_JUDGE_RUBRIC_HASH_DRIFT
        assert exc.value.evidence["score_time_sha"] == _RUBRIC_HASH
        assert exc.value.evidence["gate_time_sha"] == "d" * 64

    def test_rubric_hash_recompute_raises_internal_exception(self):
        env = _make_envelope()
        rubric = _build_rubric()
        cs = CriterionScore(
            criterion_id="b",
            score=18,
            evidence_quote="grows mushrooms",
            confidence=0.9,
            rationale="r",
        )
        verdict = _build_verdict(rubric, (cs,), total=18, max_total=20)

        def _raising(*, rubric_path: str) -> str:
            raise FileNotFoundError("not found")

        with pytest.raises(JudgeGateFailed) as exc:
            assemble_judge_post_gate(
                envelope=env,
                judge_verdict=verdict,
                rubric=rubric,
                section_drafts=(_FakeDraft("grows mushrooms"),),
                rubric_hash_recompute=_raising,
            )
        assert exc.value.failure_code == F_JUDGE_RUBRIC_HASH_DRIFT
        assert exc.value.evidence["exception_class"] == "FileNotFoundError"

    def test_rubric_hash_recompute_propagates_judge_gate_failed(self):
        env = _make_envelope()
        rubric = _build_rubric()
        cs = CriterionScore(
            criterion_id="b",
            score=18,
            evidence_quote="grows mushrooms",
            confidence=0.9,
            rationale="r",
        )
        verdict = _build_verdict(rubric, (cs,), total=18, max_total=20)

        def _gate(*, rubric_path: str) -> str:
            raise JudgeGateFailed(
                failure_code="F-CUSTOM",
                trigger="custom",
                evidence={},
            )

        with pytest.raises(JudgeGateFailed) as exc:
            assemble_judge_post_gate(
                envelope=env,
                judge_verdict=verdict,
                rubric=rubric,
                section_drafts=(_FakeDraft("grows mushrooms"),),
                rubric_hash_recompute=_gate,
            )
        assert exc.value.failure_code == "F-CUSTOM"

    def test_criterion_missing_no_subs(self):
        env = _make_envelope()
        rubric = _build_rubric()
        # Score is for a criterion id that's not in the rubric.
        class _Score:
            criterion_id = "z"
            score = 5
            evidence_quote = "grows mushrooms"
            confidence = 0.9
            rationale = "r"

        class _JO:
            criterion_scores = (_Score(),)
            total_score = 5
            max_total = 20
            rubric_sha256 = _RUBRIC_HASH

        class _V:
            judge_output = _JO()

        with pytest.raises(JudgeGateFailed) as exc:
            assemble_judge_post_gate(
                envelope=env,
                judge_verdict=_V(),
                rubric=rubric,
                section_drafts=(_FakeDraft("grows mushrooms"),),
                rubric_hash_recompute=_ok_recompute,
            )
        assert exc.value.failure_code == F_JUDGE_CRITERION_MISSING

    def test_score_out_of_bound(self):
        env = _make_envelope()
        rubric = _build_rubric()

        class _Score:
            criterion_id = "b"
            score = 99
            evidence_quote = "grows mushrooms"
            confidence = 0.9
            rationale = "r"

        class _JO:
            criterion_scores = (_Score(),)
            total_score = 99
            max_total = 20
            rubric_sha256 = _RUBRIC_HASH

        class _V:
            judge_output = _JO()

        with pytest.raises(JudgeGateFailed) as exc:
            assemble_judge_post_gate(
                envelope=env,
                judge_verdict=_V(),
                rubric=rubric,
                section_drafts=(_FakeDraft("grows mushrooms"),),
                rubric_hash_recompute=_ok_recompute,
            )
        assert exc.value.failure_code == F_JUDGE_SCORE_OUT_OF_BOUND

    def test_evidence_not_in_draft_law5(self):
        env = _make_envelope()
        rubric = _build_rubric()
        cs = CriterionScore(
            criterion_id="b",
            score=18,
            evidence_quote="something not in any draft",
            confidence=0.9,
            rationale="r",
        )
        verdict = _build_verdict(rubric, (cs,), total=18, max_total=20)
        with pytest.raises(JudgeGateFailed) as exc:
            assemble_judge_post_gate(
                envelope=env,
                judge_verdict=verdict,
                rubric=rubric,
                section_drafts=(_FakeDraft("totally other text"),),
                rubric_hash_recompute=_ok_recompute,
            )
        assert exc.value.failure_code == F_JUDGE_EVIDENCE_NOT_IN_DRAFT

    def test_check_order_canonical(self):
        """Each check fires only after upstream checks pass.
        Specifically: rubric_malformed → rubric_hash → coverage →
        score_bounds → evidence-in-draft.
        """
        env = _make_envelope()
        rubric = _build_rubric()
        # Trip multiple gates simultaneously: hash drift + evidence-not-in-draft.
        cs = CriterionScore(
            criterion_id="b",
            score=18,
            evidence_quote="never present",
            confidence=0.9,
            rationale="r",
        )
        verdict = _build_verdict(rubric, (cs,), total=18, max_total=20)

        def _drifted(*, rubric_path: str) -> str:
            return "d" * 64

        with pytest.raises(JudgeGateFailed) as exc:
            assemble_judge_post_gate(
                envelope=env,
                judge_verdict=verdict,
                rubric=rubric,
                section_drafts=(_FakeDraft("totally other text"),),
                rubric_hash_recompute=_drifted,
            )
        # Hash drift is checked before evidence-in-draft, so it fires first.
        assert exc.value.failure_code == F_JUDGE_RUBRIC_HASH_DRIFT
