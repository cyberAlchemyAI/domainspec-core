---
id: ide-extension-operations-v1-work-pack
project: ide-extension
title: "Operations V1 Work Pack"
status: ready
node_type: work-pack
updatedAt: 2026-07-12
planning_gate_status: pass
complexity: medium
output_mode: split
active_layer: L0
execution_pack_ref: EXECUTION-PACK.md
layering_artifact_ref: IMPLEMENTATION-LAYERING.md
distill_validation_status: pass
---

# Work Pack: Operations V1

## Objective

Implement and prove this trusted-local loop without changing the existing V0
publication API:

```text
exact V0 revision
  -> separate immutable operations surface
  -> retry-safe whole-document operation
  -> committed complete revision
  -> explicit workbench display
  -> user interaction and later operation
```

Success means the complete claim in the accepted architecture is supported by
restart, retry, concurrency, browser, retention, and V0 compatibility evidence.

## Source Contracts

- [Accepted architecture](../operations-v1-design/ARCHITECTURE-BUNDLE.md)
- [Decision ledger](../operations-v1-design/DECISIONS.md)
- [Closed planning gate](../operations-v1-design/PLANNING-DECISION-GATE.md)
- [Layering seed](../operations-v1-design/IMPLEMENTATION-LAYERING-SEED.md)
- [Design Distill validation](../operations-v1-design/DISTILL-VALIDATION.md)
- [Current V0 repair closeout](../v0-canvas-repair-plan/work-pack/evidence/SWU-VCR-004-REPORT.md)

## Delivery Boundary

**Included:** parser-backed whole-document append/replace/rebuild, exact V0
derivation, immutable content blobs, event-derived replay, CAS/idempotency,
explicit navigation, browser delivery, threshold-and-grace pruning, CLI and
browser value proof.

**Excluded:** declared regions, string/regex HTML mutation, collaboration,
automatic merge/rebase, per-browser display targets, durable refresh history,
remote browser control, provider execution, and protected effects.

## Delivery Slices

| Slice | Outcome | Layer | Wave | Validation |
| --- | --- | --- | --- | --- |
| OV1-S1 | Versioned contracts and deterministic parse5 transformations are frozen. | L0 | [W0](work-pack/waves/W0.md) | Schema boundaries and golden serializer fixtures pass. |
| OV1-S2 | Immutable blobs and additive event replay preserve exact bodies. | L0 | [W1](work-pack/waves/W1.md) | Dedupe, crash residue, mixed replay, reference validation, and restart pass. |
| OV1-S3 | Exact derivation and replacement prove the smallest coherent value loop. | L0 | [W2](work-pack/waves/W2.md) | Derive/replace/CAS/idempotency/content/V0 compatibility matrix passes. |
| OV1-S4 | Append is deterministic and exactly-once under retries and concurrency. | L1 | [W3](work-pack/waves/W3.md) | Fragment, duplicate, conflict, stale, and interactive output tests pass. |
| OV1-S5 | Rebuild and explicit navigation control one durable workbench target. | L2 | [W4](work-pack/waves/W4.md) | Drift, display restart, refresh acknowledgement, selected/non-selected, and browser tests pass. |
| OV1-S6 | Manual grace and automatic reclamation bound storage without silent loss. | L2 | [W5](work-pack/waves/W5.md) | Diagnostics, preview, tombstone, shared-ref, timer, hard-limit, 410, and retry-after-prune tests pass. |
| OV1-S7 | Agent CLI and browser evidence prove the complete user workflow and close traceability. | L2 | [W6](work-pack/waves/W6.md) | Real value witness, full Node/Playwright suites, schema/dispatch checks, and scoped audit pass. |

## Task Board

