---
tags: [framework-unification, artifacts, ontology, concept-map, pipeline]
node_type: discovery
is_session: true
layer: architecture
nature: explanatory, reference
status: active
created: 2026-06-16
timestamp: 2026-06-16T11:31:22-03:00
expires: 2026-08-15
conversation_id: 2026-06-16-framework-unification-artifacts
decisions_made: true
contradictions_found: true
specs_updated: [projects/framework-unification/CONCEPT-MAP.md, projects/framework-unification/components/ARTIFACTS.md, implementation/domainspec/TUNING-LOOP.md]
promoted_candidates: []
expected_importance: 8
importance_rationale: "Establishes the conceptual spine (two-axis map, four-tier artifact catalog, three ontology planes) the whole unification effort builds on."
---

# Framework Unification — Artifact Catalog & Conceptual Spine

## Summary

Mapped the framework-unification workspace and built its conceptual spine: a CONCEPT-MAP (two axes — pipeline × three mechanisms — plus 10 invariants) and a validated ARTIFACTS catalog (four tiers: object/knowledge/signal/engine). Initialized the `implementation/domainspec` + `arcanum` submodules to ground the map in real code (closes OQ-5), locked the canonical lifecycle order (`define → research → findings → discovery → plan → spec → stories → tests → implement → verify → emit-signals`), and fixed `TUNING-LOOP.md` to match. Surfaced the three-ontology distinction (meta-system / domain-types / domain-instances) and the drift-observability criterion for what counts as a trustworthy artifact.

## Contradictions

- questions `implementation/domainspec/CLAUDE.md` Route 3 ("Spec → Plan") vs the built orchestrator (`domainspec-pipeline` Step 1=plan, Step 2=spec) — likely two distinct "plan" concepts (CONCEPT-MAP OQ-A).

## Next Steps

- Open OQ-5 as its own node: the business-ontology foundation flow (plane 3 + sufficiency) — `projects/framework-unification/`.
- Resolve ARTIFACTS OQ-1/2/3 with owner: granularity rule, problem-statement placement, code-as-leaf.
- Decide one-plan-vs-two (CONCEPT-MAP OQ-A sub-question).
- Commit the `TUNING-LOOP.md` change in the submodule (`checkout main` → commit + push → bump parent) per `SUBMODULE-DISCIPLINE.md`.

## Open Questions

- How to incrementally build the domain ontology + when it is "enough" (ARTIFACTS OQ-5).
- How to mechanically guarantee every artifact carries `## Open Questions` (ARTIFACTS OQ-6).
- One plan stage or two — plan-execution vs plan-implementation (CONCEPT-MAP OQ-A).

## Files touched

- projects/framework-unification/CONCEPT-MAP.md
- projects/framework-unification/components/ARTIFACTS.md
- implementation/domainspec/TUNING-LOOP.md
- telemetry/agents/subagents-dispatch.yaml
