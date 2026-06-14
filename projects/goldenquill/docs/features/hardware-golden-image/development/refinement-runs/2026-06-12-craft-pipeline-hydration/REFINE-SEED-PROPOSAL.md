    # Refine Seed Proposal - Hardware and Golden Image

    ## Target

    - Craft layer: `hardware-golden-image`
    - Context ID: `CTX-HGI-ROOT`
    - Source contract: `docs/golden-quill-task-role-breakdown-handoff.md`
    - Run ID: `2026-06-12-craft-pipeline-hydration`
    - Preset: `standard`
    - Research mode: `research-if-gap-appears`

    ## Operator Intent

    now at each layer we need to create a dispatch-spec so we can research refine all tasks, and invoke first artifacts with next direction and start hydrating craft pipeline.

    ## Desired Outcome

    A smallest-testable hardware and Golden Image plan with acceptance evidence before per-node replication.

    ## Source Context

    Hardware reference workstation, burn-in, OS baseline, imaging, backup/export, signing, and kit readiness.

    ## Write Scope

    This run may write only inside `docs/features/hardware-golden-image/development/refinement-runs/2026-06-12-craft-pipeline-hydration/` until Josh confirms runtime-backed execution. It may update this Craft ledger with route links and next moves. It must not mutate canonical Golden Quill architecture, client org context, promotion-governance state, or executable implementation files.

    ## Current Open Gaps

    - `GAP-HGI-REFERENCE-SPEC` (flag): Reference workstation and approved alternative are not yet captured as a testable spec.
- `GAP-HGI-BURN-IN` (flag): Burn-in and acceptance procedure needs thermal, memory, storage, and inference benchmark thresholds.
- `GAP-HGI-IMAGE-VERIFY` (block): Golden Image write process needs repeatable verification evidence per unit.
- `GAP-HGI-BACKUP-RECOVERY` (block): Backup, customer-owned export, and recovery posture need a tested procedure.

    ## Selected Technique Overlays

    - `baseline_sequence`: Every layer needs the canonical ten-stage Refine order before runtime execution.
- `xray_for_hidden_structure`: The layer has hidden workflow, architecture, dependency, or delivery structure that must be made visible before planning.
- `toy_game_for_low_cost_falsification`: The layer needs a low-cost acceptance or failure scenario before implementation claims harden.

    ## Done Criteria For The Next Approved Run

    - Context Builder emits a strict evidence baseline for this layer.
    - Invoke Define produces a task/term baseline for this layer.
    - Interrogation records unsupported assumptions and stable disagreement.
    - Research decision records whether local evidence is sufficient or a named external gap needs confirmation.
    - Distill selects the smallest coherent unit and records rejected alternatives.
    - Invoke Design and Invoke Plan produce non-executed authoring artifacts with validation surfaces.
    - Final synthesis writes `RESULT.md` and recommends the next owner route without executing it.

    ## Validation Surface

    - Dispatch route: `docs/features/hardware-golden-image/development/refinement-runs/2026-06-12-craft-pipeline-hydration/REFINE-DISPATCH.json`
    - Dispatch validator: `.agents/skills/dispatch-spec/scripts/validate-dispatch.py`
    - Craft ledger YAML parse for `.craft/ledger.yml`
    - Local link check for `CRAFT.md` and generated run artifacts

    ## Permission Boundary

    This seed is strategy-ready only. Runtime-backed stages, delegated subagents, and external research remain blocked until Josh confirms the dispatch strategy.
