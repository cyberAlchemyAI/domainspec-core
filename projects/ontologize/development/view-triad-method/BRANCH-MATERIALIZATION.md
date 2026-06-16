# Branch Materialization - Ontologize View-Triad Method

This artifact refines the view-triad method so each view materializes Ontologize's four ontology branches without creating a fourth `branch-view`.

## Authority Boundary

`BRANCH-MATERIALIZATION.md` is a method-local coverage profile. It does not redefine the branches.

| Source | Authority |
| --- | --- |
| [../../ONTOLOGY-BRANCHES.md](../../ONTOLOGY-BRANCHES.md) | Branch definitions, branch-to-product mapping, branch-to-client examples, and branch interaction language. |
| [../../DAG-AND-METRICS.md](../../DAG-AND-METRICS.md) | Node vocabulary, edge catalog, event model, metrics, and drift vs contradiction graph rules. |
| [DESIGN.md](DESIGN.md) | View sequencing and artifact ownership. |
| [WORK-PACK.md](WORK-PACK.md) | SWU handoff, validation gates, and publication blockers. |

The branch materialization rule is:

```text
view = a governed projection of B1 meaning, B2 system, B3 run-context, and B4 bridge into an artifact layer whose authority is explicit
```

## Branch Materialization Register

Every run begins with a Branch Materialization Register. The register is run evidence, not canonical doctrine.

| Field | Required Meaning |
| --- | --- |
| `register_id` | Stable handle for one branch materialization row. |
| `branch` | One of `B1-meaning`, `B2-system`, `B3-run-context`, or `B4-bridge`. |
| `source_selector` | File and heading, table, row, or line anchor that supplies the branch evidence. |
| `source_role` | What the selector contributes: policy, system artifact, event, metric, run boundary, bridge edge, drift signal, contradiction, gate, or residue. |
| `system_view_materialization` | Shape, stake, tension, or stance handle named by `system-view`; no verdicts. |
| `engineer_view_materialization` | Decision row, authority, schema/contract, runtime mechanic, enforcement note, or OPEN/CRITICAL blocker owned by `engineer-view`. |
| `ontology_view_materialization` | Typed node, edge, guard, forbidden relation, coined-edge route, or blocker owned by `ontology-view`. |
| `status` | `covered`, `open`, `blocked`, or `not-applicable`, with reason. |
| `owner` | Human or artifact owner for unresolved decisions. |
| `residue` | What later execution must resolve before publication or product integration. |

## Branch-To-View Matrix

Each branch must appear through each view's existing authority lane.

| Branch | System-View Materializes | Engineer-View Materializes | Ontology-View Materializes |
| --- | --- | --- | --- |
| B1 meaning | Business/domain intent, policy stakes, value claims, outcome tensions, and stakeholder-facing stances. | Authority-backed verdict rows for policy/rule/value/outcome choices; OPEN/CRITICAL rows for unresolved meaning decisions. | Business/domain nodes, claim nodes, criteria, policy concepts, and source-backed meaning terms. |
| B2 system | Operating shape, artifacts, records, events, tests, gates, and implementation tensions. | Schemas, contracts, runtime mechanics, event/source verification, enforcement gaps, and authority strikes. | System nodes, event/data shapes, source artifacts, test links, and system-side edge endpoints. |
| B3 run-context | Run boundary stakes, denominator stakes, lifecycle posture, scope, and stage-vs-outcome tensions. | Denominator decisions, lifecycle-state decisions, run-boundary verdicts, scope/posture decisions, and publication blockers when B3 is incomplete. | `LifecycleState`, `OutcomeEvent`, run-context nodes, metric denominator links, and outcome-event relations. |
| B4 bridge | Alignment, drift, contradiction, evidence-gap, realization, observation, and test tensions between branches. | Bridge verdict rows, owner-decision routes, promotion blockers, contradiction adjudication, and authority separation. | Typed bridge edges, edge catalog legality, forbidden cross-branch relationships, guard status, and coined-edge routes. |

## B3 Run-Context Record

B3 is first-class and cannot be collapsed into generic context. The pilot triad must include a B3 run-context record before publication.

| Field | Required Meaning |
| --- | --- |
| `run_boundary` | The bounded run unit, such as lot, order, shipment, assessment run, or product pilot run. |
| `denominator` | Metric denominator and interpretation limit. |
| `lifecycle_state` | Current lifecycle projection, with source and rule for stage depth. |
| `scope` | Organization, client, corpus, product, or sub-project scope. |
| `posture` | Decision posture, deadline, assessment state, or execution state. |
| `stage_outcome_check` | Explicit separation between lifecycle stage and real outcome evidence. |
| `source_events` | Event or source selectors that back the run context. |
| `open_decision` | Owner and route for any unresolved run-boundary or denominator choice. |

Publication is blocked if B3 is missing, if denominator semantics are unstated, or if stage is treated as outcome.

## B4 Bridge Ledger

B4 owns cross-branch evidence, not a vague "relationship" note.

| Field | Required Meaning |
| --- | --- |
| `edge` | Governed edge such as `realized_by`, `observed_by`, `tested_by`, `drifts_from`, `traced_to`, `contradicts`, or proposed edge handle. |
| `source_branch` | Origin branch for the evidence or relation. |
| `target_branch` | Target branch for the evidence or relation. |
| `evidence_ref` | Selector proving the bridge claim or documenting the evidence gap. |
| `drift_or_contradiction_status` | `none`, `raw-drift`, `adjudicated-contradiction`, `evidence-gap`, or `blocked`. |
| `owner_decision_route` | OwnerDecision route, decision gate, or explicit deferral. |
| `catalog_status` | `catalogued`, `proposed-unfiled`, `blocked`, or `not-applicable`. |
| `residue` | Follow-up required before promotion, product integration, or client reuse. |

## Authority Map

The method keeps signals and decisions separate.

| Item | Meaning | Owning Surface |
| --- | --- | --- |
| Raw drift signal | Observed divergence between behavior and intended meaning. It preserves both sides and does not decide conflict. | B4 ledger plus ontology-view edge typing. |
| Adjudicated contradiction | A governance conflict that blocks promotion until resolved. | Engineer-view verdict row plus DAG OwnerDecision route. |
| Engineer-view verdict | The single method-local decision row for a stance or branch boundary. | Engineer-view. |
| DAG OwnerDecision | Product or graph governance decision such as approve, reject, retire, or contradict. | DAG and metrics governance. |
| Product approval | Permission to mutate product/public docs or publish claims. | Owner/operator, outside this development pack. |

## Validation Gates

| Gate | Rule |
| --- | --- |
| B1 meaning gate | Meaning claims cite source/authority; unresolved policy, rule, value, or outcome stances become engineer-view OPEN/CRITICAL rows. |
| B2 system gate | System claims trace to event, source, mechanic, test, or gate evidence; RESOLVED mechanics require reachable authority. |
| B3 run-context gate | Run boundary, denominator, lifecycle state, scope/posture, and stage-vs-outcome separation are explicit before publication. |
| B4 bridge gate | Cross-branch claims use the governed edge catalog; coined edges need route or blocker; open `contradicts` blocks promotion. |
| Recomposition gate | BI or optimization claim traces claim -> optimization chain -> owning view row -> source evidence without restating verdicts or definitions. |

## Non-Goals

- Do not duplicate the definitions, product-layer table, or client examples from [../../ONTOLOGY-BRANCHES.md](../../ONTOLOGY-BRANCHES.md).
- Do not create a standalone `branch-view` unless a future owner decision changes the method.
- Do not apply product-facing doc patches from this development pack.
- Do not promote coined edges or branch vocabulary without the owning governance route.
