---
stage: S7-design-review
capability: interrogation
mode: refine-design-review
status: pass
updatedAt: 2026-06-08
---

# S7 Interrogation Design Review

## Review Question

Does the design preserve the difference between source evidence, generated
Inventory read models, and future execution/pilot mutation?

## Answer

Yes, if the plan carries these constraints:

1. Source docs remain read-only until a later task explicitly owns source edits.
2. Inventory pilot mutation requires a target confirmation.
3. Generated cards and indexes are lookup/read models, not canonical game rules.
4. Open Body War decisions stay open in a gap/risk queue until resolved by the
   correct owner.
5. The first pilot corpus remains bounded around Park Track Control.

## Main Risk

The tempting failure mode is to invent a whole Body War inventory now. That
would skip the intended MVP sequence: contract, templates, validators, then
pilot.

## Design Repair

Make `TASK-BW-INV-001` create only the feature-pack baseline. Keep `pilot/`
folders planned but not populated until target confirmation and templates exist.

## Verdict

Pass. Safe to plan.
