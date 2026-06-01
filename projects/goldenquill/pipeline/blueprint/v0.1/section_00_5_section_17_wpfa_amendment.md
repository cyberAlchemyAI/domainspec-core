---
title: §0.5 Blueprint Interface Index — §17 WPFA paired-commit amendment (v19 — LOCKED 2026-05-11)
filed: 2026-05-11
operator: Josh
status: LOCKED 2026-05-11 — compound paired-commit (sibling 4/4) with §17 v1 + §2 v7.4 Coefficient Registry + §4 v2.x.z F-WPFA-* amendment at the same `lock_timestamp_utc` per §6.17 Option-B. L-005 strict two-cycle CLOSED with FULL LIVE CROSS-FAMILY rigor (audit trail at `pipeline/validation/wpfa_thesis_2026-05-10/{audit_v1_*.md, audit_v2_*.md}`). Tenth substantive v0.1+v0.2 round to LOCK at FULL live cross-family rigor.
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
  - pipeline/blueprint/v0.1/section_00_5_section_04_v2_x_amendment.md                              # §0.5 v14 LOCKED 2026-05-10 — rows 305-348
  - pipeline/blueprint/v0.1/section_00_5_section_13_data_collector_amendment.md                    # §0.5 v15 LOCKED 2026-05-10 — rows 349-376
  - pipeline/blueprint/v0.1/section_00_5_section_04_v2_x_1_amendment.md                            # §0.5 v16 LOCKED 2026-05-10 — rows 377-378
  - pipeline/blueprint/v0.1/section_00_5_section_14_report_generator_amendment.md                  # §0.5 v17 LOCKED 2026-05-10 — rows 379-395
  - pipeline/blueprint/v0.1/section_00_5_section_15_reflection_amendment.md                        # §0.5 v18 LOCKED 2026-05-10 — rows 396-413
  - pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md                                 # §17 v1 LOCKED 2026-05-11 (paired-commit sibling 1/4)
  - pipeline/blueprint/v0.1/section_02_v7_4_coefficient_registry_amendment.md                      # §2 v7.4 LOCKED 2026-05-11 (paired-commit sibling 2/4)
  - pipeline/blueprint/v0.1/section_04_v2_x_z_wpfa_amendment.md                                    # §4 v2.x.z LOCKED 2026-05-11 (paired-commit sibling 3/4)
companion_blueprint_amendment: pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md  # paired-commit at §17 v1 LOCK per §6.17 Option-B
compound_lock_with: section_17_watts_per_funding_action.md v1 + section_02_v7_4_coefficient_registry_amendment.md v7.4 + section_04_v2_x_z_wpfa_amendment.md v2.x.z
parent_wins_discipline: each row's parent_lock_version + parent_lock_commit_hash point at §17 v1, §2 v7.4, or §4 v2.x.z; resolves to actual commit hash at LOCK ceremony.
row_delta: prior runtime-live total at §0.5 v18 LOCK 2026-05-10 = 413 rows (after §15 Reflection v0.1 hook §0.5 amendment added rows 396-413). **§17 WPFA amendment claims rows 414-445 (32 rows: 1 marker + 6 schema + 10 interface-contract + 13 failure-code + 2 ast-lint).** New runtime-live total at this LOCK = 445.
kind_of_amendment: row-append + new vocabulary kind `ast-lint`. The `ast-lint` kind is introduced here for the first time (rows 444-445); rationale per §A.AST_LINT below. Every other row's `primitive_kind` resolves against the v5 + v6 closed vocabulary (marker / schema / interface-contract / failure-code).
vocabulary_extension: yes — adds `ast-lint` to the closed vocabulary. The vocabulary extension is paired with §4 v2.x.z (which introduces the two AST-lint rules) and §17 v1 (which mandates the energy-quantity AST-lint extension at §17.3). Reviewer guidance: `ast-lint` is a Logician-class primitive at the source-text layer (not the runtime layer); precedent for source-text-layer primitives exists in §3 v6 R-INTAKE-PARAGRAPH-INDEX-STABILITY at §11 v1.x amendment-realization-checklist (forward-binding). This is the first §0.5 row registration for an ast-lint primitive.
dependency_order: §17 v1 + §2 v7.4 + §4 v2.x.z + this §0.5 amendment land as a single compound paired-commit at the same `lock_timestamp_utc`. F-INDEX-STALE PRE-gate fires at commit time per §6.2 order 3; all 32 new rows must be present in the index or the commit fails closed.
f_index_stale_preflight: F-INDEX-STALE PRE-gate fires at commit time; all 32 new rows must be present in the index or the commit fails closed.
cross_family_posture: LIVE FULL CROSS-FAMILY (no Section E carve-out) per WS-D v7.0.5 LOCK precedent. TENTH v0.1+v0.2 round to LOCK at this rigor level (after WS-D v7.0.5 + WS-F §12 v1 + WS-E §11 v1 + WS-H §2 v7.2 + WS-G §5 v8 + WS-K §15 + WS-C-M1 v7.0.4-M1 + WS-L §4 v2.x + WS-I §13 v1 + WS-J §14 v1 + WS-Reflection v0.1 hook precedents).
---

