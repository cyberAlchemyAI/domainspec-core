---
tags: [ide, ergonomics, arcanum, domainspec, refinement, workflow]
node_type: project
is_session: false
layer: product, workflow, governance
nature: refinement-seed
status: strategy-proposal
created: 2026-06-19
---

# ide-ergonomics

Project seed for turning DomainSpec and Arcanum workflows into low-friction IDE
actions without weakening their governance boundaries.

This project is also a proof surface for the CyberAlchemy v2 value proposition:
synergetic cybernetic human-machine integration. The point is not only to expose
agent tools inside an editor; it is to help a person and machine stay in a shared
control loop where attention, evidence, owner routes, tests, handoffs, and domain
priority remain visible.

The project starts from a simple observation: Arcanum already has strong route
contracts, capability owners, handoff artifacts, definition governance,
subagent permission gates, and observability hooks. The ergonomic gap is that
users still have to recognize and invoke those flows manually while a
conversation is moving.

## Working Hypothesis

An IDE-side Arcanum action surface should detect actionable conversation spans
and offer bounded, owner-safe actions:

- a candidate term appears, so offer to create a definition candidate;
- a useful aside appears, so offer to capture a side node without interrupting
  the active flow;
- a workflow reaches handoff state, so offer a handoff composer with suggested
  destination and content;
- route ambiguity appears, so offer a bounded sigil or spell menu;
- subagent fanout would help, so show role cards, receipt requirements, and a
  permission gate;
- a recent inventory or ontology search matters again, so offer cached knowledge
  entry references with a file-reference-style popup;
- a governed token appears inline (a schema field, contract key, or definition ID
  such as `CAV2-D40`), so resolve it on hover into a read-only popover that points
  at its authoritative content without breaking flow;
- a teammate handoff exists or should be written, so open an addressed memo window
  with start prompt, open calls, source refs, and resolution state;
- Craft state exists, so show a control panel with pending nodes and route choices
  such as Interrogation, Decision Gate, Refine, export, or defer;
- Craft work, human attention, user-run checks, and domain priority all matter, so
  let Connective recommend the next execution lane with an explanation and receipt
  expectation;
- repeated route friction appears, so suggest a Spellcraft or Sigil Development
  maintenance path rather than silently changing a capability;
- the opportunity map itself has a high-value, evidenced candidate, so offer a
  button that suggests, self-assembles, and tests that improvement in isolation and
  notifies the user with a test to run and approve — never promoting it on its own.

## Source Evidence

| Source | Signal |
| --- | --- |
| `.arcanum/necronomicon/capabilities.json` | The local harness already selects routing, definitions, inventory, spellcraft, sigil-development, task-session, and observability capabilities. |
| `arcanum/spells/necronomicon/README.md` | Necronomicon already models active interactions, side notes, candidate knowledge, gap ledgers, and owner-safe handoffs. |
| `arcanum/arcana/spellcraft/SKILL.md` | Spellcraft owns composed multi-sigil workflows, phases, gates, handoffs, failure policy, and observability. |
| `arcanum/formulae/dispatch-spec/WEAVER-EXTRACTION.md` | Weaver extraction supplies the bounded route menu, safe frame, handle, trace, and DAG orchestration ideas. |
| `implementation/domainspec/PRODUCT-COMPONENTS-IDEA.md` | DomainSpec already names Knowledge Graph IDE, Agentic Runtime, Copilot/Skills Pack, action-bearing signals, and session contribution to knowledge. |
| `implementation/domainspec/docs/features/agent-execution-orchestrator/SPEC.md` | Existing DomainSpec feature evidence models explicit route composition, run lifecycle, telemetry envelopes, and signal emission. |
| `implementation/domainspec/docs/features/knowledge-graph-visualization/SPEC.md` | Existing DomainSpec feature evidence models whiteboard navigation, concept detail focus, definition pointers, and graph projection. |
| `.arcanum/inventory/index.json`, `.arcanum/inventory/index.md`, and `.arcanum/ontology-vault/map-2026-06-18-dispersed-knowledge.md` | Repo-local knowledge surfaces already expose inventory entries, EvidenceSets, ontology-map candidates, status, tags, source refs, and authority boundaries that an IDE can preview. |
| `cyberAlchemy-v2/TO-VLAD/` | Local teammate memo examples show addressed handoffs, next-session prompts, open calls, discussion drafts, and resolution records. |
| `cyberAlchemy-v2/VALUE-AND-PHILOSOPHY-PROPOSITION.md` | CyberAlchemy v2 frames these ergonomics as human-machine integration, not only tool interfaces. |
| `.agents/skills/craft/SKILL.md`, `.agents/skills/interrogation/SKILL.md`, `.agents/skills/decision-gate/SKILL.md`, and `.agents/skills/refine/SKILL.md` | Local native skill contracts define Craft state export, one-question interviews, decision gates with explain-more choices, and Refine strategy proposals before execution. |
| `projects/arcanum-journey/.craft/ledger.yml` and `projects/arcanum-journey/CRAFT.md` | A live project already frames Craft as the control surface and records route choices such as `/refine`, `/interrogation`, and decision-gated scoping. |
| [craft-control-panel/](craft-control-panel/README.md) | The local control-surface primitive gives Connective the read-first workbench shape: Craft state in, selected owner route out. |
| `.codex/hooks.json` and `.codex/hooks/arcanum-*.sh` | Codex hooks already open, update, and close observer envelopes around slash-command use. |
| `arcanum/development/session-handoffs/20260612T163122Z-vscode-zoo-code-conversion-handoff.md` | Prior host-surface planning showed how Arcanum can be projected into IDE-like tools while preserving canonical source authority. |
| `arcanum/disciplines/DISCIPLINES.md` | Arcanum already has a discipline layer for recurring cross-capability practices that are not yet sigils or spells. |

