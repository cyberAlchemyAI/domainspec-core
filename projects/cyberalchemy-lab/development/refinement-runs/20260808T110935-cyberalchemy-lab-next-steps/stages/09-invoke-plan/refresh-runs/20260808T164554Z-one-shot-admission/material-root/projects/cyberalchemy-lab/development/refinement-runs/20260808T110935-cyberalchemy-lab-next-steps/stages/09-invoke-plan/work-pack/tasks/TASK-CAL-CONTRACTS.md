# TASK-CAL-CONTRACTS — Deterministic contract foundation

- Layer/slice: L0 / S-CAL-01
- Waves: W0, W1
- Objective: implement the smallest deterministic identity primitive, then close candidate record/relation and projection/privacy contracts.
- Source contracts: `../../shared/CONTEXT.md`, `../../../06-invoke-design/ARCHITECTURE.md`, `../../../08-distill-repair.md`.
- Blockers: none for synthetic L0.
- Machine execution contract: `../admission/L0-EXECUTION-CONTRACTS.json` entries `SWU-CAL-001` through `SWU-CAL-003`; those entries close argv/cwd, exact write partition, runtime, validation, receipt, successor, and stop semantics.

## SWU-CAL-001 — Canonical JSON and digest primitive

- Primary behavior: deterministically parse, restrict, serialize, and hash `cal-canonical-json-v1` values.
- Independent acceptance boundary: equivalent objects with different key order emit identical bytes/digest; every forbidden value/key/duplicate-key case fails before hashing.
- Split analysis: parser restrictions, serialization, and hashing were considered as children, but none is independently safe—the digest contract is executable only when all three share one closed profile. Schema/domain records are independent and remain SWU-CAL-002.
- Dependencies: none.
- Source anchors: Stage 08 `Repair 1 — Closed canonical JSON profile`; Stage 06 `Package self-binding rule` only for downstream use.
- Related context: no product package or Research Tower scaffold is required to test this pure primitive.
- Write scope:
  - `projects/cyberalchemy-lab/research/tower-evidence-navigator/schemas/canonical-json-profile.json`
  - `projects/cyberalchemy-lab/research/tower-evidence-navigator/tools/canonical-json.mjs`
  - `projects/cyberalchemy-lab/research/tower-evidence-navigator/tests/canonical-json.test.mjs`
  - `projects/cyberalchemy-lab/development/execution-receipts/WP-CAL-TEN-L0/SWU-CAL-001.json`
- Algorithm:
  1. scan raw JSON and reject duplicate object keys before ordinary materialization;
  2. recursively reject floats, exponent values, negative zero, unsafe integers, non-ASCII keys, unsupported values, and cycles;
  3. sort object keys by ASCII byte order, preserve array order, serialize strings with deterministic ECMAScript JSON escaping, and add no whitespace;
  4. encode UTF-8 and return bytes plus SHA-256 tagged with profile/schema version;
  5. expose pure functions only; perform no filesystem/network write.
- Edge/failure cases: empty object/array, Unicode string values, escaped control characters, integer boundaries, nested key order, duplicate keys, `-0`, float/exponent, non-ASCII key.
- Done criteria: profile JSON documents the closed vocabulary; module and tests agree on every valid/invalid vector; receipt lists exact bytes and commands.
- Acceptance evidence: passing Node tests plus two fixed byte/digest golden vectors.
- Validation: `node --test projects/cyberalchemy-lab/research/tower-evidence-navigator/tests/canonical-json.test.mjs`.
- Execution owner: `local-fallback` through one Task Session.
- Handoff note: do not create the package scaffold or any schema beyond the canonical profile; return exact golden bytes/digests and touched-file inventory.

## SWU-CAL-002 — Closed candidate records and relation registry

