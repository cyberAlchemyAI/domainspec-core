# HTML podcast-presentation validation

Validated: `2026-08-03T19:49:45Z`  
Artifact: `presentation.html`  
SHA-256: `79dc004fa7ba0a87a5c8e823ab6346e0d45d1f43f6047142e5165c3c307848eb`

## Result

Status: pass with live-room residue

The HTML implements the approved podcast story as twelve image-led scenes with twenty-one progressive reveals. Full narration is available in the presenter-notes drawer, while the projected surface stays sparse. The original keyboard, touch, timer, fullscreen, notes, help, progress, hash navigation, and print controls remain available.

## Static checks

| Check | Result |
|---|---|
| Slide sections | pass — 12 |
| Presenter-note templates | pass — 12 |
| Progressive fragments | pass — 21 |
| Unique local illustrations | pass — 8 |
| Rejected `Pilot A` language | pass — absent |
| Broken relative image references | pass — none |
| Projected internal paths or authoring IDs | pass — none |

## Browser checks

Runtime:

- Playwright: `1.59.1`
- Chromium revision: `1217`
- Executable: `/home/vrondelli/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome`

| Check | Result |
|---|---|
| All 12 image elements load at 1672 × 941 | pass |
| All progressive reveals advance before slide navigation | pass |
| Presenter-note drawer opens with the correct narration | pass |
| 1440 × 900 settled layouts | pass — 12/12 |
| 1280 × 720 settled layouts | pass — 12/12 |
| 390 × 844 settled layouts | pass — 12/12 |
| Horizontal or vertical projected-surface overflow | pass — none across 36 checks |
| Page and console errors | pass — none |
| Help dialog, timer surface, navigation controls | pass |
| Reduced-motion fallback | present |

The first 1280 × 720 run exposed an over-tall title on Moment 6. A compact title treatment was added, and the complete 36-layout matrix passed on rerun.

## Preview receipt

- URL: `http://127.0.0.1:39913/presentation.html`
- Server: reused managed loopback instance
- HTTP status: `200`
- Content type: `text/html; charset=utf-8`
- Exact target bytes: verified at preview-open time

The preview server receipt proves local reachability and byte identity at the recorded open. It does not prove visual quality; the separate browser matrix supplies layout and interaction evidence.

## Residue

- Live-room pacing and comprehension remain untested.
- Presenter notes share the projected browser window; keep the drawer closed when mirroring the display.
- Responsive browser evidence does not promote the presentation, ontology, or Augmentor implementation state.
