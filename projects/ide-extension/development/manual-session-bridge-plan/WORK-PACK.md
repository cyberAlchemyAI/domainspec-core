---
module: ide-extension-manual-session-bridge
version: current
status: pilot-ready
updatedAt: 2026-07-12
docType: work-pack
---

# WORK-PACK: Manual Session Bridge

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | L0 closure audit passes; bounded local pilot is ready. |
| complexity | medium | Durable typestate migration spans contracts, kernel, APIs, session tooling, UI, and evidence. |
| outputMode | split | Six tasks and eleven SWUs require independent contracts. |
| executionPackRef | [EXECUTION-PACK.md](EXECUTION-PACK.md) | Cross-task choreography. |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | L0-L3 boundary authority. |
| dispatchTechniqueTrace | [manual-session-bridge-plan.dispatch.json](manual-session-bridge-plan.dispatch.json) | Validated planning route. |
| distillValidationStatus | pass | See [DISTILL-VALIDATION.md](DISTILL-VALIDATION.md). |
| activeLayerWindow | L0 | L1-L3 are explicit deferrals, not executable waves. |
| lastUpdatedAt | 2026-07-12 | Closure audit completed. |
| readinessProfile | pilot | Loopback manual read-only witness. |
| closureReport | [CLOSURE-REPORT.md](task-sessions/20260712T115410Z-task-verify-readiness/CLOSURE-REPORT.md) | Exact evidence-backed L0 claim and residue. |

## Objective Summary

- Objective: implement a truthful manual poll bridge from Approval Desk to the
  active Codex session and return actual read-only skill results to the kernel.
- Primary inputs: approved [architecture](../manual-session-bridge-design/ARCHITECTURE-BUNDLE.md),
  passed [decisions](../manual-session-bridge-design/DECISIONS.md), approved
  [UX plan](../manual-session-bridge-design/UX-PLAN.md), and no-op
  [refresh](../manual-session-bridge-refresh/REFRESH-REPORT.md).
- Success condition: one real blind request completes the full prepare ->
  authorize -> ready -> poll -> claim -> skill -> result path, with separate
  receipts, operator recovery, no v1 regression, and complete automated/browser
  evidence.

## Delivery Slices

| Slice | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-001 | Versioned contract and replay baseline can express the bridge without invalidating v1 history. | L0 | [W0](work-pack/waves/W0.md) | none | Schema fixtures and v1/v2 projector tests pass. |
| S-002 | Kernel owns singleton targeting, atomic claim, interruption/requeue, result admission, and two receipts. | L0 | [W1](work-pack/waves/W1.md) | S-001 | API, binding, concurrency, and artifact tests pass. |
| S-003 | Codex has a bounded one-shot session protocol and the human has truthful task/target/recovery/result controls. | L0 | [W2](work-pack/waves/W2.md) | S-002 | CLI/protocol and workbench tests pass. |
| S-004 | Hostile/restart/browser evidence plus one real blind witness prove the complete L0 route. | L0 | [W3](work-pack/waves/W3.md) | S-003 | Full Node, schema, Playwright, and manual receipt evidence pass. |

## Task Status Board

| Task | Goal | Layer | Complexity | Wave | Gate | Status |
| --- | --- | --- | --- | --- | --- | --- |
| [TASK-CONTRACT-MIGRATION](work-pack/tasks/TASK-CONTRACT-MIGRATION.md) | Define v2 contracts while preserving v1 history. | L0 | high | W0 | passed | completed |
| [TASK-BRIDGE-KERNEL](work-pack/tasks/TASK-BRIDGE-KERNEL.md) | Implement target, claim, recovery, result, and receipt authority. | L0 | high | W1 | passed | completed |
| [TASK-SESSION-PROTOCOL](work-pack/tasks/TASK-SESSION-PROTOCOL.md) | Provide the explicit one-shot Codex polling/return protocol. | L0 | medium | W2 | passed | completed |
| [TASK-HUMAN-WORKBENCH](work-pack/tasks/TASK-HUMAN-WORKBENCH.md) | Deliver visible task, receipt, target, claim, recovery, and evidence states. | L0 | medium | W2 | passed | completed |
| [TASK-VALIDATION-WITNESS](work-pack/tasks/TASK-VALIDATION-WITNESS.md) | Prove hostile, restart, browser, and real manual behavior. | L0 | high | W3 | passed | completed |
| [TASK-VERIFY-READINESS](work-pack/tasks/TASK-VERIFY-READINESS.md) | Audit closure and synchronize evidence-backed status. | L0 | medium | W3 | passed | completed |

## SWU Manifest

