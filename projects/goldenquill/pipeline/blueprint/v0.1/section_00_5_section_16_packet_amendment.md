---
title: §0.5 Blueprint Interface Index — §16 Reflection Packet paired-commit amendment (v21 — LOCKED 2026-05-15)
filed: 2026-05-15
operator: Josh
status: LOCKED 2026-05-15 — compound paired-commit (sibling 3/3) with §16 v1 + §4 v2.x.y F-PACKET-* at the same `lock_timestamp_utc` per §6.17 Option-B. L-005 strict two-cycle CLOSED with FULL LIVE CROSS-FAMILY rigor (audit trail at `pipeline/validation/reflection_packet_thesis_2026-05-11/{audit_v{1,2}_*.md, cycle_{1,2}_disposition.md}`). Thirteenth substantive v0.1+v0.2 round to LOCK at FULL live cross-family rigor.
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
  - pipeline/blueprint/v0.1/section_00_5_section_17_wpfa_amendment.md                              # §0.5 v19 LOCKED 2026-05-11 — rows 414-445; `ast-lint` vocabulary kind landed
  - pipeline/blueprint/v0.1/section_00_5_section_11_v1_1_amendment.md                              # §0.5 v19 paired-commit 2026-05-11 (narrow-corrective; rows 414-415 actually allocated by §11 v1.1; full §0.5 v19 spans 414-445 due to WPFA dual-commit at same row range vocabulary alignment)
  - pipeline/blueprint/v0.1/section_00_5_section_funding_goal_amendment.md                         # §0.5 v20 LOCKED 2026-05-11 — rows 446-470; `seat_owner` row attribute extension landed (RT-19 closure)
  - pipeline/blueprint/v0.1/section_16_reflection_packet.md                                        # §16 v1 (paired-commit sibling 1/3)
  - pipeline/blueprint/v0.1/section_04_v2_x_y_packet_amendment.md                                  # §4 v2.x.y (paired-commit sibling 2/3)
companion_blueprint_amendment: pipeline/blueprint/v0.1/section_16_reflection_packet.md  # paired-commit per §6.17 Option-B
compound_lock_with: section_16_reflection_packet.md v1 + section_04_v2_x_y_packet_amendment.md v2.x.y
parent_wins_discipline: each row's parent_lock_version + parent_lock_commit_hash point at §16 v1 or §4 v2.x.y; resolves to actual commit hash at LOCK ceremony.
row_delta: prior runtime-live total at §0.5 v20 LOCK 2026-05-11 = 470 rows. **§0.5 v22 amendment claims rows 471-505 (35 rows: 1 marker + 7 schema + 8 interface-contract + 19 failure-code).** Every row carries `seat_owner: "reflection_packet"` per RT-19 extension landed at §0.5 v20 row 414+ (FG amendment). New runtime-live total at this LOCK = 505.
kind_of_amendment: row-append with seat_owner attribute. NO new vocabulary kind — every row's `primitive_kind` resolves against the v5 + v6 + v19 closed vocabulary (marker / schema / interface-contract / failure-code / ast-lint).
seat_owner_attribute: every row in this amendment carries `seat_owner: "reflection_packet"` per RT-19 extension (landed at §0.5 v20 FG amendment). F-INDEX-STALE PRE-gate verifies seat_owner consistency across all 35 rows at compound commit; deviation triggers F-INDEX-STALE with sub-tag `.seat_owner_mismatch` per §0.5 v20 RT-C2-09 precedent.
dependency_order: §16 v1 + §4 v2.x.y + this §0.5 amendment land as a single compound paired-commit at the same `lock_timestamp_utc`. F-INDEX-STALE PRE-gate fires at commit time per §6.2 order 3; all 35 new rows must be present in the index or the compound commit fails closed.
f_index_stale_preflight: F-INDEX-STALE PRE-gate fires at commit time; all 35 new rows must be present in the index AND every row must carry seat_owner: "reflection_packet" or the commit fails closed.
cross_family_posture: LIVE FULL CROSS-FAMILY (no Section E carve-out) per WS-D v7.0.5 LOCK precedent. THIRTEENTH v0.1+v0.2 round to LOCK at this rigor level (after WS-D v7.0.5 + WS-F §12 v1 + WS-E §11 v1 + WS-H §2 v7.2 + WS-G §5 v8 + WS-K §15 + WS-C-M1 v7.0.4-M1 + WS-L §4 v2.x + WS-I §13 v1 + WS-J §14 v1 + WS-Reflection v0.1 hook + WS-WPFA + WS-FG precedents).
---

