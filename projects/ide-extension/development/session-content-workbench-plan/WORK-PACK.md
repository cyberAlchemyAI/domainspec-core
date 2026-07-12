---
id: ide-extension-session-content-workbench-work-pack
project: ide-extension
title: "Session Content Workbench Work Pack"
status: ready
node_type: work-pack
updatedAt: 2026-07-12
planning_gate_status: pass
active_layer: V0-C
---

# Work Pack: Session Content Workbench

## Objective

Implement and prove the generic trusted-local loop:

```text
Codex -> project HTML -> publish -> workbench -> user event -> poll -> Codex
```

## Delivery Slices

| Slice | Outcome | Layer | Wave | Validation |
| --- | --- | --- | --- | --- |
| S-001 | Canvas contracts and replay coexist with current bridge history. | V0-A | [W0](work-pack/waves/W0.md) | Schemas and replay pass. |
| S-002 | Existing HTML publishes and works after manual Refresh. | V0-A | [W1](work-pack/waves/W1.md) | API/CLI/UI/Playwright pass. |
| S-003 | Complete generated revisions update automatically. | V0-B | [W2](work-pack/waves/W2.md) | SSE/reconnect/revision tests pass. |
| S-004 | Decision and Craft actions return through generic events. | V0-C | [W3](work-pack/waves/W3.md) | API/CLI/browser round trips pass. |
| S-005 | Real Codex presentation and interaction witnesses demonstrate value. | V0-C | [W4](work-pack/waves/W4.md) | Retained manual evidence and closure pass. |

## Task Board

| Task | Goal | Layer | Wave | Status |
| --- | --- | --- | --- | --- |
| [TASK-CANVAS-CONTRACT](work-pack/tasks/TASK-CANVAS-CONTRACT.md) | Define schemas, state, and replay. | V0-A | W0 | completed |
| [TASK-PUBLISH-DISPLAY](work-pack/tasks/TASK-PUBLISH-DISPLAY.md) | Publish and display existing HTML manually. | V0-A | W1 | completed |
| [TASK-LIVE-UPDATE](work-pack/tasks/TASK-LIVE-UPDATE.md) | Automatically load complete revisions. | V0-B | W2 | completed |
| [TASK-INTERACTION-RETURN](work-pack/tasks/TASK-INTERACTION-RETURN.md) | Return generic user events to session polling. | V0-C | W3 | completed |
| [TASK-VALUE-WITNESSES](work-pack/tasks/TASK-VALUE-WITNESSES.md) | Prove generated presentation, Decision Gate, and Craft value. | V0-C | W3-W4 | in-progress |

## SWU Manifest