| SWU | Parent | Goal | Dependencies | Write scope | Evidence/validation | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-MSB-001 | [TASK-CONTRACT-MIGRATION](work-pack/tasks/TASK-CONTRACT-MIGRATION.md) | Add the bounded spec/grant/schema/fixture contract including typed receipt branches. | none | `SPEC.md`, `schemas/`, schema registry/fixtures/tests, `src/kernel/grants.mjs` | [PASS: 12 schemas, 41 fixtures, 58 Node tests](task-sessions/20260712T055820Z-swu-msb-001/TASK-SESSION-RESULT.md) | local-fallback | completed |
| SWU-MSB-002 | [TASK-CONTRACT-MIGRATION](work-pack/tasks/TASK-CONTRACT-MIGRATION.md) | Add version-aware v1/v2 replay and complete bridge typestate transitions. | 001 | projector/envelope/storage compatibility modules and focused tests | [PASS: exact v1, mixed v2, restart, 65 Node tests](task-sessions/20260712T060816Z-swu-msb-002/TASK-SESSION-RESULT.md) | local-fallback | completed |
| SWU-MSB-003 | [TASK-BRIDGE-KERNEL](work-pack/tasks/TASK-BRIDGE-KERNEL.md) | Implement singleton ready/unready and authorization receipt flow. | 002 | bridge kernel/server/artifacts plus focused API tests | [PASS: authorization/target/restart/secrecy, 72 Node tests](task-sessions/20260712T062325Z-swu-msb-003/TASK-SESSION-RESULT.md) | local-fallback | completed |
| SWU-MSB-004 | [TASK-BRIDGE-KERNEL](work-pack/tasks/TASK-BRIDGE-KERNEL.md) | Implement atomic claim, interrupt, and operator release/requeue. | 003 | bridge kernel/server/projector plus concurrency/recovery tests | [PASS: atomic claim/recovery/restart, 77 Node tests](task-sessions/20260712T062622Z-swu-msb-004/TASK-SESSION-RESULT.md) | local-fallback | completed |
| SWU-MSB-005 | [TASK-BRIDGE-KERNEL](work-pack/tasks/TASK-BRIDGE-KERNEL.md) | Admit bound terminal result and mint execution receipt/artifacts. | 004 | bridge kernel/server/receipt/artifacts plus tests | [PASS: result/receipt/artifacts/restart, 83 Node tests](task-sessions/20260712T063105Z-swu-msb-005/TASK-SESSION-RESULT.md) | local-fallback | completed |
| SWU-MSB-006 | [TASK-SESSION-PROTOCOL](work-pack/tasks/TASK-SESSION-PROTOCOL.md) | Add one-shot ready/claim/result/interrupt CLI and protocol documentation. | 005 | `scripts/session-bridge.mjs`, protocol doc, package script, focused tests | [PASS: one-shot CLI/process/API, 86 Node tests](task-sessions/20260712T063619Z-swu-msb-006/TASK-SESSION-RESULT.md) | local-fallback | completed |
| SWU-MSB-007 | [TASK-HUMAN-WORKBENCH](work-pack/tasks/TASK-HUMAN-WORKBENCH.md) | Repair task/approval/receipt language and evidence display. | 005 | `public/demo/l0.html`, UI/API tests | [PASS: semantic task/approval/receipt UI, 87 Node tests](task-sessions/20260712T063929Z-swu-msb-007/TASK-SESSION-RESULT.md) | local-fallback | completed |
| SWU-MSB-008 | [TASK-HUMAN-WORKBENCH](work-pack/tasks/TASK-HUMAN-WORKBENCH.md) | Add ready target, claim/interruption, operator recovery, and result UX. | 006, 007 | workbench HTML and bridge UI tests | [PASS: complete operator state matrix, 88 Node tests](task-sessions/20260712T064328Z-swu-msb-008/TASK-SESSION-RESULT.md) | local-fallback | completed |
| SWU-MSB-009 | [TASK-VALIDATION-WITNESS](work-pack/tasks/TASK-VALIDATION-WITNESS.md) | Add hostile, race, replay, restart, and v1 non-regression suite. | 008 | bridge integration/adversarial/recovery tests and test scripts | [PASS twice: 66/66 bridge safety cases](task-sessions/20260712T064639Z-swu-msb-009/TASK-SESSION-RESULT.md) | local-fallback | completed |
| SWU-MSB-010 | [TASK-VALIDATION-WITNESS](work-pack/tasks/TASK-VALIDATION-WITNESS.md) | Prove desktop/mobile prepare, receipts, target, recovery, and terminal evidence. | 009 | Playwright spec/assets and package scripts | [PASS: 4/4 desktop/mobile Chromium journeys](task-sessions/20260712T064813Z-swu-msb-010/TASK-SESSION-RESULT.md) | local-fallback | completed |
| SWU-MSB-011 | [TASK-VALIDATION-WITNESS](work-pack/tasks/TASK-VALIDATION-WITNESS.md) | Run one real blind manual Codex poll and preserve bound execution evidence. | 010 | temporary state plus checked-in evidence report/assets only | [PASS: blind claim, terminal flagged result, two receipts, 7/7 evidence](task-sessions/20260712T065218Z-swu-msb-011/TASK-SESSION-RESULT.md) | manual | completed |

