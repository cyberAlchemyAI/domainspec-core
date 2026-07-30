# TASK-BWAA-001 — Derive Directed Lens Flows

Layer: L0  
Dependencies: none  
SWU: `SWU-BWAA-001`  
Execution owner recommendation: `local-fallback` through one Task Session

## Task Objective

Create the pure, fail-closed aggregation contract that later arrow rendering
consumes. This task contains exactly one SWU.

## Smallest Working Units

- `SWU-BWAA-001`: derive and validate the exact directed lens-flow partition.

## Primary Behavior

Extend the pure atlas projection with deterministic `lens_flows` that group
the 109 canonical portals by ordered `(source_lens_id, target_lens_id)`.

## Source Anchors

- `SPEC.md#acceptance-contracts`
- `ARCHITECTURE.md#projection-contract`
- `projects/body-war/ontology/business/scripts/view-atlas-projection.mjs`
- `projects/body-war/ontology/business/authoring/view-atlas-catalog.mjs`

## Write Scope

- `projects/body-war/ontology/business/scripts/view-atlas-projection.mjs`
- `projects/body-war/ontology/business/scripts/validate-view-atlas.mjs`
- `projects/body-war/ontology/business/tests/business-view-atlas-projection.test.mjs`

## Implementation Detail

Inputs:

- ordered six-lens catalog;
- canonical projected `portals`, each with relation ID, source lens, and target
  lens;
- existing coverage invariants.

Output:

- `projection.lens_flows`, an ordered array of
  `{source_lens_id, target_lens_id, relation_ids, relation_count}`.

Algorithm:

```text
assert every configured lens ID is unique
create one lens-order index
for each portal in canonical portal order:
  reject unknown source/target lens or same-lens portal
  reject a relation ID already assigned to a flow
  append the relation ID to the ordered source/target group
sort groups by source lens order, then target lens order
sort each relation_ids list by canonical relation ID
set relation_count from relation_ids length
assert group count = 13
assert sum(relation_count) = 109
assert assigned relation IDs exactly equal portal relation IDs
return immutable projection data
```

Precedence is source lens order, target lens order, then canonical relation ID.
Reciprocal pairs never merge.

Failure modes:

- unknown or duplicate lens ID;
- unknown portal endpoint;
- same-lens record incorrectly classified as a portal;
- duplicated or omitted relation ID;
- expected group or total mismatch.

All failures stop projection/validation with a diagnostic; none are repaired by
inventing a group.

## Acceptance

- exactly 13 ordered flow groups;
- group relation counts sum to 109;
- every portal relation ID appears exactly once;
- reciprocal directions remain separate;
- ordering follows the fixed lens order, then target lens order;
- unknown lenses, duplicate IDs, or total mismatch fail closed;
- 237/231/122/109/44 and all existing projection tests remain exact.

Expected directed groups:

| Source | Target | Count |
| --- | --- | ---: |
| behavior | business-objects | 55 |
| behavior | governance-lifecycle | 13 |
| behavior | hypotheses-outcomes | 4 |
| behavior | participants-boundaries | 2 |
| business-objects | governance-lifecycle | 5 |
| business-objects | hypotheses-outcomes | 2 |
| business-objects | participants-boundaries | 1 |
| hypotheses-outcomes | business-objects | 1 |
| hypotheses-outcomes | governance-lifecycle | 1 |
| participants-boundaries | behavior | 12 |
| participants-boundaries | business-objects | 11 |
| participants-boundaries | governance-lifecycle | 1 |
| participants-boundaries | responsibilities | 1 |

## Validation

```bash
node --test projects/body-war/ontology/business/tests/business-view-atlas-projection.test.mjs
node projects/body-war/ontology/business/scripts/validate-view-atlas.mjs
git diff --check -- projects/body-war/ontology/business/scripts/view-atlas-projection.mjs projects/body-war/ontology/business/scripts/validate-view-atlas.mjs projects/body-war/ontology/business/tests/business-view-atlas-projection.test.mjs
```

## Split And Done

Candidate children were `deriveLensFlows`, invariant validation, and unit-test
fixtures. They are retained together because the aggregation has no
independently acceptable result without exact partition proof; no presentation
is allowed. Done requires a terminal receipt proving the exact 13/109
partition and unchanged semantic locks.

## Handoff And Closeout

Context Builder needs this task, `SPEC.md`, `ARCHITECTURE.md`, the three source
files, `WORK-PACK.md#semantic-locks`, and
`../shared/EXECUTION-CONTROL.md`. Known blockers: any current digest drift or a
lens/portal count different from the locked baseline.

Expected result:

```yaml
swu_id: SWU-BWAA-001
result: pass | flag | block | interrupted
capability_ref: task-session
receipt_kind: native-stage | local-fallback | blocked
receipt_artifact: work-pack/closeout/SWU-BWAA-001.receipt.json | none
files_touched: [declared paths only]
validation: [command and result]
blockers: [blocker or none]
residue: [residue or none]
reroute: invoke-refresh | none
handoff_note: exact 13/109 result and whether 002 is dependency-ready
```
