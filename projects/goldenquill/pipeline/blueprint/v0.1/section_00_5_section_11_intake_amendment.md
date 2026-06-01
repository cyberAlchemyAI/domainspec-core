---
title: §0.5 Blueprint Interface Index — §11 Intake rows amendment (LOCKED 2026-05-10)
filed: 2026-05-10
operator: Josh
status: LOCKED 2026-05-10 — compound paired-commit with §11 v1 LOCK per §6.17 Option-B. L-005 strict two-cycle CLOSED with FULL cross-family rigor (audit trail at pipeline/validation/blueprint_section_11_intake_2026-05-10/{cycle_1_audit.md, audit_v1_synthesis.md, audit_v2_synthesis.md}).
parent_locks:
  - pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md                      # §0.5 v5 LOCKED 2026-04-19 — 101 master rows
  - pipeline/blueprint/v0.1/section_00_5_section_06_operating_envelope_amendment.md     # §0.5 v6 LOCKED 2026-04-21 — rows 102-117
  - pipeline/blueprint/v0.1/section_00_5_section_07_scribe_amendment.md                 # §0.5 v7 LOCKED 2026-04-21 — rows 118-158
  - pipeline/blueprint/v0.1/section_00_5_section_10_red_team_amendment.md               # §0.5 v8 LOCKED 2026-05-02 — rows 159-211
  - pipeline/blueprint/v0.1/section_11_intake.md                                        # §11 v1 LOCKED 2026-05-10
companion_blueprint_amendment: pipeline/blueprint/v0.1/section_11_intake.md  # paired-commit at §11 v1 LOCK per §6.17 Option-B
compound_lock_with: section_11_intake.md v1
parent_wins_discipline: each row's parent_lock_version + parent_lock_commit_hash point at §11 v1; resolves to actual commit hash at LOCK ceremony.
row_delta: prior runtime-live total at §0.5 v8 LOCK 2026-05-02 = 211 rows. §0.5 §12 amendment SCOPING DRAFT (filed 2026-05-09 — claims rows 212-232) is unfiled-LOCKED at §11 LOCK time. **§11 amendment claims rows 233-256 (24 rows)** to avoid collision; if §12 LOCKs after §11, §12's rows hold per its filed amendment. If §12 is withdrawn or renumbered, §11's claim is unaffected. Runtime-live total at this LOCK = 211 + 24 = 235 (§12 not yet LOCKed; if §12 LOCKs first, total = 211 + 21 + 24 = 256).
kind_of_amendment: row-append. NO vocabulary extension — every row's `primitive_kind` resolves against the v5 + v6 16-value closed vocabulary (marker / schema / interface-contract / failure-code / pre-gate-check / post-gate-check).
dependency_order: §11 v1 LOCK + this §0.5 amendment land as a single compound paired-commit at the same `lock_timestamp_utc`. §4 v2.x amendment (Code session per WS-L, registering F-EXTRACTOR-* + F-INTAKE-* family) is the third sibling in the same compound transaction.
f_index_stale_preflight: F-INDEX-STALE PRE-gate fires at commit time; all 24 new rows must be present in the index or the commit fails closed.
cross_family_posture: LIVE FULL CROSS-FAMILY (no Section E carve-out) per WS-D v7.0.5 LOCK precedent (lock_history row 179, 2026-05-10).
---

# Amendment intent

This amendment lands paired with §11 v1 LOCK per §6.17 Option-B compound-commit pattern. It registers §11-owned primitives (one section-anchor marker + five schema/contract rows + eleven exploded failure-code rows + seven consolidated pre/post-gate-check rows) into the Index. It does NOT reserve section anchors for §13 / §14 / §15 — each downstream blueprint claims its own §-number at its own v1 LOCK alongside its own §0.5 amendment file, matching the §6 / §7 / §10 / §12 per-section precedent.

The §10 amendment (§0.5 v8 LOCKED 2026-05-02 with rows 159–211 across 53 rows) is the load-bearing precedent for the explode-per-failure-code pattern. F-EXTRACTOR-* + F-INTAKE-* gate family at v1 contains 11 codes; this amendment registers one `failure-code` row per code (rows 239–249), then seven consolidated `pre-gate-check` / `post-gate-check` rows (rows 250–256) per the §4 v2.2 consolidated-check-callable pattern.

