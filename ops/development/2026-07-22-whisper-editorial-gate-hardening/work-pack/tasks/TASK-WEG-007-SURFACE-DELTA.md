# TASK-WEG-007 — Surface Delta and Retell Ownership

## Objective and mapping

- Layer/slice/wave: L1 / S1 / W1.
- Decision: require every added audience block to own one necessary job and stop validation retells from becoming automatic duplicate copy.
- Dependency: SWU-WEG-006.
- Blockers: none.

## Inputs and outputs

- Input: composition plan, existing surface map, proposed block changes.
- Output: change manifest with `replaces`, `distinct_job`, or `validation_only` classification; validation findings.

## Algorithm

1. Enumerate all added or substantially rewritten audience-visible block IDs.
2. Require exactly one ownership classification per block.
3. For `replaces`, require existing block IDs and ensure they are removed/consolidated in the proposed surface.
4. For `distinct_job`, require a named audience job and human-review rationale.
5. For `validation_only`, ensure the block is absent from rendered audience surfaces.
6. For `retell_chain`, default to `validation_only`; rendering requires both a distinct job and replacement mapping.
7. Emit deterministic structural findings; route semantic duplication to post-apply human review.

Edge cases: an accessibility label or navigation aid may have a distinct job without replacing prose; changing a heading in place is not an added block; shared IDs or absent replacement targets block manifest integrity.

## Smallest Working Unit: SWU-WEG-007

- Primary behavior: change-manifest validation accounts for every new audience block.
- Independent acceptance boundary: unowned additions, missing replacement targets, validation-only rendered blocks, and unjustified retells fail; valid replacements/distinct jobs pass.
- Split analysis: retell and added-block rules were considered separately; retell is the high-risk specialization of the same surface ownership behavior, so one manifest validator preserves coherent enforcement.
- Source anchors: `../../DESIGN.md#37-change-manifest`, decision D-05.
- Related context: SWU-WEG-005 generation admission and SWU-WEG-006 first surface.
- Write scope: change-manifest schema/validator functions, fixture subtree, canonical Whisper delivery-flow/retell clarification.
- Done criteria: complete red/green control family and human-review residue for semantic duplication.
- Acceptance evidence: change-manifest validation report.
- Verification:

```bash
python3 arcanum/spells/whisper/tools/validate-whisper-run-receipt.py --fixtures arcanum/spells/whisper/development/fixtures/editorial-admission/surface-delta
```

- Execution owner: `local-fallback` through Task Session under Spellcraft.
- Handoff note: never claim the manifest proves semantic uniqueness; its proof is ownership/accounting only.

## Synchronization

Rerun generation-admission fixtures because an invalid change manifest is a pre-generation block.
