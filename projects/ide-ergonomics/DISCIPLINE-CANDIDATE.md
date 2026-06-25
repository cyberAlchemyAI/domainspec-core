# Discipline Candidate: IDE Action Surface

Status: **formalized 2026-06-24** → see [disciplines/ide-action-surface.md](disciplines/ide-action-surface.md)
and the project catalog [disciplines/DISCIPLINES.md](disciplines/DISCIPLINES.md).
This file is the originating candidate, preserved for provenance.
Steward: Discipline Governance, with Necronomicon and Spellcraft as likely
workflow owners

## Purpose

Name the recurring practice of turning live conversation and artifact signals
into bounded IDE actions that preserve Arcanum ownership, gates, handoffs, and
receipts.

## Boundary

This discipline does not own canonical definitions, ontology promotion, spell
creation, sigil mutation, subagent execution, or IDE plugin implementation. It
only names the cross-capability practice and the quality bar for projecting it
into user-facing editor actions.

## Evidence

- `.arcanum/necronomicon/capabilities.json` - selected local capabilities already
  include the route owners needed for action cards.
- `arcanum/spells/necronomicon/README.md` - active interaction, side note queue,
  candidate knowledge, handoff, and gap models already exist.
- `arcanum/arcana/spellcraft/SKILL.md` - repeated multi-sigil actions already
  have a lifecycle owner.
- `arcanum/formulae/dispatch-spec/WEAVER-EXTRACTION.md` - bounded route menus,
  frames, handles, and audit traces are already named as dispatch lessons.
- `implementation/domainspec/PRODUCT-COMPONENTS-IDEA.md` - DomainSpec product
  thinking already requires action-bearing signals and session contribution to
  knowledge.
- `.arcanum/inventory/index.json` and `.arcanum/ontology-vault/` - repo-local
  knowledge surfaces already expose read-model entries that need reference,
  freshness, and authority display when surfaced in an IDE.
- `cyberAlchemy-v2/TO-VLAD/` - local addressed memos show how agent + human
  partnership handoffs can carry recipient, source, open calls, prompts,
  concrete edits, and resolution state.
- `.agents/skills/craft/SKILL.md`, `.agents/skills/interrogation/SKILL.md`,
  `.agents/skills/decision-gate/SKILL.md`, and `.agents/skills/refine/SKILL.md`
  - local native contracts define Craft pending-by-node state, one-question
  interviews, explainable decision choices, and Refine strategy proposals.
- `projects/arcanum-journey/CRAFT.md` - a live project already names Craft as a
  control surface and records route choices through Refine, Interrogation, and
  Decision Gate.
- `projects/ide-ergonomics/craft-control-panel/` - local control-panel primitive
  provides the work-state export and interactive route-choice substrate that the
  Connective task manager composes.
- `.codex/hooks.json` - command usage already opens and closes observer
  envelopes, proving a thin host-surface instrumentation path exists.

## Validation

- Mode: prose-review
- Check: this candidate stays project-local until `discipline-governance
  formalize` creates a card and catalog row.
- Latest result: not-run

## Quality Bar

A useful IDE action surface must:

- offer bounded route choices, not a generic tool list;
- cite the source span or artifact handle that triggered the action;
- show freshness and authority state for knowledge-entry references;
- preserve recipient, source, status, and open calls for teammate handoff memos;
- show Craft pending work by node and route selected items without mutating
  `.craft/ledger.yml` directly;
- keep attention and cognitive-load indicators opt-in, reviewable, and balanced
  against domain priority when recommending task execution;
- name the owning capability;
- distinguish candidate, handoff, execution, and promotion authority;
- show blocked or deferred fields;
- require explicit user approval before subagent fanout or mutation;
- write receipts or handoffs through the owning capability;
- keep observability gaps visible.

## Promotion Guardrail

Discipline evidence can recommend a route, but it cannot directly promote a
definition, ontology concept, spell, sigil, runtime surface, or product feature.

## Next Hardening Move

If this practice survives one or two concrete host-surface examples, route:

1. `discipline-governance formalize ide-action-surface`
2. `spellcraft design ide-assisted-arcanum-routing`
3. `invoke define` for the first host integration surface
4. `task-session` only after the design names validation evidence