The master `section_00_5_interface_index_locked.md` remains LOCKED v5 on-disk; this amendment file is runtime-live at compound LOCK with §11. Future master re-author folds all v6 / v7 / v8 / §12 / this amendment files into the master.

# Amendment §A — row append (rows 233–256)

All rows enter §0.5 at `stability_tier = "STABLE"` at compound v1 LOCK (no PARENT_UNLOCKED transit since §11 LOCKs in the same compound transaction).

**Marker (row 233) — §11 section anchor:**

| Row | primitive_id | defined_at | parent_lock_version | parent_lock_commit_hash | kind | stability_tier |
|---|---|---|---|---|---|---|
| 233 | `blueprint.section_anchor.s11_intake.v1` | `pipeline/blueprint/v0.1/section_11_intake.md` | §11 v1 | `<resolved_at_commit>` | marker | STABLE |

**Schemas + interface-contract (rows 234–238) — §11 v1 canonical shapes:**

| Row | primitive_id | defined_at | kind | Parent |
|---|---|---|---|---|
| 234 | `intake.bulk_input.v1` | `pipeline/blueprint/v0.1/section_11_intake.md#§11.4.1` | schema | IntakeBulkInput frozen kw_only |
| 235 | `intake.incremental_input.v1` | `pipeline/blueprint/v0.1/section_11_intake.md#§11.4.2` | schema | IntakeIncrementalInput frozen kw_only |
| 236 | `intake.award_input.v1` | `pipeline/blueprint/v0.1/section_11_intake.md#§11.4.3` | schema | IntakeAwardInput frozen kw_only; content-hash binding per RT-05 closure |
| 237 | `intake.pending_facts_queue.v1` | `pipeline/blueprint/v0.1/section_11_intake.md#§11.5.1` | schema | pending_facts.v1 schema; substrate-aware anchors per RT-02/RT-03 closures (source_paragraph_id for DOCX, source_line_id for TXT/MD) |
| 238 | `intake.proposal_commitments.v1` | `pipeline/blueprint/v0.1/section_11_intake.md#§11.5.2` | schema | proposal_commitments.v1 with `status: PENDING_OPERATOR_REVIEW` flag; PROMOTED-only consumption by Report Generator (§14, v0.2) |

**Failure codes (rows 239–249) — explode pattern per §10 / §12 precedent; one row per F-EXTRACTOR-* / F-INTAKE-* code at v1:**

