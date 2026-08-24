# TASK-CONTRACT — Make identifiers, cursors, and schemas executable

Layer/slice: L0 / S-CONTRACT. Source contracts: `API-CONTRACT.md`,
`SECURITY-BOUNDARY.md`, and `stages/08-toy-scenarios.md`.

## SWU-CAPI-004 — Contract schemas and fixtures

- Primary behavior: machine-check request/response/problem, manifest,
  authorization-view, cursor, and freshness-observation shapes.
- Independent boundary: schemas accept all positive fixtures and reject all
  boundary fixtures without running a server.
- Split analysis: each schema is small, but the shared response/snapshot binding
  is the minimum interoperable contract set; separating it creates incompatible
  fixture dialects.
- Dependencies: private implementation root approval.
- Write scope: `implementation/domainspec/tools/craft-consultation-api/contracts/`
  and `implementation/domainspec/tools/craft-consultation-api/test/fixtures/`.
- Done/evidence: versioned schemas, zero private payloads, positive and negative
  fixture matrix, deterministic schema validation receipt.
- Validation: JSON/YAML parse, schema validation, secret scan, fixture hashes.
- Owner/handoff: bounded implementation helper or local Task Session.

## SWU-CAPI-005 — Opaque IDs and cursor primitives

- Primary behavior: byte-exact HMAC space IDs plus authenticated, typed,
  expiring space/row cursors.
- Independent boundary: deterministic vectors and tamper/replay/key-rotation
  tests pass without HTTP or WaveDB.
- Split analysis: identifier and cursor modules may be separate source files, but
  one key/version/canonicalization contract is the acceptance boundary.
- Dependencies: SWU-CAPI-004; secret-provider interface decision (fake provider
  allowed in tests, no real secret access).
- Write scope: `implementation/domainspec/tools/craft-consultation-api/src/security/`
  and `implementation/domainspec/tools/craft-consultation-api/test/security/`.
- Done/evidence: published non-secret vectors; path dictionary, signature,
  scope, policy, snapshot, limit, expiry, and rotation negatives pass.
- Validation: unit/property tests and no-key-in-output scan.
- Owner/handoff: bounded implementation helper or local Task Session.

Synchronization: fixtures are authoritative only for this private candidate
implementation; they do not promote public definitions.
