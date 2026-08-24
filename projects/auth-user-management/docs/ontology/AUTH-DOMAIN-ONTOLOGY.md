---
id: auth-access-control.business-domain
feature: auth-access-control
title: Auth Access Control Business Domain Ontology
summary: Human view of the business-domain ontology graph — concepts, typed relations, rules, confidence, and findings.
status: candidate
pillar: platform
domain: auth-access-control-ontology
audience:
  - developers
  - operations
priority: p1
lang: en
owners:
  - platform-core
updatedAt: 2026-08-19
dependencies:
  - ../auth-access-control/SPEC.md
includes: []
---

# Auth Access Control — Business Domain Ontology

> **GENERATED — DO NOT EDIT.**
> Source of truth: [`docs/ontology/auth-domain-ontology.json`](auth-domain-ontology.json) 
> Regenerate with `python3 docs/ontology/render.py`; validate with `python3 docs/ontology/validate.py`.

> This graph is an evidence artifact, not source authority.
> docs/auth-access-control/ remains the DomainSpec source of truth.
> .craft/ledger.yml remains the project knowledge source of truth.
> JSON owns field names, IDs, enums, and validation rules; the markdown view is derived.

## Run

| Field | Value |
| ----- | ----- |
| Ontology type | `business-domain` |
| Selection source | user (confidence: exact) |
| Rejected candidates | `business-system-bridge`, `system-runtime`, `knowledge-vault`, `architecture-property` |
| Branch | `business` |
| Mode | `map` |
| Runtime | inline (profile: none) |
| Knowledge inflection | **high** — Dense formalized docs, closed decisions, explicit invariants. Investment belongs in promotion gates and convention repair, not further discovery. |
| Graph size | 178 nodes · 241 edges · 13 findings |

## Scope

**In scope (business branch):** domain meaning, actors, entities, value objects, enumerations, business rules, derivation rules, guarantees, decision policies, orchestrations, lifecycle semantics, domain events, decisions, scope boundaries.

**Out of scope for this run:**

- implementation facts (src/, dist/, Drizzle schema, ports and adapters) — system branch not read; no claim in this graph is sourced from code.
- realization, drift, and test-coverage claims — bridge edges require evidence from both branches; none is asserted here.
- knowledge-lifecycle governance of the craft ledger itself — that is a knowledge-vault ontology type, not business-domain.
- architecture property and constraint enforcement — that is an architecture-property ontology type.

**Declared outside the domain** (the package disclaims these):

| Concern | Evidence |
| ------- | -------- |
| HTTP routes | `README.md#boundaries` |
| browser cookies | `README.md#boundaries` |
| CSRF policy | `README.md#boundaries` |
| OAuth providers such as Strava | `docs/ADOPTION.md` |
| consumer UI | `README.md#boundaries` |
| product role defaults | `README.md#boundaries` |

## Sources

| Source | Branch | Read | Used for |
| ------ | ------ | ---- | -------- |
| `docs/auth-access-control/SPEC.md` | mixed | full | concept registry, capability list, concept graph |
| `docs/auth-access-control/domain.md` | business | full | entities, value objects, enumeration, invariants |
| `docs/auth-access-control/operations.md` | business | full | behaviors, rules, calculations, guarantees, error states |
| `docs/auth-access-control/workflows.md` | business | full | orchestrations, permission policy, workflow invariants |
| `docs/auth-access-control/states.md` | business | full | lifecycles, transitions, invalid transitions |
| `docs/auth-access-control/events.md` | business | full | domain events, payloads, consumers |
| `docs/auth-access-control/queries.md` | business | full | read models, inactive reason precedence |
| `docs/auth-access-control/capabilities/` | business | partial | capability framing and aspect maps |
| `docs/auth-access-control/STORIES.md` | business | full | acceptance claims and coverage matrix |
| `docs/auth-access-control/decisions.en.md` | business | full | confirmed, open, and deferred decisions |
| `docs/auth-access-control/PILOT-DECISIONS.md` | mixed | full | policy posture decisions |
| `docs/auth-access-control/mappings.md` | mixed | full | inbound validation and defaults only |
| `docs/auth-access-control/interfaces.md` | system-leaning | headings | boundary check only; see CON-08 |
| `README.md` | business | full | package scope boundary |
| `docs/ADOPTION.md` | business | partial | consumer responsibilities and boundary |
| `.craft/ledger.yml` | mixed | partial | DEF-AUTH-UM-001/002/003, DEC-AUTH-TRANSPORT-001, DEC-AUTH-STRAVA-SCOPE-001 |

Not read as evidence: `docs/auth-access-control/TEST-SPEC.md`, `docs/auth-access-control/observability.md`, `docs/auth-access-control/UI-SPEC.md`, `docs/auth-access-control/UI-REVIEW.md`, `docs/auth-access-control/ALIGNMENT-REPORT.md`, `docs/auth-access-control/LAYERING-ALIGNMENT-PLAN.md`, `docs/auth-access-control/LAYERING-ALIGNMENT-REPORT.md`, `docs/auth-access-control/OBSERVABILITY-REPORT.md`, `docs/auth-access-control/PIPELINE-REPORT.md`, `docs/auth-access-control/CHANGELOG.md`, `docs/auth-access-control/tasks.en.md`, `development/`, `src/`, `tests/`, `e2e/`, `drizzle/`.

## Local Label → Generic Concept

Local labels are reporting aliases only. They are not promoted into reusable Arcanum vocabulary.

| Local label | Generic concept |
| ----------- | --------------- |
| Capability | `capability` |
| Aspect | `concept partition by role` |
| Operation | `behavior` |
| Query | `read_model` |
| Entity | `entity` |
| Value Object | `value_object` |
| Enum | `enumeration` |
| Rule (R*) | `business_rule` |
| Calculation (C*) | `derivation_rule` |
| Invariant (I*) | `constraint` |
| Postcondition (P*) | `guarantee` |
| State Machine / Lifecycle | `lifecycle` |
| Policy | `decision_policy` |
| Workflow | `orchestration` |
| Story (US-*) | `acceptance_claim` |
| Confirmed / Open / Deferred Decision | `decision` |
| Concept Registry | `concept index` |
| Feature Concept Graph | `typed relation set` |
| .craft definition (DEF-*) | `domain definition` |
| .craft decision (DEC-*) | `decision` |
| .craft gap (GAP-*) | `evidence gap` |

## Node Roles

| Role | Count | Meaning |
| ---- | ----- | ------- |
| `actor` | 14 | A party that initiates or consumes domain behavior. |
| `entity` | 4 | Domain concept with a stable identity. |
| `value_object` | 3 | Domain concept identified by its values. |
| `enumeration` | 3 | Closed set of named domain values. |
| `error_code` | 15 | A named failure outcome. |
| `permission_key` | 2 | A canonical permission identifier. |
| `capability` | 7 | A user-facing unit of domain function. |
| `behavior` | 6 | A mutating domain behavior (operation). |
| `read_model` | 2 | A non-mutating domain read (query). |
| `lifecycle` | 2 | A state model owning an entity's states. |
| `lifecycle_state` | 6 | One state within a lifecycle. |
| `domain_event` | 7 | A named fact emitted by a behavior. |
| `decision_policy` | 3 | A rule set that selects an outcome. |
| `orchestration` | 2 | An ordered composition of behaviors. |
| `constraint` | 12 | An invariant restricting admissible values. |
| `business_rule` | 24 | A precondition a behavior must satisfy. |
| `derivation_rule` | 10 | A calculation producing a domain value. |
| `guarantee` | 16 | A postcondition a behavior must uphold. |
| `decision` | 27 | A recorded commitment about the domain. |
| `acceptance_claim` | 12 | A story asserting expected behavior. |
| `boundary_concept` | 1 | A concept the feature's own concept registry names but the package scope boundary disclaims. Present so the dispute is queryable, not to assert ownership. |

## Concept Inventory

Concept IDs reuse the existing `auth-access-control.*` registry namespace. `spec` marks membership in `SPEC.md#concept-registry`; this ontology invents no competing authority namespace.

### Actor (14)

| ID | Label | Summary | Flags | Evidence |
| -- | ----- | ------- | ----- | -------- |
| `actor.admin` | Admin | Holds admin permissions; may terminate any session. |  | `docs/auth-access-control/operations.md` |
| `actor.alerting-pipeline` | Alerting pipeline | Raises signal on repeated denials. |  | `docs/auth-access-control/events.md` |
| `actor.api-gateway` | API gateway or service middleware | Runs authenticate then authorize. |  | `docs/auth-access-control/operations.md` |
| `actor.application-lifecycle` | Application lifecycle | Auto-triggers bootstrap on boot. |  | `docs/auth-access-control/operations.md` |
| `actor.audit-subsystem` | Audit subsystem | Records auth events. |  | `docs/auth-access-control/events.md` |
| `actor.automation-principal` | Automation principal | subjectType = automation. |  | `docs/auth-access-control/operations.md` |
| `actor.cache-invalidator` | Cache invalidator | Invalidates token cache entries. |  | `docs/auth-access-control/events.md` |
| `actor.consuming-feature` | Consuming feature or admin tooling | player-management, player-makeup, financial-settlement, admin tooling. |  | `docs/auth-access-control/SPEC.md` |
| `actor.end-user` | End user | Authenticates with identifier and password. |  | `docs/auth-access-control/operations.md` |
| `actor.operations-engineer` | Operations engineer | Observes bootstrap output. |  | `docs/auth-access-control/operations.md` |
| `actor.security-analytics` | Security analytics | Tracks denied access patterns. |  | `docs/auth-access-control/events.md` |
| `actor.security-operator` | Security operator or tooling | Introspects tokens. |  | `docs/auth-access-control/operations.md` |
| `actor.service-principal` | Service principal | subjectType = service. |  | `docs/auth-access-control/operations.md` |
| `actor.session-tracker` | Session tracker | Maintains active session registry. |  | `docs/auth-access-control/events.md` |

### Capability (7)

| ID | Label | Summary | Flags | Evidence |
| -- | ----- | ------- | ----- | -------- |
| `auth-access-control.capability.authenticate-request` | Authenticate Request | Capability Authenticate Request. |  | `docs/auth-access-control/capabilities/authenticate-request.md` |
| `auth-access-control.capability.authorize-request` | Authorize Request | Capability Authorize Request. |  | `docs/auth-access-control/capabilities/authorize-request.md` |
| `auth-access-control.capability.browse-permission-catalog` | Browse Permission Catalog | Capability Browse Permission Catalog. |  | `docs/auth-access-control/capabilities/browse-permission-catalog.md` |
| `auth-access-control.capability.introspect-token` | Introspect Token | Capability Introspect Token. |  | `docs/auth-access-control/capabilities/introspect-token.md` |
| `auth-access-control.capability.login` | Login | Capability Login. |  | `docs/auth-access-control/capabilities/login.md` |
| `auth-access-control.capability.logout` | Logout | Capability Logout. |  | `docs/auth-access-control/capabilities/logout.md` |
| `auth-access-control.capability.system-bootstrap` | System Bootstrap | Capability System Bootstrap. |  | `docs/auth-access-control/capabilities/system-bootstrap.md` |

### Entity (4)

| ID | Label | Summary | Flags | Evidence |
| -- | ----- | ------- | ----- | -------- |
| `auth-access-control.AccessToken` | AccessToken | Bearer credential representing a session for a bounded window. | spec | `docs/auth-access-control/domain.md#accesstoken` |
| `auth-access-control.PermissionGrant` | PermissionGrant | Grant record binding a grantee to a permission key with an ALLOW or DENY effect. | spec | `docs/auth-access-control/domain.md#permissiongrant` |
| `auth-access-control.Principal` | Principal | Authenticated actor with role and direct permission assignments. | spec | `docs/auth-access-control/domain.md#principal` |
| `auth-access-control.Session` | Session | Server-owned authenticated session; its id is the authoritative JWT identity claim. | spec | `docs/auth-access-control/domain.md#session` |

**`auth-access-control.AccessToken` fields** (identity: tokenId)

| Field | Type | Required | Domain / constraint | Note |
| ----- | ---- | -------- | ------------------- | ---- |
| `tokenId` | `string` | yes |  | carried as JWT jti |
| `sessionId` | `string` | yes |  | carried as JWT sid |
| `issuedAt` | `datetime` | yes |  |  |
| `expiresAt` | `datetime` | yes |  |  |
| `revokedAt` | `datetime` | no |  |  |
| `scope` | `string[]` | no |  | cache; session remains source of truth |

**`auth-access-control.PermissionGrant` fields** (identity: grantId)

| Field | Type | Required | Domain / constraint | Note |
| ----- | ---- | -------- | ------------------- | ---- |
| `grantId` | `string` | yes |  |  |
| `granteeType` | `string` | yes | `role`, `principal` |  |
| `granteeKey` | `string` | yes |  |  |
| `permissionKey` | `string` | yes |  |  |
| `effect` | `string` | yes | `ALLOW`, `DENY` |  |
| `createdAt` | `datetime` | yes |  |  |

