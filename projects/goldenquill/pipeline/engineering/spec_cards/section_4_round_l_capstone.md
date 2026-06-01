# Spec card — §4 Round L Capstone (Logician integration + BT property tests + cross-module fuzz)

**STATUS:** DRAFT (pre-staged 2026-04-22; awaiting Batches A/B/C LOCK + spec-card LOCK)

**Blueprint anchor:** `pipeline/blueprint/v0.1/section_04_logician.md` v2.1 (LOCKED-internal 2026-04-18, sha16 `e0507e6daaa18676`)
**Amendment anchor:** `pipeline/blueprint/v0.1/section_04_v2_2_consolidated_amendment.md` v2.2 (LOCKED 2026-04-21, sha16 `b643d0540a509715`) + v2.3 privacy router + v2.4/v2.5 canary/runtime-integrity (LOCKED-internal 2026-04-19)
**Architecture anchor:** `pipeline/architecture/v0.1/tilth_architecture_locked.md` v7 A1-A12 (LOCKED 2026-04-19)
**Round:** §4 Round L — Section-4 capstone integration + BT property tests + cross-module fuzz
**Spec-card version:** v1
**Date pre-staged:** 2026-04-22
**Precedent rounds:** §4 Logician Group 7 Batches A/B/C per-module LOCKs (target: 9/9 code rows at `LOCKED (committee 5/5 PASS cycle-1)` upon Batches A+B+C close); §4 v2.2 12-gate Wave 1-4 LOCKs (already complete, rows 68–86); §1 Round J capstone (LOCKED 2026-04-21), §2 Round K capstone (LOCKED 2026-04-22), §5 R13 capstone (LOCKED 2026-04-21) — the three patterns this round mirrors verbatim.

---

## Purpose

Section 4 Logician is built module-by-module across:

- **9 non-gate modules** (Group 7 Batches A/B/C — `pre_gate`, `post_gate`, `gate_runner`, `cedar_eval`, `claim_evidence`, `source_tag_verify`, `dossier_verify`, `admin_risk`, `conversation_log`).
- **12 amendment-enforcement gates** (v2.2 Waves 1-4 — F-AMDT-01 through F-AMDT-12, each its own committee-LOCKed module under `pipeline/logician/gates/`).
- **3 v2.x cross-cutting amendments** (v2.3 privacy router, v2.4 canary, v2.5 runtime-integrity — internal LOCKs awaiting cross-section promotion).

Round L is the **integration capstone**: verify these 21+ modules compose correctly as the Logician PRE → silent-loop → POST orchestrator at the §4.4.1 13-step level; verify the §4-owned BT invariants hold end-to-end across the gate runner; establish the §4 cross-module test-suite discipline at section scope.

This round does NOT write new §4 code. It writes the integration test surface that documents §4's whole-section coherence.

Promotes §4 from LOCKED-per-module (9/9 non-gate + 12/12 gate code rows + 3/3 v2.x amendments) to **LOCKED-as-a-whole-section** (Round L capstone verdict).

## Scope

**§4-owned BTs** (per architecture A1 BT registry):

- **BT7** — atomic claim-evidence sign-overwrite (`claim_evidence.py`).
- **BT9** — USER_DATA conversation-anchor integrity (`conversation_log.py`).
- **BT10** — DOC_SOURCED grep windowing + ±5 escalation + full-text fallback (`source_tag_verify.py`).
- **BT11** — cross-org dossier reference policy (`dossier_verify.py` + Cedar `cross_org_dossier_reference`).
- **BT13** — rails report signing under per-session HMAC (currently consumed via `gate_runner.py` § step 10; if `rails_report.py` lands as a separate module before Round L dispatch, fold into the test surface).
- **L-001** — operator final-review gate (verify-gate precedent honoured at §4.9).
- **M7** — health-tuple signature verification.
- **M8** — admin-risk ledger monotonicity (`admin_risk.py`).
- **M9** — per-org BYOK key scoping (Cedar `byok_key_scope`).
- **M11 / S11c** — dossier-lock cite-time three-part verify (canonical path × inode × content-hash, `dossier_verify.py`).
- **M14 / M15** — Cedar policy load + evaluation surface (`cedar_eval.py`); seed-manifest hash verification.

