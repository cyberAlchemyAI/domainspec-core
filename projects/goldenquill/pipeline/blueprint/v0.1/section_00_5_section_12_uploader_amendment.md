---
title: §0.5 Blueprint Interface Index — §12 Uploader rows amendment (LOCKED 2026-05-10)
filed: 2026-05-09
locked: 2026-05-10
operator: Josh
status: LOCKED 2026-05-10 — L-005 strict two-cycle PASS per `pipeline/validation/v12_v1_thesis_2026-05-09/audit_v2_synthesis.md` with FULL live cross-family rigor. All 21 rows (212–232) promoted PARENT_UNLOCKED → STABLE atomically with the compound LOCK of §12 v1 + §4 v2.7. Companion-file pattern matches §0.5 §6 / §0.5 §7 / §0.5 §10 amendments. Runtime-live row count at LOCK: 232.
parent_locks:
  - pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md                      # §0.5 v5 LOCKED 2026-04-19 — 101 master rows
  - pipeline/blueprint/v0.1/section_00_5_section_06_operating_envelope_amendment.md     # §0.5 v6 LOCKED 2026-04-21 — rows 102-117 + `procedure` kind extension
  - pipeline/blueprint/v0.1/section_00_5_section_07_scribe_amendment.md                 # §0.5 v7 LOCKED 2026-04-21 — rows 118-158
  - pipeline/blueprint/v0.1/section_00_5_section_10_red_team_amendment.md               # §0.5 v8 LOCKED 2026-05-02 — rows 159-211 (compound with §10 v1.1 + §5 v7 amendment)
  - pipeline/blueprint/v0.1/section_12_uploader.md                                      # §12 v1.1 SCOPING DRAFT 2026-05-09 — primitives enumerated in §12.15
companion_blueprint_amendment: pipeline/blueprint/v0.1/section_12_uploader.md  # paired-commit at §12 v1 LOCK per §6.17 Option-B
compound_lock_with: section_12_uploader.md v1
parent_wins_discipline: each row's parent_lock_version + parent_lock_commit_hash point at §12 v1; carries `TO_BE_PINNED_AT_COMMIT` until §12 v1 LOCK ceremony resolves the parent-file SHA-3-512 hash.
row_delta: prior runtime-live total at §0.5 v8 LOCK 2026-05-02 = 211 rows. This amendment adds 21 rows (rows 212–232). Runtime-live total at compound LOCK = 232.
kind_of_amendment: row-append. NO vocabulary extension — every row's `primitive_kind` resolves against the v5 + v6 16-value closed vocabulary.
dependency_order: §12 v1 SCOPING DRAFT + this §0.5 amendment land as a single compound paired-commit at the same `lock_timestamp_utc`. §4 v2.7 amendment (Code session, registering F-UPLOADER-* family + R-UPLOADER-NO-SUBMIT AST-lint rule) is the third sibling in the same compound transaction.
f_index_stale_preflight: F-INDEX-STALE PRE-gate fires at commit time; all 21 new rows must be present in the index or the commit fails closed.
prefix_pass_changelog_2026_05_09:
  - "File RENAMED from section_00_5_v6_amendment.md to section_00_5_section_12_uploader_amendment.md to eliminate name collision with the existing section_00_5_section_06_operating_envelope_amendment.md (§0.5 v6 LOCKED 2026-04-21) and to match the per-section amendment-file pattern (§6 / §7 / §10). JSON companion renamed section_00_5_interface_index.v6.json to section_00_5_section_12_uploader.json."
  - "Section-anchor reservations for §11 / §13 / §14 / §15 DROPPED. Each blueprint claims its own §-number at its own v1 LOCK per §6 / §7 / §10 precedent. This amendment is §12-only."
  - "New vocabulary kinds section_anchor and gate-family DROPPED. §12 anchor row re-cast as kind=marker per the v1 closed vocabulary (precedent: sovereignty.marker.parent_unlocked at §0.5 v1/v2 / §1 placeholder discipline). F-UPLOADER-* family exploded to per-code rows per §10 amendment style — one failure-code row per gate, one pre-gate-check / post-gate-check row per check callable. Both vocabulary OQs (OQ-v6-VOCAB-1 + OQ-v6-VOCAB-2) resolved by the rescope."
  - "Row count math recomputed against runtime-live 211 (not 101). §E reconciliation table corrected."
  - "§A Vocabulary Extension block removed (no longer extending vocabulary)."
  - "§C Open Questions entries about gate-family fold/explode and section_anchor removed."
  - "Row count: 21 (NOT 32 as the originating dispatch brief proposed). Brief's 32-row math (1 marker + 5 schema/contract + 13 failure-code + 13 pre/post-gate-check) assumed §12 HIGH-2 path-a (compound-LOCK §12 v1 with §2 v7.2 attachments sub-kind). Brief itself RECOMMENDED path-b (defer attachments to v1.1) for clean LOCK now. §12 v1.1 SCOPING DRAFT chose path-b. Path-b consequence cascade: no AttachmentRef schema at v1 (-1 schema), no F-UPLOADER-ATTACHMENT-MISSING / -TAMPERED / -ADMIN-RISK-UNFLAGGED at v1 (-3 failure-codes, -3 corresponding gate-checks; ADMIN-RISK gate is attachment-text-scoped per §7.11 scanner contract and naturally moves to v1.1 with attachments), pre/post-gate-check consolidation per §4 v2.2 pattern (-4 vs the brief's per-code 1:1 pre/post-check expansion). Final inventory: 1 marker + 4 schema/contract + 10 failure-code + 3 PRE-gate-check + 3 POST-gate-check = 21 rows. Runtime-live total: 211 + 21 = 232. The path-b row reduction is documented at §H Non-goals + §12.6 (attachment deferral rationale) + §12.2 Law 4 v1.1 horizon note (preserves the §7 v1.1.1 silent-delegation lesson)."
