# W2 - L1 Diff And Action Trust

## Layer Question

After this wave, we know whether visible changes and durable reversible actions
are represented honestly enough for operator trust.

## Tasks

- [TASK-GSP-002](../tasks/TASK-GSP-002-visible-change-diff.md)
- [TASK-GSP-003](../tasks/TASK-GSP-003-action-annotation-mobile.md)

## Dependencies

- `SWU-GSP-001` must pass first.

## Validation

- CSS/theme/global visible mutation cannot produce silent zero-diff confidence.
- Accept/Revert confirmation prevents accidental durable history advance.
- Mobile before/after and annotation first-slice are inspectable.
