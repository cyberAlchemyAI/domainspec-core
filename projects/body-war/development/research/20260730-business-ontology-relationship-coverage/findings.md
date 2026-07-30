# Body War Business Ontology Relationship Coverage

## Exact answer

The current candidate-local package has **237 node files** after excluding
`nodes/manifest.json`, **231 explicit relation records**, **193 nodes incident
to at least one explicit relation**, and **44 explicit zero-degree nodes**.
There are **zero missing endpoints** and **61 weak components**: 44 singleton
isolates and 17 non-singleton components. Directed degree sums are
`in = 231` and `out = 231`. These measurements come from
`projects/body-war/ontology/business/nodes/*.json#/concept_id` and
`projects/body-war/ontology/business/relations/relations.json#/relations`; the
declared relation count is independently present at
`projects/body-war/ontology/business/relations/relations.json#/relation_count`.

No, every node does **not** need an explicit relation under the current
contract. The node contract has no incidence field
(`cyberAlchemy-v2/ontology/NODE-MODEL.md#Node Concept Contract`), the Body War
coverage contract requires kinds, named concepts, predicates, lifecycle
policies, and minimum counts rather than per-node degree
(`projects/body-war/ontology/business/profile.json#/coverage_contract`), and
current coverage validation computes no degree or component invariant
(`projects/body-war/ontology/business/scripts/validate.mjs:685-727`). A
universal-incidence rule would incorrectly reject useful standalone,
deferred, and lifecycle-policy vocabulary.

## What “related” means here

- **Explicitly related** means named as `source_concept` or `target_concept` in
  an admitted relation row:
  `projects/body-war/ontology/business/relations/relations.json#/relations/*`.
  This is the only meaning counted as graph degree.
- **Lifecycle-policy member** means named under
  `projects/body-war/ontology/business/lifecycle-policies/*.json#/state_concepts`.
  It is typed lifecycle structure, but not an explicit relation row.
- **Source-bound**, **branch-included**, **residue-affected**, and
  **challenge-referenced** refer respectively to node `#/source_refs`,
  `#/branch_roles`, residue `#/items/*/affected_concepts`, and node
  `#/challenge_contract`. They are provenance, view, routing, or challenge
  surfaces—not relation incidence.
- A **candidate endpoint association** says that current source bytes place two
  concepts in one domain object. It is not a relation unless predicate,
  direction, owner, evidence, authority effect, value effect, cycle policy,
  and collapse boundary are all admitted. That full requirement is owned by
  `projects/body-war/ontology/business/schemas/relation.schema.json#/required`
  and `cyberAlchemy-v2/ontology/RELATION-MODEL.md#Endpoint Rule`.

## Reproducible count

From repository root: sort all `.json` files in
`projects/body-war/ontology/business/nodes/`, remove `manifest.json`, parse
their `#/concept_id`, then parse
`projects/body-war/ontology/business/relations/relations.json#/relations`.
Initialize `(in,out)=(0,0)` for every concept; increment the source out-degree
and target in-degree for each row while asserting that both endpoints exist.
Nodes with `in + out == 0` are the 44 isolates. Add each relation in both
directions to an adjacency map and run DFS from every unseen node to reproduce
the 61 weak components. This method also yields 231 increments on each directed
side and zero missing endpoints. Current endpoint enforcement is visible at
`projects/body-war/ontology/business/scripts/validate.mjs:309-371`.

## Complete isolate classification

This is a research classification, not a deployed rule. Exactly one primary
disposition is assigned using this precedence:
`SOURCE-DEFECT`, `ASSOCIATION-REVIEW`, `OWNER-DECISION`, `DEFERRED`,
`POLICY-MEMBER`, `STANDALONE`.

### `POLICY-MEMBER` — 24; keep as-is

These nodes are explicit-relation isolates but named lifecycle-policy members:

- activity: `state.activity.empty`, `.loading`, `.not-loaded`,
  `.provider-error`, `.ready`
- auth: `state.auth.error`, `.unconfigured`
- challenge/controller: `state.challenge.expired`,
  `state.controller.expired`
- evidence candidate: `state.evidence-candidate.accepted`,
  `.operator-review`, `.rejected`, `.submitted`
