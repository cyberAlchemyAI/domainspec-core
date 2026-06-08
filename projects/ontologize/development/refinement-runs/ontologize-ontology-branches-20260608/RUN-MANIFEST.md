# RUN-MANIFEST — ontologize-ontology-branches-20260608

- Target: `projects/ontologize` — explain all ontology branches + interactions
- Owner: refine · Parent dispatch: `ontologize-research-20260608`
- Preset: standard · Research: no-research · Subagents: recommended, approved (1)
- Dispatch route: `REFINE-DISPATCH.json` (dispatch-spec validator: pass)
- Runtime: inline native stages + 1 approved subagent

## Stage receipts

| #   | Stage                       | Capability           | Artifact                                                            | Status |
| --- | --------------------------- | -------------------- | ------------------------------------------------------------------- | ------ |
| 1   | Context baseline            | context-builder      | DAG-AND-METRICS.md + ontology-vault SKILL + git:master ontology DAG | pass   |
| 2   | Invoke Define               | invoke               | stages/02-define.md                                                 | pass   |
| 3   | Interrogation refine-review | interrogation        | stages/03-interrogation-review.md                                   | flag   |
| 4   | Research decision           | refine               | (decision: no-research)                                             | pass   |
| 4s  | Subagent survey             | Agent×1              | stages/04-branch-evidence-mapper-receipt.md                         | pass   |
| 5   | Distill                     | distill              | stages/05-distill.md                                                | pass   |
| 6   | Invoke Redesign             | invoke               | ../../ONTOLOGY-BRANCHES.md                                          | pass   |
| 7   | Interrogation design-review | interrogation        | stages/07-design-review.md                                          | flag   |
| 8   | Distill Repair              | distill              | stages/08-distill-repair.md                                         | pass   |
| 9   | Invoke Plan                 | invoke               | stages/09-plan-deltas.md                                            | pass   |
| 10  | Final synthesis             | interrogation/refine | RESULT.md                                                           | pass   |

## Subagent lifecycle

| Agent           | Role                   | Spawn   | Join      | Close  |
| --------------- | ---------------------- | ------- | --------- | ------ |
| branches-mapper | branch-evidence-mapper | spawned | completed | closed |

## Artifacts produced (target-owned)

- `projects/ontologize/ONTOLOGY-BRANCHES.md` (new)
- `projects/ontologize/DESIGN.md` (View 1b), `DAG-AND-METRICS.md` (branch note)

## Guardrails honored

ontology-vault skill defs + GoldenQuill ontology DAG read-only (master via git); candidate-tagged;
no canonical promotion; no pricing/clients.
