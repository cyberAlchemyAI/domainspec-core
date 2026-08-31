# TASK-MPX-003-REVIEW — Human review and bounded witness verdict

## Objective

Obtain one precommitted role-label-blind human semantic review of the exact positive pair and boundary case, then issue the candidate-specific non-vacuity verdict under the accepted claim ceiling.

## Mapping

- Slice: S-MPX-03
- Layer: L0
- Wave: W2
- SWU: SWU-MPX-003
- Source contracts: `../../IMPLEMENTATION-PLAN.md#SWU-MPX-003--perform-human-review-and-issue-witness-verdict`; `../../IMPLEMENTATION-PLAN.md#Non-vacuity-verdict-rule`

## Dependencies

- passing SWU-MPX-002 Task Session receipt;
- joined `invoke:refresh` closeout for SWU-MPX-002;
- exact passing mechanical receipt;
- explicit participation by one human reviewer.

## Smallest Working Unit: SWU-MPX-003

- Primary behavior: obtain one role-label-blind human review and issue its candidate-specific non-vacuity verdict.
- Independent acceptance boundary: the pre-review commitment, blind packet, human response, reveal, and deterministic verdict close as one exact chain without reader or integration claims.
- Candidate child units: commitment/packet preparation; human semantic response; reveal/verdict computation.
- Retained-boundary rationale: none can pass independently as the experiment result. A packet without a response is unfinished; a response without its precommitted reveal cannot bind the candidate; a reveal without the exact human response has no human-owned meaning. Interruption before reveal blocks and restarts the whole SWU rather than resuming hidden state.
- Write scope:
  - `ops/development/2026-08-25-whisper-writing-frameworks-research/minto-pyramid-experiment-001/review/BLINDING-COMMITMENT.json`
  - `ops/development/2026-08-25-whisper-writing-frameworks-research/minto-pyramid-experiment-001/review/BLINDED-REVIEW-PACKET.json`
  - `ops/development/2026-08-25-whisper-writing-frameworks-research/minto-pyramid-experiment-001/review/HUMAN-REVIEW-RESPONSE.json`
  - `ops/development/2026-08-25-whisper-writing-frameworks-research/minto-pyramid-experiment-001/review/HUMAN-REVIEW-AND-WITNESS.json`
  - `ops/development/2026-08-25-whisper-writing-frameworks-research/minto-pyramid-experiment-001/precloseout/SWU-MPX-003.json`
  - `ops/development/2026-08-25-whisper-writing-frameworks-research/minto-pyramid-experiment-001/receipts/SWU-MPX-003.task-session.json`
- Invoke-owned closeout output, excluded from Task Session write scope:
  - `ops/development/2026-08-25-whisper-writing-frameworks-research/minto-pyramid-experiment-001/closeouts/SWU-MPX-003.invoke-refresh.json`
- Done criteria:
  - commitment is persisted before packet creation and contains no mapping or nonce;
  - packet binds actual case/mechanical/commitment bytes; carries the complete role-neutral review context, exact instructions, and six fixed human-readable prompts; contains generic A/B text blocks derived exactly from the case views; and omits the mapping and nonce;
  - reviewer is human, receives only the packet, and completes an exact packet-bound response before variant mapping is revealed;
  - actual case, mechanical, commitment, packet, and response paths, hashes, and sizes are recomputed;
  - factual equivalence, fair representation, executive-transport fit, hierarchy plausibility, named decision change, and boundary-case inactivity each recorded as `pass`, `fail`, or `inconclusive` with rationale;
  - the named-decision judgment identifies A, B, or none; pass requires that the selected label reveal as candidate;
  - mapping and nonce reveal recomputes the commitment and is timestamped after response completion;
  - verdict rule applied exactly;
  - limitations and disagreement retained;
  - `reader_outcome_claims=false`, `integration_authorized=false`, `canonical_change_authorized=false`, `authority_effect=none`.
- Acceptance evidence: human review identity class, commitment/packet/response/reveal timestamps, complete judgments, recomputed actual-byte bindings, and a structurally valid verdict receipt.
- Execution owner: manual human review inside one Task Session; no model-only fallback.
- Handoff note: stop and return `block` if no human reviewer participates. Do not ask the reviewer whether Minto is “better”; ask only the bounded semantic and decision-change questions.

## Human review/witness shape

The SWU produces four closed artifacts in order:

1. `BLINDING-COMMITMENT.json`: canonical mapping-plus-nonce digest and creation time only.
2. `BLINDED-REVIEW-PACKET.json`: exact predecessor references; commitment reference; role-neutral audience, purpose, transport, unit, supported-concept/limit, decision/failure, boundary-intent, and claim context; exact instructions; generic A/B views; boundary view; and six fixed prompt records with allowed statuses, rationale requirements, and the A/B/none instruction for the named-decision judgment.
3. `HUMAN-REVIEW-RESPONSE.json`: exact packet reference, human attestation, review timestamps, mapping-not-known flag, six ordered judgments, rationales, and limitations.
4. `HUMAN-REVIEW-AND-WITNESS.json`: exact references to every prior artifact, mapping/nonce reveal and reveal time, recomputed verdict, limitations, and claim ceilings.

`non_vacuity_verdict=pass` is legal only when the actual mechanical receipt passes, all six human judgments pass, the selected hierarchy label reveals as candidate, the commitment and chronology validate, and all exact byte bindings match. A `fail` or `inconclusive` result is a valid experiment outcome and must not be rewritten into pass.

## Synchronization

On Task Session pass, route only the declared terminal closeout target inventory through `invoke:refresh:apply-approved`. The unique successor is `__complete__`; no integration route is implied.
