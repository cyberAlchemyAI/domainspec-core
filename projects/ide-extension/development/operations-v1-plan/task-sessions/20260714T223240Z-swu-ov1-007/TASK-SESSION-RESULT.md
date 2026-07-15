# Task Session Result: SWU-OV1-007

```yaml
swu_id: SWU-OV1-007
result: pass
capability_ref: task-session
receipt_kind: local-fallback
receipt_artifact: development/operations-v1-plan/task-sessions/20260714T223240Z-swu-ov1-007/TASK-SESSION-RESULT.md
files_touched:
  - package.json
  - src/kernel/operations.mjs
  - src/server.mjs
  - tests/operations-v1-append.test.mjs
  - tests/e2e/operations-v1-append.spec.mjs
  - tests/operations-v1-replace.test.mjs
validation:
  - npm run test:operations-append: pass
  - npm run test:e2e:operations-append: pass
  - npm run test:operations-replace: pass
  - npm run test:operations-transform: pass
  - npm run test:operations-replay: pass
  - npm run test:operations-derive: pass
  - npm run test:canvas-publish: pass
  - npm run test:canvas-replay: pass
  - npm run test:canvas-paths: pass
  - npm run test:persistence: pass
  - Node syntax and scoped whitespace checks: pass
blockers: []
residue:
  - Rebuild and durable navigation remain deferred to W4.
  - Browser proof loads the committed content URL directly; workbench frame routing to Operations display state remains deferred.
  - Trusted-local appended scripts execute when loaded; hostile HTML safety is not claimed.
  - Invalid UTF-8 Operations content fails append explicitly rather than being silently normalized.
  - Unrelated concurrent worktree changes remain preserved outside this SWU.
reroute: SWU-OV1-008
handoff_note: Reuse the generic operation/CLI path for exact-hash workspace rebuild while preserving Operations surface identity and lineage.
```

## Result

PASS. The generic content-operation route and CLI now admit body-context
`append` alongside `replace` without a second protocol. Append keeps the proven
operation-id lookup before CAS, exact retry, conflict, stale rejection, blob-
before-event, immutable content, and selected-surface-only notice behavior.

For a new append operation, the service enforces the 512 KiB UTF-8 fragment
limit, reads the current verified blob, requires a lossless UTF-8 round trip,
parses the current complete document and fragment in body context with parse5
8.0.1, appends parsed nodes in input order, serializes one complete document,
and enforces the 8 MiB result limit before commit. The normal V4 content event
records only digests and metadata.

The focused corpus covers empty fragments, text and multiple elements,
scripts/styles, malformed nesting, table-like markup, comments, Unicode,
SVG/MathML, duplicate retry, id conflict, stale input, two concurrent writers,
fragment/result limits, invalid UTF-8 current content, append-failure orphan,
and projection-failure repair.

## Browser Witness

Playwright loaded the committed appended revision directly in real Chromium on
desktop and mobile. The page retained its original content and appended a
button, output, and script in document order. Clicking the appended control
changed the output from `idle` to `active` and set a body witness attribute,
proving that the server committed one complete interactive HTML revision rather
than a partial or inert fragment stream.

## Compatibility Recovery

Enabling append correctly invalidated one old SWU-006 assertion that append was
unavailable. That obsolete assertion was removed; all replacement-specific
rebuild, binding, limit, CAS, retry, content, recovery, CLI, and 410 checks
remain and pass.

## Validation Evidence

| Command | Result |
| --- | --- |
| `npm run test:operations-append` | PASS: 5 tests. |
| `npm run test:e2e:operations-append` | PASS: 2 Chromium projects. |
| `npm run test:operations-replace` | PASS: 7 tests. |
| `npm run test:operations-transform` | PASS: 6 tests. |
| `npm run test:operations-replay` | PASS: 8 tests. |
| `npm run test:operations-derive` | PASS: 6 tests. |
| `npm run test:canvas-publish` | PASS: 4 tests. |
| `npm run test:canvas-replay` | PASS: 4 tests. |
| `npm run test:canvas-paths` | PASS: 5 tests. |
| `npm run test:persistence` | PASS: 6 tests. |
| Service/server/test syntax checks | PASS. |
| Scoped `git diff --check` | PASS. |

## Session Metadata

- Context pack: [CONTEXT-PACK.md](CONTEXT-PACK.md)
- Gate: [GATE.md](GATE.md)
- Strict context coverage: pass, 12/12 obligations
- Gate verdict: pass
- Runtime: local
- Handoff: none
- Subagents: not applicable; started 0, completed 0, failed 0, blocked 0
- Experiment harness: not applicable
- L1 promotion recommendation: pass
- Next bounded unit: `SWU-OV1-008`