**`auth-access-control.Principal` fields** (identity: id)

| Field | Type | Required | Domain / constraint | Note |
| ----- | ---- | -------- | ------------------- | ---- |
| `id` | `string` | yes |  |  |
| `subjectType` | `string` | yes | `user`, `service`, `automation` |  |
| `status` | `string` | yes | `ACTIVE`, `DISABLED` |  |
| `roleKeys` | `string[]` | yes |  |  |
| `directPermissions` | `string[]` | no |  |  |

**`auth-access-control.Session` fields** (identity: id)

| Field | Type | Required | Domain / constraint | Note |
| ----- | ---- | -------- | ------------------- | ---- |
| `id` | `string` | yes |  | carried as JWT sid |
| `principalId` | `string` | yes |  |  |
| `status` | `string` | yes | `ACTIVE`, `TERMINATED`, `EXPIRED` |  |
| `effectivePermissions` | `string[]` | yes |  |  |
| `createdAt` | `datetime` | yes |  |  |
| `expiresAt` | `datetime` | yes |  |  |

### Value Object (3)

| ID | Label | Summary | Flags | Evidence |
| -- | ----- | ------- | ----- | -------- |
| `auth-access-control.AuthContext` | AuthContext | Normalized per-request authorization context built from the server-side session. |  | `docs/auth-access-control/domain.md#authcontext` |
| `auth-access-control.PermissionKey` | PermissionKey | Canonical three-segment permission identifier: microservice.scope.action. |  | `docs/auth-access-control/domain.md#permissionkey` |
| `auth-access-control.RoleDefinition` | RoleDefinition | Consumer-provided role to permission-key mapping used at bootstrap. | spec | `docs/auth-access-control/domain.md#roledefinition` |

**`auth-access-control.AuthContext` fields** (identity: principalId + sessionId + tokenId + sorted permissions)

| Field | Type | Required | Domain / constraint | Note |
| ----- | ---- | -------- | ------------------- | ---- |
| `principalId` | `string` | — | non-empty |  |
| `sessionId` | `string` | — | non-empty |  |
| `permissions` | `string[]` | — | deduplicated |  |
| `tokenId` | `string` | — | non-empty |  |
| `issuedAt` | `datetime` | — |  |  |
| `expiresAt` | `datetime` | — |  |  |

**`auth-access-control.PermissionKey` fields** (identity: all three segments)

| Field | Type | Required | Domain / constraint | Note |
| ----- | ---- | -------- | ------------------- | ---- |
| `microservice` | `string` | — | kebab-case |  |
| `scope` | `string` | — | kebab-case |  |
| `action` | `string` | — | camelCase |  |

**`auth-access-control.RoleDefinition` fields** (identity: roleKey)

| Field | Type | Required | Domain / constraint | Note |
| ----- | ---- | -------- | ------------------- | ---- |
| `roleKey` | `string` | yes | kebab-case, unique |  |
| `displayName` | `string` | yes |  |  |
| `permissions` | `string[]` | yes |  |  |

### Enumeration (3)

| ID | Label | Summary | Flags | Evidence |
| -- | ----- | ------- | ----- | -------- |
| `auth-access-control.AuthErrorCode` | AuthErrorCode | Declared closed set of authentication and authorization error outcomes. | spec | `docs/auth-access-control/domain.md#autherrorcode` |
| `auth-access-control.InactiveReason` | InactiveReason | Introspection reason vocabulary explaining why a token is not active. |  | `docs/auth-access-control/queries.md#introspecttoken` |
| `auth-access-control.RevocationReason` | RevocationReason | Allowed values of TokenRevoked.reason. |  | `docs/auth-access-control/events.md#tokenrevoked` |

### Error Code (15)

