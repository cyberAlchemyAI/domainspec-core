# SWU-BWVA-001 — Complete Pure Atlas Projection

Status: `ready`

## Primary behavior

Derive a source-conserving six-lens ID projection for every current business
ontology node and relation, validate the exact 44-node research disposition
registry, and emit a deterministic bounded coverage receipt.

## Material write scope

- `projects/body-war/ontology/business/authoring/view-atlas-catalog.mjs`
- `projects/body-war/ontology/business/scripts/view-atlas-projection.mjs`
- `projects/body-war/ontology/business/scripts/validate-view-atlas.mjs`
- `projects/body-war/ontology/business/tests/business-view-atlas-projection.test.mjs`

## Execution output scope

- `projects/body-war/ontology/business/receipts/view-atlas-coverage-receipt.json`

## Forbidden writes

- `nodes/`
- `relations/`
- `lifecycle-policies/`
- `profile.json`
- `residue.json`
- `views/business.json`
- generated HTML

## Acceptance

- six unique lens IDs and all 17 observed kinds mapped exactly once;
- 237 unique core node IDs assigned exactly once;
- 231 unique relation IDs partitioned into 122 internal and 109 portals;
- source/outbound and target/inbound portal indexes reference the same relation;
- all exact source tuple directions remain unchanged;
- the current parallel endpoint pair remains two relations;
- degree is computed from all admitted relations without status/effect filtering;
- exactly 44 zero-degree nodes match exactly one catalog disposition;
- missing/multiple kind mapping, duplicate node/relation, dangling endpoint,
  missing/extra/non-isolate disposition, and parallel deduplication controls
  reject;
- coverage receipt binds exact sources and `authority_effect:none`;
- semantic input digests remain at the work-pack lock.

## Validation

```text
node --test projects/body-war/ontology/business/tests/business-view-atlas-projection.test.mjs
node projects/body-war/ontology/business/scripts/validate-view-atlas.mjs
node projects/body-war/ontology/business/scripts/validate.mjs
```

## Closeout

Write terminal receipts under
`projects/body-war/development/task-sessions/SWU-BWVA-001/`, then Invoke Refresh
may mark this row complete and advance only to `SWU-BWVA-002`.
