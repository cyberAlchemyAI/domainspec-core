# TASK-CAL-SNAPSHOT — Complete candidate package identity

- Layer/slice: L0 / S-CAL-04
- Wave: W3
- Objective: bind every authored package file into one non-circular ordered package snapshot.
- Dependencies: SWU-CAL-008.
- Sources: `../../../06-invoke-design/ARCHITECTURE.md#Package-self-binding-rule`, `../../../08-distill-repair.md#Repair-1--Closed-canonical-JSON-profile`.
- Machine execution contract: `../admission/L0-EXECUTION-CONTRACTS.json` entry `SWU-CAL-009`; it closes argv/cwd, exact write partition, runtime, validation, receipt, successor, and stop semantics.

## SWU-CAL-009 — Package snapshot builder and manifest

- Primary behavior: enumerate the declared authored-file set, apply normalized self-binding, and emit/verify `PACKAGE-SNAPSHOT.json`.
- Independent acceptance boundary: every package file appears exactly once; any add/remove/change/reorder/stale-self field fails with a new expected ID.
- Split analysis: enumeration, self-digest, and tower snapshot ID were considered separately, but the complete package identity exists only when all agree over the same ordered material. Generated witness output is separate SWU-CAL-010.
- Dependencies: SWU-CAL-008.
- Source anchors: Stage 06 package self-binding rule and Stage 08 closed canonical JSON repair.
- Related context: Stage 07 projection/package cycle review.
- Write scope:
  - `projects/cyberalchemy-lab/research/tower-evidence-navigator/tools/build-package-snapshot.mjs`
  - `projects/cyberalchemy-lab/research/tower-evidence-navigator/PACKAGE-SNAPSHOT.json`
  - `projects/cyberalchemy-lab/research/tower-evidence-navigator/tests/package-snapshot.test.mjs`
  - `projects/cyberalchemy-lab/development/execution-receipts/WP-CAL-TEN-L0/SWU-CAL-009.json`
- Algorithm: enumerate explicit allowlisted package files; exclude witness-run output only; compute file digests/sizes; normalize manifest entry/root self fields; canonicalize/hash; compute tower snapshot ID; materialize; verify from disk; reject extras/missing/order drift.
- Edge/failure cases: manifest includes generated projection, manifest omits itself, duplicate path, symlink escape, unordered filesystem enumeration, stale self/tower ID, unexpected file.
- Done criteria: `--check` passes from a clean invocation; M14 fails with `CAL_PACKAGE_MANIFEST_STALE`; all prior package bytes except the three owned targets remain unchanged.
- Validation: `node --test projects/cyberalchemy-lab/research/tower-evidence-navigator/tests/package-snapshot.test.mjs && node projects/cyberalchemy-lab/research/tower-evidence-navigator/tools/build-package-snapshot.mjs --check`.
- Execution owner: `local-fallback`.
- Handoff note: no generated projection or executed ValidationRecord may enter package identity; unexpected files block rather than auto-admit.

## Synchronization

Passing SWU-CAL-009 enables only the synthetic witness run. It does not close L0 or admit L1.
