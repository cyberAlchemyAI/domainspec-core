# TASK-IFR-006: Manifest-Bound Runtime Sync

## Objective And Mapping

- Layer/slice: L3 / S-06.
- SWU: `SWU-IFR-006`.
- Goal: install/check/apply only the generated Inventory runtime payload and
  prove that consumer-owned state is outside the managed set.

## Dependencies

- Passing `SWU-IFR-003` and `SWU-IFR-005` receipts.

## Implementation Detail

Inputs:

- canonical runtime files and manifest;
- installed `.arcanum/inventory/` root;
- mode `--check` or `--apply`.

Outputs:

- exact missing/drifted/extra-managed member list;
- check/apply receipt;
- post-sync member digests;
- consumer-state unchanged evidence.

Algorithm:

1. Load the canonical manifest and validate relative paths.
2. Reject paths outside the declared generated member roots.
3. Hash canonical and installed managed members.
4. `--check` reports differences and writes nothing.
5. `--apply` stages managed members, replaces only allowlisted targets, and
   verifies postwrite digests.
6. Hash declared consumer-owned negative-fixture paths before and after.
7. Fail if any consumer-owned path changes.
8. Emit a sync receipt separate from append receipts.

Managed payload:

```text
bin/
lib/
schemas/
scripts/validate-index-json.sh
scripts/validate_projection_conformance.py
runtime-manifest.json
```

Forbidden managed roots:

```text
entries/
queries/
raw/
receipts/
index.json
index.md
schema.md
tags.md
log.md
```

## Smallest Working Unit: SWU-IFR-006

- Primary behavior: synchronize one manifest-owned runtime payload.
- Independent acceptance boundary: exact runtime drift is repaired while every
  consumer-owned fixture digest remains unchanged.
- Candidate children: manifest; check; apply; docs.
- Split analysis: check/apply safety depends on one managed-set contract and
  cannot be accepted from any individual part.
- Write scope:
  - `arcanum/arcana/inventory/runtime-manifest.json`
  - `arcanum/arcana/inventory/scripts/sync-runtime.sh`
  - `arcanum/arcana/inventory/test/runtime-sync.test.cjs`
  - `arcanum/arcana/inventory/test/fixtures/runtime-sync/`
  - `arcanum/arcana/inventory/SKILL.md`
  - `arcanum/arcana/inventory/README.md`
  - `arcanum/arcana/inventory/templates/package-readme.md`
- Done criteria:
  - check detects precise drift;
  - apply repairs only managed members;
  - missing helper blocks append;
  - consumer-owned bytes remain unchanged.
- Acceptance evidence: `inventory.runtime-sync-result.v1`.
- Validation:

```sh
node --test arcanum/arcana/inventory/test/runtime-sync.test.cjs
```

- Execution owner: `sigil-development`.

## Closeout

Passing this unit unlocks only `SWU-IFR-007`.

