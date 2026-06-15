# Operational branch carry-set (confirmed candidate)

Step `define-operational-branch` (`definitions-governance`). The node/edge/mutation types the
operational ontology branch carries, confirmed against the fanout. Status legend: **SB**
source-backed · **TD** telemetry-derivable (L3 candidate max) · **H** hypothesis (no source yet).
All items are candidate; none is promoted.

## Node types

| Node type | Carries | Basis | Max authority from evidence |
| --------- | ------- | ----- | --------------------------- |
| `route` / dispatch | a composed route over capabilities | SB (`*.dispatch.json`, 63) | L3 candidate |
| `capability` (sigil/spell) | an operating capability + its tier | SB (necronomicon, by-sigil) | L3 candidate |
| `invocation` | one capability run + outcome | TD (envelopes, 401 signals) | L1 reviewable |
| `prompt_contract` | a capability's input/output contract | SB (SKILL.md output contracts) | L3 candidate |
| `operational_discipline` | a recurring operating practice | SB (`DISCIPLINES.md`) | discipline ladder (feeds L5+) |
| `decision` | a gated operational choice | TD partial (decision-gate signals, dispatch gates) | L3 candidate |
| `workflow_gap` / `failure_mode` | an observed operating failure | TD (observer.workflow_gaps) | L0 evidence |
| `lesson` | a generalizable operating insight | TD sparse (workflow-reflect) | L3 candidate |
| `maintenance_trigger` | a condition that should prompt maintenance | TD (reflection_trigger, config thresholds) | L0 (thresholds are config) |
| `operational_policy` | a promoted operating rule (L5) | H (target of promotion) | L5 (only via PromotionRecord) |
| `operational_constitution` | the "how" governance set (L6) | H (the apex, the verdict's target) | L6 (Constitution Governance) |
| `operational_axiom` | the "why" invariant (L7) | H (rare apex) | L7 (Constitution Governance) |

## Edge types — REUSE the single edge catalog, do not invent

[SB DAG-AND-METRICS.md §3]. Applicable to the operational branch:

| Edge | Use in operational branch | Acyclic |
| ---- | ------------------------- | ------- |
| `triggers` | invocation/decision → next invocation; maintenance_trigger → maintenance | yes |
| `derived_from` | lesson/policy `derived_from` invocation+gap evidence | yes |
| `governed_by` | route/capability `governed_by` operational_policy/constitution | yes |
| `observed_by` | invocation `observed_by` a signal/metric | yes |
| `realized_by` | route `realized_by` capability | yes |
| `contradicts` | candidate policy `contradicts` another (blocks promotion) | no |
| `drifts_from` | observed operation `drifts_from` intended operating rule | no |

## Mutation types (what the branch records over time)

| Mutation | Stream today | Status |
| -------- | ------------ | ------ |
| route run recorded | envelopes / dispatch receipts | SB |
| capability invoked | sigil-invocations | SB |
| decision gated | decision-gate signals | SB (sparse) |
| reflection triggered | reflection-state, reflection_trigger | SB |
| gap found | observer.workflow_gaps | SB |
| discipline hardened | — | **H — no stream; new mutation type** |
| lesson promoted to policy/constitution | — | **H — no stream; requires PromotionRecord + owner** |

## Boundary (binding)

- Operational branch owns **agent-operation** knowledge. It does **not** own per-run denominators —
  that is `run-context` (B3). [SB RECONCILIATION.md §1]
- Telemetry items seed **L3 candidates only**; promotion past L3 needs Constitution Governance +
  ontology-harness review. [verdict conditions §2]
- `operational_discipline` nodes **feed** policy/constitution; they do not hold that authority. [verdict]
