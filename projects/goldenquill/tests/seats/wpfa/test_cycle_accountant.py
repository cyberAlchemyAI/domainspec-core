"""Cycle Accountant deterministic composition tests. [§17.5]"""

from __future__ import annotations

import pytest

from pipeline.orchestrator.seats.wpfa.cycle_accountant import (
    CycleAccountantInput,
    SpanRecord,
    compose_receipt,
)
from pipeline.vault.sub_kinds.coefficient_registry import (
    CoefficientEntry,
    CoefficientRegistry,
)
from pipeline.vault.sub_kinds.cycle_receipts import (
    CycleReceipt,
    to_canonical_bytes,
)


def _registry() -> CoefficientRegistry:
    return CoefficientRegistry(
        schema_version="1.0.0",
        quarter="Q3-2026",
        published_at="2026-07-01T00:00:00Z",
        sn_llc_signature_ed25519="a" * 128,
        sn_llc_signing_key_id="sn-llc-q3",
        baseline_model_id="claude-sonnet-4-6",
        entries=(
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
                citation_url="https://example.com/c",
                measurement_date="2026-07-01",
                measurement_methodology_url="https://example.com/m",
            ),
            CoefficientEntry(
                model_id="local/m3-ultra-llama-70b",
                is_local=True,
                hardware_sku="apple_m3_ultra",
                dollars_per_million_input_tokens_minor_units=0,
                dollars_per_million_output_tokens_minor_units=0,
                watt_hours_per_million_input_tokens_micro=50000,
                watt_hours_per_million_output_tokens_micro=100000,
                idle_watts_baseline_micro=10000000,
                peak_watts_under_load_micro=200000000,
                citation_url="https://example.com/c",
                measurement_date="2026-07-01",
                measurement_methodology_url="https://example.com/m",
            ),
        ),
        methodology_url="https://example.com/wpfa",
        rollback_pointer=None,
    )


def _input(*, attestation: bool = False) -> CycleAccountantInput:
    return CycleAccountantInput(
        run_id="run-1",
        cycle_id="cyc-2026-05-11-001",
        org_slug="fit-farms-llc",
        cycle_close_marker_span_id="span-close",
        logfire_export_path="/tmp/logfire/trace-1.json",
        classification_register_version="f" * 128,
        coefficient_registry_path="/tmp/registry.yaml",
        dimensions_requested=("dollars", "energy"),
        operator_attestation_requested=attestation,
        invoked_at_utc="2026-05-11T12:00:00Z",
    )


def _spans() -> list[SpanRecord]:
    return [
        SpanRecord(
            span_id="s-local-1",
            trace_id="t-1",
            model_id="local/m3-ultra-llama-70b",
            input_tokens=1_000_000,
            output_tokens=500_000,
        ),
        SpanRecord(
            span_id="s-cloud-1",
            trace_id="t-1",
            model_id="claude-sonnet-4-6",
            input_tokens=2_000_000,
            output_tokens=1_000_000,
        ),
    ]


