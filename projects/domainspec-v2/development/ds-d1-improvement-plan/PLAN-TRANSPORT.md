---
module: ds-d1-improvement-plan
feature_code: DSD1
status: draft
updatedAt: 2026-07-03
docType: plan-transport
---

# Plan Transport: DS-D1 Improvement Plan

## Invoke Summary

- Mode: plan.
- Target artifact: DomainSpec v2 DS-D1 meta-type authority maturity.
- Owner cycle: Invoke authors the plan; Task Session owns execution;
  definitions-governance owns DS-D1 promotion; validation-governance owns
  validator behavior; relationship authority owns DS-D8 changes.
- Output mode: split.
- Phase status: flag.

## Source Signals

| Signal | Used As |
| --- | --- |
| [DS-D1 category-boundary findings](../r3-research/ds-d1-metatype-category-boundary/findings.md) | Accepted staged-authority diagnosis and per-type risk map. |
| [Meta-type formalization work-pack](../meta-type-formalization/WORK-PACK.md) | Existing schema+fixture+validator convention and completed backend 14 state. |
| [Meta-type definitions work-pack](../meta-type-definitions/WORK-PACK.md) | Existing candidate approval path and root definitions route. |
| [Current DS-D1 registry](../../definitions/meta-types/meta-types.yml) | Machine read-model of current 14/25 mismatch and challenge/confirm contracts. |
| [Root DS-D8 authority](../../definitions/relationships/relationships.yml) | Active endpoint law that pressures DS-D1 types but does not define their formation. |
| [Craft current state](../../CRAFT.md) | Continuation state and open meta-type/UI residue. |

## Template/Profile Selection

- `implementation-layering`: selected because plan mode requires a global L0-L3
  boundary artifact.
- `work-pack`: selected because DS-D1 improvement needs executable SWUs and
  source anchors.
- `execution-pack`: selected because medium complexity needs wave choreography.
- Split task/wave files: selected because UI, Saga, backend hardening,
  validators, and closeout have different owners and write scopes.

## Dispatch Techniques

Selected: `sequence`, `scu_swu_reduction`, `recomposition_proof`,
`validation_loop`, `owner_boundary_check`, `authority_split_gate`,
`artifact_contract_bridge`, `execution_receipt_handoff`, `residue_ledger`,
`concrete_path_evidence`, `state_namespace_boundary`.

Full dispatch document: [ds-d1-improvement.dispatch.json](ds-d1-improvement.dispatch.json).

## Distill Result

Verdict: flag.

- Proposer claim: the smallest coherent first unit is a DS-D1 maturity
  ledger/read-model sync.
- Balancer objection: this does not itself improve schemas or validators.
- Reconciliation: accepted. It is still the right first unit because it prevents
  later implementation from baking in blurred authority.
- Pass: SWU-DSD1-001 is executable and recomposes into every later DS-D1
  improvement.
- Flag: UI-11 path and Saga fork require owner decisions before mutation.
- Pass: full category law is deferred and does not pollute the executable plan.

## Distill Closure And Recomposition

- Current smallest coherent unit: `SWU-DSD1-001`, align staged DS-D1 maturity.
- Closure: it has named inputs, write scope, done criteria, and validation.
- Recomposition: it unlocks UI decision, Saga fork, backend hardening, validator
  changes, and closeout by giving every later SWU the same status vocabulary.
- Deferred complexity: category laws, private derivation semantics, broad UI
  runtime behavior, and unselected UI/Saga branches.

## Next Route

`task-session` on [SWU-DSD1-001](WORK-PACK.md#swu-manifest), with context
selected from:

- `projects/domainspec-v2/development/r3-research/ds-d1-metatype-category-boundary/findings.md`
- `projects/domainspec-v2/definitions/meta-types/meta-types.yml`
- `projects/domainspec-v2/definitions/meta-types/meta-types.md`
- `projects/domainspec-v2/development/meta-type-definitions/CANDIDATES.md`
- `projects/domainspec-v2/development/meta-type-formalization/WORK-PACK.md`
- `projects/domainspec-v2/CRAFT.md`

## Unresolved Gaps

- `DEC-DSD1-UI11-PATH`: decide add UI schemas now, narrow 25-type claim, or
  keep an explicit deferral.
- `DEC-DSD1-SAGA-FORK`: decide Saga harden versus owner-routed
  collapse/deprecation.
- `GAP-DSD1-SEMANTIC-DEPTH`: backend 14 need deeper finite witnesses for some
  type claims.
- `GAP-DSD1-CATEGORY-LAWS`: category laws remain a future formalization route.
