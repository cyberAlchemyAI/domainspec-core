# Refine Seed Proposal

- Target: `projects/ui-prototyping-studio` — the **component-system architecture** (not the page surface).
- Seed needed: `yes`
- Source context:
  - `development/deep-spec-dispatch/SYNTHESIZED-DEEP-DESIGN.md` §2.3 (Identity/DNA lifecycle), §2.4 (**Component registry model — Q4, partially RESIDUE**), §3.1–3.4 (UI types, the 24 DNA enums, `DiffSummary` conformance-delta, `proposedChampionLabel`).
  - `development/deep-spec-dispatch/CONTEXT-PACK.md` (s1: resonant-os-design-tokens mapped onto the 24 `UIVisualSignature` enums as `external_context`, gate g1 — **not promoted**).
  - `backend/src/` (built: L0 session machine + governance + `data-od-id` model + honest diff; **the registry/DNA layer is designed, not yet in code**).
  - `provenance/open-design-reference/VENDORED-LICENSES.md` (vendored = voltagent-design-md MIT, nexu-io/open-design Apache-2.0; **resonant NOT vendored**).
- Write scope: `none` (architecture design only; non-executed plan).
- Done criteria: a non-executed plan that (a) names the component-system architecture (`UIElementIdentity` / `UIElementInstance` / `UIIdentityRelationType` / 24 DNA enums / `DiffSummary` / `TypedReference` index), (b) **closes or scopes the Q4 registry-entity residue** (how identities are stored/queried/matched across sessions), (c) decides **owned vs external (resonant) vs hybrid** as the DNA/token source, (d) connects to a future components page and the per-element composition, (e) names deferrals.
- Validation surface: review evidence (interrogation verdicts); the architecture must be expressible in the *existing* domainspec UI vocabulary (deep-spec constraint: no new entity names) and must not break L0.
- Preset: `standard`
- Research: `research-if-gap-appears` (resonant evaluation = a possible named gap → would need bounded-research confirmation).
- Dispatch route: `REFINE-DISPATCH.json` (validation: **pass**).
- Technique overlays selected:
  - `baseline_sequence` — canonical loop.
  - `xray_for_hidden_structure` (**primary**) — the registry → identity → instance → DNA → conformance-delta structure is the uncertainty; the design must emit an explanation handle.
  - `route_menu_for_ambiguity` — the owned vs external vs hybrid source fork.
  - *Not selected:* `dialectic` (light run; route_menu + 2 opposed reviewers suffice — promotable if the fork hardens), `tournament`, `toy_game`, `protected_context` (resonant is named but not being ingested this run).
- Subagent strategy: `recommended` → authorized; 2 roles (`owned-vocabulary-advocate`, `external-system-advocate`), axis owned-DNA-substrate ⟷ external-design-system-adoption.
- Planned stages: context-builder → invoke define → interrogation refine-review (2-agent fanout) → research decision → distill → invoke design → interrogation refine-design-review (parent-led, light) → distill repair → invoke plan → final synthesis.
- Run manifest / index / runtime / result: as named above.

## Architecture fork to resolve (route menu)

1. **Owned-vocabulary registry** — build on `UIElementIdentity`/`UIElementInstance` + the 24 DNA enums; close Q4.
2. **Adopt resonant** — anchor component/token vocabulary on resonant-os-design-system (vendor it); needs license/provenance gate + bounded-research.
3. **Hybrid** — owned registry; map resonant-os-design-tokens onto the 24 DNA enums as `external_context` (gate g1, no canonical promotion) to fill the R-7 DNA underfill (Motion/Interaction/State/Feedback/Numeric).
