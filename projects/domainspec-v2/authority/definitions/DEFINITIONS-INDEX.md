# DomainSpec v2 — Authority Definitions Index

Lookup layer for [DEFINITIONS.md](DEFINITIONS.md) (governance vocabulary, `DSV2-D*`). Last updated: 2026-07-01.

| ID | Term | Status | Cites (cav2, owned) | One-line |
| --- | --- | --- | --- | --- |
| [DSV2-D1](DEFINITIONS.md#dsv2-d1-edge-law-admissibility) | edge-law admissibility | active | CAV2-D22 / D29 / D16 | An edge earns its type iff it composes into different code; source-widen OK, target-change overload. |
| [DSV2-D2](DEFINITIONS.md#dsv2-d2-executable-typed-graph) | executable typed graph | active | — | The spec as nodes (taxonomy) + edges (edge-law) + composability, governed by layering/validation/drift. |
| [DSV2-D3](DEFINITIONS.md#dsv2-d3-two-plane-boundary) | two-plane boundary | active | — | Ontology on the authoring plane, derivation on the contract plane; authority flows contract→authoring only. |

## Aliases
| Alias | Canonical |
| --- | --- |
| edge-type admissibility · composes-differently test | DSV2-D1 |
| spec-as-graph · node/edge/realization decomposition | DSV2-D2 |
| authoring-vs-contract plane · ontology-lens boundary | DSV2-D3 |

## Boundaries
- **Governance vocabulary only.** Spec-level domain terms (`DS-D1` meta-types, `DS-D2` edge verbs) belong
  in `impl/spec/DEFINITIONS.md` (pending reformulation R7), not here.
- **References, never redefines** cav2 `CAV2-D*`.
- Rules that *use* these terms live in the constitution (`../constitutions/`), not here.