---

# Amendment intent

This amendment lands paired with §12 v1 LOCK per §6.17 Option-B compound-commit pattern. It registers §12-owned primitives (one section-anchor marker + four schema/contract rows + ten exploded failure-code rows + six consolidated pre/post-gate-check rows) into the Index. It does NOT reserve section anchors for §11 / §13 / §14 / §15 — each downstream blueprint claims its own §-number at its own v1 LOCK alongside its own §0.5 amendment file, matching the §6 / §7 / §10 per-section precedent. There is no "v0.2 wave anchor reservation" surface in this amendment.

The §10 amendment (§0.5 v8 LOCKED 2026-05-02 with rows 159–211 across 53 rows) is the load-bearing precedent for the explode-per-failure-code pattern. F-UPLOADER-* gate family at v1 contains 10 codes; this amendment registers one `failure-code` row per code (rows 217–226), then six consolidated `pre-gate-check` / `post-gate-check` rows (rows 227–232) per the §4 v2.2 consolidated-check-callable pattern.

The master `section_00_5_interface_index_locked.md` remains LOCKED v5 on-disk; this amendment file is runtime-live at compound LOCK with §12. Future master re-author folds all v6 / v7 / v8 / this amendment files into the master.

# Amendment §A — row append (rows 212–232)

All rows enter §0.5 at `stability_tier = "PARENT_UNLOCKED"` while §12 is SCOPING DRAFT. At compound v1 LOCK, all rows promote to `stability_tier = "STABLE"` via the parent-backfill discipline §0.5 v6 / v7 / v8 used.

**Marker (row 212) — §12 section anchor:**

| Row | primitive_id | defined_at | parent_lock_version | parent_lock_commit_hash | kind | stability_tier |
|---|---|---|---|---|---|---|
| 212 | `blueprint.section_anchor.s12_uploader.v1` | `pipeline/blueprint/v0.1/section_12_uploader.md` | §12 v1 | TO_BE_PINNED_AT_COMMIT | marker | PARENT_UNLOCKED |

**Schemas + interface-contract (rows 213–216) — §12 v1 canonical shapes:**

