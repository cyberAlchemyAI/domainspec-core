"""Round-trip tests for the ``narrative_entries`` operational sub-kind. [§2.11.4, §2.13]"""

from __future__ import annotations

from pathlib import Path

import pytest

from pipeline.vault.error_codes import VaultCrossOrgAccess
from pipeline.vault.sub_kinds.narrative_entries import (
    ADMIN_RISK_SEVERITY,
    INTENT,
    NarrativeEntry,
    SUB_KIND,
    VAULT_SUBTREE,
    from_canonical_bytes,
    to_canonical_bytes,
)
from pipeline.vault.sub_kinds.registry import SUB_KIND_REGISTRY
from pipeline.vault.vault_write import vault_write


@pytest.fixture
def sample() -> NarrativeEntry:
    return NarrativeEntry(
        record_id="n-001",
        authored_at="2026-05-10T12:00:00Z",
        author="josh@fitfarms",
        body="Site visit today; rye cover crop is breaking through.",
        tags=("site-visit", "field-A"),
    )


class TestSchemaInvariants:
    def test_body_must_be_non_empty(self) -> None:
        with pytest.raises(ValueError, match="body"):
            NarrativeEntry(
                record_id="r",
                authored_at="2026-05-10T12:00:00Z",
                author="a",
                body="",
                tags=(),
            )

    def test_author_must_be_non_empty(self) -> None:
        with pytest.raises(ValueError, match="author"):
            NarrativeEntry(
                record_id="r",
                authored_at="2026-05-10T12:00:00Z",
                author="",
                body="b",
                tags=(),
            )


class TestCanonicalRoundTrip:
    def test_round_trip(self, sample: NarrativeEntry) -> None:
        assert from_canonical_bytes(to_canonical_bytes(sample)) == sample


class TestRegistryBinding:
    def test_descriptor_present(self) -> None:
        descriptor = SUB_KIND_REGISTRY[SUB_KIND]
        assert descriptor.intent == INTENT
        assert descriptor.severity_default == ADMIN_RISK_SEVERITY


class TestVaultRoundTrip:
    def test_write_read_decode(
        self, operational_org: dict[str, Path], sample: NarrativeEntry
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
        sample: NarrativeEntry,
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
