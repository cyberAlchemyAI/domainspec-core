# Visual systems review receipt

## Identity

- Action: `spawn-0001`.
- Dispatch: `20260809T192255Z-white-canvas-proper-tower`.
- Run / wave / step: `review-run-001` / `white-canvas-review` / `s03-review`.
- Role / capability / mode: `visual-systems-reviewer` / `interrogation` / `refine-review`.
- Mutation: none; read-only static source review.
- Receipt completeness: pass.
- Target-design verdict: `flag` pending implementation and browser evidence.

## Findings

1. The current dark color scheme, rotating photographic scenes, veil, glass panels, orbit, live-lab sprite, and robots contradict the selected White Canvas.
2. There is no proper tower: evidence floors are horizontal pills and the `.tower-scene` is a detached card. No shell or spine exists.
3. Floor selection is separated from its state and claim ceiling across competing absolute-positioned regions.
4. Evidence floors and Tower System controls share almost the same control language, which is too weak to protect their semantic distinction.
5. The mobile view remains an absolute 990px stage with offset docks; static inspection cannot establish non-overlap or tower-to-detail reading order.
6. Existing tests require the old scenic/robot/orbit composition and would reward regression from the new direction.

## Selected geometry

Use a centered `max-width: 1200px` white workspace with a two-column content grid:

- left `clamp(360px, 34vw, 440px)` tower shell;
- right `minmax(480px, 1fr)` evidence detail;
- `40–48px` gap and `32–48px` canvas padding;
- `520–560px` shell with one structural border, 16px radius, restrained shadow, roof/base lines, and 2px internal spine;
- three native floor buttons in L0 → L1 → L2 DOM order, each at least 96px high with 18–20px connectors;
- every floor visibly exposes label, technical ID, evidence state, and implementation status;
- selected state is textual and structural, not color-only.

The top-to-bottom L0 → L2 order preserves evidence progression and keyboard order. It must not be visually inverted to mimic physical floor numbering.

## Mobile transformation

At `<=720px`, use one normal-flow column:

1. compact tower shell;
2. evidence detail;
3. source/relation/residue inspection;
4. separate System Atlas.

Use 16px gutters, full-width floors, at least 44px targets, at least 80px floor height, no fixed/absolute docks, no tabs or carousel.

## Component placement

- Move `[data-list="levels"]` inside `[data-panel="tower-shell"]`.
- Retain `[data-scene-id]`; add `.tower-floor`.
- Add an `aria-hidden="true"` `[data-panel="tower-spine"]`; it carries no exclusive meaning.
- Add `[data-panel="evidence-detail"]` beside the tower on desktop and immediately after it in DOM order.
- Keep scene, source, relation, residue, and ceiling information in that anchored detail region.
- Put `[data-panel="system-atlas"]` outside the tower shell. System activation clears all floor pressed states and renders refusal detail.

## Candidate tokens

```css
--canvas: #fbfaf7;
--surface: #ffffff;
--ink: #17212b;
--muted: #5e6b78;
--line: #d6dee6;
--guide: #e9eef3;
--blue: #1769aa;
--blue-soft: #eaf4fc;
--amber: #9b5d00;
--amber-soft: #fff4dd;
--success: #1d6b52;
--danger: #a13a32;
--focus: #0b64c0;
--shadow: 0 16px 40px rgba(23, 33, 43, 0.08);
```

These are candidates, not contrast proof. Floors use neutral/blue structure; the System Atlas uses a neutral dashed structure plus amber refusal text.

## Interaction states

- Hover changes fill/border without moving geometry.
- Focus uses a 3px ring with offset.
- Selected floor combines `aria-pressed="true"`, a solid edge, pale fill, explicit selected label/icon, and emphasized decorative spine node.
- Atlas selection uses explicit `Unavailable`; all floor controls are unpressed.
- Loading/error remains textual; no glow-only state.
- Reset activates and focuses `evidence-l0-corpus`.
- Reduced motion removes connector/selection transitions but preserves content and focus.
- Retain a motion control only if any continuous decoration remains.

## Rejected alternatives

- Recoloring the dark scene instead of removing it.
- Retaining radial orbit/constellation composition.
- Three unrelated cards without a shared shell/spine.
- Treating Tower System layers as floors or a second tower.
- CSS visual order that differs from DOM order.
- Mobile tabs, carousel, fixed docks, modal-only detail, or animation-defined hierarchy.

## Selector and test change requests

Retain/relocate the workbench root, levels/system lists, scene status/content/ceiling/unavailable panels, source/residue detail, relation filter/list, claim ceiling, and reset action. Add:

- `[data-layout="white-tower"]`
- `[data-panel="tower-shell"]`
- `.tower-floor`
- `[data-panel="tower-spine"]`
- `.tower-connector`
- `[data-panel="evidence-detail"]`
- `[data-panel="system-atlas"]`

Remove or retire `.scene-stack`, `.scene`, `.veil`, `.guides`, `#constellation-core`, `.core`, `.source-orbit`, `[data-panel="live-lab"]`, `.cowork-robots`, `[data-robot-role]`, `.tower-focused`, and `[data-action="focus-tower"]`.

E2E must assert the new layout and containment, keep floor count/keyboard/refusal/reset/source/relation/residue/ceiling/overflow behavior, prove System controls are outside the tower and clear floor selection, assert old decoration is absent, and prove mobile order/bounds plus reduced-motion parity.

## Severity

- P0: remove scenic/radial composition; build one semantic shell with three native floors; separate the System Atlas; use responsive normal flow; update tests.
- P1: consolidate detail; implement complete visual states; preserve reset/keyboard; contrast-check the palette.
- P2: restrained guides/spine motion, roof/base silhouette, typography/density polish.

## Evidence and boundary

Sources: `stages/02-define.md`, `strategy-inventory-packet.json`, current page, browser test, prior Refine result, and Tower System view. No server/test/browser run occurred. Contrast, clipping, touch geometry, focus sequence, responsive stacking, and hierarchy remain unverified. Return to Refine design/plan; separate authorization is required for implementation and browser acceptance.
