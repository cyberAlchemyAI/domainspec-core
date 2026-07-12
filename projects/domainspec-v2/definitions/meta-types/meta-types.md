<!-- DomainSpec v2 — DS-D1 Meta-Type System (human cards). Linked from ../DEFINITIONS.md (#ds-d1-meta-type-system).
     Machine view: meta-types.yml. Per-type criterion: ../../impl/spec/meta-types/<category>/<type>.schema.yml.
     Scheme: DS-D* = the DomainSpec domain node/edge alphabet (distinct from this repo's governance/method scheme
     domainspec-v2-D*). INTERNAL/private. Each card keeps three voices. -->

# DS-D1 — Meta-Type System (definition cards)

Status: candidate (owner approval in progress, 1-by-1)
Owner: definitions-governance (domain-local)
Machine view: [meta-types.yml](./meta-types.yml) · Criterion per type: `../../impl/spec/meta-types/<category>/<type>.schema.yml`

**meta-type** = a candidate concept type in the DomainSpec node alphabet. The descriptive catalog names 24
candidates, but this authority surface currently carries cards only for 13 backend types. Each backend
card's Formal voice restates its `.schema.yml` criterion; Evidence links the schema (the machine source of
truth) + the TAXONOMY entry.

## Maturity Ledger

| Candidate slice | Current status | Authority boundary |
| --- | --- | --- |
| `DS-D1.1..9`, `DS-D1.11..14` backend | Shape/fixture-backed candidates; confirmation remains owner-gated and deeper semantic laws may still need hardening. | Schema presence proves checked shape, not full semantic authority; the explicit ID gap preserves later identities. |
| `DS-D1.15..25` UI | Formation-deferred; no cards or criterion schemas live in this authority surface. | Active DS-D8 endpoint use is evidence pressure only and does not promote DS-D1 formation. |

The deferred UI candidate trail remains in
[`development/meta-type-definitions/CANDIDATES.md`](../../development/meta-type-definitions/CANDIDATES.md).

---

## DS-D1.1 · Entity (Structural)

Source kind: domain-vocabulary; formalized (criterion in `entity.schema.yml`)

Evidence: [entity.schema.yml](../../impl/spec/meta-types/structural/entity.schema.yml) (machine criterion) ·
[TAXONOMY.md → Entity](../../impl/spec/TAXONOMY.md) (descriptive catalog)

Formal voice:

```text
Entity =
  a persisted, lifecycle-tracked domain object with a stable identity.
  well-formedness criterion (entity.schema.yml):
    identity   : >=1 field flagged identity  (bounded exists over the fields table)
    typedness  : every field declares a non-empty type
  two Entities with equal field values but different identity are DIFFERENT.
```

Plain-language voice: a thing you'd give an ID in a database and track over time — User, Order,
PaymentTransaction. Its sameness is its identity, not its field values.

Domain-context voice: the primary "actor" node in a DomainSpec aspect file; SOURCE of `belongs-to` /
`contains` / `emits` / `owns` / `performs`, TARGET of `belongs-to` / `derives` / `maps` / `owns` /
`produces-for` / `queries` (the DS-D8 edge slice). Checked by the content validator against
`entity.schema.yml`.

Use carefully: "identity" is a *declared* field flag (the `Identity` column), not inferred; an Entity MAY link
a State Machine but need not.

Misuse warning: a field table with no identity + an Equality clause is a Value Object, not an Entity — the
validator rejects it as Entity.

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; contradiction edge = "a concept
equal-by-fields that must still be tracked by a designated id" → challenges `identity`; owner route =
definitions-governance; resolution gate = owner decision + `entity.schema.yml` fixtures re-run; blocking
question = "must instances be told apart by a designated id, not by their values?"; residue → `definitions/reviews/`.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner approves +
`entity.schema.yml` pos/neg fixtures discriminate + criterion exercised on ≥1 real aspect concept; gate =
definitions-governance owner gate; status on confirm = candidate → active.

Promotion boundary: local domain vocabulary (DomainSpec v2); the criterion is the public schema, never the
engine δ-derivation (moat).

---

## DS-D1.2 · Value Object (Structural)

Source kind: domain-vocabulary; formalized (criterion in `value-object.schema.yml`)

Evidence: [value-object.schema.yml](../../impl/spec/meta-types/structural/value-object.schema.yml) (machine criterion) ·
[TAXONOMY.md → Value Object](../../impl/spec/TAXONOMY.md) (descriptive catalog)

Formal voice:

```text
Value Object =
  identity = the value itself (the full field tuple); NO designated identity field.
  well-formedness criterion (value-object.schema.yml):
    no_identity : no field is flagged identity  (identity is by value, not by a field)
    typedness   : every field declares a non-empty type
    equality    : the concept declares an Equality clause
  equal fields => equal value (there is no id to distinguish two equal instances).
```

Plain-language voice: Money is the clearest case — any $5 equals any other $5. Two Money are the same when
their amount + currency match; there's no serial number to chase. Sameness is by *content*, not a tracked id —
that's what makes it a Value Object.

Domain-context voice: the reusable value pieces embedded inside Entities and shared across features — `Money`
on a Payment, `Address` on a User. It has fields but no lifecycle and no state machine; TARGET of `contains`
under DS-D8. Checked by the content validator against `value-object.schema.yml`.

Use carefully: equality is a *declared* clause (a prose marker), not proven semantic equality.

Misuse warning: if instances must be told apart by a *designated* id (not by their values), it's an **Entity**
— the validator rejects it as Value Object.

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; contradiction edge = "an instance
equal-by-fields that must still be tracked by a designated id" → challenges `no_identity`; owner route =
definitions-governance; resolution gate = owner decision + `value-object.schema.yml` fixtures re-run; blocking
question = "does any instance need a designated id to be distinguished?"; residue → `definitions/reviews/`.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner approves +
`value-object.schema.yml` pos/neg fixtures discriminate + criterion exercised on ≥1 real aspect concept; gate =
definitions-governance owner gate; status on confirm = candidate → active.

Promotion boundary: local domain vocabulary (DomainSpec v2); the criterion is the public schema, never the
engine δ-derivation (moat).

---

## DS-D1.3 · Enum (Structural)

Source kind: domain-vocabulary; formalized (criterion in `enum.schema.yml`)

Evidence: [enum.schema.yml](../../impl/spec/meta-types/structural/enum.schema.yml) (machine criterion) ·
[TAXONOMY.md → Enum](../../impl/spec/TAXONOMY.md) (descriptive catalog)

Formal voice:

```text
Enum =
  a fixed, finite set of named values.
  well-formedness criterion (enum.schema.yml):
    value_table : provides a table with a `Value` column and >=1 row
  no typed field table, no identity — a closed value list, not an object.
```

Plain-language voice: the allowed-values guardrail on a field — a fixed, closed set with nothing in between.
`PaymentMethod` is exactly {CREDIT_CARD, BANK_TRANSFER, WALLET}, so a field typed by it can't hold a typo or a
fourth option nobody defined. If you can write out every value and it almost never grows, it's an enum.

Domain-context voice: constrains what a field may hold and drives per-value branching; no active DS-D8
relationship signatures currently target or source Enum. Checked by the content validator against
`enum.schema.yml`.

Use carefully: "finite + rarely-changes" is the intent; a set that grows constantly is data, not an enum.

Misuse warning: if it moves through states/transitions it's a **State Machine**; if its values carry typed
fields it's an **Entity / Value Object** — the validator rejects a field-table declared as Enum.

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; edge = "a set whose values must
carry fields or transitions" → challenges `value_table`; owner route = definitions-governance; gate = owner
decision + `enum.schema.yml` fixtures re-run; blocking question = "closed value list, or does each value carry
structure/lifecycle?"; residue → `definitions/reviews/`.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner approves +
`enum.schema.yml` fixtures discriminate + criterion exercised on ≥1 real aspect concept; gate =
definitions-governance owner gate; status on confirm = candidate → active.

Promotion boundary: local domain vocabulary (DomainSpec v2); the criterion is the public schema, never the
engine δ-derivation (moat).

---

## DS-D1.4 · Operation (Behavioral)

Source kind: domain-vocabulary; formalized (criterion in `operation.schema.yml`)

Evidence: [operation.schema.yml](../../impl/spec/meta-types/behavioral/operation.schema.yml) (machine criterion) ·
[TAXONOMY.md → Operation](../../impl/spec/TAXONOMY.md) (descriptive catalog)

Formal voice:

```text
Operation =
  a state-changing business action (the write side).
  well-formedness criterion (operation.schema.yml):
    writes_state : declares state_change = yes  (in the Attribute | Value table)
  validates input, checks rules, transitions entities, emits events.
```

Plain-language voice: a verb that leaves a mark — after it runs, the world is different: a payment charged, an
order cancelled. Not a plain CRUD "update"; a named action with business meaning and postconditions.

