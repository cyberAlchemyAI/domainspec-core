# Verbatim Explorer Returns

Dispatch:
`2026-07-30-body-war-business-ontology-relationship-coverage`  
Sheet SHA-256:
`fd1b1abd94aa3581a4cf1cca1a4192e496348191c47aa97c60448a0cf8212f19`

The sections below preserve the three explorer returns. They are research
inputs, not parent-approved findings.

## Agent 1 — Abramsky, Samson

## Verdict

Independent enumeration confirms the packet’s preliminary measurement:

- Actual node files: **237**, excluding `nodes/manifest.json`.
- Explicit relation records: **231**; `relations/relations.json#/relation_count` also equals 231.
- Distinct nodes used as an explicit source or target: **193**.
- Explicit zero-degree nodes: **44**.
- Missing source/target endpoints: **0**.
- Directed degree totals: `Σ out-degree = 231`, `Σ in-degree = 231`.
- Weakly connected components: **61**: 44 singleton isolates plus 17 non-singleton components sized `101,21,14,12,6,5,4,4,4,4,4,3,3,2,2,2,2`.

“Isolated” here means absent from every `relations/relations.json#/relations/*/{source_concept,target_concept}` endpoint. It does not mean absent from the package: all 44 have a business branch role and source provenance; 24 are lifecycle-policy members.

## Reproducible method

Run from repository root with Node:

```js
files = sort(readdir("projects/body-war/ontology/business/nodes"))
  .filter(f => f.endsWith(".json") && f !== "manifest.json");
nodes = files.map(JSON.parse);
relations = JSON.parse(readFile(".../relations/relations.json")).relations;
degree[id] = {in: 0, out: 0};
for (relation of relations) {
  assert(nodesById.has(relation.source_concept));
  assert(nodesById.has(relation.target_concept));
  degree[relation.source_concept].out++;
  degree[relation.target_concept].in++;
  undirectedAdjacency.addBothEndpoints(relation);
}
isolates = nodes.filter(n => degree[n.concept_id].in + degree[n.concept_id].out === 0);
components = DFS(nodesById.keys(), undirectedAdjacency);
```

Load-bearing pointers are:

- Node identity/kind/status: each listed node file at `#/concept_id`, `#/business_kind`, and `#/candidate_status`.
- Explicit endpoints: `relations/relations.json#/relations/*/source_concept` and `#/relations/*/target_concept`.
- Relation declaration: `relations/relations.json#/relation_count`.
- Secondary surfaces: each node’s `#/branch_roles`, `#/source_refs`, and `#/challenge_contract/{contradiction_edges,validation_edges}`; lifecycle files at `#/subject_concept` and `#/state_concepts`; `residue.json#/items/*/affected_concepts`.

## Degree and classification distributions

Total-degree histogram:

`0:44, 1:92, 2:37, 3:24, 4:15, 5:9, 6:7, 7:4, 8:1, 9:1, 10:2, 12:1`.

All-node business-kind distribution:

`actor 12; bounded_context 12; capability 18; entity 16; event 18; external_system 1; interface 4; ledger 1; lifecycle_state 58; metric 3; operation 32; outcome 2; policy 11; premise 10; query 17; value_object 17; workflow 5`.

All-node candidate-status distribution:

`blocked 29; candidate 31; deferred 12; reviewed-candidate 165`.

Zero-degree distribution:

- Kind: `lifecycle_state 24; premise 10; value_object 7; actor 2; bounded_context 1`.
- Status: `reviewed-candidate 27; candidate 15; deferred 2`.

Predicate distribution at `relations/relations.json#/relations/*/predicate`:

`awards 1; becomes 1; changes_state_of 1; consumes 24; contains 25; contests 2; controls 1; defends 1; depends_on 16; does_not_promote 2; exposes 10; governed_by 16; maps_to 2; owns 21; participates_in 4; produces 41; projects 2; provides 2; reads 22; records 4; supports 6; transitions_to 26; validates 1`.

## Complete isolate inventory

