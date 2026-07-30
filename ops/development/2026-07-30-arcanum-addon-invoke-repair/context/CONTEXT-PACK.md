# Context Pack: Arcanum add-on Invoke repair

## Summary

- Task: close `NEW-001` and `NEW-BAL-001` in the existing blocked
  Define/Design/Plan package.
- Mode: standard, strict
- Files selected: 14
- Obligation coverage: 100%
- Handoff pack: none; this is refresh authoring evidence, not runtime context.
- Inventory lookup: repository-local Inventory is absent; exact file inventory
  was used and this fallback is recorded as a validation gap.
- Strict coverage: pass

## Obligations

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| O1 | Make partial-wave advancement structurally impossible. | revalidation findings `NEW-001`; current `WORK-PACK` SWU graph; `DISPATCH.json` | covered |
| O2 | Separate enabled/running degradation from the later disabled lifecycle snapshot. | revalidation findings `NEW-BAL-001`; `VALIDATION-CONTRACTS.md`; TASK-4 | covered |
| O3 | Synchronize every derived result/status artifact affected by O1/O2. | Design/Plan result JSON and both Distill validation docs | covered |
| O4 | Preserve block, all owner/lifecycle blockers, and `selectedSWU: none`. | `WORK-PACK.md`; `PLAN-RESULT.json` | covered |
| O5 | Materialize only the approved path set and validate exact repaired bytes. | Invoke refresh contract; material receipt; validation scripts | covered |
| O6 | Document the corpus digest algorithm beside review digest evidence. | Design and Plan Distill validation docs; refresh report | covered |

## Selected Evidence

| Source | Selectors | Obligation |
| --- | --- | --- |
| `ops/development/2026-07-30-arcanum-addon-plan-revalidation/findings.md` | `NEW-001`, `NEW-BAL-001`, Ordered Change Requests, Claim Ceiling | O1, O2, O4, O6 |
| `.agents/skills/invoke/refresh.md` | Activation Gate, Mutation Modes, Mode Gates, Evidence Capability Contract | O3, O5 |
| `.arcanum/profiles/decision-profile.yml` | smallest-reliable, testable, reconcile-before-act, owner-scoped, immutable Arcanum | O1, O4, O5 |
| target `plan/WORK-PACK.md` | SWU Execution Handoff, Blockers, Gate Checks | O1, O3, O4 |
| target `plan/DISPATCH.json` | implementation route | O1 |
| target `design/VALIDATION-CONTRACTS.md` | Fixtures, Validator Contracts | O2 |
| target TASK-4 | degradation, uninstall, rollback, security, synchronization | O2 |
| target `plan/work-pack/shared/CLOSEOUT-SYNC.md` | DEGRADE, UNINSTALL, ROLLBACK, SECURITY rows | O1, O2 |
| target Design/Plan result JSON | Distill, repository validation, next route | O3, O4 |
| target Design/Plan Distill docs | review chronology and current claim ceiling | O3, O4, O6 |
| helper receipt | independent minimum-delta and derived-file check | O1-O5 |

## Exact Target Inventory

1. `development/arcanum-addon/plan/DISPATCH.json`
2. `development/arcanum-addon/design/VALIDATION-CONTRACTS.md`
3. `development/arcanum-addon/plan/work-pack/tasks/TASK-4-LIFECYCLE-ACCEPTANCE.md`
4. `development/arcanum-addon/plan/work-pack/shared/CLOSEOUT-SYNC.md`
5. `development/arcanum-addon/plan/WORK-PACK.md`
6. `development/arcanum-addon/design/DISTILL-VALIDATION.md`
7. `development/arcanum-addon/plan/DISTILL-VALIDATION.md`
8. `development/arcanum-addon/design/DESIGN-RESULT.json`
9. `development/arcanum-addon/plan/PLAN-RESULT.json`

## Excluded Candidates

- `EXECUTION-PACK.md`, W4, W5, and TASK-5: already require complete prior-wave
  closure and need no semantic delta.
- Runtime/product files: outside Invoke refresh scope.
- Public `arcanum/`: immutable substrate for this consumer repair.
- Browser execution: downstream of implementation and security closure.
- GitHub/Project mutation: still owned by `B-GOV-001`.

## Authority And Claim Ceiling

This pack authorizes only the nine-path planning refresh already approved by
the user. It does not select an SWU, execute a Task Session, mutate Bootstrap
packages, run a browser, close `B-DESIGN-001`, or establish readiness,
promotion, deployment, or release.
