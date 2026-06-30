# Findings: DDD Process Managers And Event-Sourced Email Uniqueness

## 1. Status / Verdict

**Verdict: accepted only after reviewer repairs.** A process manager or saga is the right orchestration mechanism for registration and mutable-email workflows, but it is not the proof of uniqueness. The recommended default is: stable `UserId`; versioned `EmailKey`; separate `EmailClaim` boundary keyed by `{scope}:{normalizationPolicyVersion}:{normalizedEmail}`; process manager coordinates create/change/verify/release/expire workflows; persistence enforces races through same-key serialization, an event-store precondition, an inline unique index, or an external unique reservation/claim table.

`EmailClaim` owns the invariant for one contended email key, not vague global uniqueness.

## 2. Short Answer

A process manager coordinates the email lifecycle. It listens to events, persists enough workflow state, survives across timeouts/retries/compensations, and emits commands for the next step. That matches the [EIP Process Manager](https://www.enterpriseintegrationpatterns.com/patterns/messaging/ProcessManager.html), Microsoft CQRS Journey's preference for "process manager" over overloaded "saga" language, and EventSourcingDB's distinction between sagas and process managers ([CQRS Journey](https://github.com/microsoftarchive/cqrs-journey/blob/master/docs/Reference_06_Sagas.markdown), [EventSourcingDB](https://docs.eventsourcingdb.io/blog/2026/04/20/sagas-vs-process-managers/)).

Uniqueness enforcement is different. Hard uniqueness must serialize all contenders for the same normalized key at the write-side acceptance point: one claim stream, one claim aggregate, one unique index, one event-store precondition, or one external unique reservation/claim table. Async projections/read models are advisory; only inline/synchronous projection updated in the same transaction and backed by a unique index participates in hard acceptance. Idempotency handles retries, not competing distinct claims.

Normalization is part of the domain policy. Scope and normalization policy version are part of the key. Provider-specific dot/plus rules are business choices, not universal email truth; [RFC 5321](https://datatracker.ietf.org/doc/html/rfc5321) preserves the local-part caveat even if most systems choose pragmatic case-folding.

## 3. Term Boundaries

| Term | Boundary | What It Can Do | What It Must Not Be Mistaken For |
|---|---|---|---|
| Process manager | Durable workflow coordinator | React to events, persist process state, emit commands, manage timeouts/retries/compensations | The uniqueness authority |
| Saga | Long-running transaction pattern with compensating actions | Coordinate multi-step work where failure requires compensating prior steps, as in the original [Saga paper](https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf) | A synonym for every coordinator or a uniqueness proof |
| Aggregate | Transactional consistency boundary | Enforce invariants inside one aggregate instance; Vernon's aggregate guidance pushes consistency into small boundaries ([Part I](https://www.dddcommunity.org/wp-content/uploads/files/pdf_articles/Vernon_2011_1.pdf), [Part II](https://www.dddcommunity.org/wp-content/uploads/files/pdf_articles/Vernon_2011_2.pdf)) | A scanner of all users |
| Domain service | Domain operation that does not naturally belong to one entity/value object | Express domain calculation/policy using already-available facts | A place to bypass write-side serialization |
| Application service / command handler | One request/use-case initiator | Load state, call domain behavior, append events, map infrastructure conflicts to domain conflicts | A process manager; it does not survive across events, timeouts, retries, and compensations |
| Projection / read model | Query-optimized derived state | Search, display availability hints, support monitoring | Hard acceptance gate when async/eventually consistent |
| Inline projection + unique index | Synchronous derived state in the same transaction | Participate in hard acceptance when updated inline and backed by a unique index, e.g. Marten [inline projections](https://martendb.io/events/projections/inline) plus [unique indexes](https://martendb.io/documents/indexing/unique) | A normal async projection |
| Unique index / event-store precondition / external reservation table | Write-side collision primitive | Serialize same-key contenders and reject the loser | Workflow orchestration |
| Idempotency key | Retry dedupe key | Make repeated delivery of the same command/event safe | Protection from two different users claiming the same email |

## 4. Precedent / Prior Art Labels

| Label | Source / Shape | Use In This Decision |
|---|---|---|
| EIP Process Manager | [Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/patterns/messaging/ProcessManager.html) | Workflow routing and sequence state |
| Saga / compensation | [Garcia-Molina and Salem](https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf) | Long-running process recovery |
| DDD Aggregate transactional consistency boundary | Vernon aggregate essays ([Part I](https://www.dddcommunity.org/wp-content/uploads/files/pdf_articles/Vernon_2011_1.pdf), [Part II](https://www.dddcommunity.org/wp-content/uploads/files/pdf_articles/Vernon_2011_2.pdf)) | Decide where invariant ownership lives |
| Reservation Pattern / per-key claim aggregate | Event-sourced email uniqueness guidance ([EventSourcingDB](https://docs.eventsourcingdb.io/blog/2026/04/30/email-uniqueness-in-event-sourcing/)) | Best default for mutable email |
| CQRS read model / materialized view | CQRS projection practice | Availability hints, not hard acceptance |
| Optimistic concurrency / expected revision / stream precondition | Kurrent append expectations and EventSourcingDB preconditions ([Kurrent](https://docs.kurrent.io/clients/node/v1.1/appending-events), [EventSourcingDB](https://docs.eventsourcingdb.io/fundamentals/preconditions/)) | Same-key stream creation or revision checks |
| Relational unique constraint | Database uniqueness primitive | Pragmatic write-side enforcement |
| Inline projection plus unique index | Marten inline projections and unique indexes | Transactional derived uniqueness |
| Axon set-based consistency validation | Axon validation discussions ([original](https://www.axoniq.io/blog/2020set-based-consistency-validation), [revisited](https://www.axoniq.io/blog/set-based-consistency-validation-revisited)) | Command-side lookup needs consistency backing |
| Per-value aggregate / actor | One actor/aggregate per contended value | Serialize only same-email contenders |
| Global uniqueness aggregate | One aggregate owns all emails | Correct but hot/unbounded; avoid as default |
| Idempotent Receiver / event-id dedupe | Messaging retry pattern | Retry safety only |

## 5. Write-Side Collision Contract

The write-side acceptance key is:

```text
EmailClaim/{scope}:{normalizationPolicyVersion}:{normalizedEmail}
```

Acceptance rule: a command may commit an active `reserved` or `assigned` claim only if the `EmailClaim` boundary for that exact key currently permits the transition. All contenders for the same key must collide on the same write primitive: same stream, same aggregate id, same unique index key, same event-store precondition, or same external unique reservation/claim table row.

A `User` stream append, process-manager state transition, or async projection result is not sufficient. They can record or coordinate the outcome, but they cannot be the proof that no other active claim exists for the same key.

## 6. Mutable Email Decision Model

| Policy Question | Options | Recommended Default |
|---|---|---|
| What is unique? | Global, tenant scoped, realm scoped, active-only, active-plus-pending | Scoped active-plus-pending key |
| What is identity? | Email, username, generated id | Stable `UserId`; email is mutable contact/credential claim |
| When is email claimed? | At request, after verification, after activation | Reserve before verification with TTL |
| How is normalized key built? | Lowercase domain only, full case-fold, provider aliases, custom policy | Versioned normalizer; conservative by default |
| Can email change? | Never, admin-only, self-service, recovery-only | Self-service with verification and old-address notification |
| When is old email released? | Immediate, cooldown, never, support-only | Cooldown/tombstone for consumer auth; shorter or immediate only when business accepts account-reuse risk |
| What about privacy? | Keep raw tombstones, HMAC tombstones, purge | Minimize retained personal data; define retention and erasure policy using ICO/GDPR guidance ([minimisation](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/data-minimisation/), [storage limitation](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/storage-limitation/), [Art. 17](https://gdpr-info.eu/art-17-gdpr/)) |
| How are existence leaks handled? | Explicit conflict, generic response, delayed notice | Generic external responses where auth enumeration matters, per [OWASP auth guidance](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) |

## 7. Technique Taxonomy

| Technique | Owner / Primitive | Mutable Fit | When To Use | Failure Mode |
|---|---|---|---|---|
| Email-as-user-stream id | `User/{normalizedEmail}` stream with no-stream append | Poor | Only if email is immutable identity | Email change becomes identity migration |
| Email claim stream | `EmailClaim/{scope}:{version}:{normalizedEmail}` with expected-empty append | Strong | Default event-sourced model | Orphan reservations need expiry/compensation |
| Per-value aggregate / actor | One aggregate/actor per normalized key | Strong | High contention must localize to one key | Hot keys serialize, but only per email |
| Inline projection + unique index | Same transaction projection document/table | Strong | Store supports atomic event+projection commit | Loser aborts append and must map to conflict |
| External unique reservation/claim table | External table with unique key | Good | Existing relational identity boundary | Dual-write divergence unless transaction/outbox is designed |
| Event-store query precondition | Transactional predicate at append | Mixed | Low-volume or store-supported predicates | Expensive global scans if misused |
| Async read-model validation | Eventually consistent projection | Weak | Availability hints and UX pre-checks | TOCTOU duplicate acceptance |
| Global uniqueness aggregate | One aggregate with all emails | Correct but poor | Tiny bounded systems | Hotspot, unbounded history, operational fragility |
| Idempotency key / event id | Command id or event id dedupe | Necessary but incomplete | Retries, at-least-once delivery, replay safety | Distinct competing commands still race |

## 8. Concrete Create Race

Scenario: U1 and U2 both attempt `alice@example.com`.

1. Availability projection is stale and says `alice@example.com` is available to both callers. This is acceptable only as advisory UX.
2. Both commands normalize using the same policy: `{scope}:{normalizationPolicyVersion}:alice@example.com`.
3. U1 attempts to create `EmailClaim/{scope}:{normalizationPolicyVersion}:alice@example.com` as `reserved`.
4. U2 attempts the same claim key.
5. The write-side primitive serializes the contenders. U1 wins; U2 receives a domain conflict such as `EmailAlreadyClaimed`.
6. The process manager for U1 sends verification and records timeout state.
7. If U1 verifies before expiry, the claim becomes `assigned` and the user creation completes or is confirmed.
8. If U1 does not verify before expiry, the process manager emits `ExpireEmailClaim`; the claim transitions to `expired` or `released`, after which U2 may retry and compete against the current claim state.

The decisive point is step 3-5, not the projection lookup and not the process-manager transition.

## 9. Concrete Change-Email Race

Scenario: U1 owns `a@example.com`; U1 and U2 contend for `b@example.com`.

1. U1 requests change from `a@example.com` to `b@example.com`; U2 requests create/change to `b@example.com`.
2. Both requests normalize to the same `EmailClaim/{scope}:{normalizationPolicyVersion}:b@example.com`.
3. The winner reserves the proposed claim. Suppose U1 wins.
4. U2's command receives `EmailAlreadyClaimed` or a retryable conflict, depending on whether the reservation is pending, assigned, or expired.
5. The process manager for U1 sends verification to `b@example.com` and may notify `a@example.com`, following account-change safety guidance from [OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html).
6. When verification arrives, the process manager commands `ApplyEmailChange(userId=U1, expectedRevision=...)`.
7. If U1's user stream expected revision conflicts, the process manager reloads and decides whether to retry, reject, or compensate the proposed `b@example.com` claim.
8. If the user change succeeds but assigning the new claim fails, that is a serious split-brain candidate and must be compensated or repaired before acceptance is externally visible.
9. Old-email policy then runs: release `a@example.com`, cool it down, tombstone it, or route to support-only reuse. Release failure does not invalidate the new email assignment unless the domain explicitly requires atomic swap; it creates a cleanup/support obligation.

## 10. Old Email Release Semantics

| Policy | Meaning | Use When | Release Failure Effect |
|---|---|---|---|
| Immediate release | Old claim becomes available as soon as new email is assigned | Low-risk domains, admin-managed accounts, internal systems | Blocks reuse until retried; should not roll back new assignment unless atomic swap is required |
| Cooldown / tombstone | Old email cannot be reused until retention window expires | Consumer auth, account takeover risk, mistaken changes | Leaves old key unavailable; process manager retries or support resolves |
| Permanent tombstone | Old email is never reusable in the scope | High-risk identity domains | Failure is operationally serious because reuse policy depends on durable tombstone |
| Support-only | Old email reuse requires manual review | Fraud-prone or regulated contexts | Failure opens a support queue; automated reuse remains blocked |

## 11. Failure / Compensation

| Failure | Required Handling |
|---|---|
| Reservation succeeds; verification never arrives | Process manager expires reservation after TTL; claim transitions to `expired`/`released`/`tombstoned` per policy |
| Reservation succeeds; user append conflicts | Reload user; retry if still valid; otherwise compensate/release proposed claim |
| User append succeeds; new-claim assignment fails | Treat as split acceptance risk; block external success, retry assignment, or run repair that restores invariant |
| Old release fails | Keep old claim unavailable; retry cleanup; route to support if retention/reuse SLA is breached |
| Projection lags | Do not use it for hard acceptance; show advisory state and reconcile monitoring |
| Duplicate command retry | Idempotency key returns prior result or safely no-ops; it does not let a distinct claimant through |
| External table / event store dual-write divergence | Use same transaction where possible; otherwise outbox/repair process plus invariant audit over claims |

## 12. Falsifiable Invariant

At no committed acceptance point may two active assigned claims exist for the same `{scope}:{normalizationPolicyVersion}:{normalizedEmail}`.

## 13. Implementation Sketch

Commands:

```text
RequestUserRegistration(userId, rawEmail, scope, normalizationPolicyVersion, idempotencyKey)
ReserveEmailClaim(claimKey, claimantUserId, purpose, expiresAt, idempotencyKey)
SendEmailVerification(claimKey, verificationToken)
VerifyEmailClaim(claimKey, token, verifiedAt)
AssignEmailClaim(claimKey, userId, expectedClaimRevision)
CreateUserWithAssignedEmail(userId, claimKey, expectedUserRevision)
RequestEmailChange(userId, newRawEmail, scope, normalizationPolicyVersion, idempotencyKey)
ApplyEmailChange(userId, oldClaimKey, newClaimKey, expectedUserRevision)
ReleaseEmailClaim(claimKey, reason)
ExpireEmailClaim(claimKey, now)
TombstoneEmailClaim(claimKey, retentionReason, until)
CompensateEmailClaim(claimKey, reason)
```

Events:

```text
EmailClaimReservationRequested
EmailClaimReserved
EmailVerificationSent
EmailClaimVerified
EmailClaimAssigned
EmailClaimReservationExpired
EmailClaimReleased
EmailClaimTombstoned
EmailClaimCompensated
UserRegistrationRequested
UserCreated
UserEmailChangeRequested
UserEmailChanged
OldEmailReleaseRequested
OldEmailReleaseFailed
EmailChangeProcessTimedOut
EmailChangeProcessCompensated
```

Default flow:

1. Application service receives command and normalizes email.
2. It reserves `EmailClaim/{scope}:{normalizationPolicyVersion}:{normalizedEmail}` using same-key serialization.
3. Process manager observes `EmailClaimReserved`, sends verification, tracks timeout.
4. Verification commands assignment and user create/change with expected revisions.
5. Process manager releases, cools down, or tombstones the old claim according to policy.
6. Projections update user-facing views after the fact; inline unique projections may participate only if they are inside the same transaction.

## 14. Source Notes And Uncertainties

The explorer evidence converges on a clean separation: process managers coordinate message flow; aggregates/claims/constraints own consistency. CQRS Journey explicitly narrows process-manager responsibility to coordination, while the Saga paper supplies the compensation lineage. Vernon's aggregate essays do not discuss email uniqueness directly, but they strongly imply that cross-user uniqueness cannot be hidden inside a normal `User` aggregate. EventSourcingDB's email article is the closest direct precedent for separating stable user identity from mutable email reservations.

Uncertainties remain implementation-specific:

- Some event stores now support stronger multi-stream or query preconditions than older designs. That changes mechanics, not the invariant owner.
- Provider-specific email normalization is policy, not protocol truth.
- Privacy treatment of old-email tombstones depends on jurisdiction, retention purpose, and reversibility/linkability.
- Enumeration-safe UX may require generic responses even when the command internally knows the precise conflict.

## 15. Agents Spawned / Closeout Note

This document is writer-authored by `Shannon, Claude` from 4 explorers, synthesizer, 3 reviewers with robot-talk convergence; auditor pending.
