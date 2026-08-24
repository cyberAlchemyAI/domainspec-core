# Execution Pack: WaveDB reviewed-source build

## Control fields

| Field | Value |
| --- | --- |
| planningGateStatus | pass |
| complexity | medium |
| baselineWave | W0 |
| activePlanRef | `WORK-PACK.md` |
| workPackManifest | `WORK-PACK.md` |
| layeringArtifact | `IMPLEMENTATION-LAYERING.md` |
| specRef | `../define/SPEC.md` |
| activeLayerWindow | L0 |
| selectedSWU | SWU-WCSB-003 |
| selectedAttempt | `wcsb-20260805-node26-01` |
| selectedToolchain | Node `v26.6.0`, npm `11.18.0` |
| readinessProfile | pilot |

## Choreography

```text
Original Dispatch/Distill/runner proof
  -> SWU-WCSB-002 Node 22 attempt (closed BLOCK, immutable)
     -> direct-user Invoke Refresh selects controlled Node 26 diagnostic
        -> Node 26 retry Dispatch validation
           -> SWU-WCSB-003 Task Session
              -> closeout owner joins with no same-pack successor
                 -> optional parent Invoke Refresh only on PASS
```

Only one SWU executes. No parallelization or subagent delegation is used. The
Node 26 attempt may compare against the Node 22 receipt but may not change it.
Each failure stops the route without implicit retry.

## Wave table

| Wave | Layer | Contents | Entry | Exit evidence | Status |
| --- | --- | --- | --- | --- | --- |
| [W0](work-pack/waves/W0-SOURCE-BUILD.md) | L0 | protocol, Node 22 observation, then selected Node 26 diagnostic | existing protocol pass plus retry dispatch pass | SWU-WCSB-003 terminal and joined closeout receipts | active-node26-diagnostic |
| [W1](work-pack/waves/W1-REPEATABILITY.md) | L1 | clean-build repeatability | separate L0 promotion decision | two fresh passing attempt receipts | deferred |
| [W2](work-pack/waves/W2-GOVERNANCE.md) | L2 | security/license governance | L1 promotion decision | owner receipts | deferred |
| [W3](work-pack/waves/W3-PACKAGING.md) | L3 | packaging/platform support | L2 promotion decision | package/publication receipts | deferred |

## Stop conditions

- Node is not exactly `v26.6.0` or npm is not exactly `11.18.0`;
- new attempt/evidence target already exists or a previous attempt changes;
- any source, submodule, lockfile, generated-source, build, load, test, canary,
  scope, receipt, or closeout validation failure;
- any request to substitute source, dependency, toolchain, or test inputs;
- any Craft or real-ledger access;
- any NVM default-alias mutation, publication, promotion, deployment,
  destructive cleanup, or production effect;
- any missing owner closeout receipt.
