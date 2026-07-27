# Define Transport

Status: pass

## Stable inputs for Design

- definition: `DEFINE.md`
- glossary: `GLOSSARY.md`
- intent and approval boundary: `INTENT-RECORD.md`
- template selection: `TEMPLATE-SELECTION.md`
- accepted evidence source:
  `../2026-07-23-invoke-lifecycle-churn-research/findings.md`
- current source contracts:
  - `../../../arcanum/spells/invoke/plan.md`
  - `../../../arcanum/spells/invoke/refresh.md`
  - `../../../arcanum/arcana/task-session/SKILL.md`

## Fixed decisions

- authored validity and handoff readiness remain separate;
- exact digest mismatch remains fail-closed;
- one epoch binds one selected SWU;
- local execution uses a pre-execution contract rather than pre-authored bytes;
- external/delegated/reusable package validation remains;
- epoch-control changes require successor/supersession;
- Refresh has four transition kinds and no target implementation;
- read models do not own progress;
- legacy plans receive no inferred readiness;
- public/private separation is mandatory.

## Design gaps to own

- transition-admission owner and public source placement;
- minimal local execution-contract schema;
- declared control-graph completeness rules;
- deterministic change-impact classifier;
- legacy admission route;
- generic live proof.

