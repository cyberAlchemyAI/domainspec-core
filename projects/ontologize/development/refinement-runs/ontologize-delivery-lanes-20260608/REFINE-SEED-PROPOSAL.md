# REFINE-SEED-PROPOSAL — ontologize delivery lanes

- Run id: `ontologize-delivery-lanes-20260608`
- Target: the `projects/ontologize` delivery method — add two implementation lanes.
- Operator sentence: "now we need to add 2 lanes, using tools that they already have or arcanum
  inventory and ontology."

## Interpretation

Two delivery lanes for installing the four-layer method (ontology / classification register /
promotion DAG / evidence-linked BI + governed agents):

- **Lane A — Existing tools:** implement on the client's current stack (ERP/TMS/spreadsheets/BI).
- **Lane B — Arcanum substrate:** implement on Arcanum `inventory` + `ontology-vault` + `context-builder`.

## Source context (reused, local-first)

- ontologize artifacts: DESIGN.md, DAG-AND-METRICS.md, PLAN.md, WORK-PACK.md, L1-pattern-map.md.
- Arcanum skills (local): `.claude/skills/inventory/SKILL.md`, `.claude/skills/ontology-vault/SKILL.md`,
  `.claude/skills/context-builder/SKILL.md`.
- GoldenQuill precedent: read-only.

## Write scope

- New: `projects/ontologize/DELIVERY-LANES.md`.
- Tighten: DESIGN.md (add lane-selection to method), PLAN.md / WORK-PACK.md (add a lane-selection step).
- Run evidence under this folder. GoldenQuill + Arcanum skills are read-only.

## Done criteria

1. Both lanes defined: what each is, its toolchain, and its boundaries.
2. Four-layer mapping per lane (how ontology / register / DAG / BI+agents are realized).
3. Selection rule: when to choose Lane A vs Lane B (cost vs capability vs sovereignty).
4. Per-vertical mapping: candidate lane for cap factory and for logistics (assessment-confirmed).
5. All candidate-tagged; no canonical promotion; no pricing/clients.

## Validation surface

- Each lane's layer mapping traces to a real tool capability (client stack) or a real Arcanum skill
  capability (with path) or is marked hypothesis.
- Dispatch route validates against the dispatch-spec validator.
- Final interrogation confirms the selection rule is decidable, not vague.

## Preset / research / subagents

- Preset: standard. Research: no-research (local). Subagents: recommended, **approved by operator**
  (2 lane-designer roles). Join: parent_synthesis.
