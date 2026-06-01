---
title: Active Blueprint Index — current vs. superseded §-blueprints
filed: 2026-05-17
basis: pipeline/engineering/lock_history.v1.jsonl through logical row 279 (physical line 283)
posture: SIDECAR. This file does not modify any LOCKed amendment. It points at them. The amendment files themselves carry their own canonical bytes + signatures and are untouched here.
source_of_truth_rule: when this index disagrees with lock_history.v1.jsonl, the lock_history is canonical. Refresh this sidecar; do not touch the ledger.
companion: ../../../PROJECT_STATUS.md · ../../../RUNTIME_MATURITY_MATRIX.md
---

# Active Blueprint Index (§-numbered)

For each §-blueprint section the **head** row is the current LOCKed amendment that supersedes everything beneath it; rows below it are the chain backward, each annotated `(superseded by …)`. The `lock_history` column cites the logical row in `pipeline/engineering/lock_history.v1.jsonl` that wrote the LOCK; rows marked `(pre-row-numbering)` LOCKed before the discipline of explicit `row` field started at row 101 (those LOCKs are recoverable by `lock_timestamp_utc` + `blueprint_section`).

The `also-see` column points at the §0.5 paired-commit row when applicable. §0.5 is the canonical signed governance ledger for the blueprint amendment surface; every blueprint LOCK from §0.5 v5 forward has a paired-commit twin row in §0.5.

---

## §0.5 — Blueprint Interface Index (signed governance ledger)

§0.5 is the canonical paired-commit twin of every other §-blueprint amendment. Its version chain is dense; grouped below as **baseline → chunk through v32**.

### §0.5 baseline (v4 → v18)

| Version | Path | LOCK evidence | Notes |
|---|---|---|---|
| **v4 baseline** | `section_00_5_interface_index.md` | pre-row-numbering 2026-04-15..18 (preserved at `section_00_5_interface_index.v1_preserved_2026-04-18.json` + `section_00_5_interface_index_locked_v2_2026-04-18.md`) | original interface index; superseded by v5+ chain |
| v5 | `section_00_5_v5_amendment.md` | pre-row-numbering | superseded by later v-chain |
| v7.0.10 | `section_00_5_v7_0_10_amendment.md` | pre-row-numbering | architecture v7.0.10 paired-commit (later folded forward) |
| v18 | `section_00_5_section_15_reflection_amendment.md` | row 204 (2026-05-10) | §15 reflection amendment paired-commit (superseded forward) |

### §0.5 v19 → v32 (active chain)

| Version | Path | LOCK row | Paired with |
|---|---|---|---|
| v19 | `section_00_5_section_17_wpfa_amendment.md` | row 208 (2026-05-11) | §17 WPFA v1 (row 207) |
| v19 (§11) | `section_00_5_section_11_v1_1_amendment.md` | row 210 (2026-05-11) | §11 v1.1 (row 209) |
| v20 | `section_00_5_section_funding_goal_amendment.md` | row 214 (2026-05-11) | §2 v7.5 + §3 v6 + §4 v2.x.4 funding-goal stack |
| v22 | `section_00_5_section_16_packet_amendment.md` | row 218 (2026-05-15) | §16 v1 + §4 v2.x.y packet (rows 216 + 217) |
| v23 | `section_00_5_section_04_v2_x_3_amendment.md` | row 220 (2026-05-15) | §4 v2.x.3 (row 219) |
| v24 | `section_00_5_section_16_v1_1_amendment.md` | row 225 (2026-05-15) | §16 v1.1 (row 221) |
| v25 | `section_00_5_section_18_cards_wave_1_paired_commit_amendment.md` | row 228 (2026-05-15) | Cards Wave 1 (rows 226 + 227) |
| v26 | `section_00_5_section_18_v1_1_amendment.md` | row 230 (2026-05-16) | §18 v1.1 (row 229) |
| v27 | `section_00_5_section_04_v2_x_5_amendment.md` | row 233 (2026-05-16) | §4 v2.x.5 provider boundary (row 232) |
| v28 (apolitical) | `section_00_5_apolitical_dialect_amendment.md` | row 237 (2026-05-16T14:00Z) | architecture v7.0.12 + §4 v2.x apolitical_dialect (rows 234 + 236) |
| v28 (§4 v2.x.6) | `section_00_5_section_04_v2_x_6_amendment.md` | row 235 (2026-05-16T16:30Z) — **see ledger-integrity note below** | §4 v2.x.6 router-dedup (row 234 16:30Z) |
| v29 | `section_00_5_cards_wave_2_amendment.md` | row 262 (2026-05-16) | Cards Wave 2 stack (rows 250–261) |
| **v30** | `section_00_5_section_18_11_v1_1_amendment.md` | **row 271 (2026-05-17 / OD-D)** | §18.11 v1.1 (row 270) |
| **v31** | `section_00_5_section_04_v2_x_7_amendment.md` | **row 273 (2026-05-17 / OD-C)** | §4 v2.x.7 (row 272) |
| **v32 (HEAD)** | `section_00_5_section_18_6_v2_amendment.md` | **row 275 (2026-05-17 / OD-E)** | §18.6 v2 dual-track (row 274 + recovery row 279) |

