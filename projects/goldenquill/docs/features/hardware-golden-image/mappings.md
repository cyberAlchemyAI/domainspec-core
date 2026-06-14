# Mappings: Hardware & Golden Image

Data transformations at the image and backup boundaries.

## ManifestToImage

Transforms a signed [ImageManifest](domain.md#imagemanifest) into the on-disk [GoldenImage](domain.md#goldenimage) file set used for write and re-hash comparison.

### Direction

Inbound (artifact → on-disk image).

### Field Mapping

| Source (manifest) | Target ([GoldenImage](domain.md#goldenimage)) | Transform | Notes |
| ----------------- | --------------------------------------------- | --------- | ----- |
| image_version     | image_version                                 | copy      | version pinned for receipts |
| file_digests      | per-file write targets                        | flash     | deterministic clone to encrypted disk |
| total_digest      | post-write compare key                        | verify    | confirms whole-image integrity |

---

## VaultToExportArchive

Transforms the appliance's mutable customer state into a portable, customer-decryptable [BackupSet](domain.md#backupset) export archive. Open formats only; customer-held keys; no vendor container.

### Direction

Outbound (vault → portable archive).

### Field Mapping

| Source (mutable state) | Target ([BackupSet](domain.md#backupset)) | Transform | Notes |
| ---------------------- | ----------------------------------------- | --------- | ----- |
| vault subtree          | archive contents                          | open-archive pack | no proprietary container |
| classification registers | archive contents                       | include   | single-org scoped (Law 3) |
| customer keys          | encrypted_with                            | customer-held | no key material to any vendor endpoint |
| state digest           | state_digest                              | sha256    | round-trip verification key |
| inside_manifest        | inside_manifest                           | open-format listing | contents enumerated for the customer |
