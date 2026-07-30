# Invoke Re-entry Repair Audit Helper Receipt

- Agent: `/root/invoke_reentry_repair_audit`
- Route: `invoke:refresh`
- Scope: read-only planning-corpus audit
- Status: `pass`
- Join status: completed
- Close status: closed
- Mutation: none

## Admitted Repair

The helper required exactly 25 machine-bound SWU admissions:

- every SWU admission consumes
  `receipts/selections/{session_id}/{selected_swu_id}.json`;
- the selection binds operator confirmation, issuing owner, session/run,
  dispatch and Plan digests, work-pack digest, source commit, literal SWU and
  step IDs, dependency receipt digests, predecessor closeout, timestamps, and
  a single-use claim;
- admission atomically claims the selection before any task start;
- stale, replayed, path/content-mismatched, dependency-incomplete, or
  predecessor-incomplete selections return zero task starts, owner attempts,
  and mutations;
- terminal SWU receipts echo the selection receipt digest; and
- joins, readiness, and `s14-boot-post-refresh` are not independently
  selectable.

## Artifact Guidance

The helper identified the Plan route, work-pack, execution pack, closeout,
technique trace, Distill result, Plan result, Plan transport, selection schema,
and runtime validator as the coherent exact scope. Task and wave files require
no change because their handoffs already defer to the shared contracts.

## Counter-examples

Required attacks included pre-created selections, replay, selection path/content
mismatch, source/Plan drift, missing predecessor closeout, two siblings in one
session, manual/verification SWU bypass, accidental selection of the BOOT-002
postcondition, and crash-after-claim replay.

## Residue

`NEW-001` and `B-DESIGN-001` remain open until fresh independent exact-byte
revalidation. Governance, Bootstrap, owner, adapter, and retention blockers
remain independent. No SWU was selected and no implementation, browser,
GitHub, or product lifecycle action was performed.
