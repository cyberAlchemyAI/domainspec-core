# Funder Intelligence Database (FID) — deep-domain lattice

**Created:** 2026-05-16 (Phase 1 kickoff)
**Anchor:** Monday 2026-05-18 (operator-confirmed §11.1)
**Authority:** `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md`
**Companion:** existing `vault_shared/funder_intelligence/` (Scout per-doc corpus storage from architecture v7.0.5; this lattice consumes that corpus but is a separate abstraction layer)

## What this is

The canonical lattice for deep-domain funder-side knowledge. Cards (`pipeline/cards/`) become smart pointers into this lattice; depth lives here, not in cards.

Four artifact families:

- `funders/<funder_id>.yaml` — agency / foundation / intermediary level
- `programs/<program_id>.yaml` — program × cycle keyed (e.g., `USDA-RD-RBDG-FY26.yaml`)
- `compliance_cascades/<framework>.yaml` — cross-cutting frameworks (2 CFR 200, Davis-Bacon, Single Audit, etc.)
- `reviewer_heuristics/<reviewer_type>.yaml` — per-reviewer-type patterns (federal program officer, foundation program officer, peer reviewer academic, etc.)

## How content gets here

Every artifact passes through the **four-pillar methodology** (per planning doc §3):

1. **Pillar 1 — Depth Charter** (operator-Ed25519-signed; template at `_templates/depth_charter_template.md`).
2. **Pillar 2 — Primary-source corpus** in `_research_corpus/<artifact_id>/` with URL + access date + SHA256 hash discipline.
3. **Pillar 3 — Extraction + structuring** (LLM-assisted extraction of facts FROM the corpus INTO structured YAML — NOT grant drafting; Logician `F-FID-FACT-ORPHAN` PRE-gate fails closed on any fact without a corpus pointer).
4. **Pillar 4 — Field-test calibration** (three tracks — see `_calibration/`). **DORMANT** as of 2026-05-16 per operator scope correction (no grant drafting active). Phase-1 active scope = Pillars 1-3 only.

## Anti-fabrication discipline (non-negotiable)

- Every fact carries `corpus_ref: <artifact_id>:<filename>:<page_or_line>` + ≤2-sentence verbatim quote.
- `_note: "NEEDED — research or review"` is the only legitimate "we don't know yet" marker.
- Primary sources only. No secondhand summaries.
- See `_research_corpus/README.md` for corpus management.

## Signed-asset pattern

- Publisher Ed25519 keypair operator-controlled. Public key pinned at `vault_shared/funder_intelligence/publisher_pubkey.signed.yaml` (mirrors v7.0.7 §6.1 router-template + §17 v1 §17.6 Coefficient Registry + Cards `vault_shared/cards/publisher_pubkey.signed.yaml` byte-for-byte).
- Per-artifact `ed25519_signature` over canonical-JSON-bytes (`sort_keys=True`, `separators=(',', ':')`, UTF-8, `ensure_ascii=False`, signature field excluded from canonical computation).
- Loader fails closed via `F-FID-SIGNATURE-INVALID` (per planning doc §2.2; predicate body lands at follow-on §4 v2.x.z amendment when first artifact LOCKs).
- Quarterly republish cadence; out-of-cycle hot-patches signed individually.

## Three-tier classification (inherited from Tilth)

- **Tier-1 commons** — public-source-only content (statutory cites, NOFO text, public 990-PFs, FOIA-returned rubrics). Stage-5 cooperative-readable.
- **Tier-2 operator-derived + opt-in shareable** — analyses, reviewer-heuristic syntheses, funder-officer-relationship notes.
- **Tier-3 my-eyes-only forever** — personal funder-officer communications, individual relationships.

Same vocabulary as Tilth substance classification (architecture v7.0.10). Same enforcement primitives.

## Failure-code family (forward-declared)

The `F-FID-*` family (eight codes per planning doc §2.2) realizes as a `§4 v2.x.z` follow-on amendment when the first FID artifact LOCKs. Not Phase-1 work.

| Code | Severity |
|------|----------|
| F-FID-SIGNATURE-INVALID | P0 |
| F-FID-FACT-ORPHAN | P0 |
| F-FID-CORPUS-HASH-MISMATCH | HIGH |
| F-FID-CLASSIFICATION-LEAK | P0 |
| F-FID-CROSS-ARTIFACT-COUPLING | HIGH |
| F-FID-STALE-RUBRIC | MED |
| F-FID-REVIEWER-HEURISTIC-FABRICATION | P0 |
| F-FID-COVERAGE-INCOMPLETE | META PRE-cycle |

## Consumers

| Component | Reads | When |
|-----------|-------|------|
| Scout DISCOVER | `funders/`, `programs/` | Opportunity discovery |
| Scout VERIFY | `programs/<program_id>.yaml` `endpoints` + `live_check_url` | Pre-CRITICAL-fit validation |
| Scribe | `programs/<program_id>.yaml` `rubric` + `reviewer_heuristics/*` + `funders/<id>.yaml` `dialect_notes` | Section drafting |
| Judge | `programs/<program_id>.yaml` `rubric.weighted_dimensions` + `compliance_cascades/*` | Scoring |
| Red Team | `reviewer_heuristics/<type>.yaml` `common_punishments` + `compliance_cascades/*` `failure_modes` | Adversarial probes |
| Logician | `compliance_cascades/*` `mandatory_gates` + `programs/<id>` `match_rules` | Deterministic PRE/POST gates |
| Report Generator | `programs/<id>` `post_award_obligations` + `commitment_extraction_pattern` | Reporting templates |
| Cards (CIC + CLC) | Field-level `funder_id` / `program_id` / `cascade_id` / `reviewer_type_id` resolved at load | Card load time |

## Phase 1 scope (weeks 1-8)

- Exemplar pair: **CIC-01 food_systems × CLC-03 operating_capacity**.
- 21 FID artifacts (8 funders + 6 programs + 3 cascades + 4 reviewer types).
- Methodology v1.0 doc filed to `_methodology/` at week 8.
- Smart-pointer migration applied to two cards (food_systems + operating_capacity); thesis_passed lifecycle UNTOUCHED.
- See `pipeline/handoffs/fid_phase_1_dispatch_plan_2026-05-16.md` for the dispatch plan.

## Cross-references

- Planning doc: `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md`
- Phase 1 dispatch plan: `pipeline/handoffs/fid_phase_1_dispatch_plan_2026-05-16.md`
- WPFA Coefficient Registry (signed-asset precedent byte-for-byte): `pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md`
- Architecture v7.0.7 white-glove Classification Review: `pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md`
- Architecture v7.0.10 three-posture routing: `pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md`
- Existing Scout per-doc corpus (v7.0.5): `vault_shared/funder_intelligence/README.md`
- Reviewer-heuristics seed (today's landing): `skills/scribe-ghostwriter/references/reviewer_heuristics.md`

## What is NOT here

- Per-client / per-applicant content (lives in `orgs/<slug>/`)
- KFR substrate (lives in `orgs/<slug>/vault/kfr/`)
- Scout's raw-doc corpus bytes (lives in `vault_shared/funder_intelligence/docs/`)
- Card content (lives in `pipeline/cards/`)
