# Craft View - ide-extension

Human view of [.craft/ledger.yml](.craft/ledger.yml). The ledger is the source
of truth for project-local state.

## Root Context - CTX-IDEEXT-L0

**Stage:** validated
**Gate:** flag

**Purpose:** Prove an L0 governed IDE-adjacent workbench before claiming an IDE
agent, VS Code/VSCodium product, embedded browser automation surface, or unified
authority layer.

**Next move:** Record the human usefulness verdict for `SWU-WUI-011`. Preserve the older
`SWU-SCW-008` usefulness verdict as independent open residue.

## Active Product Context - CTX-IDEEXT-WUI-V1

**Stage:** planned
**Gate:** pass

Workbench UI V1 is the selected next increment. It recomposes the existing
approval desk, bridge, Canvas, Craft frontier, and evidence surfaces into one
Canvas-first agent-task workflow. Agent task becomes an explicit default mode;
Dry run becomes an explicit diagnostic mode.

The governed [V1 work pack](development/workbench-ui-v1/WORK-PACK.md) contains
eleven behavior-shaped SWUs. The first is
[SWU-WUI-001](development/workbench-ui-v1/work-pack/tasks/TASK-WUI-001-SHELL.md):
introduce semantic Work, Canvas, and Inspector regions without changing layout,
state projection, interactions, or existing kernel contracts.

`SWU-WUI-001` passed its semantic landmark and compatibility checks,
`SWU-WUI-002` passed the desktop grid and approval-workflow evidence, and
`SWU-WUI-003` passed mobile Work, Canvas, and Evidence navigation, and
`SWU-WUI-004` passed explicit Agent task/Dry run payload and compatibility
evidence, and `SWU-WUI-005` passed the pure RunView mapper matrix and full bridge
suite, and `SWU-WUI-006` passed the ordered lifecycle desktop/mobile matrix on
2026-07-20, and `SWU-WUI-007` passed the legal-action matrix and desktop/mobile
journey, and `SWU-WUI-008` passed the retained Canvas placement and old-frame
failure witness, and `SWU-WUI-009` passed read-only Craft frontier seeding, and
`SWU-WUI-010` passed receipt-linked Inspector evidence. The next bounded unit
is `SWU-WUI-011`, whose machine matrix passes but whose human usefulness gate
remains open.

V1 does not claim background agent wake-up, OpenRouter execution, browser
control, or VSCodium integration.

## Operations Plan

### Operations V1

[The Operations V1 work pack](development/operations-v1-plan/WORK-PACK.md) is
in progress with fourteen ordered SWUs. W0 through W5 passed. The workbench now
derives exact V0 bytes, replaces or appends through one CAS/idempotent operation
path, serves immutable revisions, and runs appended interaction in desktop and
mobile Chromium. `SWU-OV1-008` also rebuilds from an exact-hash workspace source
without implicit V0 synchronization. `SWU-OV1-009` adds durable display plus
transient refresh/ack; `SWU-OV1-010` proves atomic browser delivery, exact
acknowledgement, old-frame retention, and V4 interaction routing. `SWU-OV1-011`
adds replay-verified storage diagnostics, durable grace, deterministic preview,
and tombstone-before-delete manual pruning. `SWU-OV1-012` adds serialized
startup/post-commit/timer evaluation, orphan/temporary-first automatic cleanup,
hard and expired-grace triggers, and restart recovery. `SWU-OV1-013` passed its
CLI, desktop/mobile machine witness, and human usefulness gate. `SWU-OV1-014`
then passed the integrated audit. Operations V1 is complete for the accepted
trusted-local whole-document claim.

## Operations V1 Completion

The [integrated audit](development/operations-v1-plan/task-sessions/20260715T010811Z-swu-ov1-014/INTEGRATED-AUDIT.md)
records 187/187 Node tests, 18/18 desktop/mobile Playwright journeys, schema and
dispatch validation, complete OV1-D/OVG traceability, one resolved stale test
assertion, and no active Operations blocker. It explicitly excludes regions,
collaboration, automatic merge, hostile HTML safety, remote control, provider
execution, protected effects, and IDE embedding.

