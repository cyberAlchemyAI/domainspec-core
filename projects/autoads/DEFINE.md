# autoads — DEFINE

> Seeded by refine run `autoads-seed-20260610`. Canonical detail in
> [stages/02-define.md](development/refinement-runs/autoads-seed-20260610/stages/02-define.md).
> Claims labeled **[SB]** source-backed (path), **[adapt]** adaptation, **[H]** hypothesis.

## What it is

autoads installs the [ontologize](../ontologize/) ontology+DAG learning loop over ad-creative
production, turning ad-network outcome data into a governed loop that promotes evidence-backed "better
creative" recommendations and feeds an auto-research stage that proposes the next creative candidates.

## Problem

- Creative iteration is opinion-led, not evidence-led; the *why a variant won* is rarely captured as
  reusable, auditable knowledge. [adapt — ontologize "scattered runs/dashboards"]
- Ad-network metrics are mistaken for authority — a high CTR becomes "truth" without attribution
  windows, confidence, or confound control. [adapt — ontologize metric≠authority, `PRODUCT.md`]
- New creative ideas are researched ad hoc, not as governed candidates entering a learning loop.

## Unit of value — the Creative Learning Cycle

One closed loop: generate a variant → dispatch to an ad network → measure outcomes over a response
window → grade (`veracidade` + `evidence_refs`) → route through promotion-DAG review gates → owner
decides promote/retire → verdict + residue feed the next generation and the auto-research pool.

## Ontologize binding

- **Ontology axes** [adapt]: (audience × creative-family) × ad-objective; cards configure generation
  vocabulary, outcome schema, and reporting rhythm.
- **Data-governance register** [adapt]: ad-network fields get authority classes with fail-closed routing.
- **Promotion DAG** [SB method, adapt vertical]: creative runs are Execution-DAG nodes; promoted
  recommendations are Promotion-DAG nodes gated by review + owner decision.
- **Evidence-linked KPIs** [adapt]: each creative KPI carries `veracidade` + `evidence_refs`.

## Out of scope (seed)

Live ad-network integration, real spend, model training, executed pipeline. **[H]** the cross-vertical
generalization of the ontologize loop from grants (GoldenQuill) to ads is the core hypothesis the MVP
must validate.