| Task | Goal | Layer | Waves | Gate | Status |
| --- | --- | --- | --- | --- | --- |
| [TASK-CONTRACT-TRANSFORM](work-pack/tasks/TASK-CONTRACT-TRANSFORM.md) | Freeze schemas, budgets, parse5 behavior, and golden bytes. | L0 | W0 | ready | not-started |
| [TASK-BLOB-REPLAY](work-pack/tasks/TASK-BLOB-REPLAY.md) | Add immutable body storage and additive event/projection replay. | L0 | W1 | blocked on 002 | not-started |
| [TASK-DERIVE-REPLACE](work-pack/tasks/TASK-DERIVE-REPLACE.md) | Derive exact V0 bytes and commit one CAS replacement. | L0 | W2 | blocked on 004 | not-started |
| [TASK-APPEND](work-pack/tasks/TASK-APPEND.md) | Append one parser fragment exactly once. | L1 | W3 | blocked on L0 | not-started |
| [TASK-REBUILD-NAVIGATION](work-pack/tasks/TASK-REBUILD-NAVIGATION.md) | Rebuild explicitly and deliver one durable display target. | L2 | W4 | blocked on 007 | not-started |
| [TASK-RETENTION](work-pack/tasks/TASK-RETENTION.md) | Ask, preview, tombstone, and automatically reclaim under policy. | L2 | W5 | blocked on 010 | not-started |
| [TASK-VALUE-VERIFY](work-pack/tasks/TASK-VALUE-VERIFY.md) | Prove the agent-to-workbench workflow and close the package. | L2 | W6 | blocked on 012 | not-started |

## SWU Manifest

