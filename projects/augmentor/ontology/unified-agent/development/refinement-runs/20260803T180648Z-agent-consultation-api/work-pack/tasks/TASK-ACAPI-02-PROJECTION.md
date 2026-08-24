# TASK-ACAPI-02: Neutral Projection

- Layer/slice: L0 / S-002.
- Dependencies: SWU-ACAPI-002.
- Sources: repair H3 and H9; QS-01, QS-04, QS-06-QS-08.
- Owner: `augmentor-consultation-candidate-owner`.
- Fixture approval reference: `fixture-only:aug-consultation-l0`; this is not
  approval for a private consumer projection.

## SWU-ACAPI-003: Projection And Manifest Schema

- Primary behavior: validate neutral records, opaque IDs, per-field
  provenance, and a compiler/source manifest.
- Independent acceptance: undeclared fields, raw paths, missing source digests,
  or missing output digest fail.
- Split analysis: record and manifest schemas are inseparable because the
  manifest establishes the record set's freshness and field admission.
- Write scope:
  `projects/augmentor/ontology/unified-agent/development/consultation-api/schemas/projection.schema.json`,
  `projects/augmentor/ontology/unified-agent/development/consultation-api/schemas/projection-manifest.schema.json`, and
  `projects/augmentor/ontology/unified-agent/development/consultation-api/fixtures/projection-cases.json`.
- Done: schema and synthetic valid/invalid fixtures exist.
- Validation: `node projects/augmentor/ontology/unified-agent/development/consultation-api/scripts/validate-contract.mjs --scope projection`.
- Evidence: `../../one-go/execution/receipts/SWU-ACAPI-003.json`.

## SWU-ACAPI-004: One-way Fixture Compiler

- Primary behavior: compile one synthetic or target-local private fixture into
  the neutral schema and reject leakage.
- Independent acceptance: deterministic output digest; no private path,
  undeclared field, secret pattern, private authority binding, or missing field
  provenance.
- Split analysis: compiler and leakage check are one behavior plus its
  acceptance boundary.
- Dependencies: SWU-ACAPI-003.
- Write scope:
  `projects/augmentor/ontology/unified-agent/development/consultation-api/scripts/build-fixture-projection.mjs`,
  `projects/augmentor/ontology/unified-agent/development/consultation-api/scripts/validate-projection-leakage.mjs`,
  `projects/augmentor/ontology/unified-agent/development/consultation-api/fixtures/source/ontology.json`,
  `projects/augmentor/ontology/unified-agent/development/consultation-api/tests/projection-compiler.test.mjs`, and
  `projects/augmentor/ontology/unified-agent/development/consultation-api/tests/projection-leakage.test.mjs`.
- Execution outputs:
  `projects/augmentor/ontology/unified-agent/development/consultation-api/fixtures/generated/projection.json` and
  `projects/augmentor/ontology/unified-agent/development/consultation-api/fixtures/generated/projection-manifest.json`.
- Validation: the four structured argv commands in `../../one-go/material-map.json`.
- Evidence: `../../one-go/execution/receipts/SWU-ACAPI-004.json`.
- Boundary: no bytes may be projected into `workspace-resonant`.

## Synchronization

Use receipt-backed `NO_OP` closeout. L1 remains outside the frozen frontier and
blocked by B-002 and B-003 even if both SWUs pass.
