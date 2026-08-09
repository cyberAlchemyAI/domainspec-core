# 09 — Invoke Plan: Tower Scene Canvas work pack (not executed)

## Work pack `WP-CAL-TOWER-SCENE-V1`

### SWU-CAL-SCENE-001 — Manifest boundary

Create a pure `buildTowerSceneManifest` module from `loadResearchTowerL0` output and tests. It accepts exactly one synthetic tower, emits the three evidence-scene descriptors, and rejects missing source/state/ceiling/axis or ambiguous level IDs.

Validation: focused Node test for valid manifest plus negative fixtures. Stop if a descriptor would imply a real corpus, authority, promotion, or runtime graph.

### SWU-CAL-SCENE-002 — Semantic navigation shell

Evolve the Research Tower page into an open-canvas shell with a tower list, level strip, selected state, evidence status region, unavailable panel, and focus/reset orientation controls. Keep the current source/relation detail dock as an evidence-level subview.

Validation: page/server integration assertions for selectors and DOM semantics. Stop if controls become canvas-only or if mobile layout hides semantic selection.

### SWU-CAL-SCENE-003 — Three synthetic scenes

Implement Corpus Observatory, Residue Conservatory, and Closure Workshop using only descriptor content. Add a separately namespaced, unavailable Tower System map only if it carries exact implementation/status copy.

Validation: selected scene renders source/state/ceiling; negative unavailable descriptor renders refusal. Stop if visual content invents a source, persona, decision, verdict, or closure.

### SWU-CAL-SCENE-004 — Motion/accessibility/browser proof

Make decoration `aria-hidden`; preserve pause control; keep reduced-motion state semantic and immediate; ensure keyboard, touch size, narrow viewport, focus/reset, and no-error browser behavior.

Validation: focused Node tests and Playwright Chromium desktop/mobile/reduced-motion acceptance. Stop at any browser acceptance failure. No game/animation dependency is introduced in this work pack.

## Execution order and boundary

`001 -> 002 -> 003 -> 004`. The work pack is implementation-ready as a candidate plan only. It does not authorize a Craft ledger application, source selection, external research, engine adoption, product mutation, promotion, publication, deployment, or release.
