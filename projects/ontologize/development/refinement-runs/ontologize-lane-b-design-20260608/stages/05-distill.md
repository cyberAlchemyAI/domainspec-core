# Stage 5 — Distill (x-ray the bridge mechanics)

**Verdict: pass.** Research: no-research. Input: capability-surveyor receipt + skill defs + DELIVERY-LANES.md.

## Distilled unit

Lane B splits cleanly into **what Arcanum gives nearly free** and **what must be built**:

- **Free / reuse [SB]:** L-ont (ontology-vault `map --branch business` + inventory entities);
  L-dag core (inventory evidence-cards/EvidenceSets + ontology-vault `distill-sessions` +
  `promote-confidence`); L-bi context delivery (inventory `lookup`/`query` + context-builder
  obligation-covered handoffs); observability spine (observability-setup + observed-invocation-loop).
- **Extend (configure on a sigil) [SB]:** Bridge 2 dispatch (inventory lookup + context-builder + OIL),
  Bridge 3 lint (inventory lint + custom `promotion-record` type), Bridge 5 cadence (workflow-reflect +
  distill-sessions + decision-gate + external scheduler).
- **Net-new (build) [SB]:** Bridge 1 signed classification register (crypto/key-mgmt), Bridge 4
  metric-drift proof-harness (time-series store).

## Build order (critical path)

**2 → 3 → (1 optional in pilot-1) → 5 → 4.** Dispatch unblocks the DAG; lint makes it safe; the signed
register is hardest and can start advisory; cadence coordinates owner decisions; metric-drift is
observability, not a gate.

## Honest framing

Of the five bridges, **3 are EXTEND** (sit on existing sigils with config + a custom entry type) and
**2 are NET-NEW** (genuine builds). So Lane B is "mostly assemble + configure Arcanum, plus two real
builds," not "all five from scratch." [SB surveyor receipt]

Output unit → [LANE-B-DESIGN.md](../../../../LANE-B-DESIGN.md).
