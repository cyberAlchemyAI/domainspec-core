# TASK-WEG-005 — Full-Derivative Admission

## Objective and mapping

- Layer/slice/wave: L1 / S1 / W1.
- Decision: prevent full generation when intent or exact-surface approval does not permit it.
- Dependency: SWU-WEG-004.
- Blockers: none.

## Inputs and outputs

- Inputs: intent state, requested derivative kind, transport policy, admissible approval record, change manifest.
- Output: `{generation_decision: allow|block, reasons[]}`.
- State touched: no mutation; this gate runs before derivative creation.

## Algorithm

```text
if full derivative and intent != frozen: block volatile-or-unfrozen
if transport requires approval and matching approval is not admissible: block unapproved-surface
if any audience block lacks replaces/distinct_job/validation_only ownership: block unaccounted-surface
otherwise allow
```

The algorithm does not use transport proof status to deny all candidate trials. Proof status constrains final readiness through SWU-WEG-003. Transport-specific policy may still block a trial for missing gates.

Edge cases: bounded audition generation remains allowed in volatile state; a frozen receipt for a prior surface does not admit a new derivative; `validation_only` content must not appear in rendered outputs.

## Smallest Working Unit: SWU-WEG-005

- Primary behavior: compute pre-generation permission for a requested derivative.
- Independent acceptance boundary: volatile full generation, wrong-surface approval, and unowned blocks are blocked while a bounded volatile audition and exact approved frozen trial are correctly classified.
- Split analysis: state, approval, and surface ownership were considered separately; they are conjunctive inputs to one pre-generation decision and partial admission would be unsafe.
- Source anchors: `../../DESIGN.md#generation-decision-algorithm`, existing Whisper intent convergence and phase 5.
- Related context: SWU-WEG-004 binding results, decision CTD-03.
- Write scope: generation-decision functions and fixtures within the run-receipt validator package; canonical Whisper phase/gate text required to call the evaluator.
- Done criteria: generation decision is emitted before derivative creation and tests prove audition/full-derivative distinction.
- Acceptance evidence: exact decision/reason report for every admission fixture.
- Verification:

```bash
python3 arcanum/spells/whisper/tools/validate-whisper-run-receipt.py --fixtures arcanum/spells/whisper/development/fixtures/editorial-admission/generation-admission
```

- Execution owner: `local-fallback` through Task Session under Spellcraft.
- Handoff note: do not treat candidate proof status as automatic generation block; keep proof and generation decisions separate.

## Synchronization

Update canonical phase text and tool behavior in one Task Session receipt; generated runtime is not regenerated until SWU-WEG-009.
