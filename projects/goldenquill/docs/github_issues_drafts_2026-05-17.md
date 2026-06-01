# GitHub Hardening Issues — Drafts for FIT-Farms/GoldenQuill
**Filed:** 2026-05-17
**Source:** Audit-prompt v1.1 surfaces + GitHub-AI feedback extraction (Codex synthesis 2026-05-17)
**Status:** drafts ready for operator review; post via `docs/post_hardening_issues_2026-05-17.sh`

---

## Issue 1: Lock-history backfill hardening + bounded sibling-chain depth verification

**Labels:** governance, ledger-integrity, hardening
**Milestone:** v0.2 substrate
**Priority:** P1
**Estimated effort:** 4-6h

### Background

`pipeline/engineering/lock_history.v1.jsonl` currently carries 198 rows with `row: null` (legacy schema pre-row-field rollout). Future v0.2 ledger migration could introduce explicit `backfilled: true` rows. Today's rows 234/235 dispositioned via append-only correction rows 263/264 set the byte-restoration precedent. Audit prompt v1.1 §G flags both as ongoing integrity concerns.

### Problem

(a) Backfilled rows currently lack explicit certification metadata — no record of who authorized the backfill or what evidence supports it. (b) Sibling-chain references (paired-commit rows sharing `lock_timestamp_utc`) can create verification loops without bounded depth, exposing the chain verifier to runaway recursion on malformed input.

### Acceptance criteria

- [ ] `backfilled: true` rows MUST carry `certified_by: <operator_ed25519_sig>` and `certification_evidence: <commit_or_pr_ref>`
- [ ] Sibling-chain verifier enforces max depth 3 hops before refusing
- [ ] Tests at `tests/engineering/test_lock_history_integrity.py` covering backfill certification + sibling-chain depth refusal
- [ ] v0.2 ledger-hygiene amendment authored at `pipeline/blueprint/v0.1/section_NN_ledger_hygiene_v0_2_amendment.md`

### Implementation notes

Rewrite of the 198 existing `row: null` rows is OUT OF SCOPE — they remain audit-only legacy. This issue covers the discipline for any future backfill or sibling-chain row going forward.

### Out of scope

- Rewriting the 198 legacy `row: null` rows (separate v0.2 ledger migration ticket)
- Schema upgrades to `lock_history.v1.jsonl` itself (paired-commit ceremony required — separate issue)

### Cross-references

- Audit prompt v1.1 §G (ledger integrity)
- Lock_history rows 234/235/263/264 dispositioned pattern

---

## Issue 2: Runtime scope guards for non-blueprint invariants (router.yaml schema, SFR-style format drift)

**Labels:** governance, runtime-guards, hardening
**Milestone:** v0.2 hardening
**Priority:** P1
**Estimated effort:** 3-5h

### Background

The §4 v2.x.6 LOCK (rows 234/235) introduced `provider_boundary.py` + `outbound_boundary.cedar` wrappers for runtime egress, but did not extend to `router.yaml` schema validation. The F-CLASS-* family covers classification/routing decisions but does not cover router.yaml malformation paths. Architecture-LOCK-only enforcement leaves runtime-config files without deterministic scope guards.

### Problem

A typo or schema violation in `router.yaml` fails at request time, not at boot — silent dispatch to wrong provider possible. There is no F-CLASS-* primitive that fires when a malformed router.yaml is loaded.

### Acceptance criteria

- [ ] `router.yaml` schema authored at `pipeline/orchestrator/schemas/router_schema.json`
- [ ] Boot-time validator at `pipeline/orchestrator/router_bootstrap.py` runs schema check fail-closed
- [ ] New F-CLASS-ROUTER-CONFIG-SCHEMA-INVALID gate added to `pipeline/logician/gates/`
- [ ] AST-lint rule for any router-modification code path that bypasses validation
- [ ] Tests at `tests/orchestrator/test_router_schema_validation.py`

### Implementation notes

Mirror the discipline of the §4 v2.x.6 provider_boundary wrappers: fail-closed at boot, AST-lint enforcement, F-CLASS-* primitive registration. The schema should cover provider family bindings, posture map, capstone hash pins, and seat assignment shape.

### Out of scope

