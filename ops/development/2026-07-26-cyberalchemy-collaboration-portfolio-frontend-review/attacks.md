# Frontend Review Attacks

Dispatch:
`2026-07-26-cyberalchemy-collaboration-portfolio-frontend-review`

This file preserves the registered attackers' initial and final robot-talk
positions verbatim. Verifier returns are appended after the synthesis gate.
The Inventory packet is discovery context only; the cited current source and
live behavior are review evidence.

## Peirce, Charles Sanders — Initial Position

INITIAL POSITION — Peirce (product/conversion attacker)

Live grounding: `https://cyberalchemize.com/` returned HTTP 200 and its HTML SHA-256 exactly matches `projects/co-op-engine/index.html` (`1db379…9486`). Playwright visual/mobile execution was attempted but the installed wrapper could not launch because Chrome is absent; mobile findings below are source-backed risks, not visual-pass claims.

Candidate findings

1. **BLOCKER — Cold visitor cannot identify CyberAlchemy.** Exhaustive current-source search has no `CyberAlchemy`/about/team copy; instead the browser title is “Co-Op Engine” (`index.html:8`), the masthead is `CO—OP / 14` with aria-label “Co-Op Engine home” (`#top .brand`, 1371–1372), and the hero defines only the meeting (`.hero__meeting`, 1392–1399). Domain recognition is not organization comprehension. **Fix:** replace the opening identity with a concise CyberAlchemy name + what-it-is sentence before project/meeting framing.

2. **BLOCKER — Contribution journey is a dead end; neither fixed contact destination exists.** All actionable project CTAs are internal `#join` anchors (first/last: `.project-offer`, 1541 and 2100); `#join` only copies a prompt (2153–2165), and the footer ends without contact (2194–2196). Exhaustive source/live search found no `mailto:`, `hello@`, LinkedIn, email, or contact link. **Fix:** add visible `mailto:hello@cyberalchemize.com` and `https://www.linkedin.com/company/cyberalchemyai/` actions in the header/hero and beside the completed offer, preserving “possible contribution, not an open role.”

3. **HIGH — The page optimizes for presenting a meeting, not recruiting a collaborator.** The scarce header CTA is “Present this page” and nav promotes “45 minutes” (1373–1379); hero repeats the weekly-meeting explanation/truth chip (1396–1407); a full five-step agenda consumes the post-project conversion position (2108–2142). The visitor’s actual next action arrives later and still cannot leave the page. **Fix:** make “Explore projects” then “Contact CyberAlchemy” the primary CTA hierarchy; demote the meeting agenda to optional disclosure or remove it.

4. **HIGH — Visible Co-Op/meta-conversation chrome obscures the portfolio’s owner and product purpose.** Complete inventory: title “Co-Op Engine — Project Map” (8); `CO—OP / 14` (1372); “Present this page” (1379); “Page cue” plus `Orienting…` (1382–1385); “The Co-Op Engine · project map / live presentation” (1390); meeting definition (1396–1399); orbit-center “Co-Op Engine” (1417); “The meeting already exists” and “45 minutes…”/Co-Op weekly room (2108–2115); “Recruitment without the theater” (2144–2147); “What this page can—and cannot—prove” (2169–2175); “Public review prototype…” (2194–2196); presentation-stage title “The Co-Op project map” (2198–2205). **Fix:** execute the fixed requirement to remove visible Co-Op branding and meta-conversation labels; retain only visitor-facing project, contribution, and honest-boundary language.

5. **HIGH (mobile source risk) — Mobile loses discovery navigation while retaining presenter chrome and a near-full-width fixed cue.** At ≤900px `.site-nav` disappears (1100–1107); at ≤640px the header still emphasizes its button (1159–1169), while `.page-cue` is fixed at `calc(100vw - 1.2rem)` across the bottom (190–206, 1252–1256). Hero CTAs stack correctly (1188–1197), but the persistent cue can cover the single-column reading/conversion flow. **Fix:** keep an always-visible compact Projects/Contact route on mobile and hide/collapse page cue/presentation controls outside explicit presentation mode.

6. **MEDIUM — Contribution clarity is structurally good but operationally vague.** Every card exposes `What exists now`, `Not yet`, `Next experiment`, and `Possible collaborators` (e.g. Whisper 1524–1538; pattern repeats through Ontologize 2083–2097), then warns current welcome requires a human owner (1542; 2101). This correctly keeps stable project truth separate from volatile welcome, but no owner/contact or expected response step is supplied. **Fix:** preserve the card truth; attach a project-aware email/LinkedIn handoff with expectations (“mention project + bounded offer; owner confirms welcome/scope”). Do not imply the working CTA proves recruitment.

Attempted attacks that survived

- **Deployment drift:** live HTML is exact-byte identical to the reviewed file.
- **Find a relevant project:** filters are craft/task-based and retain all records (1456–1473); all 14 are named and jump-addressable (1476–1503).
- **Understand one project:** cards separate vision/current proof/limit/next experiment/collaborators, and explicit `Exists` strips avoid blanket maturity claims (1504–1543; repeated across all 14).
- **Proof inflation:** final boundary explicitly separates page/browser evidence from human understanding, welcome, collaboration, and recruitment (2169–2189).
- **Offer shaping:** selecting a project updates the contribution prompt (2260–2264) and copy behavior has fallback text (2352–2360); this survives as drafting UX, not conversion evidence.

Coverage: [x] cold arrival/identity [x] all visible Co-Op/meta labels [x] all-14 discovery [x] one-project comprehension [x] contribution shaping [x] contact reachability [x] CTA hierarchy [x] meeting dominance [x] mobile source flow [x] proof boundaries [x] live/source parity [ ] rendered mobile visual check (environment blocked).

