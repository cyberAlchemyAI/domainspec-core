# Stage 2 — Invoke Define

- **Capability:** `invoke` · mode `define` · receipt: native-stage · **verdict: pass**

## What autoads is (one sentence)

**autoads installs the ontologize ontology+DAG learning loop over ad-creative production, turning
ad-network outcome data into a governed loop that promotes evidence-backed "better creative"
recommendations and feeds an auto-research stage that proposes the next creative candidates.**

## Problem

- Creative iteration is **opinion-led, not evidence-led** — variants ship, some win, but the *why* is
  rarely captured as reusable, auditable knowledge. [adapt of ontologize "scattered runs/dashboards"]
- Ad-network metrics are **mistaken for authority** — a high CTR becomes "the truth" without governance
  (attribution windows, statistical confidence, segment confounds). [adapt of ontologize metric≠authority]
- New creative ideas are **researched ad hoc**, not as governed candidates entering a learning loop.

## Unit of value

One **creative learning cycle**: a creative variant (or family) is generated → dispatched to an ad
network → outcomes measured over a response window → graded and routed through the promotion DAG →
an owner-decided "promote/retire" verdict → the verdict + residue feed the next generation and the
auto-research candidate pool.

## Ontologize binding

- **Ontology axes** [adapt]: subject/segment = audience × creative family; value-mechanism = the ad
  objective (awareness / click / conversion). Cards configure generation vocabulary, the outcome schema,
  and reporting rhythm.
- **Data-governance register** [adapt]: ad-network fields (spend, audience, identifiers) get an
  authority class with fail-closed routing — keeps PII/spend out of shareable artifacts.
- **Promotion DAG** [SB method, adapt vertical]: ad-creative runs are Execution-DAG nodes; promoted
  "better creative" recommendations are Promotion-DAG nodes gated by review + owner decision.
- **Evidence-linked KPIs** [adapt]: each creative KPI carries `veracidade` + `evidence_refs` to the
  ad-network outcome record and response window.

## Out of scope (this seed)

Live ad-network API integration, real campaign spend, model training, and any executed pipeline. The
seed produces DEFINE/DESIGN/PLAN only. [H] cross-vertical generalization of the ontologize loop to ads
is a hypothesis the MVP pilot must validate.
