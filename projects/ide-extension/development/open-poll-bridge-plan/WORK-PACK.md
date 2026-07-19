---
module: ide-extension-open-poll-bridge
version: current
status: pilot-ready
updatedAt: 2026-07-16
docType: work-pack
---

# WORK-PACK: Open Poll Bridge

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | L0 open-poll bridge evidence passed. |
| complexity | medium | Contract, server, CLI, UI, and witness changes cross several L0 surfaces. |
| outputMode | split | Five tasks and nine SWUs require independent handoffs. |
| executionPackRef | [EXECUTION-PACK.md](EXECUTION-PACK.md) | Execution choreography. |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | L0-L3 boundary authority. |
| dispatchTechniqueTrace | [open-poll-bridge-plan.dispatch.json](open-poll-bridge-plan.dispatch.json) | Planning route and techniques. |
| distillValidationStatus | pass | See [DISTILL-VALIDATION.md](DISTILL-VALIDATION.md). |
| activeLayerWindow | L0 | L1-L3 are deferred. |
| lastUpdatedAt | 2026-07-17 | Closure audit completed. |
| readinessProfile | local pilot | Non-Codex claimant witness required. |
| closureReport | [CLOSURE-REPORT.md](task-sessions/20260717T010850Z-swu-opb-009/CLOSURE-REPORT.md) | Evidence-backed L0 readiness claim. |

## Objective Summary

Implement an open singleton poll bridge: the workbench publishes one approved
request as generally available, any interested local session can poll and claim
it, and the server binds the terminal receipt to the claimant identity captured
at claim time.

Primary inputs:

- [open-poll-bridge refresh report](../open-poll-bridge-refresh/REFRESH-REPORT.md)
- [open-poll-bridge findings](../open-poll-bridge-research/findings.md)
- [manual bridge protocol](../../SESSION-BRIDGE-PROTOCOL.md)
- [manual bridge plan baseline](../manual-session-bridge-plan/WORK-PACK.md)

Success condition: a non-Codex claimant, for example
`openrouter.local-session`, can see ready availability without a selector,
claim exactly one request, return a result, and produce receipts that show the
non-Codex `agent_ref`.

## Delivery Slices

| Slice | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-001 | Contracts and replay distinguish ready availability from claim identity. | L0 | [W0](work-pack/waves/W0.md) | none | Schema fixtures and replay tests pass. |
| S-002 | Server exposes caller-neutral ready and atomic non-Codex claim/result binding. | L0 | [W1](work-pack/waves/W1.md) | S-001 | API, race, restart, and receipt tests pass. |
| S-003 | CLI and workbench teach open availability without adding worker behavior. | L0 | [W2](work-pack/waves/W2.md) | S-002 | CLI and UI tests pass. |
| S-004 | Witness proves one winner, loser secrecy, replay, restart, and browser visibility. | L0 | [W3](work-pack/waves/W3.md) | S-003 | Node, Playwright, and manual/scripted witness pass. |

## Task Status Board

| Task | Goal | Layer | Complexity | Wave | Gate | Status |
| --- | --- | --- | --- | --- | --- | --- |
| [TASK-CONTRACT-IDENTITY](work-pack/tasks/TASK-CONTRACT-IDENTITY.md) | Make claim identity explicit in schemas, fixtures, and replay. | L0 | medium | W0 | passed | completed |
| [TASK-READY-CLAIM-API](work-pack/tasks/TASK-READY-CLAIM-API.md) | Change ready/claim/result behavior to open singleton semantics. | L0 | high | W1 | passed | completed |
| [TASK-SESSION-WORKBENCH](work-pack/tasks/TASK-SESSION-WORKBENCH.md) | Update CLI/protocol and workbench affordances. | L0 | medium | W2 | passed | completed |
| [TASK-WITNESS](work-pack/tasks/TASK-WITNESS.md) | Add integrated proof for non-Codex claim, race, replay, and browser state. | L0 | high | W3 | passed | completed |
| [TASK-VERIFY-READINESS](work-pack/tasks/TASK-VERIFY-READINESS.md) | Close the L0 claim with evidence and residue. | L0 | medium | W3 | passed | completed |

