# Distill Repair

Status: `pass`
Capability: `distill`
Mode: `validate`

## Repair Target

Validate and repair the integration design so it remains a small executable
prototype gate instead of expanding into a platform rewrite or BodyWar-only
special case.

## Balancer Objections And Repairs

| Objection | Repair |
| --- | --- |
| The gate could become a replacement UI pipeline. | Keep it after `UI-SPEC.md`/`TEST-SPEC.md` and before app implementation. |
| The gate could block BodyWar Playwright work. | Make it optional and independently executable through Studio preview. |
| Handoff export could become source-of-truth promotion. | Handoff is evidence only; spec promotion requires explicit sync. |
| Prototype HTML could skip security rules. | Require no real secrets/private data and map to security/privacy clauses from UI-SPEC. |
| `data-od-id` IDs could become ad hoc. | Derive IDs from UI concepts and include unmapped/fallback selector report. |

## Repaired Unit

**Studio Prototype Gate Contract v1**

Minimum execution shape:

1. Select one feature with existing `UI-SPEC.md` and `TEST-SPEC.md`.
2. Create a Studio session with isolated `STUDIO_DATA`.
3. Register 1-3 self-contained HTML variants.
4. Stamp `data-od-id` from feature UI concepts.
5. Preview, annotate, and accept/revert within Studio.
6. Export a handoff with explicit confirmation.
7. Consume the handoff in a target-app task-session.

## Pass Criteria

| Criterion | Result |
| --- | --- |
| Small enough to execute in one or two task-sessions | pass |
| Recombines into DomainSpec UI pipeline | pass |
| Does not mutate target app | pass |
| Does not require external research | pass |
| Names validation surfaces | pass |

## Verdict

`pass`: the repaired unit is executable and bounded. It should route to Invoke
Plan and then task-session, not direct implementation inside Refine.

## Receipt

```json
{
  "stage": "08-distill-repair",
  "status": "pass",
  "artifacts": [
    "stages/08-distill-repair.md"
  ],
  "validation_result": "pass",
  "blockers": [],
  "residue": [
    "First execution should produce a reusable handoff path convention."
  ]
}
```