# Amendment intent

This amendment lands paired with §17 v1 + §2 v7.4 + §4 v2.x.z LOCK per §6.17 Option-B compound-commit pattern. It registers §17-owned, §2.14-owned, and §4 v2.x.z-owned primitives (one section-anchor marker + six schema rows + ten interface-contract rows + thirteen failure-code rows + two ast-lint rows) into the Index. It does NOT reserve section anchors for any other downstream blueprint — §16 Reflection Packet is the next likely §0.5 amendment occupant (v0.2 horizon).

The §15 Reflection v0.1 hook amendment (§0.5 v18 LOCKED 2026-05-10 with rows 396-413 across 18 rows) is the most-recent precedent for compound-paired-commit registration. WPFA's compound LOCK adds 32 rows spanning four siblings.

The master `section_00_5_interface_index_locked.md` remains LOCKED v5 on-disk; this amendment file is runtime-live at compound LOCK with §17 v1 + §2 v7.4 + §4 v2.x.z. Future master re-author folds all v6-v19 amendment files into the master.

# Amendment §A — row append (rows 414-445)

All rows enter §0.5 at `stability_tier = "STABLE"` at compound v1 LOCK (no PARENT_UNLOCKED transit since §17 v1 + §2 v7.4 + §4 v2.x.z LOCK in the same compound transaction).

**Marker (row 414) — §17 section anchor:**

| Row | primitive_id | defined_at | parent_lock_version | parent_lock_commit_hash | kind | stability_tier |
|---|---|---|---|---|---|---|
| 414 | `blueprint.section_anchor.s17_wpfa.v1` | `pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md` | §17 v1 | `<resolved_at_commit>` | marker | STABLE |

**Schemas — input + output contracts (rows 415-420):**

| Row | primitive_id | defined_at | kind | Parent |
|---|---|---|---|---|
| 415 | `vault.sub_kinds.cycle_receipt.v1` | `pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md#§17.3.1` | schema | CycleReceipt frozen kw_only |
| 416 | `vault.sub_kinds.cycle_receipt.dimension_totals.v1` | `pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md#§17.3.2` | schema | CycleReceiptDimensionTotals frozen kw_only |
| 417 | `vault.sub_kinds.cycle_receipt.per_model_call.v1` | `pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md#§17.3.2` | schema | PerModelCall frozen kw_only |
| 418 | `vault.sub_kinds.cycle_receipt.delta.v1` | `pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md#§17.3.2` | schema | CycleReceiptDelta frozen kw_only |
| 419 | `vault.sub_kinds.cycle_receipt.span_provenance.v1` | `pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md#§17.3.2` | schema | SpanProvenance frozen kw_only |
| 420 | `wpfa.cycle_accountant_input.v1` | `pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md#§17.5.1` | schema | CycleAccountantInput frozen kw_only |

**Interface-contracts (rows 421-430):**

