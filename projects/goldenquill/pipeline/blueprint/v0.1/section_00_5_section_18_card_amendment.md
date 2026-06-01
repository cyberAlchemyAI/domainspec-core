---
title: §0.5 v25 — Interface Index paired-commit for §18 Card System + architecture v7.0.11 + §4 v2.x card-hardening compound LOCK (DRAFT)
filed: 2026-05-15
operator: Josh Inklovich
status: DRAFT — LOCK-READY. Pending L-005 strict two-cycle Thesis dispatch. Compound paired-commit (sibling 4/4) with architecture v7.0.11 + §18 v1 + §4 v2.x card-hardening at the same `lock_timestamp_utc` per §6.17 Option-B.
parent_locks:
  - pipeline/blueprint/v0.1/section_00_5_section_16_v1_1_amendment.md                     # §0.5 v24 LOCKED 2026-05-15 row 225 (predecessor; runtime-live 533)
  - pipeline/blueprint/v0.1/section_00_5_section_17_wpfa_amendment.md                     # §0.5 v19 LOCKED 2026-05-11 — paired-commit precedent quadruple
companion_amendments_DRAFT:
  - pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md           # sibling 1/4 — architecture amendment
  - pipeline/blueprint/v0.1/section_18_card_system.md                           # sibling 2/4 — blueprint section
  - pipeline/blueprint/v0.1/section_04_logician_v2_x_card_hardening.md                    # sibling 3/4 — Logician hardening
compound_lock_with: architecture_v7_0_11_card_amendment.md + section_18_card_system.md + section_04_logician_v2_x_card_hardening.md
amendment_class: §0.5-paired-commit (new section + new failure-code family + new asset family)
target_lock_row: <appended at LOCK ceremony>
target_index_rows: 534-563 (30 rows estimated; 1 section-anchor + 2 schema + 14 card-namespace + 8 failure-code + 4 interface-contract + 1 AST-lint); runtime-live after v25 estimated 563.
runtime_live_pre_lock: 533
runtime_live_post_lock_estimated: 563
ws_dispatch: WS-Cards Phase A (v0.1 Beta scope — schema + Pydantic models + loader stub + fixture stubs + F-CARDS-* dormant primitives)
session_metrics: pipeline/metrics/session_log.jsonl
revised_feedback_reconciliation_2026-05-15: docs/post_alpha/post_alpha_card_system_revised_2026-05-15.md drives the row content baked in below. The three operator decisions from the morning DRAFT (common_clc_patterns_observed kill, matrix forward-compat-only, food_systems+operating_capacity first fixtures) are resolved and reflected in §0.5.v25.X.1 + §0.5.v25.X.2 row groups.
---

# §0.5 v25 — Interface Index amendment for §18 Card System compound LOCK (DRAFT)

## §0.5.v25.0 Amendment intent

This amendment registers the §18 Card System primitives into the Interface Index. Compound-paired-commit with architecture v7.0.11 + §18 v1 + §4 v2.x card-hardening at the same `lock_timestamp_utc` per §6.17 Option-B.

Three substantive primitive families register:

1. **`cards` family** — workspace-shared knowledge namespace family. Six CIC namespaces + eight CLC namespaces + one matrix forward-compat namespace family = 15 namespaces total.
2. **F-CARDS-\* failure-code family** — seven new failure-code rows; mirrors F-CLASS-\* (v7.0.7 §5.1) + F-PACKET-\* (§16 v1) + F-FG-\* (FundingGoal v0.2) byte-for-byte for structure.
3. **F-CIC-CLC-PATTERN-READ-DURING-ELIGIBILITY** — one extension row to v7.0.8's existing F-CIC-CLC-* family. Does NOT register a new family; extends the existing family roster.

Plus auxiliary rows for the §18 section anchor + card schemas + loader interface contract + AST-lint rule.

**Vocabulary check against §0.5 v24 closed vocabulary.** All `kind` values used below — `marker`, `schema`, `interface-contract`, `failure-code`, `ast-lint`, `card-namespace` — appear in v24's closed vocabulary OR are paired-commit vocabulary-extension at this LOCK. **One new vocabulary kind at this amendment:** `card-namespace` (rationale below). Precedent for namespace-class primitives: §2 v7.2 `SUB_KIND_REGISTRY` entries are conceptually adjacent but live under `schema` kind; `card-namespace` is sufficiently distinct (workspace-shared rather than per-org-vault-bound) to warrant its own vocabulary kind.

## §0.5.v25.X — Row append (rows 534-563 estimated)

All rows enter §0.5 at `stability_tier = "STABLE"` at compound v1 LOCK (no PARENT_UNLOCKED transit since architecture v7.0.11 + §18 v1 + §4 v2.x card-hardening LOCK in the same compound transaction).

