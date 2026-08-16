# Orchestrate native-runner repair proposal

Status: `CANDIDATE_VALIDATED_AWAITING_EXACT_BYTE_ACCEPTANCE`

Candidate-set digest: `b9eddd5cc97855b3e67aa60b474fc4728dd080d906184194f800ed821b9abbb4`

## Scope

This candidate repairs three governance/runtime defects exposed by the failed
Arcanum-to-cyberAlchemy-v2 wayfinding dispatch:

1. repeated waits attempted to recreate already-issued registration requests;
2. native task names were neither run-scoped nor namespace-safe;
3. a later-wave spawn failure could not produce a valid terminal blocked-run
   closeout after earlier waves had joined and passed their gates.

It also adds a selective `--runtime orchestrate` sync route so the accepted
canonical repair can regenerate only the Codex and Claude Orchestrate packages.
No schema changes are proposed.

## Root causes and repaired invariants

- `prepare_wait` treated every wait as the first wait. The candidate verifies
  and reuses existing registration requests, creates only missing requests,
  excludes terminal actions from the pending set, records every actual wait
  attempt, and makes request creation exclusive and fail-closed.
- Spawn task names used role and action only. The candidate derives an opaque
  run scope from `sha256(dispatch_id + NUL + run_id)` and emits
  `orchestrate_<scope>_<action-id>`, without leaking raw role, dispatch, run,
  target, or reference vocabulary.
- `run_blocked` validation applied same-wave cleanup rules to the entire run.
  The candidate scopes failed/cleaned actions and join/gate prohibitions to the
  blocked wave, while retaining globally unique, final terminal closeout and
  requiring joins for successful actions outside the blocked wave.
- The documented single-package sync surface did not recognize the runtime-only
  Orchestrate package. The candidate adds an explicit runtime selector and a
  regression proving unrelated generated packages remain untouched.

## Acceptance boundary

The complete target set, before/after hashes, and digest algorithm are in
`changed-byte-inventory.json`. The candidate has not been applied to canonical
Arcanum or either generated package. Acceptance of this candidate does not
authorize Git operations, publication, deployment, installation into
`.arcanum/runtime`, cyberAlchemy-v2 mutation, or execution of the r2 research
dispatch.

After exact-byte acceptance, the authorized edge is:

1. verify every before hash;
2. apply the eight candidate source/test/tool files exactly;
3. rerun the acceptance-critical test set against the applied bytes;
4. selectively regenerate the six listed Codex/Claude Orchestrate files;
5. verify every after hash and rerun scoped whitespace/content checks;
6. publish an apply receipt, then rematerialize r2 as a separately gated
   dispatch.
