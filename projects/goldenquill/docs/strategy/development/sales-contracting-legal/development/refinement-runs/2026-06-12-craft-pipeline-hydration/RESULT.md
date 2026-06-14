# Refine Strategy Result - Sales, contracting, and legal

## Refine Run Strategy Proposal

- Target: `sales-contracting-legal`
- Desired outcome: A legal-first sales and contracting plan with approval boundaries before any first-customer commitment is treated as ready.
- Preset: `standard`
- Research: `research-if-gap-appears`
- Dispatch route: `REFINE-DISPATCH.json`
- Selected overlays: `baseline_sequence`, `protected_context_for_external_or_sensitive_evidence`, `route_menu_for_ambiguity`
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

Confirm a refine pass that separates sales-readiness copy from legal and insurance gates before first LOI work.

## Research Strategy

- Strategy artifact: `RESEARCH-STRATEGY.md`
- Dispatch route: `RESEARCH-DISPATCH.json`
- Status: `prepared`; no research execution has run.
