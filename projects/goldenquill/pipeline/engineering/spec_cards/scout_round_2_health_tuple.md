# Spec card — pipeline.scout Round 2 (M7 health-tuple assembly + sign)

**STATUS:** LOCKED-backfilled

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_03_scout.md`
  - §2.3 `HealthTuple` + `SignedHealthTuple` schemas (lines 170–199) — **already landed in Round 1 `_types.py`**
  - §4.10 M7 assembly + sign (lines 923–1015) — implementation spec for this round
  - §5.3 BT6 M7 HMAC key lifecycle (lines 1101–1103) — Scout consumes the Section 1 primitive, does not manage keys
  - §6 failure codes F-SCOUT-H-01 / F-SCOUT-H-02 / F-SCOUT-H-03 / F-SCOUT-H-04 (lines 1210–1230)
  - §7.10 test surface for `health_tuple` (lines 1320–1335)
  - §8 pinned constants `SESSION_HMAC_KEY_LEN_BYTES=64` (already landed in Round 1 `_constants.py`)
  - §9 intent string `scout-run-log-write` (already landed)
- Section 1 consumed surface: `sign_health_tuple(session, tuple_bytes) -> bytes`, `hmac_sha3_512`, `Session`, `record_degradation`, `vault_write`, `nonce_registry.reserve` — all LOCKED per Rounds A–J and §2 Vault Rounds K–U.

**Blueprint hash-at-card:** `0a82d955f95b0fca` (sha3_512(section_03_scout.md)[:16]). Identical to Round 1 — no blueprint drift since Round 1 LOCK.

**Spec-card version:** v1
**Round:** Scout R2 of 11. Consumes Round 1 `HealthTuple` + `SignedHealthTuple` dataclasses and Round 1 `_constants.HEALTH_OK/DEGRADED/FAILED` + `INTENT_SCOUT_RUN_LOG_WRITE`.
**Futureproofing scope:** §4.6 / M7 signature surface is the §3 <-> §4 (Logician) contract. The Section 4 verifier is landed. Round 2 must produce bytes the already-landed `pipeline.logician` can re-derive and verify.

---

## Summary

Land `pipeline/scout/health_tuple.py` — the M7 assemble + sign call-site. Implements `assemble_and_sign_health_tuple(session, per_channel, per_channel_a_endpoints, run_wall_ns, run_tiebreak_seed) -> SignedHealthTuple`. Composes:

1. Per-channel state validation (A..F each ∈ {OK, DEGRADED, FAILED}); raises `HealthTupleSchemaError(code=F-SCOUT-H-01)` on drift.
2. Channel-A per-endpoint validation (`grants.gov`, `sam.gov`, `usaspending.gov`); raises `F-SCOUT-H-02`.
3. Backbone-failed derivation (`all three A endpoints == FAILED`).
4. `run_id` derivation: `sha3_512(session_id || run_wall_ns || monotonic_ns || urandom(8))[:24]` via hardened `_fresh_urandom` helper (A-v3-10 closure for short-read resilience → `F-SCOUT-H-03.urandom_short_read`).
5. `run_tiebreak_seed` length gate (exactly 16 bytes → `F-SCOUT-V-06`).
6. `HealthTuple` construction using Round 1's frozen kw-only dataclass.
7. Canonical bytes via Round 1's `health_tuple_canonical_bytes` (`json.dumps(sort_keys=True, separators=(",",":"), ensure_ascii=False).encode("utf-8")` under `_normalize_for_json`).
8. Delegated HMAC via Section 1 `sign_health_tuple(session, canonical) -> bytes` — Scout never opens the keystore.
9. `SignedHealthTuple` construction + vault write to `orgs/{slug}/scout/run_log/{run_id}-health.json` under `intent=INTENT_SCOUT_RUN_LOG_WRITE`.
10. Return the frozen `SignedHealthTuple` for Pipeline's downstream Logician verification.

No network. No direct keystore access. One vault write (gated by §2 Vault write path). Two crypto call-sites (Section 1 `sign_health_tuple` + `hashlib.sha3_512` for `run_id`).

## Design decisions (operator-disposed 2026-04-20, reversible)

1. **Blueprint vs §2.3 schema — `run_entropy` field disposition.** §2.3 `HealthTuple` schema does NOT list `run_entropy`; §4.10 body constructs it. Round 1's `_types.py` matched §2.3 (no `run_entropy`). Round 2 must resolve this:
   - **Option A (preferred):** Land `run_entropy: dict[str, str | int]` as an additional `HealthTuple` field in Round 2's first source edit — narrow amendment of `_types.py` plus updated canonical-bytes test vectors. Adds auditor-replayability per §4.10's stated A-v3-01 / RT-v2-HIGH-01 closure. Blueprint §2.3 table is the stale side.
   - **Option B:** Drop `run_entropy` from §4.10, sign without it. Cheaper but loses the audit-replay substrate that §4.10 justifies in-line.
   - **Decision:** Option A. Raise a `F-BLUEPRINT-DRIFT` one-line note in the Round 2 LOCK memory; do not edit `section_03_scout.md` from this seat (that requires a Thesis Team round). The amendment to `_types.py` is substrate-level and will be re-verified by Section 4 Logician's existing canonical-bytes assertions.
2. **`HealthTupleSchemaError` placement.** New in Round 2; lives inside `health_tuple.py` next to the function. Not hoisted to `_types.py` — errors are behavior, not schema. Carries `code` attribute + `sub_tag` where applicable (reuses the translator-dataclass pattern from E-019).
3. **`_fresh_urandom` helper.** Private module function per §4.10. One retry on short-read; raises `F-SCOUT-H-03.urandom_short_read` on the second failure. Test fixture monkey-patches `os.urandom` to return short bytes to exercise both paths.
4. **`run_tiebreak_seed` is an injected parameter, not module-generated.** Per §4.10 the seed is "captured at run_id time, carried here for audit" — the orchestrator (R11) generates the seed once at DISCOVER start and threads it through the signing call. Round 2 validates length only, does not generate.
5. **Injection via Protocol for Section 1 primitives.** Pattern E-017. Protocol `SessionSigner` exposes `sign_health_tuple(tuple_bytes: bytes) -> bytes` + `hmac_key_id: str` + `session_id: str` + `slug: str`. The production impl binds Section 1's `Session` + `sign_health_tuple`; tests inject fakes that return deterministic 64-byte signatures. Keeps Round 2 crypto-behavior testable without spinning up a real Session.
6. **Vault write is also injected.** Round P LOCKED `vault_write(path, bytes_, intent, session_id, slug)`. Round 2 calls it via a thin `VaultWriter` Protocol — real impl binds `pipeline.vault.vault_write.vault_write`; tests inject a memory writer that records `(path, bytes_, intent)` for assertion.
7. **`_utc_now_iso` helper.** Accept an injected `ClockFn = Callable[[], str]` default-bound to `datetime.datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")`. Lets tests pin `signed_at_utc` deterministically.
8. **`_run_log_health_path` composition.** Builds `orgs/{slug}/scout/run_log/{run_id}-health.json` under the org root using Section 1's `within_org_root(slug, ...)` for path safety. No raw `Path` concatenation.
9. **Fail-closed on verifier-side integrity.** `SignedHealthTuple.tuple_canonical` MUST be the exact byte string Section 1 signed. Round 2 tests include a negative: mutate `tuple_canonical` after signing and assert the Logician's existing verifier raises (integration test spans §3 → §4).
10. **No module-level side effects on import.** `pipeline.scout.health_tuple` import path is fresh-start safe; all state lives in the function.

