---
module: wavedb-pinned-npm-diagnostic
version: candidate-local-1
status: completed-local-diagnostic
updatedAt: 2026-08-05
docType: work-pack
---

# WORK-PACK: WaveDB pinned npm diagnostic

## Control fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | one exact direct-user-authorized diagnostic |
| complexity | low | one task, one SWU, one local environment, no migration |
| outputMode | single-file | task and SWU detail remain reviewable here |
| executionPackRef | n/a | no multi-wave choreography |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` | L0-L3 decision boundaries |
| dispatchTechniqueTrace | `DISPATCH-TECHNIQUE-TRACE.md` | technique trace pass; full dispatch not required |
| distillValidationStatus | pass | Standard inline validation, two rounds |
| swuAtomicityStatus | pass | one artifact-verdict behavior |
| firstUnitNarrownessStatus | pass | exact pinned install plus named canaries is the minimum useful proof |
| closeoutSyncStatus | pass | one target and no successor |
| admissionTiming | selected-unit-at-task-session | live admission immediately before output writes |
| executionEntryState | closed-pass | exact SWU completed; no same-pack successor |
| allowedRoutesDigest | `899cc892c4e88c1dad2440db8d50075e803c48512cd2943fe72469367d2ae3e4` | exact `allowed-routes.json` bytes |
| activeLayerWindow | L0 | local opaque-artifact behavior only |
| selectedSWU | `none` | SWU-WCND-001 closed PASS; selection cleared |
| nativeMutationAdmission | closed-pass | execution-output-only admission consumed by terminal PASS |
| lastUpdatedAt | `2026-08-05T16:35:24Z` | SWU-WCND-001 terminal PASS |
| readinessProfile | pilot | candidate-local evidence only |

## Work-Pack execution policy

```yaml
executionPolicy:
  routePolicy: automatic-in-scope
  allowedRoutesRef: allowed-routes.json
  allowedRoutesDigest: 899cc892c4e88c1dad2440db8d50075e803c48512cd2943fe72469367d2ae3e4
  automaticDecisions:
    - internal-tool-selection
    - capability-owner-routing
    - reversible-local-default
    - fresh-task-session-resumption
  stopDecisions:
    - product-or-semantic-choice
    - scope-expansion
    - destructive-or-irreversible-effect
    - credentials-or-secret-access
    - network-effect-outside-exact-npm-registry-and-lockfile-dependencies
    - authority-promotion-publication-deployment
    - failed-acceptance-critical-validation
  scopeSource: exact-work-pack-and-captured-frontier
  validationPolicy: owner-gates-remain-mandatory

executionEntry:
  state: closed-pass
  selectedUnit: null
  routeId: null
  nextOwner: null
