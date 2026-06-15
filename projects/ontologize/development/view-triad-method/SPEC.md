# SPEC - Ontologize View-Triad Method

Define-mode artifact for adding the `system-view` / `engineer-view` / `ontology-view` triad as a repeatable Ontologize method.

## Intent

Make the view triad an Ontologize method for turning a client, product, or research corpus into three governed artifacts: a stakeholder shape view, a single-owner decision inventory, and a typed ontology/edge model. The method must materialize the four ontology branches - B1 meaning, B2 system, B3 run-context, and B4 bridge - inside those three views, not by adding a fourth branch-view. The method should compose with the existing ontology+DAG engagement and optimization-chain method without promoting new product claims or changing the public offering by default.

## In Scope

- A method contract for when Ontologize should produce the view triad.
- A branch materialization register and branch-to-view coverage profile for B1/B2/B3/B4.
- A sequencing rule for the three sibling view skills.
- A skill routing map covering the other available sibling skills that may support this method.
- A pilot execution path that produces a view triad for Ontologize itself before using the method on client material.
- Validation gates that catch duplicated decisions, redefined terms, missing authorities, weak citations, and untyped/forbidden relationships.
- Task-session-ready SWUs for implementation.

## Out Of Scope

- No direct rewrite of `projects/ontologize/PRODUCT.md` or `PUBLIC-OFFERING.md`.
- No pricing, contract, signed-client, or brand-promotion changes.
- No claim that `engineer-view` or `ontology-view` are broadly validated beyond their stated transfer status.
- No autonomous client-data work.
- No public Arcanum mutation from this private parent.

## Requirements

| ID | Requirement |
| --- | --- |
| R-VTM-001 | The method must preserve the sibling division of law: system-view owns shape, engineer-view owns verdicts and mechanics, ontology-view owns term and edge typing. |
| R-VTM-002 | Every system-view stance must map to exactly one engineer-view decision row, or be marked provisional with a blocker OQ. |
| R-VTM-003 | Every engineer-view RESOLVED row must cite a verified on-disk authority; unverifiable authorities downgrade the row to OPEN. |
| R-VTM-004 | Every ontology-view term or edge must cite its source and distinguish reused, project-local, proposed-unfiled, and blocked relationships. |
| R-VTM-005 | Every run must begin with a Branch Materialization Register that maps branch evidence to the consuming view authority. |
| R-VTM-006 | B3 run-context must record run boundary, denominator, lifecycle state, scope/posture, stage-vs-outcome separation, source events, and unresolved run-boundary decisions. |
| R-VTM-007 | B4 bridge materialization must record governed edge, source branch, target branch, evidence, drift/contradiction status, owner-decision route, and catalog status. |
| R-VTM-008 | Ontologize deliverables may cite the triad outputs but must not restate verdicts or definitions in a second place. |
| R-VTM-009 | The method must include a lightweight default path and an opt-in multi-agent path through `domainspec-subagents-strategy`. |
| R-VTM-010 | The method must integrate with optimization chains by making BI claims cite the view triad where the claim depends on shape, verdict, term meaning, branch boundary, or forbidden-edge discipline. |
| R-VTM-011 | Execution must be decomposed into SWUs with write scope, acceptance evidence, and validation surface. |

## Success Criteria

- `VIEW-TRIAD-METHOD.md` exists as an Ontologize method artifact.
- A Branch Materialization Register exists for the pilot and covers B1/B2/B3/B4 or carries explicit blockers.
- A pilot triad for Ontologize exists or is explicitly deferred with a blocker ledger.
- The method artifact names when to use `system-view`, `engineer-view`, `ontology-view`, and supporting sibling skills.
- The validation checklist can reject a view triad that decides twice, leaves a stance orphaned, cites unverifiable authority, omits B3 run-context, collapses raw drift into adjudicated contradiction, or invents ontology edges without a route.
- The existing optimization-chain method remains intact and is linked as the BI-expression layer.

## Source Contracts

| Source | Contract Used |
| --- | --- |
| `projects/ontologize/OPTIMIZATION-CHAIN-METHOD.md` | Existing BI-expression method; this pack composes with it. |
| `projects/ontologize/ONTOLOGY-BRANCHES.md` | Canonical branch definitions and branch interaction source. |
| `projects/ontologize/DAG-AND-METRICS.md` | Edge catalog, event model, metrics, and drift/contradiction graph rules. |
| `projects/ontologize/SPEC.md` | Current Ontologize scope and requirements. |
| `projects/ontologize/DESIGN.md` | Existing six-view product/engagement design. |
| `projects/ontologize/PLAN.md` and `WORK-PACK.md` | Existing task-session pattern and high-complexity SWU style. |
| `implementation/domainspec/.claude/skills/system-view/SKILL.md` | Shape/stance authoring law. |
| `implementation/domainspec/.claude/skills/engineer-view/SKILL.md` | Decision inventory, authority, schema, and mechanics law. |
| `implementation/domainspec/.claude/skills/ontology-view/SKILL.md` | Typed node/edge and forbidden-relationship law. |

## Decisions

| ID | Decision | Status | Rationale |
| --- | --- | --- | --- |
| D-VTM-001 | Treat the triad as an Ontologize method extension, not a replacement baseline. | selected | Existing BI-led product docs already carry the product promise; this method adds governed explanation and decision structure. |
| D-VTM-002 | Sequence default execution as source inventory -> system-view -> engineer-view -> ontology-view -> integration. | selected | System-view names stances; engineer-view decides them; ontology-view types the terms and edges after the decision inventory has targets. |
| D-VTM-003 | Default to single-author/light path; use multi-agent zig-zag only when contested or high-risk. | selected | The sibling view skills themselves say the heavy path is opt-in and transfer-validated. |
| D-VTM-004 | Keep product-facing docs unchanged until the method boundary passes L0. | selected | Protects existing Ontologize public and internal artifacts. |
| D-VTM-005 | Route implementation through `task-session`, one SWU at a time. | selected | Invoke authors the plan; task-session owns execution. |
| D-VTM-006 | Constrain the existing triad with branch materialization rather than adding a standalone `branch-view`. | selected | `ONTOLOGY-BRANCHES.md` already owns branch definitions; the method needs coverage gates, not a fourth authority surface. |

## Open Gaps

| Gap | Severity | Route |
| --- | --- | --- |
| G-VTM-001 | No Ontologize triad artifact exists yet. | non-blocking for planning; blocks publication | TASK-VTM-002 through TASK-VTM-004. |
| G-VTM-002 | Exact final product path for generated triad artifacts is not chosen. | non-blocking | Resolve in TASK-VTM-001; proposed path is `projects/ontologize/view-triad/`. |
| G-VTM-003 | Multi-agent dispatch requires operator approval before delegated work. | non-blocking | Keep default local path; route contested runs through `domainspec-subagents-strategy`. |
| G-VTM-004 | View triad validation examples are not yet in Ontologize. | non-blocking | TASK-VTM-005 adds checklist and fixture review. |
| G-VTM-005 | Branch materialization needs a pilot register and sample branch walk trace. | non-blocking for planning; blocks publication | TASK-VTM-001 creates the register; TASK-VTM-005 validates the trace. |

## Next Route

`task-session` on [WORK-PACK.md](WORK-PACK.md), starting with `TASK-VTM-001`.