# Amendment intent

This amendment lands paired with §16 v1 + §4 v2.x.y LOCK per §6.17 Option-B compound-commit pattern (triple). It registers §16-owned, §4 v2.x.y-owned primitives (one section-anchor marker + seven schema rows + eight interface-contract rows + nineteen failure-code rows = 35 rows) into the Index. Every row carries `seat_owner: "reflection_packet"` per the §0.5 v20 RT-19 extension (FG amendment landed the attribute; this amendment is the first follow-on amendment binding under the new invariant).

The §0.5 v20 FG amendment (LOCKED 2026-05-11 with rows 446-470 across 25 rows + seat_owner attribute extension) is the most-recent precedent. Reflection Packet's compound triple LOCK adds 35 rows.

The master `section_00_5_interface_index_locked.md` remains LOCKED v5 on-disk; this amendment file is runtime-live at compound LOCK with §16 v1 + §4 v2.x.y. Future master re-author folds all v6-v21 amendment files into the master.

# Amendment §A — row append (rows 471-505)

All rows enter §0.5 at `stability_tier = "STABLE"` at compound v1 LOCK (no PARENT_UNLOCKED transit since §16 v1 + §4 v2.x.y LOCK in the same compound transaction).

**Marker (row 471) — §16 section anchor:**

| Row | primitive_id | defined_at | parent_lock_version | parent_lock_commit_hash | kind | seat_owner | stability_tier |
|---|---|---|---|---|---|---|---|
| 471 | `blueprint.section_anchor.s16_reflection_packet.v1` | `pipeline/blueprint/v0.1/section_16_reflection_packet.md` | §16 v1 | `<resolved_at_commit>` | marker | reflection_packet | STABLE |

**Schemas (rows 472-478):**

| Row | primitive_id | defined_at | kind | seat_owner | Parent |
|---|---|---|---|---|---|
| 472 | `vault.sub_kinds.reflection_packet.v1` | `section_16_reflection_packet.md#§16.2.1` | schema | reflection_packet | `ReflectionPacket` frozen kw_only |
| 473 | `vault.sub_kinds.reflection_packet.pattern_observation.v1` | `section_16_reflection_packet.md#§16.2.2` | schema | reflection_packet | `PatternObservation` frozen kw_only |
| 474 | `vault.sub_kinds.reflection_packet.proposed_lesson.v1` | `section_16_reflection_packet.md#§16.2.2` | schema | reflection_packet | `ProposedLesson` frozen kw_only |
| 475 | `vault.sub_kinds.reflection_packet.gate_pass_counts.v1` | `section_16_reflection_packet.md#§16.2.2` | schema | reflection_packet | `GatePassCounts` frozen kw_only |
| 476 | `vault.sub_kinds.reflection_packet.score_signals.v1` | `section_16_reflection_packet.md#§16.2.2` | schema | reflection_packet | `ScoreSignals` frozen kw_only |
| 477 | `vault.sub_kinds.reflection_packet.cycle_outcome.v1` | `section_16_reflection_packet.md#§16.2.2` | schema | reflection_packet | `CycleOutcome` frozen kw_only |
| 478 | `vault.sub_kinds.reflection_packet.span_provenance.v1` | `section_16_reflection_packet.md#§16.2.2` | schema | reflection_packet | `PacketSpanProvenance` frozen kw_only |

