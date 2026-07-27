# TASK-DVC-003: Independent Scope Extractor

- Slice/layer/wave: S1 / L1 / W1.
- Source: `../../../DESIGN.md#independent-extraction`.
- Dependencies: DVC-002A and DVC-002B.
- Gap owned: DVC-G05.

## SWU-DVC-003

- Primary behavior: emit deterministic normalized signals and one denominator
  receipt for an exact manifest.
- Independent acceptance: the same canonical input produces the same ordered
  signals and receipt digest; every omitted or unreadable class blocks with an
  exact diagnostic.
- Candidate splits: selector loading; signal normalization; canonical sort;
  digest; receipt output.
- Retained boundary: each is a stage of one extraction function and none
  produces an independently meaningful denominator.
- Write scope:
  `arcanum/spells/invoke/scripts/design_scope_extractor.py`.
- Execution owner: local fallback under Spellcraft.

## Inputs and outputs

- Input: schema-valid manifest JSON plus repository root.
- Output: schema-valid denominator receipt JSON to an explicit caller path.
- State: read-only repository selectors; no cache or durable authority.

## Algorithm

```text
load manifest -> validate shape
reject author identity == detector identity
for every declared field class:
    resolve exact selectors within repository root
    reject missing, escaping, unresolved, or digest-mismatched selector
    normalize each item into stable signal_id, class, selector, source_digest
reject duplicate signal ids
union authored concern ids with extracted signal ids
sort all sets canonically
compute receipt digest excluding receipt_digest
emit pass only when missing_detector_inputs and unbound_signal_ids are empty
```

The extractor reports signals; it does not choose primary concern,
disposition, owner, companion, evidence state, or promotion.

## Edge and failure cases

- symlink/path escape;
- duplicate normalized selector;
- omitted manifest field class;
- input changes during read;
- unsupported selector kind;
- author/detector identity collapse;
- partial output after failure.

On failure, write no pass receipt. A diagnostic output may be emitted only to
the explicit output path.

## Validation

```bash
python3 -m py_compile arcanum/spells/invoke/scripts/design_scope_extractor.py
arcanum/spells/invoke/development/run-design-selection-fixtures.sh --group extractor
git diff --check -- arcanum/spells/invoke/scripts/design_scope_extractor.py
```

## Closeout

Receipt must include input/output digests, fixture groups, files touched, and
the non-authority statement. Use the DVC-003 synchronization row.

## Completion evidence

- Result: pass after one bounded diagnostic-order repair.
- Controls: deterministic replay, missing field, self-issue, path escape,
  duplicate signal, and exact staged-byte parity.
- Receipt: `../session-evidence/SWU-DVC-003/execution-receipt.json`.
