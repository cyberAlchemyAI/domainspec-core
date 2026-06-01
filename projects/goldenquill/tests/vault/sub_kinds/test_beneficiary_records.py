"""Round-trip + PII discipline tests for ``beneficiary_records``. [§2.11.6, §6, §7]

Covers the two enforcement layers from R.PF2 / §2 v7.2 §2.11.6:

1. Schema validator (``BeneficiaryRecord.__post_init__``) — fail-closed at
   construction time when consent_tier ↔ pii_present is inconsistent.
2. Cedar policy evaluator (``policy_eval.evaluate_operational_write``) —
   fail-closed at write time even if a tampered-on-disk record bypassed
   the schema validator.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from pipeline.vault.error_codes import VaultCrossOrgAccess
from pipeline.vault.sub_kinds.beneficiary_records import (
    ADMIN_RISK_SEVERITY,
    ADMIN_RISK_SEVERITY_ANONYMIZED,
    BeneficiaryRecord,
    CONSENT_TIER_ANONYMIZED,
    CONSENT_TIER_OPERATOR_AUTHORIZED_IDENTIFIED,
    INTENT,
    SUB_KIND,
    VAULT_SUBTREE,
    from_canonical_bytes,
    severity_for,
    to_canonical_bytes,
)
from pipeline.vault.sub_kinds.policy_eval import (
    CedarOperationalDenied,
    OperationalPIIConsentMissing,
    OperationalPrincipal,
    OperationalResource,
    evaluate_operational_write,
)
from pipeline.vault.sub_kinds.registry import SUB_KIND_REGISTRY
from pipeline.vault.vault_write import vault_write


@pytest.fixture
def anon_record() -> BeneficiaryRecord:
    return BeneficiaryRecord(
        record_id="b-anon-001",
        beneficiary_opaque_id="op-aaaa-1111",
        service="cover-crop-workshop",
        outcome="enrolled",
        consent_tier=CONSENT_TIER_ANONYMIZED,
        pii_present=False,
        pii_fields=(),
        captured_at="2026-05-10T12:00:00Z",
    )


@pytest.fixture
def pii_record() -> BeneficiaryRecord:
    return BeneficiaryRecord(
        record_id="b-pii-001",
        beneficiary_opaque_id="op-bbbb-2222",
        service="financial-coaching",
        outcome="completed",
        consent_tier=CONSENT_TIER_OPERATOR_AUTHORIZED_IDENTIFIED,
        pii_present=True,
        pii_fields=("legal_name", "dob"),
        captured_at="2026-05-10T12:00:00Z",
    )


# ---------------------------------------------------------------------------
# Schema validator — layer 1
# ---------------------------------------------------------------------------


class TestSchemaPIIConsistency:
    def test_anon_with_pii_fields_rejected(self) -> None:
        with pytest.raises(ValueError, match="pii_fields"):
            BeneficiaryRecord(
                record_id="r",
                beneficiary_opaque_id="op-x",
                service="s",
                outcome="o",
                consent_tier=CONSENT_TIER_ANONYMIZED,
                pii_present=False,
                pii_fields=("name",),
                captured_at="2026-05-10T12:00:00Z",
            )

    def test_pii_present_with_anon_tier_rejected(self) -> None:
        with pytest.raises(ValueError, match="consent_tier"):
            BeneficiaryRecord(
                record_id="r",
                beneficiary_opaque_id="op-x",
                service="s",
                outcome="o",
                consent_tier=CONSENT_TIER_ANONYMIZED,
                pii_present=True,
                pii_fields=("name",),
                captured_at="2026-05-10T12:00:00Z",
            )

    def test_pii_present_with_empty_pii_fields_rejected(self) -> None:
        with pytest.raises(ValueError, match="pii_fields"):
            BeneficiaryRecord(
                record_id="r",
                beneficiary_opaque_id="op-x",
                service="s",
                outcome="o",
                consent_tier=CONSENT_TIER_OPERATOR_AUTHORIZED_IDENTIFIED,
                pii_present=True,
                pii_fields=(),
                captured_at="2026-05-10T12:00:00Z",
            )

    def test_anon_with_no_pii_constructs(self, anon_record: BeneficiaryRecord) -> None:
        assert anon_record.pii_present is False

    def test_identified_with_pii_constructs(self, pii_record: BeneficiaryRecord) -> None:
        assert pii_record.pii_present is True

    def test_unknown_consent_tier_rejected(self) -> None:
        with pytest.raises(ValueError, match="consent_tier"):
            BeneficiaryRecord(
                record_id="r",
                beneficiary_opaque_id="op-x",
                service="s",
                outcome="o",
                consent_tier="public",
                pii_present=False,
                pii_fields=(),
                captured_at="2026-05-10T12:00:00Z",
            )


# ---------------------------------------------------------------------------
# Severity
# ---------------------------------------------------------------------------


class TestSeverity:
    def test_pii_record_is_red(self, pii_record: BeneficiaryRecord) -> None:
        assert severity_for(pii_record) == ADMIN_RISK_SEVERITY
        assert severity_for(pii_record) == "RED"

    def test_anon_record_is_yellow(self, anon_record: BeneficiaryRecord) -> None:
        assert severity_for(anon_record) == ADMIN_RISK_SEVERITY_ANONYMIZED
        assert severity_for(anon_record) == "YELLOW"

    def test_registry_severity_for_routes_per_record(
        self, anon_record: BeneficiaryRecord, pii_record: BeneficiaryRecord
    ) -> None:
        descriptor = SUB_KIND_REGISTRY[SUB_KIND]
        assert descriptor.severity_for(anon_record) == "YELLOW"
        assert descriptor.severity_for(pii_record) == "RED"


# ---------------------------------------------------------------------------
# Canonical round-trip
# ---------------------------------------------------------------------------


class TestCanonicalRoundTrip:
    def test_anon_round_trip(self, anon_record: BeneficiaryRecord) -> None:
        assert from_canonical_bytes(to_canonical_bytes(anon_record)) == anon_record

    def test_pii_round_trip(self, pii_record: BeneficiaryRecord) -> None:
        assert from_canonical_bytes(to_canonical_bytes(pii_record)) == pii_record


# ---------------------------------------------------------------------------
# Cedar evaluator — layer 2
# ---------------------------------------------------------------------------


class TestCedarPIIEnforcement:
    def test_anon_write_permitted_for_same_org_without_pii_flag(self) -> None:
        evaluate_operational_write(
            principal=OperationalPrincipal(
                session_id="s", org_slug="myco", operator_authorized_pii=False
            ),
            resource=OperationalResource(
                sub_kind=SUB_KIND,
                org_slug_hint="myco",
                consent_tier=CONSENT_TIER_ANONYMIZED,
                pii_present=False,
            ),
        )

    def test_pii_write_permitted_with_operator_authorized(self) -> None:
        evaluate_operational_write(
            principal=OperationalPrincipal(
                session_id="s", org_slug="myco", operator_authorized_pii=True
            ),
            resource=OperationalResource(
                sub_kind=SUB_KIND,
                org_slug_hint="myco",
                consent_tier=CONSENT_TIER_OPERATOR_AUTHORIZED_IDENTIFIED,
                pii_present=True,
            ),
        )

    def test_pii_write_without_operator_authorization_denied(self) -> None:
        with pytest.raises(OperationalPIIConsentMissing):
            evaluate_operational_write(
                principal=OperationalPrincipal(
                    session_id="s",
                    org_slug="myco",
                    operator_authorized_pii=False,
                ),
                resource=OperationalResource(
                    sub_kind=SUB_KIND,
                    org_slug_hint="myco",
                    consent_tier=CONSENT_TIER_OPERATOR_AUTHORIZED_IDENTIFIED,
                    pii_present=True,
                ),
            )

    def test_cross_org_denied(self) -> None:
        with pytest.raises(CedarOperationalDenied) as exc:
            evaluate_operational_write(
                principal=OperationalPrincipal(
                    session_id="s",
                    org_slug="myco",
                    operator_authorized_pii=True,
                ),
                resource=OperationalResource(
                    sub_kind=SUB_KIND,
                    org_slug_hint="other_org",
                    consent_tier=CONSENT_TIER_ANONYMIZED,
                    pii_present=False,
                ),
            )
        assert exc.value.rule == "operational_org_isolation"

    def test_anon_with_pii_present_combination_denied(self) -> None:
        # Tampered shape — anonymized tier yet pii_present=True.
        with pytest.raises(OperationalPIIConsentMissing):
            evaluate_operational_write(
                principal=OperationalPrincipal(
                    session_id="s",
                    org_slug="myco",
                    operator_authorized_pii=False,
                ),
                resource=OperationalResource(
                    sub_kind=SUB_KIND,
                    org_slug_hint="myco",
                    consent_tier=CONSENT_TIER_ANONYMIZED,
                    pii_present=True,
                ),
            )


# ---------------------------------------------------------------------------
# Vault round-trip
# ---------------------------------------------------------------------------


class TestVaultRoundTrip:
    def test_anon_write_read_decode(
        self, operational_org: dict[str, Path], anon_record: BeneficiaryRecord
    ) -> None:
        target = (
            operational_org["root"]
            / VAULT_SUBTREE
            / f"{anon_record.record_id}.json"
        )
        payload = to_canonical_bytes(anon_record)
        ack = vault_write(
            target,
            payload,
            INTENT,
            "sess",
            operational_org["slug"],
            org_vault_root=operational_org["root"],
            write_lock_path=operational_org["lock"],
            write_mode="write-if-absent",
        )
        assert ack.committed
        assert from_canonical_bytes(target.read_bytes()) == anon_record

    def test_pii_write_read_decode(
        self, operational_org: dict[str, Path], pii_record: BeneficiaryRecord
    ) -> None:
        target = (
            operational_org["root"]
            / VAULT_SUBTREE
            / f"{pii_record.record_id}.json"
        )
        payload = to_canonical_bytes(pii_record)
        ack = vault_write(
            target,
            payload,
            INTENT,
            "sess",
            operational_org["slug"],
            org_vault_root=operational_org["root"],
            write_lock_path=operational_org["lock"],
            write_mode="write-if-absent",
        )
        assert ack.committed
        assert from_canonical_bytes(target.read_bytes()) == pii_record

    def test_cross_org_path_rejected(
        self,
        tmp_path: Path,
        operational_org: dict[str, Path],
        anon_record: BeneficiaryRecord,
    ) -> None:
        other_root = tmp_path / "orgs" / "other" / "vault"
        other_root.mkdir(parents=True, exist_ok=True)
        with pytest.raises(VaultCrossOrgAccess):
            vault_write(
                other_root / VAULT_SUBTREE / f"{anon_record.record_id}.json",
                to_canonical_bytes(anon_record),
                INTENT,
                "sess",
                operational_org["slug"],
                org_vault_root=operational_org["root"],
                write_lock_path=operational_org["lock"],
                write_mode="write-if-absent",
            )
