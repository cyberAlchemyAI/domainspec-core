---
template_id: invoke.ux-plan
target: body-war-business-ontology-atlas-arrows
status: design-validator-pass
updated_at: 2026-07-30
---

# UX Plan — Body War Ontology Atlas Arrows

## Selection contract

`ux-plan` is required because a natural-person ontology reader navigates two
changed rendered semantic surfaces: the whole-ontology direction summary and
the exact relation-arrow presentation.

## User goals

| Goal | Actor | Success signal |
| --- | --- | --- |
| See which lens points to which other lens. | ontology reader | source and target are visually explicit before opening details |
| Read a relation as a sentence. | ontology reader | source → phrase → target plus predicate/effect text |
| Follow an arrow without losing canonical direction. | keyboard/assistive reader | ordinary endpoint links preserve source/target order |
| Understand what an aggregate arrow means. | ontology reviewer | count and “navigation summary, not ontology relation” boundary are visible |
| Understand a referenced item without losing place. | ontology reader | a concise source-backed brief is available by hover, focus, touch/click, no-JS, and print |
| Keep unresolved meaning visible. | ontology reviewer | blocked status, recorded questions, residue, and explicit missing-data statements remain present |

## Journeys

| Journey | Start | Success | Failure and recovery | Reversibility |
| --- | --- | --- | --- | --- |
| Read whole-ontology flow | atlas overview | 13 bounded arrows summarize 109 portals | semantic lane list remains when graph is compressed or unavailable | return to existing lens cards |
| Descend to exact relation | overview or lens | canonical relation arrow and metadata appear together | ordinary links open source, target, or relation anchor | browser Back and “All lenses” |
| Read on mobile | 390-pixel viewport | source appears above target with visible downward arrow | text wraps and the full graph yields to lane rows | same anchors and document order |
| Read without JavaScript | initial HTML | all arrow content and destinations exist | no filtering/focus enhancement, but ordinary navigation works | reload with JS |
| Print for review | print media | all lenses and relation arrows are visible | relation diagrams avoid internal page breaks where possible | return to screen view |
| Inspect a referenced concept | any arrow, node, lens, or predicate reference | source-backed brief exposes the available definition/wording, status, and related incidence | activate the native disclosure or follow exact anchors when hover is unavailable | close the disclosure or return to the prior anchor |

## Surfaces

| Surface | Purpose | Entry | Exit |
| --- | --- | --- | --- |
| overview lens map | show direction among six editorial lenses | atlas overview | destination lens or semantic lane |
| semantic lens lanes | accessible/responsive equivalent of the overview map | overview | source or target lens |
| relation arrow card | show one exact directed relation | lens internal/outgoing section or anchor | source, target, metadata, portal action |
| exact metadata disclosure | audit tuple and authority boundaries | relation arrow card | same card |
| source-backed reference brief | inspect concise context without changing location | node, relation, lens, or predicate reference | persistent disclosure or exact canonical anchor |

## Visible meaning

| Visible evidence | Meaning | May support | Must not imply |
| --- | --- | --- | --- |
| solid arrow + explicit label | ordinary admitted candidate relation meaning | read source-to-target direction | implementation or runtime proof |
| dotted arrow + effect text | blocked, projection-only, or explicit non-promotion meaning | distinguish constrained meaning | missing relation |
| cross-lens badge | endpoints live in different editorial lenses | portal navigation | blocked or weaker meaning |
| `55 cross-lens relations` | count of canonical Behavior → Business-object portals | descend into exact rows | one new aggregated ontology relation |
| zero-degree cue without arrow | no current admitted endpoint incidence | review isolated node | meaningless or forever unrelated |
| `Definition` inside a node brief | canonical node definition from the admitted source | understand the node | relation or predicate authority |
| `Projection wording` inside a relation/predicate brief | phrase used to read the projected relationship | understand the displayed sentence | a canonical definition |
| `No blocking question recorded` | a blocked item has no question in its source data | notice unresolved source completeness | that no blocker exists |
| incoming/outgoing links and counts | exact admitted relation incidence | navigate related concepts | inferred or generated relations |

## Interaction and information order

1. Heading and boundary.
2. Six existing lens cards.
3. Desktop overview graph.
4. Thirteen semantic arrow lanes.
5. Selected lens heading and node groups.
6. Exact internal relation arrows.
7. Exact outgoing portal arrows.
8. Incoming portal references.
9. Reference briefs adjacent to their referenced labels and sentences.
10. Boundary footer.

The order is explanatory, not causal or temporal.

## Responsive semantics

| Condition | Retained information | Retained action | Relationship rule |
| --- | --- | --- | --- |
| desktop | six-node map, 13 paths, semantic lanes, 231 arrows | lens, relation, source, target, portal navigation | arrows point canonical source to target |
| 390-pixel mobile | semantic lanes and vertical relation arrows | same ordinary links | source remains before target in DOM |
| 200% text | wrapping labels, phrases, predicates, counts | same links and disclosures | no clipping or document-level horizontal scroll |
| no JavaScript | all diagrams, labels, metadata, and anchors | ordinary fragments | controller is enhancement only |
| reduced motion | all static content | same navigation | no arrow animation |
| print | all lenses, lanes, and relation arrows | n/a | line style and text retain meaning in monochrome |