| Row | primitive_id | defined_at | kind | Parent / sub-tags |
|---|---|---|---|---|
| 239 | `intake.failure_code.F-EXTRACTOR-FABRICATION.v1` | `pipeline/blueprint/v0.1/section_11_intake.md#§11.9.1` | failure-code | PRE pre-queue. Sub-tags `.page_mismatch`, `.multiple_page_match`, `.docx_paragraph_mismatch`, `.line_mismatch`, `.markdown_multiline`, `.ocr_substitution`, `.ellipsis_substring`. Substrate-dispatched per §11.9.1.A/B/C/D. |
| 240 | `intake.failure_code.F-EXTRACTOR-AWARD-SIGNATURE-INVALID.proposal.v1` | `pipeline/blueprint/v0.1/section_11_intake.md#§11.9.2` | failure-code | PRE. Sub-tags `.absent`, `.signature_invalid`, `.retired_key`, `.hash_mismatch`, `.legacy_unhashed`. Content-hash binding per RT-05 closure. |
| 241 | `intake.failure_code.F-EXTRACTOR-AWARD-SIGNATURE-INVALID.award.v1` | `pipeline/blueprint/v0.1/section_11_intake.md#§11.9.3` | failure-code | PRE. Three-layer tamper-evident attestation bypass per RT-06 closure (interactive prompt + ledger-write-before-process + signed funder-keys). |
| 242 | `intake.failure_code.F-INTAKE-ORG-CROSS-REF.v1` | `pipeline/blueprint/v0.1/section_11_intake.md#§11.9.4` | failure-code | PRE. Sub-tags `.symlink_escape`, `.path_outside_inbox`, `.award_doc_outside_vault`, `.cross_grant`. |
| 243 | `intake.failure_code.F-INTAKE-INPUT-MISSING.v1` | `pipeline/blueprint/v0.1/section_11_intake.md#§11.9.5` | failure-code | PRE. Sub-tags `.inbox_dir_absent`, `.doc_absent`, `.submission_artifact_absent`, `.award_doc_absent`. |
| 244 | `intake.failure_code.F-INTAKE-UNSUPPORTED-FORMAT.v1` | `pipeline/blueprint/v0.1/section_11_intake.md#§11.9.6` | failure-code | PRE. Quarantine path on watcher-fired runs per RT-15 closure. |
| 245 | `intake.failure_code.F-INTAKE-QUEUE-INTEGRITY.v1` | `pipeline/blueprint/v0.1/section_11_intake.md#§11.9.7` | failure-code | POST + PRE-run-start. Sub-tags `.post_write_pydantic_fail`, `.post_write_count_mismatch`, `.state_corrupted`, `.cross_run_drift`. PRE-run-start check per RT-12 closure. |
| 246 | `intake.failure_code.F-INTAKE-EMBEDDING-NS-MISMATCH.v1` | `pipeline/blueprint/v0.1/section_11_intake.md#§11.9.8` | failure-code | PRE-tool-call (NEW per RT-09 + RT-10 closures). Sub-tags `.org_slug_mismatch`, `.grant_id_mismatch`, `.compound_key_collision`. |
| 247 | `intake.failure_code.F-INTAKE-CONFIG-SIGNATURE-INVALID.v1` | `pipeline/blueprint/v0.1/section_11_intake.md#§11.9.9` | failure-code | PRE (NEW per RT-07 closure). Sub-tags `.signature_absent`, `.signature_invalid`, `.retired_key`, `.canonical_bytes_mismatch`. |
| 248 | `intake.failure_code.F-INTAKE-EMBEDDING-ENDPOINT-INVALID.v1` | `pipeline/blueprint/v0.1/section_11_intake.md#§11.9.10` | failure-code | PRE-tool-call (NEW per RT-13 closure). Sealed Golden-Image-baked endpoint config; localhost-or-unix-socket allowlist. |
| 249 | `intake.failure_code.F-INTAKE-WATCHER-TOCTOU.v1` | `pipeline/blueprint/v0.1/section_11_intake.md#§11.9.11` | failure-code | PRE-file-open (NEW per RT-11 closure). `os.O_NOFOLLOW` + post-open re-resolve. Audit-trail subclass of F-INTAKE-ORG-CROSS-REF.symlink_escape. |

**PRE-gate-checks (rows 250–254) — consolidated per check callable per §4 v2.2 pattern:**

| Row | primitive_id | defined_at | kind | Parent / consolidated codes covered |
|---|---|---|---|---|
| 250 | `intake.pre_gate.path_isolation.v1` | `pipeline/blueprint/v0.1/section_11_intake.md#§11.9.4` | pre-gate-check | Consolidates F-INTAKE-ORG-CROSS-REF (all sub-tags) + F-INTAKE-INPUT-MISSING (all sub-tags) + F-INTAKE-UNSUPPORTED-FORMAT. Single path-validation pass at PRE-gate. |
| 251 | `intake.pre_gate.award_signature.v1` | `pipeline/blueprint/v0.1/section_11_intake.md#§11.9.2` | pre-gate-check | Consolidates F-EXTRACTOR-AWARD-SIGNATURE-INVALID.proposal (all sub-tags including `.hash_mismatch`) + .award (all branches including operator-attestation). Backs §11.9.2 + §11.9.3. |
| 252 | `intake.pre_gate.verbatim_match.v1` | `pipeline/blueprint/v0.1/section_11_intake.md#§11.9.1` | pre-gate-check | Backs F-EXTRACTOR-FABRICATION; substrate-dispatched per §11.9.1.A/B/C/D; runs PRE-pre-queue per candidate. |
| 253 | `intake.pre_gate.embedding_ns_match.v1` | `pipeline/blueprint/v0.1/section_11_intake.md#§11.9.8` | pre-gate-check | Backs F-INTAKE-EMBEDDING-NS-MISMATCH (NEW from RT-09 + RT-10 closures); PRE-tool-call wrapper on every Pydantic AI tool call against the local vector store. |
| 254 | `intake.pre_gate.config_signature.v1` | `pipeline/blueprint/v0.1/section_11_intake.md#§11.9.9` | pre-gate-check | Backs F-INTAKE-CONFIG-SIGNATURE-INVALID (NEW from RT-07 closure); runs at config read time before input bundle construction. |
| 255 | `intake.pre_gate.embedding_endpoint.v1` | `pipeline/blueprint/v0.1/section_11_intake.md#§11.9.10` | pre-gate-check | Backs F-INTAKE-EMBEDDING-ENDPOINT-INVALID (NEW from RT-13 closure); PRE-tool-call wrapper on every embedding tool invocation. |

