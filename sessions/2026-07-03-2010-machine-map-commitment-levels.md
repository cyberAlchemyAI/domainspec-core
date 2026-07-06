---
tags: [machine-map, commitment-levels, canonical-artifacts, governance, claim-le-proof, subagents-dispatch]
node_type: conceptual
is_session: true
layer: architecture, governance
nature: reference, explanatory
status: active
created: 2026-07-03
timestamp: 2026-07-03T20:10:29-03:00
expires: 2026-09-01
conversation_id: 2026-07-03-machine-map-commitment-levels
decisions_made: true
contradictions_found: false
specs_updated: [development/machine-map/commitment-levels.md]
promoted_candidates: []
expected_importance: 4
importance_rationale: "A candidate conceptual lens in development/ (not canonical) that mostly re-organizes existing machinery; useful for orientation but self-flagged as adding to the already-heavy governance axis, not the generative gap (OQ-F)."
---

# Commitment-level lens authored over the machine-map

## Summary

The session began by locating what "machine map" is — `development/machine-map/findings.md`, a synthesis mapping DomainSpec/Arcanum/Saturn/cav2 as a self-governing foundry on Beer's VSM. A conceptual conversation then refined the intent→code pipeline into a commitment-level model: three bands (understanding → discovery-as-hinge → canonical → execution), the canonical band splitting into crença/regra/spec, and claim≤proof applied to governance itself (every canonical artifact has a cheap statement and an expensive discharge). The user directed a subagent cycle to capture this in the machine-map folder — propose → author → robot-talks review → zig-zag — with no confirmation gate and the parent as final approver. The Workflow tool was disabled by project policy, so the cycle was hand-orchestrated with the Agent tool and SendMessage. Three anti-biased proposers converged on creating a new companion doc rather than editing findings.md; the parent decided; an author wrote `development/machine-map/commitment-levels.md`. Five robot-talks reviewer lenses (concept, claim≤proof, consistency, enforcement, legibility) attacked it and the author revised across four zig-zag rounds, objections falling 12 → 8 → 3 → 0 before the 5-loop cap. The decisive review result was bounding the "two-faces" thesis to obliging canon (regra+spec) and keying the governance-gap on an "obliges an action?" predicate rather than node-type, since the repo's `axioma` type is heterogeneous (AX-ONT-7 is axiom-typed but an explicit bet). The doc also refuses, as an unearned orthogonal analogy, the tempting claim that the belief/rule split "re-derives" findings.md's two System-5s, and keeps three forks open. The dispatch was registered and closed in telemetry (`2026-07-03-machine-map-commitment-levels`, resolved, 9 agents, 4 loops), and load-bearing citations (ontology-vault SKILL line 84, AX-ONT-2/AX-ONT-7) were spot-checked against source files by the parent. The session's final synthesis report was rejected by the user as context-free and dense — a real communication failure, recorded for correction.

## Next steps

- Add the reciprocal `relates-to` back-link from `projects/framework-unification/CONCEPT-MAP.md` to `development/machine-map/commitment-levels.md` — flagged in the doc §9 as a proposed-but-unperformed follow-up, deliberately left outside this session's mutation.
- Reconcile the close-session skill mismatch: the repo-root `.claude/skills/close-session` targets `docs/vault/conversations/`, which the umbrella root lacks (it uses `sessions/`) — fix the skill path or scope it to the vault-bearing submodule.

## Open questions

- Given OQ-F (the engine governs/verifies more than it generates), is authoring another governance-axis lens the right marginal investment, or should effort shift to the under-built generative side?
- Should `development/` companion lenses like this one have a defined promotion path toward canonical, or remain permanently candidate?

## Recommendation

- The back-link is the cheap keystone to close the arc. But per the review's own finding, the higher-value direction is not more governance lenses — it is the generative gap named in OQ-F. This is a hunch, licensed only by the capability-census cited in CONCEPT-MAP, not by a new result this session produced.

## Files touched

- development/machine-map/commitment-levels.md
- telemetry/agents/subagents-dispatch.yaml