## Public surface (locked by spec card)

```python
# pipeline/scout/health_tuple.py

from typing import Protocol

from pipeline.scout import (
    HealthTuple, SignedHealthTuple,
    HEALTH_OK, HEALTH_DEGRADED, HEALTH_FAILED,
    INTENT_SCOUT_RUN_LOG_WRITE,
    health_tuple_canonical_bytes,
)

class SessionSigner(Protocol):
    session_id: str
    slug: str
    hmac_key_id: str
    def sign_health_tuple(self, tuple_bytes: bytes) -> bytes: ...

class VaultWriter(Protocol):
    def write(self, *, path: str, bytes_: bytes, intent: str,
              session_id: str, slug: str) -> None: ...

ClockFn = Callable[[], str]
UrandomFn = Callable[[int], bytes]
MonotonicFn = Callable[[], int]

class HealthTupleSchemaError(RuntimeError):
    code: str         # "F-SCOUT-H-01" | "F-SCOUT-H-02" | "F-SCOUT-H-03" | "F-SCOUT-V-06"
    sub_tag: str | None

def assemble_and_sign_health_tuple(
    *,
    session: SessionSigner,
    per_channel: dict[str, str],
    per_channel_a_endpoints: dict[str, str],
    run_wall_ns: int,
    run_tiebreak_seed: bytes,
    vault_writer: VaultWriter,
    clock: ClockFn = _default_clock,
    urandom: UrandomFn = os.urandom,
    monotonic_ns: MonotonicFn = time.monotonic_ns,
) -> SignedHealthTuple: ...
```

