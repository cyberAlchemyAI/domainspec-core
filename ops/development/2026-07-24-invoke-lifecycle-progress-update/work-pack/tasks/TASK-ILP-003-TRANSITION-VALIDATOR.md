# TASK-ILP-003: Transition, Supersession, and Churn Validator

## Objective

Admit only the allowed append-only edge for one epoch and deterministically
reject in-place control repair, invalid edges, and unchanged churn.

- Layer/slice/wave: L1 / S1 / W1
- Lifecycle owner: ratified transition-admission owner plus Spellcraft for
  public artifacts
- Dependencies: SWU-ILP-001 and SWU-ILP-002
- Source contracts: `../shared/DECISIONS.md`, `../../DESIGN.md`
- Candidate write scope:
  - owner-approved `epoch-transition.schema.json`
  - owner-approved `validate_epoch_transition.py`
  - owner-approved transition fixtures and runner

## Algorithm

1. Schema-check request and every evidence receipt reference.
2. Confirm `admitted_by` matches the ratified owner.
3. Recompute the request's epoch control digest.
4. Match `(from_state, to_state, transition_kind)` against the exact allowed
   table.
5. Validate edge-specific witnesses.
6. For same-epoch readiness edges, require an unchanged control digest and
   prove the only delta is newly satisfied declared evidence/material.
7. If a `plan_repair` changes any control field, reject same-epoch movement and
   require successor ID, old/new digests, reason, and retained history for
   `superseded`.
8. Reject direct supersession from `mutation_crossed`.
9. Require independent `execution_invalidating` evidence for superseding
   `execution_complete`.
10. Compute churn key; if it repeats without changed preconditions, emit
    `churn_blocked` and append no transition.

## Smallest Working Unit

### SWU-ILP-003

- Primary behavior: admit or reject one lifecycle transition.
- Acceptance boundary: one owner-bound transition receipt or causal rejection.
- Candidate children: edge table; supersession; churn.
- Retained rationale: all are branches of the same transition-admission
  function and share one append/no-append outcome.
- Execution owner: `local-fallback` under the ratified lifecycle owner.
- Done criteria:
  - every allowed edge has a positive fixture;
  - self/backward/skipped/terminal-outbound/unlisted edges reject;
  - all epoch-control changes reject same-epoch repair;
  - valid evidence-only gated/blocked -> ready retains epoch;
  - repeated churn adds no transition.
- Validation:
  `python3 <owner-approved-runner> --group transitions`
- Handoff context: SWU-ILP-001/002 receipts plus
  `../shared/DECISIONS.md`.

## Closeout

Use `../shared/CLOSEOUT-CONTRACT.md`. Any change to the owner/source decision
blocks and routes back to SWU-ILP-001 rather than being repaired locally.

