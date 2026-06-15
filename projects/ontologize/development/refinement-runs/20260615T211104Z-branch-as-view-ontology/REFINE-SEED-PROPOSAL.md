# REFINE SEED PROPOSAL - Branch-As-View Ontology

## Operator Intent

The previous branch-materialization model is still too indirect. The intended model is:

```text
the ontology is the directory / artifact tree
each branch is a view artifact
each view artifact is one ontology branch
```

This means `ontology-view` should not be one sibling artifact beside `engineer-view` and `system-view`. The ontology is the whole composed surface.

## Target

`projects/ontologize/development/view-triad-method/`

## Refinement Objective

Refine the method pack from "view triad materializes ontology branches" into "branch views are the ontology":

- B1 meaning becomes `meaning-view` or a renamed `ontology-view` only if the name is explicitly narrowed.
- B2 system becomes `engineer-view` or `system-view`, with engineering/mechanics as the system branch.
- B3 operational/run-context becomes a new `run-view` candidate.
- B4 bridge becomes `residue-view`, with bridge/residue/drift/contradiction evidence.

## Selected Working Hypothesis

Use this branch-as-view map:

| Ontology Branch | View Artifact | Why |
| --- | --- | --- |
| B1 meaning | `meaning-view.md` | Captures intent, policy, rules, value claims, outcomes, and definitions. Calling it `ontology-view` confuses the branch with the whole ontology. |
| B2 system | `engineer-view.md` | Captures implementation, artifacts, schemas, events, gates, mechanics, and source truth. |
| B3 operational / run-context | `run-view.md` | Captures bounded run, denominator, lifecycle state, scope/posture, and stage-vs-outcome separation. |
| B4 bridge | `residue-view.md` | Captures realization, observation, drift, contradiction, evidence gaps, bridge edges, and leftover tension between branches. |

## Key Design Correction

The old triad should not be the final ontology shape. It can remain as a set of authoring skills, but the durable artifact tree should be branch-native:

```text
ontology/
  README.md
  meaning-view.md
  engineer-view.md
  run-view.md
  residue-view.md
  validation-report.md
```

Alternative nested form:

```text
ontology/
  meaning/VIEW.md
  system/VIEW.md
  run/VIEW.md
  residue/VIEW.md
  validation-report.md
```

The refinement must decide which structure becomes the target output.

## Why The Operational Branch Should Become `run-view`

The operational branch is not just "operations" in the business sense and not general "agent operation." In the current Ontologize branch source, it is B3 run-context: one bounded run context where denominator truth, lifecycle state, deadline/posture, and stage-vs-outcome honesty live.

`run-view` is the least confusing name because it says what this branch does:

- defines the unit of analysis;
- defines metric denominators;
- preserves lifecycle stage without pretending it is outcome;
- ties evidence to a bounded execution context.

## Route Decision Needed

The design should compare:

1. Flat branch-view files under one ontology directory.
2. Branch directories with `VIEW.md` inside each branch.

The flat form is simpler for a first pilot. The nested form better satisfies "each directory and artifact inside of it represents the ontology."

## Write Scope

Strategy packet only until confirmed.

Allowed after confirmation:

- `projects/ontologize/development/view-triad-method/`
- this refinement run folder

Blocked until later owner approval:

- product/public docs;
- canonical branch source rewrites;
- client-facing claims.

## Research Decision

No external research. Use local repository evidence only.

## Done Criteria

This strategy is ready when it:

- records the corrected branch-as-view model;
- validates a dispatch route;
- names `run-view` as the operational branch candidate;
- blocks product-facing mutation;
- asks for confirmation before redesigning the method pack.
