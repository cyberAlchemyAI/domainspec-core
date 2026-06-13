# Events: Hardware & Golden Image

Past-tense announcements of state changes in the per-unit golden-image lifecycle.

## ReferenceSpecAccepted

**Produced by:** [AcceptReferenceSpec](operations.md#acceptreferencespec)

Fired when a SKU is admitted as a Golden Quill unit (certified or approved-alternative).

### Schema

| Field    | Type   | Description                      |
| -------- | ------ | -------------------------------- |
| sku_name | string | Admitted SKU                     |
| status   | string | certified / approved-alternative |
| operator | string | Sign-off operator                |

### Consumed By

| Consumer               | Action                                  |
| ---------------------- | --------------------------------------- |
| node-on-desk-readiness | Treat SKU as procurable Golden Quill unit |

---

## BurnInCompleted

**Produced by:** [RunBurnIn](operations.md#runburnin)
**Triggers transition:** [BurnInState](states.md#burninstate)

Fired when a unit's four-axis burn-in finishes, carrying the PASS/FAIL verdict.

### Schema

| Field       | Type   | Description           |
| ----------- | ------ | --------------------- |
| unit_serial | string | Unit tested           |
| result      | string | PASS / FAIL           |

### Consumed By

| Consumer       | Action                                       |
| -------------- | -------------------------------------------- |
| WriteAndVerify | Gate: only PASS units proceed to imaging     |

---

## ImageVerified

**Produced by:** [WriteAndVerifyImage](operations.md#writeandverifyimage)
**Triggers transition:** [VerificationState](states.md#verificationstate)

Fired when a written image is proven byte-faithful, signature-valid, and boot-manifest-valid.

### Schema

| Field         | Type   | Description       |
| ------------- | ------ | ----------------- |
| unit_serial   | string | Unit written      |
| image_version | string | Verified version  |
| total_digest  | string | Whole-image digest |

### Consumed By

| Consumer               | Action                                          |
| ---------------------- | ----------------------------------------------- |
| node-on-desk-readiness | Per-unit verification evidence for white-glove  |

---

## BackupCompleted

**Produced by:** [RunBackup](operations.md#runbackup)

Fired when an encrypted mutable-state snapshot is produced and receipted.

### Schema

| Field     | Type   | Description           |
| --------- | ------ | --------------------- |
| backup_id | string | Snapshot identifier   |
| org_slug  | string | Single-org scope      |

### Consumed By

| Consumer        | Action                          |
| --------------- | ------------------------------- |
| Audit Log       | Record backup completion        |

---

## NodeRecovered

**Produced by:** [RecoverNode](operations.md#recovernode)

Fired when a node is recovered from Golden Image + backup with byte-identical state.

### Schema

| Field       | Type   | Description       |
| ----------- | ------ | ----------------- |
| unit_serial | string | Recovered unit    |
| backup_id   | string | Source backup     |
| state_digest | string | Restored-state digest |
| operator    | string | Recovery operator |

### Consumed By

| Consumer  | Action                         |
| --------- | ------------------------------ |
| Audit Log | Record recovery round-trip     |
