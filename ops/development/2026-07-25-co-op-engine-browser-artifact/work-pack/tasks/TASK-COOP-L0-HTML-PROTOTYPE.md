# TASK-COOP-L0-HTML-PROTOTYPE

## Objective

Implement `SWU-COOP-002`: one locally opened, self-contained semantic HTML
document that lets a reader or facilitator inspect the Co-Op Engine invitation,
the 45-minute route, and exactly fourteen claim-bounded project opportunities.

## Mapping

- Layer: L0
- Slice: `S-L0-HTML-PROTOTYPE`
- Wave: W2
- Status: planned-unselected
- Dependencies:
  - `SWU-COOP-001` terminal result `pass`;
  - `SWU-COOP-001` closeout refresh `pass`;
  - explicit operator selection of `SWU-COOP-002`;
  - fresh strict Context Builder Markdown and JSON/index pair.

This task cannot execute from the current `SWU-COOP-001` goal profile.

## Source Contracts

- [Shared planning context](../shared/context.md)
- [Approved specification](../../SPEC.md)
- [UX plan](../../UX-PLAN.md)
- [Design acceptance review](../../DESIGN-ACCEPTANCE-REVIEW.md)
- [Implementation layering](../../IMPLEMENTATION-LAYERING.md)
- [SWU manifest](../../SWU-MANIFEST.json)
- [Validation strategy](../../VALIDATION-STRATEGY.md)
- [Accepted portfolio findings](../../../2026-07-25-co-op-engine-portfolio-research/findings.md)

## Smallest Working Unit: SWU-COOP-002

### Primary behavior

Render one complete, low-fidelity content and information-architecture
prototype in a real browser without implying that the exchange, project
records, or audits are operational.

### Independent acceptance boundary

At desktop and mobile viewports, `prototype.html` exposes:

- one event invitation and honesty boundary;
- the bounded seven-day exchange loop;
- the complete 45-minute route;
- exactly fourteen unique project articles;
- one current bounded description, limitation, seven-day act, and human
  contribution ask per article;
- participation choices for bringing a project, offering a skill, referring
  someone, or listening.

It produces no console errors, external requests, horizontal overflow, browser
storage, form submission, or hidden/private content.

### Split analysis

Candidate children:

- document shell;
- fourteen-card copy fixture;
- presentation route;
- responsive styles;
- interaction.

Retain the shell, complete card fixture, route, and low-fidelity responsive
styles because the single product question is whether the full portfolio and
meeting narrative cohere in one browser artifact. A shell without the complete
portfolio cannot answer that question. Presentation uses the same semantic
document and in-page anchors rather than a second truth source.

Interaction is independently executable and excluded. Final Whisper
composition, visual polish, admitted-data projection, accessibility
conformance, comprehension, privacy leakage, hosting, and recruitment outcomes
also remain separate evidence families.

### Write scope

- `projects/co-op-engine/prototype.html`

No other file may be created or changed.

## Document Contract

Use one valid HTML5 document with:

1. a descriptive `<title>` and viewport metadata;
2. a visible skip link;
3. one header containing the event name, invitation, and proper-name
   non-automation boundary;
4. one navigation region with in-document anchors;
5. one `<main>` in this semantic sequence:
   - friction and reveal;
   - seven-day experiment loop;
   - fourteen-project catalog;
   - 45-minute meeting route;
   - participation choices;
   - evidence and honesty boundary;
6. one footer with current internal-prototype status;
7. inline CSS for readable desktop/mobile layout, focus visibility,
   reduced-motion compatibility, high contrast, and print projection;
8. no `<script>`, `<form>`, `<input>`, `<button>`, `<dialog>`, remote asset,
   external stylesheet, remote font, iframe, preload, tracking, or storage.

Anchor navigation may move among the shared sections. It is navigation, not a
separate presentation state or interaction workflow.

## Working Copy Contract

The text is an internal, research-derived prototype fixture. It is not final
Whisper copy and must not expose repository paths or authoring metadata.

Opening promise:

