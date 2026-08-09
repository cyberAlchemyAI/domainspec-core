# Stage 09 — Invoke Plan: White Tower View work pack

- Capability: `invoke`.
- Mode: `plan`.
- Plan status: `pass` as a non-executed prototype work pack; mutation admission is deliberately not claimed.
- Complexity: medium — four product/test targets and seven independently reviewable units.
- Implementation layering: `stages/09-implementation-layering.md`.
- Execution owner: future Goal/Task Session only after separate user authorization.
- Current execution entry: `selection-ready`, selected first unit `SWU-WT-001`; this Markdown plan is not a machine admission receipt.

## Objective

Replace the dark scenic Research Tower page with the designed white Synthetic Evidence Tower while preserving and strengthening its candidate-local evidence contract, selection/refusal behavior, and browser accessibility boundary.

## Product write boundary

Expected targets only:

1. `projects/ide-extension/src/research-tower/l0-witness.mjs`
2. `projects/ide-extension/public/demo/research-tower.html`
3. `projects/ide-extension/tests/research-tower-explorer.test.mjs`
4. `projects/ide-extension/tests/e2e/research-tower-explorer.spec.mjs`

No server, dependency, package, asset, API-route, fixture, Tower System, Arcanum, authority, promotion, publication, deployment, or Git-history target is expected.

## Finite implementation frontier

| Order | SWU | Primary behavior | Layer | Dependencies |
| ---: | --- | --- | --- | --- |
| 1 | `SWU-WT-001` | enforce truthful floor/System descriptors | L0 | none |
| 2 | `SWU-WT-002` | create white architectural tower structure | L1 | 001 |
| 3 | `SWU-WT-003` | project floor/System selection into one detail surface | L2 | 001, 002 |
| 4 | `SWU-WT-004` | reflow tower/detail/inspection/System regions | L2 | 002, 003 |
| 5 | `SWU-WT-005` | enforce keyboard/focus/live/repeat interaction semantics | L2 | 003, 004 |
| 6 | `SWU-WT-006` | enforce true reduced motion and verified light-state contrast | L2 | 002, 005 |
| 7 | `SWU-WT-007` | close focused automated and manual prototype validation | L3 | 001–006 |

Only one SWU should execute at a time because the HTML and browser test write scopes overlap. The exact proposed first execution boundary is `SWU-WT-001`.

## SWU contracts

### SWU-WT-001 — manifest invariant hardening

- Goal: prevent the UI from receiving a scene that lacks implementation status, has a mismatched ceiling, or is blocked without a reason; validate stable System evidence references.
- Primary behavior: fail-closed scene descriptor admission.
- Write scope: `l0-witness.mjs`, focused Node test.
- Algorithm:
  1. Require non-empty `implementation_status` in evidence descriptors.
  2. Require scene ceiling equals tower and view ceiling.
  3. Require a non-empty blocker/refusal reason when evidence state is blocked/unavailable; update the built blocked L2 descriptor accordingly.
  4. Validate evidence/System IDs remain in their separate closed sets.
  5. Require stable System source reference format or convert current pseudo-selectors to stable source anchors.
  6. Add negative tests for each rejection.
- Edge cases: whitespace-only reason/status, duplicate/cross-axis ID, ceiling type drift, malformed locator.
- Done: new negatives fail before the repair and pass after; current valid fixture still loads.
- Verification: `node tests/research-tower-explorer.test.mjs` from `projects/ide-extension`.
- Split analysis: each invariant could be a smaller assertion, but they jointly define one scene-admission decision and share one independently reviewable test boundary.

### SWU-WT-002 — white architectural tower structure

- Goal: replace the rejected scenic/radial layout with one normal-flow tower shell and anchored detail region.
- Primary behavior: semantic visual structure.
- Write scope: page HTML/CSS and static server-test assertions.
- Rules: remove all listed scenic/robot/orbit selectors and URLs; set `data-layout="white-tower"`; add tower shell/spine/floor/detail/System selectors; render exact labels and candidate tokens; keep System controls outside tower containment.
- Done: DOM contains exactly three native floor buttons inside the tower; no System control is inside; forbidden decoration strings/selectors are absent; current API route remains unchanged.
- Verification: focused Node test plus a structural Playwright assertion.
- Split analysis: white background and shell markup are visually separable, but neither proves the selected architectural direction alone; they form one structural acceptance boundary without interaction behavior.

### SWU-WT-003 — selection and refusal projection

- Goal: map floor or System activation into one detail surface without focus loss or effect inflation.
- Primary behavior: exclusive selection-to-detail state projection.
- Write scope: page JS and focused E2E test.
- Rules: floor activation selects exactly one floor and clears System controls; System activation clears all floors and renders refusal; activation retains focus; reset selects/focuses L0; one atomic status; no POST or product effect.
- Done: initial, three floors, five System refusals, and reset have deterministic states; exact scene fields appear in detail.
- Verification: focused Playwright test.
- Split analysis: floor and System selection share the same exclusive state machine and detail output; separating them would leave the mutual-exclusion behavior untestable.