**Ledger-integrity note (rows 234/235 collision).** The lock_history carries row 234 + row 235 at two distinct `lock_timestamp_utc` values (`2026-05-16T14:00:00Z` for v7.0.12 / §18 v1.2, and `2026-05-16T16:30:00Z` for §4 v2.x.6 / §0.5 v28). Flagged in `daily_logs/2026-05-17.md` as out-of-scope for the §4 v2.x.6 runtime companion session. Operator triage pending (cleanup plan v1.1 §"v2.x.7 follow-on candidates" item 5).

### Other §0.5 historical / scaffold files (not in the v-chain head)

- `section_00_5_interface_index.v1.json` — original v1 sidecar (preserved at v1_preserved_2026-04-18 alongside)
- `section_00_5_interface_index.v3.json` + `section_00_5_interface_index_v3_2026-04-18.md` — v3 snapshot 2026-04-18
- `section_00_5_arch04_ast_lint_amendment.md` — architecture AST-lint paired-commit (pre-row-numbering)
- `section_00_5_cedar_policy_kinds_amendment.md` — Cedar policy kinds paired-commit
- `section_00_5_section_02_v7_2_operational_amendment.md` — §2 v7.2 paired-commit
- `section_00_5_section_04_v2_3_privacy_router_amendment.md` — §4 v2.3 paired-commit
- `section_00_5_section_04_v2_4_v2_5_canary_runtime_amendment.md` — §4 v2.4/v2.5 paired-commit
- `section_00_5_section_04_v2_x_1_amendment.md` — §4 v2.x.1 paired-commit
- `section_00_5_section_04_v2_x_3_amendment.md` — §4 v2.x.3 paired-commit (= v23 head; listed above)
- `section_00_5_section_04_v2_x_amendment.md` — §4 v2.x parent paired-commit
- `section_00_5_section_05_v6_amendment.md` + `section_00_5_section_05_v8_amendment.md` — §5 v6 + v8 paired-commits
- `section_00_5_section_06_operating_envelope_amendment.md` — §6 paired-commit
- `section_00_5_section_07_scribe_amendment.md` — §7 paired-commit
- `section_00_5_section_10_red_team_amendment.md` — §10 paired-commit
- `section_00_5_section_11_intake_amendment.md` — §11 baseline paired-commit (superseded by §0.5 v19 row 210)
- `section_00_5_section_12_uploader_amendment.md` + `section_00_5_section_12_uploader.json` — §12 paired-commit
- `section_00_5_section_13_data_collector_amendment.md` — §13 paired-commit
- `section_00_5_section_14_report_generator_amendment.md` — §14 paired-commit
- `section_00_5_section_15_archivist_amendment.md` — §15 baseline paired-commit
- `section_00_5_section_15_reflection_amendment.md` — §15 reflection paired-commit (= v18 row 204; listed above)
- `section_00_5_section_18_card_amendment.md` — §18 card baseline paired-commit

---

## §1 — Sovereignty Envelope

| Status | Version | Path | LOCK evidence |
|---|---|---|---|
| **HEAD** | v6 (LOCKed-as-a-whole) | `section_1_sovereignty_envelope.md` | multi-row chain ending Round J 2026-04-18; pre-row-numbering |
| superseded | v5 | `section_1_sovereignty_envelope_v5_2026-04-17.md` | preserved 2026-04-17 |

---

## §2 — Vault Topology

| Status | Version | Path | LOCK evidence |
|---|---|---|---|
| **HEAD (active amendment chain)** | v7.x reflection-packet subkind | `section_02_v7_x_reflection_packet_subkind_amendment.md` | row 222 (2026-05-15) |
| amendment | v7.5 funding goal | `section_02_v7_5_funding_goal_amendment.md` | row 211 (2026-05-11) |
| amendment | v7.4 coefficient registry | `section_02_v7_4_coefficient_registry_amendment.md` | row 206 (2026-05-11) |
| amendment | v7.2 operational | `section_02_v7_2_amendment.md` | pre-row-numbering |
| superseded | v7.1 head | `section_02_vault_topology.md` | multi-row chain pre-row-numbering (superseded by v7.2 + later) |
| superseded | v7 (2026-04-18 snapshot) | `section_02_vault_topology_v7_2026-04-18.md` | preserved 2026-04-18 |
| superseded | v4 (2026-04-16 snapshot) | `section_02_vault_topology_v4_2026-04-16.md` | preserved 2026-04-16 |

