"""CycleReceipt schema + canonical-bytes round-trip tests. [§17 v1, §17.3]"""

from __future__ import annotations

import pytest

from pipeline.vault.sub_kinds.cycle_receipts import (
    ADMIN_RISK_SEVERITY_DEFAULT,
    CycleReceipt,
    CycleReceiptDelta,
    CycleReceiptDimensionTotals,
    INTENT,
    PerModelCall,
    SUB_KIND,
    SpanProvenance,
    VAULT_SUBTREE,
    from_canonical_bytes,
    record_id_for,
    to_canonical_bytes,
)


def _make_receipt(*, signed: bool = False) -> CycleReceipt:
    actual = CycleReceiptDimensionTotals(
        dollars_total_minor_units=200,
        currency="USD",
        watt_hours_total_micro=500000,
    )
    counterfactual = CycleReceiptDimensionTotals(
        dollars_total_minor_units=1000,
        currency="USD",
        watt_hours_total_micro=2500000,
    )
    delta = CycleReceiptDelta(
        dollars_saved_minor_units=800,
        watt_hours_saved_micro=2000000,
        percent_dollars_saved=8000,
        percent_watt_hours_saved=8000,
    )
    rows = (
        PerModelCall(
            model_id="local/m3-ultra-llama-70b",
            is_local=True,
            hardware_sku="apple_m3_ultra",
            input_tokens=1000,
            output_tokens=500,
            dollars_minor_units=120,
            watt_hours_micro=300000,
            span_ids=("span-1", "span-2"),
        ),
        PerModelCall(
            model_id="anthropic/claude-sonnet-4-6",
            is_local=False,
            hardware_sku=None,
            input_tokens=500,
            output_tokens=250,
            dollars_minor_units=80,
            watt_hours_micro=200000,
            span_ids=("span-3",),
        ),
    )
    sp = SpanProvenance(
        trace_ids=("trace-1",),
        logfire_export_uri="/tmp/logfire/trace-1.json",
        cycle_close_marker_span_id="span-close",
        per_claim_span_ids={
            "actual.dollars_total": ("span-1", "span-3"),
            "actual.watt_hours_total": ("span-1", "span-3"),
            "counterfactual.dollars_total": ("span-1", "span-3"),
            "counterfactual.watt_hours_total": ("span-1", "span-3"),
            "delta.dollars_saved": ("span-1", "span-3"),
            "delta.watt_hours_saved": ("span-1", "span-3"),
        },
    )
    sig = "a" * 128 if signed else None
    return CycleReceipt(
        cycle_id="cyc-2026-05-11-001",
        org_slug="fit-farms-llc",
        schema_version="1.0.0",
        classification_register_version="f" * 128,
        emitted_at="2026-05-11T12:00:00Z",
        baseline_model_id="claude-sonnet-4-6",
        baseline_quarter="Q3-2026",
        coefficients_registry_version="e" * 128,
        coefficients_registry_signature_ed25519="d" * 128,
        dimensions_active=("dollars", "energy"),
        actual=actual,
        actual_per_model=rows,
        counterfactual=counterfactual,
        delta=delta,
        span_provenance=sp,
        signed_by_operator_ed25519=sig,
    )


class TestConstants:
    def test_module_constants(self) -> None:
        assert INTENT == "operational-cycle-receipt-write"
        assert SUB_KIND == "cycle_receipt"
        assert VAULT_SUBTREE == "operational/cycle_receipts/"
        assert ADMIN_RISK_SEVERITY_DEFAULT == "YELLOW"


