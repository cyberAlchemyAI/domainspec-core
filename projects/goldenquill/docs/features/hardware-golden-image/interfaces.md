# Interfaces: Hardware & Golden Image

Internal module contracts. No external/customer-facing API surface in this feature.

## GoldenImageHandoff

**Exposes:** [WriteAndVerifyImage](operations.md#writeandverifyimage)

The handoff boundary (`GAP-TRB-GOLDEN-IMAGE-HANDOFF`) where `tilth-runtime-build` delivers the signed, versioned installable artifact + its manifest, which this feature consumes. The manifest schema is locked jointly byte-for-byte: filename, digest algorithm (SHA-256), signature scheme (Ed25519 over manifest), version field format, publisher-pubkey pinning ceremony.

### Contract

| Method | Maps To | Description |
| ------ | ------- | ----------- |
| receive_artifact([SignedArtifact](domain.md#signedartifact)) -> [WriteAndVerifyImage](operations.md#writeandverifyimage) | [SignedArtifact](domain.md#signedartifact) | Hand the signed artifact into write+verify |

### Schema

| Field             | Type   | Description                              |
| ----------------- | ------ | ---------------------------------------- |
| artifact_path     | string | Location of the signed installable       |
| manifest_filename | string | Jointly locked manifest name             |
| digest_algorithm  | string | SHA-256                                  |
| signature_scheme  | string | Ed25519 over manifest                    |

### Trust Mechanism

Publisher Ed25519 signing; white-glove-pinned publisher public key; verify before apply; fail-closed on mismatch (router.yaml 17–48; `F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID` discipline). Key rotation: new key co-signed by previous (TOFU, audited).

---

## UnitReceiptStore

**Exposes:** [GetUnitReceipt](queries.md#getunitreceipt)

The persistence boundary for per-unit receipts, pinned at `deploy/unit_receipts/<unit_serial>.json`. Receipts are written on success and failure (Autonomy Rule 1) and read back through this contract.

### Contract

| Method | Maps To | Description |
| ------ | ------- | ----------- |
| get(unit_serial) -> [GetUnitReceipt](queries.md#getunitreceipt) | [VerificationReceipt](domain.md#verificationreceipt) | Read the per-unit verification receipt |

### Schema

| Field        | Type   | Description                                   |
| ------------ | ------ | --------------------------------------------- |
| receipt_path | string | deploy/unit_receipts/<unit_serial>.json       |
| unit_serial  | string | Receipt key                                   |
