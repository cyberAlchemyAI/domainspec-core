# MARS Protocol Validation Checklist

This checklist is used by `mars-research-protocol-designer` before any experiment execution.

## Criteria

| Check | Pass/Fail | Notes |
|---|---|---|
| Objective and claim mapping defined |  |  |
| Hypothesis or success criteria are measurable |  |  |
| Required data schema fields are defined |  |  |
| Metadata fields are complete (`experiment_id`, `run_id`, `timestamp`, `model`, `operator`) |  |  |
| Dependency requirements are declared |  |  |
| Source requirements are explicit |  |  |
| Inventory entry-type requirements are explicit |  |  |
| Expected row volume or sampling plan is explicit |  |  |
| Analysis path (foundation or full) is declared |  |  |
| Claim-to-paper traceability section is present |  |  |

## Decision

- PASS: all required checks pass.
- NEEDS-REVISION: non-critical checks fail.
- BLOCKED: measurable criteria or schema/dependency requirements are missing.
