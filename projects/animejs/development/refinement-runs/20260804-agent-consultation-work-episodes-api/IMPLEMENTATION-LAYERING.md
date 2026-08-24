---
module: animejs-agent-knowledge-api
version: candidate-0.1.0
status: planned-not-executed
updatedAt: 2026-08-04
docType: implementation-layering
---

# Implementation Layering

The active target is candidate-local:
`projects/animejs/ontology/agent-knowledge-vault/operational/`. It must not
create canonical ontology facts, modify current source manifests, or choose a
consumer transport.

| Layer | Question answered | Planned material | Promotion evidence | Explicitly outside |
| --- | --- | --- | --- | --- |
| L0 | Are the API vocabulary, projection allowlist, and episode transition rules closed and mechanically falsifiable? | contracts, code tables, fixtures, pure transition oracle | schema negatives, transition matrix, zero canonical-write assertion | durable service, host adapter |
| L1 | Can accepted commands be recorded and deterministically projected without corrupting or rewriting history? | atomic journal port, idempotency recovery, reducer, isolated overlay compiler | crash/retry, stale-writer, digest-chain, replay, quarantine, version-upgrade tests | external host integration |
| L2 | Can a local agent host consult and append through disjoint capability boundaries? | consultation service, episode service, evidence/context resolvers, capability adapters, integrated validator | cross-capability, cross-principal, evidence-rebinding, leakage, degraded-state tests | non-loopback transport, production retention |
| L3 | Should a consumer package, HTTP route, deployment, or verified-Lesson review be added? | none in this Work Pack | separate owner decision, threat model, retention policy, deployment and product evidence | all current implementation SWUs |

## Layer invariants

- L0 fixes data and transition meaning before storage code.
- L1 treats events as canonical only for episode history; every snapshot and
  overlay is rebuildable and version-keyed.
- L2 obtains identity, capability, context, evidence, and policy from host
  ports. Model payloads cannot supply or widen them.
- No layer changes Task state, assesses general truth, writes canonical vault
  nodes/relations, or creates verified Lessons.
- L3 cannot be inferred from successful candidate-local tests.

## Promotion gates

1. L0 → L1: closed schemas and every invalid transition fixture pass.
2. L1 → L2: repeated replay is byte-identical; crash/idempotency and
   gap/fork/quarantine fixtures pass; canonical graph delta is zero.
3. L2 → L3 consideration: all thirty scenarios pass in the integrated local
   harness and owner/security gaps are explicitly decided.
4. L3 remains a new Work Pack; this package cannot promote, release, deploy,
   or select transport.

## Deferred decisions

- transactional store technology beyond the required compare-and-append port;
- retention periods and deletion policy;
- non-loopback authentication, TLS, network allowlisting, and rate limits;
- consumer repository integration;
- candidate-Lesson extraction and verified-Lesson admission.

