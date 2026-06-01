"""Tests for §14.6.3 financial_summary sub-section composer."""

from __future__ import annotations

from decimal import Decimal

import pytest

from pipeline.orchestrator.seats.report_generator.composers._base import ComposerError
from pipeline.orchestrator.seats.report_generator.composers.financial_summary import (
    FinancialSummaryDeps,
    compose_financial_summary,
)


def _registry(*, with_float: bool = False):
    actual = 12000.0 if with_float else "12000"
    return {
        ("operational_data", "financials"): [
            {
                "line_id": "LINE-001",
                "source_path": "orgs/myorg/vault/operational/grants/G1/period_1/financials/personnel.yaml",
                "budget_line": "personnel",
                "actuals": actual,
                "content_sha3_512": "a" * 128,
                "related_commitment_id": "COMMIT-001",
            }
        ],
        ("proposal_commitments", None): [
            {
                "commitment_id": "COMMIT-001",
                "budget_line": "personnel",
                "budgeted": "12500",
                "tolerance_pct": "5",
                "scope_tags_at_commitment": ["workforce_training"],
            }
        ],
        ("reporting_template", None): [
            {
                "field_name": "budget_actuals_table",
                "column_specs": [
                    {"name": "budget_line", "required": True},
                    {"name": "budgeted", "required": True},
                    {"name": "actuals", "required": True},
                ],
            }
        ],
    }


def _make_deps(*, fixed_clock, hash_bytes, make_read_intent, make_scribe, with_float=False):
    reg = _registry(with_float=with_float)
    return FinancialSummaryDeps(
        read_financials=make_read_intent(reg),
        read_commitment_budgets=make_read_intent(reg),
        read_template_field_specs=make_read_intent(reg),
        scribe=make_scribe(),
        clock=fixed_clock,
        hash_bytes=hash_bytes,
    )


class TestComposeFinancialSummary:
    def test_happy_path_decimal_arithmetic(
        self, fixed_clock, hash_bytes, make_read_intent, make_scribe
    ):
        deps = _make_deps(
            fixed_clock=fixed_clock,
            hash_bytes=hash_bytes,
            make_read_intent=make_read_intent,
            make_scribe=make_scribe,
        )
        r = compose_financial_summary(
            deps=deps,
            org_slug="myorg",
            grant_id="G1",
            period_n=1,
            operational_data_root="orgs/myorg/vault/operational/grants/G1/period_1",
            proposal_commitments_path="y",
            reporting_template_path="z",
        )
        assert r.lines_authored == 1
        assert len(r.claims) == 1
        c = r.claims[0]
        assert c.sub_section == "financial_summary"
        assert c.claim_kind == "financial"
        assert isinstance(c.sources[0].source_value, Decimal)
        assert c.sources[0].source_value == Decimal("12000")
        # Variance = 12000 - 12500 = -500
        assert "-500" in r.markdown_fragment

    def test_float_rejected(
        self, fixed_clock, hash_bytes, make_read_intent, make_scribe
    ):
        deps = _make_deps(
            fixed_clock=fixed_clock,
            hash_bytes=hash_bytes,
            make_read_intent=make_read_intent,
            make_scribe=make_scribe,
            with_float=True,
        )
        with pytest.raises(ComposerError):
            compose_financial_summary(
                deps=deps,
                org_slug="myorg",
                grant_id="G1",
                period_n=1,
                operational_data_root="x",
                proposal_commitments_path="y",
                reporting_template_path="z",
            )
