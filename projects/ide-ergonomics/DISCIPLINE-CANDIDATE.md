# Discipline Candidate: IDE Action Surface

Status: candidate
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
