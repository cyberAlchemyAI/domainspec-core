---
template_id: invoke.ux-plan
module: body-war-ontology-focus-scene-pivot
status: design-validator-pass
updatedAt: 2026-07-30
authority_effect: none
---

# UX Plan: Bounded Ontology Scene Navigation

## Selection Contract

`UX-PLAN` is required because a natural person reads, navigates, acts, and
recovers through a changed rendered semantic contract: focus changes from
visual dimming inside a 237-node graph to an exact bounded scene with semantic
portal controls and atomic state.

## User Goals

| Goal | Actor | Success signal |
| --- | --- | --- |
| Understand what is currently in view | ontology reader | named scene, exact node count, portal count, and non-color membership cues |
| Follow a boundary-crossing relation | ontology reader | exact directed portal activates by pointer, Enter, or Space and replaces the scene |
| Verify what the relation means and where it came from | ontology reader | persistent type, description, direction, endpoint paths/statuses, and `authority:none` |
| Recover prior context | ontology reader | Back restores the previous exact scene; tour exit restores suspended pre-tour state |
| Operate without animation or color | keyboard/assistive reader | identical semantic result with reduced motion and visible forced-colors-safe focus |

## Actors

| Actor | Needs | Constraints |
| --- | --- | --- |
| Cold ontology reader | small truthful scene, literal labels, explicit boundary crossings | no assumed ontology vocabulary or color interpretation |
| Keyboard reader | bounded focus path, semantic controls, visible focus, predictable restoration | no pointer-only relation rows |
| Screen-reader user | named landmarks, exact accessible names, selection and state announcements | graph position cannot carry sole meaning |
| Development validator | deterministic state/query hooks and exact receipts | structural proof is not comprehension proof |

## Journeys

| Journey | Start | Success | Failure/recovery | Correction/reversibility |
| --- | --- | --- | --- | --- |
| Search then focus | exact search result | bounded scene and named detail landmark | unavailable node keeps truthful prior view and explains error | return to overview or select another result |
| Tour a source group | overview or focused state | exact four-node step scene with labeled portals | invalid tour membership enters degraded state | exit tour restores prior state |
| Pivot through portal | focused scene | destination scene, selected relation, breadcrumb, detail focus | missing provenance blocks pivot | remain in source scene; choose another control |
| Inspect internal relation | focused scene | persistent exact tuple without scene replacement | missing tuple field disables selection and names data gap | clear selection |
| Backtrack | destination scene | exact prior state restored | empty history disables Back | stay in current scene |
| Change/exit tour | active tour | new step exclusively active; exit restores suspended state | stale selection is cleared, never mixed | move step again or exit |

## Surfaces

| Surface | Purpose | Entry | Exit |
| --- | --- | --- | --- |
| Scene header | name current scene and announce counts/authority | focus, tour, pivot | overview, Back, tour exit |
| Graph canvas | render only admitted scene nodes/internal relations | scene commit | select relation/node/portal |
| Portal list/controls | expose crossing relations independent of geometry | scene commit | activate portal |
| Detail landmark | expose node and selected relation literals | search, node selection, pivot | Back, next control |
| Breadcrumb | show reversible scene history | successful pivot | Back or reset |
| Tour panel | enter/change/exit exact source-declared tour scenes | tour start | tour exit |
| Status/announcement region | communicate scene replacement, counts, errors, restoration | state commit | next announcement |

## State Model

| State | User meaning | Allowed transitions | Error behavior |
| --- | --- | --- | --- |
| Overview | no bounded scene chosen | focus result, start tour | source error is explicit |
| Focused | one bounded scene owns graph and detail | select, pivot, Back, tour, overview | no silent full-graph fallback |
| Tour | one exact step owns active scene | change step, pivot, exit | out-of-scene selection cleared |
| Degraded | truthful projection cannot be formed | retry, overview | explains missing/ambiguous source without fabricated scene |

## Visible State And Evidence Meaning

| Visible state/evidence | Meaning | Allowed action | Uncertainty cue | Owner |
| --- | --- | --- | --- | --- |
| Scene name + counts | exact currently rendered projection | inspect or pivot | label `tour scene` or `one-hop scene`; no semantic-branch claim | scene owner |
| Portal label | exact admitted relation crosses current boundary | activate | type and description shown distinctly | tuple owner |
| Selected relation border/attribute | exact tuple is active | inspect, pivot, clear | source path and `authority:none` remain visible | state owner |
| Candidate status | literal admitted lifecycle posture | inspect only | absent status rendered as absent, not guessed | source-literal owner |
| Structural receipt | specified browser/state checks passed for exact bytes/runtime | compare or reproduce | explicit no-comprehension/no-release ceiling | validator |

## Interaction Flows

