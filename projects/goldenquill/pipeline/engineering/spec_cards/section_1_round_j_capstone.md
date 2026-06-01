# Spec card — §1 Round J Capstone (integration + BT property tests + §7 test suite)

**STATUS:** LOCKED

**Blueprint anchor:** `pipeline/blueprint/v0.1/section_1_sovereignty_envelope.md` v6 (LOCKED-internal 2026-04-18)
**Architecture anchor:** `pipeline/architecture/v0.1/tilth_architecture_locked.md` v7 A1-A12 (LOCKED 2026-04-19)
**Round:** §1 Round J — Section-1 capstone integration + property tests
**Spec-card version:** v1
**Date:** 2026-04-21
**Precedent rounds:** A (LOCKED 2026-04-19) / B (LOCKED 2026-04-19) / C (LOCKED 2026-04-19) / D (LOCKED 2026-04-19) / E (LOCKED 2026-04-19) / F/G/H/I (LOCKED-backfilled 2026-04-20 per F-03)

---

## Purpose

Section 1 is built module-by-module across Rounds A-I. Round J is the **integration capstone**: verify the 14 §1 modules compose correctly as a sovereignty envelope; verify the blueprint-tracked (BT) property invariants hold end-to-end; and establish the §7 test-suite discipline (cross-module property tests, boot sequence, adversarial harness). This round does NOT write new §1 code — it writes the integration test surface that Group 10 outside-audit will consume as proof that §1 is coherent.

Promotes §1 from LOCKED-per-module (Rounds A-I) to LOCKED-as-a-whole-section (Round J capstone verdict).

## Scope

**§1-owned BTs** (per blueprint §1 line 65): BT1, BT2, BT3, BT4, BT6, BT8. Round J writes property tests for these six.

Out of scope (owned by other sections):
- BT5 per-session provider quota/back-off → Section 5
- BT7 atomic claim-evidence sign-overwrite → Section 4
- BT9 USER_DATA conversation-anchor integrity → Section 4
- BT10 grep-check windowing → Section 4
- BT11 cross-org dossier reference policy → Section 4
- BT12 Channel F domain preflight → Section 3
- BT13 rails report signing → Section 4
- BT14 mount-identity tuple → Section 2

