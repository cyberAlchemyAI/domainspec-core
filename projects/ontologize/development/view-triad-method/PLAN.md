# PLAN - Ontologize View-Triad Method

Implementation plan for [SPEC.md](SPEC.md), [DESIGN.md](DESIGN.md), [BRANCH-MATERIALIZATION.md](BRANCH-MATERIALIZATION.md), and [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md). Complexity: medium. Execution owner: `task-session`.

## Delivery Slices And Validation Strategy

| Slice | Layer | Outcome | Validation |
| --- | --- | --- | --- |
| S0 Method boundary | L0 | Scope, output path, source matrix, Branch Materialization Register, and mutation boundary settled. | Review confirms no product-facing docs were changed, all source anchors are listed, and B1/B2/B3/B4 rows exist or carry blockers. |
| S1 Method artifact | L0 | `VIEW-TRIAD-METHOD.md` draft. | Method names required sequence, branch gates, and sibling division of law. |
| S2 Ontologize pilot triad | L1 | `branch-materialization-register.md`, `system-view.md`, `engineer-view.md`, `ontology-view.md`, and validation report. | Stance coverage, branch coverage, B3 record, B4 ledger, authority verification, ontology guard checklist pass or carry explicit blockers. |
| S3 Integration pattern | L2 | Optimization-chain and deliverable citation pattern. | Sample BI claim traces to branch register -> shape/verdict/ontology -> optimization chain without deciding twice. |
| S4 Repeatability/readiness | L3 | Second-run checklist, signals/reflection plan, readiness result. | Method can be rerun on another safe corpus with the same validation gates. |

## Implementation-Detail Specs

### IDS-VTM-001 Method boundary procedure

- Inputs: Ontologize source docs, `ONTOLOGY-BRANCHES.md`, `DAG-AND-METRICS.md`, sibling view skill files, existing product/public artifacts.
- Outputs: source matrix, Branch Materialization Register, output path decision, dispatch mode, mutation boundary.
- Ordered rules:
  1. Resolve target and audience.
  2. List source artifacts by role: product scope, method, branch definitions, edge catalog, glossary, design, plan, work-pack, sibling law.
  3. Create Branch Materialization Register rows for B1/B2/B3/B4.
  4. Record B3 run-context row fields and B4 bridge ledger candidates when evidence exists.
  5. Decide whether product-facing docs are blocked, proposed, or approved for mutation.
  6. Choose output path for pilot triad.
  7. Choose dispatch mode; default `single`.
  8. Record any blocker requiring `domainspec-decision-gate`.
- Edge cases: user asks for immediate public mutation; keep it blocked until L0 evidence exists unless explicitly approved.
- Validation evidence: reviewer can reproduce the source boundary and branch coverage profile without reading the whole repo.

### IDS-VTM-002 View triad authoring procedure

- Inputs: source matrix, `system-view`, `engineer-view`, `ontology-view` skill files.
- Outputs: branch-aware pilot view artifacts and validation report.
- Ordered rules:
  1. System-view extracts shape layers and names branch-shaped stances; it must not state verdicts.
  2. Engineer-view harvests stances and writes exactly one decision row per stance or branch-boundary decision.
  3. Engineer-view verifies authorities on disk; unverifiable RESOLVED rows become OPEN.
  4. Engineer-view records B3 denominator/lifecycle/run-boundary decisions and B4 owner-decision routes.
  5. Ontology-view types branch terms, nodes, edges, and forbidden relations from the source and decision inventory.
  6. Ontology-view checks B4 bridge edges against the catalog and separates raw drift from adjudicated contradiction.
  7. Validation checks cross-references, no duplicated verdicts, no redefined terms, no missing B3 record, no unrouteable coined edges, and no unowned contradiction blockers.
- Edge cases: missing engineer-view row stays provisional in system-view and blocks publication, not drafting.
- Validation evidence: branch coverage table, stance coverage table, B3 run-context record, B4 bridge ledger, authority-strike list, typed edge/guard table.

### IDS-VTM-003 Integration procedure

- Inputs: pilot triad, `OPTIMIZATION-CHAIN-METHOD.md`, deliverable docs.
- Outputs: integration note and reference pattern.
- Ordered rules:
  1. Identify BI claims that depend on branch coverage, shape, verdict, term meaning, B3 denominator, B4 bridge evidence, or forbidden-edge discipline.
  2. Replace restated verdicts/definitions with citations to the owning view.
  3. Keep optimization-chain claims bounded by method family and owner-decision route.
  4. Record product-doc patches as proposals unless owner-approved.
- Edge cases: a public-facing claim has no owning view citation; keep as candidate/hypothesis or block integration.
- Validation evidence: sample trace from claim -> optimization chain -> branch register -> view triad refs -> source evidence.

## Task Decomposition

| Task ID | Goal | Layer | Depends On | Task Contract |
| --- | --- | --- | --- | --- |
| TASK-VTM-001 | Establish method boundary, source matrix, and branch materialization register. | L0 | none | [task](work-pack/tasks/TASK-VTM-001-METHOD-BOUNDARY.md) |
| TASK-VTM-002 | Author method artifact and system-view pilot shell. | L0/L1 | TASK-VTM-001 | [task](work-pack/tasks/TASK-VTM-002-SYSTEM-VIEW.md) |
| TASK-VTM-003 | Author engineer-view decision inventory. | L1 | TASK-VTM-002 | [task](work-pack/tasks/TASK-VTM-003-ENGINEER-VIEW.md) |
| TASK-VTM-004 | Author ontology-view typed model. | L1 | TASK-VTM-003 | [task](work-pack/tasks/TASK-VTM-004-ONTOLOGY-VIEW.md) |
| TASK-VTM-005 | Integrate, validate, and prepare readiness route. | L2/L3 | TASK-VTM-004 | [task](work-pack/tasks/TASK-VTM-005-INTEGRATION-VALIDATION.md) |

## Work-Pack Mapping

| Planning Source | Work-Pack Target | Mapping Rule |
| --- | --- | --- |
| Delivery slices | [WORK-PACK.md](WORK-PACK.md) task board and waves | Each slice maps to one or more SWUs. |
| Layer decisions | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) and waves | Each wave answers one layer decision question. |
| Implementation details | task files | Each task file owns local SWU execution contract. |
| Validation strategy | work-pack and execution-pack gates | Each SWU names reviewable evidence. |

## Blockers And Risks

| ID | Type | Description | Resolution Path |
| --- | --- | --- | --- |
| R-VTM-001 | risk | Pilot output path may be changed by owner preference. | Resolve in TASK-VTM-001 before writing pilot triad. |
| R-VTM-002 | risk | View skills are private submodule material. | Keep product-facing integration proposed until boundary approved. |
| R-VTM-003 | risk | Heavy dispatch could be overkill. | Default single-author route; require explicit opt-in for subagent dispatch. |
| R-VTM-004 | risk | Branch materialization repeats canonical branch definitions. | Keep [BRANCH-MATERIALIZATION.md](BRANCH-MATERIALIZATION.md) as coverage law and cite `ONTOLOGY-BRANCHES.md` for definitions. |
| R-VTM-005 | risk | B3 and B4 are under-modeled by generic view language. | Require B3 record, B4 ledger, and branch gates in SWU acceptance evidence. |

## Next Route

Run `task-session` on [WORK-PACK.md](WORK-PACK.md), starting with [TASK-VTM-001](work-pack/tasks/TASK-VTM-001-METHOD-BOUNDARY.md).
