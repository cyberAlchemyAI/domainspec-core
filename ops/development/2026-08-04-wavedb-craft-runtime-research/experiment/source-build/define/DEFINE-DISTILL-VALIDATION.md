# Define Distill validation

- Mode: `Standard` assumed from the complete Invoke-chain request.
- Target context: one remediation slice that produces a locally verified addon
  without repairing or reinterpreting npm provenance.
- Proposer claim: define a complete local source-build artifact contract.
- Balancer objection (`authority-boundary`): a source build could be mistaken
  for a corrected release or Craft runtime approval.
- Reconciliation: make the artifact platform-specific, candidate-local, and
  consumable only through a separate parent Invoke Refresh.
- Smallest coherent concept unit: `SourceBuildReceipt`, binding source,
  lockfile, toolchain, generated sources, addon, tests, and residue.
- Split pressure: dependency, compilation, and tests are acceptance stages, not
  independently meaningful artifacts for this target.
- Recomposition: the receipt closes the source-build slice and can be evaluated
  by the parent experiment without modifying the failed npm receipt.
- Evolution profile: a future platform matrix or distributable package would
  require new source-build attempts and a separate package/publication route.
- Premortem: likely failure is toolchain or node-gyp incompatibility; guardrail
  is fail-closed evidence with no fallback dependency or source substitution.
- Verdict: `pass` for Define authoring; no build readiness claim.
