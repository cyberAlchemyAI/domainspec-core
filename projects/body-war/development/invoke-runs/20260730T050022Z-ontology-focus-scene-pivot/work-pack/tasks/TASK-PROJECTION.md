# TASK-PROJECTION — Source Literals And Scene Derivation

## Objective

Implement a pure, deterministic projection independent of native UI state and
layout.

Layer: L0 then L1. Dependency: TASK-FOUNDATION.

## SWU-OFSP-005 — Join exact relation and node literals

- Primary behavior: convert an admitted edge and its endpoints into one total
  exact `RelationTuple` and reusable node `SourceLiteralSet`.
- Acceptance: exact source/target/direction/type/description/path/kind/optional
  status/authority match the independent fixture; missing required provenance
  fails and absent candidate status stays absent.
- Split analysis: node literal extraction and tuple joining share one
  source-consistency invariant; rendering and scene classification are
  independent later units.
- Dependencies: 001, 004.
- Source anchors: `SPEC.md#adapter-and-provenance`,
  `ARCHITECTURE.md#data-contracts`.
- Write scope:
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/types.ts`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/sourceLiterals.ts`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/sourceLiterals.test.ts`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/FOCUS-SCENE-OVERLAY.lock.json`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/focus-scene-overlay-manifest.json`
- Done: exact literal tests pass and no adapter mutation is needed.
- Validation: successor overlay validation plus materialized dashboard test for
  `sourceLiterals.test.ts`.
- Owner: `local-fallback` through Task Session.

## SWU-OFSP-006 — Project the named four-node tour scene

- Primary behavior: derive exact tour members, internal relations, and directed
  portals for a node in one source-declared tour.
- Acceptance: independently expected arrays match; fixed unrelated node absent;
  ambiguous membership fails; output stays byte-deterministic.
- Split analysis: tour projection is useful without one-hop projection and has
  its own independently reviewable fixture, so one-hop remains 017.
- Dependencies: 005.
- Source anchors: `SPEC.md#op-ofsp-01-derivefocusscene`,
  `T-OFSP-PROJECTION-001`.
- Write scope:
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/projectTourScene.ts`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/projectTourScene.test.ts`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/FOCUS-SCENE-OVERLAY.lock.json`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/focus-scene-overlay-manifest.json`
- Done: pure tests prove exact four-node scene and portal arrays.
- Validation: materialized dashboard test for `projectTourScene.test.ts`.
- Owner: `local-fallback` through Task Session.

## SWU-OFSP-017 — Project deterministic non-tour one-hop scenes

- Primary behavior: derive selected node plus sorted incident endpoints and
  exact internal/portal classification when no tour contains the node.
- Acceptance: named `Authentication and Consent` fixture and inbound/outbound/
  isolated cases match independent arrays; missing endpoints fail closed.
- Split analysis: one-hop is independently useful and testable after L0; it
  does not change reducer or renderer contracts.
- Dependencies: 016.
- Source anchors: `AC-OFSP-002`, `T-OFSP-ONE-HOP-002`.
- Write scope:
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/projectOneHopScene.ts`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/projectScene.ts`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/projectOneHopScene.test.ts`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/FOCUS-SCENE-OVERLAY.lock.json`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/focus-scene-overlay-manifest.json`
- Done: dispatch selects tour or one-hop deterministically and rejects unknown
  or ambiguous input.
- Validation: focused dashboard tests and 001 oracle regression.
- Owner: `local-fallback` through Task Session.

## Completion

The task completes after 005, 006, and later 017. L0 may promote to native state
integration after 006; L1 repeatability remains open until 017.
