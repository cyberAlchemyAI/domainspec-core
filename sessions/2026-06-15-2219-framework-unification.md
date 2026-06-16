---
tags: [framework-unification, arcanum, domainspec, agentic-system, research, discovery]
node_type: discovery
is_session: true
layer: architecture, ontology
nature: explanatory, procedural
status: active
created: 2026-06-15
timestamp: 2026-06-15T22:19:19-03:00
expires: 2026-08-14
conversation_id: 2026-06-15-framework-unification
decisions_made: true
contradictions_found: false
specs_updated: [projects/framework-unification/README.md, projects/framework-unification/research/RESEARCH.md]
promoted_candidates: []
expected_importance: 7
importance_rationale: "Establishes the framework-unification workspace and the first high-level map of the intent→code engine, the base for all subsequent unification work."
---

# Framework Unification — research + workspace scaffold

## Summary

Investigated whether three project folders (cyber-alchemy-lean-fusion, dispatch-composition-attack, domainspec-language) describe the same system; research (3 read-only agents) confirmed they are three adjacent **layers of the CyberAlchemy agentic-system engine** (epistemology/gate, communication/observability, representation), not separate products. Decided to build a high-level view for the owner to orient by, following research → discovery → paired-views. Created `projects/framework-unification/` with `layers/` (the three folders moved in via `git mv`, history preserved) and `research/RESEARCH.md` persisting the research synthesis; the `arcanum` submodule is uninitialized so the engine was mapped from `cyberAlchemy/` description, not source.

## Next Steps

- Run **discovery**: distill `research/RESEARCH.md` into one map (components, boundaries, open decisions) under `projects/framework-unification/`.
- Then **paired-views** over the three layers to assign a single owner to each duplicated concept.
- Optional: sweep for stale path references to the three moved folders (e.g. `context-index.json`).
- Optional: `make bootstrap` / init the `arcanum` submodule if discovery needs the real engine code.

## Open Questions

- "Dispatch composition" has two homes (cyber-alchemy View 03 vs dispatch-composition-attack) — which owns it, and does the `v0.5.2` typed-DAG draft get ratified?
- Is the residue-type blocker (cyber-alchemy) the same decision as the `obligation_id` bridge B-1 (domainspec-language)?
- Who builds the observability producer that feeds the central ledger (the one concrete unblock)?

## Files touched

- projects/framework-unification/README.md
- projects/framework-unification/research/RESEARCH.md
- projects/framework-unification/layers/cyber-alchemy-lean-fusion/ (moved)
- projects/framework-unification/layers/dispatch-composition-attack/ (moved)
- projects/framework-unification/layers/domainspec-language/ (moved)
- telemetry/agents/subagents-dispatch.yaml