> Got a project that needs more hands, or skills looking for a collaborative
> spark? This is where they meet.
>
> The Co-Op Engine is a 45-minute weekly sync for turning ideas into working
> team experiments. Come to share a concept, offer your skills, or just listen
> in and see how we collaborate.

Required clarification near the opening: “Co-Op Engine” is the event’s proper
name. The prototype does not autonomously match people or prove that
collaboration happened.

### Project fixture

| ID | Display label | Current bounded description | Explicit limitation | Seven-day act | Human contribution ask |
| --- | --- | --- | --- | --- | --- |
| `whisper` | Whisper | governed composition workflow | broader transports and quality outcomes remain unproven | compare two drafts with a blind rubric | editor and technical founder, up to 90 minutes |
| `user-guide` | User Guide / User-Translate-Guide | candidate guided-understanding pattern | preference is not mastery; consent/update protocol is unresolved | five newcomers retell and teach back one concept | educator and newcomer reviewers |
| `agentic-music-studio` | Music Interaction Process Research | interaction-process research | taxonomy is not a studio or delegated musical-behavior proof | author one editable-rule scene and hold a listening review | live coder or musician, up to 3 hours |
| `poker-agent-arena` | Poker Agent Arena | runnable Kuhn-poker bot harness | not Hold’em, hosting, final ranking, or a general benchmark | run one legal bot in both seats and inspect replay | adversarial bot author, up to 2 hours |
| `body-war` | TROQAR / Body-War | territorial-running concept | no prototype; safety, privacy, spoofing, fairness, and access remain open | mark a paper zone map after real runs | runners plus privacy reviewer |
| `ui-prototyping-studio` | UI Prototyping Studio | runnable governed UI-variant prototype | later layers and canonical-root ownership remain unresolved | complete one annotated signup-card accept/revert cycle | designer plus accessibility tester |
| `tower-system-taxonomy` | Sourced Stance-Pair Research Witness | sourced stance-pair research witness | opposition, ownership, persona, and scoring remain unresolved | hand-build one DDD node with two genuinely opposed sources | knowledge engineer |
| `ide-extension` | IDE Extension / Governed Workbench | local governed workbench demo | not autonomous, live MCP, browser control, or a shipping IDE wrapper | run five observe→approve→result trials | developer and security reviewer |
| `ide-ergonomics` | IDE Ergonomics | opportunity-routing prototype | no runtime plugin or tested productivity claim | record three route-card choices and their burden | IDE researcher and three users |
| `x-ray` | X-Ray | seed layered HTML/SVG explainer | not promoted or a validated visualization engine | ask two cold readers to retell one explainer | information designer |
| `arcanum-journey` | Arcanum Journey | unrun course concept | design and learner outcome are not witnessed | one novice completes and teaches back an artifact-first path | curriculum designer and novice adopter |
| `autoads` | Autoads | ad creative learning experiment seed | no live networks, spend, or ROAS-automation proof | grade three variants on historical or synthetic data | marketer and causal analyst |
| `sonar-loop` | Sonar Loop | docs-first quality-check orchestration specification | documentation does not prove tool or remediation behavior | manually run one repository through one governed pass | Sonar maintainer |
| `ontologize` | Ontologize | candidate metric-trust engagement | cross-vertical buyer proof and metric advantage remain hypotheses | trace one disputed metric from source through confound to decision | BI practitioner |

Preserve the distinct domain acts—draft comparison, teach-back, editable
musical rules, seat rotation, real runs, annotation, opposed sources,
authorization receipts, route choices, retell, artifact-first learning,
variant grading, quality pass, and metric trace. Do not normalize every card
into generic AI-assistant language.

## 45-Minute Route

- 0–5: orient to one decision—what seven-day experiment, if any, will you help?
- 5–12: silent scan; note help, learn, clarify, or refer.
- 12–29: two or three evidence-triggered clinics.
- 29–39: negotiate reciprocal who/what/when/where/how, boundary, effort, stop
  rule, and receipt.
- 39–45: reciprocal read-back and receipt date.

The document may describe these states. It must not implement energy marks,
candidate pairs, appointments, or receipts.

## Copy Guardrails

Require:

- plain first-use bridges for experiment, clinic, claim ceiling, stop rule, and
  receipt;