Every row has `(in,out)=(0,0)`, is branch-referenced by its own `#/branch_roles/0`, and is source-bound by at least `#/source_refs/0`.

| Class | Exact node files | Separate secondary references |
|---|---|---|
| Actors (2) | `nodes/actor.city-community-operator.json`; `nodes/actor.product-team.json` | No lifecycle or residue membership; no challenge edges |
| Bounded context (1) | `nodes/context.run-validation-anti-cheat.json` | No lifecycle or residue membership; no challenge edges |
| Premises (10) | `nodes/premise.h-001.json`; `h-002`; `h-003`; `h-004`; `h-005`; `h-006`; `h-007`; `h-008`; `h-009`; `h-010` | No lifecycle or residue membership; no challenge edges |
| Value objects (7) | `nodes/value.activity-sport-type.json`; `value.badge.json`; `value.geometry-status.json`; `value.league.json`; `value.privacy-consent.json`; `value.reference-time.json`; `value.zone-type.json` | No lifecycle or residue membership; no challenge edges |
| Activity states (5) | `nodes/state.activity.empty.json`; `state.activity.loading.json`; `state.activity.not-loaded.json`; `state.activity.provider-error.json`; `state.activity.ready.json` | Members of `lifecycle-policies/activity.json#/state_concepts` |
| Auth states (2) | `nodes/state.auth.error.json`; `state.auth.unconfigured.json` | Members of `lifecycle-policies/auth.json#/state_concepts` |
| Challenge state (1) | `nodes/state.challenge.expired.json` | Member of `lifecycle-policies/challenge.json#/state_concepts` |
| Controller state (1) | `nodes/state.controller.expired.json` | Member of `lifecycle-policies/controller.json#/state_concepts` |
| Evidence-candidate states (4) | `nodes/state.evidence-candidate.accepted.json`; `state.evidence-candidate.operator-review.json`; `state.evidence-candidate.rejected.json`; `state.evidence-candidate.submitted.json` | Members of `lifecycle-policies/evidence-candidate.json#/state_concepts` |
| Geometry-candidate states (2) | `nodes/state.geometry-candidate.rejected.json`; `state.geometry-candidate.superseded.json` | Members of `lifecycle-policies/geometry-candidate.json#/state_concepts` |
| Geometry states (5) | `nodes/state.geometry.draft.json`; `state.geometry.missing.json`; `state.geometry.placeholder.json`; `state.geometry.source-backed.json`; `state.geometry.validated.json` | Members of `lifecycle-policies/geometry.json#/state_concepts` |
| Score-preview states (3) | `nodes/state.score-preview.blocked-geometry.json`; `state.score-preview.blocked-policy.json`; `state.score-preview.superseded.json` | Members of `lifecycle-policies/score-preview.json#/state_concepts` |
| Suggested-track state (1) | `nodes/state.suggested-track.retired.json` | Member of `lifecycle-policies/suggested-track.json#/state_concepts` |

No isolate appears in `residue.json#/items/*/affected_concepts`. All node challenge arrays are empty across the package, so no isolate is challenge-referenced and none carries its own challenge edge. Branch-role and source-reference presence are metadata/provenance surfaces, not explicit graph edges. Lifecycle membership is a separate policy surface and must not be counted as relation degree.

## Corroboration and limits

`receipts/validation-receipt.json#/counts` independently records 237 nodes, 231 relations, and 11 lifecycle policies; its status is `pass`, ontology status is `candidate-local`, authority effect is `none`, and release admission is `not-granted`. The checked-in tests passed 6/6. The validator establishes endpoint validity and package constraints, but the reproduced zero-degree and component measurements come from current node/relation bytes, not from the receipt or Inventory.

The exact count falsification attempt therefore **did not falsify** the packet: 44 is current. This result does not classify an isolate as defective, invent an edge, or establish a universal-connectivity requirement.

## Agent 2 — Gadamer, Hans-Georg

## Formal contract verdict

