# TASK-ACAPI-06: Optional Extension Or Packaging

- Layer/slice: L3 / S-005.
- Dependencies: L2 pass plus B-005 owner decision.
- Status: deferred.

## SWU-ACAPI-012: One Selected Extension

- Primary behavior: implement exactly one selected extension: a typed
  `traverse`, `compare`, or stored `explain` result, or an HTTP JSON transport
  wrapper.
- Acceptance: unchanged application-service schemas and statuses; selected
  extension has compatibility and security fixtures.
- Split analysis: alternatives are mutually exclusive selections. Implementing
  more than one makes the SWU task-shaped and blocks it.
- Write scope: selected owner names exact paths only after the decision.
- Validation: selected operation contract tests or HTTP compatibility/security
  tests plus all earlier suites.
- Evidence: result 012.
- Owner: subagent under selected operation or transport owner.
- Handoff: no deployment or release is included.