- a concrete capability and limitation for every project;
- retained human judgment and one real invitation;
- project-specific voice and observable acts;
- explicit prototype status.

Reject:

- “AI collaborator,” “AI matcher,” “autonomous matching,” “knowledge graph,”
  “agentic writer studio,” or public “Agentic Music Studio”;
- “you’ve been matched,” “the AI found,” “the agent decided,” or
  “your collaborator”;
- finished-product, market-demand, efficacy, privacy-safe, validated-copy, or
  deployed-product claims;
- praise, reassurance, fake intimacy, canned coaching, or answer-bearing
  questions;
- meta-narration such as “this page shows,” “this section explains,” or “here
  we will.”

## Browser Validation

Use the installed Playwright CLI wrapper. Snapshot before referring to any
element identifier, and re-snapshot after viewport changes.

```bash
COOP_PWCLI=/home/vrondelli/.codex/skills/playwright/scripts/playwright_cli.sh
bash "$COOP_PWCLI" -s=coop-html-l0 open file:///home/vrondelli/projects/domainspec-core/projects/co-op-engine/prototype.html
bash "$COOP_PWCLI" -s=coop-html-l0 snapshot
bash "$COOP_PWCLI" -s=coop-html-l0 run-code 'async page => { const cards = await page.locator("[data-project-id]").evaluateAll(nodes => nodes.map(n => n.getAttribute("data-project-id"))); const fields = await page.locator("[data-project-id]").evaluateAll(nodes => nodes.every(n => ["current","limitation","act","ask"].every(f => n.querySelector(`[data-field=\"${f}\"]`)))); return { count: cards.length, unique: new Set(cards).size, fields, overflow: await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth) }; }'
bash "$COOP_PWCLI" -s=coop-html-l0 screenshot
bash "$COOP_PWCLI" -s=coop-html-l0 resize 390 844
bash "$COOP_PWCLI" -s=coop-html-l0 snapshot
bash "$COOP_PWCLI" -s=coop-html-l0 run-code 'async page => ({ overflow: await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth), cards: await page.locator("[data-project-id]").count() })'
bash "$COOP_PWCLI" -s=coop-html-l0 screenshot
bash "$COOP_PWCLI" -s=coop-html-l0 console error
bash "$COOP_PWCLI" -s=coop-html-l0 requests
bash "$COOP_PWCLI" -s=coop-html-l0 close
git diff --check -- projects/co-op-engine/prototype.html
```

Required adjudication:

- desktop and mobile return `count=14`, `unique=14`, `fields=true`, and
  `overflow=false`;
- the semantic snapshot contains one main region, the five narrative regions,
  the complete project catalog, and the meeting route;
- console has no errors;
- request review contains no external network activity;
- screenshots are stored under `output/playwright/` and reviewed as supporting
  evidence, not substituted for DOM evidence;
- a source scan confirms no forbidden elements, remote resources, private
  paths, or forbidden phrases.

## Evidence Ceiling

A pass establishes only that one local static prototype has complete fixture
content, semantic browser structure, responsive preservation, clean
console/network behavior, and review screenshots.

It does not establish:

- project admission or canonical truth beyond the accepted research fixture;
- real self-guided/presentation mode behavior;
- accessibility conformance;
- privacy safety across observable surfaces;
- final Whisper voice or copy quality;
- comprehension, coherence, recruitment, meeting efficacy, deployment, or
  public readiness.

## Execution Owner and Result

- Recommendation: `local-fallback`
- Capability: native goal or Task Session after explicit selection
- Expected result shape: exact `SWU-COOP-002` shape in `SWU-MANIFEST.json`
- Stop on: stale/missing source binding, write-scope conflict, need for a
  second file or JavaScript behavior, browser unavailable, fewer/more than
  fourteen distinct cards, unsupported project wording, external request,
  console error, overflow, or any privacy/publication ambiguity.

## Synchronization

On terminal execution, emit the source receipt, validate the exact closeout
contract, apply only declared status/evidence deltas through
`invoke:refresh:apply-approved`, emit the closeout receipt, and stop. L1 is not
an automatic successor.
