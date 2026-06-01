---
title: §0.5 Blueprint Interface Index — v7.0.10 three-posture routing model paired-commit amendment (v21 — companion to architecture v7.0.10 LOCKED 2026-05-11)
filed: 2026-05-15
operator: Josh
status: paired-commit companion to architecture v7.0.10 LOCKED 2026-05-11 (row 215). v7.0.10 was the SUBSTANTIVE architectural LOCK; this §0.5 paired-commit registers the four new F-CLASS-* primitives (`F-CLASS-POSTURE-MID-CYCLE-CHANGE`, `F-CLASS-SPLIT-CONTEXT-ALLOWLIST`, `F-CLASS-SPLIT-CONTEXT-LEAK`, `F-CLASS-HEAVY-JUDGE-CLOUD-DOWNLOAD`) into the Index + records the sub-tag extensions on F-CLASS-REGISTER-* gates for the new `selected_posture` field per v7.0.10 §1.4. No new schema rows / interface-contract rows / vocabulary kinds at this amendment — pure failure-code row append + sub-tag extension recording.
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
  - pipeline/blueprint/v0.1/section_00_5_section_11_v1_1_amendment.md                              # §0.5 v19 paired-commit 2026-05-11 (narrow-corrective; rows 414-415)
  - pipeline/blueprint/v0.1/section_00_5_section_funding_goal_amendment.md                         # §0.5 v20 LOCKED 2026-05-11 — rows 446-470; `seat_owner` row attribute extension landed (RT-19 closure)
  - pipeline/blueprint/v0.1/section_00_5_section_16_packet_amendment.md                            # §0.5 v22 LOCKED 2026-05-15 — rows 471-505 (Reflection Packet compound triple)
  - pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md                                   # architecture v7.0.10 LOCKED 2026-05-11 (row 215; this §0.5 amendment is the deferred paired-commit companion sweep landing 4 days after the architectural LOCK)
companion_architecture_amendment: pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md  # paired-commit deferred-sweep companion per v7.0.10 LOCK ceremony hand-back
row_delta: prior runtime-live total = 505 rows (after §0.5 v22 §16 packet LOCK at row 505). **§0.5 v21 amendment claims rows 506-509 (4 rows: four new F-CLASS-* failure-code primitives).** Every row carries `seat_owner: "f_class"` per RT-19 extension landed at §0.5 v20. Existing F-CLASS-SLOT-ID-NON-OPAQUE (row 309 in §0.5 v14) + F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED (row 308 in §0.5 v14) — disposition_at_v7_0_10 sub-tag extension recorded; no new top-level row for the disposition change. Existing F-CLASS-REGISTER-UNSIGNED (row 305 in §0.5 v14) + F-CLASS-REGISTER-SIGNATURE-INVALID (row 307 in §0.5 v14) + F-CLASS-REGISTER-HASH-MISMATCH (row 308 in §0.5 v14) — sub-tag extensions for `.posture_unsigned` / `.posture_invalid` / `.posture_hash_mismatch` recorded per v7.0.10 §1.4 + §4 v2.x amendment §4.3.7. New runtime-live total at this LOCK = 509.
kind_of_amendment: row-append (4 failure-code rows) + sub-tag-extension recording (no new top-level rows; sub-tags noted under existing-row ownership). NO new vocabulary kind — every row's `primitive_kind` resolves against the v5 + v6 + v19 closed vocabulary (marker / schema / interface-contract / failure-code / ast-lint). NO new schema / interface-contract row.
numbering_note: this amendment is **v21** in the §0.5 sequence. Per project memory `project_blueprint_section_16_reflection_packet_v1_locked.md`: "§0.5 v22 not v21 (collision avoidance with v7.0.10's in-place v21 edits)" — §16 packet amendment was promoted from v21 → v22 at LOCK so that v7.0.10's deferred §0.5 paired-commit could occupy the v21 slot. The §16 amendment file title-line `(v21 — LOCKED 2026-05-15)` is a leftover from before the bump; its body row_delta line says "**§0.5 v22 amendment claims rows 471-505**" — that is the canonical version-numbering. v21 is THIS file.
seat_owner_attribute: every row in this amendment carries `seat_owner: "f_class"` per RT-19 extension (landed at §0.5 v20 FG amendment). F-INDEX-STALE PRE-gate verifies seat_owner consistency.
cross_family_posture: deferred companion sweep (not a substantive LOCK); architecture v7.0.10 itself underwent L-005 strict two-cycle FULL LIVE CROSS-FAMILY rigor at the substantive LOCK (audit trail at `pipeline/validation/v7_0_10_thesis_2026-05-11/`). This §0.5 paired-commit is the documentation-and-row-allocation sweep authorized by the architectural LOCK's pending-companion-edits list (§companion_files_pending_edit_at_LOCK in the amendment header).
---

