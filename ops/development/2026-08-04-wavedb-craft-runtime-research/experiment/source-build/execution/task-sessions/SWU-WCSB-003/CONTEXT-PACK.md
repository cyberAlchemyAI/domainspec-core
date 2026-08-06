# Context Pack: SWU-WCSB-003

- Mode: fresh Task Session, local Codex runtime, strict coverage.
- Work Pack: `plan/WORK-PACK.md`.
- Selected unit: `SWU-WCSB-003` / `TASK-WCSB-03`.
- Authorization: direct user request `update to node 26`, normalized by the
  passing Invoke Refresh owner receipt.
- Objective: execute the unchanged reviewed-source WaveDB protocol once under
  Node `v26.6.0` and npm `11.18.0`.
- Source: `https://github.com/vijayee/WaveDB.git`, commit
  `01c77e8b70f71de9b72480e73a3a179f6e93a009`, package version `0.15.8`.
- Attempt: `wcsb-20260805-node26-01`; attempt and evidence paths are absent.
- Comparison: SWU-WCSB-002 remains a Node 22 `BLOCK`; no bytes in that attempt
  may be edited, deleted, or reused.
- Toolchain delta: install/select exact Node `v26.6.0` with existing NVM
  `0.40.1`; require bundled npm `11.18.0`; preserve NVM default alias `22`.
- Other toolchain pins: Python `3.12.3`, GCC/G++ `13.3.0`, Make `4.3`,
  binutils `2.42`, OpenSSL enabled at `/usr`.
- Repository outputs: `.work/wcsb-20260805-node26-01`,
  `execution/source-build-node26`, and the terminal SWU receipt.
- External setup effect: user-local NVM may create
  `/home/vrondelli/.nvm/versions/node/v26.6.0`; no default alias change.
- Forbidden: source/lock/build/test substitution; previous-attempt mutation;
  source repair; Craft access; workspace Git mutation; publication; deployment;
  credentials; destructive cleanup; implicit retry.
- Closeout owner: `invoke:refresh:apply-approved`, bookkeeping-only over the
  six declared planning projections.
- Claim ceiling: one local Linux x86_64 Node 26 diagnostic observation.

All toolchain, source, dependency, generated-source, build, load, upstream
test, canary, evidence, scope, previous-attempt, and NVM-default checks are
acceptance-critical. There is no fallback attempt or accepted substitute.