## Reference-brief interaction

One semantic disclosure owns the content for every input mode:

1. The compact trigger names the referenced node, relation, lens, or
   predicate.
2. Pointer hover or focus-within reveals the brief as a preview.
3. Activating the native disclosure keeps the same brief open for keyboard and
   touch/click users.
4. The content exists in document order when JavaScript is unavailable.
5. Print exposes the content without requiring interaction.

The brief body presents the shortest source-backed path first:

- node: definition, kind/role, status, owner/resolution gate, blocking
  questions, residue, then outgoing/incoming related links and exact metadata;
- relation: source → projection wording → target, then predicate, direction,
  authority/value effects, relation ID, and forbidden-collapse text;
- lens: title, question, description, counts, then flow summary;
- predicate: token, projection wording, exact usage count, then examples.

If a blocked node has no recorded question, the brief says
`No blocking question recorded`. Empty residue is omitted or explicitly named.
A zero-incidence node says `No admitted explicit relation`. The interface
never fabricates relation or predicate definitions.

## Accessibility considerations

| Consideration | Required response | Acceptance owner |
| --- | --- | --- |
| accessible names and relationships | HTML sentence names source, phrase, target, predicate, effect, and ID | product ontology owner |
| SVG duplication | relation shaft SVG is `aria-hidden`; overview graph has a semantic lane equivalent | renderer validator |
| focus order | source link precedes target link; existing focus styles remain | browser validator |
| contrast and non-color | solid/dotted effects and portal status have explicit text | renderer validator |
| reflow | desktop horizontal arrows become mobile vertical arrows without changing DOM order | browser validator |
| keyboard | all endpoints, lenses, relations, and disclosures remain ordinary controls | browser validator |
| input parity | hover, focus, touch/click, no-JS, and print expose the same source-backed brief | browser validator |
| blocker retention | blocked effects, node status, recorded questions, and residue are never hidden by brief truncation | renderer validator |

These are planned accessibility behaviors. Passing them does not establish
formal accessibility conformance.

## Content requirements

| Content | Required wording/constraint |
| --- | --- |
| overview boundary | “Navigation summary; each arrow groups canonical portal relations and is not an ontology relation.” |
| lane label | source lens, arrow, target lens, exact relation count |
| relation reading | source label, plain-language phrase, target label |
| typed meaning | predicate and explicit authority-effect phrase |
| portal meaning | separate source-lens → target-lens badge |
| claim ceiling | candidate projection only; no comprehension, promotion, release, deployment, or production claim |
| reference brief | semantic HTML; node content labeled `Definition`, relation/predicate content labeled `Projection wording` |
| missing blocker question | exactly `No blocking question recorded` |
| zero incidence | exactly `No admitted explicit relation` |

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| arrows dominate metadata | reader mistakes visual prominence for authority | exact metadata remains adjacent; boundary is repeated |
| reciprocal arrows overlap | direction becomes ambiguous | separate curved paths and semantic lanes |
| mobile arrow loses direction | source/target reversal | DOM order fixed; vertical arrow tested |
| dense page becomes slow to scan | reader fatigue | overview first, lens filtering retained, exact arrows grouped by current sections |
| hover obscures content or excludes non-pointer users | context is unavailable or disruptive | one native disclosure supports preview, persistent activation, no-JS, and print |
| projection phrase is mistaken for definition | presentation gains false authority | use exact `Projection wording` label and preserve exact metadata |

## Acceptance signals

| Signal | Polarity | Exact selector/evidence | Owner |
| --- | --- | --- | --- |
| 13 aggregate arrows total 109 | positive | overview DOM and pure grouping test | projection validator |
| reciprocal pairs remain distinct | positive | lens-flow fixture | projection validator |
| 231 relation arrows | positive | `[data-arrow-presentation="relation"]` count | renderer validator |
| no arrow on 44 isolates | negative | zero-degree DOM fixture | renderer validator |
| source precedes target at mobile | positive | pinned mobile browser assertion | browser validator |
| no horizontal document overflow | negative | scroll-width assertion at 390 and 200% text | browser validator |
| no-JS and print retain arrows | positive | pinned media-mode assertions/screenshots | browser validator |
| all source-backed briefs exist | positive | 237 node, 231 relation, six lens, and 23 predicate brief counts | renderer validator |
| blockers and missing questions remain visible | positive | blocked fixtures plus `No blocking question recorded` assertions | renderer validator |
| input modes expose the same brief | positive | hover, keyboard focus, touch/click, no-JS, and print browser assertions | browser validator |

## Gate result

- Status: `pass`
- Architecture handoff: complete in `ARCHITECTURE.md`
- Implementation-plan handoff: allowed after Design fixed-point validation
- Research handoff: deferred; human comprehension requires a separate route
