---
title: §0.5 Blueprint Interface Index — §4 v2.x WS-L gate-family rows amendment (LOCKED 2026-05-10)
filed: 2026-05-10
operator: Josh
status: LOCKED 2026-05-10 — compound paired-commit with §4 v2.x LOCK per §6.17 Option-B. L-005 strict two-cycle CLOSED with FULL cross-family rigor (audit trail at pipeline/validation/v4_v2_x_thesis_2026-05-10/). Cycle 2 PARTIAL closures REJECTED with rationale + NEW defense-in-depth notes folded into §16.10.5 deferred items per row-170 transparent disposition pattern (mirrors WS-D v7.0.5 row 179 + WS-B v7.0.7 row 180 + WS-C-M1 v7.0.4-M1 row 190 + §15 Archivist row 191 precedents).
parent_locks:
  - pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md                                 # §0.5 v5 LOCKED 2026-04-19 — 101 master rows
  - pipeline/blueprint/v0.1/section_00_5_section_06_operating_envelope_amendment.md                # §0.5 v6 LOCKED 2026-04-21 — rows 102-117
  - pipeline/blueprint/v0.1/section_00_5_section_07_scribe_amendment.md                            # §0.5 v7 LOCKED 2026-04-21 — rows 118-158
  - pipeline/blueprint/v0.1/section_00_5_section_10_red_team_amendment.md                          # §0.5 v8 LOCKED 2026-05-02 — rows 159-211
  - pipeline/blueprint/v0.1/section_00_5_section_12_uploader_amendment.md                          # §0.5 v9 LOCKED 2026-05-10 — rows 212-232
  - pipeline/blueprint/v0.1/section_00_5_section_11_intake_amendment.md                            # §0.5 v10 LOCKED 2026-05-10 — rows 233-256
  - pipeline/blueprint/v0.1/section_00_5_section_02_v7_2_operational_amendment.md                  # §0.5 v11 LOCKED 2026-05-10 — rows 257-278
  - pipeline/blueprint/v0.1/section_00_5_section_05_v8_amendment.md                                # §0.5 v12 LOCKED 2026-05-10 — rows 279-290
  - pipeline/blueprint/v0.1/section_00_5_section_15_archivist_amendment.md                         # §0.5 v13 LOCKED 2026-05-10 — rows 291-304
  - pipeline/blueprint/v0.1/section_04_v2_x_amendment.md                                           # §4 v2.x LOCKED 2026-05-10