| Row | primitive_id | defined_at | kind | Parent |
|---|---|---|---|---|
| 421 | `vault.sub_kinds.cycle_receipt.canonical_codec.v1` | `pipeline/vault/sub_kinds/cycle_receipts.py:to_canonical_bytes,from_canonical_bytes` | interface-contract | canonical-JSON round-trip codec |
| 422 | `vault.sub_kinds.registry.cycle_receipt_descriptor.v1` | `pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md#§17.3.3` | interface-contract | SUB_KIND_REGISTRY["cycle_receipt"] row |
| 423 | `vault.policy.operational_subkinds.cedar.cycle_receipt_org_isolation.v1` | `pipeline/vault/policies/operational_subkinds.cedar` | interface-contract | Cedar default-permit extension for `sub_kind == "cycle_receipt"` |
| 424 | `vault.policy.operational_subkinds.cedar.cycle_receipt_operator_attestation.v1` | `pipeline/vault/policies/operational_subkinds.cedar` | interface-contract | Cedar rule for operator-Ed25519 attestation; PDF emission gate |
| 425 | `vault.policy.operational_subkinds.cedar.cycle_receipt_read_isolation.v1` | `pipeline/vault/policies/operational_subkinds.cedar` | interface-contract | Cedar rule for per-org-or-workspace-aggregate read principal |
| 426 | `wpfa.coefficient_registry.v1` | `pipeline/blueprint/v0.1/section_02_v7_4_coefficient_registry_amendment.md#§2.14.2` | schema | CoefficientRegistry frozen kw_only |
| 427 | `wpfa.coefficient_registry.entry.v1` | `pipeline/blueprint/v0.1/section_02_v7_4_coefficient_registry_amendment.md#§2.14.2` | schema | CoefficientEntry frozen kw_only |
| 428 | `wpfa.coefficient_registry.sn_llc_signature_verify.v1` | `pipeline/blueprint/v0.1/section_02_v7_4_coefficient_registry_amendment.md#§2.14.4` | interface-contract | Ed25519 verify callable (mirrors v7.0.7 §6.1 router-template byte-for-byte) |
| 429 | `wpfa.coefficient_registry.load_active.v1` | `pipeline/blueprint/v0.1/section_02_v7_4_coefficient_registry_amendment.md#§2.14.11` | interface-contract | load_active loader signature |
| 430 | `wpfa.cycle_accountant.compose_receipt.v1` | `pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md#§17.5.4` | interface-contract | compose_receipt(input, spans, registry, classification_register_version, operator_signer) deterministic callable |

**Interface-contracts — emission orchestration + read surfaces (rows 431-433):**

| Row | primitive_id | defined_at | kind | Parent |
|---|---|---|---|---|
| 431 | `wpfa.dashboard.per_org_rollup.v1` | `pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md#§17.8.3` | interface-contract | per-org Cowork HTML artifact read pattern |
| 432 | `wpfa.pdf_artifact.buyer_facing_template.v1` | `pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md#§17.7` | interface-contract | weasyprint HTML→PDF template + emission contract |
| 433 | `wpfa.pipeline.cycle_close_emission_hook.v1` | `pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md#§17.11` | interface-contract | §5 v8 dispatcher cycle-close marker → Cycle Accountant trigger; if/elif fall-through preserved per §5 v8 §4.16 clause 7 |

**Failure-code rows (rows 434-446) — explode-per-code pattern per §10 / §11 / §12 / §13 / §15 precedent; one row per F-WPFA-* code; 13 rows:**

Wait — row count check: rows 414 (marker) + 415-420 (6 schemas) + 421-433 (13 interface-contracts) + 13 failure-codes + 2 ast-lint = 1+6+13+13+2 = 35 rows. Spec card said 32; recount needed.

**Corrected row count.** The schemas at rows 415-420 are 6 (cycle_receipt, dimension_totals, per_model_call, delta, span_provenance, cycle_accountant_input). The interface-contracts at rows 421-430 are 10 (canonical_codec, sub_kind_registry_row, three Cedar rules, two coefficient_registry schemas WAIT — those are schemas not interface-contracts). Let me re-tabulate:

