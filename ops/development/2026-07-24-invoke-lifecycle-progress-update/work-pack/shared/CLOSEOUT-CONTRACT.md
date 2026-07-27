# Shared Task Session Closeout Contract

This contract applies to SWU-ILP-002 through SWU-ILP-009. SWU-ILP-001 is
non-mutating and returns a lifecycle decision receipt instead.

## Terminal source receipt

Each SWU returns the shape declared in `../../EXECUTION-PACK.md`, including one
SWU ID, result, exact files touched, validation, blockers, residue, and next
route.

## Exact synchronization target inventory

- `../../WORK-PACK.md`
- `../../GAPS.md`
- `../../LIFECYCLE-HANDOFF.md`
- `../swu-manifest.json`

No task infers an additional synchronization target after implementation.
Adding a target is a control change and requires a successor execution epoch.

## Baseline binding

Immediately after selecting the SWU and before the first implementation write,
Task Session must:

1. prove all four targets exist;
2. compute SHA-256 for each target;
3. bind the ordered path/digest list into the selected epoch or closeout
   preflight;
4. persist the list in session evidence.

Any later mismatch blocks reuse. A task file cannot store its own live digest,
so the receipt-bound preflight is the canonical baseline witness.

## Allowed closeout delta classes

- `status_changed`
- `evidence_added`
- `blocker_changed`
- `route_changed`
- `artifact_changed`

`plan_repair` is allowed only as the declared Refresh transition kind. If the
closeout alters an epoch-control field, Refresh must create a successor epoch
and submit `superseded`; it must not retain the old epoch ID.

## Owner validation

- parse all changed JSON;
- verify all task/SWU IDs resolve;
- verify one selected SWU at most;
- run the relevant focused owner suite named by the task;
- run Dispatch Spec validation when the route changes;
- scan public changes for private project names and paths;
- verify canonical/generated parity for any changed runtime surface.

## Expected owner receipt

One separate Invoke Refresh `apply-approved` owner receipt bound to:

- the terminal Task Session source receipt;
- the exact four-target inventory;
- the captured baselines;
- the allowed delta classes;
- the validation results;
- the returned next route.

Task Session never writes these owner targets directly. A receipt-backed no-op
is acceptable when all targets already represent the terminal result.

## Successor policy

- unchanged epoch control digest + new evidence/material: allowed forward edge;
- changed epoch control digest before mutation crossed: successor epoch and old
  epoch `superseded`;
- changed control after execution complete: independent
  `execution_invalidating` receipt required for supersession;
- change during `mutation_crossed`: block and require explicit recovery; direct
  supersession is forbidden.

