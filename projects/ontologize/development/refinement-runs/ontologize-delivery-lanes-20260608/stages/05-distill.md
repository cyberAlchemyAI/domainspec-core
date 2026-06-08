# Stage 5 — Distill (tournament between the two lanes)

**Verdict: pass.** Research decision: no-research. Inputs: the two lane-designer receipts (ledger
`lane-designer-receipts`) + ontologize design + Arcanum skill definitions.

## Tournament (roles: existing-tools-lane-designer vs arcanum-substrate-lane-designer)

Compared across the convergence criteria. Pareto view (cost/lift vs governance strength vs sovereignty):

| Dimension           | Lane A (existing tools)           | Lane B (Arcanum substrate)             |
| ------------------- | --------------------------------- | -------------------------------------- |
| Adoption lift       | low                               | high (adopt harness)                   |
| Time to first proof | ~12 wk                            | ~16–20 wk                              |
| Governance strength | manual/convention, advisory gates | deterministic lint, governed promotion |
| BI surface          | native (their dashboard)          | text-first; needs UI bridge            |
| Sovereignty         | high (data stays put)             | high (own Arcanum instance)            |
| Layer-2 register    | spreadsheet, signed manually      | **native gap — needs bridge**          |
| Agent governance    | documented, not enforced          | evidence-linked handoffs, enforced     |

## Convergence — the selection rule (decidable)

- **Lane A wins** when: data must stay in existing systems, SMB scale (<~10k events/mo), fast PoC needed,
  manual governance acceptable, agents deferred, a dashboard is demanded.
- **Lane B wins** when: governance/auditability _is_ the value, agent-first ops, intent↔implementation
  drift matters, the client will adopt harness discipline, text-first reporting acceptable.
- **Recomposition proof (the real answer to G-a):** the lanes are **not strictly exclusive**. The dominant
  option for many clients is a **hybrid**: operational data + BI stay on the client's tools (Lane A
  strength), while the _governed knowledge/promotion layer_ (DAG promotion + ontology + evidence linting)
  runs on Arcanum (Lane B strength). Pure-A and pure-B are the endpoints; hybrid is the middle.

## Honest gate (source-or-hypothesis)

Lane B's governance layers are [SB] to real sigil capabilities, but Layer-2 (classification register),
runtime event→card dispatch, the 11-rule lint instantiation, the proof-harness, and reflection cadence
are **[H] bridges Arcanum does not natively provide** — surfaced, not hidden.

Output unit → [DELIVERY-LANES.md](../../../DELIVERY-LANES.md).
