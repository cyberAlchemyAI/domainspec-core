# Invoke Plan Transport Report

## Run Identity

- Observed capability: `invoke`
- Mode: `plan`
- Target artifact: `ide-extension` L0 Human Approval Desk
- Target type: ordinary feature/product workflow
- Target lifecycle owner: `ide-extension` architecture and Task Session execution cycle
- Date: 2026-07-11
- Mutation mode: planning artifacts only

## Context Builder Summary

- Mode: standard, strict
- Files selected: 13
- Obligation coverage: 7/7
- Strict coverage: pass for planning
- Runtime handoff pack: not generated; Task Session must generate session evidence for the selected SWU.
- Context artifact: [work-pack/shared/context.md](work-pack/shared/context.md)
- Excluded noise: later MCP/browser/provider/IDE integration details and individual manifests.

## Template Selection

| Artifact | Template | Eligibility |
| --- | --- | --- |
| Layering | standalone `implementation-layering` | Mandatory for Invoke plan. |
| Work-pack | standalone `work-pack` in split mode | Medium complexity and multiple coupled tasks/SWUs. |
| Execution pack | DomainSpec `execution-pack` | Required for medium complexity wave choreography. |
| Task/wave contracts | plan-mode split boundary contract | Required so Task Session can resolve one executable SWU. |

No template tie required user selection. The medium-complexity threshold makes split mode mandatory.

## Dispatch Technique Trace

- Full dispatch: [dispatch.json](dispatch.json)
- Selected: `sequence`, `scu_swu_reduction`, `recomposition_proof`, `validation_loop`, `owner_boundary_check`, `handle_handoff`, `residue_ledger`, `execution_receipt_handoff`, `authority_split_gate`, `concrete_path_evidence`.
- Activation: cross-capability Invoke-to-Task-Session handoff plus protected Craft and product-authority boundaries.
- Skipped: fanout/tournament because accepted review findings already converge on one repair route; external research because it does not change L0 acceptance.
- Validation: pass via `.agents/skills/dispatch-spec/scripts/validate-dispatch.py`.

## Distill Validation

- Mode/budget: Validate; inferred automatically from Invoke plan.
- Role path: local Proposer/Balancer simulation; no subagents.
- Proposal track: one accepted repair route.
- Recursive rounds: one validation round.
- Verdict: pass.

### Role Conversation Trace

- Proposer: make the entire repaired Approval Desk the first execution unit.
- Balancer objection, executable-size: this would couple tests, policy, persistence, UI, and browser evidence into one unreviewable mutation.
- Reconciliation: split into nine SWUs while retaining one product recomposition target.
- Proposer: start by adding Playwright to prove the existing page.
- Balancer objection, evidence validity: browser automation would certify a known-defective approval core.
- Reconciliation: `SWU-IDEAD-001` becomes the hostile baseline, and Playwright moves after kernel/evidence repair.
- Proposer: add local authentication to prove a human approved.
- Balancer objection, scope/assurance: local login would add security machinery without proving effectful principal separation.
- Reconciliation: L0 records an honest unattested operator action; attested identity remains a promotion blocker.

### Technique Pack

- Abstraction-level guard: pass; units are implementation SWUs, not isolated code edits or broad product epics.
- Recomposition proof: pass; W0-W3 recompose into the L0 job and no SWU is orphaned.
- Evolution profile: pass; extension boundary is the kernel adapter contract after L0, with all adapter work deferred.
- Frame-expiry: this plan expires if `SPEC.md` changes the L0 authority boundary, if another implementation replaces the state model, or if accepted review findings are superseded.
- Navigability: pass; the first Task Session command and all parent task paths are explicit.
- Premortem: likely failure is treating a green happy path as closure while replay/recovery/reference tests remain absent; guardrail is the AR-CAND traceability matrix and W0-first sequence.

## Recomposition Proof

`SWU-IDEAD-001` captures the finite defects. SWUs 002-005 establish the legal and structural command boundary. SWUs 006-007 make its outcomes durable and inspectable. SWUs 008-009 expose and prove the same boundary for a person. TASK-VERIFY-READINESS closes only when all accepted findings map to passing evidence. Removing any group leaves the promised local human tool either untrustworthy, non-durable, or non-operable.

## Decisions And Gaps

- Decisions: [cross-task-decisions.md](work-pack/shared/cross-task-decisions.md)
- Gaps/residue: [cross-task-gaps.md](work-pack/shared/cross-task-gaps.md)
- Blocker decisions: none for SWU-IDEAD-001.
- Target-artifact gaps: honest unattested identity boundary, dependency pin, browser availability, and later synchronization.
- Invoke-specific gaps: none.

## Transport And Observability

- Necronomicon transport: not applicable; no matching target section was requested or mutated.
- Craft transport: proposal only; canonical ledger intentionally untouched.
- Observability: one Invoke plan signal should reference this report, the dispatch validation, Distill verdict, and output paths.

## Recommended Handoff

After explicit approval, route exactly:

```text
task-session to projects/ide-extension/development/l0-human-approval-desk-plan/WORK-PACK.md --swu SWU-IDEAD-001
```
