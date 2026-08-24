# Design Distill Validation

- Target context: candidate-local QRY-003/QueryReceipt readiness
- Mode: Standard, two recursive rounds, labeled Proposer/Balancer role simulation
- Objective: identify the smallest design unit that removes the current contract defect and can recompose into the knowledge-vault route
- Proposer round 1: one unit containing schema, policy, migration, validator, fixtures, and runner
- Balancer objection (`independent-acceptance`): policy, schema, migration, semantic validation, and replay each have distinct reviewable outcomes.
- Reconciliation: split declarative closure from executable replay.
- Proposer round 2: keep policy, schema, and migration together as one declarative unit.
- Balancer objection (`task-shape`): each of those three artifacts can pass or fail independently, while the validator and replay also have separate behavior boundaries.
- Reconciliation: five units—QRY-001 policy, QRY-002 schema, QRY-003 migration, QRY-004 validator, QRY-005 replay.
- Smallest coherent unit: QRY-001 terminal policy closure
- Recomposition: the five receipts form one ordered contract/replay chain; QRY-005 becomes a prerequisite, not authority, for later relation repair
- Premortem: most likely failure is a plan that passes prose review while missing live material admission; guard with Work Pack Readiness Audit and keep runtime status separate
- Frame expiry: any change to vocabulary, precedence, terminal paths, or receipt migration invalidates this optimization point
- Verdict: pass
- Task-shaped SWUs: 0 of 5
- Next route: Invoke Plan
