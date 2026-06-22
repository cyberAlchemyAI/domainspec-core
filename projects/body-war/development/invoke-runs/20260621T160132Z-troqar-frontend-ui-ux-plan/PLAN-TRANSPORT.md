# Plan Transport - TROQAR Frontend UX

## Invoke Result

- Mode: plan
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: `.agents/skills/invoke/plan.md`
- Outputs:
  - `projects/body-war/docs/UI-ARCHITECTURE.md`
  - `projects/body-war/docs/features/troqar-product-architecture/UI-SPEC.md`
  - `projects/body-war/docs/features/troqar-product-architecture/TEST-SPEC.md`
  - `projects/body-war/app/e2e/troqar-product-architecture/ui.spec.ts`
  - `IMPLEMENTATION-LAYERING.md`
  - `WORK-PACK.md`
  - `UX-PLAN.md`
- Design views: covered by existing `ARCHITECTURE.md`, `ui-spec.md`, and new UI-SPEC.
- Glossary consistency: n/a; no glossary promotion.
- Dispatch techniques: `sequence`, `artifact_contract_bridge`, `owner_boundary_check`, `scu_swu_reduction`, `recomposition_proof`, `validation_loop`, `residue_ledger`.
- Distill validation: pass with one residue item: Playwright scaffold is not executable until SWU-TUI-002.
- Implementation layering: `IMPLEMENTATION-LAYERING.md`, L0-L3 complete.
- Work-pack: `WORK-PACK.md`, single-file medium plan with SWU manifest.
- Complexity: medium.
- Per-layer planning: compact L0-L3.
- Implementation detail: task specs complete for SWU-level execution.
- Smallest working units: complete.
- Template/profile selection: DomainSpec UI pipeline template adapted to BodyWar static app L0; Invoke plan template used for execution handoff.
- Validation strategy: build/build:e2e/diff-check now; Playwright required after runtime wiring.
- Decisions: keep static app L0; defer React/Vite promotion.
- Unresolved gaps: executable Playwright runtime and visual audit are next SWUs, not blockers for this authoring pass.
- Next route: task-session.

## Source Inputs

- `implementation/domainspec/CHANGELOG.md`
- `implementation/domainspec/docs/UI-ARCHITECTURE.md`
- `implementation/domainspec/templates/ui-spec.md`
- `projects/body-war/docs/features/troqar-product-architecture/SPEC.md`
- `projects/body-war/docs/features/troqar-product-architecture/interfaces.md`
- `projects/body-war/docs/features/troqar-product-architecture/operations.md`
- `projects/body-war/docs/features/troqar-product-architecture/queries.md`
- `projects/body-war/docs/features/troqar-product-architecture/states.md`
- `projects/body-war/docs/features/troqar-product-architecture/ui-spec.md`
- `projects/body-war/docs/features/troqar-product-architecture/VISUAL-DEFINITIONS.md`
- `projects/body-war/app/static/index.html`
- `projects/body-war/app/static/app.js`
- `projects/body-war/app/static/styles.css`