A valid Body War business ontology node is **not currently required to participate in any explicit relation**. The node contract requires identity, meaning, classification, business-branch membership, provenance, ownership, candidate status, confidence, challenge metadata, residue, and collapse boundaries, but contains no relation-degree field or connectivity requirement. The package coverage contract is threshold-and-presence based: it requires selected kinds, concepts, predicates, lifecycle policies, and minimum total counts, not per-node degree or graph connectivity.

The current endpoint rule is relation-local: if a relation exists, both endpoints must be named and must resolve to existing concepts. It does **not** require every concept to be an endpoint, infer relations from other references, prove graph reachability, or establish that an endpoint pair is semantically sufficient.

## Claim-to-source matrix

| Claim | Exact source selector / pointer | Proof status |
|---|---|---|
| Candidate nodes do not have a relation-membership requirement. | `cyberAlchemy-v2/ontology/NODE-MODEL.md` § “Node Concept Contract”, lines 12–27; `projects/body-war/ontology/business/schemas/node.schema.json` JSON pointers `/required` and `/properties`; `scripts/validate.mjs` `validateNodeShape`, lines 252–307. Required node fields include `branch_roles`, `source_refs`, and `challenge_contract`, but no relation or degree field. | proved |
| A candidate relation must name source, target, direction, owner, evidence, authority effect, and collapse boundary. | `cyberAlchemy-v2/ontology/RELATION-MODEL.md` § “Relation Contract”, lines 13–26; Body War `schemas/relation.schema.json` `/required` and `/properties/source_concept`, `/properties/target_concept`, `/properties/direction`, `/properties/owner_route`, `/properties/evidence_refs`, `/properties/authority_effect`, `/properties/value_effect`, `/properties/cycle_policy`. | proved |
| The endpoint rule rejects incomplete relation candidates; it does not create a universal-connectivity rule. | `cyberAlchemy-v2/ontology/RELATION-MODEL.md` § “Endpoint Rule”, lines 73–77; `scripts/validate.mjs` `validateRelationShape`, lines 309–371, especially JSON-path diagnostics at `relation.source_concept` and `relation.target_concept`. The function is invoked only for relation records and contains no iteration over nodes to require incidence. | proved |
| Both relation endpoints must resolve to loaded concept IDs. | `scripts/validate.mjs` lines 345–357; test `business-ontology.test.mjs` lines 73–93 verifies `BWO_RELATION_ENDPOINT_MISSING`. | proved |
| Current coverage is presence/count based, not degree/component based. | `profile.json` `/coverage_contract`, lines 72–139; `scripts/validate.mjs` `validateCoverage`, lines 685–725. It checks business-kind membership, required concept IDs, predicate presence, policy IDs, `minimum_node_count`, and `minimum_relation_count`; it computes no degree, isolates, components, or reachability. | proved |
| Lifecycle-policy membership is a separate typed policy reference, not an explicit relation row. | `schemas/lifecycle-policy.schema.json` `/properties/subject_concept`, `/properties/state_concepts`, `/properties/transitions`; `scripts/validate.mjs` `validateLifecycle`, lines 400–464. Membership must reference existing concepts, but it is validated independently of `relations/relations.json`. | proved |
| Residue impact is routing metadata, not a graph edge. | `residue.json` `/items/*/affected_concepts`, `/items/*/owner_route`, `/items/*/next_gate`; `scripts/validate.mjs` `validateResidue`, lines 655–682. It ensures affected concepts exist and expressly preserves questions as fields. | proved |
| Business branch membership is an interpretive view, not ownership, authority, lifecycle, or an edge. | `profile.json` `/classification_axes/branch_role`; `cyberAlchemy-v2/ontology/BRANCH-AS-VIEW.md` § “Definition”, lines 6–10, § “Forbidden Collapses”, lines 36–42, and § “Use Rule”, lines 44–47; `scripts/validate.mjs` `validateBranch`, lines 576–607. | proved |
| `source_refs` are provenance bindings, not semantic adjacency. | `cyberAlchemy-v2/SOURCE-MAP.md` § “Ingest Rules”, lines 23–33; `scripts/validate.mjs` `validateSourceRefs`, lines 518–574. The validator checks declaration, digest, and current bytes, not graph endpoints. | proved |
| Node challenge fields preserve challenge semantics but are not admitted relation rows under the current Body War validator. | `NODE-MODEL.md` lines 29–34; `schemas/node.schema.json` `/properties/challenge_contract/properties/contradiction_edges` and `/validation_edges`; `scripts/validate.mjs` lines 273–284. These fields are checked only as string arrays; relation-ID existence, endpoint identity, and relation-contract fields are not checked there. Treat them as challenge metadata/references unless separately materialized in `relations/relations.json`. | proved |
| Ontology and projections model meaning but do not decide authority or runtime behavior. | `PACKAGE-MODEL.md` lines 7–19, 32–68, 83–88, 123; `AUTHORITY-KINDS.md` lines 6–10 and 37–45; `BRANCH-AS-VIEW.md` lines 36–47. | proved |
| Current package validation passes with 237 nodes and 231 relations without a connectivity diagnostic. | `receipts/validation-receipt.json` `/status`, `/counts`, `/diagnostic_contract`, `/ontology_status`, `/authority_effect`, `/release_admission`; current read-only test run passed 6/6. No isolation/connectivity diagnostic appears in the receipt contract. | proved |