## Alexander, Christopher — Initial Position

INITIAL POSITION — Alexander, Christopher (IA/copy attacker)

Live/source basis: `https://cyberalchemize.com/` returned 200 and its fetched SHA-256 exactly matched `projects/co-op-engine/index.html` (`1db379…9486`). Firefox snapshot confirmed the visible hierarchy and interactions.

FIX candidates

1. BLOCKER — The surface is still Co-Op, not CyberAlchemy: title, header, hero eyebrow/explainer, diagram, meeting copy/ARIA, and presentation labels all expose Co-Op (`index.html:8,1372,1388-1417,2108-2115,2201,2302`). Fix: replace every visible/accessibility-facing Co-Op identity with a clear CyberAlchemy portfolio proposition; retain generic stage metadata only where it is not rendered as brand.

2. BLOCKER — Recruitment has no destination. The sole conversion path ends in a copied template asking “Who should I speak with?” (`2144-2165`); source/live accessibility tree contain neither required link. Fix: add explicit `mailto:hello@cyberalchemize.com` and `https://www.linkedin.com/company/cyberalchemyai/` actions at the main recruitment decision point (and likely header/hero).

3. HIGH — Persistent `Page cue` is visible process narration, not visitor content (`1382-1385`); live behavior changed it to “Opening Whisper…” after expansion and “Opening Agentic Music Studio…” after filtering (`1504-2063,2267-2284`). “Orienting / Revealing / Choosing / Opening / Testing / Inviting / Closing” tells the visitor how the author is staging the page. Fix: remove the visible cue in browse mode; preserve `data-stage`, `data-stage-title`, and presentation controls as useful internal/presenter metadata.

4. HIGH — The 10-second layer explains a weekly meeting before it establishes CyberAlchemy. The clear broad line (“Fourteen experiments across writing, music…”) survives, but it is immediately subordinated to meeting mechanics and three defensive chips (`1391-1407`). Fix: lead with who CyberAlchemy is, the fields it explores, and why collaborators matter; move meeting mechanics and proof limits later.

5. HIGH — The 30-second cards promise nontechnical reach, then many `Exists` strips switch to repository/process jargon: “research tower…claim ledger” (`1590-1601`), “Kuhn-poker…bot contract…receipt” (`1633-1644`), “L0 mutation loop” (`1719-1730`), “schemas, kernel, L0” (`1805-1816`), “L0 scaffold” (`1934-1945`). Similar opacity reaches AutoAds/Sonar/Ontologize (`1977-2074`). Fix: describe the tangible thing a musician/writer/operator can inspect or try in domain language; place exact implementation vocabulary in deep detail.

6. HIGH — Recruitment information is delayed too far: “Possible collaborators” and offer link appear only after expansion for every project (e.g. Whisper `1516-1542`; pattern repeats through `2101`), and even then no contact action exists. Fix: surface one `Needs now` line and direct contact choice in each 30-second card; keep scope/boundary detail expanded.

7. MEDIUM — The meeting agenda is direct-address coaching (“Browse silently. Mark… Visit… Turn…”) and consumes a full major section (`2108-2141`). Fix: remove from public browsing flow or reveal only inside presenter mode; the portfolio should not require its facilitation script.

8. MEDIUM — Filtering creates a contradictory hierarchy: after “Make sound editable,” live status says one project, while the heading/count and 14-item jump nav still promise the complete map (`1476-1503,2240-2257`). Fix: update/hide count and jump links with the active lens, with an obvious reset to all fourteen.

9. MEDIUM — The final proof section correctly bounds claims but resumes implementation-review narration (“The browser can test…”) and the footer calls the page a “Public review prototype” (`2169-2196`). Fix: keep visitor-relevant honesty (current state, uncertainty, human owner) and remove QA/release-process prose from the public narrative.

10. HIGH / EVIDENCE GAP — No cold-reader retellability evidence exists, so the page cannot yet be called understandable or recruitment-effective. Fix: test unprompted 10-second identity retell, 30-second project retell, deep-detail state/limit retell, and successful contact selection with technical and domain-practitioner readers.

KEEP / survived attacks

- KEEP the actual progressive-disclosure skeleton: broad promise (`1391-1395`) → project question/summary/proof (`1503-2074`) → consistent Vision / What exists now / Not yet / Next experiment / Possible collaborators details. Live expansion worked.
- KEEP all fourteen on one truth surface: filters hide the same card records (`2240-2257`), and presentation reuses those same DOM stages/details (`2286-2320`). Do not create separate presentation copy.
- KEEP the plain-language project questions: all 14 openings (`1510,1553,1596,1639,1682,1725,1768,1811,1854,1897,1940,1983,2026,2069`) are much more legible than their proof strips.
- KEEP craft-first entrances across story, music, games, interfaces, trust, and real-person testing (`1456-1473`), plus honest `Not yet` boundaries.

Coverage: hero/10s ✓; why/mechanism ✓; filters ✓; all 14 openings + proof strips ✓; one deep-detail live trace ✓; meeting ✓; recruitment/contacts ✓; boundary/footer ✓; presentation metadata/control distinction ✓; cold-reader evidence gap ✓.

## Kahneman, Daniel — Initial Position

INITIAL POSITION — Kahneman / accessibility, interaction, trust attacker

