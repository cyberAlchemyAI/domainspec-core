---
feature: api-key-management
docType: spec
template: domainspec-spec
discovery_waiver_reason: "dry-run evidence for keystone cutover; no product discovery needed"
generatedBy: invoke define (dry-run, 2026-06-14)
---

# API Key Management

> **TASK-DRYRUN evidence.** Produced by exercising `invoke define` against the new
> `domainspec-spec/` baseline. Demonstrates: (1) template selection routed to DomainSpec,
> (2) discovery soft gate fired → `--skip-discovery` waiver written to frontmatter,
> (3) Concept Registry typed against the **canonical** DS-D1/DS-D2 IDs now in arcanum.

## What This Module Owns
Issuing, listing, and revoking API keys for service authentication, including key lifecycle and revocation propagation.

## Capabilities
| Capability | What | Key Aspects |
| --- | --- | --- |
| Key issuance | Mint a scoped API key for a principal | Operation + Event + State |
| Key revocation | Invalidate a key and propagate | Operation + Event + State transition |
| Key listing | Read active/revoked keys for a principal | Query |

## Concept Registry
| Concept | ID | Type (DS-D1) |
| --- | --- | --- |
| ApiKey | AKM-001 | [Entity](../../../../arcanum/definitions/DEFINITIONS.md#ds-d1-meta-type-system) |
| KeyScope | AKM-002 | Value Object |
| KeyStatus | AKM-003 | Enum / Type |
| IssueApiKey | AKM-004 | Operation |
| RevokeApiKey | AKM-005 | Operation |
| ListApiKeys | AKM-006 | Query |
| ApiKeyLifecycle | AKM-007 | State Machine |
| ApiKeyRevoked | AKM-008 | Event |

## Typed Relationships (DS-D2)
| Edge | From → To | Verb (DS-D2) |
| --- | --- | --- |
| IssueApiKey **produces** ApiKey | AKM-004 → AKM-001 | `produces` |
| RevokeApiKey **transitions** ApiKeyLifecycle | AKM-005 → AKM-007 | `transitions` |
| RevokeApiKey **emits** ApiKeyRevoked | AKM-005 → AKM-008 | `emits` |
| ListApiKeys **queries** ApiKey | AKM-006 → AKM-001 | `queries` |

## Aspect docs (would emit)
`operations.md` (IssueApiKey, RevokeApiKey), `queries.md` (ListApiKeys), `states.md` (ApiKeyLifecycle: Active → Revoked), `events.md` (ApiKeyRevoked).

---
**Dry-run verdict: PASS.** The DomainSpec template is selectable as the `define` baseline; the Concept Registry types resolve to the canonical DS-D1 meta-types in arcanum; DS-D2 edge verbs are used correctly; the discovery soft gate + waiver writeback behave as specified in `define.md`. The cutover works end-to-end.
