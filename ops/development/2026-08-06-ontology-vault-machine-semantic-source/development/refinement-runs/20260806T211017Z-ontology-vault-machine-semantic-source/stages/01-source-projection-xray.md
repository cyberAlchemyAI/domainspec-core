# Stage 01: Context Builder And Source-Projection X-ray

## Context Pack Summary

- Task: Refine Ontology Vault machine semantic source
- Mode: standard
- Files selected: 9
- Snippets selected: 21
- Obligation coverage: 100 percent
- Estimated noise ratio: 0.12
- Output index: stages/01-context-pack.json
- Handoff pack: none; parent-inline Refine evidence
- Strict coverage: pass
- Blockers: 0

## What Exists Now

1. The canonical Ontology Vault skill owns ontology-type selection, lifecycle
   distinctions, confidence and premise review, convention updates, runtime
   profiles, and promotion guardrails.
2. The development bundle owns a reusable candidate entry/relation model,
   lifecycle axes, PromotionRecord record-kind, fixtures, and deterministic
   validators.
3. Project-local profiles can point Ontology Vault at adopter sources and emit
   non-authority reports or projections.
4. Generated Codex and Claude packages mirror canonical Arcanum source.

## Hidden Missing Spine

The current pieces do not yet form this governed chain:

    authored machine semantic package
      -> schema-suite validation
      -> deterministic normalization
      -> normalized semantic model
      -> declared human, graph, and query projections
      -> source/compiler/output digest receipt
      -> owner admission or promotion route

The missing object is not another ontology entry taxonomy. It is the package,
compiler, projection, receipt, authoring, and migration contract around the
entry model already owned by Ontology Vault development.

## Source And View Ownership

| Surface | Current posture | Candidate responsibility | Forbidden inference |
| --- | --- | --- | --- |
| SemanticPackage | missing reusable contract | Authored, machine-readable, owner-scoped semantic source. | Parseable means authoritative. |
| SchemaSuite | partial candidate entry schema | Modular structural and cross-field validation. | Valid means true or promoted. |
| NormalizedSemanticModel | missing reusable contract | Canonical deterministic IR for queries and projections. | Derived IR is a second authored source. |
| HumanView | Markdown currently often hand-authored | Deterministic reader projection with source digest. | Reader edits silently write back. |
| GraphView / QueryView | project-local and candidate | Bounded projections from the same normalized model. | Projection adds ontology meaning. |
| ProjectionReceipt | missing reusable contract | Bind source, schema, compiler, output, warnings, and status. | Passing receipt promotes meaning. |
| Owner gate | already required in principle | Admit source semantics and later promotion explicitly. | Compiler or Ontology Vault decides authority. |

## Evidence Versus Inference

Known from owner sources:

- Ontology Vault convention mutation requires explicit approval.
- Runtime profile outputs are non-authority.
- The entry model separates lifecycle, claim role, governance outcome, bridge
  outcome, evidence confidence, and commitment confidence.
- PromotionRecord is the canonical governance decision record-kind, while the
  broader schema remains a governed candidate.
- Generated runtime packages are not canonical source.

Confirmed user direction:

- one machine-readable semantic source;
- human-readable views derived from that source.

Still candidate inference:

- the best authoring representation;
- the canonicalization algorithm;
- the exact modular schema boundaries;
- whether normalized JSON is authored source or derived IR;
- how long-form human explanation is stored without making Markdown parallel
  truth;
- the compatibility and migration contract.

## Architecture Guidance

Preserve six independent owners:

1. authored semantic source;
2. schema validation;
3. deterministic normalization;
4. view projection;
5. evidence receipts;
6. lifecycle admission and promotion.

Reuse the existing entry and lifecycle model. Add only the missing source and
projection spine. Do not solve adopter-specific schemas in the public contract.

## Excluded Context

- RWO ontology drift: private motivating evidence; its identity decision is
  paused and not selected here.
- CyberAlchemy v2 ontology details: private authority pressure evidence only.
- Generated skill mirrors: projections, not source.
- External standards: deferred until a concrete local gap appears and the user
  separately authorizes research.

## Gaps Routed Forward

- G1 representation selection -> Stage 4 tournament and Stage 5 Distill.
- G2 exact projection contract -> Stage 6 Invoke Design.
- G3 migration contract -> governance/migration specialist and Stage 6 Design.

## Validation

Strict obligation coverage passes. The pack contains no implementation,
promotion, public mutation, or runtime-readiness claim.
