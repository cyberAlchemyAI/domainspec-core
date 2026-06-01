"""Tests for ``pipeline.logician.gates.f_report_template_mismatch``.

Per §14.9.5 Cycle 1 + Cycle 2 closures (RT-5a/5b/5c + RT-C2-04/05).
"""
from __future__ import annotations

import pytest

from pipeline.logician.gates._report_protocols import (
    ReportingTemplateSnapshot,
    WorkspacePublishedTemplateSnapshot,
)
from pipeline.logician.gates.f_report_template_mismatch import (
    F_REPORT_TEMPLATE_MISMATCH,
    SUB_TAG_OPERATOR_KEY_VERSION_MISMATCH,
    SUB_TAG_PERIOD_CADENCE_ACTUAL_DRIFT,
    SUB_TAG_PERIOD_CADENCE_INVALID,
    SUB_TAG_SCHEMA_REQUIRED_FIELDS_UNSPECIFIED,
    SUB_TAG_SCHEMA_REQUIRED_SUB_SECTIONS_UNRECOGNIZED,
    SUB_TAG_TEMPLATE_SIGNATURE_INVALID,
    SUB_TAG_WORKSPACE_PUBLISHED_TEMPLATE_ABSENT,
    SUB_TAG_WORKSPACE_PUBLISHED_TEMPLATE_ABSENT_FIRST_WAVE,
    SUB_TAG_WORKSPACE_PUBLISHED_TEMPLATE_DRIFT,
    SUB_TAG_WORKSPACE_PUBLISHED_TEMPLATE_MARKER_TAMPERED,
    check_template_mismatch,
)


def _good_template():
    return ReportingTemplateSnapshot(
        funder_id="VAPG",
        template_version="v1",
        template_captured_at_utc="2026-05-01",
        template_content_sha3_512="a" * 128,
        required_sub_sections=("narrative", "metrics_table"),
        required_fields_per_sub_section={
            "narrative": ({"field": "accomplishments"},),
            "metrics_table": ({"field": "outcome_metrics"},),
        },
        required_period_cadence="quarterly",
        report_due_n_days_after_period_end=30,
    )


class TestHappyPath:
    def test_clean_no_workspace_passes_with_advisory(self):
        r = check_template_mismatch(
            operator_template=_good_template(),
            workspace_published=None,
        )
        assert r.success
        # Advisory: workspace_published_template_absent (non-first-wave)
        assert SUB_TAG_WORKSPACE_PUBLISHED_TEMPLATE_ABSENT in r.fired_sub_tags

    def test_matching_workspace_hash_passes(self):
        r = check_template_mismatch(
            operator_template=_good_template(),
            workspace_published=WorkspacePublishedTemplateSnapshot(
                funder_id="VAPG", present=True,
                content_sha3_512="a" * 128, first_wave=False,
            ),
        )
        assert r.success
        assert r.fired_sub_tags == ()


class TestSchemaSubSections:
    def test_unrecognized_subsection_fires(self):
        t = ReportingTemplateSnapshot(
            funder_id="VAPG", template_version="v1",
            template_captured_at_utc="t", template_content_sha3_512="a" * 128,
            required_sub_sections=("narrative", "not_a_real_subsec"),
            required_fields_per_sub_section={"narrative": ({"field": "x"},)},
            required_period_cadence="quarterly",
            report_due_n_days_after_period_end=30,
        )
        r = check_template_mismatch(operator_template=t, workspace_published=None)
        assert not r.success
        assert SUB_TAG_SCHEMA_REQUIRED_SUB_SECTIONS_UNRECOGNIZED in r.fired_sub_tags

    def test_unspecified_fields_fires(self):
        t = ReportingTemplateSnapshot(
            funder_id="VAPG", template_version="v1",
            template_captured_at_utc="t", template_content_sha3_512="a" * 128,
            required_sub_sections=("narrative",),
            required_fields_per_sub_section={"narrative": ()},  # empty
            required_period_cadence="quarterly",
            report_due_n_days_after_period_end=30,
        )
        r = check_template_mismatch(operator_template=t, workspace_published=None)
        assert not r.success
        assert SUB_TAG_SCHEMA_REQUIRED_FIELDS_UNSPECIFIED in r.fired_sub_tags


