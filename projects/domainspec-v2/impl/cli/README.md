# `@domainspec-v2/cli`

This directory contains the canonical private DomainSpec v2 foundation CLI.
It embeds the immutable `domainspec-meta-types-current-implemented@10` catalog,
selects exactly one of
its 39 realization rows, and exposes the following command forms:

```text
domainspec-v2 add operation <source-project-root> --feature <feature> --name <operation> --description <text> --guard <guard> --failure-continuation <continuation> [--reads <csv>] [--writes <csv>] [--effects <csv>]
domainspec-v2 instantiate <source-project-root> --node <feature>:<node> --language <typescript|python|rust> --target-root <absolute-new-root>
domainspec-v2 instantiate <source-project-root> --node <feature>:<node> --language <typescript|python|rust> --target-root <absolute-new-root> --integration-profile provider-neutral-v1 --integration-binding-set <binding-set-id>
domainspec-v2 formalize <source-project-root> --target <absolute-new-lean-file>
domainspec-v2 formalize-check <source-project-root> --target <absolute-lean-file>
domainspec-v2 lint <source-or-instantiated-target-root>
domainspec-v2 receipt <source-or-instantiated-target-root>
```

`add operation` authors one closed `domainspec.node/v1` Operation in an
existing validated source project. The feature and name are lowercase
kebab-case identities; the language profiles derive their filenames and
function symbols from that single node identity. Descriptions, guards, and
failure continuations are required rather than inferred. Omitted read, write,
or effect options become explicit empty sets. The command stages and validates
the complete prospective project, rejects existing nodes and concurrent
authoring, writes the new node while it is still unreferenced, and atomically
replaces the feature index as the visibility boundary. Its result includes the
recomputed source-manifest digest. This slice does not create projects,
relationships, generated implementations, or runtime providers.

`instantiate` decodes one of the 13 closed backend meta types, plans one
deterministic language artifact, and publishes the artifact plus a
baseline-bound receipt through a single atomic directory rename. It never
updates an existing target. `lint` and `receipt` independently re-read an
instantiated target, reproduce the expected generator output for the selected
frozen row, and reject undeclared files or semantic drift.

`formalize` decodes and validates the entire authored project before it creates
one Lean file. The output binds the source-manifest and compiled-graph digests,
the immutable `@10` predecessor, all 31 DS-D8 signatures, all 45 obligation
identifiers, executable predicates for the six obligation families, and one
witness for every obligation applicable to an authored edge. State Machine
sources also project their declared states, initial state, structured
transitions, Rule guard references, and Event-intent relationships into an
executable `allProjectStateMachinesHold` theorem. The same projection carries
L1 typed-field identities, Entity identity,
Value Object structural equality, Enum closure, Event occurrence/version, and
Interface boundary/compatibility facts into `allProjectL1RolesHold`.
`formalize-check`
rebuilds that projection and rejects source or target drift. These finite Lean
proofs establish only the generated graph obligations; they do not establish
runtime conformance, business acceptance, publication, or external authority.

The optional system-integration pair is explicit and closed: both options must
be present or both absent. The CLI reads
`integrations/<binding-set-id>.json` from the source project, validates the
provider-neutral D45-D49 contract family, binds its source/profile/language and
architecture digests into the receipt, and emits one additional contract at
`src/domainspec/system-integration/<language>/<binding-set-id>.<extension>`.
DomainSpec accepts the target project's opaque adapter and resource references;
it does not select SQLite, another database, a framework, or a dependency
container. Generated contracts preserve
`runtime_guarantees_observed: false`: provider runtime behavior requires a
separate observation layer and is outside this candidate slice.

Relationship inputs are validated project-wide against a digest-bound generated
projection of all 31 canonical signatures and all 45 declared validation
obligations. Source `lint`, source `receipt`, authoring, and instantiation use the
same fail-closed project validator. The decoder rejects invalid endpoint types
and placement, deprecated aliases, authored generated views, selected duplicate
propositions, inverse `owns`/`belongs-to` collapse, and the explicit `creates`
one-to-one obligations before it plans any target. `creates` also derives the
sorted `creation_targets` semantic projection without permitting source
authorship. Operation generators keep instrumentation in an injected
outer wrapper around the pure state/outbox core; Workflow generators require an
explicit composition-root compensation callable, emit a five-state forward-recovery
plan, and preserve the selected realization's `compensation_execution: false` ceiling.
Every forward and recovery step must be connected through the canonical
`Workflow --[orchestrates]--> Operation` relationship. Explicit compensation
dependencies use `operation:depends-on:operation`; absent dependencies fall back
to reverse completed-step order. A separately owned executor preflights every
Operation binding and deterministic idempotency key before the first invocation.

State Machine bodies are closed transition tables. Each transition has a stable
identity, a declared source and target state, an optional Rule selector, and an
optional Event selector. Event intents must be backed by an incoming canonical
`Event --[transitions]--> State Machine` relationship. Generated TypeScript,
Python, and Rust runtimes apply the same fail-closed causal outcomes:
`invalid-current-state`, `undeclared-transition`, `source-mismatch`, and
`guard-rejected`. The Rule-reference evaluator is required at every call site;
there is no allow-by-default guard callback. A successful transition returns only the declared next state
and Event intent; effect execution remains outside this package.

