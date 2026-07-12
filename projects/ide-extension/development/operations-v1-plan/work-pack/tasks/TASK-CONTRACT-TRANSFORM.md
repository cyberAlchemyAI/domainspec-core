# Task Contract: Operations Contracts And HTML Transform

## Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-CONTRACT-TRANSFORM` |
| Objective | Freeze V1 request, size, version, parser, and serializer behavior before durable state is introduced. |
| Layer / slice / wave | L0 / OV1-S1 / W0 |
| Execution owner | Task Session, one SWU at a time |

## Source Handles

- [Shared context](../shared/context.md)
- [Cross-task decisions](../shared/cross-task-decisions.md)
- [Closed planning gate](../../../operations-v1-design/PLANNING-DECISION-GATE.md)
- `projects/ide-extension/src/kernel/schema-validation.mjs`
- `projects/ide-extension/scripts/validate-schemas.mjs`
- `projects/ide-extension/tests/session-content-workbench-contracts.test.mjs`

## SWU-OV1-001: Versioned Contract And Budget Baseline

**Goal:** add exact JSON contracts and UTF-8 admission constants without adding
runtime routes or events.

**Dependencies:** none.

**Exact write scope:** new Operations V1 schemas and valid/invalid fixtures,
`src/kernel/schema-validation.mjs`, a new contract/constants module, focused
contract tests, and `package.json` only for named focused test scripts.

**Inputs:** accepted `ContentOperation`, derivation, navigation, acknowledgement,
and pruning shapes plus OVG-002/003/004 decisions.

**Outputs:** strict schemas and frozen constants for:

- operation-surface derivation;
- content operation (`append | replace | rebuild`, whole document only);
- navigation (`redirect | refresh`) and transient acknowledgement;
- pruning preview/commit requests;
- 5 MiB HTTP, 4 MiB source, 512 KiB fragment, 8 MiB result;
- 1 GiB soft, 2 GiB hard, seven-day grace, reclaim-below-soft;
- additive Operations V1 event version `4` vocabulary.

**Implementation detail:** schemas use `additionalProperties: false`, bounded
identifier patterns, discriminated input kinds, and mode/input compatibility.
`append` and `replace` require `inline_html`; `rebuild` requires
`workspace_html`; target accepts only `{ "kind": "whole_document" }`.
Byte limits are checked in runtime helpers using `Buffer.byteLength(value,
'utf8')`; schema character counts are not treated as byte authority.

**Boundary matrix:** limit minus one and exact limit admit; plus one rejects.
Include multibyte UTF-8 fixtures, wrong mode/input pair, region target,
additional property, invalid id, missing digest, and invalid navigation target.

**Failure modes:** do not add permissive fallback schemas, environment overrides,
runtime route branches, events, blobs, or parser behavior in this SWU.

**Done criteria:** schema registry, fixtures, constants, and focused tests agree;
all existing schemas still validate.

**Validation:** `npm run validate:schemas`, `npm run test:schemas`, and
`npm run test:operations-contracts` from `projects/ide-extension`.

**Execution owner:** local fallback. **Expected result:** structured Task Session
receipt with fixture counts and exact constants. **Handoff:** SWU-OV1-002.

## SWU-OV1-002: parse5 Transformer And Golden Bytes

**Goal:** pin one standards-capable transformer and freeze emitted bytes for
complete documents and body-context fragments.

**Dependencies:** SWU-OV1-001 pass.

**Exact write scope:** `package.json`, lockfile, new
`src/kernel/html-transform.mjs`, transform fixtures/tests, and Task Session
evidence. Server, projector, storage, and browser are read-only.

**Inputs:** complete HTML bytes or current complete document plus fragment.

**Outputs:** `HtmlTransformEngine` methods for parse/serialize replacement and
append, with no script execution or subresource loading.

**Algorithm:**

1. Install exact `parse5` version `8.0.1` without a range.
2. Parse complete documents with parse5 document mode.
3. For append, parse current bytes as a document, locate exactly one body node,
   create a body-context fragment, and append its nodes in input order.
4. Serialize the full document once; return UTF-8 bytes plus byte length and
   SHA-256.
5. Reject a structurally unusable current tree with a typed transform error.
6. Never execute script nodes or fetch resources.

**Golden corpus:** doctype and implied document elements; malformed nesting;
comments; script/style text containing closing-tag-like strings; table-related
fragments; SVG/MathML; Unicode; empty fragment; multiple sibling nodes; body
attributes; and repeated serialization determinism.

**Edge cases:** parse5 repairs malformed HTML rather than throwing for ordinary
syntax errors. Tests must assert emitted bytes and structure instead of claiming
generic malformed HTML rejection.

**Failure modes:** no regex/string insertion, Cheerio/jsdom, DOM script
execution, source-format preservation claim, or region selector helper.

**Done criteria:** lockfile pins parse5 8.0.1, golden outputs are reviewed and
stable, and two identical transformations emit identical bytes/digests.

**Validation:** `npm run test:operations-transform` and inherited schema tests.

**Execution owner:** local fallback. **Expected result:** parser version, golden
fixture list, test count, and digest evidence. **Handoff:** SWU-OV1-003.

## Synchronization

Only Task Session receipts advance status. Any serializer fixture change after
SWU-OV1-002 requires an explicit migration note because revision digests depend
on emitted bytes.
