---
module: interactive-ontology-learning-map
version: 0.1.0-candidate
status: candidate
updatedAt: 2026-07-17
docType: domainspec-spec
scope: private
ownerRoute: private-learning-map-product-owner
---

# Interactive Ontology Learning Map — SPEC

## Purpose

Define a private learning application that projects independently owned knowledge into an inspectable mental map. It teaches how source artifacts, semantic concepts, claims, evidence, governance, Craft workflow state, and learner navigation connect while keeping their types and authority effects distinct.

## Product proposition

A learner starts from a focus question, explores a bounded spatial neighborhood, switches to an equivalent hierarchy or relation table, opens exact sources and challenges, and follows an authored journey. All surfaces share stable identities; none may silently alter semantic meaning or owner authority.

## Success contract

The L0 witness succeeds only when it can:

1. verify exact owner receipts for `FPR-01`, `FPR-02`, `FPR-03`, and the bounded `FPR-04` `Sg`, quotient, and independent retraction;
2. import that `Sg` read-only and deterministically project it with a revision-pinned non-DomainSpec source manifest into immutable candidate JSON;
3. preserve six internal classification planes without claiming they are canonical CAV2 kinds or replacement DomainSpec graph types;
4. emit separately serialized `semanticView`, `learnerView`, and `navigationView` over stable IDs;
5. prove learner/navigation removal leaves deterministic semantic bytes unchanged;
6. preserve the owner-admitted DomainSpec relation and retain incompatible or rejected local mappings only as attempted-relation residue;
7. teach the Craft operational-to-speculative claim ladder with explicit posture;
8. expose the same records, relations, sources, statuses, challenges, and actions through spatial and non-spatial surfaces;
9. serve only GET operations and infer no promotion, owner decision, FPR closure, engine acceptance, runtime proof, comprehension, accessibility conformance, or publication verdict.

## Scope

### Included in the private L0 witness

- An explicit private source allowlist and revision-pinned manifest.
- An exact read-only handle to the owner-generated bounded `FPR-04` `Sg` and its prerequisite receipts.
- Candidate record/relation/view schemas and non-collapse validators.
- Deterministic non-DomainSpec source extraction, `Sg` import validation, and immutable projection generation.
- Agent Execution Orchestrator typed-negative witness.
- Financial Settlement positive learner fixture.
- One complete Craft intention-to-residue journey across five claim classes.
- GET-only query surface.
- React Flow spatial view with precomputed ELK coordinates.
- First-class DOM hierarchy and native relation table.
- Source, claim/proof, authority, and challenge details.
- Determinism, parity, accessibility, and bounded-performance evidence.

### Excluded

- Source editing; ontology authoring; authority mutation; promotion or demotion.
- Reconstructing DomainSpec semantic nodes or admitted relations from feature SPEC tables, local parser labels, or learner material.
- Changing the retired-reference guard, FPR status, supported profile, precedence, quotient, retraction, or engine acceptance.
- Challenge adjudication or owner decisions.
- A live canonical CAV2 ontology or new CAV2 canonical kinds.
- Treating Craft ledger relations as categorical morphisms by default.
- Runtime correctness claims for source-described systems.
- Account-backed progress, collaboration, comments, or analytics.
- Canvas/WebGL renderer switching.
- Public release or a redacted private build.

### Deferred behind separate gates

- Production website integration after an exact website host and owner are selected.
- Maintained learner content after an editorial owner is named.
- Account persistence after privacy/data-governance design.
- Scale renderer review after measured triggers.
- Separately built Arcanum-only public candidate after projection and publication owners exist.

## Core domain model

### Internal planes

| Plane | Responsibility | Authority effect |
|---|---|---|
| L0 Source | Revision-pinned artifacts and exact anchors | none |
| L1 Semantic | Owner-imported DomainSpec `Sg` plus other source-local concepts, definitions, and admissible typed relations | source-local only |
| L2 Epistemic | Claims, evidence, proof scope, analogy, interpretation, unknowns | none unless separately decided |
| L3 Governance | Owners, gates, decisions, envelopes, promotion records | displayed, never inferred |
| L4 Operational | Craft contexts, artifacts, conditions, residue, gates, recomposition | continuation only |
| L5 Projection | Focus questions, journeys, layouts, annotations, view policy | none |

### Derived views

| View | Contents | Forbidden behavior |
|---|---|---|
| `semanticView` | Owner-imported DomainSpec `Sg` records/relations plus other source-backed semantic material | importing learner sequence or locally reconstructed DomainSpec relations as semantics |
| `learnerView` | Focus questions and labeled propositions | changing `semanticHash` |
| `navigationView` | prerequisites, learn-next, breadcrumbs, journey order | implying endorsement or promotion |

## Candidate record contract

Every record has a stable ID, source references, namespaced source-local kind/status, candidate normalized axes where useful, owner route, authority effect, and explicit forbidden collapses. `proofStatus` is nullable and domain-scoped. No generic `evidenceStatus` field is allowed. `generatedAt` is excluded from canonical bytes.

### DomainSpec graph consumer boundary

Imported DomainSpec records and relations retain their `Sg` identity, profile,
source-manifest, and authority provenance. Projection schemas may wrap them for
query and learning views, but cannot redefine their node kind, endpoints,
relationship label, direction, or admission posture.

The exact normalized enums remain candidate until a projection-schema owner and the relevant source definition owners approve them. See [GLOSSARY.md](./GLOSSARY.md).

## Non-collapse invariants

