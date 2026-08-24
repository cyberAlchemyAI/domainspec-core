---
node_type: research
is_session: false
status: handoff-ready
created: 2026-08-07
updated: 2026-08-07
promotion_boundary: no experiment executed
---

# Evidence Handoff

## Next governed route

Use `research-evidence-harness` to turn this lane into a validated run package. This handoff does not authorize participant recruitment, external messaging, or execution.

## Falsifiable question

Compared with evidence-equivalent prose, does the multi-form cognitive navigation instrument improve a participant's ability to traverse a richer representation and return to the concrete case while preserving claim, interpretation, and authority boundaries?

## Arms

- **Baseline:** one prose representation containing the same evidence.
- **Treatment:** horizontal expression set with explicit claim label, limits, governance, approval boundary, and a gated residue-escalation aid.
- **Agent arm:** optional structural pretest for task ambiguity and instrument leakage; cannot support human-cognition claims.
- **Human arm:** required for any human-comprehension result.

## Fixed task family

1. Restate the bounded claim in plain language.
2. Select a representation for a named audience and explain why.
3. Translate a contract or formal view to plain language and back.
4. Identify the claim ceiling and approval boundary.
5. Detect causal or mechanism overclaim.
6. Return from a richer distinction to reconstruct the original case.
7. Transfer the distinction to an unfamiliar case.
8. Classify each answer element as demonstrated, inferred, proposed, or untested.

Baseline and treatment tasks should be byte-identical wherever the arm distinction permits.

## Candidate metrics

| Metric | Observable |
|---|---|
| Semantic preservation | Required distinctions retained across translations |
| Claim-ceiling accuracy | Unsupported enlargement count |
| Authority accuracy | Approval/ownership boundary retained |
| Return fidelity | Concrete case reconstructed after abstraction |
| Transfer accuracy | Correct application to unfamiliar case |
| Causal-overclaim detection | Unsupported causal/mechanism claims rejected |
| Stall profile | Count, type, location, and recovery of stalls |
| Confidence calibration | Confidence tracks evidential sufficiency |
| Completion time | Optional secondary measure, never correctness substitute |

## Required residue classes

- missing vocabulary;
- ambiguous or overloaded term;
- edge or state-model confusion;
- claim-ceiling loss;
- authority-boundary loss;
- causal overreach;
- failed descent to the concrete case;
- transfer failure;
- instrument contamination;
- unclassified residue.

## Pre-registration requirements

- Primary metric and minimum effect direction.
- Survival, falsification, and invalidation criteria.
- Treatment and baseline digests.
- Blindness and contamination fields.
- Rule deciding local representation repair versus vertical climb.
- Separation of agent and human result claims.
- Versioned scoring rubric and adjudication process.

## Result language

- Before execution: “We define a falsifiable protocol.”
- Agent-only success: “The instrument passed a structural pretest under the recorded conditions.”
- Human result: report only the preregistered observed effect and limits.
- Failure: preserve the failed hypothesis and route typed residue; do not redescribe it as confirmation.

## Required outputs from the next route

- run schema;
- JSONL fixture set;
- baseline/treatment artifact manifests and digests;
- metric validator;
- result schema;
- contamination and blindness fields;
- claim-to-result language table;
- audit report.

