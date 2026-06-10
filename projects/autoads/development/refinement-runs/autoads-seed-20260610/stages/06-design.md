# Stage 6 — Invoke Design (parent synthesis of role fanout)

- **Capability:** `invoke` · mode `design` · pattern `fanout` · join `parent_synthesis` · **verdict: pass**

Synthesizes four role-bound design artifacts (all verdict `pass`):

| Role | Artifact | Owns |
|------|----------|------|
| ontology-reuse | [`06-design-ontology-reuse.md`](06-design-ontology-reuse.md) | ontology cards + DAG mapping |
| creative-pipeline | [`06-design-creative-pipeline.md`](06-design-creative-pipeline.md) | generation→measurement→improvement loop |
| ad-network-measurement | [`06-design-ad-network-measurement.md`](06-design-ad-network-measurement.md) | outcome schema, KPIs, data governance |
| auto-research | [`06-design-auto-research.md`](06-design-auto-research.md) | governed candidate research |

## Architecture (the Creative Learning Cycle, fully specified)

```
[Auto-Research]  --candidate (governed)-->  [Creative Generator]
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

## Tournament resolutions (T1–T3, with rationale)

- **T1 ontology granularity → per (audience × family × objective) cards** [adapt]. Reusing cards across
  networks separates network-variance (Execution DAG) from creative meaning (Promotion DAG) and matches
  ontologize's cross-vertical generalization stance.
- **T2 generation strategy → template-library-first, LLM as constrained exploration** [adapt/H].
  Promoted patterns become templates via ontology cards; LLM proposes within card vocabulary. Keeps
  generation auditable (every variant traces to a card + template + hypothesis).
- **T3 promotion cadence → batch windowed promotion with signaling gates** [adapt]. Response windows are
  immutable at family creation (per optimization-chain method); avoids the bandit's "promote before the
  window closes" violation of metric≠authority. Online signaling may *flag* but not *promote*.

## Cross-cutting decisions

- **Data governance (fail-closed):** ad-network fields carry an authority class; PII/identifier fields
  are rejected at the boundary, spend is private, aggregate CTR is shareable. No real credentials/PII in
  the seed. [adapt of ontologize register]
- **Auto-research never bypasses review:** external/auto candidates enter as `candidate` and must pass
  review gates + owner decision before reaching the Generator's hypothesis pool. [adapt]
- **Exploration guardrail:** promotion-weighted decay + a residue/external quota forces re-evaluation so
  auto-research does not overfit to past winners. [H]

## Carried residue → distill-repair / plan

1. Network-specific outcome schemas + native response windows remain [H] → bounded-research before pilot.
2. Confound thresholds (min sample, significance test) are pilot-tuned; the gate framework exists, the
   numbers do not.
3. Auto-research ↔ generator card-vocabulary update interface needs one concrete contract.
