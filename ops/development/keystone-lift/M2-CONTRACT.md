---
module: keystone-lift
docType: interface-contract
status: frozen
frozenAt: 2026-06-14
---

# M2-CONTRACT — Frozen DomainSpec spec interface

The stable interface every M2 capability consumes. **Frozen**: changes are versioned (bump `version`), never silent. Source of truth for the templates: `arcanum/spells/invoke/templates/domainspec-spec/`.

## 1. Concept Registry (consumed by: sync-registry C1, audit-alignment C6)
A table in `SPEC.md` with columns: `Concept | ID | Type`. `Type` MUST be a DS-D1 meta-type (canonical: `arcanum/definitions/DEFINITIONS.md#ds-d1-meta-type-system`). IDs are feature-scoped, stable.

## 2. Typed relationships (consumed by: sync-registry C1)
Edges expressed with DS-D2 verbs (canonical `#ds-d2-typed-relationship-system`): `From → To` + verb. Edge validity per DS-D8 signature.

## 3. Aspect docs (consumed by: test-derivation C3, obs-derivation C4, sync-user-stories C5)
Per-aspect files with these stable shapes:
- `operations.md` — Operation: type, actor, trigger, inputs, **rules**, **calculations**, **state transition**, **postconditions**, **error states**.
- `queries.md` — Query: inputs, filters, output shape, authz.
- `states.md` — State Machine: states + **transition table** (From, Event, To, guard).
- `events.md` — Event: name, payload, emitter.
- `interfaces.md` — Interface: endpoint/contract, exposure.
- `mappings.md` — Mapping: source shape → target shape.

## 4. Derivation anchors (consumed by: C3, C4)
Each derivable clause is addressable: `{aspect-file}#{anchor}`. C3/C4 content-address obligations as a function of (source anchor, rule type, canonical params) — see DS-D4 (private) for the derivation-function intent; C3 is built fresh per decision B3.

## Stability guarantees
- Column names, aspect filenames, and the transition-table shape are FROZEN.
- Adding an optional aspect doc is a minor version bump; changing an existing shape is major.
- Consumers MUST tolerate unknown extra columns/sections (forward-compat).

## Consumers gate (B-M2-1)
M2-C3/C4/C5 may not begin implementation until this contract is referenced as their input. Any required change here is a `decision-gate`, not an inline edit.
