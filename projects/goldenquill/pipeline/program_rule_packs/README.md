# Program Rule Packs (PRPs) — Live Federal & State Program Law Substrate

**Status:** v0.1 Beta scaffold landed. Substrate (schema + manifest + loader skeleton) is on-disk and reviewable; the loader top-level call raises `NotImplementedError` at v0.1 so no PRP body is validated against the schema in production until v0.2 first wave (paired with the cards loader v0.2 graduation per `pipeline/blueprint/v0.1/section_19_program_rule_packs.md`).
**Source authority:** Embedding Plan §A.3 P2-3 + §A.4 (Phase 3 docx triage feeds the v0.2 PRP body authoring). `Cards_Prompts_and_Research_Plans_v2_fused.md` §6 / §10 Program Rule Pack handoffs + master activation skill hard-rule #2.
**Reviewer entry points:** `_schema/program_rule_pack.schema.json` (frontmatter schema with v0.1 Red-Team-driven hardenings) · `_manifest/active_prps.yaml` (6 named PRPs targeted for v0.2 first wave) · `loader.py` (gate skeleton mirroring `pipeline/cards/loader.py` shape).

## What lives here

Live, time-versioned, citation-backed regulatory and program rules that change on a regulatory cycle independent of card content. Examples:

- 2 CFR 200 procurement-tier thresholds (Uniform Guidance)
- Build America, Buy America Act (BABA) material-content thresholds + waiver classes
- Davis-Bacon Act labor-compliance pathways + WH-347 cadence
- NEPA / HUD 24 CFR Part 58 environmental-review tier choices
- USDA Community Facilities rural-eligibility population thresholds
- USDA VAPG cycle-specific rubric weights + allowable-cost categories
- SBA SOP 50-10 current edition + 7(a) parameter ranges
- CDBG NOFO of record + statutory LMI thresholds
- FERPA / COPPA / FERPA-HIPAA-boundary for education-funding asks
- Subchapter T cooperative tax framework + state-cooperative statutory caps

## What does NOT live here

These belong elsewhere and importing them into a PRP is a discipline violation enforced at v0.2 by the F-PRP-COUPLING-VIOLATION + private-data gates:

| Belongs in | Not in PRP |
|------------|------------|
| **Cards** (`pipeline/cards/CIC/`, `pipeline/cards/CLC/`) | Durable underwriting grammar: reviewer dialect, narrative section patterns, fact-class taxonomies, evidence weights, common red flags, register defaults |
| **Org vault** (`orgs/<slug>/vault/`) | Per-applicant facts: EIN, UEI, addresses, budgets, signed letters, audited financials |
| **Funder Intelligence Database** (`pipeline/funder_intelligence/`, future) | Funder-specific roster: program officer names, reviewer compositions across cycles, award abstracts |
| **Out of scope** (parked at `research/future_horizons/`) | Transaction-processing infrastructure: PostgreSQL DDL for procurement ledgers, payment-flow state machines, audit-red-line enforcement-at-runtime |

The PRP/card boundary is enforced at research time by the master activation prompt's hard rule #2 (see `skills/tilth-card-research/SKILL.md`). At runtime in v0.2+, the F-PRP-COUPLING-VIOLATION gate in `loader.py` will enforce PRPs do not embed CIC↔CLC coupling fields, and the private-data-marker walker will reject PRPs that embed applicant-specific content. v0.1 Beta is honor-system on this discipline because the loader's top-level call raises `NotImplementedError`.

## Directory shape (on-disk)

```
pipeline/program_rule_packs/
├── README.md                                  # this file
├── _schema/
│   └── program_rule_pack.schema.json          # PRP frontmatter schema with Red-Team-driven hardenings
├── _manifest/
│   └── active_prps.yaml                       # active-PRP registry (6 entries, status: draft pending v0.2 first wave)
├── loader.py                                  # v0.1 scaffold; top-level raises NotImplementedError at v0.1
├── compliance_framework/                      # PRPs of kind compliance_framework (FERPA/COPPA, Subchapter T, etc.)
├── cross_cutting_regulation/                  # PRPs of kind cross_cutting_regulation (2 CFR 200, Davis-Bacon, NEPA, BABA)
├── program_specific/                          # PRPs of kind program_specific (USDA VAPG, USDA CF, SBA 7(a), CDBG annual NOFO, etc.)
└── overlays/                                  # cross-axis compliance overlays per Embedding Plan §A.4 (CIC-02 FERPA/COPPA, CIC-04 arts fiscal sponsorship, CLC-06 charter facilities)
```