## Proposed Shape

The smallest useful first artifact is not an IDE plugin. It is an explicit
product and governance model for IDE action cards:

1. Define the action-card vocabulary and authority model.
2. Design a local spell candidate, `ide-assisted-arcanum-routing`, through
   Spellcraft.
3. Treat the recurring practice as a candidate discipline until there is usage
   evidence.
4. Treat Connective as the flagship composition: a task manager over Craft work,
   human attention, user-run checks, and domain priorities.
5. Later, implement one host integration as a narrow proof: likely a Codex IDE,
   VS Code-compatible extension, or project-local rules surface.

## Candidate UX Primitives

| Primitive | User-facing behavior | Owner-safe route |
| --- | --- | --- |
| Candidate definition action | Highlight a term and offer "Create definition candidate". | `definitions-governance` receives a candidate packet; no promotion by default. |
| Side node capture | Save an aside without changing the active task. | Necronomicon side-note queue plus optional inventory candidate. |
| Handoff composer | Button opens a popup with destination, summary, source refs, gaps, and next prompt. | Necronomicon or Invoke handoff, depending on lifecycle state. |
| Route menu card | Show 3-7 viable sigil or spell actions with short labels and boundaries. | `dispatch-spec` route menu, selected route recorded. |
| Subagent preview | Show role cards, join policy, receipt fields, and permission prompt. | `dispatch-spec` strategy plus explicit user approval before spawning. |
| Knowledge entry reference | Cache recent inventory/ontology searches and open a compact popup for a selected knowledge entry. | `inventory` or `ontology-vault` read model; can feed handoffs/context packs, but no promotion. |
| Referenced field hover popover | Hover a governed token (`valid_challenge_modes`, `CAV2-D40`, …) in a schema, doc, or chat and peek its authoritative content in place. | `definitions-governance`, schema/contract source, `inventory`/`ontology-vault` read model; read-only resolution, no promotion. |
| Teammate handoff memo | Open, draft, or resolve addressed agent + human handoff memos for a person, role, future session, or agent lane. | Handoff owner or `decision-gate`; no impersonation or silent decision closure. |
| Craft control panel | Export Craft state, show pending by node, and ask which route to take for a selected item. | `craft` read model first; selected owner route such as `interrogation`, `decision-gate`, or `refine` must produce proof. |
| Connective task manager | Rank next execution lanes by balancing Craft state, cognitive load, attention, user-run tests, and domain priority. | Recommendation only; selected owner route must confirm and produce a receipt. |
| Spell or sigil improvement nudge | Suggest maintenance when repeated friction appears. | `spellcraft`, `sigil-development`, or `sigil-maintenance-loop`; no silent mutation. |
| Self-assembling ergonomics action | A button that suggests its own next ergonomics improvement, assembles and tests it in isolation, then notifies the user with a test to approve. | `invoke` author → `spellcraft`/`sigil-development` drafts → `experiment-harness` test → `decision-gate` approval; assembled-and-green is never promoted without the user gate. |
| Evidence rail | Show handles, frames, receipts, and validation state beside the conversation. | `observability`, `signal-observer`, and owner-held artifacts. |
| Intent-latitude annotation | Mark a span of the user's own message as `[literal]`, `[goal]`, or `[constraint]` to signal how much latitude the agent has. | Post-hoc validator produces a draft latitude verdict; STRONG for `[literal]`, FLAG-grade for the rest. See [intent-latitude-tags/](intent-latitude-tags/README.md). |

## Project Files

