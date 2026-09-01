# Auth Foundation Exact Permission Specification

Generated human view. Canonical semantics live in the project-local machine sources.
Graph digest: `5b6b4518c5ce9e413ff6cf7d1552fac32850f25600bbf7efa8fd81d378c79ee4`.

## Nodes

| Node | Kind | Intent |
| --- | --- | --- |
| `auth-exact-permission.AuthorizationContext` | Entity | Carry one trusted request, its decision time and current authorization revision, unique session resolution, scope evidence, and complete active-role relation into the pure decision. |
| `auth-exact-permission.AuthorizationDecision` | Entity | Represent the normative binary ALLOW or DENY result while keeping diagnostic denial reasons non-normative. |
| `auth-exact-permission.AuthorizationInvariant` | Rule | Return ALLOW exactly for an admissible request with an exact active-role permission grant and return DENY for every other in-scope request. |
| `auth-exact-permission.Permission` | Entity | Represent the exact resource, action, and trusted scope triple used by both required permissions and positive role grants. |
| `auth-exact-permission.Role` | Entity | Represent one complete authoritative role definition selected only when its identity is active in the resolved session. |
| `auth-exact-permission.Session` | Entity | Represent one resolved server-side session whose status, expiry, authorization revision, and active role identities are checked exactly. |

## Edges

| Edge | From | Type | To |
| --- | --- | --- | --- |

This file is generated; edit machine sources and rebuild.
