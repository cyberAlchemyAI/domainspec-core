# TASK-WEG-008 — Correction Replay and Observation

## Objective and mapping

- Layer/slice/wave: L2 / S2 / W2.
- Decision: preserve a rejected prior readiness claim as evidence while removing it from current readiness and reopening only bounded composition work.
- Dependencies: SWU-WEG-003 and SWU-WEG-005; W1 gate passed.
- Blockers: none.

## Inputs and outputs

- Inputs: current run receipt, prior receipt reference, correction event, current intent state.
- Outputs: appended correction event, updated current-status pointer, reduced intent state, next route, Signal Observer envelope.
- Durable state: run-local append-only JSONL and current-state projection; historical receipts are immutable.

## Transaction algorithm

```text
validate correction event and referenced prior receipt
append event before changing current projection
if meaning_core_changed or related_correction_count >= 2: intent = volatile
if false_positive_readiness: mark prior receipt superseded_for_current_readiness
select next route:
  false positive -> workflow-reflect + bounded re_audition
  volatile ordinary correction -> bounded re_audition
  otherwise -> ordinary revision
emit signal with four evidence axes, invalidated receipt, state transition, route
commit projection only after append succeeds
```

Failure/compensation: if append fails, do not update the projection; if prior receipt is absent, block with residue; duplicate event ID is idempotently rejected; historical `pass` remains visible but non-current.

## Smallest Working Unit: SWU-WEG-008

- Primary behavior: one atomic correction transaction appends evidence and updates current readiness/state/routing.
- Independent acceptance boundary: replay proves append-before-project, idempotency, prior history preservation, volatile transition, and reflect route.
- Split analysis: append, invalidation, state, and signal were considered separately; partial success would create contradictory audit/current state, so they form one transaction boundary.
- Source anchors: `../../DESIGN.md#36-correction-event`, `#correction-state-reducer`; July 22 updated reflection policy.
- Related context: SWU-WEG-003 and SWU-WEG-005 reason codes.
- Write scope: correction schema/fixtures, correction reducer helper, run evidence convention, Whisper observability contract; no Workflow Reflect or Signal Observer internals.
- Done criteria: deterministic replay and fail-safe compensation tests pass; canonical Whisper names the route and signal fields.
- Acceptance evidence: replay log, resulting projection, and emitted signal fixture.
- Verification:

```bash
python3 arcanum/spells/whisper/tools/validate-whisper-run-receipt.py --fixtures arcanum/spells/whisper/development/fixtures/editorial-admission/correction-replay
python3 -m json.tool arcanum/spells/whisper/development/fixtures/editorial-admission/correction-replay/expected-signal.json >/dev/null
```

- Execution owner: `local-fallback` through Task Session under Spellcraft.
- Handoff note: integration invokes Signal Observer/Workflow Reflect by native capability handle; do not mutate their contracts in this SWU.

## Synchronization

W2 closes only after the prior receipt remains queryable and the current readiness pointer no longer treats it as current pass evidence.
