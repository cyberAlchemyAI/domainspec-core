---
id: ide-extension-manual-session-bridge-plan
project: ide-extension
title: "Manual Session Bridge Implementation Plan"
status: pilot-ready
node_type: development-package
updatedAt: 2026-07-12
invoke_mode: plan
phase_status: pass
---

# Manual Session Bridge Implementation Plan

This package converted the approved manual-session-bridge design into a medium,
split, L0-only work-pack. Task Session completed all eleven SWUs and the closure
audit; the result is ready only for the bounded local pilot described below.

## Package Index

| Artifact | Purpose |
| --- | --- |
| [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | L0-L3 decision boundaries and promotion evidence. |
| [WORK-PACK.md](WORK-PACK.md) | Canonical executable plan, task board, SWU manifest, gates, and first route. |
| [EXECUTION-PACK.md](EXECUTION-PACK.md) | Cross-task wave choreography and merge/stop rules. |
| [DISTILL-VALIDATION.md](DISTILL-VALIDATION.md) | Smallest-unit, recomposition, hidden-gap, and navigation verdict. |
| [PLAN-TRANSPORT.md](PLAN-TRANSPORT.md) | Context selection, templates, technique trace, decisions, gaps, and handoff. |
| [manual-session-bridge-plan.dispatch.json](manual-session-bridge-plan.dispatch.json) | Machine-validated planning route and receipt handoff. |
| [CLOSURE-REPORT.md](task-sessions/20260712T115410Z-task-verify-readiness/CLOSURE-REPORT.md) | Final validation matrix, receipt audit, exact pilot claim, and residue. |
| [work-pack/shared/context.md](work-pack/shared/context.md) | Bounded planning context and obligation coverage. |
| [work-pack/shared/cross-task-decisions.md](work-pack/shared/cross-task-decisions.md) | Approved product decisions plus implementation planning defaults. |
| [work-pack/shared/cross-task-gaps.md](work-pack/shared/cross-task-gaps.md) | Accepted limitations, migration risks, and owners. |
| [work-pack/shared/traceability.md](work-pack/shared/traceability.md) | Design requirement to task/SWU/evidence mapping. |
| `work-pack/tasks/` | Six detailed task contracts. |
| `work-pack/waves/` | Four L0 execution waves. |

## Delivery Boundary

Included: a loopback, manual, read/preview-only bridge where the human approves
and marks one request ready, the active unattested Codex session claims it only
after `poll`, and the kernel records separate authorization and execution
receipts with operator-only interruption recovery.

Excluded: background workers, Codex CLI/SDK spawning, authenticated sessions,
timed leases, mutation/network effects, VSCodium/browser integration, external
providers, and remote/multi-user operation.

## Closure Status

- Eleven SWUs: completed, 11/11 PASS.
- Full Node suite: 88/88.
- Bridge safety suite: 66/66.
- Chromium desktop/mobile: 4/4.
- Real blind witness: PASS with two receipts and retained evidence.
- Readiness: local manual read/preview-only pilot.

L1-L3 remain separate governed decisions; this package does not authorize
automatic polling, authenticated identity, mutation/network effects, persistent
workers, VSCodium/browser control, providers, remote operation, or packaging.