**POST-gate-check / PRE-file-open (row 256) — consolidated:**

| Row | primitive_id | defined_at | kind | Parent / consolidated codes covered |
|---|---|---|---|---|
| 256 | `intake.post_gate.queue_integrity.v1` | `pipeline/blueprint/v0.1/section_11_intake.md#§11.9.7` | post-gate-check | Backs F-INTAKE-QUEUE-INTEGRITY (POST + PRE-run-start per RT-12 closure); checks Pydantic validity + count math + state-file sanity at run start AND at queue-write time. |

(Note: `intake.pre_gate.toctou_safe_open.v1` per RT-11 closure is in-scope but consolidated under `intake.pre_gate.path_isolation.v1` row 250 at v1 — single PRE-gate check callable owns both pre-resolve symlink rejection AND post-open re-resolve TOCTOU detection. Distinct failure-code row 249 preserved per audit-trail discipline. v1.x candidate: split if implementation cost demands.)

# Amendment §B — row description block (per-row narrative)

- **233** `blueprint.section_anchor.s11_intake.v1` (kind=marker) — §11 Intake section anchor. v0.1 always-local support agent. KFR ingestion + AWARD_INGEST extraction discipline. Three modes (BULK_INGEST / INCREMENTAL_INGEST / AWARD_INGEST). Marker per `marker` precedent in v1 closed vocabulary (§0.5.3.1).
- **234** `intake.bulk_input.v1` (kind=schema) — `IntakeBulkInput` frozen kw_only Pydantic model: run_id, org_slug, inbox_dir (Path.resolve-normalized; under orgs/<org_slug>/), confidence_autopromote_threshold (operator-tunable per-org via signed config OR per-run CLI), invoked_at_utc. Bundle invariants enforced PRE-gate by `intake.pre_gate.path_isolation.v1`.
- **235** `intake.incremental_input.v1` (kind=schema) — `IntakeIncrementalInput` frozen kw_only: run_id, org_slug, doc_path (under intake/inbox/), trigger Literal["watcher", "operator_explicit"], confidence_autopromote_threshold, invoked_at_utc. Watcher path subject to F-INTAKE-WATCHER-TOCTOU per RT-11 closure.
- **236** `intake.award_input.v1` (kind=schema) — `IntakeAwardInput` frozen kw_only: run_id, org_slug, grant_id, submission_artifact_ref (auto-resolved from --grant), award_doc_path (operator-supplied), award_doc_unsigned_attestation bool (default False; per-run flag with interactive TTY prompt requirement per RT-06 closure), invoked_at_utc. Mode flag is the SOLE driver of ±1 page tolerance carve-out per RT-04 closure.
- **237** `intake.pending_facts_queue.v1` (kind=schema) — `pending_facts.v1` per v7.0.4 §1 schema delta per §11.5.0: candidate_id (NEW), intake_run_id (NEW), extracted_at_utc (NEW), source_paragraph_id (NEW per RT-03), source_line_id (NEW per RT-02), source_format Literal["pdf","docx","txt","md"] (NEW), confidence_score (NEW), autopromote_batch (NEW), multiple_page_match (NEW per RT-01).
- **238** `intake.proposal_commitments.v1` (kind=schema) — `proposal_commitments.v1` per v7.0.4 §5.3 schema delta per §11.5.0: status Literal["PENDING_OPERATOR_REVIEW","PROMOTED"] (NEW), page_tolerance_applied (NEW per RT-01/RT-04). PROMOTED-only consumption by Report Generator (§14, v0.2).
- **239** `intake.failure_code.F-EXTRACTOR-FABRICATION.v1` (kind=failure-code) — PRE-pre-queue. Substrate-dispatched per §11.9.1.A (PDF unique-page-match per RT-01) / B (DOCX paragraph-index per RT-03) / C (TXT line-anchor) / D (Markdown single-line per RT-02). Mode-immutable from input dataclass per RT-04. Sub-tags per §11.9.1.
- **240** `intake.failure_code.F-EXTRACTOR-AWARD-SIGNATURE-INVALID.proposal.v1` (kind=failure-code) — PRE. SignedClaimEvidenceMap signature verification + key currency + content-hash binding (`submission_artifact_content_sha3_512` per RT-05 closure). Sub-tag `.legacy_unhashed` for backward-compat with pre-§11-v1-LOCK signed maps.
- **241** `intake.failure_code.F-EXTRACTOR-AWARD-SIGNATURE-INVALID.award.v1` (kind=failure-code) — PRE. Funder award document signature verification + three-layer tamper-evident operator-attestation bypass per RT-06 (interactive prompt, ledger-write-before-process, signed funder-keys file integrity).
- **242** `intake.failure_code.F-INTAKE-ORG-CROSS-REF.v1` (kind=failure-code) — PRE. Path-isolation discipline. Sub-tags per §11.9.4.
- **243** `intake.failure_code.F-INTAKE-INPUT-MISSING.v1` (kind=failure-code) — PRE. Required input file/directory existence. Sub-tags per §11.9.5.
- **244** `intake.failure_code.F-INTAKE-UNSUPPORTED-FORMAT.v1` (kind=failure-code) — PRE. Watcher quarantines unsupported files per RT-15 closure.
- **245** `intake.failure_code.F-INTAKE-QUEUE-INTEGRITY.v1` (kind=failure-code) — POST + PRE-run-start (per RT-12 closure). Sub-tags `.post_write_pydantic_fail`, `.post_write_count_mismatch`, `.state_corrupted`, `.cross_run_drift`.
- **246** `intake.failure_code.F-INTAKE-EMBEDDING-NS-MISMATCH.v1` (kind=failure-code; NEW) — PRE-tool-call. Per RT-09 + RT-10 closures. Pydantic AI tool wrapper asserts org_slug arg matches input dataclass; compound-key embedding storage path collision-detect.
- **247** `intake.failure_code.F-INTAKE-CONFIG-SIGNATURE-INVALID.v1` (kind=failure-code; NEW) — PRE. Per RT-07 closure. `intake_config.yaml` Ed25519 signature verification at config read time.
- **248** `intake.failure_code.F-INTAKE-EMBEDDING-ENDPOINT-INVALID.v1` (kind=failure-code; NEW) — PRE-tool-call. Per RT-13 closure. Sealed Golden-Image-baked endpoint config; localhost-or-unix-socket allowlist.
- **249** `intake.failure_code.F-INTAKE-WATCHER-TOCTOU.v1` (kind=failure-code; NEW) — PRE-file-open. Per RT-11 closure. `os.O_NOFOLLOW` + post-open Path.resolve() re-validation. Audit-trail subclass of F-INTAKE-ORG-CROSS-REF.symlink_escape preserved per §10 explode-pattern.
- **250** `intake.pre_gate.path_isolation.v1` (kind=pre-gate-check) — Single check callable consolidating F-INTAKE-ORG-CROSS-REF (all sub-tags including `.symlink_escape` + TOCTOU re-resolve) + F-INTAKE-INPUT-MISSING (all sub-tags) + F-INTAKE-UNSUPPORTED-FORMAT. Per §4 v2.2 consolidated-check pattern.
- **251** `intake.pre_gate.award_signature.v1` (kind=pre-gate-check) — Consolidates F-EXTRACTOR-AWARD-SIGNATURE-INVALID.proposal (all sub-tags including `.hash_mismatch` per RT-05) + .award (all branches including three-layer attestation bypass per RT-06).
- **252** `intake.pre_gate.verbatim_match.v1` (kind=pre-gate-check) — Backs F-EXTRACTOR-FABRICATION; substrate-dispatched per §11.9.1.A/B/C/D; runs PRE-pre-queue per candidate. Mode flag immutable from input dataclass per RT-04.
- **253** `intake.pre_gate.embedding_ns_match.v1` (kind=pre-gate-check; NEW) — Backs F-INTAKE-EMBEDDING-NS-MISMATCH; PRE-tool-call wrapper on every Pydantic AI tool call against local vector store; org_slug + grant_id arg validation per RT-09; compound-key collision-detect per RT-10.
- **254** `intake.pre_gate.config_signature.v1` (kind=pre-gate-check; NEW) — Backs F-INTAKE-CONFIG-SIGNATURE-INVALID; runs at `intake_config.yaml` read time before input bundle construction; Ed25519 signature verification + key currency check + canonical-bytes match.
- **255** `intake.pre_gate.embedding_endpoint.v1` (kind=pre-gate-check; NEW) — Backs F-INTAKE-EMBEDDING-ENDPOINT-INVALID; PRE-tool-call wrapper on every embedding tool invocation; sealed Golden-Image-baked endpoint config; localhost-or-unix-socket allowlist.
- **256** `intake.post_gate.queue_integrity.v1` (kind=post-gate-check) — Backs F-INTAKE-QUEUE-INTEGRITY; runs at queue-write time (POST) AND at every Intake invocation start (PRE-run-start per RT-12 closure); Pydantic validity + count math + state-file sanity reconciliation.

