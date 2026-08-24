# TASK-ROWS — Add one evidence-backed L1 row projection

Layer/slice: L1 / S-ROWS. Source contracts: `DATA-MODEL.md` row/adapter contract,
`API-CONTRACT.md` row routes, canonical Craft schema named in stage 07.

## SWU-CAPI-008 — Pure 0.3.0 adapter

- Primary behavior: normalize the exact 0.3.0 core families into family-scoped
  envelopes with unique IDs and validated references.
- Independent boundary: fixture-only adapter receipt; no HTTP or WaveDB write.
- Split analysis: each family could later split if the fixture matrix grows;
  initial core families remain one schema-version adapter because cross-family
  references are part of acceptance.
- Dependencies: SWU-CAPI-002 and SWU-CAPI-004.
- Write scope: `implementation/domainspec/tools/craft-consultation-api/src/adapters/v0_3/`,
  `implementation/domainspec/tools/craft-consultation-api/test/adapters/v0_3/`.
- Done/evidence: exact families/ID fields, composite recomposition key, duplicate
  disablement, references, limits, and unknown-field policy pass.
- Validation: fixture hashes, adapter unit/property tests, source fixtures
  unchanged.
- Owner/handoff: bounded implementation helper or local Task Session.

## SWU-CAPI-009 — Conditional row HTTP routes

- Primary behavior: advertise and serve only validated 0.3.0 rows with family-
  scoped authorization and authenticated row cursors.
- Independent boundary: HTTP tests prove authorized list/exact lookup and all
  concealment/replay/duplicate negatives.
- Split analysis: list and exact read share capability advertisement and row
  resource identity; kept as one route-level acceptance boundary.
- Dependencies: SWU-CAPI-005, 006, 007, 008.
- Write scope: `implementation/domainspec/tools/craft-consultation-api/src/http/rows/`,
  `implementation/domainspec/tools/craft-consultation-api/test/http/rows/`.
- Done/evidence: no family/schema/count/duplicate disclosure before auth; cursor
  bindings and canonical ordering pass; unsupported 0.2/0.1 remain 409.
- Validation: row contract and negative disclosure suite.
- Owner/handoff: bounded implementation helper or local Task Session.

Synchronization: 0.2.0 and 0.1 adapters require separate future SWUs only after
owner-scoped fixtures exist; they are not silently included here.
