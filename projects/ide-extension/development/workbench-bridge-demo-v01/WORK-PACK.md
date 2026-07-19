---
id: ide-extension-workbench-bridge-demo-v01-work-pack
project: ide-extension
title: "Workbench Bridge Demo V0.1 Work Pack"
status: completed
node_type: work-pack
updatedAt: 2026-07-17
planning_gate_status: pass
complexity: low
output_mode: single-file
active_layer: L0
layering_artifact_ref: IMPLEMENTATION-LAYERING.md
distill_validation_status: pass
---

# Work Pack: Workbench Bridge Demo V0.1

## Objective

Make the existing manual bridge visible and repeatable from the workbench UI.

Success means a user can understand and demonstrate:

```text
prepare -> ready -> poll -> claim -> result -> receipt
```

without the UI revealing task or requested skill before claim.

## Source Contracts

- [SPEC.md](SPEC.md)
- [Architecture bundle](ARCHITECTURE-BUNDLE.md)
- [Layering](IMPLEMENTATION-LAYERING.md)
- [Project bridge contract](../../SPEC.md)
- [Manual bridge protocol](../../SESSION-BRIDGE-PROTOCOL.md)
- [Open poll bridge work-pack](../open-poll-bridge-plan/WORK-PACK.md)

## Delivery Boundary

Included:

- `public/demo/l0.html` bridge demo UI changes,
- minimal read-model mapping if needed,
- UI labels and command-copy affordances,
- tests for ready, claim, and receipt display,
- blind-boundary validation.

Excluded:

- automatic polling,
- queue or lease behavior,
- real skill execution automation,
- provider calls,
- browser/VSCodium control,
- remote deployment.

## Task Board

| Task | Goal | Layer | Gate | Status |
| --- | --- | --- | --- | --- |
| TASK-WBD-001 | Add bridge recipe/status panel to the workbench. | L0 | pass | completed |
| TASK-WBD-002 | Add safe command-copy affordances for ready and claim. | L0 | pass | completed |
| TASK-WBD-003 | Add receipt display after admitted result. | L0 | pass | completed |
| TASK-WBD-004 | Add tests and manual demo evidence. | L0 | pass | completed |

## Execution Units

This is low complexity. Each task is already the intended executable unit; no
separate SWU layer is required.

### TASK-WBD-001 - Bridge Recipe/Status Panel

Write scope:

- `public/demo/l0.html`
- existing frontend test fixture files if needed

Implementation detail:

- Add a compact panel near existing bridge/approval desk UI.
- Show the current flow stages: prepared, approved, ready, claimed, result.
- Before claim, display only safe ready fields: state, request handle, effect profile, assurance, timestamps.
- Do not display task or requested skill from any ready-only projection.

Validation:

- PASS: `npm run test:workbench`
- PASS: focused Playwright manual bridge ready panel assertion.

### TASK-WBD-002 - Command-Copy Affordances

Write scope:

- `public/demo/l0.html`
- tests for rendered command strings

Implementation detail:

- Show `workbench-poll --ready`.
- When a request handle exists, show `workbench-poll --claim --request-handle <id>`.
- Keep these as copyable/manual command hints. Do not execute commands from browser code.

Validation:

- PASS: `npm run test:workbench`
- PASS: focused Playwright command text includes the current ready handle.

### TASK-WBD-003 - Receipt Display

Write scope:

- `public/demo/l0.html`
- tests for receipt state rendering

Implementation detail:

- When a `skill.execution` receipt exists for the current envelope, show receipt id, status, claimant, summary, and evidence refs.
- Make clear that receipt admission is terminal proof.
- Do not treat claimed state as completed.

Validation:

- PASS: `npm run test:bridge-result`
- PASS: `npm run test:workbench`
- PASS: focused Playwright receipt summary assertion.

### TASK-WBD-004 - Test And Demo Evidence

Write scope:

- `tests/`
- `development/workbench-bridge-demo-v01/evidence/`

Implementation detail:

- Add or update focused tests for ready secrecy, claim display, and receipt display.
- Preserve one manual demo note with request handle, claim id, and receipt id from a local run.

Validation:

- PASS: `npm run validate:schemas`
- PASS: `npm run test:bridge`
- PASS: `npm run test:workbench`
- PASS: `npx playwright test tests/e2e/manual-session-bridge.spec.mjs`
- Evidence: [DEMO-EVIDENCE.md](evidence/DEMO-EVIDENCE.md)

## Gate Checks

1. Do not reveal task or requested skill before claim.
2. Do not run poll/claim commands from browser code.
3. Do not add queue, lease, worker, provider, browser-act, or VSCodium scope.
4. Do not mark bridge completion without `skill.execution` receipt.
5. Do not mutate durable state outside kernel APIs.

## Distill Validation

Status: pass.

The first executable unit is `TASK-WBD-001`. It recomposes into the design
because the panel provides the visible spine for commands and receipt display.

## Next Route

Completed. Next route is daily use through `workbench-up --available` and
`workbench-poll --ready/--claim`, or a new governed plan for automatic polling,
leases, or worker behavior.