## Reference-mechanism interpretation

- **Explicit semantic graph edges:** records in `relations/relations.json` satisfying the relation schema. These alone carry the complete endpoint/predicate/direction/evidence/effect contract.
- **Lifecycle-policy membership:** semantic lifecycle structure, but owned and validated as policy membership and transitions, not relation incidence.
- **Challenge contract fields:** challenge protocol metadata with semantic intent; under the present schema/validator they are unbound strings, not independently admitted relation records.
- **Residue `affected_concepts`:** unresolved-question scope and owner routing.
- **Branch roles/views:** interpretive inclusion and projection organization.
- **Source references:** provenance and byte binding.
- **Generated/read-model projections:** presentations of allowed candidate meaning; they cannot synthesize ontology edges or authority.

The selected Inventory leads agree with these distinctions only after source verification. The novice-comprehension findings require relation-local readings and prohibit synthesized relations (`findings.md` lines 199–210, 252–275). The ontology-prototype findings require explicit finite edge records with existing endpoints and `authority_effect: none`, while keeping projection and promotion separate (`2026-07-26.../findings.md` §§ “Current-state evidence boundary” and “Minimum finite contract and witness”). The login-to-score map is a candidate artifact and explicitly has no ontology or promotion effect (`ONTOLOGY-MAP.md` lines 119–123); its planning relationships are therefore source evidence for candidate modeling, not automatically admitted Body War relation rows.

## Exact validator gaps

1. No minimum or maximum explicit degree per node.
2. No rejection, classification, or allowlist for zero-degree nodes.
3. No weak/strong component or reachability invariant.
4. No rule requiring required concepts to participate in relations.
5. No per-kind connectivity policy.
6. No binding from `challenge_contract.{contradiction_edges,validation_edges}` to admitted relation IDs.
7. No rule equating or reconciling lifecycle, residue, branch, provenance, or challenge references with explicit relation connectivity—and such equality would collapse distinct contracts.
8. Coverage proves predicate presence globally, not that predicates connect appropriate classes or every relevant node.

## Owner decision required for any stronger invariant

Universal connectivity is neither required nor justified by current contracts. A stronger policy must first be selected by `body-war.product-ontology-owner`; if load-bearing across CAV2, it also needs the CyberAlchemy v2 ontology route and potentially schema governance/decision-gate.

The smallest defensible candidate is not “every node has an edge,” but a named, class-aware **explicit-connectivity policy** that states:

- which node kinds or named concepts must have explicit incidence;
- which kinds may remain standalone vocabulary;
- whether the measure covers only admitted relation rows;
- exemptions and their evidence/owner;
- whether direction, predicate family, or reachability matters;
- the diagnostic and receipt representation.

