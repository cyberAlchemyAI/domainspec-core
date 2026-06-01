"""Cedar policy file presence + non-beneficiary policy semantics. [§6, §7]"""

from __future__ import annotations

from pathlib import Path

import pytest

from pipeline.vault.sub_kinds.policy_eval import (
    F_CEDAR_OPERATIONAL_DENIED,
    F_OPERATIONAL_PII_CONSENT_MISSING,
    F_OPERATIONAL_SCHEMA_INVALID,
    CedarOperationalDenied,
    OperationalPrincipal,
    OperationalResource,
    evaluate_operational_write,
)

_REPO_ROOT = Path(__file__).resolve().parents[3]
_POLICY = _REPO_ROOT / "pipeline" / "vault" / "policies" / "operational_subkinds.cedar"


class TestCedarPolicyFile:
    def test_policy_file_exists(self) -> None:
        assert _POLICY.is_file(), f"missing policy at {_POLICY}"

    def test_policy_text_contains_six_permit_rules(self) -> None:
        # 3 v7.2 operational-subkinds rules + 3 §17 WPFA cycle_receipt
        # extension rules (LOCKED 2026-05-11 row 205).
        text = _POLICY.read_text(encoding="utf-8")
        assert text.count("permit (") == 6, "expected exactly 6 permit rules"

    def test_policy_text_names_six_rule_anchors(self) -> None:
        text = _POLICY.read_text(encoding="utf-8")
        for anchor in (
            # v7.2 anchors
            "operational_org_isolation",
            "beneficiary_pii_anonymized",
            "beneficiary_pii_with_consent",
            # §17 WPFA anchors (LOCKED 2026-05-11)
            "cycle_receipt_org_isolation",
            "cycle_receipt_operator_attestation",
            "cycle_receipt_read_isolation",
        ):
            assert anchor in text, f"policy missing anchor {anchor!r}"


class TestNonBeneficiaryEvaluation:
    """Same-org operational writes for non-beneficiary sub-kinds pass once
    org isolation holds. Cross-org writes deny."""

    @pytest.mark.parametrize(
        "sub_kind",
        [
            "metrics",
            "financials",
            "photos",
            "narrative_entries",
            "timeline_of_activities",
            "attachments",
        ],
    )
    def test_same_org_permits(self, sub_kind: str) -> None:
        evaluate_operational_write(
            principal=OperationalPrincipal(
                session_id="s", org_slug="myco", operator_authorized_pii=False
            ),
            resource=OperationalResource(
                sub_kind=sub_kind,
                org_slug_hint="myco",
                consent_tier=None,
                pii_present=None,
            ),
        )

    @pytest.mark.parametrize(
        "sub_kind",
        [
            "metrics",
            "financials",
            "photos",
            "narrative_entries",
            "timeline_of_activities",
            "attachments",
        ],
    )
    def test_cross_org_denies(self, sub_kind: str) -> None:
        with pytest.raises(CedarOperationalDenied) as exc:
            evaluate_operational_write(
                principal=OperationalPrincipal(
                    session_id="s",
                    org_slug="myco",
                    operator_authorized_pii=False,
                ),
                resource=OperationalResource(
                    sub_kind=sub_kind,
                    org_slug_hint="other_org",
                    consent_tier=None,
                    pii_present=None,
                ),
            )
        assert exc.value.rule == "operational_org_isolation"


class TestFailureCodeSurface:
    def test_failure_codes_distinct(self) -> None:
        codes = {
            F_CEDAR_OPERATIONAL_DENIED,
            F_OPERATIONAL_PII_CONSENT_MISSING,
            F_OPERATIONAL_SCHEMA_INVALID,
        }
        assert len(codes) == 3
