# Stage 02: Invoke Define - Ontology Vault Machine Semantic Source

## Invoke Result

- Mode: define
- Spell: invoke
- Canonical ID: invoke
- Scope: library authoring into a private target-development run
- Phase status: pass
- Mode contract: arcanum/spells/invoke/define.md
- Template selection: invoke.sigil candidate family
- Discovery: pass; Ontology Vault already has a development package and governed candidate schema bundle
- Layering: L0-L3 seed recorded below
- Distill sanity: pass at definition scope; full selection remains scheduled at Stage 5
- Target lifecycle owner: Ontology Vault through Sigil Development
- Public mutation: none
- Next route: Interrogation refine-review, then governed specialist analysis

## Approved Intent Record

The user confirmed a Refine strategy whose fixed direction is:

    one admitted machine semantic source
      -> deterministic derived human and machine views

This fixes the source/view direction but not the authoring representation,
canonicalization algorithm, schema module boundaries, or migration design.

## Template Selection Evidence

The target is a reusable sigil convention and interaction contract. The
invoke.sigil candidate template is eligible because it requires sigil identity,
purpose, inputs, outputs, modes, runtime expectations, validation examples, and
a Sigil Development handoff. DomainSpec feature templates are ineligible
because this is not one product feature. The template is candidate and grants no
registry release or lifecycle mutation.

## Sigil Identity

- Name: ontology-vault machine-semantic-source convention update
- Existing sigil: ontology-vault
- Owning canonical surface: arcanum/arcana/ontology-vault/
- Current run surface: private candidate refinement folder
- Lifecycle mutation owner: Sigil Development after a later approved handoff

## Problem Definition

Ontology meaning is currently expressible through candidate schemas and human
documents, but the reusable capability does not specify one primary machine
semantic package or the deterministic production of human views. This allows
source identity, ontology version, graph packages, and Markdown descriptions to
drift or compete.

## Desired Outcome

Define one reusable contract where:

- people author or generate a machine-parseable SemanticPackage;
- a modular SchemaSuite rejects invalid structural and cross-field states;
- a deterministic normalizer produces one NormalizedSemanticModel;
- declared projectors derive HumanView, GraphView, and QueryView artifacts;
- every governed projection has a ProjectionReceipt;
- human corrections become typed SourcePatch proposals against the semantic
  source, never edits that silently turn a view into authority;
- owner admission and PromotionRecord decisions remain separate.

## Inputs

| Input | Required | Validation |
| --- | --- | --- |
| SemanticPackage manifest and modules | yes | Package identity, version, owner, ontology type, namespace, module closure, and canonicalization profile validate. |
| SchemaSuite | yes | Core and selected ontology-type modules are digest-bound and closed. |
| ProjectionDefinition | one or more | Audience, renderer, ordering, filters, target, and writeback posture are explicit. |
| Source evidence | conditional | Immutable identity, selector, proof posture, and provenance are retained when a semantic claim relies on evidence. |
| Migration map | for legacy adoption | Old identity to new identity mapping is total or residue is explicit. |

## Outputs

| Output | Consumer | Contract |
| --- | --- | --- |
| NormalizedSemanticModel | validators, query engines, projectors | Derived, deterministic, content-addressed, and not independently authored. |
| HumanView | readers and reviewers | Derived, source-bound, generator-bound, clearly marked, and non-authoritative. |
| GraphView / QueryView | tools and visualizations | Bounded projections that cannot introduce claims. |
| ProjectionReceipt | validation and drift checks | Binds source, schema, compiler, output digests, warnings, and result. |
| SourcePatch proposal | semantic package owner | Typed correction against source identity; requires owner review. |
| MigrationReceipt | adopter owner | Records identity preservation, changes, residue, and rollback. |

## Candidate Vocabulary