Domain-context voice: the write-side node; SOURCE of `produces` / `produces-for` / `queries`, TARGET of
`applies` / `calculates` / `enforces` / `exposes` / `mutates` / `orchestrates` / `performs` /
`triggers-cross`. Checked by the content validator against `operation.schema.yml`.

Use carefully: `state_change` is the *declared* attribute (the `Attribute | Value` table), not inferred from a body.

Misuse warning: if it declares `state_change = no` (read-only, returns a view), it's a **Query** — the
validator rejects it as Operation.

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; edge = "a read-only action
mislabeled as state-changing" → challenges `writes_state`; owner route = definitions-governance; gate = owner
decision + `operation.schema.yml` fixtures re-run; blocking question = "does it actually mutate entity state,
or only read?"; residue → `definitions/reviews/`.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner approves +
`operation.schema.yml` fixtures discriminate + criterion exercised on ≥1 real aspect concept; gate =
definitions-governance owner gate; status on confirm = candidate → active.

Promotion boundary: local domain vocabulary (DomainSpec v2); the criterion is the public schema, never the
engine δ-derivation (moat).

---

## DS-D1.5 · Query (Behavioral)

Source kind: domain-vocabulary; formalized (criterion in `query.schema.yml`)

Evidence: [query.schema.yml](../../impl/spec/meta-types/behavioral/query.schema.yml) (machine criterion) ·
[TAXONOMY.md → Query](../../impl/spec/TAXONOMY.md) (descriptive catalog)

Formal voice:

```text
Query =
  a read-only retrieval (the read side).
  well-formedness criterion (query.schema.yml):
    read_only : declares state_change = no  (in the Attribute | Value table)
  returns a view; same inputs => same result; no mutation.
```

Plain-language voice: a question, not an action — ask it twice and get the same answer, with no side effects.
It defines what consumers may ask for, with which filters, in what shape.

Domain-context voice: the read-side node; SOURCE of `queries`, TARGET of `exposes` / `fetches` under DS-D8.
Checked by the content validator against `query.schema.yml`.

Use carefully: `state_change` is the *declared* attribute (the `Attribute | Value` table), not inferred.

Misuse warning: if it declares `state_change = yes` (mutates), it's an **Operation** — the validator rejects
it as Query.

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; edge = "an action that mutates
state mislabeled as read-only" → challenges `read_only`; owner route = definitions-governance; gate = owner
decision + `query.schema.yml` fixtures re-run; blocking question = "does calling it change anything?"; residue
→ `definitions/reviews/`.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner approves +
`query.schema.yml` fixtures discriminate + criterion exercised on ≥1 real aspect concept; gate =
definitions-governance owner gate; status on confirm = candidate → active.

Promotion boundary: local domain vocabulary (DomainSpec v2); the criterion is the public schema, never the
engine δ-derivation (moat).

---

## DS-D1.6 · Calculation (Behavioral)

Source kind: domain-vocabulary; formalized (criterion in `calculation.schema.yml`)

Evidence: [calculation.schema.yml](../../impl/spec/meta-types/behavioral/calculation.schema.yml) (machine criterion) ·
[TAXONOMY.md → Calculation](../../impl/spec/TAXONOMY.md) (descriptive catalog)

Formal voice:

```text
Calculation =
  a pure function that derives a value from inputs.
  well-formedness criterion (calculation.schema.yml):
    returns_value : declares formal_return_type = value  (in the Attribute | Value table)
  deterministic; same inputs => same value; no state change.
```

Plain-language voice: a formula with a name — same inputs, same output, every time. FeeCalculation =
amount × rate. No state, no side effects; just a value out.

Domain-context voice: SOURCE of `calculates` / `queries`, TARGET of `applies`. Checked by the content
validator against `calculation.schema.yml`.

Use carefully: `formal_return_type` is the *declared* attribute (the `Attribute | Value` table), not inferred
by evaluating the formula.

Misuse warning: if it declares `formal_return_type = boolean` (a yes/no guard), it's a **Rule** — the
validator rejects it as Calculation.

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; edge = "a boolean guard
mislabeled as returning a value" → challenges `returns_value`; owner route = definitions-governance; gate =
owner decision + `calculation.schema.yml` fixtures re-run; blocking question = "does it return a value, or a
yes/no?"; residue → `definitions/reviews/`.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner approves +
`calculation.schema.yml` fixtures discriminate + criterion exercised on ≥1 real aspect concept; gate =
definitions-governance owner gate; status on confirm = candidate → active.

