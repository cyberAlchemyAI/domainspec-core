"""WPFA dashboard tests. [§17.8]"""

from __future__ import annotations

from pathlib import Path

from pipeline.orchestrator.seats.wpfa.dashboard import (
    PER_FLEET_PLACEHOLDER_TEXT,
    build_dashboard_data,
    render_dashboard_html,
)
from pipeline.vault.sub_kinds.cycle_receipts import (
    CycleReceipt,
    CycleReceiptDelta,
    CycleReceiptDimensionTotals,
    PerModelCall,
    SpanProvenance,
    to_canonical_bytes,
)


def _write_receipt(repo_root: Path, *, org_slug: str, cycle_id: str, attested: bool = False) -> Path:
    per_model = (
        PerModelCall(
            model_id="claude-sonnet-4-6",
            is_local=False,
            hardware_sku=None,
            input_tokens=100,
            output_tokens=50,
            dollars_minor_units=105,
            watt_hours_micro=80,
            span_ids=("s-1",),
        ),
    )
    actual = CycleReceiptDimensionTotals(
        dollars_total_minor_units=105,
        currency="USD",
        watt_hours_total_micro=80,
    )
    counterfactual = CycleReceiptDimensionTotals(
        dollars_total_minor_units=200,
        currency="USD",
        watt_hours_total_micro=200,
    )
    delta = CycleReceiptDelta(
        dollars_saved_minor_units=95,
        watt_hours_saved_micro=120,
        percent_dollars_saved=4750,
        percent_watt_hours_saved=6000,
    )
    sp = SpanProvenance(
        trace_ids=("t-1",),
        logfire_export_uri="/tmp/x.json",
        cycle_close_marker_span_id="span-close",
        per_claim_span_ids={
            "actual.dollars_total": ("s-1",),
            "actual.watt_hours_total": ("s-1",),
            "counterfactual.dollars_total": ("s-1",),
            "counterfactual.watt_hours_total": ("s-1",),
            "delta.dollars_saved": ("s-1",),
            "delta.watt_hours_saved": ("s-1",),
        },
    )
    receipt = CycleReceipt(
        cycle_id=cycle_id,
        org_slug=org_slug,
        schema_version="1.0.0",
        classification_register_version="f" * 128,
        emitted_at="2026-05-11T12:00:00Z",
        baseline_model_id="claude-sonnet-4-6",
        baseline_quarter="Q3-2026",
        coefficients_registry_version="b" * 128,
        coefficients_registry_signature_ed25519="c" * 128,
        dimensions_active=("dollars", "energy"),
        actual=actual,
        actual_per_model=per_model,
        counterfactual=counterfactual,
        delta=delta,
        span_provenance=sp,
        signed_by_operator_ed25519=("9" * 128) if attested else None,
    )
    out = (
        repo_root
        / "orgs"
        / org_slug
        / "vault"
        / "operational"
        / "cycle_receipts"
        / f"{cycle_id}.json"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(to_canonical_bytes(receipt))
    return out


class TestBuildDashboardData:
    def test_empty_repo_returns_empty_rollups(self, tmp_path: Path) -> None:
        data = build_dashboard_data(repo_root=tmp_path)
        assert data.per_org_rollups == {}
        assert data.per_quarter_rollups == {}

    def test_single_receipt_one_org_one_quarter(self, tmp_path: Path) -> None:
        _write_receipt(tmp_path, org_slug="fit-farms-llc", cycle_id="cyc-1")
        data = build_dashboard_data(repo_root=tmp_path)
        assert "fit-farms-llc" in data.per_org_rollups
        rollup = data.per_org_rollups["fit-farms-llc"]
        assert len(rollup.receipts) == 1
        assert rollup.cumulative_dollars_saved_minor_units == 95
        assert "Q3-2026" in data.per_quarter_rollups
        q = data.per_quarter_rollups["Q3-2026"]
        assert q.total_dollars_saved_minor_units == 95

    def test_two_orgs_aggregate_in_per_quarter(self, tmp_path: Path) -> None:
        _write_receipt(tmp_path, org_slug="org-a", cycle_id="cyc-a")
        _write_receipt(tmp_path, org_slug="org-b", cycle_id="cyc-b")
        data = build_dashboard_data(repo_root=tmp_path)
        assert set(data.per_org_rollups) == {"org-a", "org-b"}
        q = data.per_quarter_rollups["Q3-2026"]
        # Two orgs × 95 saved = 190
        assert q.total_dollars_saved_minor_units == 190
        assert set(q.per_org) == {"org-a", "org-b"}

    def test_attested_receipt_flagged(self, tmp_path: Path) -> None:
        _write_receipt(
            tmp_path,
            org_slug="fit-farms-llc",
            cycle_id="cyc-attested",
            attested=True,
        )
        data = build_dashboard_data(repo_root=tmp_path)
        rollup = data.per_org_rollups["fit-farms-llc"]
        assert rollup.receipts[0].is_buyer_attested is True

    def test_underscore_dirs_skipped(self, tmp_path: Path) -> None:
        # _TEMPLATE under orgs/ is not a real org
        template_dir = tmp_path / "orgs" / "_TEMPLATE"
        template_dir.mkdir(parents=True)
        data = build_dashboard_data(repo_root=tmp_path)
        assert "_TEMPLATE" not in data.per_org_rollups


class TestRenderDashboardHTML:
    def test_empty_renders_placeholder(self, tmp_path: Path) -> None:
        data = build_dashboard_data(repo_root=tmp_path)
        html = render_dashboard_html(data)
        assert "WPFA Dashboard" in html
        assert PER_FLEET_PLACEHOLDER_TEXT in html
        assert "Stage-2+" in html

    def test_html_contains_cycle_id_and_money(self, tmp_path: Path) -> None:
        _write_receipt(tmp_path, org_slug="fit-farms-llc", cycle_id="cyc-display")
        data = build_dashboard_data(repo_root=tmp_path)
        html = render_dashboard_html(data)
        assert "cyc-display" in html
        assert "$0.95" in html

    def test_attested_marker_renders(self, tmp_path: Path) -> None:
        _write_receipt(
            tmp_path,
            org_slug="x",
            cycle_id="cyc-attested-render",
            attested=True,
        )
        data = build_dashboard_data(repo_root=tmp_path)
        html = render_dashboard_html(data)
        assert "<span class='attested'>yes</span>" in html

    def test_per_fleet_placeholder_is_data_free(self, tmp_path: Path) -> None:
        """RT-11 fold-in: per-fleet placeholder MUST be static text only."""
        # Write multiple orgs + receipts to confirm per-fleet doesn't leak
        _write_receipt(tmp_path, org_slug="a", cycle_id="ca")
        _write_receipt(tmp_path, org_slug="b", cycle_id="cb")
        data = build_dashboard_data(repo_root=tmp_path)
        html = render_dashboard_html(data)
        # The placeholder text must not include SKU counts, hardware enums,
        # or aggregate facts about the fleet. Check the exact placeholder.
        assert PER_FLEET_PLACEHOLDER_TEXT in html
        # Specifically: no SKU strings in the placeholder section
        # (they may appear elsewhere in per-org tables, which is fine)
        placeholder_block_start = html.find("Per-fleet rollup")
        placeholder_block = html[placeholder_block_start:]
        for sku in ("apple_m3_ultra", "amd_gx_10", "nvidia_spark"):
            assert sku not in placeholder_block