Round J test surface references downstream-owned BTs by their section but does not re-implement them. Integration test that touches BT14 mount identity calls into §2 Vault (§1 `within_org_root` consumes §2's `mount_identity_tuple` per the §3.11d v6 clarifier).

## Integration test surface (cross-module)

Round J tests exercise the full §1 public surface as a single boot-to-session lifecycle. Each test exercises ≥3 §1 modules in a single path:

### J.1 Boot sequence (calls Rounds A-I modules end-to-end)

- `_types.py` — primitive dataclasses instantiated.
- `crypto_primitives.py` — SHA-3-512 + HMAC primitives invoked.
- `org_slug.py` — operator org slug resolved, validated against the org isolation table.
- `topology.py` — org topology discovered from vault_shared roots.
- `audit.py` — audit ledger opened, boot event appended, ledger hash computed.
- `keys.py` — provider keys retrieved via Keychain + FileKeyStore decision.
- `isolation.py` — OrgRootGate bound to today's session; TOCTOU re-stat primed.
- `session.py` — session started, session envelope sealed.
- `interrupted_state.py` — resume path tested (simulated crash mid-session + recovery).
- `admin_risk.py` — BT3 ledger opened, watermark HMAC verified.
- `degradation_log.py` — BT8 degradation log opened, head hash confirmed.
- `rfa_envelope.py` — sample RFA envelope sealed under BT1 dual-hash.
- `project_context_envelope.py` — sample PROJECT_CONTEXT sealed.
- `router_integrity.py` — router.yaml loaded, pinned hash verified.
- `boot.py` — orchestrator composes all of the above; clean shutdown + re-boot idempotency verified.

Each integration test: ≥5 adversarial cases (inject Protocol raises at each layer; verify fail-closed propagates; verify no partial state leaks).

### J.2 Per-BT property tests (≥12 per BT; 6 BTs × 12 = ≥72 property tests floor)

**BT1 — SHA-3-512 + per-RFA nonce.** Property: every RFA envelope produces a distinct `content_hash` even when URL + content are byte-identical across sessions, because nonce is per-ingest. Property: `url_hash` is stable across identical URLs to support Logician's "same URL, different content" detection. Adversarial: pre-image construction attempt; verify nonce entropy prevents.

**BT2 — OS-level namespace isolation + TOCTOU closure.** Property: open → fd → fstat re-validation closes the rename-race window. Property: `O_NOFOLLOW | O_CLOEXEC` flags on every read. Adversarial: filesystem-race harness (symlink swap between `os.stat` and `os.open`); verify detected and fail-closed.

**BT3 — Admin-risk ledger rate-limits.** Property: 10-per-day RED cap enforced across operator-attestation events; watermark HMAC trailer intact. Property: lock-before-count ordering holds under concurrent appends. Adversarial: fork-race harness (multiple concurrent appends); verify critical-section protocol holds.

**BT4 — HSM-capable key storage.** Property: MacOSKeychainKeyStore + FileKeyStore + YubiHSMKeyStore all satisfy the KeyStore contract. Property: `_retrieve_raw` is the only override point; `retrieve` is inherited. Adversarial: KeyStore subclass that overrides `retrieve` directly — verify rejected at subclass-declaration time if possible, or at first `retrieve()` call.

**BT6 — M7 per-session HMAC key lifecycle.** Property: M7 key created at session start, rotated per operator policy, zeroized at session end. Property: M7Envelope / M7VerifierState round-trip. Adversarial: key-leak path via `bytes(key_buffer)` — verify blocked (the Section 1 Round E closure).

**BT8 — Degraded-run + bypass flag append-only log.** Property: M10 degraded_run flag appends hash-chained; M13 bypass flag appends under operator-retype gate. Property: per-ledger HMAC trailer with last_seq_id; monotonic-ns + wall-clock + boot_clock_history triangulation. Adversarial: boot_clock skew injection; verify bypass expiry still enforced.

### J.3 Full boot-sequence property test

Single harness: given a clean vault, boot Tilth through all §1 modules 100 times with 100 different org slugs (parametric fuzz). Verify:
- Every boot produces a LOCKED session envelope.
- No cross-boot state leakage.
- No cross-org file access attempts (Law 3 mechanical).
- Every boot's audit ledger hash-chain terminates at a valid trailer HMAC.
- Every boot's degradation log state is consistent with operator policy.

### J.4 §7 test suite

The §7 test suite (per §1 blueprint §7 scope definition) becomes the canonical §1 test harness. Round J packages:

- `tests/sovereignty/test_section_1_integration.py` — boot sequence integration tests (J.1).
- `tests/sovereignty/test_section_1_bt_properties.py` — six BT property test classes (J.2).
- `tests/sovereignty/test_section_1_boot_sequence_property.py` — 100-org fuzz harness (J.3).
- `tests/sovereignty/conftest.py` — fixture library (clean vault, operator keypair, sample RFA, sample PROJECT_CONTEXT).

## Dependencies

- All of Section 1 Rounds A-I LOCKED on disk (currently Rounds A-E formal LOCK, Rounds F-I LOCKED-backfilled via F-03 — Round J can run against LOCKED-backfilled state).
- Section 2 Vault `mount_identity_tuple` for BT14 cross-reference (if §2 is accessible; otherwise mock per §2 Protocol contract).
- §4 Logician gate infrastructure (tests reference but do not consume Logician runtime).
- Cedar policy files for Law 3 isolation test in J.3 (currently being drafted in parallel Cowork; mock if unavailable).
- AST-lint R1-R7 clean on all test files.

## Done definition

1. All 4 test files written with ≥72 property tests across the six §1-owned BTs (≥12 per BT) + ≥15 integration tests (J.1) + 100-org fuzz harness (J.3).
2. ≥95% coverage on every §1 module via the integration + property test surface (some §1 modules were previously covered by per-round unit tests; Round J adds cross-module coverage).
3. AST-lint R1-R7 exit 0 on all test files.
4. Full suite green (current baseline: 3526 tests pass per F-AMDT-11 LOCK; Round J adds ~120+ tests — suite should clear 3650+).
5. Code Thesis Committee 5/5 PASS cycle-1 on the Round J integration surface (one dispatch; committee reviews the test suite, not new §1 code).
6. Operator signs — **§1 capstone LOCKED**. Promotes all of Section 1 from LOCKED-per-module to LOCKED-as-a-whole-section.
7. Canonical daily_log LOCK block per gate #12 discipline; §0.5 paired-commit rows (4 test files as Index entries); lock_history row with `lock_class: "code"`.
8. MEMORY.md prepend + `memory/project_impl_section_1_round_j_capstone_locked.md`.

## Test criteria

Per J.2 above: ≥12 property tests per BT × 6 BTs = ≥72 floor.
Per J.1 above: ≥15 integration tests covering the boot sequence with ≥5 adversarial cases each = ≥90 test methods (≥75 parametric).
Per J.3 above: 100-org fuzz harness counts as a single parameterized test class.

Total floor: ≥170 tests. E-024 multiplier expectation: ~255 tests. E-026 formal — use `__module__` lineage checks, not identity, for any cross-module Protocol lineage assertion.

## §0.5 paired-commit rows

| Row | Content |
|-----|---------|
| Tests | `tests/sovereignty/test_section_1_integration.py` |
| Tests | `tests/sovereignty/test_section_1_bt_properties.py` |
| Tests | `tests/sovereignty/test_section_1_boot_sequence_property.py` |
| Tests | `tests/sovereignty/conftest.py` |
| Lock history | `pipeline/engineering/lock_history.v1.jsonl` — Round J capstone row; `lock_class: "code"`; `scope: "Section 1 capstone — integration + BT property tests + §7 test suite"` |
| Blueprint | Update §1 v6 status line to include "Round J capstone LOCKED 2026-04-YY" |
| Memory | `memory/project_impl_section_1_round_j_capstone_locked.md` + MEMORY.md prepend |
| Daily log | Canonical LOCK block per gate #12 |

## Coupling

- **Downstream unlock:** Section 1 capstone LOCK is the last precondition before Group 5 Section 2 Vault committee-review dispatch (promotes §2 from LOCKED-backfilled to formal committee LOCK).
- **Ed25519 ceremony:** if the Ed25519 seal ceremony runs before Round J, the capstone LOCK row carries the first Ed25519-signed lock_history entry — validating the end-to-end signing path.
- **Group 9 integration tests:** Round J's boot-sequence property test is the prototype for Group 9 E2E. Reuse the same fuzz harness structure.

---

*Spec card v1 — 2026-04-21 — Round J capstone. Promotes §1 LOCKED-per-module → LOCKED-as-a-whole-section. Dispatch when Wave 3 + Wave 4 close so the test-suite discipline inherits the v2.2 gate #12 daily_log LOCK-block rule from session 1.*