| ID | Label | Summary | Flags | Evidence |
| -- | ----- | ------- | ----- | -------- |
| `auth-access-control.AuthErrorCode.AUTH_REQUIRED` | AUTH_REQUIRED | Missing bearer token or equivalent credential. |  | `docs/auth-access-control/domain.md#autherrorcode` |
| `auth-access-control.AuthErrorCode.FORBIDDEN` | FORBIDDEN | Authenticated but missing required permission. |  | `docs/auth-access-control/domain.md#autherrorcode` |
| `auth-access-control.AuthErrorCode.INVALID_CREDENTIALS` | INVALID_CREDENTIALS | Returned when credential verification fails. Used across eight documents but absent from the AuthErrorCode enumeration. | **referenced-undefined** · **out-of-enum** · [CON-01](#con-01) | `docs/auth-access-control/operations.md#login` · `docs/auth-access-control/mappings.md#loginrequesttosession` · `docs/auth-access-control/capabilities/login.md` · `docs/auth-access-control/STORIES.md#us-02` · `docs/auth-access-control/workflows.md#endtoendauthflow` |
| `auth-access-control.AuthErrorCode.INVALID_TOKEN` | INVALID_TOKEN | Token cannot be verified or parsed. |  | `docs/auth-access-control/domain.md#autherrorcode` |
| `auth-access-control.AuthErrorCode.PRINCIPAL_DISABLED` | PRINCIPAL_DISABLED | Principal cannot authenticate because status is disabled. |  | `docs/auth-access-control/domain.md#autherrorcode` |
| `auth-access-control.AuthErrorCode.TOKEN_EXPIRED` | TOKEN_EXPIRED | Token expiration has passed. |  | `docs/auth-access-control/domain.md#autherrorcode` |
| `auth-access-control.AuthErrorCode.TOKEN_REVOKED` | TOKEN_REVOKED | Token was explicitly revoked. |  | `docs/auth-access-control/domain.md#autherrorcode` |
| `auth-access-control.InactiveReason.NOT_FOUND` | NOT_FOUND | Introspection inactive reason NOT_FOUND. |  | `docs/auth-access-control/queries.md#introspecttoken` |
| `auth-access-control.InactiveReason.SESSION_EXPIRED` | SESSION_EXPIRED | Introspection inactive reason SESSION_EXPIRED. |  | `docs/auth-access-control/queries.md#introspecttoken` |
| `auth-access-control.InactiveReason.SESSION_TERMINATED` | SESSION_TERMINATED | Introspection inactive reason SESSION_TERMINATED. |  | `docs/auth-access-control/queries.md#introspecttoken` |
| `auth-access-control.InactiveReason.TOKEN_EXPIRED` | TOKEN_EXPIRED | Introspection inactive reason TOKEN_EXPIRED. |  | `docs/auth-access-control/queries.md#introspecttoken` |
| `auth-access-control.InactiveReason.TOKEN_REVOKED` | TOKEN_REVOKED | Introspection inactive reason TOKEN_REVOKED. |  | `docs/auth-access-control/queries.md#introspecttoken` |
| `auth-access-control.RevocationReason.ADMIN_FORCED_LOGOUT` | ADMIN_FORCED_LOGOUT | Revocation reason ADMIN_FORCED_LOGOUT. |  | `docs/auth-access-control/events.md#tokenrevoked` |
| `auth-access-control.RevocationReason.LOGOUT_ALL_SESSION_TOKENS` | LOGOUT_ALL_SESSION_TOKENS | Revocation reason LOGOUT_ALL_SESSION_TOKENS. |  | `docs/auth-access-control/events.md#tokenrevoked` |
| `auth-access-control.RevocationReason.LOGOUT_TARGETED` | LOGOUT_TARGETED | Revocation reason LOGOUT_TARGETED. |  | `docs/auth-access-control/events.md#tokenrevoked` |

### Permission Key (2)

| ID | Label | Summary | Flags | Evidence |
| -- | ----- | ------- | ----- | -------- |
| `auth-access-control.admin.logoutAnySession` | auth-access-control.admin.logoutAnySession | Permits terminating a session the caller does not own. |  | `docs/auth-access-control/operations.md#logout` · `docs/auth-access-control/queries.md#getpermissioncatalog` |
| `auth-access-control.read.introspectToken` | auth-access-control.read.introspectToken | Permits token introspection. |  | `docs/auth-access-control/capabilities/introspect-token.md` · `docs/auth-access-control/queries.md#getpermissioncatalog` |

### Behavior (6)

| ID | Label | Summary | Flags | Evidence |
| -- | ----- | ------- | ----- | -------- |
| `auth-access-control.AuthenticateRequest` | AuthenticateRequest | Verifies a bearer token and builds the request AuthContext. | spec | `docs/auth-access-control/operations.md#authenticaterequest` |
| `auth-access-control.AuthorizeRequest` | AuthorizeRequest | Decides route access from the AuthContext under deny-overrides. | spec | `docs/auth-access-control/operations.md#authorizerequest` |
| `auth-access-control.IssueAccessToken` | IssueAccessToken | Mints a signed token carrying sid, jti, iat, exp for an active session. | spec | `docs/auth-access-control/operations.md#issueaccesstoken` |
| `auth-access-control.Login` | Login | Verifies credentials and risk policy, then creates an ACTIVE session. | spec | `docs/auth-access-control/operations.md#login` |
| `auth-access-control.Logout` | Logout | Terminates a session and revokes its selected active tokens. | spec | `docs/auth-access-control/operations.md#logout` |
| `auth-access-control.SeedSystemBootstrap` | SeedSystemBootstrap | Creates the admin principal on first boot and syncs role grants on every boot. | spec | `docs/auth-access-control/operations.md#seedsystembootstrap` |

### Read Model (2)

| ID | Label | Summary | Flags | Evidence |
| -- | ----- | ------- | ----- | -------- |
| `auth-access-control.GetPermissionCatalog` | GetPermissionCatalog | Lists canonical permission keys with description and active/deprecated status. | spec | `docs/auth-access-control/queries.md#getpermissioncatalog` |
| `auth-access-control.IntrospectToken` | IntrospectToken | Reports token active state and a deterministic inactive reason. | spec | `docs/auth-access-control/queries.md#introspecttoken` |

### Lifecycle (2)

| ID | Label | Summary | Flags | Evidence |
| -- | ----- | ------- | ----- | -------- |
| `auth-access-control.SessionLifecycle` | SessionLifecycle | State model for Session. | spec | `docs/auth-access-control/states.md#sessionlifecycle` |
| `auth-access-control.TokenLifecycle` | TokenLifecycle | State model for AccessToken. | spec | `docs/auth-access-control/states.md#tokenlifecycle` |

### Lifecycle State (6)

| ID | Label | Summary | Flags | Evidence |
| -- | ----- | ------- | ----- | -------- |
| `auth-access-control.SessionLifecycle.ACTIVE` | ACTIVE | Session can issue and validate tokens. |  | `docs/auth-access-control/states.md#sessionlifecycle` |
| `auth-access-control.SessionLifecycle.EXPIRED` | EXPIRED | Session exceeded configured expiration. | terminal | `docs/auth-access-control/states.md#sessionlifecycle` |
| `auth-access-control.SessionLifecycle.TERMINATED` | TERMINATED | Session was explicitly ended by logout or admin action. | terminal | `docs/auth-access-control/states.md#sessionlifecycle` |
| `auth-access-control.TokenLifecycle.ACTIVE` | ACTIVE | Token can authenticate requests. |  | `docs/auth-access-control/states.md#tokenlifecycle` |
| `auth-access-control.TokenLifecycle.EXPIRED` | EXPIRED | Token exceeded expiration timestamp. | terminal | `docs/auth-access-control/states.md#tokenlifecycle` |
| `auth-access-control.TokenLifecycle.REVOKED` | REVOKED | Token invalidated before expiration. | terminal | `docs/auth-access-control/states.md#tokenlifecycle` |

### Domain Event (7)

| ID | Label | Summary | Flags | Evidence |
| -- | ----- | ------- | ----- | -------- |
| `auth-access-control.AccessDenied` | AccessDenied | Domain event emitted by AuthorizeRequest. |  | `docs/auth-access-control/events.md#accessdenied` |
| `auth-access-control.LoginSucceeded` | LoginSucceeded | Domain event emitted by Login. |  | `docs/auth-access-control/events.md#loginsucceeded` |
| `auth-access-control.LogoutCompleted` | LogoutCompleted | Domain event emitted by Logout. |  | `docs/auth-access-control/events.md#logoutcompleted` |
| `auth-access-control.SessionExpired` | SessionExpired | Referenced as a lifecycle transition trigger but absent from the event catalog. | **referenced-undefined** · [CON-05](#con-05) | `docs/auth-access-control/states.md` |
| `auth-access-control.TokenExpired` | TokenExpired | Referenced as a lifecycle transition trigger but absent from the event catalog. | **referenced-undefined** · [CON-05](#con-05) | `docs/auth-access-control/states.md` |
| `auth-access-control.TokenIssued` | TokenIssued | Domain event emitted by IssueAccessToken. |  | `docs/auth-access-control/events.md#tokenissued` |
| `auth-access-control.TokenRevoked` | TokenRevoked | Domain event emitted by Logout. |  | `docs/auth-access-control/events.md#tokenrevoked` |

### Decision Policy (3)

| ID | Label | Summary | Flags | Evidence |
| -- | ----- | ------- | ----- | -------- |
| `auth-access-control.InactiveReasonPrecedence` | InactiveReasonPrecedence | Selects a single inactive reason by strict precedence. |  | `docs/auth-access-control/queries.md#introspecttoken` |
| `auth-access-control.LoginRiskPolicy` | LoginRiskPolicy | Denies login on blocked IP reputation, five or more failed attempts in 15 minutes, or missing user-agent signal. Unnamed and unregistered in the source documents. | **unregistered** · [GAP-01](#gap-01) | `docs/auth-access-control/operations.md#login` |
| `auth-access-control.PermissionResolutionPolicy` | PermissionResolutionPolicy | Decides ALLOW or DENY for a required permission. |  | `docs/auth-access-control/workflows.md#permissionresolutionpolicy` |

### Orchestration (2)

| ID | Label | Summary | Flags | Evidence |
| -- | ----- | ------- | ----- | -------- |
| `auth-access-control.AuthorizeRequestFlow` | AuthorizeRequestFlow | Authenticate then authorize then execute handler. | spec | `docs/auth-access-control/workflows.md#authorizerequestflow` |
| `auth-access-control.EndToEndAuthFlow` | EndToEndAuthFlow | Login through protected call through logout. |  | `docs/auth-access-control/workflows.md#endtoendauthflow` |

### Constraint (12)

| ID | Label | Summary | Flags | Evidence |
| -- | ----- | ------- | ----- | -------- |
| `auth-access-control.constraint.I1` | I1 | Permission keys are canonical. — `permissionKey matches ^[a-z0-9-]+\.[a-z0-9-]+\.[a-zA-Z0-9*]+$` | [CON-03](#con-03) | `docs/auth-access-control/domain.md#invariants` |
| `auth-access-control.constraint.I2` | I2 | Access token expiry is after issue time. — `expiresAt > issuedAt` |  | `docs/auth-access-control/domain.md#invariants` |
| `auth-access-control.constraint.I3` | I3 | Revoked token cannot be active. — `revokedAt != null => tokenState != ACTIVE` |  | `docs/auth-access-control/domain.md#invariants` |
| `auth-access-control.constraint.I4` | I4 | Effective permissions are unique. — `len(effectivePermissions) = len(unique(effectivePermissions))` |  | `docs/auth-access-control/domain.md#invariants` |
| `auth-access-control.constraint.I5` | I5 | JWT identity claim is session id. — `token.sid != null and token.sub is optional/non-authoritative` |  | `docs/auth-access-control/domain.md#invariants` |
| `auth-access-control.constraint.SL-I1` | SL-I1 | Session terminal states remain terminal. — `state in {TERMINATED, EXPIRED} => no outgoing transitions` |  | `docs/auth-access-control/states.md#sessionlifecycle` |
| `auth-access-control.constraint.SL-I2` | SL-I2 | Active session has future expiry. — `state = ACTIVE => now < expiresAt` |  | `docs/auth-access-control/states.md#sessionlifecycle` |
| `auth-access-control.constraint.TL-I1` | TL-I1 | Token terminal states remain terminal. — `state in {EXPIRED, REVOKED} => no outgoing transitions` |  | `docs/auth-access-control/states.md#tokenlifecycle` |
| `auth-access-control.constraint.TL-I2` | TL-I2 | ACTIVE tokens must not be revoked. — `state = ACTIVE => revokedAt = null` |  | `docs/auth-access-control/states.md#tokenlifecycle` |
| `auth-access-control.constraint.TL-I3` | TL-I3 | EXPIRED tokens are not accepted. — `state = EXPIRED => authDecision != ALLOW` |  | `docs/auth-access-control/states.md#tokenlifecycle` |
| `auth-access-control.constraint.WF-I1` | WF-I1 | Protected routes always authenticate first. — `route.protected = true => AuthenticateRequest executed before handler` |  | `docs/auth-access-control/workflows.md#authorizerequestflow` |
| `auth-access-control.constraint.WF-I2` | WF-I2 | Authorization never executes without auth context. — `AuthorizeRequest.input.authContext != null` |  | `docs/auth-access-control/workflows.md#authorizerequestflow` |

### Business Rule (24)

| ID | Label | Summary | Flags | Evidence |
| -- | ----- | ------- | ----- | -------- |
| `auth-access-control.AuthenticateRequest.R1` | AuthenticateRequest R1 | Bearer token must be present. — `authorizationHeader startsWith 'Bearer '` |  | `docs/auth-access-control/operations.md#authenticaterequest` |
| `auth-access-control.AuthenticateRequest.R2` | AuthenticateRequest R2 | Token signature and claims must verify. — `verifySignature(token) = true` |  | `docs/auth-access-control/operations.md#authenticaterequest` |
| `auth-access-control.AuthenticateRequest.R3` | AuthenticateRequest R3 | Token must not be expired. — `now < token.expiresAt` |  | `docs/auth-access-control/operations.md#authenticaterequest` |
| `auth-access-control.AuthenticateRequest.R4` | AuthenticateRequest R4 | Token must not be revoked. — `token.revokedAt = null` |  | `docs/auth-access-control/operations.md#authenticaterequest` |
| `auth-access-control.AuthenticateRequest.R5` | AuthenticateRequest R5 | Token must include session id claim. — `token.sid != null` |  | `docs/auth-access-control/operations.md#authenticaterequest` |
| `auth-access-control.AuthenticateRequest.R6` | AuthenticateRequest R6 | Session identified by sid must exist and be active. — `session(token.sid).status = ACTIVE` |  | `docs/auth-access-control/operations.md#authenticaterequest` |
| `auth-access-control.AuthorizeRequest.R1` | AuthorizeRequest R1 | Required permission must be canonical. — `requiredPermission matches permissionKeyPattern` |  | `docs/auth-access-control/operations.md#authorizerequest` |
| `auth-access-control.AuthorizeRequest.R2` | AuthorizeRequest R2 | Decision must be allow by precedence policy. — `decision(authContext.permissions, requiredPermission) = ALLOW` |  | `docs/auth-access-control/operations.md#authorizerequest` |
| `auth-access-control.AuthorizeRequest.R3` | AuthorizeRequest R3 | Deny rules override allow rules. — `exists denyMatch => decision = DENY` | [CON-04](#con-04) | `docs/auth-access-control/operations.md#authorizerequest` |
| `auth-access-control.IntrospectToken.R1` | IntrospectToken R1 | Token lookup must be deterministic. — `tokenRecord = findToken(token)` |  | `docs/auth-access-control/queries.md#introspecttoken` |
| `auth-access-control.IntrospectToken.R2` | IntrospectToken R2 | Active depends on token and session. — `active = (token.revokedAt = null) and (now < token.expiresAt) and (session.status = ACTIVE)` |  | `docs/auth-access-control/queries.md#introspecttoken` |
| `auth-access-control.IntrospectToken.R3` | IntrospectToken R3 | Inactive reason must be explicit. — `active = false => inactiveReason in {TOKEN_REVOKED, TOKEN_EXPIRED, SESSION_TERMINATED, SESSION_EXPIRED, NOT_FOUND}` |  | `docs/auth-access-control/queries.md#introspecttoken` |
| `auth-access-control.IssueAccessToken.R1` | IssueAccessToken R1 | Session must exist and be active. — `session.status = ACTIVE` |  | `docs/auth-access-control/operations.md#issueaccesstoken` |
| `auth-access-control.IssueAccessToken.R2` | IssueAccessToken R2 | ttlSeconds must be within configured bounds. — `minTtl <= ttlSeconds <= maxTtl` | [GAP-05](#gap-05) | `docs/auth-access-control/operations.md#issueaccesstoken` |
| `auth-access-control.Login.R1` | Login R1 | Principal must exist and be active. — `principal(identifier).status = ACTIVE` |  | `docs/auth-access-control/operations.md#login` |
| `auth-access-control.Login.R2` | Login R2 | Credential verification must succeed. — `verifyCredential(identifier, secret) = true` |  | `docs/auth-access-control/operations.md#login` |
| `auth-access-control.Login.R3` | Login R3 | Login policy checks must pass. — `riskPolicy(context) = ALLOW` |  | `docs/auth-access-control/operations.md#login` |
| `auth-access-control.Logout.R1` | Logout R1 | Session must exist and be active. — `session(sessionId).status = ACTIVE` |  | `docs/auth-access-control/operations.md#logout` |
| `auth-access-control.Logout.R2` | Logout R2 | Caller must own session or hold admin permission. — `caller.principalId = session.principalId or hasPermission(caller, 'auth-access-control.admin.logoutAnySession')` |  | `docs/auth-access-control/operations.md#logout` |
| `auth-access-control.Logout.R3` | Logout R3 | Revocation evidence must be persisted. — `persistRevocation(sessionId, revokedTokens) = success` |  | `docs/auth-access-control/operations.md#logout` |
| `auth-access-control.SeedSystemBootstrap.R1` | SeedSystemBootstrap R1 | Admin principal must not already exist. — `principal(adminUsername) = null` |  | `docs/auth-access-control/operations.md#seedsystembootstrap` |
| `auth-access-control.SeedSystemBootstrap.R2` | SeedSystemBootstrap R2 | Generated password must meet complexity. — `len(password) >= 24 and entropy >= 128 bits` |  | `docs/auth-access-control/operations.md#seedsystembootstrap` |
| `auth-access-control.SeedSystemBootstrap.R3` | SeedSystemBootstrap R3 | Credential hash must use bcrypt. — `credentialHash = bcrypt(password, costFactor=12)` |  | `docs/auth-access-control/operations.md#seedsystembootstrap` |
| `auth-access-control.SeedSystemBootstrap.R4` | SeedSystemBootstrap R4 | All predefined roles must have grants. — `for each role in RoleDefinitions: grants exist` | [CON-07](#con-07) | `docs/auth-access-control/operations.md#seedsystembootstrap` |

### Derivation Rule (10)

| ID | Label | Summary | Flags | Evidence |
| -- | ----- | ------- | ----- | -------- |
| `auth-access-control.AuthenticateRequest.C1` | AuthenticateRequest C1 | Auth context creation. — `authContext = mapClaims(token.claims) + resolveSession(token.sid)` |  | `docs/auth-access-control/operations.md#authenticaterequest` |
| `auth-access-control.AuthorizeRequest.C1` | AuthorizeRequest C1 | Permission match score. — `score = exact > scopedWildcard > globalWildcard` |  | `docs/auth-access-control/operations.md#authorizerequest` |
| `auth-access-control.IssueAccessToken.C1` | IssueAccessToken C1 | Token expiration. — `expiresAt = issuedAt + ttlSeconds` |  | `docs/auth-access-control/operations.md#issueaccesstoken` |
| `auth-access-control.IssueAccessToken.C2` | IssueAccessToken C2 | Minimal JWT claims. — `claims = { sid: session.id, jti, iat, exp }` |  | `docs/auth-access-control/operations.md#issueaccesstoken` |
| `auth-access-control.Login.C1` | Login C1 | Session expiration. — `session.expiresAt = now + 8h` |  | `docs/auth-access-control/operations.md#login` |
| `auth-access-control.Login.C2` | Login C2 | Effective permissions. — `session.effectivePermissions = resolvePermissions(principal.roleKeys, principal.directPermissions, permissionGrants)` |  | `docs/auth-access-control/operations.md#login` |
| `auth-access-control.Logout.C1` | Logout C1 | Revocation set. — `revokedTokens = tokenId ? {tokenId} : activeTokens(sessionId)` |  | `docs/auth-access-control/operations.md#logout` |
| `auth-access-control.SeedSystemBootstrap.C1` | SeedSystemBootstrap C1 | Generate admin password. — `password = crypto.randomBytes(32).toString('base64url')` |  | `docs/auth-access-control/operations.md#seedsystembootstrap` |
| `auth-access-control.SeedSystemBootstrap.C2` | SeedSystemBootstrap C2 | Create admin principal. — `principal = { identifier, subjectType: 'user', status: 'ACTIVE', roleKeys: ['admin'], credentialHash: bcrypt(password) }` |  | `docs/auth-access-control/operations.md#seedsystembootstrap` |
| `auth-access-control.SeedSystemBootstrap.C3` | SeedSystemBootstrap C3 | Seed role grants. — `for each RoleDefinition: for each permission: create PermissionGrant(granteeType='role', effect='ALLOW')` |  | `docs/auth-access-control/operations.md#seedsystembootstrap` |

### Guarantee (16)

| ID | Label | Summary | Flags | Evidence |
| -- | ----- | ------- | ----- | -------- |
| `auth-access-control.AuthenticateRequest.P1` | AuthenticateRequest P1 | Request is enriched with a normalized auth context. |  | `docs/auth-access-control/operations.md#authenticaterequest` |
| `auth-access-control.AuthenticateRequest.P2` | AuthenticateRequest P2 | Downstream components evaluate permissions deterministically. |  | `docs/auth-access-control/operations.md#authenticaterequest` |
| `auth-access-control.AuthorizeRequest.P1` | AuthorizeRequest P1 | Request proceeds when the decision is ALLOW. |  | `docs/auth-access-control/operations.md#authorizerequest` |
| `auth-access-control.AuthorizeRequest.P2` | AuthorizeRequest P2 | Rejection returns a deterministic FORBIDDEN contract. |  | `docs/auth-access-control/operations.md#authorizerequest` |
| `auth-access-control.IssueAccessToken.P1` | IssueAccessToken P1 | Signed access token is generated. |  | `docs/auth-access-control/operations.md#issueaccesstoken` |
| `auth-access-control.IssueAccessToken.P2` | IssueAccessToken P2 | Token metadata is persisted for introspection and revocation. |  | `docs/auth-access-control/operations.md#issueaccesstoken` |
| `auth-access-control.IssueAccessToken.P3` | IssueAccessToken P3 | Session id is the authoritative identity claim in the JWT. |  | `docs/auth-access-control/operations.md#issueaccesstoken` |
| `auth-access-control.Login.P1` | Login P1 | Session is created and persisted. |  | `docs/auth-access-control/operations.md#login` |
| `auth-access-control.Login.P2` | Login P2 | Access token is issued for the new session. |  | `docs/auth-access-control/operations.md#login` |
| `auth-access-control.Logout.P1` | Logout P1 | Session is marked terminated. |  | `docs/auth-access-control/operations.md#logout` |
| `auth-access-control.Logout.P2` | Logout P2 | Selected active tokens linked to the session are revoked. |  | `docs/auth-access-control/operations.md#logout` |
| `auth-access-control.Logout.P3` | Logout P3 | Revocation evidence is stored for introspection and audit. |  | `docs/auth-access-control/operations.md#logout` |
| `auth-access-control.SeedSystemBootstrap.P1` | SeedSystemBootstrap P1 | Admin principal exists with hashed credentials. |  | `docs/auth-access-control/operations.md#seedsystembootstrap` |
| `auth-access-control.SeedSystemBootstrap.P2` | SeedSystemBootstrap P2 | All role to permission grant mappings exist. |  | `docs/auth-access-control/operations.md#seedsystembootstrap` |
| `auth-access-control.SeedSystemBootstrap.P3` | SeedSystemBootstrap P3 | Generated admin password is logged once and never persisted in plaintext. |  | `docs/auth-access-control/operations.md#seedsystembootstrap` |
| `auth-access-control.SeedSystemBootstrap.P4` | SeedSystemBootstrap P4 | Subsequent boots skip principal creation but still enforce grant sync. |  | `docs/auth-access-control/operations.md#seedsystembootstrap` |

### Acceptance Claim (12)

| ID | Label | Summary | Flags | Evidence |
| -- | ----- | ------- | ----- | -------- |
| `auth-access-control.story.US-01` | US-01 | User logs in with valid credentials |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-02` | US-02 | Login rejected for invalid credentials or disabled principal | [CON-01](#con-01) | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-03` | US-03 | Protected endpoint validates bearer token and builds auth context |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-04` | US-04 | Authentication fails deterministically per rule |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-05` | US-05 | Route permission is enforced with deny-overrides policy | [CON-04](#con-04) | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-06` | US-06 | User terminates own session |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-07` | US-07 | Admin force-terminates another user's session |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-08` | US-08 | Inspect token state with explicit inactive reason |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-09` | US-09 | Admin lists available permissions |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-10` | US-10 | Admin principal is auto-created on first boot | [CON-02](#con-02) | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-11` | US-11 | Role permission grants are seeded on every boot | [CON-07](#con-07) | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-12` | US-12 | Subsequent boots skip admin creation but sync grants |  | `docs/auth-access-control/STORIES.md` |

### Decision (27)

| ID | Label | Summary | Flags | Evidence |
| -- | ----- | ------- | ----- | -------- |
| `auth-access-control.decision.DEC-001` | DEC-001 | Permission naming format is microservice.scope.action. | confirmed | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.decision.DEC-002` | DEC-002 | Authorization is deny-by-default when no permission match exists. | confirmed | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.decision.DEC-003` | DEC-003 | Deny permission matches override allow matches. | confirmed | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.decision.DEC-004` | DEC-004 | Wildcard support is allowed (service.scope.*, service.*.*, *.*.*) and evaluated by precedence. | confirmed | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.decision.DEC-005` | DEC-005 | Standard auth error payload is { code, message, details }. | confirmed | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.decision.DEC-006` | DEC-006 | Token metadata is persisted for revocation and introspection. | confirmed | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.decision.DEC-007` | DEC-007 | Protected route guard order is authenticate first, authorize second. | confirmed | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.decision.DEC-008` | DEC-008 | JWT carries only sid, jti, iat, exp; principal and permissions resolve server-side. | confirmed | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.decision.DEC-009` | DEC-009 | Login and logout are first-class operations backed by session lifecycle transitions. | confirmed | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.decision.DEC-010` | DEC-010 | Session TTL is fixed at 8 hours. | confirmed | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.decision.DEC-011` | DEC-011 | Session expiry rejects requests as AUTH_REQUIRED. | confirmed | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.decision.DEC-012` | DEC-012 | Token revocation evidence is persisted in database-backed storage. | confirmed | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.decision.DEC-013` | DEC-013 | Effective permissions resolve from Principal.roleKeys plus Principal.directPermissions using grants. | confirmed | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.decision.DEC-014` | DEC-014 | Permission catalog governance is registry-first. | confirmed | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.decision.DEC-015` | DEC-015 | Login credential contract is identifier plus password. | confirmed | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.decision.DEC-016` | DEC-016 | Login risk policy deny conditions are fixed. | confirmed | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.decision.DEC-017` | DEC-017 | IssueAccessToken session-activity violation maps to AUTH_REQUIRED. | confirmed | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.decision.DEC-018` | DEC-018 | TokenRevoked.reason uses a fixed enum. | confirmed | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.decision.DEC-019` | DEC-019 | Introspection inactive responses must include deterministic inactiveReason precedence. | confirmed | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.decision.DEC-AUTH-STRAVA-SCOPE-001` | DEC-AUTH-STRAVA-SCOPE-001 | First provider scope is link identity plus import of recent activity summaries. | confirmed · [CON-06](#con-06) | `.craft/ledger.yml` |
| `auth-access-control.decision.DEC-AUTH-TRANSPORT-001` | DEC-AUTH-TRANSPORT-001 | Session transport is hybrid: HttpOnly cookie for browser flows, bearer for service and API flows, over one server-owned session. | confirmed · [CON-06](#con-06) | `.craft/ledger.yml` |
| `auth-access-control.decision.DEC-DEFER-001` | DEC-DEFER-001 | Multi-factor authentication policy. | deferred | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.decision.DEC-DEFER-002` | DEC-DEFER-002 | Refresh-token rotation and token-family replay protections. | deferred | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.decision.DEC-DEFER-003` | DEC-DEFER-003 | Fine-grained attribute-based access control beyond permission keys. | deferred | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.decision.DEC-DEFER-004` | DEC-DEFER-004 | Cross-region key management and rotation operations. | deferred | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.decision.DEC-OPEN-001` | DEC-OPEN-001 | Session inactivity timeout behavior beyond the fixed 8-hour TTL; no sliding window in v1. | open | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.decision.GAP-AUTH-PRODUCTION-CUSTODY-001` | GAP-AUTH-PRODUCTION-CUSTODY-001 | Hosted production still needs an explicit database and managed secret/token custody backend. | deferred | `.craft/ledger.yml` |

### Boundary Concept (1)

| ID | Label | Summary | Flags | Evidence |
| -- | ----- | ------- | ----- | -------- |
| `auth-access-control.AuthAPI` | AuthAPI | External REST boundary with five routes. Registered in the SPEC Concept Registry, disclaimed by README.md#boundaries, and system-leaning. Modeled as a disputed boundary rather than as a domain concept. | spec · **referenced-undefined** · **disclaimed** · [CON-08](#con-08) | `docs/auth-access-control/SPEC.md#concept-registry` · `docs/auth-access-control/interfaces.md` · `README.md#boundaries` |

## Typed Relations

Bridge edges present: **0**. Realization, coverage, observation, and drift edges require system-branch evidence, which this run did not read.

| Edge type | Count | From roles | To roles | Meaning |
| --------- | ----- | ---------- | -------- | ------- |
| `owns_lifecycle_of` | 2 | lifecycle | entity | Lifecycle model governs an entity's states. |
| `has_state` | 6 | lifecycle | lifecycle_state | Lifecycle admits this state. |
| `transitions_to` | 4 | lifecycle_state | lifecycle_state | Legal transition; carries trigger, guard, effect. |
| `forbidden_transition` | 5 | lifecycle_state | lifecycle_state | Explicitly invalid transition and why. |
| `produces` | 5 | behavior | domain_event | Behavior emits a domain event. |
| `triggers_transition` | 6 | domain_event | lifecycle_state | Event drives entry into a lifecycle state. |
| `governs` | 3 | decision_policy | behavior, read_model | Policy decides a behavior's outcome. |
| `constrains` | 14 | constraint | * | Constraint restricts a concept's admissible values. |
| `orchestrates` | 7 | orchestration | behavior | Orchestration sequences a behavior. |
| `reads` | 3 | read_model | entity | Read model derives from an entity. |
| `resolves_to` | 3 | * | * | Grantee or field contributes permissions to a target. |
| `denies_with` | 13 | business_rule | error_code | Violated rule yields this error outcome. |
| `authorizes` | 2 | permission_key | behavior, read_model | Permission key gates a behavior. |
| `has_rule` | 24 | behavior, read_model | business_rule | Behavior declares this precondition. |
| `has_derivation` | 10 | behavior | derivation_rule | Behavior declares this calculation. |
| `guarantees` | 16 | behavior | guarantee | Behavior declares this postcondition. |
| `performs` | 13 | actor | behavior, read_model | Actor initiates the behavior. |
| `consumes` | 10 | actor | domain_event | Actor consumes the event. |
| `aggregates` | 26 | capability | * | Capability is composed of this concept. |
| `covers` | 30 | acceptance_claim | * | Acceptance claim asserts expected behavior of this concept. |
| `decided_by` | 25 | * | decision | Concept's meaning is fixed by this decision. |
| `member_of` | 14 | error_code | enumeration | Value belongs to this enumeration. |

### `owns_lifecycle_of` (2)

| From | To | Detail | Evidence |
| ---- | -- | ------ | -------- |
| `auth-access-control.SessionLifecycle` | `auth-access-control.Session` |  | `docs/auth-access-control/states.md#sessionlifecycle` |
| `auth-access-control.TokenLifecycle` | `auth-access-control.AccessToken` |  | `docs/auth-access-control/states.md#tokenlifecycle` |

### `has_state` (6)

| From | To | Detail | Evidence |
| ---- | -- | ------ | -------- |
| `auth-access-control.SessionLifecycle` | `auth-access-control.SessionLifecycle.ACTIVE` |  | `docs/auth-access-control/states.md#sessionlifecycle` |
| `auth-access-control.SessionLifecycle` | `auth-access-control.SessionLifecycle.EXPIRED` |  | `docs/auth-access-control/states.md#sessionlifecycle` |
| `auth-access-control.SessionLifecycle` | `auth-access-control.SessionLifecycle.TERMINATED` |  | `docs/auth-access-control/states.md#sessionlifecycle` |
| `auth-access-control.TokenLifecycle` | `auth-access-control.TokenLifecycle.ACTIVE` |  | `docs/auth-access-control/states.md#tokenlifecycle` |
| `auth-access-control.TokenLifecycle` | `auth-access-control.TokenLifecycle.EXPIRED` |  | `docs/auth-access-control/states.md#tokenlifecycle` |
| `auth-access-control.TokenLifecycle` | `auth-access-control.TokenLifecycle.REVOKED` |  | `docs/auth-access-control/states.md#tokenlifecycle` |

### `transitions_to` (4)

| From | To | Detail | Evidence |
| ---- | -- | ------ | -------- |
| `auth-access-control.SessionLifecycle.ACTIVE` | `auth-access-control.SessionLifecycle.EXPIRED` | trigger: auth-access-control.SessionExpired · guard: now >= session.expiresAt · effect: Reject further token issuance and authentication | `docs/auth-access-control/states.md#sessionlifecycle` |
| `auth-access-control.SessionLifecycle.ACTIVE` | `auth-access-control.SessionLifecycle.TERMINATED` | trigger: auth-access-control.LogoutCompleted · guard: Logout operation succeeds · effect: Revoke linked active tokens | `docs/auth-access-control/states.md#sessionlifecycle` |
| `auth-access-control.TokenLifecycle.ACTIVE` | `auth-access-control.TokenLifecycle.EXPIRED` | trigger: auth-access-control.TokenExpired · guard: now >= expiresAt · effect: Reject auth with TOKEN_EXPIRED | `docs/auth-access-control/states.md#tokenlifecycle` |
| `auth-access-control.TokenLifecycle.ACTIVE` | `auth-access-control.TokenLifecycle.REVOKED` | trigger: auth-access-control.TokenRevoked · guard: Revocation operation succeeds · effect: Reject auth with TOKEN_REVOKED | `docs/auth-access-control/states.md#tokenlifecycle` |

### `forbidden_transition` (5)

| From | To | Detail | Evidence |
| ---- | -- | ------ | -------- |
| `auth-access-control.SessionLifecycle.EXPIRED` | `auth-access-control.SessionLifecycle.ACTIVE` | trigger: LoginSucceeded · reason: Login creates a new session id instead of reactivating an expired session. | `docs/auth-access-control/states.md#sessionlifecycle` |
| `auth-access-control.SessionLifecycle.TERMINATED` | `auth-access-control.SessionLifecycle.ACTIVE` | trigger: LoginSucceeded · reason: Login creates a new session id instead of reactivating a terminated session. | `docs/auth-access-control/states.md#sessionlifecycle` |
| `auth-access-control.TokenLifecycle.EXPIRED` | `auth-access-control.TokenLifecycle.ACTIVE` | trigger: LoginSucceeded · reason: Login creates new tokens and does not reactivate an expired token. | `docs/auth-access-control/states.md#tokenlifecycle` |
| `auth-access-control.TokenLifecycle.EXPIRED` | `auth-access-control.TokenLifecycle.REVOKED` | trigger: TokenRevoked · reason: Expired token is terminal; revocation has no effect. | `docs/auth-access-control/states.md#tokenlifecycle` |
| `auth-access-control.TokenLifecycle.REVOKED` | `auth-access-control.TokenLifecycle.ACTIVE` | trigger: LoginSucceeded · reason: Login creates new tokens and does not reactivate a revoked token. | `docs/auth-access-control/states.md#tokenlifecycle` |

### `produces` (5)

| From | To | Detail | Evidence |
| ---- | -- | ------ | -------- |
| `auth-access-control.AuthorizeRequest` | `auth-access-control.AccessDenied` |  | `docs/auth-access-control/events.md#accessdenied` |
| `auth-access-control.IssueAccessToken` | `auth-access-control.TokenIssued` |  | `docs/auth-access-control/events.md#tokenissued` |
| `auth-access-control.Login` | `auth-access-control.LoginSucceeded` |  | `docs/auth-access-control/events.md#loginsucceeded` |
| `auth-access-control.Logout` | `auth-access-control.LogoutCompleted` |  | `docs/auth-access-control/events.md#logoutcompleted` |
| `auth-access-control.Logout` | `auth-access-control.TokenRevoked` |  | `docs/auth-access-control/events.md#tokenrevoked` |

### `triggers_transition` (6)

| From | To | Detail | Evidence |
| ---- | -- | ------ | -------- |
| `auth-access-control.LoginSucceeded` | `auth-access-control.SessionLifecycle.ACTIVE` |  | `docs/auth-access-control/events.md#loginsucceeded` |
| `auth-access-control.LogoutCompleted` | `auth-access-control.SessionLifecycle.TERMINATED` |  | `docs/auth-access-control/events.md#logoutcompleted` |
| `auth-access-control.SessionExpired` | `auth-access-control.SessionLifecycle.EXPIRED` |  | `docs/auth-access-control/states.md` |
| `auth-access-control.TokenExpired` | `auth-access-control.TokenLifecycle.EXPIRED` |  | `docs/auth-access-control/states.md` |
| `auth-access-control.TokenIssued` | `auth-access-control.TokenLifecycle.ACTIVE` |  | `docs/auth-access-control/events.md#tokenissued` |
| `auth-access-control.TokenRevoked` | `auth-access-control.TokenLifecycle.REVOKED` |  | `docs/auth-access-control/events.md#tokenrevoked` |

### `governs` (3)

| From | To | Detail | Evidence |
| ---- | -- | ------ | -------- |
| `auth-access-control.InactiveReasonPrecedence` | `auth-access-control.IntrospectToken` |  | `docs/auth-access-control/queries.md#introspecttoken` |
| `auth-access-control.LoginRiskPolicy` | `auth-access-control.Login` |  | `docs/auth-access-control/operations.md#login` |
| `auth-access-control.PermissionResolutionPolicy` | `auth-access-control.AuthorizeRequest` |  | `docs/auth-access-control/workflows.md#permissionresolutionpolicy` |

### `constrains` (14)

| From | To | Detail | Evidence |
| ---- | -- | ------ | -------- |
| `auth-access-control.constraint.I1` | `auth-access-control.PermissionGrant` |  | `docs/auth-access-control/domain.md#invariants` |
| `auth-access-control.constraint.I1` | `auth-access-control.PermissionKey` |  | `docs/auth-access-control/domain.md#invariants` |
| `auth-access-control.constraint.I1` | `auth-access-control.RoleDefinition` |  | `docs/auth-access-control/domain.md#invariants` |
| `auth-access-control.constraint.I2` | `auth-access-control.AccessToken` |  | `docs/auth-access-control/domain.md#invariants` |
| `auth-access-control.constraint.I3` | `auth-access-control.AccessToken` |  | `docs/auth-access-control/domain.md#invariants` |
| `auth-access-control.constraint.I4` | `auth-access-control.Session` |  | `docs/auth-access-control/domain.md#invariants` |
| `auth-access-control.constraint.I5` | `auth-access-control.AccessToken` |  | `docs/auth-access-control/domain.md#invariants` |
| `auth-access-control.constraint.SL-I1` | `auth-access-control.SessionLifecycle` |  | `docs/auth-access-control/states.md#sessionlifecycle` |
| `auth-access-control.constraint.SL-I2` | `auth-access-control.Session` |  | `docs/auth-access-control/states.md#sessionlifecycle` |
| `auth-access-control.constraint.TL-I1` | `auth-access-control.TokenLifecycle` |  | `docs/auth-access-control/states.md#tokenlifecycle` |
| `auth-access-control.constraint.TL-I2` | `auth-access-control.AccessToken` |  | `docs/auth-access-control/states.md#tokenlifecycle` |
| `auth-access-control.constraint.TL-I3` | `auth-access-control.AccessToken` |  | `docs/auth-access-control/states.md#tokenlifecycle` |
| `auth-access-control.constraint.WF-I1` | `auth-access-control.AuthorizeRequestFlow` |  | `docs/auth-access-control/workflows.md#authorizerequestflow` |
| `auth-access-control.constraint.WF-I2` | `auth-access-control.AuthorizeRequest` |  | `docs/auth-access-control/workflows.md#authorizerequestflow` |

### `orchestrates` (7)

| From | To | Detail | Evidence |
| ---- | -- | ------ | -------- |
| `auth-access-control.AuthorizeRequestFlow` | `auth-access-control.AuthenticateRequest` |  | `docs/auth-access-control/workflows.md#authorizerequestflow` |
| `auth-access-control.AuthorizeRequestFlow` | `auth-access-control.AuthorizeRequest` |  | `docs/auth-access-control/workflows.md#authorizerequestflow` |
| `auth-access-control.EndToEndAuthFlow` | `auth-access-control.AuthenticateRequest` |  | `docs/auth-access-control/workflows.md#endtoendauthflow` |
| `auth-access-control.EndToEndAuthFlow` | `auth-access-control.AuthorizeRequest` |  | `docs/auth-access-control/workflows.md#endtoendauthflow` |
| `auth-access-control.EndToEndAuthFlow` | `auth-access-control.IssueAccessToken` |  | `docs/auth-access-control/workflows.md#endtoendauthflow` |
| `auth-access-control.EndToEndAuthFlow` | `auth-access-control.Login` |  | `docs/auth-access-control/workflows.md#endtoendauthflow` |
| `auth-access-control.EndToEndAuthFlow` | `auth-access-control.Logout` |  | `docs/auth-access-control/workflows.md#endtoendauthflow` |

### `reads` (3)

| From | To | Detail | Evidence |
| ---- | -- | ------ | -------- |
| `auth-access-control.GetPermissionCatalog` | `auth-access-control.PermissionGrant` |  | `docs/auth-access-control/queries.md#getpermissioncatalog` |
| `auth-access-control.IntrospectToken` | `auth-access-control.AccessToken` |  | `docs/auth-access-control/queries.md#introspecttoken` |
| `auth-access-control.IntrospectToken` | `auth-access-control.Session` |  | `docs/auth-access-control/queries.md#introspecttoken` |

### `resolves_to` (3)

| From | To | Detail | Evidence |
| ---- | -- | ------ | -------- |
| `auth-access-control.PermissionGrant` | `auth-access-control.Session` | note: Grants contribute to effectivePermissions; effect is not carried through. · [CON-04](#con-04) | `docs/auth-access-control/operations.md#login` |
| `auth-access-control.Principal` | `auth-access-control.Session` | note: roleKeys + directPermissions + grants resolve to effectivePermissions. · [GAP-02](#gap-02) | `docs/auth-access-control/operations.md#login` |
| `auth-access-control.RoleDefinition` | `auth-access-control.PermissionGrant` | note: Bootstrap materializes role permissions as ALLOW grants. | `docs/auth-access-control/operations.md#seedsystembootstrap` |

### `denies_with` (13)

| From | To | Detail | Evidence |
| ---- | -- | ------ | -------- |
| `auth-access-control.AuthenticateRequest.R1` | `auth-access-control.AuthErrorCode.AUTH_REQUIRED` |  | `docs/auth-access-control/operations.md#authenticaterequest` |
| `auth-access-control.AuthenticateRequest.R2` | `auth-access-control.AuthErrorCode.INVALID_TOKEN` |  | `docs/auth-access-control/operations.md#authenticaterequest` |
| `auth-access-control.AuthenticateRequest.R3` | `auth-access-control.AuthErrorCode.TOKEN_EXPIRED` |  | `docs/auth-access-control/operations.md#authenticaterequest` |
| `auth-access-control.AuthenticateRequest.R4` | `auth-access-control.AuthErrorCode.TOKEN_REVOKED` |  | `docs/auth-access-control/operations.md#authenticaterequest` |
| `auth-access-control.AuthenticateRequest.R5` | `auth-access-control.AuthErrorCode.INVALID_TOKEN` |  | `docs/auth-access-control/operations.md#authenticaterequest` |
| `auth-access-control.AuthenticateRequest.R6` | `auth-access-control.AuthErrorCode.AUTH_REQUIRED` |  | `docs/auth-access-control/operations.md#authenticaterequest` |
| `auth-access-control.AuthorizeRequest.R2` | `auth-access-control.AuthErrorCode.FORBIDDEN` |  | `docs/auth-access-control/operations.md#authorizerequest` |
| `auth-access-control.IssueAccessToken.R1` | `auth-access-control.AuthErrorCode.AUTH_REQUIRED` |  | `docs/auth-access-control/operations.md#issueaccesstoken` |
| `auth-access-control.Login.R1` | `auth-access-control.AuthErrorCode.PRINCIPAL_DISABLED` |  | `docs/auth-access-control/operations.md#login` |
| `auth-access-control.Login.R2` | `auth-access-control.AuthErrorCode.INVALID_CREDENTIALS` |  | `docs/auth-access-control/operations.md#login` |
| `auth-access-control.Login.R3` | `auth-access-control.AuthErrorCode.FORBIDDEN` |  | `docs/auth-access-control/operations.md#login` |
| `auth-access-control.Logout.R1` | `auth-access-control.AuthErrorCode.AUTH_REQUIRED` |  | `docs/auth-access-control/operations.md#logout` |
| `auth-access-control.Logout.R2` | `auth-access-control.AuthErrorCode.FORBIDDEN` |  | `docs/auth-access-control/operations.md#logout` |

### `authorizes` (2)

| From | To | Detail | Evidence |
| ---- | -- | ------ | -------- |
| `auth-access-control.admin.logoutAnySession` | `auth-access-control.Logout` |  | `docs/auth-access-control/operations.md#logout` |
| `auth-access-control.read.introspectToken` | `auth-access-control.IntrospectToken` |  | `docs/auth-access-control/capabilities/introspect-token.md` |

### `has_rule` (24)

| From | To | Detail | Evidence |
| ---- | -- | ------ | -------- |
| `auth-access-control.AuthenticateRequest` | `auth-access-control.AuthenticateRequest.R1` |  | `docs/auth-access-control/operations.md#authenticaterequest` |
| `auth-access-control.AuthenticateRequest` | `auth-access-control.AuthenticateRequest.R2` |  | `docs/auth-access-control/operations.md#authenticaterequest` |
| `auth-access-control.AuthenticateRequest` | `auth-access-control.AuthenticateRequest.R3` |  | `docs/auth-access-control/operations.md#authenticaterequest` |
| `auth-access-control.AuthenticateRequest` | `auth-access-control.AuthenticateRequest.R4` |  | `docs/auth-access-control/operations.md#authenticaterequest` |
| `auth-access-control.AuthenticateRequest` | `auth-access-control.AuthenticateRequest.R5` |  | `docs/auth-access-control/operations.md#authenticaterequest` |
| `auth-access-control.AuthenticateRequest` | `auth-access-control.AuthenticateRequest.R6` |  | `docs/auth-access-control/operations.md#authenticaterequest` |
| `auth-access-control.AuthorizeRequest` | `auth-access-control.AuthorizeRequest.R1` |  | `docs/auth-access-control/operations.md#authorizerequest` |
| `auth-access-control.AuthorizeRequest` | `auth-access-control.AuthorizeRequest.R2` |  | `docs/auth-access-control/operations.md#authorizerequest` |
| `auth-access-control.AuthorizeRequest` | `auth-access-control.AuthorizeRequest.R3` |  | `docs/auth-access-control/operations.md#authorizerequest` |
| `auth-access-control.IntrospectToken` | `auth-access-control.IntrospectToken.R1` |  | `docs/auth-access-control/queries.md#introspecttoken` |
| `auth-access-control.IntrospectToken` | `auth-access-control.IntrospectToken.R2` |  | `docs/auth-access-control/queries.md#introspecttoken` |
| `auth-access-control.IntrospectToken` | `auth-access-control.IntrospectToken.R3` |  | `docs/auth-access-control/queries.md#introspecttoken` |
| `auth-access-control.IssueAccessToken` | `auth-access-control.IssueAccessToken.R1` |  | `docs/auth-access-control/operations.md#issueaccesstoken` |
| `auth-access-control.IssueAccessToken` | `auth-access-control.IssueAccessToken.R2` |  | `docs/auth-access-control/operations.md#issueaccesstoken` |
| `auth-access-control.Login` | `auth-access-control.Login.R1` |  | `docs/auth-access-control/operations.md#login` |
| `auth-access-control.Login` | `auth-access-control.Login.R2` |  | `docs/auth-access-control/operations.md#login` |
| `auth-access-control.Login` | `auth-access-control.Login.R3` |  | `docs/auth-access-control/operations.md#login` |
| `auth-access-control.Logout` | `auth-access-control.Logout.R1` |  | `docs/auth-access-control/operations.md#logout` |
| `auth-access-control.Logout` | `auth-access-control.Logout.R2` |  | `docs/auth-access-control/operations.md#logout` |
| `auth-access-control.Logout` | `auth-access-control.Logout.R3` |  | `docs/auth-access-control/operations.md#logout` |
| `auth-access-control.SeedSystemBootstrap` | `auth-access-control.SeedSystemBootstrap.R1` |  | `docs/auth-access-control/operations.md#seedsystembootstrap` |
| `auth-access-control.SeedSystemBootstrap` | `auth-access-control.SeedSystemBootstrap.R2` |  | `docs/auth-access-control/operations.md#seedsystembootstrap` |
| `auth-access-control.SeedSystemBootstrap` | `auth-access-control.SeedSystemBootstrap.R3` |  | `docs/auth-access-control/operations.md#seedsystembootstrap` |
| `auth-access-control.SeedSystemBootstrap` | `auth-access-control.SeedSystemBootstrap.R4` |  | `docs/auth-access-control/operations.md#seedsystembootstrap` |

### `has_derivation` (10)

| From | To | Detail | Evidence |
| ---- | -- | ------ | -------- |
| `auth-access-control.AuthenticateRequest` | `auth-access-control.AuthenticateRequest.C1` |  | `docs/auth-access-control/operations.md#authenticaterequest` |
| `auth-access-control.AuthorizeRequest` | `auth-access-control.AuthorizeRequest.C1` |  | `docs/auth-access-control/operations.md#authorizerequest` |
| `auth-access-control.IssueAccessToken` | `auth-access-control.IssueAccessToken.C1` |  | `docs/auth-access-control/operations.md#issueaccesstoken` |
| `auth-access-control.IssueAccessToken` | `auth-access-control.IssueAccessToken.C2` |  | `docs/auth-access-control/operations.md#issueaccesstoken` |
| `auth-access-control.Login` | `auth-access-control.Login.C1` |  | `docs/auth-access-control/operations.md#login` |
| `auth-access-control.Login` | `auth-access-control.Login.C2` |  | `docs/auth-access-control/operations.md#login` |
| `auth-access-control.Logout` | `auth-access-control.Logout.C1` |  | `docs/auth-access-control/operations.md#logout` |
| `auth-access-control.SeedSystemBootstrap` | `auth-access-control.SeedSystemBootstrap.C1` |  | `docs/auth-access-control/operations.md#seedsystembootstrap` |
| `auth-access-control.SeedSystemBootstrap` | `auth-access-control.SeedSystemBootstrap.C2` |  | `docs/auth-access-control/operations.md#seedsystembootstrap` |
| `auth-access-control.SeedSystemBootstrap` | `auth-access-control.SeedSystemBootstrap.C3` |  | `docs/auth-access-control/operations.md#seedsystembootstrap` |

### `guarantees` (16)

| From | To | Detail | Evidence |
| ---- | -- | ------ | -------- |
| `auth-access-control.AuthenticateRequest` | `auth-access-control.AuthenticateRequest.P1` |  | `docs/auth-access-control/operations.md#authenticaterequest` |
| `auth-access-control.AuthenticateRequest` | `auth-access-control.AuthenticateRequest.P2` |  | `docs/auth-access-control/operations.md#authenticaterequest` |
| `auth-access-control.AuthorizeRequest` | `auth-access-control.AuthorizeRequest.P1` |  | `docs/auth-access-control/operations.md#authorizerequest` |
| `auth-access-control.AuthorizeRequest` | `auth-access-control.AuthorizeRequest.P2` |  | `docs/auth-access-control/operations.md#authorizerequest` |
| `auth-access-control.IssueAccessToken` | `auth-access-control.IssueAccessToken.P1` |  | `docs/auth-access-control/operations.md#issueaccesstoken` |
| `auth-access-control.IssueAccessToken` | `auth-access-control.IssueAccessToken.P2` |  | `docs/auth-access-control/operations.md#issueaccesstoken` |
| `auth-access-control.IssueAccessToken` | `auth-access-control.IssueAccessToken.P3` |  | `docs/auth-access-control/operations.md#issueaccesstoken` |
| `auth-access-control.Login` | `auth-access-control.Login.P1` |  | `docs/auth-access-control/operations.md#login` |
| `auth-access-control.Login` | `auth-access-control.Login.P2` |  | `docs/auth-access-control/operations.md#login` |
| `auth-access-control.Logout` | `auth-access-control.Logout.P1` |  | `docs/auth-access-control/operations.md#logout` |
| `auth-access-control.Logout` | `auth-access-control.Logout.P2` |  | `docs/auth-access-control/operations.md#logout` |
| `auth-access-control.Logout` | `auth-access-control.Logout.P3` |  | `docs/auth-access-control/operations.md#logout` |
| `auth-access-control.SeedSystemBootstrap` | `auth-access-control.SeedSystemBootstrap.P1` |  | `docs/auth-access-control/operations.md#seedsystembootstrap` |
| `auth-access-control.SeedSystemBootstrap` | `auth-access-control.SeedSystemBootstrap.P2` |  | `docs/auth-access-control/operations.md#seedsystembootstrap` |
| `auth-access-control.SeedSystemBootstrap` | `auth-access-control.SeedSystemBootstrap.P3` |  | `docs/auth-access-control/operations.md#seedsystembootstrap` |
| `auth-access-control.SeedSystemBootstrap` | `auth-access-control.SeedSystemBootstrap.P4` |  | `docs/auth-access-control/operations.md#seedsystembootstrap` |

### `performs` (13)

| From | To | Detail | Evidence |
| ---- | -- | ------ | -------- |
| `actor.admin` | `auth-access-control.GetPermissionCatalog` |  | `docs/auth-access-control/queries.md#getpermissioncatalog` |
| `actor.admin` | `auth-access-control.Logout` |  | `docs/auth-access-control/operations.md#logout` |
| `actor.api-gateway` | `auth-access-control.AuthenticateRequest` |  | `docs/auth-access-control/operations.md#authenticaterequest` |
| `actor.api-gateway` | `auth-access-control.AuthorizeRequest` |  | `docs/auth-access-control/operations.md#authorizerequest` |
| `actor.application-lifecycle` | `auth-access-control.SeedSystemBootstrap` |  | `docs/auth-access-control/operations.md#seedsystembootstrap` |
| `actor.automation-principal` | `auth-access-control.Login` |  | `docs/auth-access-control/operations.md#login` |
| `actor.consuming-feature` | `auth-access-control.AuthenticateRequest` |  | `docs/auth-access-control/operations.md#authenticaterequest` |
| `actor.consuming-feature` | `auth-access-control.AuthorizeRequest` |  | `docs/auth-access-control/operations.md#authorizerequest` |
| `actor.consuming-feature` | `auth-access-control.GetPermissionCatalog` |  | `docs/auth-access-control/queries.md#getpermissioncatalog` |
| `actor.end-user` | `auth-access-control.Login` |  | `docs/auth-access-control/operations.md#login` |
| `actor.end-user` | `auth-access-control.Logout` |  | `docs/auth-access-control/operations.md#logout` |
| `actor.security-operator` | `auth-access-control.IntrospectToken` |  | `docs/auth-access-control/queries.md#introspecttoken` |
| `actor.service-principal` | `auth-access-control.Login` |  | `docs/auth-access-control/operations.md#login` |

### `consumes` (10)

| From | To | Detail | Evidence |
| ---- | -- | ------ | -------- |
| `actor.alerting-pipeline` | `auth-access-control.AccessDenied` |  | `docs/auth-access-control/events.md#accessdenied` |
| `actor.audit-subsystem` | `auth-access-control.LoginSucceeded` |  | `docs/auth-access-control/events.md#loginsucceeded` |
| `actor.audit-subsystem` | `auth-access-control.LogoutCompleted` |  | `docs/auth-access-control/events.md#logoutcompleted` |
| `actor.audit-subsystem` | `auth-access-control.TokenIssued` |  | `docs/auth-access-control/events.md#tokenissued` |
| `actor.audit-subsystem` | `auth-access-control.TokenRevoked` |  | `docs/auth-access-control/events.md#tokenrevoked` |
| `actor.cache-invalidator` | `auth-access-control.TokenRevoked` |  | `docs/auth-access-control/events.md#tokenrevoked` |
| `actor.security-analytics` | `auth-access-control.AccessDenied` |  | `docs/auth-access-control/events.md#accessdenied` |
| `actor.session-tracker` | `auth-access-control.LoginSucceeded` |  | `docs/auth-access-control/events.md#loginsucceeded` |
| `actor.session-tracker` | `auth-access-control.LogoutCompleted` |  | `docs/auth-access-control/events.md#logoutcompleted` |
| `actor.session-tracker` | `auth-access-control.TokenIssued` |  | `docs/auth-access-control/events.md#tokenissued` |

### `aggregates` (26)

| From | To | Detail | Evidence |
| ---- | -- | ------ | -------- |
| `auth-access-control.capability.authenticate-request` | `auth-access-control.AuthContext` |  | `docs/auth-access-control/capabilities/authenticate-request.md` |
| `auth-access-control.capability.authenticate-request` | `auth-access-control.AuthenticateRequest` |  | `docs/auth-access-control/capabilities/authenticate-request.md` |
| `auth-access-control.capability.authenticate-request` | `auth-access-control.AuthorizeRequestFlow` |  | `docs/auth-access-control/capabilities/authenticate-request.md` |
| `auth-access-control.capability.authorize-request` | `auth-access-control.AccessDenied` |  | `docs/auth-access-control/capabilities/authorize-request.md` |
| `auth-access-control.capability.authorize-request` | `auth-access-control.AuthorizeRequest` |  | `docs/auth-access-control/capabilities/authorize-request.md` |
| `auth-access-control.capability.authorize-request` | `auth-access-control.PermissionResolutionPolicy` |  | `docs/auth-access-control/capabilities/authorize-request.md` |
| `auth-access-control.capability.browse-permission-catalog` | `auth-access-control.GetPermissionCatalog` |  | `docs/auth-access-control/capabilities/browse-permission-catalog.md` |
| `auth-access-control.capability.browse-permission-catalog` | `auth-access-control.PermissionGrant` |  | `docs/auth-access-control/capabilities/browse-permission-catalog.md` |
| `auth-access-control.capability.browse-permission-catalog` | `auth-access-control.PermissionKey` |  | `docs/auth-access-control/capabilities/browse-permission-catalog.md` |
| `auth-access-control.capability.introspect-token` | `auth-access-control.AccessToken` |  | `docs/auth-access-control/capabilities/introspect-token.md` |
| `auth-access-control.capability.introspect-token` | `auth-access-control.InactiveReasonPrecedence` |  | `docs/auth-access-control/capabilities/introspect-token.md` |
| `auth-access-control.capability.introspect-token` | `auth-access-control.IntrospectToken` |  | `docs/auth-access-control/capabilities/introspect-token.md` |
| `auth-access-control.capability.login` | `auth-access-control.IssueAccessToken` |  | `docs/auth-access-control/capabilities/login.md` |
| `auth-access-control.capability.login` | `auth-access-control.Login` |  | `docs/auth-access-control/capabilities/login.md` |
| `auth-access-control.capability.login` | `auth-access-control.LoginSucceeded` |  | `docs/auth-access-control/capabilities/login.md` |
| `auth-access-control.capability.login` | `auth-access-control.SessionLifecycle` |  | `docs/auth-access-control/capabilities/login.md` |
| `auth-access-control.capability.login` | `auth-access-control.TokenIssued` |  | `docs/auth-access-control/capabilities/login.md` |
| `auth-access-control.capability.login` | `auth-access-control.TokenLifecycle` |  | `docs/auth-access-control/capabilities/login.md` |
| `auth-access-control.capability.logout` | `auth-access-control.Logout` |  | `docs/auth-access-control/capabilities/logout.md` |
| `auth-access-control.capability.logout` | `auth-access-control.LogoutCompleted` |  | `docs/auth-access-control/capabilities/logout.md` |
| `auth-access-control.capability.logout` | `auth-access-control.SessionLifecycle` |  | `docs/auth-access-control/capabilities/logout.md` |
| `auth-access-control.capability.logout` | `auth-access-control.TokenLifecycle` |  | `docs/auth-access-control/capabilities/logout.md` |
| `auth-access-control.capability.logout` | `auth-access-control.TokenRevoked` |  | `docs/auth-access-control/capabilities/logout.md` |
| `auth-access-control.capability.system-bootstrap` | `auth-access-control.PermissionGrant` |  | `docs/auth-access-control/capabilities/system-bootstrap.md` |
| `auth-access-control.capability.system-bootstrap` | `auth-access-control.RoleDefinition` |  | `docs/auth-access-control/capabilities/system-bootstrap.md` |
| `auth-access-control.capability.system-bootstrap` | `auth-access-control.SeedSystemBootstrap` |  | `docs/auth-access-control/capabilities/system-bootstrap.md` |

### `covers` (30)

| From | To | Detail | Evidence |
| ---- | -- | ------ | -------- |
| `auth-access-control.story.US-01` | `auth-access-control.IssueAccessToken` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-01` | `auth-access-control.Login` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-01` | `auth-access-control.LoginSucceeded` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-01` | `auth-access-control.SessionLifecycle` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-01` | `auth-access-control.TokenIssued` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-02` | `auth-access-control.AuthErrorCode.INVALID_CREDENTIALS` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-02` | `auth-access-control.AuthErrorCode.PRINCIPAL_DISABLED` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-02` | `auth-access-control.Login` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-02` | `auth-access-control.LoginRiskPolicy` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-03` | `auth-access-control.AuthContext` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-03` | `auth-access-control.AuthenticateRequest` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-04` | `auth-access-control.AuthErrorCode` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-04` | `auth-access-control.AuthenticateRequest` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-05` | `auth-access-control.AccessDenied` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-05` | `auth-access-control.AuthorizeRequest` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-05` | `auth-access-control.PermissionResolutionPolicy` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-06` | `auth-access-control.Logout` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-06` | `auth-access-control.SessionLifecycle.TERMINATED` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-06` | `auth-access-control.TokenLifecycle.REVOKED` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-07` | `auth-access-control.Logout` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-07` | `auth-access-control.admin.logoutAnySession` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-08` | `auth-access-control.InactiveReasonPrecedence` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-08` | `auth-access-control.IntrospectToken` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-09` | `auth-access-control.GetPermissionCatalog` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-09` | `auth-access-control.PermissionGrant` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-10` | `auth-access-control.Principal` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-10` | `auth-access-control.SeedSystemBootstrap` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-11` | `auth-access-control.RoleDefinition` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-11` | `auth-access-control.SeedSystemBootstrap` |  | `docs/auth-access-control/STORIES.md` |
| `auth-access-control.story.US-12` | `auth-access-control.SeedSystemBootstrap` |  | `docs/auth-access-control/STORIES.md` |

### `decided_by` (25)

| From | To | Detail | Evidence |
| ---- | -- | ------ | -------- |
| `auth-access-control.AccessToken` | `auth-access-control.decision.DEC-006` |  | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.AccessToken` | `auth-access-control.decision.DEC-008` |  | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.AuthErrorCode` | `auth-access-control.decision.DEC-005` |  | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.AuthErrorCode.AUTH_REQUIRED` | `auth-access-control.decision.DEC-011` |  | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.AuthenticateRequest.R6` | `auth-access-control.decision.DEC-011` |  | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.AuthorizeRequest.R3` | `auth-access-control.decision.DEC-003` |  | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.AuthorizeRequestFlow` | `auth-access-control.decision.DEC-007` |  | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.GetPermissionCatalog` | `auth-access-control.decision.DEC-014` |  | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.InactiveReasonPrecedence` | `auth-access-control.decision.DEC-019` |  | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.IssueAccessToken.R1` | `auth-access-control.decision.DEC-017` |  | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.Login` | `auth-access-control.decision.DEC-009` |  | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.Login` | `auth-access-control.decision.DEC-015` |  | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.Login.C1` | `auth-access-control.decision.DEC-010` |  | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.Login.C2` | `auth-access-control.decision.DEC-013` |  | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.LoginRiskPolicy` | `auth-access-control.decision.DEC-016` |  | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.Logout` | `auth-access-control.decision.DEC-009` |  | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.Logout.R3` | `auth-access-control.decision.DEC-012` |  | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.PermissionKey` | `auth-access-control.decision.DEC-001` |  | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.PermissionKey` | `auth-access-control.decision.DEC-004` |  | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.PermissionResolutionPolicy` | `auth-access-control.decision.DEC-002` |  | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.PermissionResolutionPolicy` | `auth-access-control.decision.DEC-003` |  | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.RevocationReason` | `auth-access-control.decision.DEC-018` |  | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.Session` | `auth-access-control.decision.DEC-010` |  | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.constraint.I1` | `auth-access-control.decision.DEC-004` |  | `docs/auth-access-control/decisions.en.md` |
| `auth-access-control.constraint.I5` | `auth-access-control.decision.DEC-008` |  | `docs/auth-access-control/decisions.en.md` |

### `member_of` (14)

| From | To | Detail | Evidence |
| ---- | -- | ------ | -------- |
| `auth-access-control.AuthErrorCode.AUTH_REQUIRED` | `auth-access-control.AuthErrorCode` |  | `docs/auth-access-control/domain.md#autherrorcode` |
| `auth-access-control.AuthErrorCode.FORBIDDEN` | `auth-access-control.AuthErrorCode` |  | `docs/auth-access-control/domain.md#autherrorcode` |
| `auth-access-control.AuthErrorCode.INVALID_TOKEN` | `auth-access-control.AuthErrorCode` |  | `docs/auth-access-control/domain.md#autherrorcode` |
| `auth-access-control.AuthErrorCode.PRINCIPAL_DISABLED` | `auth-access-control.AuthErrorCode` |  | `docs/auth-access-control/domain.md#autherrorcode` |
| `auth-access-control.AuthErrorCode.TOKEN_EXPIRED` | `auth-access-control.AuthErrorCode` |  | `docs/auth-access-control/domain.md#autherrorcode` |
| `auth-access-control.AuthErrorCode.TOKEN_REVOKED` | `auth-access-control.AuthErrorCode` |  | `docs/auth-access-control/domain.md#autherrorcode` |
| `auth-access-control.InactiveReason.NOT_FOUND` | `auth-access-control.InactiveReason` |  | `docs/auth-access-control/queries.md#introspecttoken` |
| `auth-access-control.InactiveReason.SESSION_EXPIRED` | `auth-access-control.InactiveReason` |  | `docs/auth-access-control/queries.md#introspecttoken` |
| `auth-access-control.InactiveReason.SESSION_TERMINATED` | `auth-access-control.InactiveReason` |  | `docs/auth-access-control/queries.md#introspecttoken` |
| `auth-access-control.InactiveReason.TOKEN_EXPIRED` | `auth-access-control.InactiveReason` |  | `docs/auth-access-control/queries.md#introspecttoken` |
| `auth-access-control.InactiveReason.TOKEN_REVOKED` | `auth-access-control.InactiveReason` |  | `docs/auth-access-control/queries.md#introspecttoken` |
| `auth-access-control.RevocationReason.ADMIN_FORCED_LOGOUT` | `auth-access-control.RevocationReason` |  | `docs/auth-access-control/events.md#tokenrevoked` |
| `auth-access-control.RevocationReason.LOGOUT_ALL_SESSION_TOKENS` | `auth-access-control.RevocationReason` |  | `docs/auth-access-control/events.md#tokenrevoked` |
| `auth-access-control.RevocationReason.LOGOUT_TARGETED` | `auth-access-control.RevocationReason` |  | `docs/auth-access-control/events.md#tokenrevoked` |

## Findings

**5 blockers · 7 flags · 1 note.** Every finding is a defect **between documents** on the business branch. None asserts anything about the implementation.

| ID | Severity | Summary | Action | Owner route |
| -- | -------- | ------- | ------ | ----------- |
| [CON-01](#con-01) | **blocker** | INVALID_CREDENTIALS is used as an error outcome but is not a member of AuthErrorCode. | `revise` | definitions-governance |
| [CON-02](#con-02) | **blocker** | Principal omits the identifier and credentialHash fields its own operations require. | `revise` | domainspec-owner |
| [CON-03](#con-03) | **blocker** | Canonical-key invariant I1 forbids the wildcards the domain requires. | `escalate-to-decision-gate` | decision-gate |
| [CON-04](#con-04) | **blocker** | Deny-overrides is undecidable on the declared authorization input. | `escalate-to-decision-gate` | decision-gate |
| [CON-05](#con-05) | **flag** | Two lifecycle triggers are not in the domain-event catalog. | `revise` | domainspec-owner |
| [CON-06](#con-06) | **blocker** | Project domain scope and DomainSpec domain scope disagree. | `escalate-to-decision-gate` | decision-gate |
| [CON-07](#con-07) | **flag** | Example roles are asserted as acceptance requirements. | `revise` | domainspec-owner |
| [CON-08](#con-08) | **flag** | AuthAPI is registered as a domain concept but declared out of scope. | `revise` | domainspec-owner |
| [GAP-01](#gap-01) | **flag** | The login risk policy is unnamed and unregistered. | `promote` | domainspec-owner |
| [GAP-02](#gap-02) | **flag** | No precedence between Principal.directPermissions and principal-scoped grants. | `revise` | domainspec-owner |
| [GAP-03](#gap-03) | **flag** | No business outcomes or value measures are defined. | `revise` | domainspec-owner |
| [GAP-04](#gap-04) | **flag** | Service and automation principals have no modeled path. | `split` | decision-gate |
| [GAP-05](#gap-05) | **note** | IssueAccessToken TTL bounds are undefined. | `revise` | domainspec-owner |

### CON-01

**BLOCKER · contradiction · open** — INVALID_CREDENTIALS is used as an error outcome but is not a member of AuthErrorCode.

AuthErrorCode enumerates six values and does not include INVALID_CREDENTIALS. The code is nonetheless returned by Login R2, by LoginRequestToSession validation, and asserted in workflows.md, capabilities/login.md, STORIES.md US-02, TEST-SPEC.md and UI-SPEC.md. Either the enumeration is incomplete or the code is out of vocabulary.

**Subjects:** `auth-access-control.AuthErrorCode`, `auth-access-control.AuthErrorCode.INVALID_CREDENTIALS`, `auth-access-control.Login.R2`

**Evidence:** `docs/auth-access-control/domain.md#autherrorcode` · `docs/auth-access-control/operations.md#login` · `docs/auth-access-control/mappings.md#loginrequesttosession` · `docs/auth-access-control/STORIES.md#us-02`

**Consequence:** AuthErrorCode cannot be treated as the closed error vocabulary.

**Recommended action:** `revise` → owner route `definitions-governance`

### CON-02

**BLOCKER · contradiction · open** — Principal omits the identifier and credentialHash fields its own operations require.

domain.md#principal declares id, subjectType, status, roleKeys, directPermissions. Login R1 and R2 resolve a principal by identifier and verify a credential; SeedSystemBootstrap C2 constructs a principal with identifier and credentialHash; LoginRequestToSession maps identifier to principalId by principal-resolution. Neither field is declared on the entity.

**Subjects:** `auth-access-control.Principal`, `auth-access-control.Login.R1`, `auth-access-control.Login.R2`, `auth-access-control.SeedSystemBootstrap.C2`

**Evidence:** `docs/auth-access-control/domain.md#principal` · `docs/auth-access-control/operations.md#login` · `docs/auth-access-control/operations.md#seedsystembootstrap` · `docs/auth-access-control/mappings.md#loginrequesttosession`

**Consequence:** The entity definition is incomplete against its declared behavior.

**Recommended action:** `revise` → owner route `domainspec-owner`

### CON-03

**BLOCKER · contradiction · open** — Canonical-key invariant I1 forbids the wildcards the domain requires.

I1 is ^[a-z0-9-]+\.[a-z0-9-]+\.[a-zA-Z0-9*]+$ so * is admissible only in the action segment. decisions.en.md confirms wildcard support for service.*.* and *.*.*; PermissionResolutionPolicy evaluates a globalWildcard tier; the extracted admin role grants player-management.*.*, player-makeup.*.* and financial-settlement.*.*. RoleDefinition invariants simultaneously require every role permission key to match I1. Separately, the PermissionKey value object constrains scope to kebab-case and action to camelCase, which admits no wildcard at all.

**Subjects:** `auth-access-control.constraint.I1`, `auth-access-control.PermissionKey`, `auth-access-control.RoleDefinition`, `auth-access-control.decision.DEC-004`

**Evidence:** `docs/auth-access-control/domain.md#invariants` · `docs/auth-access-control/domain.md#permissionkey` · `docs/auth-access-control/domain.md#roledefinition` · `docs/auth-access-control/decisions.en.md` · `docs/auth-access-control/workflows.md#permissionresolutionpolicy`

**Consequence:** The canonical-key rule is self-contradicting; confirmed decisions and seeded example grants violate the invariant they are declared to satisfy.

**Recommended action:** `escalate-to-decision-gate` → owner route `decision-gate`

### CON-04

**BLOCKER · contradiction · open** — Deny-overrides is undecidable on the declared authorization input.

AuthorizeRequest decides over authContext.permissions typed as a deduplicated string[], itself sourced from Session.effectivePermissions, also string[]. A flat string list cannot carry PermissionGrant.effect, so no DENY is representable at decision time, yet R3 states exists denyMatch => decision = DENY and the policy ranks deny above every allow tier. The documents never say whether DENY grants are applied during resolution and dropped, or are expected to survive into the decision.

**Subjects:** `auth-access-control.AuthorizeRequest.R3`, `auth-access-control.AuthContext`, `auth-access-control.Session`, `auth-access-control.PermissionResolutionPolicy`, `auth-access-control.decision.DEC-003`

**Evidence:** `docs/auth-access-control/domain.md#authcontext` · `docs/auth-access-control/domain.md#session` · `docs/auth-access-control/operations.md#authorizerequest` · `docs/auth-access-control/workflows.md#permissionresolutionpolicy`

**Consequence:** The deny-overrides commitment has no defined carrier.

**Recommended action:** `escalate-to-decision-gate` → owner route `decision-gate`

### CON-05

**FLAG · contradiction · open** — Two lifecycle triggers are not in the domain-event catalog.

states.md drives Session ACTIVE to EXPIRED on SessionExpired and AccessToken ACTIVE to EXPIRED on TokenExpired. events.md defines exactly five domain events and neither is among them, so two of the declared transitions are triggered by events with no definition, payload, or consumer.

**Subjects:** `auth-access-control.SessionExpired`, `auth-access-control.TokenExpired`

**Evidence:** `docs/auth-access-control/states.md#sessionlifecycle` · `docs/auth-access-control/states.md#tokenlifecycle` · `docs/auth-access-control/events.md`

**Consequence:** The event catalog is incomplete.

**Recommended action:** `revise` → owner route `domainspec-owner`

### CON-06

**BLOCKER · contradiction · open** — Project domain scope and DomainSpec domain scope disagree.

DEF-AUTH-UM-001 defines the project as packaging auth domain, session transport, user/resource authorization and provider link management; DEF-AUTH-UM-003 defines provider connection as a domain term; DEC-AUTH-TRANSPORT-001 commits to hybrid cookie plus bearer transport. The DomainSpec docs contain no ProviderConnection concept, no cookie-session concept and no ownership-based authorization concept, while README.md and docs/ADOPTION.md push OAuth providers and cookie transport out to consumers.

**Subjects:** `auth-access-control.decision.DEC-AUTH-TRANSPORT-001`, `auth-access-control.decision.DEC-AUTH-STRAVA-SCOPE-001`

**Evidence:** `.craft/ledger.yml` · `README.md#boundaries` · `docs/ADOPTION.md`

**Consequence:** The ledger's domain and the SPEC's domain are not the same domain.

**Recommended action:** `escalate-to-decision-gate` → owner route `decision-gate`

### CON-07

**FLAG · contradiction · open** — Example roles are asserted as acceptance requirements.

README.md and domain.md#roledefinition state that roles are consumer-provided and the extracted Poker Team roles are examples only, not exported as package defaults. SeedSystemBootstrap R4 and C3 require grants for all predefined roles, and US-11 asserts as an acceptance check that all four role definitions (admin, manager, coach, player) have grants, itemizing example permissions per role.

**Subjects:** `auth-access-control.RoleDefinition`, `auth-access-control.SeedSystemBootstrap.R4`, `auth-access-control.story.US-11`

**Evidence:** `README.md#boundaries` · `docs/auth-access-control/domain.md#roledefinition` · `docs/auth-access-control/operations.md#seedsystembootstrap` · `docs/auth-access-control/STORIES.md`

**Consequence:** The story treats documented examples as the domain.

**Recommended action:** `revise` → owner route `domainspec-owner`

### CON-08

**FLAG · contradiction · open** — AuthAPI is registered as a domain concept but declared out of scope.

README.md#boundaries states the package does not own HTTP routes, yet interfaces.md defines AuthAPI with five REST routes and SPEC.md registers auth-access-control.AuthAPI in the Concept Registry with three exposes edges into Login, AuthenticateRequest and AuthorizeRequest. A concept the package disclaims is a first-class node in its concept graph.

**Subjects:** `auth-access-control.AuthAPI`

**Evidence:** `README.md#boundaries` · `docs/auth-access-control/interfaces.md` · `docs/auth-access-control/SPEC.md#concept-registry`

**Consequence:** Boundary ambiguity between domain concept and consumer-contract example.

**Recommended action:** `revise` → owner route `domainspec-owner`

**Note:** auth-access-control.AuthAPI is deliberately NOT a node in this graph: it is system-branch and the package disclaims it. Recorded here as an unresolved boundary question.

### GAP-01

**FLAG · gap · open** — The login risk policy is unnamed and unregistered.

Login R3 depends on riskPolicy(context) with three deterministic deny conditions and three context defaults. Unlike PermissionResolutionPolicy it has no concept ID, no entry in the Concept Registry and no policy section in workflows.md.

**Subjects:** `auth-access-control.LoginRiskPolicy`

**Evidence:** `docs/auth-access-control/operations.md#login` · `docs/auth-access-control/SPEC.md#concept-registry`

**Consequence:** Load-bearing domain policy the ontology cannot address by an owned name.

**Recommended action:** `promote` → owner route `domainspec-owner`

### GAP-02

**FLAG · gap · open** — No precedence between Principal.directPermissions and principal-scoped grants.

PermissionGrant.granteeType admits principal, and Principal also carries directPermissions. Login C2 feeds both into resolvePermissions. No rule defines their relative precedence, nor whether a principal-scoped DENY grant overrides a listed direct permission.

**Subjects:** `auth-access-control.Principal`, `auth-access-control.PermissionGrant`, `auth-access-control.Login.C2`

**Evidence:** `docs/auth-access-control/domain.md#principal` · `docs/auth-access-control/domain.md#permissiongrant` · `docs/auth-access-control/operations.md#login`

**Consequence:** Permission resolution is underspecified. Related to CON-04 but independently unresolved.

**Recommended action:** `revise` → owner route `domainspec-owner`

### GAP-03

**FLAG · gap · open** — No business outcomes or value measures are defined.

The outcome and value-measure roles have zero instances. The domain defines behaviors, rules and guarantees but no target outcome that would let anyone judge whether the auth domain is achieving its purpose rather than merely executing its rules.

**Evidence:** `docs/auth-access-control/SPEC.md` · `docs/auth-access-control/decisions.en.md`

**Consequence:** The domain cannot be evaluated against intent, only against conformance.

**Recommended action:** `revise` → owner route `domainspec-owner`

### GAP-04

**FLAG · gap · open** — Service and automation principals have no modeled path.

subjectType admits user, service and automation. Every rule, story, policy and default is written for the human-user path: identifier plus password, user-agent presence as a risk signal, IP reputation. A service principal that legitimately has no user agent is denied by the risk policy as written. No story, rule or exception covers non-human principals.

**Subjects:** `auth-access-control.Principal`, `auth-access-control.LoginRiskPolicy`, `actor.service-principal`, `actor.automation-principal`

**Evidence:** `docs/auth-access-control/domain.md#principal` · `docs/auth-access-control/operations.md#login` · `docs/auth-access-control/STORIES.md`

**Consequence:** Two of three admitted principal kinds are unreachable under the stated policy.

**Recommended action:** `split` → owner route `decision-gate`

### GAP-05

**NOTE · gap · open** — IssueAccessToken TTL bounds are undefined.

R2 requires minTtl <= ttlSeconds <= maxTtl, but neither bound is defined anywhere in the domain documents and no decision fixes them, while the session TTL beside it is a fixed domain constant of 8 hours.

**Subjects:** `auth-access-control.IssueAccessToken.R2`

**Evidence:** `docs/auth-access-control/operations.md#issueaccesstoken` · `docs/auth-access-control/decisions.en.md`

**Consequence:** Two different TTL governance styles, one unresolved.

**Recommended action:** `revise` → owner route `domainspec-owner`

## Intentional Asymmetries

Recorded so a later pass does not re-open them as defects.

- **ASYM-01** — Authentication collapses session state into AUTH_REQUIRED while introspection expands it into five reasons. *Rationale:* decisions.en.md confirms that session expiry rejects requests as AUTH_REQUIRED. (`docs/auth-access-control/decisions.en.md` · `docs/auth-access-control/queries.md#introspecttoken`)

## Confidence

Evidence confidence and commitment confidence are tracked separately. This document executes no promotion (`executes_promotion: false`).

| Cluster | Evidence | Commitment | Action | Rationale | Findings |
| ------- | -------- | ---------- | ------ | --------- | -------- |
| Session and token lifecycles | high | high | `keep` | States, transitions, invalid transitions and invariants are all explicit. |  |
| Authenticate rules R1 to R6 and error mapping | high | high | `keep` | Rules, error states, stories and capability doc agree verbatim. |  |
| Domain events | medium | medium | `revise` | Payloads and consumers defined, but two lifecycle triggers are missing. | [CON-05](#con-05) |
| Permission model | low | high | `escalate-to-decision-gate` | Commitment exceeds evidence: I1, the value object, the wildcard decisions and the role examples mutually conflict. | [CON-03](#con-03) |
| Authorization decision | low | high | `escalate-to-decision-gate` | Commitment exceeds evidence: the declared input type cannot carry the decision. | [CON-04](#con-04), [GAP-02](#gap-02) |
| Principal identity and credentials | low | medium | `revise` | The entity omits the fields its operations use. | [CON-02](#con-02) |
| Error vocabulary | low | medium | `revise` | INVALID_CREDENTIALS is out of enum across eight documents. | [CON-01](#con-01) |
| Project domain scope | low | low | `escalate-to-decision-gate` | Ledger and SPEC describe different domains. | [CON-06](#con-06) |
| Login risk policy | medium | high | `promote` | Behavior fully specified, concept unregistered. | [GAP-01](#gap-01) |
| Non-human principals | low | low | `split` | Admitted by the type, unmodeled everywhere. | [GAP-04](#gap-04) |

**Promotions recommended:** 1 (CC-risk-policy). **Demotions recommended:** 0.

Three clusters carry commitment confidence above evidence confidence and are held at the decision gate rather than demoted, because the confirmed decisions may be right and the documents wrong.

## What This Ontology Does Not Establish

- That any modeled concept is implemented. No system-branch evidence was read.
- That any finding is a defect in code. Each is a defect between documents.
- Any change to docs/auth-access-control/. Nothing there was mutated.

