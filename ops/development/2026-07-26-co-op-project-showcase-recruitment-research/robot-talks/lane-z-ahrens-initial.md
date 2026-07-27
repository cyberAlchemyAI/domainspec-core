# Initial Robot-Talk Report — Ahrens, Sönke

Dispatch: `2026-07-26-co-op-project-showcase-recruitment-research`  
Lane: `lane_z_explorers`  
Position type: **Initial; pre-discussion; not a synthesis verdict**

Local mandate: the artifact must explain fourteen projects, expose proof and limits, and provide contribution paths while sharing one factual source across self-guided browsing and live projection ([dispatch context](</home/vrondelli/projects/domainspec-core/ops/development/2026-07-26-co-op-project-showcase-recruitment-research/dispatch-sheet.json:6>)). This investigation is explicitly required to keep portfolio-first provisional and compare cards, detail routes, accordions, dialogs, filters, scrollytelling, and presentation variants ([agent record](</home/vrondelli/projects/domainspec-core/ops/development/2026-07-26-co-op-project-showcase-recruitment-research/dispatch-sheet.json:19>), [initial prompt](</home/vrondelli/projects/domainspec-core/ops/development/2026-07-26-co-op-project-showcase-recruitment-research/dispatch-sheet.json:24>)).

## Initial Position

**Inference:** Use a hybrid decision-first index leading to durable project detail routes—not a uniform fourteen-card portfolio and not a slide deck embedded in a webpage.

The opening should first let a visitor recognize a problem, domain act, or contribution appetite. A compact project collection can then support comparison. Each project needs its own URL because evidence, limitations, contribution paths, sharing, browser Back, and later return are durable information needs. Presentation mode may alter density, sequence, and controls, but should project the same content records.

Portfolio-first remains useful after initial orientation. It is not yet justified as the universal front door.

## Key Findings

### 1. Cards are a comparison aid, not an information architecture by themselves

