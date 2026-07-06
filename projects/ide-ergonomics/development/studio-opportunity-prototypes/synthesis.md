# IDE Ergonomics Studio Opportunity Prototypes - Synthesis

Dispatch: `2026-07-01-ide-ergonomics-studio-opportunity-prototypes`
Inputs: `research.md`, local `projects/ide-ergonomics/` evidence, and
`projects/ui-prototyping-studio/` operating model.

## Strategy

Use UI Prototyping Studio as a session-prototype harness, not as a slide deck.
Variants should stay inside a session family for copy/layout alternatives.
Materially different user jobs should become separate sessions.

The current `projects/ui-prototyping-studio/ide-ergonomics-experience-prototype.html`
already fits the first package: a highlighted chat phrase opens a route card,
the user chooses an action, a preview popup appears, and saving creates durable
outputs in a workbench rail.

## Recommended Studio Packages

### 1. Transition Card Workbench

Included opportunities:

- Action-card model.
- Candidate definition.
- Side node.
- Handoff composer.
- Delegated-lane preview.
- Evidence/receipt rail.
- Spell/sigil improvement nudge as later friction evidence, not first-screen
  functionality.

End-user scene:

The user clicks a highlighted IDE-chat phrase and turns it into durable
workbench artifacts. The experience should feel like "this bit of conversation
can safely become work," not like a configuration dashboard.

Click path:

`chat.hotphrase.evidence-rail` -> `popover.route-card` ->
`route.choice.candidate|route.choice.side-node|route.choice.handoff|route.choice.delegation` ->
`modal.dialog` -> `artifact.*` -> `final.workbench`.

Key `data-od-id` targets:

- `chat.hotphrase.evidence-rail`
- `popover.route-card`
- `popover.close`
- `route.choice.candidate`
- `route.choice.side-node`
- `route.choice.handoff`
- `route.choice.delegation`
- `modal.dialog`
- `artifact.rail`
- `artifact.candidate`
- `artifact.side-node`
- `artifact.handoff`
- `artifact.delegation`
- `receipt.panel`
- `final.workbench`

Acceptance evidence:

- Phrase opens route card.
- Route card can close with X, Escape, and outside click where applicable.
- Route choices open realistic previews.
- Saving previews creates durable artifacts.
- Final workbench shows all saved outputs.
- Stable ids receive Studio annotations.
- Copy says preview/gated/no promotion/no agents spawned.
- Keyboard, focus, and no-overlap checks pass.

Out of scope:

- Canonical definition writes.
- Owner-route execution.
- Subagent spawning.
- Capability mutation.
- Treating a handoff as proof of execution.

### 2. Knowledge Reference Resolver

Included opportunities:

- Knowledge entry reference popup.
- Referenced-field hover popover.
- Lightweight knowledge graph side panel only as optional navigation.

End-user scene:

The user hovers or inserts a `knowledge:<surface>/<handle>` reference or a field
token and sees source, freshness, status, authority, and safe actions.

Click path:

Token/handle hover -> reference popup -> open/copy/add-to-handoff/refresh ->
optional graph node detail.

Key `data-od-id` targets:

- `reference.token.knowledge`
- `popover.knowledge-entry`
- `popover.field-reference`
- `reference.action.open`
- `reference.action.copy`
- `reference.action.add-to-handoff`
- `reference.action.refresh`
- `graph.panel`
- `graph.node.detail`
- `receipt.panel`

Acceptance evidence:

- Resolved, unresolved, and ambiguous states are visible.
- Authority boundary and promotion owner are named.
- Actions do not edit inventory or ontology.
- Comments attach to stable popup/panel ids.

Out of scope:

- Inventory/ontology writes.
- Authority promotion.
- Fabricated source choice.
- Turning the graph into the main product.

### 3. Craft + Connective Control

Included opportunities:

- Craft control panel.
- Connective task manager.
- Evidence/receipt rail.

End-user scene:

The user opens Craft status, selects a pending node, answers one route question,
optionally adds load/test context, and sees recommended execution lanes.

Click path:

Craft status -> pending row -> route question -> candidate lane -> expected
receipt.

Key `data-od-id` targets:

- `craft.panel`
- `craft.scope`
- `craft.row.pending`
- `craft.route-question`
- `connective.session-start`
- `connective.candidate-list`
- `connective.load-snapshot`
- `connective.user-check`
- `connective.lane.recommended`
- `receipt.panel`

Acceptance evidence:

- Ledger path, freshness, pending-by-node, owner route, known/unknown/confirmed
  human indicators, and expected receipt are visible.
- No direct ledger write occurs.
- Connective recommendations preserve uncertainty rather than inventing human
  state.

Out of scope:

- Full runtime.
- Surveillance-like load inference.
- Route override.
- High-impact execution.
- Craft writes without governed receipt.

### 4. Teammate Memo Window

