# Refine Seed Proposal: Ontology Vault Machine Semantic Source

Status: proposed; awaiting explicit strategy confirmation
Run ID: `20260806T211017Z-ontology-vault-machine-semantic-source`
Target capability: public Arcanum `ontology-vault`
Ontology Vault mode: `convention-update`
Ontology type: `knowledge-vault`
Selection source: inferred
Selection confidence: high
Authority effect: none

## User Direction

Refine Ontology Vault so ontology authors create one better-typed semantic
source in a machine-readable form and derive human-readable views from that
source. The refinement must improve schema quality, creation ergonomics,
projection determinism, and governance boundaries.

## Current Evidence-Bounded State

The current Ontology Vault already owns ontology-type routing, lifecycle and
confidence distinctions, branch-aware relations, project-local profiles,
PromotionRecord boundaries, and convention-update gating. Its development
package also contains a published candidate branch-aware schema, positive and
negative fixtures, and deterministic validators.

The missing reusable contract is the source/projection spine:

1. there is no admitted primary semantic-package format;
2. there is no canonicalization and digest contract for that package;
3. there is no deterministic compiler contract from semantic source to a
   normalized model;
4. there is no governed human-view projection contract with source and
   generator receipts;
5. there is no migration rule for existing Markdown-led ontology packages;
6. schema validity is not yet cleanly separated from semantic truth,
   promotion, and owner authority at this source/projection layer.

Inventory provides a useful non-authority precedent: `index.json` is its
primary machine catalog and `index.md` is a derived human catalog. This run
will test whether a stricter, ontology-owned version of that pattern is sound.

## Fixed Direction And Claim Ceiling

The refinement will preserve this direction unless a finite counterexample
shows it cannot work:

```text
owner-approved machine semantic source
  -> schema validation
  -> deterministic normalization
  -> normalized semantic model
  -> derived human, graph, query, and visualization views
```

"Primary machine source" does not mean "automatically authoritative." A
machine document becomes the source for a governed ontology package only
through the package owner's admission route. Parsing, schema validation,
normalization, compilation, or projection cannot promote meaning.

This run may produce a candidate convention update, candidate schemas,
projection contracts, fixtures, migration design, and a non-executed Work
Pack. It does not mutate or promote the public Ontology Vault package.

## Candidate Layer Model To Test

| Layer | Candidate object | Responsibility | Must not become |
| --- | --- | --- | --- |
| S0 | `SemanticPackage` | Owner-scoped machine-readable source manifest and module set. | Automatic ontology authority. |
| S1 | `SchemaSuite` | Structural and cross-field validation for the core plus selected ontology type/profile. | A truth or promotion engine. |
| S2 | `NormalizedSemanticModel` | Deterministic canonical representation used for queries and projection. | A second authored source. |
| S3 | `ProjectionCompiler` | Deterministically derives declared read models. | A semantic decision-maker or writeback owner. |
| S4 | `HumanView` / `GraphView` / `QueryView` | Readable or operational projections with source bindings. | Editable parallel truth. |
| S5 | `ProjectionReceipt` | Binds source, schema, compiler, output digests, warnings, and validation. | Promotion evidence by itself. |
| S6 | owner gate | Admits or promotes source semantics under the correct lifecycle owner. | An Ontology Vault runtime inference. |

## Candidate Schema Suite

The refinement will test a modular suite instead of one universal mega-schema:

- `semantic-package.schema`: package identity, version, namespace, module
  references, ontology type, owner, source posture, canonicalization profile,
  projection declarations, and compatibility range;
- `semantic-record.schema`: stable IDs, record kind, lifecycle status, claim
  role, governance outcome, scope, content, confidence, and residue;
- `semantic-relation.schema`: endpoint types, relation type, direction,
  evidence, lifecycle, branch or profile constraints, and cycle policy;
- `semantic-evidence.schema`: immutable source identity, selectors,
  provenance, proof status, inference posture, and counterevidence;
- `semantic-governance.schema`: owner route, admission state, contradiction,
  rollback, retirement, supersession, and PromotionRecord link;
- `semantic-projection.schema`: projection ID, audience, renderer, ordering,
  templates, filters, expected output, and non-authority/writeback posture;
