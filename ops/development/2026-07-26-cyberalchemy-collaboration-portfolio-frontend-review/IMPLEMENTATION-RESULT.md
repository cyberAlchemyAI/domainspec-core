# CyberAlchemy collaboration portfolio implementation result

Date: `2026-07-26T21:56:37Z`

Source: `projects/co-op-engine/index.html`

Source SHA-256:
`477f2ca9a1c1787054e5e0d75b15417e59d7af113a5fdd403a69702e24cc6196`

Live target: `https://cyberalchemize.com/`

## Outcome

All eight accepted frontend findings are implemented. The automated portion of
`CAFR-EVIDENCE-001` passes locally and live in Playwright Firefox. Its
human-only comprehension, message delivery/response, current welcome,
collaboration-fit, and recruitment/conversion surfaces remain open by design.

This document records implementation after the review dispatch closed. It does
not rewrite the read-only review verdict or convert `FIX` into project or
recruitment authority.

## Finding disposition

| Finding | Result | Implementation and evidence |
| --- | --- | --- |
| `CAFR-HTML-001` | implemented | CyberAlchemy title, header, hero, footer, and presentation fallback replace visible/accessibility-facing Co-Op identity. The page cue, meta labels, cue data, and observer path were removed. Local and live visible/accessibility denylist hits: `0`. |
| `CAFR-HTML-002` | implemented | The shared contact region contains exact query-free email and LinkedIn links plus fourteen static project context targets. Every subject contains only the public project name. LinkedIn uses `_blank` with `noopener noreferrer`. JavaScript-disabled Whisper contact traversal reaches `#contact-whisper`. |
| `CAFR-HTML-004` | implemented | PageUp/PageDown are no longer captured; PageDown moved an overflowing stage from scroll top `0` to `558` without changing the stage. ArrowRight on focused Next did not navigate. Explicit Next and Escape focus recovery pass. |
| `CAFR-HTML-005` | implemented | “Proof”/“evidence” inspectability copy is replaced by “Current state” and “Current artifact.” The project source note says summaries are owner-stated, are not maturity claims, and may have public, non-public, or pending project-owned support. |
| `CAFR-HTML-007` | implemented | Filtered cards, count, contextual heading/status, and jump links synchronize. The music filter exposes one card and one jump; All 14 restores fourteen of each. |
| `CAFR-HTML-008A` | implemented | The global focus indicator uses a 3px ink outline, 4px offset, and an additional adjacent-surface ring. Computed Firefox style: `rgb(11, 16, 32) solid 3px`. |
| `CAFR-HTML-008B` | implemented | Five agenda items and three boundary cards use `h3` headings. Direct styled-`strong` residue in those structures: `0`. |
| `CAFR-HTML-009` | implemented | Passive cue narration and its IntersectionObserver are removed. Passive presentation scrolling produced zero live-region mutations. Explicit filter, copy, and presentation status surfaces remain bounded. |
| `CAFR-EVIDENCE-001` | automated slice implemented; human slice open | Exact contact paths, JavaScript-disabled traversal, mobile behavior, presentation behavior, console/network, headers, and byte identity pass. Working paths are not reported as contact success, comprehension, collaboration, or recruitment. |

## Browser and visual evidence

- Local acceptance:
  `output/playwright/ux-validator/cyberalchemy-portfolio-20260726/acceptance.json`
- Live acceptance:
  `output/playwright/ux-validator/cyberalchemy-portfolio-20260726/deployment/live-acceptance.json`
- Local summary:
  `output/playwright/ux-validator/cyberalchemy-portfolio-20260726/summary.md`
- Desktop full-page screenshot:
  `output/playwright/ux-validator/cyberalchemy-portfolio-20260726/screenshots/desktop-full.png`
- Desktop Whisper presentation screenshot:
  `output/playwright/ux-validator/cyberalchemy-portfolio-20260726/screenshots/desktop-presentation-whisper.png`
- Mobile first-viewport screenshot:
  `output/playwright/ux-validator/cyberalchemy-portfolio-20260726/screenshots/mobile-top.png`
- Deployment receipt:
  `projects/co-op-engine/infra/deployment-receipts/2026-07-26T215637Z-cyberalchemy-portfolio.md`

Visual review caught and repaired two issues before final acceptance: the
project source qualifier leaked above presentation slides, and the dark
45-minute section background lacked a local stacking context. Both corrected
surfaces were re-rendered and re-tested.

## Deployment and isolation

The existing isolated package deployed to `/srv/co-op-engine` and recreated
only `coop-engine-site`. Remote and downloaded HTML hashes equal the local
source. HTTP redirects to HTTPS; TLS validation, security headers, and direct
container health pass.

The Resonant Time Capsule remains HTTP 200 with its expected title and two-week
container continuity. TROQAR root and `/api/status` remain HTTP 200; its app and
database remain healthy with four-week continuity.

## Remaining human evidence

- Cold technical and domain-practitioner readers retell CyberAlchemy’s identity
  and one project’s state, limit, and possible contribution accurately.
- Visitors complete email and LinkedIn inquiry paths without inferring an open
  role or current owner welcome.
- Message delivery, response, collaboration fit, usefulness, current welcome,
  recruitment, and conversion are observed separately if the owner chooses to
  evaluate them.

Google Chrome was unavailable at `/opt/google/chrome/chrome`; browser claims
are limited to Playwright Firefox plus exact-byte HTTP verification.
