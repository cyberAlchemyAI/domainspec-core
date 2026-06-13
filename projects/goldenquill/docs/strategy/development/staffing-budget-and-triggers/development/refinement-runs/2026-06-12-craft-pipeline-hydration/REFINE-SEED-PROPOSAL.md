    # Refine Seed Proposal - Staffing, budget, and triggers

    ## Target

    - Craft layer: `staffing-budget-and-triggers`
    - Context ID: `CTX-SBT-ROOT`
    - Source contract: `docs/golden-quill-task-role-breakdown-handoff.md`
    - Run ID: `2026-06-12-craft-pipeline-hydration`
    - Preset: `standard`
    - Research mode: `research-if-gap-appears`

    ## Operator Intent

    now at each layer we need to create a dispatch-spec so we can research refine all tasks, and invoke first artifacts with next direction and start hydrating craft pipeline.

    ## Desired Outcome

    A budgetable staffing and trigger plan with explicit blockers for blank hours, rates, and onboarding thresholds.

    ## Source Context

    Roles, gaps, onboarding triggers, hours, rates, and capital budget readiness.

    ## Write Scope

    This run may write only inside `docs/strategy/development/staffing-budget-and-triggers/development/refinement-runs/2026-06-12-craft-pipeline-hydration/` until Josh confirms runtime-backed execution. It may update this Craft ledger with route links and next moves. It must not mutate canonical Golden Quill architecture, client org context, promotion-governance state, or executable implementation files.

    ## Current Open Gaps

    - `GAP-SBT-HOURS-RATES` (block): Est. Hrs and Notes / Rate are blank; budget cannot be computed.
- `GAP-SBT-ONBOARD-NOW` (flag): Domain Experts, Legal, and Security Reviewer are onboard-now/near-now roles that need procurement shape and cost.
- `GAP-SBT-ONBOARD-LATER` (flag): Customer Success and Field Tech handoff from Josh/engineers needs deployed-node trigger criteria.

    ## Selected Technique Overlays

    - `baseline_sequence`: Every layer needs the canonical ten-stage Refine order before runtime execution.
- `route_menu_for_ambiguity`: The layer still contains route, owner, trigger, or output choices that should be explicit before stage execution.
- `tournament_for_alternatives`: The layer has multiple plausible sequencing, staffing, design, or roadmap options that should be compared before convergence.

    ## Done Criteria For The Next Approved Run

    - Context Builder emits a strict evidence baseline for this layer.
    - Invoke Define produces a task/term baseline for this layer.
    - Interrogation records unsupported assumptions and stable disagreement.
    - Research decision records whether local evidence is sufficient or a named external gap needs confirmation.
    - Distill selects the smallest coherent unit and records rejected alternatives.
    - Invoke Design and Invoke Plan produce non-executed authoring artifacts with validation surfaces.
    - Final synthesis writes `RESULT.md` and recommends the next owner route without executing it.

    ## Validation Surface

    - Dispatch route: `docs/strategy/development/staffing-budget-and-triggers/development/refinement-runs/2026-06-12-craft-pipeline-hydration/REFINE-DISPATCH.json`
    - Dispatch validator: `.agents/skills/dispatch-spec/scripts/validate-dispatch.py`
    - Craft ledger YAML parse for `.craft/ledger.yml`
    - Local link check for `CRAFT.md` and generated run artifacts

    ## Permission Boundary

    This seed is strategy-ready only. Runtime-backed stages, delegated subagents, and external research remain blocked until Josh confirms the dispatch strategy.
