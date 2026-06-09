# Gap 1 — Meta-metrics: does the governance layer itself work?

> **Candidate. Not a contract.** Claims tagged `[proven]` / `[hypothesis]`. This section closes the
> first inherited GoldenQuill gap: GoldenQuill measured the business but did not measure whether its
> *governance layer* was working.

## The question

We install a governed learning loop. How do we know the **loop itself** is healthy — not just the
business metrics it produces? A governance layer can rot silently: lessons get promoted on thin evidence,
candidates pile up unreviewed, gates stop firing.

## The lever the graded-BI model gives us

Because every promoted lesson carries a `veracidade` grade + `evidence_refs` (reference appendix §2), the
governance layer becomes measurable. **[hypothesis]** these meta-metrics are an adaptation enabled by the
per-node grade; validated by computing them on the pilot's own ledger.

| Meta-metric | Question it answers | Source |
| --- | --- | --- |
| **Promotion evidence quality** | *What fraction of promoted KnowledgeProjections were `veracidade: high` at decision time?* | `promotion_events` ledger |
| **Override rate** | What fraction of promotions used a `veracidade: low` strategic-bet override? (high = governance being bent) | ledger `gate_results` |
| **Gate-block rate** | What fraction of candidates were blocked, and on which rule? (zero blocks = gates may not be firing) | `GATE_BLOCK` rows |
| **Candidate backlog age** | Median age of unreviewed candidates. (rising = the human gate is a bottleneck) | N4 nodes vs N5 timestamps |
| **Contradiction-resolution time** | How long open `contradicts` edges block promotion before an owner resolves them. | edge timestamps |
| **Drift-to-candidate latency** | How long a `drifts_from` signal sits before becoming a candidate. | N3/N1 vs N4 timestamps |

## Why each is computable now

**[proven]** the `promotion_events` ledger records actor, action, per-rule gate results, `veracidade`,
and `evidence_refs` on every mutation, including blocks — so each meta-metric above is a query over rows
that already exist, not a new instrument.

## Honest limit

**[hypothesis]** these are *health indicators*, not a proof the governance is correct. A high
`veracidade: high` promotion rate means promotions carried receipts — it does **not** prove the receipts
were the *right* evidence. Owner judgment (N5) remains the trust gate; the meta-metrics make that
judgment auditable, not automatic.

## What the client sees

A small governance-health panel alongside the business dashboard. `[PLACEHOLDER — target thresholds set
in pilot]` — e.g. "promotions with `veracidade: high` ≥ X%", "candidate backlog age ≤ Y days".
