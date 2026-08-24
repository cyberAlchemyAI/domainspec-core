# Game-Like Canvas Interface Research Findings

## Decision

For the finite L0 prototype contract, keep the existing semantic DOM as the evidence and control plane and add one dependency-free native SVG `WorldRenderer` as a disposable spatial projection. Do not select a game engine and do not treat the renderer as a source of evidence, workflow, worker execution, or authority.

This is a research architecture recommendation, not implementation approval. The admitted evidence closes a bounded prototype contract; it does not prove accessibility conformance, usability or human benefit, publication, release, deployment, production readiness, promotion, or authority.

## Why this is the smallest defensible slice

The current interface already owns the meaningful state transitions and the textual, focusable controls. The world layer can therefore remain narrow: it renders a room, accepts bounded navigation input, and requests an existing semantic transition through a one-to-one hotspot binding. Only the semantic owner may commit evidence selection, focus, refusals, workflow state, or any authority-relevant change.

The native SVG choice is build-from-owned precedent rather than a novelty claim. It avoids a runtime dependency and keeps room geometry and hit targets inspectable for the first slice. Canvas remains a later alternative requiring a separate accessibility, inspection, focus, hit-testing, and fallback contract.

## Selected contract

- `WorldManifest` is versioned, non-authoritative projection configuration: known IDs, bounded geometry, admitted local assets, deterministic presentation data, and mappings to semantic controls. It contains no evidence payload.
- `WorldProjectionState` owns only disposable presentation state such as renderer lifecycle, camera, decorative-avatar pose, hover, visibility, reduced motion, and failure.
- `SemanticInspectionState` is a read-only projection of the semantic control plane's committed floor, room, focus, verification, refusal, and evidence-selection state.
- `WorldIntent` is a validated navigation request with `authority_effect: none`.
- `SemanticTransition` is owned and committed by the existing semantic control plane. It alone can change semantic selection.
- `DecorativeAvatar` is deterministic presentation, not `WorkerExecution`; it has no task, prompt, tool, transport, receipt, worker identity, or authority.
- `HotspotBinding` is a total one-to-one mapping from a known SVG hotspot to a named, focusable semantic control. Unknown, missing, or duplicate bindings fail admission.
- `WorldRenderer` renders projection state and mirrors committed semantic state. It cannot create or mutate evidence or authority.

## Required witnesses

The prototype is meaningful only if its checks distinguish the proposed behavior from a static illustration or a DOM proxy.

1. **Movement:** From an exact spawn, a fixed input trace produces observable displacement to a different final coordinate. Replaying the trace is byte-identical, bounds clamp, and walls are not crossed.
2. **Geometry hit testing:** Positive inside-hit and negative outside, occluded, and unknown-hotspot cases prove that SVG geometry—not a synthetic DOM shortcut—controls world hit detection.
3. **Semantic parity:** Pointer and keyboard activation resolve the same known binding and request the same existing semantic transition. Camera changes have no evidence-selection effect.
4. **Failure and rollback:** Capture the exact pre-failure semantic-state snapshot. Renderer or bridge failure disables projection state, announces the fallback, leaves textual controls usable, and preserves the semantic snapshot byte-for-byte.
5. **Reduced motion:** Continuing decorative movement stops or is replaced while direct navigation and semantic controls remain available.
6. **Request ceiling:** No external or non-GET request is introduced. Unknown identifiers fail closed.
7. **Performance:** Frame, input, long-task, and idle budgets must declare instrumentation, sample counts, and complete pass/fail partitions with no unclassified gray zone.

Automated browser evidence can establish those finite mechanics. It cannot establish screen-reader quality, zoom/reflow fitness, high-contrast usability, motion comfort, wayfinding, comprehension, place-memory, trust, motivation, productivity, learning, or research quality; those remain human and assistive-technology validation residue.

## Engine comparison and adoption boundary

- **Phaser:** fallback only. Its current package identity is v4.2.1, but v3.90 API documentation must not be presented as version-coherent v4 capability proof.
- **PixiJS:** deferred. The reviewed current version is 8.19.0, correcting the earlier 8.18.1 reference.
- **Excalibur:** deferred. Explorer-reported license information is not sufficient adoption evidence until the canonical tagged license is independently bound.
- **Three.js / 3D:** killed for L0 because no evidenced 3D obligation justifies the added renderer, asset, camera, and accessibility surface.
- **Canvas:** deferred as an alternative renderer contract; it is not interchangeable with SVG for accessibility and inspection purposes.

Any later engine adoption requires a pinned package artifact and hash, exact license evidence, version-coherent documentation or tagged source for required APIs, module and bundling proof, bundle-size measurement, CSP compatibility, and offline validation. None of those gates is satisfied merely by this research recommendation.

## Explicit exclusions

L0 excludes an evidence-bearing renderer, decorative avatars represented as autonomous workers, CDN or runtime-generated remote assets, 3D, physics, pathfinding, minimap, persistence, multi-scene lifecycle, and worker execution. A separate `WorldScene` abstraction is premature until a second scene proves that lifecycle necessary.

## Residue and next gate

The evidence-closure record marks the writer admission ready and binds the architecture, ownership, state-separation, non-vacuity, rollback, performance, and accessibility-boundary claims. Its admitted revised synthesis and final reviewer receipts were not reinterpreted here beyond those bound rows.

The next legitimate step is a separately authorized, candidate-local L0 implementation plan or spike that pins exact files, tests, browser instrumentation, and rollback behavior. It must preserve the semantic DOM authority boundary and must not install an engine dependency without crossing the later-adoption gates above.

## Evidence basis

- `research.md`: explorer returns covering runtime precedent, human-interface constraints, and current integration boundaries.
- `receipts/reviewer-precedent.json`: ownership classification and dependency/version/license corrections.
- `receipts/reviewer-nonvacuity.json`: movement, geometry, rollback, and performance witness defects that the admitted closure records as repaired.
- `receipts/reviewer-definitional.json`: vocabulary, state separation, semantic ownership, and counterexample defects that the admitted closure records as repaired.
- `receipts/evidence-closure.json`: exact writer admission, bound claim rows, killed options, deferred residue, and claim ceiling.
