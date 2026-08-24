# Non-vacuity and overhead review

- Action: `spawn-0006`
- Reviewer: `Gödel, Kurt`
- Verdict: `REPAIR`
- Mutation: none

The architecture may proceed as a build specification, but no v0 exists. Kill
any claim that diagrams, schemas, catalogs, cards, prompts, dashboards, or
receipts constitute v0. A future v0 is admissible only as an executable,
deterministic local-fixture slice.

## Witness defects

1. Grounding lacks an exact prompt, fixture records, selected/excluded IDs,
   expected composed bytes/digest, deterministic result, and source-chip
   assertions. Current Resonant bytes prove filtered provider messages and
   budget construction only (`synthesis.md:185-190`; `research.md:297-299`;
   `../workspace-resonant/2.0.0-alpha/src/modules/chat/chat-route-request.ts:59-99`).
2. Routing/approval lacks a classifier fixture, exact input/config digest,
   proposal bytes/digest, edit mutation, approval record, and zero-effect
   counters (`synthesis.md:187-191,173-178`; `research.md:299-305`).
3. Two-child execution lacks an executable fake-host adapter, event script,
   operation binding, action/run identity fixture, marker corpus, or asserted
   event log. Current Resonant has one global transient run token
   (`synthesis.md:191-194`; `research.md:306-310,367-379`;
   `../workspace-resonant/2.0.0-alpha/src/modules/chat/run-guard.ts:5-28`).
4. Reload/consumption lacks seeded persistence, hydration inputs,
   reconciliation calls, duplicate-announcement counter, and post-attach
   invariant snapshot (`synthesis.md:194-195`; `research.md:504-523`;
   `StrategistChatRail.tsx:393-401,596-603,762-775`).
5. Intake/correction/capability-gap lacks an intake draft schema, trusted-write
   call counter, correction/tombstone input, before/after composed bytes, and
   missing-operation fixture (`synthesis.md:196-200`;
   `research.md:309-310,460-468,591-608`).

## Required repair

- Define one versioned fixture family containing literal turns, two
  handle/source records, expected RouteDecision, proposal bytes/digest,
  approval record, two child scripts, marker corpus, blocker/artifact handles,
  reload image, selective-consumption command, intake draft, and
  missing-capability case.
- Name the local-fixture adapters: thread/Interaction, snapshot composer,
  deterministic route, proposal/approval registrar, fake two-child host, join
  reducer, reload reconciler, result consumption, and local intake draft.
  Mark all production adapters absent.
- Add machine assertions for registration/spawn/owner-call counts, digests,
  addressed-input counts, parent/sibling byte equality, terminal outcomes,
  gate state, announcements, attachment effects, memory-write count, and
  zero-spawn gap behavior.
- Add exact browser harness commands and selectors; rendering a card is not
  proof.
- Keep evaluator code/calls/UI/effects out of v0.
- Assign each latency target to an operation and fixture; resolve the warm
  deterministic ≤20 ms versus route-classification ≤50 ms distinction.

The test categories are appropriate, but without fixture paths, commands,
selectors, receipts, or executions they remain a plan. All budgets are
honestly unmeasured and remain non-acceptance evidence. Measurement contracts
still need clock/warmup/sample/percentile definitions, tokenizer/model version,
storage serialization point, graph corpus/preservation proof, attention
denominators/window/cohort, and deterministic browser seed/selectors.
