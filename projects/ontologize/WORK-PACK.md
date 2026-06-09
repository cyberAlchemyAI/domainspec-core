# WORK-PACK — CyberAlchemy ontology+DAG engagement

Execution manifest mapped from [PLAN.md](PLAN.md). Each SWU is a Smallest Working Unit with one
parent task, an explicit write scope, acceptance evidence, and a reviewable check. Execution owner:
`task-session`. Complexity: high → SWU manifest + per-task SWU lists below.

## Shared SWU manifest

| SWU   | Slice | Layer | Parent task                       | Write scope                                  |
| ----- | ----- | ----- | --------------------------------- | -------------------------------------------- |
| SWU-1 | S1    | L0    | T1 Assessment instrument          | `assessment/` template files                 |
| SWU-2 | S1    | L0    | T2 Run logistics assessment       | `pilots/logistics/assessment.md`             |
| SWU-3 | S2    | L1    | T3 Install method (logistics)     | `pilots/logistics/method/`                   |
| SWU-4 | S3    | L1    | T4 Deliverable template v1        | `deliverable/` + `pilots/logistics/package/` |
| SWU-5 | S4    | L1    | T5 Proof harness (logistics)      | `pilots/logistics/proof.md`, chain fixture   |
| SWU-6 | S5    | L2    | T6 Cap factory parallel run       | `pilots/cap-factory/`                        |
| SWU-7 | S6    | L3    | T7 Cross-vertical + gap hardening | `deliverable/`, `GENERALIZATION.md`          |

Layer gate: SWU-3+ may start only after SWU-2 evidence passes; SWU-6 after SWU-5; SWU-7 after SWU-6.

## Tasks

### T1 — Assessment instrument (SWU-1)

- **Do:** Author the repeatable assessment template per [PLAN IDS-1](PLAN.md): sections for the two
  ontology axes (with operational primitives), data-inventory, agent-inventory, Four-Autonomy maturity
  rubric (0–3 each).
- **Write scope:** `projects/ontologize/assessment/`.
- **Acceptance:** template covers all IDS-1 outputs; orthogonality check present; maturity rubric scorable.
- **Check (reviewable):** a peer can fill it for a hypothetical client without missing fields.

### T2b — Select delivery lane (part of SWU-2)

- **Do:** Apply the [DELIVERY-LANES.md](DELIVERY-LANES.md) selection rule to the assessment facts
  (data residency, scale, agent maturity, dashboard demand, adoption appetite) → choose Lane A, Lane B,
  or Hybrid. If Lane B/Hybrid, scope its five bridges (register, dispatch, 11-rule lint, proof-harness,
  reflection cadence) as explicit build items.
- **Write scope:** append to `pilots/<vertical>/assessment.md`.
- **Acceptance:** a chosen lane with a one-line justification per selection-rule key.
- **Check:** the choice is traceable to observable facts, not preference. **Depends on:** T2.

### T2 — Run logistics assessment (SWU-2)

- **Do:** Use T1 on the logistics company; confirm subject/mechanism axes (validate A1), inventory
  data + agents, score maturity, decide the run definition (shipment).
- **Write scope:** `projects/ontologize/pilots/logistics/assessment.md`.
- **Acceptance:** filled assessment; client confirms accuracy (S1 validation).
- **Check:** ontology-map has ≥1 subject card × ≥1 mechanism card, runtime match rule, no baked binding.
- **Depends on:** T1.

### T3 — Install method, logistics (SWU-3)

- **Do:** Install L-ont → L-reg → L-dag → L-bi per [DESIGN View 2](DESIGN.md) + [PLAN IDS-2](PLAN.md).
  Sign the classification register before any agent runs (G-privacy).
- **Write scope:** `projects/ontologize/pilots/logistics/method/`.
- **Acceptance:** four layers installed; each layer's evidence gate passes; register signed.
- **Check:** DAG gate ruleset dry-run on sample historical shipments passes the 6 core rules.
- **Depends on:** T2.

### T4 — Deliverable template v1 (SWU-4)

- **Do:** Build the vertical-agnostic client-sendable package (overview / executive brief / reference
  appendix / client-decisions), BI-led ordering; instantiate for logistics.
- **Write scope:** `projects/ontologize/deliverable/` (template), `pilots/logistics/package/`.
- **Acceptance:** honesty gate (G-honesty) — every capability claim tagged proven/hypothesis; BI section first.
- **Check:** a reviewer with no project context understands the offer from the package alone.
- **Depends on:** T3.

### T5 — Proof harness + optimization chain, logistics (SWU-5)

- **Do:** Pick one evidence-linked metric (D-defer-1), define its evidence chain + denominator +
  baseline, measure movement per [PLAN IDS-3](PLAN.md), and express the result as an optimization
  chain per [OPTIMIZATION-CHAIN-METHOD.md](OPTIMIZATION-CHAIN-METHOD.md).
- **Write scope:** `projects/ontologize/pilots/logistics/proof.md` plus one optimization-chain fixture.
- **Acceptance:** metric traces to source events; baseline + post value + interpretation limits recorded;
  optimization-chain fixture validates against schema.
- **Check:** an independent reviewer reproduces the number from the evidence chain and validates the
  optimization-chain fixture.
- **Depends on:** T4. **Promotes L1→L2 on pass.**

### T6 — Cap factory parallel run (SWU-6)

- **Do:** Repeat T2–T5 for the cap factory; resolve the run-boundary (lot vs order) in assessment;
  instantiate method + package + proof.
- **Write scope:** `projects/ontologize/pilots/cap-factory/`.
- **Acceptance:** run-boundary decided; one evidence-linked metric moved; package instantiated.
- **Check:** cap-factory proof reproducible like T5; template reused without structural change.
- **Depends on:** T5 (template + harness exist); may start assessment portion in parallel with T3–T5.

### T7 — Cross-vertical + gap hardening (SWU-7)

- **Do:** Write the generalization report comparing both verticals' independent results (G-proof);
  close the five inherited GoldenQuill gaps (meta-metrics, buyer readiness, consequence/cost per
  decision, current→target transition, failure modes); generalize the template.
- **Write scope:** `projects/ontologize/GENERALIZATION.md`, `projects/ontologize/deliverable/`.
- **Acceptance:** explicit verdict on R1; five gap sections present; template reusable for a 3rd vertical.
- **Check:** generalization claim rests on two independent metric movements, not one.
- **Depends on:** T6.

### T-LB — Build Lane-B bridges (conditional, when Lane B/Hybrid chosen)

- **Do:** Build the five Lane-B bridges per [LANE-B-DESIGN.md](LANE-B-DESIGN.md) in critical-path order
  (2 dispatch → 3 lint → 1 signed register [advisory in pilot-1] → 5 cadence → 4 metric-drift). EXTEND
  bridges = configure existing sigils + a custom `promotion-record` entry type; NET-NEW bridges
  (1, 4) = separate `sigil-development` route.
- **Write scope:** `pilots/<vertical>/lane-b/` + any new sigil packages via sigil-development (not here).
- **Acceptance:** Bridge 2 + 3 working on the pilot's real events (dispatch routes; the 11 rules block
  violations); Bridge 1 at least advisory; Bridges 4/5 scoped or stubbed.
- **Check:** an OutcomeEvent routes to a card and a rule-violating PromotionCandidate is blocked.
- **Depends on:** T2b (lane = B or Hybrid) + T3 (method install). Owner: sigil-development / task-session.

## Guardrails (all tasks)

- No pricing, contracts, signed-client commitments, or canonical/brand promotion.
- No autonomous agent run on client data without the signed classification register.
- GoldenQuill stays read-only.
