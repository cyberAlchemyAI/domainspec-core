# W4 — Integrate and independently verify

## Question

Do the required checks fail closed and produce independently replayable evidence for the bounded backend claim and its two read-only consumer proofs?

## Sequence

1. SWU-BTE-008 — integrate the required-check manifest, command, negative cases, and receipt.
2. SWU-BTE-010 — bind the BTE, IOLM, Body War, and Craft receipts into one exact manifest.
3. TASK-BTE-VERIFY — independent closure replay under its execution-unit exemption.

## Entry gate

- W3 exact-set, execution, and mutation receipts pass.

## Exit gate

- The canonical command rejects missing, empty, stale, skipped, undiscovered, and mutation-surviving evidence.
- Independent replay reconciles all exact sets and digests.
- The receipt states only the conservative backend profile plus integrated consumer-proof contract for the approved candidate profile/version.
- Release and admission decisions remain with their owning gates.

## Promotion

Return the independent verdict to FPR-02B/FPR-04 ownership and run Invoke Refresh. Do not auto-promote a passing technical receipt into release authorization.
