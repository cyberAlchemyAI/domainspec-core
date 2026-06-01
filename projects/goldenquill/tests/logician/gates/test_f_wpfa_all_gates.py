"""F-WPFA-* failure-code family — predicate body tests. [§5.1.WPFA.*]

One test class per code (12 codes across 10 modules per §4 v2.x.z OQ-4
default — coefficient_registry_validation consolidates 3 codes).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from pipeline.logician.gates.f_wpfa_baseline_missing import (
    F_WPFA_BASELINE_MISSING,
    check_f_wpfa_baseline_missing,
)
from pipeline.logician.gates.f_wpfa_coefficient_registry_validation import (
    F_WPFA_COEFFICIENT_REGISTRY_UNSIGNED,
    F_WPFA_COEFFICIENT_ROLLBACK_INVALID,
    F_WPFA_COEFFICIENT_SIGNATURE_INVALID,
    check_f_wpfa_coefficient_registry_unsigned,
    check_f_wpfa_coefficient_rollback_invalid,
    check_f_wpfa_coefficient_signature_invalid,
)
from pipeline.logician.gates.f_wpfa_counterfactual_inflation import (
    F_WPFA_COUNTERFACTUAL_INFLATION,
    check_f_wpfa_counterfactual_inflation,
)
from pipeline.logician.gates.f_wpfa_cross_org_leak import (
    F_WPFA_CROSS_ORG_LEAK,
    check_f_wpfa_cross_org_leak,
)
from pipeline.logician.gates.f_wpfa_dimension_unsupported import (
    F_WPFA_DIMENSION_UNSUPPORTED,
    check_f_wpfa_dimension_unsupported,
)
from pipeline.logician.gates.f_wpfa_model_coefficient_missing import (
    F_WPFA_MODEL_COEFFICIENT_MISSING,
    check_f_wpfa_model_coefficient_missing,
)
from pipeline.logician.gates.f_wpfa_operator_signature_missing import (
    F_WPFA_OPERATOR_SIGNATURE_MISSING,
    check_f_wpfa_operator_signature_missing,
)
from pipeline.logician.gates.f_wpfa_pdf_confidential_leak import (
    F_WPFA_PDF_CONFIDENTIAL_LEAK,
    check_f_wpfa_pdf_confidential_leak,
)
from pipeline.logician.gates.f_wpfa_registry_drift import (
    F_WPFA_REGISTRY_DRIFT,
    check_f_wpfa_registry_drift,
    check_registry_version_mismatch_no_ledger_entry,
)
from pipeline.logician.gates.f_wpfa_schema_invalid import (
    F_WPFA_SCHEMA_INVALID,
    check_f_wpfa_schema_invalid,
)
from pipeline.logician.gates.f_wpfa_span_provenance_missing import (
    F_WPFA_SPAN_PROVENANCE_MISSING,
    check_f_wpfa_span_provenance_missing,
    check_pdf_claim_unlinked,
)


def _ok_verifier(message_bytes: bytes, signature: bytes, public_key: bytes) -> bool:
    return True


def _bad_verifier(message_bytes: bytes, signature: bytes, public_key: bytes) -> bool:
    return False


class TestCoefficientRegistryUnsigned:
    def test_pass_well_formed(self) -> None:
        r = check_f_wpfa_coefficient_registry_unsigned(signature_hex="a" * 128)
        assert r.success is True

    def test_none_fails(self) -> None:
        r = check_f_wpfa_coefficient_registry_unsigned(signature_hex=None)
        assert r.success is False
        assert r.failure_code == F_WPFA_COEFFICIENT_REGISTRY_UNSIGNED

    def test_empty_fails(self) -> None:
        r = check_f_wpfa_coefficient_registry_unsigned(signature_hex="")
        assert r.success is False
        assert r.failure_code == F_WPFA_COEFFICIENT_REGISTRY_UNSIGNED

    def test_wrong_length_returns_signature_invalid(self) -> None:
        r = check_f_wpfa_coefficient_registry_unsigned(signature_hex="abc")
        assert r.failure_code == F_WPFA_COEFFICIENT_SIGNATURE_INVALID
        assert r.sub_tag == "signature_bytes_invalid"


class TestCoefficientSignatureInvalid:
    def test_pass_when_verifier_returns_true(self) -> None:
        r = check_f_wpfa_coefficient_signature_invalid(
            canonical_signing_payload=b"payload",
            signature_hex="a" * 128,
            pinned_pubkey_hex="b" * 64,
            signature_verify=_ok_verifier,
        )
        assert r.success is True

    def test_fails_when_verifier_returns_false(self) -> None:
        r = check_f_wpfa_coefficient_signature_invalid(
            canonical_signing_payload=b"payload",
            signature_hex="a" * 128,
            pinned_pubkey_hex="b" * 64,
            signature_verify=_bad_verifier,
        )
        assert r.success is False
        assert r.failure_code == F_WPFA_COEFFICIENT_SIGNATURE_INVALID

    def test_verifier_raising_is_fail_closed(self) -> None:
        def boom(*args, **kwargs):
            raise RuntimeError("crypto down")

        r = check_f_wpfa_coefficient_signature_invalid(
            canonical_signing_payload=b"payload",
            signature_hex="a" * 128,
            pinned_pubkey_hex="b" * 64,
            signature_verify=boom,
        )
        assert r.success is False
        assert "RuntimeError" in r.detail

    def test_strict_identity_truthy_not_accepted(self) -> None:
        # Verifier returning a truthy non-True value MUST fail-closed.
        def truthy(*args, **kwargs) -> bool:
            return 1  # type: ignore[return-value]

        r = check_f_wpfa_coefficient_signature_invalid(
            canonical_signing_payload=b"payload",
            signature_hex="a" * 128,
            pinned_pubkey_hex="b" * 64,
            signature_verify=truthy,
        )
        assert r.success is False

    def test_wrong_pubkey_length(self) -> None:
        r = check_f_wpfa_coefficient_signature_invalid(
            canonical_signing_payload=b"p",
            signature_hex="a" * 128,
            pinned_pubkey_hex="b" * 32,  # too short
            signature_verify=_ok_verifier,
        )
        assert r.sub_tag == "pubkey_mismatch"


class TestCoefficientRollbackInvalid:
    def test_existing_target_passes(self, tmp_path: Path) -> None:
        history = tmp_path / "history"
        history.mkdir()
        target = "c" * 128
        (history / f"{target}.yaml").write_text("")
        r = check_f_wpfa_coefficient_rollback_invalid(
            rollback_target_sha3=target,
            history_dir=history,
        )
        assert r.success is True

    def test_missing_target_fails(self, tmp_path: Path) -> None:
        history = tmp_path / "history"
        history.mkdir()
        r = check_f_wpfa_coefficient_rollback_invalid(
            rollback_target_sha3="c" * 128,
            history_dir=history,
        )
        assert r.success is False
        assert r.failure_code == F_WPFA_COEFFICIENT_ROLLBACK_INVALID

    def test_invalid_target_format_fails(self, tmp_path: Path) -> None:
        r = check_f_wpfa_coefficient_rollback_invalid(
            rollback_target_sha3="not-hex",
            history_dir=tmp_path,
        )
        assert r.success is False


class TestModelCoefficientMissing:
    def test_all_present_passes(self) -> None:
        r = check_f_wpfa_model_coefficient_missing(
            span_model_ids=["a", "b"],
            registry_model_ids=["a", "b", "c"],
        )
        assert r.success is True

    def test_missing_fails(self) -> None:
        r = check_f_wpfa_model_coefficient_missing(
            span_model_ids=["a", "missing"],
            registry_model_ids=["a", "b"],
        )
        assert r.success is False
        assert r.failure_code == F_WPFA_MODEL_COEFFICIENT_MISSING
        assert r.sub_tag == "unknown_model_id"
        assert "missing" in r.missing_model_ids

    def test_deprecated_fails(self) -> None:
        r = check_f_wpfa_model_coefficient_missing(
            span_model_ids=["a"],
            registry_model_ids=["a"],
            deprecated_model_ids=["a"],
        )
        assert r.success is False
        assert r.sub_tag == "deprecated_model_referenced"


class TestBaselineMissing:
    def test_resolves_passes(self) -> None:
        r = check_f_wpfa_baseline_missing(
            baseline_model_id="claude-sonnet-4-6",
            registry_model_ids=["claude-sonnet-4-6", "other"],
        )
        assert r.success is True

    def test_empty_fails(self) -> None:
        r = check_f_wpfa_baseline_missing(
            baseline_model_id="",
            registry_model_ids=["a"],
        )
        assert r.success is False
        assert r.failure_code == F_WPFA_BASELINE_MISSING

    def test_unresolved_fails(self) -> None:
        r = check_f_wpfa_baseline_missing(
            baseline_model_id="missing",
            registry_model_ids=["a", "b"],
        )
        assert r.success is False


class TestSpanProvenanceMissing:
    def test_all_required_keys_resolve(self) -> None:
        per_claim = {
            "actual.dollars_total": ("s1",),
            "actual.watt_hours_total": ("s1",),
            "counterfactual.dollars_total": ("s1",),
            "counterfactual.watt_hours_total": ("s1",),
            "delta.dollars_saved": ("s1",),
            "delta.watt_hours_saved": ("s1",),
        }
        r = check_f_wpfa_span_provenance_missing(
            per_claim_span_ids=per_claim,
            resolvable_span_ids={"s1"},
        )
        assert r.success is True

    def test_missing_required_key_fails(self) -> None:
        per_claim = {
            "actual.dollars_total": ("s1",),
            # missing several
        }
        r = check_f_wpfa_span_provenance_missing(
            per_claim_span_ids=per_claim,
            resolvable_span_ids={"s1"},
        )
        assert r.success is False
        assert r.sub_tag == "claim_key_unmapped"

    def test_unresolvable_span_fails(self) -> None:
        per_claim = {
            "actual.dollars_total": ("ghost",),
            "actual.watt_hours_total": ("s1",),
            "counterfactual.dollars_total": ("s1",),
            "counterfactual.watt_hours_total": ("s1",),
            "delta.dollars_saved": ("s1",),
            "delta.watt_hours_saved": ("s1",),
        }
        r = check_f_wpfa_span_provenance_missing(
            per_claim_span_ids=per_claim,
            resolvable_span_ids={"s1"},
        )
        assert r.success is False
        assert r.sub_tag == "trace_id_unresolvable_in_logfire"

    def test_pdf_claim_unlinked_pass(self) -> None:
        r = check_pdf_claim_unlinked(
            pdf_rendered_claims=["actual.dollars_total"],
            per_claim_span_ids={"actual.dollars_total": ("s",)},
        )
        assert r.success is True

    def test_pdf_claim_unlinked_fail(self) -> None:
        r = check_pdf_claim_unlinked(
            pdf_rendered_claims=["actual.dollars_total", "phantom.claim"],
            per_claim_span_ids={"actual.dollars_total": ("s",)},
        )
        assert r.success is False
        assert r.sub_tag == "pdf_claim_unlinked"


class TestCounterfactualInflation:
    def test_match_passes(self) -> None:
        r = check_f_wpfa_counterfactual_inflation(
            receipt_baseline_model_id="claude-sonnet-4-6",
            registry_baseline_model_id="claude-sonnet-4-6",
        )
        assert r.success is True

    def test_mismatch_fails_p0(self) -> None:
        r = check_f_wpfa_counterfactual_inflation(
            receipt_baseline_model_id="claude-opus-4-6",  # higher cost!
            registry_baseline_model_id="claude-sonnet-4-6",
        )
        assert r.success is False
        assert r.failure_code == F_WPFA_COUNTERFACTUAL_INFLATION

    def test_buyer_attested_detail_mentions_m13(self) -> None:
        r = check_f_wpfa_counterfactual_inflation(
            receipt_baseline_model_id="x",
            registry_baseline_model_id="y",
            is_buyer_attested=True,
        )
        assert "M13 NOT permitted" in r.detail


class TestOperatorSignatureMissing:
    def test_pdf_with_signature_passes(self) -> None:
        r = check_f_wpfa_operator_signature_missing(
            signed_by_operator_ed25519="a" * 128,
            target_artifact="pdf",
        )
        assert r.success is True

    def test_pdf_with_none_signature_fails(self) -> None:
        r = check_f_wpfa_operator_signature_missing(
            signed_by_operator_ed25519=None,
            target_artifact="pdf",
        )
        assert r.success is False
        assert r.failure_code == F_WPFA_OPERATOR_SIGNATURE_MISSING

    def test_non_pdf_target_returns_pass(self) -> None:
        r = check_f_wpfa_operator_signature_missing(
            signed_by_operator_ed25519=None,
            target_artifact="dashboard",
        )
        assert r.success is True

    def test_malformed_signature_fails(self) -> None:
        r = check_f_wpfa_operator_signature_missing(
            signed_by_operator_ed25519="too-short",
            target_artifact="pdf",
        )
        assert r.success is False


class TestDimensionUnsupported:
    def test_v0_1_correct_passes(self) -> None:
        r = check_f_wpfa_dimension_unsupported(
            dimensions_active=("dollars", "energy"),
            deployment_schema_version="1.0.0",
        )
        assert r.success is True

    def test_v0_1_with_water_fails(self) -> None:
        r = check_f_wpfa_dimension_unsupported(
            dimensions_active=("dollars", "energy", "water"),
            deployment_schema_version="1.0.0",
        )
        assert r.success is False
        assert r.sub_tag == "water_at_v0_1"

    def test_v0_1_with_co2_fails(self) -> None:
        r = check_f_wpfa_dimension_unsupported(
            dimensions_active=("dollars", "energy", "co2"),
            deployment_schema_version="1.0.0",
        )
        assert r.success is False
        assert r.sub_tag == "co2_at_v0_1"


class TestRegistryDriftAdvisory:
    def test_no_local_metric_passes(self) -> None:
        r = check_f_wpfa_registry_drift(
            hardware_sku="apple_m3_ultra",
            measured_idle_watts_micro=None,
            measured_peak_watts_micro=None,
            measured_watt_hours_per_million_input_tokens_micro=None,
            measured_watt_hours_per_million_output_tokens_micro=None,
            registry_idle_watts_micro=None,
            registry_peak_watts_micro=None,
            registry_watt_hours_per_million_input_tokens_micro=None,
            registry_watt_hours_per_million_output_tokens_micro=None,
        )
        assert r.success is True

    def test_drift_within_tolerance_passes(self) -> None:
        # measured 1050 vs registry 1000 = 5% deviation, tolerance 20%
        r = check_f_wpfa_registry_drift(
            hardware_sku="apple_m3_ultra",
            measured_idle_watts_micro=10500000,
            measured_peak_watts_micro=None,
            measured_watt_hours_per_million_input_tokens_micro=None,
            measured_watt_hours_per_million_output_tokens_micro=None,
            registry_idle_watts_micro=10000000,
            registry_peak_watts_micro=None,
            registry_watt_hours_per_million_input_tokens_micro=None,
            registry_watt_hours_per_million_output_tokens_micro=None,
        )
        assert r.success is True

    def test_drift_beyond_tolerance_advisory(self) -> None:
        # measured 13000 vs registry 10000 = 30% deviation, tolerance 20%
        r = check_f_wpfa_registry_drift(
            hardware_sku="apple_m3_ultra",
            measured_idle_watts_micro=13000000,
            measured_peak_watts_micro=None,
            measured_watt_hours_per_million_input_tokens_micro=None,
            measured_watt_hours_per_million_output_tokens_micro=None,
            registry_idle_watts_micro=10000000,
            registry_peak_watts_micro=None,
            registry_watt_hours_per_million_input_tokens_micro=None,
            registry_watt_hours_per_million_output_tokens_micro=None,
        )
        assert r.success is False
        assert r.failure_code == F_WPFA_REGISTRY_DRIFT
        assert any(
            a.sub_tag == "idle_watts_drift" for a in r.advisories
        )

    def test_version_mismatch_no_ledger_fails(self) -> None:
        r = check_registry_version_mismatch_no_ledger_entry(
            receipt_registry_version="a" * 128,
            active_registry_version="b" * 128,
            admin_risk_ledger_entries_for_cycle=(),
        )
        assert r.success is False


class TestSchemaInvalidClassification:
    def test_a12_message_maps_to_numeric_field_float(self) -> None:
        r = check_f_wpfa_schema_invalid(
            error_message="amount must decode as int (A12 mandate)",
            error_type=ValueError,
        )
        assert r.success is False
        assert r.sub_tag == "numeric_field_float"

    def test_dimensions_active_classifies(self) -> None:
        r = check_f_wpfa_schema_invalid(
            error_message="dimensions_active entry 'water' not in v0.1 set",
            error_type=ValueError,
        )
        assert r.sub_tag == "dimensions_active_invalid"

    def test_unknown_message_falls_back_to_schema_drift_advisory(self) -> None:
        r = check_f_wpfa_schema_invalid(
            error_message="something unanticipated happened",
            error_type=ValueError,
        )
        assert r.sub_tag == "schema_drift_advisory"


class TestCrossOrgLeak:
    def test_matching_slug_passes(self) -> None:
        r = check_f_wpfa_cross_org_leak(
            target_write_path="orgs/fit-farms-llc/vault/operational/cycle_receipts/c.json",
            receipt_org_slug="fit-farms-llc",
        )
        assert r.success is True

    def test_mismatched_slug_fails_p0(self) -> None:
        r = check_f_wpfa_cross_org_leak(
            target_write_path="orgs/other-org/vault/operational/cycle_receipts/c.json",
            receipt_org_slug="fit-farms-llc",
        )
        assert r.success is False
        assert r.failure_code == F_WPFA_CROSS_ORG_LEAK

    def test_path_outside_subtree_fails(self) -> None:
        r = check_f_wpfa_cross_org_leak(
            target_write_path="/tmp/other.json",
            receipt_org_slug="x",
        )
        assert r.success is False


class TestPdfConfidentialLeak:
    def test_all_shareable_passes(self) -> None:
        r = check_f_wpfa_pdf_confidential_leak(
            rendered_field_paths=["client.name", "client.cycle_id"],
            classification_register={
                "client.name": "shareable",
                "client.cycle_id": "public",
            },
        )
        assert r.success is True

    def test_confidential_field_fails(self) -> None:
        r = check_f_wpfa_pdf_confidential_leak(
            rendered_field_paths=["client.name", "client.salary"],
            classification_register={
                "client.name": "shareable",
                "client.salary": "confidential",
            },
        )
        assert r.success is False
        assert r.failure_code == F_WPFA_PDF_CONFIDENTIAL_LEAK

    def test_none_register_fails_closed(self) -> None:
        r = check_f_wpfa_pdf_confidential_leak(
            rendered_field_paths=["x"],
            classification_register=None,
        )
        assert r.success is False
        assert r.sub_tag == "classification_register_unread_at_emit"

    def test_unset_field_fails_closed(self) -> None:
        r = check_f_wpfa_pdf_confidential_leak(
            rendered_field_paths=["client.name"],
            classification_register={},
        )
        assert r.success is False
