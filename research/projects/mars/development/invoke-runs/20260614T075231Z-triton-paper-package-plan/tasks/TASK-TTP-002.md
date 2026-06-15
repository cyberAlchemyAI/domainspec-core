# TASK-TTP-002 - Claim And Non-Claim Classification

Status: `pending`
Layer: L0

## Objective

Create supported-claim and non-claim guard tables from the evidence manifest.

## Write Scope

- `research/projects/mars/papers/triton-top2-backward-kernel/EVIDENCE-MANIFEST.md`
- optional `research/projects/mars/papers/triton-top2-backward-kernel/CLAIM-GUARDS.md`

## Implementation Detail

Extract supported claims from `FINAL-PRIOR-ART-NOVELTY-REPORT.md`,
`CAP2-W6-PARITY-REPORT.md`, and `TRITON-BENCHMARK-REPORT.md`.

Every claim row must include:

- claim text;
- support artifact;
- support level;
- validation or review check;
- paper section target.

Every non-claim row must include:

- prohibited or caveated claim;
- source report enforcing the guard;
- wording to use instead.

## Smallest Working Units

| SWU ID | Goal | Done Criteria | Verification |
| --- | --- | --- | --- |
| SWU-TTP-002A | Create supported claim table. | Each supported claim maps to evidence. | review table |
| SWU-TTP-002B | Create non-claim guard table. | Guards include hard Top2, novelty, exact 2-sparsity, dynamic load, production perf. | `rg -n "novel|hard Top2|production" ...` |

## Validation

Review `FINAL-PRIOR-ART-NOVELTY-REPORT.md` non-claims against the paper package
claim guards.

