# Business Meaning — Deny Overrides Allow

## Identity

| Field | Value |
| --- | --- |
| Candidate ID | `BusinessMeaning:auth-access-control.deny-overrides/v1` |
| Bounded context | `auth-access-control` |
| Source rule | `AuthorizeRequest.R3` |
| Domain owner route | auth access-control business/domain owner |
| Current state | observed source; meaning has an unresolved carrier |

## Business Statement

When a protected action has both permission to proceed and an applicable rule
that explicitly denies it, the explicit denial wins.

In plain language:

> A specific refusal must not be hidden by a broader permission.

Example:

- Ana may administer users because she has `auth-access-control.admin.*`.
- Ana also has an explicit DENY for
  `auth-access-control.admin.delete`.
- Ana may read and update users, but she must not delete a user.

Counterexample:

- The system sees the broad ALLOW first and lets Ana delete the user without
  checking the exact DENY.

## Existing Source Evidence

| Source | What it says |
| --- | --- |
| `docs/auth-access-control/operations.md#authorizerequest` | R3 says `exists denyMatch => decision = DENY`. |
| `docs/auth-access-control/workflows.md#permissionresolutionpolicy` | DENY ranks above exact, scoped wildcard, global wildcard, and no match. |
| `docs/auth-access-control/decisions.en.md` | The confirmed decision says DENY overrides ALLOW. |
| `docs/ontology/auth-domain-ontology.json#CON-04` | The declared input cannot carry a DENY effect, so the rule has no documented carrier. |

## Meaning That Must Be Fixed Before Admission

The phrase “applicable DENY” needs answers to four questions:

1. Where does the DENY grant come from at decision time?
2. Which grantee types apply: principal, role, group, or all of them?
3. Which snapshot and time decide whether a grant is current?
4. Does wildcard matching use the same rule for ALLOW and DENY?

The current implementation answers only part of this operationally: it loads
principal grants from `PermissionGrantRepository` and retains their DENY
effects. Implementation behavior is useful evidence, but it cannot decide the
business meaning by itself.

## First Bounded Slice

To keep the first EVF experiment small, the candidate `FormalClaim` covers:

- one protected authorization request;
- one principal;
- one authoritative grant snapshot loaded for that principal;
- exact permission-key matching;
- at least one matching principal DENY;
- any number of matching or broader ALLOW grants; and
- the resulting authorization decision.

Declared loss for this first slice:

- role and group DENY grants;
- wildcard DENY matching;
- grant expiry, revocation, and concurrent updates;
- distributed snapshot consistency;
- all other authentication and session rules; and
- whether the complete broad wording of R3 is correct for every grant type.

This bounded slice can be used only if the business owner accepts that it is a
faithful first part of R3, not a replacement for the full rule.