**Out of scope** (owned by other sections):
- BT1-BT4, BT6, BT8 → Section 1 (covered by §1 Round J capstone 2026-04-21).
- BT5 per-session provider quota / back-off → Section 5 (R13 capstone 2026-04-21).
- BT12 Channel F domain preflight → Section 3.
- BT14 Vault-topology family → Section 2 (Round K capstone 2026-04-22).
- BT15 USER+CONTEXT+RULE composability → Section 6 (Operating Envelope) — separate capstone.

Round L touches §1/§2/§3/§5 only through their existing public-API consumer surfaces. No cross-section behavioural binding.

## Integration test surface (cross-module)

Round L tests exercise the full §4 public surface as a single PRE → silent-loop → POST orchestrator lifecycle. Each test exercises ≥3 §4 modules in a single path.

### L.1 Gate runner lifecycle (calls all 21+ §4 modules end-to-end)

Per blueprint §4.4.1 + §4.2 — the 18-check PRE-gate sequence, mid-loop silent invariant, and 13-step POST-gate sequence:

1. **PRE-gate** (18 checks per §4.2.1, dispatched by `pre_gate.py`): cedar-signed → admin-risk-ledger → dossier-signoffs → corpus-complete → cedar-policy-compiles → KGIE → 13 caller-pre-computed checks (1-3, 5-9, 11-13, 16, 18). Verify strict-order short-circuit semantics: first FAIL aborts with `completed_checks` truncated to the failure inclusive.
2. **State machine** (per `gate_runner.py`): PRE → BETWEEN → POST → DONE; `LogicianMidLoopCall` raised on any violation with `F-PRE-19.logician_mid_loop_call`.
3. **POST-gate** (13 steps per §4.4.1, dispatched by `gate_runner.py`): claim-extraction (3) → source-tag verify (4, BT10) → S11c+BT11 dossier verify (5) → admin-risk hard-block (6, M8) → structural (7) → rigor-breach (8) → claim-evidence assembly (9, BT7) → rails-report signing (10, BT13) → lessons delta (11) → vault-write atomic (12) → Section-5 signal (13).
4. **v2.2 amendment gates** (12 F-AMDT-*): integrated where applicable per §4.5/§4.6 row tables — verify PRE-20..PRE-28 fire under their respective trigger conditions, POST-14/POST-15/POST-16 fire on verdict close + lock_history append.
5. **Cedar evaluation** (M14/M15): three policies (`org_isolation`, `byok_key_scope`, `cross_org_dossier_reference`) loaded from `vault_shared/cedar/` per §4.7 + §2.6.

Eight integration classes, one per major orchestrator phase:

- **L.1.a** — PRE-gate strict-order short-circuit (steps 1-18 from §4.2.1; verify abort propagation per §4.2.3).
- **L.1.b** — silent-loop invariant (§4.3): no operator-visible state between PRE and POST; `LogicianMidLoopCall` enforcement.
- **L.1.c** — POST claim-extraction + source-tag verify (steps 3, 4; BT10 cascade ±2 → ±5 → full-text).
- **L.1.d** — POST dossier verify + S11c three-part check (step 5; BT11 cross-org Cedar route).
- **L.1.e** — POST admin-risk hard-block + monotonicity (step 6; M8; F-POST-10).
- **L.1.f** — POST claim-evidence assembly + BT7 atomic sign-overwrite (step 9; canonicalise → hash → operator-sign → vault_write).
- **L.1.g** — POST rails-report signing (step 10; BT13 per-session HMAC; signature breaks on edit).
- **L.1.h** — POST conversation-log append + BT9 USER_DATA anchor (step 12 sub-path; chain-verify on subsequent reads).

Each integration class: ≥5 adversarial cases (inject signature tamper / chain break / monotonicity violation / Cedar policy mismatch / mid-loop-call attempt / partial-write-rollback failure / etc.; verify fail-closed propagation, verify no partial state leaks, verify lock_history append integrity).

**≥15 integration tests × 8 classes × adversarial expansion ≈ ≥30 integration test methods floor** (∼60 with parametric expansion).

### L.2 Per-BT property tests (≥12 per BT × 7 BTs = ≥84 property tests floor)

**BT7 — atomic claim-evidence sign-overwrite.** Property: `SignedClaimEvidenceMap` triple `(map, signature, operator_key_id)` round-trips byte-identically; signature breaks on any byte tamper to map; canonicalisation is deterministic for semantically-equal but key-shuffled inputs. Adversarial: post-delivery edit invalidates signature; signing under retired key still verifies historical maps; canonicalise-after-sign fails (operation-order invariant).

