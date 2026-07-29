# Distill Validation

Budget: `Standard` (assumed because the user did not select another budget).

## Proposer pass

The accepted review can be implemented as three independently verifiable
behaviors:

1. separate learner and reviewer surfaces;
2. repair the exact journey stimulus;
3. validate exact rendered behavior in a browser and emit a receipt.

## Balancer pass

- Combining learner generation with journey repair would create two acceptance
  boundaries and make contamination failures harder to localize.
- Splitting authority tones from navigation semantics would force both SWUs to
  rewrite the same generator, tests, and generated HTML while neither is useful
  alone as a protocol stimulus.
- Browser validation must follow both source SWUs because its receipt binds
  final bytes.
- Human and blind-agent observations are not source implementation and are
  excluded from this mutation frontier.

## Decision

Keep three SWUs. Each has one primary behavior, a distinct validation surface,
an explicit write set, and one successor.

Verdict: `pass`.

