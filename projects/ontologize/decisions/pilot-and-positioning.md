# Decision Record — ontologize pilot & positioning

- Scope: CyberAlchemy first product (project `ontologize`)
- Date: 2026-06-08
- Source of decision: user (operator), via `decision-gate`
- Gate result: PASS

Resolves open residue [R1, R2, R3, R8](../residue/open-residue.md) and the open product
decisions in [L2-product-closure-plan.md](../levels/L2-product-closure-plan.md).

---

## Decision 1 — First pilot client

**Question:** Which client should be the first ontology+DAG pilot?

**Options considered:**

- **Logistics company** — discrete shipment runs with measurable outcomes; cleanest match to the
  promotion DAG + evidence-linked BI; strongest single proof. Cost: higher data/system complexity.
- **Cap factory** — bounded manufacturing scope; simpler, faster, lower-risk proof. Cost: continuous
  production makes the run→outcome→learning loop less crisp.
- **Both in parallel** — two proofs across very different verticals; strongest generalization claim.
  Cost: doubles effort, dilutes focus.

**Selected: Both in parallel (cap factory + logistics company).**

**Rationale:** The product's central unproven claim is cross-vertical generalization (R1). Proving
it in two structurally different verticals at once — discrete-run (logistics) and continuous-production
(cap factory) — is the most convincing evidence that the ontology+DAG pattern is general, not a
grant-only artifact. The operator already has access to both clients, lowering the usual cost barrier
of a two-vertical pilot.

**Downstream impact:** Engagement runs two parallel assessment→design→pilot tracks. The deliverable
template must be vertical-agnostic with per-vertical instantiations. Proof is measured independently
per vertical, then compared to demonstrate generalization.

## Decision 2 — Offer positioning / lead value

**Question:** Which value should the consulting offer lead with?

**Options considered:**

- **Combined, BI as the lever** — lead with traceable evidence-linked BI, governed agents as the
  deeper hook. Balanced; slightly larger scope.
- **BI-led only** — fastest demonstrable value; less differentiated from ordinary analytics consulting.
- **Agent-governance-led** — strongest for agent-mature clients; slow to prove for others.

**Selected: Combined, BI as the lever.**

**Rationale:** Evidence-linked BI is the fastest, most measurable value on data both clients already
have, so it opens the engagement and de-risks the sale. Governed agents (ontology-driven routing +
deterministic gates + the promotion learning loop) are the durable differentiator and the reason the
BI stays trustworthy over time — so they anchor the offer without gating first value.

**Downstream impact:** The deliverable leads with the KPI/evidence layer; ontology cards, classification
register, promotion DAG, and agent governance are positioned as what makes the BI trustworthy and
self-improving.

---

## Deferred decisions (revisit during assessment, not blocking)

- **D-defer-1 — Proof metric per vertical.** Candidate (to confirm with each client's data):
  logistics = on-time-delivery or cost-per-lane traced to its evidence chain; cap factory =
  defect/rework rate or on-time order fulfillment traced to its evidence chain. Owner: design.
- **D-defer-2 — Target buyer per client.** Working assumption: an ops/data lead with an executive
  sponsor at each client; confirm during assessment. Owner: product. (R3)
- **D-defer-3 — Sequencing within "parallel."** Truly simultaneous vs lightly staggered starts;
  resolve once assessment scheduling with both clients is known. Owner: product.

## Assumptions recorded (proceed if labeled)

- **A1 — Candidate ontology axes** (to validate in assessment, not asserted as final):
  - Logistics: subject = clients/lanes × service type; mechanism = shipment/contract types.
  - Cap factory: subject = product lines/SKUs × customer or sales channel; mechanism = order/channel types.
- **A2 — No pricing, contracts, or named-client commitments** are made by this decision; client names
  here ("cap factory", "logistics company") are pilot references, not signed engagements.

## Remaining blockers

None. Both blocker-level decisions are resolved.
