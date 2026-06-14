    # Refine Seed Proposal - Golden Quill node-on-desk readiness

    ## Target

    - Craft layer: `node-on-desk-readiness`
    - Context ID: `CTX-NOD-ROOT`
    - Source contract: `docs/golden-quill-task-role-breakdown-handoff.md`
    - Run ID: `2026-06-12-craft-pipeline-hydration`
    - Preset: `standard`
    - Research mode: `research-if-gap-appears`

    ## Operator Intent

    now at each layer we need to create a dispatch-spec so we can research refine all tasks, and invoke first artifacts with next direction and start hydrating craft pipeline.

    ## Desired Outcome

    A recomposition-ready non-executed plan that joins all child routes into a working customer-node readiness path.

    ## Source Context

    Parent recomposition surface for all Node on the Desk workstreams.

    ## Write Scope

    This run may write only inside `docs/strategy/development/node-on-desk-readiness/development/refinement-runs/2026-06-12-craft-pipeline-hydration/` until Josh confirms runtime-backed execution. It may update this Craft ledger with route links and next moves. It must not mutate canonical Golden Quill architecture, client org context, promotion-governance state, or executable implementation files.

    ## Current Open Gaps

    - `GAP-NOD-HOURS-RATES` (block): Est. Hrs and Notes / Rate columns are blank across the workbook; staffing and capital budget cannot be computed yet.
- `GAP-NOD-CANON-VOCAB` (block): Workbook posture language includes deprecated vocabulary that must be translated to the current three-posture canon before any customer-facing or engineer-facing surface uses it.
- `GAP-NOD-SEQUENCE` (flag): Workbook lists tasks and roles but not dependency order, done definitions, or recomposition gates.

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

    - Dispatch route: `docs/strategy/development/node-on-desk-readiness/development/refinement-runs/2026-06-12-craft-pipeline-hydration/REFINE-DISPATCH.json`
    - Dispatch validator: `.agents/skills/dispatch-spec/scripts/validate-dispatch.py`
    - Craft ledger YAML parse for `.craft/ledger.yml`
    - Local link check for `CRAFT.md` and generated run artifacts

    ## Permission Boundary

    This seed is strategy-ready only. Runtime-backed stages, delegated subagents, and external research remain blocked until Josh confirms the dispatch strategy.
