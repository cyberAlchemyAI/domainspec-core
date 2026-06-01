"""PDF emitter Code-phase tests. [§17.7]"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pytest

from pipeline.orchestrator.seats.wpfa.pdf_emitter import (
    PDF_RENDERED_CLAIMS_V0_1,
    PdfRenderContext,
    build_pdf_render_context,
    default_weasyprint_render,
    emit_buyer_facing_pdf,
    scan_indirect_template_data,
)
from pipeline.vault.sub_kinds.cycle_receipts import (
    CycleReceipt,
    CycleReceiptDelta,
    CycleReceiptDimensionTotals,
    PerModelCall,
    SpanProvenance,
)


def _receipt(*, attested: bool = True) -> CycleReceipt:
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
        per_claim_span_ids={k: ("s-1",) for k in PDF_RENDERED_CLAIMS_V0_1},
    )
    return CycleReceipt(
        cycle_id="cyc-test-001",
        org_slug="test-org",
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


class TestIndirectTemplateDataScan:
    def test_no_confidential_values_returns_empty(self) -> None:
        html = "<html><body>Hello world</body></html>"
        assert scan_indirect_template_data(
            rendered_html=html, confidential_value_strings=()
        ) == ()

    def test_html_text_leak_detected(self) -> None:
        html = "<p>EIN: 12-3456789 visible</p>"
        leaked = scan_indirect_template_data(
            rendered_html=html,
            confidential_value_strings=("12-3456789",),
        )
        assert "12-3456789" in leaked

    def test_css_content_property_leak_detected(self) -> None:
        html = "<style>.x::before{content:'SECRET-EIN-12-3456789'}</style><body></body>"
        leaked = scan_indirect_template_data(
            rendered_html=html,
            confidential_value_strings=("SECRET-EIN-12-3456789",),
        )
        assert "SECRET-EIN-12-3456789" in leaked

    def test_inline_js_string_literal_leak_detected(self) -> None:
        html = "<script>var s = 'CONFIDENTIAL-X';</script>"
        leaked = scan_indirect_template_data(
            rendered_html=html,
            confidential_value_strings=("CONFIDENTIAL-X",),
        )
        assert "CONFIDENTIAL-X" in leaked

    def test_value_not_present_no_leak(self) -> None:
        html = "<p>safe content</p>"
        assert scan_indirect_template_data(
            rendered_html=html,
            confidential_value_strings=("unrelated-secret",),
        ) == ()

    def test_html_strip_includes_unescaped_entities(self) -> None:
        # Test that &amp; and friends are unescaped during the strip pass
        html = "<p>EIN&#x3A; 12-3456789</p>"
        leaked = scan_indirect_template_data(
            rendered_html=html,
            confidential_value_strings=("EIN: 12-3456789",),
        )
        assert "EIN: 12-3456789" in leaked


class TestEmitBuyerFacingPDF:
    def test_unsigned_receipt_fails_operator_signature(self, tmp_path: Path) -> None:
        receipt = _receipt(attested=False)
        ctx = build_pdf_render_context(
            receipt=receipt,
            client_name="x",
            operator_display_name="x",
            signing_key_id_display="x",
            methodology_url="https://example.com/m",
        )
        out = emit_buyer_facing_pdf(
            receipt=receipt,
            context=ctx,
            output_dir=tmp_path,
            classification_register={},
            weasyprint_render=lambda **kw: (kw["output_path"], ""),
            write_pdf=lambda html, path: None,
        )
        assert not out.success
        assert "F-WPFA-OPERATOR-SIGNATURE-MISSING" in out.failure_codes

    def test_missing_classification_register_fails(self, tmp_path: Path) -> None:
        receipt = _receipt(attested=True)
        ctx = build_pdf_render_context(
            receipt=receipt,
            client_name="x",
            operator_display_name="x",
            signing_key_id_display="x",
            methodology_url="https://example.com/m",
        )
        # Use a rendered_field_paths that requires the register
        ctx = PdfRenderContext(
            client_name=ctx.client_name,
            operator_display_name=ctx.operator_display_name,
            signing_key_id_display=ctx.signing_key_id_display,
            methodology_url=ctx.methodology_url,
            delta_dollars_display=ctx.delta_dollars_display,
            delta_kwh_display=ctx.delta_kwh_display,
            percent_local_display=ctx.percent_local_display,
            per_cycle_rows=ctx.per_cycle_rows,
            rendered_field_paths=("client.name",),  # forces register check
            confidential_value_strings=(),
        )
        out = emit_buyer_facing_pdf(
            receipt=receipt,
            context=ctx,
            output_dir=tmp_path,
            classification_register=None,
            weasyprint_render=lambda **kw: (kw["output_path"], ""),
            write_pdf=lambda html, path: None,
        )
        assert not out.success
        assert "F-WPFA-PDF-CONFIDENTIAL-LEAK" in out.failure_codes

    def test_happy_path_with_stubbed_renderer(self, tmp_path: Path) -> None:
        receipt = _receipt(attested=True)
        ctx = build_pdf_render_context(
            receipt=receipt,
            client_name="Test Client",
            operator_display_name="Test Operator",
            signing_key_id_display="op-1",
            methodology_url="https://example.com/m",
        )
        out = emit_buyer_facing_pdf(
            receipt=receipt,
            context=ctx,
            output_dir=tmp_path,
            classification_register={},
            weasyprint_render=lambda **kw: (
                kw["output_path"],
                "<html><body>safe</body></html>",
            ),
            write_pdf=lambda html, path: path.write_text(html),
        )
        assert out.success
        assert out.output_path is not None
        assert out.output_path.is_file()

    def test_indirect_scan_leak_fails(self, tmp_path: Path) -> None:
        receipt = _receipt(attested=True)
        ctx = build_pdf_render_context(
            receipt=receipt,
            client_name="Test Client",
            operator_display_name="Test Operator",
            signing_key_id_display="op-1",
            methodology_url="https://example.com/m",
            confidential_value_strings=("SECRET-12-3456789",),
        )

        def leaking_render(**kw):
            return kw["output_path"], "<p>Visible: SECRET-12-3456789</p>"

        out = emit_buyer_facing_pdf(
            receipt=receipt,
            context=ctx,
            output_dir=tmp_path,
            classification_register={},
            weasyprint_render=leaking_render,
            write_pdf=lambda html, path: None,
        )
        assert not out.success
        assert "F-WPFA-PDF-CONFIDENTIAL-LEAK" in out.failure_codes

    def test_renderer_returning_wrong_shape_fails(self, tmp_path: Path) -> None:
        receipt = _receipt(attested=True)
        ctx = build_pdf_render_context(
            receipt=receipt,
            client_name="x",
            operator_display_name="x",
            signing_key_id_display="x",
            methodology_url="https://example.com/m",
        )
        out = emit_buyer_facing_pdf(
            receipt=receipt,
            context=ctx,
            output_dir=tmp_path,
            classification_register={},
            weasyprint_render=lambda **kw: kw["output_path"],  # NOT a tuple
            write_pdf=lambda html, path: None,
        )
        assert not out.success
        assert "F-WPFA-PDF-RENDER-FAILED" in out.failure_codes


class TestBuildPdfRenderContext:
    def test_context_derives_displays_from_receipt(self) -> None:
        receipt = _receipt(attested=True)
        ctx = build_pdf_render_context(
            receipt=receipt,
            client_name="Test",
            operator_display_name="Op",
            signing_key_id_display="op-1",
            methodology_url="https://example.com/m",
        )
        # delta dollars saved was 95 minor units = $0.95
        assert ctx.delta_dollars_display == "0.95"
        # percent local: 0 tokens local (only cloud span) = 0
        assert ctx.percent_local_display == "0"

    def test_per_cycle_rows_carries_trace_id(self) -> None:
        receipt = _receipt(attested=True)
        ctx = build_pdf_render_context(
            receipt=receipt,
            client_name="Test",
            operator_display_name="Op",
            signing_key_id_display="op-1",
            methodology_url="https://example.com/m",
            grant_identifier="TEST-GRANT-1",
        )
        assert len(ctx.per_cycle_rows) == 1
        assert ctx.per_cycle_rows[0]["trace_id_ref"] == "t-1"
        assert ctx.per_cycle_rows[0]["grant_identifier"] == "TEST-GRANT-1"


class TestDefaultWeasyprintRenderContract:
    """The default renderer uses Jinja2 + weasyprint. Test the Jinja2 step."""

    def test_default_renderer_returns_tuple_with_html(self, tmp_path: Path) -> None:
        receipt = _receipt(attested=True)
        ctx = build_pdf_render_context(
            receipt=receipt,
            client_name="Test",
            operator_display_name="Op",
            signing_key_id_display="op-1",
            methodology_url="https://example.com/m",
        )
        # Note: this test only exercises the Jinja2 render step, not
        # weasyprint write. If Jinja2 isn't installed the import fails.
        pytest.importorskip("jinja2")
        from pipeline.orchestrator.seats.wpfa.pdf_emitter import TEMPLATE_PATH

        result = default_weasyprint_render(
            receipt=receipt,
            context=ctx,
            template_path=TEMPLATE_PATH,
            output_path=tmp_path / "x.pdf",
        )
        assert isinstance(result, tuple) and len(result) == 2
        assert isinstance(result[1], str)
        assert receipt.cycle_id in result[1]