**BT9 — USER_DATA conversation-anchor integrity.** Property: every `ConversationLogEntry` carries a session_id + turn_ordinal + USER_DATA payload + predecessor_hash + session_key_signature; chain verify walks every link tail-to-head; per-session signing uses BT6-active key; retired keys verify historical entries but cannot sign new ones. Adversarial: hash-chain break mid-tail; signature verify against rotated-out key; in-place edit rejection at write boundary.

**BT10 — DOC_SOURCED grep windowing cascade.** Property: ±2-sentence default window matches → `verify_method = "grep_window_pm2"`; ±5-sentence escalation matches → `"grep_window_pm5"`; full-text fallback matches → `"grep_fulltext_fallback"`; all three miss → UNSOURCED. Property: M12 path-whitelist enforced before grep (no path traversal). Adversarial: tokenizer abbreviation-list malformed; symlink pointing outside `orgs/{slug}/materials/`; full-text fallback runs only when both windowed passes miss (efficiency + semantic correctness).

**BT11 — cross-org dossier reference policy.** Property: dossier under `orgs/A/...` cited from session anchored to `orgs/B/...` routes through `cedar_eval.evaluate("cross_org_dossier_reference", ...)`; Cedar denial reclassifies UNSOURCED with the Cedar failure_code propagated. Property: same-org dossier citation does NOT route through cross-org policy (efficiency invariant). Adversarial: malformed cross-org flag at ClaimEntity construction; Cedar policy unsigned → PRE-04 abort.

**BT13 — rails-report signing.** Property: rails report signed by Logician's per-session BT6 HMAC key before delivery; post-delivery edit invalidates signature. Property: rails report contains every flag batched in POST (no short-circuit). Adversarial: signature verify against pre-rotation key passes; against post-rotation key fails (rotation isolation); BT6 key absent at sign-time → fail-closed F-POST-03.

**M8 — admin-risk monotonicity.** Property: cumulative_low / cumulative_medium / cumulative_high never decrease across appends; rate-limit propagation from Section 1 BT3 surfaces F-POST-06; 18-entry register cardinality + canonical hash pinned at module load. Adversarial: decrement attempt → M8 FAIL; rate_limit_exceeded silently swallowed → HIGH no-hidden-scope finding.

**M11 / S11c — dossier-lock three-part check.** Property: path equality + inode equality + content-hash equality, all three independently checked; failure of ANY single leg reclassifies UNSOURCED. Property: cite-time uses lock-time captured metadata (TOCTOU window closed). Adversarial: path-equal/inode-different (atomic replace); inode-equal/hash-different (rare collision); hash-equal/path-different (move within materials/).

### L.3 Full PRE → silent-loop → POST parametric fuzz

Single harness: given a clean Logician instance, run the full lifecycle N times with N distinct `(org_slug, session_id, claim_set)` triples (N parametrized over `[2, 8, 16, 32]`). Verify:

- Every run produces a `PostGateResult(success=True, ...)` OR a fail-closed `PostGateResult(success=False, failure_code=...)` — never partial state.
- Every run's lock_history append (one per LOCK if any) carries F-AMDT-12 daily-log block.
- No cross-org claim-evidence map leak (Law 3 mechanical: session-A in org-A cannot reference dossier from org-B without Cedar `cross_org_dossier_reference` route).
- Admin-risk monotonicity holds across the full run (no decrement).
- Rails report signature verifies post-delivery; tamper invalidates.
- Conversation log chain integrity holds across all N sessions (no cross-session chain break).

Counted as a single parameterized test class with ≥ N runs per N value (so ∑ ≥ 58 individual test instances).

### L.4 §7 test-suite packaging

The §7 test suite (per §2 / §5 capstone precedent) becomes the canonical §4 test harness. Round L packages:

- `tests/logician/conftest_section_4.py` — fixture library (clean Logician instance with all 21+ modules wired, sample `PreGateInput` + `PostGateInput`, sample Cedar policy bundle, sample `ConversationLogEntry` chain, sample admin-risk register, mock vault_write capturing intent + canonical bytes, mock Section 1 keyring with BT6 rotation-aware lookup).
- `tests/logician/test_section_4_integration.py` — L.1 PRE → silent-loop → POST integration tests (8 classes).
- `tests/logician/test_section_4_bt_properties.py` — seven §4-owned BT property test classes (BT7 + BT9 + BT10 + BT11 + BT13 + M8 + M11/S11c).
- `tests/logician/test_section_4_lifecycle_property.py` — N-instance parametric fuzz harness (L.3).

