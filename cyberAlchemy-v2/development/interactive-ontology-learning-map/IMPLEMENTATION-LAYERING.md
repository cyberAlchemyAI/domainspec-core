---
module: interactive-ontology-learning-map
version: 0.1.0-candidate
status: planned-blocked-on-upstream-graph
updatedAt: 2026-07-14
docType: implementation-layering
---

# Implementation Layering

## Target and boundary

- Target: private repository-local witness under `./prototype/`.
- Current state: accepted research plus define/design/plan artifacts; no implementation.
- Governing rule: later layers preserve source-local ownership, non-collapse laws, semantic byte stability, GET-only behavior, and spatial/non-spatial parity.
- External readiness boundary: L0 consumes an exact owner-generated DomainSpec `Sg` only after the live retired-reference guard and FPR-01/02/03/FPR-04 receipts pass. It does not implement, close, or reinterpret those upstream nodes.
- Production website integration and public packaging are outside the active layer window.

## Layer decisions

| Layer | Decision unlocked | Minimum working unit | Included | Deferred | Exit evidence | Promotion decision |
|---|---|---|---|---|---|---|
| L0 Contract witness | After this layer, we know whether the import/projection contract can consume the exact `Sg` handle and express the six planes, three derived views, and typed-negative witness without collapse. | approved owner route + exact `Sg` readiness handle + import-contract schema/fixture validator | owner decision, read-only `Sg` import contract, manifest contract, record/relation/view schemas, source and negative fixtures | compiler, API, UI | owner record; FPR readiness handle; schema pass/fail fixtures; source manifest coverage | continue, repair vocabulary, route upstream residue, or stop |
| L1 Deterministic read model | After this layer, we know whether owner-generated `Sg` plus selected documentary sources compile repeatably into a queryable immutable snapshot. | clean read-only import and build of both witnesses | `Sg` adapter, documentary adapters, validator kernel, semantic/learning/navigation builders, ELK layout, search, GET API | UI, pilot, website integration | unchanged imported-edge receipt; repeated-build bytes/hash/layout/index/ETag; endpoint residue; route inventory | continue, narrow sources, or stop |
| L2 Learning interface | After this layer, we know whether graph, hierarchy, and table provide equivalent usable journeys. | both journeys through all surfaces | React Flow neighborhood, hierarchy, table, detail/challenge views, non-drag controls | accounts, production website, alternate renderer | parity diff; keyboard/touch/reduced-motion/screen-reader receipts | pilot, repair, or stop |
| L3 Private pilot | After this layer, we know whether the bounded map improves correct distinctions for target learners and can be integrated privately. | named pilot on curated 50–150-node surface | comprehension protocol, performance traces, private integration decision | public derivative, accounts, scale renderer | raw pilot data, scored rubric, perf distributions, exact integration decision | integrate privately, iterate, or stop |

## Active layer window

The active window is pre-L0. G-OWNER has passed through the [bounded private-product owner decision](work-pack/shared/G-OWNER-DECISION.md). G-DSV2-SG remains blocked pending the exact upstream guard/FPR receipts and read-only `Sg` handle. No prototype implementation begins until that handle passes.

## Non-regression guardrails

- Semantic bytes never depend on learner, navigation, layout, or clock material.
- Rejected attempted relations never enter semantic export.
- DomainSpec relations are never reconstructed from feature tables or local fixtures; the owner-generated `Sg` is imported unchanged.
- No layer creates source-owner, promotion, runtime, comprehension, accessibility, or publication evidence by inference.
- Equivalent non-spatial access is not traded away for renderer scale.
- The public derivative stays absent from all four layers; it requires its own Invoke/owner/publication route.

## Recommended next move

Run the existing DomainSpec guard/FPR owner route to produce the exact FPR-01/02/03 and bounded FPR-04 graph/quotient/retraction receipts. After G-DSV2-SG passes, Task Session may execute `SWU-IOLM-001-A` using the persisted G-OWNER handle; otherwise stop without freezing the candidate schema or creating a local substitute graph.
