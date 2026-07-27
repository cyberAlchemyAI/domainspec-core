# TASK-DVC-002: Public Design-Selection Schemas

- Slice/layer/wave: S1 / L1 / W1.
- Source: `../../../DESIGN.md` planned public contracts.
- Dependency: SWU-DVC-001.
- Gaps owned: DVC-G02, DVC-G03, DVC-G04.

## Objective

Add three versioned schemas without collapsing author, detector, validator,
selection, or evidence-state responsibilities.

## SWU-DVC-002A: Scope manifest schema

- Write scope:
  `arcanum/spells/invoke/schemas/design-scope-manifest.schema.json`.
- Primary behavior: accept exactly a closed normalized manifest.
- Done: all field classes are typed; `unknowns` must be empty for pass-ready
  inputs; source and target bindings require digests; author identity is
  required.
- Edge cases: duplicate IDs, unresolved selector, empty required digest,
  malformed exclusion, unknown field class.
- Validation:
  `python3 -m json.tool arcanum/spells/invoke/schemas/design-scope-manifest.schema.json`.

## SWU-DVC-002B: Denominator receipt schema

- Dependencies: DVC-002A.
- Write scope:
  `arcanum/spells/invoke/schemas/design-denominator-receipt.schema.json`.
- Primary behavior: accept exactly one detector receipt bound to one manifest
  digest.
- Done: detector identity/version/owner, inspected selectors, extracted
  signals, denominator IDs, unbound and missing-input arrays, verdict, receipt
  digest, and validator owner are typed.
- Edge cases: author equals detector, stale manifest digest, duplicate signal
  IDs, `pass` with missing/unbound signals.
- Validation:
  `python3 -m json.tool arcanum/spells/invoke/schemas/design-denominator-receipt.schema.json`.

## SWU-DVC-002C: Selection result schema

- Dependencies: DVC-002B.
- Write scope:
  `arcanum/spells/invoke/schemas/design-selection-result.schema.json`.
- Primary behavior: accept exactly one total fixed-point selection result.
- Done: primary concern, four owner fields, four dispositions, selected
  outputs, pass digests, fixed-point boolean, diagnostics, and Design evidence
  state are typed; Plan evidence states are forbidden.
- Edge cases: selected recommended output, N/A without evidence selectors,
  unresolved owner, unequal pass digests with fixed point true, Plan evidence
  in a Design result.
- Validation:
  `python3 -m json.tool arcanum/spells/invoke/schemas/design-selection-result.schema.json`.

## Split analysis

The three schemas can validate independently and therefore remain separate
SWUs. Their dependency order prevents the result schema from redefining a
denominator or manifest field.

## Closeout

Each SWU emits its own schema receipt and updates only its exact row in
`../shared/CLOSEOUT-CONTRACT.md`.

## Completion evidence

- SWU-DVC-002A: pass; 1 valid and 4 invalid manifest controls. Receipt:
  `../session-evidence/SWU-DVC-002A/execution-receipt.json`.
- SWU-DVC-002B: pass; 1 valid and 4 invalid denominator controls. Receipt:
  `../session-evidence/SWU-DVC-002B/execution-receipt.json`.
- SWU-DVC-002C: pass; 1 valid and 4 invalid selection-result controls.
  Receipt: `../session-evidence/SWU-DVC-002C/execution-receipt.json`.
