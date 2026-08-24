# Invoke Refresh Report: Node 26 diagnostic retry

- Phase status: `pass`.
- Activation source: `direct-user`.
- Mutation mode: `apply-approved`.
- Handoff status: `ready` for `task-session:execute SWU-WCSB-003`.
- Toolchain target: Node `v26.6.0`, npm `11.18.0`.
- Attempt: `wcsb-20260805-node26-01`.

## Applied deltas

- Added one controlled-variable Node 26 diagnostic SWU and exact task contract.
- Added a separate serial retry dispatch; Dispatch Spec returns pass with zero
  blocks and flags.
- Updated Work Pack, Execution Pack, W0, traceability, and gap projection.
- Corrected two stale selectors: Execution Pack no longer points to SWU-WCSB-001,
  and completed TASK-WCSB-01 no longer says `Selected: yes`.

## Evidence boundaries

- The Node 22 attempt and blocker remain unchanged.
- The WaveDB source commit, package version, lockfile, build files, OpenSSL
  mode, and test set remain unchanged.
- Node 26 execution has not happened yet.
- No Craft, publication, deployment, production, or addon handoff effect occurred.

## Material gates

- Primary package:
  `wavedb-reviewed-source-build:node26-retry-20260805`, digest
  `e962126022d6f2bd3c695bd4abd1b53d9ac52acb11b510f25af2bc560a92b8f8`.
- Selector correction package:
  `wavedb-reviewed-source-build:node26-selector-fix-20260805`, digest
  `fe0979d316013e38a44486389459fbd1ae657a248129f47c7f42a91c002a473c`.
- Both material and handoff receipts pass owner, dependency, publication,
  exact-path, and digest gates.

The next owner is Task Session for exactly `SWU-WCSB-003`.
