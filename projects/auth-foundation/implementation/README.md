# Auth Foundation D65 Rust Vertical

This package implements one bounded authorization decision:

> Return `ALLOW` exactly when one uniquely resolved session is current, trusted
> scope evidence and the complete active-role relation are present, and an
> active role grants a permission whose resource, action, and scope exactly
> equal the required permission. Return `DENY` otherwise.

The construction chain is:

```text
accepted Auth definitions
  -> Product Capability
  -> proposed business ontology
  -> DomainSpec v2 authored source
  -> deterministic graph and system ontology
  -> DomainSpec meta-type CLI-generated Rust kernel
  -> exact generated-source binding
  -> local static conformance evidence
  -> binary runtime contract
  -> successor runtime system ontology
  -> pure Rust adapter
  -> local in-memory runtime evidence
  -> SQLite provider contract and successor system ontology
  -> transaction-scoped Rust provider
  -> local in-memory and file-backed provider evidence
  -> candidate command-boundary definitions and Product Capability
  -> capability-local command-boundary business ontology
  -> DomainSpec Rule-guarded `admit-authorization-command` Operation
  -> deterministic Rust command-boundary kernel
  -> trusted Rust boundary over authentication and route-binding ports
  -> unchanged SQLite authorization decision service
```

The Rust crate is a pure decision kernel. Session lookup, role storage, trusted
scope construction, HTTP, tokens, and audit transport remain outside that
kernel slice. Callers reach it through the adapter and, at L5, the bounded
SQLite provider.

L6 adds the request trust boundary without changing the frozen L3–L5
artifacts. An inbound caller supplies only `request_id`, an opaque
`authentication_evidence_ref`, and `route_id`. Server-owned ports resolve the
session and exact route permission/scope requirement. The generated
`admit-authorization-command` Operation returns `Ready` only when four
DomainSpec Rules establish unique trusted evidence and exact candidate
provenance. Every other result is `Deny`, and the downstream authorization
service is not called. The `trusted-boundary/` crate then passes the derived
command to the existing SQLite service through a trait implemented entirely in
L6.

This slice intentionally does not introduce a DomainSpec Policy. There is one
fixed admission strategy, so Rules express its truth conditions. A Policy is
deferred until more than one legitimate strategy must be selected.

The new definition pack is an authored candidate awaiting owner admission.
Consequently, L6 has local technical evidence but semantic conformance is
`not_evaluable`; the candidate does not claim adopted capability meaning or an
admitted business/system ontology.

The `runtime-adapter/` successor constructs that context through five explicit
ports: session resolution, complete active-role resolution, trusted scope
evidence, current authorization revision, and decision time. It always invokes
the generated kernel and maps `Allow` to public `Allow` and every
`Deny(reason)` to public `Deny`. A failure in any port also fails closed to
`Deny`; internal reasons never cross the adapter boundary.

`runtime-contract.json` owns that binary boundary.
`runtime-construction-binding.json` creates a successor to the immutable L3
construction. The corresponding runtime system ontology, implementation
binding, and evidence live under `standard-conformance/`.

`provider-contract.json` binds the first concrete provider. The
`sqlite-provider/` crate resolves the four durable evidence ports inside one
SQLite transaction and keeps decision time injected. Its versioned migration
maps session, role, permission, revision, and scope-evidence columns back to
the capability-local ontology properties. `SqliteAuthorizationService` exposes
only `Allow` or `Deny`; database, query, conversion, incomplete-relation, and
transaction failures fail closed. The provider system ontology, exact
implementation binding, and evidence receipt are under
`standard-conformance/`.

The property-closed source under `operation-source/` is instantiated by the
standard CLI as `standard-runtime/`. Its receipt binds all 22 record
properties, 15 variants, eight Rules, the selected Operation, and the exact
generated Rust and Cargo manifest. The generated `authorize` function evaluates
the closed Rule internally; callers cannot inject the decision as a Boolean.
Each Rule is a generated Rust predicate with an exact ontology Rule, DomainSpec
selector, and Rust symbol binding.

The specialized Auth generator and its runtime package have been retired.
`standard-conformance/oracle.rs` is a frozen, non-generating copy of the old
evaluator used only by the independent `behavior.rs` harness. The harness
compares the standard candidate across 24 permitted, fail-closed, duplicate,
ordering, whitespace, and combined-failure decision-class cases.
`standard-conformance/receipt.json` reports structural coverage, compilation,
behavioral parity, determinism, and Lean characterization separately.
`standard-conformance/migration-receipt.json` binds the 29 retired paths,
their pre-migration digests, and the preservation matrix.

Build and validate from the repository root:

```bash
TMPDIR=/tmp /home/vrondelli/.nvm/versions/node/v22.12.0/bin/node \
  projects/domainspec-v2/impl/cli/node_modules/tsx/dist/cli.mjs \
  projects/auth-foundation/implementation/scripts/build.ts
python3 projects/auth-foundation/implementation/scripts/validate.py --write-receipt
```

Generated files live under `standard-runtime/` and
`command-boundary-runtime/`; evidence artifacts are named compiled graph,
system ontology, implementation binding, conformance, migration, provider,
command-boundary, and chain receipts. Edit the corresponding definition-bound
source, rebuild, and rerun validation. Direct edits to generated Rust fail
exact observation and two-run-determinism checks. Do not edit the frozen
oracle; changing it requires new migration evidence.

The L4 runtime evidence remains deterministic and in-memory. L5 adds one local
SQLite provider with in-memory and temporary file-backed evidence. HTTP,
tokens, administrative writes, audit transport, multi-node behavior,
deployment, and production observability remain later layers.
L6 still has no real authentication-evidence registry, route-binding registry,
HTTP transport, token flow, administrative mutation, or production-security
claim.
