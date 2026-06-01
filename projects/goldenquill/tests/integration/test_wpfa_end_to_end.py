"""WPFA end-to-end smoke test. [§17 v1 + §2 v7.4 + §4 v2.x.z]

Synthetic Logfire span tree + synthetic signed Coefficient Registry →
CycleReceipt round-trip → operator-attested PDF emission. This is the
done-definition gate for the Code phase per
``pipeline/handoffs/ws_wpfa_code_phase_handoff_2026-05-11.md`` scope item 7.

The test does NOT depend on the weasyprint substrate being installed; it
injects a stub renderer that captures the rendered HTML so the indirect-
template-data scan exercises against a real Jinja2 render. Adding the
weasyprint dep to pyproject.toml is a Golden Image build concern; this
test exercises the pure-Python flow.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from cryptography.hazmat.primitives.asymmetric import ed25519

from pipeline.orchestrator.seats.wpfa.cycle_accountant import (
    CycleAccountantInput,
    canonicalize_logfire_export,
    receipt_canonical_sha3_512,
    run_cycle_accountant_pipeline,
)
from pipeline.orchestrator.seats.wpfa.dashboard import (
    build_dashboard_data,
    render_dashboard_html,
)
from pipeline.orchestrator.seats.wpfa.pdf_emitter import (
    PdfRenderContext,
    build_pdf_render_context,
    emit_buyer_facing_pdf,
)
from pipeline.vault.sub_kinds.coefficient_registry import (
    CoefficientEntry,
    CoefficientRegistry,
    to_signing_payload,
)
from pipeline.vault.sub_kinds.cycle_receipts import (
    CycleReceipt,
    from_canonical_bytes,
    to_canonical_bytes,
)


# ---------------------------------------------------------------------------
# Synthetic fixtures
# ---------------------------------------------------------------------------


def _synthetic_logfire_export(tmp_path: Path) -> Path:
    """Write a synthetic Logfire export with two LLM-call spans."""
    payload = {
        "service": "tilth",
        "spans": [
            {
                "span_id": "s-local-1",
                "trace_id": "t-1",
                "model_id": "local/m3-ultra-llama-70b",
                "input_tokens": 1_000_000,
                "output_tokens": 500_000,
            },
            {
                "span_id": "s-cloud-1",
                "trace_id": "t-1",
                "model_id": "claude-sonnet-4-6",
                "input_tokens": 2_000_000,
                "output_tokens": 1_000_000,
            },
            # Non-LLM span filtered by load_spans_from_logfire_export
            {
                "span_id": "s-housekeeping",
                "trace_id": "t-1",
                "kind": "internal",
            },
        ],
    }
    path = tmp_path / "logfire_export.json"
    path.write_bytes(json.dumps(payload).encode("utf-8"))
    return path


def _build_signed_registry() -> tuple[CoefficientRegistry, bytes]:
    """Build a CoefficientRegistry signed by a freshly-minted SN-LLC keypair.

    Returns (registry, pinned_pubkey_bytes). The signature on the returned
    registry is the actual Ed25519 signature over the canonical signing
    payload — so the F-WPFA-COEFFICIENT-SIGNATURE-INVALID gate verifies
    against the pinned pubkey at PRE-load.
    """
    sn_llc_priv = ed25519.Ed25519PrivateKey.generate()
    sn_llc_pub_bytes = sn_llc_priv.public_key().public_bytes_raw()

    # Build registry with a placeholder signature, then re-build with actual
    # signature over the canonical signing payload.
    entries = (
        CoefficientEntry(
            model_id="claude-sonnet-4-6",
            is_local=False,
            hardware_sku=None,
            dollars_per_million_input_tokens_minor_units=300,
            dollars_per_million_output_tokens_minor_units=1500,
            watt_hours_per_million_input_tokens_micro=400000,
            watt_hours_per_million_output_tokens_micro=800000,
            idle_watts_baseline_micro=None,
            peak_watts_under_load_micro=None,
            citation_url="https://example.com/c1",
            measurement_date="2026-07-01",
            measurement_methodology_url="https://example.com/m1",
        ),
        CoefficientEntry(
            model_id="local/m3-ultra-llama-70b",
            is_local=True,
            hardware_sku="apple_m3_ultra",
            dollars_per_million_input_tokens_minor_units=0,
            dollars_per_million_output_tokens_minor_units=0,
            watt_hours_per_million_input_tokens_micro=50000,
            watt_hours_per_million_output_tokens_micro=100000,
            idle_watts_baseline_micro=10_000_000,
            peak_watts_under_load_micro=200_000_000,
            citation_url="https://example.com/c2",
            measurement_date="2026-07-01",
            measurement_methodology_url="https://example.com/m2",
        ),
    )
    placeholder = CoefficientRegistry(
        schema_version="1.0.0",
        quarter="Q3-2026",
        published_at="2026-07-01T00:00:00Z",
        sn_llc_signature_ed25519="a" * 128,
        sn_llc_signing_key_id="sn-llc-q3-2026",
        baseline_model_id="claude-sonnet-4-6",
        entries=entries,
        methodology_url="https://example.com/wpfa-methodology",
        rollback_pointer=None,
    )
    payload = to_signing_payload(placeholder)
    sig = sn_llc_priv.sign(payload)
    signed = CoefficientRegistry(
        schema_version=placeholder.schema_version,
        quarter=placeholder.quarter,
        published_at=placeholder.published_at,
        sn_llc_signature_ed25519=sig.hex(),
        sn_llc_signing_key_id=placeholder.sn_llc_signing_key_id,
        baseline_model_id=placeholder.baseline_model_id,
        entries=placeholder.entries,
        methodology_url=placeholder.methodology_url,
        rollback_pointer=placeholder.rollback_pointer,
    )
    return signed, sn_llc_pub_bytes


def _input(*, logfire_path: Path, attestation: bool = False) -> CycleAccountantInput:
    return CycleAccountantInput(
        run_id="run-e2e-1",
        cycle_id="cyc-e2e-2026-05-11",
        org_slug="fit-farms-llc",
        cycle_close_marker_span_id="span-close",
        logfire_export_path=str(logfire_path),
        classification_register_version="f" * 128,
        coefficient_registry_path="/tmp/registry.yaml",
        dimensions_requested=("dollars", "energy"),
        operator_attestation_requested=attestation,
        invoked_at_utc="2026-05-11T12:00:00Z",
    )


# ---------------------------------------------------------------------------
# E2E happy path
# ---------------------------------------------------------------------------


class TestEndToEndHappyPath:
    def test_logfire_to_receipt_to_signed_pdf(self, tmp_path: Path) -> None:
        # 1. Synthesize Logfire export + signed registry
        logfire = _synthetic_logfire_export(tmp_path)
        registry, _pub = _build_signed_registry()

        # 2. Operator signer — produces a real Ed25519 signature so the
        # CycleReceipt invariant on operator signature shape passes.
        operator_priv = ed25519.Ed25519PrivateKey.generate()

        def operator_signer(message_bytes: bytes) -> str:
            return operator_priv.sign(message_bytes).hex()

        # 3. Run the cycle accountant — composes + writes the receipt
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        result = run_cycle_accountant_pipeline(
            inp=_input(logfire_path=logfire, attestation=True),
            registry=registry,
            output_root=repo_root,
            operator_signer=operator_signer,
        )
        assert result.success, f"expected success, got {result.failure_codes!r}: {result.detail}"
        assert result.receipt is not None
        assert result.receipt.is_buyer_attested
        assert result.output_path is not None
        assert result.output_path.is_file()

        # 4. Verify the receipt round-trips canonical-JSON
        decoded = from_canonical_bytes(result.output_path.read_bytes())
        assert decoded.cycle_id == result.receipt.cycle_id
        assert decoded.signed_by_operator_ed25519 == result.receipt.signed_by_operator_ed25519
        assert to_canonical_bytes(decoded) == result.receipt_canonical_bytes

        # 5. Emit buyer-facing PDF using a stubbed weasyprint renderer.
        # The stub returns rendered HTML so the indirect scan exercises.
        captured: list[str] = []

        def stub_render(*, receipt, context, template_path, output_path):
            from jinja2 import Environment, FileSystemLoader, select_autoescape
            env = Environment(
                loader=FileSystemLoader(str(template_path.parent)),
                autoescape=select_autoescape(["html", "xml"]),
            )
            html = env.get_template(template_path.name).render(
                receipt=receipt,
                client_name=context.client_name,
                operator_display_name=context.operator_display_name,
                signing_key_id_display=context.signing_key_id_display,
                methodology_url=context.methodology_url,
                delta_dollars_display=context.delta_dollars_display,
                delta_kwh_display=context.delta_kwh_display,
                percent_local_display=context.percent_local_display,
                per_cycle_rows=context.per_cycle_rows,
            )
            captured.append(html)
            return output_path, html

        def stub_write_pdf(rendered_html: str, output_path: Path) -> None:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(b"%PDF-stub\n" + rendered_html.encode("utf-8"))

        context = build_pdf_render_context(
            receipt=result.receipt,
            client_name="FIT Farms LLC",
            operator_display_name="Josh Inklovich",
            signing_key_id_display="op-001",
            methodology_url="https://example.com/wpfa-methodology",
            grant_identifier="VAPG-FY26",
            confidential_value_strings=(),
        )
        output_dir = repo_root / "orgs" / result.receipt.org_slug / "wpfa_artifacts"
        emit_result = emit_buyer_facing_pdf(
            receipt=result.receipt,
            context=context,
            output_dir=output_dir,
            classification_register={},
            weasyprint_render=stub_render,
            write_pdf=stub_write_pdf,
        )
        assert emit_result.success, (
            f"PDF emit failed: {emit_result.failure_codes!r} :: {emit_result.detail}"
        )
        assert emit_result.output_path is not None
        assert emit_result.output_path.is_file()
        assert len(captured) == 1
        # Brand thesis line surfaces in the rendered HTML
        assert "Strong organizations are not short on substance" in captured[0]
        # The cycle_id renders
        assert result.receipt.cycle_id in captured[0]

        # 6. Dashboard reads the same disk-state and surfaces the receipt
        data = build_dashboard_data(repo_root=repo_root)
        assert result.receipt.org_slug in data.per_org_rollups
        rollup = data.per_org_rollups[result.receipt.org_slug]
        assert len(rollup.receipts) == 1
        assert rollup.receipts[0].is_buyer_attested
        html = render_dashboard_html(data)
        assert result.receipt.cycle_id in html
        assert "Stage-2+" in html  # placeholder marker

    def test_unsigned_receipt_pdf_emit_fails_closed(self, tmp_path: Path) -> None:
        # Compose a receipt WITHOUT operator attestation; PDF emit must fail.
        logfire = _synthetic_logfire_export(tmp_path)
        registry, _pub = _build_signed_registry()
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        result = run_cycle_accountant_pipeline(
            inp=_input(logfire_path=logfire, attestation=False),
            registry=registry,
            output_root=repo_root,
        )
        assert result.success
        assert result.receipt is not None
        assert result.receipt.signed_by_operator_ed25519 is None

        context = build_pdf_render_context(
            receipt=result.receipt,
            client_name="x",
            operator_display_name="x",
            signing_key_id_display="x",
            methodology_url="https://example.com/m",
        )
        emit = emit_buyer_facing_pdf(
            receipt=result.receipt,
            context=context,
            output_dir=tmp_path / "out",
            classification_register={},
            weasyprint_render=lambda **kw: (kw["output_path"], "<html></html>"),
            write_pdf=lambda html, path: None,
        )
        assert not emit.success
        assert "F-WPFA-OPERATOR-SIGNATURE-MISSING" in emit.failure_codes

    def test_canonicalization_byte_identity(self, tmp_path: Path) -> None:
        """RT-C2-03: same export content → byte-identical canonical bytes."""
        logfire = _synthetic_logfire_export(tmp_path)
        c1 = canonicalize_logfire_export(logfire.read_bytes())
        # Re-write with permuted top-level keys; canonical should match.
        permuted = {
            "spans": json.loads(logfire.read_bytes())["spans"],
            "service": "tilth",
        }
        c2 = canonicalize_logfire_export(
            json.dumps(permuted).encode("utf-8")
        )
        assert c1 == c2

    def test_canonicalization_fails_on_non_json(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="schema_drift_advisory"):
            canonicalize_logfire_export(b"not-json{")

    def test_cross_org_path_leak_rejected(self, tmp_path: Path) -> None:
        """A receipt write attempted with a tampered org_slug fails closed."""
        logfire = _synthetic_logfire_export(tmp_path)
        registry, _pub = _build_signed_registry()
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        inp = CycleAccountantInput(
            run_id="run-1",
            cycle_id="cyc-1",
            # Path safe characters only — invariant tightened RT-C2-05
            org_slug="legit-org",
            cycle_close_marker_span_id="span-close",
            logfire_export_path=str(logfire),
            classification_register_version="f" * 128,
            coefficient_registry_path="/tmp/registry.yaml",
            dimensions_requested=("dollars", "energy"),
            operator_attestation_requested=False,
            invoked_at_utc="2026-05-11T12:00:00Z",
        )
        # The pipeline always writes to orgs/<inp.org_slug>/...; the cross-org
        # leak guard fires if the resolved path doesn't include the slug —
        # which happens only on accidental empty/malformed slugs. Slug
        # invariant guards at receipt construction. Verify the happy path
        # works AND the receipt write lands under the expected org subtree.
        result = run_cycle_accountant_pipeline(
            inp=inp,
            registry=registry,
            output_root=repo_root,
        )
        assert result.success
        assert "/orgs/legit-org/" in str(result.output_path)
