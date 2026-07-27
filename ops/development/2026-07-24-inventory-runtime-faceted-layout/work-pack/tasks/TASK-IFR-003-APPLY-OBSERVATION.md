# TASK-IFR-003: Sequential Apply Observation

## Objective And Mapping

- Layer/slice: L2 / S-03.
- SWU: `SWU-IFR-003`.
- Goal: apply already-validated candidate bytes sequentially and report the
  exact observed success, write failure, or postwrite mismatch.

## Dependencies

- Passing `SWU-IFR-002` receipt.

## Implementation Detail

Inputs:

- admitted candidate JSON/Markdown bytes and expected digests;
- exact baseline target digests;
- apply mode.

Outputs:

- `applied`, `write-failed`, or `postwrite-digest-mismatch` receipt;
- attempted writes, observed changed paths, expected/actual digests;
- repair-required residue when success is not observed.

Algorithm:

1. Reconfirm target baseline digests immediately before write.
2. If they changed, block without writing.
3. Write the intended projections in the declared sequential order.
4. After each attempted write, record whether it returned or failed.
5. Re-read both target projections regardless of failure.
6. Compare actual digests with candidate digests.
7. Set `committed=true` only when both candidate digests are observed.
8. On any other outcome, set `committed=false`,
   `possible_partial_mutation=true`, and `repair_required=true`.
9. Never claim rollback, transaction, or atomic commit.

Failure injection:

- first write fails;
- second write fails after the first changes;
- external alteration produces postwrite mismatch.

## Smallest Working Unit: SWU-IFR-003

- Primary behavior: observe one sequential apply outcome.
- Independent acceptance boundary: success and both partial-failure shapes are
  distinguishable from observed bytes.
- Candidate children: success path; write failure; postwrite mismatch.
- Split analysis: all are variants of the same write-observation state machine
  and must share one precedence contract.
- Write scope:
  - `arcanum/arcana/inventory/bin/inventory`
  - `arcanum/arcana/inventory/lib/inventory-update.cjs`
  - `arcanum/arcana/inventory/test/append-apply.test.cjs`
  - `arcanum/arcana/inventory/test/fixtures/append-apply/`
- Done criteria:
  - baseline drift blocks before write;
  - applied means both exact candidate digests observed;
  - failure receipts expose possible partial mutation and repair route.
- Acceptance evidence: `inventory.append-apply-result.v1`.
- Validation:

```sh
node --test arcanum/arcana/inventory/test/append-apply.test.cjs
```

- Execution owner: `sigil-development`.
- Handoff: no live consumer state; use isolated fixture targets.

## Closeout

Passing this unit satisfies the apply dependency of `SWU-IFR-006`.