`__all__` addition at `pipeline/scout/__init__.py`: `assemble_and_sign_health_tuple`, `HealthTupleSchemaError`, `SessionSigner`, `VaultWriter`. `__version__` bumps to `"0.1.0-scout-r2"`.

## Failure-code taxonomy

| Code | Raised when |
|------|-------------|
| `F-SCOUT-H-01` | `per_channel[ch]` missing or not ∈ {OK, DEGRADED, FAILED} for any ch ∈ A..F |
| `F-SCOUT-H-02` | `per_channel_a_endpoints[ep]` missing or not ∈ {OK, DEGRADED, FAILED} for any ep ∈ {grants.gov, sam.gov, usaspending.gov} |
| `F-SCOUT-H-03.urandom_short_read` | `os.urandom(n)` returned a short buffer twice in `_fresh_urandom` |
| `F-SCOUT-H-04` | Section 1 `sign_health_tuple` propagated an exception (Round 2 re-raises as `HealthTupleSchemaError(code=F-SCOUT-H-04)` with `__cause__`) |
| `F-SCOUT-V-06` | `run_tiebreak_seed` length ≠ 16 bytes |

## Test surface (target ~45 tests)

- `TestAssembleHappyPath` (4) — all-OK tuple; one-DEGRADED tuple; one-FAILED tuple (channel_e); backbone_failed=True when all three A endpoints FAILED.
- `TestChannelStateValidation` (6 parametrized) — missing channel, typo channel value, all 6 channels each in turn invalid.
- `TestChannelAEndpointValidation` (4 parametrized) — missing grants.gov, typo sam.gov, typo usaspending.gov, empty dict.
- `TestRunIdDerivation` (5) — run_id is 24 hex chars; changes with run_wall_ns; changes with session.session_id; changes with monotonic jitter; changes with urandom jitter.
- `TestUrandomShortRead` (3) — first short triggers retry; second short raises F-SCOUT-H-03.urandom_short_read; full length no-op.
- `TestRunTiebreakSeed` (4) — correct length accepts; wrong length raises F-SCOUT-V-06; zero-length raises; exact-16 passes.
- `TestCanonicalBytes` (3) — `signed.tuple_canonical` == `health_tuple_canonical_bytes(tuple_obj)`; determinism across two calls with pinned fakes; bit-identical re-canonicalization (sign→verify round-trip).
- `TestSignatureDelegation` (3) — `session.sign_health_tuple` is called with exactly `tuple_canonical`; returned `hmac_sha3_512` is the fake's output; `hmac_key_id` flows through.
- `TestVaultWriteCallSite` (3) — path is `orgs/{slug}/scout/run_log/{run_id}-health.json`; intent==INTENT_SCOUT_RUN_LOG_WRITE; session_id + slug match.
- `TestVerifierRoundTrip` (2) — integration: signed bytes deserialize; Section 4 `pipeline.logician` verifier (already landed Round 5/6) accepts the signature and REJECTS a mutated `tuple_canonical`.
- `TestSignatureFailurePropagation` (2) — when `session.sign_health_tuple` raises, surfaces as F-SCOUT-H-04 with `__cause__` preserved; `vault_writer.write` NOT called on signing failure.
- `TestASTLintRegression` (1) — `lint_tree(pipeline/scout/health_tuple.py, DEFAULT_RULES) == []`.
- `TestKWOnly` (1) — positional call rejected.
- `TestProtocolDiscipline` (2) — SessionSigner and VaultWriter are Protocols (not concrete classes); a minimal duck-typed fake works.
- `TestRunEntropyField` (2) — if Option A adopted: `run_entropy` present in canonical bytes; contains `run_urandom_hex`, `run_monotonic_ns`, `run_tiebreak_seed_hex`.

