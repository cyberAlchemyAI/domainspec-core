---
template_id: invoke.ux-plan
module: body-war-business-ontology-view-atlas
status: design-validator-pass
updatedAt: 2026-07-30
authority_effect: none
---

# UX Plan: Whole-Ontology Editorial Lens Atlas

## User goals

| Goal | Success signal |
| --- | --- |
| Start with a manageable map | six plain-language lens summaries explain their question, included kinds, and counts |
| Inspect actors and boundaries first | “Participants and boundaries” groups actors, external systems, and interfaces without creating an actors-only authority package |
| Understand one literal kind | each kind has its own heading and complete node list inside its assigned lens |
| Follow a relation into another view | exact directed sentence names the destination lens; the portal focuses its exact endpoint |
| Understand an unconnected node | “No admitted explicit relation” appears with a bounded explanation and no fabricated edge |
| Verify meaning and source | node and relation details expose exact IDs, kinds, status, authority, owner, paths, predicate, direction, and description |
| Recover prior position | URL fragment, Back, overview link, and visible lens navigation remain coherent |

## Reader model

The default reader may understand Body War but not ontology terminology.
Therefore each lens starts with a question and plain-language description.
Literal kinds and technical tuples remain one disclosure away; they are never
hidden or rewritten.

## Information architecture

```text
skip link
header: title + candidate/projection ceiling
overview:
  six lens cards
  search
main:
  lens
    question + boundary note + counts
    kind group(s)
      core node list
        node summary
        exact metadata details
        incident relation links
    internal relation section
    outgoing portals
    incoming portals
footer:
  how to read arrows
  zero-degree meaning
  authority/research ceiling
```

## Lens wording

| Lens | Reader question | Boundary phrase |
| --- | --- | --- |
| Participants and boundaries | Who participates, and through which external or interface boundary? | Groups actors, external systems, and interfaces for navigation only. |
| Responsibilities | Which contexts group which capabilities? | Shows responsibility vocabulary; it does not declare runtime modules. |
| Behavior | What can happen, be requested, be answered, or be observed? | Keeps workflow, operation, query, and event kinds literal. |
| Business objects | What information, records, values, and measures are carried? | Groups entity/value/ledger/metric vocabulary without changing ownership. |
| Governance and lifecycle | What constrains behavior and names lifecycle postures? | Policy and lifecycle membership remain distinct from relation incidence. |
| Hypotheses and outcomes | What is believed or sought? | Premise source defects remain explicitly unresolved. |

## Journeys

| Journey | Start | Success | Recovery |
| --- | --- | --- | --- |
| Whole map to actors | overview | participants lens opens at actor group | ordinary overview link |
| Actor to business object | actor node | exact outgoing portal opens target lens/node and retains direction | browser Back or source endpoint link |
| Search exact concept | search | result opens canonical core node location | clear search to restore overview |
| Inspect an isolate | lens or search | bounded zero-degree cue and research disposition render separately | return to kind heading |
| Review a relation | node or lens relation list | exact tuple and both endpoints are inspectable | close native details or follow endpoint |
| No JavaScript | page load with JS disabled | all six lenses, nodes, relation sentences, links, and boundary text remain usable | ordinary browser navigation |

## Interaction contract

- Use native anchors for overview, lens, node, relation, and portal targets.
- Use native `<details>/<summary>` for metadata.
- JavaScript may add search filtering, controlled lens disclosure, focus
  transfer, announcements, and history replacement/push.
- Enter activates links by native behavior; no custom Space contract is added
  to anchors.
- Focus moves only after the destination exists and is revealed.
- Search result ordering is stable by label then concept ID.
- Target-side portal links never rewrite the displayed relation direction.

## Content and evidence meaning

| Visible element | Meaning | Forbidden implication |
| --- | --- | --- |
| editorial lens | removable navigation grouping | semantic ontology branch or new kind |
| kind badge | exact source `business_kind` | module, role, or lifecycle inference |
| relation sentence | exact admitted source, predicate phrase, target | causality, sequence, or reverse edge unless explicitly admitted |
| inbound/outbound portal label | relation's original orientation relative to the current lens | copied or reversed relation |
| zero-degree cue | absent from current explicit relation endpoints | meaningless, invalid, or unrelated in every sense |
| research disposition | accepted review classification for the 44 isolates | profile policy or ontology admission |
| candidate status and authority | exact source posture | release or promotion |
| structural receipt | exact assertions passed for bound bytes/runtime | comprehension, accessibility conformance, or production readiness |

## Accessibility and responsive contract

| Condition | Required behavior |
| --- | --- |
| keyboard | skip link, lens nav, search, summaries, nodes, relations, and portal anchors have visible focus |
| screen reader | one `h1`, ordered headings, labeled navigation/search, live status, and exact descriptive anchor names |
| no color | kinds, direction, status, authority, and disposition have text labels |
| reduced motion | no scrolling animation or transition required for state/focus |
| 390px viewport | one-column reading order; no horizontal document overflow |
| 200% text | content reflows and controls remain visible |
| print | all lenses are expanded/visible; controls that only filter are omitted |
| no JavaScript | complete content and ordinary navigation remain |

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Six editorial names are mistaken for ontology branches | repeat “navigation lens” and list exact literal kinds |
| Dense 237-node page remains overwhelming | closed overview, kind subheadings, search, stable anchors, progressive disclosure |
| Portal duplication confuses relation counts | render one canonical relation; inbound/outbound indexes reference it |
| Isolate disposition is mistaken for policy | label “research disposition” and show the unadopted-policy boundary |
| Ten premise defects look repaired | show source-defect disposition and explicit unresolved cue |
| Graph layout is expected | explain that the atlas is a complete indexed reading view; current graph/journey views remain linked |

## Acceptance signals

- six lens cards and 17 kind headings exist;
- every source node has one canonical DOM target;
- every relation has one canonical DOM target;
- 109 portals have valid source and target lens/node links;
- all 44 zero-degree cues exist;
- exact boundary text exists in overview, lens content, and footer;
- no-JS, keyboard, focus, narrow, reduced-motion, and print checks pass;
- all structural claims remain within the Design selection ceiling.

## Gate result

Target users, tasks, information architecture, content meanings, error
recovery, accessibility structure, responsive behavior, and evidence ceilings
are explicit. Human comprehension remains a separately authorized study.
Result: `pass`.

