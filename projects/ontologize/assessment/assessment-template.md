# Assessment Instrument (blank template) — CyberAlchemy ontology+DAG engagement

> **Status: candidate template.** Blank intake; fill once per vertical. No pricing, contracts, or
> named-client commitments. "cap factory" / "logistics company" are pilot references only. Method
> assertions are tagged **[SB]** source-backed / **[H]** hypothesis. — *candidate-only.*

**How to fill:** work A → E top to bottom (the order is the [IDS-1](../PLAN.md) rule order [SB]). Each
field has a *prompt* in italics telling you what to elicit. Leave nothing blank — if a field truly
does not apply, write `n/a — <reason>` so a reviewer can tell "empty" from "absent." A worked
hypothetical fill is in [`worked-example.md`](worked-example.md).

---

## Header

| Field | Value | Prompt |
| --- | --- | --- |
| Vertical / engagement | | *Pilot reference name, e.g. "logistics company" or "cap factory". Not a signed client.* |
| Production shape | continuous ▢ / discrete ▢ | *Continuous production (cap-factory-like) or discrete runs (logistics-like)? Drives A.3.* |
| Assessor | | *Who ran the intake.* |
| Date | | |
| Interview sources | | *Who was interviewed + which systems/sample data were seen. Inventories are only as good as these.* |

---

## Section A — Two-axis ontology mapping (B1 business + B3 run-context)

> Produces the `ontology-map`: **subject/segment axis × value-mechanism axis** as cards, plus the
> **run-context** primitives, plus the **orthogonality check**. The two axes populate **B1 — business**
> (canonical; aliases meaning/domain/intent) [SB [RECONCILIATION.md](../RECONCILIATION.md) §1]. The
> two axes must stay **orthogonal** — any baked subject→mechanism binding is a coupling violation and
> is rejected at A.4. [SB [PRODUCT.md](../PRODUCT.md) "coupling-violation guard"; [PLAN.md](../PLAN.md):27]

### A.1 — Subject / segment axis cards (who/what the client serves)

*Prompt: elicit who or what the client serves — customer segments, lanes, product lines, SKUs.
One card per distinct subject. Capture the four card primitives so the card configures
behavior downstream, never just a label. [SB [PRODUCT.md](../PRODUCT.md) method L1; [PLAN.md](../PLAN.md):29]*

Repeat this card per subject (≥1 required):

- **Subject card name:** *(e.g. a segment, lane, or product line)*
- **What it is:** *one-line definition*
- **Search vocabulary:** *the terms/keywords this subject's work is described in*
- **Evidence schema:** *what counts as evidence for this subject (record/field shapes)*
- **Language register:** *how reporting for this subject is phrased (operational, executive, regulatory)*
- **Reporting rhythm:** *cadence this subject is reported on (per-shift, daily, per-shipment, monthly)*

### A.2 — Value-mechanism axis cards (how value flows)

*Prompt: elicit how value flows — order types, shipment/contract types, channels. One card per
mechanism. Same four primitives. The mechanism is "how," independent of "who" (A.1). [SB [PLAN.md](../PLAN.md):26]*

Repeat this card per mechanism (≥1 required):

- **Mechanism card name:** *(e.g. an order type, shipment type, channel)*
- **What it is:** *one-line definition*
- **Search vocabulary:**
- **Evidence schema:**
- **Language register:**
- **Reporting rhythm:**

### A.3 — Run-context (B3) primitives

> **B3 — run-context** is the bounded run that defines metric **denominators**. Named "run-context"
> (not "operational ontology") to avoid colliding with the arcanum "Operational Ontology =
> agent-operation knowledge" branch [SB [RECONCILIATION.md](../RECONCILIATION.md) §1 B3]. Denominators
> live *inside* a run context, so "stage ≠ outcome" and honest denominators are a **branch boundary**.
> [SB [ONTOLOGY-BRANCHES.md](../ONTOLOGY-BRANCHES.md):28-30]

| Primitive | Value | Prompt |
| --- | --- | --- |
| **Run boundary** | | *What is one "run"? (logistics: a shipment id; cap factory: a lot or an order — decide which).* |
| **Org scope** | | *Whose run is it — which org/site/line owns it?* |
| **Lifecycle state set** | | *The states a run moves through (e.g. created → in-progress → delivered → closed).* |
| **Deadline / posture** | | *Any deadline or risk posture attached to a run.* |
| **Denominator definition** | | *Given the run boundary, what is the denominator for "rate" metrics? (e.g. shipments-in-window, lots-completed). Anti-collapse.* |