---

## §3 — Scout

| Status | Version | Path | LOCK evidence |
|---|---|---|---|
| **HEAD (active amendment chain)** | v6 funding goal | `section_03_v6_funding_goal_amendment.md` | row 212 (2026-05-11) |
| companion | v7.0.5 companion | `section_03_v7_0_5_companion.md` | pre-row-numbering (architecture v7.0.5 companion) |
| superseded | v0.1 head | `section_03_scout.md` | multi-row chain rows 101 + pre-row-numbering (superseded by v6 + companion) |

---

## §4 — Logician (the deepest amendment chain in the repo)

| Status | Version | Path | LOCK evidence |
|---|---|---|---|
| **HEAD (v0.1 amendment chain)** | **v2.x.7 card-coupling-value-position** | `section_04_v2_x_7_card_coupling_value_position_amendment.md` | **row 272 (2026-05-17 / OD-C)** |
| amendment | v2.x.6 router-dedup | `section_04_v2_x_6_router_dedup_amendment.md` | row 234 (2026-05-16T16:30Z; see ledger-integrity note above) |
| amendment | v2.x.5 provider boundary | `section_04_v2_x_5_provider_boundary_amendment.md` | row 232 (2026-05-16) |
| amendment | v2.x.4 funding goal | `section_04_v2_x_4_funding_goal_amendment.md` | row 213 (2026-05-11) |
| amendment | v2.x.3 | `section_04_v2_x_3_amendment.md` | row 219 (2026-05-15) |
| amendment | v2.x.z WPFA | `section_04_v2_x_z_wpfa_amendment.md` | row 207 (2026-05-11) |
| amendment | v2.x.y packet | `section_04_v2_x_y_packet_amendment.md` | row 217 (2026-05-15) |
| amendment | v2.x.y.1 packet bodies | `section_04_v2_x_y_1_packet_bodies_amendment.md` | row 223 (2026-05-15) |
| amendment | v2.x apolitical dialect | `section_04_logician_v2_x_apolitical_dialect.md` | row 236 (2026-05-16T14:00Z) |
| amendment | v2.x card hardening | `section_04_logician_v2_x_card_hardening.md` | pre-row-numbering (paired with §18 card LOCK) |
| amendment | v2.x uploader gates | `section_04_v2_x_uploader_gates_amendment.md` | pre-row-numbering (§12 uploader paired) |
| amendment | v2.x.2 | `section_04_logician_v2_x_2_amendment.md` | row 203 (2026-05-10) |
| amendment | v2.x.1 | `section_04_v2_x_1_amendment.md` | pre-row-numbering |
| amendment | v2.x parent | `section_04_v2_x_amendment.md` | pre-row-numbering |
| amendment | v2.7.1 attachment family | `section_04_v2_7_1_attachment_family_amendment.md` | pre-row-numbering |
| amendment | v2.6 deferred scope | `section_04_v2_6_deferred_scope_amendment.md` | pre-row-numbering |
| amendment | v2.4 / v2.5 canary runtime | `section_04_v2_4_v2_5_amendment.md` | pre-row-numbering |
| amendment | v2.3 privacy router | `section_04_v2_3_amendment.md` | pre-row-numbering |
| amendment | v2.2 consolidated | `section_04_v2_2_consolidated_amendment.md` | pre-row-numbering (Waves 1/2/3/4 consolidated; zero-semantic-delta reading-surface roll-up) |
| amendment | v2.2 wave-2 | `section_04_v2_2_wave_2_amendment.md` | pre-row-numbering |
| amendment | v2.2 | `section_04_v2_2_amendment.md` | pre-row-numbering |
| amendment | v2.1.1 | `section_04_v2_1_1_amendment.md` | pre-row-numbering |
| companion | v7.0.5 companion | `section_04_v7_0_5_companion.md` | pre-row-numbering |
| companion | legibility companion | `section_04_legibility_companion.md` | pre-row-numbering |
| superseded | v2.1 head (Logician parent) | `section_04_logician.md` | pre-row-numbering; LOCKed 2026-04-19 (Round-A committee dispatch) — base for the entire v2.x chain |
| superseded | v2 (2026-04-18 snapshot) | `section_04_logician_v2_2026-04-18.md` | preserved 2026-04-18 |
| scaffold | program rule packs scoping draft | `section_04_program_rule_packs_scoping_draft.md` | scaffold; not LOCKed |
| scaffold | v2.7 unresolved primitives | `section_04_v2_7_unresolved_primitives_2026-05-09.md` | scaffold-snapshot 2026-05-09 (folded forward into v2.x amendments) |

