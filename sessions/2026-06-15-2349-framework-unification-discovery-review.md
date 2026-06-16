---
tags: [framework-unification, arcanum, domainspec, discovery, review, subagents, operationalization]
node_type: discovery
is_session: true
layer: architecture
nature: procedural, technical
status: active
created: 2026-06-15
timestamp: 2026-06-15T23:49:42-03:00
expires: 2026-08-14
conversation_id: 2026-06-15-framework-unification-discovery-review
decisions_made: true
contradictions_found: false
specs_updated: [projects/framework-unification/SCOPE.md, projects/framework-unification/README.md, projects/framework-unification/IMPROVEMENTS.md, projects/framework-unification/discovery/discovery.md, projects/framework-unification/research/domainspec-findings.md, projects/framework-unification/research/RESEARCH.md, projects/framework-unification/review/findings.md, projects/framework-unification/review/attacks.md]
promoted_candidates: []
expected_importance: 7
importance_rationale: "Sets the workspace's operationalization direction (novelty=Lean), produces the discovery + scope conventions, and red-teams the orientation artifacts."
---

# Framework Unification — Discovery, Review, and Operationalization Direction

## Summary

Continued the framework-unification workspace: added the Lean formalization + PermGuard to RESEARCH.md (subagent eval→edit, reviewer-gated), then authored the discovery chain (domainspec-findings.md + discovery.md) following the ../domainspec lifecycle pragmatically (research source = RESEARCH.md, disclosed). Ran a 7-agent review red-team (with a double check-tension gate) over discovery/findings — the 3 draft CRITICALs did not survive verification; 3 MAJORs (Saturn mis-cite, `layer: ontology`, invented `feeds` edge) did and were fixed. The owner decided **novelty lives in Lean; this workspace is operationalization (judged by utility)**, adopting an open-questions-per-artifact discipline as the operational residue accounting (new SCOPE.md), which reassigns the §7 residue-type "blocker" to Lean as a deferred integration point.

## Next Steps

- Run **paired-views** over the three layers to assign single owners (dispatch composition; `obligation_id` bridge) — next pipeline phase, see README.md Path.
- Decide **OQ-5** (init `arcanum` submodule vs description-only) — gates paired-views; discovery/discovery.md OQ-5.
- Optional: apply the review **MINOR** fixes — review/findings.md.
- Optional: run the B-2 Gibbs `README ↔ PRIZES` check in `../domainspec-lean-formalization` — IMPROVEMENTS.md B-2.

## Open Questions

- OQ-5 — initialize `arcanum` for real-code paired-views, or accept description-only? (discovery/discovery.md)
- OQ-1 — who owns "dispatch composition", and does `v0.5.2` typed-DAG ratify? (discovery/discovery.md)
- OQ-2 — who owns the `obligation_id` bridge (B-1)? (discovery/discovery.md)
- OQ-3 — who builds the observability producer feeding the central ledger? (discovery/discovery.md)

## Files touched

- projects/framework-unification/SCOPE.md
- projects/framework-unification/README.md
- projects/framework-unification/IMPROVEMENTS.md
- projects/framework-unification/discovery/discovery.md
- projects/framework-unification/research/domainspec-findings.md
- projects/framework-unification/research/RESEARCH.md
- projects/framework-unification/review/findings.md
- projects/framework-unification/review/attacks.md
- telemetry/agents/subagents-dispatch.yaml
