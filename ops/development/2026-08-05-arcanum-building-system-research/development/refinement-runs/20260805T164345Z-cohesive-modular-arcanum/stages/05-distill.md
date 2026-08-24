# Distill — Architecture Tournament

## Target context

An existing public Arcanum capability ecosystem whose local contracts are substantial but whose cross-owner building path is difficult to understand, partially duplicated, and not proven end to end.

## Objective and output artifact

Select the smallest architectural unit that creates system-wide cohesion without centralizing capability authority. Output: a design frame for Invoke Design.

## Mode and budget

- Mode: tournament within a deep Refine run
- Proposal tracks: 5 after the independent critic added a hybrid and a lower-risk migration alternative
- Recursive rounds: 3/3
- Role path: parent-labeled Proposer/Balancer passes plus an approved independent critic receipt to be joined later

## Track comparison

| Criterion | A: owner-preserving contract kernel | B: hierarchical build coordinator | C: event/ledger-centered composition |
|---|---|---|---|
| Authority safety | strongest: effect owners remain explicit | weakest: coordinator tends to absorb selection and lifecycle decisions | safe only if ledger is non-authoritative |
| Cohesion | strong through stable transition grammar | superficially strongest through one API | strong for traceability, weaker for semantic contracts |
| Migration | additive adapters and conformance fixtures | flag-day risk and duplicated transition logic | medium; requires event/state schema migration |
| Compatibility | old routes can become stateless facades | old owners become subroutines | old state must be replayed or bridged |
| Replay/freshness | explicit per-transition binding | centralized but high blast radius | strong append-only history, difficult currentness rules |
| Diagnosability | owner plus gate plus receipt visible | easy top-level trace, harder authority attribution | good history, risk of treating history as truth |
| Positive-witness proofability | compositional trace across exact owner receipts | one runner trace may hide owner proof | event trace is strong but still needs owner receipts |

### Pareto result

The original Track A is not accepted alone. Two critic-added tracks were admitted:

- **D — A plus non-authoritative causal journal:** owner-native receipts remain authoritative; an append-only journal records attempts, causal links, joins, crashes, reconciliation, and residue for diagnostics only.
- **E — bilateral-adapter-first migration:** implement no universal kernel initially; build versioned adapters and the witness harness around one real boundary, then extract only demonstrated common fields.

Track D is selected as the target architecture because it adds durable causal visibility without giving the journal semantic authority. Track E is selected as the migration strategy and first proof slice because it avoids a flag-day universal schema. B is rejected as the target because its central state machine risks owner collapse. C is rejected as semantic authority but incorporated as D's evidence sidecar. A remains the minimal protocol component inside D, repaired below.

## Smallest coherent unit

**Owner-Bound Transition Contract (OBTC): one versioned envelope plus a pure structural validator for one owner-to-owner handoff.**

Owned responsibility: decide only whether a declared handoff is structurally well-formed and evidence references are present. The consumer/effect owner separately decides semantic admissibility and issues its own policy, selection, admission, lifecycle, or release receipt.

Minimum fields:

- protocol and transition version;
- transition ID and attempt/run correlation;
- source and target state kinds;
- producer, effect owner, validator, router, consumer, and evidence-store roles;
- input artifact/receipt identities and digests;
- precondition gates and first-stop behavior;
- output receipt schema and authority effect;
- freshness, replay, retry, and idempotency binding;
- owner-declared next-transition hint and consumer route, treated as data rather than kernel policy;
- residue and reroute.

The protocol schema steward has `authority_effect:none`. Every semantic owner independently declares which protocol versions it accepts. A kernel version change cannot alter owner policy or become current for a consumer without that owner's compatibility declaration.

## Closure and recomposition proof

The OBTC closes because one pure validator can accept or reject one transition from its complete record. Splitting field definitions from validation would leave neither unit useful. Adding routing, owner execution, ledger writes, or lifecycle decisions would add independent behavior and violate the selected boundary.

It recomposes upward as:

`owner artifact -> OBTC validation -> owner operation -> owner receipt -> next OBTC validation`

