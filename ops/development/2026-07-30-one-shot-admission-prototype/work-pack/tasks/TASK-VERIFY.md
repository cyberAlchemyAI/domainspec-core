# TASK-VERIFY

## SWU-OAP-009 — Consolidated prototype validation

- Primary behavior: prove all declared candidate evidence in one report.
- Dependencies: OAP-007 and OAP-008.
- Write scope:
  - `ops/development/2026-07-30-one-shot-admission-prototype/receipts/SWU-OAP-009.json`
  - `ops/development/2026-07-30-one-shot-admission-prototype/PROTOTYPE-VALIDATION.md`
- Checks: schemas; WPRA suites; chain suites; 19 private fixtures; generated
  parity; public/private literal scan; scoped diff check; offline proof that
  the parent gitlink is unchanged; Handoff Notice locator integrity.
- Deferred network check: `make bump-check` is required only after the public
  submodule bytes are intentionally committed and pushed. It is not meaningful
  for uncommitted candidate bytes and is forbidden by this no-network fast
  lane.
- Done criteria: all acceptance-critical checks pass and residue is named.
- Execution owner: local fallback under candidate fast lane.
