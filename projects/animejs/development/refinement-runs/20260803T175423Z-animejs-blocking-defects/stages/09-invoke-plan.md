# Stage 09 — Invoke Plan

## Plan status

`non_executed`. This plan does not authorize implementation, ontology construction, browsing, publication, or promotion.

## Work sequence

| Order | Work unit | Bounded output | Planned validation | Stop condition |
| --- | --- | --- | --- | --- |
| 1 | `SWU-AKV-NV-001` Query contract | Candidate QRY-003/QueryReceipt schema, validator, algorithm-version migration note, and eight fixtures. | Static closed-code check plus the eight terminal cases. | Any emitted code is undeclared or precedence/nullability is ambiguous. |
| 2 | `SWU-AKV-NV-002` Relation canonicalization | Decisions for the five `MERGE` rows and explicit exclusion of the three `DEFER` rows. | Equality-mismatch fixtures or one canonical representation per merge row. | A duplicate representation can diverge silently or a deferred edge is admitted. |
| 3 | `SWU-AKV-NV-003` Witness materialization | Executable baseline and one-mutant fixtures for the 17 retained rows. | Exactly 17 baseline/mutant comparisons with observable assertions. | Any retained relation has no discriminating runtime delta. |
| 4 | `SWU-AKV-NV-004` Candidate package review | Integrated candidate contract and validation receipts, still unpromoted. | Re-run closed-code, row-count, disposition, and mutation gates. | Any fixture fails or evidence is incomplete. |
| 5 | `SWU-AKV-NV-005` Ontology selection gate | A separately confirmed Ontology Vault decision on whether the validated candidate may be materialized/admitted. | Ontology Harness/Vault receipts appropriate to that future route. | Missing owner confirmation, authority crossing, or failed candidate validation. |

## First implementation slice

`SWU-AKV-NV-001` is the nearest bounded slice because it eliminates the undeclared-code defect without entangling graph serialization. It must still carry all query findings—tie mapping alone is insufficient.

## Dependencies

- Work units 2 and 3 depend on the 25-row planned matrix.
- Work unit 4 depends on passing execution receipts from 1–3.
- Work unit 5 depends on a separately confirmed ontology route and must not infer authority from Refine.

## Rollback and failure routing

All future implementation should remain candidate-local until acceptance. A failed fixture restores the previous candidate bytes, preserves the failing receipt, and routes back to the owning design decision. Historical query receipts are never rewritten. Closed research artifacts are never used as rollback targets.

## Required next authorization

Execution requires a new bounded Task Session or equivalent governed implementation route. Ontology creation requires the later Ontology Vault/Harness owner and explicit confirmation.
