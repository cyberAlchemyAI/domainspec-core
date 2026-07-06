---
node_type: reference
is_session: false
status: candidate
created: 2026-07-02
authored_by: task-session (M1 — spec-comprehension-model)
source:
  - ./  (the per-type schema+md cards — the 14 backend meta-types)
  - ../TAXONOMY.md  (the 25 meta-types, categories, "Backend Counterpart" shadow column)
  - ../../../definitions/relationships/relationships.yml  (root relationship authority — 31 signatures; the edge reading-view below)
  - ../../../development/spec-comprehension-model/{DESIGN.md,ORDER.md}  (M1)
  - ../../../development/comprehension-novice-test/stall-dataset.md  (S1 individuation, S6 feature/context, S9)
promotion_boundary: PUBLIC reading aid. Tiering is a LEARNING order, never a deletion — all 25 stay typed for the engine/validator. Proposed definitions (§4) promote to definitions-governance separately.
---

# Meta-type learning order — read this before authoring a spec

DomainSpec has **25** meta-types, but an author does not meet them all at once. This is a **learning
order**, not a new type system: every type below is still typed for the engine and validator. Tier is a
**per-domain declarable lens** (Evans/Vernon: the same subdomain is core or generic depending on what the
org does) — a UI-heavy product may promote UI types; a pure-backend service may leave them generic.

**Tier ≠ category.** Category (Structural/Behavioral/Connective/Lifecycle/UI) is *where a type lives in the
graph*; tier is *when you learn it*. Event is Connective by category but Core by tier.

## 1. The three tiers (all 25)

### CORE (6) — internalize these; one worked example each
| Type | One-line | Category |
| --- | --- | --- |
| **Entity** | has identity; tracked over time | Structural |
| **Value Object** | equal-by-fields; no identity | Structural |
| **Operation** | changes state | Behavioral |
| **Rule** | returns a boolean; blocks/allows | Behavioral |
| **State Machine** | states + transitions | Lifecycle |
| **Event** | announces something that already happened | Connective |

### SUPPORTING (6) — learn on demand, as "an X is a Y that…"
| Type | Learn it as… | Category |
| --- | --- | --- |
| **Enum** | a Value Object that is a finite value *set* | Structural |
| **Query** | an Operation that is **read-only** | Behavioral |
| **Calculation** | an Operation that **returns a value**, changes nothing | Behavioral |
| **Workflow** | orchestrates Operations **within one feature** | Behavioral |
| **Policy** | a Rule that **selects a strategy** instead of a boolean | Behavioral |
| **Interface** | an exposed boundary (what the outside can call) | Connective |

### GENERIC (13) — recognize + template; do not "learn" as vocabulary
- **Saga** — a Workflow that spans features (a *scope* modifier, `@cross`).
- **Mapping** — transforms fields between two shapes (has a direction).
- **The 11 UI types** — Page, Layout, Component, View Model, Hook, Form, Action, Guard, Binding, Adapter,
  State Indicator. Five are **shadows of a backend type** (see §2); the rest are UI-structure you template,
  not model. *(A UI-led domain may promote Form/Component/Page to Supporting via the declarable lens.)*

`6 core + 6 supporting + 13 generic = 25.` ✓

## 2. The 5 shadows — a one-line dictionary (but they keep their own edges)
Per TAXONOMY's own "Backend Counterpart" column, five UI types mirror a backend type. Learn them as a
lookup, **not** as new concepts — but note they are **first-class in the graph** (they carry edges their
backend twin does not; do not treat them as interchangeable):

| UI shadow | mirrors | its own edges (the root relationship authority) |
| --- | --- | --- |
| View Model | Value Object | `derives`←Entity, `displays`←Component, `shapes`←Adapter |
| Guard | Rule | `protects`→Page, `mirrors`→Rule |
| Binding | Interface | `fetches`→Query, `mutates`→Operation |
| Adapter | Mapping | `shapes`→View Model |
| State Indicator | State Machine / Enum | `reflects`→State Machine |

## 3. Edge reading-view (authority = the root relationship authority, NOT the card `edge_participation` slices)
> ⚠ The per-type `edge_participation` slices are known-inconsistent with the root relationship authority (novice stall S4,
> handed to R3). Until R3 reconciles them, **read edges from the root relationship authority.** Group the backend edges by
> what they express — with a `@cross` modifier for the cross-feature variants:

| Family | Base edge(s) | Reads as |
| --- | --- | --- |
| **actor** | `performs` | Entity does an Operation |
| **produce** | `produces` (→Event), `produces-for` (→Entity) | an Operation's output |
| **govern** | `enforces` (`@cross` = `enforces-cross`), `applies` | a Rule blocks / a Policy steers an Operation |
| **derive** | `calculates`, `queries` | a Calculation/Query reads to produce values |
| **structure** | `contains` | an Entity embeds a Value Object |
| **lifecycle** | `transitions` | an Event moves a State Machine |
| **announce** | `emits` (Entity→Event), `triggers-cross` (`@cross`) | events out / cross-feature triggers |
| **expose / map** | `exposes`, `maps` | an Interface publishes; a Mapping reshapes |

Modifiers: **`@cross`** = spans features (the `-cross` edges); **`@shadow`** = a UI mirror edge (§2).
*(This is a reading aid; the root relationship authority remains the source of truth and the validator's authority.)*

## 4. Two terms the surface never defined (proposed — promote via definitions-governance)
The novice could not resolve these from the surface; here are **working definitions** (S6, S1). These are
proposed for `definitions/DEFINITIONS.md` as DS-D terms — not yet canonical.

- **feature / bounded context** *(resolves the Workflow↔Saga axis, S6):* a **feature** is the unit a spec
  is authored for — one `impl/spec/features/<name>/` package with its own concept registry. **Intra-feature**
  = all concepts resolve inside one such package; **cross-feature** (`@cross`) = a relationship or process
  whose endpoints live in two different packages. So: Workflow = intra-feature orchestration; Saga =
  cross-feature. *(This is the operational meaning; a fuller DDD "bounded context" definition — a boundary
  of language consistency — is a definitions-governance decision.)*
- **concept individuation cue** *(where one concept/operation begins & ends, S1):* one **Entity** = one
  identity (one thing you'd reference by id). One **Operation** = one state-changing action with a single
  transactional outcome and a single trigger — **split** it when there are two independent outcomes or two
  distinct triggers; **merge** when two steps always succeed or fail together. Value-vs-computation: model
  the *result* as a Value Object and the *computing* as a Calculation only when the result is referenced on
  its own. *(A cue, not a decision procedure — individuation is genuinely a judgment; Evans concurs.)*

## 5. Boundary
Tiering reorganizes **learning emphasis**; it deletes nothing. **Completeness lives in the type system**
(the engine/validator ranges over all 25); **comprehensibility lives in this order.** The tier split is a
per-domain declarable lens. Adding a machine-readable `tier:` field to each `.schema.yml` is a **deferred**
follow-on — it must first confirm the schema validator accepts an optional field (else it regresses
`validate:*`). Until then, this doc is the authority for tier.