## Resolved Operations Value Gate

### DEC-IDEEXT-OV1-VALUE-USEFULNESS

The [machine witness](development/operations-v1-plan/task-sessions/20260715T004506Z-swu-ov1-013/MACHINE-WITNESS-REPORT.md)
proves publish, derive, replace, append, display, iframe interaction, and
restart recovery on desktop and mobile. The human selected Option 1 in the
[Decision Gate](development/operations-v1-plan/task-sessions/20260715T004506Z-swu-ov1-013/DECISION-GATE.md):
the bounded result is useful enough to enter integrated audit. Deferred L3
capabilities remain excluded.

## Closed Bridge Increment

[Workbench Bridge Demo V0.1](development/workbench-bridge-demo-v01/WORK-PACK.md)
is complete. The workbench shows prepare, approve, ready, claim, result, and
receipt state while preserving blind pre-claim disclosure. `workbench-poll`
v0.2.0 now continues from claim into the requested skill in the active session
by default; `--claim-only` preserves the transport-only diagnostic path.

## Resolved Retention Gate

### DEC-IDEEXT-OV1-PRUNING-COMPLETION

The human selected Option 1 in the
[Decision Gate](development/operations-v1-plan/task-sessions/20260714T234403Z-swu-ov1-012/DECISION-GATE.md).
Migration `OV1-EVENT-V4-M2` adds `canvas.pruning_completed` as the seventh V4
event, allowing replay to close an active request only after physical storage
is verified below soft. The
[migration note](development/operations-v1-plan/task-sessions/20260715T002431Z-swu-ov1-012-resume/EVENT-V4-MIGRATION.md)
preserves exact revision-tombstone meaning.

`SWU-OV1-012` passed its automatic, replay, persistence, and recovery matrix.
`SWU-OV1-013` passed machine evidence and the human usefulness review;
`SWU-OV1-014` passed integrated closeout.

## Resolved Contract Gate

### DEC-IDEEXT-OV1-V4-INTERACTION

The human selected Option 1 in the
[Decision Gate](development/operations-v1-plan/task-sessions/20260714T214740Z-swu-ov1-004/DECISION-GATE.md).
Migration `OV1-EVENT-V4-M1` reuses `canvas.interaction_recorded` for V4 and
keeps the V3 binding distinct through `event_version`. The
[migration note](development/operations-v1-plan/task-sessions/20260714T215322Z-swu-ov1-004-resume/EVENT-V4-MIGRATION.md)
is the authority for the six-name V4 vocabulary.

## Pending Human Gate

### GAP-IDEEXT-SCW-HUMAN-REVIEW

The [SWU-008 report](development/session-content-workbench-plan/work-pack/evidence/SWU-SCW-008-REPORT.md)
records a passing machine browser witness, but a person still needs to decide
whether receiving and operating the presentation in the workbench is more
useful than receiving it only in chat. This blocks the value-witness closeout
and `SWU-SCW-009`; it does not block Operations V1 execution.

## Decisions

### DEC-IDEEXT-WUI-V1-FRONTIER

Selected: Workbench UI V1, a Canvas-first operator workspace with Agent task as
the explicit default preparation mode.

Rationale: the bridge and operations foundations work, but live use showed that
implicit request mode and separate proof panels obscure the intended product
journey. The next value lies in coherent UI composition, not another backend
authority layer.

### DEC-IDEEXT-L0-BOUNDARY

Selected: local-server-first governed workbench.

Rationale: the evidence supports a loopback workbench with manifests,
approval-gated dry-run envelopes, and receipts. It does not yet support an
autonomous IDE agent or embedded VSCodium automation claim.

### DEC-IDEEXT-MODULES-NOT-KERNEL

Selected: Craft, Whisper, UI Studio, IDE Ergonomics, OpenRouter, OpenClaw,
Hermes, and ResonantOS precedents are modules/adapters, not kernel dependencies.

Rationale: kernel bloat would collapse the project into a renamed bundle of
prior surfaces instead of a distinct governed action boundary.

### DEC-IDEEXT-OV1-V4-INTERACTION

