# DESIGN — CyberAlchemy ontology+DAG engagement

Design-mode artifact. Converts [SPEC.md](SPEC.md) into a governed design across six views. Source
precedent: GoldenQuill (read-only). All client-facing claims tagged proven/hypothesis per R-D.

## View 1 — Context

The engagement sits between a client's existing systems (ERP/TMS/spreadsheets, dashboards, any
agents) and its decision-makers. CyberAlchemy installs four governance layers and hands back a
self-improving BI + agent loop plus a client-sendable package. Two clients run in parallel:
**cap factory** (continuous production) and **logistics company** (discrete shipment runs).

## View 1b — Ontology branches

The ontology is a **4-branch** model (meaning · system · operational · bridge), connected by bridge
edges and governed for drift. Full enumeration + branch→layer and branch→client-work maps:
[ONTOLOGY-BRANCHES.md](ONTOLOGY-BRANCHES.md). The operational branch is first-class — metric
denominators are defined inside a run context.

## View 2 — Components

1. **Assessment instrument** — repeatable intake. Inputs: client interviews, system access,
   sample data. Outputs: `ontology-map` (two axes), `data-inventory`, `agent-inventory`,
   `maturity-score` (Four Autonomy Rules).
2. **Method install kit** — the four layers as repeatable steps:
   - L-ont: ontology cards (subject × mechanism, orthogonal, runtime-matched).
   - L-reg: signed classification register (field → authority class).
   - L-dag: promotion DAG + deterministic gate ruleset (events→evidence→candidate→review→decision).
   - L-bi: evidence-linked KPI taxonomy + counterfactual receipts; agent routing + gates on top.
3. **Deliverable template** — vertical-agnostic client-sendable package: overview, executive brief,
   reference appendix (KPI/ontology taxonomy), client-decisions sheet, plus the five gap-closing
   sections. BI-led ordering.
4. **Per-vertical instantiation** — cap factory + logistics seeds for components 1–3.
5. **Proof harness** — defines, per vertical, the one evidence-linked metric, its evidence chain,
   baseline, and movement measurement.

## View 3 — Data / artifacts flow

`assessment → ontology-map + inventories → method install (L-ont→L-reg→L-dag→L-bi) →
evidence-linked KPIs + receipts → deliverable package → proof harness reading → cross-vertical verdict`.
Each arrow is an artifact handoff; no step mutates the prior step's record (audit integrity, P3).

## View 4 — Governance / gates

- **G-honesty (R-D)** — every client claim tagged proven/hypothesis; block on untagged capability claims.
- **G-privacy (R-F)** — classification register signed before any agent runs on client data; fail-closed.
- **G-promotion** — no pricing/contracts/canonical promotion in any artifact; block.
- **G-layer** — a layer installs only after the prior layer produced its evidence (P-layering).
- **G-proof (R-E)** — generalization claim is made only after both verticals report independent metric movement.

> **DAG & metrics are now specified concretely** in [DAG-AND-METRICS.md](DAG-AND-METRICS.md)
> (node/edge types, event model, metric families, improve-over-time loop, deterministic gates),
> lifted from GoldenQuill's `grant_dag` on `master`. This view keeps only the per-vertical framing.

## View 5 — Per-vertical design notes

**Cap factory** (continuous production):

- Subject axis: product lines / SKUs. Mechanism axis: order/sales channel (wholesale / retail /
  custom / e-com). [A1 — validate in assessment]
- DAG framing: a "run" = a production lot or an order-fulfillment cycle; evidence = quality/defect
  - on-time data; candidate = process/scheduling lesson. The run boundary is the design risk
    (continuous flow) — resolve by choosing lot- or order-as-run during assessment.
- Candidate proof metric: defect/rework rate OR on-time order fulfillment, traced to its evidence. [D-defer-1]

**Logistics company** (discrete runs):

- Subject axis: clients / lanes. Mechanism axis: shipment / contract type. [A1]
- DAG framing: a "run" = a shipment; evidence = delivered/delayed/damaged + cost; candidate =
  routing/carrier lesson. Maps almost 1:1 to GoldenQuill's grant-run DAG — lowest design risk.
- Candidate proof metric: on-time-delivery rate OR cost-per-lane, traced to its evidence. [D-defer-1]

## View 5b — Delivery lane

Each engagement installs the four layers via one of two lanes (or the hybrid): **Lane A** (the
client's existing tools) or **Lane B** (Arcanum `inventory` + `ontology-vault` + `context-builder`),
with a **Hybrid** (data/BI local + governance on Arcanum) as the usual answer. Full spec + the
decidable selection rule: [DELIVERY-LANES.md](DELIVERY-LANES.md). The lane is chosen during assessment.

## View 6 — Dependencies / risks

- Dep: client system access + sample data for each vertical (assessment gating input).
- Risk: continuous-production run boundary (cap factory) — mitigated by assessment decision.
- Risk: cross-vertical generalization is a hypothesis (R1) — mitigated by independent per-vertical proof.
- Risk: client data sensitivity — mitigated by G-privacy (signed register before agents).

## Glossary consistency

Terms used here resolve to [GLOSSARY.md](GLOSSARY.md)/[DEFINITIONS.md](DEFINITIONS.md). No drift; no new
canonical terms. Status: pass.