# Amendment intent

Architecture v7.0.10 LOCKED 2026-05-11 (row 215) deprecated the v7.0.7 four-posture-implicit framing in favor of an explicit three-posture customer-facing vocabulary (Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign). The architectural LOCK introduced four new F-CLASS-* primitives + two repurposed-as-defense-in-depth dispositions + three sub-tag extensions on existing F-CLASS-REGISTER-* gates. The LOCK ceremony's companion_files_pending list named this §0.5 paired-commit as one of the deferred-sweep deliverables.

This file is the paired-commit. It registers:

1. Four new failure-code primitives (rows 506-509) per v7.0.10 §5.3 + §4 v2.x §4.4 (the §4 v2.x amendment companion update).
2. Sub-tag extensions on existing F-CLASS-REGISTER-* rows (305, 307, 308 in §0.5 v14) per v7.0.10 §1.4 + §4 v2.x amendment §4.3.7 — `.posture_unsigned` / `.posture_invalid` / `.posture_hash_mismatch`.
3. Disposition_at_v7_0_10 sub-tag extension on the two defense-in-depth-repurposed primitives (rows 308-309 in §0.5 v14: `F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED` + `F-CLASS-SLOT-ID-NON-OPAQUE`) — broadened regex `\[SLOT_[^\]]*\]` + defense-in-depth role per v7.0.10 §2.2 + §5.2 + §4 v2.x amendment §4.3.6.

No new schema rows. No new interface-contract rows. No new vocabulary kind. No new section-anchor marker (the existing architecture v7 anchor at §0.5.8.11 covers v7.0.x amendments by inheritance per the §0.5.8 v4 architecture-rows aggregation pattern).

# Amendment §A — row append (rows 506-509)

All rows enter §0.5 at `stability_tier = "STABLE"` at architecture v7.0.10 LOCK (the architectural LOCK 2026-05-11 row 215 is the parent; no PARENT_UNLOCKED transit).

**Failure codes (rows 506-509) — explode-per-code pattern per §10 / §11 / §12 / §13 / §14 / §15 / §16 / §17 precedent:**

