# TASK-WEG-003 — Final Status Ceiling

## Objective and mapping

- Layer/slice/wave: L0 / S0 / W0.
- Decision: make final readiness the strictest applicable gate, never a promotion from unrelated machine success.
- Dependency: SWU-WEG-002.
- Blockers: none.

## Inputs and outputs

- Input: schema-valid run receipt and transport profile.
- Output: `{status_ceiling, final_status, reasons[]}` with deterministic order.
- State touched: no durable mutation; pure evaluation.

## Algorithm

```text
validate envelope integrity; invalid -> block
ceiling = pass
apply in order:
  transport candidate/unproven -> flag
  required audition absent/non-pass/digest-invalid -> flag
  newcomer comprehension absent/non-pass/digest-invalid -> flag
  post-apply verification required and absent/non-pass/digest-invalid -> flag
  open correction invalidates current receipt -> flag
  any explicit blocking gate or integrity violation -> block
final = stricter(requested_status, ceiling)
return stable reason codes in rule order
```

`stricter` uses `block < flag < pass`. Source/structure and implementation/render passes are recorded but never raise the ceiling. A candidate transport with all human gates passing still returns at most `flag`.

Edge cases: requested `block` remains block; multiple flag reasons are retained; `not_required` is accepted only from the transport profile; unknown status is a schema/integrity block.

## Smallest Working Unit: SWU-WEG-003

- Primary behavior: compute final status and reason codes from independent axes.
- Independent acceptance boundary: a table-driven suite covers each ceiling contributor alone, combined contributors, green proof, and non-substitution.
- Split analysis: individual ceiling rules were considered as child units; they are rows of one pure precedence function and splitting would permit inconsistent ordering/aggregation.
- Source anchors: `../../DESIGN.md#final-status-algorithm`, `../../DEFINE.md#proof-model`.
- Related context: SWU-WEG-001 expected outcomes; SWU-WEG-002 schemas.
- Write scope: `arcanum/spells/whisper/tools/validate-whisper-run-receipt.py`, `arcanum/spells/whisper/development/fixtures/editorial-admission/status-ceiling/**`.
- Done criteria: deterministic output and exact reason codes for every table case; existing draft validator behavior unchanged.
- Acceptance evidence: evaluator test report plus a candidate-all-human-pass result of `flag`.
- Verification:

```bash
python3 arcanum/spells/whisper/tools/validate-whisper-run-receipt.py --fixtures arcanum/spells/whisper/development/fixtures/editorial-admission/status-ceiling
python3 arcanum/spells/whisper/tools/validate-whisper-draft.py --help >/dev/null
```

- Execution owner: `local-fallback` through Task Session under Spellcraft.
- Handoff note: do not add language scoring; if fixture semantics would require understanding prose, route that assertion to the human record instead.

## Synchronization

Record exact evaluator version/hash in the receipt. W1 does not open until SWUs 001–003 all pass.