| SWU | Parent | Goal | Dependencies | Write scope summary | Acceptance evidence | Verification | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-OV1-001 | [TASK-CONTRACT-TRANSFORM](work-pack/tasks/TASK-CONTRACT-TRANSFORM.md) | Add V1 request schemas, fixed budgets, event vocabulary, and boundary fixtures. | none | schemas, schema registry/fixtures/tests, contract constants, package scripts | Exact minus/exact/plus boundaries and additional-property rejection | `npm run test:operations-contracts` | local-fallback | ready |
| SWU-OV1-002 | [TASK-CONTRACT-TRANSFORM](work-pack/tasks/TASK-CONTRACT-TRANSFORM.md) | Pin parse5 8.0.1 and freeze document/fragment serialization. | 001 | package files, transform adapter, golden fixtures/tests | Golden bytes and inert-script/parser corpus | `npm run test:operations-transform` | local-fallback | blocked-dependency |
| SWU-OV1-003 | [TASK-BLOB-REPLAY](work-pack/tasks/TASK-BLOB-REPLAY.md) | Add atomic content-addressed blob storage and diagnostics. | 002 | new blob module and focused tests | Dedupe, atomic cleanup, read, stats, proven-orphan inventory | `npm run test:operations-blobs` | local-fallback | blocked-dependency |
| SWU-OV1-004 | [TASK-BLOB-REPLAY](work-pack/tasks/TASK-BLOB-REPLAY.md) | Add additive V4 events/projection and blob-reference reconciliation. | 003 | projector/storage/schema fixtures and replay tests | Mixed V1-V4 replay, restart repair, missing-body fail-closed | `npm run test:operations-replay` | local-fallback | blocked-dependency |
| SWU-OV1-005 | [TASK-DERIVE-REPLACE](work-pack/tasks/TASK-DERIVE-REPLACE.md) | Derive one immutable operations surface from an exact V0 revision. | 004 | operations service, server routes, CLI, focused API tests | Exact bytes, drift rejection, idempotency key conflict, no redirect | `npm run test:operations-derive` | local-fallback | blocked-dependency |
| SWU-OV1-006 | [TASK-DERIVE-REPLACE](work-pack/tasks/TASK-DERIVE-REPLACE.md) | Apply one CAS/idempotent replacement and serve it after restart. | 005 | operation service/route/content route and tests | Replace, stale, same-id same/different-input, append-failure residue, V0 parity | `npm run test:operations-replace` | local-fallback | blocked-dependency |
| SWU-OV1-007 | [TASK-APPEND](work-pack/tasks/TASK-APPEND.md) | Append a body-context fragment once under retries and concurrency. | 006 | transform/service and append/concurrency tests | Ordered nodes, malformed/table/SVG/script corpus, duplicate and stale matrix | `npm run test:operations-append` | local-fallback | blocked-dependency |
| SWU-OV1-008 | [TASK-REBUILD-NAVIGATION](work-pack/tasks/TASK-REBUILD-NAVIGATION.md) | Rebuild from an exact-hash workspace source with lineage. | 007 | service/server/CLI and rebuild tests | Exact source, drift/escape/size rejection, lineage, stable surface id | `npm run test:operations-rebuild` | local-fallback | blocked-dependency |
| SWU-OV1-009 | [TASK-REBUILD-NAVIGATION](work-pack/tasks/TASK-REBUILD-NAVIGATION.md) | Add durable redirect target and transient refresh/ack runtime. | 008 | projector, notification hub, server routes, navigation tests | Redirect restart/idempotency; refresh expiry; V0 current unchanged | `npm run test:operations-navigation` | local-fallback | blocked-dependency |
| SWU-OV1-010 | [TASK-REBUILD-NAVIGATION](work-pack/tasks/TASK-REBUILD-NAVIGATION.md) | Make the browser load the display projection and acknowledge navigation. | 009 | `l0.html`, interaction binding, Node/Playwright tests | Old-frame retention, selected-only reload, reconnect, desktop/mobile | `npm run test:e2e:operations-navigation` | local-fallback | blocked-dependency |
| SWU-OV1-011 | [TASK-RETENTION](work-pack/tasks/TASK-RETENTION.md) | Add diagnostics, soft-threshold grace, preview, and manual prune. | 010 | retention coordinator, projector/events, API/UI, tests | 1 GiB/7-day policy, candidate digest, tombstone-before-delete, 410 | `npm run test:operations-retention` | local-fallback | blocked-dependency |
| SWU-OV1-012 | [TASK-RETENTION](work-pack/tasks/TASK-RETENTION.md) | Add hard/expired-grace automatic reclamation and restart recovery. | 011 | scheduler/startup/commit hooks and policy tests | 2 GiB trigger, expired grace, orphan-first, shared refs, fail-closed history | `npm run test:operations-retention-auto` | local-fallback | blocked-dependency |
| SWU-OV1-013 | [TASK-VALUE-VERIFY](work-pack/tasks/TASK-VALUE-VERIFY.md) | Add agent CLI commands and retain a create/append/show interactive witness. | 012 | session bridge CLI, fixtures/e2e/evidence only | CLI JSON contracts plus real presentation append and browser interaction | `npm run test:operations-value` | local-fallback | blocked-dependency |
| SWU-OV1-014 | [TASK-VALUE-VERIFY](work-pack/tasks/TASK-VALUE-VERIFY.md) | Run integrated audit and synchronize plan evidence. | 013 | tests and plan evidence/status only | Full tests, schemas, dispatch, V0 parity, traceability, scoped diff | reviewable integrated report | local-fallback | blocked-dependency |

## Blockers And Gaps

| ID | Class | Description | Owner | Treatment |
| --- | --- | --- | --- | --- |
| GAP-OV1-001 | accepted limitation | Trusted local HTML may execute scripts when loaded by the browser. | product boundary | Keep parser execution inert; do not claim hostile HTML safety. |
| GAP-OV1-002 | accepted limitation | Transient refresh acknowledgement is lost on restart. | navigation task | Recover durable target; never replay stale refresh. |
| GAP-OV1-003 | intentional semantics | Pruned operation retries retain metadata but cannot return removed HTML. | retention task | Return explicit unavailable-body result and stable `410 revision_pruned`. |
| GAP-OV1-004 | deferred design | Region mutation and scaffolding semantics are unresolved. | future design | Exclude from all SWU write scopes and schemas. |
| GAP-OV1-005 | workspace | Repository contains unrelated concurrent changes. | all SWUs | Inspect exact scope, preserve intersecting changes, use scoped diffs. |

