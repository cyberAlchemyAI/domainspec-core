# CyberAlchemy v2 Definitions

Status: active local source
Owner: definitions-governance
Canonical source: `authority/definitions/DEFINITIONS.md`
Lookup index: `authority/definitions/DEFINITIONS-INDEX.md`

## Authority Rule

Only this file defines normative semantics for CyberAlchemy v2 terms it
contains. Downstream artifacts may explain, apply, or reference these terms, but
should not redefine them as project authority.

Arcanum-wide terms remain owned by [../../arcanum/definitions/DEFINITIONS.md](../../../arcanum/definitions/DEFINITIONS.md).
CyberAlchemy v2 definitions are local until a later promotion route says
otherwise.

## CAV2-D1: Stable Repository

Status: active
Term: stable repository
Aliases: stable repo, next stable repository, base repository, downloadable base repository

### Normative Definition

A stable repository is a maintainable repository surface whose authority,
source evidence, promoted contracts, validation evidence, implementation work,
and operating traces can be understood without hidden conversation context, and
whose exported base can support downstream construction without requiring users
to rediscover or re-promote its foundation.

### Operational Interpretation

Use this term when deciding whether CyberAlchemy v2 is ready to move from a
project folder inside `domainspec-core` into its own repository. The repository
is not stable merely because files exist; it is stable when its authority model,
source spine, promotion gates, and validation surfaces are navigable and
reviewable. When CyberAlchemy v2 is extracted, the stable repository objective
is that a user can download CyberAlchemy as this governed base and build project
or domain towers above it.

### Plain-Language Intuition

A stable repository is the trustworthy base someone can download, understand,
and build on without guessing what counts.

### Domain-Context Voice

In CyberAlchemy v2, this term names the target state for extracting this project
from the private `domainspec-core` umbrella into a repository with its own
authority imports, definitions, constitutions, validation, and operating trace.
That extracted repository is intended to become the next owner of the
CyberAlchemy base authority: it should preserve what has been settled here and
leave clear construction surfaces for downstream users to extend above the base.

### Boundary

This term does not mean finished product, public repository, automatic ownership
of every historical CyberAlchemy source, or implementation complete. Standalone
extraction and any transfer of authority from older source spaces remain
promotion decisions.

### Primary Consumers

- [../../README.md](../../README.md)
- [../promotion-policy.md](../promotion-policy.md)
- [../../development/constitution-pack.md](../../development/constitution-pack.md)

## CAV2-D2: Source-Ledgered Amalgamation

Status: active
Term: source-ledgered amalgamation
Aliases: governed amalgamation, source-ledgered consolidation

### Normative Definition

Source-ledgered amalgamation is the practice of consolidating dispersed work by
recording source cohorts, authority posture, and promotion routes instead of
copying every source into one folder or treating synthesis as authority.

### Operational Interpretation

Use this term when CyberAlchemy v2 gathers material from inventory,
ontology-vault, CyberAlchemy, Arcanum, framework-unification, DomainSpec, and
validation sources. The consolidation should preserve source links, evidence
confidence, commitment confidence, and owner routes.

### Plain-Language Intuition

It is an amalgamation with receipts.

### Domain-Context Voice

In CyberAlchemy v2, this term describes the move from scattered source systems
into import manifests, source maps, candidate ontology, and later promoted
authority without flattening the original source ownership.

### Boundary

This term does not authorize private-to-public conversion, global term
promotion, or implementation mutation.

### Primary Consumers

- [../../SOURCE-MAP.md](../../SOURCE-MAP.md)
- [../../disciplines/cards/stable-repository-stewardship.md](../../disciplines/cards/stable-repository-stewardship.md)
- [../constitutions/STABLE-REPOSITORY-CONSTITUTION.md](../constitutions/STABLE-REPOSITORY-CONSTITUTION.md)

## CAV2-D3: Authority Layer

Status: active
Term: authority layer
Aliases: local authority surface, authority surface

### Normative Definition

An authority layer is a project-local surface that is allowed to define
normative meaning, structural rules, promotion decisions, or contracts for a
specific scope.

### Operational Interpretation

Use authority layers to prevent research, inventory, ontology, observability,
memory, generated projections, and implementation evidence from silently
rewriting definitions or rules.

### Plain-Language Intuition

An authority layer says which document is allowed to count.

### Domain-Context Voice

In CyberAlchemy v2, the authority layers are currently
`authority/definitions/`, `authority/constitutions/`, `disciplines/`,
`authority/decisions/`, and later promoted `specs/`.

### Boundary

An authority layer can cite evidence, but evidence does not become authority
unless the responsible owner promotes it.

### Primary Consumers

- [../README.md](../README.md)
- [../boundaries.md](../boundaries.md)
- [../promotion-policy.md](../promotion-policy.md)

## CAV2-D4: Source Spine

Status: active
Term: source spine
Aliases: first source spine, bootstrap source spine

### Normative Definition

A source spine is the selected, minimal set of source cohorts used to orient a
project phase, with each cohort assigned a role and authority posture.

### Operational Interpretation

Use the source spine to decide where an agent should look first and what it may
infer from each source. A source spine narrows search without pretending that
excluded sources are irrelevant forever.

### Plain-Language Intuition

It is the starting bibliography with boundaries attached.

### Domain-Context Voice

In CyberAlchemy v2, the source spine is smaller than the import corpus. It helps
orientation, while [../imports/](../imports/README.md) stages the broader
definition and constitution source set.

### Boundary

A source spine is not a full inventory, complete literature review, or final
architecture decision.

### Primary Consumers

- [../../SOURCE-MAP.md](../../SOURCE-MAP.md)
- [../../research/README.md](../../research/README.md)

## CAV2-D5: Promotion Gate

Status: active
Term: promotion gate
Aliases: owner gate, authority gate

### Normative Definition

A promotion gate is an explicit owner route that decides whether evidence,
candidate meaning, a recurring practice, or a structural rule may become local
authority, implementation work, or standalone repository material.

### Operational Interpretation

Use a promotion gate whenever a claim would cross from source evidence,
inventory, ontology, research, observability, or memory into definitions,
constitutions, specs, capabilities, implementation, or public-facing material.

### Plain-Language Intuition

A promotion gate is the moment the project asks, "is this allowed to count now?"

### Domain-Context Voice

In CyberAlchemy v2, promotion gates decide when imported definitions,
constitutions, ontology candidates, inventory cards, research findings, or
validation evidence become local authority or implementation work.

### Boundary

The gate may return pass, flag, or block. A flag is not a silent pass; it carries
named risk and follow-up.

### Primary Consumers

- [../promotion-policy.md](../promotion-policy.md)
- [../constitutions/STABLE-REPOSITORY-CONSTITUTION.md](../constitutions/STABLE-REPOSITORY-CONSTITUTION.md)

## CAV2-D6: Stable Repository Stewardship

Status: active
Term: stable repository stewardship
Aliases: repository stewardship, stewardship discipline

### Normative Definition

Stable repository stewardship is the recurring practice of keeping a repository
surface source-ledgered, authority-bounded, navigable, validated, and ready for
future extraction or maintenance.

### Operational Interpretation

Use this term for the project-local discipline that keeps CyberAlchemy v2 from
becoming another pile of true but unowned documents.

### Plain-Language Intuition

It is the habit that keeps the repo understandable after the exciting part.

### Domain-Context Voice

In CyberAlchemy v2, stable repository stewardship now includes maintaining the
authority import ledgers, not only maintaining the skeleton folders created in
the first pass.

### Boundary

The discipline recommends hardening routes. It does not promote definitions,
constitutions, specs, ontology, or implementation by itself.

### Primary Consumers

- [../../disciplines/DISCIPLINES.md](../../disciplines/DISCIPLINES.md)
- [../../disciplines/cards/stable-repository-stewardship.md](../../disciplines/cards/stable-repository-stewardship.md)

## CAV2-D7: Authority Import

Status: active
Term: authority import
Aliases: authority import ledger, import ledger

### Normative Definition

An authority import is a staged capture of source paths that may contain
definitions, constitutions, axioms, rules, or other authority-bearing material,
with enough classification to preserve source posture and route later promotion.

### Operational Interpretation

Use authority imports before consolidating scattered repository vocabulary or
rules into CyberAlchemy v2. The import records what exists and where it lives
without copying authority into the local canonical source.

### Plain-Language Intuition

An authority import is a shelf of candidates with labels.

### Domain-Context Voice

In CyberAlchemy v2, authority imports live under [../imports/](../imports/README.md)
and currently stage 149 definition-like candidates plus 106 constitution/axiom
candidates from the broader `domainspec-core` checkout.

### Boundary

An authority import is not promotion. It does not make a source term or rule
canonical for CyberAlchemy v2.

### Primary Consumers

- [../imports/README.md](../imports/README.md)
- [../imports/definitions/MANIFEST.md](../imports/definitions/MANIFEST.md)
- [../imports/constitutions/MANIFEST.md](../imports/constitutions/MANIFEST.md)

## CAV2-D8: Import Candidate

Status: active
Term: import candidate
Aliases: staged candidate, authority candidate

### Normative Definition

An import candidate is a source path captured by an authority import that may
contain reusable vocabulary, rules, evidence, examples, or governance patterns,
but has not been promoted into CyberAlchemy v2 authority.

### Operational Interpretation

Use import candidates as the first review queue for scattered definitions and
constitutions. Classify their source family, authority posture, reuse value,
conflicts, and promotion owner before extracting content.

### Plain-Language Intuition

An import candidate is something worth reviewing before it gets a vote.

### Domain-Context Voice

In CyberAlchemy v2, import candidates are recorded in the definition and
constitution manifests. They should be clustered and deduplicated before any
new canonical term or constitution rule is added.

### Boundary

An import candidate may be source-of-truth for its original project while still
remaining candidate-only for CyberAlchemy v2.

### Primary Consumers

- [../imports/definitions/MANIFEST.md](../imports/definitions/MANIFEST.md)
- [../imports/constitutions/MANIFEST.md](../imports/constitutions/MANIFEST.md)
- [../promotion-policy.md](../promotion-policy.md)

## CAV2-D9: CyberAlchemy v2

Status: active
Term: CyberAlchemy v2
Aliases: CyberAlchemy stable repository candidate, v2 consolidation surface, CyberAlchemy base repository, CyberAlchemy base

### Normative Definition

CyberAlchemy v2 is the project-local stable repository candidate that organizes
the dispersed CyberAlchemy, Arcanum, DomainSpec, inventory, ontology, research,
validation, and operations material into source-ledgered authority layers,
candidate towers, promotion queues, and execution surfaces so it can become the
downloadable CyberAlchemy base repository after owner review and extraction.

### Operational Interpretation

Use this term for the local consolidation project at `cyberAlchemy-v2/`, not for
all CyberAlchemy work everywhere. CyberAlchemy v2 owns local definitions,
constitutions, source maps, Craft state, and promotion routes for this stable
repository effort. Its objective is to become the base repository users receive
when they download CyberAlchemy, with enough authority, ontology, inventory, and
runtime projection structure for others to construct above it.

### Plain-Language Intuition

CyberAlchemy v2 is the home base: the repo you can download, trust, and build
above.

### Domain-Context Voice

