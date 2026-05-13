# Evaluator Day 0-Day 1

## Scope

Evaluator onboarding assumptions and first-value framing for the first 24 hours.

## Finalized Decisions (Wave 1)

| Question | Decision                                                                             | Implication                                                                                     |
| -------- | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| Q1       | `A` - Engineering director is primary economic buyer                                 | Keep buyer-facing language anchored in release-risk reduction and governance confidence         |
| Q2       | `C` - CI exists, Sonar maturity is low, bootstrap needed                             | Keep onboarding flow guidance bootstrap-friendly and explicit about initial governance setup    |
| Q3       | `B` - First value moment is actionable finding bundles exported as remediation tasks | Lead day-1 value narrative with usable work output, not only policy explanation                 |
| Q4       | `C` - Top objection is overhead without outcome gain                                 | Show outcome proof with measured tasking and governance evidence, not additional process claims |

## Day 0 Entry Condition

- Target evaluator has active CI but uneven Sonar maturity.
- Sonar Loop positioning starts with guided bootstrap and governed defaults.
- The evaluator should see concrete task outputs by day 1.

## Day 1 Value Proof

Primary proof package:

1. Actionable finding bundles converted into remediation tasks.
2. Task export path is explicit and auditable.
3. Governance evidence remains visible to counter overhead concerns.

Primary references:

- [CreateAndExportRemediationTasks](../operations.md#createandexportremediationtasks)
- [ApiFirstTaskIntegrationPolicy](../rules.md#apifirsttaskintegrationpolicy)
- [Story US-006](../STORIES.md#us-006-run-sonar-against-selected-gate-and-bundle-findings)
- [Story US-007](../STORIES.md#us-007-export-finding-tasks-to-github-and-jira-via-api-first-paths)

## Objection Handling: Overhead vs Outcome

To address the day-1 overhead objection, evaluation messaging must tie each mandatory control to visible output:

- checkpoint and control semantics reduce unsafe loop continuation risk
- finding bundles improve remediation context quality
- task export states make progress inspectable without hidden work

See also: [workflows.md](../workflows.md), [rules.md](../rules.md), [README.md](../../../../README.md)
