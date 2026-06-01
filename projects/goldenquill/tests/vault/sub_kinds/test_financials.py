"""Round-trip tests for the ``financials`` operational sub-kind. [§2.11.2, §2.13]"""

from __future__ import annotations

from pathlib import Path

import pytest

from pipeline.vault.error_codes import VaultCrossOrgAccess
from pipeline.vault.sub_kinds.financials import (
    ADMIN_RISK_SEVERITY,
    FinancialsRecord,
    INTENT,
    SUB_KIND,
    VAULT_SUBTREE,
    from_canonical_bytes,
    to_canonical_bytes,
)
from pipeline.vault.sub_kinds.registry import SUB_KIND_REGISTRY
from pipeline.vault.vault_write import vault_write


@pytest.fixture
def sample() -> FinancialsRecord:
    return FinancialsRecord(
        record_id="f-2026-05-10-001",
        amount_minor_units=12345,
        currency="USD",
        posted_at="2026-05-10T12:00:00Z",
        category="supplies",
        description="seed trays",
        vendor="Acme Supply",
    )


class TestSchemaInvariants:
    def test_amount_must_be_int_not_float(self) -> None:
        with pytest.raises(ValueError, match="amount_minor_units"):
            FinancialsRecord(
                record_id="r",
                amount_minor_units=12.5,  # type: ignore[arg-type]
                currency="USD",
                posted_at="2026-05-10T12:00:00Z",
                category="c",
                description="d",
                vendor="v",
            )

    def test_amount_rejects_bool(self) -> None:
        with pytest.raises(ValueError, match="amount_minor_units"):
            FinancialsRecord(
                record_id="r",
                amount_minor_units=True,  # type: ignore[arg-type]
                currency="USD",
                posted_at="2026-05-10T12:00:00Z",
                category="c",
                description="d",
                vendor="v",
            )

    def test_currency_must_be_3_uppercase_letters(self) -> None:
        with pytest.raises(ValueError, match="currency"):
            FinancialsRecord(
                record_id="r",
                amount_minor_units=1,
                currency="usd",
                posted_at="2026-05-10T12:00:00Z",
                category="c",
                description="d",
                vendor="v",
            )

    def test_currency_rejects_four_letters(self) -> None:
        with pytest.raises(ValueError, match="currency"):
            FinancialsRecord(
                record_id="r",
                amount_minor_units=1,
                currency="USDX",
                posted_at="2026-05-10T12:00:00Z",
                category="c",
                description="d",
                vendor="v",
            )

    def test_posted_at_must_end_with_Z(self) -> None:
        with pytest.raises(ValueError, match="posted_at"):
            FinancialsRecord(
                record_id="r",
                amount_minor_units=1,
                currency="USD",
                posted_at="2026-05-10T12:00:00",
                category="c",
                description="d",
                vendor="v",
            )


class TestCanonicalRoundTrip:
    def test_round_trip(self, sample: FinancialsRecord) -> None:
        assert from_canonical_bytes(to_canonical_bytes(sample)) == sample


class TestRegistryBinding:
    def test_descriptor_present(self) -> None:
        descriptor = SUB_KIND_REGISTRY[SUB_KIND]
        assert descriptor.intent == INTENT
        assert descriptor.severity_default == ADMIN_RISK_SEVERITY


class TestVaultRoundTrip:
    def test_write_read_decode(
        self, operational_org: dict[str, Path], sample: FinancialsRecord
    ) -> None:
        target = (
            operational_org["root"] / VAULT_SUBTREE / f"{sample.record_id}.json"
        )
        payload = to_canonical_bytes(sample)
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
        assert from_canonical_bytes(target.read_bytes()) == sample

    def test_cross_org_path_rejected(
        self,
        tmp_path: Path,
        operational_org: dict[str, Path],
        sample: FinancialsRecord,
    ) -> None:
        other_root = tmp_path / "orgs" / "other" / "vault"
        other_root.mkdir(parents=True, exist_ok=True)
        with pytest.raises(VaultCrossOrgAccess):
            vault_write(
                other_root / VAULT_SUBTREE / f"{sample.record_id}.json",
                to_canonical_bytes(sample),
                INTENT,
                "sess",
                operational_org["slug"],
                org_vault_root=operational_org["root"],
                write_lock_path=operational_org["lock"],
                write_mode="write-if-absent",
            )
