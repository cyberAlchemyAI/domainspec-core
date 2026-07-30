# Task Session Closeout Sync Contract

## Common Contract

Every SWU terminal receipt validates structurally against
`TASK-SESSION-RECEIPT.schema.json` and semantically against
`validate-task-session-receipt.py`. A Task Session terminal receipt is not an
Invoke Refresh owner receipt; each keeps its own identity and owner.

Invoke Refresh may update only:

- this run's `WORK-PACK.md`;
- this run's `CONTINUATION.json`;
- `work-pack/closeout/<SWU-ID>.receipt.json`;
- the exact terminal Task Session receipt and declared SWU files.

Baseline: SHA-256 of every declared target at preflight, with absent planned
files bound as `absent`. Allowed owner deltas:
`evidence_added`, `blocker_opened`, `blocker_resolved`, `status_changed`, and
`route_changed`. Refresh cannot implement another SWU, change authority,
promote, publish, deploy, clean unrelated files, or infer targets.

## Successor Ledger

The "inventory" column summarizes the exact file lists in the task contract;
those linked lists, not prose inference, are authoritative.

| Unit | Inventory | Expected closeout receipt | Successor |
| --- | --- | --- | --- |
| 001 | generator + fixture JSON + fixture test | `work-pack/closeout/SWU-OFSP-001.receipt.json` | 002 |
| 002 | overlay lock/manifest + admission test | `work-pack/closeout/SWU-OFSP-002.receipt.json` | 003 |
| 003 | materializer + test | `work-pack/closeout/SWU-OFSP-003.receipt.json` | 004 |
| 004 | handle schema + verifier + test | `work-pack/closeout/SWU-OFSP-004.receipt.json` | 005 |
| 005 | types/literal join/test + overlay bindings | `work-pack/closeout/SWU-OFSP-005.receipt.json` | 006 |
| 006 | tour projector/test + overlay bindings | `work-pack/closeout/SWU-OFSP-006.receipt.json` | 007 |
| 007 | reducer focus/serializer/test + overlay bindings | `work-pack/closeout/SWU-OFSP-007.receipt.json` | 008 |
| 008 | reducer portal/serializer/test + overlay bindings | `work-pack/closeout/SWU-OFSP-008.receipt.json` | 009 |
| 009 | patch 0002 + store bridge test + bindings | `work-pack/closeout/SWU-OFSP-009.receipt.json` | 010 |
| 010 | patch 0003 + renderer test + bindings | `work-pack/closeout/SWU-OFSP-010.receipt.json` | 011 |
| 011 | patch 0004 + landmark test + bindings | `work-pack/closeout/SWU-OFSP-011.receipt.json` | 012 |
| 012 | patch 0005 + relation-control test + bindings | `work-pack/closeout/SWU-OFSP-012.receipt.json` | 013 |
| 013 | patch 0006 + focus/motion test + bindings | `work-pack/closeout/SWU-OFSP-013.receipt.json` | 014 |
| 014 | new verified L0 build attempt | `work-pack/closeout/SWU-OFSP-014.receipt.json` | 015 |
| 015 | browser validator/schema/test | `work-pack/closeout/SWU-OFSP-015.receipt.json` | 016 |
| 016 | new L0 browser attempt | `work-pack/closeout/SWU-OFSP-016.receipt.json` | 017 |
| 017 | one-hop projector/dispatcher/test + bindings | `work-pack/closeout/SWU-OFSP-017.receipt.json` | 018 |
| 018 | pure tour reducer/test + bindings | `work-pack/closeout/SWU-OFSP-018.receipt.json` | 019 |
| 019 | patch 0007 + tour bridge test + bindings | `work-pack/closeout/SWU-OFSP-019.receipt.json` | 020 |
| 020 | patch 0008 + literal-surface test + bindings | `work-pack/closeout/SWU-OFSP-020.receipt.json` | 021 |
| 021 | patch 0009 + forced-colors test + bindings | `work-pack/closeout/SWU-OFSP-021.receipt.json` | 022 |
| 022 | new verified L1 build attempt | `work-pack/closeout/SWU-OFSP-022.receipt.json` | 023 |
| 023 | new L1 browser regression attempt | `work-pack/closeout/SWU-OFSP-023.receipt.json` | 024 |
| 024 | pure degraded policy/test + bindings | `work-pack/closeout/SWU-OFSP-024.receipt.json` | 025 |
| 025 | patch 0010 + degraded UI/browser tests + bindings | `work-pack/closeout/SWU-OFSP-025.receipt.json` | `TASK-VERIFY` |
| `TASK-VERIFY` | completion verification only | `work-pack/closeout/TASK-VERIFY.receipt.json` | `TASK-AUDIT-ALIGNMENT` |
| `TASK-AUDIT-ALIGNMENT` | spec/design/code/evidence audit only | `work-pack/closeout/TASK-AUDIT-ALIGNMENT.receipt.json` | `TASK-AUDIT-LAYERING` |
| `TASK-AUDIT-LAYERING` | owner/layer/authority audit only | `work-pack/closeout/TASK-AUDIT-LAYERING.receipt.json` | 026 |
| 026 | guide + prototype schema + new reproduction attempt | `work-pack/closeout/SWU-OFSP-026.receipt.json` | none |

Full closure task contracts live at
`../tasks/TASK-CLOSURE.md`. They use the same terminal schema with their exact
ID in `unit_id`, have no source/material write scope, and cannot repair
findings. Their only write is the declared closeout receipt.

`work-pack/closeout/` may be absent before execution. The first admitted
closeout owner creates it atomically, fails if a non-directory occupies the
path, never overwrites an existing receipt, and records creation or reuse in
its terminal receipt.
