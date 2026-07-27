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
