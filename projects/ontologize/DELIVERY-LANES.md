# Delivery Lanes — how the method gets installed

Two delivery lanes for the four-layer ontology+DAG+BI method, plus the hybrid between them. Produced
by the refine run [`ontologize-delivery-lanes-20260608`](development/refinement-runs/ontologize-delivery-lanes-20260608/)
with two role-bound lane-designer subagents.

Tags: **[SB]** source-backed (ontologize design or a cited Arcanum skill path), **[RP]** reusable
pattern, **[H]** hypothesis/bridge. Candidate design only — no canonical promotion, no pricing/clients.
GoldenQuill and the Arcanum skill definitions are read-only evidence.

The four layers (recap): **L-ont** ontology cards · **L-reg** classification register · **L-dag**
promotion DAG (6 node types + 11 rules, see [DAG-AND-METRICS.md](DAG-AND-METRICS.md)) · **L-bi**
evidence-linked BI + governed agents.

---

## Lane A — "tools they already have"

Install the four layers on the client's existing stack (ERP/TMS/order system, spreadsheets, BI tool,
email). **No new platform.** Boundary: governance is convention-based; gates are advisory, not
runtime-enforced.

| Layer | Realized on existing tools [SB]                                                                                                                                                                                          |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| L-ont | governed spreadsheet: subject tab × mechanism tab + a "matching rules" tab (runtime reference, not a baked binding)                                                                                                      |
| L-reg | access-controlled, signed register sheet (`field → authority class`, manual hash, fail-closed default = restricted)                                                                                                      |
| L-dag | append-only tables for the 6 node types (OutcomeEvent / LifecycleState / MetricObservation / PromotionCandidate / OwnerDecision / KnowledgeProjection); the 11 rules as data-validation + formula checks + manual review |
| L-bi  | BI dashboard measures with documented denominators + an evidence-linked receipt sheet; agent routing as documented (advisory) rules                                                                                      |

- **Strengths [RP]:** high sovereignty (data never leaves), low adoption lift, modular install, fast
  proof (~12 wk/vertical [H]).
- **Hard limits [SB/H]:** deterministic gates are advisory not fail-closed; evidence composition is
  manual; spreadsheet ceiling ~10k events/mo [H]; weekly/monthly promotion cadence; agent rules
  documented but unenforced.

## Lane B — "Arcanum inventory + ontology"

Install the four layers on Arcanum's own sigils as the governed substrate.

| Layer | Realized on Arcanum [SB skill paths]                                                                                                                                                                                                                                           | Status            |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------- |
| L-ont | `ontology-vault` `map --branch business` roles/axes/edge-rules + `inventory` entity/concept entries                                                                                                                                                                            | [SB]              |
| L-reg | **no native sigil** — descriptive "source authority rules" only; needs a custom `classification-record` entry type + lint bridge                                                                                                                                               | **[H] hard gap**  |
| L-dag | `inventory` evidence-cards/EvidenceSets (state, `source_refs`, `promotion_owner`) + `ontology-vault` `distill-sessions` (candidates) + `promote-confidence` (owner decision, falsification, blocks premature promotion) + `inventory lint` (the 11 rules as custom checks [H]) | [SB] with bridges |
| L-bi  | `inventory lookup`/`query` + `context-builder` obligation-covered handoff packs feed agents; **no native dashboard UI**, **no proof-harness for metric drift over time**                                                                                                       | [SB] with gaps    |

- **What Arcanum adds [SB]:** governed promotion with deterministic lint, audit-immutable source spine,
  evidence-linked context for agents, branch-aware business↔system drift detection, baked-in
  inventory→ontology-vault→context-builder pipeline.
- **Hard limits [SB/H]:** adoption curve; text-first (no native BI dashboard); the Layer-2 register
  gap; no time-series/proof-harness; no native reflection cadence (use the `schedule` skill or external
  cron to batch `distill-sessions`).
- **Bridges Lane B requires [H]:** (1) signed classification register; (2) runtime event→ontology-card
  dispatch; (3) the 11-rule lint schema; (4) a proof-harness for metric drift; (5) a reflection cadence.
  **Each is now designed (reuse/extend/net-new + MVP + build order) in
  [LANE-B-DESIGN.md](LANE-B-DESIGN.md) — 3 EXTEND existing sigils, 2 are NET-NEW builds.**

---

## Selection rule (decidable from observable client facts)

- **Choose Lane A** when: data must stay in existing systems · SMB scale (<~10k events/mo) · a fast
  proof-of-concept is the goal · manual governance is acceptable · agents are deferred · the client
  demands a visual dashboard.
- **Choose Lane B** when: auditable governance _is_ the value · the client is agent-first · intent↔
  implementation drift matters · the client will adopt harness discipline · text-first reporting is fine.
- **Choose the Hybrid** (the common best answer, [RP] recomposition proof) when both pull: keep
  operational data + BI on the client's tools (Lane A surface) and run the **governed knowledge /
  promotion layer** (L-dag promotion + L-ont + evidence linting) on Arcanum (Lane B core). Pure-A and
  pure-B are the endpoints; most clients land in the middle.

```text
data must stay put + SMB + fast PoC + dashboard demanded ........ Lane A
governance/audit is the point + agent-first + adopts harness .... Lane B
both pull (data/BI local, governance on Arcanum) ................ Hybrid  ← usual
```

## Per-vertical candidate (confirm in assessment, [H])

- **Cap factory** — ERP-centric, continuous, wants dashboards → **Lane A** surface, optional Lane-B
  governance overlay for the promotion DAG.
- **Logistics** — clean discrete shipment runs + carrier-rule learning + likely routing agents →
  **Hybrid** leans valuable: Lane A TMS/BI surface + Lane B governed carrier-rule promotion.

## Residue

- Lane B's five bridges [H] are real build items, not assumed-present — scope them before promising Lane B.
- The actual lane per client is an assessment decision (adds a step to PLAN/WORK-PACK).
- Spreadsheet→DB substrate switch for Lane A at >10k events/mo [H].
