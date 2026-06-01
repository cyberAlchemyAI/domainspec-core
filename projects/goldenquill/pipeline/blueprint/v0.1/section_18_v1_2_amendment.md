---
title: Blueprint §18 Card System — Amendment v1.2 (CIC card dialect_routing_table item-shape extension — retire funder_political_axis; add clc + register + example_program)
filed: 2026-05-15
operator: Josh Inklovich
amendment_status: LOCKED 2026-05-16T14:00:00Z. L-005 strict two-cycle Thesis CLOSED 2026-05-16 PM (Editor=groq/llama-3.3-70b-versatile + Judge=google/gemini-2.5-pro + Red Team=groq/openai/gpt-oss-120b via osascript→openclaw bridge). Verdict: READY_TO_LOCK. 28 fold-ins applied (12 Cycle 1 + 16 Cycle 2) per per-amendment appendix section appended below. Single `lock_timestamp_utc=2026-05-16T14:00:00Z` per §6.17 Option-B (4-amendment compound: architecture v7.0.12 + §18 v1.2 + §4 v2.x apolitical_dialect + §0.5 v28 — rebased from pre-staged v27 due to coordination conflict with CC-007 §0.5 v27 LOCK at lock_history row 233). Cards + admin_risk_register re-sign + Wave 2 LOCK deferred to separate ceremony per operator-confirmed Option B split (22-36 hour pre-ceremony operator work required first). Audit trail: `pipeline/validation/v7_0_12_thesis_2026-05-16/`.
parent_lock: pipeline/blueprint/v0.1/section_18_card_system.md  (§18 v1 — paired with architecture v7.0.11 + §4 v2.x card-hardening + §0.5 v25 — compound LOCK pending Wave 1 LOCK ceremony)
parent_lock_chain:
  - pipeline/blueprint/v0.1/section_18_v1_1_amendment.md  (§18 v1.1 LOCKED 2026-05-16 — narrow-corrective + schema-item-shape-extension precedent at §0.5 v26)
