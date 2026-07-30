# Revised Synthesis

Status: synthesis-review zig-zag 1/1; reviewer recheck input

## Exact answer

The candidate-local Body War business ontology contains:

- 237 node files, excluding `nodes/manifest.json`;
- 231 explicit relation records;
- 193 nodes incident to an explicit relation;
- 44 explicit zero-degree nodes;
- zero missing relation endpoints; and
- 61 weak components: 44 singleton isolates and 17 non-singleton components.

The directed degree sums are `in=231` and `out=231`.

An **explicit zero-degree node** is absent from every admitted relation row's
`source_concept` and `target_concept`. Lifecycle-policy membership, source
provenance, branch roles, residue impact, challenge metadata, projections,
runtime dependencies, and authority movement do not contribute to explicit
relation degree.

Current contracts do not require every node to participate in an explicit
relation. A universal-incidence rule is unsupported and contradicted by useful
standalone vocabulary, deferred concepts, and lifecycle-policy members that
are explicit-relation isolates.

## Research classification model

The recommendation is a **review-classification completeness policy**, not a
connectivity policy and not a current rule.

If the product ontology owner later adopts it, every explicit-relation isolate
would receive exactly one primary disposition. The first supported disposition
in this deterministic precedence would win:

1. `RCC-SOURCE-DEFECT`
2. `RCC-ASSOCIATION-REVIEW`
3. `RCC-OWNER-DECISION`
4. `RCC-DEFERRED`
5. `RCC-POLICY-MEMBER`
6. `RCC-STANDALONE`

Optional evidence labels may coexist without changing the primary disposition.
Examples are `lifecycle-policy-member`, `source-bound`,
`branch-role-present`, `deferred-source`, and
`candidate-endpoint-association`. Labels are evidence annotations, not graph
edges or alternate primary dispositions.

An adopted disposition record would need a stable disposition ID, exact
concept ID, explicit-relation-isolation scope, owner route, exact evidence path
and selector, review status, and optional evidence labels.

## Complete 44-node classification

### `RCC-POLICY-MEMBER` — 24

These are lifecycle-policy members and explicit-relation isolates. Exact
evidence is each applicable lifecycle file's `#/state_concepts`. No relation is
inferred.

`state.activity.empty`, `state.activity.loading`,
`state.activity.not-loaded`, `state.activity.provider-error`,
`state.activity.ready`, `state.auth.error`, `state.auth.unconfigured`,
`state.challenge.expired`, `state.controller.expired`,
`state.evidence-candidate.accepted`,
`state.evidence-candidate.operator-review`,
`state.evidence-candidate.rejected`,
`state.evidence-candidate.submitted`,
`state.geometry-candidate.rejected`,
`state.geometry-candidate.superseded`, `state.geometry.draft`,
`state.geometry.missing`, `state.geometry.placeholder`,
`state.geometry.source-backed`, `state.geometry.validated`,
`state.score-preview.blocked-geometry`,
`state.score-preview.blocked-policy`,
`state.score-preview.superseded`, `state.suggested-track.retired`.

### `RCC-SOURCE-DEFECT` — 10

`premise.h-001` through `premise.h-010`.

Their node definitions disagree with the current SHA-matching
`docs/HYPOTHESES.md#H-001` through `#H-010` selectors. The source SHA-256 is
`b7dea56637909e03b0e73bf96e572e6f68f872ee05bb7204241708882cdb703d`.
Reconciliation is P0 and is owned by `body-war.product-ontology-owner`.
Relations must not be used as a repair.

### `RCC-STANDALONE` — 6

`value.activity-sport-type`, `value.badge`, `value.geometry-status`,
`value.league`, `value.reference-time`, `value.zone-type`.

These are useful vocabulary nodes without evidence selecting a unique
predicate and endpoint pair. No change is proposed.

### `RCC-ASSOCIATION-REVIEW` — 1

`value.privacy-consent`.

Journey `SPEC.md#RunnerConfirmation`, SHA-256
`55a0969eddebcadafc7c43601ded0be754065723353e389594fdd37bb127a185`,
supports an owner-gated candidate endpoint association between
`entity.runner-confirmation` and `value.privacy-consent`. It does not resolve an
admitted predicate. No typed relation, direction, value effect, cycle policy,
or validator repair is proposed.

### `RCC-DEFERRED` — 1

`actor.city-community-operator`.

Its source explicitly preserves future city/community/pilot operation. It is
useful deferred vocabulary and needs no current edge.

### `RCC-OWNER-DECISION` — 2

`actor.product-team`, `context.run-validation-anti-cheat`.

These are useful source-backed concepts for which neither predicate nor target
is unambiguous. Their exact current owner is
`body-war.product-ontology-owner`. Any additional co-owner is unresolved and
must be explicitly selected, never inferred.

The partition sums to `24 + 10 + 6 + 1 + 1 + 2 = 44`.

## Unimplemented recommendations

The review-classification completeness policy, validator diagnostics, and
tests are research recommendations only. They are not deployed rules, current
admission law, or evidence that current validation violates its owned
contract.

If `body-war.product-ontology-owner` adopts the policy in a later governed
change, that change could consider a profile-owned disposition registry;
missing/unknown/duplicate-primary diagnostics; tests for each disposition and
an unclassified failure; and separate owner-gated investigation of the
privacy-consent endpoint association.

Existing endpoint validation must remain relation-local. No classification may
satisfy relation degree or synthesize an edge.

## Reviewer-fix closure

| Finding | Closure |
|---|---|
| Policy, diagnostics, tests, and failing-test gate are not deployed | All are explicitly unimplemented owner-decision research proposals. |
| Privacy-consent `records` edge is unsupported | Removed; only an endpoint association with unresolved predicate remains. |
| `lifecycle-connected` collapses policy and graph semantics | Replaced with `lifecycle-policy member and explicit-relation isolate`. |
| Exactly-one classification lacked overlap handling | One primary disposition uses deterministic precedence; optional evidence labels may coexist. |
| Product-team/anti-cheat co-owner was inferred | Exact current owner is the product ontology owner; any additional co-owner is unresolved. |
| Premise repair priority was unclear | Source-definition reconciliation is P0 and precedes any relation consideration. |

## Boundary

The ontology remains `candidate-local`, with `authority_effect: none` and
`release_admission: not-granted`. This synthesis authorizes no ontology,
schema, validator, test, application, Inventory, projection, promotion,
release, runtime, production, or authority mutation.

