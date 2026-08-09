# Task Session Closeout Contract

Every SWU ends with two separate receipts:

1. a Task Session execution receipt under `projects/cyberalchemy-lab/development/execution-receipts/WP-CAL-TEN-L0/` proving exact touched files and validation;
2. an Invoke Refresh closeout receipt under this plan's `work-pack/receipts/` proving only synchronization of the Work Pack, parent task, wave, and next execution-entry projection.

The closeout route may change only status/evidence/blocker fields and the one-unit execution-entry projection and its regenerated `EXECUTION-ENTRY-VALIDATION.json`. It may not modify product bytes, design semantics, another SWU, authority, promotion, publication, deployment, or Git state.

## Baseline rule

Before product mutation, Task Session hashes the exact closeout target inventory. Existing targets bind their current SHA-256 and byte size. A future receipt target binds the explicit state `absent:create`. Any target drift before closeout blocks synchronization and routes to `invoke:refresh` review; it is not merged by inference.

## Allowed delta classes

- `status_changed`
- `evidence_added`
- `blocker_opened`
- `blocker_resolved`
- `route_changed`

No semantic task/SWU, write-scope, validation, dependency, or authority change is admitted by closeout.

## Closeout receipt shape

| Field | Required runtime value |
| --- | --- |
| `schema_version` | constant `cyberalchemy-lab.closeout-receipt/v1` |
| `work_pack_id` | constant `WP-CAL-TEN-L0` |
| `swu_id` | exact SWU ID from `CLOSEOUT-TARGETS.json` |
| `baseline_bindings` | one entry per exact target: path, `existing` or `absent:create`, pre-mutation SHA-256/byte size or explicit nulls for create |
| `execution_receipt` | exact immutable attempt path, current SHA-256, and terminal result `pass` |
| `execution_entry_projection` | exact successor (or complete) one-unit projection, route digest, and canonical projection digest; it remains verifiable after the live entry advances again |
| `admitted_delta_classes` | subset of the five closed classes above; `route_changed` is the only class that may replace the one-unit execution-entry projection with its unique successor |
| `changed_paths` | exact subset of the declared target inventory |
| `validation` | named closeout checks with terminal `pass` or `block` |
| `successor` | exact successor from `CLOSEOUT-TARGETS.json`, or null for CAL-010 |
| `authority_effect` | constant `none` |
| `status` | `pass` or `block` |

Task Session writes each terminal receipt at `attempt_receipt_root/<attempt-leaf>.json`; a path is derived from exactly one `attempt_id`, must never be overwritten, and a pre-existing legacy blocking receipt remains preserved at its historical path. Successor is deterministic only after a passing execution receipt and passing closeout validation. Invoke Refresh updates `EXECUTION-ENTRY.json` and regenerates `EXECUTION-ENTRY-VALIDATION.json` together; a failed acceptance-critical command blocks before successor projection. The last closeout emits the empty complete projection, not another selectable SWU.
