# MARS Canonical Definitions

Purpose: normative semantics for MARS governance terms used across planning, execution, analysis, and evidence adjudication.

Interpretation rule:
- Definition statements are normative.
- `Intuition` notes are explanatory and non-normative.

## MARS-DEF-001 Methodology Profile

Definition:
A methodology profile is the experiment-scoped method contract that declares tier, measurement commitments, validity-treatment policy, and reproducibility metadata obligations.

Intuition:
This is the ruleset for how the experiment must be run and judged, not just a description of intent.

## MARS-DEF-002 Source Quality Gate (G2)

Definition:
The source quality gate is the mandatory control that verifies selected sources satisfy accessibility, authority-depth fitness, and immutable version-pin requirements before execution can proceed.

Intuition:
If sources are weak or unpinned, all later conclusions are fragile.

## MARS-DEF-003 Inventory Readiness Gate (G3)

Definition:
The inventory readiness gate is the mandatory control that verifies every required primary source has complete inventory extraction coverage and traceable linkage to experiment requirements.

Intuition:
Do not run an experiment if required knowledge was not extracted and normalized first.

## MARS-DEF-004 Context Bundle

Definition:
A context bundle is the experiment-scoped synthesis artifact that normalizes term mappings, metric definitions, source roles, and known conflicts required for deterministic execution and interpretation.

Intuition:
This is the shared map that keeps everyone using the same meaning during the run.

## MARS-DEF-005 Claim Adjudication

Definition:
Claim adjudication is the structured decision process that maps analyzed experiment evidence to claim-strength status and records explicit support, weakness, or contradiction updates.

Intuition:
It is the formal judgment step where evidence changes claim confidence.

## MARS-DEF-006 Foundation Tier

Definition:
Foundation tier is the minimum valid rigor mode requiring stages S1-S9 and S11, with optional S10, to produce directional evidence under hard-gate enforcement.

Intuition:
This is the cheapest acceptable run that still produces credible directional findings.

## MARS-DEF-007 Full Tier

Definition:
Full tier is the publication-grade rigor mode requiring stages S1-S12 with deep-analysis and synthesis obligations for high-impact claim updates.

Intuition:
This is the complete end-to-end evidence path used when stronger confidence is required.
