# State synthesis — revision 2

Status: evidence-bounded synthesis ready for the final reviewer gate. This revision preserves revision 1 and closes only the round-2 defects recorded in `review-round-2.md`.

## Typed reasoning-entry boundary

`ReasoningEntryVerdict` governs exactly one proposed reasoning invocation before command mapping, actor-cut materialization, ACI admission, observation admission, evaluator execution, or artifact admission.

- Owner: a separately conformed reasoning-entry owner, external and currently unselected. Ownership is not inherited by RWO, Dispatch confirmation, route eligibility, ACI, the semantic evaluator, artifact admission, or the exact-effect owner.
- Frozen inputs: exact confirmed Dispatch reference/digest; bound-seat identity; proposed ACI lifecycle-command identity/digest precommitted in the frozen run envelope; command/envelope/schema/version identities; freshness context and evidence-cut digest.
- Output: a persisted `pass | block` receipt binding verdict and owner identity/version, subject digest, evidence-cut digest, freshness basis, and input-schema identities.
- Pass: permits only command mapping and proposal to ACI. It does not map or accept the command and authorizes no actor, evaluation, artifact, route, or effect.
- Block: terminates the subject at this boundary. Only the valid owner's block receipt may be persisted.
- Fail closed: missing/unconformed owner; missing or non-pass receipt; stale context; subject, Dispatch, seat, command, evidence-cut, schema, or version mismatch; unknown schema/version; cross-run receipt substitution.
- Zero calls on every non-pass/missing/mismatched case: mapper, ACI admission, actor, actor-cut materializer, observation admitter, evaluator, artifact admission, exact-effect, effect-intent, and external-effect attempt.
- No writes on those cases beyond the valid entry owner's own pass/block receipt, or a future typed boundary-rejection record explicitly owned by that contract. Missing ownership cannot be repaired by a locally invented record.
- Forbidden substitutes: Dispatch confirmation, host binding, ACI acceptance, route/domain/evidence-closure/semantic/artifact/exact-effect verdicts, and orchestration completion.

The conditional documentation path is:

```text
ConfirmedDispatch + frozen run envelope
  -> external ReasoningEntryVerdict pass | block
  -> on exact pass only: ReasoningRunCommandMapper
  -> proposed ACI lifecycle command
  -> ACI accept | reject
  -> accepted lifecycle record
  -> materializer verifies journal cut
  -> observation admit | reject
  -> bounded semantic evaluator
  -> semantic verdict + receipt
  -> artifact admit | reject
  -> exact-effect pass | block
  -> proposed ACI effect intent
  -> ACI accept | reject
  -> external-effect attempt
  -> ACI records observed outcome or honest unknown
```

No edge means therefore authorized, true, or executed. Before entry pass, the proposed command identity/digest is frozen envelope data only; the mapper is not called and ACI sees no command. After entry pass, mapper output must exactly bind to the precommitted command identity/digest or block before ACI.

## Eight executable discriminating fixtures

Each fixture is required future executable evidence unless its tier says otherwise.