class TestSchemaInvariants:
    def test_minimal_valid_receipt_constructs(self) -> None:
        r = _make_receipt()
        assert isinstance(r, CycleReceipt)
        assert r.is_buyer_attested is False

    def test_signed_receipt_is_buyer_attested(self) -> None:
        r = _make_receipt(signed=True)
        assert r.is_buyer_attested is True

    def test_a12_extends_to_energy_int_only(self) -> None:
        with pytest.raises(ValueError, match="A12 mandate"):
            CycleReceiptDimensionTotals(
                dollars_total_minor_units=100,
                currency="USD",
                watt_hours_total_micro=1.5,  # type: ignore[arg-type]
            )

    def test_dollars_field_rejects_bool(self) -> None:
        with pytest.raises(ValueError, match="A12"):
            CycleReceiptDimensionTotals(
                dollars_total_minor_units=True,  # type: ignore[arg-type]
                currency="USD",
                watt_hours_total_micro=100,
            )

    def test_currency_identity_actual_vs_counterfactual(self) -> None:
        actual = CycleReceiptDimensionTotals(
            dollars_total_minor_units=100,
            currency="USD",
            watt_hours_total_micro=100,
        )
        counter = CycleReceiptDimensionTotals(
            dollars_total_minor_units=100,
            currency="EUR",
            watt_hours_total_micro=100,
        )
        with pytest.raises(ValueError, match="currency"):
            CycleReceipt(
                cycle_id="c",
                org_slug="o",
                schema_version="1.0.0",
                classification_register_version="f" * 128,
                emitted_at="2026-05-11T00:00:00Z",
                baseline_model_id="b",
                baseline_quarter="Q1-2026",
                coefficients_registry_version="e" * 128,
                coefficients_registry_signature_ed25519="d" * 128,
                dimensions_active=("dollars", "energy"),
                actual=actual,
                actual_per_model=(),
                counterfactual=counter,
                delta=CycleReceiptDelta(
                    dollars_saved_minor_units=0,
                    watt_hours_saved_micro=0,
                    percent_dollars_saved=0,
                    percent_watt_hours_saved=0,
                ),
                span_provenance=SpanProvenance(
                    trace_ids=("t",),
                    logfire_export_uri=None,
                    cycle_close_marker_span_id="s",
                    per_claim_span_ids={"actual.dollars_total": ("s",)},
                ),
            )

    def test_v0_1_dimensions_locked(self) -> None:
        # dimensions_active outside the v0.1 closed set fails at top-level
        # invariant scan; the WPFA dimension-unsupported gate catches this
        # at PRE-emission, but the schema itself accepts the v0.1 closed
        # set values plus future-set entries — invariant 9 only restricts
        # closed-set membership, not the v0.1 == ("dollars","energy")
        # equality (that's the gate's responsibility).
        r = _make_receipt()
        assert r.dimensions_active == ("dollars", "energy")

    def test_per_model_aggregate_mismatch(self) -> None:
        actual = CycleReceiptDimensionTotals(
            dollars_total_minor_units=999,  # mismatch
            currency="USD",
            watt_hours_total_micro=500000,
        )
        counterfactual = CycleReceiptDimensionTotals(
            dollars_total_minor_units=1000,
            currency="USD",
            watt_hours_total_micro=2500000,
        )
        delta = CycleReceiptDelta(
            dollars_saved_minor_units=1,
            watt_hours_saved_micro=2000000,
            percent_dollars_saved=0,
            percent_watt_hours_saved=8000,
        )
        rows = (
            PerModelCall(
                model_id="m",
                is_local=True,
                hardware_sku="apple_m3_ultra",
                input_tokens=100,
                output_tokens=100,
                dollars_minor_units=200,
                watt_hours_micro=500000,
                span_ids=("s",),
            ),
        )
        sp = SpanProvenance(
            trace_ids=("t",),
            logfire_export_uri=None,
            cycle_close_marker_span_id="s",
            per_claim_span_ids={"actual.dollars_total": ("s",)},
        )
        with pytest.raises(ValueError, match="per_model_aggregate_mismatch"):
            CycleReceipt(
                cycle_id="c",
                org_slug="o",
                schema_version="1.0.0",
                classification_register_version="f" * 128,
                emitted_at="2026-05-11T00:00:00Z",
                baseline_model_id="claude-sonnet-4-6",
                baseline_quarter="Q3-2026",
                coefficients_registry_version="e" * 128,
                coefficients_registry_signature_ed25519="d" * 128,
                dimensions_active=("dollars", "energy"),
                actual=actual,
                actual_per_model=rows,
                counterfactual=counterfactual,
                delta=delta,
                span_provenance=sp,
            )

    def test_delta_arithmetic_mismatch(self) -> None:
        actual = CycleReceiptDimensionTotals(
            dollars_total_minor_units=200,
            currency="USD",
            watt_hours_total_micro=500000,
        )
        counterfactual = CycleReceiptDimensionTotals(
            dollars_total_minor_units=1000,
            currency="USD",
            watt_hours_total_micro=2500000,
        )
        # Wrong delta: counterfactual - actual = 800, but we claim 700
        delta = CycleReceiptDelta(
            dollars_saved_minor_units=700,  # wrong
            watt_hours_saved_micro=2000000,
            percent_dollars_saved=7000,
            percent_watt_hours_saved=8000,
        )
        rows = (
            PerModelCall(
                model_id="m",
                is_local=False,
                hardware_sku=None,
                input_tokens=10,
                output_tokens=10,
                dollars_minor_units=200,
                watt_hours_micro=500000,
                span_ids=("s",),
            ),
        )
        sp = SpanProvenance(
            trace_ids=("t",),
            logfire_export_uri=None,
            cycle_close_marker_span_id="s",
            per_claim_span_ids={"actual.dollars_total": ("s",)},
        )
        with pytest.raises(ValueError, match="delta_arithmetic_mismatch"):
            CycleReceipt(
                cycle_id="c",
                org_slug="o",
                schema_version="1.0.0",
                classification_register_version="f" * 128,
                emitted_at="2026-05-11T00:00:00Z",
                baseline_model_id="claude-sonnet-4-6",
                baseline_quarter="Q3-2026",
                coefficients_registry_version="e" * 128,
                coefficients_registry_signature_ed25519="d" * 128,
                dimensions_active=("dollars", "energy"),
                actual=actual,
                actual_per_model=rows,
                counterfactual=counterfactual,
                delta=delta,
                span_provenance=sp,
            )

    @pytest.mark.parametrize(
        "bad_cycle_id",
        [
            "../etc/passwd",
            "..\\etc\\passwd",
            "/abs/path",
            "with spaces",
            "with.dots",
            "with$special",
            "with/slash",
            "",
            "a" * 129,  # too long
        ],
    )
    def test_cycle_id_rejects_path_traversal_and_special_chars(
        self, bad_cycle_id: str
    ) -> None:
        # Cycle 2 RT-C2-05 FIX-IN-PLACE regression
        r = _make_receipt()
        with pytest.raises(ValueError):
            CycleReceipt(
                cycle_id=bad_cycle_id,
                org_slug=r.org_slug,
                schema_version=r.schema_version,
                classification_register_version=r.classification_register_version,
                emitted_at=r.emitted_at,
                baseline_model_id=r.baseline_model_id,
                baseline_quarter=r.baseline_quarter,
                coefficients_registry_version=r.coefficients_registry_version,
                coefficients_registry_signature_ed25519=r.coefficients_registry_signature_ed25519,
                dimensions_active=r.dimensions_active,
                actual=r.actual,
                actual_per_model=r.actual_per_model,
                counterfactual=r.counterfactual,
                delta=r.delta,
                span_provenance=r.span_provenance,
            )

    def test_cycle_id_accepts_well_formed_values(self) -> None:
        # RT-C2-05 strict regex accepts the canonical naming pattern
        r = _make_receipt()
        for good in ("cyc-2026-05-11-001", "abc_123", "ABC", "0", "a-b_c-d"):
            CycleReceipt(
                cycle_id=good,
                org_slug=r.org_slug,
                schema_version=r.schema_version,
                classification_register_version=r.classification_register_version,
                emitted_at=r.emitted_at,
                baseline_model_id=r.baseline_model_id,
                baseline_quarter=r.baseline_quarter,
                coefficients_registry_version=r.coefficients_registry_version,
                coefficients_registry_signature_ed25519=r.coefficients_registry_signature_ed25519,
                dimensions_active=r.dimensions_active,
                actual=r.actual,
                actual_per_model=r.actual_per_model,
                counterfactual=r.counterfactual,
                delta=r.delta,
                span_provenance=r.span_provenance,
            )


class TestCanonicalRoundTrip:
    def test_round_trip_byte_identity(self) -> None:
        r = _make_receipt()
        payload = to_canonical_bytes(r)
        back = from_canonical_bytes(payload)
        assert to_canonical_bytes(back) == payload

    def test_round_trip_signed(self) -> None:
        r = _make_receipt(signed=True)
        payload = to_canonical_bytes(r)
        back = from_canonical_bytes(payload)
        assert back.signed_by_operator_ed25519 == "a" * 128
        assert back.is_buyer_attested is True

    def test_decode_rejects_float_dollars(self) -> None:
        import json

        r = _make_receipt()
        payload_dict = json.loads(to_canonical_bytes(r).decode("utf-8"))
        payload_dict["actual"]["dollars_total_minor_units"] = 200.0
        tampered = json.dumps(
            payload_dict, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        with pytest.raises(ValueError, match="A12"):
            from_canonical_bytes(tampered)

    def test_record_id_for_returns_cycle_id(self) -> None:
        r = _make_receipt()
        assert record_id_for(r) == "cyc-2026-05-11-001"
