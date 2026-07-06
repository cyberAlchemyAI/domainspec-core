# IDE Ergonomics Studio Opportunity Prototypes - Research Evidence

Dispatch: `2026-07-01-ide-ergonomics-studio-opportunity-prototypes`
Date: 2026-07-01
Mode: read-only explorer evidence, then synthesis/review/write/audit

## Scope

The task is to determine how the opportunities in `projects/ide-ergonomics/`
should become prototype experiences using `projects/ui-prototyping-studio/`.
The user specifically wants the presentation/prototype to show what an end user
would experience, with click-driven next steps and popups, rather than slides
that describe abstract architecture.

## Explorer A - End-User Scene Matrix

Explorer A treated `ERGONOMICS-OPPORTUNITIES.md` as the opportunity list and
`PRODUCT-VIEW.md` as the shared product shape. The key distinction is between
standalone scenes and variants inside a shared transition-card suite.

| Opportunity | User visibly does in prototype | User receives | Scene type | Source |
| --- | --- | --- | --- | --- |
| Action-card model | Selects or accepts a detected chat span, then clicks a route card option. | Bounded route menu naming owner, preview artifact, permission, blocked actions. | Shared suite root | `PRODUCT-VIEW.md:127`, `ERGONOMICS-OPPORTUNITIES.md:12` |
| Candidate definition action | Highlights a term and clicks `Create candidate`. | Definition candidate packet with term, context, source span, destination; no promotion. | Variant in transition-card suite | `ERGONOMICS-OPPORTUNITIES.md:31`, `PRODUCT-VIEW.md:184` |
| Handoff composer popup | Clicks `Compose handoff draft`, chooses destination type. | Handoff artifact draft with summary, refs, gaps, blocked work, next prompt, checks. | Variant in transition-card suite | `ERGONOMICS-OPPORTUNITIES.md:62`, `PRODUCT-VIEW.md:190` |
| Side node capture | Clicks `Park as side node` on a tangent. | Saved aside classified as fact/research/definition/unblocker/contradiction/reminder/route gap; active flow stays put. | Variant in transition-card suite | `ERGONOMICS-OPPORTUNITIES.md:95`, `PRODUCT-VIEW.md:112` |
| Craft control panel | Opens Craft status, selects a pending node, answers one route question. | Owner-routed artifact, receipt, export, defer state, or blocked reason; Craft updates only by governed receipt. | Standalone scene sharing substrate with Connective | `ERGONOMICS-OPPORTUNITIES.md:297`, `PRODUCT-VIEW.md:99` |
| Connective task manager | Starts session, reviews candidates, enters optional attention/load snapshot, attaches a user-run check, chooses lane. | Ranked execution lanes with reasons, warnings, owner route, expected receipt. | Standalone flagship scene | `ERGONOMICS-OPPORTUNITIES.md:346`, `ERGONOMICS-OPPORTUNITIES.md:517` |
| Subagent fanout preview | Clicks `Preview delegated lanes`, reviews role cards, approves or declines. | Role/context/join-policy/receipt preview; if approved, spawned lanes and parent synthesis. | Variant in transition-card suite | `ERGONOMICS-OPPORTUNITIES.md:120`, `PRODUCT-VIEW.md:192` |
| Spell or sigil improvement nudge | Sees repeated route-miss nudge and clicks a maintenance route. | Draft maintenance path: Spellcraft, Sigil Development, Discipline Governance, or maintenance loop; no promotion. | Shared-suite variant after repeated evidence | `ERGONOMICS-OPPORTUNITIES.md:153`, `PRODUCT-VIEW.md:292` |
| Evidence and receipt rail | Opens side rail after route choice or run, clicks receipt/blocker/proposed item. | Visible trail of run evidence, proposed work, blocked fields, handoffs, next actions. | Shared suite infrastructure | `PRODUCT-VIEW.md:120`, `ERGONOMICS-OPPORTUNITIES.md:20` |
| Knowledge entry reference popup | Hovers/inserts `knowledge:<surface>/<handle>` or reopens a recent inventory/ontology result. | Popup with query, source surface, handle, snippet, status, freshness, authority boundary, safe actions. | Standalone reference micro-scene | `ERGONOMICS-OPPORTUNITIES.md:212`, `PRODUCT-VIEW.md:91` |
| Referenced field hover popover | Hovers `valid_challenge_modes`, `confidence_reference`, `CAV2-D40`, etc. | Read-only authoritative meaning, source boundary, confidence/status, open/copy/add actions, or unresolved/ambiguous marker. | Variant in reference suite | `ERGONOMICS-OPPORTUNITIES.md:397` |
| Teammate handoff memo window | At start-work or handoff boundary, chooses read/draft/reply/resolve/defer. | Addressed memo or resolution draft with recipient, why-now, open calls, next actions, boundaries. | Standalone scene related to handoff suite | `ERGONOMICS-OPPORTUNITIES.md:255`, `PRODUCT-VIEW.md:95` |
| Intent-latitude annotation | Selects span in own message and taps `[literal]`, `[goal]`, or `[constraint]`. | Annotated span plus validator preview and draft verdict; unenforced spans are flagged, not passed. | Standalone input-side scene | `ERGONOMICS-OPPORTUNITIES.md:173` |
| Self-assembling ergonomics action | Taps `Build this` on a scoped opportunity candidate, then later tests/approves or rejects. | Isolated candidate artifacts, frozen acceptance criterion, experiment verdict, and "ready for your test and approval" notification. | Standalone meta-scene | `ERGONOMICS-OPPORTUNITIES.md:454` |
| Knowledge graph side panel | Opens graph panel, clicks definition/handoff/route/evidence node. | Node detail with visible source pointers and related references; mainly navigation/understanding, not mutation. | Standalone side-panel scene sharing reference model | `ERGONOMICS-OPPORTUNITIES.md:26`, `ERGONOMICS-OPPORTUNITIES.md:449` |
| Host-surface package | Opens command palette/sidebar/code lens/chat action in a host shell. | Generated package surface exposing commands, sidebars, action providers, rules/modes; not itself the workflow artifact. | Delivery wrapper, not standalone product scene | `ERGONOMICS-OPPORTUNITIES.md:27`, `ERGONOMICS-OPPORTUNITIES.md:527` |

