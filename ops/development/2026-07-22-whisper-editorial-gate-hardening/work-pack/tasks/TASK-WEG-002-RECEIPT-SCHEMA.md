# TASK-WEG-002 — Run Receipt Schema

## Objective and mapping

- Layer/slice/wave: L0 / S0 / W0.
- Decision: define one machine-checkable envelope that cannot collapse independent evidence axes.
- Dependency: SWU-WEG-001.
- Blockers: none.

## Inputs and outputs

- Inputs: design sections 3.2 through 3.6 and fixtures from SWU-WEG-001.
- Outputs: schemas for run receipt, surface manifest, approval/comprehension/post-apply evidence, and correction event; schema validation fixture results.

## Data and rules

1. Require stable run/transport/audience/intent identity.
2. Require the four evidence-axis objects separately; absence is explicit.
3. Require artifact and surface SHA-256 fields when a human evidence axis is present.
4. Require `approval_kind` and `prompt_id` for approval records.
5. Require reviewer kind, required question IDs, answers, and outcome for comprehension records; do not validate answer semantics.
6. Require producer stage and review stage for post-apply records.
7. Require computed decision fields but leave policy consistency to SWU-WEG-003/005.
8. Permit additive residue; reject unknown status enums and malformed digests.

Edge cases: non-newcomer transports may use `not_required` comprehension only when the profile says so; a missing axis is not serialized as `pass`; multiple approvals must identify the selected approval.

Failure mode: if the schema encodes editorial quality as a numeric machine score or allows one axis to substitute for another, block the SWU.

## Smallest Working Unit: SWU-WEG-002

- Primary behavior: schema validation accepts complete envelopes and rejects incomplete/cross-axis envelopes.
- Independent acceptance boundary: positive and negative schema fixtures return their expected parse/validation result without invoking status policy.
- Split analysis: schema files and fixtures were considered separately; a schema without negative examples cannot prove the evidence boundary.
- Source anchors: `../../DESIGN.md#31-transport-profile-extension` through `#36-correction-event`; `../../GLOSSARY.md` evidence-axis terms.
- Related context: SWU-WEG-001 fixture IDs and `../shared/cross-task-decisions.md#ctd-01`.
- Write scope: `arcanum/spells/whisper/schemas/editorial-run-receipt.schema.json`, `arcanum/spells/whisper/schemas/editorial-correction-event.schema.json`, `arcanum/spells/whisper/schemas/examples/editorial-admission/**`.
- Done criteria: schemas parse; all expected-good fixtures pass; all expected-bad fixtures fail for the recorded field/reason.
- Acceptance evidence: machine-readable schema-test report.
- Verification:

```bash
python3 -m json.tool arcanum/spells/whisper/schemas/editorial-run-receipt.schema.json >/dev/null
python3 -m json.tool arcanum/spells/whisper/schemas/editorial-correction-event.schema.json >/dev/null
```

- Execution owner: `local-fallback` through Task Session under Spellcraft.
- Handoff note: use the repository's available JSON Schema validator if present; otherwise add a narrow standard-library shape validator only with Spellcraft approval and record the limitation.

## Synchronization

Publish the schema-test report as the SWU receipt. Do not mark status or generation evaluators complete from schema success.
