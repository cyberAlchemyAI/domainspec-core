---
id: ide-extension-workbench-bridge-demo-v01-evidence
project: ide-extension
status: pass
updatedAt: 2026-07-17
---

# Demo Evidence

## Result

PASS.

Workbench Bridge Demo V0.1 is implemented for the L0 manual loop:

```text
prepare -> ready -> poll -> claim -> result -> receipt
```

## Files Changed

- `public/demo/l0.html`
- `tests/l0-workbench-ui.test.mjs`
- `tests/e2e/manual-session-bridge.spec.mjs`
- `development/workbench-bridge-demo-v01/WORK-PACK.md`

## What The UI Now Shows

- A compact Bridge demo panel in the proposal sidebar.
- Manual flow stages: Prepare, Approve, Ready, Claim, Result, Receipt.
- Safe ready-only fields: request handle, ready state, effect profile, assurance, claimant.
- Copyable command hints:
  - `workbench-poll --ready`
  - `workbench-poll --claim --request-handle <id>`
- Terminal receipt summary after `skill.execution` is admitted.

## Boundary Checks

- The panel does not execute poll or claim commands.
- The safe ready fields do not reveal task or requested skill before claim.
- The panel does not add queue, lease, worker, provider, browser-act, or VSCodium scope.
- Completion remains receipt-bound; chat output alone is explicitly not terminal proof.

## Validation

| Check | Result |
| --- | --- |
| `npm run test:workbench` | PASS: 6 tests |
| `npm run test:bridge-result` | PASS: 6 tests |
| `npm run validate:schemas` | PASS: 21 runtime schemas, 6 module manifests, 81 schema fixtures |
| `npm run test:bridge` | PASS: 68 tests |
| `npx playwright test tests/e2e/manual-session-bridge.spec.mjs` | PASS: desktop and mobile |

## Manual Receipt From This Session

Before this implementation slice, the new workbench-poll bridge flow admitted a
real result receipt for the claimed refine task:

```text
receipt-898eb851-3f13-49e3-a7a6-ca46f19803fe
```

That receipt proved the claim/result path. This implementation makes that path
visible and repeatable in the workbench UI.