## SWU Manifest

| SWU | Parent | Goal | Dependencies | Write scope | Evidence/validation | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-OPB-001 | [TASK-CONTRACT-IDENTITY](work-pack/tasks/TASK-CONTRACT-IDENTITY.md) | Add schema fixtures for open ready and claim-bound `agent_ref`. | none | `schemas/`, fixtures, schema tests | [PASS: schema validation, schema tests, contract tests](task-sessions/20260717T005539Z-swu-opb-001/TASK-SESSION-RESULT.md) | local-fallback | completed |
| SWU-OPB-002 | [TASK-CONTRACT-IDENTITY](work-pack/tasks/TASK-CONTRACT-IDENTITY.md) | Update reducer/projector replay to preserve stored claim identity. | 001 | `src/envelopes/`, bridge replay tests | [PASS: replay, contract, schema validation](task-sessions/20260717T005707Z-swu-opb-002/TASK-SESSION-RESULT.md) | local-fallback | completed |
| SWU-OPB-003 | [TASK-READY-CLAIM-API](work-pack/tasks/TASK-READY-CLAIM-API.md) | Make ready polling caller-neutral and selector-free. | 002 | server routes, bridge kernel helpers, API tests | [PASS: authorization, claim, full bridge suite](task-sessions/20260717T005841Z-swu-opb-003/TASK-SESSION-RESULT.md) | local-fallback | completed |
| SWU-OPB-004 | [TASK-READY-CLAIM-API](work-pack/tasks/TASK-READY-CLAIM-API.md) | Bind non-Codex claim/result identity and preserve race secrecy. | 003 | claim/result handlers, receipts, concurrency tests | [PASS: claim, result, full bridge suite](task-sessions/20260717T010003Z-swu-opb-004/TASK-SESSION-RESULT.md) | local-fallback | completed |
| SWU-OPB-005 | [TASK-SESSION-WORKBENCH](work-pack/tasks/TASK-SESSION-WORKBENCH.md) | Update session bridge CLI/protocol for open ready and claim identity. | 004 | `scripts/session-bridge.mjs`, protocol doc, CLI tests | [PASS: CLI and full bridge suite](task-sessions/20260717T010136Z-swu-opb-005/TASK-SESSION-RESULT.md) | local-fallback | completed |
| SWU-OPB-006 | [TASK-SESSION-WORKBENCH](work-pack/tasks/TASK-SESSION-WORKBENCH.md) | Update workbench labels and states from target/selected to available/claimed. | 004 | `public/demo/l0.html`, UI tests | [PASS: workbench, bridge, focused Playwright](task-sessions/20260717T010408Z-swu-opb-006/TASK-SESSION-RESULT.md) | local-fallback | completed |
| SWU-OPB-007 | [TASK-WITNESS](work-pack/tasks/TASK-WITNESS.md) | Add Node witness for open ready, non-Codex claim, race, result, replay, and restart. | 005,006 | integration/adversarial/recovery tests | [PASS: dedicated Node witness and bridge suite](task-sessions/20260717T010554Z-swu-opb-007/TASK-SESSION-RESULT.md) | local-fallback | completed |
| SWU-OPB-008 | [TASK-WITNESS](work-pack/tasks/TASK-WITNESS.md) | Add Playwright/manual witness evidence for the workbench path. | 007 | `tests/e2e/`, evidence report/assets | [PASS: workbench UI and focused Playwright witness](task-sessions/20260717T010713Z-swu-opb-008/TASK-SESSION-RESULT.md) | manual-or-local-fallback | completed |
| SWU-OPB-009 | [TASK-VERIFY-READINESS](work-pack/tasks/TASK-VERIFY-READINESS.md) | Audit closure, sync status, and preserve residue. | 008 | plan status, task-session result, closeout report | [PASS: closure report and final validation](task-sessions/20260717T010850Z-swu-opb-009/TASK-SESSION-RESULT.md) | local-fallback | completed |

