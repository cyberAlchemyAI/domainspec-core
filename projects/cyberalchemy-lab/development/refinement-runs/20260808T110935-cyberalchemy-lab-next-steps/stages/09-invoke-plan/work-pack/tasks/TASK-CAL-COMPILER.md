# TASK-CAL-COMPILER — Deterministic projection and negative matrix

- Layer/slice: L0 / S-CAL-03
- Wave: W2
- Objective: compile the valid fixture into canonical projection bytes and prove every required invalid transition fails closed.
- Source contracts: `../../shared/CONTEXT.md`, `../../../06-invoke-design/ARCHITECTURE.md`, `../../../08-distill-repair.md`.
- Machine execution contract: `../admission/L0-EXECUTION-CONTRACTS.json` entries `SWU-CAL-007` and `SWU-CAL-008`; those entries close argv/cwd, exact write partition, runtime, validation, receipt, successor, and stop semantics.

## SWU-CAL-007 — Deterministic projection compiler

- Primary behavior: validate one allowlisted input graph and emit one canonical privacy-filtered forward/reverse projection.
- Independent acceptance boundary: valid fixture compiles twice to byte-identical output/revision; no negative matrix is required yet beyond unit boundary cases.
- Split analysis: input validation, graph construction, privacy filter, revision, and atomic output were considered separately, but independently passing fragments cannot prove the selected end-to-end transformation. Negative mutants are a distinct acceptance behavior in SWU-CAL-008.
- Dependencies: SWU-CAL-006.
- Source anchors: Stage 06 compiler workflow, projection revision, and decision flow; Stage 08 canonicalization/privacy repairs.
- Related context: Stage 05 recomposition proof and Stage 07 compiler-independence review.
- Write scope:
  - `projects/cyberalchemy-lab/research/tower-evidence-navigator/tools/compile-projection.mjs`
  - `projects/cyberalchemy-lab/research/tower-evidence-navigator/tests/compile-projection.test.mjs`
  - `projects/cyberalchemy-lab/development/execution-receipts/WP-CAL-TEN-L0/SWU-CAL-007.json`
- Algorithm: execute the Stage 06 compiler workflow with Stage 08 canonicalization/privacy repairs; recompute all IDs; validate anchors/relations/gates; stable-sort records/relations; build forward/reverse adjacency; compute revision; write temp then atomic rename only after final scan.
- Edge/failure cases: pre-existing valid output on failed run, same input repeated, temp cleanup, unknown kind, missing endpoint, denied nested field, stale ID.
- Done criteria: two isolated compiles produce identical bytes/revision; input remains byte-identical; no external/IDE/graph/database effect occurs.
- Validation: `node --test projects/cyberalchemy-lab/research/tower-evidence-navigator/tests/compile-projection.test.mjs`.
- Execution owner: `local-fallback`.
- Handoff note: compiler may emit diagnostics/build input lock but not a passing ValidationRecord or authority decision.

## SWU-CAL-008 — Fifteen fail-closed mutants

- Primary behavior: prove the exact Stage 08 mutant-to-failure-code matrix without replacing a valid projection.
- Independent acceptance boundary: every mutant changes one primary condition, fails with its exact code, and preserves prior valid output bytes.
- Split analysis: each mutant can fail independently, but the required acceptance boundary is matrix completeness and single-fault attribution; splitting would allow omitted failure classes to pass unnoticed. Runtime POST behavior is explicitly excluded—M12 is static contract evidence only.
- Dependencies: SWU-CAL-007.
- Source anchors: Stage 08 required deterministic mutant matrix M01-M15.
- Related context: Stage 07 static-versus-runtime evidence ceiling for POST/publication.
- Write scope:
  - `projects/cyberalchemy-lab/research/tower-evidence-navigator/fixtures/invalid/mutant-matrix.json`
  - `projects/cyberalchemy-lab/research/tower-evidence-navigator/tests/negative-mutants.test.mjs`
  - `projects/cyberalchemy-lab/development/execution-receipts/WP-CAL-TEN-L0/SWU-CAL-008.json`
- Algorithm: derive each mutant from the valid fixture using the single committed delta contract `fixtures/invalid/mutant-matrix.json`; assert one changed primary condition; run compile/validator; assert stable code, no replacement output, and no unexpected effect; report matrix completeness by IDs M01-M15.
- Edge/failure cases: mutant triggers earlier unrelated failure, multiple faults, missing ID, wrong code, output changed on failure, M12 mislabeled runtime proof.
- Done criteria: all 15 IDs execute once and pass exact-code/no-write assertions; matrix report names static versus runtime ceilings.
- Validation: `node --test projects/cyberalchemy-lab/research/tower-evidence-navigator/tests/negative-mutants.test.mjs`.
- Execution owner: `local-fallback`.
- Handoff note: do not weaken input to make expected codes easier; repair ordering only when the single-fault mutant demonstrates ambiguous precedence.

## Synchronization

Order is 007 -> 008. Any acceptance-critical mutant mismatch blocks W2 and prevents package snapshot/witness generation.
