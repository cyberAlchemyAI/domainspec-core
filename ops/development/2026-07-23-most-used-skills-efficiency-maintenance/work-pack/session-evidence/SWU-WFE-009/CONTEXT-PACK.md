# Context Pack: SWU-WFE-009

Status: strict coverage pass

Mode: standard

Lifecycle route: Sigil Development for Inventory

## Task boundary

Add one deterministic projection-conformance validator for Inventory. It must
compare configured source records, the primary machine index, exact derived
maps, the human catalog, and every enabled projection. It must emit independent
subresults and one lookup-readiness verdict. Repair only generated map drift in
the live Inventory; do not reinterpret entry meaning or close the tag
vocabulary.

## Obligation matrix

| ID | Obligation | Controlling evidence | Status |
| --- | --- | --- | --- |
| INT2-O1 | Configured source paths and machine rows agree in both directions. | TASK-WFE-009 algorithm 1-2 | covered |
| INT2-O2 | Stable IDs are unique, paths are unique, embedded source IDs agree when present, and `by_id` is exact. | WFE-R09 identity boundary | covered |
| INT2-O3 | Every indexed path exists inside the repository boundary. | TASK-WFE-009 acceptance | covered |
| INT2-O4 | All seven derived maps equal a deterministic recomputation from `entries`. | INT-1 producer contract | covered |
| INT2-O5 | Human rows agree with machine path and type wherever the human table represents them. | TASK-WFE-009 algorithm 4 | covered |
| INT2-O6 | Every enabled projection proves current source and projection digests plus the source timestamp. | TASK-WFE-009 algorithm 5 | covered |
| INT2-O7 | Missing rows, orphan rows, missing paths, stale projections, map drift, and human mismatch have causal red fixtures. | TASK-WFE-009 acceptance | covered |
| INT2-O8 | Uncontrolled historical tags warn but do not block conformance. | TASK-WFE-009 acceptance | covered |
| INT2-O9 | Lookup reports the conformance verdict and cannot substitute parseability for readiness. | TASK-WFE-009 primary behavior | covered |
| INT2-O10 | Canonical and generated Inventory runtime contracts remain synchronized if lookup text changes. | generated-runtime policy | covered |

## Selected evidence

| Path | Selectors | Why selected |
| --- | --- | --- |
| `work-pack/tasks/TASK-WFE-009-INVENTORY-PROJECTION-FRESHNESS.md` | objective, algorithm, acceptance | complete SWU contract |
| `arcanum/arcana/inventory/scripts/validate-index-json.sh` | current partial checks | extension point |
| `arcanum/arcana/inventory/SKILL.md` | lookup and machine-index contracts | runtime behavior authority |
| `.arcanum/inventory/index.json` | 208 entries and seven derived maps | live machine witness |
| `.arcanum/inventory/index.md` | represented path/type rows | live human witness |
| `.arcanum/inventory/tools/inventory-update.cjs` | map construction order and supported kinds | producer semantics |
| `.arcanum/inventory/entries/`, `wiki/`, `lint/`, `raw/manifests/` | 152 configured sources | live source set |

## Baseline findings

- All 152 configured source files have machine rows.
- All 208 indexed paths exist.
- `by_id` and `by_evidence_card` are current.
- `by_type`, `by_tag`, `by_source`, `by_status`, and `by_evidence_set`
  contain stale or legacy values and require deterministic regeneration.
- No optional projection is currently enabled.
- Historical tags outside `tags.md` remain warnings by accepted policy.

## Mutation strategy

Implement the reusable validator and causal fixture harness in canonical public
Inventory source. Add an explicit live source-root configuration to the
Inventory validation object. Recompute only derived maps from existing entries,
preserving entry order and content. Update the lookup contract, then regenerate
the Inventory runtime packages from canonical source in isolation before
synchronizing only the two Inventory package directories.

## Validation surface

```bash
bash arcanum/arcana/inventory/scripts/validate-index-json.sh \
  .arcanum/inventory/index.json
bash arcanum/arcana/inventory/development/run-projection-validation-fixtures.sh
git diff --check -- \
  arcanum/arcana/inventory \
  .arcanum/inventory \
  .agents/skills/inventory \
  .claude/skills/inventory
```

## Context Builder result

- Files selected: 7
- Obligation coverage: 10/10
- Uncovered obligations: 0
- Contradictions: 0
- Strict coverage: pass
- Mutation gate: pass
- Runtime handoff: isolated canonical regeneration for Inventory only
