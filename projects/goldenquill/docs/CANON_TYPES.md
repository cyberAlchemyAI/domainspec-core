# Golden Quill / Tilth — Canon Types for Truth-Layer Restoration

Status: ACTIVE FOR RESTORATION SPRINT  
Scope: Phase 0 through Phase 2 implementation guidance  
Purpose: temporary but authoritative type contract until runtime schemas are reconciled

## 1. Governing Rule

No feature is real until it passes through the governed path.

The governed path is:

```text
Python governed projection endpoint
→ strict identity envelope
→ Pydantic-validated response
→ one React API client
→ read-only UI
→ no fixture fallback in production
```

## 2. Active UI Surface

`apps/tilth_ui_react` is the active React operator UI path for the restoration sprint.

`apps/tilth_ui` and `apps/tilth_demo_v0` are historical/prototype surfaces unless explicitly reactivated by a later architecture decision.

## 3. VerificationState

Canonical Phase 1 `VerificationState` values:

```text
unverified
verified
needs_review
stale
blocked
```

Definitions:

* `unverified`: no validated evidence has been attached yet.
* `verified`: source-backed and current.
* `needs_review`: evidence exists, but human/system review is still required.
* `stale`: evidence was previously verified but is no longer fresh enough to rely on.
* `blocked`: the claim or row cannot proceed because a required condition is missing, invalid, forbidden, or unresolved.

`missing_evidence` is not a `VerificationState`.

Use `missing_evidence` as a blocker reason, evidence issue, or missing-material code.

## 4. IdentityContext v1

`X-Identity-Context` is a base64-encoded JSON envelope.

Canonical local development envelope:

```json
{
  "schema_version": "identity_context.v1",
  "org_slug": "example-org",
  "operator_id": "local-operator",
  "applied_as": "Example Organization",
  "node_fingerprint": "local-node-fingerprint",
  "origin": "local_ui",
  "token_validity": "valid",
  "is_human": true,
  "roles": ["operator"],
  "posture": "hybrid"
}
```

Allowed `origin` values:

```text
local_ui
test_harness
trusted_proxy
```

Allowed `posture` values:

```text
unrestricted
hybrid
sanitized
sovereign
```

## 5. Identity Failure Behavior

The Python API must fail closed.

```text
missing X-Identity-Context → 401
malformed base64 → 401
malformed JSON → 401
schema-invalid envelope → 401
token_validity != valid → 401
valid identity but unauthorized action → 403 only where an authorization hook already exists
```

## 6. Important Security Clarification

For local single-tenant Founder Node operation, `X-Identity-Context` is a trusted local operator envelope. It validates shape, posture, and operator context.

It is not a cryptographic authentication boundary.

Before any networked, hosted, or multi-tenant exposure, this envelope must be replaced by or wrapped in a signed/session-backed authentication mechanism.

## 7. Projection Response Direction

The active projection endpoint is:

```text
/api/projections/current
```

The response must be Pydantic-validated before it reaches React.

The response must preserve:

```text
CurrentProjectionResponse.scout_pipeline
```

Every row must include provenance sufficient to explain where it came from:

```text
source_kind
source_path
```

`source_record_id` may be added where available.

## 8. Fixture Rule

Production runtime must not silently fall back to demo or fixture data.

Developer fixture mode requires an explicit flag:

```text
TILTH_DEV_FIXTURE_MODE=1
```

Projection tests must include anti-demo sentinels.