---

## §5 — Pipeline Orchestrator

| Status | Version | Path | LOCK evidence |
|---|---|---|---|
| **HEAD (active amendment chain)** | v8 | `section_05_v8_amendment.md` | pre-row-numbering (post-row-101 chain via §0.5 paired-commit) |
| amendment | v7 | `section_05_v7_amendment.md` | pre-row-numbering |
| amendment | v6 | `section_05_v6_amendment.md` | rows 102 + 103 + 104 (2026-04-19 chain) |
| companion | v7.0.5 companion | `section_05_v7_0_5_companion.md` | pre-row-numbering |
| companion | v6.1 seat-output-schema-pin proposal | `section_05_v6_1_seat_output_schema_pin_proposal.md` | proposal; not LOCKed |
| draft | v6 str additions draft | `section_05_v6_str_additions_draft.md` | draft; not LOCKed |
| superseded | v6 head | `section_05_pipeline.md` | row 102 + 103 + 104 (LOCK 2026-04-19; superseded by v7 + v8 amendments) |
| superseded | v3 (2026-04-18 snapshot) | `section_05_pipeline_v3_2026-04-18.md` | preserved 2026-04-18 |

---

## §6 — Operating Envelope

| Status | Version | Path | LOCK evidence |
|---|---|---|---|
| **HEAD** | v1 | `section_06_operating_envelope.md` | pre-row-numbering; §0.5 paired-commit at `section_00_5_section_06_operating_envelope_amendment.md` |

---

## §7 — Scribe

| Status | Version | Path | LOCK evidence |
|---|---|---|---|
| **HEAD** | v1.1.1 | `section_07_scribe.md` | multi-row chain pre-row-numbering; §0.5 paired-commit at `section_00_5_section_07_scribe_amendment.md` |

---

## §10 — Red Team

| Status | Version | Path | LOCK evidence |
|---|---|---|---|
| **HEAD** | v1 | `section_10_red_team.md` | pre-row-numbering; §0.5 paired-commit at `section_00_5_section_10_red_team_amendment.md` |

---

## §11 — Intake

| Status | Version | Path | LOCK evidence |
|---|---|---|---|
| **HEAD (active amendment)** | v1.1 | `section_11_intake_v1_1_amendment.md` | row 209 (2026-05-11); §0.5 v19 paired-commit row 210 |
| superseded | v1 head | `section_11_intake.md` | pre-row-numbering; §0.5 paired-commit at `section_00_5_section_11_intake_amendment.md` (superseded by v1.1) |

---

## §12 — Uploader

| Status | Version | Path | LOCK evidence |
|---|---|---|---|
| **HEAD** | v1 | `section_12_uploader.md` | pre-row-numbering; §0.5 paired-commit at `section_00_5_section_12_uploader_amendment.md` + `section_00_5_section_12_uploader.json` |

---

## §13 — Data Collector *(v0.2-horizon — spec-locked)*

| Status | Version | Path | LOCK evidence |
|---|---|---|---|
| **HEAD** | v1 | `section_13_data_collector.md` | pre-row-numbering; §0.5 paired-commit at `section_00_5_section_13_data_collector_amendment.md` |

---

## §14 — Report Generator *(v0.2-horizon — spec-locked)*

| Status | Version | Path | LOCK evidence |
|---|---|---|---|
| **HEAD** | v1 | `section_14_report_generator.md` | pre-row-numbering; §0.5 paired-commit at `section_00_5_section_14_report_generator_amendment.md` |

---

## §15 — Archivist *(v1.x-horizon — spec-locked)*

| Status | Version | Path | LOCK evidence |
|---|---|---|---|
| **HEAD (active amendment)** | v2.x archivist-reflection | `section_15_v2_x_archivist_reflection_amendment.md` | row 224 (2026-05-15) |
| superseded | v1 head | `section_15_archivist.md` | pre-row-numbering; §0.5 paired-commit at `section_00_5_section_15_archivist_amendment.md` (superseded by v2.x) |

---

## §16 — Reflection Packet *(v0.2-horizon — spec-locked)*

