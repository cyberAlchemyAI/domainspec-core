# Lane B — detailed design (buildable)

Makes [DELIVERY-LANES.md](DELIVERY-LANES.md) Lane B buildable: the four-layer mapping against real
Arcanum sigil capabilities, the five bridges designed (verdict + MVP + gap + owner), and a build order.
Produced by refine run [`ontologize-lane-b-design-20260608`](development/refinement-runs/ontologize-lane-b-design-20260608/)
with one capability-surveyor subagent.

Tags: **[SB]** cited skill path · **[H]** hypothesis. Candidate design only — building any bridge or
installing a sigil is a separate `sigil-development`/`task-session` route. Arcanum skills read-only.

## Headline

Lane B is **mostly assemble + configure Arcanum, plus two real builds** — not five from scratch.
Of the five bridges: **3 EXTEND** existing sigils (config + a custom entry type), **2 are NET-NEW**.

## Four-layer mapping (what Arcanum gives nearly free) [SB]

| Layer                         | Arcanum realization                                                                                                                                                                                                                                           | Status          |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| L-ont ontology cards          | `ontology-vault` `map --branch business` (roles/axes/edge-rules) + `inventory` entity/concept entries                                                                                                                                                         | reuse           |
| L-reg classification register | — (see **Bridge 1**)                                                                                                                                                                                                                                          | **net-new**     |
| L-dag promotion DAG           | `inventory` evidence-cards/EvidenceSets (state, `source_refs`, `promotion_owner`) + `ontology-vault` `distill-sessions` (candidates) + `promote-confidence` (owner decision, falsification, blocks premature promotion) + `inventory lint` (see **Bridge 3**) | reuse + extend  |
| L-bi BI + agents              | `inventory` `lookup`/`query` + `context-builder` obligation-covered handoff packs feed agents; metric drift = **Bridge 4**; observability spine = observability-setup + observed-invocation-loop                                                              | reuse + net-new |

## The five bridges

### Bridge 1 — Signed classification register · **NET-NEW** · owner: sigil-development

- **Why:** Arcanum has no native signed/enforced field→authority register (inventory can _store_ classes
  as evidence-cards, ontology-vault _maps_ roles — neither signs nor gates before agents run). [SB]
- **MVP:** a sigil holding a `field → authority_class` schema + per-entry signature + a pre-agent
  fail-closed validation check + observability signals.
- **Gap:** crypto/key-management + tie-in to the client's credential store; key rotation/escrow out of scope.

### Bridge 2 — Event→ontology-card dispatch · **EXTEND** · owner: sigil-development

- **Reuse:** `inventory lookup` (match event→card by tags) + `context-builder` (assemble card + evidence)
  - `observed-invocation-loop` (wrap, emit telemetry, route follow-up). [SB]
- **MVP:** accept a source-validated OutcomeEvent → inventory lookup by event/source tags → context-builder
  assembles the matched card + evidence chain → OIL telemetry.
- **Gap:** no native card index _by event type_ — needs a governed event-type→card map; medium-confidence
  matches need human confirmation.

### Bridge 3 — 11-rule lint schema · **EXTEND** · owner: sigil-development

- **Reuse:** `inventory lint` + a custom `promotion-record` entry type (required fields = the DAG node fields). [SB]
- **MVP:** read promotion-records, run the 11 GoldenQuill rules (GQ-PR-L0-001..011) as hard assertions,
  block on violation, emit structured lint output.
- **Gap:** inventory lint won't enforce _semantic_ rules (e.g., "denominator excludes cancellations");
  rule instantiation is per-vertical.

### Bridge 4 — Proof-harness for metric drift · **NET-NEW** · owner: sigil-development

- **Why:** observability tracks _sigil invocations_, not metric time-series; workflow-reflect groups
  signals, not metrics. [SB]
- **MVP:** ingest MetricObservation (N3); store numerator/denominator/period/source immutably; compute
  trend; flag denominator drift vs metric drift; route anomalies to workflow-reflect.
- **Gap:** storage choice (jsonl/sqlite/tsdb); alerting (candidate-triggering) is separate.

### Bridge 5 — Reflection cadence · **EXTEND** · owner: sigil-development

- **Reuse:** `workflow-reflect` + `ontology-vault distill-sessions` + `decision-gate` + an external
  scheduler (`schedule`/cron). [SB]
- **MVP:** pull aged/mature PromotionCandidates → distill-sessions packet → decision-gate owner approval
  → `promote-confidence` projection → batch summary.
- **Gap:** no native scheduler; cadence thresholds are a lane-design choice. [H]

## Build order

```text
Bridge 2 (dispatch) ─▶ Bridge 3 (lint) ─▶ [Bridge 1 signed register — advisory in pilot-1] ─▶ Bridge 5 (cadence) ─▶ Bridge 4 (metric drift)
```

- **2 first** — dispatch unblocks the whole DAG (every downstream node depends on event→card routing).
- **3 next** — lint makes the DAG safe before agents act.
- **1 descope-able** — hardest (crypto); start with advisory routing, add signing when agent volume justifies it.
- **5 then 4** — cadence coordinates owner decisions; metric-drift is observability, not a gate.

## Free-vs-build summary (the honest offer)

A client on Lane B gets the reuse layers + 3 EXTEND bridges by **configuring Arcanum**, and pays for
**2 NET-NEW builds** (signed register, metric-drift harness). Scope and price those two explicitly;
don't imply the harness covers them.

## Residue

- Per-vertical rule/metric instantiation (Bridge 3/4) — assessment + pilot. [H]
- Scheduler choice + cadence thresholds (Bridge 5) — pilot tuning. [H]
- Key-management for Bridge 1 depends on the client's credential infrastructure. [H]
- Building/installing any bridge is a separate `sigil-development` route, not this design.