```

## Objective summary

- Objective: determine whether exact npm artifact `@vijayee/wavedb@0.15.8`
  installs, loads, and passes named black-box canaries under Node `v26.6.0`.
- Artifact identity: SHA-1 `107472e4634729de8533b68c351859ff496cc56e`
  and SRI `sha512-o4G13W9V1jIzKOVSETUeg3oFDJde8GDDUeFF/a0nOJ1/LR0cN6pPurtdUGb+9vssUeB0B7OYbtWT+mEgI+pMnQ==`.
- Attempt: `wcnd-20260805-node26-01`, fresh and single-use.
- Success: exact identity checks, install/build, addon load, basic operations,
  empty values, batch/reopen, and 100 concurrent writes all pass within external
  time bounds; scope checks pass; a terminal receipt binds every result.
- Claim ceiling: one pinned npm tarball on one local Linux x86_64 Node 26
  environment and only the named canaries.

## Execution result

- Result: PASS for the admitted npm-artifact diagnostic.
- Terminal evidence: [npm diagnostic receipt](../execution/npm-node26/npm-diagnostic-receipt.json)
  and [Task Session receipt](../execution/task-sessions/SWU-WCND-001/terminal-receipt.json).
- All identity, install/build, addon-load, basic, empty-value, batch/reopen,
  100-write concurrency, and scope gates passed.
- The npm and prior Node 26 source-build addons are byte-identical at SHA-256
  `cbd5ebdab82635cf95ced5b0d3d3b50de7c224a6d99ebc2aa1dad57afb2ea8c9`;
  their JavaScript wrapper text is also equal after line-ending normalization.
- Therefore this PASS supports isolated use of the pinned npm artifact for the
  named canaries, but it does not prove that a different package version fixed
  the prior full-suite stall. Test-process lifecycle or cross-test context
  remains a live explanation, not a proven root cause.
- Source provenance remains unresolved, the prior full-suite blocker remains
  preserved, and Craft integration/addon handoff remain unauthorized and absent.

## Source contracts

- [Decision](DECISION.md)
- [Planning context](context/CONTEXT-PACK.md)
- [Implementation layering](IMPLEMENTATION-LAYERING.md)
- [Distill validation](DISTILL-VALIDATION.md)
- [Provenance result](../../../execution/wp0-provenance/RESULT.md)
- [History reconstruction](../../../execution/wp0-provenance/HISTORY-RECONSTRUCTION.md)
- [Node 26 source-build terminal receipt](../../execution/task-sessions/SWU-WCSB-003/terminal-receipt.json)

## Delivery slice and task

| Slice | Task | Outcome | Layer | Gate | Status |
| --- | --- | --- | --- | --- | --- |
| S-WCND-01 | TASK-WCND-01 | one integrity-bound npm artifact verdict | L0 | closed-pass | completed |

### TASK-WCND-01: execute pinned npm diagnostic

- Objective: produce one exact black-box PASS or BLOCK observation.
- Dependencies: `DG-WCNPM-001` resolved; exact registry metadata unchanged;
  Node `v26.6.0` and npm `11.18.0` available.
- Network scope: exact npm metadata/tarball plus only dependencies resolved by
  the isolated install.
- Forbidden: alternate package/version/tarball; source checkout/substitution;
  Craft access; prior-attempt edits; NVM default change; credentials; cleanup;
  Git history; publication; deployment.

## SWU-WCND-001

- Primary behavior: install and black-box-test one exact opaque npm artifact.
- Independent acceptance boundary: one terminal receipt says PASS only when
  all identity, install, load, functional, concurrency, and scope gates pass;
  otherwise it says BLOCK at the first failed gate.
- Candidate child units: metadata fetch, tarball verification, native install,
  addon load, functional canaries, scope audit.
- Retained-boundary rationale: each child provides useful partial evidence but
  none independently answers whether the package works for the admitted local
  contract; the per-stage results remain separately visible inside the receipt.
- Execution owner: local Task Session; subagents none.
- Write scope:
  - `../.work/wcnd-20260805-node26-01/**`;
  - `execution/npm-node26/**`;
  - `execution/task-sessions/SWU-WCND-001/**`.
- Handoff note: use exact paths, exact integrity, exact Node/npm, external
  process timeouts, preserved residue, and zero Craft access.

## Ordered algorithm

1. Prove the attempt/evidence paths are absent and capture Craft, prior
   attempt, NVM-default, and Git baselines.
2. Require Node `v26.6.0` and npm `11.18.0` without changing the default alias.
3. Query exact registry metadata and require version, SHA-1, SRI, and tarball
   URL equality.
4. Download with `npm pack --ignore-scripts --json`, then independently hash
   the tarball and require SHA-1/SRI equality before any install script runs.
5. Inspect the packed `package.json`, file manifest, install script, and package
   name/version. Treat the tarball as the only artifact identity.
6. Create an isolated consumer and install only the local verified tarball
   under an external 180-second timeout; preserve lockfile, dependency tree,
   npm logs, native addon path/hash, and install result.
7. Require addon load under an external 20-second timeout.
8. Run attempt-local black-box harness modes under external 30-second timeouts:
   basic string/binary put/get, empty-string round trip, batch plus close/reopen,
   and the upstream-shaped 100-write `Promise.all` case with readback.
9. Stop on any failure or timeout. Terminate only the exact timed command's
   process group; record the signal/exit as controller-caused, not package
   crash proof.
10. Verify Craft paths, prior immutable evidence, NVM default, Git history,
    publication/deployment state, and all declared output paths.
11. Emit one terminal Task Session receipt and run exact closeout bookkeeping.

## Acceptance-critical validation

| Gate | Pass requirement |
| --- | --- |
| registry identity | exact name/version/SHA-1/SRI/tarball URL |
| tarball | independent SHA-1 and SHA-512/SRI match before scripts |
| toolchain | exact Node/npm plus preserved compiler/OpenSSL observation |
| install/build | local tarball install exit 0 within 180 seconds |
| addon | exactly one `wavedb.node`, hashed and loadable |
| basic | string and binary put/get match exact values |
| empty value | empty string round-trips as empty, not missing/null |
| batch/reopen | batch values survive close/reopen exactly |
| concurrency | 100 concurrent `put` promises and 100 reads complete within 30 seconds with exact values |
| scope | Craft, Node 22/26 source attempts, NVM default, Git history, publication, and deployment unchanged |
| receipt | terminal receipt binds inputs, commands, outputs, effects, and claim ceiling |

No unavailable or substitute gate counts as pass. A timed command produces
BLOCK and preserved residue.

## Task Session closeout synchronization contract

| SWU | Owner route | Terminal receipt | Target inventory | Baseline binding | Delta classes | Owner validation | Expected owner receipt | Successor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-WCND-001 | `invoke:refresh:apply-approved` | `execution/task-sessions/SWU-WCND-001/terminal-receipt.json` | `plan/WORK-PACK.md` only | Task Session preflight live SHA-256 and size | `evidence_added`, `blocker_opened`, `status_changed`, `route_changed` | terminal receipt parse/result, zero selected SWUs, exact evidence refs, scoped whitespace | `execution/task-sessions/SWU-WCND-001/invoke-refresh-receipt.json` | none; any Craft experiment requires a new direct decision |

Closeout is bookkeeping-only. It cannot execute another task, admit an addon,
change authority, publish, deploy, or clean residue.

## Distill validation

| Check | Result | Evidence |
| --- | --- | --- |
| smallest coherent unit | pass | one opaque-artifact verdict |
| atomicity/split analysis | pass | partial stages cannot establish final behavior |
| first-unit narrowness | pass | no Craft or repeatability work bundled |
| recomposition | pass | only informs a later decision |
| hidden critical gaps | pass | source provenance explicitly out of scope, not hidden |
| deferred complexity | pass | repeatability, security, packaging, Craft |
| navigation | pass | start here at `SWU-WCND-001` |

## Current state and stop conditions

- Current state: SWU-WCND-001 closed PASS; selection cleared; no same-pack successor.
- Exact provenance blocker: remains open for source-bound routes and does not
  disappear if this diagnostic passes.
- Stop at identity drift, install/build failure, addon mismatch/load failure,
  any canary failure/timeout, unexpected scope effect, or missing closeout.
- No retry or alternate package is implicit.

## Required links

- [Allowed routes](allowed-routes.json)
- [Decision](DECISION.md)
- [Technique trace](DISPATCH-TECHNIQUE-TRACE.md)
- [Distill validation](DISTILL-VALIDATION.md)
- [Layering](IMPLEMENTATION-LAYERING.md)

## Change log

| Date | Change | Author |
| --- | --- | --- |
| 2026-08-05 | SWU-WCND-001 passed all named npm-artifact gates; selection cleared without Craft handoff | Codex Invoke Refresh |
| 2026-08-05 | Initial one-SWU pinned npm diagnostic authorized by direct user | Codex Invoke Plan |