| Row | primitive_id | defined_at | kind | Parent |
|---|---|---|---|---|
| 213 | `uploader.input.v1` | `pipeline/blueprint/v0.1/section_12_uploader.md#§12.4` | schema | UploaderInput frozen kw_only |
| 214 | `uploader.output.v1` | `pipeline/blueprint/v0.1/section_12_uploader.md#§12.5` | schema | UploaderOutput; `submitted: bool` hardcoded False per §12.9.3 runtime invariant |
| 215 | `uploader.portal_adapter_protocol.v1` | `pipeline/blueprint/v0.1/section_12_uploader.md#§12.10` | interface-contract | Protocol-DI; four v1 implementations: grants_gov, sam_gov, common_grant_app, copy_paste |
| 216 | `uploader.readiness_checklist.v1` | `pipeline/blueprint/v0.1/section_12_uploader.md#§12.7` | schema | ReadinessChecklist + ChecklistItem; 10 items at v1 |

(Note: `uploader.attachment_ref.v1` is intentionally absent at v1 — attachments deferred to v1.1 per §12 §12.6 + §12 §OQ-12.4. Re-introduces at §12 v1.1 amendment.)

**Failure codes (rows 217–226) — explode pattern per §10 precedent; one row per F-UPLOADER-* code at v1:**

| Row | primitive_id | defined_at | kind | Parent |
|---|---|---|---|---|
| 217 | `uploader.failure_code.F-UPLOADER-PACKAGE-INCOMPLETE.v1` | `pipeline/blueprint/v0.1/section_12_uploader.md#§12.9.1` | failure-code | §12.9 POST |
| 218 | `uploader.failure_code.F-UPLOADER-FORMAT-MISMATCH.v1` | `pipeline/blueprint/v0.1/section_12_uploader.md#§12.9.2` | failure-code | §12.9 POST (sub-tags `.format`, `.page_limit`, `.file_size`) |
| 219 | `uploader.failure_code.F-UPLOADER-AUTOSUBMIT-ATTEMPTED.v1` | `pipeline/blueprint/v0.1/section_12_uploader.md#§12.9.3` | failure-code | §12.9 PRE structural; no M13 bypass |
| 220 | `uploader.failure_code.F-UPLOADER-SIGNATURE-MISSING.v1` | `pipeline/blueprint/v0.1/section_12_uploader.md#§12.9.4` | failure-code | §12.9 PRE (sub-tags `.absent`, `.hash_mismatch`) |
| 221 | `uploader.failure_code.F-UPLOADER-CONTENT-MUTATION.v1` | `pipeline/blueprint/v0.1/section_12_uploader.md#§12.9.5` | failure-code | §12.9 POST under §12.8 tolerance model |
| 222 | `uploader.failure_code.F-UPLOADER-INPUT-INCONSISTENT.v1` | `pipeline/blueprint/v0.1/section_12_uploader.md#§12.9.5` | failure-code | §12.9 PRE |
| 223 | `uploader.failure_code.F-UPLOADER-RFA-MISSING.v1` | `pipeline/blueprint/v0.1/section_12_uploader.md#§12.9.5` | failure-code | §12.9 PRE |
| 224 | `uploader.failure_code.F-UPLOADER-SIGNATURE-MISMATCH.v1` | `pipeline/blueprint/v0.1/section_12_uploader.md#§12.9.5` | failure-code | §12.9 PRE; audit-trail subclass of SIGNATURE-MISSING.hash_mismatch |
| 225 | `uploader.failure_code.F-UPLOADER-ORG-CROSS-REF.v1` | `pipeline/blueprint/v0.1/section_12_uploader.md#§12.9.5` | failure-code | §12.9 PRE (sub-tags `.multi_org_path`, `.symlink_escape`) |
| 226 | `uploader.failure_code.F-UPLOADER-FIELD-MAP-CLOUD-ROUTED.v1` | `pipeline/blueprint/v0.1/section_12_uploader.md#§12.9.6` | failure-code | §12.9 PRE; HIGH-5 fix; routing-posture defense |

**PRE-gate-checks (rows 227–229) — consolidated per check callable per §4 v2.2 pattern:**