companion_lock: pipeline/blueprint/v0.1/section_00_5_apolitical_dialect_amendment.md  (§0.5 v27 paired-commit — 3 rows: 1 marker + 1 failure-code + 1 ast-lint)
companion_architecture_amendment: pipeline/architecture/v0.1/architecture_v7_0_12_apolitical_dialect_amendment.md
companion_logician_amendment: pipeline/blueprint/v0.1/section_04_logician_v2_x_apolitical_dialect.md
amendment_class: narrow-corrective + schema-item-shape-extension
precedent_pattern: §18 v1.1 (lock_history row 565, 2026-05-16) — narrow-corrective amendment extends an LOCKed schema's item shape without modifying the parent LOCKed text in-place. This v1.2 amendment uses the same pattern at smaller scope (one schema item shape touched on one schema; v1.1 touched three item shapes across two schemas).
threat_severity_at_v0_1_v0_2: LOW — schema item-shape refinement under v0.1 Beta single-operator deployment. The enforcement teeth live at §4 v2.x apolitical_dialect (F-DIALECT-POLITICAL-AXIS-LEAK runtime + R-NO-POLITICAL-AXIS-LITERAL ast-lint); §18 v1.2 narrow-corrective scope is strictly bounded to the CIC schema item-shape replacement. No prose-vs-schema reconciliation needed at v1.2 (the §18 v1 + v1.1 prose surface does not document `funder_political_axis` outside the schema-fragment block which gets a direct replacement at LOCK).
purpose: Apply architecture v7.0.12 retirement of the four-axis political enum to the CIC card `dialect_routing_table` item shape. Schema-binding wins: drop `funder_political_axis` property; add `clc` property (enum reused from `pipeline/types/identity_capital.py` `CapitalLogicCard` per v7.0.8); add `register` property (free-form string, matches §18 schema's existing `register_defaults.language_register` semantics); add `example_program` optional escape hatch (for program-internal CLC variation per architecture v7.0.12 §1.2 footnote).
companion_code_landed_at_LOCK:
  - "pipeline/cards/_schema/card_cic.schema.json — `dialect_routing_table[*]` item schema: drop `funder_political_axis` enum property; add `clc` enum property referencing the CapitalLogicCard 8-slug closed set; add `register` string property (1-256 chars); add `example_program` optional string property (1-256 chars). `dialect` property name preserved (semantic continuity with §18 v1.1 dialect_routing_table item shape; the *keying mechanism* changes, not the *Scribe sub-mode rendering* downstream)."
  - "pipeline/cards/CIC/food_systems.yaml — `dialect_routing_table` items re-keyed from funder_political_axis values to clc slugs; operator re-sign at LOCK ceremony per v7.0.11 §1 signed-card discipline."
  - "pipeline/cards/CIC/educator.yaml — same as food_systems."
  - "pipeline/cards/CIC/public_agency.yaml — same."
  - "pipeline/cards/CIC/arts_culture.yaml — same."
  - "pipeline/cards/CIC/cooperative.yaml — same."
  - "pipeline/cards/CIC/ecosystem_intermediary.yaml — same."
companion_tests_landed_at_LOCK:
  - "pipeline/cards/tests/test_cic_schema_validation.py — six fixtures (one per CIC card) validating against the refined schema; tests pre-existing at §18 v1 LOCK, fixtures re-pinned at v1.2 LOCK."
  - "pipeline/logician/tests/test_f_dialect_political_axis_leak.py — eight tests per §4 v2.x apolitical_dialect §4.X.4 (file lives at §4 v2.x apolitical_dialect, not §18 v1.2; cross-reference here for traceability)."
done_definition:
  - "Schema delta applied to `pipeline/cards/_schema/card_cic.schema.json` — `funder_political_axis` property removed; `clc` + `register` + `example_program` properties added; `dialect` property name preserved."
  - "Six CIC cards (food_systems + educator + public_agency + arts_culture + cooperative + ecosystem_intermediary) re-keyed at LOCK ceremony; operator Ed25519 re-signing applied to each card per v7.0.11 §1 signed-card discipline; SHA3-512 of patched canonical forms pinned in §0.5 v27 paired-commit at compound LOCK."
  - "L-005 strict two-cycle Thesis CLOSED with FULL live cross-family rigor (Editor + Judge + Red Team via openclaw bridge per AGENTS.md). Audit trail at `pipeline/validation/v7_0_12_thesis_<date>/`."
  - "Compound LOCK with architecture v7.0.12 + §4 v2.x apolitical_dialect + §0.5 v27 paired-commit at the same `lock_timestamp_utc` per §6.17 Option-B."
cowork_thesis_dispatch_status: PENDING at DRAFT — Thesis dispatch reserved for LOCK ceremony. Cycle 1 + Cycle 2 modeled on `pipeline/validation/v7_0_11_thesis_2026-05-15/` (joint v7.0.11 round) and `pipeline/validation/section_18_v1_1_thesis_2026-05-15/` (v1.1 narrow-corrective precedent).
session_metrics: pipeline/metrics/session_log.jsonl
---

# Amendment v1.2 — Narrow-corrective schema item-shape extension (retire funder_political_axis; add clc + register + example_program)

## §0. Amendment intent + scope

This narrow-corrective amendment **refines** (does **not** replace) the §18 v1 + v1.1 schema surface with one operator-pinned resolution surfaced at architecture v7.0.12 LOCK: the four-axis political enum on `dialect_routing_table` items is retired and replaced with a CLC-keyed routing primitive plus an optional `example_program` escape hatch.

The amendment does NOT modify §18 v1 architectural decisions on the Card System; it does NOT modify §18 v1.1 prose-vs-schema reconciliations (uppercase CIC/CLC paths, `review_status` field name, `frequency_observed` enum, `provenance_requirements` additionalProperties shape — all preserved unchanged); it does NOT add new failure-code primitives at this section (the F-DIALECT-POLITICAL-AXIS-LEAK gate is registered at §4 v2.x apolitical_dialect and §0.5 v27 row 567); it does NOT add new AST-lint rules at this section (R-NO-POLITICAL-AXIS-LITERAL is registered at §4 v2.x apolitical_dialect and §0.5 v27 row 568); it does NOT introduce new vocabulary kinds at §0.5 (the §0.5 v27 paired-commit registers 1 marker + 1 failure-code + 1 ast-lint under the existing v5+v6+v19+v22 closed vocabulary).

The amendment lands two binding deliverables:

1. **Schema refinement on CIC schema** — `dialect_routing_table[*]` item shape: drop `funder_political_axis` property; add `clc` + `register` + `example_program` properties; preserve `dialect` property name.
2. **Card conformance patches** — all six CIC cards re-keyed at LOCK ceremony; operator Ed25519 re-signing applied per v7.0.11 §1 signed-card discipline.

The amendment composes against §18 v1 LOCK + §18 v1.1 LOCK + architecture v7.0.11 LOCK + this same compound paired-commit's architecture v7.0.12 + §4 v2.x apolitical_dialect + §0.5 v27.

## §1. Operator-pinned resolution — political-axis retirement on CIC `dialect_routing_table`

### §1.1 Ambiguity statement

The §18 v1 (+ v1.1) CIC card schema documents `dialect_routing_table` items with the property `funder_political_axis` carrying enum values `conservative | centrist | progressive | soul_fire`. Per architecture v7.0.12, this is a Law 4 self-contradiction — Law 4's title is "Apolitical Sector Language" but the substrate carries a four-axis political enumeration as a routing primitive. The retirement is non-negotiable for the apolitical claim to be honest.

### §1.2 On-disk evidence

Verified at `pipeline/cards/_schema/card_cic.schema.json` (`dialect_routing_table.items.properties.funder_political_axis` enum block); `pipeline/cards/CIC/food_systems.yaml` (`dialect_routing_table[*].funder_political_axis` populated values); `pipeline/cards/CIC/educator.yaml` + four other cards (same); `pipeline/seats/scribe/dialect.py` (routing function signatures); `pipeline/engineering/agents/references/dialect_codebook.yaml` (dialect codebook keyed by political axis); architecture v7.0.11 + revised post-Alpha source doc (§18 schema fragment carries the same enum).

### §1.3 Operator-pinned resolution

Replace the political-axis enum with CLC-keyed routing. Architecture v7.0.12 §1.2 specifies the schema shape; this amendment renders that into the §18 CIC schema.

### §1.4 Schema delta — `pipeline/cards/_schema/card_cic.schema.json`

**Before** (v1.1 — superseded at v1.2 LOCK):

```json
{
  "dialect_routing_table": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "funder_political_axis": {
          "type": "string",
          "enum": ["conservative", "centrist", "progressive", "soul_fire"]
        },
        "dialect": {"type": "string"},
        "example_funder": {"type": "string"}
      },
      "required": ["funder_political_axis", "dialect"],
      "additionalProperties": false
    }
  }
}
```

**After** (v1.2 LOCK):

```json
{
  "dialect_routing_table": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "clc": {
          "type": "string",
          "enum": [
            "public_purpose_works",
            "catalytic_change",
            "operating_capacity",
            "research_evidence",
            "market_access",
            "credit_underwriting",
            "sponsorship_corporate",
            "shared_assets"
          ],
          "description": "CLC slug from the canonical CapitalLogicCard enum (v7.0.8). Closed set of 8. Adding a new CLC requires an architecture amendment that updates pipeline/types/identity_capital.py + this schema; F-CIC-CLC-ENUM-DRIFT enforces."
        },
        "dialect": {
          "type": "string",
          "minLength": 1,
          "maxLength": 64,
          "description": "Scribe sub-mode key (e.g., 'civic-formal', 'audience-brand', 'systems-change'). The keying mechanism changes at v1.2 (from political axis to CLC); the dialect rendering downstream is unchanged."
        },
        "register": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256,
          "description": "Free-form description of the register expected by this CLC's typical reviewer. Used by Scribe for prompt composition; not a routing key."
        },
        "example_program": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256,
          "description": "Optional escape hatch for program-internal variation within one CLC. Useful for cases like NEA Challenge America vs Our Town (both sponsorship_corporate, different register expectations). Not a routing key; advisory only."
        }
      },
      "required": ["clc", "dialect", "register"],
      "additionalProperties": false,
      "not": {
        "required": ["funder_political_axis"]
      }
    }
  }
}
```

**Discipline notes:**

- `clc` is required.
- `dialect` is required (preserved from v1.1; the Scribe sub-mode key downstream).
- `register` is required (free-form description; replaces the implicit register the political-axis enum was carrying).
- `example_program` is optional (the escape hatch; per operator scoping 2026-05-15 "whatever you suggest" with the recommendation to keep it survivable).
- `funder_political_axis` is explicitly forbidden via the `not.required` JSON Schema construct — any card carrying the retired property name fails schema validation at load time, surfacing as `F-DIALECT-POLITICAL-AXIS-LEAK.schema_property` per §4 v2.x apolitical_dialect §4.X.1 Layer 3.

### §1.5 Card patches at LOCK

All six CIC cards re-keyed at LOCK ceremony. Each card's `dialect_routing_table` block is rewritten from the political-axis form to the CLC form. The rewrite is operator-driven (the political-axis → CLC mapping is not mechanical — each CIC's dialect routing carries semantic content that operator decides which CLC slug to assign per row).

