# Cross-Task Decisions

## Decision Register

| Decision ID | Status   | Selected Option                        | Rationale                                                                                                  | Locked At  | Affected Tasks                                                                                           |
| ----------- | -------- | -------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ---------- | -------------------------------------------------------------------------------------------------------- |
| D-001       | selected | L0 creates local repository tasks only | Keeps the POC at the smallest slice that proves governed quality-to-task flow before external export risk. | 2026-05-14 | [TASK-L0-POC](../tasks/TASK-L0-POC.md), [TASK-L2-GOVERNANCE](../tasks/TASK-L2-GOVERNANCE.md)             |
| D-002       | selected | Keep L2 and L3 separate                | Keeps fallback/export/override governance evidence complete before multi-repo and packaging-fit claims.    | 2026-05-14 | [TASK-L2-GOVERNANCE](../tasks/TASK-L2-GOVERNANCE.md), [TASK-L3-SCALE-FIT](../tasks/TASK-L3-SCALE-FIT.md) |

## Decision Enforcement

- W1 must not require GitHub or Jira API success for L0 exit.
- W3 must add GitHub/Jira API-first export governance and degraded completion controls.
- W4 must not start until W3 degraded-path governance evidence exists.
- Any execution-time change to these decisions requires updating this file and [../../WORK-PACK.md](../../WORK-PACK.md) before mutation continues.
