---
id: ide-extension-workbench-bridge-demo-v01-architecture
project: ide-extension
status: planned
updatedAt: 2026-07-17
invoke_mode: design
---

# Architecture Bundle: Workbench Bridge Demo V0.1

## 1. Context View

The current system already proves the bridge mechanically. The missing product
piece is a clear operator surface.

Actors:

- operator: prepares and approves work in the workbench,
- poller session: runs `workbench-poll --ready` and `--claim`,
- local kernel: owns state, admission, artifacts, and receipts,
- workbench UI: displays state and command recipes.

Source contracts:

- `SPEC.md` manual session bridge contract,
- `SESSION-BRIDGE-PROTOCOL.md` command contract,
- `open-poll-bridge-plan/WORK-PACK.md` pilot-ready closeout,
- `workbench-up` and `workbench-poll` sigils.

## 2. High-Level Structure View

```text
public/demo/l0.html
  -> existing /api/state or focused bridge endpoints
  -> bridge projection
  -> copyable command hints
  -> receipt viewer
```

The demo panel should reuse existing projection data. If a narrower read route
already exposes the needed bridge status, prefer it. If not, add the smallest
read-only projection route rather than teaching the UI to inspect state files.

## 3. Low-Level Components View

| Component | Responsibility |
| --- | --- |
| Bridge recipe panel | Shows current manual flow, commands, and status. |
| Ready card | Shows request handle and safe metadata only. |
| Claim card | Shows claimant and claim state after claim. |
| Receipt card | Shows terminal receipt id, status, summary, and evidence refs. |
| UI state mapper | Converts projection state into human labels. |
| Tests | Verify status display and blind-boundary behavior. |

## 4. Workflow Process View

1. Operator prepares and approves a task.
2. Operator marks it ready.
3. Workbench shows "Ready for any interested local session" with a handle.
4. Workbench shows `workbench-poll --ready`.
5. When a request is ready, workbench shows `workbench-poll --claim --request-handle <id>`.
6. After claim, workbench shows claimant state but does not pretend the work is complete.
7. After result admission, workbench shows `skill.execution` receipt details.

## 5. Decision Flow View

| Question | Decision |
| --- | --- |
| Should the UI auto-poll? | No. Manual one-shot polling remains the L0 proof. |
| Should the UI reveal task before claim? | No. Ready display must remain opaque. |
| Should the UI create a result? | No. Result is submitted by the claimed session through bridge commands/API. |
| Should the UI show receipts? | Yes. Admitted receipt is the useful terminal proof. |

## 6. Dependency Interface View

| Interface | Used For | Constraint |
| --- | --- | --- |
| `GET /demo/l0` | Workbench shell | Must keep existing route. |
| Bridge ready/projection API | Safe status display | Must not reveal task before claim. |
| `/api/state` | Possible read source | Debug-wide; prefer narrowed mapping if practical. |
| `npm run bridge:session` | Command recipe | UI can display command text but must not run it. |
| Receipt artifacts | Terminal proof | Display only after kernel admission. |

## Risks And Gaps

| ID | Gap | Treatment |
| --- | --- | --- |
| WBD-G1 | Existing `/api/state` may include debug-wide state. | UI mapper must display only safe ready fields before claim. |
| WBD-G2 | Too much UI copy could become tutorial clutter. | Use compact status labels and command chips. |
| WBD-G3 | Result display may lag until refresh. | Accept manual refresh or existing polling; no worker needed. |

## Design Dispatch Technique Trace

| Technique | Applied To | Validation Expectation |
| --- | --- | --- |
| `sequence` | Visible bridge timeline | UI order follows typestate. |
| `owner_boundary_check` | UI vs kernel | UI displays state; kernel owns admission. |
| `artifact_contract_bridge` | receipt card | Terminal proof is receipt-bound. |
| `validation_loop` | UI tests | Tests prove blind-boundary state. |

## Distill Design Check

Result: pass.

The coherent design unit is the visible manual bridge recipe. It is small enough
to execute without opening automatic polling or provider execution.