- Primary behavior: accept only the designed candidate record kinds and valid typed relation endpoints/cardinality/cycle policies.
- Independent acceptance boundary: record/relation contract tests pass without projection/privacy behavior.
- Split analysis: record schema and relation registry were considered separately, but every candidate's evidence/definition/residue closure requires the relation endpoint contract to validate the record graph. Projection output remains independent in SWU-CAL-003.
- Dependencies: SWU-CAL-001.
- Source anchors: Stage 06 `Closed record kinds` and `Required relation registry`; Stage 08 fixture cardinality.
- Related context: Stage 02 glossary baseline and Stage 07 identity/authority review.
- Write scope:
  - `projects/cyberalchemy-lab/research/tower-evidence-navigator/schemas/lab-records.schema.json`
  - `projects/cyberalchemy-lab/research/tower-evidence-navigator/ontology/relation-registry.json`
  - `projects/cyberalchemy-lab/research/tower-evidence-navigator/tests/record-contract.test.mjs`
  - `projects/cyberalchemy-lab/development/execution-receipts/WP-CAL-TEN-L0/SWU-CAL-002.json`
- Algorithm:
  1. define closed kind discriminators and shared constants (`authority_effect`, status, privacy, fixture class);
  2. validate per-kind required fields and ID/digest grammar;
  3. load a closed relation registry and verify direction, admitted endpoint kinds, cardinality, and cycle policy;
  4. reject unknown fields/kinds, dangling endpoints, ID collisions, inferred equality, unanchored claims/candidates, and unblocked promotion.
- Edge/failure cases: equal bytes/different logical IDs, duplicate logical ID, symmetric contradiction pair, extra contradiction cycle, open residue absent, unsupported relation.
- Done criteria: all designed kinds and only required relation kinds are expressible; invalid graph vectors fail with stable codes.
- Acceptance evidence: schema parse plus Node contract tests.
- Validation: `node --test projects/cyberalchemy-lab/research/tower-evidence-navigator/tests/record-contract.test.mjs`.
- Execution owner: `local-fallback`.
- Handoff note: do not author actual fixture records or projection schema; preserve exact kind/relation vocabularies from Stage 06/08.

## SWU-CAL-003 — Privacy-filtered projection contract

- Primary behavior: define one disposable projection shape and field-level privacy policy that fail closed before any IDE transport exists.
- Independent acceptance boundary: projection/privacy contract vectors validate without compiler or source fixture.
- Split analysis: projection structure and privacy policy could be separate documents but cannot pass independently because the output schema must require the applied policy digest and deny unfiltered fields. IDE transport is independently verifiable and deferred.
- Dependencies: SWU-CAL-001, SWU-CAL-002.
- Source anchors: Stage 06 `Projection revision`, reserved direct-GET fields; Stage 08 `Repair 4 — Privacy scan`.
- Related context: current IDE projection precedent is context only; no IDE path is writable.
- Write scope:
  - `projects/cyberalchemy-lab/research/tower-evidence-navigator/schemas/projection.schema.json`
  - `projects/cyberalchemy-lab/research/tower-evidence-navigator/privacy/privacy-policy.json`
  - `projects/cyberalchemy-lab/research/tower-evidence-navigator/projection/projection-contract.json`
  - `projects/cyberalchemy-lab/research/tower-evidence-navigator/tests/projection-contract.test.mjs`
  - `projects/cyberalchemy-lab/development/execution-receipts/WP-CAL-TEN-L0/SWU-CAL-003.json`
- Algorithm:
  1. close projection header/revision inputs, record/relation/adjacency ordering, invalid/stale flags, fixture class, and authority fields;
  2. define allowed/denied fields and byte sentinels by privacy class;
  3. recursively scan candidate output values and serialized bytes;
  4. reject POST/publication/effectful reserved consumer contracts statically;
  5. require every output record to bind privacy-policy digest and source/claim ceiling metadata.
- Edge/failure cases: nested denied locator, content sentinel, missing privacy class, stale revision input, extra output key, POST/publication token, cleared residue.
- Done criteria: contract exposes all later direct-GET fields without defining a route/server; privacy mutants fail with stable codes.
- Acceptance evidence: Node contract tests and exact expected projection skeleton.
- Validation: `node --test projects/cyberalchemy-lab/research/tower-evidence-navigator/tests/projection-contract.test.mjs`.
- Execution owner: `local-fallback`.
- Handoff note: no adapter, HTTP server, HTML, browser, or IDE file is in scope.

## Synchronization

Each SWU writes its execution receipt, then the exact `CLOSEOUT-CONTRACT.md` route updates this task, its wave, `WORK-PACK.md`, the one-unit execution projection, and a closeout receipt. Successful order is 001 -> 002 -> 003; no sibling runs in parallel because each consumes the preceding contract.
