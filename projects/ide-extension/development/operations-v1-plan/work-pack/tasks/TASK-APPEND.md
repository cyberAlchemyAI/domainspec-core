# Task Contract: Parser Append And Retry

## Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-APPEND` |
| Objective | Append one HTML fragment exactly once under retries and concurrency. |
| Layer / slice / wave | L1 / OV1-S4 / W3 |
| Execution owner | Task Session, one SWU |

## Source Handles

- [Content operation contract](../../../operations-v1-design/ARCHITECTURE-BUNDLE.md#content-operation-contract)
- [Transformer task](TASK-CONTRACT-TRANSFORM.md)
- [Replacement task](TASK-DERIVE-REPLACE.md)

## SWU-OV1-007: Body-Context Append

**Goal:** transform current immutable bytes plus one fragment into one new
complete revision without duplicate application.

**Dependencies:** SWU-OV1-006 pass and L0 promotion evidence.

**Exact write scope:** transform adapter append path, operations service append
branch, focused parser/idempotency/concurrency/browser-structure tests, and Task
Session evidence.

**Algorithm:**

1. Apply the same normalized-digest and operation-id-before-CAS sequence proven
   by replacement.
2. Enforce 512 KiB UTF-8 fragment limit.
3. Read and verify current immutable blob bytes.
4. Parse current bytes as a document and fragment in body context.
5. Append parsed nodes to body in input order and serialize the full document.
6. Enforce 8 MiB complete-result limit before blob/event commit.
7. Store and append one normal content-operation event.

**Test corpus:** empty fragment; text and multiple elements; scripts/styles;
malformed nesting; table-context-like markup; comments; Unicode; SVG/MathML;
missing/implied body; exact duplicate retry; id conflict; two concurrent writers;
and a fragment that crosses the result limit after serialization.

**Failure modes:** no raw string insertion, auto-rebase, merge, partial stream,
duplicate event, or notification for a non-displayed surface.

**Done criteria:** same request appends once, stale second writer rejects, and
the committed complete document executes its trusted-local interaction when
loaded in the browser harness.

**Validation:** `npm run test:operations-append`, focused Playwright append
fixture, and inherited L0/V0 suites.

**Execution owner:** local fallback. **Expected result:** exact retry/concurrency
matrix and L1 promotion recommendation. **Handoff:** SWU-OV1-008.

## Synchronization

Any parser golden-output change must be reconciled with SWU-OV1-002 evidence;
append cannot silently redefine replacement serialization.
