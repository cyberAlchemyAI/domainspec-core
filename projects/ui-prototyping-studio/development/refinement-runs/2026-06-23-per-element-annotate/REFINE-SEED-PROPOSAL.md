# Refine Seed Proposal

- Target: `projects/ui-prototyping-studio` — the **annotate + preview surface** (`backend/src/cli/studio.ts` preview server, the `data-od-id` component model, `captureCommentEvent` / `list-pending-comments` / `run-cycle`).
- Seed needed: `yes`
- Source context:
  - `backend/src/cli/studio.ts` (preview server, `/annotate`, `/comment`, `/state`, `/accept|/discard|/revert`, click→postMessage overlay)
  - `backend/src/modules/ui-prototyping-studio/application/` (`capture-comment-event.ts`, `list-pending-comments.ts`, `synthesize-mutation-batch.ts`, `accept-staged-revision.ts`, `run-cycle.test.ts`, `ports.ts`, `session-store.ts`)
  - `backend/src/modules/ui-prototyping-studio/domain/canonicalize.ts` (per-component honest-diff fragment model)
  - variant HTML under `development/prototype-gate/troqar-product-architecture/production-login-variants/` (real `data-od-id` exemplars)
  - **Live session evidence (this conversation):** the saturated tagline had **no `data-od-id`** (un-annotatable per-element) and a `--green` theme-token edit produced a **0-changed honest diff** (theme edits invisible to per-component diff). These two facts are the load-bearing constraints.
- Write scope: `none` (discovery/design only — non-executed plan; no studio code mutated by this run)
- Done criteria: an MVP-ready **non-executed plan** for the per-element Figma-like annotate loop that resolves: (1) per-element addressing for *untagged* elements, (2) element-property extraction model, (3) hover-form capture + persistence, (4) batch-comments → run-cycle UX, (5) expand-candidate-to-full-page / back-to-grid view-state, (6) how the honest per-component diff stays honest when freeform/theme edits are allowed.
- Validation surface: review evidence (interrogation verdicts) + existing `pnpm test` / `pnpm test:e2e` cited as the harness the plan must keep green; no new code run in this refine.
- Preset: `standard` (`full` offered — the target carries a genuine governance/ergonomics tension)
- Loop count: canonical ten-stage loop, budget tuned by preset
- Research: `research-if-gap-appears` (local-first; likely named gap = in-browser stable element-addressing / annotation-overlay UX patterns)
- Dispatch route: `REFINE-DISPATCH.json`
- Dispatch validation: `pass` (conforms to `dispatch.schema.yml`; required: dispatch_id, intent, mode, steps, gates, observability)
- Dispatch techniques: `sequence`, `frame_handoff`, `validation_loop`, `owner_boundary_check`, `observability_grouping`, `route_menu`, `dialectic`, `zig_zag`, `residue_ledger`, `x_ray`, `component_descriptor`, `entity_component_reference`
- Technique overlays selected:
  - `baseline_sequence` — canonical ten-stage order.
  - `route_menu_for_ambiguity` — the operator request contains an explicit unresolved fork ("get element props **by spec, or by** …"), plus "**saved or sent** to the server" (persistence) and tagged-only-vs-any-element (scope). Bounded choices must be recorded before design.
  - `dialectic_for_tension` — **governed integrity** (honest per-component diff, `data-od-id` model, auditable mutation) vs **Figma freeform ergonomics** (annotate *any* element, hover anywhere, theme-level edits). We hit this tension live; it is load-bearing, not decorative.
  - `xray_for_hidden_structure` — the element → property → component-composition model and the browser→server→CLI→cycle→UI comment flow are the hidden structure the design depends on; design step must emit an explanation handle.
- Technique overlays considered but not selected:
  - `tournament_for_alternatives` — deferred: route_menu + dialectic already force the comparison; promote to a tournament inside Distill only if ≥2 full rival designs survive review.
  - `toy_game_for_low_cost_falsification` — deferred to a **next route**: the claim "annotate any element AND keep an honest diff" deserves a controlled failure test, but after the plan exists, not inside it.
  - `memory_residue_for_context_recovery` — folded into Context Builder (this session's residue is cited directly); not a full overlay.
  - `protected_context_for_external_or_sensitive_evidence` — no external/sensitive evidence in scope.
- Planned execution stages:
  - Context Builder evidence baseline: `context-builder`, `standard`, `--strict --emit both --handoff runtime`
  - Invoke Define: `invoke define`
  - Interrogation: `interrogation --mode refine-review`
  - Research decision: `refine`
  - Distill: `distill`, `standard`
  - Invoke Redefine / Design: `invoke design`
  - Interrogation: `interrogation --mode refine-design-review`
  - Distill Repair: `distill`, `validate`
  - Invoke Plan: `invoke plan`
  - Final Interrogation and Synthesis: `interrogation --mode refine-final`, then Refine synthesis
- Runtime default: `arcanum-runtime` (native skill stages via the current host runtime)
- Runtime eligibility: `pass`
- Blocked runtime fields: `none`
- Run manifest: `RUN-MANIFEST.md`
- Evidence index: `evidence-index.json`
- Runtime handoff: `RUNTIME-HANDOFF.md`
- Result artifact: `RESULT.md`
- Recommended next routes: deferred until final synthesis (likely candidates: `task-session` for the MVP slice, `toy-game` falsification of the honest-diff-under-freeform claim).

## Product decisions to record before design (route menu)

These are the genuine forks in the operator request. They will be confirmed with the operator (or recorded as a blocked decision):

1. **Element addressing (untagged elements).** How does a *non-`data-od-id`* element (e.g. the tagline) get a stable handle?
   - (a) auto-mint stable handles (structural CSS path / nth-child fingerprint) at register time;
   - (b) require authors to stamp `data-od-id` (keep governed-only, reject freeform);
   - (c) hybrid: freeform draft handle now, promote to a real `data-od-id` on accept.
2. **Property extraction ("by spec, or by …").**
   - (a) **by spec** — read a per-component descriptor/DNA file (aligns with deferred L4 identity/DNA);
   - (b) **by computed style** — `getComputedStyle` from the rendered DOM (gets "button font" live, headless);
   - (c) **by static parse** — read the variant HTML/CSS.
3. **Persistence ("saved or sent").** Local draft buffer flushed on "run cycle", vs immediate `POST /comment` per edit, vs both (optimistic local + server sync).
4. **View-state.** Expand-candidate-to-full-page + back-to-grid as pure in-page CSS view-state, vs a routed full-page view (`/full/<label>`).
5. **Honest-diff reconciliation.** When a freeform/theme edit changes no `data-od-id` fragment, does the diff: (a) report a new "theme/global" change class; (b) force theme edits to bind to a synthetic component; (c) accept a documented "visual-only, diff-silent" class with a warning.