| SWU | Parent | Goal | Dependencies | Write scope | Validation | Status |
| --- | --- | --- | --- | --- | --- | --- |
| SWU-SCW-001 | [TASK-CANVAS-CONTRACT](work-pack/tasks/TASK-CANVAS-CONTRACT.md) | Add canvas contract, schemas, fixtures, and spec/architecture deltas. | none | `SPEC.md`, `ARCHITECTURE.md`, `schemas/`, schema registry/fixtures/tests, package scripts | [PASS: 14 schemas, 54 fixtures, focused contracts](task-sessions/20260712T134140Z-swu-scw-001/TASK-SESSION-RESULT.md) | completed |
| SWU-SCW-002 | [TASK-CANVAS-CONTRACT](work-pack/tasks/TASK-CANVAS-CONTRACT.md) | Add canvas event replay and projection state. | 001 | projector/storage fixtures and replay tests | [PASS: mixed v1/v2/v3, restart, 66 bridge tests](task-sessions/20260712T134539Z-swu-scw-002/TASK-SESSION-RESULT.md) | completed |
| SWU-SCW-003 | [TASK-PUBLISH-DISPLAY](work-pack/tasks/TASK-PUBLISH-DISPLAY.md) | Add publish/current/content APIs and CLI publish. | 002 | canvas kernel helper, server, CLI, API/CLI tests | [PASS: API/CLI, race, drift, restart, append failure](task-sessions/20260712T134934Z-swu-scw-003/TASK-SESSION-RESULT.md) | completed |
| SWU-SCW-004 | [TASK-PUBLISH-DISPLAY](work-pack/tasks/TASK-PUBLISH-DISPLAY.md) | Add full workbench canvas and manual Refresh witness. | 003 | `l0.html`, UI/e2e harness/spec | [PASS: real presentation, desktop/mobile, 6 browser journeys](task-sessions/20260712T135310Z-swu-scw-004/TASK-SESSION-RESULT.md) | completed |
| SWU-SCW-005 | [TASK-LIVE-UPDATE](work-pack/tasks/TASK-LIVE-UPDATE.md) | Add EventSource complete-revision notification and reload. | 004 | notification helper, server, UI, tests | [PASS: auto-update, duplicate, reconnect, restart, fallback](task-sessions/20260712T135927Z-swu-scw-005/TASK-SESSION-RESULT.md) | completed |
| SWU-SCW-006 | [TASK-INTERACTION-RETURN](work-pack/tasks/TASK-INTERACTION-RETURN.md) | Add interaction POST/store/poll API and CLI events. | 005 | schemas, projector/server/CLI, focused tests | [PASS: 16 KiB, bindings, retry, cursor, restart, CLI](task-sessions/20260712T140913Z-swu-scw-006/TASK-SESSION-RESULT.md) | completed |
| SWU-SCW-007 | [TASK-VALUE-WITNESSES](work-pack/tasks/TASK-VALUE-WITNESSES.md) | Add presentation, Decision Gate, and Craft automated HTML witnesses. | 006 | HTML fixtures, Node/Playwright specs, package scripts | [PASS: three surfaces, exact CLI payloads, six screenshots](task-sessions/20260712T141822Z-swu-scw-007/TASK-SESSION-RESULT.md) | completed |
| SWU-SCW-008 | [TASK-VALUE-WITNESSES](work-pack/tasks/TASK-VALUE-WITNESSES.md) | Run real Codex generated-presentation publish/update witness. | 007 | evidence/report/assets only | [BLOCK: machine proof passed; human usefulness review pending](task-sessions/20260712T142559Z-swu-scw-008/TASK-SESSION-RESULT.md) | blocked-human-review |
| SWU-SCW-009 | [TASK-VALUE-WITNESSES](work-pack/tasks/TASK-VALUE-WITNESSES.md) | Run real Decision Gate and Craft interaction/poll witness and close readiness. | 008 | evidence/report/assets and status synchronization only | real poll payloads and human value review | blocked-dependency |

## Blockers And Gaps

| ID | Type | Description | Owner | Treatment |
| --- | --- | --- | --- | --- |
| GAP-SCW-001 | snapshot | Workspace file is canonical; old revisions cannot be replayed after later edits. | V1 design | V0 content route detects hash drift; defer snapshots. |
| GAP-SCW-002 | session routing | V0 has one global canvas/event stream rather than authenticated per-session routing. | V1 design | Accept trusted-local singleton experiment. |
| GAP-SCW-003 | effect evidence | `craft.action.requested` does not prove Craft ran. | active session | Preserve separate task/result evidence. |
| GAP-SCW-004 | environment | SWU-008/009 require an active Codex session and human browser interaction. | witness owner | Return block rather than simulate. |
| GAP-SCW-005 | workspace | Repository contains unrelated changes. | unrelated owners | Use scoped checks; never clean or revert them. |

No gap blocks `SWU-SCW-001`.

## Gate Checks

1. Execute exactly one ready SWU per Task Session.
2. Preserve all existing bridge and v1/v2 replay tests.
3. Do not load HTML until its complete revision has committed.
4. Do not begin automatic update before manual display works.
5. Do not add skill-specific event APIs.
6. Do not claim Craft completion from a browser request event.
7. Do not simulate the two live witnesses.

## Expected Result Shape

```yaml
swu_id: SWU-SCW-NNN
result: pass | flag | block | interrupted
capability_ref: task-session
receipt_kind: native-stage | local-fallback | blocked
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
human review of projects/ide-extension/development/session-content-workbench-plan/work-pack/evidence/SWU-SCW-008-REPORT.md
```