Every SWU is expanded in its parent task contract with source anchors, ordered
rules, edge cases, done criteria, acceptance evidence, verification, execution
owner, and expected result shape.

## Blockers And Gaps

| ID | Type | Description | Owner | Treatment |
| --- | --- | --- | --- | --- |
| GAP-MSBP-001 | migration | Existing v1 `receipt.appended` events encode approval as completed dry-run execution. | SWU-001/002 | Preserve v1 reducer branch and history; emit v2 for bridge; never rewrite logs. |
| GAP-MSBP-002 | assurance | `session_ref` does not authenticate Codex or a process. | architecture owner | Record `assurance: unattested`; keep L0 read-only. |
| GAP-MSBP-003 | recovery | Operator requeue may repeat a read-only attempt. | SWU-004/009 | Preserve attempt history; no silent retry; mutation layers require a new policy. |
| GAP-MSBP-004 | environment | The final witness requires a live active Codex session and human browser actions. | SWU-011 owner | Resolved for L0 by the retained real blind witness; keep as an environment prerequisite for reruns. |
| GAP-MSBP-005 | workspace | Repository-wide diff currently has unrelated cyberAlchemy-v2 EOF findings. | unrelated owner | Use scoped checks; do not touch unrelated files or claim global clean state. |

No gap blocks `TASK-VERIFY-READINESS`. GAP-MSBP-002 and GAP-MSBP-003 remain
accepted L0 boundaries; GAP-MSBP-005 remains unrelated workspace residue.

## Dispatch Technique Trace

| Technique | Applied to | Validation expectation | Status |
| --- | --- | --- | --- |
| `sequence` | W0 -> W1 -> W2 -> W3 | Every wave consumes prior receipts. | pass |
| `scu_swu_reduction` | Eleven SWUs | Each unit has one parent and independent evidence. | pass |
| `recomposition_proof` | SWUs -> approved L0 design | All units close the single manual bridge loop without L1-L3 scope. | pass |
| `validation_loop` | Every slice/SWU | Each mutation has a command or reviewable check. | pass |
| `owner_boundary_check` | Invoke, Task Session, kernel, session, operator | No owner claims another boundary. | pass |
| `handle_handoff` | Plan -> Task Session | Execution consumes paths/selectors, not ambient transcript. | pass |
| `residue_ledger` | Gaps and deferrals | Every residue has owner/treatment. | pass |
| `execution_receipt_handoff` | Every SWU | Result shape includes files, validation, blockers, residue, reroute. | pass |
| `authority_split_gate` | authorization/claim/result/promotion | Human, kernel, session, and plan owners remain separate. | pass |
| `artifact_contract_bridge` | typed receipts/evidence | Artifact checks bind without claiming execution prematurely. | pass |
| `concrete_path_evidence` | closure/readiness | Every claim cites a path, test, receipt, or review check. | pass |

## Distill Validation

| Check | Result | Evidence |
| --- | --- | --- |
| Smallest coherent unit | pass | SWU-MSB-001 creates the complete versioned contract oracle before behavior changes. |
| Recomposition proof | pass | 001-002 contracts; 003-005 kernel; 006-008 protocol/UI; 009-011 proof. |
| Hidden acceptance-critical gaps | pass | Legacy replay, two receipts, singleton targeting, interruption, session assurance, and real witness are explicit. |
| Deferred complexity | pass | Timers, auth, mutation, workers, IDE/browser/provider adapters remain outside active layer. |
| Navigation to first unit | pass | Start with `--swu SWU-MSB-001`. |

## Gate Checks

1. Execute one SWU per Task Session.
2. Do not emit v2 behavior until v1 replay fixtures pass.
3. Do not expose claim APIs until singleton targeting and authorization receipt
   bindings pass.
4. Do not expose UI recovery until kernel actor/state tests pass.
5. Do not run the real witness until automated and Playwright suites pass.
6. Do not mark the bridge complete unless the execution receipt resolves and
   the authorization receipt makes no execution claim.
7. Do not admit L1-L3 scope or mutate unrelated repositories/artifacts.

## Expected SWU Result

```yaml
swu_id: SWU-MSB-NNN
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

```text
L0 bounded local pilot is ready. Do not promote to L1-L3 without a new governed
design/plan and the evidence required by IMPLEMENTATION-LAYERING.md.
```
