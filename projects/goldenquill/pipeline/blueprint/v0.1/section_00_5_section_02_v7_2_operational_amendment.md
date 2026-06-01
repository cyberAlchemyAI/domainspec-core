---
title: §0.5 Blueprint Interface Index — §2 v7.2 operational sub-kinds rows amendment (LOCKED 2026-05-10)
filed: 2026-05-10
operator: Josh
status: LOCKED 2026-05-10 — compound paired-commit with §2 v7.2 LOCK per §6.17 Option-B. L-005 strict two-cycle CLOSED with FULL live cross-family rigor (audit trail at pipeline/validation/v2_v7_2_thesis_2026-05-10/). Operator confirmed Path C-LOCK on architecture-domain disagreement branch (RT-01 maintained on raw-FS write bypass; v7 LOCKED A1+A4+Section O.5 bound v0.1 threat model; v0.2 multi-tenant work track per §10.1 probe checklist).
parent_locks:
  - pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md                      # §0.5 v5 LOCKED 2026-04-19 — 101 master rows
  - pipeline/blueprint/v0.1/section_00_5_section_06_operating_envelope_amendment.md     # §0.5 v6 LOCKED 2026-04-21 — rows 102-117
  - pipeline/blueprint/v0.1/section_00_5_section_07_scribe_amendment.md                 # §0.5 v7 LOCKED 2026-04-21 — rows 118-158
  - pipeline/blueprint/v0.1/section_00_5_section_10_red_team_amendment.md               # §0.5 v8 LOCKED 2026-05-02 — rows 159-211
  - pipeline/blueprint/v0.1/section_00_5_section_12_uploader_amendment.md               # §0.5 v9 LOCKED 2026-05-10 — rows 212-232
  - pipeline/blueprint/v0.1/section_00_5_section_11_intake_amendment.md                 # §0.5 v10 LOCKED 2026-05-10 — rows 233-256
  - pipeline/blueprint/v0.1/section_02_v7_2_amendment.md                                # §2 v7.2 LOCKED 2026-05-10
companion_blueprint_amendment: pipeline/blueprint/v0.1/section_02_v7_2_amendment.md  # paired-commit at §2 v7.2 LOCK per §6.17 Option-B
compound_lock_with: section_02_v7_2_amendment.md v7.2
parent_wins_discipline: each row's parent_lock_version + parent_lock_commit_hash point at §2 v7.2; resolves to actual commit hash at LOCK ceremony.
row_delta: prior runtime-live total after §11 LOCK 2026-05-10 = 256 rows (master 101 + §6 v6 16 + §7 v7 41 + §10 v8 53 + §12 v9 21 + §11 v10 24). **§2 v7.2 amendment claims rows 257-278 (22 rows)**. Runtime-live total at this LOCK = 256 + 22 = 278.
kind_of_amendment: row-append. NO vocabulary extension — every row's `primitive_kind` resolves against the v5 + v6 16-value closed vocabulary (marker / schema / interface-contract / failure-code / pre-gate-check / post-gate-check).
dependency_order: §2 v7.2 LOCK + this §0.5 amendment land as a single compound paired-commit at the same `lock_timestamp_utc`.
f_index_stale_preflight: F-INDEX-STALE PRE-gate fires at commit time; all 22 new rows must be present in the index or the commit fails closed.
cross_family_posture: LIVE FULL CROSS-FAMILY (no Section E carve-out). Editor=groq/llama-3.3-70b-versatile (Meta family) + Judge=google/gemini-2.5-pro (Google family) + Red Team=groq/openai/gpt-oss-120b (OpenAI-OSS family) across both Cycle 1 and Cycle 2. L-005 architecture-domain disagreement branch fired at Cycle 2 close (RT-01 maintained on raw-FS write); operator Path C-LOCK confirmation per v7.0.7 row 180 precedent.
---

# Amendment intent

Lands paired with §2 v7.2 LOCK per §6.17 Option-B compound-commit pattern. Registers §2 v7.2-owned operational sub-kind primitives (one section-anchor marker + eight schema rows + seven interface-contract intent rows + four failure-code rows + one PRE-gate-check row + one POST-gate-check row) into the Index.

The §11 amendment (§0.5 v10 LOCKED 2026-05-10 with rows 233-256) is the load-bearing precedent for substantive blueprint per-section amendments under L-005 strict two-cycle closure with FULL cross-family rigor. v7.2 is a §2 amendment (additive to v7.1 LOCKED 2026-04-19; §2 LOCKED-as-a-whole 2026-04-22) introducing seven SIMPLE operational sub-kinds without altering existing v7.1 SIMPLE/COMPOUND callers.

# Amendment §A — row append (rows 257-278)

All rows enter §0.5 at `stability_tier = "STABLE"` at compound v7.2 LOCK (no PARENT_UNLOCKED transit since §2 v7.2 LOCKs in the same compound transaction).

**Marker (row 257) — §2 v7.2 amendment anchor:**

