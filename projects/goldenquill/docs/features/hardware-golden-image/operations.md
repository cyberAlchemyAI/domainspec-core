# Operations: Hardware & Golden Image

Behavioral concepts: per-unit acceptance, burn-in, image write+verify, and backup/recovery operations with their rules and calculations. Receipts are emitted on success AND failure (Autonomy Rule 1). Law 3: no `orgs/` data is read; operations act on the image, the unit, and the appliance's own mutable state.

## AcceptReferenceSpec

**Type:** Operation (mutation)
**Actor:** [ReferenceWorkstationSpec](domain.md#referenceworkstationspec)
**Triggers:** [GetReferenceSpec](queries.md#getreferencespec)

Validates a SKU spec and assigns a [SpecStatus](domain.md#specstatus). Certified for the named reference SKUs; approved-alternative for SKUs that pass all four conditions; rejected otherwise. SKU datasheet values stay [OPERATOR-INPUT / EXTERNAL-DEFERRED] (EXT-HGI-1) — the floor/rule logic is complete regardless.

### Input

| Field | Type                                                          | Required | Description           |
| ----- | ------------------------------------------------------------- | -------- | --------------------- |
| spec  | [ReferenceWorkstationSpec](domain.md#referenceworkstationspec) | yes    | Candidate SKU spec    |
| operator_signoff | boolean                                            | yes      | Final approval gate   |

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| R1 | [MemoryFloorRule](#memoryfloorrule): unified memory must meet the canonical floor | `spec.unified_memory_gb >= 128` |
| R2 | [ApprovedAlternativeRule](#approvedalternativerule): non-certified SKU admitted iff all four conditions hold | `meets_memory_floor && runs_substrate && passes_burn_in && operator_signoff` |

#### MemoryFloorRule

Mechanically rejects any spec below 128GB unified memory. `unified_memory_gb < 128 → rejected`.

#### ApprovedAlternativeRule

A non-certified SKU is `approved-alternative` iff (1) meets memory floor, (2) runs substrate, (3) passes burn-in against the same threshold table, AND (4) operator sign-off recorded.

### State Transition

`[ReferenceWorkstationSpec](domain.md#referenceworkstationspec): candidate -> certified | approved-alternative | rejected`

### Postconditions

- A [SpecStatus](domain.md#specstatus) is assigned to the spec.
- A [ReferenceSpecAccepted](events.md#referencespecaccepted) event is produced on admission.

### Error States

| Condition | Result |
| --------- | ------ |
| unified_memory_gb < 128 | Spec rejected; not admitted as a Golden Quill unit |
| approved-alternative without operator sign-off | Spec stays candidate; not admitted |

---

## RunBurnIn

**Type:** Operation (mutation)
**Actor:** [GoldenImage](domain.md#goldenimage)
**Triggers:** Field Tech checklist

Runs the four-axis burn-in (thermal / memory / storage / inference) on one unit and emits an [AcceptanceReceipt](domain.md#acceptancereceipt). Each axis captures its metrics even on failure (no early-abort). Thresholds read from `burn_in_thresholds.yaml` ([BurnInThresholds](domain.md#burninthresholds)); numeric values are [OPERATOR-INPUT] pending EXT-HGI-2.

### Input

| Field      | Type                                            | Required | Description                         |
| ---------- | ----------------------------------------------- | -------- | ----------------------------------- |
| unit_serial | [UnitSerial](domain.md#unitserial)             | yes      | Unit under test                     |
| thresholds | [BurnInThresholds](domain.md#burninthresholds)  | yes      | Config thresholds (EXT-HGI-2)       |

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| R1 | [BurnInThresholdRule](#burninthresholdrule): verdict is computed against config thresholds, never hardcoded | `result == all(axis.metric within thresholds[axis])` |

#### BurnInThresholdRule

The pass/fail verdict is a function of the supplied threshold table. With thresholds deferred (EXT-HGI-2) the procedure runs and captures metrics but cannot compute a final PASS.

### Calculations

| ID | Calculation | Formula |
| --- | --- | --- |
| C1 | [AcceptanceVerdictCalc](#acceptanceverdictcalc): mechanical verdict across axes | `PASS iff every axis metric satisfies its threshold` |

### State Transition

`[GoldenImage](domain.md#goldenimage): burn-in pending -> passed | failed` (see [BurnInState](states.md#burninstate))

### Postconditions

- Exactly one [AcceptanceReceipt](domain.md#acceptancereceipt) is emitted regardless of outcome.
- A [BurnInCompleted](events.md#burnincompleted) event is produced.
- A `FAIL` blocks the unit from proceeding to imaging.

### Error States

| Condition | Result |
| --------- | ------ |
| an axis fails | Receipt result FAIL; later axes still captured; unit blocked |
| thresholds absent | Metrics captured; final verdict cannot compute (EXT-HGI-2 gate) |

---

## WriteAndVerifyImage

**Type:** Operation (mutation)
**Actor:** [GoldenImage](domain.md#goldenimage)
**Triggers:** [GoldenImageHandoff](interfaces.md#goldenimagehandoff)

Deterministically writes the signed image to the unit's encrypted target disk, then verifies in three stages: pre-write Ed25519 signature, post-write volume re-hash, and boot-time manifest. Emits a [VerificationReceipt](domain.md#verificationreceipt) on PASS and FAIL.

### Input

| Field      | Type                                          | Required | Description                       |
| ---------- | --------------------------------------------- | -------- | --------------------------------- |
| artifact   | [SignedArtifact](domain.md#signedartifact)    | yes      | Signed installable + manifest     |
| unit_serial | [UnitSerial](domain.md#unitserial)           | yes      | Target unit                       |

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| R1 | [ManifestSignatureRule](#manifestsignaturerule): manifest signature must verify before any write | `verify_ed25519(manifest, pinned_publisher_pubkey) == true` |
| R2 | [PostWriteDigestRule](#postwritedigestrule): written volume digests must match the manifest | `volume_digests == manifest.file_digests && total == manifest.total_digest` |

#### ManifestSignatureRule

Pre-write fail-closed gate. Reuses the `F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID` discipline (router.yaml 17–48). On mismatch, no write proceeds and a HIGH admin-risk ledger entry is recorded.

#### PostWriteDigestRule

After write, re-hash the written volume's files and compare to the manifest digest set; confirm the total-image digest. A single corrupted byte fails this rule.

### Calculations

| ID | Calculation | Formula |
| --- | --- | --- |
| C1 | [VolumeDigestCalc](#volumedigestcalc): re-hash written volume | `sha256(each written file) -> digest set` |

### State Transition

`[GoldenImage](domain.md#goldenimage): unwritten -> written -> verified | failed` (see [VerificationState](states.md#verificationstate))

### Postconditions

- A [VerificationReceipt](domain.md#verificationreceipt) is written to `deploy/unit_receipts/<unit_serial>.json` on every run.
- An [ImageVerified](events.md#imageverified) event is produced on PASS.
- Two units of the same SKU yield receipts with identical image_version and matching digest sets (repeatability).

### Error States

| Condition | Result |
| --------- | ------ |
| manifest signature invalid | Fail-closed at pre-write; no write; HIGH admin-risk ledger entry |
| corrupted byte on written volume | Post-write digest mismatch; receipt FAIL |
| frozen-substrate artifact missing/modified | Boot-manifest check fails-closed; receipt FAIL |

---

## RunBackup

**Type:** Operation (mutation)
**Actor:** [BackupSet](domain.md#backupset)
**Triggers:** Scheduler

Produces a scheduled encrypted snapshot of the appliance's mutable customer state to a customer-attached/local target. The immutable Golden Image is excluded (re-derivable). Disk-encryption keys remain customer-held.

### Input

| Field      | Type                                     | Required | Description                    |
| ---------- | ---------------------------------------- | -------- | ------------------------------ |
| org_slug   | string                                   | yes      | Single-org scope (Law 3)       |
| target     | string                                   | yes      | Local/customer-attached target |

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| R1 | Mutable-state only: image files excluded from the snapshot | `backup.contents ∩ image_file_set == ∅` |

### State Transition

`[BackupSet](domain.md#backupset): none -> snapshotted`

### Postconditions

- A [BackupSet](domain.md#backupset) encrypted with customer-held keys is produced.
- A [BackupCompleted](events.md#backupcompleted) event is produced.
- A backup receipt is emitted regardless of outcome.

### Error States

| Condition | Result |
| --------- | ------ |
| target unreachable | Backup receipt FAIL; no partial unencrypted spill |

---

## ExportVault

**Type:** Operation (mutation)
**Actor:** [BackupSet](domain.md#backupset)
**Triggers:** Authenticated Operator

One-command export producing a portable, customer-decryptable archive of the vault + a copy of the customer's keys + an inside-manifest, in open formats. Honors the Sovereignty Promise: openable on a machine with no Golden-Quill software.

### Input

| Field      | Type   | Required | Description                |
| ---------- | ------ | -------- | -------------------------- |
| org_slug   | string | yes      | Single-org scope (Law 3)   |

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| R1 | [SovereignExportRule](#sovereignexportrule): no key material leaves the node to any vendor endpoint | `export.keys.custody == customer && no_callhome` |
| R2 | [SingleOrgScopeRule](#singleorgscoperule): export of one node never co-mingles another org's vault | `export.orgs == {org_slug}` |

#### SovereignExportRule

The archive is decryptable by customer-held keys only; open archive + open encryption format; no proprietary container that locks the customer out; no FIT Farms/publisher dependency.

#### SingleOrgScopeRule

Law 3 structural: the export manifest is single-org scoped; cross-org vault content is never present.

### State Transition

`[BackupSet](domain.md#backupset): snapshotted -> exported`

### Postconditions

- A portable archive openable with customer-held keys on clean hardware is produced.
- The inside-manifest lists archive contents in an open format.

### Error States

| Condition | Result |
| --------- | ------ |
| more than one org in scope | Export refused (Law 3 violation) |

---

## RecoverNode

**Type:** Operation (mutation)
**Actor:** [BackupSet](domain.md#backupset)
**Triggers:** Authenticated Operator

Recovers a wiped node: re-write the Golden Image (via [WriteAndVerifyImage](#writeandverifyimage)) then restore mutable state from the latest [BackupSet](domain.md#backupset) and re-verify by digest. Must NOT require any FIT Farms/publisher-side service.

### Input

| Field      | Type                              | Required | Description                |
| ---------- | --------------------------------- | -------- | -------------------------- |
| backup     | [BackupSet](domain.md#backupset)  | yes      | Latest backup/export       |
| unit_serial | [UnitSerial](domain.md#unitserial) | yes    | Target unit                |

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| R1 | [RoundTripDigestRule](#roundtripdigestrule): restored state must be byte-identical to pre-wipe | `restored_state_digest == backup.state_digest` |

#### RoundTripDigestRule

After wipe → image re-write → state restore, the vault contents and audit log are byte-identical to pre-wipe, verified by digest.

### State Transition

`[BackupSet](domain.md#backupset): exported -> restored`

### Postconditions

- A [NodeRecovered](events.md#noderecovered) event is produced.
- A recovery receipt is emitted regardless of outcome.
- Recovery completes with no publisher-side service reachable.

### Error States

| Condition | Result |
| --------- | ------ |
| restored digest mismatch | Recovery receipt FAIL; round-trip not proven |
| image re-write fails | Recovery halts at image stage; receipt FAIL |

---

## AcceptanceVerdictCalc

**Type:** Calculation
**Calculates for:** [RunBurnIn](#runburnin)

Deterministic per-axis comparison of captured metrics against [BurnInThresholds](domain.md#burninthresholds). Pure once thresholds are supplied; produces the PASS/FAIL verdict consumed by [RunBurnIn](#runburnin).

### Input

| Field      | Type                                           | Required | Description           |
| ---------- | ---------------------------------------------- | -------- | --------------------- |
| metrics    | object                                         | yes      | Per-axis captured metrics |
| thresholds | [BurnInThresholds](domain.md#burninthresholds) | yes      | Config thresholds     |

### Formula

`verdict = PASS iff for every axis a: metric(a) satisfies thresholds[a]; else FAIL`

### Properties

- Deterministic: same metrics + same thresholds → same verdict.
- Bounded: output ∈ {PASS, FAIL}.

---

## VolumeDigestCalc

**Type:** Calculation
**Calculates for:** [WriteAndVerifyImage](#writeandverifyimage)

Deterministic re-hash of the written target volume, producing the digest set compared against the manifest by [WriteAndVerifyImage](#writeandverifyimage)'s [PostWriteDigestRule](#postwritedigestrule).

### Input

| Field        | Type   | Required | Description                  |
| ------------ | ------ | -------- | ---------------------------- |
| written_volume | string | yes    | Path to the written target volume |

### Formula

`digest_set = { sha256(file) for file in written_volume }`

### Properties

- Deterministic: identical bytes → identical digest set.
- Collision-sensitive: a single flipped byte changes the digest.
