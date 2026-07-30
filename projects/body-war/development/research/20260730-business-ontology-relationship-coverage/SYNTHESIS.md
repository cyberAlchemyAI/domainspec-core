# Candidate Synthesis

Status: reviewer input, not final findings  
Action: `spawn-0004`

## Exact Answer

The current candidate-local Body War business ontology has **237 node files**
after excluding `nodes/manifest.json`, **231 explicit relations**, **193 nodes
incident to at least one explicit relation**, and **44 explicit zero-degree
nodes**. All relation endpoints resolve. The graph has 61 weak components: 44
singleton isolates plus 17 non-singleton components. The existing contracts do
**not** require every node to have an explicit relation.

“Zero-degree” means a concept ID occurs in neither
`relations/relations.json#/relations/*/source_concept` nor
`#/relations/*/target_concept`. It must not be collapsed with lifecycle-policy
membership, branch-role inclusion, source provenance, residue impact,
challenge metadata, projection membership, runtime dependency, or authority
movement.

## Complete Classification

| Disposition | Exact nodes | Count | Reason / action |
|---|---|---:|---|
| Separate lifecycle-policy surface; explicit-edge isolation acceptable | `state.activity.empty`, `state.activity.loading`, `state.activity.not-loaded`, `state.activity.provider-error`, `state.activity.ready`; `state.auth.error`, `state.auth.unconfigured`; `state.challenge.expired`; `state.controller.expired`; `state.evidence-candidate.accepted`, `state.evidence-candidate.operator-review`, `state.evidence-candidate.rejected`, `state.evidence-candidate.submitted`; `state.geometry-candidate.rejected`, `state.geometry-candidate.superseded`; `state.geometry.draft`, `state.geometry.missing`, `state.geometry.placeholder`, `state.geometry.source-backed`, `state.geometry.validated`; `state.score-preview.blocked-geometry`, `state.score-preview.blocked-policy`, `state.score-preview.superseded`; `state.suggested-track.retired` | 24 | Each is named by one policy’s `#/state_concepts`. Membership is semantic lifecycle structure but is not an admitted relation row. Do not infer `transitions_to` edges from membership or state-label transitions. |
| Premise source-binding defect; do not relate or rely on current definitions | `premise.h-001` through `premise.h-010` | 10 | Node IDs/selectors and current source digest bind to `H-001`–`H-010`, but all ten node definitions express different premises. Owner must reconcile meaning first. |
| Intentional standalone vocabulary | `value.activity-sport-type`, `value.badge`, `value.geometry-status`, `value.league`, `value.reference-time`, `value.zone-type` | 6 | Sources establish useful values/types, but not a uniquely supported endpoint pair and predicate. No change. |
| Source-complete candidate relation | `value.privacy-consent` | 1 | Journey `SPEC.md#RunnerConfirmation` defines versioned consent data within existing `entity.runner-confirmation`; candidate: runner-confirmation `records` privacy-consent. Requires owner acceptance and a failing-then-passing validator/test witness. |
| Deferred but useful | `actor.city-community-operator` | 1 | Source explicitly preserves future city/community/pilot operation. No edge required now. |
| Useful concept; relation decision open | `actor.product-team`; `context.run-validation-anti-cheat` | 2 | Definitions are source-backed, but nearby ownership/scope prose does not select an unambiguous predicate and target. Owner decision required. |

Total: `24 + 10 + 6 + 1 + 1 + 2 = 44`; each isolate appears exactly
once.

## Premise Source-Binding Defect

The premise nodes are graph isolates, but graph isolation is not their primary
defect. Their current SHA-matching selectors point to hypotheses whose meanings
drifted away from the node definitions. Examples:

- H-001 node: physical-activity motivation; H-001 source:
  defense-after-loss behavior.
- H-003 node: Strava trust; H-003 source: clan obligations and solo-runner
  retention.
- H-010 node: operator review; H-010 source: notification urgency and premium
  conversion.

This is a P0 source/definition repair decision owned by
`body-war.product-ontology-owner`. Adding relations before repair would amplify
incorrect semantics.

## Privacy-Consent Candidate Edge

- source: `body-war.business.entity.runner-confirmation`
- predicate: `records`
- target: `body-war.business.value.privacy-consent`
- evidence:
  `projects/body-war/development/invoke-runs/20260728T055629Z-login-suggest-track-score-preview/SPEC.md#RunnerConfirmation`
