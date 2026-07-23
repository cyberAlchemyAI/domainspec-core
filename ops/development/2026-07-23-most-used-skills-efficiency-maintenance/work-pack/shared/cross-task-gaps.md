# Cross-Task Gaps

| Gap | Status | Owner | Repair |
| --- | --- | --- | --- |
| Inventory kind validator fails on 15 rows | open, nonblocking to SWU-WFE-001 | TASK-WFE-004 | normalize aliases and guard updater |
| Task Session critical-validation fixture missing | open | TASK-WFE-002 | add causal red/green fixture |
| Material-package validator absent | resolved by SWU-WFE-003A; runtime packaging resolved by Option 1 | TASK-WFE-003 | promote executable support to `scripts/`, schemas to `schemas/`, then integrate the handoff |
| Runtime overlay manifests absent | open | TASK-WFE-007/008 | define classified overlays and parity validators |
| Dirty canonical/generated worktrees overlap possible future writes | conditional blocker | each lifecycle owner | inspect scoped diff before mutation and stop on unknown overlap |
| Cross-repository rollout not designed | deferred | future owner | require separate evidence and Invoke package |
