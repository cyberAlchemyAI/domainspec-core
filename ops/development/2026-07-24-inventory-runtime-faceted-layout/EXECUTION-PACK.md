# Execution Pack: Inventory Runtime And Faceted Layout

## Control

| Field | Value |
|---|---|
| planningGateStatus | block-until-owner-integration |
| complexity | medium |
| baselineWave | W0 |
| workPackManifest | [WORK-PACK.md](WORK-PACK.md) |
| layeringArtifact | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) |
| specRef | [SPEC.md](SPEC.md) |
| activeLayerWindow | L0 |
| readinessProfile | pilot |

## Wave Board

| Wave | Question | Tasks/SWUs | Entry gate | Exit evidence |
|---|---|---|---|---|
| [W0](work-pack/waves/W0-OWNER-BASELINE.md) | Has the Inventory lifecycle owner accepted this delta and reconciled the active plan? | owner integration; no implementation SWU | explicit Sigil Development acceptance | accepted canonical target/write scopes |
| [W1](work-pack/waves/W1-L0-RECEIPT.md) | Is the receipt kernel byte-reproducible? | TASK-001 / SWU-001 | W0 pass | kernel receipt tests |
| [W2](work-pack/waves/W2-L1-DRY-RUN.md) | Is the full no-write transition attributable? | TASK-002 / SWU-002 | W1 pass | four dry-run evidence classes |
| [W3](work-pack/waves/W3-L2-APPLY-FACETS.md) | Are sequential writes visible and new facets conformant? | TASK-003, 004, 005 / SWU-003..005 | W2 pass | apply failure and facet projection receipts |
| [W4](work-pack/waves/W4-L3-PACKAGE-PROOF.md) | Is the runtime portable without consumer-state overwrite? | TASK-006, 007, VERIFY / SWU-006..007 | W3 pass | sync, installed proof, final audit |

## Ordering

- Execute one SWU at a time.
- W3 is sequential because SWU-003..005 share the append/projection engine.
- W4 consumer proof starts only after the complete managed runtime is frozen.
- No Task Session may bypass W0.

## Receipt Choreography

```text
owner acceptance
-> receipt kernel result
-> dry-run result
-> apply result + facet admission result
-> facet projection result
-> runtime sync result
-> installed consumer proof
-> final audit
```

Every arrow consumes an exact receipt reference. Missing, mismatched, flagged,
or blocked receipts stop the route.

