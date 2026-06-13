    # Refine Seed Proposal - Capital Logic Library

    ## Target

    - Craft layer: `capital-logic-library`
    - Context ID: `CTX-CLL-ROOT`
    - Source contract: `docs/golden-quill-task-role-breakdown-handoff.md`
    - Run ID: `2026-06-12-craft-pipeline-hydration`
    - Preset: `standard`
    - Research mode: `research-if-gap-appears`

    ## Operator Intent

    now at each layer we need to create a dispatch-spec so we can research refine all tasks, and invoke first artifacts with next direction and start hydrating craft pipeline.

    ## Desired Outcome

    A library-hydration plan that links promotion governance without overwriting the existing promotion-governance Craft ledger.

    ## Source Context

    Card schema, launch cards, expert review, seed libraries, and recurring funder rule packs.

    ## Write Scope

    This run may write only inside `docs/features/capital-logic-library/development/refinement-runs/2026-06-12-craft-pipeline-hydration/` until Josh confirms runtime-backed execution. It may update this Craft ledger with route links and next moves. It must not mutate canonical Golden Quill architecture, client org context, promotion-governance state, or executable implementation files.

    ## Current Open Gaps

    - `GAP-CLL-LAUNCH-CARDS` (flag): Five launch cards need current authoring and validation status captured.
- `GAP-CLL-DOMAIN-EXPERTS` (block): Four segment experts need scoped paid structured input.
- `GAP-CLL-RULE-PACKS` (flag): Recurring funder rule packs need ownership and ongoing maintenance shape.

    ## Selected Technique Overlays

    - `baseline_sequence`: Every layer needs the canonical ten-stage Refine order before runtime execution.
- `memory_residue_for_context_recovery`: The layer depends on prior session decisions, linked ledgers, or open residue that should be recovered by handle.
- `protected_context_for_external_or_sensitive_evidence`: The layer may touch legal, security, customer, external, or non-canonical evidence that must stay labelled and permission-gated.

    ## Done Criteria For The Next Approved Run

    - Context Builder emits a strict evidence baseline for this layer.
    - Invoke Define produces a task/term baseline for this layer.
    - Interrogation records unsupported assumptions and stable disagreement.
    - Research decision records whether local evidence is sufficient or a named external gap needs confirmation.
    - Distill selects the smallest coherent unit and records rejected alternatives.
    - Invoke Design and Invoke Plan produce non-executed authoring artifacts with validation surfaces.
    - Final synthesis writes `RESULT.md` and recommends the next owner route without executing it.

    ## Validation Surface

    - Dispatch route: `docs/features/capital-logic-library/development/refinement-runs/2026-06-12-craft-pipeline-hydration/REFINE-DISPATCH.json`
    - Dispatch validator: `.agents/skills/dispatch-spec/scripts/validate-dispatch.py`
    - Craft ledger YAML parse for `.craft/ledger.yml`
    - Local link check for `CRAFT.md` and generated run artifacts

    ## Permission Boundary

    This seed is strategy-ready only. Runtime-backed stages, delegated subagents, and external research remain blocked until Josh confirms the dispatch strategy.