Status: FLAG. Current local HTML and live URL are exact-byte identical (`1db379…`), consistent with `deployment/live-acceptance.json:5-13`. I inspected the live accessibility tree and interactions in Firefox at 390×844 because the CLI’s Chrome channel was absent; therefore Chromium-specific reconfirmation remains required. The receipt’s `verdict: pass` proves deployment/layout/runtime checks only, not contact conversion, claim truth, or complete accessibility (`live-acceptance.json:14-49`).

Candidate findings

1. HIGH — Presentation makes keyboard reading compete with slide navigation. On mobile the first stage was scrollable (1302px content / 844px viewport), but PageDown advanced from stage 1 to stage 2 with scrollTop still 0. Global interception at `projects/co-op-engine/index.html:2338-2349` prevents the expected reading-scroll behavior; Arrow keys also fire regardless of focused child. Fix: reserve Left/Right for stage changes only when focus is not on an interactive control; never hijack PageUp/PageDown on overflowed stages; retain explicit Back/Next buttons.

2. HIGH — Recruitment path is a dead end. Live DOM has zero `mailto:` or LinkedIn links. Fourteen project offers only jump to `#join` (`:1541` and repeated), where the sole action copies text (`:2153-2165`, `:2352-2360`). This cannot establish successful contact, exactly as Inventory’s browser/copy/human/recruitment separation requires. Fix: add clearly named contact actions for `mailto:hello@cyberalchemize.com` and `https://www.linkedin.com/company/cyberalchemyai/`, visible and keyboard reachable on mobile; retain “possible contribution / human confirms” copy.

3. HIGH — “Evidence/proof” is asserted but not inspectable. Copy says visitors can “see the evidence” and “open evidence” (`:1430-1451`, `:2111-2114`), while each “Exists” strip opens only more prose and exposes no evidence/source link (`:1515-1543`, pattern repeated). Browser evidence cannot validate those project claims. Fix: link each public-safe Exists statement to inspectable evidence, or relabel it as an owner-supplied current-artifact statement and keep truth verification as residue.

4. MEDIUM — Live regions can over-announce coaching and duplicate state. Passive IntersectionObserver scrolling mutates the always-live page cue (`:1382-1385`, `:2276-2284`); entering presentation updates filter status before also updating cue and presentation progress (`:2240-2251`, `:2290-2320`, `:2200-2203`). My live DOM showed all four status/live nodes present. Fix: preserve one concise status aid, but remove live semantics from passive scroll narration; announce one atomic stage string only after explicit navigation. This applies the Inventory audit rule without deleting useful state.

5. MEDIUM — Presentation CTAs remain focusable but cease to work as promised. In presentation, first Tab reaches “Find a project by what I do”; Enter changes hash to `#choose` while active stage/title remain `top`. CSS hides non-active stages (`:1003-1017`) but hero anchors remain (`:1400-1403`). Fix: hide/inert ordinary CTAs during presentation or route them through `setStage()`.

6. MEDIUM — Focus indicator fails the 3:1 component contrast proxy on light surfaces. `:focus-visible` is coral (`#ff765f`) (`:68-71`), only 2.31:1 against paper and 2.58:1 against paper-strong. Fix: use ink or a two-color focus ring; validate every component in forced/default color states.

7. MEDIUM — Heading/article semantics are incomplete. “Why this exists” targets a section with no heading (`:1421-1454`); agenda `<section>` items and boundary `<article>` items use `<strong>` rather than headings (`:2115-2141`, `:2177-2189`). Fix: promote those labels to h2/h3 while preserving styling.

8. MEDIUM — Rebrand residue survives outside visible copy. Even treating visible Co-Op removal as fixed, rename `<title>` (`:8`), brand accessible name (`:1372`), stage title/data (`:1388`, `:2201`), agenda accessible name (`:2115`), and script fallbacks (`:2302`, `:2329`). The live accessibility tree currently announces “Co-Op Engine home/meeting route/project map.”

9. SOFT TRUST FLAG — “The weekly meeting already exists” is repeated as fact (`:1397`, `:1405`, `:2108-2113`) but neither source nor deployment receipt proves ongoing operation. “Fourteen experiments” (`:1393`) also includes docs-only/non-executed items. Fix: require dated owner confirmation or soften to a meeting format and “projects at different evidence stages.”

Privacy/contact safety

- Initial load survived: receipt shows one same-origin GET, zero external requests, and strong CSP/permissions/referrer headers (`live-acceptance.json:34-49`); no tracking evidence observed.
- Email publishes the mailbox to scrapers and hands content to the visitor’s mail provider; LinkedIn discloses network/device context and, under current `strict-origin-when-cross-origin`, the site origin. State that these actions open external services; use `rel="noopener noreferrer"` for a new LinkedIn tab and no tracking parameters. Do not prefill personal/project-sensitive data.

Concrete black-box checks

- Mail: `getByRole('link', {name:/email/i})` is visible at 390×844, keyboard reachable, exact href begins `mailto:hello@cyberalchemize.com`, contains no cc/bcc or sensitive prefill, and click emits no HTTP request. OS mail-client launch remains manual residue.
- LinkedIn: exact href is `https://www.linkedin.com/company/cyberalchemyai/`; accessible name says CyberAlchemy + LinkedIn; keyboard activation yields that HTTPS origin/path (allow login redirect); if `_blank`, assert `rel` contains `noopener noreferrer`; no query tracking.
- Keyboard: skip link focuses `main` (survived); native details opens with Enter (survived); every long presentation stage can scroll by PageDown without stage change; focus remains visibly within viewport after filtering; filtered jump links do not target hidden cards; Escape returns focus to Present (survived).
- Live state: one announcement per filter/stage/copy action; none from passive scrolling; rebrand text absent from title and accessibility snapshot.
- Mobile: CTA targets ≥24px (current hero buttons were ~44.8px and no horizontal overflow—survived); contact actions remain visible/reachable; presentation controls do not obscure final content.

