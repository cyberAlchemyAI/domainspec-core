---
id: ide-extension-domainspec-roadmap-lab-plan-transport
status: pass
updatedAt: 2026-07-14
invoke_mode: plan
---

# Invoke Plan Transport

## Preconditions

- [Design transport](DESIGN-TRANSPORT.md): pass.
- [Distill design validation](DISTILL-DESIGN-VALIDATION.md): pass.
- Approved design references: [architecture](ARCHITECTURE-BUNDLE.md),
  [UX](UX-PLAN.md), [decisions](DESIGN-DECISIONS.md).
- Scope: medium-complexity split work-pack; trusted-local newcomer pilot.
- Subagents: none. Future SWU owner labels are recommendations, not dispatched
  agents or granted permission.

## Inventory And Template Lookup

The repository-local Inventory was queried before template selection. It had
ide-extension architecture/strategy result entries but no Roadmap Lab package;
therefore no prior Roadmap Lab result was promoted or treated as canonical. The
plan used:

- Invoke DomainSpec architecture/execution templates;
- Invoke implementation-layering and work-pack templates;
- `PLAN-ARTIFACT-BOUNDARIES.md`;
- the existing `session-content-workbench-plan` only as a local navigation and
  Canvas-planning convention, not as current state.

Task Session/Context Builder must generate execution-time context for the one
selected SWU. Invoke does not pre-generate 14 stale handoff packs.

## Planning Outputs

| Responsibility | Artifact |
| --- | --- |
| System delta, contracts, algorithms, tests, task mapping | [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md) |
| L0–L3 decision and promotion governance | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) |
| Canonical task/SWU status and execution gates | [WORK-PACK.md](WORK-PACK.md) |
| Five-wave choreography | [EXECUTION-PACK.md](EXECUTION-PACK.md) and [waves](work-pack/waves/) |
| Task-local execution contracts | [tasks](work-pack/tasks/) |
| Shared source/decision/gap/trace context | [shared](work-pack/shared/) |
| Smallest-unit/recomposition validation | [DISTILL-PLAN-VALIDATION.md](DISTILL-PLAN-VALIDATION.md) |

## Dispatch Technique Trace

| Technique | Concrete effect | Validation |
| --- | --- | --- |
| `sequence` | Design check gates plan; layers and waves preserve dependency order. | Dispatch step order and W0–W4 entry gates. |
| `scu_swu_reduction` | FPR-01 is L0 and each task has two independently receiptable SWUs. | Task-local scopes/done criteria. |
| `recomposition_proof` | 14 units map back to all accepted outcomes. | Distill plan and shared traceability. |
| `validation_loop` | Each unit names positive/negative/degraded/human evidence. | Canonical SWU manifest. |
| `owner_boundary_check` | Browser, session adapter, and lifecycle owners have separate effect rights. | Architecture/packet/round-trip gates. |
| `handle_handoff` | Future Task Session receives one task/SWU plus source handles. | Work-pack selection/result contracts. |
| `artifact_contract_bridge` | Fingerprinted generated HTML crosses roadmap-to-Canvas without authority transfer. | 003–006 acceptance. |
| `state_namespace_boundary` | Copy, graph/roadmap, Canvas, and review evidence are distinct. | Shared decisions and task scopes. |
| `residue_ledger` | Human availability, owner acceptance, source resolver, identity, and broader effects stay visible. | Shared gaps and work-pack board. |
| `concrete_path_evidence` | Every SWU names exact files/modules or evidence surfaces. | Manifest and task contracts. |
| `observability_grouping` | Design and plan results share one dispatch ID with phase-specific signals. | Dispatch and Invoke result. |

## Deterministic Dispatch Validation

Command:

```bash
python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py \
  projects/ide-extension/development/domainspec-roadmap-lab/domainspec-roadmap-lab.dispatch.json
```

Result: `VALIDATION=pass`.

## Handoff Gate

Status: **pass for selection, closed for mutation**.

The plan is navigable and complete, but no SWU is selected. The next lifecycle
owner is Task Session for one operator-selected ready unit after a live
dirty-worktree ownership review. Invoke performs no runtime mutation.

