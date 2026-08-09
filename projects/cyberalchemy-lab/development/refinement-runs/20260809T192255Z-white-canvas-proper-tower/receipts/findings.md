# White canvas proper tower — verified change requests

## Review boundary

Two independent read-only reviewers attacked the same current interface from different methodologies. The parent accepts the change-request list below as the review deliverable. `FIX` means the future implementation must apply the request; it does not mean product files were changed in this run.

## Current canvas

| # | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| V1 | `projects/ide-extension/public/demo/research-tower.html` | Dark color scheme, three rotating background images, veil, glass panels, circular core/source orbit, live-lab sprite, robots, and absolute docks dominate the current page. | MAJOR | Remove the entire scenic/radial composition and use a warm-white normal-flow workspace. |
| V2 | same | Evidence controls are horizontal pills; there is no shared tower shell or spine, and the detail card is detached. | MAJOR | Build one vertical semantic tower shell containing exactly three native floor buttons and an `aria-hidden` structural spine. |
| V3 | same | Evidence floors and System controls share near-identical visual/control treatment. | MAJOR | Move the System Atlas outside the tower and use explicit unavailable/refusal language and containment. |
| V4 | same | Absolute mobile stage/dock placement cannot establish a stable reading order or non-overlap. | MAJOR | Use a two-column desktop grid and one-column mobile normal flow with tower → detail → inspection → System reference order. |
| S1 | same | “Proper Tower,” “selected tower,” “L0 corpus,” “L2 closure,” and “Witness verified” exceed or blur the synthetic evidence ceiling. | MAJOR | Use synthetic-fixture language, `Evidence floor N of 3`, blocked/open states, and “Locked synthetic witness loaded.” |
| S2 | same | Class-only “Focus tower” styling does not perform keyboard focus; repeatable interactions use one-shot listeners. | MAJOR | Remove the focus-style action or make it actually move focus; make all repeatable interactions persistent and test them twice. |
| S3 | same | Selection/refusal lacks a fully specified single announcement and control/detail relationship. | MAJOR | Add `aria-controls`, dynamic `aria-labelledby`, one atomic polite status, focus-stable activation, and text states independent of color. |

Verdict: **FIX**.

## Scene manifest and validator

| # | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| M1 | `projects/ide-extension/src/research-tower/l0-witness.mjs` | Evidence scene validation does not require `implementation_status`. | MAJOR | Require non-empty `implementation_status` on every evidence scene. |
| M2 | same | Scene ceiling is present but not checked for exact equality with tower/view ceiling. | MAJOR | Reject any scene/tower/view claim-ceiling mismatch. |
| M3 | same | A blocked scene may retain `unavailable_reason: null`. | MAJOR | Require a non-empty blocker/refusal reason for blocked or unavailable evidence states. |
| M4 | same | System `source_refs` are non-empty but are not checked as stable source selectors. | MINOR | Bind and validate stable source selectors before exposing inspectable System evidence links. |

Verdict: **FIX**.

## Tests

| # | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| T1 | `projects/ide-extension/tests/research-tower-explorer.test.mjs` | Server assertions currently require background images, sprite, robots, and lab animation. | MAJOR | Assert white-tower structure and absence of forbidden decoration; add manifest negatives for M1–M4 and axis collision. |
| T2 | `projects/ide-extension/tests/e2e/research-tower-explorer.spec.mjs` | Tests require spatial canvas, live lab/robots, scenic motion, `.01ms` reduced motion, and focus-style class behavior. | MAJOR | Rewrite around tower containment/order, selection/refusal mutual exclusion, real focus, repeated interactions, no POST, reflow/overflow/zoom, contrast targets, and true no-animation reduced motion. |
| T3 | same | Existing browser checks do not prove a manual screen-reader/browser matrix or human comprehension. | MINOR | Keep those as explicit future/manual evidence; do not make conformance or usability claims from automated tests alone. |

Verdict: **FIX**.

## Accepted design

- Desktop: a centered `max-width: 1200px` two-column workspace; 360–440px tower at left, flexible evidence detail at right.
- Mobile: one normal-flow column with tower identity/floors, detail, inspection, then separate System reference.
- Tower: one shell, one hidden spine, three L0→L2 native floor controls in DOM order.
- Detail: one anchored surface containing scene state/content/ceiling plus source/relation/residue inspection.
- Semantics: exact synthetic labels and floor bindings; System activation clears floor selection and renders focus-stable refusal.
- Motion: no continuous motion by default; reduced motion removes animation and transitions rather than shortening them.

## Parent approval

The parent accepts this cited list for Refine repair and planning. No finding is refuted. Review closeout is `resolved` because the change requests are accepted as deliverables; product readiness remains absent until a separate implementation and validation run.