## Dependencies

- All §4 Group 7 Batch A/B/C per-module LOCKs complete (target: 9/9 cycle-1 5/5 PASS).
- All v2.2 12-gate F-AMDT-* LOCKs already complete (Waves 1-4, rows 68–86).
- v2.3/v2.4/v2.5 internal LOCKs promoted (or carve-out documented).
- §1 Round J capstone LOCKED 2026-04-21 — Round L consumes §1 primitives via the public BT6 keyring + admin-risk-register + USER_DATA-anchor surface.
- §2 Round K capstone LOCKED 2026-04-22 — Round L consumes §2 vault-write public surface.
- §5 R13 capstone LOCKED 2026-04-21 — Round L's `gate_runner` ↔ §5 orchestrator wire-up consumed at §5's published surface.
- §3 Scout R11 LOCKED 2026-04-21 — Round L consumes Scout's Channel F disclosure log via §3 public surface.
- AST-lint R1-R7 clean on all 4 test files.
- `pyproject.toml` Python pin `>=3.11` + `.venv` 3.14 — run via `scripts/run_tests.sh` or `.venv/bin/python3 -m pytest`.

## Done definition

1. All 4 test files written with ≥84 property tests across the seven §4-owned BT/M-family invariants (≥12 per family) + ≥30 integration tests (L.1) + parametric fuzz harness (L.3).
2. ≥95% coverage on every §4 module via the union of per-module + cross-module tests.
3. AST-lint R1-R7 exit 0 on all test files.
4. Full suite green (baseline ≥6074 pass per Batch A pre-stage; Round L adds ≥150 tests → suite should clear 6224+ once Batches A+B+C LOCK without test churn).
5. Code Thesis Committee 5/5 PASS cycle-1 on the Round L capstone surface — OR self-LOCK per §1 Round J + §2 Round K + §5 R13 + §3 Scout R5-R9 + §5 Pipeline R3-R12 compositional-round precedent (test-only round composing already-LOCKed primitives; every consumed module has independent committee LOCK on record).
6. Operator signs — **§4 capstone LOCKED-as-a-whole**. Promotes all of Section 4 from LOCKED-per-module to LOCKED-as-a-whole-section.
7. Canonical daily_log LOCK block per gate #12 discipline; §0.5 paired-commit rows (4 test files as Index entries); `lock_history.v1.jsonl` row appended via `pipeline.harness.gates.append_lock_history` (F-AMDT-12 compliant) with `lock_class: "code"`, `scope: "Section 4 capstone — PRE→silent-loop→POST integration + BT property matrix + lifecycle parametric fuzz + §7 test suite"`.
8. MEMORY.md prepend + `memory/project_impl_section_4_round_l_capstone_locked.md`; blueprint §4 v2.1 + v2.2 + v2.3/v2.4/v2.5 header status lines amended to include "§4 LOCKED-as-a-whole 2026-04-YY".

## Test criteria

- L.2: ≥12 property tests per BT/M-family × 7 families = **≥84 floor**.
- L.1: ≥15 integration tests × 8 classes (orchestrator phases) with ≥5 adversarial cases each ≈ **≥30 integration test methods floor**.
- L.3: parametric fuzz harness across N ∈ {2, 8, 16, 32} `(org_slug, session_id, claim_set)` triples = **single parameterized class, ≥58 individual test instances**.
- Total floor: **≥150 tests**. E-024 capstone-shape multiplier 1.3× target ≈ 195 tests. §1 Round J landed 214 tests at 1.26×; §2 Round K landed 230 at 1.53×; §5 R13 landed ~160 at 1.3× — comparable target for Round L is 195-230.
- E-026 formal: use `__module__` lineage checks, not identity, for any cross-module Protocol lineage assertion (Round L composes Protocols across 21+ modules).
- Stage/undo-cap RAM-safety: monkeypatched constants for any vault-touching test (mirror §2 Round K K.3 RAM-safety pattern).
- Deterministic hash ops: canonical bytes recipe `json.dumps(obj, sort_keys=True, separators=(",",":"), ensure_ascii=False).encode("utf-8")` → SHA-3-512; no alternative encodings.
- `@dataclass(frozen=True, kw_only=True)` requirement — Python 3.10+; any `.venv` drift surfaced as collection-error, not test failure.

## §0.5 paired-commit rows