Coverage: keyboard/focus ✓; live regions ✓; presentation ✓; headings/links ✓; contact safety/clarity ✓; mobile CTA ✓; privacy ✓; claim bounds ✓. Human residues: current meeting reality, project evidence truth, comprehension, trust, recruitment outcome.

## Peirce, Charles Sanders — Final Position

FINAL POSITION — Peirce

1. **KEEP — BLOCKER: CyberAlchemy is unidentified.** Alexander independently confirms the cold-reader failure; Kahneman extends it to title, accessible names, stage titles, and script fallbacks. Replace all visible and accessible Co-Op identity residue with a 10-second CyberAlchemy identity layer before any meeting/process explanation.

2. **KEEP — BLOCKER: contribution cannot reach a human.** Use one central, persistent contact route: email as the primary action, LinkedIn secondary. Each project’s “Build an offer” action should carry the selected project into that central contact panel and prefill a safe mailto subject/body; avoid duplicating both destinations fourteen times. Validate exact destinations, keyboard activation, new-tab behavior, and mail-client fallback. Do not treat working links as recruitment evidence.

3. **MODIFY — HIGH: meeting/presentation framing dominates recruitment.** Remove the five-step agenda from normal browse flow; it is coaching material, not portfolio content. It may remain presenter-only. Keep a short, owner-confirmed meeting note only if currently true. Demote “Present this page” beneath Explore/Contact. Preserve non-rendered `data-stage` machinery, but fix PageDown hijacking, focus-state desynchronization, and long-stage navigation before retaining presentation mode.

4. **KEEP — HIGH: visible meta-conversation chrome should be removed.** Remove Page cue, cue verbs, live-presentation labels, “Recruitment without the theater,” prototype-review framing, and visible Co-Op branding. Extend removal through `<title>`, accessible names, initial stage title, and script fallbacks. Retain honest visitor-facing boundaries, not the page’s self-narration.

5. **MODIFY — HIGH: mobile conversion path is weak, but drop the unverified overlap claim.** Kahneman’s black-box pass found no responsive overflow, so I retract any implication of demonstrated layout breakage. The supported issue remains: mobile hides primary navigation while retaining presenter emphasis and passive live-region cueing. Provide compact Projects/Contact navigation, remove the passive cue, and re-test a complete mobile choose-project → understand → contact journey.

6. **MODIFY — MEDIUM/HIGH: project truth is well structured but not sufficiently actionable or inspectable.** Keep one canonical all-fourteen surface and the per-card sequence: plain-language “What exists now,” “Not yet,” “Needs now,” and “Who could help.” Replace jargon-heavy “Exists” strips, surface “Needs now” in the 30-second layer, and link evidence where publicly inspectable. Current welcome remains volatile and owner-confirmed; the repeated “meeting already exists” claim belongs in that same volatile category. Also make filtered counts and jump navigation reflect the active result set.

Accessibility findings strengthen, rather than replace, the conversion advice: contact links must be safely operable; focus contrast and heading structure need correction; redundant live regions should be reduced; PageDown must not be globally captured. These are release blockers where they prevent or confuse the contact journey.

Surviving strengths remain: exact live/source parity, all-fourteen single truth surface, craft filters, strong opening questions, progressive details, honest “Not yet” boundaries, skip link, keyboard-operable details, Escape focus return, and responsive no-overflow. Cold-reader comprehension and real contact conversion remain unproved until tested with people.

## Alexander, Christopher — Final Position

FINAL POSITION — Alexander, Christopher, IA/copy attacker

The peers strengthen the original verdict: the page has a viable portfolio structure, but its current identity, narration, and handoff make it a meeting deck rather than a CyberAlchemy recruitment surface. Live bytes matched the reviewed source.

### Finding dispositions

1. **KEEP — BLOCKER: CyberAlchemy identity is absent.**  
   Co-Op remains in the title, visible brand, accessible names, hero, diagram, meeting labels, and script fallbacks (`index.html:8,1372,1388-1417,2108-2115,2201,2302`).  
   **Change:** replace the complete visible and accessibility-facing Co-Op inventory with one plain CyberAlchemy identity and portfolio proposition.

2. **MODIFY — BLOCKER: preserve one central handoff, not fourteen duplicated contact flows.**  
   Peirce is right that every project offer reaches the same copy-only dead end (`1541-1542` through `2100-2101`, then `2144-2165`). Per-card email/LinkedIn duplication would make fourteen truth surfaces drift.  
   **Change:** each card gets a project-aware “Talk about [project]” route into one shared contact section; that section exposes exactly `mailto:hello@cyberalchemize.com` and `https://www.linkedin.com/company/cyberalchemyai/`, carrying the selected project in visible text and, for email, the subject/body.

3. **KEEP — HIGH: remove the visible Page cue and narration vocabulary.**  
   `Page cue`, `Orienting`, `Revealing`, `Choosing`, fourteen `Opening` cues, `Testing`, `Inviting`, and `Closing` are facilitation narration (`1382-1388,1421,1456,1504-2063,2108,2144,2169`). Kahneman additionally shows the passive cue competes with genuine filter/copy/presentation live status.  
   **Change:** remove the cue UI and its live region. Retain `data-stage`, `data-stage-title`, active stage title/count, Back/Next/Exit, and Escape return only inside explicit presentation mode. Retain filter and copy-result status announcements; do not narrate scrolling.