Adopting it requires changes to `profile.json`’s coverage contract and `scripts/validate.mjs`; changing the closed contract may also require corresponding schema and test updates. No edge should be inferred from lifecycle membership, source proximity, branch inclusion, residue impact, challenge strings, or product-flow prose.

Boundary: this interpretation does not authorize schema changes, relation creation, ontology promotion, runtime behavior, release admission, or production claims. The package remains `candidate-local`, `authority_effect: none`, and `release_admission: not-granted`.

## Agent 3 — Simon, Herbert

## Product/domain verdict

Current bytes reproduce **44 explicit zero-degree nodes** from 237 node files (excluding `nodes/manifest.json`) and 231 relations. The preliminary 24/10/7/3 grouping is numerically correct, but the product interpretation needs one material correction: the ten premise nodes are not presently trustworthy standalone hypotheses because their definitions do not match the current, hash-matching `H-001`–`H-010` source rows.

“Zero-degree” here means absent from every `relations/relations.json#/relations/*/{source_concept,target_concept}`. Lifecycle membership, source provenance, business-view inclusion, residue impact, and challenge metadata are separate surfaces, not explicit graph edges.

## Complete classification

| Classification | Nodes | Product judgment |
|---|---|---|
| Related through lifecycle-policy surface | 24 | Keep as explicit-edge isolates unless the owner separately chooses to model omitted transitions. Each is a named member of one lifecycle policy, so it has domain meaning without requiring a fabricated relation. |
| Redundant/unjustified in current form | 10 | The premise node IDs point to real hypothesis selectors, but their definitions disagree with those selectors. Repair source binding/meaning before considering premise-to-domain relations. |
| Intentional standalone vocabulary | 6 | Useful domain vocabulary whose cited sources define values/types, but current evidence does not establish a required typed graph edge. |
| Likely missing explicit typed relation | 1 | `value.privacy-consent` is structurally part of `RunnerConfirmation` in the journey SPEC; a source-complete candidate edge is available below. |
| Deferred but still useful | 1 | `actor.city-community-operator` explicitly describes deferred city/community/pilot operations. |
| Useful owner/organizational concept; relation decision open | 2 | `actor.product-team` and `context.run-validation-anti-cheat` have source-backed definitions, but their nearby ownership/scope prose is insufficient to select a schema predicate without an owner decision. |

### 24 lifecycle-policy members

- `activity.json#/state_concepts`: `state.activity.empty`, `.loading`, `.not-loaded`, `.provider-error`, `.ready`
- `auth.json#/state_concepts`: `state.auth.error`, `.unconfigured`
- `challenge.json#/state_concepts`: `state.challenge.expired`
- `controller.json#/state_concepts`: `state.controller.expired`
- `evidence-candidate.json#/state_concepts`: `state.evidence-candidate.accepted`, `.operator-review`, `.rejected`, `.submitted`
- `geometry-candidate.json#/state_concepts`: `state.geometry-candidate.rejected`, `.superseded`
- `geometry.json#/state_concepts`: `state.geometry.draft`, `.missing`, `.placeholder`, `.source-backed`, `.validated`
- `score-preview.json#/state_concepts`: `state.score-preview.blocked-geometry`, `.blocked-policy`, `.superseded`
- `suggested-track.json#/state_concepts`: `state.suggested-track.retired`

These are lifecycle-connected, not relation-connected. Their definitions and source selectors occur in each exact node file under `nodes/`, while policy membership is independently recorded at the pointers above. Some look like omitted terminal/error transitions, but the policy transition records use state labels rather than concept IDs and do not alone authorize new `transitions_to` edges.

### 10 premise nodes: current source-binding defect

Files `nodes/premise.h-001.json` through `premise.h-010.json` cite `projects/body-war/docs/HYPOTHESES.md#H-001` through `#H-010` with the correct current SHA-256 `b7dea566…cdb703d`, yet their definitions are different claims.

Examples:

- Node H-001 says gamification increases physical-activity motivation; source H-001 says runners return to defend after a loss event.
- Node H-003 says Strava evidence improves trust; source H-003 concerns clan obligations and solo-runner retention.
- Node H-010 says local operator review supports pilot learning; source H-010 concerns notification urgency and later premium conversion.

This applies across all ten IDs. Classification: **redundant/unjustified as currently expressed**, pending owner-led reconciliation. Adding edges now would attach incorrect claims to otherwise valid concepts.

### 7 value objects

- Intentional standalone vocabulary:
  - `nodes/value.activity-sport-type.json` → `mappings.md#Strava Activity To RunActivity`
  - `nodes/value.badge.json` → `game-rules/SPEC.md#Badge`
  - `nodes/value.geometry-status.json` → `states.md#Geometry State`
  - `nodes/value.league.json` → `game-rules/SPEC.md#League`
  - `nodes/value.reference-time.json` → `game-rules/SPEC.md#Reference time`
  - `nodes/value.zone-type.json` → `game-rules/SPEC.md#Zone types`
- Likely missing relation:
  - `nodes/value.privacy-consent.json` → journey `SPEC.md#RunnerConfirmation`

The six standalone values remain useful as typed vocabulary even without graph degree. Prose proximity is not enough to decide whether they are consumed, governed, recorded, or projected.

### 3 other concepts

- `nodes/actor.city-community-operator.json`: **deferred but useful**; definition and `INITIAL-DEFINITIONS.md#Pilot Operations` explicitly preserve a future rollout/operator role.
- `nodes/actor.product-team.json`: **useful, relation open**; `PROJECT-OVERVIEW.md#Project Shape` supports scope ownership, but not an unambiguous relation predicate and target.
- `nodes/context.run-validation-anti-cheat.json`: **useful, relation open**; `INITIAL-DEFINITIONS.md#Run Validation and Anti-Cheat` supports the bounded context, but selecting `contains`, `governed_by`, or another predicate requires an owner decision.

## One source-complete candidate edge

Candidate only; owner review remains required:

- source: `body-war.business.entity.runner-confirmation`
- predicate: `records`
- target: `body-war.business.value.privacy-consent`
- evidence: `projects/body-war/development/invoke-runs/20260728T055629Z-login-suggest-track-score-preview/SPEC.md#RunnerConfirmation`, SHA-256 `55a0969e…7a185`
- owner: `body-war.product-ontology-owner`
- authority_effect: `none`
- value_effect: `value-constraining`
- cycle_policy: `acyclic`
- forbidden collapse: Recording the exact versioned consent statement does not prove lawful provider access, geometry admissibility, implementation, runtime execution, lifecycle promotion, or production readiness.

The source specifies `consentVersion`, canonical `consentText`, and affirmative `geometryUseAcknowledged`; both endpoint nodes already exist. No other isolate has equally complete endpoint-plus-predicate evidence in the inspected corpus.

## Priority decision matrix

| Priority | Decision | Owner |
|---|---|---|
| P0 | Reconcile all ten premise definitions against current `HYPOTHESES.md` before relating or relying on them. | `body-war.product-ontology-owner` |
| P1 | Review the `runner-confirmation records privacy-consent` candidate relation and add a validator/test witness only if accepted. | `body-war.product-ontology-owner` |
| P2 | Keep 24 lifecycle members explicitly classified as lifecycle-connected; do not synthesize graph transitions from membership alone. | lifecycle policy owners |
| P3 | Keep six vocabulary values and the deferred operator as no-change cases unless a current source supplies an exact typed relation. | `body-war.product-ontology-owner` |
| P4 | Decide whether product-team and anti-cheat-context ownership should be graph-modeled; predicate and target remain open. | product ontology owner plus relevant domain owner |

No universal “every node must have an explicit relation” rule is justified. A safer product policy is: every zero-degree node must have an explicit reviewed disposition—standalone vocabulary, separate-surface membership, deferred scope, source defect, or source-complete proposed relation—without equating those dispositions with graph connectivity.