**Sequencing discipline:** card patches land BEFORE the LOCK ceremony pins SHA3-512 of canonical card forms — same discipline as §18 v1.1 Wave 1 coordination note (file's §coordination_note block at top). Failure to apply patches before LOCK pinning surfaces as a Wave-2-class re-pin follow-on ceremony per §18 v1.1 §0 coordination conflict protocol.

**Re-signing discipline:** each patched card gets operator Ed25519 + ML-DSA-65 hybrid signing per A12 crypto-agility + v7.0.11 §1 signed-card discipline. Re-signing happens before the card's canonical SHA3-512 is recorded in lock_history rows at compound LOCK.

## §2. What this amendment does not do

- Does not modify the four-CIC-card non-dialect-routing-table fields (search_vocabulary, evidence_signals, kfr_fact_classes, register_defaults, admin_risk_term_register's non-political-register fields, reporting_cadence_typical, metrics_table_template, narrative_sections_typical, capacity_signals_required, compliance_burdens, common_risk_register_entries, common_funders_observed, `_research_metadata`).
- Does not modify the §18 v1.1 schema refinements (`frequency_observed` enum on `common_funders_observed`, `provenance_requirements` additionalProperties shape).
- Does not modify the CLC card schema (`pipeline/cards/_schema/card_clc.schema.json`) — CLC schema does not have `dialect_routing_table` per §18.6 schema scope; the retirement is CIC-side only.
- Does not modify the `register_defaults.language_register` enum (still `formal | conversational | movement | hybrid` per §18 v1).
- Does not modify Scribe's underlying register-rendering capability — the four `dialect` sub-modes survive unchanged; only the routing key changes.
- Does not register new §0.5 rows at this section — the §0.5 v27 paired-commit (1 marker + 1 failure-code + 1 ast-lint) lives at the apolitical_dialect amendment file; this §18 v1.2 amendment is an inner-schema delta under §0.5 v25 cards._schema row precedent.
- Does not modify the admin_risk_register schema directly — the `progressive_register` → `per_clc_register` schema swap is part of architecture v7.0.12 §1.2 (admin_risk_register lives at `pipeline/institutional_memory/`, not `pipeline/cards/`; outside §18 scope).

## §3. Composition with §18 v1.1

§18 v1.2 composes with §18 v1.1 as follows:

- v1.1's three item-shape extensions stay (frequency_observed enum, provenance_requirements additionalProperties, dialect_routing_table standardization-of-item-shape — the latter was a generic item-shape standardization, not a property-set change).
- v1.2 changes the dialect_routing_table item property set: drops `funder_political_axis`, adds `clc` + `register` + `example_program`.
- v1.1 + v1.2 together produce the CIC card schema at compound v7.0.12 LOCK.
- Future §18 v1.3 (if needed) would be another narrow-corrective at the same precedent pattern.

## §4. Composition with v7.0.12 + §4 v2.x apolitical_dialect + §0.5 v27

The compound paired-commit lands four amendments at the same `lock_timestamp_utc`:

| File | Role |
|---|---|
| `architecture_v7_0_12_apolitical_dialect_amendment.md` | Architectural decision — retire enum + re-ground Law 4 |
| `section_04_logician_v2_x_apolitical_dialect.md` | Logician enforcement — F-DIALECT-POLITICAL-AXIS-LEAK gate + R-NO-POLITICAL-AXIS-LITERAL AST-lint |
| `section_00_5_apolitical_dialect_amendment.md` | Interface-index registration — 3 rows (1 marker + 1 failure-code + 1 ast-lint) |
| **`section_18_v1_2_amendment.md` (this file)** | CIC card schema item-shape extension — drop funder_political_axis; add clc + register + example_program |

F-INDEX-STALE PRE-gate verifies the §0.5 v27 paired-commit at compound LOCK; failure on any sibling amendment fails the compound LOCK ceremony.

## §5. Lock-history note + sequencing

If v7.0.11 + v7.0.12 joint LOCK (preferred per architecture v7.0.12 §6), this v1.2 amendment lands alongside the v7.0.11 card schema's first LOCK — the schema goes straight to v1.2-shape at v7.0.11 LOCK rather than transiting through v1.1-shape-with-political-axis. In that case, §18 v1.1 LOCK row stays at 565 (already LOCKED 2026-05-16), §18 v1 LOCK row reflects the v1.2-shape directly, and §0.5 v27 lands the compound-paired-commit registration at one ceremony.

If v7.0.11 LOCKs first (with the v1.1-shape carrying political axis), this v1.2 amendment lands as a narrow-corrective on the already-LOCKed v1.1 schema — same shape as §18 v1.1 lands on §18 v1.

Either path is acceptable. The L-005 Thesis dispatch determines the ceremony order based on Cycle-2 verification across both rounds.


---

# §6. Cycle 1 + Cycle 2 fold-ins applied at LOCK 2026-05-16T14:00:00Z

L-005 strict two-cycle Thesis CLOSED 2026-05-16. Verdict: READY_TO_LOCK. Audit trail: `pipeline/validation/v7_0_12_thesis_2026-05-16/`. Per row-170 transparent disposition, fold-ins applicable to this amendment are baked into LOCKed canonical bytes here.

## Cycle 1 fold-ins applicable to this amendment (verbatim patches in `cycle_1/foldins_applied.md`)

- **FI-5 (closes JD-1)**: §1.4 JSON Schema delta — **remove the ineffective `not: { required: ["funder_political_axis"] }` clause**. The `additionalProperties: false` coupled with absence of `funder_political_axis` from the `properties` map is the actual enforcement mechanism. Schema description updated to document that retired property is forbidden via additionalProperties: false.
- **FI-6 (closes JD-2)**: §1.4 schema — **rename `register` property to `register_description`** to disambiguate from `progressive_register` (retired), `register_defaults.language_register` (preserved per §2), and the general "admin-risk register" term. Description: "Free-form description of the register expected by this CLC's typical reviewer. Used by Scribe for prompt composition; not a routing key."
- **FI-9 REVISED (closes ED-2 + ED-4)**: §1.5c card rewrite operator procedure — **content-judgment-driven; NO political-axis-to-CLC table** (operator pushback 2026-05-16: any heuristic mapping re-encodes the retired axis; per `feedback_no_heuristic_mapping_on_enum_retirement.md`). Operator reads each existing routing row's dialect content + example_funder text + decides which CLC slug captures the funder cluster THIS row served. No reference to the old `funder_political_axis` value should appear in the new row. Burden estimate: 3-5 hours per card × 6 cards = 18-30 hours operator review at cards-ceremony.

## Deferred per row-170 transparent disposition

- None applicable to this amendment beyond the inheritance from architecture v7.0.12 deferrals.

## Disposition summary

- Cycle 1 fold-ins applied: 3 (FI-5, FI-6, FI-9 REVISED)
- Cycle 2 fold-ins applied: 0 (Judge JD-C2-LOW findings landed at architecture v7.0.12 + §4 v2.x; no Cycle 2 finding applies directly to this amendment's schema delta)
- **This amendment LOCK fold-in count: 3 applied.**
