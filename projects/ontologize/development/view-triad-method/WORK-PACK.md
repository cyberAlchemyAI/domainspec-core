---
module: ontologize-view-triad-method
version: current
status: draft
updatedAt: 2026-06-15
docType: work-pack
---

# WORK-PACK: Ontologize View-Triad Method

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass-for-planning | Ready for task-session planning execution; product-doc mutation remains blocked until L0 evidence passes. |
| complexity | medium | Crosses method, artifacts, validation, and skill routing, but stays in docs/method scope. |
| outputMode | split | Task contracts and wave contracts are included. |
| executionPackRef | [EXECUTION-PACK.md](EXECUTION-PACK.md) | Required for medium complexity. |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | L0-L3 boundary source. |
| activeLayerWindow | L0 | Start with method boundary. |
| lastUpdatedAt | 2026-06-15 | Initial pack creation. |
| readinessProfile | pilot | Target is method pilot readiness. |

## Objective Summary

- Objective: make the view triad a repeatable Ontologize method with safe implementation sequence, branch materialization, and validation gates.
- Primary inputs: Ontologize docs, sibling view skills, existing optimization-chain method, `ONTOLOGY-BRANCHES.md`, and `DAG-AND-METRICS.md`.
- Success condition: a pilot triad can be authored and validated with B1/B2/B3/B4 coverage, no product-doc drift, and no double decision.

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S0 | Method boundary, source matrix, and Branch Materialization Register. | L0 | [W0](work-pack/waves/W0.md) | none | Source matrix, B1/B2/B3/B4 coverage profile, and mutation boundary reviewed. |
| S1 | Method artifact plus branch-aware system-view shell. | L0/L1 | [W1](work-pack/waves/W1.md) | S0 | No verdicts in system-view shell; branch-shaped stances named. |
| S2 | Engineer-view decision inventory. | L1 | [W1](work-pack/waves/W1.md) | S1 | One row per stance or branch boundary; authorities verified or struck; B3 decisions explicit. |
| S3 | Ontology-view typed model. | L1 | [W2](work-pack/waves/W2.md) | S2 | Node/edge/guard checklist complete; B4 bridge edges catalogued or blocked. |
| S4 | Integration, validation, readiness. | L2/L3 | [W3](work-pack/waves/W3.md) | S3 | Branch gates, claim trace, and validation report pass or carry blockers. |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Waves | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [TASK-VTM-001](work-pack/tasks/TASK-VTM-001-METHOD-BOUNDARY.md) | Establish method boundary, source matrix, and branch materialization register. | L0 | medium | W0 | [SPEC.md](SPEC.md), [DESIGN.md](DESIGN.md), [BRANCH-MATERIALIZATION.md](BRANCH-MATERIALIZATION.md) | ready | not-started |
| [TASK-VTM-002](work-pack/tasks/TASK-VTM-002-SYSTEM-VIEW.md) | Author method artifact and system-view pilot shell. | L0/L1 | medium | W1 | `system-view` skill, [PLAN.md](PLAN.md) | ready-after-001 | not-started |
| [TASK-VTM-003](work-pack/tasks/TASK-VTM-003-ENGINEER-VIEW.md) | Author engineer-view decision inventory. | L1 | medium | W1 | `engineer-view` skill | ready-after-002 | not-started |
| [TASK-VTM-004](work-pack/tasks/TASK-VTM-004-ONTOLOGY-VIEW.md) | Author ontology-view typed model. | L1 | medium | W2 | `ontology-view` skill | ready-after-003 | not-started |
| [TASK-VTM-005](work-pack/tasks/TASK-VTM-005-INTEGRATION-VALIDATION.md) | Integrate, validate, and prepare readiness route. | L2/L3 | medium | W3 | [OPTIMIZATION-CHAIN-METHOD.md](../../OPTIMIZATION-CHAIN-METHOD.md), [SKILL-ROUTING.md](SKILL-ROUTING.md) | ready-after-004 | not-started |

## SWU Execution Handoff

