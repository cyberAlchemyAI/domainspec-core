# TASK-RUNTIME — Prove and encapsulate snapshot reads

Layer/slice: L0 / S-RUNTIME. Source contracts: `DATA-MODEL.md` snapshot closure
and runtime boundary; passing and failed WaveDB receipts cited by the run.

## SWU-CAPI-000 — Regenerate the immutable 0.15.9 Craft snapshot

- Primary behavior: create one new derived WaveDB snapshot with the verified
  npm `@vijayee/wavedb@0.15.9` tarball under Node `v26.6.0`, using sequential
  awaited puts and explicit close.
- Independent boundary: package identity, source inventory, 55-record manifest,
  immediate readback, same-process reopen, and input immutability close in one
  content-addressed pass/fail receipt with no API code.
- Split analysis: package canaries do not prove Craft ingestion, while a
  fresh-process reader cannot run until a version-matched snapshot exists; this
  is the smallest missing predecessor.
- Dependencies: diagnostic receipt SHA-256
  `6243febc06f345d0fa22b8b1210742c19e7d4cda74ca6a840e36f8d32428918c`,
  Task Session receipt SHA-256
  `eb07d1a14c4dacb30a272240057432c87f8acc430a6b064e0096f99e6107553c`,
  tarball SHA-256
  `e8156c107117c8bc7f3394ceb16dff439c87c0cb4f8991033dad960b13ae396f`,
  and the preserved 0.15.8 import receipt only as the input-scope baseline.
- Write scope:
  `ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-ledger-import/.work/wcli-20260805-node26-0.15.9-01/`
  and
  `ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-ledger-import/execution/wcli-20260805-node26-0.15.9-01/`
  only.
- Done/evidence: the exact manifest-bound 27-ledger scope produces 55 records;
  all lengths and SHA-256 values match immediately and after same-process
  reopen; source bytes are unchanged; dependency/tarball/addon identities and
  attempt paths are recorded. If the current source inventory differs from the
  preserved baseline, block and refresh the scope instead of silently changing
  counts.
- Validation: run the builder once in the immutable attempt; validate every
  JSON receipt; compare pre/post source inventories; prove no existing store,
  Craft ledger, NVM default, Git history, or public artifact changed.
- Owner/handoff: `experiment-harness` inside one later authorized Task Session.

## SWU-CAPI-001 — Fresh-process reader witness

- Primary behavior: after the SWU-CAPI-000 builder exits, a separately launched
  Node process opens only its already closed 0.15.9 snapshot and verifies all 55
  manifest-bound records.
- Independent boundary: pass/fail receipt needs no API code.
- Split analysis: process launch and byte verification are one claim; either
  alone cannot prove fresh-process reopen.
- Dependencies: accepted SWU-CAPI-000 receipt, its exact closed snapshot,
  pinned Node `v26.6.0`, and npm `@vijayee/wavedb@0.15.9` identities.
- Write scope: `ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-ledger-import/execution/wcli-fresh-reader-0.15.9-01/` only.
- Done/evidence: child process exit 0; manifest plus 55 exact lengths/digests;
  environment and input hashes; source/store unchanged; JSON receipt.
- Validation: launch two independent reader processes against isolated copies;
  JSON/schema check; compare pre/post source and store tree digests.
- Owner/handoff: `experiment-harness` inside one later authorized Task Session.

## SWU-CAPI-002 — Dependency-pinned pure snapshot verifier

- Primary behavior: bind the accepted runtime dependency and expose one pure
  adapter that normalizes supported core reads and closes every expected
  manifest-derived key under configured resource ceilings.
- Independent boundary: the dependency lock and fixture tests prove one exact
  runtime-backed snapshot model or one typed unavailable result, never partial
  data.
- Split analysis: the verifier cannot be reviewed against an unbound native
  runtime; the exact lock is an admission gate for this one adapter behavior,
  not a separate API feature.
- Dependencies: accepted SWU-CAPI-001 receipt, approved private root, Node
  `v26.6.0`, npm `@vijayee/wavedb@0.15.9`, exact tarball SRI/SHA-256, and the
  accepted native-addon SHA-256
  `4846a91117cfeaee42011e401e65448216d85c0ebd04fc860585e3a32e17bb3b`.
- Write scope: `implementation/domainspec/tools/craft-consultation-api/package.json`,
  `implementation/domainspec/tools/craft-consultation-api/package-lock.json`,
  `implementation/domainspec/tools/craft-consultation-api/src/snapshot/`, and
  `implementation/domainspec/tools/craft-consultation-api/test/snapshot/`.
- Done/evidence: the owner-selected manifest and lock bind the exact runtime;
  expected closure, normalization boundaries, limits, extra-key unreachability,
  and same-snapshot binding tests pass; no WaveDB writer or Subtree surface is
  reachable from the adapter.
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

Synchronization: SWU-CAPI-000 closes before SWU-CAPI-001 can be selected;
SWU-CAPI-001 closes before the runtime pin and SWU-CAPI-002 can be selected.
Every SWU closes through `invoke:refresh:apply-approved`; no successor begins
from an unjoined or failed receipt.
