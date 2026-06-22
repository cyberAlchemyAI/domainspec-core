# Refine Seed Proposal: IDE Ergonomics

Status: strategy-proposal
Run ID: 20260619T171214Z-ide-ergonomics
Dispatch ID: refine-20260619T171214Z-ide-ergonomics
Target: `projects/ide-ergonomics`
Preset: standard
Research mode: no-research
Operator intent: Create a new project called `ide-ergonomics` and inspect the
DomainSpec Core plus Arcanum workflow to suggest IDE-side ergonomics.

## Target Resolution

The target project did not exist before this run. This pass creates a project
seed under:

```text
projects/ide-ergonomics/
```

This is a private parent-repository project. It may cite the public `arcanum`
submodule as source evidence, but it does not mutate public Arcanum canonical
files.

## Underlying Problem

Arcanum has strong capability contracts, but the user has to notice workflow
moments manually:

- a candidate definition appears;
- a side note should be captured;
- a handoff is ready;
- a subagent route could help;
- a repeated workflow should become a spell;
- a capability contract may need maintenance.

The IDE should make these moments visible as safe actions without pretending
that a button grants promotion or execution authority.

## Starting Hypothesis

Create an IDE Action Surface discipline and a Spellcraft candidate named
`ide-assisted-arcanum-routing`.

The product primitive is an action card over a conversation span or artifact
handle. Each action card names:

- source span;
- detected action kind;
- owning capability;
- authority class;
- route preview;
- required approval;
- handoff or receipt destination.

## Local Evidence

| Source | Relevance |
| --- | --- |
| `.arcanum/necronomicon/capabilities.json` | The local harness already has definitions, inventory, spellcraft, sigil-development, decision-gate, task-session, signal-observer, workflow-reflect, and invoke selected. |
| `arcanum/spells/necronomicon/README.md` | Active interaction, side note queue, candidate classification, gap ledger, and handoff semantics match the requested conversation ergonomics. |
| `arcanum/arcana/spellcraft/SKILL.md` | A repeated multi-sigil IDE workflow belongs to Spellcraft, not an overloaded single sigil. |
| `arcanum/formulae/dispatch-spec/WEAVER-EXTRACTION.md` | Bounded route menus, frames, handles, and audit traces map directly to IDE cards and popup previews. |
| `implementation/domainspec/PRODUCT-COMPONENTS-IDEA.md` | DomainSpec already wants action-bearing signals, Knowledge Graph IDE, Agentic Runtime, and session contribution back to knowledge. |
| `implementation/domainspec/docs/features/agent-execution-orchestrator/SPEC.md` | Explicit route composition, run lifecycle, telemetry envelopes, and signal emission already exist as DomainSpec feature concepts. |
| `implementation/domainspec/docs/features/knowledge-graph-visualization/SPEC.md` | Concept detail, definition pointers, graph edges, and navigation are existing product patterns for side panels and nodes. |
| `.codex/hooks.json` | Existing Codex hooks prove command-level observer envelopes can be attached to host interactions. |
| `arcanum/development/session-handoffs/20260612T163122Z-vscode-zoo-code-conversion-handoff.md` | Prior host-surface work shows that generated IDE/rules packages should be defined before implementation. |
| `arcanum/disciplines/DISCIPLINES.md` | Cross-capability practices can become discipline candidates before they become sigils or spells. |

## Candidate Features

1. Candidate definition action.
2. Side node capture.
3. Handoff composer popup.
4. Bounded route menu card.
5. Subagent fanout preview.
6. Spell or sigil improvement nudge.
7. Evidence and receipt rail.

## Proposed Route Menu

| Route | Use When | Owner |
| --- | --- | --- |
| IDE Action Surface discipline | The practice needs shared rules before implementation. | `discipline-governance` |
| IDE Assisted Arcanum Routing spell | The workflow should compose Necronomicon, Dispatch Spec, Definitions Governance, handoffs, and observability. | `spellcraft` |
| Host integration define/design | A real Codex/VS Code/Zoo Code/Cursor surface is selected. | `invoke` |
| Candidate definition button only | The first proof should be narrow and knowledge-focused. | `definitions-governance` plus Necronomicon |
| Subagent dispatch preview only | The first proof should focus on safe delegation. | `dispatch-spec` plus active owner |

Selected route for this seed: discipline plus spell candidate, with host
implementation deferred.

## Write Scope

Allowed now:

- project seed and recommendation artifacts under `projects/ide-ergonomics/`;
- local refinement strategy packet under this run folder.

Deferred:

- writing `.arcanum/spells/ide-assisted-arcanum-routing/README.md`;
- editing `arcanum/disciplines/DISCIPLINES.md`;
- editing canonical Arcanum sigils, spells, or definitions;
- generating host extension code;
- spawning subagents.

## Done Criteria For This Proposal Step

- Project folder exists.
- Repository evidence is summarized with concrete paths.
- Candidate IDE ergonomics are listed.
- Spellcraft-style candidate is drafted.
- Discipline candidate is drafted.
- Dispatch route validates.
- Runtime handoff records that subagents and execution require confirmation.
