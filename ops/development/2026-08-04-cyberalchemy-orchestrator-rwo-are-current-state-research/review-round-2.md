# Reviewer Round 2

Status: three precise repairs remain after synthesis revision 1. They collapse
to two changes: insert a typed reasoning-entry verdict and make the eight
finite fixtures executable discriminating traces.

## Precedent

All prior ownership defects are closed except omission of the entry-gate edge.
The conditional path must become:

`ConfirmedDispatch + frozen run envelope → entry-gate pass/block → proposed
ACI lifecycle command → ACI accept/reject`.

The entry owner is external and unselected. RWO may neither produce nor
substitute its verdict. Every entry non-pass or missing/mismatched owner receipt
must yield zero mapper, ACI, actor, evaluator, and effect calls.

## Definitional soundness

Define `ReasoningEntryVerdict`:

- subject: one exact proposed reasoning invocation before actor-cut
  materialization or evaluator execution;
- owner: separately conformed reasoning-entry owner, not inherited by RWO, ACI
  lifecycle admission, or the evaluator;
- inputs: confirmed Dispatch reference/digest, bound seat, proposed command
  identity/digest, required schema/version identities, freshness context;
- output: persisted `pass | block` with subject/evidence-cut digests;
- failure: missing owner/receipt, stale/mismatched subject, unknown version, or
  non-pass blocks every downstream semantic/effect stage;
- forbidden substitutions: confirmation, ACI acceptance, route eligibility,
  artifact admission, semantic verdict, or exact-effect verdict.

## Non-vacuity

The proof-tier narrowing passes. The remaining repair is an eight-row fixture
matrix whose rows each specify frozen inputs/start state, ordered operations,
positive and negative observations, zero-call/no-write assertions,
terminal/replay expectation, and required evidence tier:

1. confirmation → compiled seat → accepted binding/journal → identical and
   divergent redelivery → child/parent close behavior → journal verification;
2. recursive A → typed routing-readiness verdict → B, including blocked,
   missing-artifact, and wrong-digest paths plus cursor rebuild;
3. fan-in partial/invalid/all-valid inputs plus separately owned reconciliation;
4. deterministic sidecar rebuild and independence under late/fail/divergent
   sidecar;
5. entry non-pass with only entry verdict persisted and all downstream calls
   zero;
6. positive L0 plus effect non-pass, and effect pass without ACI acceptance;
7. exact historical replay versus new-identity current revalidation;
8. missing owner receipt, matching receipt, cross-run substitution, and missing
   exact-effect owner receipt.
