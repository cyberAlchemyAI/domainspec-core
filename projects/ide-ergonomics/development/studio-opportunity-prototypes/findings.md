# IDE Ergonomics Studio Opportunity Prototypes - Findings

Dispatch: `2026-07-01-ide-ergonomics-studio-opportunity-prototypes`

## Core Finding

Use `projects/ui-prototyping-studio/` as an interactive Studio-session harness,
not as a slide deck. The goal is to make each IDE Ergonomics opportunity visible
as something an end user clicks, reviews, and saves as local prototype evidence.
Built prototype packages must produce Studio L0-L2 acceptance evidence; deferred
items remain local strategy or storyboards until their fixtures exist.

Do not make one slide per opportunity. Build the route-card shell first, then
run child sessions for concrete work outputs that share that shell. Use variants
only inside a session for copy/layout alternatives; do not use variants as the
unit for different opportunity families.

## Prototype Effects Strip

Every prototype should include this persistent strip:

- `Preview: no write`
- `Save draft to workbench: local Studio draft artifact, not canonical`
- `Apply: stages Studio candidate`
- `Accept: advances Studio session only`
- `Export: terminal confirmation required`

Every route card, popup, rail card, or final workbench output should also show:

- `Studio draft artifact`
- `not canonical`
- `allowed effect: save local prototype evidence`
- `Owner route`
- `Required gate`
- `Forbidden effects`
- `Expected receipt`

## Build Order

1. Route-card shell and evidence/receipt rail.
2. Candidate definition child session.
3. Side-node child session.
4. Handoff child session.
5. Delegated-lane decision-preview session.
6. Knowledge reference popup session.
7. Craft read-only panel session.
8. Teammate memo window session.
9. Intent-latitude L0 session.
10. Self-assembling / maintenance approval L0 storyboard.
11. Connective task manager only after fixture-backed manual load/test inputs exist.

## Opportunity Coverage

| Opportunity | Studio treatment | Why |
| --- | --- | --- |
| Action-card model | Route-card shell | It is the reusable transition primitive. |
| Evidence/receipt rail | Shared rail in every session | It makes proof, draft, blocked, and receipt states visible. |
| Candidate definition | Child session under route-card shell | Same trigger, distinct artifact lifecycle. |
| Side node capture | Child session under route-card shell | Same trigger, distinct parking result. |
| Handoff composer | Child session under route-card shell | Same trigger, distinct next-session artifact. |
| Subagent fanout preview | Separate decision-preview session | Preview only; execution requires dispatch-spec confirmation. |
| Spell/sigil improvement nudge | Fold into self-assembling/maintenance storyboard | It is friction evidence, not first-pass capability mutation. |
| Knowledge entry reference | Popup session | Read-only resolver with resolved/ambiguous/unresolved fixtures. |
| Referenced field hover | Resolver fixture/state inside reference session | Same resolver shell, different token kind. |
| Knowledge graph side panel | Deferred navigation experiment | First pass should not become a dashboard. |
| Craft control panel | Craft read-only panel session | Strong standalone read/routing scene. |
| Connective task manager | Deferred until manual fixture inputs exist | Avoid inferred human state and runtime claims. |
| Teammate handoff memo | Memo window session | Concrete, reviewable start-work/handoff scene. |
| Intent-latitude annotation | L0/report session | Useful input-side proof, but not enforcement yet. |
| Self-assembling ergonomics action | L0 approval storyboard | High-risk; must show gates before action. |
| Host-surface package | Deferred host validation dependency | Not a product scene until a concrete IDE target is validated. |
| Dispatch grammar routing | Latent/internal | Surfacing the full grammar overbuilds the product. |
| Restraint floor | Cross-cutting strip | It belongs in every session, not as its own prototype. |
| Lifecycle progression | Receipt-debt cue only | A full graph is too much for the MVP. |

## Owner-Route Map

