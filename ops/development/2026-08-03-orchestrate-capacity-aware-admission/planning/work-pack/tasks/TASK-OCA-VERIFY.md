---
taskId: TASK-OCA-VERIFY
status: planned-read-only
layer: L2-boundary
wave: W6
---

# Integrated verification

## Objective

Verify that the five SWUs recompose into one capacity-aware Orchestrate flow,
preserve current behavior, and stay inside public/private and host-authority
boundaries. This is a closure task, not an implementation SWU.

## Read scope

- exact canonical/generated paths changed by the five SWUs
- their terminal Task Session and Invoke Refresh receipts
- `WORK-PACK.md`, `SWU-MANIFEST.json`, and `VALIDATION-STRATEGY.md`
- current Orchestrate regression fixtures

## Procedure and acceptance

1. Verify all five receipts bind current target digests and the planned SWU.
2. Run every exact command in `VALIDATION-STRATEGY.md` plus each new test file.
3. Exercise the recomposed sufficient, blocked, and residual late-failure
   scenarios.
4. Compare canonical/generated manifests and scan public bytes for private
   incident/path/account details.
5. Confirm no code claims reservation, physical release, queueing, deployment,
   or production readiness without corresponding owner evidence.
6. Run scoped whitespace and unrelated-diff checks.

Pass requires zero-action capacity blocks, causally valid null-agent failures,
honest provider ceilings, non-mutating options, projection parity, and all
regressions green. Any failure routes to its owning SWU; verification does not
silently repair bytes.

Owner: independent validation owner. Result: one pass/block receipt with exact
commands, hashes, failures, and carried residue. No live spawn canary is part of
this task.
