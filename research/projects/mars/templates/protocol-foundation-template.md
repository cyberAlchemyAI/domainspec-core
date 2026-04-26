# EX: [Experiment Title]

**Status:** draft
**Tier:** foundation
**Paper Claim:** C1 | C2 | C3 | C4
**Paper Section:** [section reference]
**Priority:** P0 | P1 | P2

---

## Objective

[One clear statement of what this experiment validates.]

## Methodology Profile

- Method profile path: `experiments/<experiment-key>/methodology.md`
- Method contract: `definitions/METHODOLOGY-PROFILE-CONTRACT.md`
- Tier: foundation
- Primary framework: [for example Wohlin + GQM]
- Validity plan: [internal, external, construct, conclusion]

## Protocol

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Claim Mapping

| Claim ID | Research Question | Expected Signal |
|---|---|---|
| Cx | [question] | [signal] |

## Definition Anchors

- Definitions index path: `definitions/DEFINITIONS-INDEX.md`
- Referenced definition IDs: [MARS-DEF-...]

## Reference Anchors

- Reference ledger path: `sources/REFERENCE-LEDGER.md`
- Authoritative references used by this protocol: [REF-...]

## Context Bundle

- Context bundle path: `experiments/<experiment-key>/context.md`
- Template: `templates/context-bundle-template.md`

## Data Schema

- Schema file: `templates/schema-foundation-template.json`
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
| G1 | Methodology-linked protocol measurable with definition/context anchors and schema complete | checklist + methodology path + definitions + context + schema path | pass/pending/blocked |
| G2 | Sources validated and pinned | EX-sources file | pass/pending/blocked |
| G3 | Inventory readiness confirmed | readiness report | pass/pending/blocked |
| G4 | Data integrity pass | integrity report | pass/pending/blocked |

## Artifact Paths

- Experiment bundle root: `experiments/<experiment-key>/`
- Methodology profile: `experiments/<experiment-key>/methodology.md`
- Protocol: `experiments/<experiment-key>/protocol.md`
- Source selection: `experiments/<experiment-key>/sources.md`
- Context bundle: `experiments/<experiment-key>/context.md`
- Raw data: `experiments/<experiment-key>/data/run-YYYY-MM-DD[-suffix].jsonl`
- Results: `experiments/<experiment-key>/results/<run-id>-results.md`

## Notes

[Record assumptions, constraints, and known risks.]
