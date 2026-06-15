# Invoke Design - Triton Top2 Paper Package Through MARS

Mode: `design`
Complexity: `high`

## Design Goal

Use MARS as a publication/evidence harness to turn the completed Triton Top2
research tower into a traceable paper package.

The design keeps three layers separate:

1. MARS framework authority: how evidence and paper derivation are governed.
2. Triton case-study evidence: what was built, tested, benchmarked, and not
   claimed.
3. Paper-facing synthesis: how the work becomes a document a reader can review.

## Six-View Design

### 1. Artifact View

Create `research/projects/mars/papers/triton-top2-backward-kernel/` with:

- `PAPER-SPEC.md`
- `PAPER-STORIES.md`
- `PAPER-TEST-SPEC.md`
- `PAPER-REVIEW.md`
- `EVIDENCE-MANIFEST.md`
- `REFERENCE-LEDGER.md`
- `DATA-APPENDIX.md`
- `paper.md`

Optional supporting folders:

- `appendices/`
- `figures/`
- `data/`

### 2. Evidence View

Evidence must be divided into source classes:

| Class | Examples | Use |
| --- | --- | --- |
| MARS governance | `MARS-PIPELINE.md`, `PAPER-DERIVATION-RULES.md` | explains evidence/paper method |
| Triton final reports | `FINAL-PRIOR-ART-NOVELTY-REPORT.md`, `CAP2-W6-PARITY-REPORT.md` | claim boundary |
| Work-pack state | `WORK-PACK.md` | completion and task trace |
| Validation receipts | task-session `RESULT.md`, `evidence-index.json` | reproducibility |
| Benchmark data | W7 `benchmark.json`, `BENCHMARK.md`, `TRITON-BENCHMARK-REPORT.md` | quantitative results |
| Code/test surfaces | `reference/*.py`, `tests/*.py`, benchmark script | implementation evidence |

### 3. Paper View

The paper should be structured as:

1. Abstract
2. Problem and Non-Differentiability Background
3. Research Method and MARS Evidence Harness
4. Baselines and Prior Art Positioning
5. CAP2-v0 Relaxation and Exact Fixed-Load Backward
6. Formal Boundary Validation
7. Triton Implementation
8. Validation and Benchmark Results
9. Limitations and Non-Claims
10. Conclusion
11. Reproducibility Appendix

### 4. Traceability View

Every paper claim must map to:

- source artifact path;
- evidence class;
- support level;
- validation command or reviewable check;
- non-claim guard when applicable.

No claim should appear in `paper.md` unless `PAPER-TEST-SPEC.md` has a matching
obligation and `PAPER-REVIEW.md` marks it pass or explicit caveat.

### 5. Execution View

Execution should run through `task-session` one SWU at a time:

- inventory evidence;
- create paper contract artifacts;
- extract data tables;
- draft paper;
- review paper against evidence;
- close package readiness.

### 6. Risk View

Primary risks:

- overclaiming CAP2 novelty;
- overclaiming Lean as proof of Triton implementation correctness;
- treating smoke benchmark data as production performance;
- losing provenance by copying snippets without source paths;
- mixing canonical MARS assets with project-derived paper artifacts;
- leaking private or unrelated repository material into a paper package.

Mitigations:

- explicit claim/non-claim ledger;
- section-level paper test spec;
- evidence manifest with source paths;
- private/public boundary review before presentation;
- final review task that can block publication.
- formal-validation report with proved/stubbed/deferred statuses.

## Design Decisions

| Decision | Selection | Rationale |
| --- | --- | --- |
| Output owner | `research/projects/mars` | MARS owns evidence and paper lifecycle. |
| Technical corpus | `research/triton-top2-backward-kernel` | Completed case-study tower. |
| Canonical framework source | `implementation/mars` | Reusable definitions/templates are canonical there. |
| Paper format | Markdown first | Reviewable in repo, easy to convert later. |
| Claim posture | candidate, no novelty claim | Matches existing final report evidence. |
| Lean lane | add before paper draft | Useful for formal claim boundary, not implementation proof. |
