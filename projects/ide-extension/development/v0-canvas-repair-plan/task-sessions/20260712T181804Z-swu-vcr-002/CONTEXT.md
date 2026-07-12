# Context Pack: SWU-VCR-002

## Selection

- Work-pack: `projects/ide-extension/development/v0-canvas-repair-plan/WORK-PACK.md`
- Task: `TASK-PATH-ADMISSION`
- SWU: `SWU-VCR-002`
- Mode: standard, strict local Task Session
- Runtime handoff: not requested

## Obligations

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| O1 | Require SWU-VCR-001 policy dependency. | Work-pack and prior Task Session result. | covered-pass |
| O2 | Preserve lexical normalized relative `.html` validation. | `normalizeCanvasPath`, task algorithm 1. | covered |
| O3 | Resolve canonical root and target before reading. | K1/P1 and task algorithm 2. | covered |
| O4 | Reject canonical targets outside canonical root. | Implementation-plan containment predicate. | covered |
| O5 | Read one regular file through one opened handle. | VCR-D4 and task algorithm 4-7. | covered |
| O6 | Keep bounded publish errors and map content admission failures to unavailable. | Server publish/content branches and error table. | covered |
| O7 | Preserve schemas, events, projection, and V0 identity. | Exact write scope and done criteria. | covered |
| O8 | Prove normal, in-root-link, external-link, and retarget behavior. | Focused tests plus existing publish suite. | covered |
| O9 | Do not claim hostile portable race immunity. | GAP-VCR-001 and failure policy. | covered |

## Selected Evidence

1. `work-pack/tasks/TASK-PATH-ADMISSION.md`, SWU-VCR-002: exact algorithm,
   errors, edge cases, and write scope.
2. `src/kernel/canvas.mjs`, `normalizeCanvasPath` and `readWorkspaceHtml`: one
   shared helper owns publish and content bytes.
3. `src/server.mjs`, canvas publish and content routes: bounded response mapping
   and no-byte response boundary.
4. `tests/session-content-workbench-publish.test.mjs`: inherited complete-file,
   idempotency, drift, restart, invalid-input, and append-failure behavior.
5. Prior SWU result: trusted-local policy is resolved; no approval subsystem is
   part of this mutation.

## Execution Decisions

- Add a small canonical containment predicate based on `path.relative`.
- Resolve the configured root and requested target with `realpath`.
- Allow symlinks only when their resolved target remains inside the canonical
  root.
- Open the canonical target with `O_RDONLY` and `O_NOFOLLOW` when available,
  then use handle `stat()` and `readFile()` before closing in `finally`.
- Map missing/broken paths to `canvas_file_not_found`, final-link loops/races to
  `canvas_path_escape`, and non-regular targets to `canvas_not_file`.
- Map all three content admission failures to `canvas_file_unavailable` without
  returning filesystem details.
- Add focused helper and HTTP tests; leave the full adversarial matrix to
  SWU-VCR-003.

## Gates

- Dependency: SWU-VCR-001 PASS.
- Decisions: no blocker; the work-pack selected realpath/file-handle admission.
- Platform: Node v22.12.0 on Linux exposes `O_NOFOLLOW`; portable fallback is
  defined for platforms where the constant is absent.
- Write scope: kernel helper, two server error branches, focused tests, and
  Task Session evidence.
- Validation: focused test and existing canvas publish suite available.
- Strict coverage: pass, 9/9 obligations covered.

## Excluded Context

- Operations V1 parsing/blob storage and regions: separate lifecycle.
- Native `openat2` or hostile multi-user filesystem defense: deferred platform
  hardening, not required by the retained counterexample.
- Unrelated bridge, approval, and browser implementation: outside write scope.