In this workspace, CyberAlchemy v2 currently lives inside the private
`domainspec-core` umbrella as a project folder. It is not yet a standalone
repository, but it now has local authority imports, definitions, definition
towers, a Craft ledger, ontology package research, and extraction blockers.
The project objective is to make this folder the governed CyberAlchemy base:
settled authority is preserved here, unresolved authority is routed through
owner gates, and downstream projects can extend the base without inheriting
private source ambiguity.

### Boundary

CyberAlchemy v2 is not the same as public Arcanum, private DomainSpec, the
older `cyberAlchemy/` source folder, or a finished standalone product. It may
reference those sources, but it does not automatically absorb their authority.
It becomes the owner of CyberAlchemy base authority only through import,
promotion, boundary review, and standalone extraction decisions.

### Primary Consumers

- [../../README.md](../../README.md)
- [../../CRAFT.md](../../CRAFT.md)
- [DEFINITION-TOWERS.md](DEFINITION-TOWERS.md)

## CAV2-D10: Definition Tower

Status: active
Term: definition tower
Aliases: semantic tower, term tower

### Normative Definition

A definition tower is a bounded cluster of related terms arranged by conceptual
altitude, source posture, authority boundary, owner route, and next review
action so that local definitions can be promoted deliberately instead of copied
from scattered sources.

### Operational Interpretation

Use definition towers to organize top-level anchors, framework references,
private DomainSpec references, knowledge-governance terms, research/product
terms, and execution-evidence terms before adding or updating canonical
definitions.

### Plain-Language Intuition

A definition tower is a stack of terms with a map, a boundary, and a next
review step.

### Domain-Context Voice

In CyberAlchemy v2, definition towers are mapped in
[DEFINITION-TOWERS.md](DEFINITION-TOWERS.md) and executed through the Craft
context `CTX-CAV2-DEF-TOWERS`. They are the first ordering surface for the 149
definition import candidates.

### Boundary

A definition tower is a classification and routing surface, not canonical
definition authority by itself. Authority lives in this file after
definitions-governance promotion.

### Primary Consumers

- [DEFINITION-TOWERS.md](DEFINITION-TOWERS.md)
- [../../CRAFT.md](../../CRAFT.md)
- [../imports/definitions/MANIFEST.md](../imports/definitions/MANIFEST.md)

## CAV2-D11: Tower Space

Status: active
Term: tower space
Aliases: tower-bearing space, definition space

### Normative Definition

A tower space is a project, source, or execution area that can own, supply,
consume, or route content for one or more definition towers while preserving its
own authority posture.

### Operational Interpretation

Use tower spaces to distinguish CyberAlchemy v2 project folders from external
source spaces such as Arcanum, DomainSpec, prior CyberAlchemy material,
framework-unification, research towers, and validation evidence.

### Plain-Language Intuition

A tower space is where tower content comes from, lives, or gets worked on.

### Domain-Context Voice

In CyberAlchemy v2, tower spaces are grouped as project spaces, source spaces,
and Craft execution spaces in [DEFINITION-TOWERS.md](DEFINITION-TOWERS.md).
This lets `inventory/`, `ontology/`, `authority/`, `research/`, `ops/`, and
external source folders stay distinct.

### Boundary

A tower space does not become authoritative because it is listed in a tower map.
Each space keeps its own owner, source posture, and promotion gate.

### Primary Consumers

- [DEFINITION-TOWERS.md](DEFINITION-TOWERS.md)
- [../../SOURCE-MAP.md](../../SOURCE-MAP.md)
- [../../CRAFT.md](../../CRAFT.md)

## CAV2-D12: Craft Execution Surface

Status: active
Term: Craft execution surface
Aliases: Craft surface, local Craft surface, Craft ledger surface

### Normative Definition

A Craft execution surface is the project-local Craft ledger, derived index, and
linked human view used to record recursive work state, blockers, decisions,
candidate definitions, gaps, artifacts, next moves, and recomposition evidence
for a bounded project scope.

### Operational Interpretation

Use the Craft execution surface when continuing CyberAlchemy v2 work from
structured state. The source of truth is `.craft/ledger.yml`; `CRAFT.md` and
`.craft/index.json` are derived navigation surfaces.

### Plain-Language Intuition

It is the workbench where the project remembers what is open and what happens
next.

### Domain-Context Voice

In CyberAlchemy v2, the Craft execution surface owns contexts such as
`CTX-CAV2-DEF-TOWERS`, `CTX-CAV2-AUTHORITY-IMPORTS`, and
`CTX-CAV2-CONSTITUTION-TOWERS`. It records the route memory for definitions and
constitution work, but the owner sigils still govern promotion.

### Boundary

Craft can carry local candidate definitions and receipts, but it does not make
terms canonical and does not replace definitions-governance,
constitution-governance, decision-gate, or task-session.

### Primary Consumers

- [../../CRAFT.md](../../CRAFT.md)
- [../../.craft/ledger.yml](../../.craft/ledger.yml)
- [DEFINITION-TOWERS.md](DEFINITION-TOWERS.md)

## CAV2-D13: Authority Promotion Queue

Status: active
Term: authority promotion queue
Aliases: promotion queue, definition promotion queue, rule promotion queue

### Normative Definition

An authority promotion queue is the ordered set of candidate terms, rules,
claims, or artifacts awaiting owner classification, duplicate/conflict review,
boundary review, and explicit promotion decision before entering a canonical
authority layer.

### Operational Interpretation

Use an authority promotion queue to decide what should be reviewed next without
allowing queue position to imply approval. The queue can include definition
candidates, constitution candidates, ontology candidates, or extraction
readiness items.

### Plain-Language Intuition

It is the review line for things that might be allowed to count.

### Domain-Context Voice

In CyberAlchemy v2, the first authority promotion queue is Q1 in
[DEFINITION-TOWERS.md](DEFINITION-TOWERS.md): top anchors before framework
references, DomainSpec references, imported term clusters, constitution
clusters, and execution readiness.

### Boundary

An authority promotion queue is not a promotion gate result. Items in the queue
remain candidate-only until the responsible owner records a pass, flag, block,
deferral, or rejection.

### Primary Consumers

- [DEFINITION-TOWERS.md](DEFINITION-TOWERS.md)
- [../promotion-policy.md](../promotion-policy.md)
- [../../CRAFT.md](../../CRAFT.md)

## CAV2-D14: Source Space

Status: active
Term: source space
Aliases: source evidence space, external source space

### Normative Definition

A source space is a repository area outside the current CyberAlchemy v2
authority surface that supplies candidate evidence, vocabulary, rules, examples,
or operating precedent for review.

### Operational Interpretation

Use source spaces when tracing imported definitions, constitutions, ontology
branches, research towers, validation evidence, or implementation patterns back
to their originating folders and owner boundaries.

### Plain-Language Intuition

A source space is where a candidate came from before CyberAlchemy v2 decides
what to do with it.

### Domain-Context Voice

In CyberAlchemy v2, source spaces include public Arcanum, private DomainSpec,
the older `cyberAlchemy/` source folder, framework-unification, research
folders, project glossaries, and validation evidence.

### Boundary

A source space may be authoritative for itself while remaining candidate-only
for CyberAlchemy v2. Source-space evidence requires import classification and
promotion before becoming local authority.

### Primary Consumers

- [../../SOURCE-MAP.md](../../SOURCE-MAP.md)
- [DEFINITION-TOWERS.md](DEFINITION-TOWERS.md)
- [../imports/definitions/MANIFEST.md](../imports/definitions/MANIFEST.md)

## CAV2-D15: Project Space

Status: active
Term: project space
Aliases: local project space, CyberAlchemy v2 project area

### Normative Definition

A project space is a folder or surface inside CyberAlchemy v2 that has a
declared project-local role for authority, candidate synthesis, research,
architecture, capabilities, specifications, implementation, validation,
inventory, ontology, observability, operations, or Craft state.

### Operational Interpretation

Use project spaces to decide where CyberAlchemy v2 should place work after
promotion or routing. Project spaces are local homes such as `authority/`,
`research/`, `architecture/`, `specs/`, `validation/`, `ops/`, `inventory/`,
`ontology/`, and `.craft/`.

### Plain-Language Intuition

A project space is a room inside CyberAlchemy v2 with a declared job.

### Domain-Context Voice

In CyberAlchemy v2, project spaces make the future stable repository navigable
while it is still staged inside `domainspec-core`. Some spaces, especially
`inventory/` and `ontology/`, remain under review before standalone extraction.

### Boundary

A project space can hold authority only when its role permits it. Research,
inventory, ontology, observability, operations, and Craft surfaces may preserve
evidence or route work without becoming canonical definition sources.

### Primary Consumers

- [../../README.md](../../README.md)
- [DEFINITION-TOWERS.md](DEFINITION-TOWERS.md)
- [../../CRAFT.md](../../CRAFT.md)

## CAV2-D16: Typed Coupling Invariant

Status: active
Term: typed coupling invariant
Aliases: explicit coupling invariant, typed coupling rule, explicit typed relation rule, non-orthogonality explicitness rule

### Normative Definition

A typed coupling invariant is the CyberAlchemy v2 rule that any dependency,
bridge, constraint, influence, or co-change relation between non-orthogonal
artifacts, concepts, stages, authorities, or owners must be represented as an
explicit typed relation with named endpoints, direction, relation kind, owner,
evidence, and validation or promotion effect.

### Invariant Statement

For any two local objects `A` and `B`, if `A` and `B` cannot vary independently
for the decision being made, then CyberAlchemy v2 must record a typed relation
`R(A, B)` before the coupling can influence authority, routing, validation, or
implementation.

At minimum, `R(A, B)` records:

- source endpoint
- target endpoint
- relation type
- direction or symmetry
- owner route
- evidence reference
- validation, promotion, or blocking effect

If the relation cannot yet be typed, the coupling remains an open question,
residue, blocker, or candidate note rather than a hidden assumption.

### Operational Interpretation

Use this invariant when orthogonality fails. If maturity affects promotion,
schema affects contract, route affects authority, artifact provenance affects
trust, or one owner lane constrains another, the relation must be modeled
directly instead of left as prose implication, file adjacency, or remembered
context.

### Plain-Language Intuition

If two things are wired together, draw the wire and label it.

### Domain-Context Voice

In CyberAlchemy v2, this term sits above the definition towers as a primordial
rule. It explains why framework-unification separates axes, why DomainSpec
requires typed relationships, why provenance cannot live only in memory, and
why non-orthogonal links such as maturity-to-promotion, schema-to-contract, or
source-to-authority must be explicit before they can govern work.

### Boundary

This invariant does not require every related idea to be coupled. Orthogonal
axes should remain separate. It applies only when a decision, validation,
promotion, or implementation would rely on one object constraining or changing
with another. A typed relation is also not automatic promotion; it is the
minimum representation needed before a coupling can be reviewed.

### Primary Consumers

- [DEFINITION-TOWERS.md](DEFINITION-TOWERS.md)
- [source-clusters/primordial.md](source-clusters/primordial.md)
- [../../CRAFT.md](../../CRAFT.md)

## CAV2-D17: Reflection Tower Method