| Flow | Steps | Risk | Recovery |
| --- | --- | --- | --- |
| Focus a node | select result → commit scene → announce counts → focus detail | focus lands before state commit | coordinator moves focus only after committed scene |
| Activate portal | focus portal → activate → select tuple → push history → replace scene → focus destination | duplicate events or mixed scenes | event identity prevents duplicate breadcrumb; atomic reducer |
| Back | activate Back → restore stored scene/selection → focus restored control/landmark | target control no longer exists | focus scene landmark |
| Tour | start → suspend state → step scene → change resets active selection → exit restores | hidden stale inspector | active and suspended state rendered separately |

## Content Requirements

| Content | Surface | Claim bound | Constraint | Owner |
| --- | --- | --- | --- | --- |
| Scene kind and counts | header/announcement | structural projection only | never call scene an ontology branch | UX owner |
| Relation label | portal/detail | exact tuple | show generic type and relation-local description distinctly | tuple owner |
| Node kind/status/authority/path | search/card/detail/accessibility | admitted source literals | do not fabricate absent status | literal owner |
| Tour ordering | tour panel | presentation order | never imply workflow, causality, lifecycle, or promotion | tour owner |
| Evidence ceiling | receipt/status | exact validation scope | no human-comprehension, release, deployment, or production claim | validator |

## Accessibility Considerations

| Consideration | Applies to | Required response | Acceptance owner |
| --- | --- | --- | --- |
| Focus order and visible focus | skip route, scene, portal, detail, breadcrumb, tour | named landmark, fixed bounded Tab route, nonzero outline/border geometry | UX validator |
| Reflow and reading/operation order | narrow/zoomed viewport | header → graph/portal summary → detail → history remains coherent | UX owner |
| Contrast and non-color meaning | selection, kind, status, authority, portal | text plus icon/shape/border survives authored-color suppression; no contrast claim without measurement | UX validator |
| Accessible names and relationships | nodes, relations, portals, landmark | exact endpoints, displayed predicate, direction, status, authority, and relationship | source-literal owner |
| Keyboard and assistive operation | every pivot-capable control | pointer/Enter/Space parity, semantic controls, selected state | state owner |
| Reduced motion | pivot and tour transitions | same state replacement immediately; no rotation | UX validator |

## Responsive Semantics

| Condition | Information retained | Actions retained | Order retained | Recovery |
| --- | --- | --- | --- | --- |
| 1440px desktop | scene, portal, detail, history visible | all | scene then detail relationship | Back/overview |
| 390px narrow | same literals/counts/authority | all | DOM order independent of visual columns | detail landmark and breadcrumb remain reachable |
| 200% text zoom | no truncated critical literal or hidden control | all | accessible reading order | scroll, not clipped action |
| forced colors | text/icon/border meanings | all | unchanged | visible focus geometry |
| reduced motion | all semantic state | all | unchanged | immediate replacement |

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Four nodes remain confusing | structural success mistaken for comprehension | keep claim ceiling; schedule separate human study only after structural admission |
| Too many portals recreate overload | bounded scene still has high boundary fan-out | deterministic portal list, counts, stable ordering; measure before any semantic pruning |
| Layout rotation disorients | user loses location | semantic commit first, optional restrained orientation, immediate reduced-motion path |
| Search/card/detail vocabulary diverges | reader misreads kind/status | one `SourceLiteralSet` formatter across surfaces |
| Graph and portal list duplicate focus stops | keyboard burden | graph-level/roving strategy plus one explicit semantic portal control set; pin Tab bound |

## Acceptance Signals

| Signal | Polarity | Selector | Accountable owner | Validator |
| --- | --- | --- | --- | --- |
| exact named scene arrays | positive/negative | `AC-OFSP-001/002` | projection owner | independent fixture validator |
| literal portal and atomic destination | positive | `AC-OFSP-003` | state owner | deterministic + browser validator |
| pointer/keyboard/motion parity | positive | `AC-OFSP-004` | state owner | canonical-state validator |
| tour suspend/reset/restore | positive/negative | `AC-OFSP-005` | tour owner | reducer/browser validator |
| source-literal parity | positive/negative | `AC-OFSP-006` | literal owner | surface validator |
| visible focus and bounded route | positive/negative | `AC-OFSP-007` | UX owner | browser validator |

## Handoff Boundaries

- Architecture handoff: complete in `ARCHITECTURE.md`.
- Implementation-plan handoff: required through `WORK-PACK.md`.
- Research handoff: human comprehension remains separately deferred; no study
  is admitted by this plan.

## Gate Result

- target users: known
- workflow scope: known
- changed semantic surface: proved
- success/failure/recovery/reversibility: covered
- accessibility contract: covered
- planned evidence: not run
- status: `pass`

