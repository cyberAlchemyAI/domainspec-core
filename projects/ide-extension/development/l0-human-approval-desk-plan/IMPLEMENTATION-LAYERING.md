---
module: ide-extension-l0-human-approval-desk
version: current
status: planned
updatedAt: 2026-07-11
docType: implementation-layering
---

# Implementation Layering: L0 Human Approval Desk

## Purpose

Turn the existing cooperative L0 demo into the smallest trustworthy and human-workable local tool before admitting MCP, browser, provider, or IDE execution authority.

## Target And Scope

- Target: `ide-extension` L0 Human Approval Desk
- Scope: local human-in-the-loop product workflow and kernel repair
- Current state: partially implemented brownfield witness
- Active layer window: L0 only
- Readiness target: local pilot

## Layer Mapping

This plan uses L0-L3 planning layers while preserving the finer labels in [ARCHITECTURE.md](../../ARCHITECTURE.md):

| Planning Layer | Architecture Labels | Meaning |
| --- | --- | --- |
| L0 | L0 local workbench | Trustworthy local no-op Approval Desk. |
| L1 | L0.5 MCP/chat admission | One fake offline `observe` adapter behind the repaired kernel. |
| L2 | L0.6 browser-first MV3 | Typed browser observation/action with no authority bypass. |
| L3 | L1 IDE chrome and L2 validation witnesses | Optional IDE wrapper and evidence-only external witnesses. |

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | User-Visible Outcome | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | After this layer, we know whether one local person can inspect and resolve multiple no-op proposals exactly once with durable, resolvable evidence. | Loopback Approval Desk with a proposal queue, approve/reject actions, closed grants, runtime schema enforcement, serialized persistence, before/after artifacts, receipts, and browser proof. | Present-L0 repairs AR-CAND-001 through AR-CAND-008; hostile regression tests; local HTML workflow. | Attested identity, external adapters, network, browser action, shell, Git, providers, VSCodium, collaboration, marketplace packaging. | A person can prepare, inspect, approve or reject, reload, and review history without minting duplicate or dishonest receipts. | Unit, hostile, restart/recovery, schema, smoke, and Playwright tests all pass; every receipt ref resolves. | Continue to L1 only if the L0 acceptance matrix passes and promotion gates are separately approved. |
| L1 | After this layer, we know whether one offline external adapter can be admitted without acquiring approval or receipt authority. | Fake stdio `McpChatWitnessAdapter` with one allowlisted `observe` tool. | Bounded CWD/env/HOME, no network or mutation, kernel receipt, negative tests. | Real MCP servers, Claude delegation, live providers, Chrome, GitHub, deployment. | A local observation can be proposed, approved once, invoked once, and evidenced. | Existing L0 guarantees plus the L0.5 acceptance checks in `SPEC.md`. | Harden, narrow, or stop before browser capability. |
| L2 | After this layer, we know whether typed browser interaction can preserve the same governance boundary. | One MV3 browser witness admitted through L1 contracts. | Typed observe first; bounded action only behind explicit policy and approval. | Broad DevTools, authenticated sensitive pages, remote browser custody, autonomous browsing. | A person can review browser-derived evidence and any proposed action before it occurs. | Negative capability tests, exact action receipts, credential and origin boundaries. | Admit a narrow pilot or return to evidence-only operation. |
| L3 | After this layer, we know whether IDE chrome and external validation improve use without becoming authority. | VS Code/VSCodium opens the same local URL; Playwright/DevTools/Kernel remain evidence lanes. | Host command/webview wrapper, packaging, recovery and upgrade checks. | Collaboration, mobile, generic multi-agent platform, Nimbalyst transplant. | The same Approval Desk is reachable from the IDE without changing its kernel contract. | Wrapper parity, lifecycle, failure, and packaging evidence. | Package a pilot or defer. |

## L0 Value And Cost Boundary

- Decision unlocked: whether the local approval/evidence loop is trustworthy enough for a human pilot.
- User-visible value: queue, clear disposition controls, durable history, and inspectable evidence.
- Risk reduced: replay, false attribution, unreachable approvals, arbitrary grant records, invalid contracts, divergent persistence, and symbolic evidence.
- Main cost drivers: state-machine repair, event replay/reconciliation, hostile tests, and browser evidence.
- Stop rule: no L1 adapter work enters the active window until all L0 exit evidence is present.

## Non-Regression Guardrails

- Bind the server to loopback by default.
- Keep L0 no-op and read-only; no adapter, provider, browser, shell, Git, or network effect enters this plan.
- Never treat caller-provided text or a browser click as attested human identity.
- Only the kernel transitions proposal state, appends authoritative events, and mints receipts.
- A committed approval can produce at most one receipt; rejection produces no success receipt.
- Every durable object is schema-valid before its authoritative write.
- Every receipt reference resolves to a materialized artifact before receipt commit.
- Canvas and projection state remain rebuildable views, not authority.
- Nimbalyst remains pinned product/protocol precedent, not a dependency.

## Recommended Next Layer

- Next layer: L0
- First executable unit: `SWU-IDEAD-001` hostile regression harness
- Key decision unlocked: whether all known present-L0 failures can be reproduced deterministically before repair
- Major deferred scope: every effectful or externally delegated capability
