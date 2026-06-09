# Vertical instantiation — Logistics company (discrete shipment runs)

> **Candidate. Not a contract. No client data fabricated.** Every value below is a labeled
> `[PLACEHOLDER]` to be filled from the logistics assessment. Reference names ("logistics company") are
> pilot references, **not** signed engagements. Claims tagged `[proven]` / `[hypothesis]`.

This file instantiates the shared template for a discrete-run logistics company. The discrete-shipment
model maps almost 1:1 to the GoldenQuill grant-run DAG — **lowest design risk** of the two verticals.
Only the vertical-specific slots appear here.

## Ontology axes `[hypothesis — confirm in assessment]`

- **Subject axis:** clients / lanes. `[PLACEHOLDER — actual subject cards]`
- **Mechanism axis:** shipment / contract type. `[PLACEHOLDER — actual mechanism cards]`
- Orthogonality check: `[PLACEHOLDER — confirm no baked coupling]`. **[proven]** coupling-violation guard.

## Run boundary `[hypothesis — clean]`

A "run" = a **shipment** (clean discrete boundary, low risk). `[PLACEHOLDER — confirm shipment as run]`.

## Event catalog `[hypothesis]`

`shipment_booked`, `picked_up`, `delivered`, `delivery_exception` (late/damaged), `cost_posted`,
`claim_filed`. `[PLACEHOLDER — confirmed events + source systems (TMS)]`.

## BI lever — proof metric `[hypothesis — decision D4]`

Candidate: **on-time-delivery rate** (on-time ÷ *delivered*, not ÷ *booked*) OR **cost-per-lane**, traced
to its evidence chain. `[PLACEHOLDER — chosen metric]`.

| Field | Value |
| --- | --- |
| numerator | `[PLACEHOLDER]` |
| denominator | `[PLACEHOLDER — e.g. delivered, not booked]` |
| period | `[PLACEHOLDER]` |
| source events | `[PLACEHOLDER]` |
| interpretation limit | `[PLACEHOLDER — e.g. does not count cancellations]` |
| baseline | `[PLACEHOLDER — pre-pilot value]` |
| post value | `[PLACEHOLDER — measured]` |
| `veracidade` | `[PLACEHOLDER — should be high with receipts]` |
| `evidence_refs` | `[PLACEHOLDER — non-empty for high]` |

## Delivery lane `[hypothesis]`

Candidate: **Hybrid** — Lane A TMS/BI surface + Lane B governed carrier-rule promotion (clean runs +
carrier-rule learning + likely routing agents). `[PLACEHOLDER — confirmed lane + per-key justification]`.

## Owner decisions

Use `client_decisions.md` D1–D7; record logistics answers here: `[PLACEHOLDER]`.

## Buyer-readiness

Score the `gaps/buyer-readiness.md` rubric for logistics: `[PLACEHOLDER]`. Discrete shipment runs and a
TMS export typically score the data/run-definition dimensions higher than continuous production.
**[hypothesis]**.
