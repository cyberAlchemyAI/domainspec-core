# Stage 06 — Invoke Redefine / Design

- Capability: `invoke`.
- Mode: `design`.
- Runtime surface: parent-native authoring from accepted review receipts.
- Template/profile: UX-plan companion over the existing page and scene-manifest boundary.
- Design evidence state: `authored-complete`; no product/runtime witness is claimed.
- Plan evidence: pending.
- Verdict: `pass` for Refine design; future implementation and browser validation remain separate.

## Design decision

Replace the current scenic spatial canvas with a **Synthetic Evidence Tower**: one warm-white workspace containing one vertical three-floor tower at left and one evidence detail surface at right. The five Tower System descriptors move to a separate reference region below the primary workspace and retain explanatory refusal behavior.

User-facing tower identity:

> Synthetic evidence tower
>
> Preloaded contract fixture · not representative · read-only navigation

Loaded status:

> Locked synthetic witness loaded
>
> Exact-input validation record bound; this does not establish corpus coverage, representativeness, or authority.

## View 1 — Context

### User goal

The user wants a white canvas and a proper tower rather than a dark image-backed dashboard. The visual object must help orient research evidence without inventing Tower System runtime capability.

### Current state

- one verified synthetic scene manifest;
- three evidence progression scenes;
- five separately namespaced System architecture descriptors;
- working selection, refusal, reset, source, relation, residue, and claim-ceiling behaviors;
- dark/scenic/radial/robot composition that obscures the desired hierarchy.

### Claim ceiling

Candidate-local synthetic mechanics only. No representative tower, real corpus coverage, IDE/product authority, live graph/persona/policy/adjudication, promotion, publication, deployment, release, or production claim.

## View 2 — High-level structure

```text
page
├── compact header
│   ├── CyberAlchemy Lab identity
│   └── locked synthetic witness status
├── primary white workspace
│   ├── tower region
│   │   ├── tower identity
│   │   ├── structural shell + hidden spine
│   │   └── three ordered evidence-floor buttons
│   └── evidence detail region
│       ├── single selection announcement
│       ├── selected floor identity/state/status/ceiling
│       ├── source inspection
│       ├── relations
│       └── open residue
└── Tower System reference
    └── five explanation controls; capabilities unavailable in this Lab
```

Desktop uses two columns for tower and detail. Mobile uses exactly the same DOM order in one column. The System reference is never a floor, second tower, or live room.

## View 3 — Components

### `white-tower-workspace`

- Selector: `[data-layout="white-tower"]`.
- Responsibility: normal-flow canvas and responsive grid.
- Tokens: `--canvas #fbfaf7`, `--surface #fff`, `--ink #17212b`, `--muted #5e6b78`, `--line #d6dee6`, `--blue #1769aa`, `--blue-soft #eaf4fc`, `--amber #9b5d00`, `--amber-soft #fff4dd`, `--focus #0b64c0`.
- Validation: contrast measured during implementation; values remain candidates until checked.

### `tower-shell`

- Selector: `[data-panel="tower-shell"]`.
- Named region with visible heading and description.
- Desktop width `clamp(360px, 34vw, 440px)`, approximately 520–560px tall.
- Contains `[data-list="levels"]` and exactly three `.tower-floor` native buttons.
- Contains `[data-panel="tower-spine"] aria-hidden="true"`; spine has no exclusive meaning.

### `tower-floor`

- Existing identity: `[data-scene-id]`; new class `.tower-floor`.
- Native button with `aria-pressed`, `aria-controls="evidence-detail"`, and accessible name containing floor number, subject, and state.
- Visible fields: label, technical ID, evidence state, implementation status, selected/unselected text.
- No transform movement on hover or selection.

Exact visible bindings:

| ID | Label | State/status | Sources | Required caveat |
| --- | --- | --- | --- | --- |
| `evidence-l0-corpus` | Evidence floor 1 of 3 — Synthetic corpus anchors | `locked-synthetic`; `candidate-local` | `source:toy:readme`, `source:toy:tower`, `source:toy:l0` | fixture locks do not prove corpus coverage or representativeness |
| `evidence-l1-residue` | Evidence floor 2 of 3 — Open representative-selection residue | `open`; `candidate-local` | `source:toy:l1`, `source:toy:residue` | never present the open residue as completed progress |
| `evidence-l2-closure` | Evidence floor 3 of 3 — Closure plan, blocked | `blocked`; `candidate-local` | `source:toy:l2`, `source:toy:gates` | no representative source is selected; the view cannot select one or run a workflow |

Every floor uses the exact view/tower claim ceiling.

### `evidence-detail`

- Selector/id: `[data-panel="evidence-detail"]`, `id="evidence-detail"`.
- One `role="status" aria-live="polite" aria-atomic="true"` summary for meaningful selection/refusal changes.
- `aria-labelledby` resolves to the active floor or System control.
- Consolidates existing scene, source, relation, residue, projection, and claim-ceiling details.
- Selection activation retains focus; reset is the only action that intentionally moves focus to the L0 floor.

### `system-atlas`

