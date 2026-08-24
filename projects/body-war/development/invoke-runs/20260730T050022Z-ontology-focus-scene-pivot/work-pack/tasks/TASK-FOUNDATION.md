# TASK-FOUNDATION — Independent Oracle And Native Overlay Route

## Objective

Establish a test-owned scene oracle and a reproducible successor native
dashboard overlay/build path before feature source is changed.

Layer: L0. Slice: foundation. Dependencies: none.

## SWU-OFSP-001 — Derive the independent Body War scene oracle

- Primary behavior: derive and pin expected tour nodes, internal relations,
  portals, exact literal tuple, and one unrelated-node negative directly from
  the frozen graph bytes.
- Independent acceptance: the fixture test proves graph digest `e8f754…`,
  current 237/231 baseline, exact `Business capability map` arrays, and the
  `Identity and Consent` → `Authentication and Consent` tuple without importing
  production scene-selector code.
- Split analysis: generator, fixture, and test are one evidence contract; the
  generated fixture has no useful acceptance boundary without its independent
  derivation test.
- Dependencies: none.
- Source anchors: `SPEC.md#acceptance-contracts`,
  `ARCHITECTURE.md#planned-witness-contracts`, frozen presentation graph.
- Write scope:
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/scripts/derive-body-war-focus-scene-fixture.mjs`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/test/fixtures/body-war-focus-scenes.json`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/test/focus-scene-fixture.test.mjs`
- Done: deterministic regeneration is byte-identical; fixture asserts the
  current failing baseline and exact source literals; production selector
  imports are rejected.
- Validation: `node --test test/focus-scene-fixture.test.mjs`.
- Execution owner: `local-fallback` through one Task Session.

## SWU-OFSP-002 — Admit the successor native overlay contract

- Primary behavior: bind the exact native logical source preimages,
  destinations, feature files, upstream commit/archive, and historical
  immutability rules in a new overlay contract.
- Independent acceptance: validator rejects changed upstream archive/preimage,
  missing/extra overlay entry, generated target, historical lock rewrite, and
  unbound native file.
- Split analysis: the manifest and its validation test form one admission
  behavior; materialization and build verification remain separate SWUs.
- Dependencies: 001.
- Source anchors: `ARCHITECTURE.md#ownership-correction`,
  `UPSTREAM.lock.json`, current overlay/first-working manifests.
- Write scope:
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/FOCUS-SCENE-OVERLAY.lock.json`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/overlay/focus-scene-overlay-manifest.json`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/test/focus-scene-overlay.test.mjs`
- Done: new contract is independently testable, identifies the eight native
  logical owners, keeps historical locks/manifests immutable, and declares a
  test-only copy from
  `test/fixtures/body-war-focus-scenes.json` into the materialized dashboard
  test tree. A negative import check forbids production projection modules from
  consuming that fixture.
- Validation: `node --test test/focus-scene-overlay.test.mjs` plus
  `git diff --check -- upstream/FOCUS-SCENE-OVERLAY.lock.json upstream/overlay/focus-scene-overlay-manifest.json test/focus-scene-overlay.test.mjs`.
- Execution owner: `local-fallback` through one Task Session.

## SWU-OFSP-003 — Materialize a fresh successor-overlay workroot

- Primary behavior: generalize the retained
  `scripts/materialize-l1-workroot.mjs` lifecycle into a successor materializer
  that can create an outside-repository,
  digest-named workroot from the pinned archive, apply the exact successor
  overlay/patch set once, run frozen install/test/build commands, emit a handle,
  and clean up.
- Independent acceptance: tests prove traversal/symlink/preimage/duplicate
  patch/unbound file failures, isolated store, no workspace/global fallback,
  recorded commands, and cleanup in `finally`.
- Split analysis: extraction, exact overlay application, build invocation, and
  cleanup are one lifecycle owned by the materializer; independent handle
  verification is split to 004.
- Dependencies: 002.
- Source anchors: `ARCHITECTURE.md#build-and-acceptance`,
  `upstream/L1-TOOLCHAIN.lock.json`.
- Write scope:
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/scripts/materialize-focus-scene-build.mjs`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/test/focus-scene-materializer.test.mjs`
- Done: materializer unit/integration fixtures pass without retaining an
  immutable build attempt. Its Task Session receipt proves tooling readiness
  only; the first real producer handle is SWU-OFSP-014.
- Validation: `node --test test/focus-scene-materializer.test.mjs`.
- Execution owner: `local-fallback` through one Task Session.

## SWU-OFSP-004 — Independently verify successor build handles

- Primary behavior: extend the retained independent-verification pattern
  to validate a successor materializer handle
  against exact lock, input,
  command, output-tree, runtime, and cleanup contracts.
- Independent acceptance: valid handle passes; stale input, missing command,
  changed output tree, self-issued verification, or surviving workroot fails.
- Split analysis: schema, verifier, and negative tests define one verification
  behavior; producing the first feature build remains 014.
- Dependencies: 003.
- Source anchors: `ARCHITECTURE.md#validator-contracts`.
- Write scope:
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/contracts/focus-scene-build-handle.schema.json`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/scripts/verify-focus-scene-build.mjs`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/test/focus-scene-build-verifier.test.mjs`
- Done: verifier fixtures are distinct from producer code and fail closed on
  all named mutations. Its Task Session receipt proves verifier readiness only;
  SWU-OFSP-014 produces and verifies the first immutable handle. The
successor `FOCUS-SCENE-BUILD.lock.json` imports only verified upstream,
toolchain, and execution substrate; the historical `?oew=1` feature inputs stay
excluded.
- Validation: `node --test test/focus-scene-build-verifier.test.mjs`.
- Execution owner: `local-fallback` through one Task Session.

## Synchronization And Completion

Run sequentially. Each unit closes through
`../shared/CLOSEOUT-CONTRACT.md`; no later unit may infer a missing predecessor
receipt. Task completes when 001–004 pass and the next route is 005.
