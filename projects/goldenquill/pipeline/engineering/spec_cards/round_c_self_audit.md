# Round C — Spec-Card Self-Audit (Rule 2 Magic Step)

**STATUS:** LOCKED

**Author:** Claude Code CLI window (2026-04-19 late)
**Round:** C (crypto_primitives.py v2 extension + keys.py new)
**Status:** LOCKED 2026-04-19 via E3 operator synthesis. Committee-confirmed at `pipeline/validation/code_reviews/round_c_2026-04-19/final_synthesis.md`. Post-delta addition: `FileKeyStore.__enter__/__exit__/close()` context manager (D-22 structural closure) + 3 tests. Cumulative pytest final: 290/290 green.

Cumulative pytest: **287 / 287 green** on Python 3.14.4 + pytest 9.0.3. Round A 103 + Round B 96 + Round C 88 (39 crypto ext + 49 keys).

---

## Artifact 1 — `pipeline/sovereignty/crypto_primitives.py` v2 extension

### Spec card row-by-row (round_c_keys.md §"Public API — crypto_primitives extension")

| Row | Status | Evidence |
|---|---|---|
| `SecretBytes` context manager | ✓ | crypto_primitives.py L365-437; `__slots__`, init from bytes/bytearray/memoryview, zero idempotence, view-after-zero raises, `with` zeroes on exit + exception, `__len__`, `zeroed` property. Tested in `TestSecretBytesInit`, `TestSecretBytesZero`, `TestSecretBytesContextManager`. |
| `ZeroizedBufferAccessed` exception | ✓ | crypto_primitives.py L361-362 |
| `aesgcm_encrypt(key, nonce, plaintext, aad) -> bytes` | ✓ | crypto_primitives.py L440-490; 32-byte key, 12-byte nonce, E-001 type gates. |
| `aesgcm_decrypt(key, nonce, ciphertext, aad) -> bytearray` | ✓ | crypto_primitives.py L493-550; returns bytearray per §3.11 v3 contract; InvalidTag propagation. |
| `pbkdf2_sha3_512(passphrase, salt, iterations, dklen) -> bytearray` | ✓ | crypto_primitives.py L553-599; default 600_000 iterations + dklen 32 per §8. |
| `__all__` public export | ✓ | 5 new symbols added; Round-A 6 symbols unchanged. |
| Backward-compat — Round-A 103 tests unchanged | ✓ | pytest shows all 103 green post-extension. |
| §4.1 Public API | ✓ | __all__ extended |
| §4.2 Schema versioning | N/A — no new on-disk artifacts in this delta (SecretBytes is in-memory, AES-GCM is primitive layer) |
| §4.4 Crypto-agility | ✓ | module-level `_AESGCM_KEY_BYTES`, `_PBKDF2_HASH_NAME` constants; future ChaCha20-Poly1305 or ML-KEM add as parallel primitives without refactor |
| §4.6 BLUEPRINT_DEPS | ✓ | extended with §4.6 v2 + §5.4 BT4 entries |
| §4.10 type hints | ✓ | all 5 new public functions fully typed |
| §4.11 docstring anchors | ✓ | every new symbol cites [§4.6 v2] or [§5.4 BT4] |
| E-001 enforce-by-default | ✓ | SecretBytes rejects str/int; aesgcm_* checks key/nonce lengths before semantic op; pbkdf2 checks iterations/dklen ≥ 1 |
| E-002 case discipline | ✓ | `_ALGO_SHA3_512 = "sha3-512"` already lowercase; new `_PBKDF2_HASH_NAME = "sha3_512"` lowercase (hashlib-compatible) |

### LOC
Round-A LOCKed at 349 LOC. Round-C extension added 250 LOC (599 total). Spec card estimated +190. Actual overage (+60 LOC = 32% over delta estimate) driven by more extensive type-gate blocks and docstring anchors than initial estimate assumed. Within the spirit of E-005.

---

## Artifact 2 — `pipeline/sovereignty/keys.py` (NEW, 1000 LOC)

