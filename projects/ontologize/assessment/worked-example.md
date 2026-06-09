# Worked Example (ILLUSTRATIVE — FABRICATED) — Assessment fill

> **⚠ This is a fabricated, illustrative fill. No real client. All values are invented to show a peer
> what a complete assessment looks like end to end.** Candidate-only; no pricing/contracts/named
> clients. The hypothetical is a *logistics-shaped* company called **"Northwind Freight (HYPOTHETICAL)"**
> — a pilot-reference shape, not a signed engagement. A cap-factory fill would use the same structure
> with continuous-production values (see notes at the end). — *candidate-only, illustrative.*

This demonstrates the T1 check: *a peer can fill it for a hypothetical client without missing fields.*

---

## Header

| Field | Value |
| --- | --- |
| Vertical / engagement | Northwind Freight (HYPOTHETICAL logistics company) |
| Production shape | discrete ☑ |
| Assessor | (illustrative) |
| Date | (illustrative) |
| Interview sources | (illustrative) ops lead + data analyst interviewed; saw TMS export sample, BI dashboard, no agent code |

---

## Section A — Two-axis ontology mapping

### A.1 — Subject / segment axis cards

**Subject card: "Lane A→B (regional express)"**
- What it is: a shipping lane serving regional express customers.
- Search vocabulary: lane id, origin/destination DC, carrier code, service SLA.
- Evidence schema: shipment record (shipment_id, lane, carrier, promised_date, delivered_date).
- Language register: operational (dispatcher-facing) + executive (on-time % rollup).
- Reporting rhythm: per-shipment events, daily on-time rollup.

**Subject card: "Lane C→D (long-haul contract)"**
- What it is: long-haul lane under negotiated contract customers.
- Search vocabulary: contract id, lane id, carrier code, fuel surcharge.
- Evidence schema: shipment record + contract terms reference.
- Language register: operational + contractual/regulatory.
- Reporting rhythm: per-shipment events, monthly contract-performance review.

### A.2 — Value-mechanism axis cards

**Mechanism card: "Spot shipment"**
- What it is: one-off shipment priced at spot rate.
- Search vocabulary: spot rate, booking id, tender accept/reject.
- Evidence schema: booking + rate quote + delivery outcome.
- Language register: operational.
- Reporting rhythm: per-shipment.

**Mechanism card: "Contracted shipment"**
- What it is: shipment fulfilled under a standing carrier contract.
- Search vocabulary: contract id, committed volume, lane rate card.
- Evidence schema: contract + allocation + delivery outcome.
- Language register: contractual.
- Reporting rhythm: per-shipment + monthly contract review.

### A.3 — Run-context (B3) primitives

| Primitive | Value |
| --- | --- |
| Run boundary | one **shipment_id** = one run |
| Org scope | the originating distribution center (DC) |
| Lifecycle state set | booked → tendered → in-transit → delivered → closed (with `delivery_exception` branch) |
| Deadline / posture | promised_date per shipment; winter-weather elevated-risk posture |
| Denominator definition | "on-time %" = on-time deliveries ÷ **shipments closed in the window**, per lane (not per booking — anti-collapse) |

Edge case: discrete runs exist (shipment_id) → **run-boundary decision status: decided.** Candidate
boundaries considered: shipment vs booking; chose shipment (a booking can split into shipments).

### A.4 — Orthogonality check (coupling-violation guard)

| Check | Result | Note |
| --- | --- | --- |
| Reachability sweep — every subject reaches >1 mechanism? | PASS | Lane A→B runs both spot and contracted; Lane C→D runs both. No subject locked to one mechanism. |
| No baked subject→mechanism binding anywhere? | PASS | No card or rule says "regional express = always spot." A 2×2 (subject × mechanism) grid is fully reachable. |
| Axes genuinely distinct (no collapse)? | PASS | "which lane/customer" (subject) ≠ "spot vs contracted" (mechanism) — independent distinctions. |

**Runtime match rule:** *the incoming shipment event's `lane` selects the subject card; its
`booking_type` (spot/contracted) selects the mechanism card; the (subject × mechanism) pair is resolved
per shipment at runtime — never a static table.* (`match_rule: runtime`)

> If, say, Lane C→D could **only** ever be contracted, A.4 row 1 would FAIL and we would either drop
> "contracted" as a separate mechanism or re-interview — we would **not** ship a coupled model.

---

## Section B — Data inventory

