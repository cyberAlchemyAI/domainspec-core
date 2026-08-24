# Bella wheel-zoom navigation deployment receipt

- Date: `2026-08-02T14:45:09Z`
- Domain: `https://cyberalchemize.com/bella`
- Source/live/remote SHA-256: `e84c444e470b3ffd5fa11c5f109b3a4d9246a420ff0cd33814d6c3af2472716b`
- Previous live SHA-256: `2d93fd1b65cf2d97416e8c9c19bbbda64d19b38875405004aed572de4fe68ba2`
- Retained rollback backup: `/srv/co-op-engine/backups/20260802T144240Z`
- Container: `coop-engine-site`
- Result: `pass`

## Delivered behavior

- Click or keyboard focus activates wheel/trackpad zoom.
- Zoom is centered on the pointer rather than the canvas center.
- `Escape` releases wheel zoom so the document scroll resumes.
- At a zoom limit, unconsumed wheel input remains available to the page.
- `+`/`−` zoom and `0` fits the full graph.
- The toolbar reports the current zoom percentage.
- Pan and zoom are clamped to the graph bounds.
- A visible hint explains activation, movement, keyboard shortcuts, and release.

## Acceptance

| Check | Result | Evidence |
| --- | --- | --- |
| Inactive wheel | pass | At scroll 400, wheel moved the document to 516 without changing the viewBox |
| Active wheel | pass | Wheel changed the viewBox and zoom indicator to 128% |
| Pointer anchoring | pass | Measured live drift was 0.09 px |
| Release | pass | After `Escape`, wheel again moved the document 400 to 516 while viewBox remained unchanged |
| Keyboard parity | pass | `+` reached 164%; `0` restored 100% full-graph fit |
| Graph invariants | pass | 75 nodes, 164 edges, valid endpoints, zero overlap, equivalent navigator, complete provenance |
| Existing navigation | pass | Succession route and inspector stayed synchronized; `família` search returned six results |
| Mobile | pass | 390 by 844 viewport had no horizontal document overflow |
| Browser health | pass | Firefox console reported zero errors and zero warnings; no external requests |
| Byte identity | pass | Local, remote, and live Bella HTML share the recorded hash |
| Neighbor continuity | pass | Portfolio and Craft hashes remained unchanged; Time Capsule and TROQAR remained HTTP 200 |

## Coverage boundary

The live update has Firefox desktop/mobile evidence and the local exact bytes have Chrome-for-testing evidence. It does not yet prove touch-pinch graph navigation, human discoverability, learning effectiveness, or assistive-technology behavior beyond the exercised DOM and keyboard checks.

