"""§10 Red Team R2 — judge_view + cross_rubric_dispatch + E-026 lineage tests.

Round 2 covers:
- :class:`JudgeContextView` adapter shape + truncation invariant.
- :func:`view_from_judge_verdict` adapter binding to Judge's concrete
  :class:`pipeline.seats.judge.types.JudgeVerdict`.
- :func:`select_scoring_targets` parent-vs-subcriteria dispatcher
  (closes OQ-10.8: Red Team scores at the SAME structural level Judge
  scored at — identity-invariant).
- :func:`assert_red_team_id_set_matches_judge` identity-invariant
  pre-check.
- **E-026 lineage assertions** binding Scribe's ``SectionDraft`` and
  Judge's ``JudgeVerdict`` to the forward-Protocols Red Team R1 declared.
  Guards against import-path drift between R1/R2 and Judge R3 / Scribe
  R3 LOCK rounds.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest


# ---------------------------------------------------------------------------
# E-026 lineage assertions — bind to concrete LOCKed shapes
# ---------------------------------------------------------------------------


class TestE026LineageBinding:
    """E-026 ``__module__`` lineage discipline.

    These tests assert the import paths of the concrete shapes Red Team
    R1 forward-Protocols target hasn't drifted. If Scribe or Judge moves
    a shape between modules without updating Red Team, this test fails
    loud at the next regression run.
    """

    def test_scribe_section_draft_module(self) -> None:
        from pipeline.seats.scribe.section_draft import SectionDraft

        assert SectionDraft.__module__ == "pipeline.seats.scribe.section_draft", (
            f"SectionDraft moved! current __module__ = {SectionDraft.__module__!r}"
        )

    def test_scribe_claim_evidence_module(self) -> None:
        from pipeline.seats.scribe.section_draft import ClaimEvidence

        assert ClaimEvidence.__module__ == "pipeline.seats.scribe.section_draft"

    def test_judge_judge_verdict_module(self) -> None:
        from pipeline.seats.judge.types import JudgeVerdict

        assert JudgeVerdict.__module__ == "pipeline.seats.judge.types", (
            f"JudgeVerdict moved! current __module__ = {JudgeVerdict.__module__!r}"
        )

    def test_judge_judge_output_module(self) -> None:
        from pipeline.seats.judge.types import JudgeOutput

        assert JudgeOutput.__module__ == "pipeline.seats.judge.types"

    def test_judge_rubric_module(self) -> None:
        from pipeline.seats.judge.types import Rubric

        assert Rubric.__module__ == "pipeline.seats.judge.types"

    def test_judge_responsiveness_map_module(self) -> None:
        from pipeline.seats.judge.types import ResponsivenessMap

        assert ResponsivenessMap.__module__ == "pipeline.seats.judge.types"


# ---------------------------------------------------------------------------
# JudgeContextView shape
# ---------------------------------------------------------------------------


class TestJudgeContextView:
    def _ok_view(self) -> "JudgeContextView":
        from pipeline.seats.red_team.judge_view import JudgeContextView

        return JudgeContextView(
            run_id="run-1",
            rubric_hash="a" * 64,
            total_score=85,
            max_score=100,
            recommendation="competitive",
            overall_notes="Solid effort.",
        )

    def test_constructs_with_required_fields(self) -> None:
        v = self._ok_view()
        assert v.total_score == 85

    def test_empty_run_id_rejected(self) -> None:
        from pipeline.seats.red_team.judge_view import JudgeContextView

        with pytest.raises(ValueError, match="run_id"):
            JudgeContextView(
                run_id="",
                rubric_hash="a" * 64,
                total_score=85,
                max_score=100,
                recommendation="competitive",
                overall_notes="x",
            )

    def test_empty_rubric_hash_rejected(self) -> None:
        from pipeline.seats.red_team.judge_view import JudgeContextView

        with pytest.raises(ValueError, match="rubric_hash"):
            JudgeContextView(
                run_id="r",
                rubric_hash="",
                total_score=85,
                max_score=100,
                recommendation="competitive",
                overall_notes="x",
            )

    def test_negative_total_score_rejected(self) -> None:
        from pipeline.seats.red_team.judge_view import JudgeContextView

        with pytest.raises(ValueError, match="total_score"):
            JudgeContextView(
                run_id="r",
                rubric_hash="a" * 64,
                total_score=-1,
                max_score=100,
                recommendation="competitive",
                overall_notes="x",
            )

    def test_total_exceeds_max_rejected(self) -> None:
        from pipeline.seats.red_team.judge_view import JudgeContextView

        with pytest.raises(ValueError, match="total_score"):
            JudgeContextView(
                run_id="r",
                rubric_hash="a" * 64,
                total_score=120,
                max_score=100,
                recommendation="competitive",
                overall_notes="x",
            )

    def test_overall_notes_at_truncation_cap_accepted(self) -> None:
        from pipeline.seats.red_team.judge_view import (
            OVERALL_NOTES_TRUNCATION_CHARS,
            JudgeContextView,
        )

        v = JudgeContextView(
            run_id="r",
            rubric_hash="a" * 64,
            total_score=85,
            max_score=100,
            recommendation="competitive",
            overall_notes="A" * OVERALL_NOTES_TRUNCATION_CHARS,
        )
        assert len(v.overall_notes) == OVERALL_NOTES_TRUNCATION_CHARS

    def test_overall_notes_above_cap_rejected(self) -> None:
        from pipeline.seats.red_team.judge_view import (
            OVERALL_NOTES_TRUNCATION_CHARS,
            JudgeContextView,
        )

        with pytest.raises(ValueError, match="overall_notes"):
            JudgeContextView(
                run_id="r",
                rubric_hash="a" * 64,
                total_score=85,
                max_score=100,
                recommendation="competitive",
                overall_notes="A" * (OVERALL_NOTES_TRUNCATION_CHARS + 1),
            )

    def test_truncation_constant_canonical(self) -> None:
        from pipeline.seats.red_team.judge_view import OVERALL_NOTES_TRUNCATION_CHARS

        assert OVERALL_NOTES_TRUNCATION_CHARS == 400

    def test_is_frozen(self) -> None:
        v = self._ok_view()
        with pytest.raises((AttributeError, Exception)):
            v.total_score = 99  # type: ignore[misc]

    def test_zero_max_score_rejected(self) -> None:
        from pipeline.seats.red_team.judge_view import JudgeContextView

        with pytest.raises(ValueError, match="max_score"):
            JudgeContextView(
                run_id="r",
                rubric_hash="a" * 64,
                total_score=0,
                max_score=0,
                recommendation="competitive",
                overall_notes="x",
            )

    def test_recommendation_accepts_any_str(self) -> None:
        # Judge's recommendation vocabulary may differ from Red Team's
        # closed set; the view accepts any non-empty str.
        from pipeline.seats.red_team.judge_view import JudgeContextView

        v = JudgeContextView(
            run_id="r",
            rubric_hash="a" * 64,
            total_score=85,
            max_score=100,
            recommendation="some_recommendation_string",
            overall_notes="x",
        )
        assert v.recommendation == "some_recommendation_string"


# ---------------------------------------------------------------------------
# view_from_judge_verdict adapter
# ---------------------------------------------------------------------------


class _FakeJudgeOutput:
    def __init__(self, total_score: int = 85, max_total: int = 100) -> None:
        self.total_score = total_score
        self.max_total = max_total
        self.rubric_sha256 = "f" * 64


class _FakeResponsivenessMap:
    def __init__(self) -> None:
        self.entries: tuple = ()


class _FakeJudgeVerdict:
    def __init__(self, total_score: int = 85, max_total: int = 100) -> None:
        self.judge_output = _FakeJudgeOutput(total_score, max_total)
        self.rubric_program_code = "vapg_fy26"
        self.responsiveness_map = _FakeResponsivenessMap()


class TestViewFromJudgeVerdict:
    def test_adapter_constructs_view(self) -> None:
        from pipeline.seats.red_team.judge_view import view_from_judge_verdict

        v = view_from_judge_verdict(
            _FakeJudgeVerdict(total_score=85),
            run_id="run-x",
            recommendation="competitive",
            overall_notes="Solid effort.",
        )
        assert v.total_score == 85
        assert v.run_id == "run-x"
        assert v.rubric_hash == "f" * 64

    def test_adapter_truncates_long_notes(self) -> None:
        from pipeline.seats.red_team.judge_view import (
            OVERALL_NOTES_TRUNCATION_CHARS,
            view_from_judge_verdict,
        )

        long_notes = "X" * (OVERALL_NOTES_TRUNCATION_CHARS + 200)
        v = view_from_judge_verdict(
            _FakeJudgeVerdict(),
            run_id="r",
            recommendation="competitive",
            overall_notes=long_notes,
        )
        assert len(v.overall_notes) == OVERALL_NOTES_TRUNCATION_CHARS

    def test_adapter_accepts_short_notes(self) -> None:
        from pipeline.seats.red_team.judge_view import view_from_judge_verdict

        v = view_from_judge_verdict(
            _FakeJudgeVerdict(),
            run_id="r",
            recommendation="competitive",
            overall_notes="brief",
        )
        assert v.overall_notes == "brief"

    def test_adapter_passes_rubric_hash_through(self) -> None:
        from pipeline.seats.red_team.judge_view import view_from_judge_verdict

        v = view_from_judge_verdict(
            _FakeJudgeVerdict(),
            run_id="r",
            recommendation="marginal",
            overall_notes="x",
        )
        assert v.rubric_hash == "f" * 64

    def test_adapter_passes_total_and_max_through(self) -> None:
        from pipeline.seats.red_team.judge_view import view_from_judge_verdict

        v = view_from_judge_verdict(
            _FakeJudgeVerdict(total_score=72, max_total=140),
            run_id="r",
            recommendation="not_ready",
            overall_notes="x",
        )
        assert v.total_score == 72
        assert v.max_score == 140

    def test_adapter_with_real_judge_verdict_shape(self) -> None:
        """Real-shape integration: construct a Judge JudgeVerdict and adapt."""
        from datetime import datetime, timezone

        from pipeline.seats.judge.types import (
            CriterionScore,
            JudgeOutput,
            JudgeVerdict,
            ResponsivenessMap,
        )
        from pipeline.seats.red_team.judge_view import view_from_judge_verdict

        cs = CriterionScore(
            criterion_id="need",
            score=12,
            evidence_quote="organic mango buyers exceed supply",
            confidence=0.85,
            rationale="solid framing",
        )
        jo = JudgeOutput(
            criterion_scores=(cs,),
            total_score=12,
            max_total=15,
            rubric_sha256="b" * 64,
            rfa_content_sha3_512="c" * 128,
            scored_at_utc=datetime.now(tz=timezone.utc),
        )
        jv = JudgeVerdict(
            judge_output=jo,
            rubric_program_code="vapg",
            responsiveness_map=ResponsivenessMap(entries=()),
            assembled_at_utc=datetime.now(tz=timezone.utc),
        )
        v = view_from_judge_verdict(
            jv,
            run_id="r-real",
            recommendation="marginal",
            overall_notes="real-shape integration",
        )
        assert v.run_id == "r-real"
        assert v.rubric_hash == "b" * 64
        assert v.total_score == 12
        assert v.max_score == 15


# ---------------------------------------------------------------------------
# Cross-rubric dispatch
# ---------------------------------------------------------------------------


class _FakeSubCriterion:
    def __init__(self, id_: str, name: str, max_points: int) -> None:
        self.id = id_
        self.name = name
        self.max_points = max_points


class _FakeCriterion:
    def __init__(
        self,
        id_: str,
        name: str,
        max_points: int,
        subcriteria: tuple = (),
    ) -> None:
        self.id = id_
        self.name = name
        self.max_points = max_points
        self.subcriteria = subcriteria


class _FakeRubric:
    def __init__(self, criteria: tuple) -> None:
        self.rubric_id = "vapg"
        self.criteria = criteria


class TestSelectScoringTargets:
    def test_flat_rubric_parent_only(self) -> None:
        from pipeline.seats.red_team.cross_rubric_dispatch import select_scoring_targets

        rubric = _FakeRubric(
            criteria=(
                _FakeCriterion("need", "Need", 15),
                _FakeCriterion("market", "Market", 20),
            )
        )
        targets = select_scoring_targets(
            rubric=rubric, judge_scored_ids=frozenset({"need", "market"})
        )
        assert targets == (("need", "Need", 15), ("market", "Market", 20))

    def test_hierarchical_rubric_subcriteria(self) -> None:
        from pipeline.seats.red_team.cross_rubric_dispatch import select_scoring_targets

        rubric = _FakeRubric(
            criteria=(
                _FakeCriterion(
                    "feasibility",
                    "Feasibility",
                    30,
                    subcriteria=(
                        _FakeSubCriterion("feasibility.tech", "Tech", 10),
                        _FakeSubCriterion("feasibility.market", "Market", 10),
                        _FakeSubCriterion("feasibility.ops", "Ops", 10),
                    ),
                ),
            )
        )
        targets = select_scoring_targets(
            rubric=rubric,
            judge_scored_ids=frozenset(
                {"feasibility.tech", "feasibility.market", "feasibility.ops"}
            ),
        )
        ids = [t[0] for t in targets]
        assert ids == ["feasibility.tech", "feasibility.market", "feasibility.ops"]

    def test_partial_subcriteria_only_returns_scored_subs(self) -> None:
        from pipeline.seats.red_team.cross_rubric_dispatch import select_scoring_targets

        rubric = _FakeRubric(
            criteria=(
                _FakeCriterion(
                    "feasibility",
                    "F",
                    30,
                    subcriteria=(
                        _FakeSubCriterion("feasibility.tech", "T", 10),
                        _FakeSubCriterion("feasibility.market", "M", 10),
                    ),
                ),
            )
        )
        targets = select_scoring_targets(
            rubric=rubric,
            judge_scored_ids=frozenset({"feasibility.tech"}),  # only one
        )
        assert targets == (("feasibility.tech", "T", 10),)

    def test_unknown_id_in_judge_set_raises(self) -> None:
        from pipeline.seats.red_team.cross_rubric_dispatch import select_scoring_targets

        rubric = _FakeRubric(
            criteria=(_FakeCriterion("need", "N", 10),)
        )
        with pytest.raises(ValueError, match="not in rubric"):
            select_scoring_targets(
                rubric=rubric,
                judge_scored_ids=frozenset({"need", "ghost_id"}),
            )

    def test_empty_judge_set_returns_empty(self) -> None:
        from pipeline.seats.red_team.cross_rubric_dispatch import select_scoring_targets

        rubric = _FakeRubric(criteria=(_FakeCriterion("need", "N", 10),))
        targets = select_scoring_targets(rubric=rubric, judge_scored_ids=frozenset())
        assert targets == ()

    def test_judge_scored_ids_set_coerced(self) -> None:
        # Caller passes plain set; function coerces to frozenset.
        from pipeline.seats.red_team.cross_rubric_dispatch import select_scoring_targets

        rubric = _FakeRubric(criteria=(_FakeCriterion("need", "N", 10),))
        targets = select_scoring_targets(
            rubric=rubric, judge_scored_ids=frozenset({"need"})
        )
        assert targets == (("need", "N", 10),)

    def test_mixed_parent_and_subcriteria(self) -> None:
        from pipeline.seats.red_team.cross_rubric_dispatch import select_scoring_targets

        rubric = _FakeRubric(
            criteria=(
                _FakeCriterion("need", "Need", 15),  # flat
                _FakeCriterion(
                    "feasibility",
                    "F",
                    30,
                    subcriteria=(
                        _FakeSubCriterion("feasibility.tech", "T", 10),
                    ),
                ),
            )
        )
        targets = select_scoring_targets(
            rubric=rubric,
            judge_scored_ids=frozenset({"need", "feasibility.tech"}),
        )
        # Flat criterion + subcriterion of hierarchical criterion
        assert ("need", "Need", 15) in targets
        assert ("feasibility.tech", "T", 10) in targets


class TestAssertRedTeamIdSetMatchesJudge:
    def test_identical_sets_pass(self) -> None:
        from pipeline.seats.red_team.cross_rubric_dispatch import (
            assert_red_team_id_set_matches_judge,
        )

        v = assert_red_team_id_set_matches_judge(
            red_team_scored_ids=frozenset({"need", "market"}),
            judge_scored_ids=frozenset({"need", "market"}),
        )
        assert v == ()

    def test_red_team_missing_id(self) -> None:
        from pipeline.seats.red_team.cross_rubric_dispatch import (
            assert_red_team_id_set_matches_judge,
        )

        v = assert_red_team_id_set_matches_judge(
            red_team_scored_ids=frozenset({"need"}),
            judge_scored_ids=frozenset({"need", "market"}),
        )
        assert any("F-RT-CRITERION-MISSING" in vv for vv in v)
        assert any("market" in vv for vv in v)

    def test_red_team_extra_id(self) -> None:
        from pipeline.seats.red_team.cross_rubric_dispatch import (
            assert_red_team_id_set_matches_judge,
        )

        v = assert_red_team_id_set_matches_judge(
            red_team_scored_ids=frozenset({"need", "market", "ghost"}),
            judge_scored_ids=frozenset({"need", "market"}),
        )
        assert any("F-RT-CRITERION-MISSING" in vv for vv in v)
        assert any("ghost" in vv for vv in v)

    def test_both_missing_and_extra(self) -> None:
        from pipeline.seats.red_team.cross_rubric_dispatch import (
            assert_red_team_id_set_matches_judge,
        )

        v = assert_red_team_id_set_matches_judge(
            red_team_scored_ids=frozenset({"need", "ghost"}),
            judge_scored_ids=frozenset({"need", "market"}),
        )
        # Two violation strings expected
        assert len(v) == 2

    def test_set_coercion(self) -> None:
        from pipeline.seats.red_team.cross_rubric_dispatch import (
            assert_red_team_id_set_matches_judge,
        )

        # Pass plain frozensets; ensure coerce-and-compare works.
        v = assert_red_team_id_set_matches_judge(
            red_team_scored_ids=frozenset({"need"}),
            judge_scored_ids=frozenset({"need"}),
        )
        assert v == ()
