# Runtime handoff — SWU-CAL-001 closeout contract drift

Session evidence only; this is not a canonical plan mutation.

## Identity

- Task/SWU: `TASK-CAL-CONTRACTS` / `SWU-CAL-001`
- Owner route: `invoke:refresh:apply-approved`
- Intended scope: the six `CLOSEOUT-TARGETS.json` entries for SWU-CAL-001 only.
- Result: `BLOCK` before staging or applying a closeout package.

## Obligation coverage

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| O1 | Task-local receipt scope agrees with the machine contract. | `TASK-CAL-CONTRACTS.md` lines 18-22 name the retired fixed receipt. | block |
| O2 | Work Pack closeout row agrees with the machine contract. | `WORK-PACK.md` lines 120-122 name the same retired fixed receipt. | block |
| O3 | Immutable terminal lineage is preserved. | `L0-EXECUTION-CONTRACTS.json#/units/0` requires an attempt-root template and preserves the legacy blocking receipt. | covered |
| O4 | The current Task Session attempt is valid. | Attempt receipt and terminal validation have result `pass`; the Node test passed. | covered |
| O5 | Closeout does not infer a semantic repair. | `WORK-PACK.md` lines 95-97 require stopping on prose/admission disagreement; `CLOSEOUT-CONTRACT.md` limits closeout deltas. | covered |

## Selected evidence

- `work-pack/tasks/TASK-CAL-CONTRACTS.md` — `SWU-CAL-001 / Write scope` — O1.
- `WORK-PACK.md` — `Task Session closeout synchronization contract / row 001` — O2.
- `WORK-PACK.md` — `Machine-normalized commands` — O5.
- `work-pack/admission/L0-EXECUTION-CONTRACTS.json` — `/units/0/terminal_receipt_template` and `/units/0/legacy_terminal_receipt` — O3.
- `work-pack/shared/CLOSEOUT-CONTRACT.md` — `Allowed delta classes` — O5.
- `projects/cyberalchemy-lab/development/execution-receipts/WP-CAL-TEN-L0/SWU-CAL-001/20260808T231500Z-a1.json` — exact current attempt — O4.
- `execution-runs/20260808T231500Z-l0-chain-controller-readmission/SWU-CAL-001/terminal-receipt-validation.json` — terminal validation — O4.

## Strict result

The artifact contract is contradictory: two canonical prose sources require a fixed path that is intentionally retained as immutable blocking history, while the admitted machine contract requires the fresh attempt-specific path. The specified closeout delta classes cannot repair that semantic mismatch. Stop before material package creation, closeout application, or successor projection.
