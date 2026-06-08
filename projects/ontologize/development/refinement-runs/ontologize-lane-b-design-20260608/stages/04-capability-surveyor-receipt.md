# Capability-surveyor receipt (ledger: capability-surveyor-receipt)

One approved subagent (arcanum-capability-surveyor), join parent_synthesis. Completed and closed.

## Per-bridge verdicts (reuse / extend / net-new)

| Bridge                            | Verdict     | Best Arcanum candidate                                                                                                | MVP                                                                                                                                                                           | Residual gap                                                                                                                   |
| --------------------------------- | ----------- | --------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| 1. Signed classification register | **NET-NEW** | none (inventory can store/lint classes as evidence-cards; ontology-vault maps roles — neither signs/enforces)         | custom sigil: field→authority schema + per-entry signature + pre-agent fail-closed validation + observability                                                                 | crypto/key-mgmt + client credential store; key rotation/escrow out of scope                                                    |
| 2. Event→ontology-card dispatch   | **EXTEND**  | `inventory lookup` + `context-builder` + `observed-invocation-loop`                                                   | dispatch sigil: accept OutcomeEvent (source-validated) → inventory lookup by event/source tags → context-builder assembles matched card + evidence → OIL telemetry            | no native card index by event type; event-type→card map needs its own governance; medium-confidence matches need human confirm |
| 3. 11-rule lint schema            | **EXTEND**  | `inventory lint` + custom `promotion-record` entry type                                                               | lint sigil: read promotion-records, run the 11 rules as hard assertions, block on violation, structured output                                                                | inventory lint won't enforce semantic rules (e.g., denominator excludes cancellations); rule instantiation is per-vertical     |
| 4. Proof-harness (metric drift)   | **NET-NEW** | none (observability tracks _sigil invocations_, not metric time-series; workflow-reflect groups signals, not metrics) | harness sigil: ingest MetricObservation (N3), store numerator/denominator/period/source immutably, compute trend, flag denominator drift, route anomalies to workflow-reflect | no native metric/time-series store; storage choice (jsonl/sqlite/tsdb); alerting is candidate-triggering, separate             |
| 5. Reflection cadence             | **EXTEND**  | `workflow-reflect` + `ontology-vault distill-sessions` + `decision-gate` + external scheduler                         | cadence sigil: pull aged/mature PromotionCandidates → distill-sessions packet → decision-gate owner approval → promote-confidence projection → batch summary                  | no native scheduler (external cron/`schedule`); cadence thresholds are a lane-design choice                                    |

## Build order (surveyor)

Critical path **2 → 3 → (1 optional in pilot) → 5 → 4**. Bridge 2 (dispatch) unblocks the whole DAG;
Bridge 3 (lint) makes it safe; Bridge 1 (signed register) is hardest (crypto) and can be descoped to
advisory routing in pilot-1; Bridge 5 coordinates owner decisions; Bridge 4 is observability, not a gate.

## Tags

All verdicts SOURCE-BACKED to skill paths (inventory/ontology-vault/context-builder/observed-invocation-loop/
workflow-reflect/decision-gate SKILL.md) + DELIVERY-LANES.md / DAG-AND-METRICS.md. MVP cost/cadence values are HYPOTHESIS.
