"""Tests for §14.6.2 metrics_table sub-section composer."""

from __future__ import annotations

from decimal import Decimal

import pytest

from pipeline.orchestrator.seats.report_generator.composers._base import ComposerError
from pipeline.orchestrator.seats.report_generator.composers.metrics_table import (
    MetricsTableDeps,
    MetricsTableResult,
    compose_metrics_table,
)


def _registry(*, with_float: bool = False):
    actual = 50.0 if with_float else "50"
    return {
        ("operational_data", "metrics"): [
            {
                "metric_id": "M-001",
                "source_path": "orgs/myorg/vault/operational/grants/G1/period_1/metrics/workshops.yaml",
                "metric_name": "workshops_delivered",
                "actual": actual,
                "unit": "count",
                "content_sha3_512": "a" * 128,
                "related_commitment_id": "COMMIT-001",
                "related_evaluation_field": "workshops_delivered",
            }
        ],
        ("kfr", None): [
            {
                "metric_name": "workshops_delivered",
                "kfr_value": "50",
                "kfr_unit": "count",
                "source_path": "orgs/myorg/vault/kfr/register.yaml",
                "source_row_id": "KFR-WORKSHOPS",
                "source_content_sha3_512": "b" * 128,
                "atomic_snapshot_id": "SNAP-001",
            }
        ],
        ("proposal_commitments", None): [
            {
                "commitment_id": "COMMIT-001",
                "field_name": "workshops_delivered",
                "target": "50",
                "tolerance": "0",
                "scope_tags_at_commitment": ["workforce_training"],
            }
        ],
        ("reporting_template", None): [
            {
                "field_name": "outcome_metrics",
                "column_specs": [
                    {"name": "metric_name", "required": True},
                    {"name": "target", "required": True},
                    {"name": "actual", "required": True},
                ],
            }
        ],
    }


def _make_deps(*, fixed_clock, hash_bytes, make_read_intent, make_scribe, with_float=False):
    reg = _registry(with_float=with_float)
    return MetricsTableDeps(
        read_metrics=make_read_intent(reg),
        read_kfr_metrics=make_read_intent(reg),
        read_commitment_targets=make_read_intent(reg),
        read_template_field_specs=make_read_intent(reg),
        scribe=make_scribe(),
        clock=fixed_clock,
        hash_bytes=hash_bytes,
    )


class TestComposeMetricsTable:
    def test_happy_path(
        self, fixed_clock, hash_bytes, make_read_intent, make_scribe
    ):
        deps = _make_deps(
            fixed_clock=fixed_clock,
            hash_bytes=hash_bytes,
            make_read_intent=make_read_intent,
            make_scribe=make_scribe,
        )
        r = compose_metrics_table(
            deps=deps,
            org_slug="myorg",
            grant_id="G1",
            period_n=1,
            operational_data_root="orgs/myorg/vault/operational/grants/G1/period_1",
            proposal_commitments_path="x",
            reporting_template_path="y",
            kfr_register_path="z",
        )
        assert isinstance(r, MetricsTableResult)
        assert r.rows_authored == 1
        assert len(r.claims) == 1
        c = r.claims[0]
        assert c.sub_section == "metrics_table"
        assert c.claim_kind == "numeric"
        assert len(c.sources) == 2  # operational_data + kfr
        assert c.sources[0].kind == "operational_data"
        assert c.sources[1].kind == "kfr"
        assert "workshops_delivered" in r.markdown_fragment

    def test_float_actual_rejected_decimal_mandate(
        self, fixed_clock, hash_bytes, make_read_intent, make_scribe
    ):
        deps = _make_deps(
            fixed_clock=fixed_clock,
            hash_bytes=hash_bytes,
            make_read_intent=make_read_intent,
            make_scribe=make_scribe,
            with_float=True,
        )
        with pytest.raises(ComposerError) as exc:
            compose_metrics_table(
                deps=deps,
                org_slug="myorg",
                grant_id="G1",
                period_n=1,
                operational_data_root="x",
                proposal_commitments_path="y",
                reporting_template_path="z",
                kfr_register_path="w",
            )
        assert "float" in str(exc.value).lower() or "decimal" in str(exc.value).lower()

    def test_no_metrics_raises(
        self, fixed_clock, hash_bytes, make_read_intent, make_scribe
    ):
        reg = {
            ("operational_data", "metrics"): [],
            ("kfr", None): [],
            ("proposal_commitments", None): [],
            ("reporting_template", None): [],
        }
        deps = MetricsTableDeps(
            read_metrics=make_read_intent(reg),
            read_kfr_metrics=make_read_intent(reg),
            read_commitment_targets=make_read_intent(reg),
            read_template_field_specs=make_read_intent(reg),
            scribe=make_scribe(),
            clock=fixed_clock,
            hash_bytes=hash_bytes,
        )
        with pytest.raises(ComposerError):
            compose_metrics_table(
                deps=deps,
                org_slug="myorg",
                grant_id="G1",
                period_n=1,
                operational_data_root="x",
                proposal_commitments_path="y",
                reporting_template_path="z",
                kfr_register_path="w",
            )

    def test_decimal_source_value_in_ref(
        self, fixed_clock, hash_bytes, make_read_intent, make_scribe
    ):
        deps = _make_deps(
            fixed_clock=fixed_clock,
            hash_bytes=hash_bytes,
            make_read_intent=make_read_intent,
            make_scribe=make_scribe,
        )
        r = compose_metrics_table(
            deps=deps,
            org_slug="myorg",
            grant_id="G1",
            period_n=1,
            operational_data_root="x",
            proposal_commitments_path="y",
            reporting_template_path="z",
            kfr_register_path="w",
        )
        op_ref = r.claims[0].sources[0]
        assert isinstance(op_ref.source_value, Decimal)
        assert op_ref.source_value == Decimal("50")
