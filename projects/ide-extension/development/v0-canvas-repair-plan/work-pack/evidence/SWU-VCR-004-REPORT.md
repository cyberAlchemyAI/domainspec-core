# V0 Canvas Repair Integrated Evidence Report

## Scope

- Work-pack: `projects/ide-extension/development/v0-canvas-repair-plan/WORK-PACK.md`
- Closure SWU: `SWU-VCR-004`
- Evidence date: 2026-07-12
- Result: PASS

This report closes only the retained current-V0 findings. It does not implement
or promote Operations V1, declared regions, hostile HTML safety, remote access,
or hostile multi-user filesystem race immunity.

## Implemented Boundary

1. `SPEC.md` and `ARCHITECTURE.md` now apply approvals and receipts to
   protected effects and name canvas publication/display as a narrow trusted-
   local preview/read exception.
2. `canvas.surface_published` is defined as append-only audit evidence, not a
   receipt record or protected-effect execution authority.
3. `readWorkspaceHtml` preserves lexical path validation, resolves canonical
   root and target paths, rejects targets outside the canonical root, and reads
   one regular file through one opened handle.
4. Canvas content fetch maps missing, non-file, and escaped canonical targets
   to `404 canvas_file_unavailable` without returning external path or bytes.
5. V0 request schemas, surface identity, complete-file publication,
   idempotency, drift, restart, event, and projection behavior remain unchanged.

## Changed Runtime And Contract Files

- `projects/ide-extension/SPEC.md`
- `projects/ide-extension/ARCHITECTURE.md`
- `projects/ide-extension/src/kernel/canvas.mjs`
- `projects/ide-extension/src/server.mjs`
- `projects/ide-extension/tests/session-content-workbench-path-admission.test.mjs`
- `projects/ide-extension/package.json`

Task Session evidence and V0 repair-plan statuses were also updated. No schema,
projector, interaction, browser, provider, or Operations V1 runtime file was
changed by this work-pack.

## Validation Evidence

| Command | Result |
| --- | --- |
| `npm run test:canvas-paths` | PASS, 5/5, zero skips |
| `npm run test:canvas-contracts` | PASS, 4/4 |
| `npm run test:canvas-publish` | PASS, 4/4 |
| `npm run test:canvas-replay` | PASS, 4/4 |
| `npm run test:bridge` | PASS, 66/66 |
| `npm run validate:schemas` | PASS, 14 runtime schemas, 6 manifests, 54 fixtures |
| protected-effect/exception/audit/read phrase audit | PASS |
| Operations V1 runtime/schema token audit | PASS, no matches |
| scoped `git diff --check` | PASS |
| new-file newline/whitespace/JSON/link audit | PASS |

Total executed Node tests in the integrated closeout: 83/83.

## Review Finding Closure

| Finding | Closure evidence | Verdict |
| --- | --- | --- |
| G1-A | `SPEC.md` names the trusted-local canvas exception and preserves gates for protected effects. | closed |
| G1-R | `ARCHITECTURE.md` distinguishes `canvas.surface_published` from receipt schema records. | closed |
| G1-I | Existing approval-free publish route now implements the explicit exception rather than contradicting the owner contract. | closed |
| K1 | Canonical `realpath` containment and one opened handle reject external targets. | closed for retained trace |
| P1 | Final and nested external symlink API tests reject with zero events; retargeted content returns unavailable. | closed |
| K2 | Owner prose names bytes from one opened-file read, not an atomic snapshot. | closed clarification |
| P2 | Implementation uses handle `stat()` and `readFile()` while retaining the atomic-snapshot non-claim. | closed clarification |

## Adversarial Matrix

- External final symlink publish: `400 canvas_path_escape`, zero events.
- Nested external directory link publish: `400 canvas_path_escape`, zero events.
- In-root symlink: admitted and serves intended bytes.
- Published link retargeted outside: `404 canvas_file_unavailable`; response
  contains neither external body nor external path.
- Missing HTML: `404 canvas_file_not_found`.
- `.html` directory: `400 canvas_not_file`.
- Normal publication, duplicate idempotency, drift, republish, restart,
  contracts, and replay: passing.

## Recovery Note

The first SWU-VCR-003 focused run passed 4/5 tests. The failed assertion assumed
that zero-event `/api/state` already contained a canvas namespace. The test was
corrected to the public `/api/canvas/current` contract, `{ current: null }`.
Production code was unchanged by the recovery; all final suites passed.

## Honest Claim Boundary

The evidence supports:

> Current trusted-local V0 canvas publication has an explicit preview/display
> authority exception and does not admit or serve HTML whose resolved target is
> outside the canonical workspace root in the tested final-link, nested-link,
> and post-publication-retarget cases.

It does not support hostile concurrent parent-directory race immunity,
arbitrary HTML safety, remote publication, multi-user isolation, immutable V0
history, Operations V1 readiness, or declared-region mutation.

## Residue

- Portable Node does not expose cross-platform `openat2(RESOLVE_BENEATH)`
  semantics. The retained demonstrated symlink traces are closed; stronger
  hostile filesystem guarantees remain future hardening.
- The repository still contains unrelated concurrent changes. Validation and
  diff checks were scoped; none were cleaned or reverted.
- Operations V1 remains a separate design-ready package requiring its own
  accepted Invoke plan before execution.