| Row | primitive_id | defined_at | kind | seat_owner | Parent / sub-tags |
|---|---|---|---|---|---|
| 506 | `logician.failure_code.F-CLASS-POSTURE-MID-CYCLE-CHANGE.v1` | `section_04_v2_x_amendment.md#§4.4 + §4.4.1` | failure-code | f_class | BINDING (NotImplementedError signature-stub at v7.0.10 LOCK; predicate body realized at v0.2 first-wave Code phase per dormant-binding pattern). PRE per-cycle gate. Atomically locks `posture_lock_version` Vault field at `cycle_started_at_utc` via §2 Vault topology `start_editing_transaction` / `commit_editing_transaction` primitives (LIVE per §2 v7.1 row 35). Fires inclusive-on-both-ends: any posture-change timestamp `t` where `cycle_started_at_utc ≤ t ≤ cycle_ended_at_utc` fail-closes. Bypass: M13 audited (HIGH admin-risk). Cycle 1 RT-4 closure; Cycle 2 RT-C2-2 closure. |
| 507 | `logician.failure_code.F-CLASS-SPLIT-CONTEXT-ALLOWLIST.v1` | `section_04_v2_x_amendment.md#§4.4 + §4.4.2` | failure-code | f_class | BINDING (NotImplementedError signature-stub at v7.0.10 LOCK; predicate body realized at v0.2 first-wave Code phase). PRE per-call outbound-boundary gate. Closed-set check (not open-set classification check) against operator-signed allow-list at `orgs/<slug>/vault/classification/split_context_allowlist.yaml`. Allow-list extension requires dual-sign discipline (operator Ed25519 + second-tier; v0.1 second-tier = SN-LLC publisher signature on extension diff under same router-template trust mechanism). Bypass: NO M13 (structural per §1.3 boundary rule). Cycle 2 RT-C2-1 closure (allow-list extension abuse → normalize-and-applicant-fact-scan at write time + dual-sign). |
| 508 | `logician.failure_code.F-CLASS-SPLIT-CONTEXT-LEAK.v1` | `section_04_v2_x_amendment.md#§4.4 + §4.4.3` | failure-code | f_class | BINDING (NotImplementedError signature-stub at v7.0.10 LOCK; predicate body realized at v0.2 first-wave Code phase). PRE per-call outbound-boundary gate. Pre-cloud-route applicant-fact scan under Split-Context Hybrid posture for: applicant's legal name + EIN + address strings + KFR production-metric numerics + `PROJECT_CONTEXT.partnerships` names. Match → fail-closed with admin-risk ledger entry HIGH severity. Catches attackers pushing applicant-fact text into Public + Shareable field anchors. Bypass: M13 audited (HIGH admin-risk). Cycle 1 RT-2 closure. |
| 509 | `logician.failure_code.F-CLASS-HEAVY-JUDGE-CLOUD-DOWNLOAD.v1` | `section_04_v2_x_amendment.md#§4.4 + §4.4.4` | failure-code | f_class | BINDING (NotImplementedError signature-stub at v7.0.10 LOCK; predicate body realized at v0.2 first-wave Code phase). PRE per-swap gate. 200B-class heavy-Judge binary MUST be pre-loaded on Golden Quill at white-glove (Golden-Image-build-time-signed manifest). Local-execution-pointer-switch only — no network fetch, no remote download, no cloud-routed binary transfer, no background-sync service. Alternative-update-channel ban: any model-sync service, background daemon, or external update channel mutating heavy-Judge binary outside operator-attested router-template flow → fail-closed. Bypass: NO M13 (structural — Golden Image manifest is the only trust path). Cycle 1 RT-10 closure + Cycle 2 RT-10-PARTIAL background-sync surface closure. |

**Runtime-live total at this LOCK: 509 rows** (505 + 4 new rows = 509).

# Amendment §B — sub-tag extension recording (no new top-level rows)

Per v7.0.10 §1.4 + §4 v2.x amendment §4.3.7, the three F-CLASS-REGISTER-* gates extend their predicate signature + canonical-hash scope to include the new top-level `selected_posture` field on the operator-signed register. The sub-tag-extension precedent matches §4 v2.x.1 row 198 (R-ARCHIVIST-NO-CANONICAL-MUTATE enumeration extension under existing F-ARCHIVIST-AUTO-APPLY-ATTEMPTED ownership — no new top-level row, named drift-test bindings + AST-lint enforcement under existing-row ownership).

| Existing row | primitive_id | New sub-tag (added at v7.0.10 paired-commit) | Drift-test binding |
|---|---|---|---|
| 305 (§0.5 v14) | `logician.failure_code.F-CLASS-REGISTER-UNSIGNED.v1` | `.posture_unsigned` — top-level `selected_posture` field present but operator Ed25519 signature does not cover the field | `tests/logician/gates/test_f_class_register.py::test_unsigned_posture_unsigned_fails_closed` |
| 307 (§0.5 v14) | `logician.failure_code.F-CLASS-REGISTER-SIGNATURE-INVALID.v1` | `.posture_invalid` — signature verifies against field-classifications block but not against extended block including `selected_posture` | `tests/logician/gates/test_f_class_register.py::test_signature_invalid_posture_invalid_fails_closed` |
| 308 (§0.5 v14) | `logician.failure_code.F-CLASS-REGISTER-HASH-MISMATCH.v1` | `.posture_hash_mismatch` — recomputed hash chain over extended block (including `selected_posture`) does not match on-register hash | `tests/logician/gates/test_f_class_register.py::test_hash_mismatch_posture_hash_mismatch_fails_closed` |

**AST-lint binding (R-CLASS-POSTURE-FIELD-COVERAGE).** Registered in `pipeline/linting/ast_lint.py::DEFAULT_RULES`. Confirms every register-signature gate inspects the posture field. Realization at v7.0.10 paired-commit + tests/regression at the same commit.

# Amendment §C — disposition_at_v7_0_10 sub-tag extension (defense-in-depth-repurposed primitives)

