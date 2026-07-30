# TASK-ACCEPTANCE — Verified Build And Structural Browser Evidence

## SWU-OFSP-014 — Produce and independently verify the L0 build

- Primary behavior: materialize the bound L0 overlay, run frozen tests/build,
  emit one producer handle, independently verify it, and clean the workroot.
- Acceptance: producer and verifier evidence bind inputs, commands, output tree,
  runtime, separation, and cleanup.
- Split analysis: tooling authoring was split into 003/004; this unit is one
  immutable L0 build-evidence event.
- Dependencies: 013.
- Write scope:
  - new attempt only under
    `cyberAlchemy-v2/implementation/ontology-evidence-workbench/generated/runs/SWU-OFSP-014/`
- Done/validation: producer handle and independent verification receipt pass.

## SWU-OFSP-015 — Implement the browser validator contract

- Primary behavior: validate exact arrays, literal portal/state, input/motion
  parity, focus geometry, source literals, runtime identity, and teardown.
- Acceptance: negative validator fixtures reject 237/231 focus, unrelated node,
  stale/parity state, invalid build, token persistence, and failed teardown.
- Split analysis: validator/schema/tests are one contract; real execution is
  016.
- Dependencies: 014.
- Write scope:
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/scripts/validate-body-war-focus-scene.mjs`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/contracts/body-war-focus-scene-acceptance.schema.json`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/test/body-war-focus-scene-browser.test.mjs`
- Done/validation:
  `node --test test/body-war-focus-scene-browser.test.mjs`.

## SWU-OFSP-016 — Execute the immutable L0 browser acceptance

- Primary behavior: run one native-route acceptance attempt against the verified
  L0 build and frozen presentation graph.
- Acceptance: L0 contracts pass, global Playwright/Chromium identity is pinned,
  no new package/dependency appears, and teardown/claim ceiling pass.
- Split analysis: one attempt directory and receipt is the smallest acceptance
  event.
- Dependencies: 015.
- Write scope:
  - new attempt only under
    `cyberAlchemy-v2/implementation/ontology-evidence-workbench/generated/runs/SWU-OFSP-016/`
- Done/validation: independent schema/digest verification of the new receipt.

## SWU-OFSP-022 — Produce and independently verify the L1 build

- Primary behavior: build the L1 one-hop/tour/literal/forced-colors overlay and
  independently verify one new handle.
- Acceptance: all L0 and L1 source/patch/toolchain/output bindings pass.
- Split analysis: build evidence is independent of browser regression and
  mirrors L0 separation.
- Dependencies: 021.
- Write scope:
  - new attempt only under
    `cyberAlchemy-v2/implementation/ontology-evidence-workbench/generated/runs/SWU-OFSP-022/`
- Done/validation: producer and independent verifier receipts pass.

## SWU-OFSP-023 — Execute the immutable L1 browser regression

- Primary behavior: run the full tour/one-hop/tour-lifecycle/literal/
  forced-colors regression against the verified L1 build.
- Acceptance: every L0 assertion and all L1 assertions pass.
- Split analysis: browser regression is one immutable evidence event separate
  from build production.
- Dependencies: 022.
- Write scope:
  - new attempt only under
    `cyberAlchemy-v2/implementation/ontology-evidence-workbench/generated/runs/SWU-OFSP-023/`
- Done/validation: independent browser receipt verification passes.

## Evidence Ceiling

All outputs are new immutable attempts. They prove only the exact structural
claims recorded; they do not prove comprehension, release, deployment, or
production readiness.

