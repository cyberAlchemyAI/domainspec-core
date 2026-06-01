"""Round-trip tests for the ``metrics`` operational sub-kind. [§2.11.1, §2.13]"""

from __future__ import annotations

from pathlib import Path

import pytest

from pipeline.vault.error_codes import (
    CedarSection4WritePathDenied,
    VaultCrossOrgAccess,
    VaultWriteExists,
)
from pipeline.vault.sub_kinds.metrics import (
    ADMIN_RISK_SEVERITY,
    INTENT,
    MetricsRecord,
    SUB_KIND,
    VAULT_SUBTREE,
    from_canonical_bytes,
    to_canonical_bytes,
)
from pipeline.vault.sub_kinds.registry import SUB_KIND_REGISTRY
from pipeline.vault.vault_write import vault_write


@pytest.fixture
def sample() -> MetricsRecord:
    return MetricsRecord(
        record_id="m-2026-05-10-001",
        metric_name="soil_moisture_pct",
        value=42.7,
        unit="percent",
        captured_at="2026-05-10T12:00:00Z",
        source="hand_reading",
        tags=("field-A", "season-1"),
    )


class TestSchemaInvariants:
    def test_record_id_must_be_non_empty(self) -> None:
        with pytest.raises(ValueError, match="record_id"):
            MetricsRecord(
                record_id="",
                metric_name="x",
                value=1.0,
                unit="ct",
                captured_at="2026-05-10T12:00:00Z",
                source="src",
                tags=(),
            )

    def test_metric_name_must_be_non_empty(self) -> None:
        with pytest.raises(ValueError, match="metric_name"):
            MetricsRecord(
                record_id="r",
                metric_name="",
                value=1.0,
                unit="ct",
                captured_at="2026-05-10T12:00:00Z",
                source="src",
                tags=(),
            )

    def test_captured_at_must_end_with_Z(self) -> None:
        with pytest.raises(ValueError, match="captured_at"):
            MetricsRecord(
                record_id="r",
                metric_name="m",
                value=1.0,
                unit="ct",
                captured_at="2026-05-10T12:00:00",
                source="src",
                tags=(),
            )

    def test_tags_must_be_tuple_of_strings(self) -> None:
        with pytest.raises(ValueError, match="tags"):
            MetricsRecord(
                record_id="r",
                metric_name="m",
                value=1.0,
                unit="ct",
                captured_at="2026-05-10T12:00:00Z",
                source="src",
                tags=["a"],  # type: ignore[arg-type]
            )

    def test_value_rejects_bool(self) -> None:
        with pytest.raises(ValueError, match="value"):
            MetricsRecord(
                record_id="r",
                metric_name="m",
                value=True,  # type: ignore[arg-type]
                unit="ct",
                captured_at="2026-05-10T12:00:00Z",
                source="src",
                tags=(),
            )


class TestCanonicalRoundTrip:
    def test_serialize_deserialize_equal(self, sample: MetricsRecord) -> None:
        payload = to_canonical_bytes(sample)
        restored = from_canonical_bytes(payload)
        assert restored == sample

    def test_canonical_bytes_are_deterministic(self, sample: MetricsRecord) -> None:
        a = to_canonical_bytes(sample)
        b = to_canonical_bytes(sample)
        assert a == b

    def test_to_canonical_bytes_rejects_wrong_type(self) -> None:
        with pytest.raises(TypeError):
            to_canonical_bytes("not a record")  # type: ignore[arg-type]


class TestRegistryBinding:
    def test_descriptor_present(self) -> None:
        descriptor = SUB_KIND_REGISTRY[SUB_KIND]
        assert descriptor.intent == INTENT
        assert descriptor.vault_subtree == VAULT_SUBTREE
        assert descriptor.severity_default == ADMIN_RISK_SEVERITY


class TestVaultRoundTrip:
    def test_write_read_decode(
        self, operational_org: dict[str, Path], sample: MetricsRecord
    ) -> None:
        descriptor = SUB_KIND_REGISTRY[SUB_KIND]
        target = (
            operational_org["root"]
            / VAULT_SUBTREE
            / f"{descriptor.record_id_for(sample)}.json"
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
        assert target.read_bytes() == payload
        restored = from_canonical_bytes(target.read_bytes())
        assert restored == sample

    def test_write_if_absent_collision_rejected(
        self, operational_org: dict[str, Path], sample: MetricsRecord
    ) -> None:
        target = (
            operational_org["root"] / VAULT_SUBTREE / f"{sample.record_id}.json"
        )
        payload = to_canonical_bytes(sample)
        vault_write(
            target,
            payload,
            INTENT,
            "sess",
            operational_org["slug"],
            org_vault_root=operational_org["root"],
            write_lock_path=operational_org["lock"],
            write_mode="write-if-absent",
        )
        with pytest.raises(VaultWriteExists):
            vault_write(
                target,
                payload,
                INTENT,
                "sess",
                operational_org["slug"],
                org_vault_root=operational_org["root"],
                write_lock_path=operational_org["lock"],
                write_mode="write-if-absent",
            )

    def test_overwrite_mode_rejected(
        self, operational_org: dict[str, Path], sample: MetricsRecord
    ) -> None:
        target = (
            operational_org["root"] / VAULT_SUBTREE / f"{sample.record_id}.json"
        )
        with pytest.raises(CedarSection4WritePathDenied) as exc:
            vault_write(
                target,
                to_canonical_bytes(sample),
                INTENT,
                "sess",
                operational_org["slug"],
                org_vault_root=operational_org["root"],
                write_lock_path=operational_org["lock"],
                write_mode="overwrite",
            )
        assert exc.value.reason == "post_gate_mode_mismatch"

    def test_cross_org_path_rejected(
        self,
        tmp_path: Path,
        operational_org: dict[str, Path],
        sample: MetricsRecord,
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