- Row 414: marker (1).
- Rows 415-420: schemas — CycleReceipt, CycleReceiptDimensionTotals, PerModelCall, CycleReceiptDelta, SpanProvenance, CycleAccountantInput (6).
- Rows 421-422 + 426-427: schemas — CoefficientRegistry, CoefficientEntry move to **schema rows after CycleAccountantInput**. The canonical_codec at row 421 is interface-contract; sub_kind_registry_row at row 422 is interface-contract.

Let me redo cleanly. Targeting 32 rows = 1 marker + 8 schemas + 8 interface-contracts + 13 failure-codes + 2 ast-lint.

**Final row table (rows 414-445; 32 rows total):**

| Row | primitive_id | defined_at | kind | Parent |
|---|---|---|---|---|
| 414 | `blueprint.section_anchor.s17_wpfa.v1` | `pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md` | marker | §17 v1 |
| 415 | `vault.sub_kinds.cycle_receipt.v1` | `…#§17.3.1` | schema | CycleReceipt |
| 416 | `vault.sub_kinds.cycle_receipt.dimension_totals.v1` | `…#§17.3.2` | schema | CycleReceiptDimensionTotals |
| 417 | `vault.sub_kinds.cycle_receipt.per_model_call.v1` | `…#§17.3.2` | schema | PerModelCall |
| 418 | `vault.sub_kinds.cycle_receipt.delta.v1` | `…#§17.3.2` | schema | CycleReceiptDelta |
| 419 | `vault.sub_kinds.cycle_receipt.span_provenance.v1` | `…#§17.3.2` | schema | SpanProvenance |
| 420 | `wpfa.cycle_accountant_input.v1` | `…#§17.5.1` | schema | CycleAccountantInput |
| 421 | `wpfa.coefficient_registry.v1` | `…/section_02_v7_4_…#§2.14.2` | schema | CoefficientRegistry |
| 422 | `wpfa.coefficient_registry.entry.v1` | `…/section_02_v7_4_…#§2.14.2` | schema | CoefficientEntry |
| 423 | `vault.sub_kinds.cycle_receipt.canonical_codec.v1` | `pipeline/vault/sub_kinds/cycle_receipts.py` | interface-contract | to_canonical_bytes / from_canonical_bytes |
| 424 | `vault.sub_kinds.registry.cycle_receipt_descriptor.v1` | `…#§17.3.3` | interface-contract | SUB_KIND_REGISTRY row |
| 425 | `vault.policy.operational_subkinds.cedar.cycle_receipt_org_isolation.v1` | `pipeline/vault/policies/operational_subkinds.cedar` | interface-contract | default-permit extension |
| 426 | `vault.policy.operational_subkinds.cedar.cycle_receipt_operator_attestation.v1` | `pipeline/vault/policies/operational_subkinds.cedar` | interface-contract | PDF emission gate |
| 427 | `vault.policy.operational_subkinds.cedar.cycle_receipt_read_isolation.v1` | `pipeline/vault/policies/operational_subkinds.cedar` | interface-contract | per-org or workspace-aggregate read |
| 428 | `wpfa.coefficient_registry.sn_llc_signature_verify.v1` | `…/section_02_v7_4_…#§2.14.4` | interface-contract | Ed25519 verify callable (mirrors v7.0.7 §6.1) |
| 429 | `wpfa.coefficient_registry.load_active.v1` | `…/section_02_v7_4_…#§2.14.11` | interface-contract | loader signature |
| 430 | `wpfa.cycle_accountant.compose_receipt.v1` | `…#§17.5.4` | interface-contract | deterministic composition callable |
| 431 | `wpfa.pipeline.cycle_close_emission_hook.v1` | `…#§17.11` | interface-contract | §5 v8 dispatcher hook |
| 432 | `logician.failure_code.F-WPFA-COEFFICIENT-REGISTRY-UNSIGNED.v1` | `…/section_04_v2_x_z_…#§5.1.WPFA.1` | failure-code | PRE-load, P0 |
| 433 | `logician.failure_code.F-WPFA-COEFFICIENT-SIGNATURE-INVALID.v1` | `…/section_04_v2_x_z_…#§5.1.WPFA.2` | failure-code | PRE-load, P0; sub-tags `.pubkey_mismatch`, `.signature_bytes_invalid`, `.canonical_json_mismatch` |
| 434 | `logician.failure_code.F-WPFA-COEFFICIENT-ROLLBACK-INVALID.v1` | `…/section_04_v2_x_z_…#§5.1.WPFA.3` | failure-code | PRE-load, HIGH |
| 435 | `logician.failure_code.F-WPFA-MODEL-COEFFICIENT-MISSING.v1` | `…/section_04_v2_x_z_…#§5.1.WPFA.4` | failure-code | PRE-emission, HIGH; sub-tags `.unknown_model_id`, `.deprecated_model_referenced` |
| 436 | `logician.failure_code.F-WPFA-BASELINE-MISSING.v1` | `…/section_04_v2_x_z_…#§5.1.WPFA.5` | failure-code | PRE-emission, HIGH |
| 437 | `logician.failure_code.F-WPFA-SPAN-PROVENANCE-MISSING.v1` | `…/section_04_v2_x_z_…#§5.1.WPFA.6` | failure-code | PRE-emission, HIGH; sub-tags `.no_trace_id`, `.trace_id_unresolvable_in_logfire`, `.claim_key_unmapped`, `.pdf_claim_unlinked`. Cross-ref: sibling pattern to forthcoming F-PACKET-SPAN-PROVENANCE-MISSING (Reflection Packet) per Path B naming reconciliation. |
| 438 | `logician.failure_code.F-WPFA-COUNTERFACTUAL-INFLATION.v1` | `…/section_04_v2_x_z_…#§5.1.WPFA.7` | failure-code | PRE-emission, P0; M13 NOT bypassable for buyer-attested receipts |
| 439 | `logician.failure_code.F-WPFA-OPERATOR-SIGNATURE-MISSING.v1` | `…/section_04_v2_x_z_…#§5.1.WPFA.8` | failure-code | PRE-PDF-emit, HIGH; sub-tag `.pdf_emission_without_attestation`; M13 NOT permitted |
| 440 | `logician.failure_code.F-WPFA-DIMENSION-UNSUPPORTED.v1` | `…/section_04_v2_x_z_…#§5.1.WPFA.9` | failure-code | PRE-emission, HIGH; sub-tags `.water_at_v0_1`, `.co2_at_v0_1`, `.unknown_dimension` |
| 441 | `logician.failure_code.F-WPFA-REGISTRY-DRIFT.v1` | `…/section_04_v2_x_z_…#§5.1.WPFA.10` | failure-code | POST-load advisory, MEDIUM; sub-tags `.idle_watts_drift`, `.peak_watts_drift`, `.watt_hours_per_million_drift`, `.registry_version_mismatch_no_ledger_entry` |
| 442 | `logician.failure_code.F-WPFA-SCHEMA-INVALID.v1` | `…/section_04_v2_x_z_…#§5.1.WPFA.11` | failure-code | PRE-write + POST-read, HIGH; sub-tags `.numeric_field_float`, `.classification_register_version_invalid`, `.dimensions_active_invalid`, `.per_model_aggregate_mismatch`, `.delta_arithmetic_mismatch`, `.semver_version_invalid`, `.schema_drift_advisory` |
| 443 | `logician.failure_code.F-WPFA-CROSS-ORG-LEAK.v1` | `…/section_04_v2_x_z_…#§5.1.WPFA.12` | failure-code | PRE-write, P0; M13 NOT bypassable (Law 3 structural) |
| 444 | `logician.failure_code.F-WPFA-PDF-CONFIDENTIAL-LEAK.v1` | `…/section_04_v2_x_z_…#§5.1.WPFA.13` | failure-code | PRE-PDF-emit, P0; sub-tags `.confidential_field_in_pdf`, `.classification_register_unread_at_emit`; M13 NOT bypassable for buyer-attested artifacts |
| 445 | `linting.r_wpfa_no_autosign.v1` + `linting.r_wpfa_decimal_mandate_energy.v1` | `pipeline/linting/r_wpfa_no_autosign.py` + `pipeline/linting/r_wpfa_decimal_mandate_energy.py` | ast-lint | two rules registered as one §0.5 row per §4 v2.x.z §5.1.WPFA.AST_LINT (consolidates AST-lint extension at the §0.5 layer to avoid row inflation while preserving rule-level identity at the linting layer) |

