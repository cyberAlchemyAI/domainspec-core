---
module: interactive-ontology-learning-map
version: 0.1.0-candidate
status: candidate
updatedAt: 2026-07-17
docType: architecture-bundle
scope: private
---

# Interactive Ontology Learning Map — Architecture Bundle

> Refresh synchronization (2026-07-17): the map consumes the candidate
> `feature-with-independent-node-and-edge-files@1` BTE handoff as an independent
> read-only proof lane. It does not define the denominator, profile admission,
> FPR closure, or production state. `G-DSV2-SG` remains independently blocked.

## Design decision

Build a **read-only DomainSpec `Sg` importer, private projection compiler, and immutable read application**, divided into six ownership planes and three separately stored read views. The DomainSpec adapter verifies and preserves an owner-produced `Sg`; other source adapters preserve local namespaces. A candidate normalization boundary supports cross-source learning without redefining DomainSpec semantics, and validators prevent invalid type, evidence, authority, and view collapses. The first renderer is React Flow with build-time ELK coordinates, paired with first-class DOM hierarchy and relation-table surfaces.

## Why this shape

A single graph conflates documents, concepts, claims, decisions, work state, and pedagogy. A live canonical ontology would require unresolved morphism and authority laws. A renderer-only implementation would hide provenance and accessibility behind pixels. This architecture makes the smallest useful product while keeping every strong claim behind an independent receipt.

## System context

    DomainSpec owner route
      -> FPR-01/02/03 receipts
      -> bounded FPR-04 Sg + quotient/retraction receipt
      -> read-only DomainSpec Sg adapter

    other owned sources (read only)
      -> revision-pinned source manifest
      -> source-local documentary adapters

    verified imported/source-local material
      -> candidate projection normalization
      -> independent validators
      -> deterministic projection snapshot builder
           |- semantic.json + semanticHash
           |- learner.json
           |- navigation.json
           |- layouts.json
           |- search-index.json
           +- validation receipts
      -> immutable GET query layer
      -> journey + graph + hierarchy + tables

Source owners remain upstream authority. The compiler owns only its build receipt and projection bytes. The application owns presentation and local ephemeral learner state.

## Component contracts

| Component | Owns | Emits | Must not do |
|---|---|---|---|
| DomainSpec readiness verifier | exact FPR-01/02/03 and FPR-04 graph/quotient/retraction receipts | immutable `Sg` input handle or named block | set FPR state, accept an empty graph, or infer owner approval |
| DomainSpec `Sg` adapter | exact immutable `Sg` identity and profile | unchanged imported nodes/relations plus provenance | parse feature SPEC tables into replacement DomainSpec relations |
| Source manifest | allowlist, revisions, hashes, privacy class, extractors | deterministic private manifest | glob arbitrary repo content |
| Documentary source adapters | syntax-specific extraction outside DomainSpec graph authority | source-local records/anchors | normalize away local meaning or mint DomainSpec relations |
| Candidate normalizer | versioned cross-source projection/learning axes | candidate records | claim canonical vocabulary or alter imported `Sg` semantics |
| Validation kernel | non-collapse, source, endpoint, proof, view laws | independent receipts, residue | promote or adjudicate |
| Snapshot builder | stable sort, canonical bytes, identities, hashes | immutable JSON artifacts | include clock data in canonical bytes |
| Layout builder | deterministic view coordinates | layouts keyed by snapshot/policy | affect semantic hash |
| Read API | bounded immutable queries | GET responses + ETags | expose mutation verbs |
| Learning application | journey, graph, hierarchy, table, details | accessible interactions | infer authority from prominence |
| Evidence harness | repeat builds, parity, accessibility/performance runs | run receipts | turn one gate into another |

## Data partitions

### Identity and semantic material

Snapshot identity includes projection contract version, exact `Sg` identity/profile/receipt references, other source revisions/hashes, extractor version, and source-local identity material. `semanticHash` covers unchanged imported DomainSpec records/relations plus other admitted source-local semantic material, source references, independent epistemic/governance axes, unresolved references, and relevant validation posture. Here “canonical bytes” means deterministic bytes for this private projection; it does not grant DomainSpec or CAV2 authority.

### Learning material

Focus questions, propositions, explanations, completion checks, and challenges reference stable IDs but are stored outside semantic material.

### Navigation and layout material

Journey order, prerequisites, learn-next edges, breadcrumbs, filters, coordinates, and viewport hints are separately stored. Every navigation edge is non-semantic. Layouts are versioned by layout policy.

## Stable identity policy

- IDs are namespaced, human-debuggable, and deterministic.
- Imported DomainSpec node and relation IDs remain identical to their `Sg` identities.
- Source-local objects retain their namespace when normalized axes are added.
- Non-DomainSpec relation IDs derive from source namespace, endpoints, label, and source anchor; DomainSpec relation IDs are never recomputed locally.
- Attempted relations use a separate namespace and cannot satisfy a semantic-relation reference.
- Changing identity-bearing inputs changes snapshot identity.
- Changing learner copy or navigation alone does not change semantic identity.

## Validation architecture

