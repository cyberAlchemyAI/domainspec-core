# TASK-RUNTIME — Prove and encapsulate snapshot reads

Layer/slice: L0 / S-RUNTIME. Source contracts: `DATA-MODEL.md` snapshot closure
and runtime boundary; passing and failed WaveDB receipts cited by the run.

## SWU-CAPI-001 — Fresh-process reader witness

- Primary behavior: a separately launched Node process opens the already closed
  sequential-write snapshot and verifies all 55 manifest-bound records.
- Independent boundary: pass/fail receipt needs no API code.
- Split analysis: process launch and byte verification are one claim; either
  alone cannot prove fresh-process reopen.
- Dependencies: pinned Node `v26.6.0`, npm `@vijayee/wavedb@0.15.8`, immutable
  copy of the existing successful experiment inputs.
- Write scope: `ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-ledger-import/execution/wcli-fresh-reader-01/` only.
- Done/evidence: child process exit 0; manifest plus 55 exact lengths/digests;
  environment and input hashes; source/store unchanged; JSON receipt.
- Validation: run the new builder and reader commands twice; JSON/schema check;
  compare pre/post store tree digests.
- Owner/handoff: `experiment-harness` inside one later authorized Task Session.

## SWU-CAPI-002 — Pure snapshot verifier

- Primary behavior: normalize supported reads and close every expected
  manifest-derived key under configured resource ceilings.
- Independent boundary: fixture tests return either one immutable snapshot model
  or one typed unavailable result, never partial data.
- Split analysis: parsing and expected-key verification share the one publish/no-
  publish decision and cannot pass independently.
- Dependencies: SWU-CAPI-001.
- Write scope: `implementation/domainspec/tools/craft-consultation-api/src/snapshot/`,
  `implementation/domainspec/tools/craft-consultation-api/test/snapshot/`.
- Done/evidence: expected closure, normalization boundaries, limits, extra-key
  unreachability, and same-snapshot binding tests pass.
- Validation: owner-selected package test command plus fixture digest manifest.
- Owner/handoff: bounded implementation helper or local Task Session.

## SWU-CAPI-003 — Runtime invalidation state

- Primary behavior: any post-open WaveDB read/type/digest anomaly invalidates one
  handle and all subsequent data reads return unavailable.
- Independent boundary: deterministic state-machine tests with no HTTP layer.
- Split analysis: anomaly detection without atomic invalidation is unsafe; kept
  together.
- Dependencies: SWU-CAPI-002.
- Write scope: the same `src/snapshot/` and `test/snapshot/` subtrees; execute
  sequentially with SWU-CAPI-002, never in parallel.
- Done/evidence: tamper/missing/exception fixtures close the handle once and never
  serve another record.
- Validation: state-transition and race-free fake-adapter tests.
- Owner/handoff: bounded implementation helper or local Task Session.

Synchronization: each SWU closes through `invoke:refresh:apply-approved`; no
successor begins from an unjoined or failed receipt.
