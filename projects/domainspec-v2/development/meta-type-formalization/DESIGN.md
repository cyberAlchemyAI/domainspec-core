---
node_type: design
is_session: false
status: candidate
created: 2026-07-01
authored_by: invoke (mode: design)
define: ./DEFINE.md
work_pack: ./WORK-PACK.md
target_artifact: meta-type formalization + content validator
promotion_boundary: PUBLIC validation criteria; engine δ-rules private.
---

# Design — Meta-Type Formalization

## 1. The per-type definition schema ("meta type value with its own category")

Each meta-type becomes a **card** carrying a checkable criterion, filed under its category:

```
### <TYPE>   (category: Structural | Behavioral | Connective | Lifecycle | UI-*)   [DS-D1.<n>]
- Formal criterion:   a concept is a well-formed <TYPE> IFF <checkable predicate over its content>
- Required structure: the tables/fields an aspect file must provide for this type
- Code pattern:       <from TAXONOMY "Architecture Mapping Appendix">
- Edge participation: may be SOURCE of {..}; may be TARGET of {..}   (the DS-D8 signature slice)
- Distinguisher:      how it differs from its nearest neighbour (from "Common Confusion")
- Fixtures:           positive (valid) + negative (malformed) — the discriminating pair
```

## 2. Category organization (the 25, by category)

- **Structural:** Entity, Value Object, Enum
- **Behavioral:** Operation, Query, Calculation, Rule, Policy, Workflow, Saga
- **Connective:** Interface, Event, Mapping
- **Lifecycle:** State Machine
- **UI-*** (deferred): Page, Layout, Component, View Model, Hook, Form, Action, Guard, Binding, Adapter, State Indicator

## 3. Worked exemplars (the shape — 3 concrete criteria)

**Entity (Structural).**
- Formal criterion: has ≥1 **identity field** (a field designating identity) AND fields are typed; MAY link a State Machine.
- Required structure: a field table `(name, type, required, description)` with an identity field.
- Edge participation: SOURCE of `performs, contains, emits`; TARGET of `queries, produces-for, derives`.
- Distinguisher vs Value Object: Entity **has identity**; VO is equal-by-fields.
- Negative fixture: a "field table, no identity field, has an Equality clause" → must be **rejected as Entity** (it's a VO).

**Rule (Behavioral).**
- Formal criterion: a **Formal cell that parses to a boolean predicate** over named inputs (no state mutation).
- Required structure: an `ID | Rule | Formal` row whose Formal expression is boolean-typed.
- Edge participation: SOURCE of `enforces` (+ `enforces-cross`); never a TARGET of `applies` (that's a Policy inbound). *(Governed by `domainspec-v2-D3`: `enforces` ≠ `applies`.)*
- Distinguisher vs Policy: Rule **blocks** (boolean); Policy **selects** (strategy).
- Negative fixture: a "Formal cell returning a chosen strategy/branch, not a boolean" → **rejected as Rule** (it's a Policy).

**Edge `enforces` (DS-D2/DS-D8).**
- Signature: `source.type = Rule ∧ target.type = Operation`.
- Check: both endpoints resolve to declared types matching the signature; else a violation.
- Negative fixture: `enforces` with a Calculation source → **rejected** (calculates, not enforces).

These show the shape: a criterion is a predicate over the aspect file's *structure* (tables/fields/Formal
cells) + the declared types — checkable without running the implementation.

## 4. The content validator (the enabling artifact)

```
validate-content(aspect_file, defs, edge_signatures):
  for each concept C with declared type T:
      run T.criterion over C's content  ->  pass | violation(C, T, reason)
  for each declared edge E(a --verb--> b):
      check verb.signature against type(a), type(b)  ->  pass | violation(E, reason)
  return { valid: bool, violations: [...] }
```

- **Owner:** validation-governance (it's a build-time fidelity check on the spec).
- **Relationship to existing tools:** *extends* `validate-relationships` (which already checks declared
  edges) with **per-type content criteria**; distinct from `engine lint` (canonical-tables + needs-formal)
  and from engine `derive` (the moat). This is the **type-and-edge content validator** the discussion named.
- **Boundary (DES-D2):** the engine's parser already recognizes per-type structure to *derive* tests; the
  validator's criteria are the **public contract** of "what a valid T is" — kept consistent with the engine
  but NOT importing the δ-rules. If a criterion can only be checked by running derivation, that's a
  boundary flag (FALSIFIED for that type per DEFINE), not a moat leak.

## 5. Design decisions surfaced

- **DES-D1 — where the formal criteria live.** (a) a **formal field in TAXONOMY.md** per type (single
  per-type home, upgraded from descriptive to formal) + a system-level `DS-D1` that cites it; or (b)
  per-type cards in `definitions/` (`DS-D1.<n>`). **Recommend (a)** — one per-type surface avoids drift;
  `definitions/DS-D1` becomes the governed "meta-type system" definition pointing at the formal TAXONOMY.
  The validator reads TAXONOMY's formal criteria. **Owner decision.**
- **DES-D2 — validator/engine boundary** (above): public criteria, private δ-rules; consistency, not duplication.
- **DES-D3 — criteria language.** Prose-predicate vs a small structured criterion DSL. Recommend
  **prose-predicate + a structural check in the validator** first (smallest-reliable); a criterion DSL only
  if the prose proves ambiguous.

## 6. Views coverage
Context (§1 schema) · Structure (§2 categories) · Data (the per-type cards + edge signatures) · Behavior
(§4 validator) · Alternatives (§5 DES-D1/D3) · Boundary (§4 DES-D2, engine moat).
