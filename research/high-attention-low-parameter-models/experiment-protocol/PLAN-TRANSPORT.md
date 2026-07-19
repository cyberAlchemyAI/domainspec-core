# Invoke Plan Transport

Status: block-for-execution; authoring-complete

Date: 2026-07-18

Observed capability: `invoke`

Mode: `plan`

## Activation Evidence

- Approved design: `ARCHITECTURE-BUNDLE.md` with six-view coverage.
- Source design refs: spec, glossary, all aspect docs, design decisions, risks,
  and `GLOSSARY-CONSISTENCY.md`.
- Delivery boundary: deterministic offline witness -> one-stack measurement
  smoke -> paired decision pilot -> one justified extension.
- Creation approval: the user explicitly requested Invoke plan.

## Context Builder Coverage

Standard strict selection covered specification, architecture, accepted
research findings, explorer evidence, Invoke mode contracts, templates, and
one comparable research-toolchain work-pack. Runtime context packs were not
generated; each SWU carries selectors for execution-time Context Builder use.

## Template Selection

| Template | Eligibility | Decision |
| --- | --- | --- |
| standalone implementation layering | mandatory for plan | selected |
| standalone split work-pack | high complexity | selected |
| DomainSpec execution pack | high complexity and wave choreography | selected |
| implementation-plan candidate | work-pack is the canonical executable plan in current contract | not selected to avoid redundant authority |

No template tie required user selection.

## Complexity And Output Mode

- Complexity: high.
- Reasons: eight tasks, fourteen SWUs, multiple output families, model/GPU
  dependencies, and five unresolved blocker classes.
- Output mode: split.
- Per-layer planning: explicit L0, L1, L2, L3 waves.
- Implementation detail: complete in task-local contracts.

## Dispatch Spec

Selected techniques: `sequence`, `scu_swu_reduction`,
`recomposition_proof`, `validation_loop`, `owner_boundary_check`,
`handle_handoff`, `residue_ledger`, `execution_receipt_handoff`,
`authority_split_gate`, `concrete_path_evidence`,
`artifact_contract_bridge`, and `observability_grouping`.

Full reusable cross-capability route: `DISPATCH.json`. Deterministic validator
result: pass.

## Distill Validation

- Mode: Validate.
- Verdict: pass.
- Recomposition: pass.
- SWU atomicity: pass; zero task-shaped SWUs.
- First-unit narrowness: pass; `SWU-HALP-001`.
- Structural gaps: zero.
- Execution blockers: five explicit classes with owners and repair routes.
- Evidence: `DISTILL-VALIDATION.md`.

## Outputs And Evidence Capability Contract

- `execution_path`: Invoke plan, local native authoring.
- `dispatch_trace`: `DISPATCH.json` plus work-pack trace.
- `work_pack`: `WORK-PACK.md`, split mode.
- `implementation_layering`: `IMPLEMENTATION-LAYERING.md`, L0–L3.
- `swu_manifest`: fourteen non-exempt SWUs plus one VERIFY exemption.
- `validation_strategy`: per-slice and per-SWU surfaces.
- `result`: authoring complete, execution blocked.
- `next_route`: decision gate/interrogation for `SWU-HALP-001`, then one-SWU
  Task Session handoff.

## Authority And Handoff

Invoke owns authoring only. Task Session owns bounded implementation. Experiment
Harness owns model-run orchestration. Human owners approve decisions/resources.
Inventory and Definitions Governance retain their own promotion authority.

## Unresolved Gaps

See `work-pack/shared/cross-task-gaps.md`. Any applicable unresolved blocker
keeps `workPackGateStatus = block`; no experiment execution is authorized.
