    # Refine Seed Proposal - Sales, contracting, and legal

    ## Target

    - Craft layer: `sales-contracting-legal`
    - Context ID: `CTX-SCL-ROOT`
    - Source contract: `docs/golden-quill-task-role-breakdown-handoff.md`
    - Run ID: `2026-06-12-craft-pipeline-hydration`
    - Preset: `standard`
    - Research mode: `research-if-gap-appears`

    ## Operator Intent

    now at each layer we need to create a dispatch-spec so we can research refine all tasks, and invoke first artifacts with next direction and start hydrating craft pipeline.

    ## Desired Outcome

    A legal-first sales and contracting plan with approval boundaries before any first-customer commitment is treated as ready.

    ## Source Context

    Sales materials, qualification, agreements, LOI, data policy, procurement notes, insurance, deposits, and invoicing.

    ## Write Scope

    This run may write only inside `docs/strategy/development/sales-contracting-legal/development/refinement-runs/2026-06-12-craft-pipeline-hydration/` until Josh confirms runtime-backed execution. It may update this Craft ledger with route links and next moves. It must not mutate canonical Golden Quill architecture, client org context, promotion-governance state, or executable implementation files.

    ## Current Open Gaps

    - `GAP-SCL-SALES-MATERIALS` (flag): One-pager, demo, segment framing, and pipeline tracker need claims-register evidence before use.
- `GAP-SCL-LEGAL-FIRST-LOI` (block): Legal, LOI, data policy, procurement language, and insurance are onboard-now before first LOI signs.
- `GAP-SCL-DEPOSIT-INVOICING` (flag): Deposit handling, invoicing, and cost tracking need bookkeeper trigger at first revenue.

    ## Selected Technique Overlays

    - `baseline_sequence`: Every layer needs the canonical ten-stage Refine order before runtime execution.
- `protected_context_for_external_or_sensitive_evidence`: The layer may touch legal, security, customer, external, or non-canonical evidence that must stay labelled and permission-gated.
- `route_menu_for_ambiguity`: The layer still contains route, owner, trigger, or output choices that should be explicit before stage execution.

    ## Done Criteria For The Next Approved Run

    - Context Builder emits a strict evidence baseline for this layer.
    - Invoke Define produces a task/term baseline for this layer.
    - Interrogation records unsupported assumptions and stable disagreement.
    - Research decision records whether local evidence is sufficient or a named external gap needs confirmation.
    - Distill selects the smallest coherent unit and records rejected alternatives.
    - Invoke Design and Invoke Plan produce non-executed authoring artifacts with validation surfaces.
    - Final synthesis writes `RESULT.md` and recommends the next owner route without executing it.

    ## Validation Surface

    - Dispatch route: `docs/strategy/development/sales-contracting-legal/development/refinement-runs/2026-06-12-craft-pipeline-hydration/REFINE-DISPATCH.json`
    - Dispatch validator: `.agents/skills/dispatch-spec/scripts/validate-dispatch.py`
    - Craft ledger YAML parse for `.craft/ledger.yml`
    - Local link check for `CRAFT.md` and generated run artifacts

    ## Permission Boundary

    This seed is strategy-ready only. Runtime-backed stages, delegated subagents, and external research remain blocked until Josh confirms the dispatch strategy.
