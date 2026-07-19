---
taskId: TASK-GCP-VERIFY
layer: L1-L3
slice: S1-S4
status: ready-after-proof
complexity: medium
---

# Task GCP Verify

## Objective

Independently replay each completed slice, check residue and digest continuity,
and close the evidence handoff without changing source authority.

## Acceptance Boundary

An independent verifier can locate the source anchors, rerun the declared checks,
and agree with the receipt verdict or record a discrepancy.

## Dependency

The first eligible input is the receipt from `SWU-GCP-001`; later slices remain
blocked until their own receipts exist.