# Amendment §C — Vocabulary preservation

Every row in this amendment uses one of the 16-value closed `primitive_kind` vocabulary established at §0.5 v5 LOCK + extended at §0.5 v6 LOCK (`procedure`):

- `marker` (row 233) — already in the v1 closed vocabulary (§0.5.3.1).
- `schema` (rows 234, 235, 236, 237, 238).
- `failure-code` (rows 239–249).
- `pre-gate-check` (rows 250–255).
- `post-gate-check` (row 256).

**No vocabulary extension.** Every primitive_kind in this amendment resolves against the v5 + v6 closed set. F-INDEX-STALE precondition for vocabulary extension does NOT apply.

# Amendment §D — Stability tier

All 24 rows enter §0.5 at `stability_tier = "STABLE"` at compound v1 LOCK. No PARENT_UNLOCKED transit.

# Amendment §E — Row-count reconciliation (against runtime-live total)

| Surface | Rows |
|---|---|
| §0.5 v5 master LOCKED 2026-04-19 | 1–101 (101 rows) |
| §0.5 §6 operating-envelope amendment LOCKED 2026-04-21 | 102–117 (16 rows) |
| §0.5 §7 scribe amendment LOCKED 2026-04-21 | 118–158 (41 rows) |
| §0.5 §10 amendment LOCKED 2026-05-02 | 159–211 (53 rows) |
| §0.5 §12 amendment SCOPING DRAFT (claim 212–232; 21 rows) | RESERVED — not yet LOCKED |
| **§0.5 §11 amendment (this file)** | **233–256 (24 rows: 1 marker + 5 schema + 11 failure-code + 6 pre-gate-check + 1 post-gate-check)** |
| **Total runtime-live row count at this compound LOCK** | **235** (211 + 24; §12 not yet LOCKed; if §12 LOCKs first, total becomes 256) |

