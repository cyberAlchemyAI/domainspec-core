# TASK-BWAA-002 — Render Exact Relation Arrows

Layer: L1  
Dependencies: `SWU-BWAA-001` closeout  
SWU: `SWU-BWAA-002`  
Execution owner recommendation: `local-fallback` through one Task Session

## Task Objective

Make the direction of every exact relation visually obvious while preserving
the existing canonical HTML meaning. This task contains exactly one SWU.

## Smallest Working Units

- `SWU-BWAA-002`: render and validate the exact relation-arrow component.

## Primary Behavior

Render one responsive arrow presentation inside every canonical relation
article so the exact tuple reads source → predicate → target.

## Source Anchors

- `ARCHITECTURE.md#exact-relation-arrow-component`
- `UX-PLAN.md#relation-arrow`
- `projects/body-war/ontology/business/scripts/render-view-atlas.mjs`

## Write Scope

- `projects/body-war/ontology/business/scripts/render-view-atlas.mjs`
- `projects/body-war/ontology/business/tests/business-view-atlas-render.test.mjs`

## Implementation Detail

Inputs are the existing canonical relation, its source/target nodes, portal
classification, effect, and endpoint lens lookup. Output is one
`.relation-arrow` region inside the existing relation article.

Rendering algorithm:

```text
render a source endpoint link from the canonical source node
render a geometry-only SVG shaft with one end marker
render the canonical predicate as visible HTML adjacent to the shaft
render a target endpoint link from the canonical target node
apply effect class from the canonical effect only
apply portal class from portal membership only
retain the existing relation sentence, orientation metadata, and actions
```

Desktop lays source, shaft/predicate, and target left-to-right. Narrow layout
stacks them top-to-bottom but keeps source first and target last. Focus and
target behavior remain on real links/articles. SVG has no labels and is
`aria-hidden`.

Failure modes:

- missing source or target lookup;
- missing predicate/effect;
- more or fewer than one arrow component per canonical relation article;
- marker reversal;
- effect or portal class derived from presentation guesses;
- semantic text moved exclusively into SVG.

Renderer/test failures block closeout.

## Acceptance

- all 231 canonical relation articles contain exactly one arrow component;
- source, predicate, target, relation ID, and endpoint links remain exact HTML;
- the SVG shaft and arrowhead are `aria-hidden="true"`;
- the arrowhead points from source to target in every layout;
- dotted/solid effect styling and portal styling are independent classes;
- keyboard/focus behavior and existing relation sentences remain intact;
- no overview map, generated HTML, or ontology source changes occur.

## Validation

```bash
node --test projects/body-war/ontology/business/tests/business-view-atlas-render.test.mjs
git diff --check -- projects/body-war/ontology/business/scripts/render-view-atlas.mjs projects/body-war/ontology/business/tests/business-view-atlas-render.test.mjs
```

## Split And Done

Candidate children were markup, CSS, and renderer assertions. They remain one
component contract because none is independently useful or reviewable without
the other two. Overview integration is reserved for 003. Done requires a
receipt proving 231/231 exact components with no semantic source delta.

## Handoff And Closeout

Context Builder needs this task, the 001 closeout receipt, `ARCHITECTURE.md`,
`UX-PLAN.md`, the renderer/test files, and
`../shared/EXECUTION-CONTROL.md`. Known blockers: absent/failed 001 receipt or
semantic-lock drift.

Expected result:

```yaml
swu_id: SWU-BWAA-002
result: pass | flag | block | interrupted
capability_ref: task-session
receipt_kind: native-stage | local-fallback | blocked
receipt_artifact: work-pack/closeout/SWU-BWAA-002.receipt.json | none
files_touched: [declared paths only]
validation: [command and result]
blockers: [blocker or none]
residue: [residue or none]
reroute: invoke-refresh | none
handoff_note: exact 231/231 result and whether 005 is dependency-ready
```
