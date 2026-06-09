# Open Residue

Unresolved items after the ontologize research run. Each has an owner and a next object.

## Product-level (CyberAlchemy)

- **R1 — Cross-vertical generalization unproven.** The whole offer assumes GoldenQuill's grant-vertical
  proof generalizes. Next object: a non-grant pilot. Owner: product.
- **R2 — Positioning undecided.** BI-led vs agent-governance-led vs combined. Recommendation: combined,
  BI as the lever. Owner: product. Next object: decision-gate.
- **R3 — Target buyer undecided.** Ops/data lead vs AI lead vs executive sponsor. Owner: product.
- **R4 — Inherited client-package gaps.** Meta-metrics on the governance layer, buyer-readiness
  scaffolding, consequence/cost per decision, current→target transition plan, failure-mode framing
  (from Lane 5). Owner: deliverable design. Next object: deliverable template v1.

## Source-evidence gaps (from GoldenQuill, read-only)

- **R5 — Promotion DAG is L0 / synthetic-fixtures only.** Owner-decision persistence and the
  "PromotionRecord home" (sibling vs projection) are unresolved upstream. Affects how confidently we
  claim the loop is production-ready. Owner: GoldenQuill (not ours to change).
- **R6 — Reflection Packet + card runtime graphing dormant** (v0.1 hooks). The "learning loop closes
  automatically" story is partly forward-compat. Tag as hypothesis in any client claim.
- **R7 — Sector enum vs CIC reconciliation open** upstream; minor for generalization but note it when
  citing the ontology as clean.

## Method gaps

- **R8 — No defined "proof" for a non-grant pilot.** What evidence-linked metric, on what client data,
  counts as success? Owner: product + design. Next object: pilot success criteria.
- **R9 — KPI denominator authority** (who defines numerator/denominator) is unresolved even in
  GoldenQuill; the BI layer must specify this per engagement.
- **R11 — N2→N3 gate coverage gap. [H]** [DAG-AND-METRICS §7](../DAG-AND-METRICS.md) flags that no L0
  rule currently guards the N2→N3 transition (LifecycleState → MetricObservation). Decide in assessment
  whether this transition needs an explicit gate or whether the stage≠outcome guard (GQ-PR-L0-003)
  suffices. Owner: design. Next object: assessment.

## Ontology reconciliation (from [RECONCILIATION.md](../RECONCILIATION.md))

- **R12 — B1 canonical name unresolved. [open]** "meaning" (ontologize) vs "business" (all prior art:
  `BUSINESS-ONTOLOGY.md`, `ontology-vault` `--branch business`, `ONTOLOGY-ARCHITECTURE.md`).
  Recommendation: adopt **business**, keep meaning/domain/intent as aliases. Owner: ontology owner.
  Next object: decision-gate. (R13 B3-rename and R14 4-first-class are RESOLVED 2026-06-08 — see
  RECONCILIATION.md §1.)
- **R15 — Authority-ladder reuse-as-template undecided. [open]** Whether to lift
  `cyberAlchemy/ontology/entries/knowledge-governance-authority-ladder.md` as the pilots' promotion-method
  template vs. designing fresh. (Existing entries as *content* stay separate — already decided.) Owner:
  design. Next object: assessment / WORK-PACK T1. [H]

## Promotion guardrail residue

- **R10 — Nothing here is promoted.** All terms/definitions/product framing are candidates. No
  pricing/contracts/clients. Canonical promotion needs a separate owner-review route.
