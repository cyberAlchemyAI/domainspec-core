# Spec card — Round C: `pipeline.sovereignty.keys` + `crypto_primitives` backfill

**STATUS:** LOCKED

**Blueprint anchor:** `pipeline/blueprint/v0.1/section_1_sovereignty_envelope.md` §3.11 KeyStore ABC (v4 sealed); §5.4 BT4 HSM-capable key storage; §4.6 M7 HMAC key lifecycle (v2 SecretBytes); §6.6 F-KEY-01..10; §8 constants (`FILE_KEYSTORE_PBKDF2_ITERATIONS=600_000`, `FILE_KEYSTORE_SALT_BYTES=16`, `FILE_KEYSTORE_AEAD_NONCE_BYTES=12`, `FILE_KEYSTORE_KEK_BYTES=32`, `KEYCHAIN_SERVICE_TEMPLATE`, `NONCE_REGISTRY_*`, `KEYSTORE_RETRIEVE_SEALED`, `KEYSTORE_CONTRACT_ENFORCEMENT`).
**Blueprint hash-at-card:** `<to-populate-at-LOCK>`
**Spec-card version:** v1
**Round:** C (2026-04-19)
**Futureproofing scope:** §4.1 public API / §4.2 schema versioning / §4.3 regression corpus / §4.4 crypto-agility / §4.6 BLUEPRINT_DEPS / §4.9 regression discipline / §4.10 type hints / §4.11 blueprint-citing docstrings / E-001 enforce-by-default / E-002 case-discipline / E-005 sub-system-wise LOC estimate / E-006 committee OpenAI-tier fallback.

## Scope — TWO artifacts LOCK together this round

Round-C batches a Round-A public-API extension + a new Round-C module because they are inseparable: `keys.py` depends on crypto primitives that Round A did not ship (blueprint row 2 lists them under `crypto_primitives.py`). Batching them per engineering-process §2 is warranted because (a) combined bytes ≈ 38 KiB (under 40 KiB cap), (b) no public-API boundary drift, (c) no CRIT-class failure mode.

### Artifact 1 — `pipeline/sovereignty/crypto_primitives.py` extension (LOCK cycle v2)

Round-A LOCKed this at v1 with `sha3_512_hex`, `sha3_512_with_nonce`, `verify_sha3_512_with_nonce`, `hmac_sha3_512`, `constant_time_equal`, `zero_bytes`. Round C adds:

  - `SecretBytes` context manager (blueprint row 2 + §4.6 v2 M7 key-lifecycle requirement)
  - `aesgcm_encrypt(key_bytes, nonce, plaintext, aad) -> bytes` (blueprint row 2 + §5.4 BT4 FileKeyStore envelope)
  - `aesgcm_decrypt(key_bytes, nonce, ciphertext, aad) -> bytearray` (blueprint row 2; returns bytearray per §3.11 contract so retrieve() wrap is clean)
  - `pbkdf2_sha3_512(passphrase, salt, iterations, dklen) -> bytearray` (blueprint row 2 + §5.4 BT4 KEK derivation)
  - `ZeroizedBufferAccessed` exception (blueprint §4.6 v2 `SecretBytes.view` raises after `zero()`)

All new symbols added to `pipeline/sovereignty/__all__`. Existing API unchanged (backward-compatible extension; Round-A 103 tests remain green).

### Artifact 2 — `pipeline/sovereignty/keys.py` (NEW)

Full KeyStore surface per blueprint §3.11 + §5.4 BT4 + §4.6 M7.

## Public API — crypto_primitives extension

