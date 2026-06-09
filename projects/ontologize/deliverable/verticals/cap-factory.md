# Vertical instantiation — Cap factory (continuous production)

> **Candidate. Not a contract. No client data fabricated.** Every value below is a labeled
> `[PLACEHOLDER]` to be filled from the cap-factory assessment. Reference names ("cap factory") are
> pilot references, **not** signed engagements. Claims tagged `[proven]` / `[hypothesis]`.

This file instantiates the shared template (overview → brief → appendix → decisions → gaps) for a
continuous-production manufacturer. The core sections are **not** re-written here; only the
vertical-specific slots are.

## Ontology axes `[hypothesis — confirm in assessment]`

- **Subject axis:** product lines / SKUs. `[PLACEHOLDER — actual subject cards]`
- **Mechanism axis:** order / sales channel (wholesale / retail / custom / e-com).
  `[PLACEHOLDER — actual mechanism cards]`
- Orthogonality check: `[PLACEHOLDER — confirm no baked subject↔mechanism coupling]`. **[proven]** the
  coupling-violation guard exists.

## Run boundary `[hypothesis — the named design risk]`

A "run" = a production **lot** OR an order-fulfillment **cycle** — continuous flow makes this ambiguous.
**This must be decided in assessment (decision D7).** `[PLACEHOLDER — lot or order]`.

## Event catalog `[hypothesis]`

`lot_completed`, `defect_logged`, `order_shipped`, `order_accepted`, `return_received`, `rework_logged`.
`[PLACEHOLDER — confirmed events + source systems]`.

## BI lever — proof metric `[hypothesis — decision D4]`

Candidate: **defect / rework rate** (defects ÷ lots) OR **on-time order fulfillment**, traced to its
evidence chain. `[PLACEHOLDER — chosen metric]`.

| Field | Value |
| --- | --- |
| numerator | `[PLACEHOLDER]` |
| denominator | `[PLACEHOLDER]` |
| period | `[PLACEHOLDER]` |
| source events | `[PLACEHOLDER]` |
| interpretation limit | `[PLACEHOLDER]` |
| baseline | `[PLACEHOLDER — pre-pilot value]` |
| post value | `[PLACEHOLDER — measured]` |
| `veracidade` | `[PLACEHOLDER — should be high with receipts]` |
| `evidence_refs` | `[PLACEHOLDER — non-empty for high]` |

## Delivery lane `[hypothesis]`

Candidate: **Lane A** surface (ERP-centric, continuous, wants dashboards) + optional Lane-B governance
overlay for the promotion DAG. `[PLACEHOLDER — confirmed lane + per-key justification]`.

## Owner decisions

Use `client_decisions.md` D1–D7; record cap-factory answers here: `[PLACEHOLDER]`.

## Buyer-readiness

Score the `gaps/buyer-readiness.md` rubric for cap factory: `[PLACEHOLDER]`. **[hypothesis]** run boundary
(lot vs order) is the dimension most likely to score low first.
