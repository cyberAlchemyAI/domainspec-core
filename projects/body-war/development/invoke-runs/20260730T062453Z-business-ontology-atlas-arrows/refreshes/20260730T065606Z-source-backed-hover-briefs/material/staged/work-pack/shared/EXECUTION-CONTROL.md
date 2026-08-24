# Execution And Closeout Control

## Selection And Preflight

Only one dependency-ready SWU may be selected. Context Builder must bind the
selected task, predecessor receipt, semantic locks from `WORK-PACK.md`, and
current SHA-256 for every declared write target. Existing files use their
current digest; planned new files use `absent`.

Any semantic-lock or write-target drift blocks mutation and routes to Invoke
Refresh. A Task Session may not absorb the drift.

## Common Execution Contract

1. Work only inside the selected SWU's write scope.
2. Preserve unrelated dirty worktree state.
3. Use generated-output commands rather than hand-editing generated HTML or
   receipts.
4. Run the task's exact validation plus scoped `git diff --check`.
5. Record commands, exit codes, changed paths, before/after digests, invariant
   counts, and blockers in the terminal receipt.
6. Never select or execute the successor automatically.

## Terminal Receipt Contract

The selected Task Session owns one terminal receipt at the exact path in the
successor ledger. Invoke Refresh validates the receipt before synchronizing the
Plan. Required fields are:

- `swu_id`, `result`, `capability_ref`, `receipt_kind`, and timestamp;
- selected task/SWU digest and predecessor-receipt digest;
- semantic-lock results;
- declared target inventory with preflight baseline (`sha256` or `absent`) and
  final digest;
- files touched and proof that no undeclared path changed;
- validation commands with exit code and output/evidence reference;
- blockers, residue, reroute, and handoff note;
- successor ID from this ledger or `none`;
- `authority_effect: none` and `release_admission: not-granted`.

A failed, incomplete, mismatched-owner, or schema-incomplete receipt cannot
change Work Pack state. Invoke Refresh may record the blocker only.

## Closeout Targets

Invoke Refresh may update only:

- this run's `WORK-PACK.md`;
- this run's `CONTINUATION.json`;
- `work-pack/closeout/<SWU-ID>.receipt.json`.

Allowed Plan-state deltas are `status_changed`, `evidence_added`,
`blocker_opened`, `blocker_resolved`, and `route_changed`. Refresh cannot
implement a successor, widen scope, change authority, promote, publish, deploy,
or clean unrelated files.

## Successor Ledger

| Unit | Expected closeout receipt | Successor |
| --- | --- | --- |
| `SWU-BWAA-001` | `work-pack/closeout/SWU-BWAA-001.receipt.json` | `SWU-BWAA-002` |
| `SWU-BWAA-002` | `work-pack/closeout/SWU-BWAA-002.receipt.json` | `SWU-BWAA-005` |
| `SWU-BWAA-005` | `work-pack/closeout/SWU-BWAA-005.receipt.json` | `SWU-BWAA-003` |
| `SWU-BWAA-003` | `work-pack/closeout/SWU-BWAA-003.receipt.json` | `SWU-BWAA-004` |
| `SWU-BWAA-004` | `work-pack/closeout/SWU-BWAA-004.receipt.json` | none |

The first closeout owner may create `work-pack/closeout/` only if absent and
must fail if a non-directory occupies that path. Existing receipts are never
overwritten.
