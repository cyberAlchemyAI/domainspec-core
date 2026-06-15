---
tags: [goldenquill, promotion-governance, dec-oq4, decision-vocabulary, assessment]
node_type: discovery
is_session: true
layer: domain, governance
nature: explanatory, analytical
status: active
created: 2026-06-13
timestamp: 2026-06-13T22:56:41-03:00
expires: 2026-08-12
conversation_id: 2026-06-13-dec-oq4-grant-approval-analysis
decisions_made: false
contradictions_found: false
specs_updated: []
promoted_candidates: []
expected_importance: 5
importance_rationale: "Surfaces a genuine undecided gap (operator_signoff learning-signal status) and trims the DEC-OQ4 change set for whoever closes it, but no canonical artifact changed."
---

# DEC-OQ4 — Grant-Approval Decision Surface Analysis

## Summary

Investigated GoldenQuill's blocking decision DEC-OQ4 (lock the operator-decision vocabulary so only `OwnerDecision` can promote knowledge for reuse). Probed whether the operator's grant-approval/`operator_signoff` ("deliver/revise/pause/stop") is a missing fourth decision surface. Two dispatch rounds (5 subagents) concluded it is a correctly-excluded operational gate already guarded by existing invariants (GRT-I3, ODS-I1/I2) — so DEC-OQ4 needs no fourth assertion; it only needs Josh to confirm "three typed surfaces, not one enum." One genuine blank spot remains: nobody has decided whether `operator_signoff` feeds the learning analytics — schema permits it, no doc models it.

## Next Steps

- Josh to answer DEC-OQ4: keep three typed surfaces (PursuitDecision / MatchFitVerdict / OwnerDecision), not one unified enum — unblocks L1 candidate shape + the promotion-enforcement gate.
- Park a new non-blocking open question in `projects/goldenquill/docs/features/goldenquill-promotion-governance/integration/OPEN-QUESTIONS-LEDGER.md`: should `operator_signoff` project into a GrantActionFact (learning signal)?
- On LOCK, delete seam-map cross-layer rows `confirmed_fit→approved` / `declined_cycle→retired` (category errors) per the existing OQ-4 resolution.

## Open Questions

- Does `operator_signoff` (deliver/revise/pause/stop) feed the learning loop, or stay a pure runtime gate? — analytics-methods.md GrantActionFact / ActionKpiAssociation.
- Three typed surfaces vs one unified enum — still operator-pending ("let me think"). — ledger.yml DEC-OQ4.

## Files touched

- subagents-dispatch.yaml
