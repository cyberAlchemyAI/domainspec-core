# Reviewer Returns

Status: first review pass; bounded synthesis-review zig-zag required

## Rittel — precedent and ownership

Verdict: `KEEP` with ownership corrections.

- No universal-degree rule is deployed. The node contract has no incidence
  field, endpoint validity is relation-local, and current Body War coverage is
  presence/count based.
- Projection precedent forbids a view from synthesizing relations.
- The disposition policy, validator diagnostics, and tests are not deployed.
  They are proposals requiring a new
  `body-war.product-ontology-owner` decision.
- Premise reconciliation is build-from-owned under the authored catalog and
  product ontology owner.
- The privacy-consent association is build-from-owned, but the edge remains a
  new owner admission decision.
- A failing-then-passing test witness is a proposed review gate, not current
  relation-admission law.

Exact evidence cited by the reviewer:

- `cyberAlchemy-v2/ontology/NODE-MODEL.md#Node Concept Contract`
- `cyberAlchemy-v2/ontology/RELATION-MODEL.md#Endpoint Rule`
- `projects/body-war/ontology/business/profile.json#/coverage_contract`
- `projects/body-war/ontology/business/scripts/validate.mjs:685-727`
- `projects/body-war/ontology/business/authoring/catalog.mjs:59-73,401-420`
- `projects/body-war/ontology/business/schemas/relation.schema.json`

## Popper — non-vacuity and reproduction

Verdict: `FIX`.

- Independent current-byte enumeration reproduced 237 node files after
  excluding `manifest.json`, 231 relations, 193 incident nodes, 44 explicit
  isolates, 61 weak components, degree sums `in=231/out=231`, and zero missing
  endpoints.
- Exactly 24 isolates are lifecycle-policy members. A concrete witness is
  `state.activity.empty`: degree `(0,0)` while named under
  `lifecycle-policies/activity.json#/state_concepts`.
- Every proposed disposition has a concrete witness.
- A universal degree rule is killed by useful standalone, deferred, and
  lifecycle-policy-member isolates.
- The privacy-consent typed edge is killed as a repair: the source does not
  select `records`, and no failing-then-passing validator/test exists.
- A disposition validator is retained only as an owner-decision research
  proposal because current validation has no degree/disposition witness.

The reviewer ran:

```sh
node --test projects/body-war/ontology/business/tests/business-ontology.test.mjs
node projects/body-war/ontology/business/scripts/validate.mjs --check
```

Both passed, but neither tests zero-degree disposition or the proposed edge.

## Wittgenstein — definitional soundness

Verdict: `FIX / BLOCK` until corrected.

- Keep `explicit zero-degree` defined only from admitted relation endpoints.
- Keep the rejection of a universal incidence rule.
- Replace `lifecycle-connected` with `lifecycle-policy member and
  explicit-relation isolate`.
- Rename the proposal to a `review-classification completeness policy`.
  Multiple supporting labels may coexist, so the policy must either use one
  explicit primary disposition plus labels or define deterministic precedence.
- Kill `source-complete privacy-consent edge`. The source backs an endpoint
  association, but does not select `records` over another admitted predicate
  such as `contains`.
- No persistence, runtime, implementation, promotion, release, or authority
  effect follows.

Exact evidence cited by the reviewer:

- `projects/body-war/ontology/business/scripts/validate.mjs:309,685`
- `projects/body-war/ontology/business/profile.json:72`
- `cyberAlchemy-v2/ontology/NODE-MODEL.md:12`
- `cyberAlchemy-v2/ontology/RELATION-MODEL.md:13`
- `projects/body-war/development/invoke-runs/20260728T055629Z-login-suggest-track-score-preview/SPEC.md:55`
- `projects/body-war/ontology/business/schemas/relation.schema.json:29`
- `cyberAlchemy-v2/ontology/PACKAGE-MODEL.md:45`

