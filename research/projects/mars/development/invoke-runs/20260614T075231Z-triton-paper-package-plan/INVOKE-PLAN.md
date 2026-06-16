# Invoke Plan - Triton Top2 Paper Package

Mode: `plan`
Complexity: `high`
Output mode: split work-pack plus task contracts.

## Objective

Create a MARS-governed paper package for the completed Triton Top2 backward
kernel research tower, including evidence inventory, traceability, paper
contract artifacts, data appendix, paper draft, and presentation readiness.

## Output Root

```text
research/projects/mars/papers/triton-top2-backward-kernel/
```

## Execution Waves

### W0 - Evidence Baseline

Layer: L0

Goal: identify and separate all evidence files.

Tasks:

- `TASK-TTP-001`: create evidence manifest and reference ledger.
- `TASK-TTP-002`: classify claims, non-claims, and raw validation data.

Gate:

- no paper drafting until every major claim has a source path.

### W1 - Paper Contract

Layer: L1

Goal: derive paper-design artifacts from MARS rules.

Tasks:

- `TASK-TTP-003`: create paper spec and section registry.
- `TASK-TTP-004`: create paper stories and paper test spec.
- `TASK-TTP-005`: create initial paper review.

Gate:

- no final prose until the paper test spec covers all claims and limitations.

### W2 - Paper Draft

Layer: L2

Goal: write the paper and data appendix from the contract.

Precondition:

- Lean formal-boundary lane completed or explicitly flagged as deferred.

Tasks:

- `TASK-TTP-006`: create data appendix and tables.
- `TASK-TTP-007`: draft `paper.md`.

Gate:

- every result table must link to raw evidence.

### W3 - Review And Presentation Package

Layer: L3

Goal: make the paper safe to present.

Tasks:

- `TASK-TTP-008`: run evidence-backed paper review.
- `TASK-TTP-009`: create presentation package and readiness note.

Gate:

- block presentation if unsupported novelty, hard Top2 differentiability, or
  production-performance claims appear.

## Validation Strategy

Use reviewable checks plus local commands:

```sh
test -f research/projects/mars/papers/triton-top2-backward-kernel/EVIDENCE-MANIFEST.md
test -f research/projects/mars/papers/triton-top2-backward-kernel/PAPER-SPEC.md
test -f research/projects/mars/papers/triton-top2-backward-kernel/PAPER-TEST-SPEC.md
test -f research/projects/mars/papers/triton-top2-backward-kernel/formal/FORMAL-VALIDATION-REPORT.md
cd research/projects/mars/papers/triton-top2-backward-kernel/formal && lake build
test -f research/projects/mars/papers/triton-top2-backward-kernel/paper.md
jq empty research/triton-top2-backward-kernel/development/task-sessions/*/evidence-index.json
jq empty research/triton-top2-backward-kernel/development/task-sessions/20260614T074500Z-w7-003-benchmark/artifacts/benchmark.json
rg -n "novel|hard Top2|production" research/projects/mars/papers/triton-top2-backward-kernel
```

Manual review checks:

- every paper claim has an evidence-manifest row;
- every benchmark number matches `benchmark.json`;
- every non-claim from `FINAL-PRIOR-ART-NOVELTY-REPORT.md` is preserved;
- Lean claims say proved/stubbed/deferred and never imply Triton implementation
  proof;
- no private unrelated repo material appears in the presentation package.

## Next Route

Run:

```text
task-session to research/projects/mars/development/invoke-runs/20260614T075231Z-triton-paper-package-plan/WORK-PACK.md --task TASK-TTP-001
```

Continue one task at a time until `TASK-TTP-009` passes.