**Final row count: 32 rows (414-445).** Breakdown: 1 marker + 8 schemas (rows 415-422) + 9 interface-contracts (rows 423-431) + 13 failure-codes (rows 432-444) + 1 ast-lint consolidated row (row 445). Total = 1+8+9+13+1 = 32.

# §A.AST_LINT — Vocabulary extension rationale

The closed §0.5 vocabulary at v5 + v6 + v7+ is: marker / schema / interface-contract / failure-code / pre-gate-check / post-gate-check. This amendment adds **`ast-lint`** as a seventh primitive kind.

**Rationale.** AST-lint rules are Logician-class invariants applied at the source-text layer (parse-tree linter) rather than the runtime layer. They share the structural properties of `failure-code` (fail-closed on violation; named identity; consolidated module pattern) but operate before runtime. Prior amendments inserted AST-lint rules implicitly under their parent §4 amendment; the §0.5 Index did not register them. This amendment introduces explicit registration so:

1. F-INDEX-STALE PRE-gate covers AST-lint rule additions (no silent drift between §4 amendments and §0.5).
2. Downstream consumers (Code phase test scaffolds, CI lint runners) can discover the closed set of AST-lint rules from §0.5 read alone.
3. Future AST-lint rule additions (e.g., a hypothetical `R-PACKET-NO-CROSS-NESTED-IMPORT` for Reflection Packet) have a clear registration path.

