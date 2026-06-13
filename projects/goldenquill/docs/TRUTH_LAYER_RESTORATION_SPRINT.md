
# Golden Quill / Tilth — Truth-Layer Restoration Sprint v2

Status: ACTIVE
Scope: runtime recovery, projection governance, CI guardrails
Primary Law: no feature is real until it passes through the governed path.

## 1. Governed Path

```text
Python governed projection endpoint
→ strict identity envelope
→ Pydantic-validated response
→ one React API client
→ read-only UI
→ no fixture fallback in production
```

## 2. Scope Split

### Restoration Sprint

Immediate scope:

```text
Phase 0: Containment, baseline, active canon types
Phase 1: Python projection truth layer
Phase 1.5: Legacy test burn-down
Phase 2: React consumer + locked posture screen
Phase 3: Shim characterization + deletion/quarantine
Phase 4: CI guardrails
```

Goal:

```text
One governed Scout projection path.
```

### Productization Track

Deferred until Restoration Sprint is green:

```text
Indexed SQLite read model
Golden Image
non-founder operator test
backup/restore
support runbook
first 60-day customer success path
```

## 3. Phase 0 — Containment, Baseline, Canon Types

Deliverables:

```text
docs/TRUTH_LAYER_RESTORATION_SPRINT.md
docs/ARCHITECTURE_RECOVERY_DECISION.md
docs/CANON_TYPES.md
docs/recovery_baselines/
```

Acceptance gate:

```text
No runtime code changed.
PR #97 status recorded.
Existing failures and bypasses recorded.
Canonical Phase 1 types locked.
```

## 4. Phase 1 — Python Truth Layer

Deliverables:

```text
/api/projections/current
strict base64 X-Identity-Context
Pydantic CurrentProjectionResponse
scout_pipeline rows
source_kind/source_path provenance
tracked tiny scout fixture corpus
anti-demo sentinel tests
```

Acceptance gate:

```text
Targeted projection contract tests pass.
No production fixture fallback.
Malformed identity returns 401.
Valid identity returns governed projection envelope.
```

## 5. Phase 1.5 — Legacy Test Burn-Down

Deliverables:

```text
legacy IdentityContext tests migrated
old projection expectations updated
global nervous_system tests repaired or explicitly quarantined
```

Acceptance gate:

```text
Legacy tests no longer assert old identity shape.
Global suite failures are not hidden behind Phase 1.
```

## 6. Phase 2 — React Consumer

Deliverables:

```text
SubstrateClient is the only projection access path
no direct fetch/axios outside approved client
locked posture screen for 401/403
React consumes Python projection only
```

Required locked screen text:

```text
Operator Identity Unverified or Missing.
Projection Locked.
```

Acceptance gate:

```text
UI cannot read raw CSV/staging data.
UI cannot use Node shim.
UI cannot show projection data without valid identity.
UI gracefully locks on 401/403.
```

## 7. Phase 3 — Shim Characterization and Deletion / Quarantine

Deliverables:

```text
tracked sample fixture
Node shim output characterization
Python parity comparison
server.mjs/staging.mjs deleted or quarantined after parity
static check prevents resurrection
```

Acceptance gate:

```text
Python path matches required shim behavior on sample fixture, except intentional governance changes.
Shim is no longer runtime-load-bearing.
```

## 8. Phase 4 — CI Guardrails

Deliverables:

```text
scripts/agent_preflight_and_audit.sh
scripts/verify_no_direct_fetch.sh
scripts/verify_no_fixture_fallbacks.sh
scripts/verify_react_api_boundary.sh
scripts/verify_projection_contract.py
scripts/verify_pr_lane_scope.sh
CI workflow checks
```

Acceptance gate:

```text
CI fails mixed-surface PRs.
CI fails rogue fetches.
CI fails fixture fallback.
CI fails malformed projection contracts.
CI fails shadow projection reintroduction.
```

## 9. Deferred Productization Track

After Restoration Sprint is green:

```text
SQLite indexed read model
Golden Image
non-founder operator test
backup/restore
support runbook
first 60-day customer success path
```

SQLite is the default indexed read model for app serving.

DuckDB remains future/analytics only unless a measured request-path need proves otherwise.

## 10. Forbidden Behaviors

```text
No shadow backend.
No UI-owned truth.
No fixture green.
No broad PR.
No temporary bypass without scheduled deletion or quarantine.
No architecture claim without runtime proof.
```
