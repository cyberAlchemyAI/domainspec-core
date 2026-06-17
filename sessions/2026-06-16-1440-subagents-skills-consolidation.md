---
tags: [subagents-strategy, skills, context-cost, anti-bias, register-dispatch, governance]
node_type: discovery
is_session: true
layer: architecture, governance
nature: procedural, explanatory
status: active
created: 2026-06-16
timestamp: 2026-06-16T14:40:42-03:00
expires: 2026-08-15
conversation_id: 2026-06-16-subagents-skills-consolidation
decisions_made: true
contradictions_found: false
specs_updated: [.claude/skills/domainspec-subagents-strategy/SKILL.md, .claude/skills/research/SKILL.md, .claude/skills/review/SKILL.md, .claude/skills/experiment/SKILL.md, .claude/skills/check-tension/SKILL.md, .claude/skills/register-dispatch/SKILL.md, .claude/skills/anti-bias-vector-composition/SKILL.md]
promoted_candidates: []
expected_importance: 6
importance_rationale: "Cuts the per-run context cost of every subagents-strategy dispatch and consolidates the skill family under .claude/skills, affecting all future dispatches."
---

# Subagents-strategy skills consolidation + constitution read-gating

## Summary

Consolidated the subagents-strategy skill family under `.claude/skills` and cut its per-run
context cost. Made anti-bias-vector-composition a real skill (4 vault discovery files mirrored
as `reference/`); copied `register-dispatch` (SKILL + `append-dispatch.cjs`, location-independent)
into `.claude/skills` and repointed all references. Diagnosed that the 782-line constitution was
never auto-loaded — only the pointer wording invited it — so instead of moving/deleting it, added
a **"Read budget"** guard to the router and reframed the §5 field-definition cites across router +
research/review/experiment to read from inline `register-dispatch`, leaving the constitution as
authority-of-last-resort. robot-talks was already present and identical — no change.

## Next Steps

- Decide single-source vs mirror: delete the now-duplicated `internal_tools/.../register-dispatch` and `vault/discovery/anti-bias-vector-composition` copies in the parent, or keep as homes (drift risk) — owner call.
- Reconcile the `implementation/domainspec` submodule copies under submodule discipline before any cross-repo sync.
- Commit the working changes (nothing committed yet) in the parent repo.

## Open Questions

- Should `.claude/skills` be the single source of truth, with `internal_tools/`+`vault/` mirrors retired? — answer lands in the drift decision above.
- If the physical constitution dependency must ever be removed, where does a shared (4-skill) constitution live inside `.claude/skills`? — unresolved; inlining §5/§6 was flagged as large and not recommended.

## Files touched

- .claude/skills/anti-bias-vector-composition/SKILL.md
- .claude/skills/anti-bias-vector-composition/reference/principle.md
- .claude/skills/anti-bias-vector-composition/reference/literature.md
- .claude/skills/anti-bias-vector-composition/reference/validator-check.md
- .claude/skills/anti-bias-vector-composition/reference/examples.md
- .claude/skills/register-dispatch/SKILL.md
- .claude/skills/register-dispatch/append-dispatch.cjs
- .claude/skills/domainspec-subagents-strategy/SKILL.md
- .claude/skills/check-tension/SKILL.md
- .claude/skills/research/SKILL.md
- .claude/skills/review/SKILL.md
- .claude/skills/experiment/SKILL.md