| Row | Content |
|-----|---------|
| Tests | `tests/logician/conftest_section_4.py` |
| Tests | `tests/logician/test_section_4_integration.py` |
| Tests | `tests/logician/test_section_4_bt_properties.py` |
| Tests | `tests/logician/test_section_4_lifecycle_property.py` |
| Lock history | `pipeline/engineering/lock_history.v1.jsonl` — Round L capstone row; `lock_class: "code"`; `scope: "Section 4 capstone — PRE→silent-loop→POST integration + BT property matrix + lifecycle parametric fuzz + §7 test suite"` |
| Blueprint | Update §4 v2.1 + v2.2 + v2.3/v2.4/v2.5 header status lines to include "§4 LOCKED-as-a-whole 2026-04-YY" |
| Memory | `memory/project_impl_section_4_round_l_capstone_locked.md` + MEMORY.md prepend |
| Daily log | Canonical LOCK block per gate #12 |

## Coupling

- **Downstream unlock:** §4 capstone LOCK-as-a-whole unblocks the §4 ↔ §6 Operating Envelope cross-section round (per `section_06_operating_envelope.md` v1-r1 LOCKED 2026-04-21). With §4 LOCKED-as-a-whole, the operating-envelope cross-section bindings can be exercised end-to-end.
- **§1 / §2 / §5 capstone precedent:** Round L mirrors all three precedent rounds verbatim in shape; the `tests/logician/` directory receives the same four-file capstone layout (`conftest_section_4.py` + `_integration.py` + `_bt_properties.py` + `_lifecycle_property.py`).
- **v2.2 gate composition:** the 12 F-AMDT-* gates are already individually LOCKED. Round L exercises them composed with the 9 non-gate modules — no per-gate property re-validation, only orchestrator-level invariant assertion (PRE-20..PRE-28 fire under trigger; POST-14/15/16 fire on verdict close + lock_history append; F-AMDT-07 v1.1 author-family anti-collision still holds under the cross-family math).
- **Self-LOCK candidacy:** Round L is test-only; every module it composes has an independent 5/5 PASS committee LOCK on record (post-Batches-A/B/C close). §1 Round J + §2 Round K + §5 R13 + §3 Scout R5-R9 + §5 Pipeline R3-R12 all self-LOCKed under analogous compositional-round precedent. Round L is a strong self-LOCK candidate with the same rationale. Committee dispatch remains available if operator prefers belt-and-suspenders.

## Self-LOCK eligibility (three questions)

Following §1 Round J + §2 Round K + §5 R13 precedent — the capstone author runs three audit questions before claiming self-LOCK:

1. **Did Round L modify any §4 production code?** — If YES, NOT self-LOCK eligible (committee dispatch required). If NO, proceed.
2. **Did Round L surface any §7 invariant that tests can't exercise cleanly?** — If YES, escalate (indicates blueprint/implementation gap, not test-author failure). If NO, proceed.
3. **Did Round L surface any cross-round behavioural surprise that wasn't caught by per-round tests?** — If YES, escalate (indicates per-round test surface gap; surface as a follow-up audit). If NO, self-LOCK eligible.

If all three answer NO + every consumed module is at LOCKED (committee 5/5 PASS cycle-1) or better, Round L self-LOCKs single-cycle per the established compositional-capstone precedent.

## Hard stops (STOP and report rather than paper over)

- Any §4-owned BT invariant that tests can't exercise cleanly (indicates blueprint/implementation gap).
- Any cross-round behavioural surprise surfaced by integration that wasn't caught by per-round tests.
- Coverage drop on any §4 module below its per-round LOCK baseline (≥95% target — drop indicates test-harness perturbation, but warrants investigation before LOCK).
- Full suite regression (any of the post-Batches-A/B/C green count drops).
- AST-lint violation that can't be resolved without a narrow-fix carve-out.
- F-AMDT-07 v1.1 author-family anti-collision math unsatisfied (would indicate substrate composition broke L-003 cross-family discipline).

## Round name and label

**§4 Round L** — alphabetical continuation of §1 Round J + §2 Round K. L is also "L"ogician. Spec card filename: `section_4_round_l_capstone.md`. Lock-history row's `committee_round`: `section_04_logician_round_l_capstone`.

---

*Spec card v1 — 2026-04-22 — §4 Round L capstone. Promotes §4 LOCKED-per-module → LOCKED-as-a-whole-section. Pre-staged at Batch A pre-stage time; awaits Batches A+B+C close + spec-card LOCK before dispatch. Mirrors §2 Round K spec-card structure verbatim.*
