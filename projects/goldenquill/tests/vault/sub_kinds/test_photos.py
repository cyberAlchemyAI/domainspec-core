"""Round-trip tests for the ``photos`` operational sub-kind. [§2.11.3, §2.13]"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from pipeline.vault.error_codes import VaultCrossOrgAccess
from pipeline.vault.sub_kinds.photos import (
    ADMIN_RISK_SEVERITY,
    INTENT,
    PhotoRecord,
    SUB_KIND,
    VAULT_SUBTREE,
    from_canonical_bytes,
    to_canonical_bytes,
)
from pipeline.vault.sub_kinds.registry import SUB_KIND_REGISTRY
from pipeline.vault.vault_write import vault_write


_FAKE_BLOB_HASH = hashlib.sha3_512(b"fake-photo-bytes").hexdigest()


@pytest.fixture
def sample() -> PhotoRecord:
    return PhotoRecord(
        record_id="p-001",
        blob_relative_path="2026/05/p-001.jpg",
        content_hash=_FAKE_BLOB_HASH,
        mime_type="image/jpeg",
        captured_at="2026-05-10T12:00:00Z",
        caption="Field A baseline",
        geo_lat=40.7128,
        geo_lon=-74.0060,
    )


class TestSchemaInvariants:
    def test_content_hash_must_be_128_hex(self) -> None:
        with pytest.raises(ValueError, match="content_hash"):
            PhotoRecord(
                record_id="r",
                blob_relative_path="x.jpg",
                content_hash="abc",
                mime_type="image/jpeg",
                captured_at="2026-05-10T12:00:00Z",
                caption="",
                geo_lat=None,
                geo_lon=None,
            )

    def test_mime_type_must_be_image(self) -> None:
        with pytest.raises(ValueError, match="mime_type"):
            PhotoRecord(
                record_id="r",
                blob_relative_path="x.jpg",
                content_hash=_FAKE_BLOB_HASH,
                mime_type="text/plain",
                captured_at="2026-05-10T12:00:00Z",
                caption="",
                geo_lat=None,
                geo_lon=None,
            )

    def test_geo_must_be_both_or_neither(self) -> None:
        with pytest.raises(ValueError, match="geo"):
            PhotoRecord(
                record_id="r",
                blob_relative_path="x.jpg",
                content_hash=_FAKE_BLOB_HASH,
                mime_type="image/jpeg",
                captured_at="2026-05-10T12:00:00Z",
                caption="",
                geo_lat=40.0,
                geo_lon=None,
            )

    def test_geo_lat_range(self) -> None:
        with pytest.raises(ValueError, match="geo_lat"):
            PhotoRecord(
                record_id="r",
                blob_relative_path="x.jpg",
                content_hash=_FAKE_BLOB_HASH,
                mime_type="image/jpeg",
                captured_at="2026-05-10T12:00:00Z",
                caption="",
                geo_lat=999.0,
                geo_lon=0.0,
            )


class TestCanonicalRoundTrip:
    def test_round_trip_with_geo(self, sample: PhotoRecord) -> None:
        assert from_canonical_bytes(to_canonical_bytes(sample)) == sample

    def test_round_trip_without_geo(self) -> None:
        no_geo = PhotoRecord(
            record_id="p-002",
            blob_relative_path="2026/05/p-002.jpg",
            content_hash=_FAKE_BLOB_HASH,
            mime_type="image/jpeg",
            captured_at="2026-05-10T12:00:00Z",
            caption="No EXIF geo",
            geo_lat=None,
            geo_lon=None,
        )
        assert from_canonical_bytes(to_canonical_bytes(no_geo)) == no_geo


class TestRegistryBinding:
    def test_descriptor_present(self) -> None:
        descriptor = SUB_KIND_REGISTRY[SUB_KIND]
        assert descriptor.intent == INTENT
        assert descriptor.severity_default == ADMIN_RISK_SEVERITY


class TestVaultRoundTrip:
    def test_write_read_decode(
        self, operational_org: dict[str, Path], sample: PhotoRecord
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
        sample: PhotoRecord,
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
