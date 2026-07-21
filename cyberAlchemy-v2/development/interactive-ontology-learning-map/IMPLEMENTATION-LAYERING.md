---
module: interactive-ontology-learning-map
version: 0.1.0-candidate
status: candidate-compile-blocked
updatedAt: 2026-07-20
docType: implementation-layering
---

# Implementation Layering

## Applied consumer boundary

The BTE handoff is an input contract, not a second semantic source. Layer work
must preserve imported node/edge identity and source provenance, bind every view
to the semantic hash, and reject learner/navigation mutations that alter semantic
bytes. Candidate posture remains distinct from authoritative `Sg` readiness.

## Target and boundary

- Target: private repository-local witness under `./prototype/`.
- Current state: accepted research and planning plus the passing L0C candidate-contract/provenance guard; no candidate graph, parity views, or product UI yet.
- Governing rule: later layers preserve source-local ownership, non-collapse laws, semantic byte stability, GET-only behavior, and spatial/non-spatial parity.
- Candidate readiness boundary: L0C consumes the minted-project runtime only with explicit candidate posture, source/build receipts, stable identities, and an authority non-collapse guard.
- External authority boundary: L0A consumes an exact owner-generated DomainSpec `Sg` only after the FPR-01/02/03/FPR-04 receipts pass. It does not implement, close, or reinterpret those upstream nodes.
- Production website integration and public packaging are outside the active layer window.

## Layer decisions

| Layer | Decision unlocked | Minimum working unit | Included | Deferred | Exit evidence | Promotion decision |
|---|---|---|---|---|---|---|
| L0C Candidate substrate | After this layer, we know whether one candidate source contract and projection pipeline can preserve posture, stable identity, provenance, and graph/hierarchy/table parity without claiming authority. | candidate contract/provenance guard, then minimal minted project and parity proof | project/feature metadata, node/connection files, source/build receipts, normalized read model, candidate badge/field, parity fixture | full corpus, production UI, authoritative DomainSpec labels | contract negatives; deterministic compile; parity diff; proof candidate receipts cannot satisfy G-DSV2-SG | continue candidate learning work, repair contract, or stop |
| L0D Evidence consumer | After this layer, we know whether the private application can consume an exact executable DomainSpec proof without semantic, identity, provenance, view, or authority collapse. | narrow EVF consumer run; later independent BTE breadth rerun | versioned YAML contract, JSON receipt schema, exact upstream handles, deterministic IOLM rebuild, parity and negative replay | predicate/obligation authorship, BTE execution, authority rebind, UI/pilot | fresh `SWU-IOLM-DSC-A` receipt; later distinct `SWU-IOLM-DSC-B` receipt | accept the bounded combined claim, repair the consumer, or preserve only the upstream result |
| L0A Authority rebind | After this layer, we know whether the same normalized boundary can consume the exact owner-issued `Sg` without semantic or identity drift. | exact `Sg` readiness handle + equivalence or migration proof | read-only `Sg` adapter, receipt binding, stable-ID equivalence/migration map | FPR ownership or lifecycle mutation | FPR readiness handle; unchanged import; independent retraction; rebind diff | admit authoritative input to the private projection, repair migration, or stop |
| L1 Deterministic read model | After this layer, we know whether owner-generated `Sg` plus selected documentary sources compile repeatably into a queryable immutable snapshot. | clean read-only import and build of both witnesses | `Sg` adapter, documentary adapters, validator kernel, semantic/learning/navigation builders, ELK layout, search, GET API | UI, pilot, website integration | unchanged imported-edge receipt; repeated-build bytes/hash/layout/index/ETag; endpoint residue; route inventory | continue, narrow sources, or stop |
| L2 Learning interface | After this layer, we know whether graph, hierarchy, and table provide equivalent usable journeys. | both journeys through all surfaces | React Flow neighborhood, hierarchy, table, detail/challenge views, non-drag controls | accounts, production website, alternate renderer | parity diff; keyboard/touch/reduced-motion/screen-reader receipts | pilot, repair, or stop |
| L3 Private pilot | After this layer, we know whether the bounded map improves correct distinctions for target learners and can be integrated privately. | named pilot on curated 50–150-node surface | comprehension protocol, performance traces, private integration decision | public derivative, accounts, scale renderer | raw pilot data, scored rubric, perf distributions, exact integration decision | integrate privately, iterate, or stop |

## Active layer window

The active window is L0C. G-OWNER, G-POSTURE, and `SWU-IOLM-00C-A` pass. 00C-B is selected but blocked before mutation: its required cross-feature edge is intentionally unsupported by the live compiler and no upstream support receipt exists. 00C-C remains unselected. L0D is planned but both consumer SWUs are unselected; it cannot begin before the candidate substrate and the applicable upstream core receipt exist. G-DSV2-SG remains blocked pending exact upstream receipts, but it applies only to L0A authoritative labeling/rebind.

## Non-regression guardrails

- Semantic bytes never depend on learner, navigation, layout, or clock material.
- Rejected attempted relations never enter semantic export.
- Candidate relations remain visibly candidate and never become DomainSpec relations by naming or projection; owner-generated `Sg` relations are imported unchanged only in L0A.
- Candidate and authoritative sources feed one normalized graph boundary; no second UI/read-model pipeline is allowed.
- Executable evidence enters through the versioned private consumer contract; IOLM receipts never become upstream semantic, obligation, profile, or release authority.
- No layer creates source-owner, promotion, runtime, comprehension, accessibility, or publication evidence by inference.
- Equivalent non-spatial access is not traded away for renderer scale.
- The public derivative stays absent from all four layers; it requires its own Invoke/owner/publication route.

## Recommended next move

Option 1 is recorded in `DEC-CAV2-IOLM-00C-B-CROSS-FEATURE-001`; the BTE planning contradiction has since been refreshed and independently accepted. Continue its admitted predecessor chain only through an explicitly authorized bounded Task Session. Do not create candidate graph sources or select 00C-C until a passing upstream cross-feature-support receipt exists. `DEC-GCP-002` adds the unselected L0D sibling consumer lane after the candidate substrate; the independent G-DSV2-SG owner route remains relevant only to L0A authoritative rebind.
