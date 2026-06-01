"""Round-trip tests for the ``attachments`` operational sub-kind. [§2.11.7, §2.13]"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from pipeline.vault.error_codes import VaultCrossOrgAccess
from pipeline.vault.sub_kinds.attachments import (
    ADMIN_RISK_SEVERITY,
    AttachmentRecord,
    INTENT,
    SUB_KIND,
    VAULT_SUBTREE,
    from_canonical_bytes,
    to_canonical_bytes,
)
from pipeline.vault.sub_kinds.registry import SUB_KIND_REGISTRY
from pipeline.vault.vault_write import vault_write


_FAKE_BLOB_HASH = hashlib.sha3_512(b"fake-attachment-bytes").hexdigest()


@pytest.fixture
def sample() -> AttachmentRecord:
    return AttachmentRecord(
        record_id="att-001",
        filename="letter_of_support.pdf",
        mime_type="application/pdf",
        content_hash=_FAKE_BLOB_HASH,
        size_bytes=23456,
        attached_to_grant_id="vapg-fy26-mycosym",
        proposal_section_anchor="appendix.letters_of_support",
        blob_relative_path="vapg-fy26/att-001.pdf",
    )


class TestSchemaInvariants:
    def test_filename_must_be_non_empty(self) -> None:
        with pytest.raises(ValueError, match="filename"):
            AttachmentRecord(
                record_id="r",
                filename="",
                mime_type="application/pdf",
                content_hash=_FAKE_BLOB_HASH,
                size_bytes=1,
                attached_to_grant_id="g",
                proposal_section_anchor="a",
                blob_relative_path="b.pdf",
            )

    def test_size_bytes_non_negative(self) -> None:
        with pytest.raises(ValueError, match="size_bytes"):
            AttachmentRecord(
                record_id="r",
                filename="f.pdf",
                mime_type="application/pdf",
                content_hash=_FAKE_BLOB_HASH,
                size_bytes=-1,
                attached_to_grant_id="g",
                proposal_section_anchor="a",
                blob_relative_path="b.pdf",
            )

    def test_content_hash_must_be_128_hex(self) -> None:
        with pytest.raises(ValueError, match="content_hash"):
            AttachmentRecord(
                record_id="r",
                filename="f.pdf",
                mime_type="application/pdf",
                content_hash="abc",
                size_bytes=1,
                attached_to_grant_id="g",
                proposal_section_anchor="a",
                blob_relative_path="b.pdf",
            )

    def test_attached_to_grant_id_must_be_non_empty(self) -> None:
        with pytest.raises(ValueError, match="attached_to_grant_id"):
            AttachmentRecord(
                record_id="r",
                filename="f.pdf",
                mime_type="application/pdf",
                content_hash=_FAKE_BLOB_HASH,
                size_bytes=1,
                attached_to_grant_id="",
                proposal_section_anchor="a",
                blob_relative_path="b.pdf",
            )


class TestCanonicalRoundTrip:
    def test_round_trip(self, sample: AttachmentRecord) -> None:
        assert from_canonical_bytes(to_canonical_bytes(sample)) == sample


class TestRegistryBinding:
    def test_descriptor_present(self) -> None:
        descriptor = SUB_KIND_REGISTRY[SUB_KIND]
        assert descriptor.intent == INTENT
        assert descriptor.severity_default == ADMIN_RISK_SEVERITY


class TestVaultRoundTrip:
    def test_write_read_decode(
        self, operational_org: dict[str, Path], sample: AttachmentRecord
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
        sample: AttachmentRecord,
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
