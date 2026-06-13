# Refine Strategy Result - Tilth runtime build

## Refine Run Strategy Proposal

- Target: `tilth-runtime-build`
- Desired outcome: A v0.1-safe Tilth runtime plan that separates headless backend work from deprecated or postponed surfaces.
- Preset: `standard`
- Research: `research-if-gap-appears`
- Dispatch route: `REFINE-DISPATCH.json`
- Selected overlays: `baseline_sequence`, `xray_for_hidden_structure`, `tournament_for_alternatives`, `protected_context_for_external_or_sensitive_evidence`
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

Confirm a refine pass that turns the runtime rows into layerable work packs while preserving the no-UI v0.1 boundary.

## Research Strategy

- Strategy artifact: `RESEARCH-STRATEGY.md`
- Dispatch route: `RESEARCH-DISPATCH.json`
- Status: `prepared`; no research execution has run.