### Spec card row-by-row (round_c_keys.md §"Public API — keys.py")

| Row | Status | Evidence |
|---|---|---|
| 10 failure-code exceptions (F-KEY-01..10) | ✓ | keys.py L127-175; each exception one class, short docstring citing F-code. |
| Constants (KEYCHAIN_SERVICE_TEMPLATE, NONCE_REGISTRY_SIZE_LIMIT_BYTES, env var names, § 8 internals) | ✓ | keys.py L102-122 |
| `KeyStore` ABC with sealed retrieve | ✓ | keys.py L234-287; `__init_subclass__` rejects retrieve override (F-KEY-10); `@typing.final` retrieve wraps `_retrieve_raw` output as SecretBytes; isinstance check raises F-KEY-08 on non-bytearray. |
| `MacOSKeychainKeyStore` via security CLI | ✓ | keys.py L290-448; subprocess with argv arrays (no shell); service name from §8 template; store/retrieve/zero/rotate/exists; keychain-locked detection via stderr markers → F-KEY-02; CLI-missing → F-KEY-03. |
| `FileKeyStore` | ✓ | keys.py L781-959; PBKDF2 KEK derivation, passphrase env var zeroed + deleted, per-slug persistent salt, AES-GCM-sealed key envelopes, nonce registry integration, zero unlinks, rotate mints new suffix. |
| `YubiHSMKeyStore` stub | ✓ | keys.py L962-992; init raises NotImplementedError with message routing operator. |
| `resolve_keystore` factory | ✓ | keys.py L995-1000 (caller-facing); dispatches on TILTH_KEYSTORE_PROVIDER env; F-KEY-01 on unknown; F-KEY-03 on non-Darwin keychain; F-KEY-04 on file without passphrase; NEVER silent fallback. |
| Nonce registry primitives | ✓ | keys.py L451-781: per-slug segmented JSONL with rolling HMAC chain per §5.4 v3; pre-gen size-check rotation per §5.4 v4 RT-v3 MED-1; chain verify walks every segment with monotonic-seq check + prev-trailer-hash link; rotation failure raised before nonce gen. |
| Blueprint §7-style regression tests | ✓ | `test_subclass_overriding_retrieve_rejected` (§3.11 v4 RT-v3 HIGH-2); `test_non_bytearray_return_raises` (§3.11 v3 RT-v2 HIGH-3); `test_rotation_failure_is_detected` (§5.4 v4 RT-v3 MED-1). |
| `__all__` public exports | ✓ | 20 symbols: 10 exceptions + 4 stores + factory + 4 constants + ABC. |
| §4.1 Public API | ✓ | All consumers use `from pipeline.sovereignty import ...`. |
| §4.2 Schema versioning | ✓ | nonce-registry entries + trailers carry `schema_version: "v1"`. |
| §4.3 Regression corpus | ✓ | `tests/corpus/keys/v1/pbkdf2_vectors.json` with 3 deterministic vectors. |
| §4.4 Crypto-agility | ✓ | AES-GCM key/nonce sizes pinned via module constants; future variants additive. |
| §4.6 BLUEPRINT_DEPS | ✓ | keys.py L56-72 |
| §4.9 Regression discipline | ✓ | 88 new tests; corpus monotonic. |
| §4.10 Type hints | ✓ | Full on every public method and helper. |
| §4.11 Docstring anchors | ✓ | Every public class + method cites its § anchor. |
| E-001 enforce-by-default | ✓ | Every public method type-gates before semantic work. |
| E-002 case discipline | ✓ | Provider identifiers lowercase (`"keychain"`, `"file"`, `"yubihsm"`); case-normalized via `.lower().strip()` in factory. |
| E-005 sub-system-wise LOC | ✓ | spec card decomposition followed; actual 1000 LOC under estimated ~1120 (favourable variance). |
| E-006 OpenAI Tier-1 discipline | N/A for code — applies at committee dispatch time. |
| LOC target ~1120 ±25% (840-1400) | ✓ **actual 1000 LOC** — under estimate; defensible for the 4 sub-systems implemented. |

