---
module: craft-consultation-api
version: current
status: candidate
updatedAt: 2026-08-05
docType: implementation-layering
---

# Implementation Layering: Craft Consultation API

## Target and scope

- Target: private read-only API over a verified derived Craft snapshot
- State: designed, not implemented
- Candidate private root: `implementation/domainspec/tools/craft-consultation-api/`
- Source authority: owner `.craft/ledger.yml`; API and WaveDB are derived

## Layer decision table

| Layer | Decision question | Minimum working unit | Included | Deferred | Exit evidence | Promotion |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | After this layer, do exact, authorized, manifest-bound raw reads work without write authority? | Fresh-process snapshot witness plus fixture-backed status/catalog/raw HTTP slice | verifier, opaque IDs, auth ports, status/spaces/raw, ceilings, runtime invalidation | rows, search, refresh, replacement, recovery, deployment | unit/contract tests, separate-process receipt, read-only negative tests | continue only if all close |
| L1 | After this layer, are family-scoped normalized rows repeatable? | One validated 0.3.0 adapter and rows endpoint | pure adapter, unique IDs, references, row cursors | 0.2/0.1 until separate fixtures; search | fixture hashes, adapter tests, row auth/concealment tests | add adapters individually or stop |
| L2 | After this layer, do operational safety and degraded modes hold? | Adversarial concurrency/corruption environment harness | no-overlap publication contract, multi-reader/lock/corruption tests | automatic replacement/recovery | environment matrix and failure receipts | remediate or design replacement |
| L3 | After this layer, is packaging/deployment credible? | Owner-approved private package and deployment proof | auth provider, OS sealing, observability, recovery/replacement if approved | public promotion and source writes | owner approvals, deployment acceptance, audit | pilot or defer |

## Non-regression guardrails

- Every layer keeps source-ledger authority and `authority: derived` transport.
- No later layer introduces request-triggered mutation, refresh, promotion, or
  shared-cache authorization reuse.
- A newer adapter cannot silently reinterpret an older schema.
- Failure in an expected record or runtime read invalidates the whole snapshot.
- The atomic-batch write path remains forbidden until independent upstream
  evidence changes that decision.

## Recommended next layer

L0, beginning with the separately launched reader witness. This is the narrowest
reversible test of the runtime assumption the API would depend on. Mutation is
still blocked until the Work Pack's owner prerequisites and a new execution
authorization are satisfied.