Total ≈ 45. Coverage target 100% on `health_tuple.py`.

## pyproject.toml / dep changes

None. Round 2 uses stdlib (`hashlib`, `os`, `time`, `datetime`, `typing`, `json` via canonical helper) + existing `pipeline.sovereignty` + `pipeline.vault` already installed.

## Committee dispatch

Per ARCH-04 precedent, Round 2 is substrate-layer crypto + I/O — eligible for single-cycle self-LOCK under §8b narrow-edit carve-out IF:
- All 45 tests green in one RED→GREEN cycle
- 100% coverage on `health_tuple.py`
- AST-lint clean against `pipeline/scout/`
- Integration test confirms Section 4 verifier round-trips

Otherwise dispatch 5-family Code Thesis Committee per `router.yaml`:
- Codex (OpenAI) — adversarial
- Qwen3-32B (Groq) — architecture
- Llama 3.3 70B (Groq) — invariant review
- GPT-OSS 120B (Groq) — scope-gate
- Kimi K2 (Groq) — edge-case

Cross-family rigor: no Anthropic-reviews-Anthropic. Primary Scribe is Anthropic; committee is all non-Anthropic per Law-adjacent discipline.

## Done-definition

1. `pipeline/scout/health_tuple.py` written per surface above.
2. `pipeline/scout/__init__.py` re-exports `assemble_and_sign_health_tuple`, `HealthTupleSchemaError`, `SessionSigner`, `VaultWriter`. `__version__ = "0.1.0-scout-r2"`.
3. `pipeline/scout/_types.py` amends `HealthTuple` to include `run_entropy: dict[str, str | int]` (Option A).
4. `tests/scout/test_round_2_health_tuple.py` — ≥45 tests across classes above.
5. Amend `tests/scout/test_round_1_types_constants.py::TestNumericPins` / `TestFieldCompleteness` to cover the new `run_entropy` field.
6. `scripts/run_tests.sh tests/scout/` green.
7. `scripts/run_tests.sh` full suite green (no regressions anywhere — particularly §4 Logician Round 5/6 which verifies signed health tuples).
8. `scripts/run_lint.sh` clean.
9. Coverage on `pipeline.scout.health_tuple` = 100%.
10. LOCK entry `project_impl_scout_round_2_locked.md` + MEMORY.md pointer.
11. Round 3 spec card pre-staged: `scout_round_3_channel_b_cache.md`.

## Dependencies and timing

- **Unblocks:** Scout R3..R11 (every channel module needs to report a per-channel health state that M7 will sign).
- **Blocked by:** Round 1 LOCK (done). No external blockers.
- **Risk surface:** blueprint drift on `run_entropy` (decision above); `sign_health_tuple` Section 1 signature stability (already LOCKED in Round C/E keys + session); `vault_write` Section 2 signature stability (already LOCKED in Round P).

## Pre-flight checklist

- [x] Blueprint hash computed and pinned.
- [x] Section 1 + Section 2 + Section 4 consumed surfaces confirmed LOCKED.
- [x] Round 1 `_types.py` fields cross-checked against §2.3.
- [x] §4.10 implementation cross-read against §2.3 schema — `run_entropy` drift flagged.
- [x] Test count estimate budgeted (45); coverage target set (100%).
- [x] AST-lint impact assessed — no R4/R5 surface in this round (no `setattr` on `operator_decision`, no `eval`).
- [ ] RED→GREEN cycle executed.
- [ ] Committee dispatch OR self-LOCK gate reached.