L1 domain and boundary bodies share one closed `FieldSpec`/`TypeRef`
vocabulary. Primitive references are limited to `string`, `boolean`,
`integer`, `decimal`, `timestamp`, and `uuid`; named references must resolve to
an Entity, Value Object, Enum, or Event in the compiled project graph. Entities
designate one required identity field and compare identity independently of
mutable state. Value Objects require a complete field set, no identity, exact
Rule invariant references, and structural equality. Events declare their
event type, positive integer version, required occurrence identity,
occurred-at policy, and typed payload. Interfaces declare external/internal
boundary kind, version, exact/backward compatibility direction, and typed
request/result signatures whose Operation or Query references close exactly
against authored `exposes` relationships. Generated TypeScript, Python, and
Rust artifacts preserve these roles and expose deterministic identity,
equality, Event compatibility, and Interface version checks.

The package is not released, published, registered, deployed, or production
ready. The root export is the curated instantiation/conformance API; the
architecture-conformance proof runner remains internal to `@domainspec-v2/impl`
and is not used as a code generator.

The supported target environment is Linux x64 in the repository Node toolchain
container with Node.js `v26.8.1` and npm `11.19.0`. The development workspace
uses the same container with pnpm `10.34.5`; this private CLI package has its
own npm `11.19.0` lock and package boundary. Clean-package validation packs the
compiled output into an isolated temporary consumer and compares two generated
targets byte for byte. These checks are implementation evidence only; they do
not publish, release, deploy, or claim production readiness.

## Closed Governance-kernel instantiation

`tools/governance-kernel.mjs` is a bounded, dependency-free candidate extension.
It validates the six-node DomainSpec source for the smallest Governance
evaluation kernel, binds every node to the accepted Rust realization protocol,
and deterministically emits one no-effect Rust crate. It is intentionally not a
generic generator and does not widen the supported public CLI command surface.

The generated receipt uses SHA-256 only for static source/artifact conformance.
The generated evaluator invokes no hash operation and does not use a repository
digest as identity, authority, or a lifecycle clock. Generated Rust types still
implement the standard `Hash` trait where the admitted DomainSpec realization
protocol requires equality-compatible type behavior.

Each source project pins its own admitted implementation baseline. Generation
does not follow the mutable repository-wide current pointer, so unrelated
baseline advancement cannot trigger an implicit kernel refresh.

## Property-closed Rust Operations

The standard `instantiate` command accepts a typed Operation whose referenced
records, sums, Rules, and legal relationships form one deterministic closure.
The bounded type algebra currently includes `String`, `Bool`, `UInt64`, named
types, sets, multiplicity-preserving lists, optionals, and sums. The Rule
algebra is structured data; executable Rust snippets are not accepted. List
projection preserves multiplicity unless the source explicitly applies
`to_set`, and `rule_ref` binds every target parameter by name and typed value.

For Rust, the CLI lowers that closure to typed structs, enums, and one predicate
function for every referenced Rule. It evaluates the selected guard inside the
Operation, emits deterministic ontology-to-selector-to-Rust-symbol bindings and
a Cargo manifest, and binds the complete closure into the instantiation receipt.
Missing selectors, argument drift, normalized symbol collisions, read-edge
drift, cycles, incompatible types, receipt tampering, and caller-supplied Boolean
guards fail closed.

The Auth Foundation candidate exercises this standard path:

```text
domainspec-v2 instantiate <absolute-operation-source> \
  --node auth-exact-permission:authorize \
  --language rust \
  --target-root <absolute-new-target>
```

Capability neutrality is exercised independently by the persistent
`test/fixtures/capacity-decision/` source. It selects
`capacity-decision:decide-capacity`, closes three non-Auth properties, two
result variants, one Rule, and two legal relationships, then generates and
executes a Rust capacity decision through the same command, closure compiler,
renderer, receipt, and observer. The fixture also proves that generated crates
do not retain collection imports when their selected closure does not use a
collection type or operator.

## Typed Operation fail-closed diagnostics

The L2 hardening matrix mutates that non-Auth capacity source and requires two
independent runs to return the same code, pointer, message, and exit status.
Malformed schema, missing and untyped dependencies, self-recursion, duplicate
property identity, unsupported Rule operators, and Rust semantic type mismatch
all fail before target creation.

Closure diagnostics retain the `MTCLI_TYPED_CLOSURE_*` family. Rust lowering
uses typed errors rather than generic exceptions:

- `MTCLI_TYPED_RUST_CRATE` and `MTCLI_TYPED_RUST_LITERAL` close output encoding;
- `MTCLI_TYPED_RUST_COLLISION` closes normalized symbol ambiguity;
- `MTCLI_TYPED_RUST_GUARD`, `MTCLI_TYPED_RUST_RULE`, and
  `MTCLI_TYPED_RUST_SCOPE` close dependency and binding drift;
- `MTCLI_TYPED_RUST_TYPE` and `MTCLI_TYPED_RUST_RESULT` close incompatible
  operands and output constructors;
- `MTCLI_TYPED_RUST_UNSUPPORTED` rejects forms outside the bounded Rust
  realization.

Each typed Rust diagnostic carries exit status 22 and survives the CLI failure
envelope with its code and pointer. These diagnostics are implementation
evidence, not source admission or runtime authority.

The former `tools/auth-kernel.mjs` specialization has been retired. Auth now
uses this same `instantiate` surface and typed Operation realization as every
other consumer. Historical parity evidence is owned by the Auth package, not by
an alternate CLI generator.
