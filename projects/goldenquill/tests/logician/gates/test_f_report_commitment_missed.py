"""Tests for ``pipeline.logician.gates.f_report_commitment_missed``.

Per §14.9.2 Cycle 1 + Cycle 2 closures (RT-2a/2b/2c + RT-C2-02).
"""
from __future__ import annotations

import pytest

from pipeline.logician.gates._report_protocols import (
    PromotedCommitmentRow,
    WaiverRecord,
)
from pipeline.logician.gates.f_report_commitment_missed import (
    F_REPORT_COMMITMENT_MISSED,
    SUB_TAG_COMMITMENT_EVALUATION_CRITERION_UNADDRESSED,
    SUB_TAG_COMMITMENT_ID_INVALID_FORMAT,
    SUB_TAG_COMMITMENT_PERIOD_N_NOT_DUE_YET,
    SUB_TAG_COMMITMENT_REQUIRED_SUBSECTION_MISSING,
    SUB_TAG_COMMITMENT_WAIVER_CAP_EXCEEDED,
    SUB_TAG_COMMITMENT_WAIVER_UNSIGNED,
    SUB_TAG_EMPTY_PROMOTED_SET,
    check_commitment_missed,
)


def _row(commitment_id, scope_tags=("a",), required_sub_sections=("narrative",),
         evaluation_criteria=(), period_n_window=None):
    return PromotedCommitmentRow(
        commitment_id=commitment_id,
        status="PROMOTED",
        scope_tags=scope_tags,
        required_sub_sections=required_sub_sections,
        evaluation_criteria=evaluation_criteria,
        period_n_window=period_n_window,
    )


class TestEmptyPromotedSet:
    def test_empty_set_fires_pre_pre_dispatch(self):
        r = check_commitment_missed(
            promoted_commitments=[], sub_sections_in_scope=("narrative",),
            sub_sections_authored=("narrative",), period_n=1,
            claim_commitment_links={}, addressed_criteria={}, waivers={},
        )
        assert not r.success
        assert r.fired_sub_tags == (SUB_TAG_EMPTY_PROMOTED_SET,)


class TestCommitmentIdInvalidFormat:
    def test_lowercase_commitment_id_fires(self):
        r = check_commitment_missed(
            promoted_commitments=[_row("lowercase")],
            sub_sections_in_scope=("narrative",),
            sub_sections_authored=("narrative",), period_n=1,
            claim_commitment_links={}, addressed_criteria={}, waivers={},
        )
        assert not r.success
        assert SUB_TAG_COMMITMENT_ID_INVALID_FORMAT in r.fired_sub_tags

    def test_path_traversal_commitment_id_fires(self):
        r = check_commitment_missed(
            promoted_commitments=[_row("../etc/passwd")],
            sub_sections_in_scope=("narrative",),
            sub_sections_authored=("narrative",), period_n=1,
            claim_commitment_links={}, addressed_criteria={}, waivers={},
        )
        assert not r.success
        assert SUB_TAG_COMMITMENT_ID_INVALID_FORMAT in r.fired_sub_tags


class TestRequiredSubsectionMissing:
    def test_required_subsection_not_authored_fires(self):
        r = check_commitment_missed(
            promoted_commitments=[_row("COMMIT-001", required_sub_sections=("metrics_table",))],
            sub_sections_in_scope=("metrics_table", "narrative"),
            sub_sections_authored=("narrative",),  # metrics_table NOT authored
            period_n=1,
            claim_commitment_links={"COMMIT-001": ("narrative",)},
            addressed_criteria={"COMMIT-001": frozenset()},
            waivers={},
        )
        assert not r.success
        assert SUB_TAG_COMMITMENT_REQUIRED_SUBSECTION_MISSING in r.fired_sub_tags


class TestEvaluationCriterionUnaddressed:
    def test_numeric_criterion_unaddressed_fires(self):
        crit = {"kind": "numeric", "field": "workshops_delivered", "target": 50}
        r = check_commitment_missed(
            promoted_commitments=[
                _row("COMMIT-001", evaluation_criteria=(crit,))
            ],
            sub_sections_in_scope=("narrative",),
            sub_sections_authored=("narrative",), period_n=1,
            claim_commitment_links={"COMMIT-001": ("narrative",)},
            addressed_criteria={"COMMIT-001": frozenset()},  # no field addressed
            waivers={},
        )
        assert not r.success
        assert SUB_TAG_COMMITMENT_EVALUATION_CRITERION_UNADDRESSED in r.fired_sub_tags

    def test_criterion_addressed_passes(self):
        crit = {"kind": "numeric", "field": "workshops_delivered", "target": 50}
        r = check_commitment_missed(
            promoted_commitments=[
                _row("COMMIT-001", evaluation_criteria=(crit,))
            ],
            sub_sections_in_scope=("narrative",),
            sub_sections_authored=("narrative",), period_n=1,
            claim_commitment_links={"COMMIT-001": ("narrative",)},
            addressed_criteria={"COMMIT-001": frozenset({"workshops_delivered"})},
            waivers={},
        )
        assert r.success


