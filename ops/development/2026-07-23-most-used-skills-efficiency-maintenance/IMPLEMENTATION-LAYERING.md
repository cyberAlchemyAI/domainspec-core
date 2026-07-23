# Implementation Layering: Workflow Efficiency Maintenance

## Boundary heuristic

Layer value is the decision unlocked plus unsafe states rejected plus downstream
rework avoided. Layer cost is implementation, verification, lifecycle review,
and public/private synchronization. A layer stops when its next unit answers a
different decision question.

| Layer | Decision question | Minimum working unit | Included | Deferred | Exit evidence | Promotion decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | After this layer, do existing rules and package contracts reject known forbidden or false-ready inputs at their earliest owner boundary? | `SWU-WFE-001`: Subagents appender rejects forbidden new rows with causal negative controls | DSS-1, TS-1, INV-1, INT-1 | downstream receipt consumption, runtime overlay composition, broad projection proof | focused red/green suites; material-package validator receipt; conformant Inventory index | continue only if each change rejects its named prior bad state without breaking its positive control |
| L1 | After this layer, can validated evidence cross capability boundaries without becoming ambient authority? | TS-2 consumes the INV-1 receipt | TS-2, DG-1, DSS-2 | Whisper runtime assembly, full projection/freshness proof, final status-axis consolidation | stale/mismatch receipt rejection; admissible-option and override fixtures; confirmed-sheet digest tests | harden only if producer/consumer and protected owner gates remain non-collapsing |
| L2 | After this layer, do generated runtimes, read models, and capability status stay synchronized without gaining authority? | declared Whisper overlay assembly | WH-1, INT-2, INV-2 | cross-repository rollout and promotion | overlay parity; bidirectional Inventory proof; three-axis Invoke capability fixtures | package only if canonical/local and authored/released/runtime axes remain distinct |
| L3 | After this layer, does the full maintenance set recompose without regression or authority leakage? | cross-capability verification closure | all focused and package suites, observability, work-pack evidence sync | public release, registry promotion, generalized shared framework | final closure receipt, public/private scan, generated parity, work-pack traceability | close the package or route named residue; never auto-promote |

## Non-regression guardrails

- Existing positive cases remain valid unless the accepted finding explicitly
  narrows them.
- Duplicate dispatch close remains idempotent.
- Task Session retains noncritical `FLAG`, live validation, and recovery.
- Invoke proposal-only authoring remains independent of mutation admission.
- Decision Gate retains explicit consequential consent and durable provenance.
- Inventory remains a non-authoritative read model.
- Whisper retains human editorial judgment and all declared presets.
- Later layers preserve every earlier rejection witness.

## Recommended next layer

- Next layer: L0.
- Selected unit: `SWU-WFE-001`.
- Decision unlocked: whether Subagents registration can fail closed on the rules
  the strategy already declares, without a schema expansion or another human
  confirmation.
- Major deferred scope: receipt composition and runtime/projection hardening.
