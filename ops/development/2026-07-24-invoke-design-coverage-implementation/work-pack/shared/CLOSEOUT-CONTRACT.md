# Task Session Closeout Contract: Invoke Design Coverage

Every source SWU returns the shared result shape from `CONTEXT.md`, then invokes
the lifecycle owner’s approved synchronization route. The synchronization may
update only the exact private plan targets named below.

Common controls:

- baseline binding: live pre-write digests for every source and target path;
- allowed source deltas: only the SWU write scope;
- allowed plan deltas: `evidence_added`, `status_changed`,
  `blocker_opened`, `blocker_resolved`, `route_changed`;
- owner validation: task command set plus scoped `git diff --check`;
- expected owner receipt:
  `work-pack/session-evidence/<SWU>/closeout-receipt.json`;
- no success may infer promotion, publication, commit, push, or another SWU.

## SWU closeout rows

| SWU | Terminal source receipt | Exact synchronization targets | Successor |
| --- | --- | --- | --- |
| SWU-DVC-001 | fixture-denominator receipt with corpus digest | `WORK-PACK.md`, task 001, `work-pack/swu-manifest.json`, SWU-DVC-001 session evidence | SWU-DVC-002A |
| SWU-DVC-002A | manifest-schema receipt | `WORK-PACK.md`, task 002, manifest, SWU-DVC-002A evidence | SWU-DVC-002B |
| SWU-DVC-002B | denominator-schema receipt | `WORK-PACK.md`, task 002, manifest, SWU-DVC-002B evidence | SWU-DVC-002C |
| SWU-DVC-002C | selection-schema receipt | `WORK-PACK.md`, task 002, manifest, SWU-DVC-002C evidence | SWU-DVC-003 |
| SWU-DVC-003 | extractor receipt | `WORK-PACK.md`, task 003, manifest, SWU-DVC-003 evidence | SWU-DVC-004 |
| SWU-DVC-004 | validator receipt | `WORK-PACK.md`, task 004, manifest, SWU-DVC-004 evidence | SWU-DVC-005 |
| SWU-DVC-005 | fixture-runner receipt | `WORK-PACK.md`, task 005, manifest, SWU-DVC-005 evidence | SWU-DVC-006A |
| SWU-DVC-006A | Design-mode contract receipt | `WORK-PACK.md`, task 006, manifest, SWU-DVC-006A evidence | SWU-DVC-006B |
| SWU-DVC-006B | architecture-contract receipt | `WORK-PACK.md`, task 006, manifest, SWU-DVC-006B evidence | SWU-DVC-006C |
| SWU-DVC-006C | UX-contract receipt | `WORK-PACK.md`, task 006, manifest, SWU-DVC-006C evidence | SWU-DVC-006D |
| SWU-DVC-006D | root-evidence-contract receipt | `WORK-PACK.md`, task 006, manifest, SWU-DVC-006D evidence | SWU-DVC-006E |
| SWU-DVC-006E | aggregate-runner receipt | `WORK-PACK.md`, task 006, manifest, SWU-DVC-006E evidence | SWU-DVC-007 |
| SWU-DVC-007 | generated-parity receipt | `WORK-PACK.md`, task 007, manifest, SWU-DVC-007 evidence | SWU-DVC-008 |
| SWU-DVC-008 | live-proof receipt | `WORK-PACK.md`, task 008, manifest, SWU-DVC-008 evidence | VERIFY |

If the declared successor is not uniquely dependency-ready, the successor is
`none` and the work-pack must be refreshed before another execution handoff.