Promotion boundary: local domain vocabulary (DomainSpec v2); the criterion is the public schema, never the
engine δ-derivation (moat).

---

## DS-D1.7 · Rule (Behavioral)

Source kind: domain-vocabulary; formalized (criterion in `rule.schema.yml`)

Evidence: [rule.schema.yml](../../impl/spec/meta-types/behavioral/rule.schema.yml) (machine criterion) ·
[TAXONOMY.md → Rule](../../impl/spec/TAXONOMY.md) (descriptive catalog)

Formal voice:

```text
Rule =
  a boolean guard on an operation (blocks / allows).
  well-formedness criterion (rule.schema.yml):
    boolean_predicate : declares formal_return_type = boolean  (in the Attribute | Value table)
  the boolean-ness is DECLARED, never parsed from the Formal cell (that is the engine moat).
```

Plain-language voice: a business constraint with a formal boolean expression — unambiguous and directly
testable. It guards state transitions: the condition under which an operation may execute.

Domain-context voice: SOURCE of `enforces`, TARGET of `mirrors`; **never** a TARGET of `applies` (that is a
Policy inbound; per `domainspec-v2-D3`). Checked by the content validator against `rule.schema.yml`.

Use carefully: `formal_return_type` is the *declared* attribute (the `Attribute | Value` table); a Rule
**blocks** (boolean), it does not select.

Misuse warning: if it declares `formal_return_type = strategy` (selects a branch), it's a **Policy** — the
validator rejects it as Rule.

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; edge = "a strategy-selector
mislabeled as a boolean guard" → challenges `boolean_predicate`; owner route = definitions-governance; gate =
owner decision + `rule.schema.yml` fixtures re-run; blocking question = "does it block/allow (boolean), or
select a strategy?"; residue → `definitions/reviews/`.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner approves +
`rule.schema.yml` fixtures discriminate + criterion exercised on ≥1 real aspect concept; gate =
definitions-governance owner gate; status on confirm = candidate → active.

Promotion boundary: local domain vocabulary (DomainSpec v2); the criterion is the public schema, never the
engine δ-derivation (moat).

---

## DS-D1.8 · Policy (Behavioral)

Source kind: domain-vocabulary; formalized (criterion in `policy.schema.yml`)

Evidence: [policy.schema.yml](../../impl/spec/meta-types/behavioral/policy.schema.yml) (machine criterion) ·
[TAXONOMY.md → Policy](../../impl/spec/TAXONOMY.md) (descriptive catalog)

Formal voice:

```text
Policy =
  decision logic that selects a strategy/branch (chooses how, not whether).
  well-formedness criterion (policy.schema.yml):
    selects_strategy : declares formal_return_type = strategy  (in the Attribute | Value table)
  conditions => a selected behavior (not a boolean block/allow).
```

Plain-language voice: encodes business strategy, often configurable — conditions → a selected behavior.
Change the policy, change the choice, without touching the operation.

Domain-context voice: SOURCE of `applies` (a Policy applies to Operations/Calculations; the widened
`applies : Policy → {Operation, Calculation}` per `domainspec-v2-D3`). Checked by the content validator
against `policy.schema.yml`.

Use carefully: `formal_return_type` is the *declared* attribute (the `Attribute | Value` table); a Policy
**selects**, it does not block.

Misuse warning: if it declares `formal_return_type = boolean` (blocks/allows), it's a **Rule** — the
validator rejects it as Policy.

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; edge = "a boolean guard
mislabeled as selecting a strategy" → challenges `selects_strategy`; owner route = definitions-governance;
gate = owner decision + `policy.schema.yml` fixtures re-run; blocking question = "does it choose among
behaviors, or block/allow?"; residue → `definitions/reviews/`.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner approves +
`policy.schema.yml` fixtures discriminate + criterion exercised on ≥1 real aspect concept; gate =
definitions-governance owner gate; status on confirm = candidate → active.

Promotion boundary: local domain vocabulary (DomainSpec v2); the criterion is the public schema, never the
engine δ-derivation (moat).

---

## DS-D1.9 · Workflow (Behavioral)

Source kind: domain-vocabulary; formalized (criterion in `workflow.schema.yml`)

Evidence: [workflow.schema.yml](../../impl/spec/meta-types/behavioral/workflow.schema.yml) (machine criterion) ·
[TAXONOMY.md → Workflow](../../impl/spec/TAXONOMY.md) (descriptive catalog)

Formal voice:

```text
Workflow =
  multi-step orchestration of operations within or across feature boundaries.
  authority criterion (workflow.schema.yml implementation follows in SGRM-003/004):
    admitted_scope : declares scope in {intra-feature, cross-feature}
                     (in the Attribute | Value table)
  ordered steps with one declared ownership-boundary scope.
```

Plain-language voice: coordinates several ordered operations across time. The declared scope says whether the
coordination stays inside one feature or crosses feature boundaries.

Domain-context voice: SOURCE of `orchestrates` for same-feature or cross-feature Operation coordination; no
active DS-D8 target signatures. The content-validator implementation is migrated in SGRM-003/004.

Use carefully: `scope` is the *declared* attribute (the `Attribute | Value` table), not an inferred structural
witness. Its admitted values are `intra-feature` and `cross-feature`.

Misuse warning: a missing, empty, or unknown scope is not a valid Workflow declaration.

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; edge = "an orchestration with
missing or unknown scope" → challenges `admitted_scope`; owner route =
definitions-governance; gate = owner decision + `workflow.schema.yml` fixtures re-run; blocking question =
"does it declare exactly one admitted ownership-boundary scope?"; residue → `definitions/reviews/`.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner approves +
`workflow.schema.yml` fixtures discriminate + criterion exercised on ≥1 real aspect concept; gate =
definitions-governance owner gate; status on confirm = candidate → active.

Promotion boundary: local domain vocabulary (DomainSpec v2); the criterion is the public schema, never the
engine δ-derivation (moat).

---

## DS-D1.11 · Interface (Connective)

Source kind: domain-vocabulary; formalized (criterion in `interface.schema.yml`)

Evidence: [interface.schema.yml](../../impl/spec/meta-types/connective/interface.schema.yml) (machine criterion) ·
[TAXONOMY.md → Interface](../../impl/spec/TAXONOMY.md) (descriptive catalog)

Formal voice:

```text
Interface =
  an API boundary exposing operations/queries to consumers.
  well-formedness criterion (interface.schema.yml):
    declares_boundary : declares interface_kind (external | internal)  (in the Attribute | Value table)
  documents request/response shapes + how they map to domain concepts.
```

Plain-language voice: a typed contract at a system edge — what a consumer may call, with what payload, and
what comes back. External (METHOD + path) or internal (a method signature).

Domain-context voice: the boundary node exposing the domain to consumers; SOURCE of `exposes`, TARGET of
`contracts` / `maps` under DS-D8. Checked by the content validator against `interface.schema.yml`.

Use carefully: `interface_kind` is a *declared* attribute (the `Attribute | Value` table); any value
(`external` / `internal`) present satisfies it.

Misuse warning: a field-by-field transform between two shapes is a **Mapping**, not an Interface — an
Interface must declare `interface_kind`.

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; edge = "a field transform
mislabeled as a boundary" → challenges `declares_boundary`; owner route = definitions-governance; gate = owner
decision + `interface.schema.yml` fixtures re-run; blocking question = "is it an exposed boundary, or a shape
transform?"; residue → `definitions/reviews/`.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner approves +
`interface.schema.yml` fixtures discriminate + criterion exercised on ≥1 real aspect concept; gate =
definitions-governance owner gate; status on confirm = candidate → active.

Promotion boundary: local domain vocabulary (DomainSpec v2); the criterion is the public schema, never the
engine δ-derivation (moat).

---

## DS-D1.12 · Event (Connective)

Source kind: domain-vocabulary; formalized (criterion in `event.schema.yml`)

Evidence: [event.schema.yml](../../impl/spec/meta-types/connective/event.schema.yml) (machine criterion) ·
[TAXONOMY.md → Event](../../impl/spec/TAXONOMY.md) (descriptive catalog)

Formal voice:

```text
Event =
  a past-tense notification of a domain state change.
  well-formedness criterion (event.schema.yml):
    past_tense : declares temporal = past  (in the Attribute | Value table)
  a typed payload + consumers; decouples what happened from who reacts.
```

Plain-language voice: a past fact about the system's state — something that already happened
(PaymentCompleted, OrderShipped), broadcast so other parts can react without the emitter knowing them.

Domain-context voice: SOURCE of `transitions` / `triggers-cross`, TARGET of `emits` / `produces` under DS-D8.
Checked by the content validator against `event.schema.yml`.

Use carefully: `temporal` is the *declared* attribute (the `Attribute | Value` table); an Event names what
already happened, not a request.

