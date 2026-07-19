# Codex Goal Profile: GOAL-DISTILL-EXECUTION-EVIDENCE-BACKEND

## Source

- Work-pack: `arcanum/spells/invoke/development/distill-execution-evidence/WORK-PACK.md`
- Ordered stream: `SWU-DEE-004` through `SWU-DEE-013`, then `TASK-DEE-VERIFY`
- Handoff pack: `.arcanum/profiles/distill-execution-evidence-backend-goal/handoff-pack.md`
- Handoff index: `.arcanum/profiles/distill-execution-evidence-backend-goal/handoff-index.json`
- Decision profile: none
- One-shot mode: yes, explicitly selected by the operator's “finish this backend” instruction

## Readiness

| Check | Status | Evidence |
| --- | --- | --- |
| Prerequisites | pass | DEE-002 and DEE-003 result artifacts |
| Write scope | pass | receipt-bound per future SWU; sidecar scope explicit |
| Done criteria | pass | remaining task contracts and final verify task |
| Verification | pass | receipt-named focused suites and integrated verify |
| Handoff pack | pass | Markdown and JSON/index sidecar |
| Strict coverage | pass | orchestration obligations covered; future paths receipt-gated |
| Fallback exploration | pass | named gaps only |
| Current blockers | flag | DEE-004 receipt must be authored before its implementation |
| Goal budget | pass | compact goal below 4000 characters |
| Capability policy | pass | bounded sigils, no ambient subagents |

## Native Codex Goal

```text
/goal Finish the Distill Execution Evidence backend stream from SWU-DEE-004 through TASK-DEE-VERIFY, verified by each receipt-named focused suite, final dispatch validation, and integrated verification. Use .arcanum/profiles/distill-execution-evidence-backend-goal/handoff-pack.md and handoff-index.json as the execution frame. Before each unit, use Spellcraft to bind the canonical owner and exact implementation/evidence paths; then run exactly one Task Session SWU, synchronize its result, and require focused validation before advancing. Allowed lanes: spellcraft, task-session, context-builder, experiment-harness, decision-gate for blockers only. No ambient subagents, invoke, refine, craft, Distill contract edits, or broad exploration. Broaden only for named gaps in the sidecar, and report every extra source used. Stop immediately on unresolved authority, missing receipt, validation failure, scope contradiction, or promotion request, reporting attempted unit, files, evidence, blocker, and next owner.
```

## Audit

- Verification surface: receipt-named focused tests, Dispatch Spec validator, and
  `TASK-DEE-VERIFY`.
- Boundaries: future implementation writes exist only after their exact lifecycle receipt;
  current task/Work Pack/result records synchronize evidence; sidecar remains private.
- Iteration: advance only after the current unit's receipt, implementation, validation, and
  result are all present; never skip a dependency or combine SWUs.
- Stop: unresolved authority, missing evidence, failed validation, public/private breach, or
  promotion request.
