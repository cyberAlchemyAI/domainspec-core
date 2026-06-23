---
tags: [claude-md, router, agent-context, three-pillars, governance]
node_type: conceptual
is_session: true
layer: authority, architecture
nature: procedural, reference
status: active
created: 2026-06-22
timestamp: 2026-06-22T22:30:59-03:00
expires: 2026-08-21
conversation_id: 2026-06-22-claude-md-router
decisions_made: true
contradictions_found: false
specs_updated: [CLAUDE.md]
promoted_candidates: []
expected_importance: 6
importance_rationale: "The root CLAUDE.md is loaded into every session, so its shape and the adopt/reject rationale steer all future agent behavior in the umbrella."
---

# Umbrella CLAUDE.md reframed as a lean Agent Context Router

## Summary

Reframed the umbrella root CLAUDE.md from a terse instruction list into a lean "Agent
Context Router" carrying the three-pillar (DomainSpec/Arcanum/Saturn) orientation plus 7
objective-routes; subagents verified every cited path/skill and corrected one overclaim
(sigil/spell/capability are only described in `arcanum/README.md`, not defined in
`arcanum/definitions/`). Then harvested patterns from sibling/nested CLAUDE.md files and
adopted only two — collapsing Route 6 to a pointer-digest of `SUBMODULE-DISCIPLINE.md`,
and adding a propose-first / no-silent-fix clause — rejecting the rest as bloat or
app-vs-umbrella misfit.

## Next Steps

- Fix two typos in CLAUDE.md preamble line 5 (`objetive`→`objective`, `build`→`builds`) — pending user ok.
- De-duplicate root `AGENTS.md` submodule rules → point to `SUBMODULE-DISCIPLINE.md` (same "point, don't restate" rule).
- Commit `CLAUDE.md` + `telemetry/agents/subagents-dispatch.yaml` (parent private; no submodule touched).
- Define `DEF-ARC-SIGIL`/`SPELL`/`CAPABILITY` in `arcanum/definitions/` (open item carried from 2026-06-22 prior session; cited by Route 3).

## Open Questions

- Should root `CLAUDE.md` and `AGENTS.md` split roles (CLAUDE=brief, AGENTS=deep ops) like nested repos, or stay merged? → resolve in `AGENTS.md`.
- Which tone model is canonical across pillars (umbrella vs domainspec vs goldenquill variants)? → CLAUDE.md preamble decision.

## Files touched

- CLAUDE.md
- telemetry/agents/subagents-dispatch.yaml