| Surface | Owner route shown in UI | Boundary text |
| --- | --- | --- |
| Route-card shell | `dispatch-spec` plus Necronomicon | route suggestion only; no execution or route switch |
| Candidate definition | `definitions-governance` | candidate packet only; no canonical definition write |
| Side node | Necronomicon side-note queue | active route unchanged; no Craft write |
| Handoff composer | Necronomicon plus Invoke | draft handoff only; not proof and not sent |
| Delegated-lane preview | `dispatch-spec` | plan only; no agents spawned without confirmation |
| Knowledge reference popup | Inventory/Ontology read model | read-only lookup; no authority promotion |
| Referenced field hover | Definitions/schema/inventory resolver | read-only field meaning; ambiguous stays ambiguous |
| Craft read-only panel | Craft | draft routing answer only; no ledger mutation |
| Connective task manager | Craft plus host owner plus selected route owner | recommendation only; no inferred human state |
| Teammate memo window | Handoff owner plus Decision Gate | draft reply/resolution only; no external send |
| Intent-latitude annotation | Validator contract plus DomainSpec v2 owner | L0 report only; no marker-based enforcement |
| Self-assembling storyboard | Spellcraft, Sigil Development, and Decision Gate | proposal/approval storyboard only; no build or promotion claim |

## Reviewer Evidence Table

| Scene | Click target | Popup/rail content | User-visible result | Screenshot/id evidence |
| --- | --- | --- | --- | --- |
| Route-card shell | `chat.hotphrase.evidence-rail` | source span, owner route, gate, forbidden effects, expected receipt | possible transition becomes preview-only route card | route card open/close, mobile/desktop, `popover.route-card` |
| Candidate definition | `route.choice.candidate` | source span, owner, draft meaning, proposed destination, blocked action | candidate draft saved to workbench, not canonical | current: `modal.dialog`; required before field review: `modal.candidate.*`; saved: `artifact.candidate`, `final.card.candidate` |
| Side node | `route.choice.side-node` | class, source, summary, next | tangent parked while active route stays unchanged | current: `modal.dialog`; required before field review: `modal.side-node.*`; saved: `artifact.side-node`, `final.card.side-node` |
| Handoff | `route.choice.handoff` | start prompt, open call, source refs, boundary | next-session draft created, not sent and not proof | current: `modal.dialog`; required before field review: `modal.handoff.*`; saved: `artifact.handoff`, `final.card.handoff` |
| Delegation preview | `route.choice.delegation` | roles, context, join policy, receipt, no agents spawned | delegation plan saved; run action remains gated | current: `modal.dialog`; required before field review: `modal.delegation.*`; saved: `artifact.delegation` |
| Reference popup | `reference.token.knowledge` | handle, source, freshness, status, authority, residue | citation can be copied or added to draft handoff | `popover.knowledge-entry`, `popover.field-reference` |
| Craft read-only | `craft.row.pending` | ledger path, freshness, route question, expected receipt | draft routing answer without ledger mutation | `craft.panel`, `craft.route-question` |
| Memo window | `memo.item.open` | to/from, why now, open call, boundary | draft reply/resolution/defer receipt | `memo.detail`, `memo.action.*` |
| Intent latitude | `intent.span.selected` | literal/goal/constraint tag and draft verdict | annotated message span, unenforced states visible | `intent.tag.*`, `validator.preview` |
| Self-assembling storyboard | `action.build-this` | friction evidence, allowlist, frozen criterion, approval state | L0 experiment proposal, not shipped/promoted | `friction.nudge`, `criterion.frozen`, `approval.ready` |

## Session 1: Route-Card Shell

Fixture: a chat phrase such as `evidence rail` is highlighted inside an IDE
conversation.

Click path:

`chat.hotphrase.evidence-rail` -> route card titled
`Possible workflow transition detected` -> `preview only` pill -> route buttons
-> receipt/evidence rail.

Required route buttons:

- `Create candidate`
- `Park side node`
- `Compose handoff draft`
- `Preview delegated lanes`

Required route-card content:

- `Source span`
- `Owner route`
- `Allowed effect`
- `Required gate`
- `Forbidden effects`
- `Expected receipt`

Forbidden effects:

- canonical mutation;
- owner-route execution;
- agent execution;
- Craft ledger writes;
- authority promotion;
- hidden route switching.

Acceptance:

- phrase opens the route card;
- close works by X button, Escape, and outside click where applicable;
- route buttons open realistic previews or child-session links;
- receipt rail is visible;
- stable ids receive Studio comments;
- desktop/mobile layouts do not overlap.

## Child Sessions Under The Route-Card Shell

| Child session | Concrete fixture | Popup fields | Required labels |
| --- | --- | --- | --- |
| Candidate definition | term: `evidence rail` | `Source span`, `Owner`, `Draft meaning`, `Proposed destination`, `Blocked action` | `candidate-not-canonical`, `Save draft to workbench`, `canonical promotion blocked` |
| Side node | tangent: `Maybe this belongs in the knowledge graph later` | `Class`, `Source`, `Summary`, `Next` | `active-route-unchanged`, `does not switch task`, `does not write Craft` |
| Handoff composer | next-session prompt: `Collect Studio acceptance evidence for the route-card shell` | `Start prompt`, `Open call`, `Source refs`, `Boundary` | `handoff is not proof`, `draft only`, `not sent` |

Add field-level ids before field-level review:

- `modal.candidate.source-span`
- `modal.candidate.owner`
- `modal.candidate.blocked-action`
- `modal.side-node.class`
- `modal.side-node.source`
- `modal.side-node.next`
- `modal.handoff.start-prompt`
- `modal.handoff.open-call`
- `modal.handoff.refs`
- `modal.handoff.boundary`

Until those ids exist, Studio comments should target `modal.dialog`,
`route.choice.*`, `artifact.*`, and `final.card.*` rather than claiming durable
field-level annotation.

## Delegated-Lane Preview

Build this as a decision-preview session, not as part of the first shell.

Fixture: user clicks `Preview delegated lanes`.

Required content:

- role lanes;
- role owner;
- visible context;
- join policy;
- validation or receipt requirement;
- `No agents spawned`;
- `Recommendation is not permission`.

Button copy:

- primary: `Save delegation plan`;
- disabled/downstream: `Run delegation requires dispatch-spec confirmation`.

Add delegation field ids before field-level review:

- `modal.delegation.role`
- `modal.delegation.visible-context`
- `modal.delegation.join-policy`
- `modal.delegation.receipt-required`

Forbidden effects: spawning subagents, treating preview as permission, hidden
execution.

## Knowledge Reference Popup

Fixtures:

- resolved: `knowledge:inventory/evidence-rail`;
- ambiguous: `confidence_reference`;
- unresolved: `knowledge:ontology/missing-handle`.

Required popup content:

- handle;
- source surface;
- freshness;
- snippet;
- status;
- confidence;
- authority boundary;
- promotion owner;
- residue;
- safe actions.

Safe action labels:

- `Open source`
- `Copy reference`
- `Add citation to draft handoff`
- `Re-run lookup`

Header label: `Read-only resolver`.

Forbidden effects: inventory writes, ontology writes, authority promotion,
fabricated source choice, stale hiding, generic knowledge badge.

Defer the knowledge graph side panel until the popup states are accepted.

## Craft Read-Only Panel

Fixture:

`Pending node: transition-card workbench needs acceptance evidence`

Route question:

`Is this a prototype review, implementation handoff, or blocked decision?`

Expected receipt:

`accepted Studio revision + screenshot/id coverage, no ledger write`

Required labels:

- `Read-only Craft view`
- `Draft routing answer - does not update ledger, close blocker, or change status`
- `Ledger path`
- `Freshness`
- `Pending by node`
- `Owner route`
- `Expected receipt`

Forbidden effects: direct ledger writes, blocker closure, status mutation, stale
hiding.

## Connective Task Manager

Defer full Connective until Craft is clear and manual fixture inputs exist.

