# Invoke Refresh Context Pack — OEWSN Owner Decisions

Status: strict coverage pass; session evidence only

## Identity

- Mode: `invoke:refresh:apply-approved`
- Target: `ontology-evidence-workbench-semantic-navigation`
- Evidence date: 2026-08-02
- Activation: direct user
- Runtime handoff: none; Invoke applied its own bounded planning delta

## Obligations

| ID | Obligation | Status | Controlling evidence |
| --- | --- | --- | --- |
| O-01 | Apply only the approved Body War profile | covered | Decision Gate result and approved profile |
| O-02 | Close OD-01–OD-04 without inventing decisions | covered | four resolved decision rows and five admissibility digests |
| O-03 | Select only SWU-OEWSN-004 | covered | Work Pack, SWU manifest, TASK-01 and W1 |
| O-04 | Keep product mutation blocked until Task Session admission | covered | mutation-admission contract and closeout inventory |
| O-05 | Make material/output partitions machine exact | covered | SWU manifest fields for all 17 implementation/evidence units |
| O-06 | Preserve private/internal and authority-none ceilings | covered | approved profile, material package and receipt |
| O-07 | Validate exact applied planning bytes | covered | staged package, handoff result and post-apply checks |

## Selected Sources

| Path | Selectors | Obligations |
| --- | --- | --- |
| `planning/decisions/DECISION-GATE-RESULT.json` | result, resolved, receipts, next step | O-01, O-02 |
| `planning/decisions/BODY-WAR-PROFILE-APPROVED.json` | OD-01–OD-04, remaining blockers, authority effect | O-01, O-02, O-06 |
| `planning/WORK-PACK.md` | control fields, task board, SWUs, gates/gaps | O-02, O-03, O-04 |
| `planning/SWU-MANIFEST.json` | selected unit, dependencies, write scopes, handoff states | O-03, O-05 |
| `planning/MUTATION-ADMISSION-CONTRACT.json` | pre-mutation requirements and forbidden effects | O-04, O-05, O-06 |
| `planning/CLOSEOUT-SYNC-INVENTORY.json` | SWU-004 closeout targets and successor policy | O-04, O-07 |
| `planning/work-pack/tasks/TASK-OEWSN-00-PROFILE-DECISIONS.md` | four manual SWUs | O-02 |
| `planning/work-pack/tasks/TASK-OEWSN-01-RELATION-CORE.md` | SWU-004 contract | O-03, O-04 |
| `planning/work-pack/waves/W0-OWNER-DECISIONS.md` | owner-decision gate | O-02 |
| `planning/work-pack/waves/W1-L0-RELATION-CORE.md` | first L0 gate | O-03, O-04 |
| `planning/work-pack/shared/cross-task-gaps.md` | remaining non-owner gaps | O-02, O-06 |

## Constraints And Resolution

- Decision receipts are immutable evidence inputs, not refresh targets.
- `selected_swu=SWU-OEWSN-004` is selection evidence only.
- `mutation_authorized=false` and `mutation_ready=false` remain true for
  product work until Task Session produces a live admission receipt.
- Human/novice A/B testing is not required for this local single-owner
  prototype; human-outcome claims remain outside the evidence ceiling.
- The read-only helper found no unresolved owner choice and changed no files.

## Excluded Candidates

- Historical Define/Design/Plan receipts: retained as the evidence state at
  their original run; not rewritten by this bounded refresh.
- Product implementation paths: excluded until Task Session admission.
- Ontology, authority, publication, release and deployment paths: forbidden.

## Strict Coverage

- Obligations covered: 7/7
- Contradictions unresolved: 0 inside the refresh scope
- Product mutation admitted: no
- Next owner: Task Session for `SWU-OEWSN-004`
