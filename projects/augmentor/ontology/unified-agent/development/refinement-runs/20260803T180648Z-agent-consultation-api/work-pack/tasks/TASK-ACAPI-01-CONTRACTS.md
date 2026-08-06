# TASK-ACAPI-01: Closed Contracts

- Layer/slice: L0 / S-001.
- Dependencies: SWU-ACAPI-000.
- Owner: `augmentor-consultation-candidate-owner`.
- Sources: `../../stages/08-distill-repair.md#H1`, `#H2`, `#H3`, `#H4`,
  `#H6`; `../../stages/08-question-scenarios.md`.

## SWU-ACAPI-001: Query Schema

- Primary behavior: accept only the model-visible `lookup`, `search`, or
  `context` query and reject every undeclared field or protected operation.
- Independent acceptance: valid fixtures pass; caller identity, paths, globs,
  writes, routing, approval, reasoning, execution, and unknown fields fail.
- Split analysis: schema and fixtures are retained together because neither
  proves a closed callable contract alone.
- Write scope:
  - `projects/augmentor/ontology/unified-agent/development/consultation-api/schemas/query.schema.json`
  - `projects/augmentor/ontology/unified-agent/development/consultation-api/fixtures/query-cases.json`
  - `projects/augmentor/ontology/unified-agent/development/consultation-api/scripts/validate-contract.mjs`
- Done: closed schema, hard maximum syntax, and positive/negative fixtures exist.
- Validation: `node projects/augmentor/ontology/unified-agent/development/consultation-api/scripts/validate-contract.mjs --scope query`.
- Acceptance evidence: `../../one-go/execution/receipts/SWU-ACAPI-001.json`.
- Execution owner: `augmentor-consultation-candidate-owner` after approved-epoch
  Task Session admission.
- Handoff: select this SWU only; do not create response or service files.

## SWU-ACAPI-002: Result Union And Evidence Statements

- Primary behavior: validate one status-tagged result union with minimal denial
  and statement-level provenance.
- Independent acceptance: every variant accepts only its allowed fields; denial
  rejects projection, policy, counts, IDs, sources, conflicts, and gaps.
- Split analysis: response variants and evidence statements share one safety
  boundary; an evidence-carrying variant without provenance is invalid.
- Dependencies: SWU-ACAPI-001.
- Write scope:
  - `projects/augmentor/ontology/unified-agent/development/consultation-api/schemas/result.schema.json`
  - `projects/augmentor/ontology/unified-agent/development/consultation-api/schemas/evidence-statement.schema.json`
  - `projects/augmentor/ontology/unified-agent/development/consultation-api/fixtures/result-cases.json`
- Done: all mechanical statuses, precedence metadata, retrieval metric, and
  confidence assessment are closed and fixture-backed.
- Validation: `node projects/augmentor/ontology/unified-agent/development/consultation-api/scripts/validate-contract.mjs --scope result`.
- Acceptance evidence: `../../one-go/execution/receipts/SWU-ACAPI-002.json`.
- Execution owner: `augmentor-consultation-candidate-owner`.
- Handoff: preserve reviewer H2-H5; do not implement service logic.

## Synchronization

Use the immutable closeout rows in `../../WORK-PACK.md`. During the approved
epoch, do not rewrite this task, the work pack, or traceability. Join the exact
terminal receipt and a semantic `NO_OP` proof before advancing.
