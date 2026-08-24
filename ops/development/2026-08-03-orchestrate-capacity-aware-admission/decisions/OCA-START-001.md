---
decisionId: OCA-START-001
status: selected
createdAt: 2026-08-03T21:34:14Z
resolvedAt: 2026-08-03T21:44:57Z
profile: pilot
---

# Decision: start improving Orchestrate

## Blocker question

Should the lifecycle owner authorize the L0/L1 safe-core stream to begin with
exactly `SWU-OCA-001`, while preserving per-SWU Task Session admission and
Invoke Refresh closeout?

## Structurally admissible options

### OCA-START-SAFE-CORE — Start now

- Benefit: begins the earliest reversible prevention seam and then repairs the
  no-agent failure branch.
- Cost/risk: governed multi-agent execution becomes strict; missing or unknown
  capacity evidence blocks rather than silently falling back.
- Choose when: the priority is to improve safety now without inventing host
  reservation/release authority.
- Downstream: authorize only the OCA-001 material handoff and Task Session
  preflight. Later SWUs still require predecessor and closeout receipts.
- Recommendation: yes.

### OCA-DEFER-SAFE-CORE — Defer

- Benefit: no public runtime mutation or compatibility risk now.
- Cost/risk: predictable capacity pressure can still be discovered only after
  a wave begins spawning.
- Choose when: another repository objective currently outranks this repair.
- Downstream: package remains authored; `mutation_authorized` stays false.

### OCA-STOP-WORK — Stop

- Benefit: closes the initiative without deleting evidence.
- Cost/risk: the identified Orchestrate gap remains unresolved and the package
  receives no execution owner.
- Choose when: this direction is no longer wanted.
- Downstream: record a stop decision; no Task Session handoff.

## Structurally rejected option

`OCA-IMPLEMENT-FULL-ARCHITECTURE-NOW` is not presented as a choice. L2 lacks a
host-owned lease/release contract, L3 lacks an executable adoption work pack,
and the active lifecycle permits one receipt-gated SWU at a time.

## Decision evidence

- Request: `OCA-START-001-admissibility-request.json`
- Receipt: `OCA-START-001-admissibility-receipt.json`
- Selection: `OCA-START-SAFE-CORE`
- Selection source: explicit user confirmation, `Start safe core through the L2 boundary.`
- Authorized destination: execute the ordered L0/L1 safe-core stream and its
  L2-boundary verification, with each SWU independently admitted and closed.
- Excluded claim: true L2 host reservation/release remains deferred to its
  separately admitted native-host contract and canary.
- Explain/more context remains available and does not resolve the decision.
