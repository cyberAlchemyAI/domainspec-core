    # Refine Seed Proposal - Company operations and finance

    ## Target

    - Craft layer: `company-operations-finance`
    - Context ID: `CTX-COF-ROOT`
    - Source contract: `docs/golden-quill-task-role-breakdown-handoff.md`
    - Run ID: `2026-06-12-craft-pipeline-hydration`
    - Preset: `standard`
    - Research mode: `research-if-gap-appears`

    ## Operator Intent

    now at each layer we need to create a dispatch-spec so we can research refine all tasks, and invoke first artifacts with next direction and start hydrating craft pipeline.

    ## Desired Outcome

    An operations floor plan that separates first-revenue setup from ongoing support and finance cadence.

    ## Source Context

    Entity hygiene, banking, bookkeeping, filing, support channel, issue log, Node Care operations, and validation packet maintenance.

    ## Write Scope

    This run may write only inside `docs/strategy/development/company-operations-finance/development/refinement-runs/2026-06-12-craft-pipeline-hydration/` until Josh confirms runtime-backed execution. It may update this Craft ledger with route links and next moves. It must not mutate canonical Golden Quill architecture, client org context, promotion-governance state, or executable implementation files.

    ## Current Open Gaps

    - `GAP-COF-ENTITY-HYGIENE` (flag): Entity hygiene, banking, bookkeeping, filing, and insurance need operating checklist.
- `GAP-COF-SUPPORT-TRIAGE` (block): Support channel, issue log, and triage rules need boundaries for support absorbs vs engineering sees.
- `GAP-COF-NODE-CARE-OPS` (flag): Node Care updates, source-index maintenance, quarterly check-ins, and vault care need operating cadence.
- `GAP-COF-VALIDATION-PACKET` (flag): Investor/funder relations and validation packet maintenance need evidence ownership.

    ## Selected Technique Overlays

    - `baseline_sequence`: Every layer needs the canonical ten-stage Refine order before runtime execution.
- `route_menu_for_ambiguity`: The layer still contains route, owner, trigger, or output choices that should be explicit before stage execution.
- `memory_residue_for_context_recovery`: The layer depends on prior session decisions, linked ledgers, or open residue that should be recovered by handle.

    ## Done Criteria For The Next Approved Run

    - Context Builder emits a strict evidence baseline for this layer.
    - Invoke Define produces a task/term baseline for this layer.
    - Interrogation records unsupported assumptions and stable disagreement.
    - Research decision records whether local evidence is sufficient or a named external gap needs confirmation.
    - Distill selects the smallest coherent unit and records rejected alternatives.
    - Invoke Design and Invoke Plan produce non-executed authoring artifacts with validation surfaces.
    - Final synthesis writes `RESULT.md` and recommends the next owner route without executing it.

    ## Validation Surface

    - Dispatch route: `docs/strategy/development/company-operations-finance/development/refinement-runs/2026-06-12-craft-pipeline-hydration/REFINE-DISPATCH.json`
    - Dispatch validator: `.agents/skills/dispatch-spec/scripts/validate-dispatch.py`
    - Craft ledger YAML parse for `.craft/ledger.yml`
    - Local link check for `CRAFT.md` and generated run artifacts

    ## Permission Boundary

    This seed is strategy-ready only. Runtime-backed stages, delegated subagents, and external research remain blocked until Josh confirms the dispatch strategy.