No acceptance-critical blocker remains. `SWU-OV1-001` is ready.

## Dispatch Technique Trace

| Technique | Applied to | Validation expectation | Status |
| --- | --- | --- | --- |
| `sequence` | Design gate -> W0-W6 -> Task Session | Every SWU consumes passed dependency evidence. | pass |
| `scu_swu_reduction` | Fourteen one-owner units | Each unit has one parent, bounded writes, done criteria, and command. | pass |
| `recomposition_proof` | 001-006 L0 and later layer promotion | L0 proves the accepted smallest coherent unit; L1/L2 preserve it. | pass |
| `validation_loop` | Every SWU and wave | Focused checks precede inherited and integrated suites. | pass |
| `owner_boundary_check` | Invoke -> Task Session -> project lifecycle | This package authors only; execution and promotion remain separate. | pass |
| `handle_handoff` | Task/SWU source anchors | Workers consume paths and headings, not copied private context. | pass |
| `residue_ledger` | Gaps and deferred regions | Every residue has an owner and route. | pass |
| `execution_receipt_handoff` | One-SWU Task Sessions | Every unit returns the standard structured receipt. | pass |
| `concrete_path_evidence` | Validation and closeout | Completion claims cite files, commands, and retained reports. | pass |
| `authority_split_gate` | Trusted preview versus protected effects | Canvas operations never grant shell/provider/domain authority. | pass |
| `observability_grouping` | Invoke plan and later SWUs | Runs use the Operations V1 package and SWU id. | pass |

Full route shape is in [operations-v1-plan.dispatch.json](operations-v1-plan.dispatch.json).

## Distill Validation

| Check | Result | Evidence |
| --- | --- | --- |
| Smallest coherent unit | pass | `SWU-OV1-001` through `006` recompose to derive plus replacement after restart. |
| SWU executability | pass | Fourteen units have one parent, dependencies, write scope, evidence, command, and owner. |
| Recomposition | pass | L1 append and L2 rebuild/navigation/retention preserve L0 identities and blob authority. |
| Hidden acceptance-critical gaps | pass | Parser, limits, retention, and navigation blockers are resolved in the closed gate. |
| Deferred complexity | pass | Regions, merge, collaboration, remote control, and per-browser targets remain excluded. |
| First-unit navigation | pass | Start with `SWU-OV1-001` in `TASK-CONTRACT-TRANSFORM.md`. |

## Gate Checks

1. Execute exactly one selected SWU per Task Session.
2. Do not begin a dependent SWU without a synchronized pass receipt.
3. Keep `/api/canvas/publish` and `/api/canvas/current` V0-compatible; use a
   separate display projection for Operations V1 workbench selection.
4. Write every referenced blob durably before its event append.
5. Reject payload/source/result overflows before blob or event commit.
6. Never implement HTML mutation with strings or regular expressions.
7. Never rebase or merge a stale operation automatically.
8. Do not delete a referenced blob before a durable prune tombstone.
9. Preserve the current revision and all shared unpruned blob references.
10. Do not add regions, protected effects, remote control, or provider calls.
11. Browser failure preserves the previously loaded complete revision.
12. Unknown or malformed replay history disables automatic reclamation.

## Expected Result Shape

```yaml
swu_id: SWU-OV1-NNN
result: pass | flag | block | interrupted
capability_ref: task-session
receipt_kind: native-stage | subagent | local-fallback | blocked
receipt_artifact: path-or-none
files_touched: []
validation: []
blockers: []
residue: []
reroute: next-swu-or-none
handoff_note: concise continuation state
```

## Next Route

```text
task-session SWU-OV1-001
```
