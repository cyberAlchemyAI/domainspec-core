# UX Plan: Invoke Design Dispositions

## User goals

| Goal | Actor | Success signal |
| --- | --- | --- |
| know why a companion or extension was selected | developer | result cites the signal, predicate, owner, and output |
| know how to repair a blocked Design | developer | diagnostic identifies the missing input, unknown, unbound signal, owner, or changed pass |
| distinguish planned from proved evidence | maintainer | result shows one exact evidence state and never implies later evidence |

## Human semantic contract

The changed surface is textual rather than graphical. A user reads and acts on
four dispositions:

- `required`: must be authored now;
- `recommended`: advisory, with owner and revisit condition;
- `not-applicable-with-rationale`: negative detector evidence and selectors
  establish the boundary;
- `block`: repair is required before validator-backed Design handoff.

## Journeys

| Journey | Success | Failure/recovery |
| --- | --- | --- |
| ordinary bounded Design | exact minimal companions are selected | unexpected universal selection exposes predicate/fixture failure |
| missing scope signal | block names source selector and signal class | user repairs manifest and reruns from pass one |
| unresolved owner | block names the concern and required owner fields | user names an accountable owner or routes consequential choice |
| changed pass two | block shows changed signal/disposition/output | user supersedes input digest; no third implicit loop |
| Plan handoff | `design-validator-pass` is explicit | `authored-complete` routes only to validator remediation |

## Content and accessible operation

- Diagnostics use stable codes plus plain-language explanations.
- Meaning never depends on color, position, or icon alone.
- Tables and generated Markdown preserve headings and reading order.
- Every repair message states: what failed, evidence selector, owner, and next
  action.
- Recommended outputs cannot be visually or textually confused with required
  outputs.

## Acceptance

| Signal | Evidence owner |
| --- | --- |
| positive human-semantic fixture selects `ux-plan` | fixture runner |
| backend-only and semantics-preserving controls do not select `ux-plan` | fixture runner |
| focus, reflow, accessible-name, recovery, and operator-visible evidence mutations trigger UX | mutation fixture suite |
| every blocking diagnostic names a repair path | selection validator |

## Handoff boundary

- Architecture owns structural surface placement and data flow.
- UX owns the human meaning, recovery, content, and accessible operation.
- Plan owns runnable fixtures and rendered-output checks.

