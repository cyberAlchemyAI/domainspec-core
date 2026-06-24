# Stage 02 — Invoke Define

- Capability: `invoke` · Mode: `define` · Owner receipt: parent coordinator
- Status: **pass**

## Problem definition

**Today** the studio annotates only `data-od-id` components, via *click*, with a fixed `severity/intent/note` form, in a height-clipped grid. **The operator wants** a Figma-like surface: hover *any* element → an inline form pre-filled with that element's properties → comments saved to the server and batched → a CLI/skill-triggered cycle synthesizes a candidate → user reviews, can **expand a candidate to full page and return to the grid**.

## Definition of the unit being refined

A **per-element annotation loop** = `{ address an element, extract its properties, capture an intent against it, persist, drain via CLI, synthesize a candidate, review at variant- and page-scale }`.

## Invariants that must survive (non-negotiable studio identity)

- **D1 Two-gate apply** — agent stages a candidate; head advances only on explicit human accept.
- **D2 Honest diff** — the per-component diff must not *lie*. If a change is visual but unattributed, the surface must say so rather than report "0 changes."
- **D3 Append-only manifest** — every accepted revision recorded; reversible verbs (discard/revert) only in-browser; export terminal-only.
- **D4 Sandbox** — raw variant HTML stays sandboxed; only the trusted wrapper gets `allow-scripts`.
- **D5 Ergonomics-first** — the loop must reduce friction for the human; governance is a feature, not a tax.

## Definitional forks (must be resolved before Design — gate g05)

- **F1 Element addressing** for untagged elements: auto-mint stable handle | require `data-od-id` | hybrid draft→promote.
- **F2 Property extraction**: by spec (component descriptor/DNA) | by computed style (`getComputedStyle`) | by static HTML/CSS parse.
- **F3 Persistence**: local draft buffer flushed on run | immediate `POST /comment` | optimistic-local + server-sync.
- **F4 View-state**: in-page CSS expand/collapse | routed `/full/<label>` view.
- **F5 Honest-diff reconciliation**: add a "theme/global" change class | bind theme edits to a synthetic component | accept a documented "visual-only, diff-silent" class with a warning.

## Done criteria for the refine

A non-executed plan that (a) picks F1–F5 with rationale, (b) preserves D1–D5, (c) is buildable on node+fastify+no-build preview as an MVP slice, (d) keeps the existing test/e2e harness green, (e) names what is deferred.

## Residue / open assumptions for interrogation

- Is "hover" the right trigger, or does it fight text selection / scroll / touch? (ergonomics vs precision)
- Does "compose the page from elements" imply an element *registry/DNA*, or just better addressing? (scope creep risk)
- Can the honest diff stay honest if users edit theme tokens and untagged elements? (the central tension)