> **Edge case — continuous production with no discrete run** [SB [PLAN.md](../PLAN.md):32]: if the
> client cannot name a discrete run, **do not force one.** Record the candidate boundaries here and
> flag the **run-boundary decision** as open (resolved later in the pilot, not in this instrument):
>
> - Candidate run boundaries considered: ________________
> - **Run-boundary decision status:** decided ▢ (value above) / **OPEN — flagged** ▢

### A.4 — Orthogonality check (coupling-violation guard) — REQUIRED

> The two axes must be **independent**: any (subject × mechanism) pair must be reachable in principle.
> A baked subject→mechanism binding (e.g. "segment X always uses mechanism Y") is a **category error**
> — it falsely constrains the model and is rejected. Matching is **runtime / per-event**, never
> hardcoded at design time. This mirrors GoldenQuill's CIC × CLC orthogonality + the
> F-CIC-CLC-COUPLING-VIOLATION fail-closed guard. [SB [PRODUCT.md](../PRODUCT.md) method L1;
> `projects/goldenquill/CLAUDE.md` "CICs and CLCs do not have hardcoded coupling"]

**How the check works** (run it before leaving Section A):

1. **Reachability sweep.** For each subject card (A.1), confirm that **more than one** mechanism card
   (A.2) can in principle apply to it. If a subject can only ever pair with exactly one mechanism, the
   axes are coupled — STOP.
2. **No-baked-binding assertion.** Confirm no card text, no proposed rule, and no system field encodes
   a fixed subject→mechanism mapping. The mapping is observed per run, not declared.