Explorer A conclusion:

- Standalone scenes: Craft control panel, Connective task manager, teammate memo
  window, intent-latitude annotation, self-assembling action, knowledge graph
  side panel.
- Shared-suite variants: candidate definition, handoff composer, side node,
  subagent preview, spell/sigil nudge, knowledge popup, referenced-field hover,
  evidence/receipt rail.
- The action-card model is the suite shell.
- The host-surface package is the wrapper that exposes the suite.

## Explorer B - Owner Boundary Matrix

Explorer B treated "opportunity" as the same priority map and cross-checked
against concrete README/SPEC folders where they exist. This pass focused on
what each prototype must label and what it must not imply.

| Opportunity | Prototype call | Owner boundary | Forbidden automatic effects | UI labels that must be visible |
| --- | --- | --- | --- | --- |
| Action-card model | Merge as common shell | `dispatch-spec` plus Necronomicon; every button preserves route ownership. | No canonical change, execution, or route switch without human gate. | Source span, route owner, allowed effect, gate required, expected receipt. |
| Candidate definition | Visible MVP | Definitions Governance candidate packet. | Must not write canonical definitions. | Detected term, local context, authority path, source handle, proposed destination, `candidate-not-canonical`. |
| Handoff composer | Visible MVP | Necronomicon plus Invoke owner-specific handoff. | Handoff is not execution proof. | Destination type, summary, source refs, unresolved gaps, blocked/deferred work, next prompt, validation checks. |
| Side node capture | Visible small action | Necronomicon side-note queue; active flow continues. | Cannot silently switch active route. | Side-node class, source span, active-route-unchanged, optional owner target. |
| Craft control panel | Visible prototype | Craft read model first; selected owner route produces receipt. | No direct ledger write, blocker closure, user-route selection, stale hiding. | Craft scope, ledger path, freshness, pending by node, selected row, route owner, `Explain / more context`, expected receipt. |
| Connective task manager | Prototype after Craft substrate; defer full runtime. | Craft plus host owner plus selected route owners. | No invented human indicators, surveillance, override, high-impact run without receipts, or Craft writes. | Craft rows, known/unknown/confirmed human indicators, user test freshness, domain priority, load warning, recommended lane, owner route, expected receipt. |
| Subagent fanout preview | Visible MVP | `dispatch-spec` plus active owner plus explicit user approval. | Runtime cannot spawn subagents without authorization. | Role cards, role ownership, visible context, join policy, receipt requirements, permission prompt, fallback. |
| Spell/sigil improvement nudge | Merge into action-card/evidence rail; defer standalone. | `spellcraft`, `sigil-development`, maintenance loop. | Must not author/promote reusable capability changes without owner approval. | Friction evidence, suggested owner route, draft-only state, approval required. |
| Evidence/receipt rail | Merge as cross-cutting rail; no standalone spec yet. | Observability plus signal-observer. | Must not blur proposed, run, blocked, or receipt states. | Ran/proposed/blocked, owner artifact, receipt ref, validation state, `dispatch_id`. |
| Knowledge entry reference | Visible prototype | Inventory/Ontology read model; promotion remains downstream. | No inventory/ontology edits, authority promotion, stale hiding, generic knowledge badge. | Handle, source surface, freshness, status, confidence, authority boundary, promotion owner, residue, refresh action. |
| Referenced field hover | Visible as hover variant; merge resolver with knowledge refs. | Definitions/schema/inventory resolver, read-only. | Never edit, fabricate, silently pick ambiguous source, or collapse authority classes. | Token kind, authoritative content, source surface, authority boundary, unresolved/ambiguous, no-edit actions. |
| Teammate handoff memo | Visible prototype | Handoff owner plus Decision Gate; owner decision remains explicit. | No external send, impersonation, fake human answer, hidden status, canonical change. | To/from, memo type, status, project scope, why now, open calls owner/status, boundaries, resolution/still open. |
| Intent-latitude annotation | Visible only as L0/report prototype; defer `[goal]`/`[constraint]` promotion. | Validator contract; DomainSpec v2 owner. | No magic-marker claim, no silent pass for unenforced spans, no mutation before approved task-session. | Tag, latitude, grounding strength, check class, verdict, `unenforced`, draft verdict, L0/PoC status. |
| Self-assembling ergonomics | High-risk gated prototype; defer autonomy beyond L0/L1. | Host plus Spellcraft/Sigil Development plus Decision Gate owner promotion. | No unevidenced suggestion, self-consent, canonical write, criterion edit, retry-until-green, shipped claim, direct promotion. | Map/friction evidence, scoped consent, candidate space, write allowlist, frozen criterion, verdict, `ready for test + approval`, promotion owner, receipt. |
| Knowledge graph side panel | Defer or merge with field-hover/knowledge refs. | Knowledge Graph IDE owner. | Avoid dashboard-only signal and authority collapse. | Node type, source surface, authority status, owner, source refs, unresolved state. |
| Host-surface package | Defer; packaging/internal until host validation. | `arcanum-bootstrap` or future host-surface capability. | No generic run-agent button; host specifics must be verified. | Host target, exposed commands/rules/sidebars, route menu bounds, source owner, validation evidence. |