The fourteen laws in the [accepted findings](../research/2026-07-14-interactive-ontology-learning-map/findings.md#core-non-collapse-laws) are normative for this candidate package. The minimum implementation fixtures MUST demonstrate:

- artifact instance is not semantic concept;
- source anchor is not evidence record or source authority;
- canonical kind, concept role, authority kind, authority state, and workflow status remain distinct;
- verification, proof, authority, evidence confidence, and commitment confidence remain independent;
- learner edge is not semantic relation;
- projection is not promotion or publication;
- renderer success is not comprehension or accessibility conformance.

## Witnesses

### W-01 Agent Execution Orchestrator

- Traverse the owner-produced two-node/one-admitted-edge `FPR-04` `Sg`; do not rebuild its relation from the AEO feature table.
- Fail when required input is missing or empty instead of returning an empty-success graph (`EGI-008`).
- Retain an incompatible or unapproved local edge mapping as `AttemptedRelation` plus operational residue (`EGI-010`).
- Require mutated node, field, edge direction, edge, and quotient fixtures to fail the independent `Sg -> G -> Sg_canonical` comparison (`EGI-011`).
- Never export attempted mappings into `semanticView`, relabel them as CAV2 morphisms, or mint replacement FPR/gap identities.
- Keep schema/endpoint documentary posture separate from executable endpoint and runtime evidence, both initially `NOT_RUN`.

### W-02 Financial Settlement

- Teach `NoDuplicateMakeupRule --enforces--> GenerateSettlement --produces-for--> SettlementTransaction`.
- Show exact document anchors and separate them from runtime/business conformance.

### W-03 Craft claim ladder

Teach five separately typed positions: operational method, domain-scoped formal correspondence, structural analogy, philosophy of making, and universal/reality horizon. The UI MUST NOT imply an upward proof relation between them.

## Independent gates

| Gate | Requirement | Define status |
|---|---|---|
| G-OWNER | Combined projection owner and vocabulary approval route selected | `PASS` — [decision](work-pack/shared/G-OWNER-DECISION.md) |
| G-DSV2-SG | Exact FPR-01/02/03 owner receipts plus schema-valid bounded FPR-04 `Sg`, explicit `Sg -> G`, and independent retraction receipt | `BLOCKED` |
| G-HOST | Private L0 witness root selected | `PASS` — `./prototype/` |
| G-SOURCE | All emitted records resolve to allowed revision-pinned anchors | `NOT_RUN` |
| G-SEMANTIC | Kinds/relations are source-local or explicitly candidate | `NOT_RUN` |
| G-ENDPOINT | Both relation endpoints are admissible | `NOT_RUN` |
| G-PROOF | Claim, proof, verification, assumptions, and counterevidence separated | `NOT_RUN` |
| G-DETERMINISM | Repeated builds agree on canonical bytes, layout, indexes, hashes, ETags | `NOT_RUN` |
| G-A11Y | Equivalent journeys work with keyboard, touch, reduced motion, and tested screen readers | `NOT_RUN` |
| G-PERF | Measured curated witness stays inside accepted budgets | `NOT_RUN` |
| G-PUBLICATION | Separate allowed public build and exact-manifest verdict | out of L0; `NOT_RUN` |

Passing one gate never closes another.

## Acceptance criteria

- AC-01: A schema validator rejects every fixture that violates a named non-collapse law.
- AC-02: Two identical builds produce byte-identical semantic output, stable coordinates/search index, equal hashes, and equal ETags.
- AC-03: Modifying only learner or navigation content leaves semantic bytes and `semanticHash` unchanged.
- AC-04: W-01 exports exactly the admitted relation and retains the rejected attempt only in residue/challenge material.
- AC-05: W-02 is navigable from concept registry through source anchors without a runtime-conformance claim.
- AC-06: W-03 labels each claim class and exposes its evidence/proof posture and challenge route.
- AC-07: Spatial graph, hierarchy, and table expose equivalent record/relation information and preserve selected stable ID across lenses.
- AC-08: All spatial interactions have non-drag alternatives; color is not the only state signal.
- AC-09: API surface is GET-only; mutation verbs and authority actions are absent.
- AC-10: L0 outputs remain inside the approved private host; no file is written under public `arcanum/`.
- AC-11: The DomainSpec input binds exact FPR/profile/source/graph identities, rejects missing or empty input, preserves imported relations unchanged, retains unapproved mappings as residue, and fails all named retraction mutants.

## Authority and lifecycle

- Source meaning: source-local owners.
- Candidate projection contract: `private-learning-map-product-owner`; projection fields/enums only, with authority-relevant handback to definitions governance and affected source owners.
- Learner content: `UNRESOLVED`.
- Implementation/evidence: bounded to `./prototype/` only after both G-OWNER and G-DSV2-SG pass; production website integration remains a separate host decision.
- Public derivative and publication: outside L0 and separately owned.
- Next authoring route: none selected; the applied refresh supersedes the historical define/design mutation route without rewriting those receipts.
- Next mutation route: deferred while G-DSV2-SG is open; after it passes, Task Session may execute one selected SWU using the persisted G-OWNER handle.

## FPR-02B consumer-proof handoff

The accepted FPR-02B profile decision makes this map an independent, read-only
consumer proof surface. The input handle must carry:

- `feature-with-independent-node-and-edge-files@1` candidate or authoritative
  posture;
- source, profile, registry, schema, graph, generated-root, `O_spec`, `O_gen`,
  `T_gen`, `E_run`, and receipt identities/digests;
- unchanged imported node/edge IDs and source provenance;
- semantic, learner, navigation, layout, index, and ETag hashes; and
- negative results for missing, empty, mismatched, unapproved, stale, unknown-ID,
  and semantic-mutating overlays.

IOLM may verify and project those handles but cannot define `O_spec`, admit the
successor profile, close FPR-02B, change Craft continuation, or authorize
production. `G-DSV2-SG` remains `BLOCKED` until the IOLM-owned exact receipt and
bounded `Sg` requirements pass; this refresh does not close that gate.
