# TASK-WCSB-03: diagnose the source build on Node 26

## Execution status

- Status: `selected`.
- Direct authorization: user request `update to node 26` on 2026-08-05.
- Attempt: `wcsb-20260805-node26-01`; reuse and fallback attempts are forbidden.
- Toolchain delta: Node `v26.6.0` and npm `11.18.0` only.
- Source identity: WaveDB `0.15.8` at
  `01c77e8b70f71de9b72480e73a3a179f6e93a009`.
- Prior evidence: SWU-WCSB-002 remains blocked under Node `v22.12.0`; its
  attempt, receipts, logs, and addon are immutable inputs, not retry outputs.

## Objective and mapping

- Slice: S-WCSB-03.
- Layer/wave: L0 / W0.
- Objective: run the validated protocol once under the exact Node 26
  toolchain to determine whether the concurrent-write stall reproduces.
- Claim ceiling: one local Linux x86_64 Node 26 diagnostic observation.

## Source contracts

- `../../../design/ARCHITECTURE.md#source-closure-algorithm`
- `../../../design/ARCHITECTURE.md#dependency-closure-algorithm`
- `../../../design/ARCHITECTURE.md#build-algorithm`
- `../../../design/ARCHITECTURE.md#verification-algorithm`
- `../shared/context.md`
- passed SWU-WCSB-001 protocol receipt;
- blocked SWU-WCSB-002 terminal receipt as comparison evidence;
- `../../../execution/refreshes/20260805T153202Z-node26-retry/context/CONTEXT-PACK.md`.

## SWU-WCSB-003

- Primary behavior: execute the unchanged reviewed-source protocol under one
  exact Node 26 toolchain and bind the result.
- Dependencies: SWU-WCSB-001 pass; SWU-WCSB-002 terminal block preserved;
  Node 26 retry dispatch pass; Invoke Refresh owner receipt selecting this SWU.
- Selected: yes.
- External setup scope: install Node `v26.6.0` through the existing user-local
  NVM only when absent; do not change the NVM default alias.
- Repository write scope:
  - `experiment/source-build/.work/wcsb-20260805-node26-01/**`;
  - `experiment/source-build/execution/source-build-node26/**`;
  - `experiment/source-build/execution/task-sessions/SWU-WCSB-003/**`.
- Network scope: official Node distribution through NVM,
  `https://github.com/vijayee/WaveDB.git`, and lockfile-declared npm tarballs.
- Forbidden: editing or cleaning either prior attempt; alternate source,
  lockfile, build file, OpenSSL mode, or toolchain; source repair; real Craft
  access; parent plan mutation inside the task; publication; deployment;
  destructive cleanup; credentials; changing the user's NVM default alias.

## Ordered execution

1. Prove the new attempt and evidence paths are absent and capture all live
   plan/runtime baselines.
2. Install or select Node `v26.6.0` through NVM and require npm `11.18.0`.
3. Re-run the unchanged validated runner with attempt
   `wcsb-20260805-node26-01`, evidence `execution/source-build-node26`, the
   reviewed commit, OpenSSL `/usr`, and exact existing build-file digests.
4. Require source, recursive submodule, dependency, generated-source,
   compilation, addon-cardinality, and addon-load gates.
5. Run the same direct upstream Mocha test set. Stop at its bounded command
   timeout or any earlier failure; do not kill or retry outside the runner.
6. Only after upstream pass, run the empty-value canary, scope audit, and
   independent terminal receipt validator.
7. Write terminal Task Session evidence and close out through Invoke Refresh.

## Split analysis

This is one controlled-variable experiment. Installation, compilation, load,
tests, canary, and receipt cannot independently establish Node 26 compatibility;
they remain ordered acceptance stages of one exact attempt.

## Done criteria and validation

- Node reports exactly `v26.6.0` and npm reports exactly `11.18.0`;
- all source, submodule, lockfile, build-file, Python, GCC/G++, Make, linker,
  and OpenSSL identities match the task contract;
- exactly one addon exists and its live hash matches the receipt;
- addon load, upstream tests, empty-value canary, and scope audit pass;
- validator passes the live terminal source-build receipt;
- no previous attempt, Craft path, Git history, publication, deployment, or
  NVM default alias changes;
- terminal Task Session and joined closeout owner receipts exist.

Validation command on a passing run:

```bash
python3 runtime/validate_source_build.py \
  --receipt execution/source-build-node26/source-build-receipt.json \
  --source-build-root . \
  --expected-source-commit 01c77e8b70f71de9b72480e73a3a179f6e93a009 \
  --expected-lockfile-sha256 26fbf0839106a0521f1ad6785764cefa3d39aedd9ff8412c982689c09b109f95
```

Execution owner: Task Session local. A pass returns a separate parent Invoke
Refresh route; a block preserves the exact new residue and returns no addon.
