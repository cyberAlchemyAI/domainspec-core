# UX Validation — Co-Op Project Showcase

Status: pass for the local L0 review target

Evidence root:
`output/playwright/ux-validator/co-op-showcase-20260726/`

## Black-box behavior

- Fourteen project records and fourteen unique project IDs.
- Fourteen native disclosures, each with opening, vision, now, limit, next,
  and help fields.
- The music lens shows one matching project; reset restores all fourteen.
- Whisper opens by pointer and keyboard and exposes the requested story-world
  knowledge-graph description.
- Presentation mode has twenty unique stages and keeps all fourteen project
  records in the DOM.
- Previous, next, exit, Arrow/Page navigation, progress, and same-record
  project detail are implemented.
- The final `browse → open → present → advance → exit` sequence passes after a
  bounded repair to guard an empty URL hash.
- Meta-narration updates with visible regions and active project stages.

## Responsive and visual review

- Desktop 1440×900: no horizontal overflow; hero, full map, and presentation
  screenshots inspected.
- Mobile 390×844: no document or active-card overflow and no visible bounds
  offenders; self-guided and Whisper presentation screenshots inspected.
- Narrow mobile 320×720: document width equals viewport width; all fourteen
  cards remain available.
- Fixed presentation controls leave the active card vertically scrollable.

## Accessibility and semantics

- First Tab reaches the visible skip link with a 3px focus outline.
- Enter moves focus to `main`.
- Native summary disclosure opens with Enter.
- One H1; H1–H4 levels present; header, two navs, main, and footer landmarks.
- No duplicate IDs or unnamed interactive controls.
- Four live/status regions, fourteen details/summaries, and a reduced-motion
  rule.

## Runtime integrity

- Inline JavaScript syntax check: pass.
- Final console: zero errors and zero warnings.
- Network: one local document request, zero external requests.
- No forms, storage, analytics, tracking, remote fonts, or external assets.
- Final interaction trace packaged and integrity-tested.

## Evidence ceiling

The validation proves local Chromium behavior. It does not prove participant
comprehension, collaboration, recruitment outcome, owner welcome,
cross-browser parity, or publication readiness.
