---
tags: [inventory, schema, relationship-invariant, search-sequence, v2-repo, promotion-guardrail, formalization]
node_type: query
is_session: false
layer: knowledge-governance
nature: reference
status: active
created: 2026-06-21
dispatch_id: 2026-06-21-schema-relationship-invariants
dispatch_type: lookup
working_folder: .arcanum/inventory/queries/2026-06-21-schema-relationship-invariants/
sources: [cyberAlchemy-v2/authority/definitions/, projects/framework-unification/, arcanum/definitions/, domainspec-lean-formalization/, domainspec-formalization/, .arcanum/inventory/]
---

# Schema And Relationship Invariant Search Sequence

Status: active inventory query
Owner: inventory + definitions-governance
Canonical effect: none

## Purpose

Use this sequence whenever CyberAlchemy v2 needs to search, review, or promote
terms around `schema`, `typed relation`, `relationship invariant`, edge
signatures, taxonomy, relation profiles, or graph admissibility.

The sequence makes later searches reusable:

1. inventory records the source ladder and durable selectors;
2. definitions-governance decides whether a term becomes canonical;
3. ontology-vault may later condense governed meaning;
4. generated inventory pages remain read models, not authority.

## Current Read

`schema` already has an Arcanum definition in
`arcanum/definitions/DEFINITIONS.md#def-arc-schema-schema`. CyberAlchemy v2
should not redefine it casually.

The likely CyberAlchemy v2 candidate is `relationship invariant`, but it
currently appears as a family of related rules:

- `CAV2-D16` typed coupling invariant: non-orthogonal dependencies must be
  explicit typed relations with endpoints, direction, relation kind, owner,
  evidence, and effect.
- DomainSpec `DS-D2`, `DS-D7`, and `DS-D8`: relation verbs live in typed edge
  families and an edge is valid only when its endpoint meta-types satisfy the
  declared signature.
- Framework-unification graph invariants: connection integrity, forbidden edges
  made unconstructible, claim not exceeding proof, and contract/schema
  non-collapse.
- Formalization evidence: typed objects and edge laws are carried by typing
  functors or sigma-valid edge witnesses; structural typing is not semantic or
  runtime correctness.

## Search Ladder

| Order | Source | Why Here | Selector Pattern | Output |
| --- | --- | --- | --- | --- |
| 0 | `.arcanum/inventory/index.md` and evidence sets | Avoid re-searching already mapped knowledge. | `schema`, `relationship`, `typed edge`, `ontology`, `v2-repo`, `promotion-guardrail` | Existing cards, exclusions, and gaps. |
| 1 | `cyberAlchemy-v2/authority/definitions/` | Check current local canon before importing source pressure. | `CAV2-D16`, `CAV2-D19`, `ledger`, `recursivity`, `orthogonality`, drift audit | Current promotion boundary and undefined terms. |
| 2 | `projects/framework-unification/` | First broad source family for system-level invariants and the pipeline/mechanism split. | `CONCEPT-MAP.md`, `connection integrity`, `forbidden edges`, `schema`, `residue`, `claim <= proof`, `typed-DAG` | Candidate invariant family and source-order hypotheses. |
| 3 | `arcanum/definitions/` | Canonical Arcanum/DomainSpec vocabulary for schema, taxonomy, and typed relationships. | `DEF-ARC-SCHEMA`, `DS-D1`, `DS-D2`, `DS-D7`, `DS-D8`, `RELATIONSHIPS.md`, `TAXONOMY.md` | Normative vocabulary and explanatory catalogs. |
| 4 | `domainspec-lean-formalization/` | More formal source pressure for schema/instance/tower and typed-edge admissibility. | `MetaType`, `EdgeLaw`, `tau`, `sigmaValid`, `EdgeRow.wellTyped`, `all_edges_well_typed`, `residue` | Formal constraints and proof-boundaries. |
| 5 | `domainspec-formalization/` | Earlier formalization for the smaller meta-type/edge-law core and meta-layer framing. | `MetaType`, `EdgeLaw`, `GeneralSchema`, `L7 Semantic Coherence`, `schema residue` | Historical/formal comparison. |
| 6 | repo-wide backstop | Catch scattered definitions only after the governed source ladder has run. | `rg` over non-generated source roots, excluding generated skill copies and build outputs | New candidates or drift to file as evidence cards. |

