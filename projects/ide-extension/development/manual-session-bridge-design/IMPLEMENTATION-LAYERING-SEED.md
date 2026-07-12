---
id: ide-extension-manual-session-bridge-layering-seed
project: ide-extension
title: "Manual Session Bridge Implementation Layering Seed"
status: approved
node_type: implementation-layering-seed
updatedAt: 2026-07-12
---

# Implementation Layering Seed: Manual Session Bridge

This is a design-stage seed, not the standalone implementation-layering
artifact required by `invoke plan`.

## Layer Decision Table

| Layer | Question answered | Included boundary | Evidence required for promotion |
| --- | --- | --- | --- |
| L0 manual read/preview bridge | Can one approved request be selected, claimed only after explicit poll, reveal its skill late, recover by human action, and return truthful receipts? | Visible required task; authorization/execution receipt split; singleton ready target; atomic claim; operator release/requeue; fake claimant tests; one real Codex witness; `preview.read` only. | Schema/projector/API tests, singleton/duplicate-claim/recovery negative tests, receipt binding artifacts, desktop/mobile Playwright proof, real manual receipt. |
| L1 reliable local bridge | Can interrupted and repeated local use recover automatically without duplicate execution? | Claim lease, expiry, heartbeat, retry policy, idempotency keys, timeout receipts, multi-session coordination. | Clock-controlled recovery tests, restart/reconciliation tests, replay/adversarial tests, degraded-mode UX proof. |
| L2 enforceable effect bridge | Can write/network-capable skills be constrained by a runtime boundary rather than agent cooperation? | Executor adapter, cwd/write scopes, tool policy, env/credential allowlists, process lifecycle, effect-specific approvals. | Hostile fixture, scope-escape tests, network denial proof, before/after workspace evidence, policy receipts. |
| L3 packaged session routing | Can the bridge support persistent workers, VSCodium chrome, multiple sessions, or remote adapters safely? | Authenticated sessions, worker registry, routing, push/wake protocol, packaging, upgrade/migration, operational observability. | Identity assurance, multi-session isolation, rollout/rollback, upgrade, degraded-mode, and release evidence. |

## Active Layer Window

- Active: L0 only.
- Explicitly deferred: L1-L3.
- Promotion rule: no layer may be entered because it is convenient; its previous
  layer evidence must exist and the operator must approve the new effect/risk
  boundary.

## L0 Smallest Coherent Unit

```text
visible task + private skill
  -> human approval (authorization)
  -> authorization receipt
  -> exactly one ready poll target
  -> explicit chat poll
  -> atomic claim (late disclosure)
  -> installed skill resolution
  -> read/preview execution
  -> claim-bound result
  -> kernel execution receipt

interrupted claim
  -> operator release/requeue
  -> approved
```

Removing any node breaks the proof:

- without the task, the skill receives unusable intent;
- without approval, the request is unauthorized;
- without a distinct authorization receipt, approval evidence is conflated with
  execution evidence;
- without the ready target, plain poll is ambiguous when several requests exist;
- without explicit poll, the bridge is no longer manual;
- without claim, duplicate sessions can execute;
- without late disclosure, the blind property is not preserved;
- without result admission, completion exists only in chat;
- without the kernel receipt, the Approval Desk cannot prove the loop closed.

## L0 Non-Goals

- No automatic polling or persistent worker.
- No Codex CLI/SDK spawning.
- No authenticated session claim.
- No workspace write, shell mutation, network, provider, browser-act, commit,
  push, publication, or external account effects.
- No timed lease or automatic reclaim; operator release/requeue is required.
- No full prompt or transcript persistence.

## Promotion Blockers

| Promotion | Blocker until |
| --- | --- |
| L0 implementation | Approved design and decision record are handed to a plan that owns the spec/typestate delta. |
| L0 -> L1 | Real manual witness returns a kernel execution receipt and duplicate claim/result tests pass. |
| L1 -> L2 | An executor boundary can enforce cwd, write scope, tools, env, network, and credentials. |
| L2 -> L3 | Session identity, isolation, recovery, rollout, and packaging evidence exist. |

## Recomposition Target

The L0 bridge remains one adapter lane inside the existing ide-extension local
kernel. Later browser, IDE, MCP/chat, provider, OpenClaw, and Hermes lanes may
reuse claim/result semantics, but they do not become part of this first unit.
