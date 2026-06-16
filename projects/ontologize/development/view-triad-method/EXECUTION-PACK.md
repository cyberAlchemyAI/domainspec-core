# EXECUTION-PACK - Ontologize View-Triad Method

Wave choreography for [WORK-PACK.md](WORK-PACK.md). This pack schedules execution; task files remain the source of truth for SWU contracts.

## Execution Policy

- Execute one SWU at a time through `task-session`.
- Start with `SWU-VTM-001`.
- Do not mutate product-facing Ontologize docs until L0 method boundary, Branch Materialization Register, and owner approval are explicit.
- Use local execution by default; use subagents only after an approved `domainspec-subagents-strategy` route.

## Waves

| Wave | Layer | Tasks | SWUs | Entry Gate | Exit Evidence |
| --- | --- | --- | --- | --- | --- |
| [W0](work-pack/waves/W0.md) | L0 | TASK-VTM-001 | SWU-VTM-001 | Pack exists and source boundary is accepted. | Method boundary, source matrix, Branch Materialization Register, output path decision. |
| [W1](work-pack/waves/W1.md) | L0/L1 | TASK-VTM-002, TASK-VTM-003 | SWU-VTM-002, SWU-VTM-003 | W0 exit evidence present. | Branch-aware system-view shell, engineer-view inventory, B3 run-context record. |
| [W2](work-pack/waves/W2.md) | L1 | TASK-VTM-004 | SWU-VTM-004 | W1 stance/decision/branch coverage present. | Ontology-view typed model, B4 bridge ledger, and guard checklist. |
| [W3](work-pack/waves/W3.md) | L2/L3 | TASK-VTM-005 | SWU-VTM-005 | W2 typed model and bridge ledger present. | Validation report, branch recomposition trace, integration proposal, readiness result. |

## Parallelization

No initial parallelization is recommended. The artifact sequence is intentionally dependent:

```text
branch register -> system-view stances -> engineer-view rows -> ontology-view targets -> integration validation
```

After W0, source-inventory refinement and method prose drafting may run in parallel only if they write disjoint files and synchronize before W1 exit.

## Completion Evidence Shape

Each task-session result should report:

```yaml
swu_id: SWU-VTM-###
result: pass | flag | block | interrupted
files_touched:
  - path
validation:
  - review or command result
blockers:
  - blocker id or none
next_swu: SWU-VTM-### or none
handoff_note: summary for coordinator
```