Selected: reuse `canvas.interaction_recorded` in V4; `event_version`
distinguishes the V3 and V4 bindings.

Rationale: one semantic event name is sufficient when each version keeps a
strict payload contract. Migration `OV1-EVENT-V4-M1` records the compatible
change from five to six V4 event names.

### DEC-IDEEXT-OV1-PRUNING-COMPLETION

Selected: add exact `canvas.pruning_completed` semantics through migration
`OV1-EVENT-V4-M2`.

Rationale: cleanup-only convergence needs a durable transition without
fabricating a revision tombstone or deriving authoritative state from disk.

### DEC-IDEEXT-OV1-VALUE-USEFULNESS

Selected: Option 1. The retained desktop/mobile Operations V1 workbench result
is useful enough for integrated closeout; this does not approve deferred L3.

## Active Gaps

- GAP-IDEEXT-PLAYWRIGHT-MCP: Playwright MCP has not yet driven the local
  workbench.
- GAP-IDEEXT-VSCODIUM-WEBVIEW: embedded VSCodium webview automation is not
  locally witnessed.
- GAP-IDEEXT-MANIFEST-VALIDATOR: schemas exist, but the manifest validator is
  minimal and should grow failing invalid-fixture tests.
- GAP-IDEEXT-PROVIDER-ADAPTER: OpenRouter adapter is a boundary stub; no live
  key handling or streaming proof yet.
- GAP-IDEEXT-SCW-HUMAN-REVIEW: machine evidence passed, but the workbench value
  claim still requires a real human usefulness verdict.

## Pending By Node

### CTX-IDEEXT-L0 - flag

- Operations V1: complete for the accepted trusted-local whole-document claim.
- Workbench Bridge Demo V0.1: complete.
- Selected child: `CTX-IDEEXT-WUI-V1`.
- Human gate: close `GAP-IDEEXT-SCW-HUMAN-REVIEW`, then run `SWU-SCW-009`.
- Deferred evidence: Playwright MCP and embedded VSCodium webview proof.
- Separate adapter work: manifest hardening evidence and live OpenRouter proof.

### CTX-IDEEXT-WUI-V1 - in_progress

- Plan: [Workbench UI V1](development/workbench-ui-v1/WORK-PACK.md).
- Ready unit: `SWU-WUI-011`.
- Next move: record the explicit human usefulness verdict for the already-green
  WUI-011 machine matrix without claiming deferred integrations.
- Final gate: desktop/mobile machine evidence plus explicit human usefulness review.

## Artifacts

