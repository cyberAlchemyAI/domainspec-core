# SWU-DVC-006E Staged Delta

- Target:
  `arcanum/spells/invoke/development/run-validation-fixtures.sh`
- Required preimage SHA-256:
  `aa09a0efd524d8252473e42e922958e14f5b4a8e8238b4c412f8579e3b305303`
- Preserve every existing byte except the anchored additions and obsolete
  Design status expectation below.

## Required behavior

1. Bind the executable Design-selection child runner and its deterministic
   latest-summary report.
2. Fail aggregate validation when the runner is missing, not executable,
   returns nonzero, or succeeds without producing its report.
3. Preserve every child output line in the aggregate event stream.
4. Surface both the runner and child report paths in aggregate output
   artifacts and print the child report path explicitly.
5. Require the new Design evidence fields from the root contract.
6. Replace the obsolete Design status expectation with
   `implemented (L1 contract with deterministic selection validation)`.

No other aggregate-runner behavior may change.