**Fact:** The UK Department for Education design system says cards can make content harder to understand when overused and recommends testing structured headings, paragraphs, and grid content first. Its cards expose a heading, short description, and optional metadata; a linked card represents a single destination. [DfE Card guidance](https://design.education.gov.uk/design-system/components/card)

**Inference:** Fourteen visually equal cards risk “card sameness”: they communicate equal weight and comparable shape even when projects differ in maturity, domain, proof, and desired contribution.

**Proposal:** Cards should be generated projections of richer project records and used only where the user is genuinely comparing projects. The opening should remain meaningful as headings and prose if card styling disappears.

### 2. Search/filter collections work when visitors already possess discriminating criteria

**Fact:** NASA’s Missions collection combines search, status filters, mission-type filters, and project summaries; JPL’s current missions collection similarly offers search, filtering, sorting, result counts, compact descriptions, and separate mission destinations. [NASA Missions](https://www.nasa.gov/missions/), [NASA JPL Missions](https://www.jpl.nasa.gov/missions/)

**Inference:** Filterable collections are strong for “show me active rover missions,” but weak for a newcomer who does not yet know whether “ontology,” “writing,” or “IDE ergonomics” names the problem they care about. Fourteen items also do not justify a heavy faceted-search shell unless the facets answer real visitor decisions.

**Proposal:** Prefer a small set of plain-language entry lenses—such as “make meaning explicit,” “create with AI,” or “improve the building environment”—over taxonomy-heavy filters. Preserve an unfiltered “all projects” route.

### 3. Accordions fit bounded supplementary sections; dialogs are poor containers for project stories

**Fact:** W3C describes accordions as headings that reveal associated sections and requires operable header buttons, state communication, and keyboard behavior. It also warns against landmark proliferation when more than roughly six panels can be open. [WAI Accordion Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/accordion/)

**Fact:** A modal dialog makes the underlying page inert, contains the tab sequence, requires focus placement and restoration, and closes with Escape. W3C notes that long, structured dialog content requires special focus handling. [WAI Modal Dialog Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)

**Inference:** A fourteen-project accordion creates a long control stack and hides comparison evidence. A project-detail modal adds focus and scrolling debt, weakens deep linking, and interrupts non-linear exploration.

**Proposal:** Reserve accordions for secondary material inside a detail route—methods, chronology, or extra evidence. Reserve dialogs for short, reversible tasks. Project stories should be pages or route-addressable views.

### 4. Browser-native presentation can share truth without forcing the website to impersonate slides

**Fact:** reveal.js supports an overview mode for non-linear navigation and a separate speaker view with presenter notes. [reveal.js Overview Mode](https://revealjs.com/overview/), [reveal.js Speaker View](https://revealjs.com/speaker-view/)

**Fact:** Browser history exists to preserve expected Back/Forward movement. MDN specifically explains that dynamically replaced SPA content breaks that expectation unless history entries and state restoration are implemented. URL fragments also provide direct links to document sections. [MDN History API](https://developer.mozilla.org/en-US/docs/Web/API/History_API/Working_with_the_History_API), [MDN URL fragments](https://developer.mozilla.org/en-US/docs/Web/URI/Reference/Fragment/Text_fragments)

**Inference:** “Same artifact” should mean shared project facts and durable destinations, not identical screen density. A presentation layer may offer overview, next/previous, presenter cues, and projection-sized text while retaining the same project IDs and canonical content fields.

**Proposal:** Make project and evidence states URL-addressable. Treat presentation mode as a view over those records, with a visible escape to normal browsing and no presenter-only factual claims.

### 5. Museum precedent supports visitor-chosen depth and multiple access modes

**Fact:** Cooper Hewitt’s Pen let visitors collect objects from labels, later explore related objects and contextual material on large tables, and retrieve their collection beyond the immediate encounter. [Cooper Hewitt, “Designing the Pen”](https://www.cooperhewitt.org/new-experience/designing-pen/)

**Fact:** Smithsonian visitor guidance provides complementary large-print, captioned, audio-described, mobile, and human-assisted modes instead of assuming one interface form serves every visitor. [Smithsonian Accessibility for Visitors](https://www.si.edu/visit/accessibility)

**Inference:** A showcase can offer a memorable encounter, overview, and retained deep route without forcing every visitor through the same sequence. The transferable lesson is continuity of identity and access across modes—not Cooper Hewitt’s particular visual or hardware design.

**Proposal:** Give every project a stable identity and “save/share/return” destination; let live presentation point into those same destinations.

## Precedent Matrix

| Pattern / precedent | 10-second decision | 30-second decision | 2-minute decision | Deep-link / Back | Mobile / keyboard | Projection | Main failure |
|---|---|---|---|---|---|---|---|
| Structured headings before cards — DfE | “Is this collection relevant?” | Scan meaningful distinctions | Compare summaries without opening all items | Native links behave predictably | Strong when semantic HTML survives layout | Readable if density is constrained | Styling fourteen items into false sameness |
| Filterable collection — NASA/JPL | “Can I narrow this?” | Select known status/type | Inspect a result and open its detail | Strong with separate result URLs; filter state must be preserved | Filter controls can become long on mobile | Weak unless a presenter controls the subset | Taxonomy assumes prior knowledge |
| Accordion index — WAI pattern | See section names | Open one or two sections | Read bounded supplementary content | Often weak unless expansion state is encoded | Defined keyboard behavior, but fourteen headers add tab/scroll debt | Poor when collapsed content matters | Hidden comparison and repeated toggling |
| Modal project detail — WAI pattern | Quick preview | Focus on one item | Long content becomes awkward | Commonly weak; Back/refresh/share need extra engineering | Focus trap and small viewport raise complexity | Poor: background context disappears | Click debt and inaccessible long-form overlays |
| Durable detail route + history | Recognize destination | Inspect compact opening | Verify evidence, limits, and contribution path | Strongest option for share, return, Back, and direct citation | Native document navigation is robust | Good when presentation opens exact sections | Can feel slow if every small fact requires a new page |
| Browser presentation variant — reveal.js | Grasp current topic | Follow a curated sequence | Jump via overview or revisit a project | Possible if project IDs map to URLs | Requires explicit keyboard/mobile validation | Strong; overview and speaker separation are native concepts | “Slide-deck cosplay”: sparse pages, presenter dependence |
| Museum collect-and-revisit — Cooper Hewitt | Notice an object/project | Choose what to retain | Explore related context later | Stable identities enable continuity | Multiple access modes are necessary | Strong encounter; later browsing differs in density | Novel interaction overshadows content |
| Scrollytelling | Follow one causal story | Understand a staged reveal | Absorb a selected narrative | Deep links and reverse navigation are often secondary | Motion and scroll coupling need care | Presenter can lose pacing/control | Imposes one sequence on a non-linear portfolio |

## Recommended Progressive-Disclosure Grammar

This is a **proposal**, not final copy or an admitted content schema.

1. **Orientation — approximately 10 seconds**
   - One concrete, memorable domain tension.
   - Three to five visitor-recognizable entry lenses.
   - A direct “all fourteen projects” route.
   - No internal framework vocabulary unless the concrete act has already earned it.

2. **Collection — approximately 30 seconds**
   - Each project projection contains:
     - project name,
     - one concrete act or problem,
     - current state/proof marker,
     - one explicit “needs” or contribution signal,
     - one durable detail link.
   - Allow comparison by a few decision-bearing lenses.
   - Do not force all projects into identical prose length or visual weight.

3. **Compact project opening — first screen of detail**
   - What someone can understand or do here.
   - Who it is for.
   - What exists now.
   - What is explicitly not yet proven.
   - The current contribution path.

4. **Deep project story — approximately 2 minutes and beyond**
   - Problem and domain scene.
   - Current artifact or mechanism.
   - Evidence with evidence type.
   - Limits and unresolved questions.
   - Concrete contribution task, prerequisites, owner/contact route.
   - Related projects as optional onward paths.

5. **Presentation view**
   - Uses the same project ID and content fields.
   - Enlarges one compact opening at a time.
   - May sequence or suppress detail, but must not invent facts.
   - Offers overview/jump controls and a visible normal-page link.
   - Produces a shareable project URL for post-meeting continuation.

Implementation consequences include native headings and links first; accordions only within detail; no long-form project dialogs; URL-addressable collection selection and project state; preserved browser Back/Forward; and motion treated as optional. View transitions are not universally available and must degrade cleanly; full-screen motion should respect reduced-motion preferences. [web.dev View Transitions](https://web.dev/learn/css/view-transitions-spas)

## Counterexample Breaking Portfolio-First

A musician arrives with a narrow desire: “I want an AI tool that helps me hear and reshape harmonic relationships, and I can contribute domain examples but not framework code.”

A project-name-first grid of fourteen cards makes this visitor translate their desire into unfamiliar project identities before they can decide where to act. A problem/contribution-first opening can route them directly to the relevant one or two projects, then expose the wider portfolio as context.

Therefore, portfolio-first fails when:

- project names are not meaningful to outsiders;
- the visitor has a concrete job but lacks internal taxonomy;
- only a small subset accepts the visitor’s type of contribution;
- project maturity or availability differs materially.

This supports a hybrid: decision-first entrance, portfolio overview as the stable comparison layer.

## Gaps or Inconsistencies

- No cited precedent establishes that project-first, problem-first, contribution-first, or hybrid entry performs best for this specific audience.
- The local Inventory explicitly records `no_inventory_match`, not a clean precedent result ([STRATEGY.md lines 140–146](</home/vrondelli/projects/domainspec-core/ops/development/2026-07-26-co-op-project-showcase-recruitment-research/STRATEGY.md:140>)).
- The fourteen projects lack an owner-admitted shared public schema and have unresolved names, roots, or statuses ([STRATEGY.md lines 147–148](</home/vrondelli/projects/domainspec-core/ops/development/2026-07-26-co-op-project-showcase-recruitment-research/STRATEGY.md:147>)).
- External precedents demonstrate mechanics, not comprehension or recruitment outcomes.
- reveal.js demonstrates browser-presentation capabilities, not that a slide grammar is appropriate for this artifact.
- Museum precedents preserve encounter-to-detail continuity, but their physical setting and repeat-visit behavior differ from a weekly technical showcase.
- No current human evidence shows whether outsiders can retell project distinctions after 10 seconds, 30 seconds, or two minutes.

## Local Tensions

- **One factual substrate vs two interaction densities:** self-guided readers need durable depth; projected audiences need aggressive density reduction.
- **Project voice vs comparable scanning:** preserving distinct voices can weaken cross-project comparison; enforcing identical cards can erase meaningful differences.
- **Memorable opening vs immediate choice:** a strong narrative opening may delay the visitor’s route to a relevant project.
- **Evidence visibility vs card brevity:** proof and limits are essential, but full evidence cannot fit safely into overview cards.
- **Technical specificity vs accessible entry:** internal vocabulary may be precise for builders yet opaque to writers, musicians, and newcomers.
- **Portfolio completeness vs recruitment honesty:** showing all fourteen projects does not imply all fourteen have an open or validated contribution path.
- **Browser evidence vs human evidence:** the local packet explicitly says browser behavior cannot prove understanding or recruitment intent ([STRATEGY.md lines 149–152](</home/vrondelli/projects/domainspec-core/ops/development/2026-07-26-co-op-project-showcase-recruitment-research/STRATEGY.md:149>)).

## Questions for Synthesis

1. What first decision must the opening support: “Which project interests me?”, “Which problem is mine?”, or “How can I contribute?”
2. Which two to four lenses are understandable without internal framework knowledge and supported by all fourteen project records?
3. Is every project entitled to equal overview prominence, or should current proof and contribution availability change ordering?
4. What is the minimum owner-admitted public field set that can generate both cards and presentation views?
5. Which evidence markers remain meaningful at projection distance without turning status into unsupported marketing?
6. Must collection filters, selected project, and presentation position all be shareable URLs?
7. What content may presentation mode suppress, and what proof/limit fields must never disappear?
8. What human test will distinguish attractive scanning from actual retellability and contribution choice?
9. Can a newcomer reach an appropriate project without knowing any project name?
10. Where should a visitor land when a project currently has no concrete contribution path?

## Explicit Exclusions

- No redesign of the existing 45-minute meeting.
- No final marketing copy, naming, visual style, illustration direction, or screenshot-derived aesthetic verdict.
- No claim that any cited precedent proves comprehension, coherence, contribution, or recruitment.
- No investor-prioritization hierarchy; the local strategy rejects investor purpose as a proxy for collaborator decisions ([STRATEGY.md lines 128–136](</home/vrondelli/projects/domainspec-core/ops/development/2026-07-26-co-op-project-showcase-recruitment-research/STRATEGY.md:128>)).
- No revival of the prior Exchange admission, appointment, SLA, expiry, or receipt mechanism.
- No assumption that browser tests establish learning.
- No modal-as-project-page recommendation.
- No requirement for view transitions, scrollytelling, or reveal.js; these are precedent probes, not selected dependencies.
- No authority claim from Inventory: it is expressly a non-authority discovery read model ([STRATEGY.md lines 151–152](</home/vrondelli/projects/domainspec-core/ops/development/2026-07-26-co-op-project-showcase-recruitment-research/STRATEGY.md:151>)).
- No final post-discussion position is supplied here; this report intentionally preserves only the initial position for later Robot Talks synthesis.
