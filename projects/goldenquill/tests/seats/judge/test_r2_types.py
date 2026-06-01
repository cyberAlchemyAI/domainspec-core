"""Tests for §9 R2 type extensions — JudgeVerdict + ResponsivenessEntry +
ResponsivenessMap.

Spec card: ``pipeline/engineering/spec_cards/section_09_judge_round_2_cross_rubric_and_verdict.md``.

Covers:

- ResponsivenessEntry construction-time invariants (empty fields, empty
  factor_values tuple, non-string factor_values entries).
- ResponsivenessMap dedup invariant (duplicate (criterion_id,
  factor_name) pairs).
- JudgeVerdict construction + invariants (timestamp ordering,
  timezone-awareness, program_code non-empty).
- All shapes are frozen dataclasses with slots (rebind-resistance).
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone

import pytest

from pipeline.seats.judge.types import (
    CriterionScore,
    JudgeOutput,
    JudgeVerdict,
    ResponsivenessEntry,
    ResponsivenessMap,
)


UTC = timezone.utc
SCORED_AT = datetime(2026, 4, 29, 12, 0, 0, tzinfo=UTC)
ASSEMBLED_AT = datetime(2026, 4, 29, 12, 0, 1, tzinfo=UTC)
SHA256_VALID = "0" * 64
SHA3_512_VALID = "0" * 128


def _judge_output(**overrides) -> JudgeOutput:
    kw = dict(
        criterion_scores=(
            CriterionScore(
                criterion_id="a",
                score=10,
                evidence_quote="quote",
                confidence=0.9,
                rationale="ok",
            ),
        ),
        total_score=10,
        max_total=20,
        rubric_sha256=SHA256_VALID,
        rfa_content_sha3_512=SHA3_512_VALID,
        scored_at_utc=SCORED_AT,
    )
    kw.update(overrides)
    return JudgeOutput(**kw)


# ---------------------------------------------------------------------------
# ResponsivenessEntry
# ---------------------------------------------------------------------------


class TestResponsivenessEntry:
    def test_constructs_with_full_field_set(self):
        e = ResponsivenessEntry(
            criterion_id="f.i",
            factor_name="qualifying_categories",
            factor_values=("Beginning Farmer", "Veteran Farmer"),
        )
        assert e.criterion_id == "f.i"
        assert e.factor_name == "qualifying_categories"
        assert e.factor_values == ("Beginning Farmer", "Veteran Farmer")

    def test_single_value_accepted(self):
        e = ResponsivenessEntry(
            criterion_id="g",
            factor_name="categories",
            factor_values=("Geographic diversity",),
        )
        assert len(e.factor_values) == 1

    def test_empty_criterion_id_rejected(self):
        with pytest.raises(ValueError, match="criterion_id is empty"):
            ResponsivenessEntry(
                criterion_id="   ",
                factor_name="qualifying_categories",
                factor_values=("X",),
            )

    def test_empty_factor_name_rejected(self):
        with pytest.raises(ValueError, match="factor_name is empty"):
            ResponsivenessEntry(
                criterion_id="f.i",
                factor_name="",
                factor_values=("X",),
            )

    def test_empty_factor_values_tuple_rejected(self):
        with pytest.raises(
            ValueError, match="factor_values must be non-empty"
        ):
            ResponsivenessEntry(
                criterion_id="f.i",
                factor_name="qualifying_categories",
                factor_values=(),
            )

    def test_whitespace_factor_value_rejected(self):
        with pytest.raises(ValueError, match=r"factor_values\[1\] must be"):
            ResponsivenessEntry(
                criterion_id="f.i",
                factor_name="qualifying_categories",
                factor_values=("Real value", "   "),
            )

    def test_non_string_factor_value_rejected(self):
        with pytest.raises(ValueError, match=r"factor_values\[0\] must be"):
            ResponsivenessEntry(
                criterion_id="f.i",
                factor_name="qualifying_categories",
                factor_values=(123,),  # type: ignore[arg-type]
            )

    def test_frozen_dataclass(self):
        e = ResponsivenessEntry(
            criterion_id="f.i",
            factor_name="qualifying_categories",
            factor_values=("X",),
        )
        with pytest.raises(FrozenInstanceError):
            e.factor_name = "other"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# ResponsivenessMap
# ---------------------------------------------------------------------------


class TestResponsivenessMap:
    def test_empty_entries_accepted(self):
        m = ResponsivenessMap(entries=())
        assert m.entries == ()

    def test_single_entry_accepted(self):
        e = ResponsivenessEntry(
            criterion_id="f.i",
            factor_name="qualifying_categories",
            factor_values=("X",),
        )
        m = ResponsivenessMap(entries=(e,))
        assert m.entries == (e,)

    def test_multiple_distinct_entries_accepted(self):
        e1 = ResponsivenessEntry(
            criterion_id="f.i",
            factor_name="qualifying_categories",
            factor_values=("X",),
        )
        e2 = ResponsivenessEntry(
            criterion_id="f.ii",
            factor_name="qualifying_applicants",
            factor_values=("Y",),
        )
        m = ResponsivenessMap(entries=(e1, e2))
        assert m.entries == (e1, e2)

    def test_same_criterion_different_factor_accepted(self):
        e1 = ResponsivenessEntry(
            criterion_id="f.ii",
            factor_name="qualifying_applicants",
            factor_values=("X",),
        )
        e2 = ResponsivenessEntry(
            criterion_id="f.ii",
            factor_name="must_benefit",
            factor_values=("Y",),
        )
        m = ResponsivenessMap(entries=(e1, e2))
        assert m.entries == (e1, e2)

    def test_duplicate_criterion_factor_pair_rejected(self):
        e1 = ResponsivenessEntry(
            criterion_id="f.i",
            factor_name="qualifying_categories",
            factor_values=("X",),
        )
        e2 = ResponsivenessEntry(
            criterion_id="f.i",
            factor_name="qualifying_categories",
            factor_values=("Y",),
        )
        with pytest.raises(
            ValueError,
            match=r"duplicate \(criterion_id='f\.i'",
        ):
            ResponsivenessMap(entries=(e1, e2))

    def test_frozen_dataclass(self):
        m = ResponsivenessMap(entries=())
        with pytest.raises(FrozenInstanceError):
            m.entries = ()  # type: ignore[misc]


# ---------------------------------------------------------------------------
# JudgeVerdict
# ---------------------------------------------------------------------------


class TestJudgeVerdict:
    def test_constructs_with_full_field_set(self):
        v = JudgeVerdict(
            judge_output=_judge_output(),
            rubric_program_code="VAPG-FY26",
            responsiveness_map=ResponsivenessMap(entries=()),
            assembled_at_utc=ASSEMBLED_AT,
        )
        assert v.rubric_program_code == "VAPG-FY26"
        assert v.responsiveness_map.entries == ()
        assert v.assembled_at_utc == ASSEMBLED_AT
        assert v.judge_output.total_score == 10

    def test_assembled_equal_to_scored_at_accepted(self):
        # boundary — equal timestamps allowed (assembly and scoring on
        # same instant).
        v = JudgeVerdict(
            judge_output=_judge_output(),
            rubric_program_code="VAPG-FY26",
            responsiveness_map=ResponsivenessMap(entries=()),
            assembled_at_utc=SCORED_AT,
        )
        assert v.assembled_at_utc == SCORED_AT

    def test_empty_program_code_rejected(self):
        with pytest.raises(
            ValueError, match="rubric_program_code is empty"
        ):
            JudgeVerdict(
                judge_output=_judge_output(),
                rubric_program_code="   ",
                responsiveness_map=ResponsivenessMap(entries=()),
                assembled_at_utc=ASSEMBLED_AT,
            )

    def test_naive_assembled_at_rejected(self):
        with pytest.raises(
            ValueError, match="assembled_at_utc must be timezone-aware"
        ):
            JudgeVerdict(
                judge_output=_judge_output(),
                rubric_program_code="VAPG-FY26",
                responsiveness_map=ResponsivenessMap(entries=()),
                assembled_at_utc=datetime(2026, 4, 29, 12, 0, 1),
            )

    def test_assembled_before_scored_rejected(self):
        too_early = SCORED_AT - timedelta(seconds=1)
        with pytest.raises(
            ValueError, match="precedes judge_output.scored_at_utc"
        ):
            JudgeVerdict(
                judge_output=_judge_output(),
                rubric_program_code="VAPG-FY26",
                responsiveness_map=ResponsivenessMap(entries=()),
                assembled_at_utc=too_early,
            )

    def test_carries_responsiveness_entries(self):
        e = ResponsivenessEntry(
            criterion_id="f.i",
            factor_name="qualifying_categories",
            factor_values=("Beginning Farmer",),
        )
        v = JudgeVerdict(
            judge_output=_judge_output(),
            rubric_program_code="VAPG-FY26",
            responsiveness_map=ResponsivenessMap(entries=(e,)),
            assembled_at_utc=ASSEMBLED_AT,
        )
        assert v.responsiveness_map.entries == (e,)

    def test_frozen_dataclass(self):
        v = JudgeVerdict(
            judge_output=_judge_output(),
            rubric_program_code="VAPG-FY26",
            responsiveness_map=ResponsivenessMap(entries=()),
            assembled_at_utc=ASSEMBLED_AT,
        )
        with pytest.raises(FrozenInstanceError):
            v.rubric_program_code = "other"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Public surface (R2 additions)
# ---------------------------------------------------------------------------


class TestR2PublicSurface:
    def test_judge_verdict_imported_from_seat(self):
        from pipeline.seats.judge import JudgeVerdict as Re_export

        assert Re_export is JudgeVerdict

    def test_responsiveness_entry_imported_from_seat(self):
        from pipeline.seats.judge import (
            ResponsivenessEntry as Re_export,
        )

        assert Re_export is ResponsivenessEntry

    def test_responsiveness_map_imported_from_seat(self):
        from pipeline.seats.judge import (
            ResponsivenessMap as Re_export,
        )

        assert Re_export is ResponsivenessMap
