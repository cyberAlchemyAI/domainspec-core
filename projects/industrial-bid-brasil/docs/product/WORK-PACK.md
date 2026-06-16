---
module: industrial-bid-brasil
version: seed
status: draft
updatedAt: 2026-06-11
docType: work-pack
---

# WORK-PACK: Industrial Bid Brasil

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Ready for L0 task-session execution. |
| complexity | medium | Crosses docs, data templates, scoring logic, and future app surface. |
| outputMode | single-file | Split task files can be added after L0. |
| executionPackRef | n/a | Not required until the build exceeds this seed scope. |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | Global layer decisions. |
| activeLayerWindow | L0 | Current objective is proof of deterministic decision support. |
| lastUpdatedAt | 2026-06-11 | Seed package creation date. |
| readinessProfile | pilot | Build toward one-contractor pilot readiness. |

## Objective Summary

Deliver a local-first L0 prototype path for Industrial Bid Brasil that turns the
seed intelligence into inspectable scorecards, data templates, and a deterministic
opportunity report.

Success means one realistic opportunity can be loaded with organization data and
produce a bid/no-bid recommendation, missing-evidence list, buyer questions,
habilitation readiness, cost-confidence score, and submission checklist.

## Source Contracts

- [Wladimir intelligence extraction](../strategy/brazil_industrial_bid_intelligence_wladimir_2026-06-11.md)
- [Research strategy](../strategy/brazil_industrial_bid_research_strategy_2026-06-11.md)
- [MVP spec](MVP_SPEC.md)
- [Data requirements](DATA_REQUIREMENTS.md)
- [Scoring model](SCORING_MODEL.md)
- [Implementation layering](IMPLEMENTATION-LAYERING.md)

## Delivery Slices

| Slice ID | Outcome | Layer | Dependencies | Validation |
| --- | --- | --- | --- | --- |
| S-001 | Seed data templates are normalized and usable. | L0 | Current seed package. | Header review and one sample row per critical template. |
| S-002 | Opportunity and organization schemas are defined. | L0 | S-001, MVP spec. | Schema review against Wladimir seed rules. |
| S-003 | Deterministic scorecards are implemented. | L0 | S-002, scoring model. | Fixture produces expected blockers and flags. |
| S-004 | Local report surface exists. | L0 | S-003. | Report shows rationale, missing evidence, and next actions. |
| S-005 | Wladimir seed case validates the model. | L0 | S-004. | Human review notes captured. |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- |
| TASK-001 | Finalize data templates and seed examples. | L0 | low | DATA_REQUIREMENTS.md | ready | not-started |
| TASK-002 | Define JSON schemas for opportunity, organization data, and report output. | L0 | medium | MVP_SPEC.md, SCORING_MODEL.md | ready | not-started |
| TASK-003 | Implement deterministic scorecard engine. | L0 | medium | SCORING_MODEL.md | ready | not-started |
| TASK-004 | Build local report surface. | L0 | medium | MVP_SPEC.md | ready-after-TASK-003 | not-started |
| TASK-005 | Validate against Wladimir seed case and update scoring notes. | L0 | medium | Wladimir seed artifacts | ready-after-TASK-004 | not-started |
| TASK-VERIFY | Verify seed package and L0 prototype readiness. | L0 | low | all source contracts | ready-after-implementation | not-started |

## SWU Execution Handoff

| SWU ID | Parent Task | Source Anchors | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-IBB-001 | TASK-001 | DATA_REQUIREMENTS.md, data_templates | none | `data_templates/*`, `examples/wladimir_seed/*` | Templates have complete headers and one realistic seed row where useful. | Diff review and template checklist. | Manual CSV/header inspection. | local-fallback | ready |
| SWU-IBB-002 | TASK-002 | MVP_SPEC.md, SCORING_MODEL.md | SWU-IBB-001 | future `engine/schemas/*` | Opportunity, org-data, and report schemas exist. | Schema files and field mapping note. | JSON schema validation or review. | local-fallback | ready-after-001 |
| SWU-IBB-003 | TASK-003 | SCORING_MODEL.md | SWU-IBB-002 | future `engine/scorecards/*` | Composite and component scores run deterministically. | Fixture report with blockers and flags. | Unit test or deterministic CLI run. | local-fallback | ready-after-002 |
| SWU-IBB-004 | TASK-004 | MVP_SPEC.md | SWU-IBB-003 | future `app/*` or `reports/*` | User can inspect report without reading raw JSON. | Rendered report or HTML prototype. | Browser or static render check. | local-fallback | ready-after-003 |
| SWU-IBB-005 | TASK-005 | examples/wladimir_seed | SWU-IBB-004 | docs/product, examples | Wladimir seed case produces useful review notes. | Validation memo. | Human review checklist. | manual | ready-after-004 |

## Implementation Detail Notes

### TASK-002 Schema Logic

Inputs:

- opportunity source fields: object, quantities, deadline, contract, payment
  terms, penalties, site visit, technical specification
- organization records: certificates, atestados, equipment, labor, supplier
  quotes, historical bids, job actuals
- scoring config: component weights and blocker rules

Outputs:

- normalized opportunity object
- organization data pack object
- scorecard report object

Required behavior:

- preserve source references and confidence per field
- represent missing critical fields explicitly
- distinguish unknown, not applicable, and unavailable

### TASK-003 Scorecard Logic

Algorithm:

1. Evaluate hard blockers first.
2. Compute each component score with visible deductions.
3. Compute composite only when no critical blocker prevents scoring.
4. Select recommendation using thresholds and special rules.
5. Emit rationale and next action for every flag.

Edge cases:

- missing object or quantities blocks pricing confidence
- no site visit should not always block, but must lower confidence
- bad payment terms can override otherwise strong technical fit
- incomplete required planilha is eliminatory at submission stage

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action | Target Date |
| --- | --- | --- | --- | --- | --- |
| B-001 | product | Product name is not locked. | operator | Decide after L0 proof. | deferred |
| B-002 | data | No real contractor historical bid corpus yet. | operator | Collect from first pilot organization. | deferred |
| B-003 | pricing | Cost formulas are seed rules, not validated production formulas. | estimator | Validate against real job actuals. | L1 |

## Gate Checks

1. L0 can start because seed source contracts and templates exist.
2. Runtime execution should begin with one SWU, preferably `SWU-IBB-001`.
3. No public or private connector work should start before local scorecards are
   validated.
4. No pricing automation should ship without estimator review and job-actual
   validation.

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-06-11 | Initial invoked seed work-pack created. | Codex |
