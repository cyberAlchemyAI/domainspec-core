# Work Pack - Triton Top2 Paper Package

Status: `complete-ready-for-review`

Owner: `research/projects/mars`

## Objective

Create a MARS-governed paper package for the completed Triton Top2 backward
kernel research tower.

## Output Root

`research/projects/mars/papers/triton-top2-backward-kernel/`

## Task Matrix

| Task ID | Wave | Objective | Dependencies | Status | Validation |
| --- | --- | --- | --- | --- | --- |
| [TASK-TTP-001](tasks/TASK-TTP-001.md) | W0 | Create evidence manifest and reference ledger. | none | pass | manifest paths and source classes review |
| [TASK-TTP-002](tasks/TASK-TTP-002.md) | W0 | Classify claims, non-claims, and raw validation data. | TASK-TTP-001 | pass | claim table maps to evidence |
| [TASK-TTP-003](tasks/TASK-TTP-003.md) | W1 | Create paper spec and section registry. | TASK-TTP-002 | pass | paper sections have required inputs |
| [TASK-TTP-004](tasks/TASK-TTP-004.md) | W1 | Create paper stories and paper test spec. | TASK-TTP-003 | pass | every claim has a test obligation |
| [TASK-TTP-005](tasks/TASK-TTP-005.md) | W1 | Create initial paper review. | TASK-TTP-004 | pass | review verdicts pass/flag/block each section |
| [TASK-TTP-005L](tasks/TASK-TTP-005L.md) | W1L | Verify Lean setup and create formal validation scaffold. | TASK-TTP-005 | pass | local Lean/Lake build |
| [TASK-TTP-005M](tasks/TASK-TTP-005M.md) | W1L | Add Lean boundary proof slice and formal validation report. | TASK-TTP-005L | pass | Lean build plus proved/stubbed/deferred report |
| [TASK-TTP-006](tasks/TASK-TTP-006.md) | W2 | Create data appendix and result tables. | TASK-TTP-005M | pass | benchmark numbers match raw JSON |
| [TASK-TTP-007](tasks/TASK-TTP-007.md) | W2 | Draft paper narrative. | TASK-TTP-006 | pass | paper draft cites evidence manifest |
| [TASK-TTP-008](tasks/TASK-TTP-008.md) | W3 | Run evidence-backed paper review. | TASK-TTP-007 | pass | paper test spec review passes or flags residuals |
| [TASK-TTP-009](tasks/TASK-TTP-009.md) | W3 | Create presentation package and readiness note. | TASK-TTP-008 | pass | presentation package has no unsupported claims |

## SWU Manifest

| SWU ID | Parent Task | Goal | Write Scope | Verification |
| --- | --- | --- | --- | --- |
| SWU-TTP-001A | TASK-TTP-001 | Create output root and evidence manifest skeleton. | `research/projects/mars/papers/triton-top2-backward-kernel/` | review file exists |
| SWU-TTP-001B | TASK-TTP-001 | Populate reference ledger from MARS and Triton artifacts. | paper package only | review source paths |
| SWU-TTP-002A | TASK-TTP-002 | Create supported claim table. | paper package only | claims map to evidence |
| SWU-TTP-002B | TASK-TTP-002 | Create non-claim guard table. | paper package only | non-claims match final report |
| SWU-TTP-003A | TASK-TTP-003 | Create section registry. | `PAPER-SPEC.md` | all sections have inputs |
| SWU-TTP-004A | TASK-TTP-004 | Create reader stories. | `PAPER-STORIES.md` | stories cover sections |
| SWU-TTP-004B | TASK-TTP-004 | Create paper test spec. | `PAPER-TEST-SPEC.md` | obligations cover claims |
| SWU-TTP-005A | TASK-TTP-005 | Create initial review. | `PAPER-REVIEW.md` | each section has verdict |
| SWU-TTP-005L-A | TASK-TTP-005L | Verify Lean tooling and pin version. | `formal/` | `lean --version && lake --version` |
| SWU-TTP-005L-B | TASK-TTP-005L | Scaffold Lake project. | `formal/` | `lake build` |
| SWU-TTP-005L-C | TASK-TTP-005L | Create formal report skeleton. | `formal/FORMAL-VALIDATION-REPORT.md` | report exists |
| SWU-TTP-005M-A | TASK-TTP-005M | Encode fixed-boundary definitions. | `formal/TritonTop2/*.lean` | `lake build` |
| SWU-TTP-005M-B | TASK-TTP-005M | Add first proof/stub targets. | `formal/TritonTop2/*.lean` | report marks PO status |
| SWU-TTP-005M-C | TASK-TTP-005M | Integrate paper-facing report. | `formal/FORMAL-VALIDATION-REPORT.md` | proved/stubbed/deferred table |
| SWU-TTP-006A | TASK-TTP-006 | Extract benchmark and validation tables. | `DATA-APPENDIX.md` | JSON values match |
| SWU-TTP-007A | TASK-TTP-007 | Draft paper. | `paper.md` | evidence citations present |
| SWU-TTP-008A | TASK-TTP-008 | Review paper against test spec. | `PAPER-REVIEW.md` | unsupported claims absent |
| SWU-TTP-009A | TASK-TTP-009 | Create presentation readiness note. | `PRESENTATION-PACKAGE.md` | private/public review checklist complete |

## Source Anchors

MARS governance:

- `implementation/mars/definitions/MARS-PIPELINE.md`
- `implementation/mars/definitions/PAPER-DERIVATION-RULES.md`
- `research/projects/mars/README.md`
- `research/projects/mars/registry/ARTIFACT-INDEX.md`
- `research/projects/mars/registry/TRACEABILITY-MATRIX.md`

Triton tower:

- `research/triton-top2-backward-kernel/WORK-PACK.md`
- `research/triton-top2-backward-kernel/FINAL-PRIOR-ART-NOVELTY-REPORT.md`
- `research/triton-top2-backward-kernel/CAP2-W6-PARITY-REPORT.md`
- `research/triton-top2-backward-kernel/TRITON-BENCHMARK-REPORT.md`
- `research/triton-top2-backward-kernel/FORMAL-MATH-SPEC.md`
- `research/triton-top2-backward-kernel/FORMAL-MATH-STUBS.md`
- `research/triton-top2-backward-kernel/development/task-sessions/*/RESULT.md`
- `research/triton-top2-backward-kernel/development/task-sessions/*/evidence-index.json`

Implementation/test surfaces:

- `research/triton-top2-backward-kernel/reference/router_torch.py`
- `research/triton-top2-backward-kernel/reference/router_triton.py`
- `research/triton-top2-backward-kernel/tests/test_router_torch.py`
- `research/triton-top2-backward-kernel/tests/test_router_triton.py`
- `research/triton-top2-backward-kernel/scripts/benchmark_triton_paths.py`

## Gates

- G1: no paper claim without evidence-manifest row.
- G2: no novelty claim unless explicitly supported by prior-art evidence.
- G3: no hard Top2 differentiability claim.
- G4: no presentation package until paper review passes or residuals are
  explicitly labeled.

## Current State

Next ready task: none.

Execution receipt:
`research/projects/mars/development/task-sessions/20260614T081500Z-triton-paper-package-all-tasks/RESULT.md`.

Lean tooling note: local `elan`, `lean`, and `lake` are available. The
repo-owned Lake project under the paper package builds successfully.
