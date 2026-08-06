# Decision Gate: Learner-View Mutation Admission

- Decision ID: `learning-projection-a001-owner-admission`
- Target: all ten SWUs in the learner-projection Work Pack
- Classification: blocker
- Hazard: protected authority boundary
- Status: option 2 selected; bounded request prepared; owner response pending
- Source: user requested selection/execution of the whole SWU package
- Admissibility receipt: `decision-admissibility-receipt.json`

## Why Execution Stopped

The series intent is valid and the ten-unit frontier is finite and ordered, but
W0 and A-001 require a current learner-view mutation-admission receipt before
SWU selection becomes active or any product file changes. The user selection
request and the owner admission are deliberately separate records.

## Admissible Options

### provide-current-owner-receipt — recommended when the receipt exists

Provide the current receipt issued by `learner-view-navigation-owner`. It must
bind the exact host/product scope, current baselines, candidate-only claim
ceiling, validation policy, and supersession/invalidation policy.

- Benefit: directly satisfies the missing W0 evidence when current and valid.
- Cost/risk: requires owner-issued typed evidence; a chat approval or draft is
  insufficient.
- Downstream impact: the chain can be re-preflighted and may activate only
  `SWU-LGP-001` as the first fresh Task Session.

### prepare-owner-admission-request

Prepare a bounded request for the learner-view/navigation owner.

- Benefit: creates the exact packet the owner needs to review.
- Cost/risk: does not satisfy A-001 or authorize implementation.
- Downstream impact: the chain stays blocked until the owner returns the typed
  receipt.

### defer-series

Leave the captured frontier unexecuted.

- Benefit: preserves all current product and authority state.
- Cost/risk: the learning projection remains a validated plan only.
- Downstream impact: a later invocation must rebind the live Work Pack and W0
  evidence.

## Rejected Bypasses

- `treat-chat-selection-as-admission`: rejected because free-form selection
  cannot satisfy a protected owner gate.
- `execute-swu-001-before-w0`: rejected because SWU-001 is not dependency-ready.

## Selection

- Selected option: `prepare-owner-admission-request`
- Selection source: user message `2`
- Prepared request:
  `.arcanum/task-session/chains/learning-projection-all-swus-20260801/owner-admission-request.json`
- Request SHA-256:
  `a3c464c6e63d468e77eaa20e56211ad050d53be3f189ad748890da0cb9f18b99`
- Required receipt path:
  `cyberAlchemy-v2/development/research/2026-08-01-learning-graph-next-route-guide/invoke/work-pack/owner-evidence/W0/mutation-admission.json`
- Receipt status: absent
- Authority interpretation: option 2 authorizes preparation of the bounded
  request only; it is not converted into the separately produced owner receipt.
- Remaining blocker: A-001 learner-view mutation admission pending owner response
- Explain / more context: available and non-committal
