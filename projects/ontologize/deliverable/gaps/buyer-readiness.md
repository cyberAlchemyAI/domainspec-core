# Gap 2 — Buyer-readiness scaffolding

> **Candidate. Not a contract.** Claims tagged `[proven]` / `[hypothesis]`. Closes the second inherited
> GoldenQuill gap: the GoldenQuill package described the offer but gave the buyer no way to assess
> whether *they* were ready for it.

## The question a buyer should be able to answer before saying yes

*"Is my organization ready to get value from this, or will it stall?"* This section is a self-assessment
the buyer fills in honestly. None of it requires CyberAlchemy to be present.

## Readiness rubric (score each 0–3)

`[PLACEHOLDER — buyer scores each row]`. 0 = absent, 1 = ad hoc, 2 = partial, 3 = solid.

| Dimension | What "ready" looks like | Why it matters |
| --- | --- | --- |
| **Run definition** | You can name one repeatable unit of work (a shipment, a lot, an order). | The DAG has nothing to attach to without it. (See decision D7.) |
| **Source-backed data** | Outcomes live in a system you can export, not only in memory. | The source-truth gate rejects events with no provenance. |
| **A real owner** | One named person can approve/reject reuse and is available for review cadence. | The OwnerDecision gate (N5) is a human role; no owner = no promotion. |
| **A metric you distrust** | You have a number you currently second-guess. | That is the BI lever — the fastest provable value. |
| **Data-boundary clarity** | You know which fields are sensitive. | Drives the classification register; fail-closed needs a starting map. |
| **Agent posture** | You know whether agents touch this workflow (and how mature). | Selects the delivery lane and whether agent governance is in scope. |
| **Review appetite** | An owner will spend ~`[PLACEHOLDER]` per cadence on candidate review. | The loop improves only if someone reviews candidates. |

## Reading the score

- **Mostly 2–3:** ready for a full pilot (assessment → design → pilot → handoff).
- **Mixed, with run-definition or owner at 0–1:** start with a scoped assessment only; resolve those two
  before installing anything. **[proven]** run-definition and a human owner are structural requirements
  in the reference build, not preferences.
- **Mostly 0–1:** not yet ready; the engagement would stall. Honest answer: defer.

## Readiness is per-vertical

A buyer may be ready in one vertical and not another. Score each vertical separately — the parallel
cap-factory / logistics pilots exist partly because readiness differs by vertical. **[hypothesis]** the
cap-factory run boundary (lot vs order) is the readiness item most likely to score low first.

## What CyberAlchemy commits to here

If the rubric surfaces a 0–1 on a structural dimension, we say so and scope a smaller first step rather
than sell a pilot that will stall. **[hypothesis]** mirrors the "candidates only / no premature
promotion" discipline applied to the engagement itself.
