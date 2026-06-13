---
title: Blueprint §0.5 — Section 18 Card Runtime Wiring Amendment (DRAFT)
filed: 2026-05-18
operator: Josh Inklovich
amendment_status: DRAFT — LOCK-READY. Paired with architecture v7.0.13 §1 (Card Runtime Wiring Amendment). LOCKs atomically at the same `lock_timestamp_utc` per §6.17 Option-B.
parent_lock: pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md
companion_amendment: pipeline/architecture/v0.1/architecture_v7_0_13_card_runtime_wiring_amendment.md
authority_source: Operator directive 2026-05-18. Realizes blueprint §18.16.B v0.2 first wave runtime context injection.
audit_trail: pipeline/validation/v7_0_13_thesis_<date>/   # populated when L-005 round dispatches
---

# Amendment intent

Register the v0.2-first-wave Card runtime wiring entities in the interface index. Paired with architecture v7.0.13 §1.

# §0.5 v?? — New interface-index rows

The following entities register as new §0.5 rows. Compound-paired-commit per §6.17 Option-B at the LOCK ceremony.

## Top-level kinds added

- **`cards:runtime_context`** — directory/module family. One row.

## Per-entity rows

### `cards:runtime_context` family

| kind | path | role | shippable_in | notes |
|------|------|------|--------------|-------|
| `module` | `pipeline/cards/runtime_context.py` | `CardRuntimeContext` primitive + `build_card_runtime_context` constructor | `v0.2` | Frozen + kw-only + slots dataclass per A12. Bound to one cycle for one org. |

### `cards:seat_dependencies` family (extension)

The `pipeline/cards/seat_dependencies.py` module is already registered at v7.0.11 LOCK as the static field-dependency registry. This amendment populates its per-seat dependency declarations for the v0.2-first-wave runtime seats; the module path stays unchanged. The row's `last_modified_amendment` updates to v7.0.13.

### `seats:card_wiring` family

| kind | path | role | shippable_in | notes |
|------|------|------|--------------|-------|
| `module` | `pipeline/scout/card_wiring.py` | `ScoutCardView` + `build_scout_card_view` | `v0.2` | Scout lives at `pipeline/scout/` (not `pipeline/seats/scout/`) for historical reasons. |
| `module` | `pipeline/seats/scribe/card_wiring.py` | `ScribeCardView` + `build_scribe_card_view` | `v0.2` | |
| `module` | `pipeline/seats/editor/card_wiring.py` | `EditorCardView` + `build_editor_card_view` | `v0.2` | |
| `module` | `pipeline/seats/judge/card_wiring.py` | `JudgeCardView` + `build_judge_card_view` | `v0.2` | |

### Loader graduation

The `pipeline/cards/loader.py` module is already registered at v7.0.11 LOCK. This amendment graduates its `load_card` function from raising `NotImplementedError` at the seat-injection boundary to returning a `LoadedCard` with the parsed model + consuming-seat roster. The row's `last_modified_amendment` updates to v7.0.13.

### `seats:Editor` consuming-seat membership

The `SEAT_NAMES` enum at `pipeline/cards/seat_dependencies.py` extends from 7 entries to 8 with `"Editor"` added. The `Editor` value joins the consuming-seat roster because Editor's clarity review reads CIC voice/register defaults + CLC reviewer-pov red flags at v0.2 first wave.

## §0.5 row count delta

- v7.0.11 LOCK candidate: 28 runtime-live rows.
- v7.0.13 LOCK additions: +5 module rows (runtime_context + 4 card_wiring modules) +1 README row at `pipeline/seats/README.md` = +6.
- v7.0.13 LOCK total: 34 runtime-live rows.

# §1 — Atomic paired commit (§6.17 Option-B)

When L-005 LOCKs the architecture v7.0.13 amendment, this §0.5 amendment paired-commits at the same `lock_timestamp_utc`. Both file paths appear in the `lock_history.yaml` row for v7.0.13.

# §2 — Forward-binding

The v0.2 second wave compound LOCK (multi-track CLC + `*-envelope.v2` rev carrying explicit CIC/CLC slugs + R-CARDS-SEAT-DEPS-DRIFT AST-lint + heavy-Judge swap card-substrate hardening) extends this row family. The contract pattern (one `card_wiring.py` per consuming seat, one `{Seat}CardView` per module, one declared dependency row in `seat_dependencies.py`) stays unchanged at the v0.2 second wave LOCK — only the per-seat field rosters grow.
