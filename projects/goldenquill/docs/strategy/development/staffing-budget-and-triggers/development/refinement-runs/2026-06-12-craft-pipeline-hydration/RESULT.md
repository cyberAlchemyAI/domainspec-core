# Refine Strategy Result - Staffing, budget, and triggers

## Refine Run Strategy Proposal

- Target: `staffing-budget-and-triggers`
- Desired outcome: A budgetable staffing and trigger plan with explicit blockers for blank hours, rates, and onboarding thresholds.
- Preset: `standard`
- Research: `research-if-gap-appears`
- Dispatch route: `REFINE-DISPATCH.json`
- Selected overlays: `baseline_sequence`, `route_menu_for_ambiguity`, `tournament_for_alternatives`
- Subagent strategy: `recommended`
- Proposed subagents: see `REFINE-DISPATCH.json` `subagent_strategy.roles`
- Join policy: `parent_synthesis`
- Receipt requirements: native stage receipt fields plus subagent lifecycle fields
- Runtime plan after confirmation: run Context Builder, Invoke Define, Interrogation, research decision, Distill, Invoke Design, Interrogation, Distill Repair, Invoke Plan, and final synthesis.
- Deferred work: runtime-backed stages, delegated reviewers, and external research.
- Confirmation prompt: Confirm to run this strategy?

## Strategy Status

- Dispatch validation: `pass`
Status is `flag`: the route is prepared and permission-gated. No Refine stages, Invoke modes, subagents, or external research were executed during hydration.

## Next Move

Confirm a refine pass that compares staffing trigger alternatives and produces the first budget-ready Invoke plan direction.

## Research Strategy

- Strategy artifact: `RESEARCH-STRATEGY.md`
- Dispatch route: `RESEARCH-DISPATCH.json`
- Status: `prepared`; no research execution has run.
