# TASK-4: Lifecycle, Security, and Browser Acceptance

## Objective

Prove independent lifecycle effects, redaction/fail-closed behavior, and the
literal local browser scenario.

- Layer/slice: L3 / S4
- Wave: W4
- Dependencies: TASK-3
- Current gate: blocked

## Source Contracts

- `../../../design/MIGRATION-ROLLOUT.md`
- `../../../design/DATA-LIFECYCLE.md`
- `../../../design/SECURITY-ABUSE.md`
- `../../../design/VALIDATION-CONTRACTS.md`
- product change-to-check matrix and shared browser runtime contract

## Smallest Working Units

### SWU-ARC-DEGRADE-001 — Compatibility-drift and owner-loss transition

- Primary behavior: move an enabled or running candidate to an honest
  fail-closed degraded state when generated-package provenance drifts or a
  required execution owner becomes unavailable.
- Independent acceptance: zero new starts; existing owner history is preserved;
  projections show `Unavailable`, `Incompatible`, `Blocked`, or `Unknown` from
  owner truth; recovery requires compatibility/owner restoration and an
  explicit re-enable decision.
- Split analysis: compatibility drift and owner loss are distinct stressors but
  exercise the same state transition and recovery contract; separate fixtures
  are required under one transition boundary.
- Write scope: degradation state/service/UI fixtures and focused tests.
- Dependencies: accepted TASK-3 candidate and pinned compatibility/owner
  baselines.
- Evidence: digest-bound drift and owner-loss fixtures with launch counters,
  owner-history comparison, projected state, and recovery decision.

### SWU-ARC-DISABLE-001 — Disable and revoke launch authority

- Primary behavior: disable product add-on and reject every new/cached launch.
- Independent acceptance: zero new owner starts; owner history preserved;
  in-flight work is quarantined without fabricated cancellation.
- Write scope: lifecycle host/client/UI/tests.
- Dependencies: result actions.

### SWU-ARC-UNINSTALL-001 — Uninstall product-owned state

- Primary behavior: disable, revoke product grants/access, and remove only
  admitted product-owned configuration.
- Independent acceptance: Bootstrap-managed packages and external owner records
  follow their separate policies and are not silently deleted.
- Dependencies: one isolated copy of the accepted DISABLE-001 snapshot and an
  accepted retention policy.
- Write scope: product uninstall service/UI/tests only.
- Fixture rule: this branch cannot share mutated state with ROLLBACK-001; its
  starting snapshot digest and forbidden Bootstrap/history mutation counters
  are part of the receipt.

### SWU-ARC-ROLLBACK-001 — Restore a pinned prior product adapter/profile

- Primary behavior: restore a prior product manifest/adapter/runtime profile.
- Independent acceptance: owner history remains readable; generated packages
  are untouched; disable remains available if rollback fails.
- Dependencies: a separate isolated copy of the same accepted DISABLE-001
  snapshot and a pinned rollback fixture.
- Write scope: product rollback service/fixtures/tests.
- Fixture rule: rollback success and forced failure both preserve the starting
  owner-history digest and generated-package inventory; forced failure remains
  disabled.

### SWU-ARC-SECURITY-001 — Close security and repository gates

- Primary behavior: execute the complete negative matrix and repository checks.
- Independent acceptance: degradation plus both isolated lifecycle branches
  pass and recompose; all declared controls pass; defects open owning SWUs and
  are not repaired under this receipt.
- Write scope: evidence/receipts only.
- Dependencies: all product mutation SWUs, DEGRADE-001, and the admitted
  UNINSTALL-001 and ROLLBACK-001 branch receipts from the same accepted disabled
  snapshot digest.
- Validation: focused tests, browser-first suite, security pipeline,
  pre-release scan, `verify:alpha`.

### SWU-ARC-BROWSER-001 — Literal two-child local browser witness

- Primary behavior: execute the significant scenario in real Chrome against a
  local deterministic fixture.
- Independent acceptance: every proposal/approval/child/clarification/reload/
  result/disable observation and screenshot exists with redaction.
- Write scope: temporary fixture/evidence roots only; no runtime repair.
- Dependencies: SECURITY-001 pass and all deterministic gates.
- Validation: exact scenario matrix and screenshot/record bindings.
- Owner: browser validation owner.

## Synchronization

Lifecycle SWUs remain separate. UNINSTALL-001 and ROLLBACK-001 are parallel
branches from isolated copies of one accepted disabled snapshot; neither feeds
the other. Security recomposes only after both branch receipts and DEGRADE-001
pass. Security/browser validation cannot patch implementation. Bootstrap
restore is not a product SWU and requires its own Bootstrap route and approval.

## Completion Evidence

L3 implementation evidence closes only when the lifecycle, security, repository,
and live Chrome receipts are complete. Readiness still requires TASK-5.