## Evidence Selectors From This Pass

| Selector | Source Ref | Relevance |
| --- | --- | --- |
| `schema-shape-not-authority` | `arcanum/definitions/DEFINITIONS.md#def-arc-schema-schema` | Schema validates shape but does not prove execution, promotion, or authority transfer. |
| `typed-edge-vocabulary` | `arcanum/definitions/DEFINITIONS.md#ds-d2-typed-relationship-system`, `arcanum/definitions/RELATIONSHIPS.md` | DomainSpec relation verbs are a closed typed vocabulary with explanatory examples. |
| `edge-signature-operator` | `arcanum/definitions/DEFINITIONS.md#ds-d8-edge-signature-operator` | Endpoint meta-types must match the relation signature. |
| `taxonomy-source` | `arcanum/definitions/TAXONOMY.md` | Meta-types are the typed node vocabulary used by relationship signatures. |
| `two-edge-catalog-warning` | `projects/framework-unification/CONCEPT-MAP.md#two-distinct-edge-catalogs-do-not-conflate-them` | Artifact-provenance edges and domain-concept edges must not collapse. |
| `framework-invariants` | `projects/framework-unification/CONCEPT-MAP.md#invariants-what-must-always-hold-across-the-graph` | Names connection integrity, contract/schema non-collapse, and forbidden-edge unconstructibility. |
| `dispatch-typed-dag-boundary` | `projects/framework-unification/layers/dispatch-composition-attack/research.md` | Step/wave relation edges and reopen loops are gated by typed-DAG decisions. |
| `sigma-admissibility` | `projects/framework-unification/layers/domainspec-language/development/refinement-runs/2026-06-08-lean-functor-validation/stages/s6-invoke-design/TRANSLATOR-DESIGN.md` | Candidate edges become well-typed only if sigma-valid; invalid edges become residue. |
| `formal-edge-law` | `domainspec-formalization/lean-formalization/DomainSpec.lean` | Earlier formal core exposes `MetaType`, `EdgeLaw`, typing functor, and general schema. |
| `schema-instance-dependence` | `domainspec-lean-formalization/docs/emergence-as-asymmetric-dependence.md` | Instances depend on schema; schema/instance dependence should not be flattened. |

## Candidate Synthesis

Do not promote this yet, but the candidate invariant is:

> A relationship may govern navigation, validation, promotion, inheritance, or
> execution only when its endpoints, direction, relation kind, owner/source,
> evidence, effect, and admissibility rule are explicit. If the relationship is
> a DomainSpec concept edge, its endpoint meta-types must satisfy the declared
> edge signature. If the relationship crosses CyberAlchemy authority surfaces,
> it must also satisfy the typed coupling invariant and name the owner route.

## Boundary Rules

- Do not collapse `schema` into `contract`.
- Do not collapse artifact-provenance edges into domain-concept edges.
- Do not treat a typed relation as automatic promotion.
- Do not use generated indexes or inventory pages as canonical definitions.
- Do not treat formal edge admissibility as runtime correctness.
- Do not introduce inheritance, override, promotion, or reopen edges without a
  relation profile and owner gate.

## Recommended Next Search

1. Create evidence-cards for the selectors above if `relationship invariant` is
   ready for promotion review.
2. Run definitions-governance on `relationship invariant` only after the
   evidence-cards distinguish it from `CAV2-D16`.
3. Keep `schema` as an Arcanum authority reference unless CyberAlchemy v2 needs
   a local subtype such as `authority schema` or `tower schema`.
4. Use this sequence before repo-wide `rg` in future definition searches.
