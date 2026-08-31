# FormalClaim Candidate — Matching Principal DENY Wins

## Candidate Identity

| Field | Value |
| --- | --- |
| Claim ID | `FormalClaim:auth-access-control.principal-exact-deny-wins/v1` |
| Formal-claims owner | pending exact role binding |
| Business binding | `BusinessMeaning:auth-access-control.deny-overrides/v1` |
| Relation | proposed `formalizes` |
| State | blocked before admission |
| Formal profile | candidate DS-SFOL bounded predicate |

The proposed `formalizes` relation is limited to the first bounded slice. Its
declared loss is recorded in `BUSINESS-MEANING.md`. It is not an accepted claim
that this formula captures all of R3.

## Canonical Proposition Candidate

Plain technical English:

> For every authorization request and its authoritative principal-grant
> snapshot, if at least one current principal DENY grant has the exact required
> permission key, the authorization decision is DENY, even when an ALLOW grant
> also matches.

Logic-shaped form:

```text
forall request, grantSnapshot.
  canonical(request.requiredPermission)
  and authoritativeFor(
        grantSnapshot,
        request.principalId,
        request.evaluationTime)
  and exists denyGrant in grantSnapshot.
        denyGrant.granteeType = PRINCIPAL
        and denyGrant.granteeKey = request.principalId
        and denyGrant.effect = DENY
        and denyGrant.permissionKey = request.requiredPermission
  implies
    authorizeDecision(request, grantSnapshot) = DENY
```

“Even when an ALLOW grant also matches” is covered because the implication does
not exclude ALLOW grants from `grantSnapshot`.

## Why This Is One Claim, Not One Test

The proposition combines two necessary facts:

1. `AuthorizeRequest` decides over an authoritative grant snapshot that includes
   the applicable DENY; and
2. the decision policy gives a matching DENY priority over every ALLOW.

A unit test of `resolvePermissionDecision` can support fact 2. It cannot support
fact 1. The operation-level business rule needs both.

## Candidate DS-SFOL Projection

After the carrier decision, the executable projection should use:

- a record sort for `AuthorizationRequest`;
- a record sort for `PermissionGrant`;
- an enum sort for `GrantEffect = ALLOW | DENY`;
- a fixture universe for the bounded grant snapshot;
- an `exists` quantifier for a matching DENY; and
- an implication whose result is the `DENY` enum member.

That projection must bind exactly this claim version and digest. It must not
become a second source of business meaning.

## Admission Blockers

| ID | Blocker | Why it matters |
| --- | --- | --- |
| `AUTH-R3-B01` | DENY carrier is not selected in the business model. | The formula would silently choose an operation dependency and responsibility. |
| `AUTH-R3-B02` | The exact authoritative snapshot/currentness rule is not defined. | “Applicable” cannot be evaluated consistently. |
| `AUTH-R3-B03` | Formal-owner assertion and independent business-owner fidelity acceptance do not exist. | The selected FormalClaim ontology candidate requires both for `formalizes`; its protected contracts also remain admission-pending. |
| `AUTH-R3-B04` | The candidate DS-SFOL projection and interpretation environment do not exist. | No executable predicate may be invented from the prose. |

## Claim Ceiling

If later admitted and evidenced, this claim could support only:

> For the exact accepted principal/exact-match/snapshot semantics and exact
> bound implementation, matching principal DENY grants cause a DENY decision
> under the recorded execution and evidence boundary.

It would not establish complete R3 coverage, role/group/wildcard behavior,
general authorization security, absence of vulnerabilities, production
readiness, or obligation discharge.