# Amendment §F — Companion JSON

`pipeline/blueprint/v0.1/section_00_5_section_11_intake.json` — canonical-JSON encoding of this amendment's 24 rows. Sorted keys (`sort_keys=True`), UTF-8, LF, no trailing whitespace, no BOM, `ensure_ascii=False`, key separator `": "`, item separator `", "`. JSON companion's `index_version` field is `v9` (next runtime-live version after §0.5 v8 LOCKED 2026-05-02 + §12 v9 reserved). Filename matches the per-section amendment-file pattern.

# Amendment §G — Paired-commit reminder

This §0.5 §11 amendment commits atomically with §11 v1 LOCK + §4 v2.x amendment LOCK (compound paired-commit per §6.17 Option-B; three-sibling transaction). F-INDEX-STALE PRE-gate fails-closed if any of the 24 rows are not in the index at the moment of compound commit.

# Amendment §H — Non-goals

- Does NOT modify any v5 master row.
- Does NOT modify any v6 / v7 / v8 amendment row.
- Does NOT modify §12 amendment rows (212–232) which remain reserved.
- Does NOT modify F-INDEX-STALE semantics.
- Does NOT reserve §13 / §14 / §15 section anchors — each downstream blueprint claims its own at its own v1 LOCK.
- Does NOT extend the closed `primitive_kind` vocabulary.
- Does NOT modify `section_00_5_interface_index_locked.md` on disk — master re-author is a separate ceremony.

# Amendment §I — L-005 audit record

**Status: LOCKED 2026-05-10** — L-005 strict two-cycle CLOSED with FULL cross-family rigor. Audit trail at:
- Cycle 1: `pipeline/validation/blueprint_section_11_intake_2026-05-10/audit_v1_{editor,judge,red_team}.md` + `audit_v1_synthesis.md`
- Cycle 2: `pipeline/validation/blueprint_section_11_intake_2026-05-10/audit_v2_{editor,judge,red_team}.md` + `audit_v2_synthesis.md`

Cycle 2 verdicts: Editor READY_TO_LOCK + Judge READY_TO_LOCK 100/100 + Red Team PASS blocking:false.

# End of amendment
