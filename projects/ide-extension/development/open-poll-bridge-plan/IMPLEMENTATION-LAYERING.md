---
module: ide-extension-open-poll-bridge
version: current
status: planned
updatedAt: 2026-07-16
docType: implementation-layering
---

# Implementation Layering: Open Poll Bridge

## Purpose

Prove that the local workbench can publish one open request that any interested
session can poll, while preserving singleton safety, late disclosure, claim
identity, and truthful receipts.

## Target And Scope

- Target: `ide-extension` manual session bridge.
- Scope: local L0 bridge contract, server API, CLI, workbench copy, and witness.
- Current state: the manual bridge works for the Codex-shaped path but still
  models ready work as selected/targeted and defaults identity to Codex.
- Active layer window: L0 only.
- Readiness target: human-workable local pilot witness for a non-Codex claimant.

## Layer Boundary Rule

```text
After this layer, we know whether a local request can be made openly available,
claimed by a non-Codex session, and closed with the claimed identity preserved.
```

## Layer Decision Table

| Layer | Decision question | Minimum working unit | Included scope | Deferred scope | Exit evidence | Promotion decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | Can one approved request be visible to any poller, claimed by exactly one session, and completed with claim-bound identity? | Contract fixture -> caller-neutral ready -> atomic claim with `agent_ref` -> result receipt bound to stored claim -> UI/CLI witness. | Schema/replay identity split; ready endpoint without selector; claim request identity; result receipt identity; CLI protocol; workbench copy; race/restart/browser/manual witness. | Multi-request queue, background poller, authenticated workers, leases, mutation effects, remote providers, IDE/browser control. | Node schema/API/replay/CLI tests, Playwright workbench check, and one non-Codex manual or scripted witness. | Continue only after the non-Codex claim witness passes. |
| L1 | Can repeated local operation avoid stale claims without operator micromanagement? | Lease/heartbeat/reclaim policy with duplicate-execution tests. | Timers, fake-clock tests, recovery UX. | Mutation, remote identity, packaging. | Expiry/reclaim/restart evidence. | Admit automatic polling only after duplicate-execution risk is bounded. |
| L2 | Can effectful skills be technically constrained? | Executor policy adapter for cwd/write/tool/network/env. | Mutation approvals, denial tests, before/after evidence. | Remote multi-agent platform. | Scope-escape denials and mutation receipts. | Admit narrow effectful pilot or remain read-only. |
| L3 | Can this become packaged workbench infrastructure? | Authenticated session registry plus IDE/browser packaging around the same kernel. | Provider adapters, VSCodium or browser extension shell, upgrade/rollback. | Generic cloud orchestration. | Identity/isolation/packaging evidence. | Package only if L0-L2 invariants remain intact. |

## L0 Guardrails

- Open availability does not mean a queue; L0 keeps one ready item at a time.
- `GET /api/bridge/ready` must not require or honor an `agent_ref` selector.
- The ready payload must not disclose `requested_skill` before claim.
- `POST /api/bridge/claim` is the first moment the claimant identity is bound.
- Result admission must use the stored claim identity.
- A loser in a claim race must learn only safe state, not the task payload.
- CLI and UI language must say available/open/claimed, not selected-for-Codex.
- Operator recovery remains explicit; no background worker or auto-poll loop.

## Recommended Next Layer

- Next layer: L0.
- First executable unit: `SWU-OPB-001`.
- Key decision unlocked: whether the contract can express claim-bound identity
  before any endpoint behavior changes.
