# Context Pack: SWU-OV1-007

- Task: `SWU-OV1-007` - Body-Context Append
- Mode: standard
- Handoff: none; local Task Session execution
- Strict coverage: pass
- Gate verdict: pass
- Runtime: local
- Dependency receipt: `../20260714T222220Z-swu-ov1-006/TASK-SESSION-RESULT.md`

## Obligation Matrix

| ID | Obligation | Status |
| --- | --- | --- |
| O1 | Reuse fixed operation normalization, id lookup before CAS, conflict, exact retry, and stale semantics. | covered |
| O2 | Enforce 512 KiB UTF-8 fragment limit. | covered |
| O3 | Read and verify the current immutable Operations blob, never workspace content. | covered |
| O4 | Decode valid UTF-8, parse current complete document, and parse fragment in body context. | covered |
| O5 | Append all parsed nodes to body in input order and serialize one complete document. | covered |
| O6 | Enforce 8 MiB complete-result limit before blob/event commit. | covered |
| O7 | Store exact serialized bytes and append the existing V4 content event with mode append. | covered |
| O8 | Cover empty, text/elements, script/style, malformed, table-like, comments, Unicode, SVG, and MathML. | covered |
| O9 | Prove exact retry, id conflict, stale and concurrent writers without duplicate append or auto-rebase. | covered |
| O10 | Preserve orphan/projection recovery and non-displayed notification behavior from replacement. | covered |
| O11 | Load committed complete bytes in Chromium and execute one trusted-local appended interaction. | covered |
| O12 | Run inherited L0, V0, parser, replay, content, CLI, and persistence suites before L1 promotion. | covered |

## Implementation Shape

- Generalize the existing service operation method to admit `replace` and
  `append` while retaining one normalization/CAS/event path.
- For append, read the current revision through the blob store, reject invalid
  UTF-8 round trips, and call `htmlTransformEngine.append`.
- Keep the existing POST operation and CLI `operate` contracts unchanged.
- Add focused Node append tests and one Playwright spec that loads the committed
  content URL directly, clicks an appended control, and observes script-driven
  DOM state.

## Write Scope

- `src/kernel/operations.mjs` append branch.
- `src/server.mjs` only if append introduces one stable error mapping.
- Focused Node and Playwright append tests plus package commands.
- Task Session and synchronized plan/Craft evidence.

## Excluded

- Rebuild, navigation/redirect, browser workbench frame routing, retention
  deletion, regions, collaboration, merge, and automatic rebase.

## Context Builder Result

- Obligation coverage: 12/12, 100 percent
- Strict coverage: pass
- Blockers: 0
- Fallback search: none
- Noise: bounded to append and inherited compatibility evidence
