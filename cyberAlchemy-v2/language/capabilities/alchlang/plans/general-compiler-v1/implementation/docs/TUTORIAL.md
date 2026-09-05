# AlchLang tutorial

AlchLang turns a domain description into typed, deterministic artifacts. A
single `.alch` file can define all 13 DomainSpec backend types, logical constraints, read models,
calculations, mappings, policies, actions, events, and explicit effect
boundaries.

This tutorial builds two examples:

- a read-only commerce model that demonstrates the SFOL logic and typed backend;
- an order operation that binds an effect to a transactional Outbox provider.

By the end, you will be able to validate an AlchLang file, inspect its compiled
artifacts, run a guarded local action, and identify where operational evidence
belongs.

## On this page

- [Five-minute quickstart](#five-minute-quickstart)
- [How AlchLang is organized](#how-alchlang-is-organized)
- [Create an AlchLang file](#create-an-alchlang-file)
- [Express logic with SFOL](#express-logic-with-sfol)
- [Use the complete backend profile](#use-the-complete-backend-profile)
- [Build generated artifacts](#build-generated-artifacts)
- [Define and run actions](#define-guarded-actions)
- [Use ORODI for operational evidence](#use-orodi-for-operational-evidence)
- [Current implementation limits](#current-implementation-limits)
- [Troubleshooting](#troubleshooting)

## Five-minute quickstart

The CLI is currently run from this repository. From the `implementation`
directory, verify Node.js, compile the CLI, check both maintained examples, and
build the typed example:

```bash
node --version
npm run typecheck
npm run build
node dist/cli.js check examples/typed-backend.alch
node dist/cli.js check examples/backend-types.alch
node dist/cli.js check examples/outbox-operation.alch
node dist/cli.js build examples/typed-backend.alch \
  --out generated/typed-commerce
```

The package requires Node.js 26.8.1 or newer. A successful `check` prints JSON
with `"status": "valid"`; a successful `build` creates `manifest.json` and the
generated domain files. Continue for the language model and a complete action
workflow.

## How AlchLang is organized

AlchLang separates domain meaning from operational realization:

```text
.alch source
    |
    v
SFOL terms and formulas
    |
    v
domain contracts: Query, Calculation, Mapping, Policy, Action, Effect
    |
    v
Integration Binding
    |
    v
architecture pattern and runtime provider
    |
    v
runtime observations and ORODI evaluation
```

Each layer answers a different question:

| Layer | Question |
| --- | --- |
| SFOL | What is true for the supplied values? |
| Domain contract | What may be selected, returned, or requested? |
| Integration Binding | Which infrastructure responsibilities apply? |
| Runtime provider | Which implementation performs the work? |
| ORODI | What does the operational evidence show? |

> Execution boundary: SFOL evaluates conditions over supplied values. An
> Integration Binding identifies infrastructure responsibilities, an explicit
> runtime command invokes a provider, and ORODI evaluates the resulting
> operational observations.

## Run from this repository

No package-registry installation is documented yet. From the `implementation`
directory, verify the runtime and build the repository-local CLI:

```bash
node --version
npm run typecheck
npm run build
node dist/cli.js check examples/typed-backend.alch
```

The remaining examples use `domainspec` for readability. In this checkout,
replace it with `node dist/cli.js`.

## Create an AlchLang file

Copy the complete maintained example so every later command operates on the
same source:

```bash
cp examples/typed-backend.alch commerce.alch
```

Its domain header is:

```alchlang
domain typed-commerce "Typed commerce"
owner typed-commerce-owner
logic sfol-v1
```

AlchLang source files follow these rules:

- The file extension is `.alch`.
- The encoding is UTF-8 without a byte-order mark.
- Declare one domain and one owner.
- Top-level declarations are not indented; declaration bodies are indented.
- Full-line comments start with `#`.
- Markdown fences are not allowed inside `.alch` files.

`logic sfol-v1` selects the bounded SFOL profile used by the current compiler.
It is optional for compatibility with earlier carrier-v2 input, but new source
files should declare it explicitly.

## Define domain data

Entities define the fields available to SFOL formulas and typed contracts:

```alchlang
entity Order:
  order_id: identifier required
  amount: integer required
  status: string required

entity OrderSummary:
  summary_id: identifier required
  total: integer required
  risk_band: string required
```

Supported scalar types are:

| Type | Intended value |
| --- | --- |
| `string` | Text |
| `integer` | Whole number |
| `decimal` | Decimal number |
| `boolean` | `true` or `false` |
| `identifier` | Stable identifier |
| `timestamp` | Timestamp value |
| `duration` | Duration value |
| `enum` | Named choice |
| `reference` | Reference to another value |
| `list` | Ordered collection |
| `record` | Structured record |

Fields are required by default. Add `optional` only when absence is part of the
domain contract.

## Use the complete backend profile

DomainSpec defines 13 active backend meta-types: Entity, Value Object, Enum,
Operation, Query, Calculation, Rule, Policy, Workflow, Interface, Event,
Mapping, and State Machine. The complete maintained source is
[`examples/backend-types.alch`](../examples/backend-types.alch).

The distinctions are contractual. Value Objects have equality fields but no
identity. Enums are finite value sets, while State Machines have transitions.
Operations declare state change plus exact read, write, and effect sets.
Workflows order multiple Operations within an admitted scope. Interfaces expose
Operations or Queries across a declared internal or external boundary.

The AlchLang compiler emits deterministic TypeScript contracts for these
surfaces. The canonical DomainSpec v2 baseline separately realizes all 13 types
in TypeScript, Python, and Rust through its private instantiation CLI; this
tutorial does not imply that AlchLang currently emits Python or Rust.

## Express logic with SFOL

SFOL is the single logical kernel for AlchLang. Rules, query filters,
permissions, transition guards, inline action conditions, and policy cases all
compile to the same formula representation.

Add a named rule:

```alchlang
rule OpenOrder:
  status == "open"
```

The current `sfol-v1` surface is a quantifier-free executable subset. It
supports:

| Category | Syntax |
| --- | --- |
| Equality | `==`, `!=` |
| Ordering | `<`, `<=`, `>`, `>=` |
| Membership | `in`, `contains` |
| Boolean composition | `and`, `or`, `not` |
| Presence | `exists(field)`, `absent(field)` |

Equality and ordering operands must have compatible declared types, and Boolean
operators require Boolean formulas. Quote string literals in canonical source.
Declared fact names resolve as fact references; the current parser may accept a
bare undeclared right-hand word as a string literal. A formula position must
produce a Boolean result:

```alchlang
rule Invalid:
  amount
```

SFOL evaluation is deterministic and value-bound. Provider operations belong
to the runtime layer described above.

## Add a Query

A Query filters and shapes rows supplied by its caller:

```alchlang
query OpenOrders:
  source Order
  where status == "open"
  order amount desc
  limit 2
  project order_id, amount
```

The pipeline is fixed:

```text
filter -> order -> limit -> project
```

`where`, `order`, and `limit` are optional. `project` is required and must
contain unique declared fields. Without `order`, the caller's input order is
preserved. Declaring `source Order` records semantic provenance. The caller
supplies the rows evaluated by a Query.

## Add a Calculation

A Calculation is a side-effect-free SFOL term over unsigned 64-bit integers:

```alchlang
calculation ApplyFee:
  inputs amount
  expression add(amount, 5)
  rounding reject
```

Available operators are `add`, `subtract`, `multiply`, and `divide`. Expressions
may nest:

```alchlang
expression multiply(add(amount, 5), 2)
```

Every arithmetic operation is checked. Compilation or evaluation rejects
unknown inputs, negative values, overflow, underflow, division by zero, and
inexact division when `rounding reject` is selected. Division may instead use
`floor` or `ceil`.

## Add a Mapping

A Mapping constructs a declared target shape:

```alchlang
mapping SummarizeOrder:
  source Order
  target OrderSummary
  total true
  field summary_id <- order_id
  field total <- amount
  field risk_band default string "standard"
```

Only authored field clauses produce output; source fields do not pass through
implicitly. With `total true`, evaluation fails when an authored clause cannot
produce its target value. Authors provide a clause for every required target
field.

## Add a Policy

A Policy selects one declared Calculation or Action:

```alchlang
calculation KeepAmount:
  inputs amount
  expression amount
  rounding reject

policy FeePolicy:
  inputs amount
  case amount > 100 -> ApplyFee
  default KeepAmount
```

Cases run in source order. The first true SFOL formula selects its target; the
default handles the remaining values. Selection returns a target identifier
for a separate runtime step.

The complete example is available at
[`examples/typed-backend.alch`](../examples/typed-backend.alch).

## Validate before building

Run the read-only check command:

```bash
domainspec check commerce.alch
```

A successful check returns JSON with the source format, domain identifier, and
deterministic plan digest:

```json
{
  "status": "valid",
  "source": "/absolute/path/to/commerce.alch",
  "file_format": "canonical-alch",
  "domain_id": "typed-commerce",
  "plan_digest": "<sha256>",
  "authority_effect": "none"
}
```

`check` parses, normalizes, type-checks, and lowers the source in memory.

## Build generated artifacts

Compile the domain into a new output directory:

```bash
domainspec build commerce.alch --out generated/typed-commerce
```

The generated directory contains the normalized carrier, typed interfaces,
contract data, graph data, traceability, test obligations, and a manifest with
the source and plan digests. Domains that contain Query, Calculation, Mapping,
or Policy declarations also receive `domain.typed-backend.ts`.
Backend-profile builds also include `domain.operations.ts`,
`domain.workflows.ts`, and `domain.interfaces.ts`.

The writer refuses to replace a non-empty output directory. Use a dedicated
generated directory. `--force` recursively replaces every existing entry in
the selected output directory:

```bash
domainspec build commerce.alch \
  --out generated/typed-commerce \
  --force
```

Review `manifest.json` in CI or deployment preparation. Its `source_digest` and
`plan_digest` identify the inputs, `files` binds every generated payload file,
and `authority_effect` records the command's effect classification. The
manifest itself is created after the payload digests and is not listed in
`files`.

## Define guarded actions

Actions use named SFOL rules as preconditions and permissions:

```alchlang
actor OrderService

rule operation-pending:
  status == "pending"

boundary order-transaction-authority:
  owner order-domain-owner

permission commit-order-with-outbox:
  actor OrderService
  action CommitOrderWithOutbox
  when operation-pending
  boundary order-transaction-authority

action CommitOrderWithOutbox:
  actor OrderService
  subject OrderOperation
  input operationId, orderId, outboxMessageId, occurredAt, payload
  requires operation-pending
  permission commit-order-with-outbox
  boundary order-transaction-authority
  emits outbox-message-recorded
  performs PersistOrderWithOutbox using sqlite-transactional-outbox
```

Action execution requires all of the following:

1. The actor is declared for the action.
2. Required input facts are present.
3. Every referenced SFOL rule evaluates to true.
4. The permission actor equals the executing actor, and its boundary equals the
   Action boundary.
5. The caller supplies the exact authority grant.
6. A matching adapter or effect binding is selected explicitly.

Failure at any step stops execution before a successful result is returned.
Before invoking the current runtime, a calling application must verify that
each permission's declared `action` references include the action being
executed.

## Bind an Effect to infrastructure

An Effect declares the required operational contract:

```alchlang
effect PersistOrderWithOutbox:
  pattern transactional-outbox
  binding sqlite-transactional-outbox
  writes OrderOperation, OutboxMessage
  emits outbox-message-recorded
  guarantee atomic-state-and-outbox
  on-failure rollback
  boundary order-transaction-authority
```

The Integration Binding connects this contract to a registered infrastructure
shape. The architecture pattern determines which generator and runtime
responsibilities must be available. The runtime provider performs the concrete
database or transport work.

Inspect the registered patterns before building or running an effectful domain:

```bash
domainspec patterns
domainspec patterns --available
domainspec pattern transactional-outbox
```

Pattern availability reports that the registered local technical inputs are
present. Runtime selection remains an explicit command step.

The complete operational example is available at
[`examples/outbox-operation.alch`](../examples/outbox-operation.alch).

## Run the local transactional Outbox example

Validate the source first:

```bash
domainspec check examples/outbox-operation.alch
```

Then execute the guarded action against an explicitly selected local SQLite
database:

```bash
domainspec run examples/outbox-operation.alch CommitOrderWithOutbox \
  --actor OrderService \
  --facts '{"operationId":"operation-1","orderId":"order-1","status":"pending","outboxMessageId":"message-1","occurredAt":"2026-09-03T12:00:00.000Z","payload":{"kind":"order-committed"}}' \
  --grant order-transaction-authority \
  --binding sqlite-transactional-outbox \
  --database ./outbox.sqlite \
  --effect-request-file examples/outbox-request.json
```

The command validates the action, actor, SFOL rules, permission, authority
grant, Effect, Integration Binding, transaction guarantee, failure
continuation, aggregate type, and event types before invoking the selected
provider. The SQLite provider is required to record the state change and
Outbox message in one transaction. Dispatch remains a separate operation. See
the [local runtime integration test record](../../RUNTIME-INTEGRATION-RESULTS.md)
for the provider checks associated with this example.

Inspect pending messages:

```bash
domainspec outbox pending --database ./outbox.sqlite
```

Dispatch is a separate operation. Use the local stdout transport during
development:

```bash
domainspec outbox dispatch \
  --database ./outbox.sqlite \
  --transport stdout \
  --worker-id local-worker
```

HTTP dispatch requires an endpoint and two matching origin confirmations. The
endpoint origin must equal both confirmation values:

```bash
domainspec outbox dispatch \
  --database ./outbox.sqlite \
  --transport http \
  --worker-id http-worker \
  --endpoint https://events.example.test/outbox \
  --allow-origin https://events.example.test \
  --confirm-network-dispatch https://events.example.test
```

## Use ORODI for operational evidence

Compilation answers whether the source is structurally and semantically valid.
Runtime execution produces observations. ORODI evaluates those observations
against operational claims such as durability, recovery, canary behavior, or
rollback readiness.

The evidence chain is:

| Outcome | Established by |
| --- | --- |
| A formula evaluated to `true` | SFOL evaluator |
| An action passed its guards | Action runtime |
| A provider performed an operation | Runtime receipt and observation |
| An operational obligation passed | ORODI evaluation over bound evidence |
| A release or deployment may proceed | The deployment authority for that environment |

Operational claims use observations from the relevant provider and environment.

## Add AlchLang checks to CI

A minimal CI sequence is:

```bash
npm run typecheck
npm test
npm run build
node dist/cli.js check examples/typed-backend.alch
node dist/cli.js check examples/outbox-operation.alch
```

For generated artifacts, build into a fresh directory and preserve the
resulting manifest with the test output. Rebuild after the source, compiler,
profile, or provider catalog changes.

## Current implementation limits

- Repeated `domain` or `owner` headers are accepted with the final value. The
  authoring policy requires one declaration for each header.
- `in` and `contains` are parsed without operand-shape validation. Use equality,
  ordering, Boolean composition, or presence operators for compiler-checked
  formulas.
- `total true` checks whether each authored Mapping clause produces a value.
  Review clause coverage against required target fields.
- Permission `action` references are recorded in the carrier. Before invoking
  the current runtime, a calling application must verify action membership.

## Troubleshooting

### `SOURCE_EXTENSION`

The source path does not use the lowercase `.alch` extension. Rename the source
file and rerun `check`.

### `SOURCE_CONTAINER`

The `.alch` file contains a Markdown fence. Remove the fence and retain only the
AlchLang source.

### `SFOL_PROFILE`

The logic profile is unknown or appears more than once. Declare exactly one
`logic sfol-v1` line.

### `SFOL_FORMULA_TYPE`

A rule, query filter, permission, or policy case produced a non-Boolean term.
Add a comparison or another Boolean operator.

```alchlang
# Invalid
rule HasAmount:
  amount

# Valid
rule HasAmount:
  amount > 0
```

### `UNRESOLVED_REFERENCE`

A formula or contract refers to a field, entity, rule, target, event, or
boundary that is not declared. Check spelling, then run `check` again.

### `TYPE_MISMATCH`

An operator received incompatible operand types, or a Mapping default does not
match its target field. AlchLang does not coerce strings to numbers or numbers
to strings.

### `OUTPUT_EXISTS`

The selected build directory is not empty. Choose a new dedicated directory.
Pass `--force` only when every current entry in that output directory may be
recursively replaced.

### `AUTHORITY_DENIED`

The run command did not receive the exact boundary required by the Action.
Supply the declared boundary with `--grant` only when that local execution is
intended.

### `EFFECT_BINDING_REQUIRED`

The Action performs an Effect, but the run command did not select its binding.
Provide the declared binding and the provider-specific inputs required by the
runtime.

### `OUTBOX_HTTP_CONFIRMATION_REQUIRED`

HTTP dispatch requires the endpoint origin, `--allow-origin`, and
`--confirm-network-dispatch` to match exactly.

## Language profile

The current compiler supports quantifier-free SFOL over bounded supplied
values. The profile excludes general quantifiers, infinite-domain reasoning,
embedded proof scripts, and automatic theorem proving. Providers, credentials,
and network access are supplied to explicit runtime commands.

Use the [language reference](LANGUAGE.md) for declaration-level syntax and the
[package README](../README.md) for concise command examples.
