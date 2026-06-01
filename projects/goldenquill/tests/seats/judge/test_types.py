"""Tests for pipeline.seats.judge.types — §9 R1 shape invariants.

Spec card: ``pipeline/engineering/spec_cards/section_09_judge_round_1_types_and_rubric_primitives.md``.

Covers:

- Rubric / RubricCriterion / RubricSubCriterion construction + invariants.
- CriterionScore score / confidence bound enforcement.
- JudgeInput non-empty drafts + RFA hash hex format.
- JudgeOutput total / max_total bound + repeated hash fields.
- Forward-Protocol structural conformance via runtime_checkable.
- F-code constants string-equality.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from pipeline.seats.judge.types import (
    ClaimEvidenceLike,
    CriterionScore,
    F_JUDGE_CRITERION_MISSING,
    F_JUDGE_EVIDENCE_NOT_IN_DRAFT,
    F_JUDGE_RUBRIC_HASH_DRIFT,
    F_JUDGE_RUBRIC_MALFORMED,
    F_JUDGE_SCORE_OUT_OF_BOUND,
    F_JUDGE_SCORE_UNPARSEABLE,
    JudgeInput,
    JudgeOutput,
    LLMCallFn,
    Rubric,
    RubricCriterion,
    RubricSubCriterion,
    SectionDraftLike,
)


UTC_NOW = datetime(2026, 4, 29, 12, 0, 0, tzinfo=timezone.utc)
SHA256_VALID = "0" * 64
SHA3_512_VALID = "0" * 128


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _sub(**overrides) -> RubricSubCriterion:
    kw = dict(
        id="a.i",
        name="Technological feasibility",
        max_points=10,
        must_address=("Process description",),
        tiers=({"points": 5, "description": "ok"},),
    )
    kw.update(overrides)
    return RubricSubCriterion(**kw)


def _crit(**overrides) -> RubricCriterion:
    kw = dict(
        id="b",
        name="Qualifications",
        max_points=20,
        scorer="review_panel",
        subcriteria=(),
        must_address=("All key personnel",),
        tiers=({"points": 5, "description": "ok"},),
    )
    kw.update(overrides)
    return RubricCriterion(**kw)


def _rubric(**overrides) -> Rubric:
    kw = dict(
        program_code="TEST-FY26",
        funder="Test Funder",
        nofo_number="TEST-001",
        max_score=20,
        min_score=0,
        criteria=(_crit(),),
        rubric_sha256=SHA256_VALID,
        loaded_at_utc=UTC_NOW,
    )
    kw.update(overrides)
    return Rubric(**kw)


# ---------------------------------------------------------------------------
# RubricSubCriterion
# ---------------------------------------------------------------------------


class TestRubricSubCriterion:
    def test_constructs_with_full_field_set(self):
        sub = _sub()
        assert sub.id == "a.i"
        assert sub.max_points == 10
        assert sub.must_address == ("Process description",)
        assert len(sub.tiers) == 1

    def test_empty_id_rejected(self):
        with pytest.raises(ValueError, match="id is empty"):
            _sub(id="   ")

    def test_empty_name_rejected(self):
        with pytest.raises(ValueError, match="name is empty"):
            _sub(name="")

    def test_negative_max_points_rejected(self):
        with pytest.raises(ValueError, match="max_points must be >= 0"):
            _sub(max_points=-1)

    def test_zero_max_points_allowed(self):
        # A rubric tier of 0 points exists in VAPG (criterion 'd' tier 0 =
        # no cash match). max_points=0 itself is unusual for a subcriterion
        # but not invalid.
        sub = _sub(max_points=0)
        assert sub.max_points == 0

    def test_frozen_dataclass(self):
        sub = _sub()
        with pytest.raises(FrozenInstanceError):
            sub.max_points = 5  # type: ignore[misc]


# ---------------------------------------------------------------------------
# RubricCriterion
# ---------------------------------------------------------------------------


class TestRubricCriterion:
    def test_constructs_with_full_field_set(self):
        crit = _crit()
        assert crit.id == "b"
        assert crit.scorer == "review_panel"

    def test_review_panel_scorer_accepted(self):
        assert _crit(scorer="review_panel").scorer == "review_panel"

    def test_state_office_scorer_accepted(self):
        assert _crit(scorer="state_office").scorer == "state_office"

    def test_administrator_scorer_accepted(self):
        assert _crit(scorer="administrator").scorer == "administrator"

    def test_unknown_scorer_rejected(self):
        with pytest.raises(ValueError, match="scorer must be one of"):
            _crit(scorer="judge_panel")  # type: ignore[arg-type]

    def test_empty_id_rejected(self):
        with pytest.raises(ValueError, match="id is empty"):
            _crit(id="")

    def test_negative_max_points_rejected(self):
        with pytest.raises(ValueError, match="max_points must be >= 0"):
            _crit(max_points=-5)

    def test_empty_name_rejected(self):
        with pytest.raises(ValueError, match="name is empty"):
            _crit(name=" ")

    def test_subcriteria_only_no_tiers_accepted(self):
        # VAPG criterion 'a' has subcriteria + no top-level tiers.
        crit = _crit(
            subcriteria=(_sub(),),
            tiers=(),
        )
        assert len(crit.subcriteria) == 1
        assert crit.tiers == ()

    def test_tiers_only_no_subcriteria_accepted(self):
        # VAPG criterion 'b' has tiers + no subcriteria.
        crit = _crit(subcriteria=(), tiers=({"points": 5, "description": "ok"},))
        assert crit.subcriteria == ()
        assert len(crit.tiers) == 1

    def test_both_empty_rejected_for_review_panel(self):
        with pytest.raises(ValueError, match="incoherent"):
            _crit(subcriteria=(), tiers=())

    def test_both_empty_rejected_for_state_office(self):
        with pytest.raises(ValueError, match="incoherent"):
            _crit(scorer="state_office", subcriteria=(), tiers=())

    def test_both_empty_allowed_for_administrator(self):
        # VAPG FY26 criterion 'g' is administrator-discretionary; the
        # rubric carries ``categories`` rather than ``tiers`` and the
        # loader does not surface those into the tiers field.
        crit = _crit(scorer="administrator", subcriteria=(), tiers=())
        assert crit.subcriteria == ()
        assert crit.tiers == ()

    def test_duplicate_subcriterion_id_rejected(self):
        with pytest.raises(ValueError, match="duplicate subcriterion id"):
            _crit(subcriteria=(_sub(), _sub()))


# ---------------------------------------------------------------------------
# Rubric
# ---------------------------------------------------------------------------


class TestRubric:
    def test_constructs_with_full_field_set(self):
        r = _rubric()
        assert r.program_code == "TEST-FY26"
        assert r.max_score == 20

    def test_empty_program_code_rejected(self):
        with pytest.raises(ValueError, match="program_code is empty"):
            _rubric(program_code="")

    def test_empty_funder_rejected(self):
        with pytest.raises(ValueError, match="funder is empty"):
            _rubric(funder="")

    def test_empty_nofo_rejected(self):
        with pytest.raises(ValueError, match="nofo_number is empty"):
            _rubric(nofo_number="")

    def test_negative_max_score_rejected(self):
        with pytest.raises(ValueError, match="max_score must be >= 0"):
            _rubric(max_score=-1)

    def test_negative_min_score_rejected(self):
        with pytest.raises(ValueError, match="min_score must be >= 0"):
            _rubric(min_score=-1)

    def test_min_greater_than_max_rejected(self):
        with pytest.raises(ValueError, match="min_score .* > max_score"):
            _rubric(min_score=50, max_score=20)

    def test_empty_criteria_rejected(self):
        with pytest.raises(ValueError, match="criteria must be non-empty"):
            _rubric(criteria=())

    def test_short_sha256_rejected(self):
        with pytest.raises(ValueError, match="rubric_sha256 must be 64"):
            _rubric(rubric_sha256="abcd")

    def test_uppercase_sha256_rejected(self):
        with pytest.raises(ValueError, match="must be lowercase hex"):
            _rubric(rubric_sha256="A" * 64)

    def test_non_hex_sha256_rejected(self):
        with pytest.raises(ValueError, match="must be lowercase hex"):
            _rubric(rubric_sha256="g" * 64)

    def test_naive_loaded_at_utc_rejected(self):
        with pytest.raises(ValueError, match="must be timezone-aware"):
            _rubric(loaded_at_utc=datetime(2026, 4, 29, 12, 0, 0))

    def test_duplicate_criterion_id_rejected(self):
        c1 = _crit(id="a")
        c2 = _crit(id="a", name="Second")
        with pytest.raises(ValueError, match="duplicate criterion id"):
            _rubric(criteria=(c1, c2), max_score=40)

    def test_max_score_below_sum_criterion_max_rejected(self):
        c1 = _crit(id="a", max_points=30)
        c2 = _crit(id="b", max_points=20)
        with pytest.raises(ValueError, match=r"max_score .* < sum"):
            _rubric(criteria=(c1, c2), max_score=40)

    def test_max_score_equal_to_sum_accepted(self):
        c1 = _crit(id="a", max_points=30)
        c2 = _crit(id="b", max_points=20)
        r = _rubric(criteria=(c1, c2), max_score=50)
        assert r.max_score == 50

    def test_max_score_above_sum_accepted(self):
        # Discretionary headroom (e.g. priority points cap > sum of fixed).
        c1 = _crit(id="a", max_points=30)
        r = _rubric(criteria=(c1,), max_score=50)
        assert r.max_score == 50


# ---------------------------------------------------------------------------
# CriterionScore
# ---------------------------------------------------------------------------


class TestCriterionScore:
    def test_constructs_with_full_field_set(self):
        cs = CriterionScore(
            criterion_id="a.i",
            score=8,
            evidence_quote="The mushroom processing facility is operational.",
            confidence=0.85,
            rationale="Strong process narrative",
        )
        assert cs.criterion_id == "a.i"
        assert cs.score == 8

    def test_empty_criterion_id_rejected(self):
        with pytest.raises(ValueError, match="criterion_id is empty"):
            CriterionScore(
                criterion_id="",
                score=5,
                evidence_quote="x",
                confidence=0.5,
                rationale="y",
            )

    def test_negative_score_rejected(self):
        with pytest.raises(ValueError, match="score must be >= 0"):
            CriterionScore(
                criterion_id="b",
                score=-1,
                evidence_quote="x",
                confidence=0.5,
                rationale="y",
            )

    def test_zero_score_accepted(self):
        cs = CriterionScore(
            criterion_id="b",
            score=0,
            evidence_quote="x",
            confidence=0.0,
            rationale="y",
        )
        assert cs.score == 0

    def test_confidence_below_zero_rejected(self):
        with pytest.raises(ValueError, match=r"confidence must be in"):
            CriterionScore(
                criterion_id="b",
                score=5,
                evidence_quote="x",
                confidence=-0.01,
                rationale="y",
            )

    def test_confidence_above_one_rejected(self):
        with pytest.raises(ValueError, match=r"confidence must be in"):
            CriterionScore(
                criterion_id="b",
                score=5,
                evidence_quote="x",
                confidence=1.01,
                rationale="y",
            )

    def test_confidence_one_accepted(self):
        cs = CriterionScore(
            criterion_id="b",
            score=5,
            evidence_quote="x",
            confidence=1.0,
            rationale="y",
        )
        assert cs.confidence == 1.0


# ---------------------------------------------------------------------------
# JudgeInput / JudgeOutput
# ---------------------------------------------------------------------------


class _FakeClaimEvidence:
    def __init__(self, claim_text: str, evidence_kind: str, source_pointer: str):
        self.claim_text = claim_text
        self.evidence_kind = evidence_kind
        self.source_pointer = source_pointer


class _FakeSectionDraft:
    def __init__(
        self,
        section_name: str,
        section_order: int,
        body_text: str,
        claim_evidence_map: tuple = (),
    ):
        self.section_name = section_name
        self.section_order = section_order
        self.body_text = body_text
        self.claim_evidence_map = claim_evidence_map


class TestJudgeInput:
    def test_constructs_with_full_field_set(self):
        draft = _FakeSectionDraft(
            section_name="Project Narrative",
            section_order=1,
            body_text="We grow gourmet mushrooms.",
        )
        ji = JudgeInput(
            section_drafts=(draft,),
            rubric=_rubric(),
            rfa_content_sha3_512=SHA3_512_VALID,
        )
        assert ji.section_drafts[0].section_name == "Project Narrative"

    def test_empty_drafts_rejected(self):
        with pytest.raises(ValueError, match="section_drafts must be non-empty"):
            JudgeInput(
                section_drafts=(),
                rubric=_rubric(),
                rfa_content_sha3_512=SHA3_512_VALID,
            )

    def test_short_rfa_hash_rejected(self):
        draft = _FakeSectionDraft("S", 1, "body")
        with pytest.raises(ValueError, match="must be 128"):
            JudgeInput(
                section_drafts=(draft,),
                rubric=_rubric(),
                rfa_content_sha3_512="ab",
            )

    def test_uppercase_rfa_hash_rejected(self):
        draft = _FakeSectionDraft("S", 1, "body")
        with pytest.raises(ValueError, match="must be lowercase hex"):
            JudgeInput(
                section_drafts=(draft,),
                rubric=_rubric(),
                rfa_content_sha3_512="F" * 128,
            )


class TestJudgeOutput:
    def _ok_score(self, score: int = 8):
        return CriterionScore(
            criterion_id="a.i",
            score=score,
            evidence_quote="x",
            confidence=0.85,
            rationale="y",
        )

    def test_constructs_with_full_field_set(self):
        jo = JudgeOutput(
            criterion_scores=(self._ok_score(),),
            total_score=8,
            max_total=10,
            rubric_sha256=SHA256_VALID,
            rfa_content_sha3_512=SHA3_512_VALID,
            scored_at_utc=UTC_NOW,
        )
        assert jo.total_score == 8

    def test_empty_scores_rejected(self):
        with pytest.raises(ValueError, match="criterion_scores must be non-empty"):
            JudgeOutput(
                criterion_scores=(),
                total_score=0,
                max_total=0,
                rubric_sha256=SHA256_VALID,
                rfa_content_sha3_512=SHA3_512_VALID,
                scored_at_utc=UTC_NOW,
            )

    def test_negative_total_rejected(self):
        with pytest.raises(ValueError, match="total_score must be >= 0"):
            JudgeOutput(
                criterion_scores=(self._ok_score(),),
                total_score=-1,
                max_total=10,
                rubric_sha256=SHA256_VALID,
                rfa_content_sha3_512=SHA3_512_VALID,
                scored_at_utc=UTC_NOW,
            )

    def test_negative_max_total_rejected(self):
        with pytest.raises(ValueError, match="max_total must be >= 0"):
            JudgeOutput(
                criterion_scores=(self._ok_score(),),
                total_score=0,
                max_total=-1,
                rubric_sha256=SHA256_VALID,
                rfa_content_sha3_512=SHA3_512_VALID,
                scored_at_utc=UTC_NOW,
            )

    def test_total_above_max_rejected(self):
        with pytest.raises(ValueError, match=r"total_score .* > max_total"):
            JudgeOutput(
                criterion_scores=(self._ok_score(),),
                total_score=15,
                max_total=10,
                rubric_sha256=SHA256_VALID,
                rfa_content_sha3_512=SHA3_512_VALID,
                scored_at_utc=UTC_NOW,
            )

    def test_short_rubric_hash_rejected(self):
        with pytest.raises(ValueError, match="rubric_sha256 must be 64"):
            JudgeOutput(
                criterion_scores=(self._ok_score(),),
                total_score=8,
                max_total=10,
                rubric_sha256="abc",
                rfa_content_sha3_512=SHA3_512_VALID,
                scored_at_utc=UTC_NOW,
            )

    def test_uppercase_rubric_hash_rejected(self):
        with pytest.raises(ValueError, match="must be lowercase hex"):
            JudgeOutput(
                criterion_scores=(self._ok_score(),),
                total_score=8,
                max_total=10,
                rubric_sha256="A" * 64,
                rfa_content_sha3_512=SHA3_512_VALID,
                scored_at_utc=UTC_NOW,
            )

    def test_short_rfa_hash_rejected(self):
        with pytest.raises(ValueError, match="must be 128"):
            JudgeOutput(
                criterion_scores=(self._ok_score(),),
                total_score=8,
                max_total=10,
                rubric_sha256=SHA256_VALID,
                rfa_content_sha3_512="ab",
                scored_at_utc=UTC_NOW,
            )

    def test_uppercase_rfa_hash_rejected(self):
        with pytest.raises(ValueError, match="rfa_content_sha3_512 must be lowercase hex"):
            JudgeOutput(
                criterion_scores=(self._ok_score(),),
                total_score=8,
                max_total=10,
                rubric_sha256=SHA256_VALID,
                rfa_content_sha3_512="F" * 128,
                scored_at_utc=UTC_NOW,
            )

    def test_naive_scored_at_utc_rejected(self):
        with pytest.raises(ValueError, match="must be timezone-aware"):
            JudgeOutput(
                criterion_scores=(self._ok_score(),),
                total_score=8,
                max_total=10,
                rubric_sha256=SHA256_VALID,
                rfa_content_sha3_512=SHA3_512_VALID,
                scored_at_utc=datetime(2026, 4, 29, 12, 0, 0),
            )


# ---------------------------------------------------------------------------
# Forward-Protocol structural conformance
# ---------------------------------------------------------------------------


class TestForwardProtocols:
    def test_section_draft_like_structural_conformance(self):
        d = _FakeSectionDraft("S", 1, "body", claim_evidence_map=())
        assert isinstance(d, SectionDraftLike)

    def test_claim_evidence_like_structural_conformance(self):
        ce = _FakeClaimEvidence("c", "e", "PROJECT_CONTEXT:foo")
        assert isinstance(ce, ClaimEvidenceLike)

    def test_section_draft_missing_field_does_not_conform(self):
        class Missing:
            section_name = "S"
            section_order = 1
            # No body_text, no claim_evidence_map.

        # runtime_checkable Protocols verify attribute presence (not types),
        # so missing fields fail isinstance.
        assert not isinstance(Missing(), SectionDraftLike)

    def test_llm_call_fn_callable_conformance(self):
        def fake_call(*, prompt: str, max_tokens: int) -> str:
            return "{}"

        # LLMCallFn is runtime_checkable; a plain function is structurally
        # compatible (callable returning str).
        assert isinstance(fake_call, LLMCallFn)


# ---------------------------------------------------------------------------
# Failure-code constants
# ---------------------------------------------------------------------------


class TestFailureCodeConstants:
    def test_rubric_malformed_value(self):
        assert F_JUDGE_RUBRIC_MALFORMED == "F-JUDGE-RUBRIC-MALFORMED"

    def test_criterion_missing_value(self):
        assert F_JUDGE_CRITERION_MISSING == "F-JUDGE-CRITERION-MISSING"

    def test_score_unparseable_value(self):
        assert F_JUDGE_SCORE_UNPARSEABLE == "F-JUDGE-SCORE-UNPARSEABLE"

    def test_evidence_not_in_draft_value(self):
        assert F_JUDGE_EVIDENCE_NOT_IN_DRAFT == "F-JUDGE-EVIDENCE-NOT-IN-DRAFT"

    def test_score_out_of_bound_value(self):
        assert F_JUDGE_SCORE_OUT_OF_BOUND == "F-JUDGE-SCORE-OUT-OF-BOUND"

    def test_rubric_hash_drift_value(self):
        assert F_JUDGE_RUBRIC_HASH_DRIFT == "F-JUDGE-RUBRIC-HASH-DRIFT"
