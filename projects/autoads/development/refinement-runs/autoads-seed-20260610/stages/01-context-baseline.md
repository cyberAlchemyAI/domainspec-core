# Stage 1 — Context Builder evidence baseline

- **Capability:** `context-builder` · mode `standard` · receipt: native-stage · **verdict: pass**

## Evidence pack (read-only)

| Source | What it supplies |
|--------|------------------|
| `projects/ontologize/PRODUCT.md` [SB] | Two-axis ontology (subject/segment × value-mechanism); 4 installed layers: ontology, data-governance register, promotion DAG, evidence-linked BI + governed agents. |
| `projects/ontologize/DAG-AND-METRICS.md` [SB] | Two linked DAGs (Execution = what happened; Promotion = what we trust); events that update them; KPI families; `veracidade` grade + `evidence_refs`; CycleReceipt. |
| `projects/ontologize/OPTIMIZATION-CHAIN-METHOD.md` [SB] | Generalized method binding run nodes → evidence-linked KPIs → response windows → analysis methods → claim labels → owner-governed reuse into named optimizations. |
| GoldenQuill (via ontologize, read-only) [SB] | Reference implementation: promotion-record DAG (5 node types, 11 rules), routed self-validating council. |

## Baseline frame: `autoads-evidence-baseline`

autoads is a **new vertical of the ontologize method**: the company is *itself* (or a client) running
ad campaigns; the "operational runs" are creative variants shipped to ad networks; the "outcomes" are
ad-network metrics. The ontologize promotion DAG is the learning loop; ad-network outcomes are the
events feeding it. The open question the rest of the loop must answer: **what is the autoads-specific
pipeline that turns measured outcomes into demonstrably better next-generation creatives, and how does
auto-research feed it candidates?**

Coverage: complete for method substrate. Gap flagged for research decision: how real ad networks expose
outcome metrics and attribution windows (external).
