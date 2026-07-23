# TASK-WFE-004 — Restore Inventory Kind Conformance

- Change: INT-1 / WFE-R08
- Layer/slice/wave: L0 / S0 / W0
- Lifecycle owner: `sigil-development` for Inventory plus repository Inventory owner
- Status: complete — [SWU-WFE-004A receipt](../session-evidence/SWU-WFE-004A/receipt.json)
  and [SWU-WFE-004B receipt](../session-evidence/SWU-WFE-004B/receipt.json)

## Objective

Normalize the exact 15 out-of-enum kind aliases to existing structural kinds and
prevent the deterministic updater from producing another invalid row.

## Sources

- `.arcanum/inventory/index.json`: exact 15 rows
- `.arcanum/inventory/tools/inventory-update.cjs`: `normalizeEntry`, `validate`
- `arcanum/arcana/inventory/scripts/validate-index-json.sh`: supported kind enum
- `arcanum/arcana/inventory/SKILL.md`: machine-index contract
- `../../DESIGN.md#inventory-kind-normalization`

## Dependencies and scope

- Program-order dependency: TASK-WFE-003 closure.
- Write scope: local Inventory index, deterministic updater and updater tests;
  human index/log only if the migration convention requires a durable record.
- Canonical kind enum remains unchanged unless migration discovers a row that
  cannot be represented by existing structural kinds.
- Forbidden: changing IDs, paths, types, sources, tags, selectors, status,
  evidence refs, or Inventory authority.

## SWU-WFE-004A — Exact row migration

- Primary behavior: migrate four aliases over exactly 15 rows:
  `strategy-result` under `entries/` → `entry`; `query-file`,
  `research-findings`, and `research-transcript` under `queries/` → `query`.
- Acceptance boundary: invalid count goes 15→0; supported-kind validator passes;
  every non-kind field and all derived memberships remain identical.
- Split analysis: the aliases form one closed conformance defect and one
  validator verdict; partial migration intentionally remains invalid.

Algorithm: capture before digest/field projection, apply deterministic mapping,
rebuild/verify derived indexes without reordering unrelated rows, compare all
non-kind fields, run validator.

## SWU-WFE-004B — Producer guard

- Dependency: SWU-WFE-004A pass.
- Primary behavior: updater rejects a new unsupported kind before write.
- Acceptance boundary: unsupported input leaves files byte-identical and exits
  non-zero; supported `entry` and `query` controls remain idempotent.
- Split analysis: one producer-validation rule plus its causal fixture.

### Validation

```bash
bash arcanum/arcana/inventory/scripts/validate-index-json.sh .arcanum/inventory/index.json
node .arcanum/inventory/tools/test/test-inventory-update.cjs
jq -e '[.entries[] | select(.kind | IN("page","entry","query","lint","raw-manifest","evidence-card-bundle","evidence-set-bundle") | not)] | length == 0' .arcanum/inventory/index.json
```

Extend the existing focused updater suite at
`.arcanum/inventory/tools/test/test-inventory-update.cjs`; do not substitute a
prose check or create a second competing updater harness.

- Execution owner: `sigil-development`/local Inventory owner.
- Handoff: inspect the live dirty Inventory diff and isolate these 15 rows; stop
  if any row has concurrent semantic edits.
- Receipt: exact before/after IDs and kinds, preserved-field comparison,
  validator result, updater negative/positive fixtures.

## Done

Current index conforms, future unsupported inputs fail before mutation, and
Inventory continues to be a non-authoritative read model.