```python
class SecretBytes:
    """Mutable secret buffer. Zeros in-place on __exit__ or explicit zero(). [§4.6 v2]"""
    def __init__(self, data: bytes | bytearray | memoryview) -> None: ...
    def view(self) -> memoryview: ...                    # raises ZeroizedBufferAccessed after zero()
    def zero(self) -> None: ...                           # idempotent
    def __enter__(self) -> "SecretBytes": ...
    def __exit__(self, *_) -> None: ...                   # calls zero()
    def __len__(self) -> int: ...
    @property
    def zeroed(self) -> bool: ...                        # for tests + defensive callers


class ZeroizedBufferAccessed(RuntimeError):
    """Raised by SecretBytes.view() after the buffer has been zeroed. [§4.6 v2]"""


def aesgcm_encrypt(
    key: bytes | bytearray | memoryview,
    nonce: bytes,
    plaintext: bytes,
    aad: bytes = b"",
) -> bytes:
    """AES-256-GCM encrypt. Key 32 bytes, nonce 12 bytes. [§5.4 BT4]"""


def aesgcm_decrypt(
    key: bytes | bytearray | memoryview,
    nonce: bytes,
    ciphertext: bytes,
    aad: bytes = b"",
) -> bytearray:
    """AES-256-GCM decrypt. Returns bytearray (mutable, §3.11 contract). [§5.4 BT4]"""


def pbkdf2_sha3_512(
    passphrase: bytes | bytearray | memoryview,
    salt: bytes,
    iterations: int = 600_000,
    dklen: int = 32,
) -> bytearray:
    """PBKDF2-HMAC-SHA3-512 → bytearray KEK. [§5.4 BT4, §8 FILE_KEYSTORE_PBKDF2_ITERATIONS]"""
```

Dependency: `cryptography` library (for AES-GCM) — Round C adds to `pyproject.toml`. No other new deps.

## Public API — keys.py

```python
# Failure codes (§6.6)
class KeyStoreConfigError(RuntimeError): ...               # F-KEY-01
class KeychainLockedError(RuntimeError): ...               # F-KEY-02
class KeyStoreUnavailable(RuntimeError): ...               # F-KEY-03
class FileKeyStoreUnavailable(KeyStoreUnavailable): ...    # F-KEY-04
class KeyCorrupt(RuntimeError): ...                         # F-KEY-05
class NonceReused(RuntimeError): ...                        # F-KEY-07
class KeyStoreContractViolation(TypeError): ...             # F-KEY-08 + F-KEY-10
class NonceRegistryOverSizeLimit(RuntimeError): ...         # F-KEY-09 variant
class NonceRegistryTrailerMismatch(RuntimeError): ...       # F-KEY-09 variant
class NonceRegistryRotationFailed(RuntimeError): ...        # F-KEY-09 variant
class NonceRegistryTruncated(RuntimeError): ...             # F-KEY-09 variant


class KeyStore(abc.ABC):
    """[§3.11 v4 — retrieve() is SEALED via @typing.final + __init_subclass__]"""
    def __init_subclass__(cls, **kwargs) -> None: ...       # F-KEY-10 raised at class-def
    @typing.final
    def retrieve(self, key_id: str) -> SecretBytes: ...     # SEALED; wraps _retrieve_raw
    @abc.abstractmethod
    def _retrieve_raw(self, key_id: str) -> bytearray: ...  # subclasses override
    @abc.abstractmethod
    def store(self, *, key_id: str, key_bytes: bytes | bytearray, purpose: str) -> None: ...
    @abc.abstractmethod
    def rotate(self, key_id: str) -> str: ...               # returns new key_id
    @abc.abstractmethod
    def zero(self, key_id: str) -> None: ...
    @abc.abstractmethod
    def exists(self, key_id: str) -> bool: ...
    @abc.abstractmethod
    def provider(self) -> str: ...                          # "keychain" | "file" | "yubihsm"


class MacOSKeychainKeyStore(KeyStore):
    """macOS `security` CLI subprocess wrapper. [§3.11 + §5.4 BT4]

    Service name: com.goldenquill.tilth.{slug} per §8 KEYCHAIN_SERVICE_TEMPLATE.
    Account name: {purpose}.{key_id}.
    Returns raw bytes via CLI `-w` hex output; _retrieve_raw decodes to bytearray.
    """


class FileKeyStore(KeyStore):
    """PBKDF2-SHA3-512 → AES-256-GCM on-disk envelope. [§5.4 BT4 v2+v3]

    Path: sovereignty/keys/{slug}/{key_id}.aead.
    Passphrase: read from TILTH_FILE_KEYSTORE_PASSPHRASE env var at __init__,
    PBKDF2'd into 32-byte KEK, original passphrase zero_bytes'd, env var deleted.
    Nonce registry per §5.4 v3 rolling HMAC chain.
    """


class YubiHSMKeyStore(KeyStore):
    """v0.1 stub — raises NotImplementedError. [§5.4 BT4 Phase-2 deferred]"""


def resolve_keystore(env_var: str = "TILTH_KEYSTORE_PROVIDER") -> KeyStore:
    """Factory. [§5.4 BT4 + §6.6 F-KEY-01/F-KEY-03]

    "keychain" → MacOSKeychainKeyStore (macOS default).
    "file"     → FileKeyStore.
    "yubihsm"  → YubiHSMKeyStore (stub).
    Unknown    → KeyStoreConfigError (F-KEY-01).
    Missing on macOS when keychain path fails → KeyStoreUnavailable (F-KEY-03) — NEVER silent fallback to FileKeyStore.
    """
```

