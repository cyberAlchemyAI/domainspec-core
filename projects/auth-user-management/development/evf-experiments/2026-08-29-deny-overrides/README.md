# Deny Overrides — First Business Rule To EVF Obligations

Status: candidate definition; semantic decision required
Visibility: private
Authority effect: none
Implementation effect: none
EVF execution: not selected

## Purpose

Use one real rule from `auth-user-management` to learn how business meaning
becomes a `FormalClaim`, then becomes proof obligations, checks, and bounded
evidence.

The selected rule is `AuthorizeRequest.R3`:

> Deny rules override allow rules.

The current short formula is:

```text
exists denyMatch => decision = DENY
```

This is a good first case because the business idea is easy to explain and the
repository already contains documentation, code, unit tests, and a Postgres E2E
scenario. It also contains a real modeling gap: the documented
`AuthContext.permissions` is a list of strings and cannot carry `ALLOW` or
`DENY`. The code solves this by loading principal DENY grants during
authorization, but the business documents do not yet say that this is the
intended domain rule.

## Current Result

We can create the chain as a candidate, but we cannot honestly call the
`FormalClaim` admitted yet.

```text
BusinessMeaning: deny overrides allow
  -> FormalClaim candidate: matching principal DENY implies DENY decision
  -> planned obligation 1: the operation sees every applicable DENY grant
  -> planned obligation 2: the decision function gives DENY first priority
  -> supporting obligation: DENY becomes FORBIDDEN and AccessDenied
```

The first obligation is the critical one. Proving only the decision function
would show that precedence works **when DENY data is present**. It would not show
that `AuthorizeRequest` actually receives the DENY data required by the business
rule.

## Artifact Guide

| Artifact | Use |
| --- | --- |
| [BUSINESS-MEANING.md](BUSINESS-MEANING.md) | The rule in business language, its examples, scope, and open decision. |
| [FORMAL-CLAIM-CANDIDATE.md](FORMAL-CLAIM-CANDIDATE.md) | The first exact formal statement and its declared limits. |
| [PROOF-OBLIGATIONS.md](PROOF-OBLIGATIONS.md) | The obligations, expected negative cases, and current evidence anchors. |
| [ONTOLOGY-AND-EVF-MAP.md](ONTOLOGY-AND-EVF-MAP.md) | How the auth ontology, DomainSpec ontology, and EVF evidence chain connect. |
| [INDEPENDENT-SEMANTIC-REVIEW.md](INDEPENDENT-SEMANTIC-REVIEW.md) | Read-only review of the proposition, obligation split, and claim ceiling. |
| [experiment-model.json](experiment-model.json) | Machine-readable candidate map. It is not a `FormalClaimSourcePayload/v2`. |

## Decision Required

The domain owner must select where DENY information lives when authorization is
decided.

| Path | Meaning | Consequence |
| --- | --- | --- |
| A — load DENY grants during authorization | `AuthorizeRequest` reads the authoritative grant store before deciding. | Matches the current code. Requires the operation dependency and grant snapshot to become part of the meaning and binding. |
| B — carry typed grants in `AuthContext` | The authenticated context contains permission key plus effect. | Makes the decision input self-contained, but changes the context/session contract and stale-data risk. |
| C — resolve DENY before authorization | Another operation produces a final decision or filtered capability set. | Moves R3 out of `AuthorizeRequest`; the current ontology and responsibility statement must change. |

For the first experiment, Path A is the smallest implementation-aligned path.
That is a recommendation, not business-owner acceptance.

## Next Gate

Run a small domain decision over Paths A–C. If Path A is accepted, freeze the
exact grant snapshot rules, admit the bounded `FormalClaim`, derive the two R3
obligations, and then create an executable DS-SFOL projection. Until then the
correct EVF result is `needs_formal` or `blocked`, not PASS.

## Claim Ceiling

This package defines an experiment candidate. It does not accept business
meaning, admit a formal claim, derive canonical obligations, prove the code,
discharge an obligation, establish full authorization security, authorize a
release, or make any publication claim.