- [PRODUCT-VIEW.md](PRODUCT-VIEW.md) - product-readable overview, MVP, test plan, and future direction.
- [IDE-ERGONOMICS-PRODUCT-VIEW.pdf](IDE-ERGONOMICS-PRODUCT-VIEW.pdf) - shareable PDF export of the product view.
- [ERGONOMICS-OPPORTUNITIES.md](ERGONOMICS-OPPORTUNITIES.md) - improvement map.
- [SPELL-IDE-ASSISTED-ARCANUM-ROUTING.md](SPELL-IDE-ASSISTED-ARCANUM-ROUTING.md) - Spellcraft-style spell candidate.
- [DISCIPLINE-CANDIDATE.md](DISCIPLINE-CANDIDATE.md) - discipline candidate for IDE action surfaces.
- [development/refinement-runs/20260619T171214Z-ide-ergonomics/](development/refinement-runs/20260619T171214Z-ide-ergonomics/) - local Refine strategy packet.
- [development/mvp-validation/20260619T172822Z-two-lane-mvp/MVP-TWO-LANE-PLAN.md](development/mvp-validation/20260619T172822Z-two-lane-mvp/MVP-TWO-LANE-PLAN.md) - two-lane MVP validation route.
- [development/mvp-validation/20260619T172822Z-two-lane-mvp/MVP-TWO-LANE-SYNTHESIS.md](development/mvp-validation/20260619T172822Z-two-lane-mvp/MVP-TWO-LANE-SYNTHESIS.md) - executed lane synthesis and MVP decision.
- [development/mvp-validation/20260619T172822Z-two-lane-mvp/MVP-NEXT-HANDOFF.md](development/mvp-validation/20260619T172822Z-two-lane-mvp/MVP-NEXT-HANDOFF.md) - next Invoke handoff for the selected MVP.
- [intent-latitude-tags/](intent-latitude-tags/README.md) - input-side primitive: user marks interpretation latitude (`[literal]`/`[goal]`/`[constraint]`) on their own message spans, enforced by a post-hoc validator. Research-backed; L0 PoC planned.
- [intent-latitude-tags/INTENT-LATITUDE-TAGS-PRODUCT-VIEW.pdf](intent-latitude-tags/INTENT-LATITUDE-TAGS-PRODUCT-VIEW.pdf) - shareable product-view brief for the intent-latitude-tags primitive; companion to [IDE-ERGONOMICS-PRODUCT-VIEW.pdf](IDE-ERGONOMICS-PRODUCT-VIEW.pdf).
- [knowledge-entry-references/](knowledge-entry-references/README.md) - knowledge-system primitive: cache recent inventory/ontology searches and reopen entries through source-aware reference popups.
- [teammate-handoff-memos/](teammate-handoff-memos/README.md) - collaboration primitive: open, draft, and resolve addressed teammate handoff memos, with a start-work check for relevant partner context.
- [craft-control-panel/](craft-control-panel/README.md) - control-surface primitive: export Craft state into a pending-by-node panel and route selected items through Interrogation, Decision Gate, Refine, export, or defer.
- [connective-task-manager/](connective-task-manager/README.md) - flagship primitive: task manager that balances Craft work, human attention, user-executed tests, and domain priorities to recommend the next execution lane.
- [self-assembling-ergonomics/](self-assembling-ergonomics/README.md) - meta primitive: a command/button that suggests its own next ergonomics improvement, assembles and tests it in an isolated candidate space, and notifies the user with a bounded test to run and approve before any promotion.

## Boundaries

- This project does not mutate `arcanum/` canonical sigils, spells,
  definitions, disciplines, or generated runtime packages.
- The first pass is repository-grounded strategy, not runtime proof.
- Any future reusable spell routes through Spellcraft.
- Any future sigil routes through Sigil Development.
- Any future definition promotion routes through Definitions Governance.
- Any future knowledge-entry reference surface remains read-only until an owner
  route explicitly turns a reference into a handoff, context pack, or candidate
  artifact.
- Any future teammate handoff surface must preserve recipient/source/status and
  cannot impersonate a human teammate or close human-owned decisions by itself.
- Any future Craft control panel must keep `.craft/ledger.yml` authoritative and
  route mutations through Craft or the selected owner capability with receipts.
- Any future Connective task manager must keep human indicators opt-in and
  reviewable, preserve domain priority, and treat recommendations as explainable
  choices rather than automatic execution.
- Any future self-assembling ergonomics action may suggest, assemble, and test
  autonomously but must keep assembly in an isolated candidate space and may not
  promote, install, or mutate any canonical capability or runtime before the user
  runs the delivered test and approves.
- Any future host integration needs its own validation evidence before it is
  treated as product-ready.
