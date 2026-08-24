---
module: body-war-ontology-focus-scene-pivot
version: current
status: approved-for-design
updatedAt: 2026-07-30
docType: domainspec-spec
authority_effect: none
release_admission: not-granted
---

# DomainSpec: Body War Ontology Focus Scene And Portal Pivot

## Intent

Let a reader inspect one bounded, source-derived portion of the Body War
business ontology at a time, follow a relation that crosses that boundary, and
retain exact provenance and authority meaning across pointer, keyboard, and
reduced-motion operation.

The feature changes only the OEW presentation and interaction contract. It does
not change ontology nodes, relations, lifecycle state, promotion gates, or
authority.

## Actors

| ID | Actor | Goal | Constraint |
| --- | --- | --- | --- |
| `ACT-OFSP-READER` | Ontology reader, including keyboard and assistive-technology users | Locate a bounded scene, inspect exact relations, pivot to a connected scene, and recover the previous scene | Must not need color, pointer input, motion, or inferred ontology meaning |
| `ACT-OFSP-VALIDATOR` | Development validator | Prove deterministic projection and interaction parity from pinned source bytes | Structural acceptance cannot claim comprehension |

## Capability Registry

| Capability ID | Capability | Outcome |
| --- | --- | --- |
| `CAP-OFSP-01` | Derive bounded focus scene | A selected node resolves to one deterministic node/internal-relation/portal set |
| `CAP-OFSP-02` | Pivot through a portal | A crossing relation atomically selects the destination, replaces the scene, and records history |
| `CAP-OFSP-03` | Preserve selected relation | Source, target, direction, generic type, relation description, endpoint provenance, status, and authority remain visible and programmatically selected |
| `CAP-OFSP-04` | Operate without pointer or motion | Pointer, Enter, Space, and reduced-motion paths serialize the same semantic state |
| `CAP-OFSP-05` | Keep tour state atomic | Tour entry suspends the prior state, each step exclusively owns active state, and exit restores the suspended state |
| `CAP-OFSP-06` | Present source-consistent meaning | Search, graph/card, detail, relation, accessible name, and breadcrumb reuse admitted source literals with non-color cues |
| `CAP-OFSP-07` | Emit bounded acceptance evidence | Deterministic and browser checks bind source, overlay, runtime, and observed state without inflating authority |

## Concept Registry

All concepts below are UI/runtime concepts. They are not additions to the Body
War ontology.

| Concept ID | DS-D1 meta-type | Meaning |
| --- | --- | --- |
| `OFSP-C01` | Entity | `FocusScene`, a removable UI projection over admitted graph bytes |
| `OFSP-C02` | ValueObject | `SceneKey`, the deterministic identity of a tour or one-hop scene |
| `OFSP-C03` | Entity | `SceneNode`, an admitted presentation node rendered in the active scene |
| `OFSP-C04` | Relation | `InternalRelation`, an admitted edge whose endpoints are both in the scene |
| `OFSP-C05` | Relation | `Portal`, an admitted directed edge with exactly one endpoint in the scene |
| `OFSP-C06` | ValueObject | `RelationTuple`, exact source, target, direction, type, description, paths, statuses, and authority |
| `OFSP-C07` | Entity | `SelectedRelation`, persistent selection state for one exact relation tuple |
| `OFSP-C08` | Entity | `SceneSession`, active scene, selection, history, and optional suspended pre-tour state |
| `OFSP-C09` | ValueObject | `SceneBreadcrumb`, ordered, reversible scene transition history |
| `OFSP-C10` | ValueObject | `SuspendedSceneState`, the complete pre-tour state stored outside active tour state |
| `OFSP-C11` | ValueObject | `SourceLiteralSet`, business kind, candidate status if present, authority, file path, type, and description |
| `OFSP-C12` | Evidence | `ProjectionWitness`, test-owned expected nodes, internal relations, portals, and negative members |
| `OFSP-C13` | Evidence | `InteractionWitness`, canonical serialized semantic state for an activation path |
| `OFSP-C14` | Policy | `ProjectionBoundaryRule`, the deterministic tour/one-hop/portal classification rule |
| `OFSP-C15` | Policy | `ClaimCeiling`, the no-authority/no-comprehension/no-release boundary |

## Concept Relations

