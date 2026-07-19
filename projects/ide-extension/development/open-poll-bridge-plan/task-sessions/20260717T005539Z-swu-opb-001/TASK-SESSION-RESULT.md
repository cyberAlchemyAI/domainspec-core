---
module: ide-extension-open-poll-bridge
taskId: TASK-CONTRACT-IDENTITY
swuId: SWU-OPB-001
status: pass
capability_ref: task-session
receipt_kind: local-fallback
createdAt: 2026-07-17T00:55:39Z
---

# TASK SESSION RESULT: SWU-OPB-001

## Scope

Add schema fixtures for open ready and claim-bound `agent_ref`.

## Context Pack

- Mode: lean.
- Strict coverage: pass.
- Sources: `WORK-PACK.md`, `TASK-CONTRACT-IDENTITY.md`,
  bridge claim/result/envelope/receipt schemas, schema validation tests,
  manual bridge contract tests, and schema fixture validator.
- Controlling obligations: accept `openrouter.local-session`, reject malformed
  claimant identity, and keep ready targeting selector-free.

## Decisions

- No blocker decisions.
- Assumption: the local identifier pattern used by `session_ref` is acceptable
  for L0 claimant references until authenticated identity exists.

## Files Updated

- `projects/ide-extension/schemas/bridge-claim-request.schema.json`
- `projects/ide-extension/schemas/agent-envelope.schema.json`
- `projects/ide-extension/schemas/receipt.schema.json`
- `projects/ide-extension/tests/fixtures/schemas/bridge-claim-request.valid.json`
- `projects/ide-extension/tests/fixtures/schemas/receipt.valid.execution.json`
- `projects/ide-extension/tests/fixtures/schemas/bridge-claim-request.invalid-agent-ref.json`
- `projects/ide-extension/tests/fixtures/schemas/receipt.invalid-agent-ref.json`
- `projects/ide-extension/tests/fixtures/schemas/bridge-target-request.invalid-agent-ref.json`
- `projects/ide-extension/tests/l0-schema-validation.test.mjs`
- `projects/ide-extension/tests/manual-session-bridge-contracts.test.mjs`

## Validation

- PASS: `npm --prefix projects/ide-extension run validate:schemas`
  - validated 21 runtime schemas, 6 module manifests, and 81 schema fixtures.
- PASS: `npm --prefix projects/ide-extension run test:schemas`
  - 7 tests passed.
- PASS: `npm --prefix projects/ide-extension run test:bridge-contracts`
  - 7 tests passed.

## Result

PASS. The contract now accepts non-Codex claimant identity and rejects malformed
claimant identity, while the ready/target request remains selector-free.

## Reroute

Proceed to `SWU-OPB-002`.
