---
tags: [arcanum, subagents-strategy, dispatch-composition, dispatch-spec, wiring]
node_type: implementation-plan
is_session: true
layer: architecture, application
nature: procedural, explanatory
status: active
created: 2026-06-15
timestamp: 2026-06-15T17:23:53-03:00
expires: 2026-08-14
conversation_id: 2026-06-15-subagents-strategy-arcanum-wiring
decisions_made: true
contradictions_found: false
specs_updated: [projects/dispatch-composition-attack/plan.md]
promoted_candidates: []
expected_importance: 6
importance_rationale: "Locks the private-overlay wiring decisions and produces the dispatch-composition-attack wiring plan that future implementation will execute."
---

# Subagents-strategy → Arcanum wiring (private)

## Summary

Copied the dispatch-composition-attack research into the repo and worked through how to wire a subagents-strategy capability into Arcanum, integrating it with the private domainspec subagents-dispatch-hooks tooling. Decided to keep everything private in the parent repo, keep subagents-strategy a separate skill (not folded into the public dispatch-spec), and not port to public arcanum — since the private domainspec dispatch ledger already covers most of the dispatch-composition-attack substance. Authored a wiring plan (plan.md) and clarified the Arcanum authoring method (discovery → paired-views) via a worked permission-kernel example.

## Next Steps

- Decide the generation path for subagents-strategy (private-profile vs parent-sync vs install.cjs) — engineer-view decision row, still OPEN.
- If pursuing it, author a discovery seed + paired-views triad for the integration (scope-interview/refine) into a private projects/ folder.
- Hydrate the empty implementation/domainspec submodule (`git submodule update --init`) before relying on subagents-strategy here.
- Re-verify dispatch-composition-attack anchors against the pinned arcanum commit before executing plan.md (paths came from a different Arcanum tree).

## Open Questions

- Which generation path for the private subagents-strategy capability? → engineer-view decision row.
- Central cross-capability observability ledger, or is the per-dispatch private ledger enough? → unanswered.
- Are the dispatch-composition-attack cross-repo claims (v0.5.2 / R30) valid against the live domainspec tree? → plan.md OQ-D.

## Files touched

- projects/dispatch-composition-attack/discovery.md
- projects/dispatch-composition-attack/research.md
- projects/dispatch-composition-attack/findings.md
- projects/dispatch-composition-attack/system-view.md
- projects/dispatch-composition-attack/engineer-view.md
- projects/dispatch-composition-attack/ontology-view.md
- projects/dispatch-composition-attack/plan.md
- telemetry/agents/subagents-dispatch.yaml
