# CRAFT - Staffing, Budget, And Triggers

Human-readable view of [.craft/ledger.yml](.craft/ledger.yml). The ledger is the source of truth.

## Quick Links

- Source workbook: [golden-quill-task-role-breakdown-handoff.md](../../../golden-quill-task-role-breakdown-handoff.md)
- Parent space: [node-on-desk-readiness](../node-on-desk-readiness/CRAFT.md)

## Active Gaps

- `GAP-SBT-HOURS-RATES`: blank hours/rates.
- `GAP-SBT-ONBOARD-NOW`: paid expert/legal/security onboarding.
- `GAP-SBT-ONBOARD-LATER`: Customer Success and Field Tech trigger model.

## Open Decision

- `DEC-SBT-TRIGGER-MODEL`: deployment count or revenue trigger for each absorbed role.

## Next Move

Validate the research dispatch, then decide whether to approve local-first research execution and any bounded external research for this node.

## Pipeline Hydration

- Refine run: [2026-06-12-craft-pipeline-hydration](development/refinement-runs/2026-06-12-craft-pipeline-hydration/RUN-MANIFEST.md)
- Dispatch route: [REFINE-DISPATCH.json](development/refinement-runs/2026-06-12-craft-pipeline-hydration/REFINE-DISPATCH.json)
- Runtime handoff: [RUNTIME-HANDOFF.md](development/refinement-runs/2026-06-12-craft-pipeline-hydration/RUNTIME-HANDOFF.md)
- Invoke first artifacts direction: [INVOKE-FIRST-ARTIFACTS.md](development/refinement-runs/2026-06-12-craft-pipeline-hydration/INVOKE-FIRST-ARTIFACTS.md)
- Status: strategy-ready and permission-gated; runtime stages, subagents, Invoke modes, and external research are not run yet.
- Next move: review the strategy and confirm whether this layer should enter the runtime-backed Refine loop.

## Research Strategy

- Strategy artifact: [RESEARCH-STRATEGY.md](development/refinement-runs/2026-06-12-craft-pipeline-hydration/RESEARCH-STRATEGY.md)
- Dispatch route: [RESEARCH-DISPATCH.json](development/refinement-runs/2026-06-12-craft-pipeline-hydration/RESEARCH-DISPATCH.json)
- Status: strategy-ready and permission-gated; external research and research subagents are not run yet.
- Next move: validate the route, then decide whether to approve local-first research execution for this node.