3. **Collapse test.** If the two axes describe the same distinction in two words (the "axes collapse
   into one" failure [SB [PLAN.md](../PLAN.md):35]), they are not two axes — re-interview; **do not
   force** an artificial second axis.

| Check | Result | Note |
| --- | --- | --- |
| Reachability sweep — every subject reaches >1 mechanism? | PASS ▢ / FAIL ▢ | *List any subject that reaches only one mechanism.* |
| No baked subject→mechanism binding anywhere? | PASS ▢ / FAIL ▢ | *Name any binding found.* |
| Axes are genuinely distinct (no collapse)? | PASS ▢ / FAIL ▢ | *If FAIL: re-interview, do not force.* |

**Runtime match rule** (the `match_rule` IDS-1 output): *state the rule that pairs a subject with a
mechanism at runtime — e.g. "the incoming event's lane + service type select the subject card; the
order/shipment type selects the mechanism card; the pair is resolved per event." This is the
`match_rule: runtime`, NOT a static table.* [SB [PLAN.md](../PLAN.md):24]

> **Gate:** if any A.4 row is FAIL, the ontology-map is **not** complete. Resolve (re-interview) before
> Sections B–E carry forward an invalid map.

---

## Section B — Data inventory (B2 system sources) + scale/residency

> Produces the `data-inventory`. Each source gets an owner + a sensitivity guess [SB [PLAN.md](../PLAN.md):29].
> Columns marked **(lane)** double as Section E lane-selection inputs. [SB [WORK-PACK.md](../WORK-PACK.md) T2b]

| # | Source / system | Type | Owner | Event types it emits | Residency **(lane)** | Sensitivity guess | Volume ≈events/mo **(lane)** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | | *ERP / TMS / order / MES / spreadsheet / BI tool* | *role who owns it* | *e.g. delivered, defect_logged, cost_posted* | *cloud / on-prem / must-stay-local* | *public / shareable / confidential* | *order of magnitude* |
| 2 | | | | | | | |
| … | | | | | | | |

- **Event types catalog** *(prompt: list every business event the systems emit — these become the
  promotion-DAG OutcomeEvents later. Logistics e.g. `delivered`, `delivery_exception`, `cost_posted`,
  `claim_filed`; cap factory e.g. `lot_completed`, `defect_logged`, `rework_logged`.* [SB
  [ONTOLOGY-BRANCHES.md](../ONTOLOGY-BRANCHES.md):59-67]*):*
- **Total scale (≈events/mo):** ________________ *(prompt: sum / dominant order of magnitude; the
  ~10k events/mo threshold is an illustrative lane signal, not a measured limit [SB [DELIVERY-LANES.md](../DELIVERY-LANES.md)]*
- **Residency constraint (overall):** ________________ *(prompt: must data stay in existing systems /
  on-prem? Hard constraints feed Lane A; "cloud OK" opens Lane B.)*
- **Data-access blocker?** none ▢ / **BLOCKED — flag** ▢ *(prompt: if the client cannot grant data
  access, the pilot (S2) is blocked for this vertical [SB [PLAN.md](../PLAN.md):34] — flag here.)*

---

## Section C — Agent inventory

> Produces the `agent-inventory` [SB [PLAN.md](../PLAN.md):30]. If the client runs **no** agents, this
> is still filled: write "none — greenfield," and Section D maturity = 0 (the agent layer is
> greenfield) [SB [PLAN.md](../PLAN.md):33].

| # | Agent / automation | What it does | Triggers / inputs | Governance state | Touches what data |
| --- | --- | --- | --- | --- | --- |
| 1 | | *task it performs* | *what kicks it off* | *ungoverned / ad-hoc rules / has guardrails+validation* | *which Section B sources* |
| … | | | | | |

- **If no agents:** `none — greenfield` ▢ → Section D scored 0 across all rules; agent layer is a
  net-new install in the pilot.
- **Dashboard demand (lane):** none ▢ / nice-to-have ▢ / **required** ▢ *(prompt: does the client
  demand a visual dashboard? "required" pulls toward Lane A [SB [DELIVERY-LANES.md](../DELIVERY-LANES.md)].
  Carried to Section E.)*

---

## Section D — Four-Autonomy maturity rubric (score each rule 0–3)

> Scores the client's current agent practice against the **canonical Four Autonomy Rules**
> (Save State Always · Test Your Own Work · Be Explicit · Clean Output) — source-backed in
> `projects/goldenquill/SOUL.md:40-50` and [DEFINITIONS.md](../DEFINITIONS.md):56. [SB] Score **0–3**
> per rule using the level descriptors in [`maturity-rubric.md`](maturity-rubric.md). A client with no
> agents scores 0 on all four (greenfield) [SB [PLAN.md](../PLAN.md):33].

| Rule | Score (0–3) | Evidence for the score (what you observed) |
| --- | --- | --- |
| **R1 — Save State Always** *(state persisted on success AND failure)* | | |
| **R2 — Test Your Own Work** *(agents validate before marking complete)* | | |
| **R3 — Be Explicit** *(tasks carry input/output paths, scope, done-definition)* | | |
| **R4 — Clean Output** *(structured output stripped/validated, not raw LLM)* | | |
| **Maturity total** (0–12) | | *sum; descriptive only — not a pass/fail gate* |

*Prompt: score against the descriptors in the rubric file; cite the observed behavior, not intent.
"They plan to" = the lower level. The total is a maturity read, used as a Section E lane input.*

---

## Section E — Lane-selection input capture (for T2b)

> Captures the **five observable facts** the lane-selection rule needs [SB [WORK-PACK.md](../WORK-PACK.md)
> T2b; [DELIVERY-LANES.md](../DELIVERY-LANES.md) selection rule]. **This instrument records the facts; it
> does NOT choose the lane** — lane selection is T2b, done after the assessment. Capture facts, not a
> preference.

| # | Lane-selection input | Observed value | Pulls toward | Source field |
| --- | --- | --- | --- | --- |
| 1 | **Data residency** | | must-stay-local → Lane A · cloud-OK → opens Lane B | Section B residency |
| 2 | **Scale (≈events/mo)** | | <~10k → Lane A viable · higher → DB/Lane B | Section B volume |
| 3 | **Agent maturity** | | low/greenfield → A or hybrid · agent-first → Lane B | Section D total |
| 4 | **Dashboard demand** | | required → Lane A surface | Section C dashboard demand |
| 5 | **Adoption appetite** | | will adopt harness discipline → Lane B · wants no-new-platform → Lane A | *prompt: interview — appetite for new tooling/discipline* |

*Note for T2b (not decided here):* the [DELIVERY-LANES.md](../DELIVERY-LANES.md) rule maps these to Lane A
/ Lane B / Hybrid, with **Hybrid the usual answer** when both pull (data+BI local, governance on
Arcanum). [SB [DELIVERY-LANES.md](../DELIVERY-LANES.md)]

---

## Sign-off (S1 validation gate)

> The assessment passes only when the client confirms the map + inventories reflect reality [SB
> [PLAN.md](../PLAN.md):36; [WORK-PACK.md](../WORK-PACK.md) T2 acceptance].

| Check | Status |
| --- | --- |
| Ontology-map has ≥1 subject card × ≥1 mechanism card | ▢ |
| Orthogonality check (A.4) all PASS (or resolved by re-interview) | ▢ |
| Runtime match rule stated (no baked binding) | ▢ |
| Run-boundary decided OR explicitly flagged open (A.3) | ▢ |
| Data inventory has owner + sensitivity per source | ▢ |
| Agent inventory complete (or "none — greenfield") | ▢ |
| Maturity scored 0–3 on all four rules | ▢ |
| All five lane-selection inputs captured (E) | ▢ |
| **Client confirms the map + inventories are accurate** | ▢ |

Client confirmation by: ________________  Date: __________