| Term | Working definition | Status |
| --- | --- | --- |
| SemanticPackage | Owner-scoped machine-readable source manifest and modules for one ontology package. | candidate |
| SchemaSuite | Versioned core plus ontology-type/profile constraint modules. | candidate |
| NormalizedSemanticModel | Deterministic derived semantic IR used by validation and projection. | candidate |
| ProjectionDefinition | Machine record declaring how one bounded read model is produced. | candidate |
| HumanView | Deterministic reader projection from the normalized model. | candidate |
| ProjectionReceipt | Digest-bound evidence for one projection execution. | candidate |
| SourcePatch | Proposed typed change to the admitted semantic source. | candidate |
| MigrationMap | Explicit old-to-new identity and compatibility mapping. | candidate |
| AdmissionRecord | Owner decision that a source package is accepted for a stated scope. | candidate; must not duplicate PromotionRecord without later analysis |

No term is promoted into Definitions Governance by this run.

## Functional Requirements

- Stable semantic IDs independent of display order or file position.
- Closed module reference graph and ontology-type selection.
- Deterministic canonicalization and normalization.
- Structural and cross-field validation with typed unknown and contradiction.
- Deterministic projections with declared ordering and omission rules.
- Source, schema, compiler, and output digest binding.
- Semantic diffs and schema-guided SourcePatch authoring.
- Identity-preserving migration and explicit rollback.
- Generated-view headers and drift validation.
- Public/private fixture separation.

## Negative Requirements

- No view writeback by proximity.
- No schema-valid-equals-true inference.
- No normalization-equals-promotion inference.
- No missing-evidence-equals-pass behavior.
- No private adopter vocabulary in reusable public schemas.
- No direct generated-mirror edits.
- No public convention mutation from this Refine result.
- No resolution of the paused RWO ontology identity gate.

## Definition-Scope Distill Sanity

Proposer: treat the whole semantic-source system as one new schema.

Balancer objection, category boundary overload: one mega-schema would collapse
source records, validation, compiler configuration, projections, receipts, and
promotion.

Reconciliation: the smallest coherent definition unit is the semantic-source
spine: SemanticPackage plus normalized-model boundary plus ProjectionDefinition
and ProjectionReceipt, with entry/relation/evidence/governance schemas reused as
modules. It recomposes into the larger Ontology Vault through convention-update
and later Sigil Development. Further reduction would lose the source-to-view
invariant; further expansion would smuggle runtime and promotion work.

Verdict: pass for Define. Representation choice and exact modules remain
evidence questions for Stages 4-6.

## Implementation Layering Seed

- L0: schema modules, canonical examples, negative fixtures, and receipt shapes.
- L1: deterministic canonicalizer, normalizer, Markdown projector, and drift validator.
- L2: authoring helpers, semantic diffs, SourcePatch flow, and legacy migration.
- L3: lifecycle integration, profile adapters, observability, and governed synchronization.

This is a definition seed, not a plan or implementation authorization.

## Dispatch Technique Trace

| Technique | Effect |
| --- | --- |
| sequence | Define consumes the Stage 1 context pack and feeds Stage 3. |
| owner_boundary_check | Invoke authors the candidate; Ontology Vault and Sigil Development retain lifecycle authority. |
| authority_split_gate | Source admission, schema validation, projection, and promotion remain separate. |
| residue_ledger | Representation, AdmissionRecord overlap, and migration questions remain explicit. |
| route_projection_boundary | Human and graph outputs are projections, not source. |

The enclosing REFINE-DISPATCH.json passes Dispatch Spec validation.

## Unresolved Gaps

- Select the authoring representation.
- Decide whether AdmissionRecord is needed or PromotionRecord already covers it.
- Define canonicalization and deterministic byte domain.
- Define rich human explanation storage.
- Define schema-version compatibility and migration.
- Determine which private pressure fixtures are necessary without leaking them.

## Handoff

Invoke Define is complete at candidate-authoring level. It does not release a
registry capability or make mutation runtime-ready. Continue to Stage 3
Interrogation and the confirmed specialist strategy.