| Row | primitive_id | defined_at | kind | Parent / consolidated codes covered |
|---|---|---|---|---|
| 227 | `uploader.pre_gate.input_invariants.v1` | `pipeline/blueprint/v0.1/section_12_uploader.md#§12.4` | pre-gate-check | Consolidates RFA-MISSING, SIGNATURE-MISSING (both sub-tags), SIGNATURE-MISMATCH (subclass), INPUT-INCONSISTENT, ORG-CROSS-REF (both sub-tags). Single bundle-validation pass. |
| 228 | `uploader.pre_gate.autosubmit_structural.v1` | `pipeline/blueprint/v0.1/section_12_uploader.md#§12.9.3` | pre-gate-check | AST-lint allow-list (Layer 1) + namespace-egress capability check (Layer 2) + runtime invariant (Layer 3). Backs F-UPLOADER-AUTOSUBMIT-ATTEMPTED. |
| 229 | `uploader.pre_gate.field_map_routing.v1` | `pipeline/blueprint/v0.1/section_12_uploader.md#§12.9.6` | pre-gate-check | Per portal-field-disambiguation call site; backs F-UPLOADER-FIELD-MAP-CLOUD-ROUTED. Input shape: `FieldMapCallContext` (frozen kw_only dataclass with portal_field_id / portal_field_label / caller_module / `routed_to: Literal["local","cloud"]` / model_id / classification_at_call) — defined inline in §12.9.6; covered by this row per consolidation pattern (no separate `field_map_call_context` schema row). |

**POST-gate-checks (rows 230–232) — consolidated per check callable:**

| Row | primitive_id | defined_at | kind | Parent / consolidated codes covered |
|---|---|---|---|---|
| 230 | `uploader.post_gate.package_completeness.v1` | `pipeline/blueprint/v0.1/section_12_uploader.md#§12.9.1` | post-gate-check | Backs F-UPLOADER-PACKAGE-INCOMPLETE; walks `RfaExtractedRecord.section_structure` against `submission_manifest.yaml`. |
| 231 | `uploader.post_gate.format_compliance.v1` | `pipeline/blueprint/v0.1/section_12_uploader.md#§12.9.2` | post-gate-check | Backs F-UPLOADER-FORMAT-MISMATCH; checks format / page_limit / file_size per portal adapter. |
| 232 | `uploader.post_gate.content_mutation.v1` | `pipeline/blueprint/v0.1/section_12_uploader.md#§12.9.5` | post-gate-check | Backs F-UPLOADER-CONTENT-MUTATION; deterministic text-extraction diff under §12.8 tolerance model. |

# Amendment §B — row description block (per-row narrative)

