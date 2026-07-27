# TASK-IFR-002: No-Write Append Transition

## Objective And Mapping

- Layer/slice: L1 / S-02.
- SWU: `SWU-IFR-002`.
- Goal: compute one complete baseline-to-candidate append receipt with zero
  filesystem mutation from any working directory.

## Source Contracts

- [SPEC command/state contract](../../SPEC.md#command-contract)
- [Architecture append workflow](../../ARCHITECTURE.md#append)
- `SWU-IFR-001` receipt kernel
- Existing canonical validator pair under
  `arcanum/arcana/inventory/scripts/`

## Dependencies

- Passing `SWU-IFR-001` receipt.

## Implementation Detail

Inputs:

- record JSON;
- explicit timestamp;
- installed Inventory root resolved from executable path;
- exact baseline `index.json` and `index.md`;
- complete validator bundle.

Outputs:

- `dry-run-ready`, `identical-no-op`, or a prewrite block receipt;
- staged candidate bytes/digests;
- structured warning delta;
- unchanged filesystem digest inventory.

Algorithm:

1. Parse exactly one mode and require `--json`.
2. Resolve runtime root from the executable and verify required helper members.
3. Read exact baseline bytes and record their digests.
4. Run the full baseline validator.
5. Normalize the record in canonical field order.
6. If ID exists, compare normalized content; return no-op or conflict.
7. Otherwise stage candidate JSON and Markdown in memory or a temporary
   directory outside consumer targets.
8. Run the full candidate validator.
9. Derive warning IDs as
   `sha256(code + NUL + subject + NUL + selector)`.
10. Compute introduced, resolved, and inherited sets in bytewise order.
11. Build the receipt through the L0 kernel.
12. Re-read consumer target digests and prove zero mutation.

Failure precedence:

```text
tooling-unavailable
> baseline-blocked
> invalid-request
> identical-no-op | id-conflict
> candidate-blocked
> dry-run-ready
```

Edge cases:

- caller CWD is unrelated;
- one validator helper is missing or has a wrong digest;
- baseline already contains warnings;
- one candidate warning is new;
- ID exists with reordered input keys but equal normalized content;
- candidate Markdown has no valid target table.

## Smallest Working Unit: SWU-IFR-002

- Primary behavior: compute a complete mutation-free append transition.
- Independent acceptance boundary: one canonical receipt explains exact
  baseline/candidate/warning state and target bytes remain unchanged.
- Candidate children: root resolution; validator calls; identity comparison;
  warning delta; CLI.
- Split analysis: each helper is independently testable, but only their joined
  result closes the Inventory-domain no-write transition.
- Write scope:
  - `arcanum/arcana/inventory/bin/inventory`
  - `arcanum/arcana/inventory/lib/inventory-update.cjs`
  - `arcanum/arcana/inventory/test/append-dry-run.test.cjs`
  - `arcanum/arcana/inventory/test/fixtures/append-dry-run/`
- Done criteria:
  - unrelated-CWD package resolution passes;
  - clean and one-new-warning deltas are exact;
  - repeated receipts are byte-identical;
  - all dry-run/no-op/block cases prove zero mutation.
- Acceptance evidence: `inventory.append-dry-run-result.v1`.
- Validation:

```sh
node --test arcanum/arcana/inventory/test/append-dry-run.test.cjs
```

- Execution owner: `sigil-development`.
- Handoff: return named receipt fixtures and before/after filesystem digests.

## Closeout

Passing this unit makes `SWU-IFR-003` and `SWU-IFR-004` dependency-ready but
does not select them together.

