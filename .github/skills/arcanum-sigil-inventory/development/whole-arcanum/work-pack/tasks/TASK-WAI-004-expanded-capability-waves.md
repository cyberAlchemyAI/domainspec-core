---
module: inventory-whole-arcanum
task: TASK-WAI-004
status: ready
layer: L2
---

# TASK-WAI-004: Expanded Capability Waves

## Objective

Scale the inventory after the proof slice by source family, preserving ownership
boundaries and reporting duplicate or conflicting concepts instead of merging
them silently.

## Implementation Detail

Use the source manifest to schedule family slices:

- `arcana/` capability packages,
- `spells/`, `transmutations/`, and `formulae/` composition surfaces,
- `framework/`, `registry/`, `tools/`, and command surfaces.

Each slice should produce cards, a family index, and a coverage note naming what
was intentionally not captured.

## Smallest Working Units

| SWU | Goal | Write Scope | Done Criteria | Validation |
| --- | --- | --- | --- | --- |
| SWU-WAI-008 | Expand `arcana/` family cards. | `cards/arcana/` | high-value capability cards exist | coverage report |
| SWU-WAI-009 | Expand composition family cards. | `cards/composition/` | spells/transmutations/formulae cards exist | coverage report |
| SWU-WAI-010 | Expand runtime/governance support cards. | `cards/runtime/` | framework/registry/tools cards exist | coverage report |

## Source Anchors

- `source-manifest.*`
- `SOURCE-POLICY.md`
- L1 pilot validation results