- geometry candidate: `state.geometry-candidate.rejected`, `.superseded`
- geometry: `state.geometry.draft`, `.missing`, `.placeholder`,
  `.source-backed`, `.validated`
- score preview: `state.score-preview.blocked-geometry`, `.blocked-policy`,
  `.superseded`
- suggested track: `state.suggested-track.retired`

All IDs above carry the prefix `body-war.business.`. Their exact membership is
at:

- `projects/body-war/ontology/business/lifecycle-policies/activity.json#/state_concepts`
- `projects/body-war/ontology/business/lifecycle-policies/auth.json#/state_concepts`
- `projects/body-war/ontology/business/lifecycle-policies/challenge.json#/state_concepts`
- `projects/body-war/ontology/business/lifecycle-policies/controller.json#/state_concepts`
- `projects/body-war/ontology/business/lifecycle-policies/evidence-candidate.json#/state_concepts`
- `projects/body-war/ontology/business/lifecycle-policies/geometry-candidate.json#/state_concepts`
- `projects/body-war/ontology/business/lifecycle-policies/geometry.json#/state_concepts`
- `projects/body-war/ontology/business/lifecycle-policies/score-preview.json#/state_concepts`
- `projects/body-war/ontology/business/lifecycle-policies/suggested-track.json#/state_concepts`

These classes exist because lifecycle membership already supplies separate
typed meaning; no relation is inferred.

### `SOURCE-DEFECT` — 10; owner decision, P0

`premise.h-001`, `.h-002`, `.h-003`, `.h-004`, `.h-005`, `.h-006`, `.h-007`,
`.h-008`, `.h-009`, and `.h-010` (all prefixed `body-war.business.`) are
isolates whose node `#/definition` values disagree with their current
index-matched source rows. The node definitions are:

- `projects/body-war/ontology/business/nodes/premise.h-001.json#/definition`
- `projects/body-war/ontology/business/nodes/premise.h-002.json#/definition`
- `projects/body-war/ontology/business/nodes/premise.h-003.json#/definition`
- `projects/body-war/ontology/business/nodes/premise.h-004.json#/definition`
- `projects/body-war/ontology/business/nodes/premise.h-005.json#/definition`
- `projects/body-war/ontology/business/nodes/premise.h-006.json#/definition`
- `projects/body-war/ontology/business/nodes/premise.h-007.json#/definition`
- `projects/body-war/ontology/business/nodes/premise.h-008.json#/definition`
- `projects/body-war/ontology/business/nodes/premise.h-009.json#/definition`
- `projects/body-war/ontology/business/nodes/premise.h-010.json#/definition`

Compare them index-for-index with
`projects/body-war/docs/HYPOTHESES.md#H-001` through `#H-010`; the node
`#/source_refs/0/sha256` values match the current source digest
`b7dea56637909e03b0e73bf96e572e6f68f872ee05bb7204241708882cdb703d`.
The generated definitions are also visible at
`projects/body-war/ontology/business/authoring/catalog.mjs:401-420`.
`body-war.product-ontology-owner` must reconcile meaning and source binding
before any relation review. Relations are not a repair.

### `STANDALONE` — 6; keep as-is

`value.activity-sport-type`, `value.badge`, `value.geometry-status`,
`value.league`, `value.reference-time`, and `value.zone-type` are useful typed
vocabulary, but current evidence selects no unique predicate and endpoint
pair. Evidence and meaning remain explicit at:

- `projects/body-war/ontology/business/nodes/value.activity-sport-type.json#/definition`
  and `#/source_refs/0`
- `projects/body-war/ontology/business/nodes/value.badge.json#/definition` and
  `#/source_refs/0`
- `projects/body-war/ontology/business/nodes/value.geometry-status.json#/definition`
  and `#/source_refs/0`
- `projects/body-war/ontology/business/nodes/value.league.json#/definition` and
  `#/source_refs/0`
- `projects/body-war/ontology/business/nodes/value.reference-time.json#/definition`
  and `#/source_refs/0`
- `projects/body-war/ontology/business/nodes/value.zone-type.json#/definition`
  and `#/source_refs/0`

No change is proposed.

