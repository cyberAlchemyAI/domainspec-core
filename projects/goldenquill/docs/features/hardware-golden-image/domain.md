# Domain: Hardware & Golden Image

Structural concepts for the per-unit golden-image lifecycle. Law 3: nothing here reads `orgs/` client data — entities describe the image, the unit, and the appliance's own mutable state only.

## Entities

### GoldenImage

The immutable, signed, versioned appliance image written onto a unit. Re-derivable from its [SignedArtifact](#signedartifact); does not itself require backup (only re-writing). Carries the frozen substrate (Ollama/vLLM, Logician/Cedar, parsing utils) with no marketplace access.

| Field        | Type                                       | Required | Description                                  |
| ------------ | ------------------------------------------ | -------- | -------------------------------------------- |
| image_version | string                                    | yes      | Version field format coordinated with tilth-runtime-build |
| manifest     | [ImageManifest](#imagemanifest)            | yes      | Embedded per-file digest set + total digest  |
| artifact     | [SignedArtifact](#signedartifact)          | yes      | The signed installable source               |

**Operations:** [WriteAndVerifyImage](operations.md#writeandverifyimage), [RunBurnIn](operations.md#runburnin)
**Contains:** [ImageManifest](#imagemanifest)
**Emits:** [ImageVerified](events.md#imageverified)

---

### SignedArtifact

The signed, versioned installable artifact produced by `tilth-runtime-build` and consumed across the [GoldenImageHandoff](interfaces.md#goldenimagehandoff). Carries the publisher Ed25519 signature over the manifest; verified against the white-glove-pinned publisher public key before any write.

| Field            | Type                            | Required | Description                                |
| ---------------- | ------------------------------- | -------- | ------------------------------------------ |
| artifact_path    | string                          | yes      | On-disk location of the installable        |
| manifest         | [ImageManifest](#imagemanifest) | yes      | Manifest the signature covers              |
| ed25519_signature | string                         | yes      | Publisher signature over the manifest bytes |

**Operations:** [WriteAndVerifyImage](operations.md#writeandverifyimage)

---

### AcceptanceReceipt

The gate artifact emitted by burn-in. A `FAIL` blocks the unit from proceeding to imaging. Emitted on PASS and FAIL (Autonomy Rule 1: save state always).

| Field      | Type                                   | Required | Description                              |
| ---------- | -------------------------------------- | -------- | ---------------------------------------- |
| unit_serial | [UnitSerial](#unitserial)             | yes      | The unit under test                      |
| sku        | string                                 | yes      | SKU label                                |
| thermal    | object                                 | yes      | Captured thermal metrics                 |
| memory     | object                                 | yes      | Captured memory metrics                  |
| storage    | object                                 | yes      | Captured storage metrics                 |
| inference  | object                                 | yes      | Captured inference-benchmark metrics     |
| result     | [ReceiptResult](#receiptresult)        | yes      | PASS / FAIL                              |
| operator   | string                                 | yes      | Field tech who ran it                    |
| timestamp  | string                                 | yes      | ISO-8601                                 |

**Contains:** [UnitSerial](#unitserial)
**Operations:** [RunBurnIn](operations.md#runburnin)

---

### VerificationReceipt

Per-unit record proving the written image is byte-faithful, signature-valid, and boot-manifest-valid. Emitted on PASS and FAIL. Pinned on-disk at `deploy/unit_receipts/<unit_serial>.json`.

| Field                     | Type                                   | Required | Description                              |
| ------------------------- | -------------------------------------- | -------- | ---------------------------------------- |
| unit_serial               | [UnitSerial](#unitserial)              | yes      | The unit written                         |
| image_version             | string                                 | yes      | Version written                          |
| manifest_signature_status | string                                 | yes      | Pre-write Ed25519 verify outcome         |
| prewrite_verify           | string                                 | yes      | Pre-write stage result                   |
| postwrite_digest_match    | boolean                                | yes      | Post-write re-hash matched manifest      |
| boot_manifest_status      | string                                 | yes      | Boot-time manifest check outcome         |
| result                    | [ReceiptResult](#receiptresult)        | yes      | PASS / FAIL                              |
| operator                  | string                                 | yes      | Field tech                               |
| timestamp                 | string                                 | yes      | ISO-8601                                 |

**Contains:** [UnitSerial](#unitserial)
**Operations:** [WriteAndVerifyImage](operations.md#writeandverifyimage)

---

### BackupSet

An encrypted snapshot of the appliance's mutable customer state (vault, classification registers, drafts, cycle receipts, audit log, keys). Immutable image is excluded. Encrypted with customer-held keys; no key material leaves the node.

| Field          | Type                              | Required | Description                                  |
| -------------- | --------------------------------- | -------- | -------------------------------------------- |
| backup_id      | string                            | yes      | Snapshot identifier                          |
| org_slug       | string                            | yes      | Single-org scope (Law 3)                     |
| inside_manifest | object                           | yes      | Open-format listing of archive contents      |
| state_digest   | [Digest](#digest)                 | yes      | Digest of the captured mutable state         |
| encrypted_with | string                           | yes      | Customer-held key identifier (no vendor key) |

**Operations:** [RunBackup](operations.md#runbackup), [ExportVault](operations.md#exportvault), [RecoverNode](operations.md#recovernode)
**Emits:** [BackupCompleted](events.md#backupcompleted)

---

### ReferenceWorkstationSpec

A testable spec for a Golden Quill unit derived from a named reference SKU. The 128GB unified-memory floor is canonical; 32/64GB references are stale. SKU datasheet values are [OPERATOR-INPUT / EXTERNAL-DEFERRED] pending **EXT-HGI-1** — never fabricated.

| Field             | Type                            | Required | Description                                          |
| ----------------- | ------------------------------- | -------- | ---------------------------------------------------- |
| sku_name          | string                          | yes      | e.g. "Apple M3 Ultra Mac Studio" [OPERATOR-INPUT]    |
| status            | [SpecStatus](#specstatus)       | yes      | certified / approved-alternative / candidate / rejected |
| unified_memory_gb | integer                         | yes      | MUST be >= 128 [OPERATOR-INPUT exact]                |
| storage_min_gb    | integer                         | yes      | [OPERATOR-INPUT]                                     |
| substrate_compat  | boolean                         | yes      | Runs frozen substrate (Ollama/vLLM)                  |

**Operations:** [AcceptReferenceSpec](operations.md#acceptreferencespec)

---

## Value Objects

### ImageManifest

The signed inventory of a Golden Image: per-file SHA-256 digest set plus a total-image digest and the version.

| Field        | Type                          | Constraint                          |
| ------------ | ----------------------------- | ----------------------------------- |
| image_version | string                       | Coordinated with tilth-runtime-build |
| file_digests | list of [Digest](#digest)     | One per image file (SHA-256)        |
| total_digest | [Digest](#digest)             | Digest over the whole image         |

**Equality:** Two manifests are equal iff version, file-digest set, and total digest all match.

---

### UnitSerial

A stable per-unit hardware identifier used to key all per-unit receipts.

| Field  | Type   | Constraint              |
| ------ | ------ | ----------------------- |
| serial | string | Non-empty; unit-unique  |

**Equality:** Equal by serial string.

---

### Digest

A SHA-256 content digest.

| Field | Type   | Constraint            |
| ----- | ------ | --------------------- |
| algo  | string | Fixed "sha-256"       |
| hex   | string | 64-char lowercase hex |

**Equality:** Equal by (algo, hex).

---

### BurnInThresholds

The config input carrying per-axis pass/fail thresholds. Values are [OPERATOR-INPUT] pending **EXT-HGI-2**; this is a config file (`burn_in_thresholds.yaml`), never hardcoded.

| Field            | Type    | Constraint                              |
| ---------------- | ------- | --------------------------------------- |
| max_temp_c       | number  | [OPERATOR-INPUT] (EXT-HGI-2)            |
| zero_error_passes | integer | [OPERATOR-INPUT] (EXT-HGI-2)           |
| min_throughput   | number  | [OPERATOR-INPUT] (EXT-HGI-2)            |
| min_tokens_per_sec | number | [OPERATOR-INPUT] (EXT-HGI-2)           |
| max_ttft_ms      | number  | [OPERATOR-INPUT] (EXT-HGI-2)            |

**Equality:** Equal by all threshold fields.

---

## Enums

### SpecStatus

| Value                | Description                                          |
| -------------------- | ---------------------------------------------------- |
| certified            | Named reference SKU, datasheet-confirmed             |
| approved-alternative | Passes the four-condition approved-alternative rule  |
| candidate            | Under evaluation                                     |
| rejected             | Fails the memory floor or approved-alternative rule  |

### ReceiptResult

| Value | Description                          |
| ----- | ------------------------------------ |
| PASS  | All checks/axes met their criteria   |
| FAIL  | One or more checks/axes failed       |

### VerificationStage

| Value         | Description                                       |
| ------------- | ------------------------------------------------- |
| prewrite      | Manifest Ed25519 signature verify (pre-write gate) |
| postwrite     | Re-hash written volume, compare to manifest       |
| boot-manifest | First-boot Golden Image manifest check            |
