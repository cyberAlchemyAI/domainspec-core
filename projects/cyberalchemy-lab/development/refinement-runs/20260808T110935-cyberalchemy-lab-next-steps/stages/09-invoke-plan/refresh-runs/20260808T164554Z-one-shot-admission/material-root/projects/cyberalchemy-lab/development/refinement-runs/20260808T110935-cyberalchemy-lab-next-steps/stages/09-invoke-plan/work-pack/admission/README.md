# WP-CAL-TEN-L0 admission package

This directory freezes the plan-time contracts needed to audit the finite frontier `SWU-CAL-001` through `SWU-CAL-010`. It is an admission surface, not an execution surface.

## Artifacts

- `L0-EXECUTION-CONTRACTS.json` closes per-unit owner invocation, exact write partition, runtime, validation, receipts, successor, and stop behavior.
- `FINITE-FRONTIER-CONTRACT.json` closes the ten-unit controller boundary and action budget.
- `WPRA-CONFIG.json` is the Work Pack Readiness Audit v2 input.
- the three schemas close the admission, Task Session receipt, closeout receipt, and frontier shapes.
- `validate-admission.py` validates schema conformance, graph continuity, exact write algebra, runtime references, receipt paths, and the one-unit projection preservation rule.

## Owner split

`implementation-readiness` is the outer finite-frontier controller. `task-session-until-blocker` owns fresh-session admission/resumption. Task Session owns one SWU implementation and terminal receipt at a time. Invoke Refresh owns only closeout synchronization and the next one-unit projection. Decision Gate remains the future approval owner.

The `command` object for each SWU is a host-native capability invocation descriptor. It is not a shell subprocess. `validation_contracts` contain actual structured process `argv` and exact runtime bindings.

## Frozen boundary

The package does not select a unit, initialize chain state, bind direct execution intent, run Decision Gate, start Task Session, create material packages, mutate product files, promote authority, publish, deploy, commit, or push. `EXECUTION-ENTRY.json` remains the one-unit `SWU-CAL-001` projection and is excluded from this package's mutation inventory.