- **212** `blueprint.section_anchor.s12_uploader.v1` (kind=marker) — §12 Uploader section anchor. v0.1 always-local support agent. Prepare-and-stage discipline only (operator clicks final submit). Marker per `marker` precedent in v1 closed vocabulary (§0.5.3.1).
- **213** `uploader.input.v1` (kind=schema) — `UploaderInput` frozen kw_only Pydantic model: run_id, grant_id, org_slug, submission_bundle_ref (Path.resolve-normalized), section_drafts tuple, claim_evidence_map tuple, RfaExtractedRecord, OperatorSignature, target_portal Literal (4-value at v1: grants_gov | sam_gov | common_grant_app | copy_paste), optional PortalConfig, prepared_at_utc. Reads submission bundle bytes via §2 `submission-bundle-read` Vault read intent. Note: `attachments: tuple[AttachmentRef, ...]` field NOT present at v1 per §12.6 deferral.
- **214** `uploader.output.v1` (kind=schema) — `UploaderOutput` covering submission_manifest.yaml, portal-format documents, portal_fields.yaml, readiness_checklist.yaml. Includes `submitted: bool` field hardcoded False per §12.9.3 runtime invariant; `python -O`-resistant (RuntimeError, not assert). State persisted separately at `orgs/<slug>/vault/grants/<grant_id>/uploader_state/<run_id>.yaml` (NOT inside submission_package/).
- **215** `uploader.portal_adapter_protocol.v1` (kind=interface-contract) — `PortalAdapterProtocol` Protocol-DI: seven methods (portal_id, required_format, page_limit, file_size_limit, filename_convention, map_fields, assemble_package). Four v1 implementations satisfy the protocol: grants_gov, sam_gov, common_grant_app, copy_paste. Foundant / Submittable / Fluxx adapters deferred to v0.1.x per §12 §OQ-12.6.
- **216** `uploader.readiness_checklist.v1` (kind=schema) — `ReadinessChecklist` overall_status Literal["ready","not_ready"], items tuple of ChecklistItem (10 deterministic checks at v1: section_completeness, manual_attach_to_do, format_compliance, page_count_compliance, file_size_compliance, filename_convention_compliance, manifest_integrity, operator_signature_present, portal_field_completeness, content_integrity), fail/warn/pass counts, checked_at_utc.
- **217** `uploader.failure_code.F-UPLOADER-PACKAGE-INCOMPLETE.v1` (kind=failure-code) — POST-gate. Trigger: any RFA-required narrative section missing from submission_manifest.yaml. Hard-block.
- **218** `uploader.failure_code.F-UPLOADER-FORMAT-MISMATCH.v1` (kind=failure-code) — POST-gate. Sub-tags `.format` / `.page_limit` / `.file_size`. Hard-block.
- **219** `uploader.failure_code.F-UPLOADER-AUTOSUBMIT-ATTEMPTED.v1` (kind=failure-code) — PRE-gate, structural. Three-layer defense (AST-lint allow-list + network-namespace process isolation + RuntimeError invariant). No M13 bypass — architecturally prohibited per v7.0.6.
- **220** `uploader.failure_code.F-UPLOADER-SIGNATURE-MISSING.v1` (kind=failure-code) — PRE-gate. Sub-tags `.absent` (no signature) / `.hash_mismatch` (bundle modified after signature). Hard-block.
- **221** `uploader.failure_code.F-UPLOADER-CONTENT-MUTATION.v1` (kind=failure-code) — POST-gate. Text-extraction diff exceeds §12.8 tolerance model. Hard-block.
- **222** `uploader.failure_code.F-UPLOADER-INPUT-INCONSISTENT.v1` (kind=failure-code) — PRE-gate. claim_evidence_map not the union of section_drafts[*].claim_evidence_map. Hard-block.
- **223** `uploader.failure_code.F-UPLOADER-RFA-MISSING.v1` (kind=failure-code) — PRE-gate. RfaExtractedRecord absent or hash mismatch against session manifest pin. Hard-block.
- **224** `uploader.failure_code.F-UPLOADER-SIGNATURE-MISMATCH.v1` (kind=failure-code) — PRE-gate. Audit-trail subclass of SIGNATURE-MISSING.hash_mismatch — both codes resolve via the same predicate at the check level; preserved as distinct row for audit-trail clarity per §10 explode-pattern precedent.
- **225** `uploader.failure_code.F-UPLOADER-ORG-CROSS-REF.v1` (kind=failure-code) — PRE-gate. Sub-tags `.multi_org_path` (input bundle references >1 org slug) / `.symlink_escape` (Path.resolve outside declared org_slug subtree). Hard-block.
- **226** `uploader.failure_code.F-UPLOADER-FIELD-MAP-CLOUD-ROUTED.v1` (kind=failure-code) — PRE-gate. Portal-field disambiguation LLM call routed to cloud rather than local. Hard-block. HIGH-5 fix backs the §12.11 routing-posture defense.
- **227** `uploader.pre_gate.input_invariants.v1` (kind=pre-gate-check) — Single bundle-validation check callable consolidating RFA-MISSING, SIGNATURE-MISSING (both sub-tags), SIGNATURE-MISMATCH (subclass), INPUT-INCONSISTENT, ORG-CROSS-REF (both sub-tags). Per §4 v2.2 consolidated-check pattern.
- **228** `uploader.pre_gate.autosubmit_structural.v1` (kind=pre-gate-check) — Three-layer defense check callable: Layer 1 AST-lint allow-list (R-UPLOADER-NO-SUBMIT registered at `pipeline/linting/ast_lint.py`), Layer 2 namespace-egress capability check, Layer 3 RuntimeError invariant in __post_init__ + vault-write-time re-check.
- **229** `uploader.pre_gate.field_map_routing.v1` (kind=pre-gate-check) — Per-call-site routing check on portal-field disambiguation calls; backs F-UPLOADER-FIELD-MAP-CLOUD-ROUTED. Input shape: `FieldMapCallContext` (frozen kw_only dataclass with `portal_field_id`, `portal_field_label`, `caller_module`, `routed_to: Literal["local","cloud"]`, `model_id`, `classification_at_call: Literal["public","shareable","confidential"]`) — defined inline in §12.9.6; the consolidation pattern absorbs the schema into this gate-check row rather than carrying a separate `uploader.field_map_call_context` schema row, matching the precedent for ChecklistItem / ManifestEntry / PortalField sub-shapes covered by their parent schema rows. Wiring discipline: every adapter `map_fields()` LLM call site invokes the gate predicate via a Pydantic AI `before_model_request` hook (no field-map call site can land without the hook).
- **230** `uploader.post_gate.package_completeness.v1` (kind=post-gate-check) — Walks RfaExtractedRecord.section_structure against submission_manifest.yaml; backs F-UPLOADER-PACKAGE-INCOMPLETE.
- **231** `uploader.post_gate.format_compliance.v1` (kind=post-gate-check) — Iterates manifest entries × portal-adapter required_format / page_limit / file_size_limit; backs F-UPLOADER-FORMAT-MISMATCH (all three sub-tags).
- **232** `uploader.post_gate.content_mutation.v1` (kind=post-gate-check) — Deterministic text-extraction diff between input SectionDraft.body_text and output document text under §12.8 tolerance model (whitespace normalization, page-break un-pagination, table structural-hash); backs F-UPLOADER-CONTENT-MUTATION.

