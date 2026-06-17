---
tags: [subagents, dispatch, review, constitution, specs, domainspec, governance, wiring]
node_type: constitution
is_session: true
layer: governance, architecture
nature: procedural, technical
status: active
created: 2026-06-17
timestamp: 2026-06-17T13:57:19-03:00
expires: 2026-08-16
conversation_id: 2026-06-17-specs-development-review-wiring
decisions_made: true
contradictions_found: true
specs_updated: [internal_tools/subagents-dispatch-hooks/constitution/specs-development-review-constitution.md, internal_tools/subagents-dispatch-hooks/strategies/specs-development-review.md, implementation/domainspec/.claude/skills/domainspec-pipeline/SKILL.md, implementation/domainspec/.claude/skills/domainspec-spec-feature/SKILL.md]
promoted_candidates: []
expected_importance: 8
importance_rationale: "Establishes a standing spec-review governance layer (constitution + recipe) and wires it into the DomainSpec build pipeline, affecting every future feature spec."
---

# Specs-Development Review — Constitution, Recipe, and Pipeline Wiring

## Summary

Authored a modular specs-development review governance layer — a constitution (R-SDR-1..6) plus a reusable strategy recipe — requiring a red-team `review` over DomainSpec spec documents before spec-derived consumption. The first concrete review ran over the `domainspec-spec` template family (gate-passed, registered, closed `resolved`; adversarial verification cut an over-claimed 1 CRITICAL + 6 MAJOR to 1 MAJOR + 11 MINOR). A subagent review of the initial wiring proposal then killed three critical assumptions (auto-dispatch breaks the single human-gate; the pipeline plans *before* spec; ledger fork), yielding a corrected design wired into `domainspec-pipeline` Step-4b + `domainspec-spec-feature` step-10 as a warn-only deterministic checkpoint reading a `SPEC-REVIEW-REPORT.md` verdict.

## Contradictions

- validates the prior plan→spec ordering concern (framework-unification Route-3 / TUNING-LOOP) — the pipeline runs `plan → spec`, so R-SDR-1 anchors at spec→implementation, not spec→plan.

## Next Steps

- Land the wiring: fast-forward submodule `feat/spec-review-wiring` → `main`, push, then commit scoped parent governance docs + gitlink bump; run `make bump-check`.
- Decide whether to include the template-review evidence (`internal_tools/subagents-dispatch-hooks/docs/reviews/2026-06-16-domainspec-spec-template/`) in the parent commit.
- Apply or defer the C1 MAJOR fix (ship/repoint `domain.md`) in `arcanum/spells/invoke/templates/domainspec-spec/` — change requests in that review's `findings.md`.
- Optional owner flip: R-SDR-1 Step-4b from warn-only to hard `block` (both prerequisites now met).

## Open Questions

- Which ledger do feature-time reviews register into when run from domainspec-core root (parent vs `implementation/domainspec`)? Resolved generically by `$CLAUDE_PROJECT_DIR`; the in-repo two-ledger fork is unconfirmed.
- Add a thin `domainspec-spec-review` producer skill (deferred), or keep the manual `domainspec-subagents-strategy` route?

## Files touched

- internal_tools/subagents-dispatch-hooks/constitution/specs-development-review-constitution.md
- internal_tools/subagents-dispatch-hooks/strategies/specs-development-review.md
- internal_tools/subagents-dispatch-hooks/docs/reviews/2026-06-16-domainspec-spec-template/attacks.md
- internal_tools/subagents-dispatch-hooks/docs/reviews/2026-06-16-domainspec-spec-template/findings.md
- telemetry/agents/subagents-dispatch.yaml
- implementation/domainspec/.claude/skills/domainspec-pipeline/SKILL.md
- implementation/domainspec/.claude/skills/domainspec-spec-feature/SKILL.md
- implementation/domainspec/TUNING-LOOP.md
