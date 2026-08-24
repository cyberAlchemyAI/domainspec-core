# TASK-WCND-02 — Regenerate the pinned npm consumer at 0.15.9

- SWU: `SWU-WCND-002`
- Authorization: direct user request, `first regenerate the package version a new npm version is available`
- Selected artifact: `@vijayee/wavedb@0.15.9`
- Registry SHA-1: `0ab012ef85fb69bdb2aff54e65ddcb1fb10cd881`
- Registry SRI: `sha512-qoRqZUti9Rjs9UT4rj8cQKNv2Gdr8bJ25p6miU4dKojLeBMfzkgQqp+D/fd2PsaItXyhgMLrlx/wQUmyj/W8hA==`
- Runtime: Node `v26.6.0`, npm `11.18.0`, linux x64
- Result class: candidate-local opaque-artifact diagnostic

## Primary behavior

Create a new immutable consumer for the newest npm release, independently bind
the downloaded tarball to registry SHA-1/SRI before scripts, install/build it in
isolation, load the addon, and rerun the existing basic, empty-value,
batch/reopen, and 100-concurrent-write canaries.

## Exact write scope

- `ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/source-build/.work/wcnd-20260805-node26-02/**`
- `ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/source-build/npm-diagnostic/execution/npm-node26-0.15.9/**`
- `ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/source-build/npm-diagnostic/execution/task-sessions/SWU-WCND-002/**`
- `.arcanum/task-session/continuity/wavedb-npm-0-15-9.json`

## Done criteria

1. The three output roots are initially absent and the prior `0.15.8` attempt
   remains unchanged.
2. Registry identity and independently computed tarball SHA-1/SRI match exactly
   before any install script runs.
3. The packed manifest names version `0.15.9`, bundled C sources, and no
   prebuilt addon.
4. Attempt-local install/build completes within 180 seconds; one addon loads
   within 20 seconds.
5. Four canaries pass independently within 30 seconds each.
6. Scope audit finds no Craft-ledger, NVM-default, Git-history, publication, or
   deployment effect.
7. A terminal receipt records PASS or BLOCK without rewriting prior evidence.

## Claim ceiling

A pass proves only the exact `0.15.9` npm tarball under one local Node 26
environment and the named canaries. It does not prove source provenance,
fresh-process Craft snapshot reopen, Craft re-ingestion, API compatibility,
locking, recovery, deployment, or production readiness.
