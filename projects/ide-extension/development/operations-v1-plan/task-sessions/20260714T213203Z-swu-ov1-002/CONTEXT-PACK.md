# Context Pack: SWU-OV1-002

- Task: `SWU-OV1-002` - parse5 Transformer And Golden Bytes
- Mode: standard
- Handoff: none; local Task Session execution
- Strict coverage: pass
- Gate verdict: pass
- Runtime: local

This file is session evidence. It is not a canonical planning or contract
source.

## Objective

Pin parse5 8.0.1 and add one deterministic `HtmlTransformEngine` for complete
document replacement and body-context fragment append. Freeze exact serialized
bytes, lengths, and SHA-256 digests without adding routes, storage, projection,
or browser behavior.

## Obligation Matrix

| ID | Obligation | Controlling evidence | Status |
| --- | --- | --- | --- |
| O1 | Pin direct runtime dependency `parse5` at exactly `8.0.1` in package and lock files. | Task contract; OVG-001; OV1-PD2. | covered |
| O2 | Expose `HtmlTransformEngine` replacement and append methods behind a local kernel module. | Task contract; OVG-001 selected option. | covered |
| O3 | Parse complete HTML in document mode and serialize the complete document once. | Task contract algorithm; architecture Content Operation Contract. | covered |
| O4 | Parse append input in the current document body's fragment context and preserve node order. | Task contract algorithm; OV1-D5; append downstream contract. | covered |
| O5 | Return UTF-8 bytes, byte length, and SHA-256 for each deterministic result. | Task contract output and done criteria. | covered |
| O6 | Require exactly one body in the parsed current tree and return a typed transform error if that invariant fails. | Task contract failure step; accepted architecture. | covered |
| O7 | Keep script/style nodes inert and perform no resource loading. | OVG-001; shared Operations V1 boundary. | covered |
| O8 | Freeze golden behavior for the complete required corpus, including repeated determinism. | Task contract Golden corpus and Edge cases. | covered |
| O9 | Do not claim source-format preservation or generic malformed-HTML rejection. | Task contract Edge cases and Failure modes; OVG-001. | covered |
| O10 | Preserve server, projector, storage, browser, V0 routes, and existing tests. | Exact write scope; shared V0 behavior and Worktree Rule. | covered |
| O11 | Run `test:operations-transform` and inherited schema/contract checks. | Task contract Validation. | covered |
| O12 | Synchronize a PASS receipt before exposing SWU-OV1-003. | Task contract Synchronization; work-pack gate 2. | covered |

## Selected Context

1. `development/operations-v1-plan/WORK-PACK.md`
   - Selectors: SWU manifest, blockers/gaps, gate checks, next route.
   - Covers: O10-O12.
2. `development/operations-v1-plan/work-pack/tasks/TASK-CONTRACT-TRANSFORM.md`
   - Selector: `SWU-OV1-002` and Synchronization.
   - Covers: O1-O12.
3. `development/operations-v1-plan/work-pack/waves/W0.md`
   - Selectors: entry, exit, promotion, stop.
   - Covers: O8, O11, O12.
4. `development/operations-v1-plan/task-sessions/20260714T211557Z-swu-ov1-001/TASK-SESSION-RESULT.md`
   - Selectors: PASS result, frozen limits, reroute.
   - Covers: O1, O11, O12.
5. `development/operations-v1-plan/work-pack/shared/context.md`
   - Selectors: Preserved V0 Behavior, Operations V1 Boundary, Worktree Rule.
   - Covers: O7, O10.
6. `development/operations-v1-plan/work-pack/shared/cross-task-decisions.md`
   - Selector: OV1-PD2, PD3, PD11, PD12.
   - Covers: O1-O4, O7, O9.
7. `development/operations-v1-design/PLANNING-DECISION-GATE.md`
   - Selector: OVG-001 selected direct parse5 8.0.1 option.
   - Covers: O1-O4, O7-O9.
8. `development/operations-v1-design/DECISIONS.md`
   - Selectors: OV1-D3 through OV1-D5.
   - Covers: O3, O4, O9.
9. `development/operations-v1-design/ARCHITECTURE-BUNDLE.md`
   - Selector: Content Operation Contract.
   - Covers: O3, O4, O6, O9.
10. `development/operations-v1-plan/work-pack/tasks/TASK-DERIVE-REPLACE.md`
    - Selector: replacement transform and limit sequence.
    - Covers: O2, O3, O5.
11. `development/operations-v1-plan/work-pack/tasks/TASK-APPEND.md`
    - Selector: body-context append algorithm and corpus.
    - Covers: O2, O4-O8.
12. `package.json` and `package-lock.json`
    - Selectors: ESM runtime dependencies and exact lock structure.
    - Covers: O1, O10, O11.
13. `src/kernel/operations-contracts.mjs`
    - Selectors: frozen limits and typed helper style.
    - Covers: O5, O10.
14. `src/kernel/canvas.mjs` and `tests/operations-v1-contracts.test.mjs`
    - Selectors: SHA-256 result shape and Node test conventions.
    - Covers: O5, O10, O11.

## Decisions And Assumptions

- The parser choice is inherited from the closed human gate: direct parse5
  8.0.1. No new blocker decision exists.
- Export a class named `HtmlTransformEngine` with synchronous `replace(html)`
  and `append(currentHtml, fragmentHtml)` methods. Parsing and hashing are CPU
  operations with no I/O, so asynchronous wrappers would add no value.
- A result contains `html`, a UTF-8 `Buffer` named `bytes`, `byte_length`, and
  `sha256`. Later blob and operation services can consume the bytes directly.
- The engine owns deterministic transformation, structural invariants, and
  result metadata. Request/source/fragment/result admission remains with later
  operation services using the constants frozen by SWU-OV1-001.
- Ordinary malformed HTML is repaired by parse5 and represented in golden
  outputs. Typed errors cover invalid input types and a violated one-body tree
  invariant, not generic syntax rejection.
- Golden JSON fixtures store readable inputs and exact output strings/digests;
  the tests also inspect resulting structure where byte strings alone would be
  ambiguous.

## Write Scope

- Exact `parse5` dependency in `package.json` and `package-lock.json`.
- New `src/kernel/html-transform.mjs`.
- New transformer golden fixtures under `tests/fixtures/operations-transform/`.
- New `tests/operations-v1-transform.test.mjs`.
- `package.json` only for `test:operations-transform`.
- Task Session evidence and status synchronization after passing validation.

## Excluded

- Server routes, projector/event changes, storage or blobs, browser/UI changes.
- String or regular-expression HTML insertion, selectors, or regions.
- Script execution, resource loading, source-format preservation, and generic
  malformed-HTML rejection claims.
- Runtime operation admission and byte-limit enforcement beyond the existing
  SWU-OV1-001 helpers.

## Validation

1. `npm run test:operations-transform`
2. `npm run test:operations-contracts`
3. `npm run test:schemas`
4. `npm run validate:schemas`
5. `npm run test:canvas-contracts`
6. Scoped syntax, dependency-pin, fixture, and whitespace checks.

## Context Builder Result

- Files selected: 14 grouped source entries
- Obligation coverage: 12/12, 100 percent
- Strict coverage: pass
- Blockers: 0
- Fallback search: downstream transformer interface selectors only; resolved
- Noise: bounded to explicit task sources and two downstream consumers
