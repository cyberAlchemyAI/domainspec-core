# TASK-RELIABILITY — Truthful Degraded Behavior

## SWU-OFSP-024 — Enforce pure fail-closed scene-source policy

- Primary behavior: pure projector/reducer returns exact errors for unknown
  node, ambiguous tour membership, missing endpoint/provenance, or stale source
  without partial mutation.
- Acceptance: each error has an independent negative fixture; prior truthful
  state is unchanged where recovery is possible; no complete-graph fallback or
  fabricated literal occurs.
- Split analysis: pure error policy is independently testable before rendered
  degraded UX.
- Dependencies: 023.
- Write scope:
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/projectScene.ts`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/sceneReducer.ts`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/degradedPolicy.test.ts`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/FOCUS-SCENE-OVERLAY.lock.json`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/focus-scene-overlay-manifest.json`
- Done/validation: pure negative fixtures pass with exact error codes.

## SWU-OFSP-025 — Render degraded state and recovery

- Primary behavior: native UI presents exact bounded error meaning and retry/
  overview recovery without rendering fabricated or complete fallback content.
- Acceptance: each pure error maps to exact visible/accessibility output and
  recovery action; browser negative assertions pass.
- Split analysis: rendered recovery is a distinct human-facing semantic
  contract from selector/reducer policy.
- Dependencies: 024.
- Write scope:
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/patches/0010-focus-scene-degraded-state.patch`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/packages/dashboard/src/focus-scene/degradedState.test.tsx`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/test/body-war-focus-scene-degraded-browser.test.mjs`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/FOCUS-SCENE-OVERLAY.lock.json`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/focus-scene-overlay-manifest.json`
- Done/validation: component/browser recovery assertions and all regressions
  pass.

## Closure Tasks

These tasks are closure-only and SWU-exempt. Each has an exact owner and
receipt target:

| Task | Owner | Receipt |
| --- | --- | --- |
| `TASK-VERIFY` | independent acceptance validator | `work-pack/closeout/TASK-VERIFY.receipt.json` |
| `TASK-AUDIT-ALIGNMENT` | Body War product-ontology owner | `work-pack/closeout/TASK-AUDIT-ALIGNMENT.receipt.json` |
| `TASK-AUDIT-LAYERING` | OEW overlay/build owner | `work-pack/closeout/TASK-AUDIT-LAYERING.receipt.json` |

Execution order is 025 → VERIFY → AUDIT-ALIGNMENT → AUDIT-LAYERING → 026. A
failed or missing audit receipt blocks packaging.

