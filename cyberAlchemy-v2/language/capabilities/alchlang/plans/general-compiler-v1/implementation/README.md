# AlchLang CLI

AlchLang source files describe the 13 DomainSpec backend types, bounded logic,
typed contracts, actions, events, and explicit effect boundaries. Canonical source uses the
`.alch` suffix and plain UTF-8 text without Markdown fences.

> Development status: this CLI is currently run from the repository checkout.
> No package-registry installation is documented.

Start with the [AlchLang tutorial](docs/TUTORIAL.md). Use the
[language reference](docs/LANGUAGE.md) for declaration-level syntax.

The [documentation frontend](docs-app/README.md) provides a responsive React
presentation with section navigation, search, and copyable examples.

From this directory:

```bash
node --version
npm run typecheck
npm run build
node dist/cli.js check examples/typed-backend.alch
node dist/cli.js check examples/backend-types.alch
node dist/cli.js build examples/typed-backend.alch --out generated/typed-commerce
```

`examples/backend-types.alch` exercises Entity, Value Object, Enum, Operation,
Query, Calculation, Rule, Policy, Workflow, Interface, Event, Mapping, and
State Machine in one source. The compiler emits TypeScript contracts;
TypeScript/Python/Rust realization parity belongs to the separate DomainSpec v2
instantiation CLI and is not claimed by this package.

Generated artifacts are declaration-sensitive. An Entity-only source emits
`domain.types.ts`, `domain.schema.ts`, and `domain.graph.json`. Event, state
machine, action/operation, workflow, interface, example, typed-backend, effect,
traceability, and unsupported-residue files appear only when their corresponding
plan collections contain data.

Run the focused alchLang output/meta-type test from the repository root:

```bash
toolchains/node-typescript/bin/node-env run --project projects/domainspec-v2/impl -- \
  node --import tsx --test \
  ../../../cyberAlchemy-v2/language/capabilities/alchlang/plans/general-compiler-v1/implementation/test/meta-type-output.test.ts
```

Run DomainSpec's independent 26-case, 156-swap, 13-node formation test:

```bash
toolchains/node-typescript/bin/node-env run --project projects/domainspec-v2/impl -- \
  node --import tsx --test tools/tests/formation-golden-corpus.test.ts
```

Run a guarded action with an explicit local adapter:

```bash
node dist/cli.js run examples/customer-approval.alch ReleaseCredit \
  --actor CreditOperator \
  --facts '{"customerId":"c-1","riskScore":600,"status":"approved","amount":100}' \
  --grant credit-release-authority \
  --adapter memory
```

Run the SQLite transactional Outbox example with an explicit infrastructure
request:

```bash
node dist/cli.js run examples/outbox-operation.alch CommitOrderWithOutbox \
  --actor OrderService \
  --facts '{"operationId":"operation-1","orderId":"order-1","status":"pending","outboxMessageId":"message-1","occurredAt":"2026-09-03T12:00:00.000Z","payload":{"kind":"order-committed"}}' \
  --grant order-transaction-authority \
  --binding sqlite-transactional-outbox \
  --database ./outbox.sqlite \
  --effect-request-file examples/outbox-request.json

node dist/cli.js outbox pending --database ./outbox.sqlite
node dist/cli.js outbox dispatch --database ./outbox.sqlite --transport stdout \
  --worker-id local-worker
```

The SQLite provider records state and Outbox work in one transaction. Message
dispatch is a separate command. HTTP dispatch is opt-in and requires the
endpoint origin to match both `--allow-origin` and
`--confirm-network-dispatch`.

Discover registered operation patterns with:

```bash
node dist/cli.js patterns
node dist/cli.js patterns --available
node dist/cli.js patterns --blocked
node dist/cli.js pattern transactional-outbox
```

Legacy `.md` containers remain readable when they contain exactly one fenced
`alchlang` block. Use `.alch` for new and maintained source files.