Explorer B latent/internal coordinate conclusion:

- `dispatch-grammar-routing` should remain latent/internal: surfacing the full
  vocabulary is a failure mode.
- `restraint-floor` should not become a separate visible prototype; it is the
  boundary strip every prototype inherits.
- `lifecycle-progression` should appear only as a one-node work-arc label or
  receipt-debt cue for now; the full graph overbuilds the MVP.

## Explorer C - UI Prototyping Studio Operability Matrix

Explorer C evaluated how Studio itself wants the work shaped. Main conclusion:
the current IDE Ergonomics artifact is best operated as a Studio session
prototype, not as four separate variants. Variants fit visual/layout alternatives
inside a family; sessions fit multi-step outcome flows. Studio's own 1-3 variant
cap also makes "one variant per opportunity family" a poor fit.

Studio evidence basis:

- Studio loop: variant -> baseline -> annotate -> synthesize -> approve/stage
  or accept -> handoff.
- Preview captures `data-od-id` targets.
- Handoff is explicit/confirmed and is not source mutation.

| IDE Ergonomics family | Studio shape | Stable `data-od-id` targets | Preview annotations | Staged revision path | Acceptance evidence | Handoff feasibility |
| --- | --- | --- | --- | --- | --- | --- |
| Phrase to route card / evidence rail discovery | Session baseline; variants only for trigger/card alternatives. | `chat.hotphrase.evidence-rail`, `popover.route-card`, `popover.close`, `scenario.step.route`, `receipt.panel`. | Trigger discoverability, route-card copy, "preview only" boundary, route count. | Revise trigger affordance/card copy; `apply --candidate-from`, preview honest diff, `accept` or `discard`. | Screenshot/click proof: phrase opens card; comments bind to stable ids; keyboard/Escape and no-overlap checks. | High for prototype review; medium for implementation until UI/TEST specs and export profile exist. |
| Definition candidate capture | Session for artifact lifecycle; variant for packet layout alternatives. | `route.choice.candidate`, `modal.dialog`, `artifact.candidate`, `final.card.candidate`, `scenario.step.definition`. | "No promotion" wording, owner clarity, artifact state. | Revise modal/artifact copy or layout; accept staged candidate. | Save action reveals candidate artifact; final workbench shows candidate; boundary says no canonical promotion. | High as bounded design evidence; canonical definition promotion remains outside Studio. |
| Side-node / tangent parking | Session; variant only for side-node presentation. | `route.choice.side-node`, `artifact.side-node`, `final.card.side-node`, `scenario.step.side-node`. | "Active task stayed open," parked status, revisit timing. | Revise side-node modal/output rail; accept staged candidate. | Side-node artifact appears; copy preserves active-task boundary. | Medium: strong concept prototype, but real implementation needs target state/test spec. |
| Next-session handoff | Session, because it touches export semantics. | `route.choice.handoff`, `artifact.handoff`, `final.card.handoff`, `scenario.step.handoff`. | Restart prompt, open call, source refs, "handoff is not proof". | Revise handoff draft content; then export only after accepted revision with `handoff export --confirm --profile`. | Bundle should include session id, accepted revision, prototype path, id coverage, deviations, next task. | High once export profile plus UI-SPEC/TEST-SPEC exist; current bounded files are enough for local review, not full cross-project handoff. |
| Delegated-lane preview | Session-only for decision preview; not execution. | `route.choice.delegation`, `artifact.delegation`, `final.card.delegation`, `scenario.step.delegate`. | Approval-needed tag, role receipts, "no agents spawned" copy. | Revise preview/receipt cards only; actual delegation is downstream. | Modal shows role lanes; artifact says gated; receipt panel says recommendation is not permission. | Medium for decision framing; low/not feasible as actual delegation in Studio. |
| Durable workbench / output rail | Session summary; variant for final layout alternatives. | `artifact.rail`, `artifact.empty`, `artifact.*`, `final.workbench`, `final.card.*`, `receipt.panel`. | Output density, receipt caveats, final-state scanability. | Use accepted revision or `cycle exploit` for layout/copy refinements. | All four artifacts visible, final workbench shown, data-id coverage table, L1/L2 checks. | High as Studio acceptance packet; target app still needs real persistence/browser validation. |

Explorer C caveat:

- Dynamic modal field contents are not individually stamped with `data-od-id`
  today. Annotations can target `modal.dialog` plus route/artifact/final cards.
  If field-level feedback matters, add stable ids such as
  `modal.candidate.source-span`, `modal.handoff.open-call`, and
  `modal.delegation.role.validation` in the next candidate revision.

Explorer C command-path note:

- Docs use `pnpm studio ...`, but Corepack can fail in this checkout.
- The verified local CLI path is:

```bash
cd /home/vrondelli/projects/domainspec-core/projects/ui-prototyping-studio/backend
./node_modules/.bin/tsx src/cli/studio.ts
```

## Parent Initial Interpretation

The main strategy should not be "make one slide per opportunity." It should be:

1. Build one primary interactive session prototype around the phrase-to-route
   transition card and final workbench.
2. Use small variants only inside a session family, for example different route
   card copy, field-level modal layout, or final rail density.
3. Build separate Studio sessions only when the user task changes materially:
   reference lookup, teammate memo, Craft/Connective control, intent annotation,
   and self-assembling approval flow.
4. Defer host packaging and full graph/dashboard views until there is host
   validation and a clear implementation target.

