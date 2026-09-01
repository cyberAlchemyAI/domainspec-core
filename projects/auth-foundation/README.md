# Auth Foundation

Status: **proof-and-evidence candidate with a local D65 Rust vertical, SQLite provider, and technical command-boundary candidate**

This project starts a new authorization foundation without changing
`projects/auth-user-management/`.

The formalization package, business ontology, owner-accepted business meaning,
and one Auth-owned L0 FormalClaim candidate now exist. A pure, local
authorization decision kernel is generated from the bounded DomainSpec
meta-type CLI profile and has local static conformance evidence. A pure Rust
adapter now constructs the generated evaluation context through five trusted
ports and exposes only `Allow` or `Deny`. A successor Rust provider now resolves
the four durable ports from one SQLite transaction while keeping the decision
clock injected. There is no authentication or token service, administrative
write API, transport, deployment, multi-node, or production-security claim yet.
An L6 candidate now derives the internal authorization command from trusted
authentication-evidence and server-owned route-binding ports. Its DomainSpec
Rules and Rust boundary pass local technical gates, but the new definitions are
not owner-admitted, so semantic conformance remains `not_evaluable`.

Canonical artifacts are JSON and JSON Schema under [`formalization/`](formalization/).
Markdown files are human navigation only.

The first implementation-bearing slice lives under
[`implementation/`](implementation/). It carries the accepted Auth definitions
through a Product Capability, a proposed capability-local business ontology,
DomainSpec v2 authored source, deterministic generated graph and system
ontology, an exact Rust implementation binding, and local conformance evidence.
The Rust candidate is deterministically instantiated by the standard
DomainSpec CLI from a property-closed Operation. The specialized Auth generator
has been retired. A frozen copy of its evaluator remains only as an independent
behavioral oracle; it has no generation or implementation authority.
The successor runtime construction keeps those L3 bytes immutable while binding
the binary runtime contract, runtime system ontology, adapter implementation,
and deterministic in-memory adapter evidence. A second successor binds the
SQLite provider contract, schema migration, provider system ontology, exact
implementation bytes, and in-memory plus file-backed evidence without changing
the L3 or L4 receipts.
The L6 successor likewise leaves the L3–L5 artifacts unchanged while adding a
separate definition pack, Product Capability, business ontology, DomainSpec
Operation, generated Rust kernel, trusted-boundary adapter, and bounded
evidence receipt.
It is a merge candidate, not a deployment or production-security claim.

## Starting question

Can a small session-based RBAC model preserve a clear business meaning while
remaining extensible enough to support secure session currentness, trusted
scope construction, stronger policy profiles, formal proof, and runtime
evidence later?

## Current boundary

The first model says:

- authentication establishes an active session for a user;
- a session activates roles;
- a role grants permissions;
- a permission names a resource, action, and scope;
- trusted application code constructs an authorization request;
- authorization allows exactly when the session is current and an active role
  grants the exact required permission;
- every other result is deny.

The exact business meaning and interpretation are accepted by the Auth
Foundation owner. The FormalClaim that binds them is still a candidate and
requires its own admission decision. The first case is under
[`formalization/cases/AF-EXACT-SESSION-ROLE-PERMISSION-001/`](formalization/cases/AF-EXACT-SESSION-ROLE-PERMISSION-001/).
