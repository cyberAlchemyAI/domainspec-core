"""Round-trip tests for the ``timeline_of_activities`` sub-kind. [§2.11.5, §2.13]"""

from __future__ import annotations

from pathlib import Path

import pytest

from pipeline.vault.error_codes import VaultCrossOrgAccess
from pipeline.vault.sub_kinds.registry import SUB_KIND_REGISTRY
from pipeline.vault.sub_kinds.timeline_of_activities import (
    ADMIN_RISK_SEVERITY,
    INTENT,
    SUB_KIND,
    TimelineActivity,
    VAULT_SUBTREE,
    from_canonical_bytes,
    to_canonical_bytes,
)
from pipeline.vault.vault_write import vault_write


@pytest.fixture
def sample() -> TimelineActivity:
    return TimelineActivity(
        record_id="t-001",
        started_at="2026-05-10T12:00:00Z",
        ended_at="2026-05-10T15:30:00Z",
        summary="Cover crop seeding workshop",
        participants=("op-001", "op-002", "op-003"),
        location="Field A",
        outcome="6 attendees, 2 follow-up consults scheduled",
    )


class TestSchemaInvariants:
    def test_ended_after_started(self) -> None:
        with pytest.raises(ValueError, match="ended_at"):
            TimelineActivity(
                record_id="r",
                started_at="2026-05-10T12:00:00Z",
                ended_at="2026-05-10T11:00:00Z",
                summary="s",
                participants=(),
                location="",
                outcome="",
            )

    def test_summary_must_be_non_empty(self) -> None:
        with pytest.raises(ValueError, match="summary"):
            TimelineActivity(
                record_id="r",
                started_at="2026-05-10T12:00:00Z",
                ended_at=None,
                summary="",
                participants=(),
                location="",
                outcome="",
            )

    def test_ongoing_activity_allowed(self) -> None:
        # ended_at=None is ongoing — should construct cleanly.
        rec = TimelineActivity(
            record_id="r",
            started_at="2026-05-10T12:00:00Z",
            ended_at=None,
            summary="ongoing",
            participants=(),
            location="",
            outcome="",
        )
        assert rec.ended_at is None


class TestCanonicalRoundTrip:
    def test_round_trip(self, sample: TimelineActivity) -> None:
        assert from_canonical_bytes(to_canonical_bytes(sample)) == sample

    def test_round_trip_with_none_ended_at(self) -> None:
        rec = TimelineActivity(
            record_id="r",
            started_at="2026-05-10T12:00:00Z",
            ended_at=None,
            summary="ongoing",
            participants=("op-x",),
            location="",
            outcome="",
        )
        assert from_canonical_bytes(to_canonical_bytes(rec)) == rec


class TestRegistryBinding:
    def test_descriptor_present(self) -> None:
        descriptor = SUB_KIND_REGISTRY[SUB_KIND]
        assert descriptor.intent == INTENT
        assert descriptor.severity_default == ADMIN_RISK_SEVERITY


class TestVaultRoundTrip:
    def test_write_read_decode(
        self, operational_org: dict[str, Path], sample: TimelineActivity
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
        sample: TimelineActivity,
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
