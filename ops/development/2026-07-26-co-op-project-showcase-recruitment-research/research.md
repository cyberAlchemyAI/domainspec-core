# Research Transcript

This file mechanically preserves the four registered explorer returns. Initial and post-Robot-Talk positions are copied verbatim from the immutable lane snapshots; synthesizer, reviewer, writer, and auditor returns are intentionally excluded.

## Agent 1 — Ahrens, Sönke

### Initial Return

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

### Post-Robot-Talk Final Position

# Final Robot-Talk Position — Ahrens, Sönke

Dispatch: `2026-07-26-co-op-project-showcase-recruitment-research`  
Lane: `lane_z_explorers`  
Position type: **Final post-discussion position; bounded recommendation, not an implementation or recruitment verdict**

## Agreements

1. **One corpus, two view policies.** Senge and I agree that shared truth does not require identical density, ordering, or controls. Project identity, present state, proof, limit, and contribution path must remain invariant. Live mode may project a sparse subset; self-guided mode may expose the complete progressive detail. A presenter-only factual explanation would violate the shared-source requirement.

2. **Stable project identity and durable routes are non-negotiable.** Every project needs a stable slug or URL, independently orienting opening, browser-history-safe navigation, and a return route to the collection. Live jumps should resolve to these same identities. Neither a modal nor a hidden fragment should be the sole home of project truth.

3. **The live artifact needs a recoverable map.** Fourteen projects make interruption, comparison, and audience-directed branching normal. A one-action overview, visible current project, and return-to-map behavior are necessary recovery infrastructure, not presentation ornament.

4. **Cards are projections, not the architecture.** A card or compact project opening may support scanning, but fourteen equal cards would falsely imply equal maturity, equal relevance, and equal contribution availability. The underlying record must survive without card styling, and the live room must not recite all cards with equal weight.

5. **Narrative reveal must be sparse and disposable.** A concrete misconception or failed domain act can focus attention, but no fact may remain trapped behind staged disclosure. The reveal succeeds only if visitors can subsequently locate, distinguish, and revisit projects. It must resolve to readable static content and yield immediately to recovery after interruption.

6. **Mechanics are not outcomes.** Deep links, projection readability, keyboard operation, successful jumps, and browser fallback can be validated mechanically. They do not prove comprehension, retellability, recruitment intent, or contribution selection.

## Disagreements That Remain

### Decision-first opening vs room-map opening

I retain decision-first as the default **cold-entry** opening: a visitor should first recognize a problem, domain act, or contribution appetite without translating unfamiliar project names. Senge’s full landscape is stronger as the first **room-orientation checkpoint**, once the common possibility has been established. I do not support making a fourteen-project map the first unexplained screen for every visitor.

The remaining empirical question is how quickly the map must appear. My boundary is strict: the opening may earn attention, but it must not delay the full landscape long enough to conceal scope or imply a single linear story.

### Durable detail routes vs live sparse projection

There is no architectural disagreement about durable routes. The remaining tension is operational: a live sparse surface can omit so much that the presenter becomes the real information system. Senge allows visible text plus spoken connective explanation; I require every load-bearing claim and limit to be recoverable on the linked project route. Spoken transitions may connect facts, but must not repair missing project meaning.

### Card comparison vs non-linear facilitation

I still value compact side-by-side comparison for self-guided choice. Senge correctly shows that the room needs jumps and recovery more than dense simultaneous comparison. Therefore the collection should support both a semantic comparison view and a low-density room map derived from the same records. I reject forcing one layout to serve both.

### Narrative reveal vs recovery

Senge gives recovery priority whenever a question or failure interrupts a reveal. I agree. I still permit one opening contrast where it earns the project vocabulary, but the map is the recovery authority. No later project should depend on remembering the dramatic sequence, and no presenter should have to replay fragments to restore context.

## What Changed From My Initial Position

- I initially described a decision-first index followed by a portfolio overview. I now distinguish **cold-entry orientation** from **room orientation**: decision-first is the entrance; the room map must appear early and remain one action away throughout live use.
- I treated presentation mode chiefly as a lower-density view over durable routes. Senge’s failure analysis changed this into a stronger contract: presentation mode also requires explicit recovery state—current project, last project or history-safe return, labeled overview, and direct jump.
- I originally framed cards as a comparison aid. I now narrow that claim: cards may be useful in self-guided comparison, but the live map should not inherit card density or equal-card rhetoric merely for visual consistency.
- I initially accepted a memorable narrative opening with general cautions. I now cap it at one meaningful contrast, require a static resolved state, and subordinate it to immediate recovery.
- I had not made failure independence explicit enough. The final position requires semantic overview and detail content to remain usable if presentation enhancement, animation, embedded media, presenter notes, network access, or QR handoff fails.

## Explicit Tension Synthesis

**Tension:** A newcomer needs a decision-first entrance, while a live audience needs a room map before non-linear facilitation can be safe.

**Synthesis:** Use a short orientation-to-map bridge:

1. present one concrete domain act, friction, or misconception;
2. state the changed possibility in ordinary language;
3. reveal the complete project landscape immediately;
4. offer recognizable decision lenses over that landscape;
5. enter selected projects through stable identities;
6. return to the landscape after every project, interruption, or question;
7. hand off to the durable self-guided route.

This is not a compromise that alternates two unrelated openings. The concrete act explains how to read the map; the map prevents the concrete act from becoming a misleading single-story funnel. In self-guided use, a visitor may skip directly to decision lenses or all projects. In live use, the presenter may curate a route, but the audience can always see that selection is not ranking or completeness.

## Final Recommendation and Boundary

Recommend a **decision-first, map-recoverable, route-durable showcase** built from one owner-admitted project record per project.

The minimum record should support:

- stable project identity and URL;
- one recognizable domain act or problem;
- present state and proof-bearing statement;
- adjacent honest limit;
- bounded contribution path or explicit absence of one;
- deeper evidence and provenance;
- optional relations to other projects.

Derive three surfaces from those records:

1. **Cold-entry orientation:** one short concrete opening, decision lenses, and an immediate all-projects route.
2. **Self-guided collection and detail:** semantic comparison, durable project pages, complete proof and limits, breadcrumbs/history-safe return, and mobile/keyboard operation.
3. **Live projection:** sparse project openings, complete labeled room map, current-position cue, direct jumps, return-to-map recovery, and private non-authoritative presenter cues.

Do not use long-form project dialogs, autoplay, truth-bearing hidden fragments, an equal-time fourteen-card recital, or a full-screen slide deck as the default website. Do not let a dense documentation page become the projected surface. Accordions remain optional only for bounded supplementary detail.

This recommendation does **not** select a visual style, presentation framework, final taxonomy, final project ordering, or marketing copy. It does not prove the proposed opening, lenses, map, or contribution routes work. Admission requires current project truth and public boundaries from the owning lane; validation requires separate browser mechanics evidence and human tests for cold-reader orientation, project distinction, retellability, recovery after interruption, later revisit, and bounded contribution choice.

## Agent 2 — Senge, Peter

### Initial Return

## Initial Robot-Talk Report — Senge, Peter

Dispatch: `2026-07-26-co-op-project-showcase-recruitment-research`  
Role: Lane Z live-use explorer  
Method: empirical facilitation analysis of live showcases, browser-native presentations, audience participation, and presenter-to-self-guided handoff.

Local scope anchors:

- The product under research is one browser-native project showcase used both live and self-guided, not a replacement for the existing 45-minute Co-Op meeting: `ops/development/2026-07-26-co-op-project-showcase-recruitment-research/STRATEGY.md`, selectors `#corrected-scope` and `#solution-independent-problem`.
- My lane must attack the portfolio-first hypothesis from projected readability, pacing, non-linear jumps, questions, passive-listener value, speaker/audience separation, and later browsing: `ops/development/2026-07-26-co-op-project-showcase-recruitment-research/dispatch-sheet.json`, selector `groups[group_id=lane_z_explorers].agents[agent_name="Senge, Peter"].initial_prompt`.
- Inventory has no current external precedent survey for this corrected question; browser behavior cannot establish understanding or recruitment intent: `ops/development/2026-07-26-co-op-project-showcase-recruitment-research/STRATEGY.md`, selectors `#strategy-inventory-packet > gaps-and-residue` and `#strategy-inventory-packet > design-consequences`.

## Initial Position

The portfolio-first hypothesis survives the room only if “portfolio” is a navigable room map, not a fourteen-card recital.

One factual corpus can support both modes, but one layout cannot. Self-guided mode should expose comparison, persistent orientation, stable project URLs, evidence, limits, and contribution routes. Live mode should derive a lower-density projection from those same fields, provide an always-recoverable overview, support direct jumps by stable project identity, and keep presenter-only pacing prompts outside the public content.

The strongest candidate movement is:

1. concrete misconception or familiar failed act;
2. reveal the portfolio-level possibility;
3. show the full project landscape;
4. enter a few contrasting projects through recognizable acts;
5. return to the landscape for audience-directed jumps;
6. end on bounded contribution choices and a durable URL.

That uses the Veritasium-like misconception-to-reveal movement as a structural hypothesis, not imitation or visible page narration. It should be rejected if cold listeners remember the reveal but cannot locate, distinguish, or revisit projects.

## Key Findings

### 1. A live portfolio needs explicit non-linear recovery, not merely next/previous controls

