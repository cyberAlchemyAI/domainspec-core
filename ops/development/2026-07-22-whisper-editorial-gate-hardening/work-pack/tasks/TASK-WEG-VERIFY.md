# TASK-WEG-VERIFY — Full Validation and Spellcraft Decision

## Objective and mapping

- Layer/slice/wave: L3 / S3 / W3.
- Purpose: prove recomposition and issue a lifecycle validation receipt after all implementation SWUs close.
- Dependencies: SWU-WEG-001 through SWU-WEG-009.
- Blockers: any failed prior SWU or privacy/drift violation.

## Smallest Working Unit Exemption

This is a closure-only `VERIFY` task. It does not mutate feature behavior and is exempt from SWU decomposition.

## Validation regimes

1. Low: short prose receipt separates structure from editorial evidence.
2. Medium: newcomer README opening catches jargon-before-situation and absent comprehension.
3. Complex generic: interactive technical explainer covers complete first surface, exact approval, candidate ceiling, post-apply review, surface delta, and correction replay.
4. Complex private: BTE X-Ray integration runs from the private host path and stores only private result references.
5. Packaging: canonical/generated/local preset drift and public/private sweep.
6. Non-regression: existing Whisper draft-validator fixtures and public presets still pass their declared checks.

## Required result

- `arcanum/spells/whisper/development/VALIDATION.md` records commands, results, causal interpretation, residue, and transport status.
- Spellcraft returns `pass`, `flag`, or `block` for the revision.
- Candidate technical explainer remains `flag` unless a separate explicit promotion process exists; this task cannot promote it.
- Any failure is linked to the responsible SWU and leaves history intact.

## Reviewable checks

```bash
python3 arcanum/spells/whisper/tools/validate-whisper-run-receipt.py --fixtures arcanum/spells/whisper/development/fixtures/editorial-admission
git diff --check -- arcanum/spells/whisper .agents/skills/whisper .arcanum/spells/whisper
```

The exact existing canonical fixture commands must be copied from the live repository at execution time and added to the validation receipt.

- Execution owner: `manual` Spellcraft validation with Experiment Harness evidence.
- Handoff note: close the work pack only after traceability WEG-R1 through WEG-R10 has concrete evidence or named residue.
