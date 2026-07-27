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