4. **KEEP — HIGH: rebuild the 10-second layer around identity and invitation.**  
   The broad “Fourteen experiments…” line survives (`1391-1395`), but meeting mechanics and defensive chips immediately displace it (`1396-1407`).  
   **Change:** hero order becomes CyberAlchemy identity → fields explored → why outside craft matters → browse/contact actions. Proof boundaries follow, rather than leading.

5. **MODIFY — HIGH: translate proof strips and make evidence status inspectable.**  
   Domain-practitioner openings are followed by internal terms such as “research tower,” “claim ledger,” “bot contract,” “L0 mutation loop,” “schemas,” and “kernel” (`1590-1601,1633-1644,1719-1730,1805-1816,1934-1945`). Kahneman correctly adds that prose labeled `Exists` is not inspectable evidence.  
   **Change:** the 30-second strip states the tangible thing someone can see, hear, run, or review in domain language. Deep detail preserves exact technical status and adds a safe evidence link where public evidence exists; otherwise explicitly says evidence is private, unavailable, or reviewable by request.

6. **MODIFY — HIGH: surface recruitment relevance without flattening the hierarchy.**  
   “Possible collaborators” is buried inside every expansion.  
   **Change:** add one concise `Needs now` or `Useful crafts` line to the 30-second card; route its action to the shared project-aware handoff. Keep scope, limits, and owner confirmation in deep detail.

7. **MODIFY — MEDIUM: meeting agenda becomes presenter-only.**  
   The full “Orient / Scan / Open / Shape / Read back” script is direct-address coaching (`2108-2141`) and optimizes facilitation over recruitment. Kahneman also establishes that the “meeting already exists” claim lacks current owner confirmation.  
   **Change:** remove the agenda from public browse mode; optionally retain it as a presentation-only stage. Public copy may say conversations are human-confirmed, but must not assert an existing weekly meeting until reconfirmed.

8. **KEEP — MEDIUM: filtering must update the surrounding hierarchy.**  
   After the music filter, live status says one project while the heading, count, and fourteen jump links remain unchanged (`1476-1503,2240-2257`).  
   **Change:** filter the jump navigation and visible count/heading with the cards, plus provide an obvious “Show all fourteen” reset.

9. **KEEP — MEDIUM: remove QA/release narration from visitor copy.**  
   “The browser can test…” and “Public review prototype” (`2169-2196`) are review-process prose.  
   **Change:** preserve visitor-relevant boundaries—current state, uncertainty, evidence availability, human ownership—and move browser/release assertions out of the public narrative.

10. **KEEP — HIGH EVIDENCE GAP: no comprehension or recruitment claim yet.**  
    **Change:** require cold-reader checks across technical builders, writers, musicians, and other practitioners:

    - 10-second CyberAlchemy identity retell
    - 30-second selected-project retell
    - deep-detail current-state/limit/evidence retell
    - project-aware email and LinkedIn completion
    - presentation keyboard checks, including no global PageDown hijack
    - exact destination, focus contrast, heading, and announcement checks

### Survived attacks

- **KEEP** the one shared fourteen-project DOM/data surface across browse, filter, and presentation (`2240-2257,2286-2320`).
- **KEEP** the progressive-disclosure skeleton: portfolio promise → project question/summary/plain proof → vision/current state/limit/next experiment/collaborators.
- **KEEP** all fourteen plain-language opening questions (`1510,1553,1596,1639,1682,1725,1768,1811,1854,1897,1940,1983,2026,2069`).
- **KEEP** craft-first entrances and explicit `Not yet` boundaries.
- **KEEP** the proven skip link, keyboard-operable details, Escape focus return, responsive no-overflow behavior, and same-byte live/source parity.

Final recommendation: **FIX before acceptance as a CyberAlchemy portfolio or recruitment surface.** The structural chassis survives; identity, visitor-language hierarchy, evidence access, presentation containment, and contact completion do not.

## Kahneman, Daniel — Final Position

FINAL POSITION — Kahneman / accessibility, interaction, trust attacker

Status: FLAG. Peirce and Alexander strengthen the core diagnosis: this is not merely a missing-contact defect. The browse experience still presents a meeting artifact before it establishes CyberAlchemy and a usable contribution route.

Findings disposition

- KEEP, HIGH — Presentation hijacks PageUp/PageDown even when the active stage overflows. Preserve Back/Next, Escape, and stage progress, but let PageUp/PageDown scroll. Left/Right may change stages only when focus is outside interactive controls.
- MODIFY, HIGH — Contact dead end. A central contact block alone is testable but loses the project context the page worked to establish. Add:

  - A central email and LinkedIn route near the CyberAlchemy introduction.
  - One project-aware email action per card/detail, using the same mailbox with only the public project name in an encoded subject.
  - No claim that clicks prove recruitment or successful contact.

- MODIFY, HIGH — “Proof/evidence” language. Do not require public links where authority evidence is private. Use a hybrid:

  - Link “Exists” to public-safe evidence where available.
  - Otherwise label it “Current artifact — owner stated; evidence not public.”
  - Remove claims that visitors can “see/open evidence” when the page only supplies prose.
  - Preserve the Ambition / Exists / Not yet / Next experiment grammar.

- KEEP, MEDIUM — Live-region overload. Remove the visible Page cue and its passive-scroll `aria-live`. Keep:

  - Filter result status.
  - Copy/contact status.
  - One atomic presentation status containing stage title and count.

  `data-stage` and `data-cue` may remain non-rendered presenter metadata. Do not announce cue coaching automatically.

