# TASK-ACAPI-00: Deterministic Ontology Validation

- Layer/slice: L0 prerequisite / S-000.
- Dependencies: none.
- Owner: `augmentor-consultation-candidate-owner`.
- Boundary: repair only the order-sensitive view-digest construction already
  identified by final review. Do not regenerate the ontology receipt or change
  ontology content.

## SWU-ACAPI-000: Stable View Digest Ordering

- Primary behavior: calculate view digests concurrently, then construct their
  object in declared profile order before byte-sensitive receipt comparison.
- Material write:
  `projects/augmentor/ontology/unified-agent/scripts/validate.mjs`.
- Execution outputs: terminal Task Session receipt only.
- Done: repeated unchanged validator runs have one stable result and the full
  ontology test suite passes.
- Validation commands:
  - `node projects/augmentor/ontology/unified-agent/scripts/validate.mjs`
  - `node projects/augmentor/ontology/unified-agent/tests/unified-agent-ontology.test.mjs`
  - `node projects/augmentor/ontology/unified-agent/development/refinement-runs/20260803T180648Z-agent-consultation-api/one-go/scripts/check-validator-determinism.mjs`
- Material package and exact admission request:
  `../../one-go/generated/SWU-ACAPI-000/`.
- Canonical successor: `SWU-ACAPI-001`.
- Closeout: receipt-backed `NO_OP`; execution evidence stays append-only under
  `../../one-go/execution/` and does not mutate the frozen work pack.