# Amendment §C — Vocabulary preservation

Every row in this amendment uses one of the 16-value closed `primitive_kind` vocabulary established at §0.5 v5 LOCK + extended at §0.5 v6 LOCK (`procedure`):

- `marker` (row 212) — already in the v1 closed vocabulary (§0.5.3.1).
- `schema` (rows 213, 214, 216).
- `interface-contract` (row 215).
- `failure-code` (rows 217–226).
- `pre-gate-check` (rows 227–229).
- `post-gate-check` (rows 230–232).

**No vocabulary extension.** Every primitive_kind in this amendment resolves against the v5 + v6 closed set. F-INDEX-STALE precondition for vocabulary extension does NOT apply.

# Amendment §D — Stability tier

All 21 rows enter §0.5 at `stability_tier = "PARENT_UNLOCKED"` while §12 is SCOPING DRAFT. At compound v1 LOCK (post Thesis Round 1+2), all 21 rows promote to `stability_tier = "STABLE"` via the same parent-backfill discipline §0.5 v6 / v7 / v8 used.

# Amendment §E — Row-count reconciliation (against runtime-live total)

| Surface | Rows |
|---|---|
| §0.5 v5 master LOCKED 2026-04-19 | 1–101 (101 rows) |
| §0.5 §6 operating-envelope amendment LOCKED 2026-04-21 | 102–117 (16 rows) |
| §0.5 §7 scribe amendment LOCKED 2026-04-21 | 118–158 (41 rows) |
| §0.5 §10 amendment LOCKED 2026-05-02 (compound with §10 v1.1 + §5 v7 amendment) | 159–211 (53 rows) |
| **§0.5 §12 amendment (this file)** | **212–232 (21 rows: 1 marker + 4 schema/contract + 10 failure-code + 6 pre/post-gate-check)** |
| **Total runtime-live row count at this compound LOCK** | **232** |

The F-INDEX-STALE PRE-gate checks runtime-live row count (master + all amendment files) at commit time. The runtime-live total at this commit MUST be 232 or the commit fails closed.

**Frame note.** "211 + 21 = 232" is the runtime-live arithmetic (master + all four prior amendment files + this amendment). The earlier "v5 master + this amendment = 122" frame was a separate accounting (delta-against-master only) used in the prior draft of this file; runtime-live is the load-bearing frame for F-INDEX-STALE and is the only frame surfaced here.

# Amendment §F — Companion JSON

`pipeline/blueprint/v0.1/section_00_5_section_12_uploader.json` — canonical-JSON encoding of this amendment's 21 rows. Sorted keys (`sort_keys=True`), UTF-8, LF, no trailing whitespace, no BOM, `ensure_ascii=False`, key separator `": "`, item separator `", "`. JSON companion's `index_version` field is `v9` (next runtime-live version after §0.5 v8 LOCKED 2026-05-02). Filename matches the amendment-file's per-section pattern (no `vN.json` collision risk).

