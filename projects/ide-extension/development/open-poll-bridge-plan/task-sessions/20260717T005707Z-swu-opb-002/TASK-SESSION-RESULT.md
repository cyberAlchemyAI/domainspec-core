---
module: ide-extension-open-poll-bridge
taskId: TASK-CONTRACT-IDENTITY
swuId: SWU-OPB-002
status: pass
capability_ref: task-session
receipt_kind: local-fallback
createdAt: 2026-07-17T00:57:07Z
---

# TASK SESSION RESULT: SWU-OPB-002

## Scope

Update reducer/projector replay to preserve stored claim identity.

## Context Pack

- Mode: lean.
- Strict coverage: pass.
- Sources: `TASK-CONTRACT-IDENTITY.md`, bridge reducer helpers,
  projector replay checks, schema fixtures, and bridge replay tests.
- Controlling obligations: existing v1 replay remains exact; v2/open bridge
  replay preserves non-Codex claim identity through completed claim and receipt.

## Decisions

- No blocker decisions.
- Assumption: result payloads remain without an `agent_ref`; the execution
  receipt is the identity-bearing terminal artifact and must match the stored
  claim.

## Files Updated

- `projects/ide-extension/src/envelopes/manual-session-bridge.mjs`
- `projects/ide-extension/src/kernel/projector.mjs`
- `projects/ide-extension/tests/manual-session-bridge-replay.test.mjs`

## Validation

- PASS: `npm --prefix projects/ide-extension run test:bridge-replay`
  - 7 tests passed.
- PASS: `npm --prefix projects/ide-extension run test:bridge-contracts`
  - 7 tests passed.
- PASS: `npm --prefix projects/ide-extension run validate:schemas`
  - validated 21 runtime schemas, 6 module manifests, and 81 schema fixtures.

## Result

PASS. Claims now use the request `agent_ref`, projector replay accepts local
claimant identifiers, and execution receipts must match the stored claim
identity.

## Reroute

Proceed to `SWU-OPB-003`.
