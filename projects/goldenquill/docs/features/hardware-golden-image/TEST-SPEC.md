# Test Specification: Hardware & Golden Image

Test obligations derived from the spec. IDs follow `T-{ASPECT}-{Concept}-{nn}`. Tests cover BUILD-SPEC acceptance criteria (AC1–AC5 per gap). Numeric burn-in thresholds and SKU datasheet values are decision-gated (EXT-HGI-2 / EXT-HGI-1) — those tests assert the shape and the mechanical floor/rule logic, not invented numbers.

## Operations

| ID | Concept | Asserts |
| --- | --- | --- |
| T-OP-AcceptReferenceSpec-01 | AcceptReferenceSpec | unified_memory_gb >= 128 admitted as candidate-eligible |
| T-OP-AcceptReferenceSpec-02 | AcceptReferenceSpec | unified_memory_gb < 128 rejected (MemoryFloorRule) |
| T-OP-AcceptReferenceSpec-03 | AcceptReferenceSpec | approved-alternative requires all four conditions incl. operator sign-off |
| T-OP-AcceptReferenceSpec-04 | AcceptReferenceSpec | ReferenceSpecAccepted produced on admission |
| T-OP-RunBurnIn-01 | RunBurnIn | one AcceptanceReceipt emitted on PASS |
| T-OP-RunBurnIn-02 | RunBurnIn | one AcceptanceReceipt emitted on FAIL (save-state-always) |
| T-OP-RunBurnIn-03 | RunBurnIn | each axis captures metrics even when an axis fails |
| T-OP-RunBurnIn-04 | RunBurnIn | FAIL blocks the unit from imaging |
| T-OP-RunBurnIn-05 | RunBurnIn | verdict computed from config thresholds, not hardcoded |
| T-OP-WriteAndVerifyImage-01 | WriteAndVerifyImage | invalid manifest signature fails-closed pre-write; no write; HIGH ledger entry |
| T-OP-WriteAndVerifyImage-02 | WriteAndVerifyImage | corrupted byte caught at post-write digest compare → FAIL |
| T-OP-WriteAndVerifyImage-03 | WriteAndVerifyImage | boot-manifest fails-closed on missing/modified frozen artifact |
| T-OP-WriteAndVerifyImage-04 | WriteAndVerifyImage | receipt emitted on PASS and FAIL |
| T-OP-WriteAndVerifyImage-05 | WriteAndVerifyImage | two units same SKU → identical image_version + matching digest sets |
| T-OP-RunBackup-01 | RunBackup | snapshot excludes immutable image file set |
| T-OP-RunBackup-02 | RunBackup | BackupSet encrypted with customer-held keys |
| T-OP-RunBackup-03 | RunBackup | backup receipt emitted regardless of outcome |
| T-OP-ExportVault-01 | ExportVault | archive opens on clean machine with customer keys only (no call-home) |
| T-OP-ExportVault-02 | ExportVault | export refused when more than one org in scope (Law 3) |
| T-OP-ExportVault-03 | ExportVault | open archive + open encryption format, no proprietary container |
| T-OP-RecoverNode-01 | RecoverNode | wipe → re-write → restore yields byte-identical state (round-trip digest) |
| T-OP-RecoverNode-02 | RecoverNode | recovery completes with no publisher service reachable |
| T-OP-RecoverNode-03 | RecoverNode | recovery receipt emitted regardless of outcome |

## Calculations

| ID | Concept | Asserts |
| --- | --- | --- |
| T-OP-AcceptanceVerdictCalc-01 | AcceptanceVerdictCalc | PASS iff every axis metric within its threshold |
| T-OP-AcceptanceVerdictCalc-02 | AcceptanceVerdictCalc | deterministic given the same thresholds + metrics |
| T-OP-VolumeDigestCalc-01 | VolumeDigestCalc | re-hash of written volume reproduces manifest digest set on clean write |
| T-OP-VolumeDigestCalc-02 | VolumeDigestCalc | single-byte change alters the computed digest |

## Rules

| ID | Concept | Asserts |
| --- | --- | --- |
| T-RULES-MemoryFloorRule-01 | MemoryFloorRule | 128 passes; 127 fails |
| T-RULES-ApprovedAlternativeRule-01 | ApprovedAlternativeRule | missing any of four conditions → not approved |
| T-RULES-ManifestSignatureRule-01 | ManifestSignatureRule | valid signature permits write; invalid blocks |
| T-RULES-PostWriteDigestRule-01 | PostWriteDigestRule | mismatch → FAIL |
| T-RULES-SovereignExportRule-01 | SovereignExportRule | no key material to any vendor endpoint |
| T-RULES-SingleOrgScopeRule-01 | SingleOrgScopeRule | export scope is exactly one org |
| T-RULES-RoundTripDigestRule-01 | RoundTripDigestRule | restored digest equals backup digest |
| T-RULES-BurnInThresholdRule-01 | BurnInThresholdRule | verdict keys off supplied threshold table |

