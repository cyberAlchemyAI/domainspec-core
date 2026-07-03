# Relationship Types

> Implementation projection of the root relationship authority.

Machine authority:
`../../definitions/relationships/relationships.yml`

Human authority companion:
`../../definitions/relationships/relationships.md`

Validators read the root machine authority directly. This file exists as an implementation-facing view so
authors can inspect the relationship law without treating `impl/spec/` as the source of truth.

Current graph wording is `typed composable graph fragment`
(`../../definitions/DEFINITIONS.md#domainspec-v2-d19`), not full category law. A relationship is first-class
only if removing it changes at least one tracked non-collapse property:
reject/allow decision, derivation consequence, projection consequence, composition path consequence, owner
route consequence, or generated artifact consequence (`../../definitions/DEFINITIONS.md#domainspec-v2-d18`).

## Current Signature Count

Root authority defines 31 active relationship signatures.

This is a post-reconciliation count:

- `enforces-cross` is deprecated; use `enforces` with cross-feature scope metadata.
- `queries` is widened for read-capable behavioral sources.
- `applies` targets `Operation` and `Calculation`.
- `owns`, `belongs-to`, and first-class Saga orchestration are included.
- `depends-on`, Operation returns to Value Object, and Event payload/publisher split are recorded as residue.

## Backend Projection

| Signature | Notes |
| --- | --- |
| `Entity --[performs]--> Operation` | Actor/owner initiates behavior. |
| `Operation --[produces]--> Event` | Operation completion causes an event. |
| `Operation --[produces-for]--> Entity` | Cross-feature write/projection into an entity. |
| `Event --[triggers-cross]--> Operation` | Cross-feature activation. |
| `Rule --[enforces]--> Operation` | Rule gates operation execution; cross-feature is metadata. |
| `Calculation --[calculates]--> Operation` | Operation consumes a derived value. |
| `Event --[transitions]--> State Machine` | Event advances lifecycle. |
| `Interface --[exposes]--> Operation\|Query` | Interface exposes behavior. |
| `Workflow --[orchestrates]--> Operation[]` | Same-feature operation orchestration. |
| `Saga --[orchestrates]--> Operation[]` | Cross-feature orchestration with participant and compensation obligations. |
| `Policy --[applies]--> Operation\|Calculation` | Policy selects behavior. |
| `Mapping --[maps]--> Entity\|Interface` | Mapping transforms data across shapes. |
| `Entity --[contains]--> Value Object` | Entity embeds a value object. |
| `Query\|Calculation\|Operation --[queries]--> Entity` | Read-capable behavior reads entity data. |
| `Entity --[emits]--> Event` | Entity is the subject/source of an event. |
| `Entity --[owns]--> Entity` | Lifecycle, custody, or write-responsibility ownership. |
| `Entity --[belongs-to]--> Entity` | Membership, classification, or home assignment. |

## UI Projection

| Signature | Notes |
| --- | --- |
| `Page --[renders]--> Component[]` | Page renders components. |
| `Layout --[wraps]--> Page[]` | Layout wraps pages. |
| `Component --[composes]--> Component[]` | Component includes child components. |
| `Component --[consumes]--> Hook` | Component consumes state/data hook. |
| `Form --[submits]--> Action` | Form delegates to action. |
| `Adapter --[shapes]--> View Model` | Adapter returns render-ready data. |
| `Guard --[protects]--> Page` | Guard controls access. |
| `Component --[displays]--> View Model` | Component displays data. |

## Cross-Layer Projection

| Signature | Notes |
| --- | --- |
| `Binding --[fetches]--> Query` | UI binding fetches query data. |
| `Binding --[mutates]--> Operation` | UI binding invokes operation. |
| `State Indicator --[reflects]--> State Machine` | UI mirrors backend state. |
| `View Model --[derives]--> Entity` | View model derives from entity fields. |
| `Form --[contracts]--> Interface` | Form schema matches interface. |
| `Guard --[mirrors]--> Rule` | Client guard mirrors backend rule. |

## Entity Relations

`owns` and `belongs-to` are both first-class Entity-to-Entity signatures.

Use `owns` when the source entity has lifecycle authority, custody, containment authority, or write
responsibility over the target entity.

Use `belongs-to` when the source entity is a member of, classified by, or assigned to the target entity.

`owned-by` is a generated reverse-navigation view for `owns`; authors should not use it as a canonical
relationship row. `belongs-to` is not the inverse of `owns`.

`depends-on` remains deferred until a witness proves different validation behavior from a field-level
reference.

## Event Relations

Use `Operation --[produces]--> Event` when operation completion causes an event.

Use `Entity --[emits]--> Event` when the entity is the event subject/source.

`Operation --[emits]--> Event` is invalid.

## Registry Format

Aspect files declare graph rows in a flat table:

```markdown
## Feature Concept Graph

| From | Edge | To |
| --- | --- | --- |
| MaxAmountRule | enforces | ProcessPayment |
| ProcessPayment | produces | PaymentCompleted |
```

The validator resolves `From` and `To` through the same file's `Concept Registry`, then checks the triple
against root `relationships.yml`.
