---
tags: [inventory, strategy-result, dispatch, subagents, domainspec-v2]
node_type: synthesis
is_session: false
layer: strategy
nature: reference
status: proposed
created: 2026-07-12
dispatch_id: 2026-07-12-r3c-relationship-card-triage
dispatch_type: research
sources: [projects/domainspec-v2/development/r3-closeout-plan/DECISIONS.md, projects/domainspec-v2/development/r3-closeout-plan/work-pack/tasks/TASK-R3C-CARDS.md, implementation/domainspec/architecture/ARCHITECTURE-PATTERN-LIBRARY.md, projects/domainspec-v2/definitions/relationships/relationships.yml]
---

# DomainSpec v2 R3C Relationship-Card Triage Dispatch Proposal

This non-authority Inventory read model records the double-PASS but unconfirmed
`SWU-R3C-006` strategy. It is not dispatch authorization and does not change
relationship state.

## Proposed result contract

- Full outer join over 35 entries.
- 29 v1 relationship rows: 28 currently active and one deprecated label.
- Six authority-only rows marked `no-v1-card`: two active signatures, one
  generated view, and three deferred candidates.
- No card is invented for an authority-only row.
- Generated `owned-by` never becomes authored canonical; deprecated
  `enforces-cross` never becomes active; deferred candidates remain deferred.

## Proposed execution

Two tensioned explorers feed one synthesizer, two independent reviewers, one
findings writer, and one final auditor. The research dispatch may write only its
registered `research.md` and `findings.md`; the parent owns staging,
documentation validation, Craft closure, and work-pack synchronization.

## Gate state

Two independent check-tension agents returned PASS. Registration remains
blocked on explicit selection of Option A in
`DEC-R3C-006-DISPATCH`. Options B and C retain local reassignment and deferral.
