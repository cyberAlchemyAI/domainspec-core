# CyberAlchemy v2 Definition Schemas

Status: active
Owner: definitions-governance
Canonical definitions source: [DEFINITIONS.md](DEFINITIONS.md)
Lookup index: [DEFINITIONS-INDEX.md](DEFINITIONS-INDEX.md)
Last updated: 2026-06-22

## Purpose

This registry tracks the schemas carried by canonical CyberAlchemy v2
definitions, so a definition's structural shape is kept *with* the definition and
is also discoverable as a first-class, trackable artifact. A schema here is a
documentary record of the shape a definition's formal voice asserts; a
machine-checkable validator is a deferred follow-up unless a row says otherwise.

## Rule

Every canonical definition that asserts a record, tuple, field set, or structural
contract in its formal voice must:

1. carry a colocated `### Schema` section in [DEFINITIONS.md](DEFINITIONS.md)
   with a stable schema handle bound to the definition ID and per-field meanings,
   and
2. appear as a row in **Tracked Schemas** below.

A definition whose formal voice is an equation or relation rather than a
structural record is reviewed case-by-case; an equation is tracked as a schema
only when it defines a structural contract consumers must satisfy. Schema changes
follow `CAV2-D25` schema amendment witness, and any coupling between a schema
field and another authority axis follows `CAV2-D16` typed coupling invariant.

## Schema handle convention

`<DEF-ID>-SCHEMA` for the primary schema of a definition;
`<DEF-ID>-SCHEMA-<n>` when a definition carries more than one.

## Tracked Schemas

| Schema handle | Definition | Term | Shape | Status | Witness |
| --- | --- | --- | --- | --- | --- |
| `CAV2-D23-SCHEMA` | [CAV2-D23](DEFINITIONS.md#cav2-d23-authority-lifecycle-axis) | authority lifecycle axis | `L(a) = (kind, status, evidence, commitment, provenance, owner, residue)` | tracked (documentary) | review; machine validator deferred |

## Backlog: schema-bearing definitions not yet tracked

These definitions assert record/tuple/structural shapes in their formal voice but
do not yet have a colocated `### Schema` section or a Tracked Schemas row. They
are queued for promotion into tracked schemas in a later definitions-governance
pass. This list is explicit so the gap is visible, not silently truncated.

| Definition | Term | Embedded shape (in Formal Interpretation) |
| --- | --- | --- |
| CAV2-D16 | typed coupling invariant | `R(A, B)` record: endpoints, relation type, direction, owner, evidence, effect |
| CAV2-D18 | residue | residue record: operation, preservation condition, remainder, type, evidence, owner, treatment |
| CAV2-D19 | ontology | `O_U = (N, E, B, R, C, P, G)` |
| CAV2-D20 | Craft method | `L_S = (C, B, E, D, G, A, N, R)` |
| CAV2-D21 | four-facet action method | `F(a) = (K_a, S_a, H_a, M_a, R_a)` |
| CAV2-D25 | schema amendment witness | `A = (owner, scope, source, delta, compatibility, witness, residue)` |
| CAV2-D26 | append-only event ledger | event record + `P(E) = fold(apply, initial_state, E)` |
| CAV2-D27 | residue entropy | `H(R) = sum negMulLog(rho(x))` / `S_f(m') = log |fiber_f(m')|` (equation — review whether it is a structural contract) |
| CAV2-D30 | bounded recursive self-application | recursive-step record: source, target, altitude, owner, gate, residue/state, recomposition, stop |
| CAV2-D32 | method | `M = (scope, inputs, actions, roles, gates, outputs, evidence, residue_rule, validation_rule, recomposition_rule, boundary)` |
| CAV2-D33 | definition | `Definition = (id, term, status, aliases, normative_voice, plain_language_voice, domain_context_voice, boundary, provenance_or_sources, consumers, index_entry, drift_route)` |
| CAV2-D34 | constitution | `Constitution = (id, scope, governed_artifact_class, structure_rules, invariants, composition_or_import_rules, owner_route, source_or_provenance, enforcement_or_witness, residue)` |
| CAV2-D35 | discipline | `Discipline = (id, name, trigger, practice, evidence, owner_route, hardening_route, source_or_provenance, residue)` |
| CAV2-D36 | decision | `Decision = (id, question, options_considered, chosen_option, rationale, owner_route, evidence, effect, status, residue)` |
| CAV2-D37 | spec | `Spec = (id, scope, contract_kind, interface_or_shape, obligations, validation_surface, owner_route, source_or_provenance, promotion_state, residue)` |

Definitions whose formal voice is a pure equation, predicate, or non-structural
relation — for example `CAV2-D17` reflection tower method, `CAV2-D28` value-cycle
edge guard, and `CAV2-D29` axis orthogonality invariant — are out of scope unless
a later review finds they assert a structural contract.

## Open Questions

### OQ-1. Documentary schema now, machine-checkable schema later?

Context: tracked schemas are currently documentary records colocated with their
definitions. `CAV2-D21` (machine-checkable view) and `CAV2-D25` (schema amendment
witness) point toward eventual validators. Recommendation: keep documentary
tracking as the baseline; promote a schema to machine-checkable form only when an
implementation or validation surface needs it, recording the witness here.
Status: OPEN.
