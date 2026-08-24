---
module: body-war-business-ontology-atlas-arrows
version: current
status: implementation-complete-candidate-local
updatedAt: 2026-07-30
docType: work-pack
---

# Work Pack — Body War Business Ontology Atlas Arrows

## Control Fields

| Field | Value |
| --- | --- |
| `workPackGateStatus` | `pass-candidate-local-implementation` |
| `complexity` | `medium` |
| `outputMode` | `split` |
| `executionPackRef` | `EXECUTION-PACK.md` |
| `layeringArtifactRef` | `IMPLEMENTATION-LAYERING.md` |
| `dispatchTechniqueTrace` | `DISPATCH-TRACE.md` |
| `distillValidationStatus` | `pass` |
| `swuAtomicityStatus` | `pass` |
| `firstUnitNarrownessStatus` | `pass` |
| `closeoutSyncStatus` | `pass` |
| `activeLayerWindow` | `complete` |
| `readinessProfile` | `candidate-local-prototype` |
| `selected_swu` | `none` |
| `first_selectable_swu` | `none` |
| `planEvidence` | `runtime-evidence-pass` |

`pass-plan-contract` means the bounded plan is selectable. It is not mutation
admission: Context Builder and Task Session must still bind current bytes,
detect drift, and admit exactly one selected unit.

## Objective And Boundary

Make direction visible at two compatible scales:

1. a bounded overview of 13 directed flow lanes among six ontology lenses; and
2. an exact source → predicate → target arrow in each of 231 canonical relation
   cards; and
3. a concise source-backed reference brief for every node, relation, lens, and
   predicate reference.

The work changes only the atlas projection, renderer, validators, generated
atlas, and new arrow evidence. It does not change ontology nodes, relations,
lifecycle policies, catalog ownership, sibling business views, or authority.

## Delivery Slices

| Slice | SWU | Layer | Outcome | Validation |
| --- | --- | --- | --- | --- |
| S-FLOW | `SWU-BWAA-001` | L0 | 13 deterministic directed flow groups account for 109 portals | projection tests and coverage validator |
| S-EXACT | `SWU-BWAA-002` | L1 | every canonical relation card visibly reads source → predicate → target | renderer tests |
| S-BRIEF | `SWU-BWAA-005` | L1 | source-backed node, relation, lens, and predicate briefs retain blockers and related incidence | renderer tests and source-parity fixtures |
| S-OVERVIEW | `SWU-BWAA-003` | L2 | six-node overview and 13 semantic lanes recompose with exact arrows | generator, projection/render/full ontology tests |
| S-EVIDENCE | `SWU-BWAA-004` | L3 | responsive/static arrows and reference briefs are receipt-backed | browser validator plus full regression |

## Task Board

| Task | SWU | Layer | Status |
| --- | --- | --- | --- |
| [TASK-BWAA-001](work-pack/tasks/TASK-BWAA-001.md) | `SWU-BWAA-001` | L0 | flag-complete; product acceptance passed, audit residue recorded |
| [TASK-BWAA-002](work-pack/tasks/TASK-BWAA-002.md) | `SWU-BWAA-002` | L1 | flag-complete; 231/231 staged arrows, generated-boundary residue delegated |
| [TASK-BWAA-005](work-pack/tasks/TASK-BWAA-005.md) | `SWU-BWAA-005` | L1 | complete |
| [TASK-BWAA-003](work-pack/tasks/TASK-BWAA-003.md) | `SWU-BWAA-003` | L2 | complete |
| [TASK-BWAA-004](work-pack/tasks/TASK-BWAA-004.md) | `SWU-BWAA-004` | L3 | complete |

## Ordered SWU Manifest

| Order | SWU | One primary behavior | Depends on | Layer | Task |
| --- | --- | --- | --- | --- | --- |
| 1 | `SWU-BWAA-001` | derive exact lens-flow aggregation | none | L0 | [task](work-pack/tasks/TASK-BWAA-001.md) |
| 2 | `SWU-BWAA-002` | render one exact relation-arrow component | 001 | L1 | [task](work-pack/tasks/TASK-BWAA-002.md) |
| 3 | `SWU-BWAA-005` | render source-backed reference briefs | 002 | L1 | [task](work-pack/tasks/TASK-BWAA-005.md) |
| 4 | `SWU-BWAA-003` | render and generate the whole-ontology overview | 005 | L2 | [task](work-pack/tasks/TASK-BWAA-003.md) |
| 5 | `SWU-BWAA-004` | execute responsive browser acceptance | 003 | L3 | [task](work-pack/tasks/TASK-BWAA-004.md) |

All five units are sequential. Units 002, 005, and 003 share the renderer and
its test; units 003 and 004 share the generated artifact/evidence boundary.

## Semantic Locks

| Owner | SHA-256 |
| --- | --- |
| nodes | `f74785ed18002fe0636519685711de8cd2f85e59f0eadb7de58d84faec399229` |
| relations | `234ad4152b731edcb03cd1b45dfa21570bd37df741090ca6ca0940fd98c0ce00` |
| lifecycle policies | `62e5a3e499f553d305d9c214f040d9430afbc35bccf7088a16da66cdaae12438` |
| atlas profile | `cba6f78a7306dea9fbd6d97fd3d5d228d501e81839c20248e901f3067ec0b739` |
| research residue | `796b56b8d7ad0e341646ac3df0970317e958509c0e6a2d712502d8e2ca65032f` |
| business view catalog | `2897b9490c27960104a0dcdcbda899e6752795ab1f737cf181e7bc3f075d3d60` |