class TestPeriodNotDueYet:
    def test_future_window_without_waiver_fires(self):
        r = check_commitment_missed(
            promoted_commitments=[_row("COMMIT-001", period_n_window=(2, 4))],
            sub_sections_in_scope=("narrative",),
            sub_sections_authored=("narrative",), period_n=1,
            claim_commitment_links={},
            addressed_criteria={},
            waivers={},
        )
        assert not r.success
        assert SUB_TAG_COMMITMENT_PERIOD_N_NOT_DUE_YET in r.fired_sub_tags

    def test_signed_waiver_suppresses(self):
        r = check_commitment_missed(
            promoted_commitments=[
                _row("COMMIT-001", period_n_window=(2, 4)),
                _row("COMMIT-002"),
            ],
            sub_sections_in_scope=("narrative",),
            sub_sections_authored=("narrative",), period_n=1,
            claim_commitment_links={"COMMIT-002": ("narrative",)},
            addressed_criteria={"COMMIT-002": frozenset()},
            waivers={"COMMIT-001": WaiverRecord(
                commitment_id="COMMIT-001",
                waiver_reason="period_2_not_started",
                waiver_signed_at_utc="t",
                signature_valid=True,
            )},
        )
        assert r.success

    def test_unsigned_waiver_fires(self):
        r = check_commitment_missed(
            promoted_commitments=[
                _row("COMMIT-001", period_n_window=(2, 4)),
                _row("COMMIT-002"),
            ],
            sub_sections_in_scope=("narrative",),
            sub_sections_authored=("narrative",), period_n=1,
            claim_commitment_links={"COMMIT-002": ("narrative",)},
            addressed_criteria={"COMMIT-002": frozenset()},
            waivers={"COMMIT-001": WaiverRecord(
                commitment_id="COMMIT-001",
                waiver_reason="x",
                waiver_signed_at_utc="t",
                signature_valid=False,
            )},
        )
        assert not r.success
        assert SUB_TAG_COMMITMENT_WAIVER_UNSIGNED in r.fired_sub_tags


class TestWaiverCap:
    def test_waiver_cap_exceeded_fires(self):
        # Two commitments — cap is 1 (len - 1). Try to waive both.
        r = check_commitment_missed(
            promoted_commitments=[
                _row("COMMIT-001", period_n_window=(2, 4)),
                _row("COMMIT-002", period_n_window=(2, 4)),
            ],
            sub_sections_in_scope=("narrative",),
            sub_sections_authored=("narrative",), period_n=1,
            claim_commitment_links={},
            addressed_criteria={},
            waivers={
                "COMMIT-001": WaiverRecord(
                    commitment_id="COMMIT-001", waiver_reason="x",
                    waiver_signed_at_utc="t", signature_valid=True,
                ),
                "COMMIT-002": WaiverRecord(
                    commitment_id="COMMIT-002", waiver_reason="x",
                    waiver_signed_at_utc="t", signature_valid=True,
                ),
            },
        )
        assert not r.success
        assert SUB_TAG_COMMITMENT_WAIVER_CAP_EXCEEDED in r.fired_sub_tags


class TestHappyPath:
    def test_full_addressing_passes(self):
        crit = {"kind": "numeric", "field": "workshops_delivered", "target": 50}
        r = check_commitment_missed(
            promoted_commitments=[
                _row("COMMIT-001", required_sub_sections=("narrative", "metrics_table"),
                     evaluation_criteria=(crit,)),
            ],
            sub_sections_in_scope=("narrative", "metrics_table"),
            sub_sections_authored=("narrative", "metrics_table"),
            period_n=1,
            claim_commitment_links={"COMMIT-001": ("narrative", "metrics_table")},
            addressed_criteria={"COMMIT-001": frozenset({"workshops_delivered"})},
            waivers={},
        )
        assert r.success
        assert r.failure_code is None
