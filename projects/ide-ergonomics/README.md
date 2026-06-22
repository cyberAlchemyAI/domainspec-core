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
- repeated route friction appears, so suggest a Spellcraft or Sigil Development
  maintenance path rather than silently changing a capability.

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
4. Later, implement one host integration as a narrow proof: likely a Codex IDE,
   VS Code-compatible extension, or project-local rules surface.

## Candidate UX Primitives

| Primitive | User-facing behavior | Owner-safe route |
| --- | --- | --- |
| Candidate definition action | Highlight a term and offer "Create definition candidate". | `definitions-governance` receives a candidate packet; no promotion by default. |
| Side node capture | Save an aside without changing the active task. | Necronomicon side-note queue plus optional inventory candidate. |
| Handoff composer | Button opens a popup with destination, summary, source refs, gaps, and next prompt. | Necronomicon or Invoke handoff, depending on lifecycle state. |
| Route menu card | Show 3-7 viable sigil or spell actions with short labels and boundaries. | `dispatch-spec` route menu, selected route recorded. |
| Subagent preview | Show role cards, join policy, receipt fields, and permission prompt. | `dispatch-spec` strategy plus explicit user approval before spawning. |
| Spell or sigil improvement nudge | Suggest maintenance when repeated friction appears. | `spellcraft`, `sigil-development`, or `sigil-maintenance-loop`; no silent mutation. |
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

## Boundaries

- This project does not mutate `arcanum/` canonical sigils, spells,
  definitions, disciplines, or generated runtime packages.
- The first pass is repository-grounded strategy, not runtime proof.
- Any future reusable spell routes through Spellcraft.
- Any future sigil routes through Sigil Development.
- Any future definition promotion routes through Definitions Governance.
- Any future host integration needs its own validation evidence before it is
  treated as product-ready.