### `ASSOCIATION-REVIEW` — 1; proposed association, no relation

`value.privacy-consent` and `entity.runner-confirmation` have a source-backed
endpoint association: the journey object carries `consentVersion`,
`consentText`, and `geometryUseAcknowledged`
(`projects/body-war/development/invoke-runs/20260728T055629Z-login-suggest-track-score-preview/SPEC.md#RunnerConfirmation`;
current SHA-256
`55a0969eddebcadafc7c43601ded0be754065723353e389594fdd37bb127a185`).
The value node binds that selector at
`projects/body-war/ontology/business/nodes/value.privacy-consent.json#/source_refs/0`.
The source does not choose a predicate or direction. Therefore **no typed
relation, value effect, cycle policy, or validator repair is proposed**.

### `DEFERRED` — 1; keep as-is

`actor.city-community-operator` is useful deferred vocabulary. Its node
definition and status are at
`projects/body-war/ontology/business/nodes/actor.city-community-operator.json#/definition`
and `#/candidate_status`; its source is
`projects/body-war/docs/INITIAL-DEFINITIONS.md#Pilot Operations`. It needs no
current edge.

### `OWNER-DECISION` — 2

`actor.product-team` and `context.run-validation-anti-cheat` are useful
source-backed concepts, but their sources do not select a unique predicate or
target. See
`projects/body-war/ontology/business/nodes/actor.product-team.json#/definition`,
`#/source_refs/0`, and
`projects/body-war/ontology/business/nodes/context.run-validation-anti-cheat.json#/definition`,
`#/source_refs/0`. Their current `#/owner_route` is
`body-war.product-ontology-owner`; any additional co-owner must be selected,
not inferred.

The complete partition is `24 + 10 + 6 + 1 + 1 + 2 = 44`.

## Unimplemented policy recommendations

The owner may later adopt a **review-classification completeness policy**:
every explicit-relation isolate gets one primary disposition under the
precedence above, plus optional evidence labels that never count as edges. A
profile-owned registry could then support missing, unknown, and
duplicate-primary diagnostics and tests for each disposition plus one
unclassified failure. Existing endpoint validation must remain relation-local.
These are unimplemented recommendations, not current admission law; the
absence of such diagnostics is visible in
`projects/body-war/ontology/business/receipts/validation-receipt.json#/diagnostic_contract`.

## Verdict matrix

| Candidate | Ownership / precedent | Witnessed non-vacuity | Definitional soundness | Verdict |
|---|---|---|---|---|
| Keep 24 lifecycle-policy members edge-isolated | Existing lifecycle files own membership; no relation precedent | 24 current zero-degree witnesses | Policy membership remains distinct from graph incidence | **KEEP AS-IS** |
| Keep six vocabulary nodes and deferred operator | Current node/source contracts | Seven current witnesses | Standalone/deferred does not mean unrelated in every sense | **KEEP AS-IS** |
| Repair ten premise definitions | `body-war.product-ontology-owner`; authored catalog and source rows | Ten exact mismatches | Repairs meaning, not degree | **OWNER DECISION — P0** |
| Review product-team and anti-cheat context | Current node `#/owner_route` | Two source-backed isolates | Predicate and target remain unresolved | **OWNER DECISION** |
| Investigate privacy-consent association | Product ontology owner; relation contract still unsatisfied | Two source-backed endpoints, no selected predicate | Association is not an edge | **PROPOSED ASSOCIATION ONLY** |
| Require every node to have an edge | No current contract or validator precedent | Killed by useful standalone, deferred, and policy-member isolates | Collapses distinct meanings of related | **REJECT** |
| Add classification registry/diagnostics/tests | New product ontology owner decision | Concrete 44-node corpus and proposed test cases | Classifies review status without synthesizing edges | **UNIMPLEMENTED RECOMMENDATION** |

## Boundary

The package remains `candidate-local`, with `authority_effect: none` and
`release_admission: not-granted`
(`projects/body-war/ontology/business/receipts/validation-receipt.json#/ontology_status`,
`#/authority_effect`, `#/release_admission`). These findings authorize no
ontology, schema, validator, test, application, projection, promotion, release,
runtime, production, or authority mutation.
