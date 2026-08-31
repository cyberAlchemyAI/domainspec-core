# OWNER-BWSL-001 Independent Decision Review R1

## Outcome Brief

`FAIL`: do not issue an owner request from decision graph SHA-256
`0785ccb7dcf1905368376a6aaf21da1711a03138f2031f3ec0905a33680d71eb`.

All six admissibility receipts rehashed, returned `gate`, and admitted their
recommended options. The graph nevertheless understated the real external
surface and overstated privacy guarantees.

## Blocking findings

1. The normal UI route performs two activity-list provider calls: page 1 with
   `per_page=12` for `GET /api/activities`, then page 1 with `per_page=50`
   when the evidence POST revalidates the selected activity. The graph declared
   one.
2. A public `redacted_summary_sha256` is a stable correlator without useful
   public verification when values are omitted. `eligible_activity_count`
   exposes activity-frequency metadata. Neither belongs in the proposed
   minimal receipt.
3. `retained_after_cleanup: only the permitted non-private receipt`
   contradicted explicit residue: runner profile, disconnected provider-account
   metadata, SuggestedTrack state, and the source activity at Strava persist.
4. `evidence_after: absent` was too broad. Only the exact witness evidence row
   is guaranteed absent; unrelated candidates remain untouched.
5. A same-process `finally` cannot enforce a crash-safe 15-minute retention
   ceiling after abnormal process termination.

## Required repair

- Enumerate both exact activity-list calls.
- Remove payload-derived hash and activity count from non-private evidence.
- Scope deleted and retained data precisely, including external and identity
  residue.
- Assert absence only for the exact witness row.
- Require independently supervised abnormal-termination cleanup before any
  effect, or explicitly stop claiming a hard retention ceiling.
- Re-freeze, rehash, and independently review before emitting an owner request.

Reviewer-changed bytes: none. This review selects no policy and grants no
credential, provider-call, evidence-mutation, publication, deployment, release,
or production authority.
