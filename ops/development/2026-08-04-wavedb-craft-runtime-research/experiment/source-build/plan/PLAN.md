# Implementation Plan: reviewed-source WaveDB build

## Delivery boundary

Implement a deterministic local runner and validator, then execute exactly one
fresh source-build attempt. Preserve all source, dependency, toolchain, command,
addon, test, and side-effect identities in machine-readable receipts. Do not
modify the parent experiment until the build closes and a separate Invoke
Refresh consumes its receipt.

## Delivery slices

### Slice SB-A — executable build protocol

Implement the ignored-work-area policy, standard-library Python runner,
receipt schema, validator, and deterministic fixtures. The runner owns the
ordered command protocol but does not select substitute inputs or recover from
acceptance-critical failure.

### Slice SB-B — one observed source build

Run the protocol against the reviewed source commit and local pinned toolchain.
Emit source, dependency, generated-source, build, and test manifests plus one
terminal receipt. A passing receipt enables only the parent refresh decision.

## Dependency flow

```text
Design receipts
  -> SWU-WCSB-001 runner and validator
     -> joined closeout selects SWU-WCSB-002
        -> SWU-WCSB-002 source-build attempt
           -> joined closeout returns parent Invoke Refresh route
```

## Implementation decisions

1. Python standard library orchestrates commands and hashes so the runner has
   no pre-build dependency install.
2. `source-build/.work/` is ignored and each attempt directory must be absent
   before execution; there is no destructive reuse or cleanup.
3. Dependency materialization uses `npm ci --ignore-scripts --no-audit
   --fund=false` from the reviewed lockfile.
4. Build uses the reviewed `scripts/build.js` with `WAVEDB_OPENSSL=1` and
   `OPENSSL_ROOT=/usr`.
5. Upstream tests run through the installed Mocha directly to avoid the
   package's `npm test` rebuild side effect.
6. JSON receipts are written atomically inside the declared execution evidence
   directory, with the terminal receipt last.
7. Subprocess output is captured to bounded log files; secrets and environment
   dumps are not recorded.

## Validation strategy

- Static runner/schema/validator checks and deterministic pass/fail fixtures
  close SB-A.
- Exact source, submodule, lockfile, toolchain, generated-source, addon, test,
  canary, and scope checks close SB-B.
- Every check is acceptance-critical. Any missing/unavailable check is `BLOCK`.
- Descriptive duration and output size cannot turn a failed check into pass.
