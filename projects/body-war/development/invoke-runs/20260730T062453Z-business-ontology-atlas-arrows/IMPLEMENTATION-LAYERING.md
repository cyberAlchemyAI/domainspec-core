---
module: body-war-business-ontology-atlas-arrows
version: current
status: plan-ready
updatedAt: 2026-07-30
docType: implementation-layering
---

# Implementation Layering

## Purpose

Restore readable arrow representation and source-backed context to the
whole-ontology atlas without turning one page into an unreadable 231-edge
graph, hiding blockers, or changing ontology meaning.

## Target And Boundary

- Target: `projects/body-war/ontology/business/BUSINESS-VIEW-ATLAS.html`.
- Brownfield baseline: 237 nodes, 231 canonical relations, 122 internal
  relations, 109 cross-lens portals, 44 zero-degree nodes, and six lenses.
- Start layer: L0.
- Selected SWU: none.
- Implementation authority: not granted by this Plan.

## Layer Decisions

| Layer | Decision question | Smallest working result | Included | Deferred | Exit evidence |
| --- | --- | --- | --- | --- | --- |
| L0 | Can the existing 109 portals be deterministically summarized without losing direction or identity? | 13 ordered directed lens flows that retain all 109 exact relation IDs | pure projection, fail-closed coverage checks, unit tests | HTML, SVG, styling, screenshots | 13 groups, sum 109, no duplicates, all endpoints are known lenses |
| L1 | Can a reader see each exact relation and inspect concise source-backed context? | one accessible relation-arrow component plus separately receipted reference briefs | real HTML arrows; 237 node, 231 relation, six lens, and 23 predicate briefs; blocker/question/residue and incidence parity | overview map and browser claims | 231 exact arrows plus complete brief coverage with no invented definitions |
| L2 | Can a bounded whole-ontology overview show how the six lenses exchange responsibility? | six semantic lens nodes and 13 directed flow lanes, recomposed with the exact relation layer | overview map, responsive lane list, fixed known-lens layout, generated atlas | general graph layout, ontology editing, human study | 6 nodes, 13 lanes, lane counts sum to 109, exact layer remains 231 |
| L3 | Does the generated artifact remain usable across the supported static-browser modes? | new immutable browser receipt and arrow-specific screenshots | desktop, mobile, keyboard, no-JS, reduced-motion, 200% text, print checks | deployment, production, formal conformance, comprehension conclusion | validator pass, zero page errors, digest-bound receipt and screenshots |

## Stop Rules

1. L0 must not render presentation markup.
2. L1 exact arrows must not invent a second relation record or aggregate
   relation identity; reference briefs must not invent definitions, blockers,
   residue, or related incidence.
3. L2 must fail if the lens set changes; a general auto-layout is a separate
   design problem.
4. L3 must not treat browser evidence as human-comprehension evidence.
5. Any mismatch from 237/231/122/109/44 blocks generation rather than silently
   changing the visual story.

## Non-Regression Guardrails

- `nodes/`, `relations/relations.json`, lifecycle policies, authoring catalogs,
  `BUSINESS-VIEWS.html`, and `BUSINESS-JOURNEY-EXPERIMENT.html` remain
  read-only.
- Every relation sentence, link, source, predicate, target, type, effect, and
  portal identity remains real HTML.
- SVG carries only geometric presentation and is `aria-hidden="true"`.
- Solid/dotted effect semantics and portal classification stay orthogonal.
- Zero-degree nodes receive no fabricated arrows.
- Blocked status and recorded questions remain visible; a blocked item without
  a question says `No blocking question recorded`.
- Relation and predicate phrases are labelled `Projection wording`, never
  `Definition`.
- Reference briefs remain available through semantic HTML on hover, focus,
  touch/click, no-JS, and print paths.
- No new package root or Playwright dependency is allowed.
- Authority remains `none`; release admission remains `not-granted`.

## Recommended Next Layer

Select `SWU-BWAA-001` explicitly, then run one Task Session preflight. Do not
start either L1 unit until the L0 closeout receipt proves exact 13/109
aggregation. Complete 002 before 005; complete both before L2.
