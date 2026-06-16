# Invoke Define - Triton Top2 Paper Package Through MARS

Mode: `plan-prep`
Target: paper-ready evidence package and paper version for the completed
`research/triton-top2-backward-kernel` work.

## User Intent

Create a governed plan for getting all completed Triton Top2 work into this
repository as a presentable document package. The package should separate every
file that evidences:

- what was researched;
- how the work was done;
- what was implemented;
- what was validated;
- what data was produced;
- what claims are supported or not supported;
- how `implementation/mars/` and `research/projects/mars/` govern the paper
  derivation.

The end state should include a paper version with research, methods, evidence,
data, and final claims.

## Target Boundary

Primary project owner:

- `research/projects/mars/`

Canonical reusable framework inputs:

- `implementation/mars/definitions/`
- `implementation/mars/templates/`

Case-study evidence corpus:

- `research/triton-top2-backward-kernel/`

Planned output root:

- `research/projects/mars/papers/triton-top2-backward-kernel/`

## Evidence Authority

MARS controls the publication workflow:

- canonical MARS definitions and templates live under `implementation/mars/`;
- `research/projects/mars` is the evidence workspace;
- paper derivation follows `implementation/mars/definitions/PAPER-DERIVATION-RULES.md`;
- paper work should be traceable through source catalog, reference ledger,
  evidence inventory, paper spec, paper test spec, paper review, and final paper.

The Triton tower controls the technical evidence:

- `WORK-PACK.md` is complete and says no ready tasks remain;
- `FINAL-PRIOR-ART-NOVELTY-REPORT.md` is the final technical claim boundary;
- `CAP2-W6-PARITY-REPORT.md` records fixed-load CAP2 exact-backward parity;
- `TRITON-BENCHMARK-REPORT.md` records smoke benchmark data;
- task-session evidence directories record validation receipts and artifacts.

## Claims Boundary

Supported claim:

```text
The project implemented and validated a Triton-backed exact backward path for a
fixed-load continuous Top2 routing relaxation, with PyTorch/manual VJP parity,
finite-difference checks, RunPod CUDA validation, and smoke benchmark evidence.
```

Unsupported claims:

- hard Top2 differentiability;
- CAP2 novelty;
- exact 2-sparsity;
- dynamic-load gradients;
- production-optimized performance;
- exhaustive benchmark scaling.

## Deliverable Set

The planned deliverables are:

- evidence manifest;
- source/reference ledger additions;
- paper derivation graph or registry seed;
- paper spec;
- paper stories;
- paper test spec;
- paper review;
- final paper draft;
- appendix/data package that links validation commands, benchmark JSON, and
  task-session evidence.

## Planning Status

No blocker-level decision is required to create the plan. Execution should
remain gated: the paper package must not be presented as publication-ready until
the evidence manifest, test spec, and review all pass.

