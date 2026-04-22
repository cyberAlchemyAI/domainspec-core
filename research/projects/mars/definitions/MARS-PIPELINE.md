# MARS Research Pipeline v1 (12 Stages)

This document defines the canonical pipeline for the MARS research program.

Primary objective: system validity with explicit governance gates and traceable evidence.

## Pipeline Stages

| Stage | Name | Owner | Inputs | Outputs | Tier |
|---|---|---|---|---|---|
| S1 | Methodology Profile Selection | Scientist | Research objective, constraints | Method profile (foundation or full) | Foundation + Full |
| S2 | Claim Framing and Questions | Scientist | Paper scope, prior evidence | Claims and research questions | Foundation + Full |
| S3 | Protocol Design and Validation | Protocol Designer | Claims, experiment intent, existing templates | Protocol file, measurable criteria, schema | Foundation + Full |
| S4 | Source Discovery and Scoring | Sourcer | Protocol requirements | Source candidates and ranked selection | Foundation + Full |
| S5 | Source Quality Gate | Sourcer | Candidate sources | Pass/fail decision with version pins | Foundation + Full |
| S6 | Inventory Extraction and Readiness Gate | Inventorist | Selected sources, prior inventory | Inventory readiness report | Foundation + Full |
| S7 | Experiment Execution and Data Capture | Scientist | Protocol, source and inventory ready | Raw JSONL run file(s) | Foundation + Full |
| S8 | Data Integrity Audit | Analyst | Raw JSONL and schema | Integrity report, gate decision | Foundation + Full |
| S9 | Core Statistical Evaluation | Analyst | Clean data, success criteria | Descriptive + criteria pass/fail table | Foundation + Full |
| S10 | Deep Analysis Pack | Analyst | Clean data, related results | Subgroups, sensitivity, triangulation, threats | Full |
| S11 | Claim Adjudication and Evidence Update | Evidence Auditor | Analysis outputs, claim map | Claim evidence status and experiment priority updates | Foundation + Full |
| S12 | Paper Integration and Retrospective | Scientist | Evidence status and findings | Paper updates, retrospective actions | Full |

## Tiered Rigor Policy

### Foundation tier

Use for early or low-cost experiments where primary goal is directional validity.

Required stages:
- S1 through S9
- S11

Optional stage:
- S10

### Full tier

Use for high-impact experiments and publication-critical claims.

Required stages:
- S1 through S12

## Hard Governance Gates

Execution is blocked when any hard gate fails.

| Gate | Condition | Enforced at |
|---|---|---|
| G1 | Protocol approved and measurable | S3 |
| G2 | Source selection includes accessibility, depth, version pin | S5 |
| G3 | Inventory readiness confirmed for required entry types | S6 |
| G4 | Data integrity pass (schema and metadata) | S8 |

## Required Artifacts by Stage

| Stage | Required Artifact |
|---|---|
| S3 | `research/experiments/*/experiments/<id>.md` |
| S4-S5 | `research/experiments/*/sources/<id>-sources.md` |
| S6 | `research/experiments/*/inventory/INVENTORY-INDEX.md` and source entries |
| S7 | `research/experiments/*/data/<id>-run-YYYY-MM-DD.jsonl` |
| S8-S10 | `research/experiments/*/results/<id>-results.md` |
| S11 | `research/MARS-EVIDENCE-STATUS.md` |
| S12 | Paper section update + retrospective note |

Protocol gate template:

- `research/MARS-PROTOCOL-CHECKLIST.md`

## Default Handoff Chain

1. Sourcer -> source selection and quality gate.
2. Inventorist -> inventory readiness gate.
3. Scientist -> execution and data capture.
4. Analyst -> integrity plus analysis outputs.
5. Evidence Auditor -> claim status update and next-run priorities.
6. Scientist -> paper integration and retrospective closure.
