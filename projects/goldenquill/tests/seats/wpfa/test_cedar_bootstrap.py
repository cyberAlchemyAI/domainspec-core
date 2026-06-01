"""WPFA Cedar bootstrap policy tests. [§17.9]"""

from __future__ import annotations

import pytest

from pipeline.orchestrator.seats.wpfa._cedar_bootstrap import (
    CycleReceiptCedarDenied,
    CycleReceiptReadPrincipal,
    CycleReceiptResource,
    evaluate_cycle_receipt_operator_attestation,
    evaluate_cycle_receipt_read_isolation,
    evaluate_cycle_receipt_write,
    register_wpfa_policies,
)
from pipeline.vault.sub_kinds.policy_eval import (
    CedarOperationalDenied,
    OperationalPrincipal,
    OperationalResource,
)


def test_register_wpfa_policies_idempotent() -> None:
    register_wpfa_policies()
    register_wpfa_policies()  # no exception


class TestEvaluateCycleReceiptWrite:
    def test_matching_org_slug_passes(self) -> None:
        principal = OperationalPrincipal(
            session_id="op-1", org_slug="fit-farms-llc"
        )
        resource = OperationalResource(
            sub_kind="cycle_receipt",
            org_slug_hint="fit-farms-llc",
        )
        evaluate_cycle_receipt_write(principal, resource)

    def test_mismatched_slug_denies(self) -> None:
        principal = OperationalPrincipal(
            session_id="op-1", org_slug="fit-farms-llc"
        )
        resource = OperationalResource(
            sub_kind="cycle_receipt",
            org_slug_hint="other-org",
        )
        # operational_org_isolation rule raises the parent class.
        with pytest.raises(CedarOperationalDenied):
            evaluate_cycle_receipt_write(principal, resource)

    def test_wrong_sub_kind_rejected(self) -> None:
        principal = OperationalPrincipal(
            session_id="op-1", org_slug="x"
        )
        resource = OperationalResource(
            sub_kind="financials",  # not cycle_receipt
            org_slug_hint="x",
        )
        with pytest.raises(CycleReceiptCedarDenied):
            evaluate_cycle_receipt_write(principal, resource)


class TestEvaluateCycleReceiptOperatorAttestation:
    def test_pdf_with_valid_signature_passes(self) -> None:
        evaluate_cycle_receipt_operator_attestation(
            signed_by_operator_ed25519="a" * 128,
            target_artifact="pdf",
        )

    def test_pdf_without_signature_denies(self) -> None:
        with pytest.raises(CycleReceiptCedarDenied, match="M13 NOT permitted"):
            evaluate_cycle_receipt_operator_attestation(
                signed_by_operator_ed25519=None,
                target_artifact="pdf",
            )

    def test_pdf_with_malformed_signature_denies(self) -> None:
        with pytest.raises(CycleReceiptCedarDenied):
            evaluate_cycle_receipt_operator_attestation(
                signed_by_operator_ed25519="too-short",
                target_artifact="pdf",
            )

    def test_non_pdf_target_admitted_without_signature(self) -> None:
        evaluate_cycle_receipt_operator_attestation(
            signed_by_operator_ed25519=None,
            target_artifact="dashboard",
        )


class TestEvaluateCycleReceiptReadIsolation:
    def test_matching_org_slug_passes(self) -> None:
        principal = CycleReceiptReadPrincipal(
            session_id="op-1",
            principal_kind="per_org",
            org_slug="fit-farms-llc",
        )
        resource = CycleReceiptResource(
            org_slug_hint="fit-farms-llc",
            cycle_id="cyc-1",
        )
        evaluate_cycle_receipt_read_isolation(principal, resource)

    def test_mismatched_per_org_denies(self) -> None:
        principal = CycleReceiptReadPrincipal(
            session_id="op-1",
            principal_kind="per_org",
            org_slug="fit-farms-llc",
        )
        resource = CycleReceiptResource(
            org_slug_hint="other-org",
            cycle_id="cyc-1",
        )
        with pytest.raises(CycleReceiptCedarDenied):
            evaluate_cycle_receipt_read_isolation(principal, resource)

    def test_workspace_aggregate_principal_admitted(self) -> None:
        principal = CycleReceiptReadPrincipal(
            session_id="op-1",
            principal_kind="workspace_aggregate",
        )
        # Workspace aggregate may read across orgs
        for org in ("a", "b", "c"):
            evaluate_cycle_receipt_read_isolation(
                principal,
                CycleReceiptResource(
                    org_slug_hint=org,
                    cycle_id="cyc-x",
                ),
            )

    def test_per_org_principal_requires_slug(self) -> None:
        with pytest.raises(ValueError):
            CycleReceiptReadPrincipal(
                session_id="x",
                principal_kind="per_org",
                org_slug="",
            )

    def test_invalid_principal_kind_rejected(self) -> None:
        with pytest.raises(ValueError):
            CycleReceiptReadPrincipal(
                session_id="x",
                principal_kind="garbage",
            )