Included opportunities:

- Teammate handoff memo.
- Start-work memo check.
- Memo reply/resolution/defer flow.

End-user scene:

At start-work or a handoff boundary, the user reviews addressed memos and drafts
a reply, resolution, or defer state.

Click path:

Start-work check -> memo list -> memo detail -> reply/resolve/defer -> receipt.

Key `data-od-id` targets:

- `memo.window`
- `memo.list`
- `memo.item.open`
- `memo.detail`
- `memo.action.reply`
- `memo.action.resolve-draft`
- `memo.action.defer`
- `memo.open-call`
- `receipt.panel`

Acceptance evidence:

- To/from, memo type, status, project scope, why-now, open calls, boundaries,
  and still-open/resolved state are visible.

Out of scope:

- External send.
- Impersonation.
- Fake human answers.
- Canonical changes.
- Hidden resolution.

### 5. Intent Latitude Annotation

Included opportunities:

- Literal/goal/constraint span tagging.

End-user scene:

The user marks a span in their own message before it becomes execution intent.

Click path:

Select span -> choose `literal|goal|constraint` -> validator preview -> draft
verdict.

Key `data-od-id` targets:

- `input.message`
- `intent.span.selected`
- `intent.tag.literal`
- `intent.tag.goal`
- `intent.tag.constraint`
- `validator.preview`
- `verdict.draft`
- `receipt.panel`

Acceptance evidence:

- Annotated spans remain visible.
- Unenforced spans are flagged.
- Validator preview is draft/L0 only.
- Screenshots cover keyboard and no-overlap behavior.

Out of scope:

- Magic-marker enforcement.
- `[goal]` or `[constraint]` promotion.
- Mutation before approved downstream task-session.

### 6. Self-Assembling / Maintenance Approval

Included opportunities:

- Self-assembling ergonomics action.
- Spell/sigil improvement nudge.

End-user scene:

Repeated friction creates a scoped "Build this" candidate. The user consents to
an allowlisted experiment and later approves or rejects the result.

Click path:

Friction nudge -> build-this -> consent/allowlist -> frozen criterion ->
experiment verdict -> ready for approval.

Key `data-od-id` targets:

- `friction.nudge`
- `action.build-this`
- `modal.consent`
- `candidate.space`
- `write.allowlist`
- `criterion.frozen`
- `verdict.experiment`
- `approval.ready`
- `receipt.panel`

Acceptance evidence:

- Friction evidence is shown.
- Criterion is frozen.
- No self-consent.
- No retry-until-green claim.
- Promotion owner and receipt are explicit.

Out of scope:

- Autonomy beyond L0/L1.
- Canonical writes.
- Shipped claims.
- Promotion without owner approval.

### 7. Host Surface Wrapper

Included opportunities:

- Command palette delivery.
- Sidebar delivery.
- Code lens delivery.
- Chat action delivery.

End-user scene:

The user invokes the same route-card packages from an IDE host surface.

Click path:

Host affordance -> route menu -> selected session package.

Key `data-od-id` targets:

- `host.command-palette`
- `host.sidebar`
- `host.codelens`
- `host.chat-action`
- `host.route-menu`

Acceptance evidence:

- Only after real host validation.
- Wrapper exposes bounded commands and preserves source owner/route limits.

Out of scope:

- First-pass product scene.
- Generic run-agent button.
- Unverified host-specific claims.

## Priority Order

1. Transition Card Workbench, because the checked-in IDE Ergonomics prototype
   already covers the flagship flow.
2. Knowledge Reference Resolver, because it is high-value, read-only, and
   owner-safe.
3. Teammate Memo Window, because it is concrete and pairs naturally with handoff
   artifacts.
4. Craft panel first, then Connective task manager after the Craft substrate is
   clear.
5. Intent Latitude Annotation as an L0/report prototype.
6. Self-Assembling / Maintenance Approval only as a tightly gated L0 experiment.
7. Host Surface Wrapper last, after host validation and implementation target
   decisions.

## Operability Caveats

- Studio proves click-through interaction, annotation, accessibility/layout
  basics, and handoff evidence. It does not prove production fitness.
- Use one to three variants only for alternatives inside a session; use separate
  sessions for different jobs.
- Dynamic modal fields are not individually stamped today. Add ids such as
  `modal.candidate.source-span`, `modal.handoff.open-call`, and
  `modal.delegation.role.validation` before field-level review.
- Use isolated `STUDIO_DATA` directories.
- `apply` stages; `accept` advances head.
- `handoff export --confirm` remains the terminal-only irreversible edge.
- Studio owns prototype evidence, not canonical specs, owner-route promotion,
  target app mutation, Craft ledger mutation, or agent execution.
- Cross-project handoff needs `UI-SPEC.md` and `TEST-SPEC.md`; without those,
  the result is local review evidence, not implementation authority.