- KEEP, MEDIUM — Ordinary hero links remain focusable during presentation but do not change the active stage. Either hide/inert them in presentation or route them through stage navigation.
- KEEP, MEDIUM — Coral focus outline is below 3:1 against both light surfaces. Replace with ink or a dual-contrast ring.
- MODIFY, MEDIUM — Heading/article semantics. Add real headings to the “Why” section and any retained agenda/boundary cards. If the agenda becomes presenter-only, it still requires meaningful heading structure.
- KEEP, raise to HIGH — Rebrand residue. Remove Co-Op from document title, accessible home name, agenda name, stage titles, initial presentation progress, and script fallbacks—not only visible copy.
- MODIFY, HIGH trust flag — Meeting claims and placement. Keep the 45-minute agenda only as presenter-mode material. Browse mode should lead with CyberAlchemy, projects, evidence state, needs, and contact. Any “weekly meeting already exists” claim requires current owner confirmation.
- ADD, MEDIUM — Filter hierarchy is internally contradictory: all fourteen jump links remain while thirteen cards may be hidden. Filter the jump list with the cards, or make it explicitly restore “All” before navigating.
- ADD, MEDIUM — “Needs now” is buried in progressive details. Surface a concise present need plus project-aware contact action in the 30-second card layer; retain full boundaries below.

Peer tensions resolved

- Status aid: keep filter/copy status and one presentation title/count announcement; drop the scrolling Page cue and coaching narration.
- Contact: central email/LinkedIn establishes company identity, but per-project email actions are required to preserve intent and test every opening end-to-end.
- Evidence: relabel by default; link only public-safe evidence. Never imply private evidence is publicly inspectable.
- Meeting: retain it in presenter mode, not the cold-reader browse path.

Minimum black-box acceptance

1. At 390×844, the first viewport identifies CyberAlchemy and exposes a keyboard-reachable contact or project-finding action without horizontal overflow.
2. Accessibility snapshot and document title contain no Co-Op/meta-conversation residue.
3. Exactly fourteen project-aware email actions resolve to `mailto:hello@cyberalchemize.com`; accessible names identify their projects; subject contains only the public project name; no cc, bcc, or sensitive body.
4. LinkedIn resolves exactly to `https://www.linkedin.com/company/cyberalchemyai/`; its name identifies CyberAlchemy and LinkedIn; `_blank` requires `noopener noreferrer`; no tracking query.
5. Initial load makes no external requests. Email produces no HTTP request; LinkedIn traffic occurs only after activation.
6. Skip link focuses main; filters, details, contacts, presentation controls, and Escape work by keyboard; Escape restores focus.
7. PageDown scrolls an overflowing presentation stage without changing stage. Arrow navigation does not fire from focused controls.
8. Filtering keeps focus visible, announces one result update, synchronizes count/cards/jump links, and exposes no link to a hidden target.
9. Passive scrolling produces no live announcement. Each filter, copy, and stage action produces at most one concise announcement.
10. Focus indicators meet 3:1 non-text contrast, controls are unobscured, and mobile targets remain at least 24×24 CSS px.
11. Headings form a coherent h1→h2→h3 hierarchy; articles/sections have meaningful names.
12. “Evidence/proof” appears only with a public-safe link or an explicit owner-stated/non-public qualifier.

Human residue remains: current meeting operation, project-claim truth, comprehension, trust, welcome, successful contact, and recruitment outcome.

## Popper, Karl — Verifier Receipt

Verifier receipt — Popper

Taxonomy applied: CRITICAL means system-breaking, unsafe, or blocks the primary surface entirely; MAJOR means a fixed requirement or core visitor task materially fails; MINOR means bounded usability/accessibility debt. No candidate meets CRITICAL.

- `CAFR-HTML-001` — `MODIFY / MAJOR`. No objection to the evidence: source and rendered page expose Co-Op identity in title, brand/accessibility name, hero, cue, meeting label, presentation fallback, and footer; the mobile render contains no “CyberAlchemy.” Objection: CRITICAL is inflated. The page remains functional and all projects remain accessible. Required wording: “Replace browse-visible and accessibility-facing Co-Op/meta identity with CyberAlchemy portfolio identity. Preserve only presentation-operational metadata that is not visitor copy.” Do not imply the meeting itself must be deleted.

- `CAFR-HTML-002` — `MODIFY / MAJOR`. Verified: fourteen `href="#join"` links, no `mailto:` or LinkedIn destination, and the live handoff changes only visible project text through JavaScript. Objection: CRITICAL is inflated; this is a failed core conversion requirement, not a broken system. The shared contact block is source-aligned only if email and LinkedIn are ordinary static links and remain usable without JavaScript. Project context may enhance the visible label and safe mail subject, but contact must be framed as a non-binding inquiry—not an owner-authorized “open ask.” The source permits an offer/contact route only for an owner-bound `open ask`; current welcome is unbound. No `cc`, `bcc`, private body, or inferred welcome.

- `CAFR-HTML-003` — `KEEP WITH MODIFICATION / MAJOR`. Verified: browse navigation and hero foreground “Present this page,” “45 minutes,” and the meeting before CyberAlchemy/contact. The agenda may and should survive as presenter-only support because the primary source calls the existing meeting a fact and requires the same records to support it. Refute SYNTHESIS wording that the meeting should be softened absent new confirmation. Required fix: remove it from browse-mode positioning, not from the artifact.

