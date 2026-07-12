# Invoke Plan Transport Report

## Run Identity

- Observed capability: `invoke`
- Mode: `plan`
- Target: `ide-extension` manual session bridge
- Lifecycle owner: approved ide-extension design; Task Session for implementation
- Date: 2026-07-12
- Mutation mode: planning artifacts only

## Context Builder Summary

- Mode: standard, strict
- Selected context: approved architecture, decisions, UX, glossary, layering seed,
  no-op refresh, current spec/schemas/kernel/server/UI/tests, and prior split-plan conventions
- Obligation coverage: 10/10
- Strict coverage: pass for planning
- Runtime handoff pack: not generated; each Task Session must produce its own evidence
- Excluded: L1-L3 providers, browser control, VSCodium, MCP/chat adapters,
  persistent workers, external services, and ambient transcript

## Template Selection

| Artifact | Template | Reason |
| --- | --- | --- |
| Layering | standalone `implementation-layering` | Required and separates active L0 from deferred L1-L3. |
| Work-pack | standalone split `work-pack` | Medium brownfield change with six tasks and eleven SWUs. |
| Execution pack | DomainSpec `execution-pack` | Four waves have dependency and promotion gates. |
| Tasks/waves | split execution contracts | Task Session needs path-bound, independently verifiable units. |

No template tie required operator selection; medium complexity selects split mode.

## Dispatch Technique Trace

- Full dispatch: [manual-session-bridge-plan.dispatch.json](manual-session-bridge-plan.dispatch.json)
- Selected: `sequence`, `scu_swu_reduction`, `recomposition_proof`,
  `validation_loop`, `owner_boundary_check`, `handle_handoff`, `residue_ledger`,
  `execution_receipt_handoff`, `authority_split_gate`, `artifact_contract_bridge`,
  `concrete_path_evidence`, and `state_namespace_boundary`.
- Activation: cross-capability Invoke/Distill/Task Session route, v1/v2 state
  boundary, operator/kernel/session authority split, and two product receipts.
- Subagents: none during planning; runtime delegation requires its own permission.
- External research: skipped because the accepted local design already fixes L0
  interfaces and the plan does not depend on changing external facts.

## Distill Validation

- Artifact: [DISTILL-VALIDATION.md](DISTILL-VALIDATION.md)
- Verdict: pass
- First unit: `SWU-MSB-001`
- Recomposition: 001-002 contracts; 003-005 kernel; 006-008 protocol/workbench;
  009-011 proof; verification task closes evidence only.
- Premortem: likely failure is treating approval or chat output as execution;
  guardrails are typed receipt separation and required kernel result admission.

## Decisions And Residue

- Approved decisions are transported without override in
  [cross-task-decisions.md](work-pack/shared/cross-task-decisions.md).
- Known migration, assurance, recovery, live-environment, and workspace residue
  is owned in [cross-task-gaps.md](work-pack/shared/cross-task-gaps.md).
- No gap blocks 001. The live session/environment may block 011 honestly.
- Craft, Inventory, Necronomicon, canonical definitions, and runtime source were
  not mutated by Invoke.

## Validation And Observability

- Dispatch validation: pass via
  `arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py`.
- Structural plan checks: file census, SWU uniqueness/parentage, task exemption,
  wave count, local links, JSON, ASCII, and whitespace pass: 22 files, six tasks,
  four waves, and eleven uniquely parented SWUs. Scoped diff is checked at close.
- Observability: one immutable Invoke run bundle and append-only signal reference
  this report, the validated dispatch, Distill verdict, and handoff.

## Recommended Handoff

```text
task-session to projects/ide-extension/development/manual-session-bridge-plan/WORK-PACK.md --swu SWU-MSB-001
```
