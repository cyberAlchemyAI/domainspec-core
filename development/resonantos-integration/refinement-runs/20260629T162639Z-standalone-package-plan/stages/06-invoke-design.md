# S6 Invoke Design

## Status

Pass.

## Design Shape

The canonical plan uses a split work-pack:

- `IMPLEMENTATION-LAYERING.md` owns L0-L3 decisions.
- `WORK-PACK.md` owns the executable manifest.
- `EXECUTION-PACK.md` owns cross-task choreography.
- `work-pack/waves/` owns ordering.
- `work-pack/tasks/` owns SWU-level execution contracts.
- `work-pack/shared/` owns shared context, decisions, gaps, and traceability.

## Boundary Design

Private parent evidence is source evidence only. The package staging root is a future output and
must pass scrub checks before external handoff.
