# CyberAlchemy — Owner Decisions (the implementation spec)

> **Candidate. Not a contract.** These are the decisions the client owner confirms; once answered they
> become the implementation spec for the pilot. Each decision is paired with its **cost / consequence**
> (the full statement lives in `gaps/consequence-cost.md`, gap #3). No pricing or named-client
> commitments. Claims tagged `[proven]` / `[hypothesis]`.

Fill each `[PLACEHOLDER]` from the assessment — do not pre-fill from assumption.

## D1 — Reuse authority

**Who may approve a lesson for reuse beyond its original context?**
This person *is* the human OwnerDecision gate (N5). **[proven]** reuse requires an explicit owner
decision in the reference build.

- Answer: `[PLACEHOLDER — role/name from assessment]`
- **Consequence if wrong:** the wrong approver promotes lessons that should stay private, or a bottleneck
  stalls the loop. See cost statement C1.

## D2 — Privacy boundary

**Which data must always stay private, and which generalized lessons may be reused after approval?**
Drives the signed classification register and the redaction gate. **[proven]** the privacy boundary gate
exists.

- Answer: `[PLACEHOLDER — private classes + shareable-after-approval classes]`
- **Consequence if wrong:** confidential signal leaks into shared "truth" (fail-open). The register
  defaults fail-closed precisely to make this the safe direction. See cost statement C2.

## D3 — Evidence sources

**Which source types count as proof for a fact** (system export, signed record, operator-confirmed
entry, …)? No OutcomeEvent without one. **[proven]** source-truth gate.

- Answer: `[PLACEHOLDER — accepted source types]`
- **Consequence if wrong:** events admitted without real provenance — `veracidade: high` claims become
  hollow. See cost statement C3.

## D4 — KPI priority (the BI lever — decide first)

**Which KPI family matters most for the first dashboard, and which single metric is the pilot proof
metric?** This is the lead decision because BI is the lever. **[hypothesis]** candidate metrics per
vertical are in the reference appendix §3.

- Answer: `[PLACEHOLDER — priority family + one proof metric + its denominator]`
- **Consequence if wrong:** the pilot proves a metric the business does not care about. See cost
  statement C4.

## D5 — Decision cadence

**When are lessons reviewed** (per N runs, per quarter, after each outcome)? Sets the reflection cadence
and the manual promotion-scorer batch. **[hypothesis]** cadence/thresholds are pilot tuning.

- Answer: `[PLACEHOLDER — cadence + thresholds]`
- **Consequence if wrong:** stale lessons accumulate or owners are flooded with low-value candidates.
  See cost statement C5.

## D6 — Delivery lane

**Lane A (your tools), Lane B (Arcanum), or Hybrid?** Decided from observable facts (data residency,
scale, agent maturity, dashboard demand). **[proven]** the selection rule is decidable from facts;
**[hypothesis]** Lane B's five bridges are scoped before being promised.

- Answer: `[PLACEHOLDER — lane + one-line justification per selection key]`
- **Consequence if wrong:** Lane B promised without bridges built, or Lane A chosen past its
  ~10k-events/month ceiling (illustrative order-of-magnitude, not a measured limit). See cost statement C6.

## D7 — Run boundary

**What is one "run"?** (logistics = a shipment, clean; cap factory = a lot *or* an order — must be
decided). **[hypothesis]** the cap-factory run boundary is the named design risk.

- Answer: `[PLACEHOLDER — run definition for this vertical]`
- **Consequence if wrong:** the whole DAG's denominators are mis-scoped; every downstream metric inherits
  the error. See cost statement C7.

---

> Each decision maps to a cost statement (C1–C7) in `gaps/consequence-cost.md`. The transition plan in
> `gaps/transition-plan.md` sequences when each decision must be locked.
