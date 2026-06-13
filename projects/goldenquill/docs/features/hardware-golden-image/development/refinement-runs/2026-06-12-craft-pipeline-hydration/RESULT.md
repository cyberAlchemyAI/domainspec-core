# Refine Strategy Result - Hardware and Golden Image

## Refine Run Strategy Proposal

- Target: `hardware-golden-image`
- Desired outcome: A smallest-testable hardware and Golden Image plan with acceptance evidence before per-node replication.
- Preset: `standard`
- Research: `research-if-gap-appears`
- Dispatch route: `REFINE-DISPATCH.json`
- Selected overlays: `baseline_sequence`, `xray_for_hidden_structure`, `toy_game_for_low_cost_falsification`
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

Confirm a refine pass that x-rays the hardware-to-image chain and defines the first low-cost acceptance test before install work is routable.

## Research Strategy

- Strategy artifact: `RESEARCH-STRATEGY.md`
- Dispatch route: `RESEARCH-DISPATCH.json`
- Status: `prepared`; no research execution has run.