| Row | primitive_id | defined_at | parent_lock_version | parent_lock_commit_hash | kind | stability_tier |
|---|---|---|---|---|---|---|
| 257 | `blueprint.section_anchor.s2_v7_2_operational.v1` | `pipeline/blueprint/v0.1/section_02_v7_2_amendment.md` | §2 v7.2 | `<resolved_at_commit>` | marker | STABLE |

**Schemas (rows 258-265) — §2 v7.2 sub-kind record classes + registry:**

| Row | primitive_id | defined_at | kind | Parent |
|---|---|---|---|---|
| 258 | `vault.sub_kinds.metrics_record.v1` | `pipeline/blueprint/v0.1/section_02_v7_2_amendment.md#§2.11.1` | schema | MetricsRecord frozen kw_only; ISO-8601 'Z' invariant; severity GREEN |
| 259 | `vault.sub_kinds.financials_record.v1` | `pipeline/blueprint/v0.1/section_02_v7_2_amendment.md#§2.11.2` | schema | FinancialsRecord frozen kw_only; ISO-4217 currency; integer minor units; severity YELLOW |
| 260 | `vault.sub_kinds.photo_record.v1` | `pipeline/blueprint/v0.1/section_02_v7_2_amendment.md#§2.11.3` | schema | PhotoRecord frozen kw_only; SHA-3-512 content_hash; image/* MIME; geo lat/lon both-or-neither; severity YELLOW |
| 261 | `vault.sub_kinds.narrative_entry.v1` | `pipeline/blueprint/v0.1/section_02_v7_2_amendment.md#§2.11.4` | schema | NarrativeEntry frozen kw_only; severity YELLOW |
| 262 | `vault.sub_kinds.timeline_activity.v1` | `pipeline/blueprint/v0.1/section_02_v7_2_amendment.md#§2.11.5` | schema | TimelineActivity frozen kw_only; participants opaque-id-only by operator discipline (RT-04 closure); severity YELLOW |
| 263 | `vault.sub_kinds.beneficiary_record.v1` | `pipeline/blueprint/v0.1/section_02_v7_2_amendment.md#§2.11.6` | schema | BeneficiaryRecord frozen kw_only; PII-consent invariant in `__post_init__` (RED if pii_present, YELLOW if anonymized); per-org opaque-id scoping (RT-03 closure) |
| 264 | `vault.sub_kinds.attachment_record.v1` | `pipeline/blueprint/v0.1/section_02_v7_2_amendment.md#§2.11.7` | schema | AttachmentRecord frozen kw_only; SHA-3-512 content_hash; coordinated-binding to §12 grant-cycle (DC-02 acknowledgment) |
| 265 | `vault.sub_kinds.registry.v1` | `pipeline/blueprint/v0.1/section_02_v7_2_amendment.md#§2.12` | schema | SUB_KIND_REGISTRY: dict[str, SubKindDescriptor]; canonical mapping read at module import time; F-VAULT-ARTIFACT-ONLY extensibility surface (R.PF2 commitment) |

**Interface contracts (rows 266-272) — §2.13 POST_GATE_ALLOWLIST intent rows:**

| Row | primitive_id | defined_at | kind | Parent / intent string |
|---|---|---|---|---|
| 266 | `vault.intent.operational-metrics-write.v1` | `pipeline/blueprint/v0.1/section_02_v7_2_amendment.md#§2.13` | interface-contract | `operational-metrics-write` SIMPLE → prefix `operational/metrics/`, mode `write-if-absent` |
| 267 | `vault.intent.operational-financials-write.v1` | `pipeline/blueprint/v0.1/section_02_v7_2_amendment.md#§2.13` | interface-contract | `operational-financials-write` SIMPLE → prefix `operational/financials/`, mode `write-if-absent` |
| 268 | `vault.intent.operational-photos-write.v1` | `pipeline/blueprint/v0.1/section_02_v7_2_amendment.md#§2.13` | interface-contract | `operational-photos-write` SIMPLE → prefix `operational/photos/`, mode `write-if-absent` |
| 269 | `vault.intent.operational-narrative-write.v1` | `pipeline/blueprint/v0.1/section_02_v7_2_amendment.md#§2.13` | interface-contract | `operational-narrative-write` SIMPLE → prefix `operational/narratives/`, mode `write-if-absent` |
| 270 | `vault.intent.operational-timeline-write.v1` | `pipeline/blueprint/v0.1/section_02_v7_2_amendment.md#§2.13` | interface-contract | `operational-timeline-write` SIMPLE → prefix `operational/timeline/`, mode `write-if-absent` |
| 271 | `vault.intent.operational-beneficiary-write.v1` | `pipeline/blueprint/v0.1/section_02_v7_2_amendment.md#§2.13` | interface-contract | `operational-beneficiary-write` SIMPLE → prefix `operational/beneficiaries/`, mode `write-if-absent`; PII-consent gating dispatched to §6 Cedar Rules 2+3 |
| 272 | `vault.intent.operational-attachment-write.v1` | `pipeline/blueprint/v0.1/section_02_v7_2_amendment.md#§2.13` | interface-contract | `operational-attachment-write` SIMPLE → prefix `operational/attachments/`, mode `write-if-absent`; §12 v1.1 horizon binding via `attached_to_grant_id` |

**Failure codes (rows 273-276) — §7 explode pattern; one row per F-CEDAR-OPERATIONAL-* / F-OPERATIONAL-* code at v7.2:**

| Row | primitive_id | defined_at | kind | Parent / sub-tags |
|---|---|---|---|---|
| 273 | `vault.failure_code.F-CEDAR-OPERATIONAL-DENIED.v1` | `pipeline/blueprint/v0.1/section_02_v7_2_amendment.md#§7` | failure-code | Cedar evaluator deny when no rule permits. Sub-tags `.org_slug_mismatch`, `.consent_tier_mismatch_or_pii_unauthorized`. Catch-all for any combination not matching §6 Rules 1/2/3. |
| 274 | `vault.failure_code.F-OPERATIONAL-PII-CONSENT-MISSING.v1` | `pipeline/blueprint/v0.1/section_02_v7_2_amendment.md#§7` | failure-code | Schema validator caught beneficiary record claiming pii_present=True without matching consent tier OR with empty pii_fields. Fail-closed at `BeneficiaryRecord.__post_init__`. ALSO surfaces from Cedar evaluator when schema-valid record presented by principal lacking `operator_authorized_pii`. |
| 275 | `vault.failure_code.F-OPERATIONAL-SCHEMA-INVALID.v1` | `pipeline/blueprint/v0.1/section_02_v7_2_amendment.md#§7` | failure-code | Generic schema validation failure at decode (round-trip rejection); decoder re-runs `__post_init__` invariants on every read. |
| 276 | `vault.failure_code.F-OPERATIONAL-ORG-MISMATCH.v1` | `pipeline/blueprint/v0.1/section_02_v7_2_amendment.md#§7` | failure-code | NEW per RT-08 Cycle-1 closure. `policy_eval.py` raises when path-derived slug ≠ `resource.org_slug_hint`. Distinct, debuggable failure surface vs. generic F-CEDAR-OPERATIONAL-DENIED. v0.2 read-time companion adds RT-C1-03 forward probe per §10.1. |

**PRE-gate-check (row 277) — consolidated POST_GATE_ALLOWLIST validation per §4.10.4 step 4.5/5/6/7 + §4.10.6 kind-class hard-gate:**

| Row | primitive_id | defined_at | kind | Parent / consolidated codes covered |
|---|---|---|---|---|
| 277 | `vault.pre_gate.operational_allowlist_check.v1` | `pipeline/blueprint/v0.1/section_02_v7_2_amendment.md#§2.13` | pre-gate-check | Single allowlist-validation pass at PRE-gate covering all 7 SIMPLE operational intents; backs F-CEDAR-SECTION4-WRITE-PATH-DENIED (parent v7.1 surface, unchanged) + F-OPERATIONAL-ORG-MISMATCH (rev2 narrow-fix path-vs-org_slug_hint check). Validates intent type, prefix match, mode match, kind-class hard-gate (SIMPLE → MUST NOT carry txn_token). |

**POST-gate-check (row 278) — Cedar evaluator cross-product enforcement matrix:**

| Row | primitive_id | defined_at | kind | Parent / consolidated codes covered |
|---|---|---|---|---|
| 278 | `vault.post_gate.operational_cedar_evaluator.v1` | `pipeline/blueprint/v0.1/section_02_v7_2_amendment.md#§6` | post-gate-check | Cedar evaluator (`pipeline/vault/sub_kinds/policy_eval.py::evaluate_operational_write`) running §6 Rules 1/2/3 + cross-product enforcement matrix. Authoritative at v0.1 per §2 v7.1 §3.4 lifecycle until M15-sealed. Backs F-CEDAR-OPERATIONAL-DENIED + F-OPERATIONAL-PII-CONSENT-MISSING. RT-C1-04 forward probe (v0.2 / M15.x sealing CI) binds Cedar/Python equivalence at §10.1. |

# Compound paired-commit ceremony

This file lands at the same `lock_timestamp_utc` as §2 v7.2 amendment LOCK. Lock_history row 186 (lock_class=blueprint_amendment) sibling 1/2; row 187 (lock_class=blueprint_amendment_companion) sibling 2/2 — paired commit per §6.17 Option-B.

# F-VAULT-ARTIFACT-ONLY architectural commitment

Per architecture v7 LOCKED 2026-04-19 §R.PF2: a §2 spin that rejects operational data sub-kinds at the schema level fails the audit. v7.2 EXPOSES the schema via the `SUB_KIND_REGISTRY` (row 265) such that adding an eighth operational sub-kind = (1) new module under `pipeline/vault/sub_kinds/`, (2) new schema row in §0.5, (3) new interface-contract intent row in §0.5, (4) new prefix row in `POST_GATE_ALLOWLIST`. Three-line extensibility — F-VAULT-ARTIFACT-ONLY rubric satisfied.
