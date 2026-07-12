---
tags: [inventory, invoke, plan, work-pack, domainspec-v2, ui-meta-type, evidence-contract, validation-harness, relationship-invariant, promotion-guardrail]
node_type: synthesis
is_session: false
layer: plan
nature: synthesis
status: flag
created: 2026-07-11
sources:
  - projects/domainspec-v2/development/ui-meta-type-repair/SPEC.md
  - projects/domainspec-v2/development/ui-meta-type-repair/ARCHITECTURE.md
  - projects/domainspec-v2/development/ui-meta-type-repair/refresh/2026-07-12-decision-closure/REFRESH-REPORT.md
  - projects/domainspec-v2/development/ui-meta-type-repair/IMPLEMENTATION-PLAN.md
  - projects/domainspec-v2/development/ui-meta-type-repair/WORK-PACK.md
  - projects/domainspec-v2/development/ui-meta-type-repair/INVOKE-TRANSPORT.md
  - projects/domainspec-v2/development/ui-meta-type-repair/INVOKE-SUCCESSOR-TRANSPORT.md
  - projects/domainspec-v2/development/ui-meta-type-repair/ui-meta-type-repair-successor.dispatch.json
  - projects/domainspec-v2/development/ui-meta-type-repair/DECISION-LEDGER.md
---

# DomainSpec v2 UI Meta-Type Repair Invoke Package

Invoke define/design/plan package for repairing UIF evidence production through
seven bounded contracts. The architecture preserves `attribute-present`, adds a
versioned nonempty rule, requires the 165-case mutation base, separates source
and destination outcomes, composes a hard-conjunct dossier, preserves corpus
provenance, routes relationship questions to owners, and appends replayable
generations.

SWU-UIR-001 through 009 are complete. DEC-UIR-007 through 010 are resolved, and
the validated high-complexity successor plan adds SWU-UIR-011 through 015 for
bounded absence, corpus generation 002, dossier-policy evaluation,
relationship owner-decision evidence, and dossier/index v2 recomposition before
SWU-UIR-010. Both dispatches validate with zero blocks/flags, Distill passes,
44/44 repair tests and 69/69 DomainSpec tool tests pass, and SWU-UIR-011 is the
only selected next Task Session unit.

All nine UI candidates remain deferred. Portability is below threshold,
Form/Action independent positives are missing, Action-source is route-open but
unadmitted, and no DS-D1/DS-D8 authority changed.
