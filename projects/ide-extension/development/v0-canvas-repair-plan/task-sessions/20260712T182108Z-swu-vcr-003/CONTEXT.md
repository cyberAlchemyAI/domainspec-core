# Context Pack: SWU-VCR-003

## Selection

- Work-pack: `projects/ide-extension/development/v0-canvas-repair-plan/WORK-PACK.md`
- Task: `TASK-PATH-ADMISSION`
- SWU: `SWU-VCR-003`
- Mode: lean, strict local Task Session
- Runtime handoff: not requested

## Obligations

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| O1 | Require SWU-VCR-002 implementation dependency. | Prior Task Session result and work-pack. | covered-pass |
| O2 | Prove final external symlink publish rejects and appends no event. | Task matrix 1. | covered |
| O3 | Prove nested linked-directory escape rejects. | Task matrix 2. | covered |
| O4 | Prove in-root symlink publishes and serves intended bytes. | Task matrix 3. | covered |
| O5 | Prove retargeted published link becomes unavailable without external bytes. | Task matrix 4. | covered |
| O6 | Preserve normal publish/idempotency/drift/restart behavior. | Existing publish suite. | covered |
| O7 | Preserve bounded missing and directory responses. | Task matrix 6. | covered |
| O8 | Skip only unsupported symlink fixtures with explicit reason. | `symlinkOrSkip` helper. | covered |
| O9 | Keep production source read-only and run inherited suites. | Exact write scope and validation list. | covered |

## Selected Evidence

1. `work-pack/tasks/TASK-PATH-ADMISSION.md`, SWU-VCR-003 matrix and done
   criteria.
2. `tests/session-content-workbench-path-admission.test.mjs`, focused helper and
   initial HTTP retarget witnesses from SWU-VCR-002.
3. `tests/session-content-workbench-publish.test.mjs`, inherited normal,
   duplicate, drift, restart, invalid, and append-failure behavior.
4. `package.json`, existing canvas validation commands.
5. SWU-VCR-002 result, proving the implementation gate passed 3/3 focused and
   4/4 publish tests.

## Execution Decisions

- Extend the existing focused path test rather than create a parallel fixture
  harness.
- Add one named `test:canvas-paths` package command for repeatable validation.
- Assert exact HTTP status and public error body, plus zero event count for
  rejected publication attempts.
- Treat symlink unavailability as an explicit skip only for platform denial
  codes; all other failures remain failures.
- Do not edit production source, schema, projector, or owner contracts.

## Gates

- Dependency: SWU-VCR-002 PASS.
- Decisions: none unresolved.
- Write scope: focused canvas tests, package script, and Task Session evidence.
- Validation: focused path, canvas contracts, publish, and replay suites.
- Strict coverage: pass, 9/9 obligations covered.

## Excluded Context

- Hostile portable race immunity: explicit non-claim.
- Browser UI/Playwright: no display behavior changes.
- Operations V1 and regions: separate lifecycle.