**Fact.** reveal.js supports an overview showing the whole presentation, direct jumps by slide number or stable ID, and internal links to ID-addressed sections. Its speaker view separately supplies notes, next-slide preview, elapsed time, and pacing information. These are concrete precedents for overview, jump, and speaker/audience separation—not proof that this showcase should use reveal.js. [Overview mode](https://revealjs.com/overview/), [jump to slide](https://revealjs.com/jump-to-slide/), [internal links](https://revealjs.com/links/), [speaker view](https://revealjs.com/speaker-view/).

**Inference.** Fourteen projects make interruption and audience-directed branching normal, not exceptional. A purely linear “next project” sequence will produce navigation panic, skipped-context confusion, or visible backtracking.

**Proposal.** Give every project a stable slug/URL and one-key or one-control access to a labeled portfolio overview. After any project detail or audience question, “return to map” must restore the overview without losing the previous project or browser history.

### 2. Shared facts do not require shared density or sequencing

**Fact.** reveal.js explicitly distinguishes slide view for presenting from scroll view for individual reading; scroll view flattens the authored presentation into a linear flow and can activate automatically at mobile widths. This is a deployed example of one corpus rendered through different consumption modes. [reveal.js scroll view](https://revealjs.com/scroll-view/).

**Inference.** “One truth source” should mean invariant factual fields and claim ceilings, not identical DOM exposure or identical ordering. A projection may foreground one act, one proof, and one limit while self-guided detail exposes the complete record.

**Proposal.** Treat mode as a view policy:

- invariant: project identity, concrete act, present status, proof, limit, trajectory, contribution;
- live-derived: larger type, fewer simultaneous fields, controlled sequence, room map, presenter-only cue;
- self-guided-derived: comparison, complete evidence links, expanded limits, deep links, back behavior, mobile reflow.

No live-only factual claim or presenter-only “secret explanation” may be required to understand a project later.

### 3. Incremental reveal is useful only when it controls attention without hiding the record

**Fact.** reveal.js fragments can expose or highlight elements step by step. W3C guidance warns that automatically changing carousel content can be hard to discover or disorienting; users need keyboard control, understandable focus behavior, and the ability to pause or stop movement. [reveal.js fragments](https://revealjs.com/fragments/), [W3C carousel tutorial](https://www.w3.org/WAI/tutorials/carousels/), [WAI-ARIA carousel pattern](https://www.w3.org/WAI/ARIA/apg/patterns/carousel/).

**Inference.** A misconception-to-reveal movement can focus the room, but hidden fragments are poor self-guided truth storage. Auto-advance is especially dangerous when an audience question changes pace.

**Proposal.** Use at most one meaningful reveal per portfolio opening or project opening: familiar belief/act → changed possibility or constraint. In self-guided mode, all reveal states must resolve into readable static content. No auto-rotation; keyboard and visible controls must work; motion must be pausable and nonessential.

### 4. A useful demo follows a concrete actor and action, then exposes evidence and limits

**Fact.** GOV.UK service-demo guidance recommends a short setup, a user or lead, the action through the service, and the payoff; it also recommends deciding which repeated or low-value actions to skip and having one person drive when several artifacts are involved. The guidance says a good demo helps lightly briefed viewers understand the service and focus later questions. [GOV.UK service-demo guidance](https://services.blog.gov.uk/2020/10/12/service-demos-how-to-tell-the-story-of-your-service/).

**Inference.** A project opening should not begin with internal architecture. For a musician, writer, designer, or developer, orientation begins with a recognizable act—compose, revise, prototype, inspect, play, test—followed by what exists and where it stops.

**Proposal.** Each live project opening should fit: actor/domain act → friction or misconception → visible project move → present proof → honest limit → bounded ask. Architecture appears only when it explains the move, proof, or limit.

### 5. Questions and passive listening require different but simultaneous affordances

**Fact.** UK Government Analysis Function guidance advises short, non-text-heavy presentations with audience interaction or Q&A, and recommends a clear, concise script for demos. GOV.UK show-and-tell guidance describes demonstrations as a way to share completed work with a wider stakeholder audience. [Guidance for presenters](https://analysisfunction.civilservice.gov.uk/analysis-in-government-aig-month-hub/aig-month-guidance-for-presenters/), [GOV.UK agile show-and-tell guidance](https://www.gov.uk/service-manual/agile-delivery/agile-tools-techniques).

**Inference.** The room cannot depend on everyone asking questions. Passive listeners need the current project, its place in the whole, and its one-sentence claim boundary continuously recoverable. Questioners need fast direct jumps without forcing everyone through intermediate pages.

**Proposal.** Keep a compact orientation rail or returnable map containing “where we are / what this project does / what is proven.” Capture questions outside the projected truth surface; answer by jumping to an existing project field or evidence route, not by improvising a new public claim.

## Gaps or Inconsistencies

- No evidence yet establishes the actual projector size, room distance, ambient light, remote/hybrid participation, input device, or network reliability. Therefore font sizes and interaction timings remain test parameters, not settled values.
- The existing meeting’s internal agenda and speaker handoff conventions were intentionally outside my allowed reading surface. The storyboard below describes use of the artifact within 45 minutes, not a redesign of meeting governance.
- No current human observation shows whether a writer, musician, developer, or curious listener can distinguish fourteen projects after the live session.
- No evidence establishes whether audience questions cluster by project, domain, contribution type, or cross-project theme. The portfolio overview may need project-first or decision-first grouping; that remains a synthesis question.
- reveal.js demonstrates technical feasibility for dual views and non-linear control, but it is a presentation framework precedent, not evidence that its slide ontology is the right information architecture.
- The local Inventory packet says current project names, roots, and statuses remain unresolved. Stable live jump labels cannot be finalized until the repository-truth lane resolves those identities: `STRATEGY.md`, selector `#strategy-inventory-packet > gaps-and-residue`.
- “Brief but substantial and memorable” has no measured threshold. A timed opening can still be forgettable; recall and next-choice evidence must remain separate from duration.

## Local Tensions

1. **Portfolio completeness vs room comprehension.** Showing all fourteen establishes scope; narrating all fourteen with equal weight produces sameness and exhausts attention.

2. **Presenter pacing vs audience agency.** A controlled reveal can create clarity; questions demand non-linear jumps that break a staged sequence.

3. **Projection density vs self-guided trust.** The room needs large, sparse surfaces; later evaluation needs proof, limits, provenance, and detail.

4. **Memorable reveal vs project truth.** A misconception can create contrast, but it can also become the remembered “trick” while the actual project disappears.

5. **Shared page vs slide-deck cosplay.** Presentation controls are useful; forcing self-guided visitors through full-screen slides, fragments, and next/previous steps adds click debt and weakens comparison.

6. **Contribution visibility vs premature commitment.** The ask must be visible in the room, but interest, contact, and commitment must not collapse into one recruitment action.

## Questions for Synthesis

- Does the stable room map organize primarily by project, recognizable domain act, contributor role, or a hybrid of project identity plus optional filters?
- Which three or four projects are sufficiently different to demonstrate portfolio breadth without implying that unshown projects matter less?
- Must live mode have its own URL/query parameter, or should projection be a reversible control on the same canonical route?
- What is the minimum always-visible project status vocabulary that remains readable at projection distance?
- When an audience question crosses projects, should the presenter jump to a comparison surface, or return to overview and enter the second project?
- What evidence will count as a successful handoff: QR/URL scan, later project revisit, accurate retelling, identification of one relevant project, or selection of a bounded contribution?
- Can the misconception-to-reveal opening be removed without reducing orientation? If not, is it carrying genuine explanatory work or merely theatrical memory?
- What is the recovery path when the live artifact, network, embedded demo, presenter view, or input device fails?

## Candidate Live Storyboard

This is a **proposal for artifact use**, not a redesign of the Co-Op meeting.

| Elapsed time | Projected surface | Presenter action | Passive-listener value | Recovery anchor |
|---|---|---|---|---|
| 0–3 min | One concrete misconception/felt problem, then portfolio-level reveal | Establish why these projects belong in one room without naming internal frameworks first | Understand the shared possibility in ordinary language | Permanent “view all projects” control |
| 3–7 min | Full fourteen-project landscape with distinctive act + honest status | Scan breadth; explain how to read the map | See the whole before any selection | Overview remains one action away |
| 7–10 min | Audience-or-presenter choice among contrasting entry points | Select 3–4 projects representing different domain acts | Understand that selection is a route, not a ranking | Stable project slugs and overview |
| 10–25 min | Three compact project openings, about five minutes each | For each: act → friction → project move → proof → limit → ask | Retain one concrete difference per project | Project heading, status, and “back to map” |
| 25–33 min | One deeper project route | Demonstrate how opening facts expand into evidence, limits, trajectory, and contribution | Learn how to inspect any project later | Direct URL plus breadcrumb/history |
| 33–39 min | Return to map; audience-directed jumps | Take questions and jump non-linearly to existing fields or projects | Questions add value without destroying orientation | Overview and last-visited project |
| 39–43 min | Contribution comparison | Distinguish curious follow-up, offer of help, contact, and commitment | See multiple bounded ways to continue | Each ask links to its project context |
| 43–45 min | Durable handoff surface | Show memorable URL/QR and what can be explored afterward | Know where to return and what remains available | Self-guided mode defaults to readable overview/detail |

The schedule deliberately does **not** allocate equal narration time to fourteen projects. Completeness comes from the overview and durable self-guided corpus; the live sequence demonstrates how to read and trust it.

## Presenter / Self-Guided Surface Contract

| Concern | Canonical invariant | Presenter view | Self-guided view |
|---|---|---|---|
| Project identity | Stable name, slug, and domain act | Large title + act | Title, act, route metadata |
| Present truth | What exists now | One concise proof-bearing statement | Full status and evidence links |
| Claim ceiling | Honest current limit | Always visible or spoken from visible text | Expanded limit and provenance |
| Trajectory | Clearly future, not present | One bounded direction | Detailed proposed trajectory |
| Contribution | Concrete bounded action | One visible next step | CTA ladder with prerequisites and contact context |
| Sequence | No canonical “correct” project order | Curated route plus non-linear jump | Visitor-selected browse/filter/order |
| Density | Same factual fields | Sparse derived projection | Complete progressive detail |
| Notes | Never authority | Private timer, cues, question reminders | Absent |
| Navigation | Stable project URLs and history semantics | Overview, jump by label, previous/return | Links, breadcrumbs, browser Back, mobile reflow |
| Reveal | No truth exists only in a hidden state | Manual, minimal attention control | Static/readable resolved state |
| Motion | Nonessential and controllable | Manual transitions only | Respect reduced-motion; no auto-rotation |
| Failure | Facts remain accessible without enhancement | Static fallback and direct URLs | Semantic HTML/content remains usable |

Contract test: if a presenter says a load-bearing fact that a later visitor cannot find on the project route, the modes have diverged into separate truth sources.

## Failures and Recovery

| Failure | Observable symptom | Recovery | Guardrail |
|---|---|---|---|
| Presenter loses place after a question | Repeated backtracking or “where were we?” | One-action overview; mark current and last project | Stable map and project IDs |
| Audience asks about an unplanned project | Presenter searches or scrolls visibly | Jump by project label/slug | Search/jump control tested before session |
| Network or embedded demo fails | Blank frame, spinner, blocked iframe | Use locally available factual preview/evidence still; disclose demo unavailable | No load-bearing claim depends on live external content |
| Presenter notes appear on projector | Private cues or timing leak | Close/blank presenter surface; continue from public orientation fields | Separate window/display test |
| Project opening overruns | Remaining projects disappear | Return to overview; move detail to self-guided route | Per-opening cue and visible elapsed timer |
| Projection makes text unreadable | Back rows cannot identify status/limit | Switch to low-density live view or browser zoom | Room-distance rehearsal; responsive zoom without clipping |
| Animation or carousel disorients | Content changes before reading/focus moves unexpectedly | Pause motion; show resolved static state | No autoplay; keyboard controls; reduced-motion support |
| Deep jump destroys context | Audience sees detail without knowing which project/why | Persistent project identity + one-line act; return to map | Every detail route is independently orienting |
| QR code or handoff fails | Visitors cannot revisit | Speak and display a short stable URL | QR is redundant, never sole route |
| Question invites claim inflation | Presenter speculates beyond evidence | Point to visible limit; label open question; defer answer | Proof and limit adjacent in both modes |
| Browser enhancement fails | Blank or unusable presentation shell | Semantic overview/detail HTML remains readable | Progressive enhancement, not JavaScript-only truth |

## Concrete Counterexample

**A good presentation can become a poor website:** a conventional reveal.js deck with fragments, full-viewport slides, and next/previous navigation can be excellent for presenter-controlled attention. As a self-guided fourteen-project portfolio, the same default slide surface makes comparison expensive, hides upcoming content behind interactions, and turns project discovery into sequential click debt. reveal.js itself acknowledges the mismatch by providing a separate scroll view because scrollable pages are easier to read independently, and that mode flattens the slide hierarchy into a linear flow. [Fragments](https://revealjs.com/fragments/), [scroll view](https://revealjs.com/scroll-view/).

The converse also holds: the reveal.js documentation page for [speaker view](https://revealjs.com/speaker-view/) is a useful self-guided reference with navigation, prose, code, and detailed options, but projecting that documentation page as the live explanation would produce dense text, small code, competing site navigation, and no audience-level story. The facts may be good; the live presentation is bad.

Therefore the Co-Op artifact should borrow dual rendering, overview, jumps, and speaker separation—but block both “deck as website” and “documentation page on projector.”

## Position Boundary

This is my **initial position**, before Robot Talks with Ahrens or synthesis. It does not claim that the storyboard improves comprehension, recall, recruitment, or contribution. Those require separate black-box mechanics tests and human evidence: cold-reader retelling, project distinction, next-choice clarity, and bounded contribution selection.

### Post-Robot-Talk Final Position

# Final Robot-Talk Position — Senge, Peter

Dispatch: `2026-07-26-co-op-project-showcase-recruitment-research`  
Lane: `lane_z_explorers`  
Position type: **Final after exchange with Ahrens; candidate input to synthesis, not an implementation or outcome verdict**

## Agreements

1. **One factual substrate does not mean one layout.** Ahrens and I agree that project identity, concrete domain act, present proof, honest limit, trajectory, and contribution path must remain invariant, while presentation and self-guided views may change density, sequence, and controls. Neither mode may introduce a load-bearing fact unavailable in the durable project record.

2. **Every project needs a durable detail route.** Cards, filters, accordions, dialogs, fragments, and live jumps are projections or controls, not substitutes for stable project URLs, browser history, evidence links, limits, and later return. Accordions may hold bounded supplementary material; dialogs should not contain long project stories.

3. **A fourteen-card recital fails both modes.** Visually equal cards risk flattening different domains, maturity, proof, and contribution availability. In the room, narrating fourteen equal previews exhausts attention; on the website, equal cards force outsiders to translate their needs into unfamiliar project names.

4. **The live surface needs non-linear recovery.** A presentation sequence must tolerate questions and direct jumps. A labeled overview, stable project identity, return-to-map control, and last-position recovery are necessary. Next/previous navigation alone is insufficient.

5. **Narrative reveal is subordinate to orientation and truth.** A misconception-to-reveal movement may focus attention, but no fact may exist only in a hidden fragment, no reveal should auto-advance, and the technique fails if people remember the trick but cannot distinguish, locate, or revisit projects.

6. **Mechanics are not comprehension or recruitment evidence.** Browser checks can establish URL, history, keyboard, focus, responsive, projection, and fallback behavior. They cannot prove retellability, project relevance, trust, or willingness to contribute.

## Disagreements That Remain

### 1. Decision-first opening versus room-map opening

Ahrens prefers a decision-first entrance: a visitor recognizes a problem, domain act, or contribution appetite before encountering project identities. My initial live sequence used a concrete portfolio-level reveal followed quickly by the complete room map.

The disagreement remains contextual rather than absolute. For a self-guided newcomer with a concrete need, decision-first is the stronger default because project names may be meaningless. In a live room, however, a presenter must establish the finite whole early enough that a curated subset is not mistaken for the entire portfolio or a priority ranking.

I therefore reject both universal decision-first and universal map-first. The live opening should begin with one concrete decision-bearing tension, then reveal the full map as the orientation answer. The self-guided opening should offer two simultaneous exits: plain-language decision lenses and “view all projects.” The map is the shared recovery layer, not necessarily the first interactive demand.

### 2. Durable detail routes versus live sparse projection

There is no disagreement about durable routes; the remaining tension is how much of their content must stay visible live. Ahrens emphasizes complete first-screen detail fields, while my room analysis requires aggressive density reduction.

My final position is that live mode must always show project identity, concrete act, one present-proof marker, one honest limit, and the existence of a bounded ask. It may suppress evidence detail, chronology, prerequisites, related projects, and full trajectory, provided each suppressed field is reachable through the same stable project route. A spoken limit does not satisfy the contract unless the projected surface or directly opened canonical route also contains it.

### 3. Card comparison versus non-linear facilitation

Ahrens correctly treats cards as conditional comparison aids. I continue to resist making a card grid the primary live navigation mechanism. Fourteen dense cards are difficult to project, while fourteen sparse cards erase distinctions.

The final distinction is: self-guided collection projections optimize comparison; the live map optimizes recognition, location, and recovery. Both may derive from the same compact project fields, but they need not share geometry or equal density. Live jumps should use labeled project identity or a small number of audience-understandable lenses, not tiny card targets or presenter-visible taxonomy controls.

### 4. Narrative reveal versus recovery

Ahrens gives immediate choice more weight; I initially gave narrative movement more weight. I now narrow the reveal sharply. It should occur once at portfolio level, last no longer than needed to expose a concrete tension, and resolve into the stable map. Project-level openings may use contrast in language, but should not depend on staged hidden states.

If a question interrupts the reveal, the presenter must be able to resolve it immediately and show the map. Recovery outranks theatrical sequence. If cold listeners can choose an appropriate route without the reveal, the reveal is optional editorial value, not architecture.

## What Changed From My Initial Position

- I no longer recommend “misconception → reveal → full landscape” as the default opening for both modes. It is now a live candidate only; self-guided mode should foreground recognizable decision lenses alongside direct access to all projects.
- I moved the full portfolio map from “the portfolio-first opening” to “the shared orientation and recovery layer.” This preserves room coherence without forcing an outsider to start from project names.
- I accept Ahrens’s counterexample as decisive: a musician with a specific creative act and contribution type should not have to decode fourteen internal project identities before finding relevance.
- I strengthened the durable-route requirement. Live sparse projection is not a separate presentation document; it is a derived view over addressable project records with an immediate escape to normal browsing.
- I reduced project-level narrative reveal. Concrete contrast belongs in the opening grammar, but fragments or staged disclosure must not carry truth, navigation, or comprehension.
- I distinguish the self-guided comparison surface from the live recovery map. They share content fields and identities, not necessarily card layout or interaction behavior.

## Explicit Tension Synthesis

**Tension:** Decision-first routing helps an outsider find relevance, but a live room needs a common picture of the whole; showing the whole first can overwhelm, while delaying it can make curated examples look exhaustive or ranked.

**Synthesis:** Use a **decision-to-map-to-route loop**:

1. begin with one recognizable act, problem, or contribution tension;
2. reveal the finite fourteen-project map as the answer-space and orientation anchor;
3. enter a project through either that tension or a labeled project identity;
4. show a sparse proof-and-limit-bearing opening;
5. return to the map after a project or interruption;
6. hand off to the stable detail URL for self-guided evidence and contribution.

In self-guided mode, steps 1 and 2 are parallel choices rather than a forced sequence. In live mode, they are a short curated sequence, but the presenter can jump directly to steps 2–5 when questions intervene.

This synthesis preserves Ahrens’s decision-first accessibility without sacrificing shared-room orientation, and preserves my non-linear facilitation without making a card grid or slide sequence authoritative.

## Final Recommendation and Boundary

Recommend a hybrid browser artifact with:

- a plain-language decision-first opening plus an equally visible “all projects” route;
- a stable portfolio map used as the live room overview and recovery surface;
- self-guided comparison projections generated from compact project records;
- one durable URL per project and addressable evidence/contribution sections;
- a live view policy that enlarges and sequences the same records while retaining identity, proof, limit, and ask;
- presenter-only notes and pacing controls with no factual authority;
- manual, optional narrative reveal that resolves to static readable content;
- direct labeled jumps, browser-history preservation, keyboard operation, reduced-motion behavior, and semantic fallback;
- separate validation for browser mechanics, projected readability, cold-reader retellability, project-choice clarity, and bounded contribution decisions.

Do not promote a universal portfolio-first grid, a universal decision-first funnel, a slide deck embedded as the website, a documentation page projected as the presentation, or an interaction whose explanation depends on the presenter. Do not infer comprehension or recruitment success from implemented navigation.

This final position is a research recommendation for synthesis. It does not select visual style, finalize public copy, resolve project authority/name conflicts, redesign the existing Co-Op meeting, or claim that the proposed hybrid has been tested with technical builders, writers, musicians, designers, researchers, or curious listeners.

## Agent 3 — Alexander, Christopher

### Initial Return

# Initial Robot-Talk Report — Alexander, Christopher

Dispatch: `2026-07-26-co-op-project-showcase-recruitment-research`  
Lane: `lane_a_explorers`  
Position: repository-truth and content-pattern explorer  
Mutation: none

## Initial position

A project grid is a useful index, but it is a weak first decision surface. Fourteen equally weighted project names force visitors to decode internal naming before they can decide whether anything matters to them.

My provisional alternative is a hybrid, decision-first entrance:

1. “What do you want to do?” — create, understand, compete, improve a workflow, build trustworthy knowledge, or contribute a skill.
2. “Which recognizable act feels like yours?” — shape a sentence, make a sound, run a route, inspect a system, review an interface, test an agent, trust a metric.
3. Reveal the relevant projects, each with its honest maturity and one bounded contribution.
4. Preserve a complete project index as a secondary route and as the presenter’s non-linear navigation surface.

This does not replace project identity. It delays project names until the visitor has a reason to care.

## Key findings

### Facts

1. The fourteen projects do not share one maturity level. The corpus contains runnable proof slices (Poker Agent Arena, Body War pilot, UI Prototyping Studio, IDE Extension), seeds/scaffolds (X-Ray, Arcanum Journey), research-only systems (Agentic Music Studio, Tower System), candidate patterns (User/Translate/Guide, IDE Ergonomics), and non-executed specifications/offers (AutoAds, Sonar Loop, Ontologize). A uniform “our projects” voice would inflate some and diminish others.

2. The strongest shared unit is not “AI project.” It is a recognizable domain act plus a governed boundary:

   - writing from intent;
   - explaining through a learner’s known anchors;
   - editing musical structure;
   - making a legal poker decision;
   - submitting a real run;
   - choosing and annotating a UI variant;
   - preserving knowledge and disagreement;
   - approving durable IDE work;
   - routing a useful conversation moment;
   - inspecting hidden structure;
   - learning by installing and probing;
   - learning from ad outcomes;
   - running a governed code-quality cycle;
   - making business evidence auditable.

3. Current proof must remain project-specific. “Runnable,” “validated,” “research closed,” “candidate,” “scaffold,” and “docs-first” are not interchangeable.

4. Contribution asks can be concrete without inventing a recruitment system. Each project already exposes a missing witness, deferred layer, fixture, domain question, or owner decision that can become a bounded invitation.

5. Several public-name and authority conflicts remain unresolved:

   - `Body-War` is the container; `TROQAR` is the product brand.
   - UI Prototyping Studio exists at both `arcanum/projects/ui-prototyping-studio/` and `projects/ui-prototyping-studio/`; their visible READMEs are byte-equivalent in the inspected opening, but the public/private canonical destination is not established by that fact.
   - `ide-extension` and `IDE Ergonomics` overlap in IDE-adjacent experience but own different proofs: a governed local workbench versus a conversation-transition routing concept.
   - `ontologize` is the project/root name; `CyberAlchemy` is used as a working product/offer name, explicitly not a committed brand.
   - X-Ray is a seed in public Arcanum, not a promoted reusable behavior.
   - Arcanum Journey is staged in the private parent with a proposed public home; it must not be presented as shipped in public Arcanum.
   - Tower System’s owned components do not prove the assembled center.

### Inferences

- A decision-first opening will likely reduce name-decoding cost for cold visitors, but the repository corpus alone cannot establish recruitment effectiveness.
- The shared content grammar should normalize fields, not prose. Every preview may answer the same questions, but it should retain the project’s own verbs, objects, and stakes.
- “Clever” should mean a precise contrast or memorable concrete act—“a poker agent needs manners,” “a number the company can defend”—not mystery, puns, anthropomorphic AI, or generic transformation claims.
- The live presentation can use the same records if the presenter filters/sequences them rather than receiving a second set of slide copy.

### Proposals

- Make domain acts and contribution opportunities first-class filters.
- Show maturity at preview depth, not behind a detail click.
- Treat `proof` and `limit` as a paired field.
- Use exact deep links to projects; preserve browser Back and a persistent return-to-results state.
- Permit presenter mode to change density, sequence, and controls, but never facts or claim status.

## Gaps and inconsistencies

- No owner-admitted common public schema exists for all fourteen projects.
- There is no current human evidence showing whether visitors choose better by project, problem, domain act, skill, or ask.
- Some proof artifacts report historical validation but were not rerun in this lane; they are current repository receipts, not fresh execution.
- The UI Prototyping Studio duplicate root requires an owner decision before public linking.
- Body War’s root README still says no app prototype in the “first pass,” while `app/README.md` documents an app-backed validation channel. The latter is newer/current evidence; the earlier sentence should not be repeated as current whole-project status.
- Ontologize’s root README says research dispatch “not yet executed,” while `PRODUCT.md` and later research/offering artifacts exist. Public copy must cite the specific artifact/status rather than collapsing the project to the older root status.
- Inventory’s prior Experiment Exchange selection remains a typed negative: it is not the IA or recruitment mechanism for this artifact.

## Compact truth records

Each record uses:

`felt problem | domain act | exists now | honest limit | why matter | trajectory | proof | who could help | contribution | safe / forbidden`

1. **Whisper**

   Writing loses the author’s intent when drafting jumps directly from prompt to prose | shape a meaningful text by selecting audience, structure, voice, evidence, and movement | governed composition lifecycle, schemas, plans, auditions, review HTML, validators, and residue | L0 proof target is a Substack research post; other transports remain extensions, and transport availability is not proof | keeps author intent, audience fit, and review addressable | prove transports through contracts, fixtures, auditions, and human gates | canonical README defines lifecycle and explicit proof boundary | writers, editors, narrative designers, validation/tool builders | supply a bounded text intent, test a transport audition, or improve an evidence-aware review fixture | safe: “turns author intent into governed composition artifacts”; forbidden: “writes proven high-performing copy across formats” (`arcanum/spells/whisper/README.md#Purpose`, lines 10–14; `#Artifact-Lifecycle-Contract`, 60–78; `#Transport-Sequence`, 123–135).

2. **User / Translate / Guide**

   Generic explanations either flatten the target or ignore what the learner already knows | explain an unfamiliar system through a known anchor and test active understanding | candidate three-owner pattern separating protected user evidence, translation bridges, and guide orchestration | candidate pattern, not a universal tutor; must not hide profiling or silently store identity | could make technical systems learnable across domains without erasing mapping limits | stabilize owner contracts and validate active-understanding routes | current README states candidate status, responsibility split, and active-evidence promise | educators, domain translators, UX researchers, privacy/governance reviewers | provide a real cross-domain explanation case and test where its analogy breaks | safe: “candidate pattern for guided, bounded translation”; forbidden: “personalized tutor that knows or remembers the user” (`arcanum/development/user-guide/README.md#User--Translate--Guide`, lines 10–27; `#The-three-part-model`, 31–42; `#The-user-facing-promise`, 46–63).

3. **Agentic Music Studio**

   Text-to-audio systems can bypass musical craft, reproducibility, and instrument-like control | edit one shared musical specification through voice, live code, gesture, constraints, or perceptual feedback | closed local research tower, ten-process taxonomy, claim ledger, and architecture recommendation | not a build spec; “strangeness,” language-to-timbre compilation, and voice ergonomics remain unwitnessed | offers a path to agentic musical assistance where the human still shapes the music | build and test the smallest intent→spec→deterministic-realization witness | source-backed TidalCycles, stochastic synthesis, dissonance, DMI mapping, and Strasheela claims; design synthesis clearly labeled | musicians, live coders, instrument designers, DSP/perception researchers | implement or test one reversible spec-editing interface and measure latency/expressivity | safe: “researches spec-centered communication processes for music making”; forbidden: “working AI studio that makes good music or predicts listener strangeness” (`research/agentic-music-studio/README.md#Research-Tower--Agentic-Music-Studio`, lines 1–27; `#Promotion-boundary`, lines 59–62; `claim-ledger.md#Source-grounded-claims`, lines 8–17; `#Open-residue`, lines 30–35).

4. **Poker Agent Arena**

   Agent benchmarks become spectacle before legality, hidden information, timing, and replay can be trusted | submit a poker decision through a constrained protocol and inspect it hand by hand | runnable Local Arena CLI v0 with Kuhn runtime, sample agents, private transcript, redacted replay, deterministic replay, and diagnostics | no Hold’em, hosted matchmaking, real money, final composite leaderboard, or calibrated novelty mechanics | creates an inspectable test table for bounded decision agents | expand from Kuhn to Leduc, then consider engine and scoring layers | verification receipt reports unit, smoke, canary, redaction, invalid, timeout, crash, EOF, and replay checks passing | game-theory developers, protocol/test engineers, poker-agent authors | author a bounded sample agent, adversarial fixture, or Leduc reveal test | safe: “local toy-poker agent harness with verified L0 replay and boundary checks”; forbidden: “full poker competition platform or best-agent leaderboard” (`projects/poker-agent-arena/README.md#Current-Stage`, lines 9–24; `#What-The-Arena-Tests`, 26–34; `development/verification/local-arena-cli-v0/VERIFICATION.md#Outcomes`, lines 38–56; `#Deferred-Work`, 67–71).

5. **Body War / TROQAR**

   Running activity is hard to turn into a trustworthy, shared territorial game event | connect a Strava athlete, inspect runs, and submit one activity to a pilot track | app-backed pilot channel with browser UI, OAuth adapter, activity listing/submission APIs, fake-Strava Docker E2E path, and explicit pilot authority | this is a narrow pilot, not the full conquer/defend/clan/league/season game | grounds the game idea in real activity evidence before scaling mechanics | validate park-track evidence and then expand game rules/mechanics | app README documents runnable setup, endpoints, and fastest-verified-time authority | runners, game designers, geospatial engineers, privacy/security testers | run the fake-Strava flow, test redaction, or design one bounded territory-rule fixture | safe: “TROQAR pilot can submit running activity evidence to a track”; forbidden: “live territorial running platform with proven engagement” (`projects/body-war/README.md`, lines 1–27; `projects/body-war/app/README.md`, lines 1–20, 40–45, 59–77).

6. **UI Prototyping Studio**

   UI iteration can become untraceable generation or unsafe auto-application | generate 1–3 variants, choose, annotate, stage a deterministic mutation, approve, apply, and record | runnable TypeScript/Fastify CLI mutation loop, browser preview/annotation, accept/revert controls, and Playwright E2E | only L0 exists in code; L1–L2 are release hardening targets, L3–L6 remain design/deferred, and preview is not a full SPA | makes human approval and revision provenance part of interface work | harden accessibility/layout, then test deeper interaction, identity, fitness, and human evidence | README reports runnable backend and shipped preview behavior | designers, frontend/accessibility engineers, human-loop researchers | bring a real HTML variant set, test keyboard/layout behavior, or challenge the two-gate diff | safe: “working accountable UI exploration floor”; forbidden: “complete AI design studio or proven high-quality design generator” (`arcanum/projects/ui-prototyping-studio/README.md`, lines 1–32; competing identical opening at `projects/ui-prototyping-studio/README.md`, lines 1–32).

7. **Tower System**

   Learning disappears between sessions, while a single AI voice tends toward agreeable, unauditable answers | build durable domain knowledge, summon tensioned perspectives, and inspect a scored decision trail | story-first product model, owned precedent map, and a planned witness unit | the central persona→tension→grading assembly is unwitnessed; MOGT has zero live experiment runs | could join learning and application into one compounding loop | test MOGT, then build the smallest witness that proves or kills the three core unknowns | research identifies existing owned tower/dispatch components while explicitly isolating the unproven center | knowledge-system researchers, evaluators, debate/decision designers | implement the witness unit or define a non-vacuous persona/tension/grade test | safe: “credible research bet assembled from owned pieces”; forbidden: “working self-improving expert tower” (`research/tower-system-taxonomy/PRODUCT-VIEW.md#The-frustration`, lines 16–34; `#Why-it-can-work`, 87–99; `#The-honest-part`, 101–119).

8. **IDE Extension**

   IDE-adjacent agent work can cross into durable state without clear authorization or receipts | preview a work action, approve it, and inspect the resulting durable receipt | local-server-first browser workbench, schemas, minimal kernel, L0 screen, bounded manual bridge, and tests | local-only witness; not an autonomous worker, browser-control adapter, provider execution layer, or IDE wrapper | proves the approval boundary before claiming an IDE agent | complete Workbench UI V1 and independently validate any future wrapper/control adapters | current status records the local witness and explicit boundary; first proof is server→render→manifest→pending approval→receipt→durable event | workbench/frontend engineers, security reviewers, adapter/test authors | test an approval/denial/recovery path or implement a bounded UI increment | safe: “governed local workbench for IDE-adjacent agent work”; forbidden: “working autonomous IDE agent” (`projects/ide-extension/README.md`, lines 1–9, 24–59; `#Boundary`, 83–93; `#First-Witness`, 95–104).

9. **IDE Ergonomics**

   Useful moments discovered in AI conversation are easily lost or sent to the wrong workflow | select a phrase and choose a bounded next route—definition candidate, side note, handoff, ambiguity resolution, or delegation preview | product view, presentation/prototype artifacts, candidate routing contracts, and static fixture plan | strategy/draft candidate; first proof is the routing decision, not a full IDE plugin or execution layer | keeps momentum while preserving ownership and consent | test whether users understand and choose the right route from static conversation fixtures | product view defines the card, routes, pass/fail conditions, and non-execution boundaries | UX designers, IDE users, workflow/governance researchers | bring a real conversation snippet and test whether the route card makes the owner, artifact, boundary, and next choice clear | safe: “candidate conversation-transition routing layer”; forbidden: “IDE that autonomously understands and routes all work” (`projects/ide-ergonomics/PRODUCT-VIEW.md#One-Sentence-Product`, lines 13–21; `#MVP-Shape`, 178–203; `#Pass-Conditions`, 226–253; `#Product-Boundary`, 302–317).

10. **X-Ray**

   Important system structure is often buried across prose, code, plans, and implied relationships | split a bounded target into visual explanation lanes and inspect flow, dependencies, lifecycle, evidence, and risks | public Arcana seed with lane model, schemas, YAML visual library, validators, and local HTML/SVG examples | not promoted; no reusable live behavior evidence; not a production renderer | can make a complex target inspectable without pretending the diagram proves it | run live examples across target shapes, including an insufficient-context case, before promotion | README and validation package distinguish seed implementation from promotion evidence | information designers, technical writers, frontend/SVG developers, cold readers | create and test one source-marked x-ray of a bounded real system | safe: “seed for visual layered HTML explanations”; forbidden: “validated general-purpose visualization engine” (`arcanum/arcana/x-ray/README.md`, lines 1–19; `#Canonical-Lanes`, 32–57; `#Do-Not-Use-When`, 89–106; `development/VALIDATION.md#Promotion-Status`, lines 27–38, and `#Sigil-Development-Readiness`, lines 87–97).

11. **Arcanum Journey**

   Newcomers can read about Arcanum without ever learning how its tools compose or feel in use | choose a goal, install a relevant slice, learn one capability per chapter, and probe the real tool | private-parent L0 scaffold with route map, onboarding, preset, persona, boundary lint, chapters 0–1, and one HTML surface | public promotion separate; chapters 2–9, install wiring, capstone run, experiment validation, and promotion remain pending | could turn onboarding into hands-on construction rather than passive documentation | author remaining chapters, wire bootstrap, run learner evidence, then separately approve public promotion | staged skill contract contains an explicit build-state table | educators, technical writers, beginner testers, HTML learning designers | test a chapter with a newcomer or author one bounded chapter/probe pair | safe: “private staged L0 learning-course scaffold”; forbidden: “shipped public Arcanum course with proven learning outcomes” (`projects/arcanum-journey/deliverable/arcanum-journey/SKILL.md`, lines 1–16; `#Flow`, 19–35; `#Status--build-state`, 51–63; `projects/arcanum-journey/CRAFT.md`, lines 1–12, 40–48).

12. **AutoAds**

   Ad creative iteration often turns network metrics into unjustified truth and loses why a variant won | generate a variant, measure outcomes, grade evidence, and let an owner promote or retire the learning | validated project seed with Define/Design/Plan and a proposed Creative Learning Cycle | not executed; no live network integration, spend, model training, or evidence that Ontologize generalizes from grants to ads | could make creative learning auditable and reusable instead of opinion-led | research one network, then build a stubbed L0 thin slice without live spend | refine dispatch passed and artifacts exist, but outputs remain candidates | creative strategists, ad-ops practitioners, measurement researchers, adapter engineers | define one network outcome contract or build/test the no-spend stub loop | safe: “non-executed governed ad-learning-loop design”; forbidden: “system that generates better ads or has proven performance uplift” (`projects/autoads/README.md#Status`, lines 6–12; `#The-loop`, 20–31; `projects/autoads/DEFINE.md#Problem`, lines 13–25; `#Out-of-scope`, 36–39).

13. **Sonar Loop**

   Static analysis, tests, remediation, and task export often lack one repeatable, auditable completion loop | select a quality gate, map the codebase, gather evidence, evaluate, propose remediation, and make an operator-controlled continue/pause/halt/complete decision | extensive docs-first TypeScript quality-orchestration specification, governance rules, capability docs, and user journeys | SPEC is draft; project is docs-first; no implementation-completeness claim | gives teams an explicit model for fallback, evidence, risk acceptance, and completion authority | evaluate the spec, then select and witness a bounded implementation slice | current README explicitly limits claims to the documented solution model | TypeScript maintainers, quality engineers, Sonar practitioners, governance reviewers | challenge one fallback/completion rule or implement a fixture-backed thin slice | safe: “docs-first specification for a governed quality loop”; forbidden: “working product that improves code quality or integrates Sonar/GitHub/Jira end to end” (`projects/sonar-loop/README.md#What-Sonar-Loop-solves`, lines 7–17; `#How-it-works`, 38–48; `#What-you-can-evaluate-now`, 127–135; `docs/features/sonar-loop/SPEC.md`, lines 1–4, 37–94).

14. **Ontologize / CyberAlchemy candidate offer**

   Companies may have dashboards, scattered lessons, and agent work without being able to defend numbers or govern what becomes reusable knowledge | trace one business metric to source events, define its ontology and boundaries, and route learning through owner review | substantial candidate product/engagement design, public-offering draft, research packages, and a narrow founding-pilot shape | no broad cross-vertical proof, committed pricing/contracts/brand, or autonomous management claim; root status and later artifacts are temporally inconsistent | could make one operational metric and learning loop inspectable enough to challenge and improve | run one real non-grant thin-slice pilot and measure the governance layer itself | GoldenQuill is cited as grant-domain reference evidence; generalization is explicitly a hypothesis | operations/data/AI practitioners, ontology designers, BI engineers, pilot partners | bring one mistrusted metric and map its source event, exclusions, owner, and reuse boundary | safe: “candidate scoped pilot for auditable BI and governed learning”; forbidden: “proven cross-industry ontology product, autonomous decision system, or sold engagement” (`projects/ontologize/PRODUCT.md`, lines 1–17, 54–60, 79–90; `PUBLIC-OFFERING.md`, lines 1–9, 56–72, 120–132; `README.md`, lines 1–30).

## Shared 10-second / 30-second / deep-detail grammar

### 10 seconds — recognition and truth

Required fields:

- `felt_problem`: one concrete friction in domain language;
- `recognizable_act`: one thing the visitor can picture doing;
- `project_name`;
- `maturity_label`: working slice / scaffold / candidate / research / specification;
- `one-line limit`.

Decision supported: “Is this about something I care about, and is it real enough for my attention?”

Do not include architecture inventories, internal framework vocabulary, trajectories presented as present capability, or a CTA stronger than “inspect.”

### 30 seconds — distinction and next move

Add:

- `what_exists_now`;
- `why_it_could_matter`;
- `current_proof`;
- `trajectory`, visibly future;
- `who_could_help`;
- one `concrete_contribution`;
- link to canonical detail and evidence.

Decision supported: “Why this project rather than an adjacent one, and could I usefully engage?”

Every preview should contain a different concrete noun/verb pair. If project names can be swapped without rewriting the preview, the copy has flattened them.

### Deep detail — inspectability

Add:

- problem and domain context;
- current artifact map;
- mechanism or workflow;
- proof receipts with dates/status;
- limitations, deferred layers, and open decisions;
- authority/name/publication boundary;
- safe and forbidden claims;
- contribution menu by domain act or skill;
- next witness;
- source selectors;
- related projects, with explicit distinction;
- project-specific contact/interest route only if an owner supplies it.

Decision supported: “Do I trust the claim ceiling, understand the work, and know what bounded help would be valuable?”

## Decision-first alternative

### Entry surface

Present six actions, not fourteen brands:

- Shape expression — writing, music, interface work.
- Understand something difficult — guided translation, X-Ray, Arcanum Journey.
- Test decisions under constraints — Poker Agent Arena, Tower System.
- Turn physical or operational events into evidence — Body War, Ontologize, AutoAds.
- Keep agent work governable — IDE Extension, IDE Ergonomics, UI Prototyping Studio.
- Improve software with auditable evidence — Sonar Loop.

Each action reveals 2–4 projects and immediately shows maturity and contribution type. Visitors may switch to “All projects” at any time. A presenter may jump directly to the same filtered state via URL.

### Why it is genuinely different

The visitor chooses a job/domain act before a project. The primary unit is “what I want to do or help with,” not a card collection. Project identity becomes the answer to a visitor decision rather than the question imposed on them.

### Failure mode

This route can obscure the portfolio’s breadth, misclassify cross-domain projects, and weaken project-name recall. Therefore:

- all projects remain reachable in one action;
- projects may carry multiple act tags;
- presenter mode retains a project index;
- the default decision-first route must be tested against a project-first control with cold-reader retellability and next-choice questions.

## Local tensions and synthesis questions

- Should maturity be one controlled vocabulary across all projects, or project-owned phrases with a small normalized mapping?
- Which root owns public UI Prototyping Studio links?
- Should Body War appear under its container name, product brand, or `TROQAR / Body War` until ownership resolves?
- Does Ontologize appear as the project, CyberAlchemy as the offer, or both with explicit relationship?
- Can the decision-first taxonomy remain understandable to a projected room without a presenter explaining the categories?
- How many contribution types can be normalized without inventing recruitment operations?
- Should private staged work such as Arcanum Journey appear at all on a public showcase, or only in a private/internal mode?

## Explicit exclusions

- Experiment Exchange, admission lifecycle, SLA, expiry, matching automation, or appointment machinery.
- Investor-priority ordering as collaborator-facing hierarchy.
- Generic “AI-powered,” “agentic platform,” “knowledge graph,” “revolutionary,” “autonomous,” or “production-ready” copy unless a specific current source proves the bounded term.
- Private owner paths or private prose on a public Arcanum surface.
- Screenshots as evidence of understanding, usefulness, or recruitment.
- Historical validation receipts represented as checks rerun in this dispatch.
- Final marketing copy.

## Final post-discussion position

No cross-agent discussion has yet occurred, so this is not a converged position. My refined initial position is:

Use a decision-first opening with a readily available project index, then normalize only the factual fields—not voice—across project previews. The minimum trustworthy preview is:

`felt problem → recognizable act → what exists → honest limit → why it matters → one bounded way to help`.

A portfolio-first grid remains a valid secondary and live-navigation surface, but it should not be the only entrance. The decisive synthesis test is not visual elegance; it is whether a cold technical builder and a domain practitioner can each identify one relevant project, accurately retell what exists and what does not, and name a concrete next contribution without presenter coaching.

### Post-Robot-Talk Final Position

# FINAL POSITION — Alexander, Christopher

Dispatch: `2026-07-26-co-op-project-showcase-recruitment-research`  
Lane: `lane_a_explorers`  
Exchange counterpart: Christensen, Clayton  
Status: post-exchange explorer position; not synthesis or approval

## Direct conclusion

The strongest Lane A candidate is:

> **Reversible decision lens → small project set → project-owned truth → separately evidenced welcome → bounded offer.**

The visitor may enter through a domain act, problem, contribution shape, or the complete project index. The decision lens is navigation, not matching. It may narrow attention, but it must never rewrite project truth, imply personal fit, hide the full corpus, or manufacture a recruitment workflow.

The shared schema should govern factual obligations and evidence boundaries. It should not govern the projects’ prose. Recruitment freshness must be an independently maintained overlay: a project can be real without being open to outside help, and a concrete ask can be displayed only when its owner, receiving path, expected artifact, and freshness are bound.

## Agreements after exchange

1. **A fourteen-card grid is insufficient as the only entrance.** It serves returning visitors, live overview, stable deep links, and corpus completeness, but makes cold visitors interpret internal names before relevance.

2. **Decision-first is an orientation layer, not a product matcher.** A visitor-selected lens should reveal a small, explicitly non-exhaustive project set. “Browse all projects” and reset must remain visible.

3. **The sequence is asymmetrical.** Decision cues may be shared; explanation must become project-specific; recruitment must become progressively commitment-aware:

   `decision cue → candidate projects → project truth → contribution inspection → non-binding offer → human clarification → commitment outside the showcase`

4. **Project proof and welcome proof are different.** A runnable artifact, repository, research tower, or verification receipt supports what exists. It does not establish that help is wanted, a reviewer is available, outsiders may contribute, or anyone will respond.

5. **Concrete asks outperform generic welcome only when current and owner-backed.** “Designers welcome” transfers task invention to the visitor. “Test whether this keyboard path remains understandable at mobile width” is better only if the project currently wants that artifact and has somewhere to receive it.

6. **Non-code work must use native domain verbs.** Writers revise or retell; musicians annotate, perform, or listen; designers inspect decisions and interaction states; researchers compare claims or protocols; developers implement or reproduce bounded behavior. “Non-technical help” is not an adequate contribution description.

7. **Interest, contact, and commitment must not collapse into one CTA.** The page may support browsing, inspecting, saving a deep link, and making a non-binding offer. Scope agreement and commitment require human confirmation beyond the showcase.

8. **One factual source can support self-guided and live modes.** Presentation may change sequence, density, and controls, but not maturity, proof, limit, ask status, or claim ceiling.

## Remaining disagreements

### 1. Shared field schema versus recruitment freshness

I retain a stronger commitment than Christensen to a shared factual schema. Without required fields—felt problem, recognizable act, current artifact, proof, limit, trajectory, authority boundary, and safe/forbidden claim—the page will drift into incomparable marketing fragments.

Christensen is right that a shared `contribution` field becomes dangerous if treated as equally stable. Current asks decay faster than project truth and create an operational expectation.

Resolution: split the data model:

- **Project truth record:** owner/source, project name, aliases, felt problem, recognizable act, current artifact, proof, honest limit, trajectory, public boundary, safe claim, forbidden claim, last verified.
- **Welcome record:** status (`unbound`, `inquiry-only`, `open-ask`, `paused`), owner/channel, wanted act, expected artifact, prerequisites, size/uncertainty, review path, response expectation if authorized, expiry/recheck date.

No welcome record may be inferred from a roadmap gap, deferred layer, or missing witness. Those are contribution candidates until an owner binds them.

### 2. Decision-act taxonomy versus project-owned language

I initially proposed six action categories as the entry surface. Christensen’s warning is material: role or act taxonomies can flatten cross-domain projects and imply a match stronger than the evidence.

I still recommend a small decision-act taxonomy, but only as editorial navigation. Tags must be traceable to exact project language, may overlap, and must never replace the project opening. A visitor selecting “shape expression” should encounter “edit one shared musical specification” for Agentic Music Studio and “shape meaningful text from author intent” for Whisper—not two variants of “build creative AI.”

The taxonomy is successful only if removing the filter leaves each preview unmistakably its own project.

### 3. Proof-of-project versus proof-of-welcome

There is no substantive disagreement after exchange, but there is an unresolved implementation consequence. The current corpus is much stronger on proof-of-project than proof-of-welcome. Therefore most projects cannot yet support “Help with this” as a factual CTA.

A proof link, current-state sentence, and honest limit belong in every preview. A contribution action appears only where welcome evidence exists. Otherwise use one of:

- “Contribution path not yet bound.”
- “Inspect the project and its open questions.”
- “Make a non-binding inquiry,” only if a real receiving channel exists.

Absence of a CTA is more truthful than an unanswered invitation.

### 4. Public truth limits versus concrete CTAs

My initial report derived contributions from missing witnesses and deferred work. That is useful research substrate but too strong for public recruitment. A public CTA needs more than a plausible task: it needs authorization, a public-safe artifact boundary, and a recipient.

Private evidence may establish an internal claim ceiling without being publishable. If the public visitor cannot inspect the supporting proof, the page must either point to an authorized public projection or weaken the claim. Private paths, owner data, internal framework prose, and staged public intentions must not leak through the CTA.

## Changes from my initial position

1. I no longer recommend that every project preview expose “one honest contribution” unconditionally. Every preview should expose a **contribution status**; only owner-bound projects expose an actionable ask.

2. I separate `current proof` from `proof of welcome`. My initial truth-record grammar combined “who could help” and “concrete contribution” with project facts too readily.

3. I demote my six-action taxonomy from proposed primary ontology to a testable editorial lens. It must be reversible, overlapping, source-traceable, and paired with “Browse all.”

4. I add freshness and receiving-path obligations to any public ask. Specificity without upkeep can be more damaging than no ask.

5. I distinguish “who could plausibly help” from “who is currently invited.” The former is an inference for synthesis; the latter is a public fact requiring owner evidence.

6. I retain the shared 10-second/30-second/deep-detail grammar, but move recruitment fields into a conditional welcome layer rather than treating them as permanent project content.

## Explicit tension synthesis

The central tension is:

> A stable shared schema makes fourteen projects comparable, while effective recruitment depends on fresh, project-specific invitations that cannot be standardized or inferred safely.

The synthesis is a **two-clock contract**:

- The **truth clock** changes when project status, proof, limits, name, authority, or public boundary changes.
- The **welcome clock** changes when an owner opens, changes, pauses, receives, or closes an ask.

The browser joins these clocks at render time but never conflates them. A project card can remain accurate when its welcome record expires: the ask disappears or becomes `paused`, while the project truth remains. Presentation mode reads the same joined state. This preserves comparability without presenting stale recruitment as truth.

## Final content grammar

### 10 seconds: recognition and claim ceiling

- project-owned felt problem;
- recognizable domain act;
- project name and necessary alias;
- maturity label;
- one honest limit;
- optional welcome status, never an unverified ask.

Decision: “Does this matter to me, and what kind of reality am I looking at?”

### 30 seconds: distinction and trust

- what exists now;
- current proof and date/status;
- why it could matter;
- trajectory explicitly marked future;
- why the selected lens surfaced it;
- welcome state:
  - owner-backed open ask with smallest useful act, or
  - inquiry-only with named route, or
  - contribution path not yet bound.

Decision: “Why this project, what can I trust, and is approach currently possible?”

### Deep detail: inspectability and bounded approach

- project-owned story, mechanism, artifacts, and vocabulary;
- proof receipts and limitations;
- authority/name/publication conflicts;
- present versus proposed state;
- safe and forbidden claims;
- related projects and meaningful distinctions;
- if open: wanted act, expected artifact, prerequisites, scope/uncertainty, receiver, review path, visibility/privacy, freshness, and response expectation if authorized;
- if not open: no simulated task board or generic “join” language.

Decision: “Can I accurately retell the project and make a socially and technically safe next move?”

## Final recommendation and boundary

Build and test two reversible openings over the same fourteen truth records:

1. **Decision-lens opening:** choose a domain/practice, problem, contribution act, or current open ask; receive 1–3 non-exclusive project previews.
2. **Project-index opening:** browse all projects directly.

Both lead to identical project details and welcome records. The live presenter may select a lens and traverse contrasting projects, while the index remains available for non-linear jumps.

Acceptance should ask a cold technical builder and a domain practitioner to:

- identify one relevant project;
- state what exists now;
- state one important limit;
- distinguish project proof from welcome evidence;
- choose a next action without assuming acceptance or automation.

Browser behavior can show that filters, deep links, Back, reset, and CTA states work. It cannot prove comprehension, welcome, responsiveness, contribution quality, or recruitment success.

Do not build matching automation, applications, appointments, SLAs, admission states, or an Experiment Exchange. Do not publish a concrete CTA from a plausible gap alone. Do not let a recruitment lens overwrite project-owned language. Do not expose private proof or imply public contribution permission from repository visibility.

## Project-record corrections

These corrections apply to my initial compact records:

1. **All fourteen records:** replace `who could help` with two fields:

   - `plausible contribution roles` — labeled inference;
   - `welcome status / owner-backed ask` — fact, otherwise `unbound`.

2. **Whisper:** “test a transport audition” is a plausible contribution candidate, not a verified public ask. Preserve the proven/unproven transport distinction.

3. **User / Translate / Guide:** requesting a real explanation case is plausible research work, not evidence that outside cases are currently accepted.

4. **Agentic Music Studio:** implementing or testing an interface is a next-witness proposal. The research tower is local-only and does not establish an open contributor route.

5. **Poker Agent Arena:** authoring an agent or Leduc fixture is plausible from the runnable protocol and deferred work, but no inspected source binds a public contribution channel. Keep welcome `unbound` unless owner-confirmed.

6. **Body War / TROQAR:** retain `TROQAR / Body War` until naming authority resolves. The app-backed pilot supersedes the root README’s “no prototype in the first pass” as current artifact evidence, but neither authorizes public recruitment or live Strava participation.

7. **UI Prototyping Studio:** do not publish a canonical link until the competing `arcanum/projects/` and `projects/` roots are owner-resolved. A real HTML variant or accessibility test is a contribution candidate, not an open ask.

8. **Tower System:** the witness unit is the next proof target, not a public invitation. Owned parts and research closure do not prove the central assembly or welcome.

9. **IDE Extension:** tests and bounded UI increments are plausible work shapes. Repository visibility and a pilot-ready status do not establish external mutation permission or reviewer capacity.

10. **IDE Ergonomics:** real conversation snippets are fixture candidates, but their privacy, receiver, and adjudication owner must be bound before soliciting them.

11. **X-Ray:** a source-marked live example is required for promotion evidence, but that requirement alone does not mean public contributions are being accepted.

12. **Arcanum Journey:** because it is staged in the private parent and public promotion is separate, omit it from a public showcase unless an authorized public-safe projection exists. Do not solicit chapter work publicly from the private path.

13. **AutoAds:** network-contract and stub-loop tasks remain proposed next routes. Do not imply access to ad accounts, spend, credentials, data, or a public contribution lane.

14. **Sonar Loop:** the docs-first spec can be inspected publicly only where its location is authorized. “Implement a thin slice” remains a proposal, not an owner-backed ask.

15. **Ontologize / CyberAlchemy:** preserve the temporal/status conflict between the older root README and later product/offering artifacts. Use `Ontologize` for the project and `CyberAlchemy candidate offer` only with the working-name boundary. A “mistrusted metric” conversation is already phrased as a founding-pilot invitation in `PUBLIC-OFFERING.md`, but the showcase still needs current owner confirmation, a public contact route, and authorized response expectations before rendering it as an active CTA.

## Remaining evidence needs

- owner confirmation for every public name, root, and alias;
- a public-safe proof target for private or staged projects;
- one current welcome record per project, including explicit `unbound` where appropriate;
- freshness/expiry ownership for open asks;
- authorized contact routes and response expectations;
- cold-reader comparison of decision-lens versus project-index entry;
- separate human evidence for comprehension, sense of welcome, and contribution decision clarity.

This final position is a bounded design recommendation from repository truth plus Christensen’s recruitment evidence. It is not proof that the decision lens recruits better, that any project is welcoming in practice, or that any inferred contribution is authorized.

## Agent 4 — Christensen, Clayton

### Initial Return

# Initial Robot-Talk Report — Christensen, Clayton

Dispatch: `2026-07-26-co-op-project-showcase-recruitment-research`  
Lane: A — recruitment decision  
Status: explorer return; no files written; no recruitment outcome is claimed

## Initial position

A project grid is a catalog answer to a decision problem. A visitor who does not already know the fourteen project names is more likely to begin with one of four questions:

1. What kind of problem or domain act interests me?
2. What can someone with my abilities do here?
3. What help is actually needed now?
4. Is this work real, active, bounded, and safe to approach?

My initial hypothesis was therefore: lead with a decision-first navigator, let it produce a short project set, then let project detail establish explanation, evidence, limits, and the bounded ask.

## Facts from current authoritative sources

- Mozilla’s contribution page divides opportunities by recognizable contribution modes—translation, code, support, and broader community participation—and labels technical/non-technical and individual/event forms. This is evidence that role or act can be a useful entry route without requiring prior project-name knowledge. [Mozilla: Volunteer Opportunities](https://www.mozilla.org/en-US/contribute/)

- Creative Commons similarly says people can enter according to skills and interests, then names acts such as translating, hosting training, supporting open-source software, or moderating community chat. Its open-source issue system adds skill, goal, aspect, and contributor-friendliness labels so people can find work matching experience and skill. [Creative Commons Global Community](https://creativecommons.org/community/), [Creative Commons Repository Labels](https://opensource.creativecommons.org/contributing-code/repo-labels/)

- GitHub treats `CONTRIBUTING.md`, contact paths, issue templates, and `good first issue` labels as distinct aids: the README introduces the project, contribution guidance explains how to participate, and labels surface approachable work. This supports separating “understand it,” “find a possible task,” and “learn how to submit.” [GitHub contribution guidelines](https://docs.github.com/en/enterprise-cloud%40latest/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors), [GitHub helpful-contribution labels](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/encouraging-helpful-contributions-to-your-project-with-labels), [GitHub communicating repository information](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/planning-and-tracking-work-for-your-team-or-project)

- Open Source Guides describes a contributor funnel from user to contributor to maintainer and recommends reducing friction incrementally with a friendly introduction, explicit contribution guidance, current issues, beginner-sized work, documentation, recognition, and welcoming conduct. It does not support collapsing initial curiosity into commitment. [Open Source Guides: Building Welcoming Communities](https://opensource.guide/building-community/)

- Outreachy gives projects a stronger recruitment mechanism: project detail contains a task list; applicants contact mentors; a small contribution lets both sides test fit before selection. Outreachy also reports that a first contribution commonly takes 5–10 days. This is evidence for progressive commitment, but its formal application machinery is inappropriate to invent for the Co-Op page. [Outreachy Applicant Guide](https://www.outreachy.org/docs/applicant/), [Outreachy Community Guide](https://www.outreachy.org/docs/community/)

- CHAOSS treats responsiveness as relevant to newcomer recruitment and retention, recommends publishing response expectations, and warns that intake templates can deter newcomers if they demand too much information. This supports showing an honest contact expectation where one exists, not promising one where it does not. [CHAOSS Responsiveness Guide](https://chaoss.community/practitioner-guide-responsiveness/)

- The All Contributors specification explicitly recognizes non-code work, including audio, content, design, documentation, research, testing, tutorials, user testing, and talks. That is authoritative evidence against representing contribution as synonymous with development. [All Contributors contribution types](https://allcontributors.org/en/emoji-key/)

## Key findings

### 1. No single entry route serves both discovery and recruitment

**Fact:** Mozilla and Creative Commons expose contribution acts and skills; GitHub and Outreachy eventually route people to specific projects or tasks.

**Inference:** The useful unit is not “project-first versus decision-first” as a permanent choice. It is:

> decision cue → small candidate set → project truth → bounded ask

A decision-first landing should narrow attention, not replace project explanation.

### 2. “I am interested” is not “contact me,” and neither is commitment

**Fact:** Open Source Guides describes a funnel; Outreachy inserts contact and a trial contribution before selection.

**Inference:** A single “Join” button falsely compresses multiple decisions and obscures what happens next.

**Proposal:** Use a CTA ladder with visibly different consequences.

### 3. Concrete, currently bounded work is a stronger recruitment signal than generic enthusiasm

**Fact:** GitHub surfaces `good first issue`; Outreachy requires task lists; Creative Commons labels work by skill and friendliness.

**Inference:** “We need designers” is weaker than “Help test whether this browser interaction is understandable on mobile,” provided that the latter is verified as an owner-backed current ask.

**Proposal:** Every recruitable project preview should expose one honest contribution shape, the expected artifact, necessary context, and whom or what receives the offer. If those are unknown, show “ask not yet bound,” not a volunteer CTA.

### 4. Trust is operational as well as explanatory

**Fact:** GitHub separates README, contribution rules, templates, and code of conduct; CHAOSS identifies responsiveness and expectation-setting as newcomer concerns.

**Inference:** A demo or repository link proves that an artifact exists, but not that an outsider will be supported, that a proposed contribution is wanted, or that a reply will arrive.

**Proposal:** Keep proof-of-project and proof-of-welcome as separate fields.

### 5. Non-code contribution must be expressed in domain acts

**Fact:** Mozilla, Creative Commons, and All Contributors all name non-code forms of work.

**Inference:** A generic “non-technical contributors welcome” badge does not tell a writer, musician, designer, researcher, or listener what useful act they could perform.

**Proposal:** Describe contribution in verbs native to each domain: revise a passage, annotate a musical transition, test a screen-reader path, compare research claims, retell a project after hearing it, or implement a bounded interface behavior—only where the project owner has actually requested that act.

## Entry-route comparison

| Entry route | Helps answer | Main strength | Main failure |
|---|---|---|---|
| Project-first | “Which named project?” | Fast for returning or already-oriented visitors; good for presentation scan | Forces newcomers to interpret fourteen names before knowing relevance |
| Problem-first | “Which difficulty do I care about?” | Connects to felt need and cross-domain motivation | Can flatten distinct projects into generic problem statements |
| Role/skill-first | “Where can I be useful?” | Strong recruitment navigation; validates non-code work | Reduces people to occupational labels and can hide curiosity or learning |
| Domain-first | “Do I care about music, writing, interfaces, research…?” | Uses recognizable practices and vocabulary | Cross-domain projects become awkward; domain affinity does not establish task fit |
| Ask-first | “What work needs help now?” | Highest action clarity when asks are current and bounded | Weak explanation; stale asks destroy trust; poor live-presentation opening |
| Hybrid decision-first | “What draws me, and what can I do next?” | Preserves multiple motives before narrowing to projects | Requires disciplined tagging and may imply matching automation if overdesigned |

## Genuine decision-first alternative

Do not open with fourteen equal cards. Open with the visitor decision:

> What would make this worth following or helping?

Offer four plain-language routes, not a matching questionnaire:

- I care about a domain or practice.
- I want to help with a particular kind of work.
- Show me problems being explored.
- Show me concrete asks that are open now.

Each selection reveals a short, explicitly non-exhaustive set of project previews. A preview contains:

1. recognizable act or felt problem;
2. what exists now;
3. one proof link or observed artifact;
4. one honest limit;
5. why this route matched;
6. smallest available next step.

Always retain “Browse all projects,” deep links, and a resettable view. Filtering is navigation, not automated matching. The page must not claim personal fit, acceptance, or an operational workflow.

For live use, the presenter can choose a route as an audience lens, then traverse three contrasting projects. The full project index remains available but is not the opening burden.

## Decision journey

| Moment | Visitor decision | Minimum information required |
|---|---|---|
| Arrival | “Is this world relevant to me?” | One concrete portfolio-level purpose; who it is for; no framework jargon |
| Route choice | “How do I want to orient?” | Domain, problem, contribution act, or all-project option; clear that routes overlap |
| Candidate scan | “Which 1–3 projects deserve attention?” | Felt problem, domain act, present state, one limit, one contribution signal |
| Detail opening | “Is this real and understandable?” | Current artifact/proof, status/date, owner-bounded claims, distinct project language |
| Contribution inspection | “Could I usefully help?” | Specific need, expected output, prerequisite, size/uncertainty, contact path |
| Interest action | “Do I want to remember or follow this?” | Low-consequence action; no implied obligation |
| Contact | “Am I willing to identify myself and start a conversation?” | Recipient, information requested, privacy/visibility, response expectation if known |
| Commitment | “Am I agreeing to work?” | Human-confirmed scope, availability, ownership, and next step outside the showcase’s claims |

## What each visitor must know

| Visitor | Before opening detail | Before volunteering |
|---|---|---|
| Writer | The text, narrative, or comprehension act at stake | Exact material, editorial authority, desired form, review owner |
| Musician | The musical act or listening problem, not merely “AI music” | Required musical context/tools, expected recording/annotation/feedback, usage terms |
| Designer | The user decision or interaction being tested | Target state/surface, constraints, evidence expected, design authority |
| Developer | Current implementation surface and technical boundary | Reproduction/setup, bounded issue, acceptance check, maintainer/contact |
| Researcher | Question, evidence state, and claim ceiling | Corpus/protocol, expected analysis, citation/data rules, adjudication owner |
| Curious listener | Why observing or reacting matters | Whether feedback is wanted, prompt/duration, recording/privacy, how it will be used |

Before any person volunteers, all need to know: what is real now, what is proposed, what help is actually open, what the smallest useful act is, and what happens after contact.

## CTA ladder

1. **Notice:** Browse all / choose another lens.
2. **Understand:** Open project detail / inspect evidence and limits.
3. **Stay interested:** Save or copy a deep link; follow a public update channel only if one exists.
4. **Offer:** “I may be able to help with…” using a short, non-binding contact path.
5. **Clarify:** Speak with a named owner or channel about fit and scope.
6. **Commit:** Agree to a bounded task only after human confirmation.

The showcase may implement levels 1–4 as navigation/contact affordances. Levels 5–6 are lifecycle states it must describe cautiously, not pretend to automate.

## Trust-signal matrix

| Signal | What it supports | What it does not prove |
|---|---|---|
| Dated runnable artifact or browser witness | Something observable exists | Production readiness or recruitment readiness |
| Repository/source link | Inspectable implementation exists | Approachability, current activity, or public contribution permission |
| Current-state sentence | Present scope is named | Accuracy unless tied to owner/source evidence |
| Honest limit | Claim ceiling is visible | That the limitation will be resolved |
| Specific owner-backed ask | Help is presently wanted | Contributor acceptance or successful completion |
| Expected artifact/check | The contribution can be understood | Review capacity or response time |
| Named contact/channel | There is a route to inquire | Guaranteed response |
| Published response expectation | Visitor can calibrate waiting | Actual responsiveness until observed |
| Contribution guide / conduct rules | Participation norms exist | A welcoming lived experience |
| Named prior contributors and contribution types | Non-code work is recognized | Equal authority or future opportunity |
| “Updated on” date | Staleness is detectable | Freshness by itself |

## Abandonment risks

- Fourteen equal project cards create interpretation debt before relevance.
- A role picker excludes people who do not identify with a professional label.
- Too many filtering questions feel like an application or fake matching engine.
- “Join us” implies commitment before the visitor understands the work.
- Generic “all skills welcome” language transfers the burden of inventing useful work to the newcomer.
- A repository link presented as the only next step privileges developers.
- Stale asks or dead “good first” tasks are worse than showing no open ask.
- Missing owner, review path, or reply expectation makes volunteering socially risky.
- Long intake forms deter tentative offers; CHAOSS explicitly warns against over-demanding templates.
- Hype about finished capabilities undermines trust when detail reveals prototypes or proposals.
- Private/unavailable proof behind a public claim creates a verification dead end.
- A filter that hides “Browse all” can make the corpus feel manipulated or incomplete.

## Recruitment-success / presentation-failure counterexample

Outreachy’s project-selection pattern can succeed at recruitment because it exposes detailed task lists, mentor contact, qualification steps, deadlines, contribution recording, and a real commitment progression. Those mechanics help applicants and mentors test fit.

The same pattern would damage the Co-Op live presentation: eligibility, schedules, applications, and task administration would dominate the explanation of what the projects are and why they matter. It would turn a showcase into an intake funnel and reproduce the explicitly excluded exchange/workflow design. Borrow the small-trial and mentor/contact clarity; block the application machinery. [Outreachy Applicant Guide](https://www.outreachy.org/docs/applicant/)

A simpler ask-first board has the same tension: it can recruit efficiently from already-motivated specialists while making a poor opening for listeners who first need meaning, differentiation, and evidence.

## Gaps and inconsistencies

- The sources show deployed patterns, not a controlled comparison proving that one entry route recruits best for this audience.
- No current evidence establishes how writers, musicians, designers, developers, researchers, and curious listeners interpret the Co-Op’s actual project language.
- A source-backed list of currently open, owner-approved asks for the fourteen projects is not yet available in this lane.
- Contact owners, response expectations, contribution visibility, licensing, and review authority remain locally unresolved.
- Role and skill taxonomies risk flattening project-specific acts; Alexander’s project-truth lane must constrain them.
- Self-guided recruitment clarity and projected explanation may require different density while sharing facts. This lane does not settle that presentation contract.
- Browser clicks can show route use, not comprehension, willingness, trust, or recruitment success.

## Local tensions

- **Discoverability vs. integrity:** tags help navigation but can imply a stronger match than the evidence warrants.
- **Specific asks vs. freshness:** specificity recruits, but it creates maintenance obligations.
- **Low-friction contact vs. owner capacity:** easy outreach can produce unanswered offers.
- **Role recognition vs. whole-person curiosity:** “writer” and “developer” are useful shortcuts but poor identities.
- **Recruitment efficiency vs. explanation:** ask-first routes optimize action while weakening the portfolio story.
- **One truth source vs. two use modes:** the facts can be shared, but projected and self-guided ordering need not be identical.
- **Welcoming language vs. bounded acceptance:** invitation must not imply that every proposal will be accepted.

## Synthesis questions

1. Which project facts are stable enough to tag by problem, domain act, skill, and current ask?
2. Who owns each public contribution ask, and how is staleness detected?
3. Can every recommended route preserve a visible “all projects” escape and stable deep links?
4. What is the smallest contact action owners can genuinely support?
5. Which projects have no current recruitable ask and should say so plainly?
6. How will the live mode demonstrate the decision-first route without polling or redesigning the meeting?
7. What cold-reader test distinguishes “I liked it” from “I can name one relevant project, its real state, and a plausible next step”?
8. Should “curious listener” be an explicit route, or should observation/feedback appear across projects?
9. Which labels are project-owned facts, and which are merely editorial interpretations?
10. What response expectations can be published without inventing an SLA?

## Final post-research position

The decision-first alternative survives, but only as a reversible orientation layer—not as the entire information architecture and not as a matching product.

My recommended comparison candidate for Lane Z is:

> **Decision lens → 1–3 project previews → project truth → bounded contribution ladder**, with “Browse all projects” always available.

Project-first remains necessary for returning visitors, live overview, deep linking, and corpus completeness. Ask-first is powerful only after the artifact has established meaning and only where an owner-backed current ask exists. The strongest design is therefore asymmetrical: decision-first at entry for an uninitiated visitor, project-specific in explanation, and progressively commitment-aware in recruitment.

This is an evidence-backed design inference, not proof of improved recruitment. It needs project-truth reconciliation, owner confirmation of asks, browser observation, cold-reader retellability, and actual contribution-decision testing before promotion.

### Post-Robot-Talk Final Position

# FINAL POSITION — Christensen, Clayton

Dispatch: `2026-07-26-co-op-project-showcase-recruitment-research`  
Lane: A — recruitment decision after exchange with Alexander  
Status: converged where stated; unresolved boundaries remain explicit

## Direct conclusion

Use a decision-first orientation layer over project-owned truth records, but do not turn every missing witness or possible contribution into a recruitment CTA.

The durable sequence is:

> visitor decision → small candidate set → project-owned explanation → proof and limit → contribution state

The last stage has three possible states, not one:

1. **No public ask:** the project can be understood or followed, but no contribution invitation is authorized.
2. **Contribution possibility:** the detail can name a useful kind of work or next witness, but contact and commitment are not yet offered.
3. **Open bounded ask:** an owner has confirmed that help is wanted now, named the expected artifact and recipient, and supplied a public contact route.

This preserves Alexander’s repository-truth discipline while retaining a genuine recruitment journey. It also prevents a stable project schema from becoming a stale jobs board.

## Agreements

### 1. A project grid is necessary but insufficient

We agree that fourteen equally weighted names impose decoding work on a cold visitor. A complete project index remains necessary for corpus completeness, returning visitors, deep links, and non-linear live navigation, but it should not be the only entrance.

The alternative is genuinely decision-first: the visitor first chooses a recognizable act, problem, domain, or contribution interest; the surface then reveals a small set of projects. “All projects” must remain available in one action.

### 2. Shared fields should normalize questions, not voice

We agree on a stable truth grammar:

`felt problem → recognizable act → project name → maturity → what exists → proof → honest limit → why it may matter`

At deeper levels it can add trajectory, next witness, authority boundary, related projects, and safe/forbidden claims.

The field names may be shared; the prose and nouns must remain project-owned. Poker cannot sound like music, music cannot sound like governed IDE work, and a private course scaffold cannot sound like a shipped public capability. If project names can be exchanged without rewriting the preview, the schema has flattened the work.

### 3. Proof and limit must travel together

We agree that maturity is visible at preview depth, not hidden behind detail. “Runnable slice,” “scaffold,” “candidate,” “research,” and “docs-first specification” must not collapse into a uniform portfolio voice.

Every proof signal needs its corresponding limit. A repository or receipt supports the existence of an artifact; it does not prove public availability, production readiness, newcomer support, recruitment readiness, or a current owner-backed ask.

### 4. Decision-first navigation is not matching

We agree that act and skill tags are reversible editorial navigation. They do not assess personal fit, assign people to projects, admit contributors, reserve work, or predict successful collaboration.

Stable URLs, Back behavior, resettable filters, and an always-visible project index keep the decision layer inspectable rather than magical.

### 5. Interest, contact, and commitment remain distinct

We agree that a single “Join” control is unsound. Understanding a project, expressing tentative interest, contacting an owner, and committing to bounded work have different consequences and proof requirements.

The showcase may help a visitor notice, understand, save, follow, or make a tentative offer. It must not present human clarification and commitment as automated showcase states.

## Remaining disagreements

### 1. Shared field schema versus recruitment freshness

Alexander treats `who_could_help` and `concrete_contribution` as useful 30-second fields across the corpus. I accept them only if their epistemic status is visible.

A repository-derived missing witness can support:

> “A useful next test would be…”

It does not automatically support:

> “We are recruiting someone to do this now.”

The latter requires a current owner, an “updated on” date or equivalent freshness signal, a recipient, and a public route. Without those, the field must be presented as a contribution possibility or next witness, not an open ask.

The shared schema is therefore two-layered:

- **durable truth fields:** problem, act, current artifact, maturity, proof, limit, trajectory, next witness;
- **volatile recruitment fields:** open/closed/unbound ask state, owner, expected artifact, prerequisites, contact route, response expectation if known, last confirmation.

Volatile fields must be allowed to disappear or degrade to “no public ask.” Their absence must not make the project explanation incomplete.

### 2. Decision-act taxonomy versus project-owned language

Alexander’s six action groups are useful as a test fixture, but I do not accept them as canonical categories yet. Labels such as “Shape expression” and “Keep agent work governable” are editorial syntheses, not project-owned language, and may require presenter explanation.

The act taxonomy should be derived from the project truth records and tested with cold readers. It may group projects, but each result must immediately say why it matched using the project’s own concrete verb and object.

I recommend a deliberately shallow taxonomy:

- what I want to make or practice;
- what I want to understand or test;
- what kind of help I can offer;
- what help is open now;
- all projects.

The next screen can expose project-specific acts such as shape a passage, edit musical structure, inspect a replay, submit a run, annotate a variant, challenge a metric, or test an approval boundary. The broad taxonomy orients; it must not become the public definition of the projects.

### 3. Proof-of-project versus proof-of-welcome

Alexander correctly inventories project proof, but proof-of-project and proof-of-welcome remain independent.

| Evidence | Supports | Does not support |
| --- | --- | --- |
| Runnable artifact, receipt, source, or current design | The project has a bounded present state | That outside help is wanted |
| Honest maturity and limit | The claim ceiling is inspectable | That an owner can support a newcomer |
| Named next witness | Valuable future work is identifiable | That it is available for volunteering |
| Owner-confirmed ask | Help is wanted now | That every offer will be accepted |
| Contribution guide, contact, conduct rules | A participation route is described | Actual responsiveness or welcome |
| Published response expectation | Waiting can be calibrated | A guaranteed response |
| Observed timely, useful replies | Some operational welcome exists | Future recruitment success |

The page should never borrow trust from the first column to imply the second. A well-tested project with no supported contact path is not recruitment-ready. Conversely, a warm invitation cannot inflate an unwitnessed project into a working product.

### 4. Public truth limits versus concrete CTAs

Alexander shows that many projects have possible bounded contributions, but several also have unresolved names, roots, public/private status, or current authority. A concrete CTA is unsafe when its supporting detail cannot be published or its recipient is not bound.

Accordingly:

- private staged work may appear only in an authorized private/internal surface;
- public Arcanum links must not disclose private paths or imply promotion;
- unresolved canonical roots must block a public contribution link, even if local material suggests useful work;
- a CTA must not point a visitor toward evidence they cannot inspect;
- a future trajectory must not be rewritten as an available task;
- “contact us” is not a substitute for a recipient and consequence.

The correct fallback is not vague enthusiasm. It is an honest non-recruitment state: “Inspect the project,” “Follow this question,” or “No public contribution route is currently bound.”

## Changes from my initial position

1. I no longer recommend that every recruitable-looking preview expose a contribution shape at equal prominence. Every preview may expose a **next witness**, but only owner-confirmed projects expose an **open ask**.
2. I now separate stable content records from volatile recruitment records. Freshness is a property of the ask, not of the whole project card.
3. I narrow the decision taxonomy. Alexander’s corpus proves that project-specific acts are strong; it does not prove that six editorial group names are understandable without coaching.
4. I strengthen project-first navigation as a coequal escape and live index. Decision-first is the cold-visitor entrance, not the sole architecture.
5. I add a three-state contribution model—no public ask, contribution possibility, open bounded ask—so that public truth can remain useful without manufacturing recruitment.
6. I treat public/private authority and canonical link ownership as CTA gates, not merely copy-review concerns.

## Explicit tension synthesis

The central tension is:

> Recruitment needs a fresh, concrete invitation; trustworthy explanation needs stable, source-bounded truth.

Trying to satisfy both with one permanent `concrete_contribution` sentence fails in opposite directions. If the sentence is stable, it becomes generic and weak. If it is concrete, it can quickly become stale or outrun owner capacity.

The synthesis is not compromise copy. It is a structural separation:

> stable project truth record + separately owned volatile ask record

The truth record answers, “What is this, what exists, and what remains unproven?” The ask record answers, “Is help wanted now, for what artifact, by whom, through which public route, and when was that confirmed?” The interface may compose them, but authority and freshness remain separate.

This also resolves the presentation tension. Live projection can reliably use stable truth and selected project acts. Recruitment details appear only when relevant and confirmed; they do not dominate the shared explanation or turn the meeting into an intake workflow.

## Final recommendation

Build the research substrate around two joined but independent records.

### Project truth record

- project-owned name and public-safe route;
- felt problem;
- recognizable domain act;
- maturity;
- what exists now;
- dated or status-bounded proof;
- paired honest limit;
- why it may matter;
- trajectory or next witness, visibly future;
- safe and forbidden claims;
- authority/publication boundary.

### Recruitment ask record

- state: `none`, `possibility`, or `open`;
- project relationship;
- project-owned contribution verb and object;
- expected artifact or observable outcome;
- prerequisites and approximate size only if owner-confirmed;
- recipient/owner;
- public contact route;
- response expectation only if actually supportable;
- last-confirmed date and stale behavior;
- explicit statement that contact is not commitment.

The entry surface should offer a reversible decision lens, return 1–3 candidate projects, explain why each matched, and preserve “All projects.” The project detail then presents truth before invitation. A CTA ladder may progress from inspect, save/follow, tentative offer, contact, and human-confirmed commitment, but the showcase must not invent the latter stages.

## Final boundary

This lane supports a decision-first comparison candidate; it does not establish that decision-first recruits better than project-first. It supports concrete invitations only where public authority, owner, freshness, recipient, and expected contribution are bound. It does not authorize matching automation, application machinery, SLAs, contribution acceptance, public promotion, or recruitment-success claims.

The decisive validation is dual:

1. a cold technical builder and a domain practitioner can each find one relevant project and accurately retell what exists and what does not; and
2. when an open ask is shown, each can distinguish interest, contact, and commitment and can name the bounded next action without presenter coaching.

If either test fails, the design is not recruitment-ready, regardless of click-through behavior or visual polish.