Misuse warning: if it declares `temporal = present` (a request to make something happen), it's an
**Operation/command** — the validator rejects it as Event.

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; edge = "a present-tense command
mislabeled as an event" → challenges `past_tense`; owner route = definitions-governance; gate = owner decision
+ `event.schema.yml` fixtures re-run; blocking question = "does it name something that already happened, or
request something to happen?"; residue → `definitions/reviews/`.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner approves +
`event.schema.yml` fixtures discriminate + criterion exercised on ≥1 real aspect concept; gate =
definitions-governance owner gate; status on confirm = candidate → active.

Promotion boundary: local domain vocabulary (DomainSpec v2); the criterion is the public schema, never the
engine δ-derivation (moat).

---

## DS-D1.13 · Mapping (Connective)

Source kind: domain-vocabulary; formalized (criterion in `mapping.schema.yml`)

Evidence: [mapping.schema.yml](../../impl/spec/meta-types/connective/mapping.schema.yml) (machine criterion) ·
[TAXONOMY.md → Mapping](../../impl/spec/TAXONOMY.md) (descriptive catalog)

Formal voice:

```text
Mapping =
  a field-by-field data transformation between two shapes.
  well-formedness criterion (mapping.schema.yml):
    has_direction : declares direction (inbound | outbound | bidirectional)  (in the Attribute | Value table)
  source field -> target field, with defaults, computed fields, boundary validation.
```

Plain-language voice: a translator between two shapes: source field → target field, plus defaults, computed
fields, and validation at the boundary.

Domain-context voice: the shape-conversion node; SOURCE of `maps` under DS-D8. Checked by the content
validator against `mapping.schema.yml`.

Use carefully: `direction` is a *declared* attribute (the `Attribute | Value` table); any value
(`inbound` / `outbound` / `bidirectional`) present satisfies it.

Misuse warning: the exposed boundary itself is an **Interface**, not a Mapping — a Mapping must declare
`direction`.

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; edge = "an exposed boundary
mislabeled as a transform" → challenges `has_direction`; owner route = definitions-governance; gate = owner
decision + `mapping.schema.yml` fixtures re-run; blocking question = "does it convert between two shapes, or
expose a boundary?"; residue → `definitions/reviews/`.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner approves +
`mapping.schema.yml` fixtures discriminate + criterion exercised on ≥1 real aspect concept; gate =
definitions-governance owner gate; status on confirm = candidate → active.

Promotion boundary: local domain vocabulary (DomainSpec v2); the criterion is the public schema, never the
engine δ-derivation (moat).

---

## DS-D1.14 · State Machine (Lifecycle)

Source kind: domain-vocabulary; formalized (criterion in `state-machine.schema.yml`)

Evidence: [state-machine.schema.yml](../../impl/spec/meta-types/lifecycle/state-machine.schema.yml) (machine criterion) ·
[TAXONOMY.md → State Machine](../../impl/spec/TAXONOMY.md) (descriptive catalog)

Formal voice:

```text
State Machine =
  the states an entity moves through + the valid transitions between them.
  well-formedness criterion (state-machine.schema.yml):
    has_transitions : declares has_transitions = yes  (in the Attribute | Value table)
  states + transitions (guards, effects) + invariants; the most testable meta-type.
```

Plain-language voice: an entity's lifecycle made explicit — all states, which transitions are legal, and
what each transition requires and does.

Domain-context voice: the lifecycle node; TARGET of `reflects` / `transitions` under DS-D8. Checked by the
content validator against `state-machine.schema.yml`.

Use carefully: `has_transitions` is the *declared* attribute (the `Attribute | Value` table); a State Machine
has moves between states.

Misuse warning: if it declares `has_transitions = no` (a flat value set), it's an **Enum** — the validator
rejects it as State Machine.

Challenge contract (CAV2-D40, protocol-only): modes = contradiction / scope; edge = "a flat value set
mislabeled as having transitions" → challenges `has_transitions`; owner route = definitions-governance; gate =
owner decision + `state-machine.schema.yml` fixtures re-run; blocking question = "does it move along defined
transitions, or is it a flat value set?"; residue → `definitions/reviews/`.

Confirm contract (promotion — build-from-owned on the cav2 promotion gate): promotes when = owner approves +
`state-machine.schema.yml` fixtures discriminate + criterion exercised on ≥1 real aspect concept; gate =
definitions-governance owner gate; status on confirm = candidate → active.

Promotion boundary: local domain vocabulary (DomainSpec v2); the criterion is the public schema, never the
engine δ-derivation (moat).