Plus internal nonce-registry helpers (`_nonce_registry_append`, `_rotate_nonce_registry`, `_verify_nonce_registry_chain`, `_compute_nonce_registry_hmac_trailer`).

## Sub-system LOC estimate (per E-005 discipline)

### crypto_primitives.py extension (added to existing 349 LOC)
| Sub-system | LOC | Rationale |
|---|---|---|
| SecretBytes class | 70 | `__slots__`, init on bytes/bytearray/memoryview, view/zero/enter/exit/len, ZeroizedBufferAccessed |
| aesgcm_encrypt/decrypt | 50 | thin `cryptography.hazmat.primitives.ciphers.aead.AESGCM` wrapper + type gates |
| pbkdf2_sha3_512 | 30 | `hashlib.pbkdf2_hmac` wrapper + type gates + dklen default 32 |
| Constants + doc block | 10 | module-level AES-GCM length constants, new algorithm identifiers |
| Type-gate overhead (20%) | 30 | E-001 enforce-by-default across new public surface |
| **crypto_primitives delta** | **~190 LOC** | new total: ~540 LOC |

### keys.py (NEW)
| Sub-system | LOC | Rationale |
|---|---|---|
| Failure-code exceptions (10 classes) | 90 | F-KEY-01..10 each ~8 LOC for docstring + constructor |
| Constants (KEYCHAIN_SERVICE_TEMPLATE, NONCE_REGISTRY_*, paths) | 30 | §8 pinned values |
| KeyStore ABC + sealed retrieve + __init_subclass__ | 130 | v4 contract sealing, abstract methods, docstrings |
| MacOSKeychainKeyStore | 170 | subprocess wrapper, _retrieve_raw hex decode, store via `security add-generic-password -U`, rotate, zero, exists, provider |
| FileKeyStore | 220 | __init__ passphrase hygiene (PBKDF2 → KEK → zero passphrase → del env var), _retrieve_raw AES-GCM decrypt + nonce registry integration, store, rotate, zero, exists, provider |
| Nonce registry (segmented with rolling HMAC chain) | 200 | _nonce_registry_append + pre-gen size check + _rotate_nonce_registry + _verify_nonce_registry_chain + HMAC trailer computation under single fcntl.LOCK_EX |
| YubiHSMKeyStore stub | 30 | each method raises NotImplementedError with routing message |
| resolve_keystore factory | 60 | env var read, dispatch, fail-closed on unknown / unavailable, no silent fallback |
| Type-gate overhead (20%) | 190 | E-001 applied across every public method |
| **keys.py target** | **~1120 LOC** | ±25% = 840-1400 acceptable |

### Round C combined LOC budget
- crypto_primitives.py: 349 → ~540 (delta +190)
- keys.py: ~1120 (new)
- **Round-C authored-code total: ~1310 LOC** ±25% = 983-1638 acceptable per E-005.

## Data structures

No frozen dataclasses in this round (KeyStore subclasses hold backing state; keys are passed by value into SecretBytes). Nonce-registry entries serialize as canonical JSON lines:

```json
{"key_id": "tilth.session.abc.hmac.v1", "nonce_hex": "...", "ts_utc": "2026-04-19T20:00:00Z", "seq_id": 4237, "prev_hash": "..."}
```

