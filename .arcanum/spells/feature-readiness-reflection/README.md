---
canonical_id: feature-readiness-reflection
aliases: []
scope: local
created_at: 2026-06-14T19:51:07Z
owner: spellcraft
status: draft
---

# Feature Readiness Reflection

## Purpose

Compose observability reflection with scoped Craft ledgers, Invoke plan
artifacts, and Refine strategy outputs so open feature work can be checked for
real execution readiness before another capability is asked to mutate code.

## Trigger Conditions

- A user asks what improvements should be made to Craft, Invoke, Refine, or an
  open feature workflow.
- A Refine strategy proposal, Invoke plan, or Craft next move has been mistaken
  for an executable work-pack.
- A scoped Craft ledger contains the next move, but the executable artifact or
  gate status is unclear.
- `task-session` blocks because the named target is not an execution-ready
  `WORK-PACK.md` or SWU.
- An adjacent evidence workspace may contain relevant observability signals,
  Craft ledgers, approval records, or nested product worktrees.

## Required Sigils

| Sigil | Role |
| --- | --- |
| `workflow-reflect` | Analyze signals and write evidence-backed improvement proposals. |
| `craft` | Resolve scoped ledgers and expose blockers, gaps, next moves, and linked artifacts. |
| `invoke` | Provide define/design/plan output boundaries, work-pack gate status, and executable SWU handoff state. |
| `refine` | Provide strategy proposal state, dispatch readiness, runtime handoff state, and pending Invoke route. |

## Optional Sigils

| Sigil | Use when |
| --- | --- |
| `task-session` | A reflection finding depends on a blocked or successful execution attempt. |
| `decision-gate` | A blocker-level decision prevents moving from plan to execution. |

## Prerequisites

- `.arcanum/observability/signals/sigil-invocations.jsonl` exists, or an
  explicit signal ledger is supplied.
- Any target feature has an owning Craft ledger or an explicit plan artifact.
- Reflection output is proposal-only unless a separate maintenance task is
  approved.
- External evidence workspaces are read-only unless the user separately starts
  a maintenance task in that workspace.

## Shared State

| State | Owner | Notes |
| --- | --- | --- |
| Signal ledger | observability | Primary trend evidence. |
| External signal ledger | observability | Optional adjacent-workspace evidence. |
| Scoped ledger state | `craft` | Source for current next moves, blockers, decisions, and linked artifacts. |
| Work-pack gate state | `invoke` | Source for execution readiness and SWU boundaries. |
| Strategy proposal state | `refine` | Source for non-executable planning state and pending confirmation. |
| Approval records | target owner | Source for whether local/static, product mutation, git, CI, active tests, or publication are allowed. |
| Reflection report | `workflow-reflect` | Proposal artifact for maintainers. |

## Execution Phases

| Phase | Input | Output | Gate |
| --- | --- | --- | --- |
| Resolve scope | User request plus available ledgers | Target sigils/features and ledgers | Block if scope is ambiguous and no safe default exists. |
| Load evidence | Signal ledgers, reflection state, scoped artifacts, optional adjacent workspaces | Signal counts and evidence table | Flag weak findings below threshold. |
| Compare readiness surfaces | Craft next moves, Invoke work-packs, Refine results, approval records | Proposal-vs-plan-vs-execution classification | Block direct execution when no work-pack/SWU or approval scope exists. |
| Generate proposals | Threshold-backed findings and structural gaps | Reflection report | Do not mutate observed sigils. |
| Route follow-up | Report decisions and owner split | Next owner recommendation | Route sigil contract changes through their owner lifecycle. |

## Handoff Artifacts

- `.arcanum/observability/reflections/<timestamp>-feature-readiness-reflection.md`
- `.arcanum/observability/reflection-state.json`
- Optional scoped Craft ledger paths and Invoke/Refine artifact paths cited in
  the report.
- Optional adjacent-workspace signal ledgers and Craft ledgers cited as external
  evidence.

## Gates

- Direct sigil mutation is forbidden during reflection.
- A Refine strategy proposal is not executable until an Invoke plan emits a
  `WORK-PACK.md` or equivalent execution contract.
- An Invoke plan with `block-for-app-mutation` can still be executable for
  explicitly ready W0 documentation SWUs.
- Craft evidence must resolve the owning ledger scope before proposing ledger
  state changes.
- Weak Craft findings caused by missing telemetry must be labeled as structural
  or instrumentation gaps, not trend-backed defects.
- Approval records must be treated as first-class readiness gates, especially
  when local/static checks are allowed but product mutation, git, CI, active
  tests, or publication remain blocked.
- Workspace roots and nested product git worktrees must not be conflated.

## Failure Policy

- Return `block` when signal ledgers cannot be read or the target scope cannot
  be resolved.
- Return `flag` when useful proposals exist but one or more target sigils lack
  enough direct telemetry.
- Return `pass` when threshold-backed proposals are written and owner routes are
  clear.

## Local Customization

This local spell is tuned for `domainspec-core`, where public `arcanum`
submodule changes must be handled submodule-first and parent-last. Reflection
reports may mention public sigil changes, but implementation must be routed
through the appropriate submodule and validated with the repository discipline.

## Observability

Each run should record the signal ledgers inspected, sigils/features covered,
thresholds triggered, proposal count, report path, and next owner route.

## Output Contract

```markdown
## Feature Readiness Reflection Result

- Spell: feature-readiness-reflection
- Signals inspected: <count and paths>
- Scoped ledgers inspected: <count or paths>
- External evidence: <paths or none>
- Threshold-backed findings: <count>
- Structural findings: <count>
- Report: <path>
- Next owner routes: <owners>
- Direct mutations: none
```
