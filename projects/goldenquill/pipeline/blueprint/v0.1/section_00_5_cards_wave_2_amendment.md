---
title: §0.5 v29 — Interface Index paired-commit for Cards Wave 2 LOCK ceremony (12-card signature_status flip)
filed: 2026-05-16
operator: Josh Inklovich
status: LOCKED 2026-05-16T16:00:00Z at lock_history row 262
parent_locks:
  - pipeline/blueprint/v0.1/section_00_5_apolitical_dialect_amendment.md       # §0.5 v28 LOCKED 2026-05-16 row 237 (predecessor)
  - pipeline/blueprint/v0.1/section_00_5_section_18_cards_wave_1_paired_commit_amendment.md  # §0.5 v25 LOCKED 2026-05-15 row 228 (Wave 1 precedent)
compound_lock_with: 12 Wave 2 card LOCKs (rows 250-261) at the same lock_timestamp_utc per §6.17 Option-B
amendment_class: §0.5-paired-commit-narrow-corrective (signature_status flip-only, no new rows)
target_lock_row: 262
runtime_live_pre_lock: 538
runtime_live_post_lock: 538
session_metrics: pipeline/metrics/session_log.jsonl
---

# §0.5 v29 — Interface Index amendment for Cards Wave 2 LOCK ceremony

## §0.5.v29.0 Amendment intent

This amendment is a paired-commit with the Cards Wave 2 LOCK ceremony (12 cards LOCKed at rows 250-261 of lock_history.v1.jsonl at compound timestamp `2026-05-16T16:00:00Z`).

**No new primitive_id rows are appended to §0.5.** All 14 card namespaces (6 CIC + 8 CLC) were already registered in §0.5 v25 at LOCK rows 537-550. This amendment is a narrow-corrective `signature_status` flip on the 12 Wave 2 card primitives — Wave 1 (food_systems + operating_capacity) already flipped at §0.5 v25 LOCK.

**Vocabulary check.** No new `kind` values introduced. All updates land within the existing `card-namespace` kind registered at §0.5 v25.

## §0.5.v29.1 — Per-primitive signature_status flips (12 entries)

| primitive_id | field | before | after | card_lock_row |
|---|---|---|---|---|
| `cards.cic.educator.v1` | `signature_status` | `unsigned` | `signed` | 250 |
| `cards.cic.public_agency.v1` | `signature_status` | `unsigned` | `signed` | 251 |
| `cards.cic.arts_culture.v1` | `signature_status` | `unsigned` | `signed` | 252 |
| `cards.cic.cooperative.v1` | `signature_status` | `unsigned` | `signed` | 253 |
| `cards.cic.ecosystem_intermediary.v1` | `signature_status` | `unsigned` | `signed` | 254 |
| `cards.clc.public_purpose_works.v1` | `signature_status` | `unsigned` | `signed` | 255 |
| `cards.clc.catalytic_change.v1` | `signature_status` | `unsigned` | `signed` | 256 |
| `cards.clc.research_evidence.v1` | `signature_status` | `unsigned` | `signed` | 257 |
| `cards.clc.market_access.v1` | `signature_status` | `unsigned` | `signed` | 258 |
| `cards.clc.credit_underwriting.v1` | `signature_status` | `unsigned` | `signed` | 259 |
| `cards.clc.sponsorship_corporate.v1` | `signature_status` | `unsigned` | `signed` | 260 |
| `cards.clc.shared_assets.v1` | `signature_status` | `unsigned` | `signed` | 261 |

## §0.5.v29.2 — Per-card audit pointer

Each of the 12 Wave 2 cards is signed with operator publisher Ed25519 key (pinned at `vault_shared/cards/publisher_pubkey.signed.yaml`, pubkey hex `0b1a0bbfa5ee9149af2c4e6153ed037dd03c0d562c94d3eaefeaf798e6f375bd`). Per-card signature + canonical-JSON SHA3-512 recorded in lock_history rows 250-261. Audit trail at `pipeline/validation/cards_wave_2_lock_ceremony_2026-05-16/`.

| card_id | slug | lock_history_row | sig prefix (16 hex) | sha3 prefix (16 hex) |
|---|---|---|---|---|
| TILTH-CIC-02 | educator | 250 | `de90a25e0956eb70` | `eb1ba9adf005c983` |
| TILTH-CIC-03 | public_agency | 251 | `ff7ddc6a3b8aee05` | `57bb9e077fa553bc` |
| TILTH-CIC-04 | arts_culture | 252 | `34eb758b3ac7407f` | `8e1779b85bc28d2d` |
| TILTH-CIC-05 | cooperative | 253 | `373af84b400a28ea` | `9ea4e6907177f07a` |
| TILTH-CIC-06 | ecosystem_intermediary | 254 | `9d0afcb26ee4bcd9` | `64704c7e566e625e` |
| TILTH-CLC-01 | public_purpose_works | 255 | `812631cb11bcc2a5` | `578dd1cfd1cb0a50` |
| TILTH-CLC-02 | catalytic_change | 256 | `ae039ca336e77679` | `fd225e386c3363b0` |
| TILTH-CLC-04 | research_evidence | 257 | `42b80c9810b5a747` | `dc5ae6a90e82bd0a` |
| TILTH-CLC-05 | market_access | 258 | `28d78c1ff18851ce` | `09b7eee8db77744c` |
| TILTH-CLC-06 | credit_underwriting | 259 | `4cefd73f702ecbff` | `c0f4993ed9a5a885` |
| TILTH-CLC-07 | sponsorship_corporate | 260 | `7502058e7846ed36` | `1e2e97faf38c3d06` |
| TILTH-CLC-08 | shared_assets | 261 | `3c8802c1414e0b84` | `9ed64de78933fbf7` |

## §0.5.v29.3 — Operator-decision dispositions (Wave 2 close synthesis)

- **OD-F** (CIC-05 named-org cleanup): resolved pre-ceremony via Phase D A.1 full anonymization (named soul_fire orgs Cooperation Jackson / USFWC / DAWI / Industrial Commons / Highlander removed entirely per operator directive 2026-05-16T14:00:00Z, not relocated). Per Law 5 substance discipline.
- **OD-H** (CIC-03/CIC-04 racial-justice severity): confirmed defensible per Phase A.2 refresh — both CIC-03 public_agency and CIC-04 arts_culture carry `racial justice = HIGH` (original CC-8 finding stale; refreshed flag is `DEI / equity / inclusion` HIGH on CIC-02 + CIC-04 vs MED on CIC-03 + CIC-05, applied as-authored).
- **OD-A/B/C/D/E/G/I**: deferred to post-LOCK follow-on dispatches (see Wave 2 close synthesis).

## §0.5.v29.4 — LOCK metadata

- LOCK timestamp: `2026-05-16T16:00:00Z`
- LOCK row: 262
- Publisher pubkey: `0b1a0bbfa5ee9149af2c4e6153ed037dd03c0d562c94d3eaefeaf798e6f375bd`
- Compound-LOCK with: 12 Wave 2 card rows (250-261)
- Ceremony audit trail: `pipeline/validation/cards_wave_2_lock_ceremony_2026-05-16/`