### §0.5.v25.X.0 — Section anchor + schemas (rows 534-536)

| Row | primitive_id | defined_at | parent_lock_version | kind | stability_tier |
|---|---|---|---|---|---|
| 534 | `blueprint.section_anchor.s18_card.v1` | `pipeline/blueprint/v0.1/section_18_card_system.md` | §18 v1 | marker | STABLE |
| 535 | `cards._schema.card_cic.v1` | `pipeline/cards/_schema/card_cic.schema.json` | §18 v1 | schema | STABLE |
| 536 | `cards._schema.card_clc.v1` | `pipeline/cards/_schema/card_clc.schema.json` | §18 v1 | schema | STABLE |

### §0.5.v25.X.1 — CIC card namespaces (rows 537-542)

Six rows, one per CIC slug. Each row registers a `cards:cic:<slug>` namespace under the new `card-namespace` kind.

| Row | primitive_id | defined_at | kind | stability_tier |
|---|---|---|---|---|
| 537 | `cards.cic.food_systems.v1` | `pipeline/cards/CIC/food_systems.yaml` | card-namespace | STABLE |
| 538 | `cards.cic.educator.v1` | `pipeline/cards/CIC/educator.yaml` | card-namespace | STABLE |
| 539 | `cards.cic.public_agency.v1` | `pipeline/cards/CIC/public_agency.yaml` | card-namespace | STABLE |
| 540 | `cards.cic.arts_culture.v1` | `pipeline/cards/CIC/arts_culture.yaml` | card-namespace | STABLE |
| 541 | `cards.cic.cooperative.v1` | `pipeline/cards/CIC/cooperative.yaml` | card-namespace | STABLE |
| 542 | `cards.cic.ecosystem_intermediary.v1` | `pipeline/cards/CIC/ecosystem_intermediary.yaml` | card-namespace | STABLE |

### §0.5.v25.X.2 — CLC card namespaces (rows 543-550)

Eight rows, one per CLC slug. Each row registers a `cards:clc:<slug>` namespace.

| Row | primitive_id | defined_at | kind | stability_tier |
|---|---|---|---|---|
| 543 | `cards.clc.public_purpose_works.v1` | `pipeline/cards/CLC/public_purpose_works.yaml` | card-namespace | STABLE |
| 544 | `cards.clc.catalytic_change.v1` | `pipeline/cards/CLC/catalytic_change.yaml` | card-namespace | STABLE |
| 545 | `cards.clc.operating_capacity.v1` | `pipeline/cards/CLC/operating_capacity.yaml` | card-namespace | STABLE |
| 546 | `cards.clc.research_evidence.v1` | `pipeline/cards/CLC/research_evidence.yaml` | card-namespace | STABLE |
| 547 | `cards.clc.market_access.v1` | `pipeline/cards/CLC/market_access.yaml` | card-namespace | STABLE |
| 548 | `cards.clc.credit_underwriting.v1` | `pipeline/cards/CLC/credit_underwriting.yaml` | card-namespace | STABLE |
| 549 | `cards.clc.sponsorship_corporate.v1` | `pipeline/cards/CLC/sponsorship_corporate.yaml` | card-namespace | STABLE |
| 550 | `cards.clc.shared_assets.v1` | `pipeline/cards/CLC/shared_assets.yaml` | card-namespace | STABLE |

### §0.5.v25.X.3 — Matrix forward-compat namespace family (row 551)

One row registers the matrix namespace family (per-intersection patterning is a v1.x activation; the family itself registers as forward-compat at v7.0.11 LOCK).

| Row | primitive_id | defined_at | kind | stability_tier |
|---|---|---|---|---|
| 551 | `cards.matrix.forward_compat_family.v1` | `pipeline/cards/matrix/_FORWARD_COMPAT_ONLY.md` | card-namespace | STABLE |

### §0.5.v25.X.4 — Interface contracts (rows 552-555)

| Row | primitive_id | defined_at | kind | stability_tier |
|---|---|---|---|---|
| 552 | `cards.loader.load_card.v1` | `pipeline/blueprint/v0.1/section_18_card_system.md#§18.14` | interface-contract | STABLE |
| 553 | `cards.validators.self_validation_phase_4.v1` | `pipeline/blueprint/v0.1/section_18_card_system.md#§18.11` | interface-contract | STABLE |
| 554 | `cards.memory.namespace_resolver.v1` | `pipeline/blueprint/v0.1/section_18_card_system.md#§18.13` | interface-contract | STABLE |
| 555 | `cards.signing.publisher_pubkey_pin.v1` | `pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md#§1.10` | interface-contract | STABLE |

### §0.5.v25.X.5 — F-CARDS-* failure-code family (rows 556-562)

Seven rows mirror F-CLASS-* and F-PACKET-* family registration shape byte-for-byte.