The compliance_framework/, cross_cutting_regulation/, program_specific/, and overlays/ subdirectories receive PRP YAML bodies in Phase 3 docx triage authoring + per-cycle refresh. v0.1 Beta scaffold ships them as empty directories with the manifest declaring the 6 v0.2-first-wave targets.

## PRP categorization (three kinds)

Per `_schema/program_rule_pack.schema.json`'s `prp_kind` enum, every PRP declares one of three kinds:

| `prp_kind` | What it describes | Example |
|-------------|--------------------|---------|
| **compliance_framework** | A standing compliance regime that applies across many programs and rarely-if-ever expires. Example: FERPA / COPPA / Subchapter T. | TILTH-PRP-FERPA-COPPA-HIPAA, TILTH-PRP-SUBCHAPTER-T |
| **cross_cutting_regulation** | A federal-or-state regulation that flows down to every grant of a class. Example: 2 CFR 200 (Uniform Guidance), Davis-Bacon (federal construction), NEPA / 24 CFR Part 58. | TILTH-PRP-2CFR200, TILTH-PRP-DAVIS-BACON, TILTH-PRP-NEPA-24CFR58 |
| **program_specific** | A single program's cycle of record. Refreshes on the program's NOFO cycle. Example: USDA VAPG FY26, CDBG 2026, SBA SOP 50-10 current. | TILTH-PRP-USDA-VAPG-FY26 |

`cross_references.inherits_from` lets program-specific PRPs declare their flow-down. E.g. `TILTH-PRP-USDA-VAPG-FY26` will declare `inherits_from: TILTH-PRP-2CFR200` at v0.2 first wave authoring, indicating that 2 CFR 200's procurement tiers apply to every VAPG award.

## v0.2 first wave target roster (per `_manifest/active_prps.yaml`)

Six PRPs are declared in the manifest with `status: draft` + `content_hash: TBD`. v0.2 first wave authors the YAML bodies and runs the LOCK ceremony.

| Entry | `prp_kind` | Maps to Phased Audit synthesis recommendation |
|-------|------------|------------------------------------------------|
| TILTH-PRP-FERPA-COPPA-HIPAA | compliance_framework | #1 Decouple Student Profiles |
| TILTH-PRP-2CFR200 | cross_cutting_regulation | #4 Deploy Programmatic Compliance Locks (procurement) |
| TILTH-PRP-DAVIS-BACON | cross_cutting_regulation | #3 Automate Davis-Bacon Checking |
| TILTH-PRP-NEPA-24CFR58 | cross_cutting_regulation | #4 Deploy Programmatic Compliance Locks (NEPA) |
| TILTH-PRP-SUBCHAPTER-T | compliance_framework | #5 Enforce Cooperative Equity Rules |
| TILTH-PRP-USDA-VAPG-FY26 | program_specific | program-specific exemplar |

The roster intentionally undersized at six PRPs so the v0.2 first wave can validate the loader graduation + signing ceremony + Logician composition under realistic load before scaling to the Phase 3 docx triage's full ~10-pack target.

## How cards reference PRPs

Cards reference PRPs by `pack_slug` (or in the live manifest by `prp_id`) in their `compliance_burdens` (CIC) or `compliance_obligations` (CLC) field:

```yaml
# Example CIC card snippet (cooperative.yaml)
compliance_burdens:
  - regime: "subchapter_t_cooperative_tax"
    prp_id: "TILTH-PRP-SUBCHAPTER-T"          # pointer, not embedded content
    applies_when: "cooperative legal form + patronage allocation"
    burden_summary: "Patronage allocation mechanics + state-statute caps"
    # DO NOT embed specific allocation formulas, par-value caps, or
    # reserve percentages here. Those live in the PRP and refresh with
    # state statute amendments.
```

At runtime in v0.2+, Logician follows the `prp_id` pointer and resolves current-cycle thresholds from the PRP rather than from card content. v0.1 Beta is operator-aware honor-system.