class TestPeriodCadence:
    def test_invalid_cadence_fires(self):
        t = ReportingTemplateSnapshot(
            funder_id="VAPG", template_version="v1",
            template_captured_at_utc="t", template_content_sha3_512="a" * 128,
            required_sub_sections=("narrative",),
            required_fields_per_sub_section={"narrative": ({"field": "x"},)},
            required_period_cadence="weekly",  # invalid
            report_due_n_days_after_period_end=30,
        )
        r = check_template_mismatch(operator_template=t, workspace_published=None)
        assert not r.success
        assert SUB_TAG_PERIOD_CADENCE_INVALID in r.fired_sub_tags

    def test_actual_cadence_drift_advisory(self):
        r = check_template_mismatch(
            operator_template=_good_template(),  # quarterly = 3 months
            workspace_published=None,
            actual_period_cadence_months=4,  # mismatch
        )
        assert SUB_TAG_PERIOD_CADENCE_ACTUAL_DRIFT in r.fired_sub_tags
        # Advisory only; gate may still pass
        assert r.success


class TestTemplateSignature:
    def test_signature_present_invalid_fires(self):
        t = ReportingTemplateSnapshot(
            funder_id="VAPG", template_version="v1",
            template_captured_at_utc="t", template_content_sha3_512="a" * 128,
            required_sub_sections=("narrative",),
            required_fields_per_sub_section={"narrative": ({"field": "x"},)},
            required_period_cadence="quarterly",
            report_due_n_days_after_period_end=30,
            template_signature_present=True,
            template_signature_valid=False,
        )
        r = check_template_mismatch(operator_template=t, workspace_published=None)
        assert not r.success
        assert SUB_TAG_TEMPLATE_SIGNATURE_INVALID in r.fired_sub_tags


class TestOperatorKeyRotation:
    def test_key_version_mismatch_fires(self):
        t = ReportingTemplateSnapshot(
            funder_id="VAPG", template_version="v1",
            template_captured_at_utc="t", template_content_sha3_512="a" * 128,
            required_sub_sections=("narrative",),
            required_fields_per_sub_section={"narrative": ({"field": "x"},)},
            required_period_cadence="quarterly",
            report_due_n_days_after_period_end=30,
            operator_key_version="v1",
        )
        r = check_template_mismatch(
            operator_template=t, workspace_published=None,
            operator_pinned_key_version="v2",
        )
        assert not r.success
        assert SUB_TAG_OPERATOR_KEY_VERSION_MISMATCH in r.fired_sub_tags


class TestWorkspacePublishedDrift:
    def test_hash_drift_fires(self):
        r = check_template_mismatch(
            operator_template=_good_template(),
            workspace_published=WorkspacePublishedTemplateSnapshot(
                funder_id="VAPG", present=True,
                content_sha3_512="b" * 128, first_wave=False,
            ),
        )
        assert not r.success
        assert SUB_TAG_WORKSPACE_PUBLISHED_TEMPLATE_DRIFT in r.fired_sub_tags


class TestFirstWaveAbsenceMarkerTamper:
    def test_first_wave_absent_fires_failclosed(self):
        r = check_template_mismatch(
            operator_template=_good_template(),
            workspace_published=WorkspacePublishedTemplateSnapshot(
                funder_id="VAPG", present=False, first_wave=True,
            ),
        )
        assert not r.success
        assert SUB_TAG_WORKSPACE_PUBLISHED_TEMPLATE_ABSENT_FIRST_WAVE in r.fired_sub_tags

    def test_non_first_wave_absent_advisory(self):
        r = check_template_mismatch(
            operator_template=_good_template(),
            workspace_published=WorkspacePublishedTemplateSnapshot(
                funder_id="VAPG", present=False, first_wave=False,
            ),
        )
        assert r.success
        assert SUB_TAG_WORKSPACE_PUBLISHED_TEMPLATE_ABSENT in r.fired_sub_tags

    def test_first_wave_marker_sig_invalid_fires(self):
        r = check_template_mismatch(
            operator_template=_good_template(),
            workspace_published=WorkspacePublishedTemplateSnapshot(
                funder_id="VAPG", present=True,
                content_sha3_512="a" * 128, first_wave=True,
                first_wave_marker_signature_valid=False,
                first_wave_marker_hash_bound_to_lock_history=True,
            ),
        )
        assert not r.success
        assert SUB_TAG_WORKSPACE_PUBLISHED_TEMPLATE_MARKER_TAMPERED in r.fired_sub_tags

    def test_first_wave_marker_hash_not_bound_fires(self):
        r = check_template_mismatch(
            operator_template=_good_template(),
            workspace_published=WorkspacePublishedTemplateSnapshot(
                funder_id="VAPG", present=True,
                content_sha3_512="a" * 128, first_wave=True,
                first_wave_marker_signature_valid=True,
                first_wave_marker_hash_bound_to_lock_history=False,
            ),
        )
        assert not r.success
        assert SUB_TAG_WORKSPACE_PUBLISHED_TEMPLATE_MARKER_TAMPERED in r.fired_sub_tags