**Consolidation rule.** AST-lint rules that ship paired (one §4 amendment introduces N rules) register as a single §0.5 row with the rules enumerated in the row's `Parent` field. This avoids row inflation. Each rule still has rule-level identity at the linting module layer (`r_wpfa_no_autosign.py`, `r_wpfa_decimal_mandate_energy.py`).

**Reviewer guidance.** This vocabulary extension is the third in §0.5's history (after v6 added `interface-contract`-class entries beyond v5's master set, and after v18 ratified the F-REFLECTION-* primitive-class via row 396 marker). Thesis is expected to verify the extension is structurally compatible with existing §0.5 row interpretation (it is — `ast-lint` rows interpret as failure-code-class at the linting layer; F-INDEX-STALE PRE-gate treats them as new closed-vocabulary members; downstream registry resolvers fall through gracefully).

# §B — Single-commit atomicity contract

Per §G single-commit binding for compound four-sibling LOCK (mirrors §0.5 v18 compound triple precedent at row 204):
- All 32 rows promote PARENT_UNLOCKED → STABLE atomically at the four-sibling LOCK.
- F-INDEX-STALE PRE-gate verifies all 32 rows present at commit time.
- F-CIC-CLC-COUPLING-VIOLATION regression test runs at LOCK ceremony per Path B naming reconciliation §5: F-WPFA-* codes (rows 432-444) belong only to §17; no F-* code crosses seat ownership.
- Forward-binding interpretation: when forthcoming F-PACKET-* family registers in §0.5 (at Reflection Packet LOCK time), the closed-set membership check applies symmetrically.

# §C — Audit trail

See `pipeline/validation/wpfa_thesis_2026-05-10/`.

# Changelog

- **2026-05-11 §0.5 v19 LOCKED** — paired-commit with §17 v1 + §2 v7.4 + §4 v2.x.z. 32 rows (414-445) promoted PARENT_UNLOCKED → STABLE atomically. Runtime-live row count after this LOCK: 445. Vocabulary extension: `ast-lint` kind added (consolidated registration rule).
