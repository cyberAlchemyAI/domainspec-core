# Explorer Transcript: DDD Process Managers And Event-Sourced Uniqueness

Dispatch: `2026-06-30-ddd-process-manager-uniqueness`

## Agent 1: Hewitt, Carl

**Explorer: Hewitt, Carl**

**Findings**
- CQRS Journey deliberately prefers **Process Manager** over **Saga** for CQRS orchestration because the 1987 Saga paper already defined saga as a long-lived transaction decomposed into subtransactions with compensations. Microsoft’s guidance says common CQRS “saga” usage meant message coordination, so “process manager” was clearer. ([github.com](https://github.com/microsoftarchive/cqrs-journey/blob/master/docs/Reference_06_Sagas.markdown)) ([cs.cornell.edu](https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf))
- The core flow is: a process manager listens to events, keeps enough process state/correlation to know where the workflow is, and emits commands for the next step. EIP frames it as a central unit that maintains sequence state and chooses next processing steps from intermediate results. CQRS Journey’s order/reservation/payment example shows aggregates reporting facts while the PM mediates the next commands. ([enterpriseintegrationpatterns.com](https://www.enterpriseintegrationpatterns.com/patterns/messaging/ProcessManager.html)) ([github.com](https://github.com/microsoftarchive/cqrs-journey/blob/master/docs/Reference_06_Sagas.markdown))
- Historically, this sits in the Greg Young/CQRS/Event Sourcing lineage: Greg is publicly credited with coining CQRS, and by 2016-2017 process managers had become enough of a CQRS/ES concern that he had a dedicated “Event Sourced Process Managers” workshop. The public materials prove the topic’s place in the lineage, but not a single canonical Greg-authored definition. ([virtualddd.com](https://virtualddd.com/videos/greg-young-a-decade-of-ddd-cqrs-event-sourcing/)) ([2017.dddeurope.com](https://2017.dddeurope.com/speakers/greg-young/))
- It differs from an **aggregate** because aggregates own command handling and consistency/business invariants inside a boundary; PMs localize workflow routing so aggregates do not need to know the whole next-step choreography. CQRS Journey is strict that business logic belongs in aggregates, though community threads show uncertainty over whether “choose the next command” is itself business logic. ([github.com](https://github.com/microsoftarchive/cqrs-journey/blob/master/docs/Reference_06_Sagas.markdown)) ([groups.google.com](https://groups.google.com/g/dddcqrs/c/OnkyzZZ5CUU))
- It differs from a **projection/read model** because projections build query-optimized state and are eventually consistent; a PM is an active coordinator that reacts to events and sends commands. Greg’s group reply on projections points to checkpoint/catch-up mechanics, while Azure’s CQRS guidance says read models avoid domain logic/validation and can lag. ([groups.google.com](https://groups.google.com/g/dddcqrs/c/QiwE3nJoyn4)) ([learn.microsoft.com](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs))
- It differs from a **database constraint** because a PM encodes temporal process flow, retries, compensations, waits, and message correlation. The original Saga paper is about avoiding long locks for long-lived transactions, not replacing every invariant; it also distinguishes application-level process constraints from database constraints. ([cs.cornell.edu](https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf))
- Implementation practice is not one fixed shape. A PM may be persisted, event-sourced, actor-like, or reconstructed by correlation. Greg’s 2015 group comments suggest deterministic IDs plus event-store idempotency can help with duplicate handling, but he explicitly frames that as one option, not universal doctrine. ([groups.google.com](https://groups.google.com/g/dddcqrs/c/fENSgemiTNE))

**Implications For Mutable Email Uniqueness**
- Do **not** make a process manager the sole authority for “no two active users have this normalized email.” If the uniqueness rule must be immediate, put it in a write-side consistency boundary: a unique DB constraint, a deterministic `email-{normalizedHash}` stream, or an `EmailClaim/EmailAddress` aggregate keyed by normalized email.
- A PM is useful for the **workflow** around mutable email: request change, reserve email, send verification, expire reservation, confirm, update user, release old email, compensate on failure.
- A projection can help users search/check availability, but it is stale by construction, so it should not be the acceptance gate.
- Best fit: immutable `userId` as identity; mutable email as a claimed address with states like `available/reserved/verified/assigned/released`. PM coordinates transitions; the uniqueness owner/constraint rejects races.

**Sources**
- Microsoft CQRS Journey, “A Saga on Sagas”: https://github.com/microsoftarchive/cqrs-journey/blob/master/docs/Reference_06_Sagas.markdown
- EIP Process Manager: https://www.enterpriseintegrationpatterns.com/patterns/messaging/ProcessManager.html
- Garcia-Molina & Salem, “Sagas”: https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf
- DDD/CQRS Google Groups process-manager threads: https://groups.google.com/g/dddcqrs/c/QiwE3nJoyn4 and https://groups.google.com/g/dddcqrs/c/fENSgemiTNE
- Greg Young DDD/CQRS/Event Sourcing context: https://virtualddd.com/videos/greg-young-a-decade-of-ddd-cqrs-event-sourcing/ and https://2017.dddeurope.com/speakers/greg-young/
- Microsoft CQRS pattern/read-model guidance: https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs

## Agent 2: Simon, Herbert

**Research Dispatch: Simon, Herbert**

**Findings**
- Vernon’s aggregate rule is strict: an aggregate is a transactional consistency boundary, and the normal goal is one aggregate instance modified per transaction. So email uniqueness across many users is not naturally a `User` aggregate invariant unless all users are one aggregate, which is the wrong shape at scale. ([dddcommunity.org](https://www.dddcommunity.org/wp-content/uploads/files/pdf_articles/Vernon_2011_1.pdf))

- The Vernon rule set pushes toward small aggregates, references by identity, and explicit cross-aggregate coordination. Holding other aggregate objects or querying around from inside an aggregate is discouraged; application services may resolve references, but that still does not grant permission to mutate multiple aggregates together. ([dddcommunity.org](https://www.dddcommunity.org/wp-content/uploads/files/pdf_articles/Vernon_2011_2.pdf))

- Cross-aggregate rules are normally eventual. Vernon quotes the Evans aggregate guidance that rules spanning aggregates are not expected to be current at all times, and recommends domain events/subscribers, each updating one aggregate in its own transaction, with retry/compensation/intervention on failure. ([dddcommunity.org](https://www.dddcommunity.org/wp-content/uploads/files/pdf_articles/Vernon_2011_2.pdf))

- The key modeling question is “whose job is it?” If the user changing/registering email must know immediately whether the email is available, that leans transactional. If the system can reconcile later, it can be eventual. Vernon treats this as a domain question, not a CQRS/technical preference. ([dddcommunity.org](https://www.dddcommunity.org/wp-content/uploads/files/pdf_articles/Vernon_2011_2.pdf))

- Bounded context matters. Vernon’s 2026 KurrentDB/IDDD article uses Identity and Access as its own bounded context because auth has distinct language and integration events; email uniqueness should probably live in the Identity/Access context, not leak as a global invariant into Collaboration/Profile/Notification contexts unless those contexts explicitly share that rule. ([kurrent.io](https://www.kurrent.io/blog/implementing-ddd-with-kurrentdb/))

- A process manager is coordination state, not the aggregate that owns the uniqueness invariant. EventSourcingDB’s process-manager guidance describes a stateful component that reacts to events and dispatches commands; it is useful for “reserve new email, update user, release old email, timeout/compensate” workflows, but the lock/reservation aggregate or index must still be the authority for uniqueness. ([docs.eventsourcingdb.io](https://docs.eventsourcingdb.io/blog/2026/04/20/sagas-vs-process-managers/))

- In event sourcing, stream-level optimistic concurrency protects one stream/subject well, but global uniqueness is not free. KurrentDB supports expected stream state/revision checks such as `noStream()` and exact stream revision, which can enforce “only one reservation stream for this normalized email,” but it does not magically make every `User-*` stream globally unique by email. ([docs.kurrent.io](https://docs.kurrent.io/clients/java/v1.1/appending-events))

- For mutable email, the strongest fit is a separate normalized-email reservation/claim boundary: stable `UserId` remains the user identity; normalized email has its own reservation stream/aggregate or external unique index; email-change workflow reserves the new email before applying `UserEmailChanged`, then releases the old one. EventSourcingDB’s email-uniqueness article reaches the same practical trade-off: email-as-stream-id works until email changes; reservation separates identity from locking but adds workflow complexity. ([docs.eventsourcingdb.io](https://docs.eventsourcingdb.io/blog/2026/04/30/email-uniqueness-in-event-sourcing/))

**Direct Implications**
Mutable email uniqueness should not be enforced by a `User` aggregate scanning other users. Model it either as an `EmailReservation`/`EmailClaim` aggregate keyed by normalized email, or as an explicitly accepted external unique index. Use a process manager only to orchestrate mutation: reserve new, command user change, release old, expire abandoned reservations, compensate failed transitions. If product accepts temporary duplicates, use event-driven reconciliation, but call that out as a deliberate business trade-off because users may observe a duplicate-valid window.

**Uncertainty**
I did not find Vernon prescribing “mutable email uniqueness” specifically; that conclusion is an inference from his aggregate rules plus event-sourcing uniqueness guidance. KurrentDB 25.1+ also has atomic multi-stream append, which may change implementation options, but not the DDD modeling question of which boundary owns the invariant.

**Source List**
Kalele Effective Aggregate Design index; Vernon Effective Aggregate Design Parts I-III; Vernon’s KurrentDB IDDD/Event Sourcing article; KurrentDB append/concurrency docs; EventSourcingDB email uniqueness and saga/process-manager articles.

## Agent 3: Turing, Alan

**Explorer Result**
Agent: `Turing, Alan`. Core finding: event-sourced uniqueness is not one mechanism; it is a choice of where to serialize, where to index, and what failure mode the business can tolerate.

| Technique Candidate | Enforcement Primitive | Mutable Email Fit | Race Implication |
|---|---|---|---|
| Email-as-stream / subject lock | Encode normalized email in stream/subject, append with `NO_STREAM` / `no_stream` or `isSubjectPristine`. Kurrent documents `no_stream`; EventSourcingDB subjects identify streams and has pristine preconditions. ([docs.kurrent.io](https://docs.kurrent.io/clients/node/v1.1/appending-events)) ([docs.eventsourcingdb.io](https://docs.eventsourcingdb.io/fundamentals/subjects/)) ([docs.eventsourcingdb.io](https://docs.eventsourcingdb.io/fundamentals/preconditions/)) | Weak if email is also user identity; better only as separate lock stream. | Two commands for same email collide on same stream; one wins, one gets conflict. |
| Reservation stream / claim aggregate | Create `/email-reservations/{email}` first, then user stream. EventSourcingDB’s email article calls this the clean separation pattern. ([docs.eventsourcingdb.io](https://docs.eventsourcingdb.io/blog/2026/04/30/email-uniqueness-in-event-sourcing/)) | Strong candidate for mutable email: reserve new email, change user, release old email. | One reservation wins. Split workflows need TTL, release, and compensation; atomic multi-stream append helps where supported. |
| Inline projection + unique index | Project current email into a document/table inline, with a DB unique index. Marten inline projections run during `SaveChanges` in the same DB transaction; Marten supports unique indexes. ([martendb.io](https://martendb.io/events/projections/inline)) ([martendb.io](https://martendb.io/documents/indexing/unique)) | Very good for “current email must be unique,” including changes. | Concurrent writes race at the DB index; loser aborts the whole append transaction and should be mapped to domain conflict. |
| Command-side lookup/read model | Axon pattern: command-side lookup table updated by subscribing processor, then checked by dispatcher/handler/parameter resolver. ([axoniq.io](https://www.axoniq.io/blog/2020set-based-consistency-validation)) ([github.com](https://github.com/AxonIQ/code-samples/blob/main/set-based-validation/README.md)) | Usable, but only if command-owned and immediately consistent. | Check-before-write alone has TOCTOU risk; central table needs unique constraint. Axon later notes distributed transaction concerns when event store and projection are separate. ([axoniq.io](https://www.axoniq.io/blog/set-based-consistency-validation-revisited)) |
| Per-value aggregate / actor | One aggregate/entity per unique value, e.g. `EmailUniquenessCheck(email)`, then create user in same command transaction. ([axoniq.io](https://www.axoniq.io/blog/set-based-consistency-validation-revisited)) | Good for mutable email if claim/release semantics are explicit. | Serializes only contenders for same email, avoiding global aggregate hotspot. |
| Global uniqueness aggregate | One aggregate owns all emails. EventSourcingDB article lists it as clean but unbounded. ([docs.eventsourcingdb.io](https://docs.eventsourcingdb.io/blog/2026/04/30/email-uniqueness-in-event-sourcing/)) | Technically supports mutation, operationally poor at scale. | All registration/change commands serialize through one stream; safe but hot and ever-growing. |
| Query precondition on write | EventSourcingDB `isEventQlQueryTrue` can express uniqueness as a transactional write precondition. ([docs.eventsourcingdb.io](https://docs.eventsourcingdb.io/fundamentals/preconditions/)) | Avoid for hot registration paths. | Correct under store serialization, but global scans grow with history; EventSourcingDB article warns this is the wrong place for global invariants. ([docs.eventsourcingdb.io](https://docs.eventsourcingdb.io/blog/2026/04/30/email-uniqueness-in-event-sourcing/)) |
| External unique lock table | Insert normalized email into SQL table with `UNIQUE`, then append event. ([docs.eventsourcingdb.io](https://docs.eventsourcingdb.io/blog/2026/04/30/email-uniqueness-in-event-sourcing/)) | Pragmatic if SQL is already part of identity boundary. | DB race is solved, but event-store write and SQL insert are not one transaction unless same store/unit of work. Lock leaks and orphan events are the danger. |
| Idempotency key / event id | Kurrent/EventStoreDB uses event id plus stream for idempotence; with expected version it can acknowledge duplicate retries without duplicate append. ([docs.kurrent.io](https://docs.kurrent.io/clients/tcp/dotnet/21.2/appending)) | Necessary but not sufficient. | Protects retry of the same command/event, not two different commands claiming same email. Axon also treats idempotent handlers as required for at-least-once/replay edge cases. ([docs.axoniq.io](https://docs.axoniq.io/axon-framework-reference/4.12/events/event-processors/streaming/)) |

**Race Notes**
The strongest primitive is “make the contended value the key”: stream name, subject, aggregate id, or unique index key. `expectedRevision/no_stream` and `isSubjectPristine` only enforce uniqueness if every contender maps to the same stream/subject.

For mutable email, avoid making email the user stream identity. Use user-id streams plus either reservation streams/per-email aggregates or an inline current-email projection with a unique index.

Async read models are not safe validators for uniqueness. EventSourcingDB explicitly frames read-model lag as expected; critical validation needs write-side checks or synchronous validation. ([docs.eventsourcingdb.io](https://docs.eventsourcingdb.io/best-practices/read-model-consistency-and-lag/))

KurrentDB now documents atomic multi-stream append in 25.1+, while older TCP transactions are single-stream only; design the reservation/user update boundary according to the deployed capability. ([docs.kurrent.io](https://docs.kurrent.io/clients/node/v1.1/appending-events)) ([docs.kurrent.io](https://docs.kurrent.io/clients/tcp/dotnet/21.2/appending))

**Source List**
EventSourcingDB email uniqueness article; EventSourcingDB preconditions, subjects, consistency, read-model lag; Kurrent/EventStoreDB append and idempotence docs; Marten appending, inline projections, unique indexes, natural keys; AxonIQ set-based validation, revised per-value aggregate approach, subscribing/streaming processor docs. ([docs.eventsourcingdb.io](https://docs.eventsourcingdb.io/blog/2026/04/30/email-uniqueness-in-event-sourcing/)) ([docs.eventsourcingdb.io](https://docs.eventsourcingdb.io/fundamentals/preconditions/)) ([docs.eventsourcingdb.io](https://docs.eventsourcingdb.io/about-eventsourcingdb/consistency-guarantees/)) ([docs.kurrent.io](https://docs.kurrent.io/clients/tcp/dotnet/21.2/appending)) ([martendb.io](https://martendb.io/events/appending)) ([martendb.io](https://martendb.io/events/natural-keys)) ([docs.axoniq.io](https://docs.axoniq.io/axon-framework-reference/4.12/events/event-processors/subscribing/))

## Agent 4: Meadows, Donella H.

**Explorer: Meadows, Donella H.**

**Findings**

- Email uniqueness is a time-based business rule, not a storage keyword. EventSourcingDB’s email uniqueness article is right to reframe the question as “what does unique mean here?” because event sourcing stores history, while uniqueness asks about derived current state and timing. ([docs.eventsourcingdb.io](https://docs.eventsourcingdb.io/blog/2026/04/30/email-uniqueness-in-event-sourcing/))

- If email can ever change, do not make email the account identity. Email-as-subject/stream gives strong uniqueness for creation, but breaks when the business later needs change, release, account recovery, or privacy-preserving deletion. Keep `UserId` stable; make email a claim/reservation with its own lifecycle. ([docs.eventsourcingdb.io](https://docs.eventsourcingdb.io/blog/2026/04/30/email-uniqueness-in-event-sourcing/))

- Email change is a process, not just a field update. OWASP recommends pending change state, time-limited nonces, current-address notification, proposed-address confirmation, and stronger checks when MFA is absent. That maps naturally to a process manager: stateful workflow, correlation, timeouts, and failure handling. ([cheatsheetseries.owasp.org](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)) ([docs.particular.net](https://docs.particular.net/architecture/workflows))

- Releasing an old email is the hard policy edge. Options: immediate release, release after cooldown, release only after new email verification, release only by support, or permanent tombstone. Each implies different user safety, reuse, abuse, and GDPR retention consequences.

- Tombstones are personal data risk, even when hashed, if they remain linkable or testable. GDPR-style minimisation/storage-limitation requires a purpose, retention period, and erasure/anonymisation plan; pseudonymisation usually does not remove the retention obligation. ([ico.org.uk](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/data-minimisation/)) ([ico.org.uk](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/storage-limitation/)) ([gdpr-info.eu](https://gdpr-info.eu/art-17-gdpr/))

- Normalization must be explicit and versioned. Domain case-folding is safe, but RFC 5321 says mailbox local-parts are technically case-sensitive, even though exploiting that hurts interoperability. Provider-specific dot/plus alias rules should not be universal unless the business accepts false collisions. ([datatracker.ietf.org](https://datatracker.ietf.org/doc/html/rfc5321))

- “Write first, reconcile later” is operationally viable only if the business accepts a duplicate-validity window and has deterministic compensation, monitoring, and user messaging. EventSourcingDB calls out the bad UX when two accounts appear valid until reconciliation catches up. ([docs.eventsourcingdb.io](https://docs.eventsourcingdb.io/blog/2026/04/30/email-uniqueness-in-event-sourcing/))

**Policy Decision Table**

| Policy Question | Practical Choices | Implementation Consequence |
|---|---|---|
| What is unique? | Global email, per tenant, per realm, only active users, active plus pending claims | Defines uniqueness key: `tenantId + normalizedEmail`, not just email |
| Can email change? | Never, admin-only, self-service, recovery-only | If mutable, separate `User` stream from `EmailClaim`/reservation stream |
| When is email claimed? | On registration start, after verification, after account activation | Earlier claim prevents races but creates abandoned reservations and expiry work |
| Verification window? | 15 min, 24h, 7d, manual extension | Needs `EmailReservationExpiresAt`, timeout events, retry/renew rules |
| Must old email confirm? | Always, only without MFA, never, support fallback | Adds process-manager branches and lockout/account-takeover tradeoffs |
| When release old email? | Immediately after change, after cooldown, never, support-only | Requires `OldEmailReleased` or `EmailTombstoned`; affects reuse and privacy |
| What is retained? | Raw email, normalized key, HMAC key, salted tombstone, nothing | Raw is easiest but privacy-worst; HMAC/tombstone still needs retention basis |
| How handle duplicate found later? | Earliest event wins, verified wins, paid account wins, support queue | Must encode deterministic compensation and notify affected users |

**Direct DDD/Event Sourcing Implications**

Model email as a lifecycle aggregate or claim, not a property uniqueness check hidden inside `User`. Useful events: `EmailReservationRequested`, `EmailReserved`, `EmailReservationExpired`, `EmailVerificationSent`, `EmailVerified`, `UserEmailChangeRequested`, `CurrentEmailNotified`, `UserEmailChanged`, `OldEmailReleased`, `EmailTombstoned`, `EmailClaimCompensated`.

Use a process manager for multi-step registration/change flows: listen to reservation, verification, timeout, support, and failure events; emit commands like `SendVerificationEmail`, `ExpireReservation`, `ReleaseEmail`, `ApplyEmailChange`, `NotifyOldAddress`.

Keep normalization versioned: store raw display email separately from `normalizedEmailKey` and `normalizationPolicyVersion`. A future normalization change is a migration/reclaim workflow, not a silent replay surprise.

Treat read models as advisory unless updated inline/transactionally. If uniqueness must be hard, enforce at append/precondition, reservation stream, or unique index boundary. If using an external SQL unique index, design for dual-write compensation because the event store and lock table can diverge. ([docs.eventsourcingdb.io](https://docs.eventsourcingdb.io/blog/2026/04/30/email-uniqueness-in-event-sourcing/)) ([martendb.io](https://martendb.io/events/learning))

Operational checks should include stuck reservations, expired-but-not-released emails, duplicate active claims, projection lag, replay under old normalizer versions, support overrides, and user-enumeration leaks. OWASP’s generic response guidance matters because uniqueness errors can reveal whether an email is already registered. ([cheatsheetseries.owasp.org](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html))
