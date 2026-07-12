---
module: ide-extension-manual-session-bridge
version: current
status: planned
updatedAt: 2026-07-12
docType: implementation-layering
---

# Implementation Layering: Manual Session Bridge

## Purpose

Deliver the smallest truthful bridge from the local Approval Desk to the active
Codex session before adding automatic recovery, enforceable effects, identity,
or packaging complexity.

## Target And Scope

- Target: `ide-extension` manual Codex session bridge
- Scope: local agent-envelope workflow and evidence loop
- Current state: partially implemented brownfield L0 Approval Desk plus a
  successful but chat-only blind poll experiment
- Active layer window: L0 only
- Readiness target: local pilot witness

## Layer Boundary Rule

```text
After this layer, we know whether the stated decision is supported by evidence.
```

## Layer Decision Table

| Layer | Decision question | Minimum working unit | Included scope | Deferred scope | Exit evidence | Promotion decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | After this layer, we know whether one human-approved, desk-selected request can be claimed only after explicit poll, reveal its skill late, run read-only, recover by human action, and return truthful receipts. | Required task + private skill -> authorization receipt -> singleton ready target -> poll -> atomic claim -> read/preview skill -> execution receipt; interruption branches through operator release/requeue. | v1 replay compatibility; v2 bridge typestate/events; `skill.invoke` + `preview.read`; ready/unready; claim/interrupt/release/result; session CLI/protocol; HTML states; hostile tests; real witness. | Automatic polling, timed leases, authenticated identity, writes/network, provider/browser/IDE adapters, packaging. | Schema/projector/API/CLI/UI tests, restart/replay tests, Playwright desktop/mobile, and one real blind manual receipt. | Continue to L1 only after the L0 witness and non-regression matrix pass. |
| L1 | After this layer, we know whether repeated local operation can recover automatically without duplicate execution. | Expiring claim lease with heartbeat, idempotency, timeout, and multi-session coordination. | Clock-controlled lease/reclaim, retry policy, degraded mode, restart recovery. | Mutation effects, remote identity, packaging. | Fake-clock, crash/restart, duplicate-execution, and degraded-UX evidence. | Harden, narrow, or stop before effectful execution. |
| L2 | After this layer, we know whether mutation-capable skills can be technically constrained rather than merely instructed. | Executor adapter with cwd/write/tool/env/network/credential policy. | Effect-specific approval, process custody, hostile scope-escape tests, before/after evidence. | Remote workers, broad providers, packaging. | Denial proofs, bounded mutation receipts, credential/network isolation, interruption evidence. | Admit a narrow effectful pilot or remain read-only. |
| L3 | After this layer, we know whether persistent and packaged routing can preserve the same authority split. | Authenticated worker/session registry plus optional IDE chrome around the same kernel. | Persistent worker, routing/wake protocol, VSCodium wrapper, packaging, upgrade/rollback, multi-session isolation. | Generic remote multi-agent platform. | Identity, isolation, rollout, recovery, parity, and packaging evidence. | Package a pilot or defer. |

## Active L0 Value And Cost Boundary

- Decision unlocked: whether the manual bridge closes the browser -> session ->
  kernel evidence loop without overstating identity or execution.
- User-visible value: a clear task field, two receipt kinds, one visible poll
  target, claim progress, interruption recovery, and actual result evidence.
- Risk reduced: pre-poll skill disclosure, wrong-request claims, duplicate
  execution packets, approval-as-completion, lost chat-only results, and silent
  authority widening.
- Main cost drivers: version-aware event replay, typestate migration, binding
  tests, truthful UI states, and the real manual witness.
- Stop rule: no L1-L3 scope enters this work-pack even if convenient.

## Non-Regression Guardrails

- Bind the server to loopback by default.
- Preserve every valid v1 event log without rewriting history.
- New bridge events use an explicit v2 contract; reducers remain version-aware.
- Server stores and validates the skill slug but never resolves a skill path.
- Pre-claim responses omit `requested_skill`; the successful claim packet is
  the first agent-facing disclosure.
- Exactly one envelope may be `ready_for_poll`.
- Only an unattested local operator action may ready, unready, revoke, release,
  or requeue.
- L0 permits only `skill.invoke` and `preview.read`; any required write/network
  effect returns a bound blocked result.
- Authorization and execution receipts are distinct and non-substitutable.
- Full prompts, secrets, and model transcripts remain outside kernel state.
- Later layers must preserve every L0 binding and receipt guarantee.

## Recommended Next Layer

- Next layer: L0
- First executable unit: `SWU-MSB-001` versioned bridge contract and fixture
  baseline
- Key decision unlocked: whether the complete v2 contract can coexist with v1
  replay before behavior changes
- Major deferred scope: every automatic, authenticated, mutation-capable,
  remote, browser, provider, and packaged capability