Status: active
Term: reflection tower method
Aliases: reflection tower, reflection-tower method, residue climb, tower climb method, residue escalation method

### Normative Definition

A reflection tower method is the CyberAlchemy v2 primitive method that handles
structural residue by turning unresolved residue from one schema/data layer into
the seed for a higher explanatory layer with its own objective, schema, target
data, validation, and recomposition path.

### Formal Step

Given a layer `L_n` with schema `S_n`, data or instance surface `D_n`, translator
or operation `T_n`, and residue `R_n`, the method first attempts local repair.
If `R_n` cannot be closed inside `L_n` without increasing residue or breaking
recomposition, then:

```text
R_n -> seed(L_n+1)
```

The next layer must name what the lower layer could not name, then route the new
schema, validation, owner, and recomposition obligation back to the tower.

When the DomainSpec formalization evidence applies, the preferred formal reading
is:

```text
L1^(n+1) := L1^n + Carrier(mu_n)
```

where `Carrier(mu_n)` records the residue's failure-locus and the promotion
`P_n : L1^n -> L1^(n+1)` preserves prior distinctions while adding new
vocabulary. CyberAlchemy v2 uses this as the governing shape of the method, not
as a requirement that every operational use materialize a Lean-level category.

### Operational Interpretation

Use this method when a task, definition, schema, artifact, or governance route is
already reduced to a responsible unit, but residue still remains because the
current layer lacks a schema, relation, taxonomy, validation rule, authority
rule, or owner route. The answer is not more splitting by default; the answer is
to name the missing layer that would make the residue intelligible.

### Plain-Language Intuition

When the current floor cannot explain the leftover problem, build the next floor
from that leftover problem and make it explain its way back down.

### Domain-Context Voice

In CyberAlchemy v2, reflection tower method sits beside orthogonality,
recursivity, and typed coupling as a primordial method. It explains how Craft
turns persistent residue into higher-layer work, why DomainSpec evidence treats
residue promotion as vertical growth rather than a third peer layer, and why v2
must keep ontology towers, capability towers, and reflection towers distinct
unless a typed coupling explicitly relates them.

### Boundary

The reflection tower method is not ordinary recursion, not endless
decomposition, not folder nesting, and not automatic promotion. It applies only
when local repair fails and the residue indicates a missing higher schema or
owner layer. It must stop by explicit closure, gate, or owner decision; it does
not promise total final closure at a finite rung. The existence of an omega-level
substrate does not by itself authorize fixed-point or absorption claims; those
remain construction-sensitive and must be stated only at the strength supported
by the current evidence.

### Primary Consumers

- [DEFINITION-TOWERS.md](DEFINITION-TOWERS.md)
- [source-clusters/primordial.md](source-clusters/primordial.md)
- [../../CRAFT.md](../../CRAFT.md)

## CAV2-D18: Residue

Status: active
Term: residue
Aliases: typed residue, residue signal, residual remainder, unpreserved structure

### Normative Definition

Residue is the typed remainder exposed by a transformation, translation,
promotion, validation, or governance operation when the target representation,
layer, or decision path does not preserve, name, justify, validate, or carry all
source structure required by the operation's intended use.

A residue becomes actionable in CyberAlchemy v2 only when it records:

- source operation or transformation
- expected preservation or closure condition
- observed remainder or failure-locus
- residue type
- evidence reference
- owner route
- treatment: repair, type, gate, climb, accept, or defer

### Formal Interpretation

For an operation `F : A -> B` with an intended preservation condition `P`, the
residue of `F` is the evidence-bearing part of `A` that `B` cannot preserve,
name, reconstruct, justify, or validate under `P`.

In DomainSpec formalization contexts, this umbrella has several non-identical
readings:

- schema residue: a schema-level unit failure or missing faithful shadow
- instance residue: an instance-level round-trip or migration failure
- `ResidueObject`: a finite probabilistic residue object with entropy
- `ResidueStructure`: a carrier/schema/signal/noise/refinement structure
- `ResidueCat`: a category of bundled residue structures and monotone morphisms
- `Carrier(mu_n)`: the reflection-tower carrier that turns level `n` residue
  into level `n+1` vocabulary

These readings may inform each other, but CyberAlchemy v2 must not treat them as
interchangeable without a typed coupling.

### Operational Interpretation

Use residue when something meaningful remains after a local operation has done
what it knows how to do. The remainder may be information loss, untyped noise,
missing vocabulary, failed validation, a broken recomposition path, an authority
gap, or an unresolved owner route.

First type the residue. Then either repair it locally, record a typed coupling,
route it through a gate, promote it through the reflection tower method, accept
it as tolerated residue, or defer it as an open question.

### Plain-Language Intuition

Residue is the meaningful leftover: the part the current representation could
not carry.

### Domain-Context Voice

In CyberAlchemy v2, residue is the reason the system cannot stop at clean
summaries, folders, or pass/fail checks. It is the evidence that tells Craft
when a unit needs repair, when a relation needs typing, when authority needs a
gate, and when a reflection tower climb is justified. It sits between
`CAV2-D16` typed coupling invariant and `CAV2-D17` reflection tower method:
couplings label cross-object residue, while reflection tower method promotes
structural residue into a higher explanatory layer.

### Boundary

Residue is not any bug, not any uncertainty, not proof of novelty, and not
automatic promotion. Some residue is acceptable, some is repairable, some is a
blocker, and some is the seed for a higher layer. The imported term
`TranslationResidue` remains a source-specific candidate until a later pass
decides whether it is a subtype, alias, or separate term.

### Primary Consumers

- [DEFINITION-TOWERS.md](DEFINITION-TOWERS.md)
- [source-clusters/primordial.md](source-clusters/primordial.md)
- [../../CRAFT.md](../../CRAFT.md)

## CAV2-D19: Ontology

Status: active
Term: ontology
Aliases: governed meaning layer, ontology candidate, ontology map, ontology branch map, ontology candidate condensation

### Normative Definition

An ontology is a governed meaning layer that represents a domain, workspace,
system, or operation as typed knowledge objects, typed relations, branch or role
assignments, provenance, confidence, promotion state, and use obligations.

In CyberAlchemy v2, an ontology becomes actionable only when it records:

- scope or domain of meaning
- knowledge object types
- typed relations or edge rules
- branch, role, or ownership assignment
- evidence and provenance references
- evidence confidence and commitment confidence when claims are load-bearing
- promotion state and next gate
- contradiction, drift, residue, or invalidation route
- retrieval or use guidance for downstream agents or humans

### Formal Interpretation

Given source evidence `S`, inventory evidence layer `I`, and intended use `U`,
an ontology `O` is a typed structure over selected evidence:

```text
O_U = (N, E, B, R, C, P, G)
```

where:

- `N` is a set of typed knowledge objects or nodes
- `E` is a set of typed relations or edges over `N`
- `B` assigns branch, role, or ownership context
- `R` links ontology claims back to source or inventory evidence
- `C` records confidence, scope, validity, and expiry where relevant
- `P` records candidate, reviewed, promoted, demoted, or deferred state
- `G` records gates, contradiction paths, drift routes, and use obligations

An ontology may be graph-shaped, tree-shaped, branch-aware, entry-based, or
artifact-tree-shaped, but it must keep typed meaning, evidence, and authority
posture together. A pointer list without usable content, typed relations, and
governance state is inventory or index material, not ontology.

### Operational Interpretation

Use ontology after source evidence has been located and inventory has made it
findable, when the project needs meaning that agents or humans can actually use:
what a thing is, where it belongs, how it relates to other things, what supports
it, how confident the project is, and when it may guide later work.

Branch-aware ontology separates business or meaning claims, system claims, and
bridge claims so implementation evidence cannot silently redefine intent and
intent cannot pretend implementation exists. Some local systems add further
branches, such as an agent-operation branch or run-context branch, but those are
typed substructures and not aliases for ontology itself.

### Plain-Language Intuition

An ontology is a map of meaning with typed links, receipts, and rules for use.

### Domain-Context Voice

In CyberAlchemy v2, ontology is the layer that condenses scattered repository
knowledge into candidate branch maps, thick knowledge entries, and promotion
requests without making them canonical by proximity. The current
`.arcanum/ontology-vault/` map reduces search and suggests branches; future
`ontology/` project-space material may hold candidate branch maps and promotion
requests. Definitions still become canonical only in this file, and source
authority still comes from the source space unless a promotion gate passes.

Inside the future CyberAlchemy base repository, `ontology/` is the workspace
where authority relations are made explicit, reviewable, and constructible as a
candidate/projection package. It is where v2 fixes the shape of authority for
the base by mapping meaning, evidence, owner routes, promotion requests,
projection boundaries, and residue before any downstream project builds above
that base.

This term connects `CAV2-D16` typed coupling invariant, `CAV2-D18` residue, and
the knowledge-governance tower: an ontology can type relations, preserve
meaningful residue, and route candidate meaning toward context-builder,
decision-gate, definitions-governance, or implementation work.

### Boundary

Ontology is not raw source, not inventory, not a glossary, not memory, not a
session transcript, not a generated search index, and not automatic authority.
Candidate ontology may condense meaning, but it cannot promote definitions,
constitutions, runtime contracts, or public claims by itself. The ontology
package fixes authority by making candidate authority structure explicit; it
does not own authority transitions.

`Operational Ontology` is demoted as a CyberAlchemy v2 definition candidate.
Treat it as source-local shorthand for an operation-facing ontology projection:
a `CAV2-D19` ontology view whose authority posture is governed by `CAV2-D23`.
It is not a primitive, not a peer ontology branch, not a standalone subtype, and
not a `CAV2-D23` alias.

When a source uses `Operational Ontology`, normalize the phrase instead of
promoting it:

- typed meaning, relation, branch, evidence, retrieval, or use obligations route
  to `CAV2-D19` ontology;
- lifecycle posture, status, evidence confidence, commitment, provenance,
  owner, or residue separation routes to `CAV2-D23` authority lifecycle axis;
- agent-operation, run, action, routing, or workflow obligations must be named
  as concrete object, relation, action, run, or schema obligations rather than
  hidden inside the broad phrase;
- if no concrete obligation remains after the D19/D23 split, retire the phrase
  in local wording.

### Primary Consumers

- [DEFINITION-TOWERS.md](DEFINITION-TOWERS.md)
- [../../CRAFT.md](../../CRAFT.md)
- [../../../.arcanum/ontology-vault/map-2026-06-18-dispersed-knowledge.md](../../../.arcanum/ontology-vault/map-2026-06-18-dispersed-knowledge.md)
- [../../development/reviews/2026-06-22-operational-ontology-authority-lifecycle-review/findings.md](../../development/reviews/2026-06-22-operational-ontology-authority-lifecycle-review/findings.md)
- [../../../.arcanum/inventory/entries/evidence-sets/2026-06-22-operational-ontology-authority-lifecycle-sets.md](../../../.arcanum/inventory/entries/evidence-sets/2026-06-22-operational-ontology-authority-lifecycle-sets.md)

## CAV2-D20: Craft Method

Status: active
Term: Craft method
Aliases: recursive ledger method, residue-carrying ledger method, Craft recursive method

### Normative Definition

