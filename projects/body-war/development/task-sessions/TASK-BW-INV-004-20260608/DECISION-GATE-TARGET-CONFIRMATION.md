# Decision Gate: Park Track Control Inventory Slice

## Target Scope

`TASK-BW-INV-005`: Confirm and create the Park Track Control pilot slice.

## Blocker Question

Should Inventory create the bounded Park Track Control pilot slice now?

## Context

The feature pack now has:

- target confirmation template,
- chat-view templates,
- selector/link/index examples,
- validator checks and negative fixtures.

The next task would create generated read-model files under:

```text
docs/features/inventory-interface-indexing/pilot/park-track-control/
```

This is a consequential mutation because it creates the first concrete generated
Inventory slice.

## Options

### Option 1 - Confirm Park Track Control Slice

Create the bounded pilot slice using the approved source corpus.

Benefit: unlocks retrieval/coverage proof and later lookup/status/explain examples.

Cost/Risk: creates generated Inventory state before the operator reviews target
scope one last time.

Choose when: the current target, sources, exclusions, write path, and known risks
are accepted.

Downstream impact: `TASK-BW-INV-005` can proceed.

### Option 2 - Change Target Or Source Corpus

Revise the target label, source list, exclusions, or write path before generation.

Benefit: prevents generating the wrong first Inventory slice.

Cost/Risk: delays pilot-slice creation and may require updating templates or
validators.

Choose when: the desired Inventory target is not exactly Park Track Control.

Downstream impact: `TASK-BW-INV-005` remains blocked until the revised target is confirmed.

### Option 3 - Stop Before Pilot Slice

Keep the interface/index/validator package ready but do not generate a slice.

Benefit: preserves a clean handoff without creating generated artifacts.

Cost/Risk: lookup/status/explain examples that depend on a real slice remain blocked.

Choose when: the package should be reviewed before any generated Inventory state exists.

Downstream impact: `TASK-BW-INV-005`, `TASK-BW-INV-006`, and `TASK-BW-INV-007` remain blocked.

## Recommendation

Option 1 is recommended if the current Body War Inventory target is accepted:
generate only the bounded Park Track Control slice, not a whole-repository
inventory.