Per v7.0.10 §2.2 + §5.2 + §4 v2.x amendment §4.3.6, the two F-CLASS-* primitives policing the opaque-slot discipline at v7.0.7 are repurposed as defense-in-depth gates. The repurposing is a disposition change recorded as a sub-tag-extension on the existing rows; no top-level row change.

| Existing row | primitive_id | Disposition_at_v7_0_10 |
|---|---|---|
| 309 (§0.5 v14) | `logician.failure_code.F-CLASS-SLOT-ID-NON-OPAQUE.v1` | **DEFENSE-IN-DEPTH.** No legitimate trigger path under any v7.0.10 posture (no posture emits slot tokens into cloud routing). Firing = bug or attack. Regex broadened from `\[SLOT_(\d+)\]` to `\[SLOT_[^\]]*\]` at LOCK. HARD_BLOCK / no M13 bypass retained. AST-lint binding: `R-V0-10-NO-SLOT-TOKEN-EMISSION` (registered in `pipeline/linting/ast_lint.py::DEFAULT_RULES`) — Layer 1 of three-layer defense; fails any module-load that constructs a literal `[SLOT_*]` token destined for a cloud-routed prompt. |
| 308 (§0.5 v14) | `logician.failure_code.F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED.v1` | **DEFENSE-IN-DEPTH.** No legitimate trigger path. Firing = bug or attack. POST-call outbound-boundary scan extended to fail-closed on any `\[SLOT_[^\]]*\]` pattern at any registered anchor or unregistered position. P0 / M13 audited disposition retained. |

# Amendment §D — F-CIC-CLC-COUPLING-VIOLATION-class regression scope extension

F-CIC-CLC-COUPLING-VIOLATION-class regression test runs at v7.0.10 paired-commit per Path B naming reconciliation:

- F-CLASS-* codes (rows 305-348 in §0.5 v14 + rows 506-509 in this amendment) belong only to v7.0.7 + v7.0.10 architecture-layer classification routing (seat_owner: "f_class").
- F-WPFA-* codes (rows 434-445 in §0.5 v19) belong only to §17 WPFA.
- F-REFLECTION-* codes (rows 397-413 in §0.5 v18) belong only to §15 Archivist sub-mode.
- F-ARCHIVIST-* codes (rows 299-303 in §0.5 v13) belong only to §15 Archivist proper.
- F-FG-* codes (rows 457-464 in §0.5 v20) belong only to §2 v7.5 FG.
- F-PACKET-* codes (rows 487-505 in §0.5 v22) belong only to §16 Reflection Packet.

No F-* code crosses seat ownership. AST-lint enforces at module-import time.

# Amendment §E — seat_owner attribute on every row

Per the §0.5 v20 RT-19 / RT-C2-09 closure, every row in this amendment carries `seat_owner: "f_class"`. F-INDEX-STALE PRE-gate at compound commit verifies:

- All 4 new rows (506-509) present in runtime-live index.
- All 4 new rows carry `seat_owner: "f_class"`.
- Sub-tag extensions on rows 305 / 307 / 308 / 309 recorded under existing-row ownership (no seat_owner change on existing rows).
- Deviation triggers F-INDEX-STALE with sub-tag `.seat_owner_mismatch`.

# Amendment §F — vocabulary preservation

NO new vocabulary kind. Every row's `primitive_kind` resolves against the v5 + v6 + v19 closed vocabulary (marker / schema / interface-contract / failure-code / ast-lint). The four new rows are all `kind: failure-code`; the sub-tag extensions inherit the parent row's kind.

# Amendment §G — paired-commit discipline summary

This §0.5 v21 amendment is the deferred-sweep companion to architecture v7.0.10 LOCKED 2026-05-11 (row 215). v7.0.10's substantive LOCK underwent the full L-005 strict two-cycle FULL LIVE CROSS-FAMILY rigor (Editor=Llama-3.3-70B/Groq + Judge=Gemini-2.5-Pro/Google + Red Team=GPT-OSS-120B/Groq via openclaw bridge — audit trail at `pipeline/validation/v7_0_10_thesis_2026-05-11/`). This paired-commit is the row-allocation + documentation sweep authorized by the architectural LOCK's companion_files_pending list; no new substantive design surface is introduced.

Master `section_00_5_interface_index_locked.md` remains LOCKED v5 on-disk; this amendment file is runtime-live as part of the §0.5 v6-v22 amendment chain. Future master re-author folds all v6-v22 amendment files (including this v21) into the master.