| Status | Version | Path | LOCK evidence |
|---|---|---|---|
| **HEAD (active amendment)** | v1.1 | `section_16_v1_1_amendment.md` | row 221 (2026-05-15); §0.5 v24 paired-commit row 225 |
| superseded | v1 head | `section_16_reflection_packet.md` | row 216 (2026-05-15); §0.5 v22 paired-commit row 218 (superseded by v1.1) |

---

## §17 — Watts Per Funding Action (WPFA) *(v0.2-horizon — spec-locked)*

| Status | Version | Path | LOCK evidence |
|---|---|---|---|
| **HEAD** | v1 | `section_17_watts_per_funding_action.md` | row 205 (2026-05-11); §0.5 v19 paired-commit row 208 |
| companion | §4 v2.x.z WPFA amendment | `section_04_v2_x_z_wpfa_amendment.md` | row 207 (2026-05-11) |

---

## §18 — Card System

| Status | Version | Path | LOCK evidence |
|---|---|---|---|
| **HEAD (active amendment chain)** | v1.2 | `section_18_v1_2_amendment.md` | row 235 (2026-05-16T14:00Z) — see ledger-integrity note |
| amendment | v1.1 | `section_18_v1_1_amendment.md` | row 229 (2026-05-16); §0.5 v26 paired-commit row 230 |
| superseded | v1 head | `section_18_card_system.md` | pre-row-numbering; §0.5 paired-commit at `section_00_5_section_18_card_amendment.md` (superseded by v1.1 + v1.2; ALSO vocab-scrub-supersession row 241 cartridge→card on 2026-05-16; ALSO blueprint_supersession row 269 post-OD-D phase-4 fold-in append on 2026-05-17) |
| paired-commit (Wave 1) | Cards Wave 1 paired-commit amendment | `section_18_cards_wave_1_paired_commit_amendment.md` — see `section_00_5_section_18_cards_wave_1_paired_commit_amendment.md` at §0.5 v25 row 228 | row 228 (2026-05-15) |

### §18.6 v2 — dual-track CLC schema *(sub-section amendment)*

| Status | Version | Path | LOCK evidence |
|---|---|---|---|
| **HEAD** | **v2** | `section_18_6_v2_dual_track_amendment.md` | **row 274 (2026-05-17 / OD-E) + recovery row 279** (post-`amendment_status` flip supersession); §0.5 v32 paired-commit row 275 |

### §18.11 v1.1 — fold-in discipline checklist *(sub-section amendment)*

| Status | Version | Path | LOCK evidence |
|---|---|---|---|
| **HEAD** | **v1.1** | `section_18_11_v1_1_fold_in_discipline_amendment.md` | **row 270 (2026-05-17 / OD-D)**; §0.5 v30 paired-commit row 271 |

---

## Today's adds (2026-05-17)

- **§18.11 v1.1** fold-in discipline checklist — OD-D — row 270 + §0.5 v30 row 271
- **§4 v2.x.7** card-coupling-value-position — OD-C — row 272 + §0.5 v31 row 273
- **§18.6 v2** dual-track CLC schema — OD-E — row 274 + §0.5 v32 row 275 + recovery row 279
- **CLC card supersession-re-sign** (market_access / credit_underwriting / sponsorship_corporate) — rows 276 / 277 / 278 (post-§18.6 v2 dual-track restructure)
- **§18 main file blueprint_supersession** — row 269 (pre-OD-D bytes superseded; OD-D appended Phase 4 fold-in discipline checklist to §18.11)

---

## Cross-references

- **Cards Wave 1** (rows 226 + 227) and **Wave 2** (rows 250–261) card cartridges sit at `pipeline/cards/CIC/` + `pipeline/cards/CLC/`; they are `asset-signed`, not blueprint sections, so they are not in this index. See `../../../RUNTIME_MATURITY_MATRIX.md` § `asset-signed`.
- **Architecture v7.x amendments** (`pipeline/architecture/v0.1/architecture_v7_0_*_amendment.md`) are paired with §-blueprint amendments but are NOT §-blueprint sections themselves. The architecture chain is the parent governance surface (architecture v7 LOCKED A1–A12 2026-04-19); §-blueprints LOCK under it. The latest architecture amendments at v0.1: v7.0.9 (row 202), v7.0.10 (row 215), v7.0.11 card (paired with Wave 1), v7.0.12 apolitical_dialect (row 234 14:00Z).
- **§0.5 internal index row counts** — runtime-live row count is now **541** as of §0.5 v32 (was 540 pre-OD-E, 539 pre-OD-C, 538 pre-OD-D, per `daily_logs/2026-05-17.md`).