Owner-specific adapters map Invoke, WPRA, Task Session, Continuation Router, Refresh, lifecycle, Craft references, generated parity, and registry boundaries into the shared envelope without changing their payload authority. The causal journal stores hashes, handles, and causal status, never a replacement verdict.

The model explicitly splits `AuthoredWorkPack` (Invoke Plan) from `FrozenWorkPackSnapshot` (WPRA). Closeout splits into `ExecutionTerminalReceipt` (Task Session), `CloseoutMutationReceipt` (Refresh), `OwnerJoinReceipt` (Continuation Router), `SynchronizedResultReceipt` (Task Session), and `ContinuityCursor` (Task Session under the current contract). The series owner consumes the cursor and advances its own frontier; it does not produce the Task Session cursor.

## Series-owner recommendation

Evidence favors **Implementation Readiness as the sole runtime owner of ordered frontier, visited set, action correlation, retry, join, and stop state**, because its current reducer already owns those transitions and launches owner/Task Session routes. `task-session-until-blocker` should become a compatibility spell/profile for `mode=until-real-blocker`, delegating to Implementation Readiness and retaining no independent chain ledger or reducer.

This is a design recommendation, not an applied lifecycle decision. `DECISION-LOOP-OWNER-001` remains a Decision Gate before implementation because changing or retiring the spell's state ownership belongs to Spellcraft/current owners.

## Proposer/Balancer trace

| Proposer claim | Balancer category and objection | Reconciliation |
|---|---|---|
| OBTC is universal. | requisite variety: owner payloads differ materially | Start with bilateral adapters; extract a minimal envelope and typed owner extensions only from demonstrated repetition. |
| One series owner reduces confusion. | migration risk: current spell consumers may depend on chain files | Preserve a stateless compatibility facade and explicit migration fixtures. |
| Craft can store protocol state. | authority collapse: local ledger would become operational truth | Store references and residue only; runtime owner keeps live series state. |
| One positive fixture proves recomposition. | non-vacuity: fixture can skip real Refresh behavior | Require synthetic conformance now and a later real owner-chain witness. |
| Registry can be another OBTC transition. | missing owner: a schema slot is not a binding | Keep registry transition blocked until an owner receipt is named. |
| Single-use admission prevents duplicate effects. | crash/replay: effect may occur before receipt durability | Add `outcome_unknown`, owner-led reconciliation, idempotency keys, and no automatic retry of indeterminate effects. |
| Digest checks prevent conflicts. | concurrency: two attempts can pass the same preflight | Require atomic baseline/lease comparison at the effect boundary and bind concurrency scope. |

## Technique trace

- abstraction-level guard: selected protocol contract, not organization-wide platform
- recomposition proof: pass
- evolution profile: owner adapters and versioned transitions are the smallest justified extension boundary
- boundary-object check: pass only with owner-specific payloads
- premortem: failure is most likely if ABP becomes another mutable state store
- cycle guard: stopped after the third round; further naming did not improve closure
- set-based tournament: A selected, C partially incorporated, B rejected

## Tension ledger

- Resolved: cohesion comes from contract conformance, not central effect ownership.
- Resolved: Craft and event logs are state/evidence sidecars.
- Resolved: kernel validation is structural only; semantic admission stays with the consumer/effect owner.
- Resolved: bilateral adapters and witness harness precede any universal-schema cutover.
- Routed: series owner requires Decision Gate/lifecycle acceptance.
- Open: material producer and registry owner bindings.
- Open: canonical repairs and real E2E proof.

## Frame-expiry note

Re-run the tournament if a canonical owner is introduced for material production or registry release, if Implementation Readiness no longer owns the outer loop, or if a real E2E witness contradicts the assumed transition order.

## Distill Result

- Verdict: pass for Design; implementation handoff remains gated
- Current smallest coherent unit: one bilateral OBTC adapter pair, pure validator, causal-event projection, and fixture for a single owner boundary
- Optimization point: one handoff is the smallest unit that remains semantically meaningful and independently testable
- Deferred complexity: central scheduler, authoritative global event store, automatic compensation, registry integration, universal cutover
- Evidence emission: not configured; stage artifact and later Refine receipts are the evidence surface
- Telemetry: not configured; no authority effect
- Next route: Invoke Design