- ontology-type modules for `knowledge-vault`, `business-domain`,
  `system-runtime`, `business-system-bridge`, `authority-governance`, and
  `architecture-property` constraints.

## Representation Alternatives

Stage 4 must compare and preserve rejected alternatives:

1. closed JSON semantic package as the authored canonical source;
2. JSON-LD source with SHACL-like constraints and explicit local closure;
3. a typed YAML or small authoring language compiled to a canonical JSON AST.

The comparison must evaluate deterministic canonicalization, schema closure,
diff ergonomics, comments and authoring usability, graph semantics, tooling
availability, migration cost, reproducible digests, and public portability.
It must not assume a standards vocabulary is useful merely because it exists.

## Required Invariants

1. One admitted semantic fact has one authored owner source.
2. Human and graph views are derived and carry the exact source digest.
3. Generated views declare generator identity/version and are never silently
   accepted as writeback input.
4. Recompiling the same canonical input under the same compiler contract
   yields byte-identical governed outputs, excluding explicitly declared
   non-semantic receipt metadata.
5. Stable semantic IDs do not depend on file position or presentation order.
6. Schema validity, evidence confidence, commitment confidence, promotion,
   and authority remain separate axes.
7. Unknown, contradictory, unsupported, and deferred states remain typed;
   absence never becomes a positive fact.
8. A projection may omit or reorganize information but cannot add semantic
   claims not present in the normalized model.
9. Migration preserves old IDs or emits explicit, queryable identity maps.
10. Public Ontology Vault conventions contain only reusable contracts;
    private adopter evidence and vocabulary remain private profiles or
    fixtures outside public Arcanum.

## Authoring Experience Questions

Machine-first must not mean hostile-to-humans. The candidate must explain:

- how a person creates and reviews a semantic record without hand-maintaining
  a large graph file;
- how schema-guided editors, forms, or commands produce valid patches;
- how comments, rationale, examples, and long-form explanations are retained;
- how a reviewer sees semantic diffs rather than formatting churn;
- how a human proposes corrections without editing a generated view;
- how invalid drafts and migration residue remain recoverable.

## Validation Witnesses Required

The final candidate must include at least:

- one small valid knowledge-vault package;
- one multi-module package;
- one deterministic Markdown human view;
- one deterministic graph/query projection;
- one stale-view digest failure;
- one projection that tries to invent a semantic claim and is rejected;
- one invalid relation endpoint case;
- one unsupported-evidence case that remains unknown;
- one migration with an identity map;
- one private-profile fixture that proves private vocabulary does not leak
  into the reusable public schema.

## Ontology Vault Routing

- Mode: `convention-update`.
- Selected type: `knowledge-vault`, inferred with high confidence because the
  target is the reusable Ontology Vault convention and knowledge lifecycle.
- Rejected primary type: `architecture-property`; it would model the typed
  properties of one architecture, not the reusable semantic-source and
  projection conventions of Ontology Vault itself.
- Branch: none.
- Runtime before confirmation: none.
- Proposed Stage 4 runtime after confirmation: governed read-only agents.

## Scope And Boundaries

Writable in this preflight:

- this private refinement-run folder only.

Read-only sources:

- canonical public Ontology Vault sources under `arcanum/arcana/ontology-vault/`;
- the repository Inventory machine index and selected entries;
- private adopter artifacts only as pressure evidence, never as public text.

Forbidden until a later owner-approved implementation route:

- `arcanum/arcana/ontology-vault/` mutation;
- `.agents/skills/ontology-vault/` or `.claude/skills/ontology-vault/` mutation;
- ontology promotion or authority decisions;
- Inventory ingestion or synchronization;
- RWO ontology migration or resolution of its paused identity gate;
- commit, push, publication, release, deployment, or production claims.

## Success Condition

Produce one exact candidate model in which the machine semantic source,
schema suite, normalized model, deterministic projections, human correction
path, receipts, migrations, and authority gates are individually owned and
testable. Then produce a non-executed Work Pack. Any public convention change
remains a later Sigil Development and owner-approval route.

## Paused Prior Work

The RWO composition-form ontology Decision Gate remains unresolved. This new
Refine run neither selects its ontology identity option nor authorizes a
roll-forward, migration, or source rewrite.