companion_blueprint_amendment: pipeline/blueprint/v0.1/section_04_v2_x_amendment.md  # paired-commit at §4 v2.x LOCK per §6.17 Option-B
compound_lock_with: section_04_v2_x_amendment.md
parent_wins_discipline: each row's parent_lock_version + parent_lock_commit_hash point at §4 v2.x; resolves to actual commit hash at LOCK ceremony.
row_delta: prior runtime-live total at §0.5 v13 LOCK 2026-05-10 = 304 rows. **§4 v2.x amendment claims rows 305-348 (44 rows: 1 marker + 43 failure-code rows across the four slices' v0.2 gate families).** New runtime-live total at this LOCK = 348.
kind_of_amendment: row-append. NO vocabulary extension — every row's `primitive_kind` resolves against the v5 + v6 16-value closed vocabulary (marker / schema / interface-contract / failure-code / pre-gate-check / post-gate-check).
dependency_order: §4 v2.x amendment LOCK + this §0.5 amendment land as a single compound paired-commit at the same `lock_timestamp_utc`.
f_index_stale_preflight: F-INDEX-STALE PRE-gate fires at commit time; all 44 new rows must be present in the index or the commit fails closed.
cross_family_posture: LIVE FULL CROSS-FAMILY (no Section E carve-out) per WS-D v7.0.5 LOCK precedent (lock_history row 179, 2026-05-10). Seventh substantive v0.1+v0.2 round to LOCK at this rigor level (after WS-D v7.0.5 + WS-F §12 v1 + WS-E §11 v1 + WS-H §2 v7.2 + WS-G §5 v8 + WS-C-M1 v7.0.4-M1 + §15 Archivist v1 precedents).
---

# Amendment intent

This amendment lands paired with §4 v2.x LOCK per §6.17 Option-B compound-commit pattern. It registers §4 v2.x-owned failure-code primitives — 44 codes across four slice families (Funder Intel + KFR residuals + F-CLASS-* dormant primitives + v7.0.4-M1 corrective predicates) plus a section-marker. It does NOT register `pre-gate-check` / `post-gate-check` rows individually — those rows are derivable from the failure-code row plus the §4 v2.x amendment's PRE/POST tables (per §4 v2.x §1.1, §1.2, §3.1, §3.2, §4.1, §4.2, §16.4, §16.5). Future §0.5 amendments at the §4 v3 horizon may explode the individual gate-check rows; at v2.x the failure-code rows are the load-bearing primitives.

The §11 amendment (§0.5 v10 LOCKED 2026-05-10 with rows 233-256 across 24 rows for §11 Intake), §12 amendment (§0.5 v9 LOCKED 2026-05-10 with rows 212-232 across 21 rows for §12 Uploader), and §15 amendment (§0.5 v13 LOCKED 2026-05-10 with rows 291-304 across 14 rows for §15 Archivist) are the load-bearing precedents for per-section gate-family registration in the Index.

The master `section_00_5_interface_index_locked.md` remains LOCKED v5 on-disk; this amendment file is runtime-live at compound LOCK with §4 v2.x. Future master re-author folds all v6 / v7 / v8 / v9 / v10 / v11 / v12 / v13 / this amendment files into the master.

# Amendment §A — row append (rows 305-348)

All rows enter §0.5 at `stability_tier = "STABLE"` at compound v2.x LOCK (no PARENT_UNLOCKED transit since §4 v2.x LOCKs in the same compound transaction).

**Marker (row 305) — §4 v2.x amendment anchor:**

| Row | primitive_id | defined_at | parent_lock_version | parent_lock_commit_hash | kind | stability_tier |
|---|---|---|---|---|---|---|
| 305 | `blueprint.amendment_anchor.s4_v2_x.v1` | `pipeline/blueprint/v0.1/section_04_v2_x_amendment.md` | §4 v2.x | `<resolved_at_commit>` | marker | STABLE |

**Failure-code rows (rows 306-348) — 43 codes across four slices:**

Per §6.17 Option-B paired-commit pattern, all 43 codes registered as `failure-code` `primitive_kind` with parent §4 v2.x v1. Defined-at column points at the §4 v2.x amendment section that owns the row (§1, §2, §3, §4, §16); the per-code module path lives in the on-disk `pipeline/logician/gates/` tree.

**Slice 1 — Funder Intel family (7 codes; rows 306-312):**

| Row | primitive_id | defined_at | tier |
|---|---|---|---|
| 306 | `logician.failure_code.F-MATCH-DB-CROSS-ORG.v1` | §4 v2.x §1 (Funder Intel) | PRE |
| 307 | `logician.failure_code.F-VECTOR-NS-MISMATCH.v1` | §4 v2.x §1 (Funder Intel) | PRE |
| 308 | `logician.failure_code.F-CHANNEL-G-CROSS-ORG-LEAK.v1` | §4 v2.x §1 (Funder Intel) | POST-extract |
| 309 | `logician.failure_code.F-CHANNEL-G-SANITIZATION-BYPASS.v1` | §4 v2.x §1 (Funder Intel) | advisory |
| 310 | `logician.failure_code.F-MATCH-DB-CONSENT-TIER-VIOLATION.v1` | §4 v2.x §1 (Funder Intel) | PRE-write + Stage-5-read |
| 311 | `logician.failure_code.F-FUNDER-CORPUS-STALE.v1` | §4 v2.x §1 (Funder Intel) | POST-cite |
| 312 | `logician.failure_code.F-FUNDER-CORPUS-INTEGRITY.v1` | §4 v2.x §1 (Funder Intel) | PRE-load + POST-load |

**Slice 2 — KFR family residuals (7 codes including 1 supersession-renamed in Slice 4; rows 313-319):**

| Row | primitive_id | defined_at | tier |
|---|---|---|---|
| 313 | `logician.failure_code.F-EXTRACTOR-FABRICATION.v1` | §4 v2.x §3 (KFR residuals) | PRE-pre-queue |
| 314 | `logician.failure_code.F-EXTRACTOR-AWARD-SIGNATURE-INVALID.v1` (umbrella `.proposal` + `.award`) | §4 v2.x §3 (KFR residuals) | PRE-AWARD_INGEST |
| 315 | `logician.failure_code.F-KFR-SIGNATURE-INVALID.v1` (superseded by F-KFR-CANONICAL-SIGNATURE-INVALID at row 339; both retained for migration audit) | §4 v2.x §3 (KFR residuals) | PRE-load + draft-time read |
| 316 | `logician.failure_code.F-KFR-AUDIT-CHAIN-BROKEN.v1` | §4 v2.x §3 (KFR residuals; combined module with row 315) | PRE-load + draft-time read |
| 317 | `logician.failure_code.F-LOGICIAN-FACT-TOLERANCE-DRIFT.v1` | §4 v2.x §3 (KFR residuals) | PRE-draft-read |
| 318 | `logician.failure_code.F-LOGICIAN-FACT-NEEDED-REQUIRED.v1` | §4 v2.x §3 (KFR residuals; HARD_BLOCK no M13) | PRE-SP0-sign-out |
| 319 | `logician.failure_code.F-BENCHMARK-CONTAINS-PER-ORG-REF.v1` (umbrella `.path` + `.value`) | §4 v2.x §3 (KFR residuals) | PRE-write + PRE-read |

**Slice 3 — F-CLASS-* dormant primitives (12 codes; rows 320-331; L-006 binding activates at this LOCK):**

| Row | primitive_id | defined_at | tier |
|---|---|---|---|
| 320 | `logician.failure_code.F-CLASS-REGISTER-MISSING.v1` | §4 v2.x §4 (F-CLASS-*; HARD_BLOCK no M13) | PRE-onboarding |
| 321 | `logician.failure_code.F-CLASS-REGISTER-UNSIGNED.v1` | §4 v2.x §4 (F-CLASS-*; HARD_BLOCK no M13) | PRE-onboarding |
| 322 | `logician.failure_code.F-CLASS-REGISTER-SIGNATURE-INVALID.v1` | §4 v2.x §4 (F-CLASS-*) | PRE-cycle |
| 323 | `logician.failure_code.F-CLASS-REGISTER-HASH-MISMATCH.v1` | §4 v2.x §4 (F-CLASS-*) | PRE-cycle |
| 324 | `logician.failure_code.F-CLASS-NEW-FACT-UNCLASSIFIED.v1` | §4 v2.x §4 (F-CLASS-*) | PRE-cycle |
| 325 | `logician.failure_code.F-CLASS-ROUTING-INDETERMINATE.v1` | §4 v2.x §4 (F-CLASS-*) | PRE-call |
| 326 | `logician.failure_code.F-CLASS-SLOT-ID-NON-OPAQUE.v1` | §4 v2.x §4 (F-CLASS-*; HARD_BLOCK structural; RT-12 closure adds re.ASCII flag) | PRE-call (outbound) |
| 327 | `logician.failure_code.F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.v1` | §4 v2.x §4 (F-CLASS-*) | POST-call (outbound) |
| 328 | `logician.failure_code.F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED.v1` | §4 v2.x §4 (F-CLASS-*) | POST-call (outbound) |
| 329 | `logician.failure_code.F-CLASS-HIGH-STAKES-FLAG-LEAK.v1` | §4 v2.x §4 (F-CLASS-*) | POST-call (outbound) |
| 330 | `logician.failure_code.F-CLASS-PER-GRANT-OVERRIDE-UNSIGNED.v1` | §4 v2.x §4 (F-CLASS-*) | PRE-per-grant |
| 331 | `logician.failure_code.F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID.v1` | §4 v2.x §4 (F-CLASS-*) | PRE update |

**Slice 3 META gate (the L-006 binding-activator; row 332):**

| Row | primitive_id | defined_at | tier |
|---|---|---|---|
| 332 | `logician.failure_code.F-CLASS-COVERAGE-INCOMPLETE.v1` | §4 v2.x §4.3.3 (META gate; L-006 dormant-binding ACTIVATES at this LOCK; HARD_BLOCK no M13) | META PRE-cycle |

**Slice 4 — v7.0.4-M1 corrective predicates (16 codes; rows 333-348; one renaming at row 339 supersedes row 315):**

| Row | primitive_id | defined_at | tier |
|---|---|---|---|
| 333 | `logician.failure_code.F-KFR-YAML-CONSTRUCT-FORBIDDEN.v1` | §4 v2.x §16 (M1 corrective; M1 §2.2.2) | PRE-load |
| 334 | `logician.failure_code.F-KFR-CANONICAL-SIGNATURE-INVALID.v1` (supersedes row 315 `F-KFR-SIGNATURE-INVALID` under canonicalization regime) | §4 v2.x §16 (M1 corrective; M1 §2.2.1) | PRE-load + draft-time read |
| 335 | `logician.failure_code.F-KFR-LEGACY-ACCEPT-RE-ENABLED-UNSIGNED.v1` | §4 v2.x §16 (M1 corrective; M1 §2.6; HARD_BLOCK no M13) | PRE-write |
| 336 | `logician.failure_code.F-KFR-PATH-SYMLINK-FORBIDDEN.v1` | §4 v2.x §16 (M1 corrective; M1 §4.2.2 atomic-read leg) | PRE-load |
| 337 | `logician.failure_code.F-KFR-TAG-MODIFIED.v1` | §4 v2.x §16 (M1 corrective; M1 §4) | PRE-write |
| 338 | `logician.failure_code.F-KFR-DUPLICATE-KEY.v1` | §4 v2.x §16 (M1 corrective; M1 §2.2.2) | PRE-load |
| 339 | `logician.failure_code.F-DERIVATION-AST-FORBIDDEN-NODE.v1` | §4 v2.x §16 (M1 corrective; M1 §3.2 + §3.3; HARD_BLOCK no M13) | PRE-eval |
| 340 | `logician.failure_code.F-DERIVATION-RUNTIME-ARITHMETIC-ERROR.v1` | §4 v2.x §16 (M1 corrective; DC-CF-01 fold-in) | POST-eval |
| 341 | `logician.failure_code.F-BENCHMARK-CROSS-CHECK-AUDIT-MISSING.v1` | §4 v2.x §16 (M1 corrective; M1 §5.2.2 DC-CF-04 closure) | PRE-compare |
| 342 | `logician.failure_code.F-BENCHMARK-SEEDING-SOURCE-UNAUTHORIZED.v1` (RT-10 closure: strict-key whitelist `_ALLOWED_ALLOWLIST_KEYS`) | §4 v2.x §16 (M1 corrective; M1 §5.2.3) | PRE-seed |
| 343 | `logician.failure_code.F-BENCHMARK-SEEDING-ALLOWLIST-SIGNATURE-INVALID.v1` (Ed25519 on canonical-JSON; RT-10 closure folded in) | §4 v2.x §16 (M1 corrective; M1 §5.2.3) | PRE-seed |
| 344 | `logician.failure_code.F-CURRENCY-FLOAT-IN-COMPARISON.v1` | §4 v2.x §16 (M1 corrective; DC-CF-02 Decimal mandate; HARD_BLOCK no M13) | PRE-runtime |
| 345 | `logician.failure_code.F-CURRENCY-CONTEXT-OMITTED.v1` (RT-04/RT-05/DC-01 Cycle 1 closure: dedicated test file) | §4 v2.x §16 (M1 corrective; HARD_BLOCK no M13) | PRE-runtime |
| 346 | `logician.failure_code.F-CURRENCY-CONTEXT-MISMATCH.v1` (RT-04/RT-05/DC-01 Cycle 1 closure: dedicated test file; identity-check on KFR_DECIMAL_CONTEXT) | §4 v2.x §16 (M1 corrective; HARD_BLOCK no M13) | PRE-runtime |
| 347 | `logician.failure_code.F-CURRENCY-DECIMAL-CONTEXT-DRIFT.v1` (RT-04/RT-05/DC-01 Cycle 1 closure: dedicated test file) | §4 v2.x §16 (M1 corrective; HARD_BLOCK no M13) | PRE-runtime |
| 348 | `logician.failure_code.F-CURRENCY-UNIT-MISMATCH.v1` | §4 v2.x §16 (M1 corrective; CF-RT-06 fold-in) | PRE-compare |

(Three further M1-family codes — `F-AWARD-INGEST-ATTN-UNVERIFIED`, `F-INTAKE-TELEMETRY-LEAK`, `F-INTAKE-LOGFIRE-STUB-MISSING` — are NOT separately registered as failure-code rows in this paired commit because they fold into the AWARD_INGEST mode + Intake bootstrap surface owned at v0.5 v10 (§11 Intake) row 256 + the §16 amendment text. They are present as on-disk module + test files per §4 v2.x §16.4 PRE-74/75/76 rows; the §0.5 paired commit defers their explicit failure-code-row registration to a follow-up §0.5 amendment when §11 Intake spins to v1.1.)

# Amendment §B — row delta + invariants

- Runtime-live total at §0.5 v13 LOCK = 304 rows.
- This amendment adds 44 rows (1 marker + 43 failure-code rows).
- New runtime-live total at compound LOCK = 348 rows.
- Vocabulary preservation: every row's `primitive_kind` resolves against the v5 + v6 16-value closed vocabulary (marker + failure-code).
- F-INDEX-STALE PRE-gate fires at commit time; all 44 new rows must be present in the index or the commit fails closed.

# Amendment §C — F-CLASS-COVERAGE-INCOMPLETE binding (L-006 activation)

Row 332 (`F-CLASS-COVERAGE-INCOMPLETE.v1`) carries the L-006 dormant-binding activation. At this LOCK ceremony, the META gate's `REQUIRED_F_CLASS_CODES` constant is satisfied: every one of the eleven non-COVERAGE F-CLASS-* codes (rows 320-331) has a live module + test on disk per §4 v2.x §16.6 audit trail. **F-CLASS-COVERAGE-INCOMPLETE PRE-cycle gate ACTIVATES** at this LOCK — Beta-deployment cycles thereafter run the META check at cycle start and refuse to proceed if any of the eleven F-CLASS-* codes loses its live module + test.

This is the **binding-activation event** that clears the v0.1 Beta architectural gate. v0.1 Beta deployment may now proceed (per CLAUDE.md "Beta-gate criterion: classification routing + KFR fact-substrate + Intake + Uploader + WS-L Logician realization").

# Amendment §D — supersession-pointer discipline

Row 315 (`F-KFR-SIGNATURE-INVALID.v1`) is **superseded** by row 334 (`F-KFR-CANONICAL-SIGNATURE-INVALID.v1`) under the canonicalization regime introduced by Slice 4 + v7.0.4-M1 §2.2.1. Both rows remain live in the Index for migration audit; consumers of the §0.5 Index that resolve the supersession pointer get directed from row 315 to row 334.

The combined module `f_kfr_signature_validation.py` (Slice 2) continues to serve `F-KFR-AUDIT-CHAIN-BROKEN` (row 316) per the §3 PRE-44 row in §4 v2.x. The Slice 4 `f_kfr_canonical_signature_invalid.py` is the v7.0.4-M1-pinned successor for the signature-invalid leg; the Slice 2 `f_kfr_signature_validation.py` continues to serve the audit-chain-broken leg per the v2.2 F-AMDT-08/09/10/11 sub-code-collapse precedent.
