# Auth Foundation

Status: **proof-and-evidence candidate with a local D65 Rust vertical**

This project starts a new authorization foundation without changing
`projects/auth-user-management/`.

The formalization package, business ontology, owner-accepted business meaning,
and one Auth-owned L0 FormalClaim candidate now exist. A pure, local
authorization decision kernel is generated from the bounded DomainSpec
meta-type CLI profile and has local static conformance evidence. There is no
authentication service, database, token provider, integrated resolver,
runtime-observation evidence, deployment, or production-security claim yet.

Canonical artifacts are JSON and JSON Schema under [`formalization/`](formalization/).
Markdown files are human navigation only.

The first implementation-bearing slice lives under
[`implementation/`](implementation/). It carries the accepted Auth definitions
through a Product Capability, a proposed capability-local business ontology,
DomainSpec v2 authored source, deterministic generated graph and system
ontology, an exact Rust implementation binding, and local conformance evidence.
The primary Rust candidate is deterministically instantiated by the standard
DomainSpec CLI from a property-closed Operation. The earlier bounded generator
is retained as a behavioral comparison oracle; Cargo and the Auth validator
compile, test, and compare both paths.
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
