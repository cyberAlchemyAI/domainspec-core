# TASK-TTP-001 - Evidence Manifest And Reference Ledger

Status: `ready`
Layer: L0

## Objective

Create `EVIDENCE-MANIFEST.md` and `REFERENCE-LEDGER.md` under
`research/projects/mars/papers/triton-top2-backward-kernel/`.

## Write Scope

- `research/projects/mars/papers/triton-top2-backward-kernel/EVIDENCE-MANIFEST.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/REFERENCE-LEDGER.md`

## Implementation Detail

1. Create the output root if missing.
2. List MARS governance sources first.
3. List Triton technical evidence second.
4. List validation/task-session receipts third.
5. List code/test surfaces fourth.
6. Include source path, evidence class, use in paper, and current confidence.

## Smallest Working Units

| SWU ID | Goal | Done Criteria | Verification |
| --- | --- | --- | --- |
| SWU-TTP-001A | Create output root and evidence manifest skeleton. | Manifest has required columns and source classes. | `test -f .../EVIDENCE-MANIFEST.md` |
| SWU-TTP-001B | Populate reference ledger. | Ledger includes MARS and Triton source anchors. | review source paths |

## Validation

```sh
test -f research/projects/mars/papers/triton-top2-backward-kernel/EVIDENCE-MANIFEST.md
test -f research/projects/mars/papers/triton-top2-backward-kernel/REFERENCE-LEDGER.md
```