**Interface-contracts (rows 479-486):**

| Row | primitive_id | defined_at | kind | seat_owner | Parent |
|---|---|---|---|---|---|
| 479 | `vault.sub_kinds.reflection_packet.canonical_codec.v1` | `pipeline/vault/sub_kinds/reflection_packets.py:to_canonical_json_bytes,from_canonical_json_bytes` | interface-contract | reflection_packet | canonical-JSON round-trip codec (LIVE scaffold at v0.1 hook; signature-field-exclusion enforced at SHA3-512 boundary per §16.2.4) |
| 480 | `vault.sub_kinds.registry.reflection_packet_descriptor.v1` | `section_16_reflection_packet.md#§16.9` | interface-contract | reflection_packet | SUB_KIND_REGISTRY["reflection_packet"] descriptor — **DORMANT at v0.1 hook per OQ-2 (a); registers at v0.2 first wave compound LOCK** |
| 481 | `vault.sub_kinds.reflection_packet.post_init_invariants.v1` | `pipeline/vault/sub_kinds/reflection_packets.py` | interface-contract | reflection_packet | 21 `__post_init__` invariants per §16.2.3 (length/grammar/type/closed-set/signature) — LIVE scaffold at v0.1 hook for dataclass mechanics + canonical-codec round-trip; semantic invariants under predicate-body NotImplementedError until v0.2 first wave |
| 482 | `vault.policy.reflection_packet.cedar.org_isolation.v1` | `pipeline/vault/policies/reflection_packet.cedar` | interface-contract | reflection_packet | Cedar default-permit extension for `sub_kind == "reflection_packet"` Law 3 isolation rule (placeholder at v0.1 hook; flips to enforcing at v0.2 first wave) |
| 483 | `vault.policy.reflection_packet.cedar.signature_required.v1` | `pipeline/vault/policies/reflection_packet.cedar` | interface-contract | reflection_packet | Cedar rule: outcome.status non-PENDING REQUIRES operator_signature_ed25519 (placeholder; lives at predicate-body layer F-PACKET-OPERATOR-SIGNATURE-MISSING at v0.2 first wave) |
| 484 | `vault.policy.reflection_packet.cedar.producer_authorization.v1` | `pipeline/vault/policies/reflection_packet.cedar` | interface-contract | reflection_packet | Cedar rule: `emitted_by_seat` ∈ closed producer registry set (placeholder; lives at predicate-body layer F-PACKET-PRODUCER-UNAUTHORIZED at v0.2 first wave) |
| 485 | `reflection_packet.signing.producer_ed25519.v1` | `section_16_reflection_packet.md#§16.5` | interface-contract | reflection_packet | producer-seat Ed25519 signing protocol; white-glove-pinned pubkey verification per v7.0.7 §6.1 pattern; canonical-bytes-must-include `cycle_id` + `packet_id` + `classification_register_version` (RT-04/RT-05 closure boundary) |
| 486 | `reflection_packet.signing.operator_ed25519.v1` | `section_16_reflection_packet.md#§16.5` | interface-contract | reflection_packet | operator Ed25519 attestation on outcome-bearing packets per §16.3 emit+backfill discipline; pubkey already pinned per v7.0.7 classification-register signature |

**Failure codes (rows 487-505) — explode-per-code pattern per §10/§11/§12/§13/§14/§15/§17 precedent:**

