# TASK-ILP-004: Execution-Mode Material and Readiness

## Objective

Compute one epoch-bound handoff-readiness verdict from a mode-compatible
producer output and an independent validator.

- Layer/slice/wave: L1 / S1 / W1
- Lifecycle owner: Spellcraft plus Sigil Development interface review
- Dependencies: SWU-ILP-002 and SWU-ILP-003
- Source contracts: `../../DESIGN.md` mode matrix,
  current material-package schemas/validator in `../shared/CONTEXT.md`
- Candidate write scope:
  - `arcanum/spells/invoke/schemas/local-execution-contract.schema.json`
  - `arcanum/spells/invoke/schemas/handoff-readiness-receipt.schema.json`
  - `arcanum/spells/invoke/scripts/validate_handoff_readiness.py`
  - lifecycle-progress fixtures/runner

## Algorithm

1. Select the mode row: local, external, delegated, or reusable.
2. Require pairwise-distinct producer, producer-validator, and consumer role
   identities.
3. For local mode, validate the immutable local execution contract against the
   epoch; require no output-byte claims.
4. For packaged modes, consume the existing material-package validator receipt
   and exact package binding without duplicating its logic.
5. Compare unit, epoch control digest, dependencies, writes, paths, publication
   class, validation surface, and receipt classes.
6. Return:
   - `ready` when every declared requirement is valid;
   - `gated` when compatible required material is not yet produced;
   - `blocked` for absent owner, incompatible mode, role collapse, invalid,
     stale, or mismatched evidence.
7. Emit exact missing/incompatible lists and blocker fingerprint.

## Smallest Working Unit

### SWU-ILP-004

- Primary behavior: compute mode-compatible handoff readiness.
- Acceptance boundary: exactly one `ready`, `gated`, or `blocked` receipt for
  one epoch.
- Candidate children: local contract; packaged adapter; role checks; verdict.
- Retained rationale: they are mode branches and conjuncts of one readiness
  decision; splitting would leave no route-wide verdict.
- Execution owner: `local-fallback` through Spellcraft.
- Done criteria:
  - local positive requires no pre-authored bytes;
  - external/reusable positives preserve exact package behavior;
  - missing producer, incompatible mode, producer=validator, validator=consumer,
    and stale digest cannot be ready;
  - readiness receipt admits no transition itself.
- Validation:
  `python3 arcanum/spells/invoke/development/run-lifecycle-progress-fixtures.py --group readiness`
- Handoff context: SWU-ILP-002/003 receipts and current material schemas.

## Closeout

Use `../shared/CLOSEOUT-CONTRACT.md`. Task Session source is review-only here;
Sigil Development must approve its later consumer integration separately.