Craft method is a recursive ledger-governance method that turns bounded work
into explicit project state by recording contexts, candidate definitions,
blockers, enablers, decisions, gaps, artifacts, next moves, validation evidence,
residue, and recomposition obligations in a source-of-truth ledger.

In CyberAlchemy v2, Craft method is valid only when it preserves these
boundaries:

- `.craft/ledger.yml` or an equivalent declared ledger is the source of truth
  for Craft state
- `CRAFT.md`, `.craft/index.json`, projections, and status output are derived
  views
- residue is typed and carried forward instead of hidden
- schema-level and instance-level validation are not collapsed
- child contexts recompose into their parent through evidence
- closure happens by owner decision, gate, or accepted residue, not by a claim
  of total final completion
- Craft state can carry local candidate definitions and receipts but cannot
  make terms canonical without definitions-governance

### Formal Interpretation

For a bounded project scope `S`, Craft method operates over a ledger state:

```text
L_S = (C, B, E, D, G, A, N, R)
```

where:

- `C` is the set of contexts or child contexts
- `B` is blockers
- `E` is enablers or available evidence
- `D` is decisions
- `G` is gaps or unresolved obligations
- `A` is artifacts and source references
- `N` is next moves or route obligations
- `R` is typed residue plus recomposition evidence

A Craft step is admissible when it preserves the declared ledger source of
truth, records the operation that changed state, keeps generated views
derivative, and either repairs, types, routes, accepts, or defers residue with an
owner.

Formal-foundations evidence supports this shape by treating residue as typed and
composable, by separating schema-fidelity from instance-fidelity, by showing
that reflection towers assemble without finite total closure, and by justifying
stop criteria based on decision and residue plateau rather than completion. This
is support evidence for the method; it does not prove that an LLM-centered Craft
run achieved a clean functor, kernel, or zero-residue translation.

### Operational Interpretation

Use Craft method when CyberAlchemy v2 needs durable work memory across sessions,
definition towers, authority imports, constitution towers, research packets,
promotion queues, or nested project spaces. The method makes the current state
explicit enough that a human or agent can continue the work without guessing
what is blocked, what is merely candidate, what has evidence, and what must
recompose upward.

### Plain-Language Intuition

Craft method is how the project keeps a living workbench honest: write the state
down, name the leftover problem, decide what can move, and carry the residue
forward instead of pretending the work is finished.

### Domain-Context Voice

In CyberAlchemy v2, Craft method governs how the local Craft execution surface
supports `CAV2-D10` definition towers, `CAV2-D13` authority promotion queues,
authority imports, constitution work, and research handoffs. It lets v2 build
towers with towers while keeping candidate definitions, receipts, and blockers
separate from canonical definitions.

The method connects `CAV2-D12` Craft execution surface, `CAV2-D17` reflection
tower method, and `CAV2-D18` residue. The execution surface is where Craft state
lives; the method is the discipline for carrying state, residue, validation, and
recomposition through recursive work.

### Boundary

Craft method is not the same thing as the Craft execution surface, not a generic
task runner, not a replacement for task-session, not a source of canonical
definitions, and not proof that a translation is complete. It may use formal
foundations as support evidence, but it must preserve their honesty boundary:
formal cousins describe the structure Craft operates inside; they do not certify
that a particular Craft run achieved the clean formal case.

Craft method also does not promote `ledger` as a cross-method primitive by
itself. Ledger remains separately flagged for review until recursivity, relation
inheritance, and local Craft ledger conformance are settled.

### Primary Consumers

- [DEFINITION-TOWERS.md](DEFINITION-TOWERS.md)
- [source-clusters/primordial.md](source-clusters/primordial.md)
- [../../CRAFT.md](../../CRAFT.md)
- [../../.craft/ledger.yml](../../.craft/ledger.yml)
- [../../../arcanum/arcana/craft/SKILL.md](../../../arcanum/arcana/craft/SKILL.md)
- [../../../arcanum/development/craft/CRAFT-FORMAL-FOUNDATIONS.md](../../../arcanum/development/craft/CRAFT-FORMAL-FOUNDATIONS.md)

## CAV2-D21: Four-Facet Action Method

Status: active
Term: four-facet action method
Aliases: governed action facet obligation, governed action facets, action facet obligations, four-facet action primitive, taxonomy-schema-human-machine obligation

### Normative Definition

Four-facet action method is the CyberAlchemy v2 primitive action rule that every
governed action must explicitly bind, create, or record typed residue for four
facets before the action can govern downstream work:

- classification or taxonomy facet
- schema facet
- human-continuation view
- machine-checkable view

A governed action is any CyberAlchemy v2 action that creates, changes, routes,
validates, promotes, implements, or interprets load-bearing artifacts, state,
meaning, or authority posture. The action is admissible only when each facet is
declared or when its absence is carried as typed residue.

At minimum:

- the classification or taxonomy facet states what kind of thing or action is
  involved and which classification catalog, taxonomy, or source vocabulary owns
  that assignment
- the schema facet states the structural shape, field set, relation shape, or
  validation surface that governs the action or artifact
- the human-continuation view states how a human can understand the action's
  purpose, status, trust boundary, blockers, residue, next route, and evidence
- the machine-checkable view states how a machine can parse or check the action
  state, including identifiers, kind, schema reference, classification
  reference, source of truth, validator or proof handle, projection status, and
  residue

If a facet is missing, impossible, or intentionally deferred, the action must
record typed residue naming the missing facet, the reason or impossibility, the
owner route, the evidence reference, and the action effect: continue, defer, or
block. If the action later asks to promote something, the same residue must also
state the promotion effect.

### Formal Interpretation

For a governed action `a`, let:

```text
F(a) = (K_a, S_a, H_a, M_a, R_a)
```

where:

- `K_a` is the classification or taxonomy facet
- `S_a` is the schema facet
- `H_a` is the human-continuation view
- `M_a` is the machine-checkable view
- `R_a` is typed residue for any missing, impossible, or deferred facet

The action satisfies the four-facet action method when each of `K_a`, `S_a`,
`H_a`, and `M_a` is either bound to an existing governed surface, created by the
action, or represented in `R_a` with owner route and effect. The method forbids
silent absence; it does not require perfect completion before exploratory work
can begin.

### Operational Interpretation

Use this method before or during any CyberAlchemy v2 action that may matter
later: definition work, constitution work, axiom work, discipline work, Craft
state changes, ontology projections, task execution, workflow design, system
design, validation, or implementation routing.

The method lets the system act without pretending the four facets already
exist. An action may instantiate existing taxonomy, schema, human view, and
machine view; create one or more missing facets; or declare typed residue for
the missing facets. What is forbidden is a silent action that later relies on an
unstated kind, shape, human continuation path, or machine-checkable state.

### Plain-Language Intuition

Before an action is allowed to matter, it must answer four questions: what kind
of thing is this, what shape governs it, how can a human continue it, and how
can a machine check it? If one answer is missing, write down the missing piece,
who owns it, and whether the action can continue.

### Domain-Context Voice

In CyberAlchemy v2, this term corrects the four-facet research finding so it is
not limited to promotion candidates. It is the base action method for work in
definitions, constitutions, axioms, disciplines, tasks, systems, workflows,
Craft, ontology, validation, and implementation routing. Promotion gates remain
stricter downstream uses of the same method, not the method's whole scope.

This method connects `CAV2-D16` typed coupling invariant, `CAV2-D18` residue,
and `CAV2-D20` Craft method. If a schema affects authority, if a classification
affects ontology, if a human view constrains execution, or if a machine view
feeds validation, the coupling must be typed. If any facet cannot be supplied,
the missing facet becomes typed residue with owner and effect.

### Boundary

Four-facet action method is not a promotion gate by itself, not proof of
authority, not a requirement that all exploratory work have perfect schemas
before it starts, and not a single required file format. It allows an action to
create missing facets or carry typed residue.

Generic `schema` semantics remain Arcanum-owned unless CyberAlchemy v2 later
defines a narrow local subtype. A classification facet is not ontology
membership or promotion. A human-continuation view is not canonical merely
because it is readable. A machine-checkable view is not authority and is not
proof beyond the named checks it can actually run.

### Primary Consumers

- [../../development/research/2026-06-21-schema-taxonomy-view-primitives/ACTION-PRIMITIVE-CORRECTION.md](../../development/research/2026-06-21-schema-taxonomy-view-primitives/ACTION-PRIMITIVE-CORRECTION.md)
- [../../development/research/2026-06-21-schema-taxonomy-view-primitives/findings.md](../../development/research/2026-06-21-schema-taxonomy-view-primitives/findings.md)
- [DEFINITION-TOWERS.md](DEFINITION-TOWERS.md)
- [source-clusters/primordial.md](source-clusters/primordial.md)
- Future `Four-Facet Action Constitution`

## CAV2-D22: Orthogonal Classification

Status: active
Term: orthogonal classification
Aliases: orthogonal ontology basis, orthogonal label discipline, retrieval-entropy classification, unique-information classification

### Normative Definition

Orthogonal classification is the CyberAlchemy v2 rule that a governed
classification axis, taxonomy label, or ontology grouping is admissible only
when it contributes a distinction that is not silently redundant with an
existing axis, label, owner lane, lifecycle state, schema field, or typed
relation.

A classification is orthogonal when changing it does not secretly change a
different authority axis. If a proposed classification cannot stay independent,
its dependency must be represented through `CAV2-D16` typed coupling invariant
before it can govern downstream work.

### Formal Interpretation

For a classified artifact `x`, let:

```text
K(x) = (k_1, k_2, ..., k_n)
```

where each `k_i` is an owned classification axis. A proposed axis `k_p` is
admissible when it contributes a unique operational distinction that cannot be
derived from the existing `K(x)`, or when every dependency between `k_p` and an
existing axis is recorded as a typed coupling with direction, owner, evidence,
and effect.

When data exists, an implementation may use mutual-information, entropy, or
retrieval-precision checks as evidence for uniqueness. When data does not
exist, review must name the unique question, routing decision, or validation
effect the classification adds.

In this definition, orthogonality is an admission and compression discipline:
it asks whether a label or axis contributes independent operational
information. It is not Hilbert-space orthogonality, not a contextuality
obstruction, and not a proof that cross-document consistency has been achieved.
Consistency claims must come from typed relations, schema rules, validators, or
owner decisions, not from the word "orthogonal" by itself.

### Operational Interpretation

Use orthogonal classification when adding taxonomy, ontology, status,
confidence, maturity, source-role, node-type, or task-kind labels. The action
must answer what new distinction the classification adds, what existing axes it
could be confused with, and whether any unavoidable dependency is explicitly
typed.

### Plain-Language Intuition

Do not add another label unless it tells the project something new. If the label
depends on another label, name that dependency instead of pretending the labels
are independent.

### Domain-Context Voice

In CyberAlchemy v2, this definition promotes the imported vault's orthogonality
and retrieval-entropy evidence into a project-local classification rule. It
supports ontology work, definition towers, authority lifecycle work, and the
four-facet action method by keeping classification separate from schema,
promotion, confidence, evidence, and implementation state.

### Boundary

Orthogonal classification is not a requirement that every classifier be
statistically proven before exploratory work begins. It is also not isolation:
classifications may interact, but the interaction must be represented through a
typed coupling, schema rule, or explicit residue.

