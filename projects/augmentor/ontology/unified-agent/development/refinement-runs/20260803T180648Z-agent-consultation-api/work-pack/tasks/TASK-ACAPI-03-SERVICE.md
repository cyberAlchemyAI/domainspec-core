# TASK-ACAPI-03: Fixture Consultation Service

- Layer/slice: L0 / S-002.
- Dependencies: SWU-ACAPI-002 and SWU-ACAPI-004.
- Sources: repaired H2, H5-H8; scenario matrix.
- Owner: `augmentor-consultation-candidate-owner`.

## SWU-ACAPI-005: Limits And Status Resolver

- Primary behavior: compute effective caps before reads and reduce observed
  mechanical conditions to one deterministic status.
- Acceptance: service/policy/request cap minimums, byte and token estimator
  versions, deadline/cancellation, and status precedence pass fixtures.
- Split analysis: cap computation and status reduction are one request-boundary
  decision; no retrieval is implemented here.
- Write scope:
  `projects/augmentor/ontology/unified-agent/development/consultation-api/src/effective-limits.mjs`,
  `projects/augmentor/ontology/unified-agent/development/consultation-api/src/status-resolver.mjs`,
  `projects/augmentor/ontology/unified-agent/development/consultation-api/tests/effective-limits.test.mjs`, and
  `projects/augmentor/ontology/unified-agent/development/consultation-api/tests/status-resolver.test.mjs`.
- Validation: `node --test projects/augmentor/ontology/unified-agent/development/consultation-api/tests/effective-limits.test.mjs projects/augmentor/ontology/unified-agent/development/consultation-api/tests/status-resolver.test.mjs`.
- Evidence: `../../one-go/execution/receipts/SWU-ACAPI-005.json`.
- Boundary: this unit proves pre-read lifetime checks; propagation through the
  actual reader is accepted only by SWU-ACAPI-006 scenarios.

## SWU-ACAPI-006: Consultation Boundary Over Fixture

- Primary behavior: execute `lookup`, `search`, and `context` against the
  fixture projection and return the validated result union.
- Acceptance: QS-01-QS-14 pass without writes or prose reasoning.
- Split analysis: recheck at admission; split lookup/search/context when each
  can pass independently in the chosen code structure.
- Dependencies: SWU-ACAPI-005.
- Write scope:
  `projects/augmentor/ontology/unified-agent/development/consultation-api/src/consultation-boundary.mjs`,
  `projects/augmentor/ontology/unified-agent/development/consultation-api/src/projection-reader.mjs`,
  `projects/augmentor/ontology/unified-agent/development/consultation-api/tests/consultation-boundary.test.mjs`, and
  `projects/augmentor/ontology/unified-agent/development/consultation-api/tests/question-scenarios.test.mjs`.
- Validation: `node --test projects/augmentor/ontology/unified-agent/development/consultation-api/tests/consultation-boundary.test.mjs projects/augmentor/ontology/unified-agent/development/consultation-api/tests/question-scenarios.test.mjs`.
- Evidence: `../../one-go/execution/receipts/SWU-ACAPI-006.json`.
- Atomicity is frozen: lookup, search, and context are closed variants of one
  public `consult` pipeline and will not split inside this epoch.
- Scenario scope: QS-01-QS-11, QS-13, and QS-14 execute against the fixture;
  QS-12 proves that L0 exposes no shared cache. Production cache isolation
  remains L2 evidence.
- Canonical successor: terminal sentinel `__complete__`.
- Handoff: stop. No host adapter, L1 successor, or actual private consumer
  projection is part of the captured frontier.