- evidence SHA-256:
  `55a0969eddebcadafc7c43601ded0be754065723353e389594fdd37bb127a185`
- owner: `body-war.product-ontology-owner`
- authority effect: `none`
- value effect: `value-constraining`
- cycle policy: `acyclic`
- forbidden collapse: recording a versioned consent statement does not prove
  lawful provider access, geometry admissibility, implementation, runtime
  execution, lifecycle promotion, release admission, or production readiness.

No other isolate has evidence closing both endpoints and predicate. Therefore,
no other edge is proposed.

## Connectivity Policy Recommendation

Do not require universal explicit degree. The smallest defensible invariant is
a profile-owned **reviewed zero-degree disposition policy**:

1. Degree is calculated only from admitted relation rows.
2. Every zero-degree node has exactly one reviewed disposition:
   separate-surface membership, standalone vocabulary, deferred scope, source
   defect, open owner decision, or source-complete edge candidate.
3. Any required-incidence rule names affected kinds/concepts, exemptions,
   predicate/direction requirements, owner, diagnostics, and receipt
   representation.
4. Lifecycle, provenance, branch, residue, challenge, and projection
   references remain distinct and never satisfy explicit degree.
5. A proposed relation is admissible only with two existing endpoints,
   supported predicate, exact evidence binding, owner route, effects, cycle
   policy, forbidden collapses, and a validator/test witness.

`body-war.product-ontology-owner` owns a Body War profile policy. A
load-bearing CAV2-wide invariant additionally requires the CyberAlchemy v2
ontology governance route.

## Validator Recommendation

After owner approval:

- extend `profile.json#/coverage_contract` with the selected class-aware
  disposition contract;
- add validator diagnostics for unclassified or multiply classified
  zero-degree nodes;
- add tests covering one allowed standalone isolate, one lifecycle member, one
  source-defect disposition, one unclassified failure, and the privacy-consent
  relation only if accepted; and
- do not alter endpoint-validation semantics.

## Exact-Binding Matrix

| Claim | Current source and selector | Explorer return | Scope | Status |
|---|---|---|---|---|
| 237 nodes, 231 relations, 44 zero-degree, zero missing endpoints | `nodes/*.json` excluding `manifest.json`; `relations/relations.json#/relation_count` and `#/relations/*/{source_concept,target_concept}` | `research.md#agent-1--abramsky-samson` | Explicit graph only | Proved |
| All 44 classified; 24 lifecycle members | Lifecycle files `#/state_concepts`; node files `#/concept_id`, `#/business_kind`, `#/candidate_status` | Agents 1 and 3 | Graph vs lifecycle | Proved |
| No current explicit-degree requirement | `NODE-MODEL.md#Node Concept Contract`; node schema `/required`; `validate.mjs#validateNodeShape`; `profile.json#/coverage_contract`; `validateCoverage` | Agent 2 | Formal contract | Proved |
| Endpoint rule is relation-local | `RELATION-MODEL.md#Endpoint Rule`; relation schema `/required`; `validateRelationShape` | Agent 2 | Existing relation validity | Proved |
| Premise/source drift affects all ten | `nodes/premise.h-001.json`…`h-010.json` `#/definition` and `#/source_refs`; `docs/HYPOTHESES.md#H-001`…`#H-010`, SHA-256 `b7dea56637909e03b0e73bf96e572e6f68f872ee05bb7204241708882cdb703d` | Agent 3 | Meaning/provenance | Proved; repair decision open |
| Privacy-consent edge is source-complete but unapproved | Journey `SPEC.md#RunnerConfirmation`, SHA-256 `55a0969eddebcadafc7c43601ded0be754065723353e389594fdd37bb127a185`; existing endpoint nodes | Agent 3 | Candidate relation only | Candidate; owner/test gate open |
| Package remains non-authoritative | `receipts/validation-receipt.json` `/ontology_status`, `/authority_effect`, `/release_admission` | Agents 1 and 2 | Authority boundary | Proved: `candidate-local`, `none`, `not-granted` |

## No-Change Cases And Boundary

Retain the 24 lifecycle members as lifecycle-connected but relation-isolated;
retain the six standalone values; retain the deferred city/community operator;
do not invent relations for product-team or anti-cheat context; and do not
relate the ten premises before source-definition reconciliation.

Nothing here authorizes ontology mutation, promotion, runtime behavior,
release, or production.
