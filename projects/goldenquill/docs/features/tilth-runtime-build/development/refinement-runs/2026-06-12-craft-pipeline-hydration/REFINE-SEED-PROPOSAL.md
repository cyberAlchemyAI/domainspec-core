    # Refine Seed Proposal - Tilth runtime build

    ## Target

    - Craft layer: `tilth-runtime-build`
    - Context ID: `CTX-TRB-ROOT`
    - Source contract: `docs/golden-quill-task-role-breakdown-handoff.md`
    - Run ID: `2026-06-12-craft-pipeline-hydration`
    - Preset: `standard`
    - Research mode: `research-if-gap-appears`

    ## Operator Intent

    now at each layer we need to create a dispatch-spec so we can research refine all tasks, and invoke first artifacts with next direction and start hydrating craft pipeline.

    ## Desired Outcome

    A v0.1-safe Tilth runtime plan that separates headless backend work from deprecated or postponed surfaces.

    ## Source Context

    Tilth local inference, routing, vault, ingestion, Scout, mapper, drafting workflow, review, audit log, evidence capture, and Golden Image packaging.

    ## Write Scope

    This run may write only inside `docs/features/tilth-runtime-build/development/refinement-runs/2026-06-12-craft-pipeline-hydration/` until Josh confirms runtime-backed execution. It may update this Craft ledger with route links and next moves. It must not mutate canonical Golden Quill architecture, client org context, promotion-governance state, or executable implementation files.

    ## Current Open Gaps

    - `GAP-TRB-WORK-PACKS` (block): Runtime rows are still task inventory, not sequenced implementation work packs.
- `GAP-TRB-POSTURE-CANON` (block): Posture row depends on boundary-and-canon correction before execution.
- `GAP-TRB-UI-PHASE` (flag): Operator console row needs phase treatment because v0.1 has no UI layer.
- `GAP-TRB-GOLDEN-IMAGE-HANDOFF` (flag): Golden Image assembly depends on hardware/image signing and runtime packaging handoff.

    ## Selected Technique Overlays

    - `baseline_sequence`: Every layer needs the canonical ten-stage Refine order before runtime execution.
- `xray_for_hidden_structure`: The layer has hidden workflow, architecture, dependency, or delivery structure that must be made visible before planning.
- `tournament_for_alternatives`: The layer has multiple plausible sequencing, staffing, design, or roadmap options that should be compared before convergence.
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

    - Dispatch route: `docs/features/tilth-runtime-build/development/refinement-runs/2026-06-12-craft-pipeline-hydration/REFINE-DISPATCH.json`
    - Dispatch validator: `.agents/skills/dispatch-spec/scripts/validate-dispatch.py`
    - Craft ledger YAML parse for `.craft/ledger.yml`
    - Local link check for `CRAFT.md` and generated run artifacts

    ## Permission Boundary

    This seed is strategy-ready only. Runtime-backed stages, delegated subagents, and external research remain blocked until Josh confirms the dispatch strategy.
