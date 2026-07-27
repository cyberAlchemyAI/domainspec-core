# TASK-IFR-007: Isolated Installed-Consumer Proof

## Objective And Mapping

- Layer/slice: L3 / S-07.
- SWU: `SWU-IFR-007`.
- Goal: reproduce the complete accepted design in a generic isolated installed
  consumer without mutating the live repository Inventory.

## Dependencies

- Passing `SWU-IFR-006` receipt.

## Implementation Detail

Inputs:

- canonical runtime payload and manifest;
- generic legacy-plus-faceted consumer fixture;
- isolated temporary installation root.

Outputs:

- named acceptance receipts:
  - `package-relative-unrelated-cwd`;
  - `warning-delta-attribution`;
  - `deterministic-repeat-dry-run`;
  - `zero-mutation`;
- apply/failure, facet, sync, legacy, and boundary results;
- installed-consumer proof receipt.

Algorithm:

1. Create an isolated consumer root through the test harness.
2. Install the runtime through the manifest owner.
3. Change process CWD outside both canonical and consumer roots.
4. Run the four required acceptance classes.
5. Run identical/no-op, conflict, apply success, injected partial failure,
   faceted admission, mixed legacy projection, and sync drift fixtures.
6. Compare all expected receipt fields and all target digests.
7. Scan canonical/generated outputs for private absolute paths and private
   evidence strings.
8. Delete only the harness-owned temporary root.
9. Emit the immutable proof receipt; do not claim current live-repository
   readiness.

## Smallest Working Unit: SWU-IFR-007

- Primary behavior: prove the installed package satisfies the approved
  acceptance matrix.
- Independent acceptance boundary: one harness returns a closed proof over the
  complete installed contract without source implementation changes.
- Candidate children: individual acceptance cases.
- Split analysis: cases remain independent fixtures but the SWU owns only the
  final installed-consumer proof that joins them; no implementation code is
  changed here.
- Write scope:
  - `arcanum/arcana/inventory/test/installed-consumer.test.cjs`
  - `arcanum/arcana/inventory/test/fixtures/installed-consumer/`
  - `ops/development/2026-07-24-inventory-runtime-faceted-layout/work-pack/session-evidence/SWU-IFR-007/`
- Forbidden scope:
  - live `.arcanum/inventory/` consumer state
  - private evidence in `arcanum/`
- Done criteria:
  - four required acceptance receipts exist and reproduce;
  - all remaining SPEC acceptance criteria pass;
  - no live consumer bytes change;
  - boundary scan passes.
- Acceptance evidence: `inventory.installed-consumer-proof.v1`.
- Validation:

```sh
node --test arcanum/arcana/inventory/test/installed-consumer.test.cjs
```

- Execution owner: `sigil-development`.

## Closeout

Passing this unit unlocks only `TASK-IFR-VERIFY`.

