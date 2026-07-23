# TASK-WEG-004 — Exact Evidence Binding

## Objective and mapping

- Layer/slice/wave: L1 / S1 / W1.
- Decision: accept human evidence only when it names the required decision and the exact artifact/surface under evaluation.
- Dependency: SWU-WEG-002.
- Blockers: none.

## Inputs and outputs

- Inputs: schema-valid receipt, surface manifest, approval/comprehension/post-apply records.
- Output: admissibility result per human record with stable failure reason.
- State touched: no durable mutation; pure digest/reference checks.

## Algorithm

1. Recompute artifact and ordered surface digests from the manifest.
2. Check the evidence record's artifact and surface digests against recomputed values.
3. Check `approval_kind` against the transport's required gate.
4. Check prompt identity and audience/transport identity.
5. For comprehension, require exactly the profile's question IDs and a human outcome; do not judge answer text.
6. For post-apply review, require the applied artifact digest and a review stage distinct from the production stage.
7. Return one admissibility result per record; never fall back to conversational keywords.

Edge cases: whitespace-normalized text must have a documented canonicalization before hashing; a new edit after approval invalidates evidence; multiple approvals select by explicit ID; same operator may review later but stage identity must differ.

## Smallest Working Unit: SWU-WEG-004

- Primary behavior: exact evidence binding rejects scope/digest substitution.
- Independent acceptance boundary: ambient approval, wrong artifact, wrong surface, wrong kind, incomplete questions, and pre-apply/post-apply substitution all fail; exact controls pass.
- Split analysis: artifact, surface, and decision-kind binding are conjuncts of one admissibility decision; partial binding would be unsafe and not independently useful.
- Source anchors: `../../DESIGN.md#33-explicit-approval-record`, `#34-evidence-axes`, decision D-02.
- Related context: SWU-WEG-002 schemas.
- Write scope: binding functions in `arcanum/spells/whisper/tools/validate-whisper-run-receipt.py`; binding fixture subtree.
- Done criteria: all substitution controls fail with stable reasons and no ordinary phrase such as `apply approved` is accepted without a typed record.
- Acceptance evidence: table-driven binding report.
- Verification:

```bash
python3 arcanum/spells/whisper/tools/validate-whisper-run-receipt.py --fixtures arcanum/spells/whisper/development/fixtures/editorial-admission/evidence-binding
```

- Execution owner: `local-fallback` through Task Session under Spellcraft.
- Handoff note: preserve the canonicalization algorithm in public docs and fixtures so evidence can be replayed.

## Synchronization

Merge only after SWU-WEG-003 still passes against the extended validator. Report any changed reason-code precedence as residue.
