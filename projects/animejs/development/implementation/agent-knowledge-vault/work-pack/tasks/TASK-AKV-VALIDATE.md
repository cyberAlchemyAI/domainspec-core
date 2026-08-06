# TASK-AKV-VALIDATE — Integrated candidate validation

## SWU-AKV-NV-008

- Primary behavior: prove deterministic package integrity and emit one digest-bound validation receipt.
- Checks: schemas, closed vocabularies, IDs, endpoints, cycles, query replay, 17 relation mutants, source counts/digests, graph/view freshness, state transitions, authority boundaries, copyright controls, zero false verified lessons, deterministic rebuild, and write isolation.
- Write scope: `scripts/validate.mjs`, `tests/ontology.test.mjs`, `README.md`, `RESIDUE.json`, `receipts/validation-receipt.json`.
- Done: validators and tests pass with zero violations; receipt binds every source/contract/node/relation/view/test digest and states candidate-local claim ceilings.
- Validation: `node projects/animejs/ontology/agent-knowledge-vault/scripts/validate.mjs && node projects/animejs/ontology/agent-knowledge-vault/tests/ontology.test.mjs`.
- Split analysis: terminal validator, documentation, residue, and receipt are one closure transaction; any promotion or runtime integration is a separate owner route.
- Execution owner: local fallback plus Ontology Vault validate owner.