This term does not authorize treating Shannon-style label independence and
Hilbert-style projector orthogonality as the same formal object. Any bridge
between classification independence and contextuality machinery must be
recorded as a separate typed coupling or rejected residue.

The imported house_project label system remains source evidence. CyberAlchemy
v2 may adopt the orthogonality rule without adopting that source's exact node
types, labels, metrics, or status vocabulary.

### Primary Consumers

- [../imports/house_project/docs/vault/ontology-conventions.md](../imports/house_project/docs/vault/ontology-conventions.md)
- [../imports/house_project/docs/vault/axiom/ontology-axioms.md](../imports/house_project/docs/vault/axiom/ontology-axioms.md)
- [../../../.arcanum/inventory/entries/evidence-cards/2026-06-21-house-project-vault-cards.md](../../../.arcanum/inventory/entries/evidence-cards/2026-06-21-house-project-vault-cards.md)
- [source-clusters/primordial.md](source-clusters/primordial.md)
- [DEFINITION-TOWERS.md](DEFINITION-TOWERS.md)

## CAV2-D23: Authority Lifecycle Axis

Status: active
Term: authority lifecycle axis
Aliases: confidence lifecycle axis, authority axis split, maturity-evidence-commitment split, status-veracity-conviction split

### Normative Definition

Authority lifecycle axis is the CyberAlchemy v2 rule that authority posture must
separate at least these dimensions when they matter to a decision:

- role or kind
- maturity or status
- evidence confidence
- commitment or conviction
- provenance
- owner

No one axis may silently stand in for another. A definition can be mature but
weakly evidenced, an imported source can be well-evidenced but not locally
canonical, an ontology candidate can be useful but unpromoted, and an owner can
be committed to a hypothesis without that hypothesis becoming authority.

### Formal Interpretation

An authority-bearing artifact `a` has lifecycle posture:

```text
L(a) = (kind, status, evidence, commitment, provenance, owner, residue)
```

where each component may be known, unknown, deferred, or source-local. A
governance move is valid only if it changes the intended component and does not
imply changes to the others unless those changes are explicitly recorded.

### Schema

Schema handle: `CAV2-D23-SCHEMA` — tracked in
[DEFINITION-SCHEMAS.md](DEFINITION-SCHEMAS.md).
Status: tracked (documentary).
Bound to: `CAV2-D23` authority lifecycle axis.

Lifecycle posture record:

```text
L(a) = (kind, status, evidence, commitment, provenance, owner, residue)
```

| Field | Meaning | Value posture |
| --- | --- | --- |
| `kind` | role or artifact kind of `a` | known, unknown, deferred, or source-local |
| `status` | maturity or lifecycle state | known, unknown, deferred, or source-local |
| `evidence` | evidence confidence | known, unknown, deferred, or source-local |
| `commitment` | owner conviction or commitment | known, unknown, deferred, or source-local |
| `provenance` | source or origin | known, unknown, deferred, or source-local |
| `owner` | responsible owner route | known, unknown, deferred, or source-local |
| `residue` | unresolved remainder per `CAV2-D18` | typed residue or none |

Schema invariant: a governance move changes the intended field without implying
a change to the others unless an explicit typed coupling (`CAV2-D16`) records the
link. This schema is documentary; a machine-checkable validator is a deferred
follow-up recorded in the registry. Schema changes follow `CAV2-D25` schema
amendment witness.

### Operational Interpretation

Use authority lifecycle axes when evaluating definitions, constitutions, axioms,
ontology nodes, inventory cards, task results, schemas, and implementation
claims. The reviewer should ask which axis is being advanced: source role,
maturity, evidence, owner commitment, provenance, or canonical authority.

### Plain-Language Intuition

"Useful", "trusted", "finished", "owned", and "canonical" are different words.
Do not let one of them impersonate the others.

### Domain-Context Voice

In CyberAlchemy v2, this definition absorbs the imported vault's mature split
between `node_type`, `status`, evidence confidence, and commitment language as a
local lifecycle principle. The source vocabulary is evidence, while CAV2 keeps
the more general axis split so Arcanum, DomainSpec, house_project, ontology,
inventory, Craft, and future implementation artifacts can share one governance
shape without sharing one exact status taxonomy.

### Boundary

Authority lifecycle axis is not a complete status schema and does not make
every artifact an ontology node. It gives the minimum separations that future
schemas, ledgers, and constitutions must preserve.

### Primary Consumers

- [../imports/house_project/docs/vault/ontology-conventions.md](../imports/house_project/docs/vault/ontology-conventions.md)
- [../imports/house_project/docs/vault/premise/ontology-premises.md](../imports/house_project/docs/vault/premise/ontology-premises.md)
- [../imports/house_project/docs/vault/confidence-levels.md](../imports/house_project/docs/vault/confidence-levels.md)
- [../../../.arcanum/inventory/entries/evidence-cards/2026-06-21-authority-node-relationship-taxonomy-cards.md](../../../.arcanum/inventory/entries/evidence-cards/2026-06-21-authority-node-relationship-taxonomy-cards.md)
- [../../../.arcanum/inventory/entries/evidence-cards/2026-06-21-house-project-vault-cards.md](../../../.arcanum/inventory/entries/evidence-cards/2026-06-21-house-project-vault-cards.md)

## CAV2-D24: Provenance-First Navigation

Status: active
Term: provenance-first navigation
Aliases: constitution-first traversal, source-indexed navigation, session-as-provenance navigation, graph-indexed lookup

### Normative Definition

Provenance-first navigation is the CyberAlchemy v2 search method that begins
from governed entrypoints, constitutions, definition indexes, inventory cards,
source manifests, and graph/index surfaces before opening broad conversation,
session, or raw source material.

Sessions and raw exploratory files may explain why a decision emerged, but they
must not be treated as the first or only authority surface when indexed
provenance, canonical sources, or owner-authored read models exist.

### Formal Interpretation

For a query `q`, provenance-first navigation builds a selector ladder:

```text
N(q) = (entrypoint, authority_surface, inventory_or_index, source_manifest,
        primary_source, provenance_session, residue)
```

The search may skip empty layers, but it must preserve the distinction between
canonical authority, read-model evidence, imported source, and provenance
session.

### Operational Interpretation

Use provenance-first navigation when searching CyberAlchemy v2, imported vaults,
ontology material, definitions, constitutions, or prior research. Start with the
nearest index and source manifest, then follow typed source references. Open
sessions or raw conversation logs only after the route needs historical
rationale, conflict evidence, or unreduced residue.

### Plain-Language Intuition

Read the map before walking the whole city. Use sessions for why, not as the
default place to discover what counts.

### Domain-Context Voice

In CyberAlchemy v2, this definition turns the imported vault's agent navigation
and graph-index pattern into a stable repository search rule. It also reinforces
the Inventory boundary: Inventory shortens lookup and supplies evidence cards,
but it does not promote authority by itself.

### Boundary

Provenance-first navigation is not a ban on reading source files. It is a
sequencing rule that protects search cost, provenance, and authority posture.
If indexes are stale or absent, the missing index becomes residue or a route for
Inventory, not permission to blur source authority.

### Primary Consumers

- [../imports/house_project/docs/vault/agent-navigation.md](../imports/house_project/docs/vault/agent-navigation.md)
- [../imports/house_project/docs/vault/graph-edges.md](../imports/house_project/docs/vault/graph-edges.md)
- [../imports/house_project/docs/vault/graph-session-index.md](../imports/house_project/docs/vault/graph-session-index.md)
- [../../../.arcanum/inventory/index.md](../../../.arcanum/inventory/index.md)
- [../../../.arcanum/inventory/entries/evidence-cards/2026-06-21-house-project-vault-cards.md](../../../.arcanum/inventory/entries/evidence-cards/2026-06-21-house-project-vault-cards.md)

## CAV2-D25: Schema Amendment Witness

Status: active
Term: schema amendment witness
Aliases: schema amendment discipline, runtime witness, schema-evolution witness, enforcement witness

### Normative Definition

Schema amendment witness is the CyberAlchemy v2 rule that any schema,
frontmatter, taxonomy, ontology, ledger, event, or machine-view change that
affects validation or authority interpretation must carry both:

- an amendment record naming owner, scope, reason, changed shape, source
  evidence, compatibility effect, and rollout or rollback route
- a witness naming the validator, runtime observation, fixture, review check,
  or typed residue that shows how the changed rule is enforced or why it cannot
  yet be enforced

### Formal Interpretation

For an authority-affecting shape change `s -> s'`, a valid amendment is:

```text
A = (owner, scope, source, delta, compatibility, witness, residue)
```

where `witness` may be deterministic, hybrid, review-based, or absent only when
the absence is typed as residue with owner and effect. The amendment is not
complete if the changed shape can govern downstream work but has no declared
enforcement or residue path.

### Operational Interpretation

Use schema amendment witness before changing frontmatter rules, ontology node
schemas, inventory entry schemas, event catalogs, ledger row identity, machine
envelopes, validation fixtures, or constitution-controlled structure. The
minimum action is to say what changed, who owns it, what evidence justifies it,
what may break, and what witness checks or carries the change.

### Plain-Language Intuition

If the shape changes, leave a receipt and show what will catch mistakes. If
nothing catches them yet, say that out loud and assign the gap.

### Domain-Context Voice

In CyberAlchemy v2, this definition promotes the imported vault's schema
amendment and runtime-witness patterns into a general governance concept. It
binds directly to `CAV2-D21` four-facet action method because schema and
machine-checkable views must either exist, be created, or be recorded as typed
residue.

### Boundary

Schema amendment witness does not redefine generic `schema`; Arcanum-wide
schema semantics remain external authority unless CyberAlchemy v2 later defines
a narrower subtype. It also does not require a fully automated validator for
every early rule. Review and typed residue are acceptable witnesses when the
artifact is not yet implementation-backed.

### Primary Consumers

- [../imports/house_project/docs/vault/constitution/framework/schema-amendment-discipline-constitution.md](../imports/house_project/docs/vault/constitution/framework/schema-amendment-discipline-constitution.md)
- [../imports/house_project/docs/vault/constitution/framework/frontmatter-ownership-constitution.md](../imports/house_project/docs/vault/constitution/framework/frontmatter-ownership-constitution.md)
- [../imports/house_project/docs/vault/constitution/framework/edge-acyclicity-constitution.md](../imports/house_project/docs/vault/constitution/framework/edge-acyclicity-constitution.md)
- [../../../.arcanum/inventory/entries/evidence-cards/2026-06-21-house-project-vault-cards.md](../../../.arcanum/inventory/entries/evidence-cards/2026-06-21-house-project-vault-cards.md)
- Future schema and machine-view validators

## CAV2-D26: Append-Only Event Ledger

Status: active
Term: append-only event ledger
Aliases: append-only ledger, idempotent event ledger, event-sourced authority ledger, deterministic event ledger

### Normative Definition

Append-only event ledger is a CyberAlchemy v2 ledger pattern for state-changing
or authority-affecting operations where each change is recorded as an additive
event instead of silently rewriting prior state.

An append-only event ledger must preserve:

- registered event kinds or event catalog membership
- deterministic subject or stream identity
- idempotency key or duplicate-guard rule for retryable operations
- event payload or source reference
- actor, owner, or route
- timestamp or ordering handle
- replay, projection, or human-audit interpretation

### Formal Interpretation

For an event stream `E = [e_1, ..., e_n]`, current projected state is:

```text
P(E) = fold(apply, initial_state, E)
```

A new event `e_{n+1}` may be appended when its event kind is admitted, its
subject identity is deterministic, and its idempotency handle prevents a retry
from producing a second semantic change. Corrections are represented by new
events, not untracked mutation of the old event.

### Operational Interpretation

Use append-only event ledger for imports, promotions, schema amendments,
authority movement, idempotent generation, task receipts, validation runs, or
runtime events when replay and audit matter. The ledger may project current
state into indexes or ontology views, but the projection is derivative.

### Plain-Language Intuition

Record what happened as a new line. If the same action is retried, it should
not count twice. If something was wrong, add the correction instead of erasing
the trace.

### Domain-Context Voice

In CyberAlchemy v2, this definition adopts the imported vault's event-system
precedent as a narrow ledger pattern. It supports authority imports, promotion
records, schema amendments, Craft receipts, and future implementation events
without yet declaring generic `ledger` to be a universal primitive.

### Boundary

Append-only event ledger is not the same as `CAV2-D20` Craft method and does
not promote the unresolved generic `ledger` primitive. It is one ledger pattern
for operations where event order, retry behavior, and projection traceability
matter.

### Primary Consumers

- [../imports/house_project/docs/vault/constitution/event-system-constitution.md](../imports/house_project/docs/vault/constitution/event-system-constitution.md)
- [../../../.arcanum/inventory/entries/evidence-cards/2026-06-21-house-project-vault-cards.md](../../../.arcanum/inventory/entries/evidence-cards/2026-06-21-house-project-vault-cards.md)
- [../../../.arcanum/inventory/entries/evidence-cards/2026-06-21-authority-harness-ledger-ontology-cards.md](../../../.arcanum/inventory/entries/evidence-cards/2026-06-21-authority-harness-ledger-ontology-cards.md)
- [reviews/ledger-primitive-review.md](reviews/ledger-primitive-review.md)

## CAV2-D27: Residue Entropy

Status: active
Term: residue entropy
Aliases: entropy observable, typed entropy observable, entropy readout, residue measure, residue measurement

### Normative Definition

Residue entropy is a CyberAlchemy v2 primitive observable for typed residue: it
measures the distinguishability, uncertainty, or information loss exposed by a
transformation, translation, coarse-graining, classification, validation, or
governance operation after the residue type and source operation have been
declared.

Residue entropy may influence authority, routing, validation, ontology, or
implementation only when the entropy claim declares:

- entropy register or mathematical reading
- source operation or transformation
- typed residue source
- measure or observable used
- finite, weighted, retrieval, probabilistic, or categorical scope
- theorem, conjecture, analogy, or review status
- authority effect or non-governing residue treatment

### Formal Interpretation

For a finite probabilistic residue object `R` with finite carrier `F_R` and
probability mass function `rho`, the residue entropy observable is:

```text
H(R) = sum_{x in F_R} negMulLog(rho(x))
```

In the finite microcanonical macrostate bridge, for a coarse-graining
`f : M -> M'`:

```text
S_f(m') = log |fiber_f(m')|
```

and positive entropy marks fully-faithful residue:

```text
S_f(m') > 0  <->  m' in ffNoise(f)
```

This makes finite Boltzmann entropy a readout of `Residue_FF(Macro)`, not a
replacement for the broader `CAV2-D18` residue primitive.

### Operational Interpretation

Use residue entropy when a CyberAlchemy v2 artifact needs to compare, rank,
route, or validate typed residue by a quantitative or categorical observable.
Valid examples include finite Shannon entropy on a `ResidueObject`, Boltzmann
`log |fiber|` in a finite coarse-graining bridge, KL or entropy-gap evidence in
a declared finite-support setting, retrieval entropy as evidence for
classification uniqueness, or an entropy profile over a declared residue chain.

Before using the observable as evidence, the artifact must name what residue is
being measured and which register supplies the measure. If the register cannot
be named, the claim remains analogy, research pressure, or typed residue.

### Plain-Language Intuition

Residue entropy is how much meaningful distinction the current layer collapsed
or left unnamed.

### Domain-Context Voice

In CyberAlchemy v2, residue entropy sits below `CAV2-D18` residue and beside
`CAV2-D22` orthogonal classification. It lets the project reuse Lean-backed
entropy evidence without turning every entropy mention into a global primitive
or treating retrieval entropy, Boltzmann entropy, Gibbs entropy, KL divergence,
and entropy profiles as interchangeable. The matching constitution rule
requires durable entropy claims to declare their register and residue source.

### Boundary

Residue entropy is not generic disorder, not uncertainty by itself, not proof of
novelty, and not automatic promotion. Non-numeric residue may still be valid and
actionable. Weighted, Gibbs, continuous, Markov-category, free-energy, RG, or
physical second-law claims require their own typed bridge before they may govern
CyberAlchemy v2 authority.

### Primary Consumers

- [DEFINITION-TOWERS.md](DEFINITION-TOWERS.md)
- [DEFINITION-DRIFT-AUDIT.md](DEFINITION-DRIFT-AUDIT.md)
- [../constitutions/STABLE-REPOSITORY-CONSTITUTION.md](../constitutions/STABLE-REPOSITORY-CONSTITUTION.md)
- `domainspec-lean-formalization/lean-formalization/Residue.lean` (embedded local source evidence)
- `domainspec-lean-formalization/lean-formalization/EntropyAsFFResidue.lean` (embedded local source evidence)
- `domainspec-lean-formalization/lean-formalization/SecondLawDiscrete.lean` (embedded local source evidence)
- `domainspec-lean-formalization/THERMODYNAMICS.md` (embedded local source evidence)

## CAV2-D28: Value-Cycle Edge Guard

Status: active
Term: value-cycle edge guard
Aliases: edge contextuality guard, value-constraining cycle guard, contextuality tripwire, edge non-contextuality guard

### Normative Definition

A value-cycle edge guard is the CyberAlchemy v2 invariant that no relation,
edge type, or ontology movement may simultaneously:

- constrain the value, label, authority state, schema field, or validation
  outcome of another artifact; and
- be allowed to participate in a cycle without an explicit acyclicity
  constraint.

If a proposed relation needs both properties, it must stop at schema governance
and receive a contextuality-obstruction review before it can influence
authority, ontology, validation, or implementation.

### Formal Interpretation

For any proposed edge type `E`, define two review predicates:

```text
value_constraining(E)
cycle_permitted(E)
```

CyberAlchemy v2 requires:

```text
not (value_constraining(E) and cycle_permitted(E))
```

unless a schema owner records an explicit exception with source evidence,
constraint semantics, satisfiability or obstruction review, validator or review
witness, and typed residue.

The current guard is a watch condition, not a theorem. It is satisfied when
value-constraining edges are acyclic and cycle-permitted edges do not constrain
values. It becomes live only when a proposed edge straddles both classes.

### Operational Interpretation

Use this guard when adding or revising ontology relations, relationship
families, edge catalogs, movement edges, schema links, authority transitions, or
validation-affecting graph rules. If the new edge can force a value or state
and can also form cycles, block the promotion until the review names what
constraints could fail to glue, what validator or reviewer will catch that
failure, and which owner accepts the remaining residue.

### Plain-Language Intuition

An edge can either force a value or freely loop around the graph. If it does
both, stop and prove the loop is safe before it becomes a rule.

### Domain-Context Voice

In CyberAlchemy v2, the TO-VLAD AX-ONT review killed the attempted bridge from
Shannon-style classification orthogonality to Lean Hilbert/projector
orthogonality. The reusable residue is this edge-layer guard: coupling lives in
relations, so the first dangerous place is an edge that both constrains values
and may cycle. CAV2 keeps that condition explicit instead of letting a future
schema change create contextuality-like residue by accident.

### Boundary

Value-cycle edge guard is not a contextuality theorem, not a spectral-presheaf
checker, not a ban on cyclic non-value relations, and not a ban on acyclic
value constraints. It does not promote any live vault edge family. It only says
which edge proposals must be stopped for schema governance and obstruction
review.

### Primary Consumers

- [../constitutions/STABLE-REPOSITORY-CONSTITUTION.md](../constitutions/STABLE-REPOSITORY-CONSTITUTION.md)
- [../../ontology/RELATION-MODEL.md](../../ontology/RELATION-MODEL.md)
- [../../TO-VLAD/TO-VLAD.md](../../TO-VLAD/TO-VLAD.md)
- [../../TO-VLAD/RESOLUTION.md](../../TO-VLAD/RESOLUTION.md)

## CAV2-D29: Axis Orthogonality Invariant

Status: active
Term: axis orthogonality invariant
Aliases: orthogonality, orthogonal-axis invariant, independent-axis invariant, non-implied progress invariant

### Normative Definition

Axis orthogonality invariant is the CyberAlchemy v2 rule that two
authority-bearing dimensions, roles, states, owner lanes, schema or instance
axes, validation concerns, or artifact properties are treated as independently
variable unless an explicit typed relation, gate, schema rule, validator, or
owner decision relates them.

Advancing one axis must not silently advance, validate, authorize, satisfy, or
rewrite another axis. If a decision depends on such co-change, the dependency
must be represented through `CAV2-D16` typed coupling invariant before it can
govern work.

### Formal Interpretation

For a governed context `C`, let:

```text
A(C) = {a_1, a_2, ..., a_n}
```

be the declared axes that matter to a decision. Axes `a_i` and `a_j` are
orthogonal for decision `d` when a valid move on `a_i` does not imply a move on
`a_j` unless there is an explicit bridge:

```text
move(a_i) does not imply move(a_j) unless R_ij is declared
```

where `R_ij` is a typed coupling, gate, schema rule, validator, or owner
decision with named endpoints, direction or symmetry, evidence, and effect.

### Operational Interpretation

Use this invariant before merging or ordering concepts such as maturity and
promotion, evidence confidence and owner commitment, schema residue and
instance residue, role and lane, source evidence and local canon, built status
and authority status, or workflow state and lifecycle status.

When the question is whether a new label or classifier adds independent
information, use `CAV2-D22` orthogonal classification. When the question is
which authority lifecycle component changed, use `CAV2-D23` authority lifecycle
axis. When the axes are not independent, use `CAV2-D16` typed coupling
invariant.

### Plain-Language Intuition

Moving one slider should not secretly move another slider. If it does, name the
wire between them.

### Domain-Context Voice

In CyberAlchemy v2, axis orthogonality is the broader primordial invariant behind
several already promoted local rules. `CAV2-D22` specializes it for
classification admission, `CAV2-D23` applies it to authority lifecycle posture,
and `CAV2-D16` handles the cases where independence fails. It lets the v2 base
separate ontology from authority movement, schema from instance evidence,
promotion from maturity, and source truth from local adoption without pretending
those axes cannot interact.

### Boundary

Axis orthogonality is not isolation, not statistical independence unless a data
model explicitly says so, not Hilbert-space or projector orthogonality, not a
contextuality theorem, and not a consistency guarantee. It is a governance
invariant about non-implied movement between axes. Interactions are allowed, but
they must be explicit.