- Extension to other YAML config files (separate per-file issues if needed)
- Migration of existing router.yaml to validated shape (covered implicitly by the boot-time validator's first run)

### Cross-references

- §4 v2.x.6 amendment
- Audit prompt v1.1 §3.D (posture routing)
- F-CLASS-* family

---

## Issue 3: Logician PRE/POST gate ordering drift detection

**Labels:** governance, logician, hardening
**Milestone:** v0.2 hardening
**Priority:** P2
**Estimated effort:** 2-4h

### Background

Logician gates execute in registered order. F-* primitive registration in `pipeline/logician/gates/__init__.py` (or equivalent) determines order. No current test asserts that order doesn't silently change across releases. Audit prompt v1.1 §B's universal acceptance question per F-* family implicitly assumes pinned ordering.

### Problem

Gate ordering can drift across refactors — e.g., a F-CLASS-* PRE-gate firing after a F-CARDS-* PRE-gate when they previously fired in the opposite order — without any test catching it. Cascading fail-closed surfaces can shift load between gates in ways that change which one fires first on a given malformation, weakening the audit-trail interpretation.

### Acceptance criteria

- [ ] `tests/logician/test_gate_ordering_pinned.py` asserts the canonical PRE/POST/COMMIT gate execution order for every registered family
- [ ] Ordering manifest at `pipeline/logician/gate_ordering_manifest.json` is the source of truth (signed asset, Ed25519)
- [ ] AST-lint rule against any registration code that bypasses the manifest
- [ ] Drift between manifest and runtime order fails the suite

### Implementation notes

The manifest should be operator-Ed25519-signed so unauthorized ordering changes fail the F-CARDS-SIGNATURE-INVALID-equivalent for gate ordering. The test should walk `pipeline/logician/gates/` and the registration map, compare against the manifest, and fail on any divergence.

### Out of scope

- Re-ordering existing gates (this issue ratifies current order as canonical)
- Cross-seat gate ordering (Scribe/Judge/Red Team gates are separate registries)

### Cross-references

- Audit prompt v1.1 §B (universal acceptance question per F-* family)
- §3.B.12 (cross-family import ban)

---

## Issue 4: Vault Law 3 metadata leakage audit (org_read_override + cross-org observable side channels)

**Labels:** governance, vault, Law-3, hardening
**Milestone:** Gate 2 first paid client
**Priority:** P0
**Estimated effort:** 6-8h

### Background

Law 3 (org isolation) enforces a hard boundary between per-org workspaces via the per-org adapter. `org_read_override` exists as an emergency operator-elevated read pattern. Metadata homogenization (timestamps, request IDs, log structure, ULID/UUID generation) could leak inter-org correlation signals even when payload boundaries hold. Audit prompt v1.1 §3.I.3 flags this surface but does not specify the leak vectors.

### Problem

An adversary observing two cross-org runs could infer relationships from metadata patterns: request-ID collisions, timestamp adjacency, log-shape similarity, ULID monotonicity. The payload boundary holds, but the metadata side channel violates the spirit of Law 3 — no client should be able to determine that another client uses the system simply by observing infrastructure-side patterns.

### Acceptance criteria

- [ ] `pipeline/vault/metadata_isolation_audit.py` enumerates every metadata field that crosses the org boundary
- [ ] `pipeline/vault/policies/metadata_homogenization.cedar` policy enforces homogenization (no raw timestamp, no shared request ID space, no cross-org-observable ULID monotonicity, per-org log-format namespacing)
- [ ] New F-VAULT-METADATA-LEAK gate added to `pipeline/logician/gates/`
- [ ] Tests at `tests/vault/test_metadata_isolation.py` covering known leak patterns
- [ ] `org_read_override` paths require operator Ed25519 attestation per invocation (not just per session)

### Implementation notes

The Cedar policy should be the load-bearing artifact. The Python audit script enumerates surfaces; the policy enforces. Per-invocation Ed25519 attestation on `org_read_override` is a meaningful operational tightening — current session-scope is too coarse for Gate-2 customer trust posture.

### Out of scope

- Re-architecting the per-org adapter shape (current adapter is correct; this issue tightens metadata)
- Cross-org analytics or aggregate reporting features (those require explicit operator-policy carve-outs, not addressed here)

### Cross-references

- Audit prompt v1.1 §3.I.3 (Law 3)
- §3.E.4 (per-org memory + KFR)
- Five Operating Laws (Law 3)

---

## Issue 5: Decimal-only currency tolerance (ban floats in KFR / tolerance comparisons)

**Labels:** governance, decimal-mandate, hardening
**Milestone:** v0.2 hardening
**Priority:** P1
**Estimated effort:** 4-6h

### Background

WPFA (§17) and KFR currency math have had R-WPFA-DECIMAL-MANDATE-ENERGY and adjacent Decimal-mandate AST-lint rules introduced for energy quantities. Extension to general currency / tolerance comparisons in KFR + admin_risk + funder award amounts is the natural next step.

### Problem

Float arithmetic in financial-amount comparisons (e.g., `if award_amount == 50000.0:` or `tolerance = 0.01 * principal`) introduces representation-error-driven false negatives in audit math. A grant amount comparison off by 0.0000001 due to float representation could cause a fail-closed gate to fire on legitimate awards, or worse, miss a real discrepancy.

### Acceptance criteria

- [ ] Extend AST-lint rule to `R-NO-FLOAT-IN-CURRENCY` — grep for float literals adjacent to currency-typed identifiers
- [ ] All KFR currency fields typed `Decimal` per the pydantic model
- [ ] Audit existing tolerance comparisons across `pipeline/` for float usage, convert to Decimal
- [ ] Tests at `tests/linting/test_r_no_float_in_currency.py` for known violation patterns
- [ ] Extend §17 v1.1 amendment to include currency-comparison Decimal mandate (paired-commit if amendment needed)

### Implementation notes

Mirror the R-WPFA-DECIMAL-MANDATE-ENERGY rule shape. The audit pass against existing code should produce a remediation diff; the AST-lint prevents recurrence. Identifier-adjacency heuristic: any variable named `*amount*`, `*award*`, `*budget*`, `*cost*`, `*tolerance*`, `*price*`, `*revenue*` should not be compared against a float literal.

### Out of scope

- Migration of historical KFR data with float values (requires per-org operator decision)
- Extension to non-currency Decimal mandates (energy is already covered; other physics quantities are separate issues)

### Cross-references

- §17 WPFA / CycleReceipt
- F-WPFA-* family
- Existing R-WPFA-DECIMAL-MANDATE-ENERGY rule