Nonce registry trailer:
```json
{"schema_version": "v1", "segment_seq": 3, "last_nonce_seq_id": 4237, "segment_hmac": "...", "prev_segment_trailer_hash": "...", "trailer_hmac": "..."}
```

Both authored as dicts inside functions — no new public dataclasses required.

## Algorithms

### SecretBytes zero-on-exit
Per blueprint §4.6 v2. Holds a `bytearray` backing store; `view()` returns `memoryview` (caller passes that into `hmac_sha3_512(key.view(), data)` for the mutable-buffer path to HMAC). Zeroing overwrites every byte to 0 and flips `_zeroed = True`. Subsequent `view()` raises `ZeroizedBufferAccessed`. Idempotent: second `zero()` is no-op.

### aesgcm_encrypt / aesgcm_decrypt
Per blueprint §5.4 BT4. 32-byte key, 12-byte nonce. `_encrypt` returns `bytes` (ciphertext + 16-byte tag). `_decrypt` returns `bytearray` (mutable for §3.11 contract — callers can zero on exit). Raises `cryptography.exceptions.InvalidTag` on MAC failure; caller catches + maps to `KeyCorrupt` (F-KEY-05).

### pbkdf2_sha3_512
`hashlib.pbkdf2_hmac("sha3_512", passphrase_bytes, salt, iterations, dklen)`. Returns `bytearray` (mutable for zeroization). Default `iterations=600_000` matches §8 + OWASP 2024 (PBKDF2-SHA3-512).

### KeyStore.__init_subclass__ sealing
Inspects `cls.__dict__` (class-local namespace, not inherited). If `"retrieve" in cls.__dict__`, raises `KeyStoreContractViolation` with F-KEY-10 message. Runs inside `type.__init__` before any instance can be constructed. Matches blueprint §3.11 v4 verbatim.