### Primary Consumers

- [source-clusters/primordial.md](source-clusters/primordial.md)
- [DEFINITION-TOWERS.md](DEFINITION-TOWERS.md)
- [../../CRAFT.md](../../CRAFT.md)
- [../../TO-VLAD/TO-VLAD.md](../../TO-VLAD/TO-VLAD.md)
- [../../../.arcanum/inventory/entries/evidence-cards/2026-06-22-presheaf-vect-novelty-orthogonality-cards.md](../../../.arcanum/inventory/entries/evidence-cards/2026-06-22-presheaf-vect-novelty-orthogonality-cards.md)

## CAV2-D30: Bounded Recursive Self-Application

Status: active
Term: bounded recursive self-application
Aliases: recursivity, bounded recursivity, recursive self-application, process recursion, altitude-bounded recursion

### Normative Definition

Bounded recursive self-application is the CyberAlchemy v2 invariant that a
governed process may be applied to artifacts produced by that same process only
when each recursive step declares its artifact, altitude or layer, scope, owner,
gate, carried state or residue, recomposition path, and stopping condition.

The recursive move must preserve authority boundaries: the process, the artifact
being processed, the owner route, and the resulting authority posture must remain
distinct unless an explicit promotion or coupling records otherwise.

### Formal Interpretation

Given a governed process `P`, an artifact `a_n` already produced, shaped, or
maintained by `P`, and an altitude marker `h_n`, a valid recursive
self-application step has the form:

```text
P_hn(a_n) -> a_(n+1) at h_(n+1)
```

The step is admissible only if it records:

- source artifact `a_n`
- target artifact `a_(n+1)`
- altitude or layer relation between `h_n` and `h_(n+1)`
- owner route
- gate or validation condition
- residue or state carried forward
- recomposition path back to the lower artifact or parent context
- stopping condition, budget, or explicit next owner

Without those fields, the move is ordinary recursion, self-hosting, looped work,
or open residue, not CyberAlchemy v2 recursivity.

### Operational Interpretation

Use bounded recursive self-application when definitions-governance defines
definition work, Craft records and routes work about Craft, CyberAlchemy applies
its method to CyberAlchemy method artifacts, or a tower creates a higher-layer
artifact that must explain back down to its source.

The action must answer: what artifact is the method operating on, at what
altitude, under which owner and gate, what residue or state is carried, how the
result recomposes with the source, and where the recursion stops or hands off.

### Plain-Language Intuition

The system can use its own method on its own work, but each loop needs a label,
a boundary, a reviewer, and a way back.

### Domain-Context Voice

In CyberAlchemy v2, this definition resolves the earlier `recursivity` candidate
by promoting the bounded form rather than the vague label. It sits beside
`CAV2-D17` reflection tower method and `CAV2-D20` Craft method: reflection tower
names the residue-to-higher-layer move, Craft method names the recursive ledger
discipline, and bounded recursive self-application names the cross-method
invariant that lets a governed method operate on its own artifacts without
collapsing authority surfaces.

This definition partially unblocks the ledger primitive review: `recursivity`
now has a local meaning, but ledger promotion still depends on inheritance
relations and local Craft ledger conformance.

### Boundary

Bounded recursive self-application is not ordinary code recursion, not generic
self-hosting, not endless reflection, not child-folder nesting, not automatic
promotion, and not a license to run agents recursively without a budget. It does
not replace `CAV2-D17` reflection tower method or `CAV2-D20` Craft method; it
governs when process-on-own-artifact moves are admissible across those and
other methods.

### Primary Consumers

- [source-clusters/primordial.md](source-clusters/primordial.md)
- [reviews/ledger-primitive-review.md](reviews/ledger-primitive-review.md)
- [DEFINITION-TOWERS.md](DEFINITION-TOWERS.md)
- [../../CRAFT.md](../../CRAFT.md)
- [../../development/research/2026-06-21-recursivity-promotion-verdict/findings.md](../../development/research/2026-06-21-recursivity-promotion-verdict/findings.md)

## CAV2-D31: Primitive Type

Status: active
Term: primitive type
Aliases: semantic primitive type, primitive semantic type, base semantic object, semantic primitive

### Normative Definition

A primitive type is a CyberAlchemy v2 base semantic kind that lower definitions,
methods, constitutions, disciplines, schemas, ontology records, or execution
artifacts may reference without deriving its meaning from a narrower source
space, implementation layer, project glossary, or generated representation.

To count as a primitive type, the term must declare its stable name, authority
scope, allowed consumers, source-evidence boundary, relation to any external
authority term, and the condition under which lower layers may specialize it.
Lower layers may instantiate, specialize, or compose a primitive type, but they
must not silently redefine it.

### Formal Interpretation

For a CyberAlchemy v2 term `t`, `primitive_type(t)` is admissible only when:

```text
authority_scope(t) = CAV2
owner(t) = definitions-governance
derived_from_narrower_source_space(t) = false
boundary(t) is declared
consumer_surface(t) is declared
specialization_rule(t) is declared
```

If `t` is borrowed from an external authority, the primitive claim applies only
to CyberAlchemy v2's local role for `t`, not to the external authority's whole
meaning.

### Operational Interpretation

Use this term when deciding whether a candidate belongs in the primordial basis
rather than a lower tower. A primitive type should be small enough for multiple
towers to reuse, but strict enough that lower artifacts cannot stretch it by
vibe, proximity, or repeated use.

### Plain-Language Intuition

A primitive type is a base kind the project is allowed to build with before it
builds narrower things.

### Domain-Context Voice

In CyberAlchemy v2, primitive type names the role played by local bases such as
axis orthogonality, bounded recursive self-application, residue, method, and
definition. It also keeps CAV2 local primitives separate from DomainSpec
meta-types, Arcanum schema/contract terms, programming types, and ontology node
types. Those may be evidence or external references, but they become CAV2
primitive types only when this file re-authors the local semantic role.

### Boundary

Primitive type is not a programming-language primitive, not a database field
type, not a schema class, not a DomainSpec `DS-D1` meta-type, not a source
glossary label, and not automatic authority for any term called "primitive" in
another folder.

### Primary Consumers

- [source-clusters/primordial.md](source-clusters/primordial.md)
- [DEFINITION-TOWERS.md](DEFINITION-TOWERS.md)
- [DEFINITION-LOCALIZATION-ROUTE.md](DEFINITION-LOCALIZATION-ROUTE.md)
- [../../CRAFT.md](../../CRAFT.md)

## CAV2-D32: Method

Status: active
Term: method
Aliases: governed method, method primitive, repeatable governance method

### Normative Definition

A method is a governed repeatable way to transform intent, source evidence,
state, or residue into artifacts and continued work under declared roles,
actions or phases, gates, validation conditions, residue handling, provenance,
and recomposition or evolution rules.

A method may be instantiated by a narrower named method, such as `CAV2-D17`
reflection tower method, `CAV2-D20` Craft method, or `CAV2-D21` four-facet
action method. The generic term names the umbrella role; each concrete method
must still declare its own scope, inputs, outputs, gates, and boundaries.

### Formal Interpretation

For a method `M`, an admissible CyberAlchemy v2 method record has at least:

```text
M = (scope, inputs, actions, roles, gates, outputs, evidence,
     residue_rule, validation_rule, recomposition_rule, boundary)
```

The method is repeatable when another execution can identify which fields are
being reused, which are being specialized, and which residue remains open.

### Operational Interpretation

Use this term when deciding whether a repeated CyberAlchemy move is merely a
task habit, an implementation pipeline, a technique, a lifecycle label, or a
governed method. A method can use engines, pipelines, checklists, ledgers,
schemas, agents, or workflows, but it is not identical to any one of them
unless the concrete definition says so.

### Plain-Language Intuition

A method is the repeatable way the project turns intent and evidence into work
that can be checked, carried forward, and improved.

### Domain-Context Voice

In CyberAlchemy v2, method is the umbrella term that lets the project compare
the CyberAlchemy Method source material, Craft method, reflection tower method,
four-facet action method, promotion routes, and later runtime workflows without
collapsing them into one pipeline. This is why `method` belongs in the
primordial basis: lower towers can build their own methods, but their method
claims must remain explicit and reviewable.

### Boundary

Method is not a single technique, not a one-off task, not a mere checklist, not
an engine, not a pipeline, not a lifecycle state, and not authority by itself.
Authority comes from the owner surface and gate that admit a method into a
particular use.

### Primary Consumers

- [source-clusters/primordial.md](source-clusters/primordial.md)
- [DEFINITION-TOWERS.md](DEFINITION-TOWERS.md)
- [../../CRAFT.md](../../CRAFT.md)
- [../../../arcanum/framework/CYBERALCHEMY-METHOD.md](../../../arcanum/framework/CYBERALCHEMY-METHOD.md)

## CAV2-D33: Definition

Status: active
Term: definition
Aliases: governed definition, canonical definition, definition unit, semantic definition unit

### Normative Definition

A definition is a governed semantic unit that assigns a term its normative
meaning inside a declared authority scope, with a stable identifier when the
scope uses identifiers, a status, aliases, colocated definition voices,
boundaries, source or provenance references, primary consumers, index presence,
and a drift route.

In CyberAlchemy v2, a candidate row, glossary note, source quote, research
finding, inventory card, generated index entry, or narrative explanation is not
a definition until definitions-governance promotes or updates it in the
canonical definitions source.

### Formal Interpretation

An admissible CyberAlchemy v2 definition record has the shape:

```text
Definition =
  (id, term, status, aliases, normative_voice, plain_language_voice,
   domain_context_voice, boundary, provenance_or_sources,
   consumers, index_entry, drift_route)
```

The normative voice determines meaning. Plain-language and domain-context
voices explain and locate the term, but they do not override the normative
voice.

### Operational Interpretation

Use this term when deciding whether a piece of wording is allowed to govern
CyberAlchemy v2 semantics. If a term is only represented in a source cluster,
inventory card, tower map, handoff, or discussion, it is still candidate
material. To become a definition, it must enter this file with the required
voices and synchronized lookup surfaces.

### Plain-Language Intuition

A definition is the place where a term is finally allowed to mean something for
this project.

### Domain-Context Voice

In CyberAlchemy v2, definition keeps the v2 authority surface honest while the
project imports scattered vocabulary from Arcanum, DomainSpec, prior
CyberAlchemy work, framework-unification, vaults, research, and validation
evidence. The project may localize all of that material for search and Craft
execution, but only this definitions surface can make a CyberAlchemy v2 term
canonical.

### Boundary

Definition is not a glossary hint, not a candidate source-cluster row, not a
research claim, not an inventory evidence card, not an ontology node by itself,
not a generated lookup row, and not a comment thread. Those surfaces may supply
evidence or navigation, but they cannot silently redefine a canonical term.

### Primary Consumers

- [DEFINITIONS-INDEX.md](DEFINITIONS-INDEX.md)
- [source-clusters/primordial.md](source-clusters/primordial.md)
- [DEFINITION-DRIFT-AUDIT.md](DEFINITION-DRIFT-AUDIT.md)
- [DEFINITION-LOCALIZATION-ROUTE.md](DEFINITION-LOCALIZATION-ROUTE.md)
- [../../CRAFT.md](../../CRAFT.md)

