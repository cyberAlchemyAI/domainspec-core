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

`Operational Ontology` remains a source-specific candidate branch term until a
later pass decides whether CyberAlchemy v2 needs it as a subtype, branch label,
alias, or separate term under this definition.

### Primary Consumers

- [DEFINITION-TOWERS.md](DEFINITION-TOWERS.md)
- [../../CRAFT.md](../../CRAFT.md)
- [../../../.arcanum/ontology-vault/map-2026-06-18-dispersed-knowledge.md](../../../.arcanum/ontology-vault/map-2026-06-18-dispersed-knowledge.md)

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

## Open Questions

### OQ-1. Which imported definitions should be promoted first?

Context: the top-anchor queue is now promoted as `CAV2-D9` through `CAV2-D15`.
The import manifest still contains 149 definition-like candidates, including
`AgenticSystem`, `OperationalOntology`, `ContextSolution`, and
`TranslationResidue` source material. Recommendation: classify and deduplicate
the remaining import candidates before promoting terms into this file. Status:
OPEN.