### MacOSKeychainKeyStore subprocess protocol
- Service name: `com.goldenquill.tilth.{slug}` per §8. Requires slug to be `canonical_slug()`'d — type gate calls `canonical_slug(slug)` and raises ValueError on non-canonical input (defensive, matches Round-B topology.py pattern).
- `store`: `security add-generic-password -s <service> -a <account> -w <hex> -U`. Key bytes hex-encoded for CLI argv (safe; argv doesn't appear in process listing if pattern is `-w HEX`, but operator tooling like `ps` may see; documented limitation, trusted-operator boundary).
- `_retrieve_raw`: `security find-generic-password -s <service> -a <account> -w`. Reads stdout bytes, strips, hex-decodes into bytearray. Explicit `encoding="ascii"` decode to avoid silent utf-8 misinterpretation.
- `zero`: `security delete-generic-password -s <service> -a <account>`.
- `exists`: `security find-generic-password -s <service> -a <account>` returns 0 exit code iff present.
- `rotate`: stores under new suffixed `key_id`, zeroes old. Returns new `key_id`.
- Keychain-locked state → `KeychainLockedError` (F-KEY-02). Headless callers hard-abort.

### FileKeyStore passphrase hygiene + nonce registry
Per §5.4 BT4 v2+v3+v4:
1. `__init__` reads `TILTH_FILE_KEYSTORE_PASSPHRASE` into `bytearray`.
2. Random 16-byte salt (per-instance or loaded from first key file — blueprint doesn't pin; spec picks per-instance random salt stored alongside ciphertext).
3. `pbkdf2_sha3_512(passphrase, salt, 600_000, 32)` → KEK bytearray.
4. `zero_bytes(passphrase_buffer)`.
5. `del os.environ["TILTH_FILE_KEYSTORE_PASSPHRASE"]`.
6. KEK held on instance as bytearray (NOT SecretBytes on instance — zeros at `close()` via explicit `zero_kek()` method; SecretBytes is for call-site ephemeral use).

Nonce registry per §5.4 BT4 v2/v3:
1. On every `_encrypt(key_id, plaintext)`:
   - Acquire fcntl.LOCK_EX on `.nonce_registry.lock` (audit.py's `_acquire_exclusive_lock` pattern — reuse or duplicate; spec picks duplicate with local name per §4.1 no-cross-module-internal-import rule).
   - Compute current segment path. `os.stat(segment).st_size` check BEFORE `os.urandom(12)` (v4 pre-gen ordering).
   - If size ≥ `NONCE_REGISTRY_SIZE_LIMIT_BYTES` (10 MiB per §8): `_rotate_nonce_registry()` under same lock; seal trailer, open next segment. Rotation failure → `NonceRegistryRotationFailed`.
   - Generate `nonce = os.urandom(12)`. Append `{key_id, nonce_hex, ts, seq_id, prev_hash}` to segment; recompute segment HMAC trailer.
   - Rolling chain: trailer includes `prev_segment_trailer_hash` linking to prior segment's HMAC. Segment 0's prev is `0x00`.
2. `_verify_nonce_registry_chain` at boot: walk every segment in order, verify HMAC trailers chain correctly. Mismatch → `NonceRegistryTrailerMismatch` (F-KEY-09).

### resolve_keystore factory
Reads `TILTH_KEYSTORE_PROVIDER`. Dispatch:
- `"keychain"` → instantiate `MacOSKeychainKeyStore`. If `platform.system() != "Darwin"` → `KeyStoreUnavailable`. If instantiation fails (security CLI missing / permission) → `KeyStoreUnavailable`, NOT silent fallback.
- `"file"` → `FileKeyStore`. Missing env passphrase → `FileKeyStoreUnavailable` (F-KEY-04).
- `"yubihsm"` → `YubiHSMKeyStore` stub.
- Any other / missing → `KeyStoreConfigError` (F-KEY-01). Default on macOS IS `"keychain"` — applied only if env var is completely absent (caller then decides).

## Failure codes (§6.6 map)

| Exception | F-code | Fire path |
|---|---|---|
| `KeyStoreConfigError` | F-KEY-01 | `resolve_keystore` on unknown provider |
| `KeychainLockedError` | F-KEY-02 | `MacOSKeychainKeyStore._retrieve_raw` subprocess returns "keychain locked" error |
| `KeyStoreUnavailable` | F-KEY-03 | `resolve_keystore` when selected provider cannot initialize |
| `FileKeyStoreUnavailable` | F-KEY-04 | `FileKeyStore.__init__` missing passphrase env var |
| `KeyCorrupt` | F-KEY-05 | `FileKeyStore._retrieve_raw` AES-GCM InvalidTag |
| `zero_bytes(bytes)` TypeError | F-KEY-06 | Already covered in Round A `zero_bytes` (defensive) |
| `NonceReused` | F-KEY-07 | `_nonce_registry_append` finds prior `nonce_hex` for same key_id |
| `KeyStoreContractViolation` (instance) | F-KEY-08 | `retrieve()` wrapper sees non-bytearray from `_retrieve_raw` |
| `NonceRegistry*` (4 variants) | F-KEY-09 | nonce registry size / trailer / rotation failures |
| `KeyStoreContractViolation` (class-def) | F-KEY-10 | `__init_subclass__` sees `retrieve` in `cls.__dict__` |

## Test surface

Target ≥ 60 tests across both files.

### crypto_primitives extension tests (≥18)
- `TestSecretBytes`: init from bytes/bytearray/memoryview (3); zero idempotence (1); ZeroizedBufferAccessed after zero (1); context-manager zeros-on-exit including on exception (2); len/zeroed property (2); view returns memoryview (1).
- `TestAESGCM`: round-trip encrypt/decrypt (1); wrong key → InvalidTag → caller-mapped exception (1); wrong nonce → InvalidTag (1); AAD mismatch → InvalidTag (1); key-not-32-bytes TypeError (1); nonce-not-12-bytes TypeError (1).
- `TestPBKDF2`: deterministic for same (passphrase, salt, iter, dklen) (1); different salt → different output (1); type gates (1); iteration < 1 rejected (1); dklen > 0 enforced (1).

### keys.py tests (≥42)
- `TestKeyStoreABC`: sealing via __init_subclass__ rejects retrieve override (2: direct + inherited); retrieve wraps _retrieve_raw output in SecretBytes (1); retrieve raises KeyStoreContractViolation if _retrieve_raw returns non-bytearray (1: bytes, str, int, list).
- `TestResolveKeystore`: unknown provider → F-KEY-01 (1); missing env var on macOS defaults to keychain (1); file provider without passphrase → F-KEY-04 (1); no silent fallback (1); yubihsm stub (1).
- `TestYubiHSMStub`: every abstract method raises NotImplementedError (5).
- `TestMacOSKeychainKeyStore`: (conditional on `platform.system() == "Darwin"` + `security` CLI available via `shutil.which`) store/retrieve round-trip (1); retrieve returns SecretBytes zero-on-exit (1); zero deletes keychain item (1); rotate produces new key_id (1); exists true/false (2); _retrieve_raw returns bytearray (1); keychain-locked → F-KEY-02 (mock'd subprocess) (1).
- `TestFileKeyStore`: (no macOS dependency) __init__ zeros passphrase env var (1); store/retrieve round-trip (1); KEK-wrong → F-KEY-05 (1: tampered ciphertext); retrieve returns SecretBytes (1); zero unlinks file (1); rotate produces new key_id (1); missing TILTH_FILE_KEYSTORE_PASSPHRASE → F-KEY-04 (1).
- `TestNonceRegistry`: append under fcntl.LOCK_EX (1); NonceReused on duplicate (F-KEY-07) (1); size-limit triggers rotation pre-gen (1); NonceRegistryRotationFailed on disk-full mock (1); trailer chain verify (1); NonceRegistryTrailerMismatch on segment-tamper (1); NonceRegistryTruncated on segment-delete (1).
- `TestConcurrency`: two threads racing `_encrypt` serialize via fcntl (1).
- `TestCorpus`: `tests/corpus/keys/v1/` seeded with (salt, iterations, passphrase, KEK) tuples for cross-implementation determinism (≥3 vectors).

### Blueprint regression tests (MUST pass)
- `test_macos_keychain_keystore_wraps_before_return` (§5.4 BT4 contract; macOS-only).
- `test_file_keystore_decrypt_wraps_before_return` (§5.4 BT4 contract).
- `test_keystore_subclass_override_retrieve_rejected` (§3.11 v4 RT-v3 HIGH-2 closure).
- `test_keystore_non_bytearray_return_rejected` (§3.11 v3 RT-v2 HIGH-3 closure).
- `test_nonce_registry_rotation_pre_gen_ordering` (§5.4 BT4 v4 RT-v3 MED-1 closure).

## Dependencies

- `pipeline.sovereignty.crypto_primitives` — Round A + this-round extension; keys.py uses `hmac_sha3_512`, `sha3_512_hex`, `constant_time_equal`, `zero_bytes`, `SecretBytes` (new), `aesgcm_encrypt` (new), `aesgcm_decrypt` (new), `pbkdf2_sha3_512` (new).
- `pipeline.sovereignty.org_slug` — `canonical_slug` for service-name defensive check.
- `cryptography` library — new pyproject.toml dependency for AES-GCM. Latest stable; pin to `>=42.0`.
- `hashlib`, `hmac`, `secrets`, `os`, `subprocess`, `platform`, `shutil`, `json`, `fcntl`, `pathlib`, `abc`, `typing` — stdlib.

## Futureproofing commitments

- §4.1 Public API: `__all__` extended in both modules.
- §4.2 Schema versioning: nonce registry entries + trailer carry `schema_version: "v1"`.
- §4.3 Regression corpus: `tests/corpus/keys/v1/` deterministic (passphrase, salt, KEK) tuples.
- §4.4 Crypto-agility: AES-GCM nonce/key sizes pinned via module constants; future ChaCha20-Poly1305 or ML-KEM wrap is an additive call, not a refactor.
- §4.6 BLUEPRINT_DEPS: populated in both files.
- §4.9 Regression discipline: every test stays; corpus monotonic.
- §4.10 Type hints: full on every public symbol.
- §4.11 Docstring anchors: every public class / method cites its blueprint §.
- E-001 enforce by default: every public method type-gates before semantic work.
- E-002 case discipline: provider identifier constants (`"keychain"` / `"file"` / `"yubihsm"`) lowercase; algorithm strings (`"aes-256-gcm"`, `"pbkdf2-sha3-512"`) lowercase.
- E-005 sub-system-wise LOC estimate: decomposition table above.
- E-006 OpenAI Tier-1 fallback: committee dispatch at LOCK uses `gpt-4o-mini` at Codex slot unless operator confirms Tier-2.

## Done definition

- ≥ 60 pytest tests passing (cumulative 259+ when combined with Rounds A+B).
- `pytest tests/` green on macOS (Keychain tests active) AND Linux runner (Keychain tests skipped via `@pytest.mark.skipif`).
- LOC target ~1310 ±25% (983-1638). Per E-005: defensible breakdown documented inline.
- `pyproject.toml` adds `cryptography>=42.0`.
- `pipeline/sovereignty/__init__.py` `__all__` extended; old imports unchanged.
- Blueprint §7.3 / §7.5 regression tests remain green (Round A + B unaffected by extension).
- crypto_primitives.py Round-A committee-LOCKed signatures + semantics unchanged (backward-compatible extension only).

## Out of scope (Round C)

- `session.py` (§4.6 M7 key lifecycle consumer — Round E target).
- `admin_risk.py` / `degradation_log.py` (§5.3 / §5.6 caller of audit.py + keys.py — Round F target).
- `boot.py` / `interrupted_state.py` (§9 boot sequence orchestrator — Round G).
- HSM integration (Phase 2 per §5.4 roadmap).
- `safe_open_lock_file` full helper (Round E / F per §3.11c; audit.py Round B had a local subset; keys.py nonce_registry lock reuses audit.py's _acquire_exclusive_lock pattern as a DUPLICATED local helper per §4.1 no-cross-section-internal-import rule).

## Drift notes pre-lock (anticipated)

- **D-15 (pending):** Round-A `crypto_primitives.py` LOCKed at v1 without SecretBytes + AES-GCM + PBKDF2 primitives that blueprint row 2 assigns to it. Round-C extends crypto_primitives.py to its blueprint-specified scope; LOCK cycle v2.
- **D-16 (pending):** `FileKeyStore` initializes KEK on instance as bytearray, not SecretBytes. Rationale: KEK lifetime == FileKeyStore instance lifetime (seconds to hours); explicit `zero_kek()` method on `close()` gives equivalent guarantee without SecretBytes context-manager overhead for the long-lived path. SecretBytes remains the default for call-site ephemeral HMAC keys.

## Committee dispatch plan

- Codex (R1): `gpt-4o-mini` per E-006 until operator's OpenAI Tier-2.
- Qwen (R2): `qwen/qwen3-32b` via Groq, temperature 0.1, max_tokens 4000 per Round-B E-006 discipline.
- Llama (R3): `llama-3.3-70b-versatile` via Groq.
- GPT-OSS (R4): `openai/gpt-oss-120b` via Groq.
- Gemini R5: `gemini-2.5-pro` via Google (Kimi fallback per E-004).

Estimated payload size: ~55K tokens given two-file + test + corpus + spec card. Within Qwen/Llama/GPT-OSS/Gemini limits. Codex on gpt-4o-mini Tier-1 has ~200K TPM.

## E1 operator review checklist (before implementation begins)

- [ ] Confirm `cryptography>=42.0` as new pyproject.toml dep is acceptable (adds ~4MB of wheels but is the stdlib AES-GCM path in Python).
- [ ] Confirm SecretBytes + aesgcm_* + pbkdf2_* go into `crypto_primitives.py` (blueprint row 2 alignment), NOT `keys.py`.
- [ ] Confirm `MacOSKeychainKeyStore` uses `security` CLI via subprocess (blueprint §3.11 pick) vs. `keyring` PyPI library.
- [ ] Confirm batching both crypto_primitives extension + keys.py into one Round-C cycle is acceptable.
- [ ] Confirm LOC target ~1310 ±25% is acceptable per E-005 decomposition.

End of spec card — awaiting operator E1 approval to begin implementation.
