# Task Contract: Canonical Canvas Path Admission

## Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-PATH-ADMISSION` |
| Objective | Prevent publish/content reads from resolving outside canonical workspace root. |
| Layer / slice / wave | L1-L2 / VCR-S2-S3 / W1-W2 |
| Execution owner | Task Session, one SWU at a time |

## Source Handles

- [Shared context](../shared/context.md)
- [Cross-task decisions](../shared/cross-task-decisions.md)
- `projects/ide-extension/src/kernel/canvas.mjs`
- `projects/ide-extension/src/server.mjs`
- `projects/ide-extension/tests/session-content-workbench-publish.test.mjs`

## SWU-VCR-002: Canonical File Admission

**Goal:** read only a canonical regular file beneath the canonical workspace
root, through one opened handle.

**Dependencies:** SWU-VCR-001 pass.

**Exact write scope:** `src/kernel/canvas.mjs`, the two canvas error-mapping
branches in `src/server.mjs`, focused helper tests, and Task Session evidence.

**Inputs:** configured workspace root and normalized relative `.html` path.

**Outputs:** original relative path, canonical absolute path, bytes, byte
length, and SHA-256; or an existing bounded canvas error.

**Algorithm:**

1. Preserve current lexical normalization and containment checks.
2. Resolve canonical root and candidate with `realpath`.
3. Use `path.relative` to reject absolute or parent-relative canonical targets.
4. Open the canonical target read-only; include final-link no-follow when the
   platform exposes it.
5. Use handle `stat()` to require a regular file.
6. Read bytes from that handle and close in `finally`.
7. Hash exactly those bytes and return canonical `absolute_path`.
8. Map missing path to `canvas_file_not_found`, outside canonical target to
   `canvas_path_escape`, and non-file to `canvas_not_file`.
9. Publish keeps its current 400/404 mapping. Content fetch maps all admission
   failures to `404 canvas_file_unavailable` and sends no path or bytes.

**Edge cases:** workspace root itself is a symlink; final link to external
file; nested linked directory to external root; in-root link to in-root file;
missing target; directory; link retarget after publication; unsupported
`O_NOFOLLOW` constant.

**Failure modes:** unexpected filesystem error remains a server error; do not
collapse permission or I/O failures into successful absence. A platform gap
that defeats the retained external-link trace returns block.

**Done criteria:** helper and server branches satisfy error table in
`IMPLEMENTATION-PLAN.md`; no request schema, event, or projection change.

**Validation:** focused helper/API tests and `npm run test:canvas-publish`.

**Expected result:** pass with admitted/rejected target matrix. **Handoff:**
SWU-VCR-003.

## SWU-VCR-003: Adversarial And Compatibility Matrix

**Goal:** make the retained symlink trace and normal V0 behavior durable.

**Dependencies:** SWU-VCR-002 pass.

**Exact write scope:** canvas publish/content test files, one new focused path-
admission test file if useful, `package.json` only when a named focused script
is required, and Task Session evidence. Production source is read-only.

**Test matrix:**

1. external final symlink publish returns `canvas_path_escape` and appends no
   event;
2. nested linked directory to external HTML also rejects;
3. in-root link to in-root HTML publishes and serves expected bytes;
4. published in-root link retargeted outside makes content unavailable and
   never returns external bytes;
5. normal file publish, duplicate publish, revision drift, republish, and
   restart remain unchanged;
6. missing and directory targets preserve bounded responses;
7. unsupported symlink environments skip only link-specific fixtures with an
   explicit reason, never report them as passed.

**Done criteria:** every retained K1/P1 counterexample has a failing-before,
passing-after assertion; inherited canvas suites remain green.

**Validation:** focused path tests, `npm run test:canvas-contracts`,
`npm run test:canvas-publish`, and `npm run test:canvas-replay`.

**Expected result:** pass with exact test names/counts. **Handoff:**
SWU-VCR-004.

## Synchronization

Only Task Session evidence may advance SWU/task/wave status. Do not edit the
accepted architecture review or Operations V1 design during this task.
