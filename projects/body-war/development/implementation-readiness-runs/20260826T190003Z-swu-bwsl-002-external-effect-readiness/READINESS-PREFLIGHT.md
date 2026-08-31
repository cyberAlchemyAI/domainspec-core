# SWU-BWSL-002 No-Effect Readiness Preflight

## Outcome Brief

The normal Body War import and submission path is locally coherent, but the
selected privacy policy cannot be executed safely yet. The current code would
refresh an expired token, has no independent cleanup supervisor or preallocated
evidence locator, does not enforce the exact granted scope set at callback, and
has no producer for the permitted non-private terminal receipt.

- Objective: determine whether one real Strava witness can be frozen for a
  separate exact external-effect request.
- Result: BLOCK before any effect request.
- Why it matters: OAuth now would cross the owner-selected privacy boundary
  without the required crash-path cleanup and receipt proof.

## Boundary And Next Decision

- Changed: run-local readiness evidence only.
- Unchanged: Body War product code, canonical planning, deferred Invoke repair,
  credentials, private identity, Strava state, real evidence, Git, deployment,
  release, and production state.
- Open questions: none requiring a policy choice; the current gaps are
  implementation and environment evidence gaps.
- User decision: none in this preflight.
- Next action: prepare a separately admitted no-effect prerequisite patch for
  the supervisor, locator, no-refresh/scope guards, and receipt producer.

## Gate Summary

| Gate | Result | Evidence |
| --- | --- | --- |
| SWU-BWSL-000 terminal dependency | PASS | cacf9624a9b015f3d05b2f4714462a76f1b2830cb8f100915e6e6a4f9e424602 |
| SWU-BWSL-001 terminal dependency | PASS | 1b675be54a89f97b531f93e6c793ff82404c8e100bdfbe534a847455323f4007 |
| OWNER-BWSL-001 policy selection | PASS | d90ef8a33769f995cb8c1dde8b87f0e25b0a396ce6dc050cbd46280403b6f205 |
| Current TypeScript compilation | PASS | tsc --noEmit |
| Current isolated emit versus dist | PASS | byte-identical |
| Exact source/binary/runtime identity | BLOCK | non-secret config and supervisor identity absent |
| Independent cleanup after primary death | BLOCK | no executable, control record, or integration proof |
| Exact pre-effect principal/evidence locator | BLOCK | no private principal prebinding exists and the database UUID is generated only at insert |
| No-refresh one-attempt path | BLOCK | expired-token branch automatically refreshes |
| Exact callback scope gate | BLOCK | returned scope is stored without exact-set enforcement |
| Non-private receipt contract | PASS as run-local schema candidate | strict schema and synthetic fixture |
| Non-private receipt producer/validator | BLOCK | no product entrypoint or script |
| App-controlled copy/environment proof | BLOCK | cannot be evaluated before exact environment freeze |
| Separate external-effect authority | BLOCK | not requested or granted |

## Current Provider Compatibility

- The app requests read and activity:read.
- Strava currently documents that the granted scope returned after OAuth may
  differ from the requested scope; the app must check it.
- Strava currently documents GET /api/v3/athlete/activities with page and
  per_page and requires activity:read.
- Strava currently supports provider-side deauthorization/revoke, but the
  selected Body War envelope contains no such call. Current
  revokeProviderAccess is local token deletion plus account disconnection only.

## Stop

No owner effect request is emitted from this run. Repeating SWU-BWSL-002 against
the unchanged blocker fingerprint
3e8cc0028a460f51697eb662995cb21eafc677d0b940de7a64deb4048fa28cf7
must return the same BLOCK rather than start OAuth.