### Concurrency + corruption resistance
- All mutations on nonce registry under single held `fcntl.LOCK_EX` per §5.3 BT3 pattern (duplicated from audit.py per §4.1 no-cross-module-internal-import).
- `test_two_threads_append_serialize` exercises 6-thread race on FileKeyStore.store.
- Rollback-attack-style surface: blueprint §5.6 rollback defences are in audit.py (Round B). Nonce-registry rollback is detected via the rolling HMAC chain — `test_truncation_detected` + `test_trailer_tamper_detected` cover the signal.

### macOS-only tests
`MacOSKeychainKeyStore` tests are guarded by `@pytest.mark.skipif(not (_DARWIN and _SECURITY_CLI))`. On Josh's M1 Mac Mini the tests run (and passed locally). On a Linux CI runner they skip cleanly with a clear reason.

---

## Round-A + Round-B lesson pre-checks (E-001..E-006)

- **E-001** enforce by default — ✓ applied across every new public symbol; defensive-type-checks before semantic work.
- **E-002** case discipline — ✓ all identifier strings lowercase; `.lower().strip()` on provider env value.
- **E-003** strict NFC — N/A for Round C (no Unicode canonicalization surfaces).
- **E-004** committee fallback — ✓ Gemini at R5 upfront per Round-A+B pattern.
- **E-005** sub-system-wise LOC — ✓ spec card decomposed per sub-system; actual LOC under estimate.
- **E-006** OpenAI Tier-1 — ✓ dispatch script will use gpt-4o-mini at Codex slot.

---

## Drift notes pre-lock (anticipated)

- **D-15 (pending):** Round-A crypto_primitives.py LOCKed at v1 without SecretBytes + AES-GCM + PBKDF2. Round-C extends per blueprint row 2. Drift is cleanly forward-going (v1 → v2 LOCK cycle).
- **D-16 (pending):** FileKeyStore holds KEK as bytearray on instance (not SecretBytes). Rationale in spec card: KEK lifetime == instance lifetime (seconds to hours); explicit `zero_kek()` method at shutdown gives equivalent zero-on-exit guarantee. SecretBytes remains the default for ephemeral call-site HMAC keys.
- **D-17 (pending):** Nonce-registry HMAC key reuses the FileKeyStore KEK. Blueprint §5.4 BT4 cites `tilth.keys.{slug}.nonce_registry.hmac.v1` as the registry HMAC key id. v0.1 Round-C uses the KEK directly; future keystore key-derivation-tree (later round) may split this into a proper sub-key. Acceptable under v0.1 trusted-operator boundary — same keystore key-material root.
- **D-18 (pending):** rotation semantics in `MacOSKeychainKeyStore.rotate` and `FileKeyStore.rotate` mint `{key_id}.rot.{ts}` suffix and zero the old id. Blueprint §4.6 M7 describes a more sophisticated `.v1/.v2` suffix scheme with grace window — that lives in session.py (Round E). Round-C's rotate is the primitive; Round-E layers on the grace-window discipline.

None are LOCK blockers.

---

## Committee dispatch plan

- Codex R1: `gpt-4o-mini` per E-006 until operator's OpenAI Tier-2.
- Qwen R2: `qwen/qwen3-32b` via Groq, max_tokens 4000, temperature 0.1, with Round-B repetition-discipline preamble.
- Llama R3: `llama-3.3-70b-versatile` via Groq.
- GPT-OSS R4: `openai/gpt-oss-120b` via Groq.
- Gemini R5: `gemini-2.5-pro` via Google.

Estimated payload: ~60K tokens (slightly larger than Round-B's 48K because two files + keys.py is the biggest). Under Groq / Gemini limits; Codex-trimmed payload drops tests + Round-A surface to fit TPM.

---

End of self-audit — proceeding to dispatch.