| SWU ID | Parent Task | Source Anchors | Related Context | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-VTM-001 | [TASK-VTM-001](work-pack/tasks/TASK-VTM-001-METHOD-BOUNDARY.md) | [SPEC.md](SPEC.md), [DESIGN.md](DESIGN.md), [BRANCH-MATERIALIZATION.md](BRANCH-MATERIALIZATION.md), [SKILL-ROUTING.md](SKILL-ROUTING.md) | Ontologize root docs listed in README source boundary; `ONTOLOGY-BRANCHES.md`; `DAG-AND-METRICS.md`. | none | `projects/ontologize/development/view-triad-method/` and proposed `projects/ontologize/view-triad/README.md` only if path approved. | Source matrix, Branch Materialization Register, output path, dispatch mode, and mutation boundary recorded. | Boundary artifact with no product-facing mutations; B1/B2/B3/B4 rows covered or blocked. | Review all links, branch register rows, and boundary decisions. | local-fallback | ready |
| SWU-VTM-002 | [TASK-VTM-002](work-pack/tasks/TASK-VTM-002-SYSTEM-VIEW.md) | `implementation/domainspec/.claude/skills/system-view/SKILL.md`, [BRANCH-MATERIALIZATION.md](BRANCH-MATERIALIZATION.md) | Ontologize product/spec/design docs and branch register. | SWU-VTM-001 | proposed `projects/ontologize/VIEW-TRIAD-METHOD.md`, `projects/ontologize/view-triad/system-view.md` | Method artifact draft and branch-aware system-view shell exist. | Stance table present; B1/B2/B3/B4 stakes named; verdicts stated count is 0. | Manual review using system-view output contract and B1/B2/B3/B4 gate list. | local-fallback | blocked-until-001 |
| SWU-VTM-003 | [TASK-VTM-003](work-pack/tasks/TASK-VTM-003-ENGINEER-VIEW.md) | `implementation/domainspec/.claude/skills/engineer-view/SKILL.md`, [BRANCH-MATERIALIZATION.md](BRANCH-MATERIALIZATION.md) | System-view stances and branch register from SWU-VTM-002. | SWU-VTM-002 | `projects/ontologize/view-triad/engineer-view.md` | Decision inventory has exactly one row per stance or branch-boundary decision; B3 denominator/lifecycle decisions explicit. | Authority verification table, struck-authority list, B3 run-context record, and B4 owner-decision route table. | Manual review using engineer-view output contract and B3/B4 authority map. | local-fallback | blocked-until-002 |
| SWU-VTM-004 | [TASK-VTM-004](work-pack/tasks/TASK-VTM-004-ONTOLOGY-VIEW.md) | `implementation/domainspec/.claude/skills/ontology-view/SKILL.md`, [BRANCH-MATERIALIZATION.md](BRANCH-MATERIALIZATION.md), `DAG-AND-METRICS.md` | Engineer-view decision rows from SWU-VTM-003. | SWU-VTM-003 | `projects/ontologize/view-triad/ontology-view.md` | Typed branch node/edge model, B4 bridge ledger, and forbidden-edge guard table exist. | Coined/proposed edges carry routes or blockers; raw drift is not treated as adjudicated contradiction. | Manual review using ontology-view output contract and edge catalog. | local-fallback | blocked-until-003 |
| SWU-VTM-005 | [TASK-VTM-005](work-pack/tasks/TASK-VTM-005-INTEGRATION-VALIDATION.md) | [OPTIMIZATION-CHAIN-METHOD.md](../../OPTIMIZATION-CHAIN-METHOD.md), [BRANCH-MATERIALIZATION.md](BRANCH-MATERIALIZATION.md), [SKILL-ROUTING.md](SKILL-ROUTING.md) | Full pilot triad and branch register. | SWU-VTM-004 | `projects/ontologize/view-triad/validation-report.md`, proposed patches only for product docs | Validation report and integration proposal exist. | Sample BI claim trace cites branch register, triad, and optimization chain. | Manual review plus `rg` checks for restated verdict/definition markers and branch gate failures. | local-fallback | blocked-until-004 |

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action | Target Date |
| --- | --- | --- | --- | --- | --- |
| B-VTM-001 | product-doc integration | Product/public docs should not be edited before L0 boundary passes. | task-session executor | Complete SWU-VTM-001 and seek owner approval if integration is desired. | open |
| B-VTM-002 | subagent dispatch | Multi-agent run requires operator approval. | owner/operator | Keep default local path unless contested/high-risk. | open |

## Gate Checks

1. L0 must pass before any edit outside development pack or proposed pilot triad path.
2. Every non-exempt SWU must keep source anchors, write scope, done criteria, and validation surface.
3. Any system-view stance without engineer-view row blocks publication.
4. Any RESOLVED engineer-view row without verified authority blocks publication.
5. Any ontology-view coined edge without route blocks publication.
6. Any missing B3 run boundary, denominator, lifecycle state, scope/posture, or stage-vs-outcome check blocks publication.
7. Any B4 bridge claim that bypasses the edge catalog, lacks owner-decision route, or collapses raw drift into adjudicated contradiction blocks promotion.
8. Product-facing integration remains proposal-only until owner-approved.

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-06-15 | Initial invoke development pack created. | Codex |
| 2026-06-15 | Refined method with branch materialization register, B3 run-context gate, and B4 bridge ledger. | Codex |