## States

| ID | Concept | Asserts |
| --- | --- | --- |
| T-ST-BurnInState-01 | BurnInState | Running → Passed on verdict PASS |
| T-ST-BurnInState-02 | BurnInState | Running → Failed on verdict FAIL; unit blocked |
| T-ST-BurnInState-03 | BurnInState | receipt emitted on entry to any terminal state (HGI-INV-1) |
| T-ST-VerificationState-01 | VerificationState | Unwritten → PreWriteRejected on invalid signature; no write (HGI-INV-3) |
| T-ST-VerificationState-02 | VerificationState | Written → Verified on digest+boot OK |
| T-ST-VerificationState-03 | VerificationState | Written → Failed on digest/boot mismatch |
| T-ST-VerificationState-04 | VerificationState | receipt emitted on entry to any terminal state (HGI-INV-4) |

## Events

| ID | Concept | Asserts |
| --- | --- | --- |
| T-EV-ReferenceSpecAccepted-01 | ReferenceSpecAccepted | emitted by AcceptReferenceSpec on admission |
| T-EV-ReferenceSpecAccepted-02 | ReferenceSpecAccepted | consumed by node-on-desk-readiness |
| T-EV-BurnInCompleted-01 | BurnInCompleted | emitted by RunBurnIn carrying PASS/FAIL |
| T-EV-BurnInCompleted-02 | BurnInCompleted | only PASS units gate to imaging |
| T-EV-ImageVerified-01 | ImageVerified | emitted by WriteAndVerifyImage on PASS |
| T-EV-ImageVerified-02 | ImageVerified | consumed as white-glove verification evidence |
| T-EV-BackupCompleted-01 | BackupCompleted | emitted by RunBackup |
| T-EV-BackupCompleted-02 | BackupCompleted | recorded by audit log |
| T-EV-NodeRecovered-01 | NodeRecovered | emitted by RecoverNode on round-trip success |
| T-EV-NodeRecovered-02 | NodeRecovered | recorded by audit log |

## Workflows

| ID | Concept | Asserts |
| --- | --- | --- |
| T-WF-VerificationProcedure-01 | VerificationProcedure | burn-in PASS gates write; FAIL blocks (HGI-INV-5) |
| T-WF-VerificationProcedure-02 | VerificationProcedure | verification receipt emitted on completion |
| T-WF-RecoveryProcedure-01 | RecoveryProcedure | image re-write then state restore round-trip (HGI-INV-7) |
| T-WF-RecoveryProcedure-02 | RecoveryProcedure | no vendor endpoint contacted (HGI-INV-6) |

## Queries

| ID | Concept | Asserts |
| --- | --- | --- |
| T-QR-GetUnitReceipt-01 | GetUnitReceipt | returns the per-unit VerificationReceipt by serial |
| T-QR-GetUnitReceipt-02 | GetUnitReceipt | reads only appliance-local receipts (Law 3) |
| T-QR-GetUnitReceipt-03 | GetUnitReceipt | absent serial returns empty, no side effect |
| T-QR-GetReferenceSpec-01 | GetReferenceSpec | returns spec + SpecStatus for a SKU |
| T-QR-GetReferenceSpec-02 | GetReferenceSpec | reflects the assigned status |
| T-QR-GetReferenceSpec-03 | GetReferenceSpec | unknown SKU returns empty, no side effect |

## Mappings

| ID | Concept | Asserts |
| --- | --- | --- |
| T-MAP-ManifestToImage-01 | ManifestToImage | manifest version + digests map to on-disk image set |
| T-MAP-VaultToExportArchive-01 | VaultToExportArchive | mutable state maps to open-format archive, single-org scoped |

## Interfaces

| ID | Concept | Asserts |
| --- | --- | --- |
| T-IF-GoldenImageHandoff-01 | GoldenImageHandoff | accepts signed artifact + manifest into write+verify |
| T-IF-GoldenImageHandoff-02 | GoldenImageHandoff | Ed25519 verify against pinned pubkey before apply |
| T-IF-UnitReceiptStore-01 | UnitReceiptStore | persists + reads receipts at deploy/unit_receipts/<serial>.json |