### SWU-WT-004 — responsive normal-flow reflow

- Goal: preserve tower-to-detail reading order across desktop, 390×844, and 320×568 without overlap or horizontal scrolling.
- Primary behavior: viewport-dependent layout only.
- Write scope: page CSS and mobile E2E assertions.
- Rules: two-column desktop; one-column <=720px; 16px mobile gutters; floors >=80px and all controls >=44×44px; no fixed/absolute docks; test DOM/bounding order, overflow, and 200%/400% reflow.
- Done: layout checks pass without changing selected state semantics.
- Verification: focused mobile Playwright profiles.
- Split analysis: breakpoint, sizes, and overflow jointly answer one responsive-layout decision; keyboard/live-region behavior remains separate.

### SWU-WT-005 — accessible and repeatable interaction

- Goal: make state relationships explicit and interactions reusable.
- Primary behavior: keyboard/focus/announcement/repeat contract.
- Write scope: page markup/JS and focused E2E assertions.
- Rules: native Enter/Space; `aria-controls`; active `aria-labelledby`; one atomic polite status; visible text state; focus ring; remove class-only focus action and `{ once:true }` listeners; test two relation changes and candidate/source/candidate cycle.
- Done: automated names/roles/state/focus/repeat checks pass; no screen-reader conformance claim.
- Verification: focused Playwright accessibility/state assertions.
- Split analysis: these rules share one operability boundary; responsive geometry and motion remain separate.

### SWU-WT-006 — reduced motion and light-state contrast

- Goal: ensure the white visual system remains readable and motion-independent.
- Primary behavior: presentation preference/state-token compliance.
- Write scope: page CSS and focused E2E assertions.
- Rules: no automatic motion by default; under reduce, `animation-name:none` and transitions none; measure candidate palette with normal text 4.5:1 and focus/borders/state 3:1 where applicable; selection still has text/non-color markers.
- Done: computed motion/contrast checks pass and semantic interactions remain unchanged.
- Verification: reduced-motion Playwright test plus contrast calculation/check.
- Split analysis: motion and light-state tokens both concern non-semantic presentation invariants and can be reviewed together after behavior is stable; neither changes data/state projection.

### SWU-WT-007 — prototype validation closeout

- Goal: establish exact local prototype evidence and list remaining manual residue.
- Primary behavior: acceptance evidence aggregation; no product behavior change.
- Write scope: tests only if a witnessed acceptance gap requires a narrow fix; otherwise none.
- Checks:
  - `node tests/research-tower-explorer.test.mjs`
  - `node tests/l0-workbench-ui.test.mjs`
  - `./node_modules/.bin/playwright test tests/e2e/research-tower-explorer.spec.mjs --reporter=line`
  - scoped `git diff --check`
  - manual screen-reader/browser/focus/zoom checklist when available.
- Done: automated suite passes; page error list empty; manual checks recorded as pass or named residue; no deployment/readiness inflation.
- Exemption: validation-only SWU.

## Validation strategy

- L0: loader/manifest positives and negative diagnostics.
- L1: static DOM selector/absence and exact API payload continuity.
- L2: state machine, keyboard/focus/live status, repeat interactions, mobile/reflow, reduced motion, contrast.
- L3: complete focused suite plus manual evidence/residue.

Failure of any acceptance-critical check stops the future implementation run; it does not get converted to a visual preference.

## Non-goals and stop decisions

Stop for any request to add a dependency/engine, change the API contract beyond the named validation invariants, select a real/representative tower, add live agents/graph/policy/adjudication, access external sources, cross private/public boundaries, publish/deploy/release, or change authority/promotion state.

## Dispatch technique trace

- `sequence`: contract → structure → state → reflow → access → presentation → closeout.
- `scu_swu_reduction`: seven independently accepted units; first is the narrow trust step.
- `recomposition_proof`: every unit maps to the authored design and prior scene-canvas objective.
- `validation_loop`: each unit has a check and failure interpretation.
- `owner_boundary_check`: Invoke plans; future Goal/Task Session mutates; source/authority owners remain unchanged.
- `handle_handoff`: future execution consumes this plan and exact source paths.
- `residue_ledger`: manual screen-reader, comprehension, real tower, and production states remain open.

## Plan boundary and next owner

This work pack is non-executed. It deliberately stops before Work-Pack mutation admission, Task Session, Goal execution, product changes, or browser proof. A future user confirmation may authorize a Goal profile that starts with `SWU-WT-001` and validates at each unit boundary.