| ID | Frozen start and ordered operations | Discriminating observations and zero-call/no-write assertions | Terminal/replay and evidence tier |
|---|---|---|---|
| F1 host seat, journal, redelivery, close, verify | At target `b42228f`, freeze opening record, prompt/manifest digests, dispatch/group/seat/turn/attempt identities, and empty verified journal. Compile and bind seat, accept lifecycle records, redeliver identical then divergent bytes, attempt premature parent close, close children then parent, restart and verify. | Identical redelivery returns the same accepted identity; divergent bytes conflict; premature parent close blocks; digest mismatch rejects. Rejections create no second event, binding, head advance, terminal parent fact, provider call, or effect call. | One coherent closed history only after children; restart reconstructs identical identities/chain. Current: implementation/test bytes observed, compiler slice alone executed 13/13. Required: dependency-complete integration run. |
| F2 recursive A -> readiness -> B | Freeze RWO design/ontology digests, accepted versioned A-then-B definition, confirmed expanded plan, A artifact digest, readiness schema, empty derived cursor. Expand once, run A, admit outcome/reference, independently assess readiness, issue B only on exact pass, rebuild cursor. Repeat block, missing artifact, wrong digest. | Exact A artifact plus independent pass makes only B eligible. Block/missing/wrong/stale/undeclared cases produce no B executor call, B command/event, fabricated artifact, or domain-success fact; cursor cannot rewrite history. | Positive terminates under B-owned status; blocked cases preserve residue; rebuild is identical. Current: proposal/precedent only. Required: accepted schemas, reducer, negatives, rebuild receipt. |
| F3 semantic fan-in | Freeze producer manifest with every identity/digest and separately owned reconciliation schema/owner. Present partial, complete-with-invalid, and all-exact sets; persist typed reconciliation; feed readiness only on exact positive result. | All expected valid inputs produce one manifest-bound result. Partial, divergent duplicate, foreign-run, invalid digest, or missing owner is typed non-pass. Negative paths call no downstream work/evaluator and write no route pass or rewritten source history. | Restart yields the same reconciliation; terminal outcome remains consumer-owned. Current: no generic witness. Required: executable reconciler and all counterexamples. |
| F4 observational sidecar independence | Freeze accepted lifecycle history and projection version. Run primary routing baseline, rebuild sidecar, restart, then inject late, failed, and divergent sidecar output with primary history fixed. | Exact sidecar rebuild is identical. Late/fail/divergent residue cannot alter route eligibility, domain status, or accepted history. Primary routing makes zero prerequisite calls to sidecar; sidecar failure writes no command, route/domain/semantic/effect fact. | Primary terminal state is unchanged with sidecar present, absent, late, or failed. Current: target projections only. Required: executable rebuild/independence suite. |
| F5 reasoning-entry non-pass | Freeze Dispatch/seat/precommitted command/schema/freshness/evidence-cut identities. Obtain exact block, then test missing owner/receipt, stale receipt, subject/schema mismatch, and cross-run substitution. | Valid block binds owner, subject, cut, freshness; integrity failures are unusable. Every case has zero mapper, ACI, actor, materializer, observation, evaluator, artifact, exact-effect, effect-intent, and attempt calls. Only a valid block receipt may be written. | Entry-blocked or entry-invalid terminal residue; replay re-verifies only and invokes nothing downstream. Current: bounded local zero-call precedent, owner unselected. Required: conformed adapter, counters, write-set/mismatch/replay tests. |
| F6 positive L0, effect non-pass, ACI rejection | Freeze valid L0 inputs and semantic/effect envelopes. Produce `RecommendedUnderSnapshot`, admit exact artifact, block exact effect; repeat with effect pass but ACI effect-intent rejection. | Recommendation/receipt persists. Effect block makes zero ACI effect-intent and adapter calls. ACI rejection makes zero adapter calls and fabricates no outcome. Neither rewrites semantic receipt. | Distinct terminal states preserve replay. Current: bounded L0/fixed-double witness. Required: separately owned artifact/effect/ACI adapters and assertions; real effect not required for this negative fixture. |
| F7 historical replay vs current revalidation | Freeze immutable original run/receipt, changed present authority/catalog/evidence/freshness, and new run identity. Replay historical inputs, then revalidate under current inputs/new identity. | Replay is byte-identical. Revalidation is a separate claim and may differ. Replay makes zero provider/authority/gate/ACI/artifact/effect/adapter calls and no writes; revalidation cannot overwrite history. | Exact history plus distinct lineage-bearing current record. Current: bounded local replay precedent. Required: identity, equality, zero-call, changed-state, immutability suite. |
| F8 owner receipts, substitution, missing effect owner | Freeze run A/B identities and entry/artifact/effect receipt schemas. Try missing entry receipt, exact matching receipt, run-B substitution into run A, then omit exact-effect owner after earlier passes. | Matching receipt permits only its immediately governed boundary. Missing/mismatched/cross-run/unknown owner or missing effect owner blocks exactly there. Entry failure calls/writes nothing downstream; artifact/effect failures make zero later calls; no component invents owner evidence. | Each negative is immutable and replay-verifiable; earlier passes cannot cure a later missing owner. Current: documentation/open residue only. Required: schemas, registries, conformance receipts, counters, cross-run negatives. |

## Readiness verdict

- Reviewer return: ready. The round-2 typed-boundary and non-vacuity defects have explicit repairs.
- Documentation-only cross-repository contract: blocked; owners and conformance/runtime receipts remain unselected or absent.
- RWO executable/promoted: no; recursive, fan-in, sidecar, composite, and cursor fixtures have not run, and RWO-OQ-010 remains unresolved.
- Executable orchestrator-to-ARE integration: not selected; the current path is documentation-only.
- Bounded L0 evidence: retained only at its local E3 tier.
- Target validation: incomplete. Protocol compilation passed 13/13; FastAPI-dependent suites remain execution-unverified.

Claim ceiling: synthesis evidence only. This does not implement or select an executable integration, assign owners, register host bindings, promote, publish, deploy, prove production readiness, or authorize external effects.
