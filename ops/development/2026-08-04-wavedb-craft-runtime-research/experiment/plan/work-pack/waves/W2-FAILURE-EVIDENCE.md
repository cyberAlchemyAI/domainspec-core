# W2: Failure and recovery evidence

- Units: `SWU-WCP-005`, `SWU-WCP-006`, `SWU-WCP-007` in that order.
- Entry: exact normal path passes.
- Exit: iterator streams are non-hybrid, every negative trigger is non-vacuous
  and fail-closed, and quarantine/sibling rebuild is exact.
- Stop: missing barrier, hybrid stream, non-zero failure output, unexpected
  target, YAML change, suspect-prefix trust, in-place repair, or inflated
  power/multiwriter claim.
