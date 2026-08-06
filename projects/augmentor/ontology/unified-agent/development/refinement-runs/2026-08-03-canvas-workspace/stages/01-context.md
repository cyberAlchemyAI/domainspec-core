# Stage 01 — Strict Context Pack

- Capability: `context-builder`
- Mode: `standard-strict`
- Status: `pass`
- Target: the generated Augmentor unified-agent ontology visualization
- Authority ceiling: session evidence for a candidate-local design; no source,
  ontology, runtime, promotion, or product authority

## Objective

Prepare the smallest evidence set needed to design a readable, canvas-first
workspace in which supporting information can be minimized without changing the
graph's semantic state.

## Evidence obligations

| ID | Obligation | Covered by |
| --- | --- | --- |
| O1 | Explain the observed node-card legibility failure and bind card geometry to the current renderer. | E1, E2 |
| O2 | Show why the current page is a vertical document around a graph card and define the canvas-first delta. | E1, E3 |
| O3 | Preserve selection, filter, view, sequence, and explanation state while support panels minimize. | E1, E4 |
| O4 | Specify desktop, mobile, keyboard, reduced-motion, and focus-return behavior. | E5, E6, E7 |
| O5 | Preserve candidate-local and `authority_effect:none` boundaries. | E8, E9 |
| O6 | Produce a non-executed plan with exact generation and browser validation anchors. | E3, E5, E6, E10 |

## Selected evidence

| ID | Artifact and selector | Why selected | Ceiling |
| --- | --- | --- | --- |
| E1 | `visualization/template.html`: `.workspace`, `.graph-card`, `.node-*`, `drawNodes`, and `state` | Direct implementation evidence for the current 156×66 cards, single-line truncation, document shell, and semantic state. | Current template bytes only |
| E2 | operator screenshot recorded in `REFINE-SEED-PROPOSAL.md#evidence-baseline` | Shows label overlap and poor card readability at the user's actual viewport. | Visual observation, not a usability study |
| E3 | `scripts/build-visualization.mjs`: template/data assembly and generated-output write | Proves the template is canonical and the root HTML is generated. | Build topology only |
| E4 | `tests/visualization.browser.mjs`: selection, Escape, filters, text view, 320px, reduced motion | Binds current interaction behavior that the new shell must preserve or intentionally revise. | Existing test intent, not future acceptance |
| E5 | `tests/ux-evidence.browser.mjs`: 320px measurements, focus, requests, screenshots, source-card output | Existing browser-evidence harness to extend for workspace behavior. | Browser-observable claims only |
| E6 | `output/playwright/ux-validator/2026-08-03-augmentor-ontology-language/findings.json` | Prior 8/8 hard-gate pass plus the technical-graph and internal-scroll soft flags. | Prior target hash only |
| E7 | `output/playwright/ux-validator/2026-08-03-augmentor-ontology-language/measurements/layout.json` | Baseline: 1440×1000 document height 3072 and 320×800 document height 7776 without page overflow. | Prior run, not the proposed design |
| E8 | `profile.json`: visualization contract | Owns the candidate-local interpretive-read-model and `authority_effect:none` ceiling. | Package description only |
| E9 | `explanations/beginner.json`: lanes and nodes | Supplies friendly names, six explanation lenses, and boundary language without replacing canonical labels. | Explanatory projection only |
| E10 | `tests/visualization.test.mjs`: generation currency, exact totals, explanation coverage, primary surfaces | Defines deterministic non-browser checks and source/generated synchronization. | Existing test coverage only |

## Excluded context

- Ontology node/relation edits: the requested problem is presentation and UI
  state, not meaning or graph membership.
- External design research: the prior evidence bundle already contains cited
  accessibility/plain-language sources and the unresolved gap is local layout.
- Audit and receipt-system expansion: explicitly deprioritized by the operator.
- Runtime routing, memory mutation, and reasoning execution: represented by the
  ontology but not implemented by this visualization.

## Strict coverage result

All six obligations have at least one direct source and an explicit authority
ceiling. No obligation depends on an unverified external claim. The pack is
`PASS` for Define and Design authoring; it does not authorize implementation.

## Handoff frame

Define must keep two namespaces separate:

- semantic exploration state: view, query, posture, selection, sequence, and
  explanation lens;
- ephemeral presentation state: dock/tray visibility, active mobile sheet,
  focus mode, and focus-return target.

