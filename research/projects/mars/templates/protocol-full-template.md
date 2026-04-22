# EX: [Experiment Title]

**Status:** draft
**Tier:** full
**Paper Claim:** C1 | C2 | C3 | C4
**Paper Section:** [section reference]
**Priority:** P0 | P1 | P2

---

## Objective

[One clear statement of what this experiment validates, including publication impact.]

## Protocol

1. [Step 1]
2. [Step 2]
3. [Step 3]
4. [Deep analysis setup]

## Claim Mapping

| Claim ID | Research Question | Expected Signal | Paper Impact |
|---|---|---|---|
| Cx | [question] | [signal] | [section change] |

## Data Schema

- Schema file: `templates/schema-full-template.json`
- Row target: [expected rows]
- Sampling plan: [how rows are collected]
- Subgroup dimensions: [list]

## Source Requirements

| Source ID | Type | Role | Why needed | Version Pin |
|---|---|---|---|---|
| [id] | [type] | primary/supporting | [reason] | [pin] |

## Inventory Requirements

| Entry Type | Required? | Coverage Target |
|---|---|---|
| domain-model | yes/no | [target] |
| paper-abstract | yes/no | [target] |
| tool-evaluation | yes/no | [target] |
| framework-architecture | yes/no | [target] |
| role-definition | yes/no | [target] |

## Success Criteria

| ID | Metric | Threshold | Pass Rule |
|---|---|---|---|
| SC-1 | [metric] | [target] | [rule] |
| SC-2 | [metric] | [target] | [rule] |
| SC-3 | [metric] | [target] | [rule] |

## Analysis Path

Full tier requires:
- Data integrity
- Descriptive statistics
- Success criteria evaluation
- Subgroup analysis
- Gap taxonomy
- Sensitivity analysis
- Triangulation
- Validity threats
- Claim adjudication
- Synthesis and paper integration

## Hard Gate Checklist

| Gate | Condition | Evidence | Decision |
|---|---|---|---|
| G1 | Protocol measurable and schema complete | checklist + schema path | pass/pending/blocked |
| G2 | Sources validated and pinned | EX-sources file + catalog pins | pass/pending/blocked |
| G3 | Inventory readiness confirmed | readiness report + index links | pass/pending/blocked |
| G4 | Data integrity pass | integrity report + schema validation | pass/pending/blocked |

## Artifact Paths

- Experiment bundle root: `experiments/<experiment-key>/`
- Protocol: `experiments/<experiment-key>/protocol.md`
- Source selection: `experiments/<experiment-key>/sources.md`
- Raw data: `experiments/<experiment-key>/data/run-YYYY-MM-DD[-suffix].jsonl`
- Results: `experiments/<experiment-key>/results/<run-id>-results.md`
- Claim evidence: `results/MARS-EVIDENCE-STATUS.md`
- Paper updates: `papers/<paper-file>.md`

## Publication Notes

- Planned section updates: [list]
- Expected claim-strength change: [supported/partial/insufficient/contradicted]
- Threats requiring explicit discussion: [list]