| # | Source / system | Type | Owner | Event types | Residency (lane) | Sensitivity | Volume ≈events/mo (lane) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TMS | transport mgmt | ops lead | `delivered`, `delivery_exception`, `cost_posted`, `claim_filed` | cloud-OK | confidential (customer + cost) | ~40k |
| 2 | Order/booking system | order | ops lead | `booking_created`, `tender_accepted`, `tender_rejected` | cloud-OK | confidential | ~15k |
| 3 | BI dashboard (Power BI) | BI tool | data analyst | (derived measures, no raw events) | cloud | shareable (rollups) | n/a |

- **Event types catalog:** `delivered`, `delivery_exception`, `cost_posted`, `claim_filed`,
  `booking_created`, `tender_accepted`, `tender_rejected`.
- **Total scale (≈events/mo):** ~55k → **above** the ~10k spreadsheet ceiling.
- **Residency constraint (overall):** cloud is acceptable; no must-stay-local mandate.
- **Data-access blocker?** none.

---

## Section C — Agent inventory

| # | Agent / automation | What it does | Triggers / inputs | Governance state | Touches |
| --- | --- | --- | --- | --- | --- |
| 1 | Nightly exception emailer | emails ops a list of delivery exceptions | cron @ 02:00, reads TMS export | ungoverned (no validation, silent failures) | TMS source 1 |
| 2 | (none else) | — | — | — | — |

- Not greenfield, but barely: one ungoverned script. Dashboard demand: **required** (the analyst runs
  the business off Power BI).

---

## Section D — Four-Autonomy maturity

| Rule | Score | Evidence |
| --- | --- | --- |
| R1 — Save State Always | 1 | Nightly emailer logs success to a file; failures are silent. |
| R2 — Test Your Own Work | 0 | No validation; humans notice if the email looks wrong. |
| R3 — Be Explicit | 2 | A runbook specifies input export path + output recipients; followed by convention. |
| R4 — Clean Output | 1 | Output is a plain email; format is consistent but never validated. |
| **Maturity total** | **4 / 12** | Low maturity; agent layer is effectively greenfield for governance. |

---

## Section E — Lane-selection inputs (facts only — lane NOT chosen here)

| # | Input | Observed value | Pulls toward |
| --- | --- | --- | --- |
| 1 | Data residency | cloud-OK, no local mandate | opens Lane B |
| 2 | Scale (≈events/mo) | ~55k | above spreadsheet ceiling → DB / Lane B |
| 3 | Agent maturity | 4/12, low | hybrid (governance net-new) |
| 4 | Dashboard demand | required | Lane A surface |
| 5 | Adoption appetite | willing to adopt governed promotion, wants to keep Power BI | both pull → Hybrid |

*T2b would read these and likely select **Hybrid** (BI on Power BI, governed promotion on Arcanum) —
matching the per-vertical candidate for logistics [SB [DELIVERY-LANES.md](../DELIVERY-LANES.md)]. The
assessment itself does **not** make that call.*

---

## Sign-off

| Check | Status |
| --- | --- |
| ≥1 subject × ≥1 mechanism card | ☑ (2 × 2) |
| Orthogonality (A.4) all PASS | ☑ |
| Runtime match rule stated | ☑ |
| Run-boundary decided / flagged | ☑ decided (shipment) |
| Data inventory owner + sensitivity per source | ☑ |
| Agent inventory complete | ☑ |
| Maturity 0–3 each rule | ☑ |
| Five lane inputs captured | ☑ |
| Client confirms accuracy | (illustrative — would be signed) |

---

## Cap-factory note (same structure, continuous shape)

A cap-factory fill uses the identical instrument. The deltas a peer should expect:

- **Production shape:** continuous. **A.3 run boundary:** the run-boundary decision may be **OPEN** —
  lot-as-run vs order-as-run is exactly the continuous-production edge case [SB [PLAN.md](../PLAN.md):32;
  [ONTOLOGY-BRANCHES.md](../ONTOLOGY-BRANCHES.md):60] — flag it open rather than forcing one.
- **A.1 subjects:** product lines / SKUs × customer or sales channel (candidate axes A1 [SB
  [decisions/pilot-and-positioning.md](../decisions/pilot-and-positioning.md) A1]).
- **A.2 mechanisms:** order / channel types.
- **Section B events:** MES — `lot_completed`, `defect_logged`, `rework_logged` [SB
  [ONTOLOGY-BRANCHES.md](../ONTOLOGY-BRANCHES.md):59].
- **Denominator:** e.g. first-pass yield = good lots ÷ **lots completed in window** on a line.

No section is added or removed — proving the instrument is vertical-agnostic.