| Source | DS-D2 verb | Target | Meaning |
| --- | --- | --- | --- |
| `OFSP-C01` | contains | `OFSP-C03` | A focus scene renders admitted scene nodes |
| `OFSP-C01` | contains | `OFSP-C04` | A focus scene renders admitted internal relations |
| `OFSP-C01` | contains | `OFSP-C05` | A focus scene exposes boundary-crossing portals |
| `OFSP-C05` | references | `OFSP-C06` | A portal preserves its exact admitted relation tuple |
| `OFSP-C07` | references | `OFSP-C06` | Selected state preserves the same tuple |
| `OFSP-C08` | references | `OFSP-C01` | A scene session owns one active focus scene |
| `OFSP-C08` | contains | `OFSP-C09` | A session owns ordered reversible history |
| `OFSP-C08` | contains | `OFSP-C10` | Tour mode may own one suspended pre-tour state |
| `OFSP-C12` | validates | `OFSP-C14` | Test-owned source-derived arrays validate projection |
| `OFSP-C13` | validates | `OFSP-C08` | Serialized witnesses validate activation parity |
| `OFSP-C15` | constrains | `OFSP-C01` | Projection cannot imply ontology or authority meaning |

## Operations

### `OP-OFSP-01 deriveFocusScene`

Input: admitted presentation graph, selected presentation node ID, source digest.

Rules:

1. Reject an unknown selected node.
2. If the node occurs in exactly one tour, use that tour's ordered `nodeIds`.
3. If the node occurs in more than one tour, fail closed with
   `SCENE_AMBIGUOUS_TOUR_MEMBERSHIP`.
4. Otherwise select the node and every one-hop endpoint connected by an admitted
   edge.
5. Sort non-tour node IDs and all relation tuples by stable source identity.
6. Classify an edge as internal when both endpoints are members.
7. Classify an edge as a portal when exactly one endpoint is a member.
8. Exclude every edge with neither endpoint in the scene.
9. Preserve every source literal; never infer a branch, kind, lifecycle, or
   authority value.

Output: `FocusScene` with `sceneKey`, `nodeIds`, `internalRelations`, `portals`,
source digest, and `authority_effect:none`.

### `OP-OFSP-02 activatePortal`

Input: active `SceneSession`, exact portal ID, activation kind.

Rules:

1. Pointer, Enter, and Space resolve the same portal tuple.
2. Persist that exact tuple as `SelectedRelation`.
3. Append the source scene and selection to the breadcrumb.
4. Derive the destination scene from the portal's outside endpoint.
5. Atomically replace active scene and active node.
6. Move focus to the named destination detail landmark after commit.
7. If reduced motion is requested, perform the same state replacement without
   orientation animation.

Output: one canonical serialized semantic state independent of activation kind
or motion preference.

### `OP-OFSP-03 enterTour`

Store the current non-tour session as `SuspendedSceneState`, clear active
selection, derive the selected tour step scene, and announce its name, node
count, and portal count.

### `OP-OFSP-04 changeTourStep`

Replace the active tour scene and clear any active node or relation not admitted
to the new step. Stale state may exist only in explicitly labeled suspended
history.

### `OP-OFSP-05 exitTour`

Restore the complete suspended state and clear the suspension. If no suspension
exists, return to the deterministic initial overview state.

### `OP-OFSP-06 selectRelation`

Expose an exact `RelationTuple` and programmatic selected state without changing
the scene when both endpoints are internal. For a portal, delegate to
`OP-OFSP-02`.

### `OP-OFSP-07 focusSceneLandmark`

Move focus through an explicit skip/selection route to a named detail landmark.
The landmark's accessible text includes the exact node name and
`authority:none`; the first relation control is reachable within a test-pinned
Tab bound.

## Queries

| Query ID | Input | Output |
| --- | --- | --- |
| `Q-OFSP-01` | scene key | Ordered node IDs, internal tuples, portal tuples, counts |
| `Q-OFSP-02` | selected relation ID | Exact relation tuple and programmatic selected state |
| `Q-OFSP-03` | active session | Active scene, active node, selected relation, breadcrumb depth, suspended-state presence |
| `Q-OFSP-04` | presentation node ID | Source literal set without fabricated absent status |

## State Model

| State | Meaning | Allowed transitions |
| --- | --- | --- |
| `overview` | Existing unbounded entry surface before a focus action | `focus`, `enter-tour` |
| `focused` | One bounded tour or one-hop scene is active | `select-internal-relation`, `activate-portal`, `back`, `enter-tour`, `overview` |
| `pivoting` | Optional visual orientation is in progress; semantic state is already committed | `focused` |
| `tour` | One tour step exclusively owns active scene state | `change-step`, `activate-portal`, `exit-tour` |
| `degraded` | Source ambiguity, missing endpoint, invalid relation, or provenance failure prevents a truthful scene | `retry-source`, `overview` |

Forbidden transitions:

- no active out-of-scene selection survives `change-step`;
- no portal activation retains the old active scene;
- no tour exit invents a state when no suspended state exists;
- no presentation transition changes ontology status, release admission, or
  authority.

## Interface Contracts

### Projection core

Pure deterministic input/output boundary:

```text
deriveScene(graph, selectedNodeId) -> SceneProjection | SceneError
```

No DOM, layout engine, mutable store, browser API, or generated bundle access is
allowed inside the selector.

### UI store

One reducer/state-store boundary owns `SceneSession`. All pointer, keyboard,
tour, breadcrumb, and reduced-motion actions dispatch explicit events through
that boundary.

### Renderer

The renderer consumes only `SceneProjection` for scene nodes and edges. It does
not independently re-filter the full graph. Portal and relation rows are native
or semantically equivalent controls with accessible names and selected state.

### Adapter and provenance

The existing Body War adapter remains the source of admitted presentation data.
The UI may preserve or project fields but may not rewrite adapter authority,
status, source paths, generic relation type, or relation-local description.

## Error Contract

| Code | Trigger | User-visible behavior | Evidence behavior |
| --- | --- | --- | --- |
| `SCENE_UNKNOWN_NODE` | selected ID absent | Keep current truthful scene; explain unavailable target | negative selector witness |
| `SCENE_AMBIGUOUS_TOUR_MEMBERSHIP` | node appears in multiple tours | fail closed; do not choose a tour by order | deterministic negative fixture |
| `SCENE_MISSING_ENDPOINT` | admitted edge references absent node | degraded scene; identify relation without rendering fabricated endpoint | adapter/projection negative witness |
| `SCENE_PROVENANCE_MISSING` | required tuple path/authority field missing | withhold pivot and show bounded data error | provenance negative witness |
| `SCENE_STALE_SOURCE` | source digest differs from fixture/receipt | reject acceptance receipt | digest mismatch witness |

## Acceptance Contracts

| ID | Contract |
| --- | --- |
| `AC-OFSP-001` | The current `237` node / `231` edge tour baseline is reproduced as a failing precondition, then the named four-node tour scene matches independently test-owned node, internal-edge, and portal arrays and excludes one fixed unrelated node. |
| `AC-OFSP-002` | The non-tour fixture resolves to the selected node plus a deterministically sorted one-hop neighborhood with exact portal classification. |
| `AC-OFSP-003` | `Identity and Consent —related to→ Authentication and Consent` preserves exact type, description, direction, endpoint paths, statuses, and `authority:none`; portal activation atomically replaces the scene and opens the destination. |
| `AC-OFSP-004` | Pointer, Enter, Space, and reduced-motion activation produce byte-equivalent canonical semantic state. |
| `AC-OFSP-005` | Tour pre-entry, entered, step-two, and exited state objects prove suspend/reset/restore behavior and reject stale active `Authentication and Consent` after a step change. |
| `AC-OFSP-006` | Exact node kind, optional candidate status, `authority:none`, and source path agree across search, graph/card, detail, accessible name, breadcrumb, and pivot destination; missing status is never fabricated. |
| `AC-OFSP-007` | Focus reaches the named detail landmark and each pivot-capable control has visible non-color focus geometry under default, grayscale, forced-colors, and reduced-motion modes. No contrast or comprehension claim is inferred. |
| `AC-OFSP-008` | Acceptance receipts bind the exact presentation graph digest, overlay inputs, Node/Playwright/Chromium runtime, canonical state bytes, teardown, and `authority_effect:none`. |

## Non-Goals

- Changing the Body War ontology, adapter vocabulary, lifecycle, or promotion
  status.
- Treating tours, one-hop neighborhoods, layout, colors, or motion as semantic
  ontology branches.
- Editing generated dashboards or generated adapter run bytes directly.
- Adding a package root or dependency solely for Playwright.
- Claiming human comprehension, workload, contrast compliance, release,
  deployment, production readiness, or upstream acceptance.
- Publishing the OEW overlay to Understand Anything upstream.

## Dispatch Technique Trace

| Technique | Define use |
| --- | --- |
| `sequence` | Review findings precede specification; specification precedes design and plan |
| `boundary_first` | Candidate-local authority, overlay ownership, generated-evidence boundary, and claim ceiling are fixed before capabilities |
| `tension_map` | Bounded navigation is preserved alongside the unproved human-comprehension ceiling |
| `evidence_binding` | Every acceptance contract names deterministic or browser evidence without treating planned witnesses as executed |

## Define Gate

- Discovery input: pass
- Target and ownership boundary: pass
- Concepts and capabilities: pass
- Acceptance contracts: pass
- Authority ceiling: pass
- Open blocker preventing Design: none
- Result: `pass`