- Selector: `[data-panel="system-atlas"]` containing existing `[data-list="system-levels"]` controls.
- Landmark label: **Tower System reference — capabilities unavailable in this Lab**.
- Enabled native buttons reveal refusal explanations.
- Activation retains focus, clears all floor pressed states, sets only the matching System control, and updates evidence detail.
- Detail includes `Unavailable in this Lab`, implementation status, exact refusal reason, evidence locator, and claim ceiling.
- No POST, persistence, execution, scoring, verdict, promotion, or authority effect.

### Retained inspector controls

Retain source detail, relation filter/list, residue detail, projection summary, and claim ceiling inside the detail region. Remove `{ once:true }` from repeatable candidate/source/relation handlers and add repeat-interaction tests.

## View 4 — Workflow process

### Load

1. GET `/api/research-tower/l0`.
2. Existing loader validates exact locks, projection, independent validation, and scene manifest.
3. Render one preloaded synthetic fixture.
4. Select `evidence-l0-corpus` without unexpected focus movement.
5. Announce locked synthetic witness status and bound validation scope.

### Evidence-floor selection

1. User activates a floor with pointer, Enter, or Space.
2. Keep focus on the floor.
3. Set that floor pressed; clear other floors and all System controls.
4. Bind scene state/status/sources/ceiling/caveat to detail.
5. Emit one atomic polite announcement.

### System-reference selection

1. User activates a System descriptor.
2. Keep focus on it.
3. Clear all floor pressed states; set only that System control.
4. Render refusal detail and exact source locator.
5. Perform no network mutation or domain effect.

### Reset

1. Clear System selection.
2. Activate L0.
3. Render L0 detail.
4. Focus its floor button.

### Repeated inspection

Candidate summary, source buttons, and relation filters remain reusable across multiple state changes. Event listeners are persistent.

## View 5 — Decision flow

```text
API result?
├── failure -> textual Witness unavailable/error; no tower interaction
└── success -> render L0 selected
    └── activation kind?
        ├── evidence floor
        │   ├── descriptor binding valid -> select floor + render detail
        │   └── invalid -> fail closed; do not render misleading floor
        └── System reference
            ├── descriptor/source locator valid -> clear floors + render refusal
            └── invalid -> fail closed; no capability simulation
```

## View 6 — Dependencies and interfaces

| Owner surface | Preserved interface | Planned change |
| --- | --- | --- |
| `l0-witness.mjs` | verified candidate-local read model and scene IDs | require scene implementation status, ceiling equality, blocked-state reason, stable System selector validation |
| `/api/research-tower/l0` | read-only GET payload | no endpoint or server change expected |
| `research-tower.html` | existing semantic selectors and interactions | replace composition, wording, layout, and repeat listeners; add tower/detail/atlas selectors |
| Node test | loader/API/page contract | add negative invariants and forbidden-decoration checks |
| Playwright test | behavior/browser surface | rewrite visual-structure assertions; preserve and expand selection/refusal/focus/source/relation/mobile/motion checks |
| Tower System source | layer meaning and evidence tiers | reference only; no runtime realization |

## Responsive and accessibility contract

- Desktop: `max-width:1200px`, two columns, 40–48px gap, 32–48px padding.
- `<=720px`: one column, 16px gutters, floor buttons full-width and >=80px tall.
- Test 320×568 and 390×844 plus existing desktop profile.
- Controls >=44×44px; no horizontal overflow.
- 200% and 400% zoom/reflow preserves labels/state/refusal/focus without two-dimensional scrolling.
- Normal text >=4.5:1; meaningful borders/focus/state marks >=3:1 where applicable.
- Focus ring >=3:1 adjacent contrast and not clipped.
- Reduced motion sets animation name to none and removes transitions; it does not shorten animation duration.
- Manual screen-reader/browser matrix remains a later acceptance item, not an automated-proof claim.

## Removed composition

Delete or retire from the primary page: `.scene-stack`, `.scene`, `.veil`, `.guides`, `.core`, `#constellation-core`, `.source-orbit`, `.residue-signal`, `.live-lab`, `.cowork-robots`, `[data-robot-role]`, `[data-panel="lab-activity"]`, `.tower-focused`, and class-only `[data-action="focus-tower"]`.

## Risks and decisions

- Risk: architecture becomes visual-only. Guard: named region, ordered controls, explicit text states.
- Risk: “floor” collapses semantic axes. Guard: `Evidence floor` labels and external System reference.
- Risk: white palette fails contrast. Guard: measure before acceptance; candidate tokens are not proof.
- Risk: contract hardening expands scope. Decision: it is the first independent SWU and prerequisite, not hidden inside the CSS change.
- Risk: human comprehension is claimed from browser automation. Guard: preserve as unverified until a separate human study.

## Dispatch technique trace

- `handle_handoff`: consumes the distilled tower-design unit.
- `owner_boundary_check`: Design changes presentation intent, not source/authority ownership.
- `component_descriptor`: each shell/floor/detail/System component has one responsibility.
- `residue_ledger`: contrast, screen-reader matrix, human comprehension, representative selection, and runtime capabilities remain open.

## Design boundary

This is an authored design. It neither changes product bytes nor establishes Design validator, Plan evidence, accessibility conformance, usability, runtime capability, authority, promotion, publication, deployment, release, or production readiness.