| Row | primitive_id | defined_at | kind | seat_owner | Parent / sub-tags |
|---|---|---|---|---|---|
| 487 | `logician.failure_code.F-PACKET-INSTANCE-LEAK.v1` | `section_04_v2_x_y_packet_amendment.md#§2 row 1` | failure-code | reflection_packet | BINDING (NotImplementedError) — PRE-emission. Sub-tags `.client_name_present`, `.funder_specific_with_client`, `.ner_entity_match`, `.unicode_homoglyph`, `.zwj_obfuscation`. |
| 488 | `logician.failure_code.F-PACKET-CROSS-ORG-LEAK.v1` | `section_04_v2_x_y_packet_amendment.md#§2 row 2` | failure-code | reflection_packet | BINDING (NotImplementedError) — PRE-emission + PRE-load. Sub-tags `.path_outside_org`, `.symlink_escape`, `.span_org_slug_mismatch` (per RT-09 fold-in). |
| 489 | `logician.failure_code.F-PACKET-FABRICATION.v1` | `section_04_v2_x_y_packet_amendment.md#§2 row 3` | failure-code | reflection_packet | BINDING (NotImplementedError) — POST-emission + POST-load. Sub-tags `.gate_count_mismatch`, `.score_mismatch`, `.span_id_unresolvable`, `.timing_mismatch`, `.classification_register_version_mismatch`. |
| 490 | `logician.failure_code.F-PACKET-CLASS-SLOT-LEAK.v1` | `section_04_v2_x_y_packet_amendment.md#§2 row 4` | failure-code | reflection_packet | BINDING (NotImplementedError) — PRE-emission. Mirrors F-CLASS-SLOT-ID-NON-OPAQUE from v7.0.7. |
| 491 | `logician.failure_code.F-PACKET-CLASS-MISLABEL.v1` | `section_04_v2_x_y_packet_amendment.md#§2 row 5` | failure-code | reflection_packet | BINDING (NotImplementedError) — PRE-emission. Sub-tags `.register_signature_invalid`, `.register_version_drift`, `.confidential_field_in_shareable_packet`. |
| 492 | `logician.failure_code.F-PACKET-EVAL-ONLY-GROUNDED.v1` | `section_04_v2_x_y_packet_amendment.md#§2 row 6` | failure-code | reflection_packet | BINDING (NotImplementedError) — PRE-emission. Sibling at artifact-validity layer to F-REFLECTION-EVAL-ONLY-GROUNDED. |
| 493 | `logician.failure_code.F-PACKET-PREMATURE-GENERALIZATION.v1` | `section_04_v2_x_y_packet_amendment.md#§2 row 7` | failure-code | reflection_packet | BINDING (NotImplementedError) — PRE-emission. Sub-tag `.frequency_one_no_severity`. |
| 494 | `logician.failure_code.F-PACKET-SPAN-PROVENANCE-MISSING.v1` | `section_04_v2_x_y_packet_amendment.md#§2 row 8` | failure-code | reflection_packet | BINDING (NotImplementedError) — PRE-emission. **SIBLING to F-WPFA-SPAN-PROVENANCE-MISSING at §0.5 v19; RESOLVES §17 v1 §6.5 forward-reference at this LOCK.** Sub-tags `.no_trace_id`, `.trace_id_unresolvable_in_logfire`, `.claim_key_unmapped`, `.span_id_from_different_cycle` (per RT-08 fold-in). |
| 495 | `logician.failure_code.F-PACKET-RETRIEVAL-CORRUPTION.v1` | `section_04_v2_x_y_packet_amendment.md#§2 row 9` | failure-code | reflection_packet | BINDING (NotImplementedError) — PRE-load (Consumer C). Sub-tags `.high_entropy_burst`, `.optimized_trigger_match`, `.embedding_anomaly_detected`. |
| 496 | `logician.failure_code.F-PACKET-MEMORY-INJECTION.v1` | `section_04_v2_x_y_packet_amendment.md#§2 row 10` | failure-code | reflection_packet | BINDING (NotImplementedError) — PRE-emission. Sub-tags `.injection_pattern_regex`, `.unicode_normalized_match`, `.classifier_score_above_threshold`. |
| 497 | `logician.failure_code.F-PACKET-SCHEMA-DRIFT.v1` | `section_04_v2_x_y_packet_amendment.md#§2 row 11` | failure-code | reflection_packet | BINDING (NotImplementedError; advisory-only at v0.1 hook per OQ-5a) — PRE-load. Sub-tags `.unknown_schema_version`, `.required_field_missing`, `.deprecated_field_present`. |
| 498 | `logician.failure_code.F-PACKET-CADENCE-VIOLATION.v1` | `section_04_v2_x_y_packet_amendment.md#§2 row 12` | failure-code | reflection_packet | BINDING (NotImplementedError) — PRE-emission. Sub-tags `.no_cycle_close_marker`, `.uploader_not_staged`, `.partial_council_pass`, `.packet_id_collision` (per Cycle 2 RT-C2-01 fold-in). |
| 499 | `logician.failure_code.F-PACKET-SIGNATURE-INVALID.v1` | `section_04_v2_x_y_packet_amendment.md#§2 row 13` | failure-code | reflection_packet | BINDING (NotImplementedError) — PRE-load. Mirrors v7.0.4-M1 §2 KFR canonical-signature-invalid byte-for-byte; producer-pubkey resolved from white-glove-pinned registry (NOT from packet `emitted_by_seat` per RT-10 fold-in). |
| 500 | `logician.failure_code.F-PACKET-OPERATOR-SIGNATURE-MISSING.v1` | `section_04_v2_x_y_packet_amendment.md#§2 row 14` | failure-code | reflection_packet | BINDING (NotImplementedError) — PRE-load (Consumer B + C). Sub-tag `.signature_present_for_pending` per Cycle 2 RT-C2-02 fold-in (defensive symmetry — Packet 1 PENDING forbids non-None operator signature). |
| 501 | `logician.failure_code.F-PACKET-OPERATOR-SIGNATURE-INVALID.v1` | `section_04_v2_x_y_packet_amendment.md#§2 row 15` | failure-code | reflection_packet | BINDING (NotImplementedError) — PRE-load. |
| 502 | `logician.failure_code.F-PACKET-CYCLE-ID-UNRESOLVABLE.v1` | `section_04_v2_x_y_packet_amendment.md#§2 row 16` | failure-code | reflection_packet | BINDING (NotImplementedError) — PRE-emission. |
| 503 | `logician.failure_code.F-PACKET-OUTCOME-EVIDENCE-MISSING.v1` | `section_04_v2_x_y_packet_amendment.md#§2 row 17` | failure-code | reflection_packet | BINDING (NotImplementedError) — PRE-emission + PRE-load. |
| 504 | `logician.failure_code.F-PACKET-PRODUCER-UNAUTHORIZED.v1` | `section_04_v2_x_y_packet_amendment.md#§2 row 18` | failure-code | reflection_packet | BINDING (NotImplementedError) — PRE-emission. v0.1 producer_registry = `frozenset({"archivist.reflection_submode"})`. |
| 505 | `logician.failure_code.F-PACKET-COVERAGE-INCOMPLETE.v1` | `section_04_v2_x_y_packet_amendment.md#§2 row 19` | failure-code | reflection_packet | BINDING (**LIVE body**) — META PRE-cycle. Dormant-binding lever per L-006; analog of F-CLASS-COVERAGE-INCOMPLETE + F-REFLECTION-COVERAGE-INCOMPLETE row 404. **F-PACKET-* EXCLUDED from F-CLASS-COVERAGE-INCOMPLETE META gate per OQ-6-style isolation precedent (§17 WPFA row 207 + §2 v7.5 FG row 213).** |