- `CAFR-HTML-004` — `KEEP / MAJOR`. Selector and behavior verified. With “Next” focused, `ArrowRight` advanced from stage 19 to 20 and moved focus; the handler also unconditionally consumes PageUp/PageDown. Gate navigation away from interactive focus, allow stage scrolling, preserve ordinary link behavior/recovery, and restore focus on exit.

- `CAFR-HTML-005` — `MODIFY / MAJOR`. Evidence quotations are correct, but “research tower,” “claim ledger,” and similar terms are not inherently defects—the primary source explicitly permits source-bound technical terms after an ordinary-domain act. The real defect is the universal “I can see the evidence”/“Proof” promise while collapsed strips provide artifact-state prose without an adjacent limit or public witness. Rename/qualify as owner-stated current state where no authorized public evidence exists; add public-safe links only when authorized.

- `CAFR-HTML-006` — `MODIFY / MAJOR`. Verified: collaborator/next-action information is hidden in every expansion. Do not surface “Needs now” unless an owner has bound a fresh open ask. Surface the contribution state instead: `none`, `possibility`, or owner-backed `open ask`; keep crafts as possibilities and preserve the detailed limit/welcome boundary.

- `CAFR-HTML-007` — `KEEP / MINOR`. Reproduced: the music filter showed one visible card while count remained `14`, heading remained “Fourteen…,” and all fourteen jump links remained available. Synchronize count/context/jumps and provide reset.

- `CAFR-HTML-008` — `KEEP / MINOR`. CSS and selectors support the focus-contrast concern; agenda and boundary cards use `<strong>` rather than headings. Fix focus contrast and section/article naming. This does not block the complete project corpus.

- `CAFR-PACKET-001` — `MODIFY / MAJOR acceptance gap`, not a page defect. The packet is explicitly non-authoritative and cannot prove the finding. Its primary source references independently state that comprehension, welcome, contact outcomes, and recruitment remain unproved; the literal/live page independently shows no contact destinations. Rewrite provenance around those primary sources and browser evidence.

Cross-cutting result: all fourteen named cards remain present, directly navigable, and retain explicit “Not yet” plus human-owner boundaries in details. Their immediate collapsed-view comprehension is weaker because limits and contribution state are hidden, and cold-reader understanding remains unproved.

Final recommendation: `FIX`. Retain the fourteen-project chassis, claim boundaries, filters, and presenter-only agenda. Demote both CRITICAL findings to MAJOR; reject meeting deletion and universal per-project offer language; require a progressive-enhancement-safe central contact route with inquiry-only project context until owner-backed asks exist. Browser verification reproduced the keyboard/filter failures and confirmed the 390×844 page has no horizontal overflow, so no mobile-overlap finding should be revived. No files were changed.

## Quine, Willard Van Orman — Verifier Receipt

## Quine verifier receipt

Scope stayed read-only. The live deployment is byte-identical to the reviewed HTML (`sha256 1db379…4cb9486e`), so browser counterexamples apply to the supplied source.

### Candidate adjudication

| ID | Decision | Severity | Objection / verification |
|---|---|---:|---|
| CAFR-HTML-001 | KEEP | CRITICAL | No objection. Live title, visible text, and accessibility snapshot expose “Co-Op Engine,” `CO—OP / 14`, “Page cue,” “project map / live presentation,” and “Public review prototype.” |
| CAFR-HTML-002 | MODIFY | CRITICAL | Missing contact is confirmed: all 14 offers are `#join`; there is no mailto or LinkedIn link. Objection: do not rely on a JS-only dynamic block. The shared block and all card entry paths must remain usable with JavaScript disabled. |
| CAFR-HTML-003 | DROP | — | The ordering recommendation is aesthetic, not a demonstrated defect. The hero already exposes both browse entrances in the mobile first viewport. CyberAlchemy identity and Contact absence are fully covered by 001/002. |
| CAFR-HTML-004 | KEEP | MAJOR | Confirmed. At 390×844, Whisper’s stage is 1411px tall in an 844px viewport; PageDown changes immediately to the next project instead of scrolling. ArrowRight also advances while focus is on “Next.” Preserve the working behavior: Escape restores focus to `presentButton`. |
| CAFR-HTML-005 | MODIFY | MAJOR | Keep only the trust defect: “I can see the evidence” and “open evidence” are not backed by inspectable public evidence or an adjacent provenance qualification. Drop the untested claim that jargon translation itself is required. |
| CAFR-HTML-006 | DROP | — | Progressive disclosure is functioning: each collapsed card already gives question, summary, and current-state strip; collaborators and offer are one native `<details>` action away. No black-box failure supports duplicating “Needs now.” |
| CAFR-HTML-007 | KEEP | MINOR | Confirmed. Music filtering yields one visible card, while heading/count remain fourteen and all 14 jump links remain; 13 target hidden cards. |
| CAFR-HTML-008 | MODIFY | MAJOR | Focus failure is confirmed: coral contrast is 2.306:1 against paper and 2.578:1 against card white. The blanket “incoherent h1→h2→h3” claim is refuted—the numeric sequence is coherent. Narrow semantics work to unnamed structural articles/agenda items and verify through the accessibility tree. |
| CAFR-PACKET-001 | MODIFY | MAJOR evidence gap | Packet contents were outside the supplied verification files, but the live acceptance receipt demonstrably contains no cold-reader, mailto, LinkedIn, or assistive-technology evidence. Keep this as unfulfilled acceptance evidence, not a page defect or success claim. |

### Corrected black-box acceptance checks

Automatable:

