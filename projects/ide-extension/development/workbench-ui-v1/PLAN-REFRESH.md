# Workbench UI V1 Plan Refresh

## Source Signal

The initial plan used one SWU per task. Operator review found those units too
large to claim safely because several contained multiple independently testable
behaviors.

## Applied Delta

- Preserved five coordination tasks and the approved product/design boundary.
- Replaced five task-shaped SWUs with eleven behavior-shaped SWUs.
- Added independent acceptance, split analysis, and first-unit narrowness proof.
- Kept `SWU-WUI-001` as the next handle, but narrowed it to semantic regions only.

## Result

The refreshed plan passes the improved Invoke atomicity contract and is ready
for one-SWU Task Session execution.
