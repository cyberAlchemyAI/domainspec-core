# Strict Refresh Context Pack

Task: refresh the Body War atlas-arrow definition, design, and Plan with
source-backed reference briefs visible on hover and keyboard focus.

Mode: standard, strict  
Activation: direct user  
Mutation mode: apply-approved  
Evidence date: 2026-07-30

## Obligations

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| O-01 | expose a brief explanation for concepts with definitions | `node.schema.json` requires `definition`; current 237/237 nodes are nonempty | covered |
| O-02 | expose related meaning without inventing ontology data | renderer already derives incident relation IDs; relation schema preserves exact tuple/effects | covered |
| O-03 | work on hover, keyboard focus, touch/click, no-JS, and print | current UX/renderer use real HTML and native disclosures | covered |
| O-04 | keep blocker and residue meaning visible | 29 blocked nodes; 21 nodes carry blocking questions; status/owner/gate/residue fields exist | covered |
| O-05 | preserve all work-pack blockers and ceilings | `WORK-PACK.md#Blocker-And-Gap-Ledger`, semantic locks, continuation, execution control | covered |
| O-06 | avoid stale Design evidence after spec/design changes | Design manifest, witnesses, denominator, and selection receipts are in apply scope | covered |
| O-07 | keep the work atomic | helper and parent review identify a separate reference-brief SWU between 002 and 003 | covered |
| O-08 | preserve implementation boundary | Invoke Refresh changes authored artifacts only; atlas implementation remains untouched | covered |

Coverage: 8/8 obligations. Strict coverage: pass.

## Selected Evidence

| Path | Selector | Obligations | Why selected |
| --- | --- | --- | --- |
| `SPEC.md` | projection/interface/acceptance contracts | O-01–O-03, O-06 | definition baseline to refresh |
| `ARCHITECTURE.md` | component and interface views | O-01–O-04, O-06 | design data hierarchy and missing-field policy |
| `UX-PLAN.md` | interaction, content, accessibility | O-01–O-04 | hover/focus/touch behavior |
| `WORK-PACK.md` | SWU manifest, blockers, locks | O-05–O-07 | executable Plan authority |
| `CONTINUATION.json` | selection and ceiling state | O-05 | must remain unselected/non-authorizing |
| `schemas/node.schema.json` | required node fields | O-01, O-04 | canonical node data contract |
| `schemas/relation.schema.json` | exact relation fields | O-02, O-04 | proves no relation-definition field exists |
| `authoring/view-atlas-catalog.mjs` | lens question/description/boundary | O-02–O-04 | source-backed lens brief |
| `authoring/view-catalog.mjs` | predicate phrases/overrides | O-02 | projection wording contract |
| `scripts/render-view-atlas.mjs` | node/relation rendering and incidence | O-01–O-04 | implementation seam |
| `PLANNED-WITNESSES.json` | planned acceptance family | O-06 | needs a new reference-brief witness |
| `.arcanum/inventory/index.json` | current lookup readiness | O-05 | inventory lookup is ready |
| inventory business-view synthesis | browser/authority boundary | O-03, O-05 | prevents comprehension claim inflation |
| helper receipt | source-field and blocker audit | O-01–O-07 | independent read-only check |

Files selected: 14. Noise ratio: low.

## Excluded

- ontology node and relation authoring: read-only source data, not a refresh
  target;
- generated atlas and renderer: implementation belongs to Task Session;
- application and SuggestedTrack runtime: outside this presentation refresh;
- broad architecture sources: no uncovered obligation requires them.

## Current External Drift

The generated `.agents/skills` mirror lost 539 tracked entries during this
turn, including Invoke and Context Builder. Canonical Arcanum sources remain
available and were used. The refresh does not repair that unrelated state; it
records a target-lifecycle preflight blocker.