1. Assert document title, rendered text, accessible names, live regions, fallbacks, and presentation UI contain none of the legacy denylist: case-insensitive `Co-Op`/`CO—OP`, “Page cue,” “project map / live presentation,” or “Public review prototype.”
2. Assert exactly these 14 project records, each with one native details disclosure and the five retained fields: Whisper; User / Translate / Guide; Agentic Music Studio; Poker Agent Arena; Body War / TROQAR; UI Prototyping Studio; Tower System; IDE Extension; IDE Ergonomics; X-Ray; Arcanum Journey; AutoAds; Sonar Loop; Ontologize.
3. Assert browse, every filter, and presentation derive from those same 14 nodes; details open state and content survive filtering/presentation transitions.
4. With JavaScript disabled, activate every card entry path and assert it reaches the shared contact region with that canonical public project name visibly present.
5. In that region assert exactly `href="mailto:hello@cyberalchemize.com"` and `href="https://www.linkedin.com/company/cyberalchemyai/"`. Same-tab LinkedIn is acceptable; `_blank` requires both `noopener` and `noreferrer`.
6. Parse every mailto. Permit no `cc`, `bcc`, or `body`. If a secondary project-aware mail link has a query, permit only `subject=<exact canonical public project name>`; retain the exact query-free base mailto.
7. For every filter, assert visible count equals unhidden cards, heading/status/count agree, every visible jump targets an unhidden card, and “All 14” restores all records.
8. On an overflowing presentation stage, PageDown must increase `scrollTop` without changing stage. Left/Right/PageUp/PageDown must not navigate when focus is inside any interactive control. Escape must return focus to the presentation trigger.
9. Passive scroll must cause zero mutations in `aria-live` nodes. Each filter, contact-context, enter/advance/exit presentation action may cause at most one concise announcement.
10. At 390×844, assert no horizontal overflow; first viewport visibly names CyberAlchemy and contains keyboard-reachable Explore and Contact actions. Test all project stages for overflow containment and unobscured controls.
11. Assert visible focus indication is at least 3:1 against adjacent colors, interactive targets satisfy the agreed 24×24 rule or documented WCAG exception, and accessibility snapshots give meaningful names to intended regions/articles.

Human-only:

- Cold readers can accurately retell CyberAlchemy, one project’s state/limit/need, and complete both project-aware contact paths.
- Trust, welcome, successful contact, collaboration, recruitment, and usefulness remain human evidence; automation cannot establish them.

### Refutations and final recommendation

Dropped: hero/agenda reordering and duplicated collapsed-card needs. Partly refuted: global heading incoherence. Keep the prior rejection of a mobile-overlap claim and of fourteen duplicated contact pairs.

Final recommendation: **FIX**. Preserve the 14-project chassis, native details, filters, presentation reuse, working Escape focus restoration, and mobile no-overflow behavior; acceptance remains blocked by identity residue, absent robust contact paths, keyboard interception, passive live-region chatter, filter desynchronization, and focus contrast.

## Quine, Willard Van Orman — Final Zig-Zag Receipt

PASS

| ID | Result |
|---|---|
| CAFR-HTML-001 | No objection |
| CAFR-HTML-002 | No objection; static no-JS context and exact base hrefs are explicit |
| CAFR-HTML-003 | No objection to drop |
| CAFR-HTML-004 | No objection; overflow scrolling, interactive-focus gating, and Escape recovery are covered |
| CAFR-HTML-005 | No objection; narrowed to inspectability/provenance |
| CAFR-HTML-006 | No objection to drop |
| CAFR-HTML-007 | No objection; count, heading/status, jumps, and reset are synchronized |
| CAFR-HTML-008A | No objection; focus contrast check is precise |
| CAFR-HTML-008B | No objection; blanket hierarchy claim is removed |
| CAFR-HTML-009 | No objection; passive versus explicit live-region behavior is testable |
| CAFR-EVIDENCE-001 | No objection; automated and human-only evidence are correctly separated |
| CAFR-PACKET-001 | No objection to replacement |

Final verdict `FIX` is supported. No material behavioral or testability blocker remains in the revised synthesis.

## Popper, Karl — Final Zig-Zag Receipt

PASS

| ID | Result |
|---|---|
| CAFR-HTML-001 | No objection — correctly demoted to MAJOR and bounded to identity/meta copy without deleting meeting capability. |
| CAFR-HTML-002 | No objection — static, no-JavaScript contact contract is source-aligned and avoids implying welcome/open asks. |
| CAFR-HTML-004 | No objection — literal handler/CSS and reproduced keyboard behavior support MAJOR. |
| CAFR-HTML-005 | No objection — now targets unsupported proof framing while preserving source-bound technical vocabulary. |
| CAFR-HTML-007 | No objection — literal source and live reproduction support MINOR. |
| CAFR-HTML-008A | No objection — split appropriately; the global focus failure reasonably supports MAJOR. |
| CAFR-HTML-008B | No objection — bounded semantics issue supports MINOR; broader hierarchy claim is correctly refuted. |
| CAFR-HTML-009 | No objection — live-region mutations are explicit in source; MINOR is proportionate. |
| CAFR-EVIDENCE-001 | No objection — correctly replaces Inventory-derived authority with literal page and live acceptance evidence. |
| CAFR-HTML-003 | No objection to drop — meeting prominence is not independently proven harmful. |
| CAFR-HTML-006 | No objection to drop — progressive disclosure survives, while “Needs now” would overstate owner-bound welcome. |
| CAFR-PACKET-001 | No objection to replacement — Inventory remains non-authoritative. |

The revised `FIX` verdict is supported. Previously dropped claims—mobile overlap, universal public-evidence links, meeting falsity, duplicated contacts, and automated recruitment proof—remain dropped. No files were changed.
