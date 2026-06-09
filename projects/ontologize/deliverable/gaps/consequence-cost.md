# Gap 3 — Consequence / cost statement per decision

> **Candidate. Not a contract.** Claims tagged `[proven]` / `[hypothesis]`. Closes the third inherited
> GoldenQuill gap: GoldenQuill asked the buyer to make decisions but never stated what each decision
> *costs or risks*. **Note: "cost" here means operational risk and effort, not price.** No pricing.

Each statement pairs with an owner decision in `client_decisions.md` (D1–D7).

## C1 — Reuse authority (D1)

- **If under-scoped (too many approvers):** private or context-specific lessons get promoted to shared
  "truth"; the privacy boundary erodes.
- **If over-scoped (one bottleneck):** the learning loop stalls — candidates pile up unreviewed (visible
  as rising backlog age in `gaps/meta-metrics.md`).
- **Effort:** the named owner spends review time each cadence. `[PLACEHOLDER — time per cadence]`.

## C2 — Privacy boundary (D2)

- **If wrong toward open:** confidential client/segment signal leaks into shared reuse — the highest-
  severity failure.
- **Mitigation built in:** the register is **fail-closed** — unknown classification defaults to
  restricted, so the *cheap* error is over-restriction, not leakage. **[proven]**.
- **Effort:** classifying fields up front; re-classifying new fields as they appear.

## C3 — Evidence sources (D3)

- **If too permissive:** events admitted without real provenance; `veracidade: high` claims become
  hollow and the meta-metrics lie.
- **If too strict:** real outcomes get rejected at the door and the DAG starves.
- **Effort:** agreeing accepted source types; wiring exports from each system.

## C4 — KPI priority / proof metric (D4)

- **If wrong:** the pilot proves a metric nobody acts on — value is real but unrecognized; the
  engagement looks like ordinary analytics. (This is the differentiation risk in the positioning
  decision.)
- **Mitigation:** lead with a number the owner *already distrusts* (see buyer-readiness rubric).
- **Effort:** defining the denominator and source chain precisely enough to reproduce.

## C5 — Decision cadence (D5)

- **Too slow:** lessons go stale; the system logs instead of learns.
- **Too fast:** owners flooded with low-value candidates; review quality drops.
- **Effort:** the recurring review block; tuning frequency/severity thresholds. **[hypothesis]** cadence
  is pilot tuning.

## C6 — Delivery lane (D6)

- **Lane B promised without bridges:** two of the five bridges are NET-NEW builds; promising Lane B
  before they exist over-commits. **[hypothesis]**.
- **Lane A past its ceiling:** the spreadsheet variant tops out around an illustrative
  order-of-magnitude of ~10k events/month (not a measured limit); beyond that needs a DB
  migration. **[hypothesis]**.
- **Effort:** adoption lift is higher for Lane B; sovereignty/dashboard trade-offs differ per lane.

## C7 — Run boundary (D7)

- **If mis-defined (esp. cap factory lot vs order):** every denominator downstream is mis-scoped; the
  whole metric set inherits the error. This is the single highest-leverage decision.
- **Mitigation:** resolved explicitly in assessment before any layer installs. **[proven]** layer-gating
  (a layer installs only after the prior produced evidence) contains the blast radius.
- **Effort:** modeling the run lifecycle for continuous production.

---

## The standing cost the buyer keeps

Beyond per-decision costs: the governed loop has an **ongoing operating cost** — the owner's review time
and the discipline of not promoting lessons too early. **[hypothesis]** the "candidates only"
guardrail is deliberately a *cost* (slower promotion) bought in exchange for trustworthy reuse. We state
this plainly rather than imply the loop is free.
