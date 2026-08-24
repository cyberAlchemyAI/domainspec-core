# TASK-NATIVE-UI — Native Dashboard Bridge And Accessible Surfaces

## Objective

Bridge the pure projection/state contracts into the reviewed native dashboard
through uniquely ordered, preimage-chained successor patches.

Common manifest targets for source-bearing units:

- `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/FOCUS-SCENE-OVERLAY.lock.json`
- `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/focus-scene-overlay-manifest.json`

## SWU-OFSP-009 — Bridge the native dashboard store

- Primary behavior: map existing native selection/focus/history actions to the
  scene reducer and expose read-only active projection/session state.
- Acceptance: focus and portal events use one reducer owner; no second mutable
  scene state remains.
- Split analysis: store bridge is testable before any renderer patch.
- Dependencies: 004, 008.
- Write scope:
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/patches/0002-focus-scene-store.patch`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/nativeStoreBridge.test.ts`
  - both common manifest targets above
- Done/validation: exact upstream pre/post hashes and materialized dashboard
  store tests pass.

## SWU-OFSP-010 — Render only the active scene and semantic portals

- Primary behavior: filter nodes/relations before layout and render exact
  internal relations plus boundary portals.
- Acceptance: named tour arrays match, fixed unrelated node is absent, and no
  full-graph focused DOM/state remains.
- Split analysis: bounded graph membership/portal exposure is one renderer
  contract; relation activation controls remain 012.
- Dependencies: 009.
- Write scope:
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/patches/0003-focus-scene-renderer.patch`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/nativeRenderer.test.tsx`
  - both common manifest targets
- Done/validation: materialized renderer tests and fixture-oracle comparison
  pass.

## SWU-OFSP-011 — Add the named detail landmark and focus transfer

- Primary behavior: add an explicit skip/selection route, named detail
  landmark, and post-commit focus coordinator.
- Acceptance: exact search/skip/portal destination focus lands on the landmark
  whose accessible text contains node name and `authority:none`; Back restores
  focus or falls back to the landmark.
- Split analysis: focus destination is independently testable without relation
  activation parity or focus styling.
- Dependencies: 010.
- Write scope:
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/patches/0004-focus-scene-detail-landmark.patch`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/detailLandmark.test.tsx`
  - both common manifest targets
- Done/validation: named landmark/skip/focus restoration component tests pass.

## SWU-OFSP-012 — Make relation controls input-equivalent

- Primary behavior: render internal relations and portals as semantic selected
  controls whose pointer, Enter, and Space activation dispatch the same action.
- Acceptance: literal tuple, programmatic selected state, breadcrumb, and
  canonical session bytes are identical for all three activation kinds.
- Split analysis: operation parity is independent of focus styling and motion.
- Dependencies: 011.
- Write scope:
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/patches/0005-focus-scene-relation-controls.patch`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/relationControls.test.tsx`
  - both common manifest targets
- Done/validation: materialized relation-control tests and reducer parity
  fixtures pass.

## SWU-OFSP-013 — Add visible focus and reduced-motion presentation

- Primary behavior: give every pivot-capable control non-color visible focus
  geometry and make reduced-motion scene replacement immediate.
- Acceptance: fixed Tab bound and nonzero outline/border geometry pass in
  default and reduced-motion modes; semantic state is unchanged and active
  orientation animation count is zero under reduced motion.
- Split analysis: presentation/motion is one CSS/media-query response and has a
  distinct browser/component boundary; no contrast claim is included.
- Dependencies: 012.
- Write scope:
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/patches/0006-focus-scene-focus-motion.patch`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/focusMotion.test.tsx`
  - both common manifest targets
- Done/validation: materialized focus/motion tests pass.

## SWU-OFSP-020 — Integrate source literals across named surfaces

- Primary behavior: reuse one formatter across search, node, detail, relation,
  breadcrumb, and pivot destination.
- Acceptance: `SuggestedTrack` exact kind/status/authority/path agrees on every
  named surface; the non-candidate fixture never fabricates status.
- Split analysis: string/accessibility parity is independently testable from
  forced-colors visuals.
- Dependencies: 019.
- Write scope:
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/patches/0008-focus-scene-literals.patch`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/sourceLiteralSurfaces.test.tsx`
  - both common manifest targets
- Done/validation: exact visible/accessibility string assertions pass.

## SWU-OFSP-021 — Add forced-colors non-color redundancy

- Primary behavior: preserve kind, status, authority, selection, and portal
  meaning with text/icon/shape/border cues when authored colors are suppressed.
- Acceptance: forced-colors component/browser checks prove cues and visible
  focus geometry; no contrast-compliance claim is made.
- Split analysis: forced-colors presentation has its own mode-specific
  acceptance and does not alter literals.
- Dependencies: 020.
- Write scope:
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/patches/0009-focus-scene-forced-colors.patch`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/forcedColors.test.tsx`
  - both common manifest targets
- Done/validation: materialized forced-colors tests pass.

## Patch Chaining

The successor manifest orders `0002` through `0010`. When two patches touch the
same native file, each later preimage equals the prior patch's postimage.
Reapplication and out-of-order application must fail.