**Runtime-live total at this LOCK: 505 rows** (470 + 35 new rows = 505).

# Amendment §B — F-CIC-CLC-COUPLING-VIOLATION-class regression scope extension

F-CIC-CLC-COUPLING-VIOLATION-class regression test runs at LOCK ceremony per Path B naming reconciliation §5 + §16 v1 §16.7 + §4 v2.x.y §6:

- F-PACKET-* codes (rows 487-505) belong only to §16 Reflection Packet (seat_owner: "reflection_packet").
- F-WPFA-* codes (rows 434-445 in §0.5 v19) belong only to §17 WPFA.
- F-REFLECTION-* codes (rows 397-413 in §0.5 v18) belong only to §15 Archivist sub-mode + sub-tag extensions on F-ARCHIVIST-*.
- F-ARCHIVIST-* codes (rows 299-303 in §0.5 v13) belong only to §15 Archivist proper.
- F-FG-* codes (rows 457-464 in §0.5 v20) belong only to §2 v7.5 FG.
- F-CLASS-* codes (rows 305-348 in §0.5 v14) belong only to §4 v2.x.
- No F-* code crosses seat ownership. AST-lint enforces at module-import time (§4 v2.x.y §6).

# Amendment §C — seat_owner attribute on every row

Per the §0.5 v20 RT-19 / RT-C2-09 closure (FG amendment landed the `seat_owner` row attribute as new §0.5 invariant), every row in this amendment carries `seat_owner: "reflection_packet"`. F-INDEX-STALE PRE-gate at compound commit verifies:

- All 35 new rows present in runtime-live index.
- All 35 new rows carry `seat_owner: "reflection_packet"`.
- Deviation triggers F-INDEX-STALE with sub-tag `.seat_owner_mismatch`.

# Amendment §D — vocabulary preservation

NO new vocabulary kind. Every row's `primitive_kind` resolves against the v5 + v6 + v19 closed vocabulary (marker / schema / interface-contract / failure-code / ast-lint). The spec card §5 proposed `invariant-cluster` / `signing-protocol` / `retention-policy` as new kinds, but Cycle 1 review surfaced that these collapse cleanly to:

- Spec card "invariant-cluster" rows → row 481 (`vault.sub_kinds.reflection_packet.post_init_invariants.v1`) under existing `interface-contract` kind (precedent: WPFA §0.5 v19 row 421 `vault.sub_kinds.cycle_receipt.canonical_codec.v1` under interface-contract).
- Spec card "signing-protocol" rows → rows 485-486 under existing `interface-contract` kind (precedent: WPFA §0.5 v19 row 428 `wpfa.coefficient_registry.sn_llc_signature_verify.v1` under interface-contract).
- Spec card "retention-policy" row → §16 v1 §16.6 retention discipline is a documentary block in the section text; no §0.5 row needed (the indefinite-retention discipline is enforced by the absence of pruning code paths at v0.1 hook + audited operator-driven pruning at v0.2 first wave — no primitive registry needed).

This collapse is the Cycle 1 fold-in disposition per row-170. Total row count drops from spec card's 25 to actual 35 (because the additional schema rows for 6 nested shapes + the additional interface-contract rows for the 3 Cedar rules + 2 signing protocols + 1 SUB_KIND_REGISTRY descriptor brought the actual count up — Cycle 1 surfaced the spec card's row count was undershoot, not overshoot).

# Amendment §E — Compound-LOCK ceremony

The §16 v1 + §4 v2.x.y + this §0.5 v22 amendment LOCK atomically at the same `lock_timestamp_utc`. F-INDEX-STALE PRE-gate fires at commit time per §6.2 order 3; all 35 new rows AND seat_owner attribute consistency AND F-CIC-CLC-COUPLING-VIOLATION regression PASS must hold or the compound commit fails closed.

# Amendment §F — Audit trail

- Spec card: `pipeline/planning/reflection_packet_dispatch_spec_2026-05-11.md`
- Thesis dispatch packet: `pipeline/handoffs/ws_reflection_packet_handoff_2026-05-11.md`
- Audit trail: `pipeline/validation/reflection_packet_thesis_2026-05-11/`

---

**Filed:** 2026-05-15. LOCKED via L-005 strict two-cycle Thesis with FULL LIVE CROSS-FAMILY rigor. Compound paired-commit sibling 3/3 with §16 v1 + §4 v2.x.y. 35 §0.5 v22 rows promoted PARENT_UNLOCKED → STABLE atomically. Runtime-live row count: 505. Seat_owner attribute applied to every row.
