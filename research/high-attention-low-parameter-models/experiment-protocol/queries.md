# Queries: High-Attention, Low-Parameter Experiment Protocol

## GetProtocolReadiness

Returns protocol version/status, unresolved decisions, missing runnable-witness
artifacts, failed validations, admitted cells, and the next blocking owner.

## GetTrialMatrix

Returns the explicit cross-product after approved pruning: fixture family, split,
arm, position, length, interference, model stack, repetition, and phase. It also
returns excluded cells with reasons.

## GetRunStatus

Returns queued, running, completed, failed, excluded, or aborted counts and links
to run receipts. It never converts failure into missing data silently.

## GetAnalysisEligibility

Returns whether every confirmatory cell has its required pair, score receipt,
resource boundary, and exclusion decision.

## GetResourceFrontier

Returns named axes, uncertainty, infeasible cells, weakly dominated cells, and
non-dominated cells. A caller must request axes explicitly; no default composite
score exists.

## GetGateStatus

Returns each decision/admission/promotion gate, owner, evidence, status, and
repair route.