| Row | primitive_id | defined_at | kind | stability_tier |
|---|---|---|---|---|
| 556 | `F-CARDS-COVERAGE-INCOMPLETE` | `pipeline/blueprint/v0.1/section_04_logician_v2_x_card_hardening.md#§4.X.1.1` | failure-code | STABLE |
| 557 | `F-CARDS-SCHEMA-INVALID` | `pipeline/blueprint/v0.1/section_04_logician_v2_x_card_hardening.md#§4.X.1.2` | failure-code | STABLE |
| 558 | `F-CARDS-UNSIGNED-PRODUCTION-LOAD` | `pipeline/blueprint/v0.1/section_04_logician_v2_x_card_hardening.md#§4.X.1.3` | failure-code | STABLE |
| 559 | `F-CARDS-SIGNATURE-INVALID` | `pipeline/blueprint/v0.1/section_04_logician_v2_x_card_hardening.md#§4.X.1.4` | failure-code | STABLE |
| 560 | `F-CARDS-PRIVATE-DATA-IN-CARD` | `pipeline/blueprint/v0.1/section_04_logician_v2_x_card_hardening.md#§4.X.1.5` | failure-code | STABLE |
| 561 | `F-CARDS-CROSS-ORG-NAMESPACE-LEAK` | `pipeline/blueprint/v0.1/section_04_logician_v2_x_card_hardening.md#§4.X.1.6` | failure-code | STABLE |
| 562 | `F-CARDS-COUPLING-VIOLATION-EXTENSION` | `pipeline/blueprint/v0.1/section_04_logician_v2_x_card_hardening.md#§4.X.1.7` | failure-code | STABLE |

### §0.5.v25.X.6 — F-CIC-CLC-* family extension (row 563)

One row extends v7.0.8's F-CIC-CLC-COUPLING-VIOLATION family with the pattern-read-during-eligibility gate. Family prefix `F-CIC-CLC-*` (not `F-CARDS-*`) preserves orthogonality-discipline ancestry per architecture v7.0.11 §1.6 #7.

| Row | primitive_id | defined_at | kind | stability_tier |
|---|---|---|---|---|
| 563 | `F-CIC-CLC-PATTERN-READ-DURING-ELIGIBILITY` | `pipeline/blueprint/v0.1/section_04_logician_v2_x_card_hardening.md#§4.X.1.8` | failure-code | STABLE |

### §0.5.v25.X.7 — AST-lint rule (row 564 — overshoots target_index_rows estimate by 1)

| Row | primitive_id | defined_at | kind | stability_tier |
|---|---|---|---|---|
| 564 | `R-CARDS-NO-COUPLING-FIELD.v1` | `pipeline/blueprint/v0.1/section_04_logician_v2_x_card_hardening.md#§4.X.3` | ast-lint | STABLE |

**Note:** target_index_rows in frontmatter says 534-563 (30 rows); actual count is 31 (rows 534-564). Frontmatter updates at LOCK ceremony to `target_index_rows: 534-564` and `runtime_live_post_lock: 564`.

## §0.5.v25.Y — Vocabulary extension rationale

**New kind `card-namespace` introduced at this amendment (rows 537-551).** Rationale: card namespaces are workspace-shared rather than per-org-vault-bound (the v7.0.7 §2 SUB_KIND_REGISTRY pattern under `schema` kind is per-org-bound). A card namespace is the family-of-bindings between a card file on disk and the memory retrieval layer's namespace contract; that family-of-bindings is sufficiently distinct from a per-org sub-kind schema to deserve its own vocabulary kind. Precedent for vocabulary extensions paired with section LOCKs exists in §17 v1 + §0.5 v19 (`ast-lint`) and §16 v1.1 + §0.5 v24 (`subkind-registry-activation`, `signed-asset`, `failure-code-live-body`, `meta-gate-strengthening`, `producer-binding`). This is the seventh vocabulary kind extension across §0.5 v6-v24.

## §0.5.v25.Z — F-INDEX-STALE preflight

F-INDEX-STALE PRE-gate fires at compound LOCK commit time per §6.2 order 3; all 31 new rows must be present in the index or the commit fails closed. The runtime-live row count flips from 533 → 564 at the same `lock_timestamp_utc`.

## §0.5.v25.W — DRAFT-state acknowledgement

This file ships as DRAFT at v0.1 LOCK candidate state alongside architecture v7.0.11 DRAFT + §18 v1 DRAFT + §4 v2.x card-hardening DRAFT. Frontmatter `status:` flips from "DRAFT — LOCK-READY" to "LOCKED 2026-05-?? — compound paired-commit ..." at the L-005 two-cycle Thesis CLOSED ceremony per §6.17 Option-B. Row numbers may shift if intervening §0.5 amendments LOCK between this DRAFT date (2026-05-15) and the v7.0.11 compound-LOCK date.