The JSON does NOT enumerate the master 101 rows + 110 prior-amendment rows — those carry their own JSON companions per the per-amendment companion pattern. At the eventual master re-author, all amendment JSONs fold into a single canonical `section_00_5_interface_index.v9.json` (or whatever the next master master version is).

**JSON build.** Authored via canonical-JSON Python: `json.dumps(payload, sort_keys=True, ensure_ascii=False, indent=2, separators=(",", ": "))` then write with LF line endings + trailing newline. Re-load + re-dump check verifies byte-identical-signable. No `index_content_hash` field at SCOPING DRAFT time — that field populates at LOCK ceremony when the parent_lock_commit_hash sentinels resolve to actual hashes.

# Amendment §G — Paired-commit reminder

This §0.5 §12 amendment commits atomically with §12 v1 LOCK + §4 v2.7 amendment LOCK (compound paired-commit per §6.17 Option-B; three-sibling transaction). F-INDEX-STALE PRE-gate fails-closed if any of the 21 rows are not in the index at the moment of compound commit.

# Amendment §H — Non-goals

- Does NOT modify any v5 master row.
- Does NOT modify any v6 / v7 / v8 amendment row.
- Does NOT modify F-INDEX-STALE semantics.
- Does NOT reserve §11 / §13 / §14 / §15 section anchors — each downstream blueprint claims its own at its own v1 LOCK.
- Does NOT extend the closed `primitive_kind` vocabulary.
- Does NOT modify `section_00_5_interface_index_locked.md` on disk — master re-author is a separate ceremony.
- Does NOT update §0.5.8.x count fields in the master — those remain at v5 numbers until master re-author.
- Does NOT register `uploader.attachment_ref.v1` or any attachment-related primitive at v1 — deferred to §12 v1.1 amendment.

# Amendment §I — Thesis round expectations (L-005 two-cycle)

**Round 1 (Editor + Judge + Red Team, cross-family per WS-B dispatch plan):**

- **Editor:** row-id naming consistency with v5 / v6 / v7 / v8 conventions; parent_lock pointer accuracy; PARENT_UNLOCKED-sentinel handling matches existing precedent; description field grounding against §12.4–§12.10 + Tilth governance support-agent definitions.
- **Judge:** scoring against §0.5 amendment rubric — parent-wins discipline preserved? row-count reconciliation math correct (211 + 21 = 232)? PARENT_UNLOCKED sentinels traceable to compound-LOCK ceremony? Per-row primitive_id matches §12.15 enumeration byte-for-byte?
- **Red Team:** adversarial — does row 224 (F-UPLOADER-SIGNATURE-MISMATCH audit-trail subclass) collide with row 220 (F-UPLOADER-SIGNATURE-MISSING) at the failure-registry level? does row 226 (F-UPLOADER-FIELD-MAP-CLOUD-ROUTED) introduce any cross-section dependency on §7 v1.1.1 dialect-routing primitives? does row 215 (`uploader.portal_adapter_protocol.v1`) accurately constrain the four v1 implementations (no foundant/submittable/fluxx leakage in description)? does row 212 (marker) collide with any §1 / §10 marker-kind row? does the file rename create any stale path reference in §0.5 master / §10 amendment / WS-B dispatch plan?

**Round 2 (verification, REFRESH only if Round 1 finds Bucket-A or Bucket-B):** verify Round 1 findings closed; verify file rename propagated through §12 + downstream cite sites; verify JSON companion canonical-bytes equality.

**Synthesis:** operator + Opus 4.7 emits LOCK commit atomically with §12 v1 LOCK + §4 v2.7 amendment LOCK. PARENT_UNLOCKED sentinels resolve at compound LOCK to STABLE.

# Amendment §J — L-005 audit record

**Status: SCOPING DRAFT 2026-05-09 — Thesis Round 1 not yet dispatched.** Per WS-B: Round 1 audits cross-family (Editor + Judge + Red Team families distinct from Scribe drafting family). Self-LOCK basis (this round only — SCOPING DRAFT, not v9 LOCK): amendment-file pattern preserves master-file lock-state; companion to compound-transaction siblings (§12 v1 + §4 v2.7 amendment).

# End of amendment
