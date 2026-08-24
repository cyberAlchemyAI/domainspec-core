---
module: one-shot-admission-prototype
version: candidate
status: approved-candidate-local
updatedAt: 2026-07-30
docType: implementation-layering
---

# Implementation Layering: One-shot admission prototype

## Purpose

Prove the accepted exact-binding architecture as a local candidate without
misstating deferred lifecycle synchronization as complete governance.

## Source Contract

- Accepted research:
  `../2026-07-30-invoke-one-shot-workflow-research/findings.md`
- User route decision: `DECISION-GATE.md`, option A.
- Public owners:
  `arcanum/spells/work-pack-readiness-audit/README.md` and
  `arcanum/spells/task-session-until-blocker/README.md`.

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | After this layer, we know whether an additive public contract can express and reject deterministic admission omissions before a Task Session request. | WPRA v2 schemas, projection generation, semantic digest, and negative fixtures. | Public, project-neutral contracts and deterministic tests. | Durable chain execution and consuming-project replay. | WPRA schema parse and fixture suite. | Continue only if v1 remains compatible and deterministic omissions block. |
| L1 | After this layer, we know whether an approved finite epoch can advance without widening one-SWU Task Session ownership. | Durable chain runner with epoch, cursor, budget, risk, NO_OP, and compensation-stop checks. | Public chain schemas, runner, and fixtures. | Upstream receipt hardening and owner dispatch adapters. | Chain fixture suite. | Continue only if every invalid epoch/transition stops before a next request. |
| L2 | After this layer, we know whether the two public candidates recompose against the frozen Body War evidence. | Private 19-case replay and aggregate validation. | Read-only frozen inputs and private receipts. | Product mutation, registry, promotion, publication, deployment. | 19 case receipts and aggregate report. | Reconcile governance only after the prototype passes. |
| L3 | After this layer, we know whether the candidate can enter the governed reusable lifecycle. | Deferred owner reconciliation. | Invoke/Interview/Decision Gate receipt hardening, generated parity, experiment evidence, owner review. | Release and production claims. | Handoff Notice plus later governed work pack. | Not authorized in this run. |

## Non-regression Guardrails

- WPRA projections always have `authorityEffect: none`.
- Existing v1 WPRA inputs and tests remain valid.
- Task Session remains one SWU per receipt.
- No private Body War path or value enters public Arcanum files.
- No automatic compensation or frontier expansion is introduced.
- Validation is mandatory even though lifecycle choreography is deferred.

## Recommended Next Layer

- Next layer: L0
- Key decision: whether exact deterministic omissions are rejected before any
  chain or Task Session request.
- Major deferred scope: upstream receipt hardening and governed lifecycle
  synchronization.