When prototyped, require:

- `manual/user-supplied only` load or attention input;
- unknown indicators rendered as `Unknown`;
- user-run check freshness;
- recommended lane with reason;
- owner route;
- expected receipt.

Forbidden effects: surveillance, inferred human state, route override,
high-impact execution, Craft writes.

## Teammate Memo Window

Fixture:

- `To: Vlad`
- `From: Codex`
- `Type: start-work`
- `Status: open`
- `Why now: transition-card proof needs owner choice`
- `Open call: 4 choices or 6?`
- `Boundary: memo is not resolution`

Actions:

- `Draft reply`
- `Propose resolution`
- `Defer locally`

Receipt labels:

- `draft created`
- `not sent`
- `resolution proposed`
- `still open`

Forbidden effects: external send, impersonation, fake human answer, hidden
decision, canonical change.

## Intent-Latitude Annotation

Fixture text:

`Do not edit files; make the synthesis believable as a click-through prototype.`

Click path:

select span -> choose `literal`, `goal`, or `constraint` -> validator preview
-> draft verdict.

Required labels:

- `L0/report prototype`
- `draft verdict`
- `unenforced`
- `no mutation before approved task-session`

Forbidden effects: magic-marker enforcement, silent pass for unenforced spans,
`[goal]` or `[constraint]` promotion.

## Self-Assembling / Maintenance Approval

Keep this as an L0 approval storyboard unless an actual experiment-harness
receipt exists.

Fixture:

`This route miss happened 3 times. Build an L0 experiment?`

Required visible states:

1. `Friction evidence detected`
2. `Candidate proposed`
3. `Experiment draft`
4. `Run approval required - disabled unless experiment-harness receipt exists`
5. `Ready for human test`
6. `Promotion request`

Forbidden effects: self-consent, canonical write, criterion editing after
freeze, retry-until-green, shipped claim, promotion without owner approval.

Spell/sigil improvement nudges belong here as friction evidence, not as a
first-pass standalone package.

## Studio Acceptance Packet

Every package must produce a Studio acceptance packet.

L0 packet:

- isolated `STUDIO_DATA` path;
- session id;
- fixture text;
- stable `data-od-id` coverage list;
- CLI transcript through baseline/comment/synthesize/approve/apply/accept where
  applicable;
- stable-id comment log;
- screenshot set;
- accepted or staged revision reference;
- explicit local-review-only statement when `UI-SPEC.md` and `TEST-SPEC.md` are
  absent.

L1 packet:

- keyboard path;
- Escape and close behavior;
- focus behavior for popups/dialogs;
- accessible names and roles;
- disabled reasons exposed;
- color not used as the only state cue;
- axe report or equivalent accessibility check.

L2 packet:

- desktop and mobile screenshots;
- breakpoint bounding-box report;
- no overflow, clip, or overlap;
- target-size check for irreversible controls;
- popup/rail text fits without covering adjacent content.

Boundary packet:

- list of allowed effects;
- list of forbidden effects;
- owner route for each action;
- required human gate;
- expected receipt;
- confirmation that no canonical files, Craft ledgers, inventory/ontology
  entries, subagents, or host surfaces were mutated by the prototype.

## Studio Operating Command

Use the local direct `tsx` command path in this checkout if Corepack blocks
`pnpm studio`:

```bash
cd /home/vrondelli/projects/domainspec-core/projects/ui-prototyping-studio/backend
STUDIO_DATA=/tmp/ups-ide-ergonomics/studio.json \
STUDIO_DOCS_ROOT=/home/vrondelli/projects/domainspec-core \
./node_modules/.bin/tsx src/cli/studio.ts <command>
```

Use a fresh directory per run for `STUDIO_DATA`.

## Deferred

Host wrapper is deferred. Do not build command-palette, sidebar, code-lens, or
chat-action packaging until a specific host target is validated. The wrapper
should eventually expose accepted Studio sessions; it is not a standalone
product scene and must not contain a generic `run agent` button.
