# Task Session Result: SWU-OV1-002

```yaml
swu_id: SWU-OV1-002
result: pass
capability_ref: task-session
receipt_kind: local-fallback
receipt_artifact: development/operations-v1-plan/task-sessions/20260714T213203Z-swu-ov1-002/TASK-SESSION-RESULT.md
files_touched:
  - package.json
  - package-lock.json
  - src/kernel/html-transform.mjs
  - tests/fixtures/operations-transform/golden.json
  - tests/operations-v1-transform.test.mjs
validation:
  - npm run test:operations-transform: pass
  - npm run test:operations-contracts: pass
  - npm run test:schemas: pass
  - npm run validate:schemas: pass
  - npm run test:canvas-contracts: pass
  - npm run smoke: pass
  - npm run test:workbench: pass
  - Craft index source hash check: pass
  - npm ls parse5 entities: pass
  - Node syntax and fixture JSON checks: pass
  - scoped whitespace checks: pass
blockers: []
residue:
  - parse5 serialization is canonical for Operations V1 and intentionally does not preserve source formatting.
  - Unrelated concurrent worktree changes remain preserved outside this SWU.
reroute: SWU-OV1-003
handoff_note: Add the atomic content-addressed blob store without appending events.
```

## Result

PASS. The package now pins direct runtime dependency `parse5` at exactly 8.0.1
and exposes one deterministic `HtmlTransformEngine` for complete-document
replacement and body-context fragment append.

Every transform returns exact UTF-8 bytes, byte length, and SHA-256. Append
requires the parsed current document to contain exactly one HTML body, parses
the fragment in that body context, moves nodes in input order, and serializes
the complete document once. Parsing performs no script execution or resource
loading.

The reviewed golden corpus contains 12 cases: five complete documents and
seven appends. It covers doctypes and implied elements, malformed nesting,
comments, script/style text, tables, SVG/MathML, Unicode, empty fragments,
multiple siblings, and body attributes. Representative frozen digests include:

- document normalization: `b188287d7c83aeb6dd10367380797e7d5546f189c38d7cd7ba6099748e2455ce`;
- table append: `44e706adc4397ed62fc47fd09740a5a4fc9fa46ecac629e7b4b8df2f48c7579b`;
- SVG/MathML append: `8edccc00a46900b6f3265a1d8b5740083bb7e15308c85b6413bd29a28b8a3f16`.

## Decisions

- `HtmlTransformEngine.replace()` and `.append()` are synchronous because the
  engine performs CPU-only parsing, serialization, and hashing.
- Admission limits remain owned by the operation services that will consume
  the engine; this SWU freezes deterministic transform behavior and metadata.
- The package Node floor is now `>=20.19.0`, matching `entities@8`, the selected
  parser's transitive runtime requirement. The validated runtime is Node 22.12.

## Validation Evidence

| Command | Result |
| --- | --- |
| `npm run test:operations-transform` | PASS: 6 tests and 12 golden cases. |
| `npm run test:operations-contracts` | PASS: 8 tests. |
| `npm run test:schemas` | PASS: 6 tests. |
| `npm run validate:schemas` | PASS: 20 schemas, 6 manifests, 76 fixtures. |
| `npm run test:canvas-contracts` | PASS: 4 tests. |
| `npm run smoke` | PASS: 1 test. |
| `npm run test:workbench` | PASS: 6 tests, including stale-index refusal. |
| Craft index source hash check | PASS: generated index matches the canonical ledger. |
| `npm ls parse5 entities` | PASS: parse5 8.0.1, entities 8.0.0. |
| Syntax, JSON, and scoped whitespace checks | PASS. |

## Session Metadata

- Context pack: [CONTEXT-PACK.md](CONTEXT-PACK.md)
- Strict context coverage: pass, 12/12 obligations
- Gate: pass
- Runtime: local
- Handoff: none
- Subagents: not applicable; started 0, completed 0, failed 0, blocked 0
- Experiment harness: not applicable
- Decision Gate Result: not applicable; parser selection was inherited from the closed planning gate
- Next bounded unit: `SWU-OV1-003`