## CAV2-D34: Constitution

Status: active
Term: constitution
Aliases: governed constitution, constitution artifact, structure constitution, modular constitution

### Normative Definition

A constitution is a governed authority artifact that fixes the required
structure, form, or composition rules an artifact class or workspace must obey,
without absorbing the term, decision, discipline, or runtime-contract authority
owned by other surfaces. A constitution constrains shape — sections, fields,
ordering, invariants, admissibility, and import or composition rules; it does
not by itself define vocabulary, decide a contested choice, or implement
behavior.

In CyberAlchemy v2, a candidate rule, imported axiom, narrative convention, or
research recommendation is not a constitution until constitution-governance
promotes it into an `authority/constitutions/` surface.

### Formal Interpretation

An admissible CyberAlchemy v2 constitution record has at least:

```text
Constitution =
  (id, scope, governed_artifact_class, structure_rules, invariants,
   composition_or_import_rules, owner_route, source_or_provenance,
   enforcement_or_witness, residue)
```

where `owner_route = constitution-governance` and `enforcement_or_witness`
names the validator, review check, or typed residue (see `CAV2-D25`) that shows
how each structure rule is enforced or why it cannot yet be.

### Operational Interpretation

Use this term when deciding whether a piece of structural guidance is allowed to
constrain CyberAlchemy v2 artifacts. A constitution is the right home for rules
such as "every spec must carry sections X, Y, Z" or "imported vault concepts
must be re-authored before adoption". It is the wrong home for what a term means
(`CAV2-D33` definition), which option to take (`CAV2-D36` decision), how to
practice a recurring activity (`CAV2-D35` discipline), or how a runtime behaves
(`CAV2-D37` spec).

### Plain-Language Intuition

A constitution is the rulebook for the shape of things, not for what they mean
or what to do.

### Domain-Context Voice

In CyberAlchemy v2, constitutions live under
[../constitutions/](../constitutions/STABLE-REPOSITORY-CONSTITUTION.md) — for
example the stable repository constitution and the vault concept adoption
constitution — and the Arcanum constitution-governance capability is the
promotion route that admits, splits, composes, validates, or retires them. The
constitution artifact kind is modeled as an authority object in
[../../ontology/NODE-MODEL.md](../../ontology/NODE-MODEL.md); this file is the
canonical CAV2 meaning, while constitution-governance remains the owner of
specific constitutions.

### Boundary

A constitution is not a definition, decision, discipline, or spec, and it is not
enforceable merely because it is written. It binds structure only after
constitution-governance promotes it, and a structure rule that affects
validation or authority must carry an enforcement witness or typed residue per
`CAV2-D25` schema amendment witness.

### Primary Consumers

- [../../ontology/NODE-MODEL.md](../../ontology/NODE-MODEL.md)
- [../constitutions/STABLE-REPOSITORY-CONSTITUTION.md](../constitutions/STABLE-REPOSITORY-CONSTITUTION.md)
- [../README.md](../README.md)
- [../promotion-policy.md](../promotion-policy.md)

## CAV2-D35: Discipline

Status: active
Term: discipline
Aliases: governed discipline, discipline practice, recurring-practice artifact

### Normative Definition

A discipline is a governed authority artifact that names a recurring
cross-capability practice together with its trigger, the practice itself, the
evidence that justifies it, and a hardening route, without claiming the term,
structure, decision, or runtime authority owned by other surfaces. A discipline
says how the project should repeatedly act; it does not define vocabulary, fix
artifact shape, decide a contested choice, or implement runtime behavior.

In CyberAlchemy v2, a candidate habit, observed pattern, or research
recommendation is not a discipline until discipline-governance catalogs and
hardens it.

### Formal Interpretation

An admissible CyberAlchemy v2 discipline record has at least:

```text
Discipline =
  (id, name, trigger, practice, evidence, owner_route,
   hardening_route, source_or_provenance, residue)
```

where `owner_route = discipline-governance`.

### Operational Interpretation

Use this term when a repeated CyberAlchemy v2 activity needs an owned home so it
is practiced consistently — for example keeping the repository source-ledgered,
authority-bounded, and navigable. A discipline is not the home for shape rules
(`CAV2-D34` constitution), meanings (`CAV2-D33` definition), one-time choices
(`CAV2-D36` decision), or contracts (`CAV2-D37` spec).

### Plain-Language Intuition

A discipline is a named good habit with evidence and a plan to make it stick.

### Domain-Context Voice

In CyberAlchemy v2, disciplines live under
[../../disciplines/](../../disciplines/DISCIPLINES.md) — the catalog plus cards
such as stable repository stewardship (`CAV2-D6`) — and the Arcanum
discipline-governance capability is the owner route. The discipline artifact
kind is modeled as an authority object in
[../../ontology/NODE-MODEL.md](../../ontology/NODE-MODEL.md); this file is the
canonical CAV2 meaning, while discipline-governance formalizes, routes,
validates, promotes, or retires specific disciplines.

### Boundary

A discipline is not a constitution, definition, decision, or spec, and it is not
an active practice merely because it is written down. It becomes active only
after discipline-governance catalogs and hardens it, and it recommends hardening
routes rather than promoting other authority by itself.

### Primary Consumers

- [../../disciplines/DISCIPLINES.md](../../disciplines/DISCIPLINES.md)
- [../../disciplines/cards/stable-repository-stewardship.md](../../disciplines/cards/stable-repository-stewardship.md)
- [../../ontology/NODE-MODEL.md](../../ontology/NODE-MODEL.md)
- [../README.md](../README.md)

## CAV2-D36: Decision

Status: active
Term: decision
Aliases: governed decision, decision record, owner decision, resolved-choice artifact

### Normative Definition

A decision is a governed authority artifact that records the resolution of a
contested or consequential choice — scope, ownership, naming, public/private
posture, sequencing, or option selection — together with the options considered,
the chosen option, the rationale, the owner, and the resulting effect, without
absorbing the term, structure, discipline, or runtime authority owned by other
surfaces.

In CyberAlchemy v2, a discussion, recommendation, open question, or research
verdict is not a decision until decision-gate, or the responsible owner route,
records it as resolved.

### Formal Interpretation

An admissible CyberAlchemy v2 decision record has at least:

```text
Decision =
  (id, question, options_considered, chosen_option, rationale,
   owner_route, evidence, effect, status, residue)
```

where `owner_route` is decision-gate or the responsible owner, and `status` is
one of resolved, deferred, or superseded.

### Operational Interpretation

Use this term when CyberAlchemy v2 must resolve a blocker-level choice before
planning, implementation, or document mutation continues — for example whether
`inventory/` and `ontology/` stay visible top-level areas, or when standalone
extraction is allowed. A decision is not the home for meanings (`CAV2-D33`
definition), shape (`CAV2-D34` constitution), recurring practice (`CAV2-D35`
discipline), or contracts (`CAV2-D37` spec).

### Plain-Language Intuition

A decision is the written record of a choice the project actually made, and why.

### Domain-Context Voice

In CyberAlchemy v2, decision records are routed through the Arcanum decision-gate
capability and are intended to live under `authority/decisions/`. The decision
artifact kind is modeled as an authority object in
[../../ontology/NODE-MODEL.md](../../ontology/NODE-MODEL.md). It is distinct from
`CAV2-D5` promotion gate: a promotion gate is the owner route that returns pass,
flag, or block, while a decision is the recorded resolution. This file is the
canonical CAV2 meaning; decision-gate remains the owner that produces decisions.

### Boundary

A decision is not a promotion-gate result by itself, not a definition,
constitution, discipline, or spec, and not authority merely because someone
expressed a preference. It counts only when the responsible owner records the
resolution with options, rationale, and effect; an unresolved choice remains an
open question or blocker.

### Primary Consumers

- [../../ontology/NODE-MODEL.md](../../ontology/NODE-MODEL.md)
- [../promotion-policy.md](../promotion-policy.md)
- [../README.md](../README.md)
- [DEFINITION-TOWERS.md](DEFINITION-TOWERS.md)

## CAV2-D37: Spec

Status: active
Term: spec
Aliases: specification, governed spec, contract spec, promoted spec artifact

### Normative Definition

A spec is a governed authority artifact that fixes a product, domain, runtime,
validation, or artifact contract for CyberAlchemy v2 after a promotion route
admits it, stating the contract's scope, interface or shape, obligations, and
validation surface, without redefining the vocabulary, structure rules,
recurring practices, or owner decisions owned by other surfaces.

In CyberAlchemy v2, a draft, research finding, candidate contract, or
architecture sketch is not a spec until the spec owner or decision-gate promotes
it.

### Formal Interpretation

An admissible CyberAlchemy v2 spec record has at least:

```text
Spec =
  (id, scope, contract_kind, interface_or_shape, obligations,
   validation_surface, owner_route, source_or_provenance,
   promotion_state, residue)
```

where `contract_kind` is one of domain, runtime, validation, or artifact, and
`promotion_state` records candidate or promoted.

### Operational Interpretation

Use this term when CyberAlchemy v2 is ready to fix a contract that downstream
implementation or validation must honor — only after the relevant definition and
constitution owners and gate have passed. A spec is not the home for meanings
(`CAV2-D33` definition), shape rules (`CAV2-D34` constitution), recurring
practice (`CAV2-D35` discipline), or contested choices (`CAV2-D36` decision).

### Plain-Language Intuition

A spec is the promised contract for how something must behave or be shaped, once
the project has committed to it.

### Domain-Context Voice

In CyberAlchemy v2, specs live under [../../specs/](../../specs/README.md) and
are promoted only after owner gates pass; the DomainSpec spec template and the
Arcanum `contract` definition supply contract precedent. The spec artifact kind
is modeled as an authority object in
[../../ontology/NODE-MODEL.md](../../ontology/NODE-MODEL.md). This file is the
canonical CAV2 meaning for the spec artifact kind; it does not redefine
Arcanum-wide contract semantics.

### Boundary

A spec is not a runtime contract until promoted, not a definition, constitution,
discipline, or decision, and not authority by proximity to the `specs/` folder.
Arcanum-wide `contract` and `schema` semantics remain external authority unless
CyberAlchemy v2 promotes a narrower local spec, and a spec that changes a
governed shape must still carry a schema amendment witness per `CAV2-D25`.

### Primary Consumers

- [../../specs/README.md](../../specs/README.md)
- [../../ontology/NODE-MODEL.md](../../ontology/NODE-MODEL.md)
- [../promotion-policy.md](../promotion-policy.md)
- [../../../arcanum/definitions/DEFINITIONS.md](../../../arcanum/definitions/DEFINITIONS.md)

## Open Questions

### OQ-1. Which imported definitions should be promoted first?

Context: the top-anchor queue is now promoted as `CAV2-D9` through `CAV2-D15`.
The import manifest still contains 149 definition-like candidates, including
`AgenticSystem`, `ContextSolution`, and `TranslationResidue` source material.
`OperationalOntology` source material has been demoted into D19/D23 language.
Recommendation: classify and deduplicate the remaining import candidates before
promoting terms into this file. Status: OPEN.