Task Session preflight must recompute these locks and the current task write
scope. Drift blocks execution and returns to Invoke Refresh; it is not resolved
inside the selected SWU.

## Atomicity Review

| SWU | Independent boundary | Why it is not task-shaped |
| --- | --- | --- |
| 001 | pure data projection and its invariant checks | HTML is excluded; implementation and evidence are one deterministic behavior |
| 002 | reusable exact-arrow relation component | overview and generated output are excluded |
| 005 | reusable source-backed reference-brief component | overview integration and browser execution are excluded; source-parity and markup are one behavior |
| 003 | bounded overview integration and regeneration | browser evidence is excluded; exact-arrow component is a predecessor |
| 004 | browser/evidence execution | it does not repair projection, briefs, or renderer defects |

Result: five coherent SWUs, zero task-shaped units.

## Recomposition Proof

```text
109 canonical portals
  -> 13 directed lens flows (001)
  -> 231 exact relation arrows remain individually readable (002)
  -> 237 node + 231 relation + 6 lens + 23 predicate briefs (005)
  -> 6-lens overview + exact arrows + briefs in one generated atlas (003)
  -> responsive/static browser evidence (004)
```

The sequence satisfies the specification only when all five receipts exist.
No layer may substitute aggregate counts for exact relation identity or
projection wording for a definition.

## Execution Handoff

- Shared execution/closeout rules:
  [EXECUTION-CONTROL](work-pack/shared/EXECUTION-CONTROL.md).
- Layer waves: [W0](work-pack/waves/W0.md),
  [W1](work-pack/waves/W1.md), [W2](work-pack/waves/W2.md), and
  [W3](work-pack/waves/W3.md).
- Context Builder creates a strict pack only after the user explicitly selects
  one dependency-ready SWU.
- One Task Session owns one SWU and one terminal receipt.
- Invoke Refresh applies only the declared Work Pack/Continuation deltas.
- No successor is selected or executed automatically.

## Deferrals

- force-directed/general graph layout;
- relation editing or ontology-authority mutation;
- redesign of the curated `BUSINESS-VIEWS.html`;
- animation beyond a reduced-motion-safe presentation;
- human comprehension study or a claim that arrows improve comprehension;
- publication, deployment, release, or production.

## Blocker And Gap Ledger

There are no acceptance-critical Plan gaps. Runtime blockers are conditional:

| ID | Trigger | Owner | Repair route |
| --- | --- | --- | --- |
| `BWAA-DRIFT` | semantic/write-target digest differs at preflight | Invoke Refresh | refresh locks and revalidate the affected SWU |
| `BWAA-PREDECESSOR` | required predecessor receipt is absent or failed | current Task Session owner | finish or repair the predecessor |
| `BWAA-RUNTIME` | shared Playwright runtime is unavailable for 004 | Task Session/runtime owner | restore the pinned shared runtime; do not add a package root |
| `BWAA-SKILL-MIRROR` | generated `.agents/skills` capability mirror is missing or drifted at Task Session preflight | Arcanum lifecycle owner | restore or explicitly admit the generated mirror from canonical Arcanum sources before execution; do not repair it inside a Body War SWU |

Non-blocking deferred residue remains listed above.

## Gate Result

- Define: pass.
- Design selection: pass and fixed point.
- Design Distill: pass.
- Plan Distill: pass.
- Plan contract: pass.
- Runtime implementation evidence: pass, candidate-local.
- Selected SWU: none.
- Implementation authority: not granted.
- SWU-BWAA-001: product acceptance passed with 8/8 tests and an exact 13/109
  flow partition. Its terminal receipt is `flag` only because the existing
  target inventory was not referenced by the Context Builder/admission digest
  chain; the exact preimages were checked before mutation and the admitted
  post-images match.
- SWU-BWAA-002: isolated generation proves 231/231 exact relation arrows. Its
  receipt is `flag` because that SWU forbids generated HTML writes while the
  inherited renderer test requires current generated bytes. SWU-BWAA-005 owns
  the generated target and resolves that declared boundary tension.
- SWU-BWAA-005: pass. The generated atlas contains 231 exact relation arrows
  plus 237 node, 231 relation, six lens, and 23 predicate reference briefs.
  Nine blocked nodes with no recorded question preserve the explicit absence.
- SWU-BWAA-003: pass. The generated atlas contains six linked overview nodes,
  13 semantic lanes conserving all 109 portal relation IDs, all 231 exact
  arrows, and the 237/231/6/23 reference-brief denominator.
- SWU-BWAA-003 revalidation: pass. Real-browser observation exposed a closed
  native-details hover defect; the bounded progressive brief repair was
  regenerated and revalidated without changing ontology semantics.
- SWU-BWAA-004: pass. The pinned Playwright 1.59.1 / Chromium 1217 run passed
  43/43 assertions with zero console, page, request, or external-network
  failures, and captured both declared screenshots.
- Next route: none. The candidate-local prototype is complete. Publication,
  deployment, release, accessibility conformance, and human comprehension
  remain outside this Work Pack.
