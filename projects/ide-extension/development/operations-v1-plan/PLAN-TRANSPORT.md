---
id: ide-extension-operations-v1-plan-transport
project: ide-extension
title: "Operations V1 Plan Transport"
status: pass
node_type: plan-transport
updatedAt: 2026-07-12
observed_capability: invoke
invoke_mode: plan
---

# Plan Transport: Operations V1

## Provenance

| Field | Value |
| --- | --- |
| Observed capability | `invoke` |
| Mode | `plan` |
| Target artifact | Operations V1 implementation package |
| Lifecycle owner | `projects/ide-extension` |
| Approved design | `operations-v1-design/ARCHITECTURE-BUNDLE.md` |
| Closed blocker gate | `operations-v1-design/PLANNING-DECISION-GATE.md` (`PASS`, 4/4) |
| Complexity / output | medium / split |
| Mutation authority | none in Invoke; Task Session per selected SWU |

## Template Selection

Selected the current standalone `WORK-PACK.md` and
`IMPLEMENTATION-LAYERING.md` templates plus a DomainSpec-style execution pack.
The retired `IMPLEMENTATION-PLAN.md` template was intentionally not generated:
the current Invoke contract makes the work pack the canonical executable plan.

Split mode is required because the work introduces durable state and exceeds
five tasks/two artifacts across kernel, storage, server, CLI, and browser.

## Bounded Context

- Accepted operations architecture and decisions.
- Closed parser, size, retention, and navigation gate.
- Current V0 kernel/server/projector/storage/browser/CLI seams.
- Completed V0 repair evidence.
- Existing `ide-extension` split work-pack conventions.

No private DomainSpec/Saturn prose was copied into public Arcanum surfaces, and
no Arcanum canonical source was changed.

## Dispatch Technique Trace

| Technique | Concrete effect |
| --- | --- |
| `sequence` | W0-W6 and SWU dependencies are linear and receipt-gated. |
| `scu_swu_reduction` | Accepted L0 unit reduces to six one-owner SWUs; later layers reduce to eight more. |
| `recomposition_proof` | 001-006 prove derive-plus-replace; later waves preserve identities and guarantees. |
| `validation_loop` | Focused checks precede inherited and integrated suites. |
| `owner_boundary_check` | Invoke authors; Task Session executes; project lifecycle and human own promotion. |
| `handle_handoff` | Task contracts use source paths and anchors. |
| `residue_ledger` | Accepted limitations and deferred L3 remain visible. |
| `execution_receipt_handoff` | Every SWU has one structured return shape. |
| `concrete_path_evidence` | Closeout requires paths, commands, counts, and screenshots. |
| `authority_split_gate` | Preview/display does not become shell/provider/domain authority. |
| `observability_grouping` | Invoke and later Task Sessions share the package/SWU identity. |

Full dispatch required: yes. The route is reusable across fourteen Task
Sessions, crosses Invoke/Task Session/project/human authority, and carries a
destructive retention boundary. Dispatch validation is recorded in
`INVOKE-RESULT.md`.

## Execution Handoff

First handle:

```text
projects/ide-extension/development/operations-v1-plan/work-pack/tasks/TASK-CONTRACT-TRANSFORM.md#swu-ov1-001-versioned-contract-and-budget-baseline
```

Task Session must create execution-time context from that task and shared
source anchors. Invoke does not pre-generate runtime context packs.

## Expected Receipt

```yaml
swu_id: SWU-OV1-001
result: pass | flag | block | interrupted
capability_ref: task-session
receipt_kind: native-stage | subagent | local-fallback | blocked
receipt_artifact: path-or-none
files_touched: []
validation: []
blockers: []
residue: []
reroute: SWU-OV1-002-or-none
handoff_note: concise continuation state
```

## Gaps And Stop Rules

There is no active planning blocker. Accepted limitations and deferred scope
are in `work-pack/shared/cross-task-gaps.md`. Execution stops on any violated
V0 compatibility, blob/event ordering, retry/CAS, pruning, browser degradation,
or authority boundary in the work pack.

## Transport Result

- Status: `pass`
- Mutation-ready route: `task-session SWU-OV1-001`
- Runtime implementation performed: none
- Region/L3 route: deferred
