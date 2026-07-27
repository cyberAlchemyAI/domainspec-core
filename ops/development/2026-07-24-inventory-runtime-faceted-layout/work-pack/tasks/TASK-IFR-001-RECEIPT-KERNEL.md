# TASK-IFR-001: Canonical Receipt Kernel

## Objective And Mapping

- Layer/slice: L0 / S-01.
- SWU: `SWU-IFR-001`.
- Goal: produce one schema-valid, byte-reproducible operation receipt from
  canonical inputs without reading or writing Inventory state.

## Source Contracts

- [SPEC receipt/invariants](../../SPEC.md#invariants)
- [Architecture receipt emitter](../../ARCHITECTURE.md#3-low-level-component-view)
- Accepted research `findings.md#required-receipt-schema`

## Dependencies And Blockers

- Dependency: Sigil Development closes `B-OWNER-INTEGRATION`.
- No implementation dependency.
- Stop if canonical source placement differs from the write scope below.

## Implementation Detail

Inputs:

- structured receipt body without `receipt_sha256`;
- caller-supplied `timestamp_input`;
- exact operation input and helper digests.

Outputs:

- canonical UTF-8 JSON bytes with newline;
- `operation_fingerprint`;
- `receipt_sha256`;
- schema validation result.

Algorithm:

1. Reject unknown or missing required receipt fields.
2. Normalize objects to schema-defined key order and arrays to their
   contract-defined order.
3. Serialize with deterministic JSON encoding and no implicit timestamps.
4. Compute `operation_fingerprint` from canonical operation inputs.
5. Compute receipt bytes excluding `receipt_sha256`.
6. Compute and insert `receipt_sha256`.
7. Serialize final bytes and append exactly one newline.
8. Repeat over identical inputs and compare bytes.

Edge/failure cases:

- unknown field;
- missing timestamp input;
- non-relative path;
- invalid digest;
- unstable array order;
- receipt digest accidentally includes itself.

## Smallest Working Unit: SWU-IFR-001

- Primary behavior: canonicalize and digest one operation receipt.
- Independent acceptance boundary: two calls with identical canonical inputs
  produce identical bytes and valid hashes; malformed inputs fail without
  state access.
- Candidate children: schema only; serializer only; digest tests only.
- Split analysis: none of the children independently proves a usable canonical
  receipt, so the kernel remains one coherent unit.
- Source anchors: SPEC invariants 1, 9, 10; architecture receipt emitter;
  research receipt schema.
- Related context: [shared context](../shared/CONTEXT.md).
- Write scope:
  - `arcanum/arcana/inventory/schemas/inventory.operation-receipt.v1.schema.json`
  - `arcanum/arcana/inventory/lib/operation-receipt.cjs`
  - `arcanum/arcana/inventory/test/operation-receipt.test.cjs`
- Done criteria:
  - schema admits the normative receipt and rejects malformed fixtures;
  - canonical bytes and both digests are stable;
  - no wall-clock or filesystem dependency exists.
- Acceptance evidence: `inventory.operation-receipt-kernel-result.v1`.
- Validation:

```sh
node --test arcanum/arcana/inventory/test/operation-receipt.test.cjs
```

- Execution owner: `sigil-development`.
- Handoff: execute only this SWU; return the standard shared result plus exact
  fixture names and byte/digest comparisons.

## Closeout

Use the common baseline and terminal receipt contract in
[WORK-PACK.md](../../WORK-PACK.md#task-session-closeout-sync-contract).
On pass, only `SWU-IFR-002` becomes ready.

