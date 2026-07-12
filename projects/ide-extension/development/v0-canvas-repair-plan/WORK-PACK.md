---
id: ide-extension-v0-canvas-repair-work-pack
project: ide-extension
title: "V0 Canvas Repair Work Pack"
status: completed
node_type: work-pack
updatedAt: 2026-07-12
planning_gate_status: pass
active_layer: closed
---

# Work Pack: V0 Canvas Repair

## Objective

Align the trusted-local canvas authority contract and prevent resolved
workspace paths from escaping the configured root, without changing V0 API
behavior or implementing Operations V1.

## Delivery Slices

| Slice | Outcome | Layer | Wave | Validation |
| --- | --- | --- | --- | --- |
| VCR-S1 | Canvas approval/receipt prose becomes coherent. | L0 | [W0](work-pack/waves/W0.md) | Contract review and phrase checks. |
| VCR-S2 | Publish and content fetch use canonical contained targets. | L1 | [W1](work-pack/waves/W1.md) | Focused helper/API tests. |
| VCR-S3 | Symlink counterexamples and normal behavior are locked by tests. | L2 | [W2](work-pack/waves/W2.md) | Adversarial and canvas suites pass. |
| VCR-S4 | Accepted findings have implementation evidence and no overclaim. | L3 | [W3](work-pack/waves/W3.md) | Integrated validation and scoped diff pass. |

## Task Board

| Task | Goal | Layer | Wave | Status |
| --- | --- | --- | --- | --- |
| [TASK-CANVAS-POLICY](work-pack/tasks/TASK-CANVAS-POLICY.md) | Declare the narrow trusted-local preview/display exception. | L0 | W0 | completed |
| [TASK-PATH-ADMISSION](work-pack/tasks/TASK-PATH-ADMISSION.md) | Enforce canonical containment and adversarial path behavior. | L1-L2 | W1-W2 | completed |
| [TASK-VERIFY](work-pack/tasks/TASK-VERIFY.md) | Run integrated audit and synchronize evidence. | L3 | W3 | completed |

## SWU Manifest

| SWU | Parent | Goal | Dependencies | Write scope | Acceptance evidence | Verification | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-VCR-001 | [TASK-CANVAS-POLICY](work-pack/tasks/TASK-CANVAS-POLICY.md) | Align canvas approval and receipt semantics. | none | `SPEC.md`, `ARCHITECTURE.md` | [PASS: exact exception, protected-effect boundary, and read clarification](task-sessions/20260712T181604Z-swu-vcr-001/TASK-SESSION-RESULT.md) | documentation review plus `rg` checks | local-fallback | completed |
| SWU-VCR-002 | [TASK-PATH-ADMISSION](work-pack/tasks/TASK-PATH-ADMISSION.md) | Implement canonical root/target admission through one file handle. | 001 | `src/kernel/canvas.mjs`, `src/server.mjs`, focused helper tests | [PASS: canonical targets, external rejection, no-byte content failure](task-sessions/20260712T181804Z-swu-vcr-002/TASK-SESSION-RESULT.md) | focused path-admission tests | local-fallback | completed |
| SWU-VCR-003 | [TASK-PATH-ADMISSION](work-pack/tasks/TASK-PATH-ADMISSION.md) | Add adversarial API and compatibility regression matrix. | 002 | canvas publish/content tests and package test script only if needed | [PASS: 17/17 path, contract, publish, and replay tests](task-sessions/20260712T182108Z-swu-vcr-003/TASK-SESSION-RESULT.md) | canvas contract/publish/replay suites | local-fallback | completed |
| SWU-VCR-004 | [TASK-VERIFY](work-pack/tasks/TASK-VERIFY.md) | Audit, record evidence, and close review traceability. | 003 | this work-pack evidence/status artifacts only | [PASS: 83/83 tests plus schema, trace, and diff audits](task-sessions/20260712T182329Z-swu-vcr-004/TASK-SESSION-RESULT.md) | full scoped validation and diff check | local-fallback | completed |

## Blockers And Gaps

| ID | Class | Description | Owner | Treatment |
| --- | --- | --- | --- | --- |
| GAP-VCR-001 | platform | Portable Node cannot provide Linux `openat2(RESOLVE_BENEATH)` semantics on every platform. | path-admission task | Prove retained symlink traces; do not claim hostile race immunity. |
| GAP-VCR-002 | definition | Exact parser and blob semantics belong to Operations V1, not this repair. | future Operations V1 plan | Exclude. |
| GAP-VCR-003 | workspace | Repository has unrelated concurrent changes. | unrelated owners | Use scoped checks; never clean or revert. |

No active blocker remains in this work-pack. GAP-VCR-001 remains an explicit
future-hardening limitation, not a V0 closure claim.

## Gate Checks

1. Execute exactly one SWU per Task Session.
2. Policy must be explicit before code changes.
3. Preserve existing request/response schemas and V0 surface identity.
4. Do not turn a canvas audit event into an execution receipt.
5. Reject canonical targets outside the root on publish and content fetch.
6. Never include external file bytes in an error or response.
7. Do not implement Operations V1 or declared regions.

## Expected Result Shape

```yaml
swu_id: SWU-VCR-NNN
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

V0 canvas repair is complete. Operations V1 remains a separate design-ready
lifecycle and requires an accepted Invoke plan before mutation-capable work.
