# TASK-CAL-WITNESS — Synthetic L0 witness and independent validation

- Layer/slice: L0 / S-CAL-05
- Wave: W3
- Objective: create one exact witness run from the locked synthetic package and record independent exact-input validation.
- Dependencies: SWU-CAL-009.
- Sources: `../../../06-invoke-design/ARCHITECTURE.md#Compiler-workflow`, `../../../08-distill-repair.md#Required-deterministic-mutant-matrix`.
- Machine execution contract: `../admission/L0-EXECUTION-CONTRACTS.json` entry `SWU-CAL-010`; it closes argv/cwd, exact write partition, runtime, validation, receipt, terminal successor, and stop semantics.

## SWU-CAL-010 — Build and independently validate the synthetic witness

- Primary behavior: bind exact inputs, compile twice in isolation, compare deterministic bytes, run the full test suite, and issue independent ValidationRecords plus an honest result.
- Independent acceptance boundary: witness projection/revision, all validation records, and RESULT agree on exact inputs and mechanics-only ceiling.
- Split analysis: compilation and independent validation can execute as commands, but a witness without its exact validation/claim ceiling is not reviewable and a validation without bound output is meaningless. Source/compiler implementation remains complete before this SWU.
- Dependencies: SWU-CAL-009.
- Source anchors: Stage 06 compiler/witness boundaries and Stage 08 complete mutant/evidence-state contracts.
- Related context: accepted findings' one-tower read-only witness contract, limited to synthetic mechanics in L0.
- Write scope:
  - `projects/cyberalchemy-lab/development/witness-runs/l0-synthetic-001/INPUT-LOCK.json`
  - `projects/cyberalchemy-lab/development/witness-runs/l0-synthetic-001/projection.json`
  - `projects/cyberalchemy-lab/development/witness-runs/l0-synthetic-001/validation-records.json`
  - `projects/cyberalchemy-lab/development/witness-runs/l0-synthetic-001/RESULT.md`
  - `projects/cyberalchemy-lab/development/execution-receipts/WP-CAL-TEN-L0/SWU-CAL-010.json`
- Algorithm:
  1. capture package snapshot, tool/test, Node version, command, environment, and privacy/rule digests in `INPUT-LOCK.json`;
  2. compile twice to isolated temporary outputs and require byte equality;
  3. move only the accepted output to `projection.json`;
  4. run all unit/contract/mutant/package checks against exact current bytes;
  5. independent harness issues immutable ValidationRecords and checks validator identity differs from compiler;
  6. write `RESULT.md` with witnessed/not-witnessed claims and `authority_effect:none`.
- Edge/failure cases: dirty/stale package snapshot, environment mismatch, nondeterministic bytes, failed mutant, compiler self-issued receipt, stale projection revision, prior run overwrite without supersession.
- Done criteria: all commands pass; input lock and output digests recompute; exactly one accepted projection exists; result denies representative/real-source/IDE/authority/effect/readiness claims.
- Validation:
  - `node --test projects/cyberalchemy-lab/research/tower-evidence-navigator/tests/*.test.mjs`
  - `node projects/cyberalchemy-lab/research/tower-evidence-navigator/tools/build-package-snapshot.mjs --check`
  - two invocations of `tools/compile-projection.mjs` against the locked valid fixture followed by exact byte comparison
  - `python3 -m json.tool` over every emitted JSON receipt/projection
- Execution owner: `manual` validation owner inside one Task Session; compiler owner cannot self-approve.
- Handoff note: stop on any failure. Do not continue to T04/T26/another real tower, IDE, promotion, publication, deployment, or release.

## Synchronization

Successful closeout marks L0 mechanics proof complete and sets successor `null`. The next lifecycle route is a separate corpus-owner L1 decision, not an automatic Work Pack successor.
