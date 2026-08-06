# TASK-WCSB-02: execute and bind one source-built addon

## Execution status

- Status: `blocked`.
- Selection evidence: `../../../WORK-PACK.md` records SWU-WCSB-001 `pass`
  and SWU-WCSB-002 as the unique selected successor.
- Attempt: `wcsb-20260804-01`; no fallback attempt is admitted.
- Terminal receipt:
  `../../../execution/task-sessions/SWU-WCSB-002/terminal-receipt.json`.
- Blocker: `WCSB-UPSTREAM-CONCURRENT-WRITE-STALL`. Source, dependency,
  generated-source, native build, and addon-load stages passed; the first
  upstream Integration concurrent-write test did not complete. The addon has
  no handoff, and the canary/final scope stages are unrun.

## Objective and mapping

- Slice: S-WCSB-02.
- Layer/wave: L0 / W0.
- Objective: run the validated protocol once against the exact reviewed source
  and local pinned toolchain, then bind a loadable/tested addon into one
  terminal source-build receipt.

## Source contracts

- `../../../design/ARCHITECTURE.md#source-closure-algorithm`
- `../../../design/ARCHITECTURE.md#dependency-closure-algorithm`
- `../../../design/ARCHITECTURE.md#build-algorithm`
- `../../../design/ARCHITECTURE.md#verification-algorithm`
- `../shared/context.md`
- passed SWU-WCSB-001 terminal and owner receipts.

## SWU-WCSB-002

- Primary behavior: produce and verify one exact local source-built addon.
- Dependencies: SWU-WCSB-001 pass and closeout selection.
- Selected: no; the failed attempt has no same-pack successor.
- Write scope:
  - `experiment/source-build/.work/wcsb-20260804-01/**`;
  - `experiment/source-build/execution/source-build/**`;
  - `experiment/source-build/execution/task-sessions/SWU-WCSB-002/**`.
- Network scope: `https://github.com/vijayee/WaveDB.git` and only
  lockfile-declared npm dependency tarballs.
- Forbidden: alternate commit/lock/toolchain, source repair, real Craft access,
  parent plan mutation inside the task, package publication, deployment,
  destructive cleanup, credentials.

## Ordered execution

1. Capture absent target and exact controlling-file baselines.
2. Run the validated runner with attempt `wcsb-20260804-01`, commit
   `01c77e8b...`, OpenSSL enabled at `/usr`, and the declared output directory.
3. Require exact root/submodule/source/build-file manifest closure before
   dependency materialization.
4. Require `npm ci --ignore-scripts --no-audit --fund=false`, unchanged
   lockfile, and a complete resolved dependency manifest.
5. Run the reviewed copy-sources and build scripts; record complete `c_src`,
   toolchain, command, and addon identities.
6. Load the addon, run direct upstream Mocha tests, and run the empty-value
   temporary-store canary.
7. Run the independent receipt validator and workspace scope audit.
8. Write terminal Task Session evidence, then closeout through Invoke Refresh.

## Split analysis

Candidate children are source fetch, dependencies, generated source, build,
load, tests, and receipt. None can independently produce an admissible addon;
allowing an intermediate pass would create precisely the partial-artifact
false success the receipt prevents. They remain ordered stages of one primary
behavior.

## Done criteria and validation

- all exact source/submodule/lock/build/toolchain identities pass;
- `c_src` manifest exists and is complete;
- exactly one expected addon exists and its live SHA-256 matches the receipt;
- addon load, upstream tests, and empty-value canary pass;
- scope audit reports no forbidden effect;
- validator returns pass against live evidence;
- source-build terminal receipt states only the bounded local claim;
- terminal Task Session and joined closeout owner receipts exist.

Validation command:

```bash
python3 runtime/validate_source_build.py \
  --receipt execution/source-build/source-build-receipt.json \
  --source-build-root .
```

Execution owner: Task Session local. On pass, return the parent
`invoke:refresh:apply-approved` route; do not run it inside this SWU.
