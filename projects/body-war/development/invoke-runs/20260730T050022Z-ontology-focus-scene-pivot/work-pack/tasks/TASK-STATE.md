# TASK-STATE — Atomic Scene Session

## Common Source Targets

- `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/sceneReducer.ts`
- `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/FOCUS-SCENE-OVERLAY.lock.json`
- `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/focus-scene-overlay-manifest.json`

## SWU-OFSP-007 — Commit focus and internal-relation selection

- Primary behavior: create a `SceneSession` from a projection and persist exact
  internal-relation selection without replacing the scene.
- Acceptance: focus sets one scene/node; internal selection adds only the exact
  tuple; invalid/stale event leaves prior state unchanged.
- Split analysis: base focus/selection is testable before portal history.
- Dependencies: 006.
- Write scope:
  - all common source targets
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/serializeSemanticState.ts`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/sceneReducer.focus.test.ts`
- Done/validation: deterministic reducer/serializer tests pass.

## SWU-OFSP-008 — Commit portal pivot and Back atomically

- Primary behavior: select the portal tuple, push one breadcrumb, derive and
  replace destination state, and restore exact prior state through Back.
- Acceptance: canonical state matches fixture; duplicate event does not
  duplicate history; Back restores the stored state.
- Split analysis: portal/Back is one reversible transition pair; UI controls
  remain SWU 012.
- Dependencies: 007.
- Write scope:
  - all common source targets
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/serializeSemanticState.ts`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/sceneReducer.portal.test.ts`
- Done/validation: literal portal and Back reducer fixtures pass.

## SWU-OFSP-018 — Implement pure tour suspension/restoration

- Primary behavior: reducer tour entry suspends pre-tour state, step change
  replaces active state/clears stale selection, and exit restores.
- Acceptance: pre-tour/entered/step-two/exited canonical state fixtures match;
  stale active `Authentication and Consent` after step change fails.
- Split analysis: reducer protocol is independently testable without native
  tour-panel wiring.
- Dependencies: 017.
- Write scope:
  - all common source targets
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/sceneReducer.tour.test.ts`
- Done/validation: pure tour state tests pass for pointer/keyboard/motion-neutral
  actions.

## SWU-OFSP-019 — Bridge native tour controls and announcements

- Primary behavior: existing `LearnPanel` start/step/exit controls dispatch the
  pure tour protocol and announce entry/replacement/restoration.
- Acceptance: native controls preserve exact active/suspended state and focus;
  no out-of-scene inspector remains active.
- Split analysis: native bridge/announcement is a distinct rendered interaction
  boundary from the reducer protocol.
- Dependencies: 018.
- Write scope:
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/patches/0007-focus-scene-tour.patch`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/nativeTourBridge.test.tsx`
  - both common manifest targets
- Done/validation: materialized LearnPanel and tour-focus tests pass.

