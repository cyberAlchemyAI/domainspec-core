# IDE Action Surface

Status: candidate
Steward: Discipline Governance (workflow owners: Spellcraft, Necronomicon)
Catalog: [DISCIPLINES.md](DISCIPLINES.md) (project-local, private-parent)
Formalized: 2026-06-24 (from [../DISCIPLINE-CANDIDATE.md](../DISCIPLINE-CANDIDATE.md))

## Purpose

Govern the recurring cross-capability practice of **turning live conversation and
artifact signals into bounded IDE actions that preserve Arcanum ownership, gates,
handoffs, and receipts.** Many capabilities (Necronomicon, Dispatch Spec, Craft,
Definitions Governance, Inventory) already produce surfaceable signals; this
discipline names the *quality bar and boundary* for projecting any of them into a
user-facing editor action, so each projection is bounded, owner-named, and
receipted rather than an unbounded "run agent" button.

A surface under this discipline carries three invariants its individual capabilities
do not coordinate on their own:

- **Bounded-route clause.** An action offers a small (3–7) menu of owner-named
  routes, never an open tool drawer. Each option names its owner, its artifact
  preview, its permission state, and what it will NOT do.
- **Capture-first clause.** A noticed signal is captured as a candidate (side note,
  opportunity, handoff draft) before any route switch or mutation — the Necronomicon
  "capture first, switch only on intent" rule lifted to the editor surface.
- **Candidate≠promotion clause (restraint floor).** An action may produce a
  candidate, draft, preview, or recorded intent, but never a canonical change,
  execution, or route switch without an explicit owner gate. This is the IDE
  Ergonomics restraint floor ([../UNIFIED-PRODUCT-VIEW.md](../UNIFIED-PRODUCT-VIEW.md)).

## Boundary

This discipline **names the operating practice** over IDE action surfaces. It does
**not** own canonical definitions, ontology promotion, spell creation, sigil
mutation, subagent execution, the coordinate model, or IDE plugin implementation.
It only names the cross-capability practice and the quality bar.

Mutation routes it hands off to:

- `spellcraft` — to author the reusable composition that runs the surface
  (`ide-assisted-arcanum-routing`); this discipline is that spell's **step-1 owner**
  per its own hardening route.
- `discipline-governance` — to advance/retire this discipline with named evidence.
- `decision-gate` + `constitution-governance` — to acknowledge that the surface (and
  any spell composing it) **promotes nothing of an un-enumerated authority kind**;
  every promotion routes to its owner (cav2 `AUTHORITY-MODEL.md` owner-route rule;
  `CAV2-D49` default-deny).
- `definitions-governance` — for any candidate term the surface produces (e.g. the
  absent "ergonomics" definition).
- the **coordinate model owner** (`PRODUCT-VIEW.md` / governance) — for admitting a
  new coordinate or primitive; this discipline never owns or invokes the
  coordinate-admission gate.

## Relation to other disciplines

- **`provisional-model-stewardship`** (cyberAlchemy-v2) governs the *coordinate model
  itself* (the IDE-ergonomics spine as a candidate frame with a completeness probe +
  evolution lifecycle). This discipline (`ide-action-surface`) governs the *action
  surfaces that feed and read that model*. They are siblings: one stewards the model,
  one stewards the surfaces. The coordinate-admission gate belongs to the model owner,
  not to this discipline.

## Evidence

- `arcanum/spells/necronomicon/README.md` — active interaction, side-note queue,
  candidate classification, handoff, gap models (cross-sigil evidence).
- `arcanum/formulae/dispatch-spec/WEAVER-EXTRACTION.md` — bounded route menus, frames,
  handles, audit traces as dispatch lessons (cross-sigil evidence).
- `arcanum/arcana/spellcraft/SKILL.md` — repeated multi-sigil actions have a lifecycle owner.
- `projects/ide-ergonomics/UNIFIED-PRODUCT-VIEW.md` — the restraint floor + coordinate
  space the surface is measured against.
- `projects/ide-ergonomics/ERGONOMICS-OPPORTUNITIES.md` — 12 documented action patterns,
  each with owner + guardrail (the practice in use).
- `projects/ide-ergonomics/OPPORTUNITY-INTAKE.md` + `opportunity-backlog.md` — the
  capture-first clause realized as a working on-ramp.
- `projects/ide-ergonomics/SPELL-IDE-ASSISTED-ARCANUM-ROUTING.md` — the step-2 spell candidate.

(Per discipline-governance v0.2.1, an `active-pattern` discipline must cite ≥1 evidence
ref outside its own owning sigil — satisfied above. Status stays `candidate` until the
spell + intake produce **usage** evidence, not just structural evidence.)

## Validation

- Mode: prose-review + catalog row.
- Check: stays project-local / private-parent; never routed into the public arcanum catalog.
- Latest result: formalized (card + row created 2026-06-24); usage-evidence: not-yet.

## Quality Bar

A useful IDE action surface must:

- offer bounded route choices (3–7), not a generic tool list;
- cite the source span or artifact handle that triggered the action;
- name the owning capability and distinguish candidate / handoff / execution / promotion authority;
- show freshness + authority state for knowledge-entry references;
- preserve recipient / source / status / open-calls for teammate handoff memos;
- show Craft pending work by node and route items without mutating `.craft/ledger.yml` directly;
- keep attention / cognitive-load indicators opt-in, reviewable, balanced against domain priority;
- require explicit user approval before subagent fanout or mutation;
- write receipts or handoffs through the owning capability;
- keep observability gaps visible;
- **promote nothing of an un-enumerated authority kind** — route every promotion to its owner.

## Promotion Guardrail

Discipline evidence can recommend a route, but it cannot directly promote a definition,
ontology concept, spell, sigil, runtime surface, coordinate, or product feature.

## Next Hardening Move

1. `spellcraft design ide-assisted-arcanum-routing` — author the step-2 spell (this revision).
2. `invoke define` for the first host-integration surface.
3. `task-session` after the design names validation evidence.
4. `discipline-governance promote ide-action-surface` to `active-pattern` once the spell
   + intake produce usage evidence (route misses, dismissals, receipts).
