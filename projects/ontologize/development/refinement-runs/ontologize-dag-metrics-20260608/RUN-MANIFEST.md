# RUN-MANIFEST — ontologize-dag-metrics-20260608

- Target: `projects/ontologize` DAG & metrics design
- Owner: refine · Parent dispatch: `ontologize-research-20260608`
- Preset: standard · Research: no-research · Subagents: none
- Dispatch route: `REFINE-DISPATCH.json` (dispatch-spec validator: pass)
- Runtime: inline native stages; operator-approved

## Stage receipts

| #   | Stage                       | Capability           | Artifact                                                | Status |
| --- | --------------------------- | -------------------- | ------------------------------------------------------- | ------ |
| 1   | Context baseline            | context-builder      | git:master:grant_dag/validate.py + DESIGN.md + receipts | pass   |
| 2   | Invoke Define               | invoke               | stages/02-define.md                                     | pass   |
| 3   | Interrogation refine-review | interrogation        | stages/03-interrogation-review.md                       | flag   |
| 4   | Research decision           | refine               | (decision: no-research)                                 | pass   |
| 5   | Distill                     | distill              | stages/05-distill.md                                    | pass   |
| 6   | Invoke Redesign             | invoke               | ../../DAG-AND-METRICS.md                                | pass   |
| 7   | Interrogation design-review | interrogation        | stages/07-design-review.md                              | flag   |
| 8   | Distill Repair              | distill              | stages/08-distill-repair.md                             | pass   |
| 9   | Invoke Plan                 | invoke               | stages/09-plan-deltas.md                                | pass   |
| 10  | Final synthesis             | interrogation/refine | RESULT.md                                               | pass   |

## Artifacts produced (target-owned)

- `projects/ontologize/DAG-AND-METRICS.md` (new)
- `projects/ontologize/DESIGN.md` (View 5 pointer), `projects/ontologize/PLAN.md` (IDS-2/IDS-3 pointers)

## Guardrails honored

GoldenQuill read-only (read via git on master); all outputs candidate-tagged; no canonical promotion;
no pricing/clients.