class TestComposeReceiptHappyPath:
    def test_basic_composition_returns_cycle_receipt(self) -> None:
        receipt = compose_receipt(
            _input(),
            spans=_spans(),
            registry=_registry(),
            currency="USD",
            classification_register_version="f" * 128,
        )
        assert isinstance(receipt, CycleReceipt)
        assert receipt.cycle_id == "cyc-2026-05-11-001"
        assert receipt.org_slug == "fit-farms-llc"
        # Two distinct models
        assert len(receipt.actual_per_model) == 2
        # Local model has 0 dollar cost per registry (free local inference)
        local = next(
            r for r in receipt.actual_per_model if r.is_local
        )
        assert local.dollars_minor_units == 0
        # Cloud model has cost
        cloud = next(
            r for r in receipt.actual_per_model if not r.is_local
        )
        # 2_000_000 * 300 / 1_000_000 + 1_000_000 * 1500 / 1_000_000 = 600 + 1500 = 2100
        assert cloud.dollars_minor_units == 2100

    def test_counterfactual_uses_baseline_for_all_tokens(self) -> None:
        receipt = compose_receipt(
            _input(),
            spans=_spans(),
            registry=_registry(),
            currency="USD",
            classification_register_version="f" * 128,
        )
        # Counterfactual: ALL tokens billed at baseline (Claude Sonnet) rates
        # local input  = 1_000_000 * 300 / 1_000_000 = 300
        # local output =   500_000 * 1500 / 1_000_000 = 750
        # cloud input  = 2_000_000 * 300 / 1_000_000 = 600
        # cloud output = 1_000_000 * 1500 / 1_000_000 = 1500
        # total counterfactual = 3150
        assert receipt.counterfactual.dollars_total_minor_units == 3150
        assert receipt.actual.dollars_total_minor_units == 2100

    def test_delta_equals_counterfactual_minus_actual(self) -> None:
        receipt = compose_receipt(
            _input(),
            spans=_spans(),
            registry=_registry(),
            currency="USD",
            classification_register_version="f" * 128,
        )
        assert receipt.delta.dollars_saved_minor_units == (
            receipt.counterfactual.dollars_total_minor_units
            - receipt.actual.dollars_total_minor_units
        )
        assert receipt.delta.watt_hours_saved_micro == (
            receipt.counterfactual.watt_hours_total_micro
            - receipt.actual.watt_hours_total_micro
        )


class TestDeterminism:
    def test_same_inputs_byte_identity(self) -> None:
        receipt_a = compose_receipt(
            _input(),
            spans=_spans(),
            registry=_registry(),
            currency="USD",
            classification_register_version="f" * 128,
        )
        receipt_b = compose_receipt(
            _input(),
            spans=_spans(),
            registry=_registry(),
            currency="USD",
            classification_register_version="f" * 128,
        )
        assert to_canonical_bytes(receipt_a) == to_canonical_bytes(receipt_b)

    def test_per_model_rows_sorted_deterministically(self) -> None:
        receipt = compose_receipt(
            _input(),
            spans=_spans(),
            registry=_registry(),
            currency="USD",
            classification_register_version="f" * 128,
        )
        model_ids = [r.model_id for r in receipt.actual_per_model]
        assert model_ids == sorted(model_ids)


class TestOperatorAttestation:
    def test_attestation_off_returns_unsigned(self) -> None:
        receipt = compose_receipt(
            _input(),
            spans=_spans(),
            registry=_registry(),
            currency="USD",
            classification_register_version="f" * 128,
        )
        assert receipt.signed_by_operator_ed25519 is None
        assert receipt.is_buyer_attested is False

    def test_attestation_on_with_signer_returns_signed(self) -> None:
        def signer(message_bytes: bytes) -> str:
            return "9" * 128

        receipt = compose_receipt(
            _input(attestation=True),
            spans=_spans(),
            registry=_registry(),
            currency="USD",
            classification_register_version="f" * 128,
            operator_signer=signer,
        )
        assert receipt.signed_by_operator_ed25519 == "9" * 128
        assert receipt.is_buyer_attested is True

    def test_attestation_on_without_signer_returns_unsigned(self) -> None:
        receipt = compose_receipt(
            _input(attestation=True),
            spans=_spans(),
            registry=_registry(),
            currency="USD",
            classification_register_version="f" * 128,
            operator_signer=None,
        )
        assert receipt.signed_by_operator_ed25519 is None


class TestModelNotInRegistry:
    def test_unknown_model_raises(self) -> None:
        spans = [
            SpanRecord(
                span_id="s",
                trace_id="t",
                model_id="unknown/model",
                input_tokens=100,
                output_tokens=100,
            )
        ]
        with pytest.raises(ValueError, match="not in registry"):
            compose_receipt(
                _input(),
                spans=spans,
                registry=_registry(),
                currency="USD",
                classification_register_version="f" * 128,
            )
