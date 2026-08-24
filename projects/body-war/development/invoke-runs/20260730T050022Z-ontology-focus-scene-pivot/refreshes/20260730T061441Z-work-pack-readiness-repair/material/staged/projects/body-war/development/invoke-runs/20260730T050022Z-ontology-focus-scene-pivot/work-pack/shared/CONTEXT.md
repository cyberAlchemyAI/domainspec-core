# Shared Implementation Context

## Immutable Inputs

- `SPEC.md`
- `ARCHITECTURE.md`
- `UX-PLAN.md`
- accepted review
  `projects/body-war/development/reviews/20260730-ontology-ui-black-box/findings.md`
  and
  `projects/body-war/development/reviews/20260730-ontology-ui-black-box/synthesis.md`
- upstream commit `2cda14e89535049e49120198886bc0b82e9e630f`
- frozen graph digest
  `e8f754e6aed7b05759439df82db421eb51fa050c78b86b37d5d689e89a751433`

## Canonical/Generated Rule

Future feature source belongs in a new successor overlay/lock under
`cyberAlchemy-v2/implementation/ontology-evidence-workbench/upstream/` and in
workbench scripts/tests/contracts. The pinned archive, materialized workroots,
generated dashboard bundles, and existing generated receipts are never edited.

## Native Logical Owners

The future overlay/patch route targets the pinned native logical sources:

- `packages/dashboard/src/store.ts`
- `packages/dashboard/src/components/KnowledgeGraphView.tsx`
- `packages/dashboard/src/components/NodeInfo.tsx`
- `packages/dashboard/src/components/LearnPanel.tsx`
- `packages/dashboard/src/components/SearchBar.tsx`
- `packages/dashboard/src/components/CustomNode.tsx`
- `packages/dashboard/src/App.tsx`
- `packages/dashboard/src/index.css`

The current checked-in `packages/dashboard/src/oew/**` overlay is a separate
`?oew=1` route and must not be mistaken for these native owners.

## Runtime Rule

- Use the existing workbench package root.
- Do not add or modify `package.json` to obtain Playwright.
- Resolve the active global Playwright/Chromium exactly as `AGENTS.md`
  prescribes and pin version, executable, revision, hashes, and teardown in the
  task receipt.
- Directly invoke new successor build/validation scripts; do not rely on the
  absent historical `materialize-l1-build.mjs` or `verify-l1-build.mjs`.

## Expected Task Session Result

Every Task Session return must validate against
`TASK-SESSION-RECEIPT.schema.json`. That is the only terminal receipt shape
used by Task Session, Dispatch Spec boundary evidence, and Invoke Refresh.

Required routing fields include `run_id`, `session_id`, `dispatch_id`,
`step_id`, `capability_ref`, `status`, and `unit_id`. Exact files/digests live in
`artifacts`; commands/exit codes live in `validation`; `files_touched`,
`blockers`, `residue`, `authority_effect`, `claim_ceiling`, and `handoff_note`
are always explicit.

## First Unit Navigation

- exact input:
  `cyberAlchemy-v2/implementation/ontology-evidence-workbench/generated/runs/BODY-WAR-ONTOLOGY-001/presentation-graph.json`
- command working directory:
  `cyberAlchemy-v2/implementation/ontology-evidence-workbench`
- selected task selector:
  `work-pack/tasks/TASK-FOUNDATION.md#swu-ofsp-001--derive-the-independent-body-war-scene-oracle`
- validation:
  `node --test test/focus-scene-fixture.test.mjs`


## Readiness And Runtime Reuse

- `COMMAND-MATRIX.json` is the exact per-unit argv/cwd/write/attempt/
  teardown contract.
- SWU 003 generalizes the retained
  `scripts/materialize-l1-workroot.mjs` lifecycle instead of creating a
  second extraction/install/cleanup owner.
- SWU 004 extends its independent-verification pattern.
- A successor `FOCUS-SCENE-BUILD.lock.json` may import only verified
  upstream/toolchain/execution substrate from `L1-BUILD.lock.json`; it
  must not import the historical `?oew=1` feature overlay.
- The closeout directory is created atomically by the first admitted
  closeout owner; an absent directory is not execution evidence.