- [README.md](README.md)
- [SPEC.md](SPEC.md)
- [ARCHITECTURE.md](ARCHITECTURE.md)
- [development/founding-research/research.md](development/founding-research/research.md)
- [development/founding-research/findings.md](development/founding-research/findings.md)
- [schemas/](schemas/)
- [public/demo/l0.html](public/demo/l0.html)
- [development/operations-v1-plan/WORK-PACK.md](development/operations-v1-plan/WORK-PACK.md)
- [development/workbench-bridge-demo-v01/WORK-PACK.md](development/workbench-bridge-demo-v01/WORK-PACK.md)
- [development/workbench-ui-v1/WORK-PACK.md](development/workbench-ui-v1/WORK-PACK.md)
- [development/workbench-ui-v1/task-sessions/20260720T153545Z-swu-wui-001/CONTEXT-PACK.md](development/workbench-ui-v1/task-sessions/20260720T153545Z-swu-wui-001/CONTEXT-PACK.md)
- [development/workbench-ui-v1/task-sessions/20260720T153545Z-swu-wui-001/TASK-SESSION-RESULT.md](development/workbench-ui-v1/task-sessions/20260720T153545Z-swu-wui-001/TASK-SESSION-RESULT.md)
- [development/workbench-ui-v1/task-sessions/20260720T154814Z-swu-wui-002/CONTEXT-PACK.md](development/workbench-ui-v1/task-sessions/20260720T154814Z-swu-wui-002/CONTEXT-PACK.md)
- [development/workbench-ui-v1/task-sessions/20260720T154814Z-swu-wui-002/TASK-SESSION-RESULT.md](development/workbench-ui-v1/task-sessions/20260720T154814Z-swu-wui-002/TASK-SESSION-RESULT.md)
- [development/workbench-ui-v1/task-sessions/20260720T155936Z-swu-wui-003/CONTEXT-PACK.md](development/workbench-ui-v1/task-sessions/20260720T155936Z-swu-wui-003/CONTEXT-PACK.md)
- [development/workbench-ui-v1/task-sessions/20260720T155936Z-swu-wui-003/TASK-SESSION-RESULT.md](development/workbench-ui-v1/task-sessions/20260720T155936Z-swu-wui-003/TASK-SESSION-RESULT.md)
- [development/workbench-ui-v1/task-sessions/20260720T161007Z-swu-wui-004/CONTEXT-PACK.md](development/workbench-ui-v1/task-sessions/20260720T161007Z-swu-wui-004/CONTEXT-PACK.md)
- [development/workbench-ui-v1/task-sessions/20260720T161007Z-swu-wui-004/TASK-SESSION-RESULT.md](development/workbench-ui-v1/task-sessions/20260720T161007Z-swu-wui-004/TASK-SESSION-RESULT.md)
- [development/workbench-ui-v1/task-sessions/20260720T161925Z-swu-wui-005/CONTEXT-PACK.md](development/workbench-ui-v1/task-sessions/20260720T161925Z-swu-wui-005/CONTEXT-PACK.md)
- [development/workbench-ui-v1/task-sessions/20260720T161925Z-swu-wui-005/TASK-SESSION-RESULT.md](development/workbench-ui-v1/task-sessions/20260720T161925Z-swu-wui-005/TASK-SESSION-RESULT.md)
- [development/workbench-ui-v1/task-sessions/20260720T162753Z-swu-wui-006/CONTEXT-PACK.md](development/workbench-ui-v1/task-sessions/20260720T162753Z-swu-wui-006/CONTEXT-PACK.md)
- [development/workbench-ui-v1/task-sessions/20260720T162753Z-swu-wui-006/TASK-SESSION-RESULT.md](development/workbench-ui-v1/task-sessions/20260720T162753Z-swu-wui-006/TASK-SESSION-RESULT.md)
- [development/workbench-ui-v1/task-sessions/20260720T164437Z-swu-wui-007/CONTEXT-PACK.md](development/workbench-ui-v1/task-sessions/20260720T164437Z-swu-wui-007/CONTEXT-PACK.md)
- [development/workbench-ui-v1/task-sessions/20260720T164437Z-swu-wui-007/TASK-SESSION-RESULT.md](development/workbench-ui-v1/task-sessions/20260720T164437Z-swu-wui-007/TASK-SESSION-RESULT.md)
- [development/workbench-ui-v1/task-sessions/20260720T165903Z-swu-wui-008/CONTEXT-PACK.md](development/workbench-ui-v1/task-sessions/20260720T165903Z-swu-wui-008/CONTEXT-PACK.md)
- [development/workbench-ui-v1/task-sessions/20260720T165903Z-swu-wui-008/TASK-SESSION-RESULT.md](development/workbench-ui-v1/task-sessions/20260720T165903Z-swu-wui-008/TASK-SESSION-RESULT.md)
- [development/operations-v1-plan/task-sessions/20260714T211557Z-swu-ov1-001/TASK-SESSION-RESULT.md](development/operations-v1-plan/task-sessions/20260714T211557Z-swu-ov1-001/TASK-SESSION-RESULT.md)
- [development/operations-v1-plan/task-sessions/20260714T213203Z-swu-ov1-002/TASK-SESSION-RESULT.md](development/operations-v1-plan/task-sessions/20260714T213203Z-swu-ov1-002/TASK-SESSION-RESULT.md)
- [development/operations-v1-plan/task-sessions/20260714T214040Z-swu-ov1-003/TASK-SESSION-RESULT.md](development/operations-v1-plan/task-sessions/20260714T214040Z-swu-ov1-003/TASK-SESSION-RESULT.md)
- [development/operations-v1-plan/task-sessions/20260714T214740Z-swu-ov1-004/TASK-SESSION-RESULT.md](development/operations-v1-plan/task-sessions/20260714T214740Z-swu-ov1-004/TASK-SESSION-RESULT.md)
- [development/operations-v1-plan/task-sessions/20260714T214740Z-swu-ov1-004/DECISION-GATE.md](development/operations-v1-plan/task-sessions/20260714T214740Z-swu-ov1-004/DECISION-GATE.md)
- [development/operations-v1-plan/task-sessions/20260714T224033Z-swu-ov1-008/TASK-SESSION-RESULT.md](development/operations-v1-plan/task-sessions/20260714T224033Z-swu-ov1-008/TASK-SESSION-RESULT.md)
- [development/operations-v1-plan/task-sessions/20260714T224925Z-swu-ov1-009/TASK-SESSION-RESULT.md](development/operations-v1-plan/task-sessions/20260714T224925Z-swu-ov1-009/TASK-SESSION-RESULT.md)
- [development/operations-v1-plan/task-sessions/20260714T230133Z-swu-ov1-010/TASK-SESSION-RESULT.md](development/operations-v1-plan/task-sessions/20260714T230133Z-swu-ov1-010/TASK-SESSION-RESULT.md)
- [development/operations-v1-plan/task-sessions/20260714T232409Z-swu-ov1-011/TASK-SESSION-RESULT.md](development/operations-v1-plan/task-sessions/20260714T232409Z-swu-ov1-011/TASK-SESSION-RESULT.md)
- [development/operations-v1-plan/task-sessions/20260714T234403Z-swu-ov1-012/TASK-SESSION-RESULT.md](development/operations-v1-plan/task-sessions/20260714T234403Z-swu-ov1-012/TASK-SESSION-RESULT.md)
- [development/operations-v1-plan/task-sessions/20260714T234403Z-swu-ov1-012/DECISION-GATE.md](development/operations-v1-plan/task-sessions/20260714T234403Z-swu-ov1-012/DECISION-GATE.md)
- [development/operations-v1-plan/task-sessions/20260715T002431Z-swu-ov1-012-resume/EVENT-V4-MIGRATION.md](development/operations-v1-plan/task-sessions/20260715T002431Z-swu-ov1-012-resume/EVENT-V4-MIGRATION.md)
- [development/operations-v1-plan/task-sessions/20260715T002431Z-swu-ov1-012-resume/TASK-SESSION-RESULT.md](development/operations-v1-plan/task-sessions/20260715T002431Z-swu-ov1-012-resume/TASK-SESSION-RESULT.md)
- [development/operations-v1-plan/task-sessions/20260715T004506Z-swu-ov1-013/MACHINE-WITNESS-REPORT.md](development/operations-v1-plan/task-sessions/20260715T004506Z-swu-ov1-013/MACHINE-WITNESS-REPORT.md)
- [development/operations-v1-plan/task-sessions/20260715T004506Z-swu-ov1-013/DECISION-GATE.md](development/operations-v1-plan/task-sessions/20260715T004506Z-swu-ov1-013/DECISION-GATE.md)
- [development/operations-v1-plan/task-sessions/20260715T010547Z-swu-ov1-013-resume/TASK-SESSION-RESULT.md](development/operations-v1-plan/task-sessions/20260715T010547Z-swu-ov1-013-resume/TASK-SESSION-RESULT.md)
- [development/operations-v1-plan/task-sessions/20260715T010811Z-swu-ov1-014/INTEGRATED-AUDIT.md](development/operations-v1-plan/task-sessions/20260715T010811Z-swu-ov1-014/INTEGRATED-AUDIT.md)
- [development/operations-v1-plan/task-sessions/20260715T010811Z-swu-ov1-014/TASK-SESSION-RESULT.md](development/operations-v1-plan/task-sessions/20260715T010811Z-swu-ov1-014/TASK-SESSION-RESULT.md)
- [development/session-content-workbench-plan/work-pack/evidence/SWU-SCW-008-REPORT.md](development/session-content-workbench-plan/work-pack/evidence/SWU-SCW-008-REPORT.md)
