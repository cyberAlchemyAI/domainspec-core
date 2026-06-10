# autoads — DESIGN

> Seeded by refine run `autoads-seed-20260610` (4-role design fanout). Canonical detail in
> [stages/06-design.md](development/refinement-runs/autoads-seed-20260610/stages/06-design.md) and the
> four role artifacts. Claims labeled **[SB]** / **[adapt]** / **[H]**.

## Architecture — the Creative Learning Cycle

```
[Auto-Research] --candidate (governed)--> [Creative Generator]
                                               | variant (lineage, hypothesis_ref)
                                               v
                                       [Network Adapter]  (system-agnostic contract)
                                               | dispatch / pull outcomes
                                               v
                                       [Outcome Measurement] --> KPI families (veracidade + evidence_refs, response window)
                                               v
                                       [Grader]  (metric != authority: confound + min-confidence gates)
                                               v
                                       [Promotion DAG]  candidate -> review gates -> OWNER DECISION -> promote | retire
                                               v
                                       [Feedback Loop] --> re-parameterize Generator + feed Auto-Research memory
```

## Components

| Component | Role | ontologize anchor |
|-----------|------|-------------------|
| Creative Generator | Variants from ontology card + candidate hypothesis (template-first, constrained LLM). | ontology cards [adapt] |
| Network Adapter | System-agnostic dispatch/pull contract; not locked to one network. | data-governance edge [adapt] |
| Outcome Measurement | Normalizes network metrics into KPI families over a response window. | evidence-linked KPIs [SB] |
| Grader | `veracidade` + `evidence_refs`; blocks promotion on confound/low confidence. | metric≠authority [SB] |
| Promotion DAG | Review gates → owner decision; reuses the 11-rule pattern. | promotion DAG [SB] |
| Auto-Research | Governed candidates from internal residue + external signals; never bypasses review. | candidate→review→owner [adapt] |
| Feedback Loop | Promoted patterns + residue re-parameterize the Generator. | optimization-chain method [SB] |

## Key design decisions (tournament resolutions)

- **Ontology granularity:** per (audience × family × objective) cards, reused across networks. [adapt]
- **Generation:** template-library-first; LLM proposes within card vocabulary → auditable lineage. [adapt/H]
- **Promotion cadence:** batch windowed promotion; response windows immutable at family creation; online
  signals may flag but never promote. [adapt]
- **Data governance (fail-closed):** PII/identifier fields rejected at boundary, spend private, aggregate
  CTR shareable; no real credentials/PII in the seed. [adapt]
- **Auto-research guardrail:** promotion-weighted decay + residue/external quota prevents overfitting to
  past winners. [H]

## Open hypotheses (→ PLAN backlog)

H1 network outcome schema/windows · H2 confound thresholds · H3 auto-research↔generator card contract ·
H4 ads generalization of the ontologize loop. See
[stages/08-distill-repair.md](development/refinement-runs/autoads-seed-20260610/stages/08-distill-repair.md).