## Blockers And Gaps

| ID | Type | Description | Owner | Treatment |
| --- | --- | --- | --- | --- |
| GAP-OPB-001 | assurance | Current proof is Codex-shaped and does not prove non-Codex claim identity. | SWU-OPB-007/008 | Add witness using a non-Codex `agent_ref`. |
| GAP-OPB-002 | contract | Ready availability is conceptually mixed with target/selector identity. | SWU-OPB-001/003 | Split ready and claim semantics in fixtures and endpoints. |
| GAP-OPB-003 | receipt | Result identity can drift if terminal request supplies or defaults `agent_ref`. | SWU-OPB-002/004 | Derive terminal identity from stored claim. |
| GAP-OPB-004 | UI | Workbench still suggests selected target/poll type rather than open availability. | SWU-OPB-006 | Rename states and action copy. |
| GAP-OPB-005 | CLI | Session CLI defaults to Codex wording. | SWU-OPB-005 | Keep Codex as a default value only, not as the model. |
| GAP-OPB-006 | scope | Multi-request queue, worker registry, leases, and automatic pollers are tempting but not needed for proof. | architecture owner | Explicit L1/L3 deferral. |
| GAP-OPB-007 | observability | `/api/state` may expose full local debug projection. | SWU-OPB-007/009 | Keep it out of the poll contract; verify public poll surfaces preserve secrecy. |

No gap blocks the L0 pilot. GAP-OPB-006 remains an accepted L1/L3 deferral, not
a defect. GAP-OPB-007 remains a debug-boundary note; public poll surfaces stayed
narrower than `/api/state` in witness tests.

## Dispatch Technique Trace

| Technique | Applied to | Validation expectation | Status |
| --- | --- | --- | --- |
| `sequence` | W0 -> W1 -> W2 -> W3 | Every wave consumes prior receipts. | pass |
| `scu_swu_reduction` | Nine SWUs | Each unit has one parent, bounded scope, and validation. | pass |
| `recomposition_proof` | SWUs -> L0 witness | Units close the single open-poll route without L1-L3 scope. | pass |
| `validation_loop` | Every SWU | Each change has command, browser, or review evidence. | pass |
| `owner_boundary_check` | operator, kernel, poller, claimant, task-session | No owner receives unapproved authority. | pass |
| `handle_handoff` | Invoke -> Task Session | Task Session receives paths/SWU IDs, not transcript-only context. | pass |
| `residue_ledger` | Gaps and deferrals | Every residue has owner and treatment. | pass |
| `execution_receipt_handoff` | Every SWU | Result shape includes status, files, validations, residue, and reroute. | pass |
| `authority_split_gate` | ready, claim, result, recovery | Availability, claim, execution, and recovery stay separate. | pass |
| `artifact_contract_bridge` | schemas, receipts, evidence | Artifact contracts bind the implementation claim. | pass |
| `state_namespace_boundary` | `/api/bridge/*` vs `/api/state` | Poll contract remains narrower than debug state. | pass |

## Gate Checks

1. Execute exactly one SWU per Task Session.
2. Do not change ready endpoint behavior until contract fixtures pass.
3. Do not expose non-Codex claim until replay preserves claim identity.
4. Do not update UI wording until API semantics are real.
5. Do not mark complete without a non-Codex claimant receipt.
6. Do not import queues, leases, background workers, mutation effects, provider
   routing, or IDE/browser control into L0.

## Expected SWU Result

```yaml
swu_id: SWU-OPB-NNN
result: pass | flag | block | interrupted
capability_ref: task-session
receipt_kind: native-stage | local-fallback | blocked
receipt_artifact: path-or-none
files_touched: []
validation: []
blockers: []
residue: []
reroute: next-swu-or-none
handoff_note: concise continuation state
```

## Next Route

Completed:

```text
L0 open-poll bridge is pilot-ready. Use the bridge in the workbench, or open a
new governed plan for automatic polling/lease behavior.
```
