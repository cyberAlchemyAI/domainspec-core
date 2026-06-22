# Distill: Smallest Coherent Unit

Status: pass
Owner: `distill` via parent Refine coordinator
Mode: `standard`

## Candidate Units

| Candidate | Decision | Reason |
| --- | --- | --- |
| Full poker-agent arena | Reject | Too broad; would mix protocol, runtime, Hold'em, scoring, and novelty. |
| Hold'em engine parity | Reject for now | Depends on L0 protocol and replay contracts. |
| Adjusted leaderboard scoring | Reject for now | Depends on reference bots and adversarial calibration fixtures. |
| Novelty mechanics | Reject for now | Time-bank and bandwidth mechanics are appendix material. |
| L0 protocol/schema/fixture repair packet | Select | Smallest unit that repairs the flagged gaps and enables `SWU-PAA-001`. |

## Selected Unit

`L0 contract repair packet`

This unit does not implement the arena. It sharpens the root docs and/or creates a docs-only L0 packet so `task-session` can execute `SWU-PAA-001` without inventing component boundaries or fixture semantics mid-run.

## Recomposition Target

After this repair, the project can recompose into:

1. `SWU-PAA-001`: freeze CLI contract and fixture skeleton.
2. `SWU-PAA-002` and `SWU-PAA-003`: Kuhn and Leduc fixtures.
3. `SWU-PAA-004`: replay and raw scoring diagnostics.
4. Later M1/M2 gates.

## Rejected Route Residue

- Engine parity still needs a later engine-choice decision.
- Adjusted scoring still needs adversarial calibration.
- Prior lane receipts remain historical evidence and may need an execution/provenance manifest to avoid drift.
