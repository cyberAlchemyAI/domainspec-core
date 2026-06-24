# Runtime Handoff

## Runtime Boundary

- Runtime: `arcanum-runtime`
- Adapter: `native-skill` (parent-owned native runtime dispatch; subagents via the Agent tool)
- Owner: `refine`
- Status: `not_run` — awaiting operator permission (g02-subagent-permission + g05-product-fork-decision)
- Runtime run folder: `development/refinement-runs/2026-06-23-per-element-annotate/`

## Runtime Objective

Run the canonical Refine loop for the **UI Prototyping Studio annotate/preview surface** using parent-owned native runtime dispatch and produce `RESULT.md` — an MVP-ready non-executed plan for the per-element Figma-like annotate loop.

## Dispatch Route

- Dispatch route: `REFINE-DISPATCH.json`
- Dispatch schema: `.claude/skills/dispatch-spec/dispatch.schema.yml`
- Dispatch validation: `pass` (validate-dispatch.py → `VALIDATION=pass`)
- Dispatch ID: `2026-06-23-per-element-annotate`
- Technique overlays: `baseline_sequence`, `route_menu_for_ambiguity`, `dialectic_for_tension`, `xray_for_hidden_structure`

## Strategy Permission State

- Strategy preview shown: `yes` (Refine Run Strategy Proposal, this conversation)
- subagent_strategy.status: `recommended`
- Proposed roles: `ergonomics-advocate`, `governance-integrity-skeptic`, `implementation-cost-realist`
- Anti-bias axis: `ergonomic-freedom <-> governed-integrity`, grounded by implementation-cost
- Authorization: `pending` — operator has not yet confirmed delegated subagent + runtime-backed execution.

## Stage Receipt Contract

- Capability handles: `context-builder`, `invoke`, `interrogation`, `distill`, `refine` (native skills)
- Runtime surface: `native skill | approved subagent`
- Receipt kind: `native-stage | subagent | blocked`
- Receipt artifact: `stages/<NN>-<stage>.md` (filled at execution) or blocked reason
- Receipt status: `not_run` for all stages

## Handoff Requirements

- Context Builder handoff pack: `pending` (produced at s01)
- Strict coverage: `pending`
- Runtime status: `not_run`
- Dispatch route validation: `pass`
- Run manifest: `RUN-MANIFEST.md`
- Evidence index: `evidence-index.json`

## Blocked Fields

- `authorization`: operator confirmation for subagent + runtime-backed execution not yet given.
- `product_forks`: five product-fork decisions (g05) not yet confirmed; design (s06) is gated on them.