| Validator | Positive fixture | Negative fixture | Receipt |
|---|---|---|---|
| DomainSpec readiness/import | exact two-node/one-edge `Sg` plus FPR/profile/quotient/retraction receipts | missing/empty input, profile mismatch, changed identity | bound input identity or named block |
| Schema/non-collapse | candidate record with independent axes | one fixture per forbidden merge | violation name + path |
| Source | allowed pinned anchors | missing/unallowed/changed anchor | manifest coverage |
| DomainSpec mapping/retraction | imported admitted edge | unapproved local label plus node/field/direction/edge/quotient mutants | unchanged import, explicit residue, independent comparison failure |
| Proof posture | domain-scoped formal claim | analogy cast as universal proof | claim/proof separation |
| View independence | semantic + learning views | mutate learner/nav only | semantic byte/hash equality |
| Determinism | two clean identical builds | changed identity input | bytes/hash/ETag/layout/index diff |
| API boundary | documented GET routes | mutation-route scan | route inventory |
| Information parity | spatial/hierarchy/table set | deliberately omitted row | parity diff |
| Accessibility | complete both journeys by tested mode | missing non-drag action | browser/AT evidence |
| Performance | curated 50–150-node fixture | measured budget breach | distributions and traces |

All executable receipts begin as `NOT_RUN`.

## Read API

The route family is defined in [queries.md](./queries.md). Responses include snapshot identity, ETag, stable IDs, and explicit truncation/pagination metadata. Neighborhood depth and relation facets are capped. Source-anchor queries resolve only through manifest entries. No endpoint accepts a filesystem path.

## UI architecture

One shared selection controller and typed read model feed four equal presentations:

1. focus-question overview and guided journey;
2. bounded spatial neighborhood;
3. authored semantic DOM hierarchy;
4. native table for relations, sources, claim posture, status, and authority effect.

Lens switches preserve selected stable ID and focus intent. The hierarchy/table never depend on geometry to carry meaning.

## Technology and scale

- Candidate renderer: React Flow major version 12.
- Candidate layout: ELK layered, precomputed under a versioned policy.
- Data: immutable JSON plus deterministic search index.
- Private witness root: `./prototype/`. Runtime framework is pinned by the first implementation task; the production website host remains unselected.
- Exact dependency versions: recheck and pin during the first implementation task.
- Candidate size: 50–150 curated nodes.
- Review triggers: more than 250 visible nodes, 500 visible edges, or 1,500 total nodes.

Crossing a trigger opens measured review; it does not authorize an automatic renderer change.

## Privacy and security

- Default-deny manifest; no crawling beyond explicit entries.
- Private paths, excerpts, JSON, indexes, source maps, logs, and receipts are private outputs.
- Query parameters cannot become filesystem paths or extractor selectors.
- Build logs are output channels subject to private-sentinel scans.
- L0 writes nothing into `arcanum/`.
- A future public Arcanum-only derivative is an independent build graph, not a feature flag.

## Degraded behavior

- Unresolved reference: retain explicit residue and fail its source gate.
- Missing, empty, mismatched, or unreceipted DomainSpec `Sg`: block before contract or projection mutation.
- Unsupported syntax: fail closed and name the manifest entry.
- Layout failure: hierarchy/table remain available, but spatial gate fails.
- Partial validation: display exact `NOT_RUN` or failed state.
- Missing learning content: semantic snapshot may remain valid without a journey.
- Missing UI host: immutable artifacts remain design evidence, not production evidence.

## Observability

Each build groups manifest ID, source revisions, extractor/schema/layout versions, snapshot/hash/ETag, record/relation/view counts, unresolved references, gate verdicts, duration, and artifact paths. Logs are evidence, not semantic nodes or owner decisions.

## Decision boundaries

| Decision | Owner status | Current effect |
|---|---|---|
| Approve combined schema/enums | unresolved | blocks contract freeze and implementation |
| Produce bounded DomainSpec `Sg` and prerequisite receipts | unresolved existing FPR owners | blocks DomainSpec import, contract freeze, and implementation |
| Select private L0 witness root | selected: `./prototype/` | permits bounded prototype work after schema owner gate |
| Select production website host | unresolved | blocks production integration only |
| Approve source-local meaning | existing source owners | adapters must preserve it |
| Maintain learner journeys | unresolved | only fixed fixtures are plan-ready |
| Approve public manifest | separate unresolved owner | outside L0 |

## Design risks

- Normalization may harden into de facto canon: retain source-local fields, candidate banners, versions, owner gate.
- A local parser may masquerade as DomainSpec authority: accept DomainSpec semantics only through exact `Sg` identity and receipts; route incompatible mappings as residue.
- Visual centrality may imply truth: explicit legends, focus framing, authority effect, labeled edges.
- Equivalent views may drift: one typed read model plus automated parity diff.
- ELK determinism may vary by version/platform: pin runtime and compare clean builds.
- Philosophy may overclaim formal support: typed claim ladder, proof-domain fields, challenges, no upward cast.

## Design gate

The architecture is complete enough to plan. G-OWNER passes through the bounded private-product [decision](work-pack/shared/G-OWNER-DECISION.md); mutation remains `BLOCKED` on G-DSV2-SG. G-HOST is satisfied for the repository-local private witness. Production website integration remains deferred. CAV2 hom-set/open-category questions are not prerequisites for this read-only candidate because it never calls application relations CAV2 morphisms.
