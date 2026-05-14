# TASK-L1-HARDENING: Deterministic Single-Repo Hardening

## Goal

Add deterministic retry, skill-bundle reuse/recompose, three-candidate solution generation, abstraction scoring, and learning writeback.

## DomainSpec Coverage

`sonar-loop.SkillBundleProfile`, `sonar-loop.SolutionCandidate`, `sonar-loop.LearningMemory`, `sonar-loop.ComposeAgnosticSkillBundle`, `sonar-loop.GenerateThreeCandidateSolutions`, `sonar-loop.SynthesizeCrossSmellAbstractions`, `sonar-loop.ApplyOperatorSelectionLearning`, `sonar-loop.SonarRetryPolicy`, `sonar-loop.SkillBundleReusePolicy`, `sonar-loop.ThreeCandidateSolutionRule`, `sonar-loop.NonRedundantAbstractionRule`, `sonar-loop.LearningFeedbackRule`, `sonar-loop.ProgressiveQualityLoopWorkflow`.

## Architecture References

- Domain layer owns retry policy, branch policy, candidate constraints, abstraction scoring, and learning invariants.
- Application layer owns compose/reuse orchestration and learning update use-cases.
- Infrastructure layer owns any runtime/pattern catalog adapter.

## Implementation Directives

- Implement one bounded Sonar retry with remediation evidence.
- Implement exactly one skill-bundle branch per pass: recomposed or reused.
- Generate exactly three candidates per remediation task.
- Apply abstraction scoring and deterministic tie-breaks before accepted abstraction references are attached.
- Persist learning only with selected candidate, rationale, observed outcome, and quality delta.

## Gaps and Questions

- Pattern catalog storage location must be confirmed during execution.
- Learning persistence backend remains adapter-owned.

## Decision Lock

- D-001 remains in force; external export is not part of L1 unless needed by local fixtures.
