# Context Pack: SWU-VCR-004

## Selection

- Work-pack: `projects/ide-extension/development/v0-canvas-repair-plan/WORK-PACK.md`
- Task: `TASK-VERIFY`
- SWU: `SWU-VCR-004`
- Mode: standard, strict local Task Session
- Runtime handoff: not requested

## Obligations

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| O1 | Require SWU-VCR-003 pass and complete prior receipts. | Task Session results 001-003 and work-pack. | covered-pass |
| O2 | Run focused and inherited canvas suites. | Package scripts and prior test surfaces. | covered |
| O3 | Run bridge regression and schema validation. | `test:bridge`, `validate:schemas`. | covered |
| O4 | Confirm protected effects, canvas exception, audit event, receipt, and read wording. | `SPEC.md`, `ARCHITECTURE.md`, SWU-001 result. | covered |
| O5 | Confirm V0 publish schema/response compatibility and no external leak. | Contract/publish/path tests, SWU-002/003 results. | covered |
| O6 | Map G1-A/G1-R/G1-I/K1/P1/K2/P2 to evidence. | Shared traceability and accepted findings. | covered |
| O7 | Confirm repair implementation contains no Operations V1 route/schema/storage. | Scoped changed-file and content audit. | covered |
| O8 | Produce report, scoped diff result, and synchronized closure state. | Exact write scope and done criteria. | covered |

## Selected Evidence

1. `work-pack/tasks/TASK-VERIFY.md`: ordered checks and honest claim boundary.
2. `work-pack/shared/traceability.md`: retained review-item mapping.
3. SWU-VCR-001 result: policy clauses and read clarification.
4. SWU-VCR-002 result: canonical helper, server mapping, focused proof.
5. SWU-VCR-003 result: 17/17 adversarial and compatibility tests.
6. `SPEC.md`, `ARCHITECTURE.md`, `src/kernel/canvas.mjs`, `src/server.mjs`,
   focused path tests, and package scripts: live closure surface.

## Execution Decisions

- Rerun all validation from the live checkout; do not rely only on prior counts.
- Write one evidence report under `work-pack/evidence/` and update plan status
  only after every mandatory check passes.
- Treat the portable hostile race limitation as residue, not a blocker or a
  closed security claim.
- Treat any Operations V1 source/schema/route in the V0 repair scope as block.

## Gates

- Dependency: SWU-VCR-003 PASS.
- Decisions: none unresolved.
- Write scope: evidence report, Task Session result, and V0 repair-plan status
  artifacts only; source/runtime read-only.
- Validation paths: complete and locally available.
- Strict coverage: pass, 8/8 obligations covered.

## Excluded Context

- Operations V1 design package is checked only as a separate non-runtime
  boundary; it is not validated or promoted by this SWU.
- Browser/Playwright is excluded because no display behavior changed.
- Hostile multi-user filesystem guarantees remain out of scope.
