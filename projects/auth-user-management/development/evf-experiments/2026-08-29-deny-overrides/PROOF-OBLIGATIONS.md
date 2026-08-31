# Planned Proof Obligations

These are obligation designs. Under the selected DomainSpec-v2 ontology
candidate, a canonical
`ProofObligation` may be derived only from an exact admitted `FormalClaim` plus
immutable derivation context. The candidate claim is not admitted, so the
`derived_from` edges below are planned, not authored canonical relations.

## R3 Obligations

| ID | Required proposition | Why separate | Candidate evidence target | Negative mutation | State |
| --- | --- | --- | --- | --- | --- |
| `PO-AUTH-R3-CARRIER-001` | Every current matching principal DENY in the authoritative snapshot is present in the grant set used by `AuthorizeRequest`. | A correct precedence function is useless if the operation never sees the denial. | Operation binding around `PermissionGrantRepository.findByGranteeKeys` and the set passed to `resolvePermissionDecision`. | Remove the repository lookup, query the wrong principal, or filter out DENY. | blocked on carrier and snapshot meaning |
| `PO-AUTH-R3-PRECEDENCE-001` | If the decision grant set contains a matching DENY, the result is DENY regardless of matching ALLOW grants. | This is the pure precedence rule. | `resolvePermissionDecision` with an independently authored expected predicate. | Check ALLOW before DENY, flip DENY to ALLOW, or ignore the DENY member. | draft; derivation blocked on claim admission |

Both obligations must pass to support the operation-level R3 claim. Passing only
`PO-AUTH-R3-PRECEDENCE-001` supports a smaller statement about a pure function,
not the business rule as used by `AuthorizeRequest`.

## Supporting Observable Obligations

These come from neighboring domain commitments. They make the DENY decision
observable, but they are not silently attributed to R3 alone.

| ID | Source commitment | Required proposition | Candidate evidence target | State |
| --- | --- | --- | --- | --- |
| `PO-AUTH-P2-FORBIDDEN-001` | `AuthorizeRequest.P2` | A DENY decision produces the deterministic `FORBIDDEN` error contract and never returns `allowed: true`. | `authorizeRequestUseCase` result/error boundary. | planned |
| `PO-AUTH-EVENT-ACCESS-DENIED-001` | `AuthorizeRequest --produces--> AccessDenied` | A DENY result emits an `AccessDenied` event with the principal, required permission, reason, and recorded time. | event callback observation. | planned |
| `PO-AUTH-POLICY-ALLOW-CONTROL-001` | `AuthorizeRequest.R2` and `PermissionResolutionPolicy` | With no matching DENY and one exact matching ALLOW, the decision is ALLOW. | `resolvePermissionDecision` and operation result boundary. | planned non-trivial control |

Event cardinality and delivery semantics must be selected before this becomes a
stronger “exactly once” obligation. The current code emits once in the observed
test path; that observation does not define the domain contract.

The ALLOW control is necessary because an implementation that always returns
DENY would satisfy R3 by itself. It is not derived from R3; its source is R2 and
the policy decision table.

## Current Evidence Anchors

The repository already gives useful baselines:

- `tests/auth-access-control.test.ts` has a memory-backed case where a principal
  exact DENY overrides a wildcard ALLOW and emits `AccessDenied`.
- `e2e/auth-api.e2e.ts` repeats the authorization case with Postgres-backed
  grants.
- `src/domain/auth-access-control/permission-resolution.ts` checks DENY before
  ALLOW.
- `src/application/auth-access-control/authorize-request.ts` loads principal
  DENY grants before calling the decision function.

These are existing implementation tests and observations. They are not derived
EVF checks, provider results, normalized evidence handles, consumer receipts, or
proof of obligation discharge.

## EVF Evidence Plan

After semantic admission:

1. bind the exact `FormalClaim` source and admitted DS-SFOL projection;
2. derive both R3 obligations with one immutable derivation context;
3. bind the operation and pure decision symbols separately;
4. generate or select positive cases and independent negative mutations;
5. execute the selected provider/runtime under an exact manifest;
6. keep timeout, unknown, missing binding, and surviving mutation unresolved;
7. normalize results into EVF evidence handles;
8. obtain an independent consumer receipt; and
9. leave obligation discharge to its separate owner decision.

## Minimum Case Set

| Case | Snapshot | Expected decision | Purpose |
| --- | --- | --- | --- |
| C1 | exact ALLOW only | ALLOW | positive control, not evidence for R3 by itself |
| C2 | exact DENY only | DENY | simplest R3 witness |
| C3 | wildcard ALLOW plus exact DENY | DENY | discrimination witness used by current tests |
| C4 | exact ALLOW plus exact DENY | DENY | direct same-key precedence witness |
| C5 | DENY for another principal | not forced by this claim | rejects carrier overreach |
| C6 | DENY for another permission | not forced by this claim | rejects match overreach |

Cases using wildcard DENY or role/group DENY remain out of the first claim and
must not be counted as covered.