## Refresh cadence

PRPs refresh on the regulatory cycle of their subject, not on Tilth's release cycle:

| `prp_kind` | Typical refresh trigger |
|------------|--------------------------|
| compliance_framework (FERPA, COPPA, Subchapter T) | Statutory amendment / agency rulemaking notice (multi-year typical) |
| cross_cutting_regulation (2 CFR 200, Davis-Bacon, NEPA, BABA) | DOL / OMB / CEQ rule changes (multi-year typical) |
| program_specific — USDA cycle packs (VAPG / LAMP / ARC) | Annual NOFO release (FY-cycle) |
| program_specific — SBA SOP 50-10 | Edition changes (multi-year typical) + parameter notices |
| program_specific — CDBG NOFO | Annual at minimum; CPD notice releases between |
| State packs (when authored) | State-specific cycle |

A PRP whose `last_verified_utc` is older than 12 months raises a warning at PRP-consumer time at v0.2+; older than 24 months fails closed at production load via F-PRP-EXPIRED.

## Authoring discipline

When authoring or refreshing a PRP at v0.2 first wave (or v0.2+ per-cycle):

1. **Cite primary sources.** Each rule statement gets a citation footnote with URL + access_date. CFR sections cite the eCFR URL with the current revision date.
2. **Mark uncertainty.** NEEDS_VERIFICATION on any rule the author could not confirm against primary source. NEEDS_OPERATOR_DECISION on any rule whose applicability depends on operator-side facts the PRP can't see.
3. **Distinguish federal text from agency interpretation.** Statutory text quotes verbatim; agency guidance summaries with attribution.
4. **No applicant-specific content.** PRPs are workspace-shareable; per-applicant material lives in `orgs/<slug>/vault/`. The schema's defense-in-depth `forbidden_law3_key_patterns` patternProperties block rejects keys matching the private-data markers list.
5. **No card-shaped content.** Reviewer dialect, narrative-section patterns, fact-class taxonomies, evidence weights belong in cards. If a regulatory document encodes one of these, it goes in the *card* with a citation back to the regulatory source, not in the PRP.
6. **Time-version explicitly.** Every PRP body block starts with the applicable cycle. When a rule changes, the old text is preserved in a "Historical text (deprecated YYYY-MM-DD)" section, not overwritten.
7. **Author against the schema.** Validate every authored body against `_schema/program_rule_pack.schema.json` before submitting for review.

## Lifecycle

```
draft (research session) → review_passed (operator review) → signed (LOCK ceremony) → runtime-loaded by Logician
                                                            ↓
                                              deprecated (when superseded by next cycle)
```

Mirrors the cards lifecycle. Deprecated PRPs are NEVER deleted — they are retained for historical-cycle reconstruction of past grant cycles' compliance posture. Deletion would break Archivist's renewal-evidence trail.

## v0.1 Beta scope boundary

At v0.1 Beta the substrate is **scaffolded but inert**:
- Schema is on disk and reviewable.
- Manifest declares 6 v0.2 first wave targets.
- Loader skeleton is on disk; the top-level call raises `NotImplementedError("v0.2 first wave")` so no PRP body is consumed in production.
- Card `compliance_burdens` / `compliance_obligations` entries are honor-system pointers; the operator validates them at LOCK ceremony but no runtime gate fires.

This matches the cards v0.1 Beta posture: substrate frozen, runtime injection deferred to v0.2. Cards and PRPs graduate at the same v0.2 ceremony.

## Phase 3 docx triage hand-off

The Phased Card System Research Audit (docs/phased_card_system_research_audit_extracted_2026-05-17.md) contains ~30 person-hours of regulatory research that maps onto this substrate. The triage decisions document at `pipeline/handoffs/phased_card_audit_triage_decisions_2026-05-17.md` (lands as part of this dispatch) routes each docx section to:

- a v0.2 first wave PRP body (extends one of the 6 manifest entries)
- a card content augmentation pass (CIC-01/02/04/05 + CLC-01/05/06/08 content deepening)
- a compliance overlay file at `overlays/`
- a parking-lot research note at `research/future_horizons/` (out-of-scope for grant-writing appliance)
