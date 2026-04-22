# EX: [Experiment Title]

**Status:** draft
**Tier:** foundation
**Paper Claim:** C1 | C2 | C3 | C4
**Paper Section:** [section reference]
**Priority:** P0 | P1 | P2

---

## Objective

[One clear statement of what this experiment validates.]

## Protocol

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Claim Mapping

| Claim ID | Research Question | Expected Signal |
|---|---|---|
| Cx | [question] | [signal] |

## Data Schema

- Schema file: `research/experiments/templates/schema-foundation-template.json`
- Row target: [expected rows]
- Sampling plan: [how rows are collected]

## Source Requirements

| Source ID | Type | Why needed | Version Pin |
|---|---|---|---|
| [id] | [type] | [reason] | [pin] |

## Inventory Requirements

| Entry Type | Required? | Notes |
|---|---|---|
| domain-model | yes/no | [notes] |
| paper-abstract | yes/no | [notes] |
| tool-evaluation | yes/no | [notes] |
| framework-architecture | yes/no | [notes] |
| role-definition | yes/no | [notes] |

## Success Criteria

| ID | Metric | Threshold | Pass Rule |
|---|---|---|---|
| SC-1 | [metric] | [target] | [rule] |
| SC-2 | [metric] | [target] | [rule] |

## Analysis Path

Foundation tier minimum analysis:
- Data integrity
- Descriptive statistics
- Success criteria evaluation
- Claim adjudication

Optional in foundation:
- Deep subgroup/sensitivity/triangulation package

## Hard Gate Checklist

| Gate | Condition | Evidence | Decision |
|---|---|---|---|
| G1 | Protocol measurable and schema complete | checklist + schema path | pass/pending/blocked |
| G2 | Sources validated and pinned | EX-sources file | pass/pending/blocked |
| G3 | Inventory readiness confirmed | readiness report | pass/pending/blocked |
| G4 | Data integrity pass | integrity report | pass/pending/blocked |

## Artifact Paths

- Protocol: `research/experiments/experiments/<id>.md`
- Source selection: `research/experiments/sources/<id>-sources.md`
- Raw data: `research/experiments/data/<id>-run-YYYY-MM-DD.jsonl`
- Results: `research/experiments/results/<id>-results.md`

## Notes

[Record assumptions, constraints, and known risks.]
