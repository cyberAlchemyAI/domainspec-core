---
title: Agent Consultation API Implementation Layering
status: draft-plan
updatedAt: 2026-08-03
owner: owner-selection-required:augmentor-consultation
scope: capability
---

# Agent Consultation API Implementation Layering

This is a non-executed implementation sequence. Layer 0 proves the contract
locally without exposing private data to the consumer product. Later layers
require their named owners and their own execution authorization.

## Context

- Target: read-only Agent Consultation API for Augmentor.
- Current state: designed, not implemented.
- Primary consumer: a host-owned answering agent.
- Primary constraint: useful evidence retrieval without acquiring source,
  reasoning, answer, memory, routing, authority, or execution ownership.
- Source references: `stages/06-design.md`, `stages/07-design-review.md`,
  `stages/08-distill-repair.md`, and `stages/08-question-scenarios.md`.

## Layering Method

- L0 proves the closed contract with a synthetic or target-local fixture.
- Each later layer answers one additional decision question.
- Every layer preserves read-only operation, source provenance, mechanical
  status, out-of-band identity, and untrusted-evidence handling.
- Promotion depends on executed evidence from the preceding layer.

## Layer Decision Table

| Layer | Decision question | Minimum working unit | Outcome | Risk reduced | Promotion decision |
| --- | --- | --- | --- | --- | --- |
| L0 | After this layer, we know whether one closed query can return bounded, source-linked evidence with fail-closed states over a deterministic fixture. | Schemas, fixtures, validator, neutral projection fixture, and `ConsultationBoundary` core. | Agents can exercise the contract locally without product or private-runtime integration. | Contract ambiguity, hidden reasoning, and leakage in the data shape. | Continue only when all 14 scenarios and invalid fixtures pass. |
| L1 | After this layer, we know whether ResonantOS can inject verified context and let an answering agent use the service without crossing owner boundaries. | Host adapter, approved projection, and answer-policy integration. | One host-backed question-to-evidence-to-answer or abstention witness. | Identity spoofing, host coupling, and answer-boundary risk. | Continue only after owner selection and an executed integration witness. |
| L2 | After this layer, we know whether access, freshness, cache isolation, limits, cancellation, and degraded modes remain correct under failure. | Policy fixtures, cache/cancellation controls, and failure tests. | Repeatable safe behavior under denied, stale, conflicting, oversized, and unavailable states. | Cross-scope leakage, stale claims, overload, and unsafe fallback. | Continue only after failure-injection and measurement receipts. |
| L3 | After this layer, we know whether an optional external transport and packaging can preserve the same contract. | HTTP wrapper or package boundary over the unchanged service. | A reusable transport without new semantics. | Protocol drift and packaging risk. | Package or pilot only after security, compatibility, and owner approval. |

## Capability Progression

| Area | L0 | L1 | L2 | L3 |
| --- | --- | --- | --- | --- |
| Query | `lookup`, `search`, `context` on fixture | same queries on approved projection | measured caps and failure behavior | optional additional typed operations |
| Identity | synthetic verified context supplied by tests | host-injected principal and policy | expiry, cancellation, denial, access-equivalence tests | external transport identity mapping |
| Projection | synthetic or target-local private fixture | owner-approved neutral consumer projection | rebuild, drift, and leakage hardening | packaged version negotiation |
| Answering agent | policy fixture only | host answering-agent integration | injection and degraded-mode tests | transport-neutral consumer guidance |
| Performance | no claim | local measurements | owner-approved service caps | pilot-scale evidence |

## Layer 0: Minimum Working Unit

### Goal

Prove one end-to-end contract without product integration:

```text
fixture question
  -> closed query
  -> verified test context
  -> deterministic fixture projection
  -> status-tagged evidence result
  -> test answer-policy decision
```

Before this path begins, SWU-ACAPI-000 makes the existing ontology regression
validator deterministic so the L0 exit check cannot pass or fail by concurrent
object-key insertion order.

### Included

- Query, response-union, evidence-statement, and projection-manifest schemas.
- Valid and invalid fixtures for all statuses and forbidden operations.
- Deterministic validator.
- Synthetic or target-local fixture projection with opaque IDs and leakage
  checks.
- Read-only consultation core for `lookup`, `search`, and `context`.
- Test-only answer-policy mapping and the 14 designed scenarios.
- Exact staged material, Task Session admission requests, terminal receipt
  contracts, and a seven-request finite-frontier chain.

### Deferred

- ResonantOS registration and real caller identity.
- Consumer projection of private bytes.
- Durable cache, distributed operation, HTTP, advanced query operations, UI,
  deployment, and release.

### Exit Evidence

- Closed schemas reject unknown fields and protected operations.
- All scenario fixtures pass deterministically.
- No returned payload contains a private path, undeclared field, embedded
  instruction role, write capability, or authority effect.
- Existing ontology validation passes deterministically across repeated runs.

### Promotion

- Continue when the contract is useful and fail-closed under all fixtures.
- Pivot when the answering agent needs data not representable as atomic evidence.
- Stop when the boundary cannot prevent private leakage or hidden reasoning.

## Layer Improvements

### L1 over L0

- Add the separately approved consumer projection and host adapter.
- Inject identity and policy outside model-visible arguments.
- Add one native tool and answer-policy integration.
- Preserve the exact L0 schemas and fail-closed variants.

### L2 over L1

- Add policy-depth, cache isolation, cancellation, deadline, drift, and failure
  injection.
- Measure candidate scans, joins, bytes, tokens, and latency before fixing caps.
- Preserve the L0/L1 read-only and non-reasoning guarantees.

### L3 over L2

- Add typed `traverse`, `compare`, or stored `explain` variants only if measured
  user need exists.
- Optionally add HTTP JSON as a transport wrapper.
- Add packaging and pilot evidence without changing service semantics.

## Wave Backbone

| Wave | Layer | Goal | Key artifacts | Verification |
| --- | --- | --- | --- | --- |
| W0 | L0 | Freeze and validate the contract. | schemas, fixtures, contract validator | candidate-local Node tests |
| W1 | L0 | Prove neutral projection and service core. | compiler fixture, reader, consultation service | contract, leakage, and scenario tests |
| W2 | L1-L2 | Integrate through host owners and harden failures. | host adapter, answer policy, access/cache/deadline tests | Vitest and end-to-end host fixture |
| W3 | L3 | Add optional operations or transport after evidence. | tagged operation variants or HTTP wrapper | compatibility and security tests |

## Non-regression Guardrails

- No model-visible credential or trusted identity field.
- No direct query over private files or arbitrary graph expressions.
- No response field that approves, recommends, writes, routes, reasons, or
  executes.
- Atomic claim provenance and compiler-manifest freshness remain mandatory.
- Retrieval relevance never becomes evidence confidence.
- Retrieved text remains untrusted data.
- Later transports call the same application service and preserve status
  semantics.

## Open Decisions

- Select the L0 candidate artifact owner before Task Session admission.
- Select production principal, policy, projection, and answer-policy owners
  before L1.
- Approve the neutral field allowlist before any consumer projection.
- Measure limits before selecting production defaults.

## Implementation Layering Result

- Target: Agent Consultation API.
- Artifact: `IMPLEMENTATION-LAYERING.md`.
- Mode: created.
- Layer count: 4.
- Recommended next layer: L0 after a separately admitted Task Session.
- Key decision unlocked by L0: whether the evidence-only contract works safely
  on deterministic fixtures.
- Major deferred scope: consumer integration, owner decisions, hardening, HTTP,
  deployment, and release.
- Validation: structure and plan linkage reviewed; no implementation tests run.
