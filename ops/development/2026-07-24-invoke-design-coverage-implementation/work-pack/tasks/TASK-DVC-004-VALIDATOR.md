# TASK-DVC-004: Design Selection Validator

- Slice/layer/wave: S1 / L1 / W1.
- Source: `../../../DESIGN.md#disposition-and-selection` and
  `#two-pass-fixed-point`.
- Dependencies: DVC-002C and DVC-003.
- Gap owned: DVC-G06.

## SWU-DVC-004

- Primary behavior: compute one total, deterministic, two-pass Design selection
  verdict.
- Independent acceptance: every denominator signal binds exactly once, owners
  and dispositions satisfy their contracts, selected outputs equal required
  outputs, and pass digests match.
- Candidate splits: precedence; ownership; disposition; output selection;
  fixed-point comparison.
- Retained boundary: they are conjuncts of one admission decision; partial pass
  has no authority.
- Write scope:
  `arcanum/spells/invoke/scripts/design_selection_validator.py`.
- Execution owner: local fallback under Spellcraft.

## Inputs and outputs

- Inputs: manifest, denominator receipt, authored concern records, predicate
  configuration, and planned witness contracts.
- Output: schema-valid selection result or deterministic blocking diagnostic.
- No network, model, Inventory, telemetry, or mutable cache input is allowed.

## Algorithm

```text
validate schemas and exact digest joins
reject stale/self-issued receipt
signals = union(authored concerns, extracted signals)
for signal in stable order:
    assign one primary class using documented precedence
    bind accountable/contributing/artifact/validator owners
    evaluate normalized required predicate
    assign one of four dispositions
    select output only when disposition == required
reject any unbound signal, unresolved owner, or unsupported state
canonicalize pass 1 and digest
repeat from original immutable inputs for pass 2
reject any changed concern, owner, disposition, output, diagnostic, or digest
emit design-validator-pass only after exact equality
```

## Diagnostics

Stable minimum codes:

`MANIFEST_NOT_CLOSED`, `MISSING_DETECTOR_INPUT`,
`STALE_DENOMINATOR_RECEIPT`, `SELF_ISSUED_RECEIPT`, `UNBOUND_SIGNAL`,
`OWNER_UNRESOLVED`, `FALSE_NA`, `ILLEGAL_SELECTION`,
`CHANGED_PASS_TWO`, `ILLEGAL_EVIDENCE_STATE`.

## Edge and failure cases

- taxonomy overlap before primary selection;
- recommendation without owner/evidence/revisit;
- N/A with prose but no negative signal;
- required concern missing output;
- selected output for recommendation/N/A;
- pass-one mutable ordering;
- planned fixture represented as executed evidence.

## Validation

```bash
python3 -m py_compile arcanum/spells/invoke/scripts/design_selection_validator.py
arcanum/spells/invoke/development/run-design-selection-fixtures.sh --group validator
arcanum/spells/invoke/development/run-design-selection-fixtures.sh --group mutations
```

## Closeout

Use the DVC-004 row. The receipt may claim only deterministic validator
behavior for the tested version.

## Completion evidence

- Result: pass after one bounded required-predicate invariant repair.
- Controls: bounded pass, stale join, self-issue, owner resolution, illegal
  selection, and changed pass two.
- Receipt: `../session-evidence/SWU-DVC-004/execution-receipt.json`.
