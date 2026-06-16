# REFINE SEED PROPOSAL - View Triad As Ontology-Branch Materialization

## Target

- Target artifact family: `projects/ontologize/development/view-triad-method/`
- Refinement run: `20260615T203401Z-view-triad-ontology-branches`
- Requested operator intent: make this view the materialization of ontology branches, using zig-zag dialectics with two lanes:
  - Lane 1: defender + skeptic.
  - Lane 2: novel proposer + skeptic.

## Refinement Objective

Refine the Ontologize view-triad method so the "view" is not a generic explanation artifact. It should be the materialization surface for ontology branches:

- B1 meaning: policy, rules, value claims, outcomes, intended business semantics.
- B2 system: implementation, events, records, services, data shapes, gates, tests.
- B3 run-context: bounded run denominator, lifecycle state, scope, posture, and outcome context.
- B4 bridge: realization, observation, constraint, contradiction, drift, and evidence edges across branches.

The refined method should show how `system-view`, `engineer-view`, and `ontology-view` each materialize those branches without deciding twice:

```text
system-view = branch shape and branch tensions at stakeholder altitude
engineer-view = branch-boundary verdicts, authorities, schemas, and mechanics
ontology-view = typed branch nodes, typed bridge edges, and forbidden branch relations
```

## Source Context

| Source | Role |
| --- | --- |
| `projects/ontologize/development/view-triad-method/README.md` | Current invoke-authored method pack. |
| `projects/ontologize/development/view-triad-method/DESIGN.md` | Current generic six-view method design to refine. |
| `projects/ontologize/development/view-triad-method/WORK-PACK.md` | Current execution/SWU plan to refine after synthesis. |
| `projects/ontologize/ONTOLOGY-BRANCHES.md` | Existing four-branch ontology model and client/product mappings. |
| `projects/ontologize/DESIGN.md` | Existing engagement design with View 1b branch section. |
| `projects/ontologize/DAG-AND-METRICS.md` | Edge catalog, DAG/metrics, branch-aware governance substrate. |
| `implementation/domainspec/.claude/skills/system-view/SKILL.md` | Shape/stance law. |
| `implementation/domainspec/.claude/skills/engineer-view/SKILL.md` | Decision inventory and authority law. |
| `implementation/domainspec/.claude/skills/ontology-view/SKILL.md` | Typed node/edge and forbidden relationship law. |

## Proposed Coherent Unit

The smallest coherent unit is a branch-materialization redesign of the method pack, not a full execution of the view artifacts yet.

Expected final synthesis should decide:

- whether branch materialization is a modification of `system-view`, `engineer-view`, and `ontology-view`, or a separate upstream "branch-view" layer;
- how each of the three views maps to B1/B2/B3/B4;
- how branch materialization changes TASK-VTM-001 through TASK-VTM-005;
- which residue should remain for later `task-session`.

## Dialectic Zig-Zag Lanes

### Lane 1 - Defender + Skeptic

Purpose: defend the current view-triad method and test whether it already materializes ontology branches if branch requirements are added as constraints.

- Defender owns the strongest case that the current triad is sufficient.
- Skeptic attacks branch coverage, B3 run-context visibility, bridge-edge materialization, and double-decision risk.

### Lane 2 - Novel Proposer + Skeptic

Purpose: propose a more explicit branch-materialization model and test whether the novelty creates redundant artifacts or authority drift.

- Novel proposer owns the strongest new model, including branch tables, branch lanes, branch-to-view matrices, and branch-specific validation gates.
- Skeptic attacks over-abstraction, duplication with `ONTOLOGY-BRANCHES.md`, and leakage into product claims.

## Preset And Research

- Preset: `standard`.
- Research mode: `no-research`.
- Rationale: the required evidence is local and already present. If a stage finds a named external-context gap, the route must stop and ask before external research.

## Write Scope

Strategy packet only until confirmed:

- `projects/ontologize/development/refinement-runs/20260615T203401Z-view-triad-ontology-branches/`

After confirmation, likely write scope:

- refined artifacts under `projects/ontologize/development/view-triad-method/`
- possible proposed deltas to `WORK-PACK.md`, `PLAN.md`, `DESIGN.md`, and task files

Product-facing Ontologize docs remain blocked unless explicitly approved later.

## Done Criteria

This strategy packet is complete when:

- `REFINE-DISPATCH.json` validates as pass or flag without block;
- the route contains the ten canonical refine stages;
- dialectic and zig-zag techniques are tied to concrete steps, roles, and convergence criteria;
- subagent strategy lists the two requested lanes and requires user permission before execution;
- runtime handoff records authorization pending.

## Validation Surface

- `arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py REFINE-DISPATCH.json`
- link check on markdown files in this run folder
- JSON parse of `REFINE-DISPATCH.json` and `evidence-index.json`

