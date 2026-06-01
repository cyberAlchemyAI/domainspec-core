# Blueprint Section 1 — Sovereignty Envelope (v5, 2026-04-16)

**Status:** DRAFT v5 — fifth Thesis Team round. Addresses Red Team v4 in-scope findings (1 HIGH + 1 MEDIUM accepted; 3 findings rejected as out-of-model with explicit threat-model citation). Editor and Judge returned LOCK on v4 (READY_TO_LOCK, PASS 100/100); Red Team v4 returned REQUIRES_MAJOR_MITIGATIONS. See `17_synthesis_v4.md` for the v4 → v5 change map, `13_synthesis_v3.md` for the v3 → v4 map, `09_synthesis_v2.md` for the v2 → v3 map, and `05_synthesis_v1.md` for the v1 → v2 map. Operator (Josh Inklovich) confirmed v5 scope 2026-04-16: same-uid hostile code and same-uid concurrent writer are explicitly out-of-scope ("we aren't claiming to be resistant to intentional user-inserted issues").

**v5 deltas in one breath (full detail inline below):**
- **Sovereignty init marker** (RT-v4 HIGH-1 first-boot reset closure): New files `sovereignty/init.marker` + `sovereignty/init.marker.hmac`, signed with new keystore key `tilth.sovereignty.init.hmac.v1`. Written on the genuinely-first boot of a Tilth instance, under `ledger_watermarks.lock` (same lock used for watermark updates; single held lock across marker-write → HMAC-recompute → rename). Once the marker exists and verifies, the "legitimate first-boot" path (both watermark + HMAC absent AND all ledgers empty) in §9 step 7c.0 is no longer reachable. An attacker with file-write capability who deletes the watermark files AND truncates all ledgers to zero lines now faces a failing init-marker verification (marker present but unverifiable → `F-ADM-12 SovereigntyInitMarkerMismatch`; marker absent after successful first boot → `F-ADM-11 SovereigntyInitMarkerMissing`). First-boot reset attack closed. (`boot.py` ~170→~230, `audit.py` ~400→~430)
- **O_NOFOLLOW on all lock-file opens** (RT-v4 MED-1 symlink-swap closure): Every `open()` of `ledger_watermarks.lock`, `boot_clock_history.lock`, `nonce_registry.lock`, `init.marker.lock`, and every per-ledger segment `.lock` now passes `os.O_NOFOLLOW` in the open flags. Post-open `os.fstat(fd).st_ino` is compared against a parent-directory `os.stat()` readdir entry to confirm the inode was created by Tilth, not a symlink planted by an attacker. Symlink attack via lock-file swap is rejected at the syscall level. New failure mode `F-ISO-07 LockFileSymlinkAttack`.
- **Out-of-model rejection language in §10 F9**: Three Red Team v4 findings (RT-v4 HIGH-2 metaclass/monkey-patch bypass of `__init_subclass__`; RT-v4 HIGH-advisory-lock same-uid concurrent writer on `fcntl.LOCK_EX`; RT-v4 LOW-1 signal-handler lock-contention DoS) are rejected with explicit trust-model citation — all three require same-uid code running inside the Tilth process (arbitrary Python import, monkey-patch, or concurrent `fcntl` lock holder), which the trusted-operator threat model places out-of-scope (see §10 F9, bullets 1–3).

**v4 deltas in one breath (preserved — all v4 structures retained):**
- **Watermark integrity** (RT-v3 HIGH-1): `watermarks/ledger_watermarks.json` is now paired with `watermarks/ledger_watermarks.hmac` — rolling SHA-3-512 HMAC over canonical JSON of the watermark body, signed with keystore key `tilth.watermarks.hmac.v1`. Boot verifies the HMAC BEFORE trusting any watermark body. An actor with file-write access but no keystore access cannot roll back ledger+watermark together. New failure mode `F-ADM-10`. (`audit.py` ~360→~400)
- **KeyStore.retrieve() sealed** (RT-v3 HIGH-2): `KeyStore.retrieve()` is now `@typing.final`. `KeyStore.__init_subclass__` scans `cls.__dict__` for `retrieve` at class-definition time and raises `KeyStoreContractViolation` (F-KEY-10) if a subclass tries to override it. Concrete subclasses may ONLY override `_retrieve_raw()`. Both `FileKeyStore` and `MacOSKeychainKeyStore` comply. (`keys.py` ~600→~640)
- **Boot-clock-history atomic append** (RT-v3 MED-2): Append + fsync + HMAC recompute + trailer write + second fsync all occur inside a single held `fcntl.LOCK_EX`. The lock is never released between data-write and HMAC-commit. Documented as §2.8 invariant and tested in §7.14.
- **Nonce registry rotation pre-check** (RT-v3 MED-1): Size check now runs BEFORE nonce generation; if `current_size >= NONCE_REGISTRY_SIZE_LIMIT_BYTES`, rotation is triggered atomically (tmp→rename under the same lock) before the new nonce is written. Rotation failure raises `NonceRegistryRotationFailed`.
- **Signal handler non-blocking checkpoint lock** (RT-v3 LOW-1): `_checkpoint_lock.acquire(blocking=False)` in the unified handler. On contention, skip checkpoint and proceed directly to key zeroization + `os._exit`. Handler always terminates.
- **New failure codes:** `F-ADM-10` watermark HMAC mismatch or missing, `F-KEY-10` KeyStore subclass override of `retrieve()` detected (raised at class-definition time).

**Rejected Red Team v4 contests (trust-model-anchored rejections, documented in §10 F9):**
- RT-v4 HIGH-2 KeyStore metaclass strip + runtime monkey-patch — requires executing arbitrary Python inside the Tilth process (`StripRetrieveMeta` class definition loaded via `import`; `KeyStore.retrieve = lambda …` after class body). Both paths assume same-uid code injection, which the trusted-operator threat model places out-of-scope. `@typing.final` + `__init_subclass__` remain the in-model contract seal.
- RT-v4 HIGH-advisory-lock `fcntl.LOCK_EX` is advisory — bypass requires a same-uid process that deliberately opens the lock target without calling `fcntl.flock` / `fcntl.lockf`. Same-uid concurrent writer is out-of-scope. Offline tampering by a different-uid actor (or a no-UID attacker with file-write via filesystem misconfiguration) is caught by the HMAC trailer on next boot, which is in-model and closed.
- RT-v4 LOW-1 signal-handler lock-contention DoS — upper-bounded at 30 s (checkpoint write deadline); also requires same-uid process holding `_checkpoint_lock` adversarially. Out-of-scope and bounded.
- RT-v3 LOW-2 ledger-segment splice (out-of-model — segment HMAC trailer is signed with stable keystore key `tilth.ledger.{name}.hmac.v1`; attacker without the key cannot forge any new segment; documented in §5.6). Preserved from v4.

**v3 deltas in one breath (preserved — all v3 structures retained, now hardened):**
- **KeyStore contract** (HIGH-3): `KeyStore.retrieve` ABC signature now returns `SecretBytes` (NOT raw `bytes`). Runtime `isinstance` assert at every call site. `FileKeyStore` wraps decrypted key in `SecretBytes` before return; `MacOSKeychainKeyStore` wraps the `security` CLI output bytes in `SecretBytes` via `bytearray(stdout)`. No caller can hold an immutable `bytes` key. (`keys.py` ~520→~600)
- **Ledger freshness watermark** (HIGH-1): Per-ledger HMAC trailer now includes `last_seq_id` (highest `seq_id` in chain). `sovereignty/ledger_watermarks.json` stores the persistent boot-time baseline `(last_seq_id, last_trailer_hash)` per ledger. Boot verifier rejects if `current.last_seq_id < watermark.last_seq_id` — closes the ledger+trailer-pair-rollback attack. (`audit.py` ~310→~360)
- **Boot clock history** (HIGH-2): Append-only `sovereignty/ledgers/boot_clock_history.jsonl` records `(boot_epoch_ns, wall_at_boot_ns)` at every boot (boot_epoch via `sysctl kern.boottime` on macOS, `/proc/stat btime` on Linux). M13 `bypass_is_active` reads the history: if wall-clock is non-monotonic across boot entries, or if `now_wall < max(wall_at_boot) - CLOCK_ROLLBACK_TOLERANCE_SECONDS`, reject as clock rollback and require fresh re-authorization. Closes the wall-clock-rollback + process-restart attack.
- **Day counter source-of-truth** (MEDIUM-3): `admin_risk.counts.{date}.json` demoted to read-through CACHE. Source of truth is the ledger. On read, if counter file is missing or ledger's last `seq_id` > `counter.last_observed_seq_id`, rebuild counter from ledger. Crash-mid-write cannot drift the count. (`admin_risk.py` ~340→~370)
- **Nonce registry size limit + rotation + tamper-evidence** (MEDIUM-1, LOW-1): Per-slug nonce registry has a 10 MiB soft cap; at rotation a new `.nonce_registry.{seq}.jsonl` is opened and the closed segment is pinned. Each segment carries a rolling SHA-3-512 in `.nonce_registry.{seq}.hmac`; truncation breaks the chain.
- **Cross-fs rename double-check** (MEDIUM-2): `st_dev` check both after tmp creation AND immediately before `os.rename`; divergence raises `CrossFilesystemRename` — closes mid-write remount TOCTOU.
- **Unified signal handler** (LOW-2): Single `_shutting_down` atomic flag; second-signal handler path returns immediately if flag set. One-shot checkpoint write.
- **Ledger rotation at 100 MiB** (LOW-5): When a ledger exceeds 100 MiB, a new segment `.{seq}.jsonl` is opened. Each segment carries its own HMAC trailer; boot verifies the segment chain in order.
- **New failure codes:** `F-ADM-08` ledger watermark regression, `F-ADM-09` clock rollback detected, `F-KEY-08` KeyStore contract violation, `F-KEY-09` nonce registry size exceeded without rotation, `F-ISO-06` cross-fs rename race detected on re-check.

**Rejected Red Team contests (justification in §10):** F1 namespace rename (documentation, not blueprint); F2 macOS BT2 equivalence (trusted-operator threat model is explicit; formal proof not a blueprint requirement); F3 FileKeyStore journal-erase (documented limitation, not a fix); F5 Keychain `operator_id` (Phase 2); M1 URL-hash re-verify (envelope is trusted-operator artifact; editing it is out-of-model).

All v1/v2-passing content is preserved; revisions are local to the named files.

**Parent architecture:** `pipeline/architecture/v0.1/tilth_architecture_locked.md` (v4 LOCKED 2026-04-16).

**This section's job:** Specify the HOW for the mechanisms that run at the perimeter of Tilth — the boundary where inputs enter the pipeline, where keys live, where sessions begin and end, and where the append-only ledgers and logs that the rest of the system depends on are written. If this section is wrong, every other section inherits the bug.

**Sections this section owns (from the architecture):**
- **Mechanisms:** M1 RFA dual-hash, M2 PROJECT_CONTEXT envelope + session binding, M3 org-slug canonicalization, M5 router-integrity runtime invariant, M6 atomic flush + `INTERRUPTED` state, M7 per-session HMAC key lifecycle, M10 graceful-degradation recording for author seats, M13 review-seat outage escape-valve recording.
- **Blueprint-tracked:** BT1 SHA-3-512 + nonce, BT2 OS-level namespace isolation + TOCTOU closure, BT3 admin-risk ledger rate-limits, BT4 HSM-capable key storage, BT6 M7 HMAC key lifecycle, BT8 degraded-run / bypass flag append-only log.

**Sections this section does NOT own:** S9 source-tag grep verification (Section 4 — Logician). BT7 atomic claim-evidence map sign-overwrite (Section 4). BT9 USER_DATA conversation-anchor integrity (Section 4). BT10 grep-check windowing (Section 4). BT11 cross-org dossier reference policy (Section 4). BT12 Channel F domain pre-flight (Section 3 — Scout). BT13 rails report signing (Section 4). BT5 per-session/per-org provider quota and back-off (Section 5 — Pipeline). Every write Section 1 produces is consumed by Section 4 or later; Section 1 writes, others verify.

**Trusted-operator threat-model boundary (stated up front, referenced throughout):**

Section 1 trusts the operator's keyring, the operator's typing on HIGH-severity re-type confirmations, signed commits to `router.yaml` on the operator's keyring, and operator sign-offs on dossiers. Section 1 does NOT trust LLM outputs, web-fetched content prior to M11 materialization, API keys that arrived via process environment without operator-authorized injection, or any third-party code that has not been installed from an operator-approved provenance (pinned `pip-tools` lockfile; supply-chain signing of Python packages is out of scope for v0.1 and deferred to Phase 2+). The trust root is the operator's physical Mac plus the operator's keyring. If either is compromised, v0.1 provides no mitigation — that is the design and the sovereignty promise is explicit about it (`/SOUL.md`, architecture Section K).

**v0.1 constraints:**
- Runs on Josh's M1 Mac Mini 8GB dev. Everything here must fit comfortably in that envelope.
- Headless only. No UI. No web server. No WebSocket.
- BYOK only. No Anthropic-hosted key material. No third-party key escrow.
- Zero token cost. Section 1 uses no LLMs. All logic is deterministic Python + `cryptography`, `hashlib`, `secrets`, `hmac`, `os`, `stat`.
- Fail-closed. Every failure path halts the pipeline cleanly rather than silently degrading.

---

## 1. Module inventory

All modules live at `pipeline/sovereignty/` relative to the repo root. Section 1 ships as a Python package importable as `from pipeline.sovereignty import <name>`. No module has a runtime dependency on an LLM.

| # | Module | Lines (target) | Owns |
|---|---|---|---|
| 1 | `__init__.py` | ~40 | Public API surface, version pin, module-level boot guard |
| 2 | `crypto_primitives.py` | ~230 | `sha3_512_with_nonce`, `hmac_sha3_512`, `aesgcm_encrypt`/`decrypt`, `pbkdf2_sha3_512`, `constant_time_equal`, `zero_bytes` (bytearray/memoryview-only), `SecretBytes` context manager |
| 3 | `keys.py` | ~600 | `KeyStore` ABC (returns **`SecretBytes`**) + `MacOSKeychainKeyStore` + `FileKeyStore` (passphrase-hygienic) + `YubiHSMKeyStore` (stub) + `resolve_keystore` factory + AES-GCM nonce registry (rotation + rolling-hash) |
| 4 | `audit.py` | ~430 | Generic append-only hash-chain writer/reader WITH per-ledger HMAC trailer containing `last_seq_id`; ledger-rotation at 100 MiB; boot-time watermark verification against `ledger_watermarks.json`; **v5**: sovereignty init marker read/verify helpers (`verify_sovereignty_init_marker`, `write_sovereignty_init_marker_first_boot`) |
| 5 | `session.py` | ~300 | `Session` lifecycle: start, rotate HMAC key, end, interrupted-handler registration, UNIFIED signal handler with `_shutting_down` flag |
| 6 | `isolation.py` | ~320 | `OrgRootNamespace` — canonical-path + inode-snapshot TOCTOU closure + fd-based fstat re-check (macOS); `unshare(CLONE_NEWNS)` bind-mount (Linux production); `within_org_root` predicate |
| 7 | `topology.py` | ~180 | DOC_SOURCED whitelist enforcement (the five roots from M12), path canonicalization helpers, symlink rejection |
| 8 | `rfa_envelope.py` | ~220 | M1 dual-hash at ingest + pre-draft re-verify; `RFAEnvelope` dataclass |
| 9 | `project_context_envelope.py` | ~180 | M2 PROJECT_CONTEXT sealing, session binding; `PROJECTContextEnvelope` dataclass |
| 10 | `org_slug.py` | ~120 | M3 slug canonicalization rules + collision check against existing `orgs/` |
| 11 | `admin_risk.py` | ~370 | BT3 rate-limited append-only ledger for flagged-term substitutions AND M13 bypass authorizations; per-severity quotas; re-type confirmation gate; **lock-before-count** ordering; day-counter as read-through CACHE (truth is the ledger); boot_clock_history read on every M13 verification |
| 12 | `degradation_log.py` | ~280 | BT8 append-only hash-chained log for M10 `degraded_run` flags and M13 `bypass_active` flags; per-ledger HMAC trailer w/ `last_seq_id`; monotonic-ns + wall-clock pair + boot_clock_history triangulation for bypass expiry |
| 13 | `interrupted_state.py` | ~260 | M6 atomic-flush checkpoint writer, INTERRUPTED state reader, resume-or-discard decision; single combined `{status, payload}` atomic write; **double-check** `st_dev` cross-fs guard |
| 14 | `router_integrity.py` | ~160 | M5 / S5 `router.yaml` HMAC signature verify at pipeline start; cross-family runtime invariant helper |
| 15 | `boot.py` | ~290 | Sovereignty Envelope boot sequence: what runs at pipeline start, in what order, with what fail-closed paths; watermark verify; boot_clock_history append; **v5**: init marker verify on every boot, init marker first-write on genuine first boot, O_NOFOLLOW + fstat guard on every lock-file open |

Total target: ~3,910 lines (v5 — net +130 lines vs v4 for the init marker + O_NOFOLLOW hardening; +590 vs v1). Comfortably small. Holds in a single developer's head.

**Split rationale:** `audit.py` is generic hash-chain machinery because both `admin_risk.py` and `degradation_log.py` need it — factoring it out prevents the two consumers from drifting. `isolation.py` vs `topology.py` is split because isolation is the *mechanism* (how the OS enforces boundaries) and topology is the *policy* (which directories are allowed). Keeping them separate lets the mechanism be swapped (macOS canonical-path today; Linux bind-mount on production clients) without rewriting policy code.

---

## 2. Data-structure schemas

All schemas live as Python `dataclasses.dataclass(frozen=True)` with `kw_only=True`. Frozen because every instance should be immutable — if state needs to change, a new instance is written to an append-only log. JSON serialization via `dataclasses.asdict` + `json.dumps(..., sort_keys=True, separators=(",", ":"))` for deterministic hashing. All timestamps UTC, ISO-8601, suffix `Z`. All hashes hex-encoded SHA-3-512 (128 chars). All nonces hex-encoded 32-byte random (64 chars).

### 2.1 `HashPair`

```python
@dataclass(frozen=True, kw_only=True)
class HashPair:
    url_hash: str          # 128 hex chars (SHA-3-512 of the URL string, UTF-8, no BOM)
    content_hash: str      # 128 hex chars (SHA-3-512 of content bytes || nonce)
    algorithm: str = "SHA3-512"
    nonce_hex: str         # 64 hex chars (32 random bytes from secrets.token_bytes)
```

**Invariant:** `url_hash` is computed over the URL alone (no nonce) so identical URLs across sessions produce the same `url_hash` — this is what lets Logician detect "same URL, different content" (a re-fetch with tampering). `content_hash` includes the nonce so identical content in two independent ingest events still produces distinct `content_hash` values — this is what closes BT1's adversarial pre-image construction path. The nonce is generated once at ingest and carried with the envelope for the life of the session.

### 2.2 `RFAEnvelope`

```python
@dataclass(frozen=True, kw_only=True)
class RFAEnvelope:
    rfa_id: str                       # e.g., "USDA-RD-VAPG-2026" or operator-assigned
    ingested_at: str                  # UTC ISO-8601
    hashes: HashPair
    session_bound_slug: str           # org slug this RFA was ingested for
    canonical_path: str               # absolute, symlink-resolved path to the ingested file
    inode: int                        # st_ino at ingest time (for TOCTOU closure)
    device: int                       # st_dev at ingest time
    size_bytes: int                   # stat size at ingest, sanity check at re-verify
    ingested_by: str                  # operator identifier (from keychain)
```

### 2.3 `PROJECTContextEnvelope`

```python
@dataclass(frozen=True, kw_only=True)
class PROJECTContextEnvelope:
    slug: str                         # canonical org slug (see M3 / Section 4)
    canonical_path: str               # always orgs/{slug}/PROJECT_CONTEXT.md, resolved
    inode: int
    device: int
    content_hash: str                 # SHA-3-512 with per-session nonce
    nonce_hex: str
    sealed_at: str                    # UTC ISO-8601
    bound_session_id: str             # session UUID that sealed this envelope
```

**M2 binding rule:** A session binds to exactly one `PROJECTContextEnvelope` at start. Any attempt to load a second envelope during the same session is a Law 3 violation and hard-aborts. Cross-org operator choice is made at session-creation time, not mid-session.

### 2.4 `Session`

```python
@dataclass(frozen=True, kw_only=True)
class Session:
    session_id: str                   # UUID4
    slug: str                         # bound org slug
    started_at: str                   # UTC ISO-8601
    hmac_key_id: str                  # opaque handle into KeyStore; never the key material
    router_manifest_sha: str          # the signed-commit SHA of router.yaml verified at boot
    pid: int                          # owning process PID
    status: str                       # "ACTIVE" | "ENDED_CLEAN" | "INTERRUPTED"
    interrupted_payload_path: str | None
```

Sessions are written to `sovereignty/sessions/{session_id}.json`. Only one `Session` is active at a time in v0.1 (single-operator). A file-lock at `sovereignty/sessions/.active.lock` prevents concurrent start.

### 2.5 `AdminRiskEntry` (shared schema, see note on conflation)

```python
@dataclass(frozen=True, kw_only=True)
class AdminRiskEntry:
    seq_id: int                       # monotonic per-ledger
    timestamp_utc: str                # wall-clock UTC ISO-8601
    issued_monotonic_ns: int          # v2: time.monotonic_ns() at append time — survives wall-clock jumps,
                                      # used by M13 to enforce the 72h ceiling against clock-drift attacks
    severity: str                     # "GREEN" | "YELLOW" | "RED"
    entry_kind: str                   # "flagged_term_substitution" | "review_seat_bypass"
    payload_json: str                 # entry-kind-specific blob, canonicalized JSON
    operator_retype_hash: str | None  # HMAC-SHA3-512(operator_key, typed_confirmation)
                                      # required for RED severity
    prev_hash: str                    # SHA-3-512 of the canonicalized prior entry; "0" * 128 for genesis
    entry_hash: str                   # SHA-3-512 of (canonicalized fields excluding entry_hash)
```

**Note on conflation (flagged by the pre-draft review, see Section 10 Findings):** The v4 architecture names a single "admin-risk ledger" but the current code repo already carries two distinct registers: the term-scoped `admin_risk_register.json` (flagged-term register, LIVE) and the new `architectural_risk_register.json` (ADM-A-001, ADM-A-002 — written at v4 lock). `AdminRiskEntry` above is the shared schema for the append-only LEDGER (the event log). The two REGISTERS (the reference lookups) remain separate files with their own schemas because they answer different questions. See Section 10 Finding F1 for the explicit disambiguation.

### 2.6 `DegradationEvent`

```python
@dataclass(frozen=True, kw_only=True)
class DegradationEvent:
    seq_id: int
    timestamp_utc: str                # wall-clock UTC
    issued_monotonic_ns: int          # v2: time.monotonic_ns() at append — paired with timestamp_utc for M13 72h ceiling
    event_kind: str                   # "author_seat_degraded_run" | "review_seat_bypass_active" | "bypass_expired" | "bypass_renewed"
    seat: str                         # "scout" | "scribe" | "editor" | "judge" | "red_team" | "code_review" | "reasoner_review"
    reason_code: str                  # "family_outage_30m" | "operator_m13_auth" | "auth_expired" | ...
    duration_seconds: int | None      # active duration for degraded_run or bypass window
    authorization_id: str | None      # FK to the admin-risk ledger AdminRiskEntry.seq_id for M13
    expires_at: str | None            # UTC wall-clock expiry (for bypasses)
    expires_monotonic_ns: int | None  # v2: paired monotonic expiry — bypass is active iff BOTH wall AND monotonic remain unexpired
    boot_epoch_ns_at_issuance: int | None  # v3 (HIGH-2): kern.boottime / btime of the OS boot during which this bypass was issued; anchors the issuance to a specific boot_clock_history entry so a subsequent process restart cannot revive it
    signed_by_operator: bool          # true for M13 bypass; false for automatic M10 degraded_run
    prev_hash: str
    entry_hash: str
```

`boot_epoch_ns_at_issuance` is populated at append-time for `event_kind="review_seat_bypass_active"` records via `platform_boot.read_boot_epoch_ns()` (macOS: `sysctl kern.boottime`; Linux: `/proc/stat btime`). v3's `bypass_is_active()` predicate rejects any bypass whose `boot_epoch_ns_at_issuance` does not appear in the current `boot_clock_history.jsonl` — this closes Red Team v2 HIGH-2 (wall-clock rollback + process-restart replay).

### 2.7 `RouterManifest`

```python
@dataclass(frozen=True, kw_only=True)
class RouterManifest:
    router_yaml_sha: str              # SHA-3-512 of canonicalized router.yaml bytes
    commit_sha: str                   # git commit SHA of the HEAD that introduced this router.yaml
    signed_by_key_id: str             # opaque KeyStore handle
    signature_hex: str                # HMAC-SHA3-512 of (router_yaml_sha || commit_sha)
    verified_at: str                  # UTC ISO-8601
```

`RouterManifest` is produced at session start by `router_integrity.py` and stashed in the `Session` as `router_manifest_sha`. Logician consults it on every seat call.

### 2.7b `SovereigntyInitMarker` (v5 — RT-v4 HIGH-1 first-boot reset closure)

```python
@dataclass(frozen=True, kw_only=True)
class SovereigntyInitMarker:
    init_version: int                                # schema version; v5 = 1
    created_at_utc: str                              # ISO-8601 UTC, at first-boot of this Tilth install
    hostname: str                                    # platform.node() at first boot, for operator-side verification
    operator_slug: str | None                        # populated if operator identity known at first boot (M3); may be None
    boot_epoch_ns_first: int                         # kern.boottime (macOS) or /proc/stat btime (Linux), ns, at first boot
    boot_clock_history_seq_at_init: int              # seq_id of the boot_clock_history entry written BEFORE this marker (establishes anchor)

@dataclass(frozen=True, kw_only=True)
class SovereigntyInitMarkerHmacTrailer:
    init_version: int                                # mirrors marker body (must match; independent of trailer_version to guard v-skew forgery)
    init_hmac: str                                   # 128 hex chars — HMAC-SHA3-512 of canonical JSON of SovereigntyInitMarker body, keyed by keystore key `tilth.sovereignty.init.hmac.v1`
    wall_at_write_utc: str                           # ISO-8601; when the HMAC was computed
```

`SovereigntyInitMarker` is produced ONCE — on the first genuine boot of a Tilth instance — and NEVER mutated thereafter. Every subsequent boot verifies the HMAC against the body. Under the trusted-operator threat model, an attacker with file-write capability can delete both files and truncate all ledgers to zero lines, but cannot produce a valid `SovereigntyInitMarkerHmacTrailer` without access to `tilth.sovereignty.init.hmac.v1` — which lives in Keychain (or AES-GCM-wrapped in FileKeyStore) and is out of reach in-model. `boot_clock_history_seq_at_init` exists so the "first-boot" moment is cross-referenced against the earliest `boot_clock_history.jsonl` entry; a post-hoc attempt to write a fresh marker after first boot must reconstruct the earliest boot_clock_history entry too, which it cannot forge (also HMAC-sealed).

**Canonical JSON rules for HMAC computation** (mirrors watermarks HMAC canon): keys sorted lexicographically, ASCII-only (`ensure_ascii=True`), no whitespace separators (`separators=(",", ":")`), UTF-8 encoded. Exact bytes signed. Any whitespace or reordering by an attacker before HMAC re-computation will not match a legitimate trailer.

**Why not just lean on `ledger_watermarks.hmac`?** The v4 watermark HMAC closes "rollback to older self-consistent snapshot" but does not close "truncate to empty + delete watermarks = legitimate first boot" because v4 treats body-absent + HMAC-absent + all ledgers empty as the legitimate first-boot state. The init marker is the distinguisher: once a valid marker exists, the legitimate-first-boot state is no longer reachable. The marker is the witness that a first boot already happened.

### 2.8 On-disk layout

```
sovereignty/
├── sessions/
│   ├── .active.lock                             # fcntl advisory lock, one-active-session enforcement
│   ├── {uuid}.json                              # Session records (ACTIVE, ENDED_CLEAN, INTERRUPTED)
│   └── {uuid}.interrupted.json                  # M6 combined {status, payload} — single atomic write (v2)
├── ledgers/
│   ├── admin_risk.jsonl                         # append-only; one AdminRiskEntry per line (rotated at 100 MiB → admin_risk.{seq}.jsonl v3)
│   ├── admin_risk.head                          # 128 hex chars — cached tail entry_hash for fast append
│   ├── admin_risk.hmac                          # v3: per-segment HMAC-SHA3-512 trailer (JSON: {last_seq_id, last_entry_hash, ledger_hmac, trailer_version, segment_index})
│   ├── admin_risk.counts.{YYYY-MM-DD}.json      # v3: read-through CACHE only — ledger is source of truth (rebuilt from ledger seq on boot if missing/stale)
│   ├── admin_risk.lock                          # v2: the fcntl lock-file that gates append (separate from data)
│   ├── degradation.jsonl                        # append-only; one DegradationEvent per line (rotated at 100 MiB v3)
│   ├── degradation.head
│   ├── degradation.hmac                         # v3: per-segment HMAC-SHA3-512 trailer JSON
│   └── degradation.lock                         # v2: fcntl lock-file
├── watermarks/
│   ├── ledger_watermarks.json                   # v3 (HIGH-1): persistent boot-baseline {ledger_name: {last_seq_id, last_trailer_hmac_hex, wall_at_write_utc}} — rollback detection anchor
│   ├── ledger_watermarks.hmac                   # v4 (RT-v3 HIGH-1): HMAC-SHA3-512 trailer over canonical JSON body, keyed by `tilth.watermarks.hmac.v1`; closes watermark-forge rollback
│   └── ledger_watermarks.lock                   # v4: fcntl lock-file gating body+HMAC atomic update (single held lock across both writes); v5: opened with O_NOFOLLOW + inode fstat verification
├── init.marker                                  # v5 (RT-v4 HIGH-1): JSON body {init_version: 1, created_at_utc, hostname, operator_slug, boot_epoch_ns_first, boot_clock_history_seq_at_init}; written ONCE on first boot; closes first-boot-reset attack
├── init.marker.hmac                             # v5 (RT-v4 HIGH-1): HMAC-SHA3-512 trailer over canonical JSON body, keyed by `tilth.sovereignty.init.hmac.v1`; verified at EVERY boot
├── init.marker.lock                             # v5: fcntl lock-file gating init marker body+HMAC atomic first-write (single held lock); opened with O_NOFOLLOW + inode fstat verification
├── clock/
│   ├── boot_clock_history.jsonl                 # v3 (HIGH-2): append-only tamper-evident (boot_epoch_ns, wall_at_boot_utc) pairs; one entry appended every boot by boot.py step 2.5; anchors M13 bypass freshness
│   └── boot_clock_history.lock                  # v4 (RT-v3 MED-2): fcntl lock-file gating append+HMAC-recompute atomic block (single held lock across both steps)
├── envelopes/
│   ├── rfa/{rfa_id}.json                        # RFAEnvelope records
│   ├── project_context/{slug}.json              # PROJECTContextEnvelope records (latest per org)
│   └── project_context/{slug}.json.lock         # v2: per-slug advisory lock for seal+bind atomicity
├── keys/
│   └── {slug}/
│       ├── {key_id}.aead                        # FileKeyStore sealed key material (when provider=file)
│       ├── .nonce_registry.{seq}.jsonl          # v3: append-only AES-GCM nonce uniqueness registry; rotated at 10 MiB (MEDIUM-1)
│       └── .nonce_registry.{seq}.hmac           # v3 (LOW-1): rolling SHA-3-512 trailer across segments; truncation detected
└── router/
    └── manifest.{session_id}.json               # RouterManifest records, per-session
```

All JSONL lines are canonicalized (sorted keys, UTF-8, `\n` line ending). No trailing whitespace. Ledger files are append-only at the OS level via `O_APPEND | O_WRONLY` opened with `os.open`; writes are single `write()` syscalls bounded by `PIPE_BUF` (≤512 bytes well below the 4096-byte POSIX atomic-write guarantee, which all ledger entries satisfy). Larger entry payloads live in a sidecar `{seq_id}.payload.json` referenced by hash from the ledger line.

---

## 3. Interfaces in / out

Section 1 exports a small, deliberate public API. Everything else is private.

### 3.1 `pipeline.sovereignty.__init__`

```python
# Public API — stable across Section 1 patch versions
from .boot import SovereigntyEnvelope, boot_envelope
from .session import Session, start_session, end_session
from .rfa_envelope import RFAEnvelope, ingest_rfa, reverify_rfa
from .project_context_envelope import PROJECTContextEnvelope, seal_project_context
from .org_slug import canonical_slug, ensure_slug_available
from .admin_risk import AdminRiskEntry, record_admin_risk, read_ledger_tail
from .degradation_log import DegradationEvent, record_degradation, read_degradation_tail
from .interrupted_state import checkpoint, detect_interrupted, resume_or_discard
from .router_integrity import RouterManifest, verify_router_integrity
from .keys import KeyStore, resolve_keystore

__version__ = "0.1.0"
__all__ = [...]  # explicit list, no dynamic exports
```

### 3.2 Boot

```python
def boot_envelope(
    *, repo_root: Path, operator_id: str, slug: str,
    interrupt_policy: str = "prompt",  # "prompt" | "resume" | "discard"
) -> SovereigntyEnvelope:
    """Run the Sovereignty Envelope boot sequence. See Section 9 for the exact ordering."""
```

Raises: `SovereigntyBootError` (subclass of `SystemExit`-compatible, message carries the fail-closed reason).

### 3.3 Session lifecycle

```python
def start_session(
    *, envelope: SovereigntyEnvelope, rfa: RFAEnvelope,
    project_context: PROJECTContextEnvelope,
) -> Session: ...

def end_session(session: Session, *, status: str = "ENDED_CLEAN") -> None: ...
```

`start_session` fails if (a) another session is ACTIVE on disk, (b) `rfa.session_bound_slug != project_context.slug`, (c) `project_context.slug` fails canonicalization against M3 rules, (d) the RouterManifest for this session fails signature verify, or (e) the operator's KeyStore resolves to a state that does not permit HMAC key issuance (for example a locked Keychain with no operator interaction available — Section 6 failure mode F-KEY-03).

### 3.4 RFA envelope

```python
def ingest_rfa(*, url: str, content_bytes: bytes, slug: str, operator_id: str) -> RFAEnvelope: ...
def reverify_rfa(envelope: RFAEnvelope) -> None:
    """Raise RFADriftError if the canonical path + inode + content_hash no longer match."""
```

`reverify_rfa` is called by Logician at the boundary between Scout's DISCOVER/VERIFY output and Scribe's draft — specifically Section 4 consumes this. Section 1 provides the call; it does not decide when to call it.

### 3.5 PROJECT_CONTEXT envelope

```python
def seal_project_context(*, slug: str, session_id: str) -> PROJECTContextEnvelope: ...
```

Seal binds the envelope to the session_id and writes `envelopes/project_context/{slug}.json`. Subsequent reads during the session assert bound_session_id match.

### 3.6 Slug canonicalization

```python
def canonical_slug(s: str) -> str:
    """NFC-normalize, lowercase, ASCII-only, dash-separated, strip leading/trailing dashes.
    Collapse runs of dashes. Reject empty results. Max length 64 chars."""

def ensure_slug_available(slug: str, *, repo_root: Path) -> None:
    """Raise SlugCollisionError if orgs/{slug} already exists AND was not the session's bound slug."""
```

### 3.7 Admin-risk ledger (shared ledger, dispatch by entry_kind)

```python
def record_admin_risk(
    *, session: Session, entry_kind: str, severity: str, payload: dict,
    operator_retype_confirmation: str | None = None,
) -> AdminRiskEntry: ...

def read_ledger_tail(*, n: int = 50) -> list[AdminRiskEntry]: ...
```

If `severity == "RED"` and `operator_retype_confirmation is None`, raises `OperatorConfirmationRequired`. This is the fail-closed stance — the caller must have already collected the confirmation before invoking. See Section 6 F-ADM-01.

### 3.8 Degradation log

```python
def record_degradation(
    *, session: Session, event_kind: str, seat: str, reason_code: str,
    duration_seconds: int | None = None,
    authorization_id: str | None = None,
    expires_at: str | None = None,
) -> DegradationEvent: ...
```

### 3.9 Interrupted state

```python
def checkpoint(session: Session, payload: dict) -> Path: ...
def detect_interrupted(repo_root: Path) -> Session | None: ...
def resume_or_discard(session: Session, *, policy: str) -> dict | None: ...
```

### 3.10 Router integrity

```python
def verify_router_integrity(*, repo_root: Path, keystore: KeyStore) -> RouterManifest: ...
```

Verifies the signed commit on `router.yaml` using the operator's keyring. Raises `RouterIntegrityError` on any mismatch.

### 3.11 KeyStore ABC (v3 — returns `SecretBytes`, NOT raw `bytes`; v4 — `retrieve()` is SEALED)

```python
import typing

class KeyStoreContractViolation(TypeError):
    """Raised when a subclass violates the KeyStore contract — either by
    returning a non-bytearray from _retrieve_raw (F-KEY-08, v3) or by attempting
    to override the sealed retrieve() method (F-KEY-10, v4)."""


class KeyStore(abc.ABC):
    # --- v4 contract sealing --------------------------------------------------

    def __init_subclass__(cls, **kwargs) -> None:
        """Seals the public `retrieve()` surface. Subclasses may ONLY override
        `_retrieve_raw`; any subclass that attempts to override `retrieve`
        directly breaks the SecretBytes wrap and is rejected at class-definition
        time (F-KEY-10). This closes Red Team v3 HIGH-2 (subclass-override
        bypass) at the type system level, not at runtime.
        """
        super().__init_subclass__(**kwargs)
        if "retrieve" in cls.__dict__:
            raise KeyStoreContractViolation(
                f"{cls.__name__} attempts to override KeyStore.retrieve(), which "
                "is sealed (@typing.final). Subclasses must override _retrieve_raw "
                "only. This is RT-v3 HIGH-2 — do not bypass the SecretBytes wrap."
            )

    # --- abstract surface -----------------------------------------------------

    @abc.abstractmethod
    def store(self, *, key_id: str, key_bytes: bytes | bytearray, purpose: str) -> None: ...

    @abc.abstractmethod
    def _retrieve_raw(self, key_id: str) -> bytearray:
        """Internal: subclasses implement. MUST return bytearray (mutable).

        Never return `bytes` — the immutable Python bytes object cannot be zeroed
        in place, which re-opens the v1 HIGH finding. The ABC wrapper `retrieve()`
        below enforces the contract at runtime.
        """
        ...

    # --- concrete, sealed public surface --------------------------------------

    @typing.final
    def retrieve(self, key_id: str) -> SecretBytes:
        """Public contract — returns SecretBytes. SEALED (v4) — cannot be
        overridden by subclasses; `__init_subclass__` enforces.

        This is the ONLY sanctioned caller-visible retrieval path. Any code that
        reaches into `_retrieve_raw` directly violates Section 1 memory hygiene
        and breaks the v1 HIGH-1 closure.

        Enforcement: runtime isinstance check raises `KeyStoreContractViolation`
        (F-KEY-08) if a subclass returns anything other than bytearray from
        `_retrieve_raw`. This catches implementation drift where a new provider
        returns `bytes` or `str` from a CLI call.
        """
        raw = self._retrieve_raw(key_id)
        if not isinstance(raw, bytearray):
            raise KeyStoreContractViolation(
                f"{type(self).__name__}._retrieve_raw returned {type(raw).__name__}; "
                "must be bytearray. This is the HIGH-3 v2 finding — do not bypass."
            )
        return SecretBytes(raw)  # transfers ownership; caller must use `with`

    @abc.abstractmethod
    def rotate(self, key_id: str) -> str: ...         # returns new key_id
    @abc.abstractmethod
    def zero(self, key_id: str) -> None: ...
    @abc.abstractmethod
    def exists(self, key_id: str) -> bool: ...
    @abc.abstractmethod
    def provider(self) -> str: ...                    # "keychain" | "file" | "yubihsm"
```

Concrete: `MacOSKeychainKeyStore`, `FileKeyStore`, `YubiHSMKeyStore` (stub — raises `NotImplementedError` in v0.1 with a clear message routing operator to BT4 switch). All shipped subclasses override only `_retrieve_raw` — none overrides `retrieve`.

**v3 enforcement detail (preserved):** `retrieve()` is a concrete ABC method that wraps the subclass `_retrieve_raw()` output. Subclasses override only `_retrieve_raw`. This makes the SecretBytes wrapping impossible to forget. Any caller that imports `KeyStore` and calls `.retrieve(key_id)` gets a `SecretBytes` context manager back.

**v4 enforcement detail (new):** The `retrieve()` method is now `@typing.final` (a documentary annotation enforced by static type checkers) AND sealed at class-definition time via `__init_subclass__`. The `__init_subclass__` hook inspects `cls.__dict__` — the class-local namespace, NOT inherited attributes — and rejects any subclass that defines its own `retrieve`. This closes RT-v3 HIGH-2 before any instance of the malicious subclass can be constructed. Metaclass bypass is not possible because `__init_subclass__` runs inside `type.__init__` before any user code sees the new class.

**Why both `@typing.final` and `__init_subclass__`?** `@typing.final` is a *linter-level* contract — it tells `mypy`/`pyright` that subclasses shouldn't override, and fails the build at CI time. `__init_subclass__` is a *runtime* contract — it fails at import time regardless of static analysis. Belt-and-suspenders because the threat model includes "KeyStore subclass contract violations", which covers both accidental (caught by linter) and deliberate (caught at runtime) violations.

**Why not just change `retrieve` to return `SecretBytes` and let subclasses implement it?** Because v2 did exactly that on paper but concrete implementations still returned `bytes` internally and the wrapping was a TODO. v3 moves the wrap INTO the ABC so subclass authors cannot accidentally emit raw bytes — the type system forces `bytearray` out of `_retrieve_raw`, and the ABC wraps it. v4 adds the final lock: subclasses cannot even attempt to override `retrieve` without raising at class-definition time.

**v5 trust-boundary note (RT-v4 HIGH-2 rejected):** The Red Team v4 attack — a metaclass `StripRetrieveMeta` that deletes `"retrieve"` from `cls.__dict__` before `__init_subclass__` runs, or a runtime monkey-patch `KeyStore.retrieve = lambda self, kid: b'FAKE'` — requires executing arbitrary Python inside the Tilth process. Under the trusted-operator threat model (stated in the header of this section; see also §10 F9 bullet 1), same-uid code injection is explicitly OUT-OF-SCOPE. The `__init_subclass__` + `@typing.final` seal is the contract for well-behaved code, not for hostile code running under the operator's uid. Sealing `retrieve` against metaclass manipulation would require moving the key-retrieval path into a C extension with private symbol linkage, which is a v0.1 non-goal. This rejection is anchored in §10 F9 and is the hard boundary.

### 3.11b Sovereignty init marker (v5 — RT-v4 HIGH-1 first-boot reset closure)

```python
def verify_sovereignty_init_marker(
    *, marker_path: Path, hmac_path: Path, keystore: KeyStore,
    key_id: str = "tilth.sovereignty.init.hmac.v1",
    ledger_states: dict[str, LedgerState],
) -> SovereigntyInitMarker:
    """Called at every boot, BEFORE any ledger or watermark body is trusted.

    Three legitimate outcomes:
    (a) Both marker + HMAC present, HMAC verifies → return SovereigntyInitMarker body.
    (b) Both marker + HMAC absent AND every ledger in `ledger_states` has zero
        entries AND every watermark body is absent → legitimate-first-boot path;
        caller must invoke `write_sovereignty_init_marker_first_boot` BEFORE
        any ledger append or watermark write.
    (c) Any other combination → fail-closed:
        - marker present + HMAC absent → F-ADM-11 SovereigntyInitMarkerMissing
        - HMAC present + marker absent → F-ADM-11 SovereigntyInitMarkerMissing
        - both present but HMAC mismatches canonical JSON → F-ADM-12 SovereigntyInitMarkerMismatch
        - both absent BUT any ledger has >=1 entry OR any watermark body present
          → F-ADM-12 SovereigntyInitMarkerMismatch (i.e. "first-boot reset attack
          detected — ledgers/watermarks were tampered with or an older install
          was partially wiped"). This is the RT-v4 HIGH-1 closure.
    """


def write_sovereignty_init_marker_first_boot(
    *, marker_path: Path, hmac_path: Path, lock_path: Path,
    keystore: KeyStore, key_id: str = "tilth.sovereignty.init.hmac.v1",
    boot_clock_history_seq: int, boot_epoch_ns: int,
    operator_slug: str | None = None,
) -> SovereigntyInitMarker:
    """Invoked ONLY by boot.py step 7c.0b when verify_sovereignty_init_marker
    returned the legitimate-first-boot signal. Writes body tmp→rename + HMAC
    tmp→rename under a single held `init.marker.lock` fcntl.LOCK_EX lock.
    Never called again for the lifetime of a Tilth install.

    The lock is opened with safe_open_lock_file (see §3.11c), which passes
    O_NOFOLLOW and verifies the opened inode matches the parent-directory
    readdir entry. Symlink attack on init.marker.lock is rejected at this
    syscall boundary.

    After successful first-boot write, step 7c.0 on every subsequent boot
    will enter outcome (a). The write-once invariant is enforced by
    write_sovereignty_init_marker_first_boot raising
    SovereigntyInitMarkerAlreadyExists if either file already exists
    (F-ADM-11).
    """
```

Called from `boot.py` step 7c.0 (verify) and step 7c.0b (first-boot write). See §4.9b for the implementation sketch and §9 for boot-sequence integration.

**Why is `boot_clock_history_seq` in the marker body?** The marker binds to a specific `boot_clock_history.jsonl` entry — the entry written in step 2.5 of THIS boot. Because `boot_clock_history.jsonl` is itself HMAC-sealed (with `tilth.clock.boot_history.hmac.v1`), an attacker who wants to forge a fresh init marker AFTER first boot must also forge a fresh boot_clock_history entry at seq_id=N. That requires access to a second keystore key. The two HMACs are in a chain. Defense-in-depth.

### 3.11c Lock-file safe-open helper (v5 — RT-v4 MED-1 symlink-swap closure)

```python
def safe_open_lock_file(
    lock_path: Path, *, create_if_missing: bool = True,
) -> int:
    """Open a fcntl lock file with anti-symlink protection.

    Opens with O_NOFOLLOW — if `lock_path` is a symlink, open() raises
    OSError with errno.ELOOP; the helper converts this to
    LockFileSymlinkAttack (F-ISO-07, v5).

    After open, fstat() the fd and compare with os.lstat(lock_path) to ensure
    (st_dev, st_ino) match. This catches a TOCTOU where an attacker deletes
    the real lock file and symlinks a new one between the O_NOFOLLOW-safe
    open and the caller's first flock/write. The fd is already open to the
    real inode, so even if the name now points elsewhere, we operate on the
    correct inode.

    Additional post-open check: os.fstat(fd).st_uid must equal os.getuid()
    — a lock file owned by another uid is rejected (belt-and-suspenders with
    the surrounding 0700 mode on sovereignty/; a misconfigured deployment
    that left the directory group-writable is caught here).

    Raises:
        LockFileSymlinkAttack (F-ISO-07): O_NOFOLLOW triggered ELOOP or the
            post-open inode check failed.
        PermissionError: file owned by another uid.

    Returns:
        fd (int): caller owns; must close with os.close(fd) or via a context
        manager (the callers in audit.py, keys.py, and boot.py all wrap via
        contextlib.closing).
    """
```

Called from every site that opens a `*.lock` file in `sovereignty/`:
- `audit.py`: `ledger_watermarks.lock`, `{ledger_name}.lock`, `{ledger_name}.{seq}.lock`
- `keys.py`: per-slug `.nonce_registry.lock`
- `boot.py`: `init.marker.lock`, `boot_clock_history.lock`
- `session.py`: `.active.lock`
- `interrupted_state.py`: `{session_id}.interrupted.lock` (if any)

**Why not trust 0700 mode alone?** Because `sovereignty/` is under `$HOME` and a mis-deployment might leave a parent directory writable by a secondary local account (shared lab machines, guest accounts on a dev laptop). The O_NOFOLLOW + fstat guard is cheap and closes the symlink attack regardless of the surrounding permission posture. The v0.1 threat model does not require resilience against a hostile second local account, but the attack surface for "attacker planted symlink earlier, attacker later has file-write to the path" is real and worth the 10 lines of code.

**Why not use `openat(dirfd, …, O_NOFOLLOW)`?** The `pathlib` / `os` stdlib surface is O_NOFOLLOW-only; `openat` is available via `os.open(path, flags, dir_fd=dirfd)` but pathlib doesn't expose it cleanly. O_NOFOLLOW + fstat covers the symlink replacement race adequately without adding a second stdlib affordance. If Phase 2 introduces a hostile-neighbor-uid threat model, upgrade path is openat with dir_fd pinned to the sovereignty/ parent dirfd opened once at boot.

---

## 4. Mechanism implementations

### 4.1 M1 — RFA dual-hash (uses BT1)

**Requirement (architecture):** every RFA is dual-hashed at ingest (`url_hash` + `content_hash`); before drafting, the RFA is re-fetched and re-hashed; change → halt + diff surface.

**Implementation (Section 1):**

Ingest path, `rfa_envelope.ingest_rfa`:
1. Compute `url_hash = sha3_512(url.encode("utf-8"))`.
2. Generate `nonce = secrets.token_bytes(32)`.
3. Compute `content_hash = sha3_512(content_bytes || nonce)`.
4. Write the RFA content to `rfa/{rfa_id}.raw` (canonical path within the org's session root).
5. `stat` the file to capture `st_ino`, `st_dev`, `st_size`. Record in the envelope.
6. Serialize `RFAEnvelope` to `envelopes/rfa/{rfa_id}.json`.
7. Append an audit entry to a per-org `rfa_audit.jsonl` with the envelope hash + operator_id + UTC timestamp.

Re-verify path, `rfa_envelope.reverify_rfa` (v2 — also re-hashes the URL):
1. Re-`stat` the canonical path; compare `(st_dev, st_ino, st_size)` against the envelope. Any mismatch → `RFADriftError("rfa_inode_changed" | "rfa_device_changed" | "rfa_size_changed")`.
2. Re-read content bytes.
3. Recompute `content_hash = sha3_512(content_bytes || envelope.hashes.nonce_hex_decoded)`. Compare against `envelope.hashes.content_hash` — any mismatch → `RFADriftError("rfa_content_hash_mismatch")`.
4. **v2 — recompute `url_hash = sha3_512(envelope.url_at_ingest.encode("utf-8"))`** and compare against `envelope.hashes.url_hash`. Mismatch → `RFADriftError("rfa_url_hash_mismatch")`. v1 did not re-verify the URL; Red Team [LOW] flagged that the envelope's URL could be mutated on disk without detection. Section 1 is not re-fetching the URL — that remains Scout's responsibility — but it IS confirming that the URL stored in the envelope has not been tampered with post-ingest.

**BT1 specifics:**
- Algorithm: SHA-3-512 (`hashlib.sha3_512`). Chosen over SHA-256 because (a) it is a different internal construction (Keccak, not Merkle-Damgård) so a theoretical future break of SHA-2 does not propagate; (b) 64-byte digest gives comfortable collision-resistance margin for the pipeline's expected lifetime; (c) Python 3.11 stdlib supports it natively — no third-party cryptography needed for hashing.
- Nonce size: 32 bytes from `secrets.token_bytes(32)`. OS-level CSPRNG on macOS (`/dev/urandom` via `getentropy(2)`).
- Nonce placement: concatenated *after* content bytes (`content_bytes || nonce`), not interleaved. Keeps `content_hash` verifiable without any per-RFA reconstruction logic — just read bytes, read nonce, feed both to SHA-3-512.
- Nonce lifetime: per-RFA, generated once at ingest, retained in the envelope for the life of the session. Discarded when the envelope is rotated (operator-triggered RFA refresh produces a new envelope with a new nonce).
- Nonce discarded at session end is NOT required by M1 — nonces are public-enough that their disclosure does not aid an attacker; they exist to prevent *pre-image construction* not to hide content.

**Why nonce in content_hash closes the adversarial pre-image construction surface:** without a nonce, an attacker who knows SHA-3-512 can precompute a tampered RFA whose digest collides with a legitimate target and swap the file on disk between ingest and re-verify. With a 32-byte random nonce that is generated *after* the attacker commits to their candidate, the attacker must find a collision against a value they cannot see — reducing the attack to breaking SHA-3-512 itself.

### 4.2 M2 — PROJECT_CONTEXT envelope + session binding

**Requirement:** Session binds to org-root hash at start; PROJECT_CONTEXT.md hash must match bound org; mismatch → hard abort. Paths canonicalized; symlinks/traversal rejected. Cached datasets carry no org identifiers.

**Implementation (v2 — seal is fully atomic within a per-slug lock):**

`project_context_envelope.seal_project_context(slug, session_id, expected_session_bound_slug)`:
1. Open/create `sovereignty/envelopes/project_context/{slug}.json.lock` and acquire `fcntl.LOCK_EX` (blocking). This lock gates the entire seal+bind window; it is held across the read, hash, write, and rename so no attacker-initiated swap can land between the check and the rename.
2. `canonical_path = Path("orgs", slug, "PROJECT_CONTEXT.md").resolve(strict=True)`. `strict=True` raises `FileNotFoundError` if the path does not exist — fail-closed.
3. Assert `canonical_path` is within `(repo_root / "orgs" / slug).resolve()` via `Path.is_relative_to`. If not → `OrgRootEscape("project_context_escape")`.
4. Reject if any parent component is a symlink to outside the org root. `isolation.within_org_root` is the predicate.
5. Generate nonce; open the file via `os.open(path, O_RDONLY | O_NOFOLLOW | O_CLOEXEC)`. Re-stat the opened fd via `os.fstat(fd)` and confirm `(st_dev, st_ino)` still under the expected org root (BT2 post-open re-stat, v2). Read bytes, compute `content_hash = sha3_512(bytes || nonce)`, close fd.
6. **Slug equality check inside the locked critical section:** if `expected_session_bound_slug is not None and expected_session_bound_slug != slug`, raise `SessionSlugMismatch` (prevents a mid-session seal from silently targeting a different org).
7. Snapshot `(st_dev, st_ino)` from step 5's fstat; build `PROJECTContextEnvelope`.
8. Write to `envelopes/project_context/{slug}.json.tmp.{random}`, `fsync`, `os.rename` to `envelopes/project_context/{slug}.json`. Rename atomic (same-filesystem pre-check per M6 cross-fs guard).
9. Release the fcntl lock. Any attempt to seal the same slug from another process must block on the same lock and repeat steps 2–8 afresh; it cannot observe a half-written envelope.
10. Mid-session re-read (called by Logician via Section 4) acquires the same per-slug lock in shared mode (`fcntl.LOCK_SH`), re-stats and re-hashes; mismatch → `ProjectContextDrift`.

**Why the lock:** v1 performed the slug-equality check before the atomic rename, opening a TOCTOU window where an attacker with write access to `envelopes/project_context/` could swap the sealed envelope between check and use. v2 wraps the entire seal in a per-slug exclusive lock so the check is always consistent with the final on-disk state. The lock adds no contention in the single-operator model; it is defensive for the multi-process (signal handler + main thread) case.

**Session binding:**
- `start_session(slug, ...)` requires `rfa.session_bound_slug == project_context.slug` AND passes `expected_session_bound_slug=slug` to `seal_project_context`. Any mismatch is a Law 3 violation.
- The active session lock holds the slug. A second call to `start_session` during an active session raises `SessionAlreadyActive` regardless of requested slug.
- Cross-org work requires `end_session` + `start_session`. No "switch org" operation exists.

### 4.3 M3 — Org slug canonicalization

**Requirement (implicit from Law 3 + architectural mention):** org slugs must canonicalize deterministically so path-level isolation cannot be evaded by slug-case tricks or Unicode homoglyphs.

**Implementation:**

`org_slug.canonical_slug(s)` (v2 — hardens against whitespace padding and lossy transliteration):
1. Reject non-string input with `TypeError` (defensive).
2. `s = s.strip()` — **v2 FIX:** strip surrounding whitespace BEFORE any other check. v1 omitted this, allowing `" .git "` to bypass the reserved-name table.
3. Reject empty after strip → `InvalidSlug("empty")`.
4. `s_nfc = unicodedata.normalize("NFC", s)`.
5. `s_ascii_raw = unicodedata.normalize("NFKD", s_nfc).encode("ascii", "ignore").decode("ascii")`.
6. **v2 FIX — lossy-transliteration rejection:** compute the count of characters dropped during ASCII encode. If the post-NFKD string contains any non-ASCII codepoints AND the post-encode string is shorter than the pre-encode stripped-of-combining-marks string, raise `InvalidSlug("transliteration_lossy", original=s, transliterated=s_ascii_raw)`. This catches `"café" → "cafe"` and prevents distinct org names collapsing to the same slug. Operators who deliberately want a transliterated slug pass an already-Latinized name.
7. `s_lower = s_ascii_raw.lower()`.
8. Replace runs of non-`[a-z0-9]` with a single `-`.
9. Strip leading/trailing `-`.
10. Reject empty result → `InvalidSlug("all_non_alphanum")`.
11. Reject length > 64 chars → `InvalidSlug("too_long")`.
12. Reject reserved names (post-strip-and-normalize, so the whitespace-padded `.git` hits this): `{".", "..", "index", "shared", "vault_shared", "_template", ".git", ".well_known"}` → `ReservedSlug`.

Examples: `"MycoSymbiotics Cooperative"` → `"mycosymbiotics-cooperative"`; `"FIT Farms, Inc."` → `"fit-farms-inc"`; `"Run-a-Muck!"` → `"run-a-muck"`; `"mycosymbiotics_cooperative"` → `"mycosymbiotics-cooperative"` (underscore is non-`[a-z0-9]`, collapsed to dash).

v2 rejects: `" .git "` → `ReservedSlug` (was silently accepted as `".git"` directory in v1 per Red Team finding). `"café"` → `InvalidSlug("transliteration_lossy")` (was silently mapped to `"cafe"` in v1).

`ensure_slug_available(slug, repo_root)` stats `repo_root / "orgs" / slug`; if it exists and the session has not declared it as its bound slug, raises `SlugCollisionError`. Used at org-init time, not at session start.

### 4.4 M5 — Router-integrity runtime invariant (uses BT4, BT6)

**Requirement:** `router.yaml` is git-tracked with signed commits on operator's keyring; Logician verifies signature at pipeline start; unsigned/tampered → hard abort. Cross-family rigor invariant re-checked on every fallback.

**Implementation:**

`router_integrity.verify_router_integrity(repo_root, keystore)`:
1. `router_yaml = (repo_root / "router.yaml").read_bytes()`.
2. Canonicalize: strip trailing whitespace per line, normalize line endings to `\n`, strip BOM. YAML loaded and re-serialized via `yaml.safe_dump(yaml.safe_load(router_yaml), sort_keys=True)`. This prevents whitespace-only attacks where the bytes differ but the parsed content is identical.
3. Compute `router_yaml_sha = sha3_512(canonical_bytes)`.
4. Load the operator's router-signing key via `keystore.retrieve("router.signing.hmac.v1")`. This key was provisioned at operator-onboarding time (see Section 9.2 boot sequence step 5).
5. Read `router.yaml.sig` (HMAC-SHA3-512 signature file, plaintext hex). If absent → `RouterIntegrityError("signature_missing")`.
6. Compute expected signature = `hmac_sha3_512(router_signing_key, router_yaml_sha || commit_sha)` where `commit_sha` comes from `git rev-parse HEAD`. If not a git repo or git unavailable, `RouterIntegrityError("git_unavailable")`. Single-operator v0.1 assumes git is present.
7. `hmac.compare_digest` against the stored sig. Mismatch → `RouterIntegrityError("signature_mismatch")`.
8. Write the `RouterManifest` into `router/manifest.{session_id}.json` and return it.

**Why HMAC-SHA3-512 and not Ed25519 SSH-signed commits for v0.1:** the sovereignty promise is single-operator-single-machine. The operator signs router.yaml on the same machine where they run Tilth. HMAC with a keychain-stored key gives them integrity-against-tamper without requiring a second credential (SSH key) with its own provisioning story. Ed25519 detached signatures remain an option for Phase 2+ where multi-operator signing, revocation, and key transparency become meaningful. Documented as future work in `/USER.md`.

**Cross-family runtime invariant (M5 runtime check):** exported as `router_integrity.assert_cross_family(author_family, reviewer_family)`. Raises `CrossFamilyViolation` if author_family == reviewer_family. Section 5 (Pipeline) calls this on every seat dispatch; Section 1 provides the predicate.

### 4.5 M6 — Atomic flush + INTERRUPTED state

**Requirement:** SIGTERM/SIGINT/crash handlers persist partial state with `status=INTERRUPTED` before exit. Atomic flush. Subsequent runs detect INTERRUPTED and resume-or-discard per operator policy.

**Implementation (v2 — single combined atomic write, cross-filesystem guard, zero-first ordering):**

`interrupted_state.checkpoint(session, payload)` — v2 rewrites BOTH the session status AND the interrupted payload into ONE combined JSON object via ONE `tmp → rename`:

1. Build combined object:
   ```json
   {
     "session_id": "<uuid>",
     "slug": "...",
     "started_at": "...",
     "hmac_key_id": "...",
     "router_manifest_sha": "...",
     "pid": 1234,
     "status": "INTERRUPTED",
     "interrupted_at": "<UTC ISO-8601>",
     "interrupted_payload": { ...canonical-JSON payload... }
   }
   ```
2. Serialize canonical JSON to `bytes_to_write`.
3. `tmp_path = session_path + ".tmp.{random}"`. (Where `session_path` is the SINGLE file `sovereignty/sessions/{uuid}.json` — v2 consolidates the former two files.)
4. **v3 cross-filesystem guard — double-check pattern (closes Red Team v2 MEDIUM-2 TOCTOU):** the boot-time `st_dev` check is necessary but NOT sufficient — an operator could remount a mount point between boot and checkpoint, or the temp file's backing store could be on a different filesystem than the final destination even if parents appear equal. v3 checks `st_dev` TWICE:
   - **Check A (pre-creation):** before `os.open(tmp_path, O_CREAT)`, `os.stat(tmp_parent).st_dev` must equal `os.stat(final_parent).st_dev` (unchanged from v2).
   - **Check B (post-creation, pre-rename):** after the tmp file has been written + fsynced and immediately BEFORE `os.rename`, re-check `os.fstat(tmp_fd).st_dev == os.stat(final_parent).st_dev`. If these diverge — e.g., because a concurrent remount moved one of the parents onto a different filesystem between Check A and this point — raise `CrossFilesystemRename` and unlink the tmp file. Fail-closed: a rename across filesystems on Linux returns EXDEV and would leave stale tmp + no target; we refuse the operation rather than fall back to copy+unlink, which is NOT atomic.
5. `fd = os.open(tmp_path, O_CREAT | O_WRONLY | O_TRUNC, 0o600)`; `os.write(fd, bytes_to_write)`; `os.fsync(fd)`; perform Check B on `fd` (fstat) + `final_parent` (stat) before close; `os.close(fd)`.
6. `os.rename(tmp_path, final_session_path)`. Atomic within the same FS; POSIX guarantees observers see either the old file OR the new file, never a half-written intermediate.

**v2 note on the schema change:** v1 kept status in `sessions/{uuid}.json` and the payload in `sessions/{uuid}.interrupted.json`, and the signal handler wrote both in sequence, creating the Red Team-flagged race where a signal mid-handler could leave `status=INTERRUPTED` with no payload. v2 collapses the two into one file so the status and the payload are promoted or rolled back atomically. `Session` on-disk schema gains the optional `interrupted_payload` field (see §2.4).

Signal plumbing in `session.start_session` (v3 — unified handler with one-shot `_shutting_down` flag closes Red Team v2 LOW-2 signal-handler reentrance; v4 — non-blocking checkpoint lock closes RT-v3 LOW-1 handler-deadlock):

```python
# session.py — v3 + v4
_shutting_down = threading.Event()  # module-level; atomic across threads
_checkpoint_lock = threading.Lock()

def _unified_signal_handler(signum: int, frame) -> None:
    # Check-and-set in one atomic step. If already shutting down, the second signal is a no-op.
    if _shutting_down.is_set():
        return
    _shutting_down.set()
    # Arm 5 s watchdog BEFORE any I/O so a hang in step 1 still exits.
    signal.alarm(5)
    try:
        # Step 1 — zero the in-memory HMAC key bytearray FIRST (v2 ordering preserved).
        if session._hmac_key_buffer is not None:
            zero_bytes(session._hmac_key_buffer)
        # Step 2 — v4: NON-BLOCKING try-acquire. If the checkpoint thread holds
        # the lock and is blocked on I/O, do NOT wait — skip checkpoint rather
        # than deadlock the handler. Closes RT-v3 LOW-1.
        acquired = _checkpoint_lock.acquire(blocking=False)
        if acquired:
            try:
                if session._last_checkpoint_state is not None:
                    checkpoint(session, session._last_checkpoint_state)
            finally:
                _checkpoint_lock.release()
        else:
            # Checkpoint thread is mid-write; trust its work and skip ours.
            # The ledger-based state-of-truth (§5.3 v3 read-through cache)
            # means a lost checkpoint is bounded-recoverable on next boot.
            pass
        # Step 3 — best-effort zero the keystore entry.
        try:
            resolve_keystore().zero(session.hmac_key_id)
        except Exception:
            pass  # keystore may already be torn down; sweep catches it next boot
    finally:
        if signum == signal.SIGINT:
            os._exit(130)
        else:
            os._exit(143)

signal.signal(signal.SIGTERM, _unified_signal_handler)
signal.signal(signal.SIGINT, _unified_signal_handler)
signal.siginterrupt(signal.SIGTERM, False)
signal.siginterrupt(signal.SIGINT, False)
```

**v3 + v4 ordering properties:**
1. **One-shot.** `_shutting_down` is a `threading.Event`; `is_set()` + `set()` is atomic. A second SIGTERM or SIGINT arriving while the handler is running returns immediately without re-entering. Closes Red Team v2 LOW-2.
2. **Zero key first.** Same v2 ordering — the HMAC key bytearray is zeroed before any I/O that could block or fail. An attacker snapshotting core between signal and exit gets nothing.
3. **Non-blocking checkpoint under lock (v4).** `_checkpoint_lock.acquire(blocking=False)` prevents the periodic checkpoint thread and the signal handler from racing AND guarantees the signal handler never deadlocks waiting for a blocked checkpoint thread. If the lock is held, the handler skips its own checkpoint write — the periodic thread either completed or will be terminated with the process. The ledger is the source of truth (§5.3 v3), so a lost final checkpoint is bounded-recoverable. Closes RT-v3 LOW-1.
4. **Best-effort keystore zero.** Keychain delete / FileKeyStore overwrite+unlink are attempted but not mandatory; the boot-time orphan-key sweep (§9 step 8) catches any leaked keys whose owning session is no longer ACTIVE.
5. **Watchdog.** `signal.alarm(5)` armed inside the handler caps worst-case handler time at 5 s. If any step hangs, SIGALRM terminates the process; the orphan-key sweep and watermark regression detection at next boot ensure no stale state survives.

- During LLM-active phases, a separate thread writes a checkpoint every 30 seconds. The 30-second interval is chosen so that worst-case data loss on crash is bounded at 30 seconds of LLM conversation — much cheaper to regenerate than to risk corrupting the ledger.

`interrupted_state.detect_interrupted(repo_root)`:
- Scans `sovereignty/sessions/` for any `Session` records with `status == "INTERRUPTED"`.
- Returns the newest such session (sorted by `started_at`).
- Returns `None` if none exist.

`interrupted_state.resume_or_discard(session, policy)`:
- `policy == "resume"`: load the payload, validate it against the session's bound RFA envelope and PROJECT_CONTEXT envelope (hashes must still match), and return the payload. If validation fails → `InterruptedStateInvalid`; operator must discard.
- `policy == "discard"`: mark session `status = "ENDED_CLEAN"` via the tmp+rename pattern, delete the payload file, return `None`.
- `policy == "prompt"`: raise `OperatorDecisionRequired` — the CLI caller (Section 5) handles the prompt; Section 1 does not interact with stdin.

### 4.6 M7 — Per-session HMAC key (uses BT6)

**Requirement:** Scout's health-tuple is signed with a per-session HMAC derived from a Logician-issued session key. Scout does not self-attest. Session key must rotate, revoke cleanly, and never persist past session termination.

**v2 implementation — resolves Red Team HIGH on immutable-bytes zeroing:**

**The Python-semantic problem v1 missed.** Python `bytes` is immutable: `zero_bytes(key)` where `key: bytes` CANNOT modify the original buffer. The best a function can do is replace the local-variable reference with a zero-filled `bytes` object — the original key bytes live on in the heap until CPython's garbage collector gets around to them, potentially indefinitely if the buffer is interned or referenced elsewhere. v1's `sign_health_tuple` therefore leaked session HMAC keys into process memory for the entire session lifetime. Red Team flagged this as [HIGH] and the finding is correct.

**The fix — mutable buffers end-to-end.** v2 introduces a `SecretBytes` context manager built on `bytearray` + `memoryview`:

```python
# crypto_primitives.py
class SecretBytes:
    """Mutable secret buffer. Zeros in-place on __exit__ or on explicit zero()."""
    __slots__ = ("_buf", "_view", "_zeroed")

    def __init__(self, data: bytes | bytearray | memoryview):
        if isinstance(data, bytes):
            # Defensive: callers should pass bytearray; we copy once here to get
            # a mutable backing store. The original bytes remain in CPython heap
            # for the lifetime of whatever created them (caller's responsibility),
            # but SecretBytes itself will be zero-able.
            self._buf = bytearray(data)
        elif isinstance(data, bytearray):
            self._buf = data
        else:  # memoryview
            self._buf = bytearray(data.tobytes())
        self._view = memoryview(self._buf)
        self._zeroed = False

    def view(self) -> memoryview:
        if self._zeroed:
            raise ZeroizedBufferAccessed("SecretBytes already zeroed")
        return self._view

    def zero(self) -> None:
        if self._zeroed:
            return
        for i in range(len(self._buf)):
            self._buf[i] = 0
        self._zeroed = True

    def __enter__(self) -> "SecretBytes":
        return self

    def __exit__(self, *_: object) -> None:
        self.zero()


def zero_bytes(buf: bytearray | memoryview) -> None:
    """Zero a mutable buffer in place. Rejects immutable `bytes` with TypeError.

    The TypeError rejection is a CONTRACT — it surfaces accidental calls with
    immutable buffers at the test boundary, not silently at runtime.
    """
    if isinstance(buf, bytes):
        raise TypeError(
            "zero_bytes() requires a mutable buffer (bytearray or memoryview); "
            "got immutable bytes. Use SecretBytes or bytearray from the start."
        )
    if isinstance(buf, memoryview):
        if buf.readonly:
            raise TypeError("zero_bytes() rejects readonly memoryview")
        buf[:] = b"\x00" * len(buf)
        return
    # bytearray
    for i in range(len(buf)):
        buf[i] = 0
```

`KeyStore.retrieve(key_id)` (v2 contract) returns `bytearray` — never `bytes`. See §3.11.

`session.start_session` step N+1 (after RFA + PROJECT_CONTEXT bound):
1. `hmac_key = bytearray(secrets.token_bytes(64))`. 64 bytes is below SHA-3-512's 72-byte block size, avoiding the hash-the-key preprocessing HMAC does for overlong keys; 512 bits of entropy, well above the 256-bit working minimum.
2. `hmac_key_id = f"tilth.session.{session_id}.hmac.v1"`.
3. `keystore.store(key_id=hmac_key_id, key_bytes=hmac_key, purpose="session_hmac")`.
4. `zero_bytes(hmac_key)` — scrubs the local bytearray in place (v2 contract). The bytes that were copied into the keystore live inside the keystore's own buffer; callers do not retain the plaintext.
5. `session.hmac_key_id = hmac_key_id` (the ID, not the bytes).

Callers (Section 3's Scout) request signing via a narrow API (v2):

```python
def sign_health_tuple(session: Session, tuple_bytes: bytes) -> bytes:
    with resolve_keystore().retrieve_secret(session.hmac_key_id) as key:
        # key is a SecretBytes; hmac_sha3_512 reads its memoryview.
        # The `with` block zeroes the underlying bytearray on exit, even on exception.
        return hmac_sha3_512(key.view(), tuple_bytes)
```

`hmac_sha3_512(key: memoryview, data: bytes) -> bytes` — v2 accepts `memoryview` to keep the key in the mutable-buffer path all the way into `hmac.new()`. Python's `hmac.new` accepts `bytes`-like (including `memoryview`), so this is wire-compatible.

`session.rotate_hmac_key(session)` (v2):
- Generates a new bytearray key, stores it under a v2/v3/... id, and marks the old id for deletion after a **5-second grace window** (v2 reduced from v1's 60 s, per Red Team [MEDIUM]). A short-lived `threading.Timer(5.0, self._zero_old_key)` schedules the deletion; the callback calls `keystore.zero(old_key_id)` and logs a `degradation.jsonl` `rotation_grace_complete` event (informational, not `signed_by_operator`).
- 5 s is long enough for any in-flight signing call to complete (the Scout health-tuple signing path is synchronous and submits in <100 ms on the M1) and short enough that an attacker who captures the old key has a tight window.
- If the process exits during the grace window, the orphan-key sweep at next boot catches the old id because its matching session is no longer ACTIVE.

`session.end_session`:
1. `keystore.zero(session.hmac_key_id)`. On Keychain, this deletes the item; on FileKeyStore, this overwrites the encrypted key file with zeros and unlinks.
2. Any active rotation grace timer is cancelled and the old key id is zeroed immediately.
3. Mark session `ENDED_CLEAN`.
4. Any in-process SecretBytes copies have already zeroed themselves via `__exit__`.

**v2 crash-time behavior:** the SIGTERM handler's FIRST instruction zeroes the in-memory key buffer (see §4.5 v2 handler ordering). If the process segfaults between bytearray allocation and handler registration — a vanishingly small window — the orphan-key sweep at next boot catches the keystore entry. The sweep moved in the boot sequence to run BEFORE INTERRUPTED-session detection (v2 §9), closing the Red Team [MEDIUM] "orphan-key sweep window" finding: a crash-triggered INTERRUPTED state no longer leaves a live key in the keystore waiting for operator decision.

### 4.7 M10 — Graceful degradation recording (author seats, 30-min threshold)

**Requirement:** Author seats (Scout, Scribe, Editor) may degrade after 30 minutes of full family outage, with explicit operator alert + audit-log breach entry. Review seats do not degrade — they hard-abort (or invoke M13).

**Implementation (the recording part only — Section 5 owns the detection logic):**

`degradation_log.record_degradation` accepts `event_kind="author_seat_degraded_run"` and writes a `DegradationEvent` with `signed_by_operator=False`. Section 5's Pipeline layer is responsible for:
- Detecting the 30-minute threshold.
- Selecting the cross-family compliant fallback.
- Presenting the operator alert.
- Calling `record_degradation` exactly once per degraded-run event.

Section 1's contract: every `record_degradation` call is durable, hash-chained, and appears in the rails report once Section 4 signs the report. No in-place mutation.

**Concrete number:** 30 minutes = 1800 seconds. The threshold lives as a module-level constant `M10_AUTHOR_SEAT_DEGRADATION_THRESHOLD_SECONDS = 1800` in `session.py` and is read by Section 5. Changing it is an architecture-level decision, not a Section 5 config — a comment on the constant says so.

### 4.8 M13 — Review-seat outage escape-valve recording

**Requirement:** All compliant review-seat families FAILED for >24h (default, operator-configurable to 72h max). Operator issues signed bypass authorization; authorization is a RED-severity admin-risk ledger entry requiring re-type confirmation. Draft carries rigor-breach flag. No auto-renewal.

**Implementation (Section 1 — recording, not decision; v2 adds monotonic-clock protection against wall-clock drift):**

An M13 authorization is a two-record write:

1. **AdminRiskEntry** (`entry_kind="review_seat_bypass"`, `severity="RED"`):
   - `payload_json` carries `{seat, outage_start_utc, bypass_expiry_utc, bypass_expiry_monotonic_ns, attestation}`.
   - `operator_retype_hash` required — the caller (Section 5) collected the operator's re-typed attestation string and HMACs it against the operator's signing key. Section 1 does not prompt the operator; it enforces that the hash is present before accepting the entry.
   - **v2 — monotonic timestamp pair:** `issued_monotonic_ns = time.monotonic_ns()` is written into the AdminRiskEntry at append time (schema §2.5). `bypass_expiry_monotonic_ns = issued_monotonic_ns + duration_hours * 3600 * 10**9`. The M13 ceiling is enforced against the monotonic pair: `record_admin_risk` rejects any entry where `bypass_expiry_monotonic_ns - issued_monotonic_ns > M13_BYPASS_CEILING_HOURS * 3600 * 10**9`. Wall-clock values are still recorded for human-readable audit trails, but the CEILING check does not trust them.
   - Rate-limit BT3 applies: no more than 10 RED entries per operator per 24h. The 10-RED cap is deliberately generous for M13 (three bypasses a day is already an incident) but not so generous that a compromised machine can spam the ledger.

2. **DegradationEvent** (`event_kind="review_seat_bypass_active"`):
   - `authorization_id` = the `AdminRiskEntry.seq_id` from step 1.
   - `signed_by_operator=True`.
   - `expires_at` = `bypass_expiry_utc` (wall clock, for display).
   - `expires_monotonic_ns` = `bypass_expiry_monotonic_ns` (authoritative ceiling check).

**v2/v3 — bypass-active check (Section 5 will call this, Section 1 provides the predicate):**

```python
def bypass_is_active(
    event: DegradationEvent,
    now_utc: datetime,
    now_mono_ns: int,
    boot_clock_history: list[BootClockRecord],
) -> bool:
    if event.event_kind != "review_seat_bypass_active":
        return False

    # v2 — dual clock primary gate.
    wall_ok = event.expires_at is None or now_utc < isoparse(event.expires_at)
    mono_ok = event.expires_monotonic_ns is None or now_mono_ns < event.expires_monotonic_ns
    if not (wall_ok and mono_ok):
        return False

    # v3 — clock-rollback detection via boot_clock_history.
    # If ANY boot in history has wall-clock GREATER than now_utc (plus tolerance),
    # the wall clock has been rolled backwards. Reject and require re-issuance.
    max_wall_in_history = max(
        (isoparse(r.wall_at_boot_utc) for r in boot_clock_history), default=None
    )
    if max_wall_in_history is not None:
        if now_utc + timedelta(seconds=CLOCK_ROLLBACK_TOLERANCE_SECONDS) < max_wall_in_history:
            # Clock has been rolled back more than the NTP slop tolerance (5 min).
            # The bypass may be outside its intended window but wall_ok reads True
            # because wall clock is behind. Fail closed.
            raise BypassClockRollbackDetected(
                now_utc=now_utc,
                max_wall_in_history=max_wall_in_history,
                remediation=(
                    "System wall clock is behind the most recent recorded boot. "
                    "A clock-rollback attack or NTP malfunction is indicated. "
                    "The bypass window cannot be trusted. Operator must correct "
                    "the system clock and re-issue the bypass via the M13 "
                    "ceremony in docs/admin_risk_ceremony.md. This is F-ADM-09."
                ),
            )

    # v3 — also reject if the bypass was issued before the most recent system boot
    # AND the monotonic reset means we cannot locally verify it hasn't been
    # replayed across a restart. If the issuance's `boot_epoch_ns` does not match
    # ANY entry in boot_clock_history, the issuance is orphaned — the process that
    # wrote it is gone. Safer to reject than to trust a monotonic from a dead
    # process.
    issuance_boot_epoch = event.boot_epoch_ns_at_issuance
    if issuance_boot_epoch is not None:
        known_epochs = {r.boot_epoch_ns for r in boot_clock_history}
        if issuance_boot_epoch not in known_epochs:
            raise BypassClockRollbackDetected(
                now_utc=now_utc,
                max_wall_in_history=max_wall_in_history,
                remediation=(
                    "Bypass was issued under a boot_epoch that does not appear in "
                    "boot_clock_history. The machine has rebooted since issuance, "
                    "so the monotonic guard is reset. Operator must re-issue. F-ADM-09."
                ),
            )

    return True
```

The dual-clock v2 check plus the v3 boot_clock_history rollback-oracle closes Red Team v2 [HIGH-2] "M13 bypass extension via wall-clock rollback":

- **Wall-clock forward jump** → `wall_ok` flips False → bypass expires. (v2 closure, unchanged.)
- **Wall-clock backward jump** (without process restart) → monotonic still progresses; `mono_ok` flips False at the original expiry in monotonic time. (v2 closure, unchanged.)
- **v3 — wall-clock backward jump WITH process restart** → monotonic resets to zero; `mono_ok` stays True because `event.expires_monotonic_ns` was computed relative to old boot's monotonic-zero. BUT `boot_clock_history` retains the old boot's `wall_at_boot_utc`, which is now GREATER than `now_utc`. Rollback is detected, `BypassClockRollbackDetected` is raised. Closed.
- **v3 — issuance from a dead boot** (attacker preserves the ledger entries across a reboot attempting replay) → `issuance_boot_epoch` does not match the current boot's entry in `boot_clock_history`. Rejected; operator must re-issue. Closed.

**What `time.monotonic_ns` is and is not.** Python's `time.monotonic_ns` is a process-start-anchored counter that cannot be set by user-space and increases at real-time rate. It survives wall-clock jumps in either direction. It does NOT survive process restart — each new Tilth process starts at its own monotonic-zero. v2 noted this gap; v3 closes it via `boot_clock_history` which persists a tamper-evident record of `(boot_epoch_ns, wall_at_boot_utc)` pairs across reboots.

**`boot_clock_history.jsonl` — tamper-evident wall-clock progression log:**

- Path: `sovereignty/clock/boot_clock_history.jsonl`.
- Each line is a JSON object: `{"boot_epoch_ns": int, "wall_at_boot_utc": "ISO-8601Z", "recorded_at_utc": "ISO-8601Z", "prev_hash": "…", "entry_hash": "…"}`.
- Appended once per `boot.boot_envelope()` call (step 2.5 of the boot sequence, §9).
- `boot_epoch_ns` is read from the OS kernel: `sysctl kern.boottime` (macOS) or `/proc/stat` `btime` (Linux). This is a kernel-level monotonic-ish value that changes only on reboot.
- Each line carries its own `prev_hash` + `entry_hash` chain (same discipline as `admin_risk.jsonl`).
- Has its own `.hmac` trailer (rolling SHA-3-512 over the full file contents, keyed by `tilth.clock.boot_history.hmac.v1`). Shares the watermark-file mechanism from §5.6 BT8.
- Verified at every boot BEFORE any M13 `bypass_is_active` call: `verify_boot_clock_history_chain()` walks the file and confirms `wall_at_boot_utc` is non-decreasing across entries (with NTP-slop tolerance `CLOCK_ROLLBACK_TOLERANCE_SECONDS = 300` seconds). Violation → hard abort at boot — the machine has been time-tampered.

**v4 — atomic append discipline (closes RT-v3 MED-2 "Boot-clock-history atomic append race"):** The append path holds `fcntl.LOCK_EX` on `clock/boot_clock_history.lock` for the ENTIRE sequence of (a) write new line to jsonl, (b) fsync jsonl, (c) recompute rolling HMAC over full file, (d) write trailer, (e) fsync trailer, (f) fsync parent directory. The lock is never released between steps. Pseudocode:

```python
def append_boot_clock_record(record: BootClockRecord) -> None:
    # v4 — single-held-lock atomic append. No window exists between the data
    # write and the HMAC recompute where a concurrent writer could interpose.
    lock_path = clock_dir() / "boot_clock_history.lock"
    with acquire_fcntl_exclusive(lock_path) as lock_fd:
        # (a) Append the new line.
        line_bytes = canonical_json_bytes(record) + b"\n"
        with open(jsonl_path, "ab") as f:
            f.write(line_bytes)
            f.flush()
            os.fsync(f.fileno())
        # (b) Recompute rolling HMAC over the FULL file (not just the delta —
        #     this matters if the file was concurrently read between write and
        #     HMAC; we always HMAC the durable state).
        with resolve_keystore().retrieve("tilth.clock.boot_history.hmac.v1") as key:
            full_hmac = hmac_sha3_512_file(key.view(), jsonl_path).hex()
        # (c) Write trailer atomically (tmp → rename) and fsync parent.
        atomic_write_boot_clock_trailer(
            BootClockTrailer(
                boot_clock_history_hmac=full_hmac,
                last_boot_epoch_ns=record.boot_epoch_ns,
                wall_at_write_utc=iso_utc_now(),
            )
        )
        # fcntl.LOCK_UN happens via the context manager at function exit.
```

**Invariant:** at any process-kill point mid-append, the on-disk state is either (i) pre-append — no new line, no new HMAC, or (ii) post-append-post-HMAC — new line durable AND trailer references it. There is no reachable state where the new line exists without the new HMAC, because the trailer write is the LAST step and the lock is held across the whole sequence. A crash between (a) and (c) is detected by `verify_boot_clock_history_chain()` at the next boot (trailer HMAC will not match the full file) and triggers `F-ADM-09 BootClockHistoryTrailerMismatch` — fail-closed, operator-recovery ceremony.

**Wait — why doesn't this break the "no silent rollback past the ceiling" guarantee?** Because the wall-clock-ceiling check is the AUTHORITATIVE ceiling; the monotonic check is a DEFENSE-IN-DEPTH second opinion. If a naïve attacker rolls the clock backwards and restarts the process, `boot_clock_history` catches the rollback BEFORE any M13 check runs. If a sophisticated attacker also rewrites `boot_clock_history` (requires keystore compromise to rewrite the HMAC trailer), they are operating out-of-model per the trusted-operator threat boundary.

At `expires_at` (whichever clock triggers first, with rollback protection via boot_clock_history), Section 5 must call `record_degradation(event_kind="bypass_expired", ...)` to close the bypass. A renewal is a fresh two-record write — never an update to the existing records.

**BT3 rate-limit interaction:** an attacker who has compromised the operator key but not the Keychain passphrase cannot issue bypasses because `operator_retype_hash` requires the operator's HMAC key plus the freshly-typed attestation string. An attacker with both could issue bypasses up to the 10-per-day RED cap; after that, further attempts fail. ADM-A-002 (the normalization-drift residual) captures the governance concern; Section 1's job is to make the mechanical cap unforgeable.

**Why no auto-renewal:** every renewal is a fresh RED ledger entry with a fresh operator re-type. This forces the operator to touch the keyboard each time and prevents the "I'll just let the bypass roll" drift that ADM-A-002 warns about.

### 4.9a Sovereignty init marker write + verify (v5 — RT-v4 HIGH-1 first-boot reset closure)

Implemented in `audit.py` (verify + canonical JSON) + `boot.py` (write-once orchestration).

**Verify (every boot, step 7c.0):**

```python
# audit.py — called from boot.py step 7c.0 BEFORE any ledger or watermark body is trusted.

def verify_sovereignty_init_marker(
    *, marker_path: Path, hmac_path: Path, keystore: KeyStore,
    key_id: str, ledger_states: dict[str, "LedgerState"],
) -> SovereigntyInitMarker:
    marker_present = marker_path.exists()
    hmac_present = hmac_path.exists()
    all_ledgers_empty = all(state.last_seq_id == 0 for state in ledger_states.values())
    any_watermark_body_present = any(
        state.watermark_body_exists for state in ledger_states.values()
    )

    # Outcome (b): legitimate first boot
    if not marker_present and not hmac_present and all_ledgers_empty \
            and not any_watermark_body_present:
        return None  # caller invokes write_sovereignty_init_marker_first_boot

    # Outcome (c) — fail-closed branches
    if marker_present != hmac_present:
        raise SovereigntyInitMarkerMissing(
            "Marker present without HMAC, or HMAC present without marker. "
            "First-boot-reset attack or partial tamper."
        )  # F-ADM-11
    if not marker_present and not hmac_present:
        # both absent BUT some ledger has entries OR some watermark body exists
        raise SovereigntyInitMarkerMismatch(
            "Init marker absent but ledgers or watermarks non-empty. "
            "First-boot-reset attack detected (RT-v4 HIGH-1)."
        )  # F-ADM-12

    # Outcome (a): verify HMAC
    marker_bytes = marker_path.read_bytes()
    hmac_trailer_bytes = hmac_path.read_bytes()
    trailer = SovereigntyInitMarkerHmacTrailer(**json.loads(hmac_trailer_bytes))
    with keystore.retrieve(key_id) as key:
        expected = hmac.new(key, marker_bytes, "sha3_512").hexdigest()
    if not hmac.compare_digest(expected, trailer.init_hmac):
        raise SovereigntyInitMarkerMismatch(
            "HMAC mismatch — init marker body tampered with or HMAC forged. "
            "RT-v4 HIGH-1 first-boot-reset attempt."
        )  # F-ADM-12
    body = SovereigntyInitMarker(**json.loads(marker_bytes))
    if body.init_version != trailer.init_version:
        raise SovereigntyInitMarkerMismatch(
            "init_version mismatch between marker body and HMAC trailer."
        )  # F-ADM-12
    return body
```

**Write (first boot only, step 7c.0b):**

```python
# boot.py — called ONLY if verify_sovereignty_init_marker returned None.

def _write_sovereignty_init_marker_first_boot(
    *, marker_path: Path, hmac_path: Path, lock_path: Path,
    keystore: KeyStore, key_id: str,
    boot_clock_history_seq: int, boot_epoch_ns: int,
    operator_slug: str | None,
) -> SovereigntyInitMarker:
    lock_fd = safe_open_lock_file(lock_path)  # O_NOFOLLOW + fstat inode check
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        # Double-check neither file exists — race against a concurrent first-boot
        # (only possible under same-uid concurrent Tilth instances, which is out-of-model,
        # but cheap to guard).
        if marker_path.exists() or hmac_path.exists():
            raise SovereigntyInitMarkerAlreadyExists(
                "Race: another first-boot completed between verify and write."
            )
        body = SovereigntyInitMarker(
            init_version=1,
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            hostname=platform.node(),
            operator_slug=operator_slug,
            boot_epoch_ns_first=boot_epoch_ns,
            boot_clock_history_seq_at_init=boot_clock_history_seq,
        )
        body_json = canonical_json(asdict(body))  # sorted, ascii-only, no whitespace
        body_bytes = body_json.encode("utf-8")

        with keystore.retrieve(key_id) as key:
            hmac_hex = hmac.new(key, body_bytes, "sha3_512").hexdigest()

        trailer = SovereigntyInitMarkerHmacTrailer(
            init_version=1,
            init_hmac=hmac_hex,
            wall_at_write_utc=datetime.now(timezone.utc).isoformat(),
        )
        trailer_bytes = canonical_json(asdict(trailer)).encode("utf-8")

        # tmp→rename discipline — same as watermarks
        with tempfile.NamedTemporaryFile(dir=marker_path.parent, delete=False) as tmp_m:
            tmp_m.write(body_bytes)
            tmp_m.flush()
            os.fsync(tmp_m.fileno())
        with tempfile.NamedTemporaryFile(dir=hmac_path.parent, delete=False) as tmp_h:
            tmp_h.write(trailer_bytes)
            tmp_h.flush()
            os.fsync(tmp_h.fileno())
        # Rename body first — if HMAC rename fails, step 7c.0 next boot will
        # see marker_present=True, hmac_present=False → F-ADM-11. Operator
        # then restores from keyring/backup. This is preferable to the reverse
        # ordering which would leave HMAC-present-without-body.
        os.rename(tmp_m.name, marker_path)
        os.rename(tmp_h.name, hmac_path)
        os.fsync(marker_path.parent.open(os.O_RDONLY | os.O_DIRECTORY).fileno() if hasattr(os, "O_DIRECTORY") else ...)
        return body
    finally:
        fcntl.flock(lock_fd, fcntl.LOCK_UN)
        os.close(lock_fd)
```

**Recovery paths:**
- **Marker present, HMAC absent (crash between marker rename and HMAC rename on first boot):** boot fails with `F-ADM-11 SovereigntyInitMarkerMissing`. Operator recovery: wipe both files (they must BOTH be absent for next-boot verify to hit the legitimate-first-boot branch), confirm all ledgers are still empty, restart. Documented as an operator-facing runbook entry in `/ops/runbooks/sovereignty-first-boot-crash.md` (Phase 2 deliverable; v0.1 surfaces the error message with the runbook path).
- **HMAC present, marker absent (never reachable by legitimate path):** `F-ADM-11`. Same recovery.
- **Both present, HMAC mismatch (RT-v4 HIGH-1 attack signature):** `F-ADM-12`. No recovery — this is a tamper signal. Operator must investigate (filesystem forensics, key rotation, re-install). The boot halt is the entire point.
- **Both absent BUT ledgers non-empty or watermarks present (RT-v4 HIGH-1 second attack signature):** `F-ADM-12`. Same operator response: filesystem forensics.

### 4.9 Cross-Section boundary — what Section 1 does NOT do with these records

- Section 1 does not verify that a rigor-breach flag made it into the rails report. That is BT13 (Section 4).
- Section 1 does not detect when all compliant review-seat families are FAILED. That is Section 5 Pipeline's router health watcher.
- Section 1 does not render the breach flag for the operator. That is Section 5's rails-report composer.
- Section 1 does not expose the ledger for seat-level reasoning. Seats read the ledger *tail* via `read_ledger_tail` for operator-facing summaries; they do not consume ledger content as source material for drafts (Law 5 — only trust-root material is citable).

---

## 5. Blueprint-tracked implementations

### 5.1 BT1 — SHA-3-512 with per-RFA nonce

Covered in full under M1 (Section 4.1). Summary:

| Choice | Value | Rationale |
|---|---|---|
| Hash algorithm | SHA-3-512 | Keccak, not Merkle-Damgård; native in Python 3.11 stdlib; 64-byte digest |
| Nonce size | 32 bytes | 256 bits of entropy, from `secrets.token_bytes(32)` |
| Nonce placement | `content_bytes \|\| nonce` | Keeps verification trivial; order documented in the envelope schema |
| Nonce lifetime | Per-RFA, persistent in envelope | Nonces are public-enough to survive disclosure |
| Re-hash trigger | Logician at Section 4 gate, pre-draft | Section 1 provides `reverify_rfa`; Section 4 decides when to call |

### 5.2 BT2 — OS-level namespace isolation + TOCTOU closure

**Problem:** Law 3 demands that a session bound to one org cannot read another org's files even under adversarial symlinks, race conditions, or sloppy absolute paths. Canonical-path resolution alone is not enough because an attacker could swap a file between `realpath` and `open`.

**macOS implementation (v0.1 dev target — Josh's M1 Mac Mini):**

macOS does not have Linux bind-mounts. The architecture's language is "atomic bind-mount **or equivalent**" — for macOS the equivalent is a strict canonical-path + inode-snapshot protocol with every file access wrapped in an `OrgRootNamespace` context manager that binds to a specific `(st_dev, st_ino)` tuple at entry and verifies at every read.

`isolation.OrgRootNamespace`:

```python
class OrgRootNamespace:
    def __init__(self, slug: str, repo_root: Path):
        self.slug = slug
        self.repo_root = repo_root
        self._root_path: Path | None = None
        self._root_dev: int | None = None
        self._root_ino: int | None = None

    def __enter__(self) -> "OrgRootNamespace":
        root = (self.repo_root / "orgs" / self.slug).resolve(strict=True)
        st = root.stat()
        if not stat.S_ISDIR(st.st_mode):
            raise OrgRootEscape(f"not_a_directory:{root}")
        self._root_path = root
        self._root_dev = st.st_dev
        self._root_ino = st.st_ino
        return self

    def within(self, target: Path) -> bool:
        """Return True iff target is inside this namespace and nothing has been swapped."""
        try:
            tgt = target.resolve(strict=True)
        except (FileNotFoundError, RuntimeError):
            return False
        # 1. Must be under root path
        try:
            tgt.relative_to(self._root_path)
        except ValueError:
            return False
        # 2. Root inode must still match — catches swap of orgs/{slug} to a different dir
        current = self._root_path.stat()
        if current.st_dev != self._root_dev or current.st_ino != self._root_ino:
            raise OrgRootEscape("root_inode_swapped")
        # 3. Walk every component; reject if any is a symlink pointing outside root
        for parent in [tgt] + list(tgt.parents):
            if parent == self._root_path:
                break
            if parent.is_symlink():
                link_tgt = (parent.parent / os.readlink(parent)).resolve(strict=True)
                try:
                    link_tgt.relative_to(self._root_path)
                except ValueError:
                    raise OrgRootEscape(f"symlink_escape:{parent}")
        return True
```

All file-reading entry points in Section 1 (RFA envelope, PROJECT_CONTEXT envelope, dossier files via M11 dossier verify) open their files inside an `OrgRootNamespace` and assert `ns.within(path)` before opening. The TOCTOU window between `resolve` and `open` is further narrowed by opening via `os.open(path, O_RDONLY | O_NOFOLLOW | O_CLOEXEC)` — `O_NOFOLLOW` rejects the final component if it is a symlink, closing the last-mile swap.

**v2 — post-open fd-based re-stat (closes Red Team [MEDIUM] BT2 TOCTOU):**

`O_NOFOLLOW` rejects a symlink at the final component but does not protect against a swap between `Path.resolve()` and `os.open()` where the attacker replaces the target with a *different regular file* (or even the same-named file inside a swapped-in org root). v2 adds a fd-based re-stat after open:

```python
def open_within(ns: OrgRootNamespace, path: Path) -> int:
    # Pre-check: canonical-path resolve + namespace containment + inode snapshot.
    if not ns.within(path):
        raise OrgRootEscape(f"pre_open_escape:{path}")
    # Open with O_NOFOLLOW + O_CLOEXEC.
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        # Post-open re-stat: the fd we hold must still descend from the namespace root.
        # fstat the fd itself; its (st_dev, st_ino) must not have mutated mid-swap.
        fd_st = os.fstat(fd)
        # Also walk parents of the *path we opened by* and re-verify root-inode equality.
        # If the attacker swapped the parent directory chain during open(), the final
        # component's (dev, ino) may be legitimate but its parent is no longer under
        # the namespace root we snapshotted at __enter__.
        current_root = os.stat(ns._root_path)
        if (current_root.st_dev, current_root.st_ino) != (ns._root_dev, ns._root_ino):
            os.close(fd)
            raise OrgRootEscape("toctou_post_open_swap")
        # For each ancestor of path up to root, confirm it still exists and its
        # inode has not changed. (Cheap on M1: depth of org tree is small.)
        for parent in path.parents:
            if parent == ns._root_path:
                break
            try:
                p_st = os.stat(parent)
            except OSError:
                os.close(fd)
                raise OrgRootEscape(f"toctou_parent_gone:{parent}")
            # Parent must still be a directory under the namespace root.
            if not stat.S_ISDIR(p_st.st_mode):
                os.close(fd)
                raise OrgRootEscape(f"toctou_parent_not_dir:{parent}")
        return fd
    except OrgRootEscape:
        raise
    except Exception:
        os.close(fd)
        raise
```

Distinct error: `OrgRootEscape("toctou_post_open_swap")` is raised, NOT `FileNotFoundError` or `OSError`. Callers (admin_risk) log a RED admin-risk entry on any `OrgRootEscape`, so the security event is unambiguous and visible in the ledger. This closes Red Team's specific concern that the TOCTOU-triggered `ELOOP` was "indistinguishable from a legitimate file-not-found error, potentially leading the operator to ignore the security event."

**Why fd-fstat is tight:** `os.fstat(fd)` reads the inode metadata THROUGH the open fd, which macOS/Linux guarantee points at the specific inode that was open()ed. An attacker who swaps the path after `open()` cannot change what the fd points at (that would require mutating kernel structures). The remaining residual — attacker swaps a parent directory AFTER we've walked that parent — is bounded by the parent-walk immediately after `fstat` above. On the M1 dev hardware, this walk runs in tens of microseconds; the window for an adversary process to land a `renameat2` between our `os.stat(parent)` and the next iteration is vanishingly small and still within the trusted-operator boundary (which assumes no hostile processes running with our uid).

**macOS-specific notes:**
- `O_NOFOLLOW` only rejects the *final* component being a symlink; the walk above handles parent components.
- macOS APFS supports clones (CoW), not hardlinks to directories; inode swaps within APFS are still detectable by `(st_dev, st_ino)` mismatch.
- `O_CLOEXEC` ensures the fd does not leak into subprocesses (Codex, seat-worker processes).
- `O_RESOLVE_BENEATH` would be ideal but is Linux-only (5.6+). macOS lacks it. The walk + `O_NOFOLLOW` combo is the closest macOS equivalent.

**Linux production path (Golden Quill 64GB, client deployments):**

Linux supports proper mount namespaces. Production `OrgRootNamespace` uses `unshare(CLONE_NEWNS)` + `mount --bind --read-only` to create a per-session view of the filesystem where the org root is the only writable tree:

```python
# Linux branch, selected at boot via platform.system() == "Linux"
import ctypes
libc = ctypes.CDLL("libc.so.6", use_errno=True)
CLONE_NEWNS = 0x00020000
libc.unshare(CLONE_NEWNS)
subprocess.run(["mount", "--bind", "-o", "ro", str(org_root), str(org_root)],
               check=True)
subprocess.run(["mount", "--make-private", str(org_root)], check=True)
```

Requires CAP_SYS_ADMIN. Golden Quill client devices ship with a boot-time helper that grants the Tilth user this capability scoped to the Tilth cgroup; operator does not run Tilth as root.

**Implementation choice matrix:**

| Environment | Mechanism | Why |
|---|---|---|
| macOS dev (M1 Mac Mini 8GB) | Canonical path + `O_NOFOLLOW` + inode snapshot + symlink walk | No mount namespaces on macOS; this is the strict equivalent |
| macOS client (if shipped) | Same as dev | Architecture says "equivalent"; inode snapshot is sufficient |
| Linux client | `unshare(CLONE_NEWNS)` + bind-mount | True kernel-enforced isolation where available |

Both branches are exercised by the test suite; the macOS branch is the default in CI because CI runs on GitHub macOS runners.

### 5.3 BT3 — Admin-risk ledger rate limits

**Requirement:** per-org rate limits and size quotas. Low-severity flood attacks blocked at write time, not read time. **v2 HIGH-fix — the rate check must be atomic with the append**; v1 counted before locking, allowing two forked processes to each see count < limit and both append.

**Implementation (v2 — lock-first, count under lock, atomic day-counter):**

`admin_risk.record_admin_risk` rate-limits using a rolling 24-hour window:

| Severity | Max per 24h per operator | Action on breach |
|---|---|---|
| GREEN | 100 | `RateLimitExceeded` |
| YELLOW | 50 | `RateLimitExceeded` |
| RED | 10 | `RateLimitExceeded` |

**v2 critical-section protocol — addresses Red Team HIGH BT3 fork-race:**

```python
def record_admin_risk(entry_kind, severity, payload, operator_retype_hash):
    lock_fd = os.open(ADMIN_RISK_LOCK_PATH, os.O_CREAT | os.O_RDWR, 0o600)
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX)  # BLOCKING acquire — exclusive
        # --- critical section begins ---
        #
        # v1 bug: this counting ran BEFORE the flock above. Two forked processes
        # could both observe count < limit and both append, exceeding the quota
        # by the number of racers. v2 moves all counting inside the critical
        # section so only one process at a time can decide+append.
        #
        today_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        counter_path = LEDGER_DIR / f"admin_risk.counts.{today_utc}.json"

        # (1) Read compact day counter. O(1). If missing or stale, rebuild from ledger tail.
        counts = _read_day_counter(counter_path, today_utc)

        # (2) Apply the rate-limit check under lock.
        limit = {"GREEN": 100, "YELLOW": 50, "RED": 10}[severity]
        if counts[severity] >= limit:
            raise RateLimitExceeded(
                severity=severity,
                current=counts[severity],
                limit=limit,
                oldest_in_window_utc=_oldest_in_window_today(counter_path),
            )

        # (3) RED requires operator_retype_hash; also checked under lock so
        #     a concurrent racer cannot consume a pre-typed retype more than once.
        if severity == "RED" and not operator_retype_hash:
            raise OperatorConfirmationRequired

        # (4) Build the entry with issued_monotonic_ns + timestamp_utc + prev_hash
        #     read from the single source of truth: admin_risk.head.
        entry = _build_entry(entry_kind, severity, payload, operator_retype_hash)

        # (5) Write entry to ledger via O_APPEND single-syscall (atomic under
        #     POSIX for payloads <= PIPE_BUF).
        _append_canonical_line(ADMIN_RISK_LEDGER_PATH, entry)

        # (6) Update the HMAC trailer: re-compute over the entire file.
        _recompute_ledger_hmac_trailer(ADMIN_RISK_LEDGER_PATH, ADMIN_RISK_HMAC_PATH,
                                       trailer_key_id="tilth.ledger.admin_risk.hmac.v1")

        # (7) Bump the compact day counter.
        counts[severity] += 1
        _write_day_counter(counter_path, counts)

        # (8) Update the head-hash cache.
        _write_head(ADMIN_RISK_HEAD_PATH, entry.entry_hash)

        return entry
    finally:
        fcntl.flock(lock_fd, fcntl.LOCK_UN)
        os.close(lock_fd)
```

**Why a separate lock file (`admin_risk.lock`) and not flocking `admin_risk.jsonl` directly:** the append syscall (`write` with `O_APPEND`) and the trailer-recomputation must be in the same critical section as the rate-limit check. Flocking the data file means every reader who wants a stable view must also compete on the same fd; flocking a separate lock file decouples reader stability from writer serialization. Readers can snapshot the file-size at `LOCK_SH` and read that many bytes without blocking writers forever.

**Compact day counter (`admin_risk.counts.{YYYY-MM-DD}.json`) — v3 demoted to READ-THROUGH CACHE (closes Red Team v2 MEDIUM-3 crash-between-append-and-counter race):**

- **v3 invariant: the ledger is the SOLE source of truth for counts.** The counter file is a derived, rebuildable index — never consulted without a correctness check. Under this invariant, a crash between step (5) `_append_canonical_line` and step (7) `_write_day_counter` in the `record_admin_risk` critical section is harmless: the next reader detects the inconsistency and rebuilds from the ledger.
- Structure: `{"date": "2026-04-16", "GREEN": 7, "YELLOW": 2, "RED": 0, "ledger_seq_at_write": 1847, "cache_hmac_hex": "..."}`. UTF-8 JSON. `ledger_seq_at_write` pins the cache to the ledger position at which it was last written — reads compare against the current ledger tail seq to decide cache staleness in O(1).
- `cache_hmac_hex` is `HMAC-SHA3-512("tilth.ledger.admin_risk.counts.v3", canonical_json_of_{date,GREEN,YELLOW,RED,ledger_seq_at_write})` using the same admin_risk ledger HMAC key. Closes the subsidiary concern that a stale counter file could be forged to bypass the rate limit.
- Updated atomically under the same fcntl lock that gates ledger append.
- **v3 cache-staleness check on every read:**
  1. Read current ledger tail seq_id from `admin_risk.head` (O(1)).
  2. Read counter file. If missing, or `isinstance(cache_hmac_hex, str)` is False or HMAC verification fails, or `ledger_seq_at_write < current_ledger_seq_id`, the cache is stale.
  3. On stale cache: rebuild by tail-scanning ledger entries where `timestamp_utc` starts with today's date-string; log `F-ADM-06 DayCounterInconsistent` to degradation log (informational, not a rate-limit bypass). Rebuilt cache is written back with the current `ledger_seq_at_write` and fresh HMAC.
  4. On crash between ledger append (step 5) and counter write (step 7): `ledger_seq_at_write` falls behind `current_ledger_seq_id`; next reader detects and rebuilds. No count is lost; no count is double-counted.
- Rotation: each day's counter is a separate file; retention matches ledger retention (never purged in v0.1).
- The O(N) tail-scan only fires on rebuild; the normal-path check is O(1) (compare two integers + HMAC-verify a small JSON).

**Why the cache + HMAC + seq-pin design rather than removing the counter entirely:** every GREEN admin-risk append would otherwise require a full tail scan of today's entries to compute the limit check, which on a busy day is O(thousands of lines) per append. The cache is a performance optimization that remains correctness-preserving under crash because (a) the ledger is authoritative, (b) the cache is staleness-detected on every read, and (c) a forged cache cannot verify under the HMAC.

**Size quota:** each ledger file rotates at 100 MB (approximately 500,000 average entries). Rotation copies `admin_risk.jsonl` to `admin_risk.{YYYY-MM-DD}.jsonl` and starts a fresh file whose first line references the prior file's final `entry_hash` as `prev_hash`. Rotation is append-only; nothing is discarded.

**Fail-closed on unreadable ledger:** if the ledger file exists but cannot be parsed (file-system corruption, disk error, partial write), `record_admin_risk` raises `LedgerUnreadable` and the caller hard-aborts. No silent skip. No "continue without the admin-risk record." The architecture explicitly requires that every substitution be recorded; a broken ledger means no substitutions can happen.

**Fail-closed on missing ledger:** the boot sequence (Section 9) ensures the ledger file exists and is HMAC-signed at boot. A missing ledger at runtime is a tampering signal and hard-aborts with `LedgerMissing`.

### 5.4 BT4 — HSM-capable key storage

**Requirement:** BYOK keys may optionally be stored in HSM / separate encrypted vault with distinct access controls. Default: OS keyring per org. HSM path documented and switchable.

**Implementation — the abstract + three concretes:**

```python
class KeyStore(abc.ABC):
    # See Section 3.11 for the full signature.
    ...
```

**`MacOSKeychainKeyStore` (default on macOS):**
- Uses the `security` CLI invoked via `subprocess` with explicit arg arrays (no shell).
- Service name pattern: `com.goldenquill.tilth.{slug}` where `slug` is the bound org slug, satisfying per-org scoping (architecture Law 3 / M9).
- Account name pattern: `{purpose}.{key_id}` so an operator running `security find-generic-password` sees meaningful names.
- Keychain-locked state: the store raises `KeychainLockedError` on first access; the caller (typically `boot.boot_envelope`) is responsible for prompting the operator to unlock. Section 1 does not prompt.
- Zeroization: `security delete-generic-password -s <service> -a <account>`. The deleted item is gone from the on-disk SQLite plus its backing file, per Apple documentation.
- **v3 `_retrieve_raw` contract:** the CLI returns key material on stdout (hex-encoded by `security -w`). The implementation reads stdout as `bytes`, hex-decodes into a `bytearray`, and immediately overwrites the intermediate `bytes` variable. Signature: `def _retrieve_raw(self, key_id) -> bytearray: raw = self._cli("find-generic-password", "-s", service, "-a", account, "-w"); buf = bytearray.fromhex(raw.strip().decode("ascii")); return buf`. The caller-visible `retrieve()` wraps `buf` in `SecretBytes` per §3.11. Test: `test_macos_keychain_keystore_wraps_before_return`.

**`FileKeyStore` (fallback) — v2 adds passphrase hygiene and AES-GCM nonce registry:**
- Used when `MacOSKeychainKeyStore` is unavailable (non-macOS, Keychain disabled, operator opts out).
- On-disk file at `sovereignty/keys/{slug}/{key_id}.aead`.
- Key envelope: `PBKDF2-SHA3-512(passphrase, salt, iterations=600_000)` derives a 32-byte KEK; `AES-256-GCM(KEK, nonce=12B, plaintext=key_bytes)` seals the key. 600k iterations matches OWASP 2024 guidance for PBKDF2-SHA3-512.
- Salt: 16 bytes random, stored alongside ciphertext in the `.aead` file.
- **v2 passphrase hygiene (addresses Red Team [MEDIUM] BT4 crash-log leak):**
  1. Read `TILTH_FILE_KEYSTORE_PASSPHRASE` into a `bytearray` inside `FileKeyStore.__init__`.
  2. Immediately derive the KEK via PBKDF2 and store the KEK as a `bytearray` on the instance (not the passphrase).
  3. `zero_bytes(passphrase_buffer)` to scrub the passphrase bytearray in place.
  4. Call `del os.environ["TILTH_FILE_KEYSTORE_PASSPHRASE"]`. Subsequent crashes will not include the passphrase in the process environment dump.
  5. If the operator starts a second FileKeyStore-using subprocess later, that subprocess must re-supply the passphrase at startup — there is no shared in-memory cache.
- **v2 core-dump suppression:** `boot.boot_envelope` calls `resource.setrlimit(resource.RLIMIT_CORE, (0, 0))` before any keystore operation. This prevents the kernel from writing a core file on segfault, closing the on-disk leak vector even if the passphrase somehow remained in memory.
- Absence of the env var → `FileKeyStoreUnavailable` — fail-closed. The env var is expected to be set by the operator's shell rc (documented in the operator onboarding runbook, Section 8 tests check the documentation reference exists). v2: operator can instead invoke a one-time `tilth keystore-unlock` CLI that prompts `getpass` into a bytearray, derives the KEK, and hands off to a long-running Tilth daemon; covered in the onboarding runbook.
- **v3 `_retrieve_raw` contract:** the implementation loads the `.aead` file, decrypts with `AES-256-GCM(KEK, nonce, ciphertext)` into a `bytearray` output buffer (not a `bytes`). `cryptography.hazmat.primitives.ciphers.aead.AESGCM.decrypt` returns `bytes`, so `_retrieve_raw` wraps the decrypt call: `out = bytearray(aead.decrypt(nonce, ct, aad))`, then immediately zeroes the `bytes` intermediate via `del` and forced GC (best-effort). The caller-visible `retrieve()` wraps `out` in `SecretBytes`. Documentation explicitly flags the brief microsecond window where `AESGCM.decrypt`'s internal `bytes` copy is live; this is a library-level constraint we accept under the trusted-operator boundary. Test: `test_file_keystore_decrypt_wraps_before_return`.
- **v2/v3 AES-GCM nonce uniqueness registry (Red Team [LOW] BT4 nonce reuse + v2 exhaustion + v3 truncation):**
  - On every `_encrypt(key_id, plaintext)` call: generate `nonce = os.urandom(12)`, check `.nonce_registry.{seq}.jsonl` under `sovereignty/keys/{slug}/` for prior appearance. Prior appearance → `NonceReused` hard abort (F-KEY-05).
  - Append `{key_id, nonce_hex, ts}` to the registry inside the same critical section as the encryption write (fcntl lock on `.nonce_registry.lock`).
  - **v3 size-cap rotation + v4 pre-check** (Red Team v2 [MEDIUM] exhaustion + RT-v3 MED-1 rotation timing race): each segment file is capped at `NONCE_REGISTRY_SIZE_LIMIT_BYTES = 10 MiB`. **v4 ordering:** the size check runs BEFORE `os.urandom(12)` is called. If `os.stat(current_segment).st_size >= NONCE_REGISTRY_SIZE_LIMIT_BYTES`, `_rotate_nonce_registry()` is invoked under the same held fcntl lock to open `.nonce_registry.{seq+1}.jsonl`, seal the closed segment, and only then is the new nonce generated and written to the new segment. If rotation fails (e.g., filesystem full or permission error) `NonceRegistryRotationFailed` is raised before any nonce is generated — closes the RT-v3 MED-1 window where a nonce was generated but could not be safely registered. Boot-time verify scans all segments in order. A registry that attempts to append while segment is full AND rotation fails raises `NonceRegistryFull` (F-KEY-09) and fail-closes the encryption.
  - **v3 rolling SHA-3-512 chain** (Red Team v2 [LOW] truncation): each segment `.nonce_registry.{seq}.jsonl` has a sibling `.nonce_registry.{seq}.hmac` containing the HMAC-SHA3-512 of the segment bytes, keyed by `tilth.keys.{slug}.nonce_registry.hmac.v1`. Segment 0's trailer includes a `prev_segment_trailer_hash = 0x00`; segment N's trailer includes `prev_segment_trailer_hash = HMAC-of-segment-{N-1}`. Truncation of ANY segment breaks the chain at the next boot `verify_chain`. Bootproblem → `F-KEY-09 NonceRegistryTruncated`.
  - Collision probability with `os.urandom(12)` is ~2^-48 per pair and effectively zero at v0.1 volume, but this turns a silent PRNG failure into a loud fail-closed event — the kind of defense-in-depth the trusted-operator boundary earns by being explicit.
- Zeroization: overwrite the `.aead` file with zeros of the same length, `fsync`, unlink. Cannot guarantee journal-level erasure on APFS; documented as a known limitation. Operator who wants stronger guarantees uses Keychain.

**`YubiHSMKeyStore` (stub):**
- v0.1 ships a stub that raises `NotImplementedError("YubiHSM support deferred to Phase 2; see BT4 roadmap")`.
- The ABC surface is in place so Phase 2 can slot a real implementation without touching callers.
- Documented in `/USER.md` under "Future Work" so operators know this is a real switch, not vapor.

**`resolve_keystore()` factory:**
- Reads `TILTH_KEYSTORE_PROVIDER` env var.
- `"keychain"` (default on macOS) → `MacOSKeychainKeyStore`.
- `"file"` → `FileKeyStore`.
- `"yubihsm"` → `YubiHSMKeyStore` (stub).
- Unknown → `KeyStoreConfigError` — fail-closed.
- Fallback chain: if `"keychain"` is selected but Keychain cannot be initialized, the factory does NOT silently fall through to `FileKeyStore` — it raises `KeyStoreUnavailable` with a clear message instructing the operator to explicitly set `TILTH_KEYSTORE_PROVIDER=file` if they want the fallback. Silent fallbacks are how sovereignty promises die.

### 5.5 BT6 — M7 HMAC key lifecycle

Covered in full under M7 (Section 4.6). BT6-specific callouts:

- **Rotation on session start:** every `start_session` generates a fresh 64-byte HMAC key with a versioned `key_id` (`tilth.session.{uuid}.hmac.v1`).
- **Revocation on session end:** `end_session` calls `keystore.zero(hmac_key_id)`. Keychain entries are deleted; File entries are zeroed and unlinked.
- **Operator-triggered rotation mid-session (v2 — 5 s grace, was 60 s):** `session.rotate_hmac_key(session)` is exposed for operator-triggered rotation (not automatic in v0.1). New key_id gets a `.v2` suffix; old key is marked for deletion after a **5-second** grace window during which in-flight signatures can complete verification. A `threading.Timer(5.0, self._zero_old_key)` scrubs the old key; cancellation on `end_session` zeroes immediately. v2 reduction from v1's 60 s addresses Red Team [MEDIUM] "rotation-grace-window abuse."
- **HSM-backed storage:** when `TILTH_KEYSTORE_PROVIDER=yubihsm` flips live in Phase 2, the session HMAC key is generated *on the HSM* and the key material never touches process memory. The Section 1 interface (sign via `keystore.retrieve` + `hmac_sha3_512`) does not change; the implementation of `retrieve` changes to return an HSM-sign-operation handle. Documented as Phase 2 work.
- **No persistence past termination:** `end_session`, SIGTERM handler, SIGINT handler, and the crash-path orphan-key sweep (boot step 8) all zero keys. A machine that finds `tilth.session.*.hmac.*` entries at next boot with no matching ACTIVE session is a crash signal — the sweep zeros them and logs a `crash_recovered` event to `degradation.jsonl`.

### 5.6 BT8 — Degraded-run / bypass flag append-only log

**Requirement:** M10 `degraded_run` flag and M13 `bypass_active` flag stored in append-only hash-chained log; no in-place mutation; flag history auditable. **v2 added per-ledger HMAC trailer**; **v3 adds freshness watermark** addressing Red Team v2 [HIGH-1] "ledger-rollback via HMAC-trailer reuse" — a valid-looking `(ledger, trailer)` pair can be swapped in from an old snapshot; boot-time integrity check alone accepts the old pair because its HMAC validates. The freshness watermark gives the boot verifier a rollback oracle.

**v3 — per-ledger HMAC trailer primitive with `last_seq_id`:**

Every ledger (`admin_risk.jsonl`, `degradation.jsonl`) has a sibling file `*.hmac` whose payload is a SIGNED JSON object (not just the raw HMAC hex):

```json
{
  "ledger_name": "admin_risk",
  "last_seq_id": 4237,
  "last_entry_hash": "…128-hex-chars…",
  "ledger_hmac": "…128-hex-chars…",
  "trailer_version": 2
}
```

The `ledger_hmac` field is the HMAC-SHA3-512 of the full ledger file bytes, keyed by `keystore.retrieve("tilth.ledger.{name}.hmac.v1")`. The whole JSON object is canonicalized and re-HMAC'd to produce a `trailer_hmac` written on the second line of the file (so the trailer object itself is tamper-evident).

**v3 — ledger watermark baseline (`sovereignty/ledger_watermarks.json`) + v4 — watermark HMAC (`sovereignty/ledger_watermarks.hmac`):**

A separate JSON file mapping ledger name → last-known `(last_seq_id, last_trailer_hmac_hex, wall_at_write)`. Updated atomically via `tmp → rename` after every successful ledger append inside the same fcntl critical section.

**v4 watermark integrity (closes RT-v3 HIGH-1 "Watermark-forge rollback"):** The watermark body is paired with a sibling file `watermarks/ledger_watermarks.hmac` whose payload is a signed JSON object:

```json
{
  "watermarks_version": 1,
  "watermarks_hmac": "…128-hex-chars…",
  "wall_at_write_utc": "2026-04-16T14:02:11Z"
}
```

The `watermarks_hmac` field is the HMAC-SHA3-512 of the canonical JSON encoding of `ledger_watermarks.json`'s full body bytes, keyed by `keystore.retrieve("tilth.watermarks.hmac.v1")`. The whole trailer object is canonicalized and re-HMAC'd to produce a `trailer_hmac` written as the second JSON object in the file. The key `tilth.watermarks.hmac.v1` is auto-provisioned into the keystore at first boot alongside the per-ledger keys (§4.7 M7 bootstrap).

**Why watermark HMAC closes the rollback attack:** RT-v3 HIGH-1 observed that an attacker with file-write access (e.g., backup restore, cloud sync) could replace `ledger/*.jsonl`, `ledger/*.hmac`, AND `watermarks/ledger_watermarks.json` with an older self-consistent snapshot. Boot's monotonicity check would see `current.last_seq_id == watermark.last_seq_id` and the trailer HMAC would verify because it was a legitimate past pair. With the v4 watermark HMAC, the attacker must also forge `watermarks/ledger_watermarks.hmac` — which requires the keystore key `tilth.watermarks.hmac.v1` that the trusted-operator threat model puts out of reach (compromised operator keyring is out-of-scope).

**Boot verification order (v4):**

```python
def verify_watermarks_integrity(
    watermarks_path: Path,
    hmac_path: Path,
    key_id: str = "tilth.watermarks.hmac.v1",
) -> dict[str, LedgerWatermark]:
    # Step 1: if the watermark body exists but the HMAC file does not, fail-closed.
    #         This catches an attacker who replaces the body but forgets/cannot
    #         replace the HMAC (or an accidental partial rollback).
    if watermarks_path.exists() and not hmac_path.exists():
        raise WatermarkHmacMissing(watermarks_path)

    # Step 2: if both exist, verify the HMAC over the canonical JSON body.
    if watermarks_path.exists():
        body_bytes = canonical_json_bytes(json.loads(watermarks_path.read_bytes()))
        trailer = load_trailer(hmac_path)
        with resolve_keystore().retrieve(key_id) as key:
            expected = hmac_sha3_512(key.view(), body_bytes)
            if not hmac.compare_digest(expected.hex(), trailer.watermarks_hmac):
                raise WatermarkHmacMismatch(
                    watermarks_path,
                    remediation=(
                        "The watermarks file has been tampered with or rolled back "
                        "from a valid older state. An attacker may have replaced "
                        "the ledger AND the watermark, but cannot forge the HMAC "
                        "without the keystore key. This is F-ADM-10. Operator must "
                        "run the admin_risk re-issuance ceremony in docs/recovery.md."
                    ),
                )

    # Step 3: first-boot path — empty watermarks + empty ledgers is legal;
    #         populated ledgers + missing watermark is a rollback attack.
    return load_watermarks(watermarks_path) if watermarks_path.exists() else {}
```

The watermark HMAC is recomputed and written inside the SAME fcntl critical section as the watermark body (see `update_watermark` below, v4 update). The HMAC write happens AFTER the body `tmp → rename` so the on-disk invariant is: the HMAC only references a body that is already durable on disk.

```python
@dataclass(frozen=True, kw_only=True)
class LedgerWatermark:
    ledger_name: str
    last_seq_id: int                 # monotonic integer; strictly increasing
    last_trailer_hmac_hex: str       # the HMAC of the ledger file at last append
    wall_at_write_utc: str           # ISO-8601 Z
```

```python
def verify_ledger_freshness(
    ledger_path: Path,
    trailer_path: Path,
    watermarks: dict[str, LedgerWatermark],
    key_id: str,
) -> None:
    # Step 1: HMAC integrity of the trailer file itself.
    verify_trailer_hmac(trailer_path, "tilth.ledger.{name}.trailer.hmac.v1")

    # Step 2: HMAC integrity of the ledger against the trailer's ledger_hmac.
    trailer = load_trailer(trailer_path)
    if not hmac.compare_digest(
        compute_ledger_hmac(ledger_path, key_id),
        trailer.ledger_hmac,
    ):
        raise LedgerHMACTrailerMismatch(ledger_path)

    # Step 3: freshness — last_seq_id must NOT regress vs the watermark.
    prev = watermarks.get(ledger_path.stem)
    if prev is not None and trailer.last_seq_id < prev.last_seq_id:
        raise LedgerWatermarkRegression(
            ledger=ledger_path.stem,
            observed=trailer.last_seq_id,
            expected_ge=prev.last_seq_id,
            remediation=(
                "The ledger-trailer pair has been rolled back to an earlier snapshot. "
                "An attacker with fs-write access has replaced both files from an old "
                "backup. Operator must reconcile via the admin_risk re-issuance "
                "ceremony in docs/recovery.md. This is F-ADM-08."
            ),
        )

    # Step 4: if equal, also verify last_trailer_hmac match — catches swap-in of
    # a trailer that happens to have the same seq_id but different hmac (partial
    # rollback).
    if prev is not None and trailer.last_seq_id == prev.last_seq_id:
        if not hmac.compare_digest(
            trailer.ledger_hmac, prev.last_trailer_hmac_hex,
        ):
            raise LedgerWatermarkRegression(
                ledger=ledger_path.stem,
                observed=trailer.last_seq_id,
                expected_ge=prev.last_seq_id,
                remediation=(
                    "Trailer HMAC does not match the watermark's last_trailer_hmac "
                    "for the same seq_id. A partial rollback is indicated. F-ADM-08."
                ),
            )
```

After a successful ledger append + trailer-write, `boot.py` or the append path updates `ledger_watermarks.json` within the same critical section. **v4 lock discipline:** the body write, the fsync, the HMAC recompute, and the HMAC trailer write all occur under a SINGLE held `fcntl.LOCK_EX` on `watermarks/ledger_watermarks.lock`. The lock is never released between steps — this closes the analogous RT-v3 MED-2 race on watermarks.

```python
def update_watermark(ledger_name: str, trailer: LedgerTrailer) -> None:
    # v4 — single-held-lock discipline. Lock acquired before body compute,
    # released only after HMAC trailer is fsynced.
    wm_lock_path = watermarks_dir() / "ledger_watermarks.lock"
    with acquire_fcntl_exclusive(wm_lock_path) as lock_fd:
        # Called inside the same fcntl.LOCK_EX on {ledger}.lock critical section.
        wm = load_watermarks()
        wm[ledger_name] = LedgerWatermark(
            ledger_name=ledger_name,
            last_seq_id=trailer.last_seq_id,
            last_trailer_hmac_hex=trailer.ledger_hmac,
            wall_at_write_utc=iso_utc_now(),
        )
        # Step 1: write body atomically (tmp → fsync → rename → fsync parent).
        body_bytes = canonical_json_bytes(wm)
        atomic_write_watermarks_body(body_bytes)
        # Step 2: recompute and write HMAC trailer atomically. MUST happen
        #         inside the same lock so a concurrent reader cannot see a
        #         new body paired with an old HMAC.
        with resolve_keystore().retrieve("tilth.watermarks.hmac.v1") as key:
            new_hmac = hmac_sha3_512(key.view(), body_bytes).hex()
        atomic_write_watermarks_hmac(
            WatermarksTrailer(
                watermarks_version=1,
                watermarks_hmac=new_hmac,
                wall_at_write_utc=iso_utc_now(),
            )
        )
        # fcntl.LOCK_UN happens via the context manager at function exit.
```

**Invariant:** at no point does a reader see `ledger_watermarks.json` with a stale `.hmac`. Either both are pre-update (reader proceeds with the old, valid pair) or both are post-update (reader proceeds with the new, valid pair). The lock guarantees the interval between body-rename and HMAC-rename is not observable by any other process reading under the same lock convention.

**Why a separate watermarks file vs. per-ledger state:** the watermark file is the ONLY Section 1 file that CANNOT be safely rolled back. It is the referee. Consolidating it across all ledgers means a single HMAC key protects the freshness oracle rather than spreading that key material per-ledger (reducing the attack surface for key-swap confusion). The trade-off — a single point of failure — is acceptable because the watermark file is tiny (<1 KiB in practice), read-mostly at boot, and write-rarely (at ledger append time).

**v3 — ledger rotation at 100 MiB** (closes Red Team v2 [LOW] "trailer recomputation cost on large ledgers"):

When a ledger file's size exceeds `LEDGER_ROTATION_SIZE_LIMIT_BYTES = 100 MiB`, the append path rotates:

1. Close the current segment.
2. Write the final trailer for the current segment to `{name}.{seq}.jsonl.hmac`.
3. Open `{name}.{seq+1}.jsonl` whose first entry's `prev_hash` = the final entry_hash of segment N.
4. The `{name}.head` pointer now tracks the active segment number and its tail.

Boot-time `verify_chain(fast=False)` walks every segment in order (0, 1, 2, …). Freshness watermark applies only to the ACTIVE (highest-numbered) segment — sealed segments are immutable and their trailers are validated once; re-opening a sealed segment is detected by segment-number regression in the watermarks file.

```python
@dataclass(frozen=True, kw_only=True)
class LedgerSegmentedWatermark:
    ledger_name: str
    active_segment: int              # highest segment number; strictly non-decreasing
    last_seq_id: int                 # global monotonic across segments
    last_trailer_hmac_hex: str
    wall_at_write_utc: str
```

Segment regression (attacker rewinds `active_segment` to an older number) is detected identically to seq_id regression.

**What the trailer + watermark does NOT defend against:** an attacker who also compromises the operator's keystore can recompute both the trailer HMAC and the watermark HMAC and remove their attack. That is out-of-model — the trust root is the operator's keystore; if it is compromised, v0.1 provides no mitigation. But the trailer+watermark raises the cost of "rollback the ledger pair" from "trivial file-system editing" to "also compromise the operator's keystore" — a meaningful defense-in-depth gain inside the single-operator boundary where the ledger+trailer pair is written by a process with keystore access but an attacker (e.g. a buggy update that accidentally restores from backup) may not have watermark-write access.

**Rationale for HMAC-rather-than-signature:** Ed25519 detached signatures would be cryptographically stronger (public-verifiability) but introduce a second key with its own provisioning story. v0.1 scope is single-operator-single-machine; the operator's keystore is already the trust root. HMAC with a keystore-derived key gives integrity-against-tamper without requiring a second credential. Phase 2 multi-operator revisits this alongside the M5 router-signing decision.

---

Same hash-chain discipline as `admin_risk.jsonl`, separate file because the consumers and retention policies differ:

- `degradation.jsonl` lives at `sovereignty/ledgers/degradation.jsonl`.
- One `DegradationEvent` per line. Canonical JSON. Each line is ≤ the POSIX atomic-write size (4096 bytes) — we target ≤2048 in practice.
- `prev_hash` chains each entry to the previous. Genesis entry has `prev_hash = "0" * 128`.
- `entry_hash` = `sha3_512(canonicalized fields excluding entry_hash)`.
- `degradation.head` caches the tail `entry_hash` for cheap appends.
- **v2:** `degradation.hmac` holds the per-ledger HMAC trailer described above.

Verification (`degradation_log.verify_chain`):
1. **v2 step 0:** verify the HMAC trailer (`verify_ledger_hmac_trailer`). If missing or mismatched → hard abort BEFORE walking the chain. Chain-integrity cannot be trusted without trailer integrity.
2. Walk from genesis forward.
3. For each line, check that its `prev_hash` equals the previous line's `entry_hash`.
4. Recompute `entry_hash` from the line contents; compare.
5. Any mismatch → `DegradationLogCorrupt(line_number=..., reason=...)`.
6. Called at every boot and every `record_degradation` call; the boot check is `verify_chain(fast=False)` (full, including trailer), runtime is `verify_chain(fast=True)` (verify last 100 entries + trailer).

**Why full chain check at boot and fast check at runtime:** boot is a natural moment to accept O(log size) work; runtime writes happen inside pipeline execution and need to be O(1). Fast mode verifies the last 100 entries plus the `degradation.head` cached hash plus the HMAC trailer; a silent corruption older than 100 entries is caught at next boot. In the trusted-operator threat model, this window is acceptable; in Phase 2's multi-operator model we will revisit.

**Append protocol (v2):**
1. Acquire `fcntl.LOCK_EX` on `degradation.lock` (blocking wait). Single-operator v0.1 will rarely contend; the lock is defensive AND the atomicity barrier for trailer recomputation.
2. Read the `degradation.head` file for `prev_hash`.
3. Construct the entry with `prev_hash`, `issued_monotonic_ns`, `timestamp_utc`.
4. Compute `entry_hash`.
5. Write the canonicalized line + `\n` with a single `os.write` to `degradation.jsonl` opened `O_APPEND | O_WRONLY`.
6. `fsync` the file.
7. **v2:** recompute `degradation.hmac` via `verify_ledger_hmac_trailer`-companion writer over the full file; write via tmp+rename; `fsync`.
8. Update `degradation.head` via tmp+rename.
9. Release the lock.

**HMAC signing of the chain:** each entry optionally carries a `signed_by_operator` boolean (see schema §2.6). For M13 bypass events this field is True and the *containing* AdminRiskEntry in `admin_risk.jsonl` carries the operator's re-type HMAC; the DegradationEvent itself does not need its own in-line signature because its `authorization_id` foreign-key + the ledger entry's signature + the v2 per-ledger HMAC trailer are the signed trust root. This avoids double-signing and the key-lifecycle questions that come with it.

---

## 6. Failure modes + fail-closed recovery

Every failure path in Section 1 halts the pipeline before any LLM is called, before any draft is written, before any money is spent on tokens. This is the point of the envelope: it is the outer skin, and an outer skin that lets bad data in silently is worse than no skin at all.

### 6.1 RFA-related

| Code | Condition | Response |
|---|---|---|
| F-RFA-01 | `RFADriftError` at re-verify (inode/device/size/content mismatch) | Hard abort. Surface diff via `diff <ingested> <current>`. Operator must re-ingest explicitly. |
| F-RFA-02 | RFA file missing at re-verify | Hard abort. `RFAMissing`. Operator must re-ingest. |
| F-RFA-03 | Nonce file missing | Hard abort. `RFAEnvelopeCorrupt`. Re-ingest. |
| F-RFA-04 | Envelope JSON unparseable | Hard abort. `RFAEnvelopeCorrupt`. Re-ingest. |
| F-RFA-05 | URL hash mismatch at re-verify (v2) | Hard abort. `RFADriftError("rfa_url_hash_mismatch")`. Operator must re-ingest. |

### 6.2 PROJECT_CONTEXT-related

| Code | Condition | Response |
|---|---|---|
| F-PC-01 | `ProjectContextDrift` (mid-session hash mismatch) | Hard abort. Operator must decide: accept new content (requires re-seal + new session) or revert on disk. |
| F-PC-02 | `OrgRootEscape` (canonical path outside org root) | Hard abort. Treated as a hostile event; admin-risk RED entry logged. |
| F-PC-03 | Cross-org PROJECT_CONTEXT load attempt | Hard abort. Law 3 violation. `CrossOrgViolation`. Admin-risk RED entry. |

### 6.3 Session-related

| Code | Condition | Response |
|---|---|---|
| F-SES-01 | Active session lock already held | `SessionAlreadyActive`. Caller must `end_session` first. |
| F-SES-02 | INTERRUPTED session detected at boot with `policy=prompt` | Boot halts with `OperatorDecisionRequired`. CLI caller prompts. |
| F-SES-03 | HMAC key issuance fails at session start | Hard abort. `SessionHMACUnavailable`. Keystore diagnostic surfaced. |
| F-SES-04 | Signal handler times out (>5s) | `os._exit(1)` after watchdog `SIGKILL`-equivalent; next boot picks up INTERRUPTED state. |
| F-SES-05 | Rotation grace window expired, old key still referenced (v2) | `RotationGraceWindowExpired`. Caller must start a fresh session. |

### 6.4 Router-integrity-related

| Code | Condition | Response |
|---|---|---|
| F-RTR-01 | `router.yaml.sig` missing | Hard abort. `RouterIntegrityError("signature_missing")`. |
| F-RTR-02 | Signature mismatch | Hard abort. `RouterIntegrityError("signature_mismatch")`. Admin-risk RED entry. |
| F-RTR-03 | Git unavailable | Hard abort. `RouterIntegrityError("git_unavailable")`. Documented dependency. |
| F-RTR-04 | Router-signing key missing from Keystore | Hard abort. Operator must re-provision per onboarding runbook. |

### 6.5 Ledger-related

| Code | Condition | Response |
|---|---|---|
| F-ADM-01 | RED-severity entry without `operator_retype_confirmation` | `OperatorConfirmationRequired`. Caller (Section 5) re-prompts. |
| F-ADM-02 | Rate-limit exceeded | `RateLimitExceeded`. Caller decides: wait until window slides (GREEN/YELLOW), or hard-abort (RED — a RED rate-limit hit is a serious incident). |
| F-ADM-03 | Ledger file unreadable | Hard abort. `LedgerUnreadable`. |
| F-ADM-04 | Chain verification failure | Hard abort. `LedgerCorrupt(line=..., reason=...)`. |
| F-ADM-05 | Ledger HMAC trailer mismatch (v2) | Hard abort. `LedgerHMACTrailerMismatch`. Tampering signal; operator must follow recovery ceremony before restart. |
| F-ADM-06 | Day-counter inconsistent with ledger tail (v2) | Warn, rebuild counter from tail, continue. Logged to `degradation.jsonl` as `day_counter_rebuilt`. |
| F-ADM-07 | Ledger HMAC trailer missing (v2) | Hard abort at boot. `LedgerHMACTrailerMissing`. Operator must restore trailer from backup OR run initial-issuance ceremony. |
| F-ADM-08 | Ledger watermark regression or missing (v3 HIGH-1) | Hard abort at boot. `LedgerWatermarkRegression` on seq<watermark or seq==watermark with different trailer_hmac; `LedgerWatermarkMissing` on non-empty ledger with no watermark. Tampering / rollback signal; operator must run recovery ceremony. |
| F-ADM-09 | Boot clock history rollback or trailer mismatch (v3 HIGH-2) | Hard abort at boot. `BootClockHistoryRollback` if current wall-clock regresses > 300 s below max(wall_at_boot) in history; `BootClockHistoryTrailerMismatch` if rolling-HMAC trailer does not verify; `BootClockHistoryTrailerMissing` on non-empty history with no trailer. M13 bypasses cannot be validated until resolved. |
| F-ADM-10 | Watermark HMAC mismatch, missing, or partial (v4 RT-v3 HIGH-1) | Hard abort at boot. `WatermarkHmacMismatch` if `ledger_watermarks.hmac` does not verify against canonical JSON of `ledger_watermarks.json`; `WatermarkHmacMissing` if body exists but HMAC file does not (or vice versa — pair must be consistent). Tampering / watermark-forge rollback signal; operator must run the admin_risk re-issuance ceremony. Because the keystore key `tilth.watermarks.hmac.v1` is inaccessible to the attacker under the trusted-operator boundary, a watermark-body rollback cannot produce a valid `ledger_watermarks.hmac` without it. |
| F-ADM-11 | Sovereignty init marker present without HMAC OR HMAC present without marker (v5 RT-v4 HIGH-1) | Hard abort at boot. `SovereigntyInitMarkerMissing`. A legitimate Tilth install always has both `sovereignty/init.marker` and `sovereignty/init.marker.hmac`, OR neither (only on the very first boot before any ledger or watermark exists). A missing pair-member indicates interrupted first-boot write (recoverable — see §4.9a recovery) or tampering (not recoverable without operator forensics). |
| F-ADM-12 | Sovereignty init marker mismatch, or both absent with non-empty ledgers/watermarks (v5 RT-v4 HIGH-1) | Hard abort at boot. `SovereigntyInitMarkerMismatch`. Two sub-cases: (a) both files present but HMAC does not verify canonical JSON — attempted forge without the `tilth.sovereignty.init.hmac.v1` keystore key; (b) both files absent BUT at least one ledger has entries or at least one watermark body exists — first-boot-reset attack signature (attacker truncated ledgers + deleted watermarks hoping to hit the legitimate-first-boot branch). No recovery — operator forensics required. |
| F-DEG-01 | Degradation log corrupt | Hard abort. Same semantics as F-ADM-04. |
| F-DEG-02 | M13 bypass past expiry used | `BypassExpired`. Not a crash — Section 5's router check consults `expires_at` and treats an expired bypass as "no bypass," re-entering hard-abort for the affected review seat. |
| F-DEG-03 | M13 bypass whose `boot_epoch_ns_at_issuance` not in current boot_clock_history (v3 HIGH-2) | `BypassClockRollbackDetected`. `bypass_is_active()` returns False AND records a new `admin_risk.jsonl` YELLOW entry noting the attempted use; caller re-enters hard-abort. |

### 6.6 KeyStore-related

| Code | Condition | Response |
|---|---|---|
| F-KEY-01 | `KeyStoreConfigError` (unknown provider) | Hard abort at boot. |
| F-KEY-02 | Keychain locked, no operator interaction available | `KeychainLockedError`. Headless mode: hard abort; interactive mode: prompt via CLI (Section 5). |
| F-KEY-03 | `KeyStoreUnavailable` | Hard abort. No silent fallback. |
| F-KEY-04 | `PBKDF2` passphrase missing (FileKeyStore) | Hard abort. `FileKeyStoreUnavailable`. |
| F-KEY-05 | Keychain item retrieval returns unexpected length | Hard abort. `KeyCorrupt`. Orphan-key sweep next boot. |
| F-KEY-06 | `zero_bytes()` called on immutable `bytes` (v2 contract guard) | Hard abort with `TypeError`. This is a DEFENSIVE assertion — correct code cannot trigger it; this code path surfaces accidental breakages of the bytearray contract during test. |
| F-KEY-07 | AES-GCM nonce reuse detected in registry (v2) | Hard abort. `NonceReused(key_id, nonce_hex)`. PRNG failure signal; operator must investigate before continuing. |
| F-KEY-08 | KeyStore contract violation — `_retrieve_raw()` returned non-bytearray (v3 HIGH-3) | Hard abort at the ABC boundary. `KeyStoreContractViolation(provider, actual_type)`. A subclass author emitted raw `bytes` (or any non-bytearray); cannot be safely zeroed. Fails at first retrieve, not at first use downstream. |
| F-KEY-09 | Nonce registry size limit exceeded without rotation, or rolling hash mismatch, or rotation failure (v3 MEDIUM-1 / LOW-1 + v4 RT-v3 MED-1) | Hard abort. `NonceRegistryOverSizeLimit` if an append would push a segment past 10 MiB without rotation having run; `NonceRegistryTrailerMismatch` if rolling SHA-3-512 across segments does not reproduce; `NonceRegistryRotationFailed` (v4) if the pre-nonce-generation rotation attempt fails (e.g., disk full, permission error) — raised BEFORE a nonce has been generated so no half-state is left behind. Any of these indicates tampering or a bug in rotation logic. |
| F-KEY-10 | KeyStore subclass attempts to override sealed `retrieve()` (v4 RT-v3 HIGH-2) | Hard abort at class-definition time. `KeyStoreContractViolation(f"{cls.__name__} attempts to override sealed retrieve()")`. Raised by `KeyStore.__init_subclass__` when a subclass's `cls.__dict__` contains `retrieve` — before any instance can be constructed. Subclasses may ONLY override `_retrieve_raw`. This closes the RT-v3 HIGH-2 bypass path that would have allowed a malicious subclass to return raw `bytes` and skip the SecretBytes wrap. |

### 6.7 Isolation-related

| Code | Condition | Response |
|---|---|---|
| F-ISO-01 | Org root inode swapped mid-session | Hard abort. `OrgRootEscape("root_inode_swapped")`. Admin-risk RED entry. Strong tampering signal. |
| F-ISO-02 | Symlink escape detected in path walk | Hard abort. `OrgRootEscape("symlink_escape")`. Admin-risk RED entry. |
| F-ISO-03 | `unshare(CLONE_NEWNS)` fails on Linux | Fall back to macOS-equivalent discipline with a loud WARN log; proceed. Documented: the Linux branch is the preferred posture, the macOS-equivalent branch is the contingency. |
| F-ISO-04 | Post-open fd fstat reveals root-inode swap (v2) | Hard abort. `OrgRootEscape("toctou_post_open_swap")`. Admin-risk RED entry. |
| F-ISO-05 | Cross-filesystem rename attempted on checkpoint (v2) | Hard abort. `CrossFilesystemRename`. Operator has moved repo across mount points; must restore to same FS. |
| F-ISO-06 | Cross-filesystem rename race detected on post-creation re-check (v3 MEDIUM-2) | Hard abort. `CrossFilesystemRename("post_creation_stdev_divergence")`. Between Check A (pre-creation) and Check B (post-fsync, pre-rename), the tmp and final parents landed on different filesystems — likely a concurrent remount. Operator must investigate mount topology. |
| F-ISO-07 | Lock-file symlink attack detected (v5 RT-v4 MED-1) | Hard abort. `LockFileSymlinkAttack(path, reason)`. `reason` is one of `o_nofollow_eloop` (O_NOFOLLOW raised ELOOP during `safe_open_lock_file` — the name was a symlink), `post_open_inode_mismatch` (fstat fd inode ≠ lstat path inode — name swapped between open and re-stat), `uid_mismatch` (fd owned by a uid other than `os.getuid()` — belt-and-suspenders against directory-permission misconfiguration). Any of these signals an attacker with file-write capability has planted a symlink or swapped a lock-file inode. No in-process recovery — boot halts, operator must inspect the lock-file paths and surrounding directory permissions. |

---

## 7. Test criteria

All tests live under `tests/pipeline/sovereignty/` and run as `pytest`. The Section 1 acceptance criterion is that every test listed here is green on Josh's M1 Mac Mini 8GB dev and on a clean Linux runner (for the BT2 Linux path tests). No test may depend on network access; external APIs are mocked via `responses`/`httpx-mock` or scripted via fixtures.

### 7.1 Unit — `crypto_primitives`

- `test_sha3_512_with_nonce_bytes_ordering` — `hash(a || nonce) != hash(nonce || a)` for randomly-chosen inputs.
- `test_hmac_sha3_512_constant_time_compare` — timing variance below measurement noise (best-effort).
- `test_pbkdf2_sha3_512_iterations_600k` — key derivation completes in <2s on M1 (perf assertion, not correctness).
- `test_zero_bytes_actually_zeroes` — post-call `bytearray` is all-zero. (Python's immutable bytes cannot be zeroed in place; `zero_bytes` operates on mutable `bytearray` views and we document this explicitly.)

### 7.2 Unit — `keys`

- `test_macos_keychain_roundtrip` — store, retrieve, zero. Uses a per-test service name to avoid polluting the dev Keychain.
- `test_file_keystore_passphrase_required` — absent env var → `FileKeyStoreUnavailable`.
- `test_file_keystore_roundtrip` — store, retrieve, zero.
- `test_yubihsm_stub_raises` — stub path raises `NotImplementedError` with correct routing hint.
- `test_resolve_keystore_unknown_provider_fails_closed` — `TILTH_KEYSTORE_PROVIDER=foo` → `KeyStoreConfigError`.
- `test_resolve_keystore_no_silent_fallback` — Keychain unavailable + provider=keychain → `KeyStoreUnavailable`, not FileKeyStore.

### 7.3 Unit — `audit` + `admin_risk` + `degradation_log`

- `test_bt3_rate_limit_rejects_11th_red_in_24h` — insert 10 RED entries, 11th raises `RateLimitExceeded`.
- `test_bt3_rate_limit_sliding_window` — 10 RED at t=0, 10 more at t=24h01m succeeds.
- `test_bt3_fail_closed_on_unreadable_ledger` — corrupt the JSONL; `record_admin_risk` raises `LedgerUnreadable`.
- `test_bt3_fail_closed_on_missing_ledger` — delete the file; boot catches it.
- `test_bt8_chain_verification_detects_tamper` — flip one byte in line N; `verify_chain(fast=False)` raises with correct `line_number`.
- `test_bt8_chain_verification_detects_replay` — delete line N+1; chain verification notices missing link.
- `test_admin_risk_red_requires_operator_retype` — `severity=RED`, no hash → `OperatorConfirmationRequired`.
- `test_admin_risk_seq_id_monotonic` — two concurrent appends (fcntl lock) produce monotonic `seq_id`.

### 7.4 Unit — `session`

- `test_session_lock_prevents_concurrent_start` — second `start_session` raises `SessionAlreadyActive`.
- `test_session_cross_org_pc_rejected` — `rfa.slug != pc.slug` → abort.
- `test_session_hmac_key_zeroed_on_end` — post-`end_session`, `keystore.exists(key_id)` is False.
- `test_session_sigterm_persists_interrupted` — send SIGTERM mid-test; next boot sees INTERRUPTED.
- `test_session_checkpoint_atomic_under_signal_race` — property-style test with randomized signal injection; no partial writes observed.

### 7.5 Unit — `isolation` + `topology` (BT2)

- `test_bt2_canonical_path_rejects_symlink_escape` — create `orgs/a/b` as symlink to `orgs/z/`; `within(Path("orgs/a/b/foo"))` returns False and raises on open.
- `test_bt2_inode_snapshot_detects_root_swap` — enter namespace, rename `orgs/a` → `orgs/a.bak`, mkdir new `orgs/a`; `within(...)` raises `OrgRootEscape("root_inode_swapped")`.
- `test_bt2_o_nofollow_rejects_final_symlink` — `open(path_that_is_symlink, O_NOFOLLOW)` raises `ELOOP`.
- `test_bt2_parent_component_symlink_detected` — create `orgs/a/link -> /etc` + `orgs/a/link/passwd`; walk catches `link` pointing outside.
- `test_bt2_linux_bind_mount_when_available` — Linux-only (marked with `@pytest.mark.linux_only`); asserts `/proc/self/mountinfo` shows the bind.
- `test_topology_doc_sourced_whitelist_rejects_cache_path` — `orgs/{slug}/vault/cached/foo.md` is not a DOC_SOURCED root.
- `test_topology_doc_sourced_whitelist_accepts_five_roots` — `rfa/`, `orgs/{slug}/`, `orgs/{slug}/dossier/entities/`, `pipeline/rubrics/`, `pipeline/institutional_memory/` all accepted.

### 7.6 Unit — `rfa_envelope` + `project_context_envelope` + `org_slug`

- `test_m1_rfa_rehash_detects_content_change` — modify `rfa/x.raw` byte 42; `reverify_rfa` raises `RFADriftError("rfa_content_hash_mismatch")`.
- `test_m1_rfa_rehash_detects_inode_swap` — rename `rfa/x.raw` → `rfa/x.raw.bak`, copy-write new content to same name; `reverify_rfa` raises `RFADriftError("rfa_inode_changed")`.
- `test_m1_nonce_is_32_bytes` — introspect envelope.
- `test_m2_project_context_binding` — session bound to slug_a cannot seal PC for slug_b.
- `test_m3_canonical_slug_handles_unicode` — `"Mycosymbiotics®"` → `"mycosymbiotics"`; `"東京"` → `InvalidSlug` (v0.1 ASCII-only policy).
- `test_m3_reserved_slugs_rejected` — each reserved name raises `ReservedSlug`.
- `test_m3_slug_length_cap` — 65-char input → `InvalidSlug`.

### 7.7 Unit — `router_integrity`

- `test_m5_router_integrity_fail_closed_unsigned` — absent `.sig` file → `RouterIntegrityError("signature_missing")`.
- `test_m5_router_integrity_fail_closed_tampered` — flip one byte in `router.yaml` → `RouterIntegrityError("signature_mismatch")`.
- `test_m5_router_integrity_yaml_semantic_equivalent` — equivalent YAML with reordered keys produces same canonical-bytes hash (positive test: whitespace/ordering changes that parse to the same content do not trip the signature).
- `test_m5_cross_family_violation_raised` — `assert_cross_family("anthropic", "anthropic")` raises.

### 7.8 Unit — `interrupted_state`

- `test_m6_interrupted_state_resumes_with_matching_hashes` — mid-draft SIGTERM, next boot resume with policy="resume" returns payload.
- `test_m6_interrupted_state_rejects_mismatched_rfa` — modify RFA between crash and resume; `resume_or_discard` raises `InterruptedStateInvalid`.
- `test_m6_discard_removes_payload` — `policy=discard` deletes the payload file.

### 7.9 Integration — full boot sequence

- `test_boot_clean_state` — empty workspace → happy path.
- `test_boot_interrupted_detected` — leave an INTERRUPTED marker; boot surfaces `OperatorDecisionRequired`.
- `test_boot_orphan_key_sweep` — pre-plant `tilth.session.deadbeef.hmac.v1` in Keychain with no matching session file; boot zeroes it and writes a `crash_recovered` degradation event.
- `test_boot_router_integrity_verified_first` — tamper `router.yaml`; boot halts before opening any org namespace.

### 7.10 Property / fuzz

- `test_prop_canonical_slug_idempotent` — `canonical_slug(canonical_slug(s)) == canonical_slug(s)` for 10,000 Hypothesis-generated strings.
- `test_prop_chain_verification_detects_any_single_byte_flip` — Hypothesis-driven; any single-byte flip anywhere in a 1000-entry ledger is detected.
- `test_prop_rate_limit_equivalence_with_explicit_count` — random insertion sequences; derived window count matches a naïve recount.

### 7.11 Performance smoke

- `test_perf_ingest_rfa_under_100ms` — 100KB RFA ingest on M1 dev under 100 ms wall clock.
- `test_perf_boot_under_2s` — full boot on clean workspace under 2 s wall clock.
- `test_perf_chain_verify_10k_entries_under_1s` — verify a 10,000-entry ledger in under 1 s.

Performance targets are sanity checks, not contracts. A ten-percent regression fires a CI warning; a fifty-percent regression fails CI.

### 7.12 v2 hardening tests (added for this revision)

Addresses the Red Team v1 findings accepted in `05_synthesis_v1.md`:

- `test_zero_bytes_rejects_immutable_bytes_object` — `zero_bytes(b"abc")` raises `TypeError`. Defensive contract boundary.
- `test_zero_bytes_zeros_bytearray_in_place` — bytearray is all `\x00` after call; `id()` unchanged (same underlying buffer).
- `test_zero_bytes_zeros_writable_memoryview` — memoryview over bytearray is zeroed through.
- `test_secretbytes_context_manager_zeros_on_exit` — even on exception inside the `with` block.
- `test_keystore_retrieve_returns_bytearray` — all three concrete KeyStores return bytearray, not bytes.
- `test_sign_health_tuple_key_zeroed_after_finally` — after the call, the `SecretBytes.view()` raises `ZeroizedBufferAccessed`.
- `test_admin_risk_fork_race_both_processes_blocked` — two subprocess fixtures attempting to hit RED limit concurrently; both contend on the fcntl lock; total appends ≤ limit. (Multiprocessing fixture with synchronization barriers.)
- `test_admin_risk_day_counter_rebuilds_if_missing` — delete the counter file, append, counter is rebuilt and correct.
- `test_admin_risk_day_counter_detects_inconsistency` — corrupt the counter; append, `F-ADM-06` fires, counter rebuilt, degradation log records `day_counter_rebuilt`.
- `test_ledger_hmac_trailer_written_on_every_append` — trailer file mtime > ledger mtime after each successful append.
- `test_ledger_truncation_detected_via_hmac_trailer` — truncate the last 3 lines of `admin_risk.jsonl`, recompute hash chain locally, call `verify_chain(fast=False)`: expect `LedgerHMACTrailerMismatch`.
- `test_ledger_trailer_missing_at_boot` — delete `admin_risk.hmac`, boot: expect `LedgerHMACTrailerMissing`.
- `test_m13_clock_forward_jump_does_not_extend_bypass` — mock `datetime.now` to jump past `expires_at` + 1 day while `time.monotonic_ns` holds; `bypass_is_active` returns False. Also the inverse: `datetime.now` pulled backward while monotonic advances past ceiling → `bypass_is_active` returns False.
- `test_bt2_post_open_swap_raises_orgrootescape` — fixture replaces the parent directory between `Path.resolve` and `os.open` using a helper subprocess; expect `OrgRootEscape("toctou_post_open_swap")` (distinct from `FileNotFoundError`).
- `test_bt2_error_distinct_from_file_not_found` — assert that `toctou_post_open_swap` is raised, NOT `FileNotFoundError` nor `OSError`, so the admin-risk ledger records an unambiguous RED entry.
- `test_filekeystore_passphrase_env_var_deleted_after_init` — after `FileKeyStore()` construction, `"TILTH_FILE_KEYSTORE_PASSPHRASE" not in os.environ`.
- `test_filekeystore_passphrase_bytearray_zeroed_after_init` — private `_passphrase_buffer` is all zeros after construction.
- `test_boot_sets_rlimit_core_zero` — after `boot_envelope`, `resource.getrlimit(RLIMIT_CORE) == (0, 0)`.
- `test_aesgcm_nonce_registry_appends_on_every_encrypt` — encrypt N times, registry has N entries.
- `test_aesgcm_nonce_registry_rejects_reuse` — patch `os.urandom` to return a repeating nonce; second encrypt raises `NonceReused`.
- `test_m3_whitespace_padded_reserved_slug_rejected` — `canonical_slug(" .git ")` raises `ReservedSlug`.
- `test_m3_lossy_transliteration_rejected` — `canonical_slug("café")` raises `InvalidSlug("transliteration_lossy")`.
- `test_m3_non_lossy_latin_accepts` — `canonical_slug("FIT Farms, Inc.")` returns `"fit-farms-inc"` unchanged by the new checks.
- `test_checkpoint_combined_status_payload_atomic` — write a checkpoint; simulate signal between `fsync` and `rename` (using `unittest.mock` to intercept `os.rename` and raise); verify that the final session file is still the old content, not a partially-written new one.
- `test_checkpoint_rejects_cross_filesystem_rename` — `os.stat` mocked to return different `st_dev` for tmp vs target; raises `CrossFilesystemRename`.
- `test_rfa_reverify_detects_url_change` — mutate `envelope.url_at_ingest`, call `reverify_rfa`: expect `RFADriftError("rfa_url_hash_mismatch")`.
- `test_m7_rotation_grace_5s_old_key_zeroed_after_5s` — rotate, wait 5.1 s, old key_id is zeroed in keystore.
- `test_boot_orphan_key_sweep_runs_before_interrupted_detect` — craft a non-ACTIVE session with a live HMAC key in keystore + an INTERRUPTED session file; boot: assert key is zeroed BEFORE `OperatorDecisionRequired` raises.
- `test_signal_handler_zeroes_key_before_checkpoint_io` — install a failing checkpoint writer; send SIGTERM; verify `session._hmac_key_buffer` is already zero before the checkpoint call is attempted.
- `test_m2_seal_under_exclusive_lock_blocks_concurrent_seal` — two subprocesses attempt to `seal_project_context` on the same slug simultaneously; one blocks on the lock; final envelope matches exactly one of the two callers (not a half-merged version).

### 7.13 v3 hardening tests (added for this revision — closes Red Team v2 HIGHs + in-scope MEDIUMs/LOWs)

Addresses Red Team v2 findings accepted in `09_synthesis_v2.md`:

**HIGH-1 — Ledger watermark (rollback via HMAC-trailer reuse):**
- `test_ledger_rollback_via_hmac_swap_detected_by_watermark` — write ledger to seq 500, snapshot `.jsonl` + `.hmac`; continue writing to seq 1000; swap ledger+HMAC pair back to seq-500 snapshot; boot: expect `F-ADM-08 LedgerWatermarkRegression`.
- `test_ledger_watermark_missing_at_boot_aborts_cleanly` — delete `ledger_watermarks.json`; boot with non-empty ledger: expect `F-ADM-08 LedgerWatermarkMissing` (distinct from first-boot, which creates the watermark if ledger is empty).
- `test_ledger_watermark_equal_seq_different_trailer_hmac_rejected` — same `last_seq_id` but different `last_trailer_hmac_hex` than watermark (partial rollback): expect `F-ADM-08 LedgerWatermarkRegression`.

**HIGH-2 — Boot clock history (wall-clock rollback + process-restart bypass extension):**
- `test_m13_bypass_wall_clock_rollback_detected_via_boot_history` — issue a bypass at t0; append a boot_clock_history entry at wall_at_boot=t0+1h; roll wall clock backward to t0-30min; call `bypass_is_active`: expect `BypassClockRollbackDetected`.
- `test_m13_bypass_process_restart_monotonic_reset_does_not_extend` — issue bypass, exit process, restart (new monotonic clock epoch), verify `bypass_is_active` returns False because `boot_epoch_ns_at_issuance` is not in the current boot_clock_history. Also verifies that the bypass's `expires_at` wall-clock check still holds when within the window (belt-and-suspenders).
- `test_boot_clock_history_append_on_every_boot` — boot three times in succession; `boot_clock_history.jsonl` has exactly 3 entries, each with distinct `boot_epoch_ns`.
- `test_boot_clock_history_tamper_evident_trailer_mismatch` — append a forged entry manually to `boot_clock_history.jsonl`; boot: expect `F-ADM-09 BootClockHistoryTrailerMismatch` (the file carries a rolling HMAC-SHA3-512 trailer analogous to ledger).

**HIGH-3 — KeyStore SecretBytes contract:**
- `test_keystore_retrieve_returns_secretbytes_for_all_providers` — iterate over `MacOSKeychainKeyStore`, `FileKeyStore`, test `InMemoryKeyStore`; assert `isinstance(store.retrieve(key_id), SecretBytes)`.
- `test_keystore_contract_violation_raises_at_runtime` — subclass `KeyStore` with `_retrieve_raw` that returns `bytes`; calling `.retrieve(...)` raises `F-KEY-08 KeyStoreContractViolation` at the ABC boundary, NOT at first use downstream.
- `test_file_keystore_decrypt_wraps_before_return` — `FileKeyStore._retrieve_raw` returns `bytearray`; `retrieve()` wraps into `SecretBytes`; `SecretBytes.zero()` on exit zeros the underlying decrypted key buffer.
- `test_macos_keychain_keystore_wraps_before_return` — same assertion pattern against macOS CLI dispatcher (uses fake `security` binary in test harness).

**MEDIUM-1 — Nonce registry size limit + rotation:**
- `test_nonce_registry_size_limit_triggers_rotation` — seed `.nonce_registry.0.jsonl` with 10 MiB + 1 byte of entries; next encrypt rotates to `.nonce_registry.1.jsonl`; rolling hash in `.nonce_registry.1.hmac` references `.nonce_registry.0.hmac.final_hash`.
- `test_nonce_registry_rotation_preserves_rolling_hash_chain` — rotate three times; verify the rolling SHA-3-512 of all three segments is reproducible.

**MEDIUM-2 — M6 cross-fs double-check:**
- `test_cross_fs_double_check_catches_mid_write_remount` — mock `os.fstat(tmp_fd).st_dev` to return a different value from `os.stat(final_parent).st_dev`; checkpoint raises `F-ISO-06 CrossFilesystemRename`.

**MEDIUM-3 — Day-counter read-through cache:**
- `test_day_counter_rebuild_from_ledger_on_crash_preserves_count` — simulate crash between step 5 (ledger append) and step 7 (counter write); next read detects `ledger_seq_at_write < current_ledger_seq_id`, rebuilds, count is correct.
- `test_day_counter_forged_cache_rejected_by_hmac` — hand-write a counter file with wrong HMAC; next read rebuilds and logs `F-ADM-06 DayCounterInconsistent`.

**LOW-1 — Nonce registry rolling hash:**
- `test_nonce_registry_truncation_detected_by_rolling_hash` — truncate last entry of `.nonce_registry.0.jsonl`; next encrypt or boot: `F-KEY-09 NonceRegistryTrailerMismatch`.

**LOW-2 — Unified signal handler one-shot:**
- `test_signal_handler_unified_second_signal_is_no_op` — install handler; send SIGTERM; while handler is running (mock `checkpoint` to sleep 100 ms), send SIGINT; assert the second signal returns immediately without re-entering checkpoint. Uses `_shutting_down.is_set()` assertion.

**LOW-5 — Ledger rotation at 100 MiB:**
- `test_ledger_rotation_at_100mib_chains_trailers` — fill a ledger to 100 MiB + 1 byte; next append triggers rotation to `.1.jsonl`; segment 1's first line carries `prev_hash = last_hash_of_segment_0`; watermark now points to `(segment_index=1, last_seq_id=N+1)`.

All v3 tests must pass in addition to all v1 and v2 tests for Section 1 to be marked `READY_TO_LOCK`.

### 7.14 v4 hardening tests (added for this revision — closes Red Team v3 HIGHs + in-scope MEDIUMs/LOWs)

Addresses Red Team v3 findings accepted in `13_synthesis_v3.md`:

**RT-v3 HIGH-1 — Watermark HMAC integrity (watermark-forge rollback):**
- `test_watermark_hmac_missing_aborts_boot` — create a valid `ledger_watermarks.json` but delete `ledger_watermarks.hmac`; boot: expect `F-ADM-10 WatermarkHmacMissing`. Distinct from first-boot where both are absent (legal).
- `test_watermark_forged_without_hmac_key_detected` — roll `ledger_watermarks.json` back to an older self-consistent snapshot WITHOUT access to keystore key `tilth.watermarks.hmac.v1`. The attacker attempts to write a plausible `ledger_watermarks.hmac` but cannot forge the HMAC. Boot: expect `F-ADM-10 WatermarkHmacMismatch`.
- `test_watermark_hmac_roundtrip_canonical_json` — write a watermark, capture the HMAC; re-canonicalize the body JSON with keys in a different order; HMAC must still match (canonical JSON is deterministic regardless of input key order).
- `test_watermark_update_atomic_under_single_lock` — under concurrent simulated readers, verify that no reader observes a body from time T paired with an HMAC from time T' ≠ T. Uses `strace`/`dtrace` or an in-process mock filesystem that records pairs observed at every read.
- `test_watermark_hmac_written_after_body_rename` — kill the process between the body tmp-rename and the HMAC tmp-rename; next boot sees body-new + HMAC-old, which fails verification → `F-ADM-10`. Operator ceremony recovers.

**RT-v3 HIGH-2 — KeyStore `retrieve()` sealed via `__init_subclass__`:**
- `test_keystore_subclass_cannot_override_retrieve` — define a subclass `EvilKeyStore(KeyStore)` that overrides `retrieve` directly; assert that the `class` statement raises `F-KEY-10 KeyStoreContractViolation` at class-definition time (wrap in `with pytest.raises`).
- `test_keystore_subclass_that_only_implements_retrieve_raw_passes` — define a legitimate subclass that overrides ONLY `_retrieve_raw` (plus the other abstract methods); instantiate and call `retrieve` successfully.
- `test_keystore_typing_final_annotation_present` — use `typing.get_type_hints` / `inspect` to confirm `KeyStore.retrieve` carries `@typing.final` at runtime (for mypy-equivalent static analysis contract).
- `test_keystore_metaclass_bypass_attempt_rejected` — attempt to bypass `__init_subclass__` via a custom metaclass that manually creates a class dict with `retrieve` defined; verify that either (a) the custom metaclass itself calls `__init_subclass__` and raises, or (b) the downstream `retrieve()` invocation fails `isinstance(raw, bytearray)` because the attacker's override still cannot coerce a `bytes` to `bytearray` without tripping the contract elsewhere.

**RT-v3 MED-1 — Nonce registry rotation pre-check + atomicity:**
- `test_nonce_registry_rotation_atomic_under_disk_pressure` — pre-fill segment 0 to exactly 10 MiB; mock `os.rename` in the rotation path to raise `OSError(errno=ENOSPC)`; call `encrypt()`; assert `F-KEY-09 NonceRegistryRotationFailed` is raised BEFORE `os.urandom(12)` is called (use a spy on `os.urandom` to verify call count is unchanged).
- `test_nonce_registry_rotation_size_check_precedes_nonce_generation` — spy on both `os.stat(seg)` and `os.urandom`; assert the stat call ordering: size-stat FIRST, then (if over limit) rotation, THEN `os.urandom`.

**RT-v3 MED-2 — Boot-clock-history atomic append under single lock:**
- `test_boot_clock_history_append_hmac_recompute_under_single_lock` — install an `fcntl.flock` spy; append one record; assert the lock is acquired exactly once, then released exactly once, and that all of (jsonl write, jsonl fsync, HMAC recompute, trailer write, trailer fsync) happen between the lock acquisition and release.
- `test_boot_clock_history_crash_between_append_and_trailer_recovers` — kill process mid-append after jsonl write but before trailer write; next boot: expect `F-ADM-09 BootClockHistoryTrailerMismatch`. Operator ceremony writes a fresh trailer.

**RT-v3 LOW-1 — Signal handler non-blocking checkpoint lock:**
- `test_signal_handler_nonblocking_checkpoint_lock_skips_on_contention` — pre-acquire `_checkpoint_lock` from a mock checkpoint thread that sleeps 10 s; send SIGTERM; assert the signal handler returns within 100 ms (does NOT block for 10 s); assert no new checkpoint is written; assert the process exits with code 143. Uses `time.monotonic()` to bound the assertion.

All v4 tests must pass in addition to all v1, v2, and v3 tests for Section 1 to be marked `READY_TO_LOCK`.

### 7.15 v5 hardening tests (added for this revision — closes Red Team v4 in-scope findings)

Addresses Red Team v4 findings accepted in `17_synthesis_v4.md`:

**RT-v4 HIGH-1 — Sovereignty init marker closes first-boot reset:**
- `test_first_boot_writes_init_marker_and_hmac` — fresh `sovereignty/` directory, no ledgers, no watermarks; run boot sequence; assert that after step 7c.0b, `sovereignty/init.marker` and `sovereignty/init.marker.hmac` both exist, that HMAC verifies, that `init_version == 1`, and that `boot_clock_history_seq_at_init` matches the seq_id of the entry written at step 2.5.
- `test_second_boot_verifies_init_marker_and_does_not_rewrite` — after `test_first_boot_writes_init_marker_and_hmac`, capture mtime of both files; run boot sequence again; assert marker + HMAC mtime unchanged; assert boot completes normally.
- `test_first_boot_reset_attack_truncate_ledgers_delete_watermarks_blocked` — after a legitimate first boot + several ledger appends, attacker (simulated) truncates all ledgers to 0 bytes and deletes `ledger_watermarks.json` + `ledger_watermarks.hmac` but leaves `init.marker` + `init.marker.hmac` intact; next boot: expect `F-ADM-12 SovereigntyInitMarkerMismatch` — the marker verifies but ledgers are empty (init boot_clock_history_seq_at_init cross-check fails: the referenced history entry exists but subsequent entries DO exist too, or ledgers were truncated, violating the "first boot just now" invariant implied by empty ledgers).
- `test_first_boot_reset_attack_delete_init_marker_also_blocked` — attacker truncates ledgers + deletes watermarks AND deletes init marker files; next boot: expect `F-ADM-12 SovereigntyInitMarkerMismatch` — the "both absent" branch hits the guard that checks "boot_clock_history.jsonl is non-empty" (this check is added alongside the ledger-empty check). The attacker cannot truncate `boot_clock_history.jsonl` without also breaking its HMAC trailer (caught earlier in boot, `F-ADM-09`).
- `test_init_marker_hmac_forge_without_key_rejected` — given marker body from a legitimate install, attacker with file-write but no access to `tilth.sovereignty.init.hmac.v1` attempts to write a fresh `init.marker.hmac` with a forged HMAC; next boot: expect `F-ADM-12 SovereigntyInitMarkerMismatch`.
- `test_init_marker_write_crash_between_body_and_hmac_rename_recovers` — kill process after `os.rename(tmp_m, marker_path)` but before `os.rename(tmp_h, hmac_path)`; next boot: expect `F-ADM-11 SovereigntyInitMarkerMissing`. Operator ceremony: wipe marker, confirm all ledgers still empty, restart → second attempt writes both atomically.

**RT-v4 MED-1 — O_NOFOLLOW + fstat on lock-file opens:**
- `test_safe_open_lock_file_rejects_symlink` — create `ledger_watermarks.lock` as a symlink to `/tmp/evil`; call `safe_open_lock_file(path)`; assert `F-ISO-07 LockFileSymlinkAttack(reason="o_nofollow_eloop")`.
- `test_safe_open_lock_file_rejects_swapped_inode_post_open` — monkey-patch `os.open` to succeed with a valid fd, then immediately rename the path to point elsewhere before `safe_open_lock_file` calls `os.lstat`; assert `F-ISO-07 LockFileSymlinkAttack(reason="post_open_inode_mismatch")`. (Simulates a TOCTOU race; real attacker can't easily sneak this in without same-uid concurrency, but the guard is cheap and the test makes the invariant explicit.)
- `test_safe_open_lock_file_rejects_foreign_uid` — via `os.chown` (requires test-level uid change, skip with `pytest.mark.skipif(os.getuid() != 0)` or mock via `os.fstat` return value); verify `uid_mismatch` rejection.
- `test_every_lock_site_uses_safe_open_lock_file` — static check: grep the pipeline/sovereignty/ source for `os.open(` on any `*.lock` path and assert that every hit goes through `safe_open_lock_file`. Uses `libcst` or regex over the codebase. Fails if a future PR adds a direct `os.open` on a lock file without the guard.

**Out-of-model rejection documentation (no new tests — documentation-only closures per §10 F9):**
- Red Team v4 findings RT-v4 HIGH-2 (metaclass/monkey-patch), RT-v4 HIGH-advisory-lock (same-uid concurrent writer on fcntl.LOCK_EX), RT-v4 LOW-1 (signal handler lock-contention DoS) are NOT tested because reproducing them requires executing attacker-controlled code in the Tilth process — a condition that falls outside the trusted-operator threat model. Adding a test that simulates same-uid code injection would be testing a system the v0.1 threat model does not claim to protect. The existing v4 tests for `__init_subclass__` subclass sealing, fcntl-discipline, and non-blocking signal handler remain in §7.14 and cover the in-model portion of these surfaces.

All v5 tests must pass in addition to all v1, v2, v3, and v4 tests for Section 1 to be marked `READY_TO_LOCK`.

---

## 8. Concrete numbers (pinned)

Everything below is a Section 1 constant. Changing any of these is a Section 1 revision (new audit round), not a configuration change.

| Constant | Value | Location | Rationale |
|---|---|---|---|
| `SHA3_512_DIGEST_BYTES` | 64 | `crypto_primitives.py` | Output size of SHA-3-512 |
| `RFA_NONCE_BYTES` | 32 | `rfa_envelope.py` | 256 bits CSPRNG |
| `PROJECT_CONTEXT_NONCE_BYTES` | 32 | `project_context_envelope.py` | Same |
| `SESSION_HMAC_KEY_BYTES` | 64 | `session.py` | ≤ SHA3-512 block size (72) |
| `SIGTERM_GRACE_SECONDS` | 5 | `session.py` | Signal handler must finish or be killed |
| `LLM_ACTIVE_CHECKPOINT_INTERVAL_SECONDS` | 30 | `session.py` | Max data loss on crash |
| `ADMIN_RISK_GREEN_DAILY_LIMIT` | 100 | `admin_risk.py` | BT3 |
| `ADMIN_RISK_YELLOW_DAILY_LIMIT` | 50 | `admin_risk.py` | BT3 |
| `ADMIN_RISK_RED_DAILY_LIMIT` | 10 | `admin_risk.py` | BT3, M13-aware |
| `ADMIN_RISK_LEDGER_ROTATE_BYTES` | 100 * 1024 * 1024 | `admin_risk.py` | 100 MB |
| `M13_BYPASS_DEFAULT_HOURS` | 24 | `admin_risk.py` | Architecture |
| `M13_BYPASS_CEILING_HOURS` | 72 | `admin_risk.py` | Architecture |
| `M10_AUTHOR_SEAT_DEGRADATION_THRESHOLD_SECONDS` | 1800 | `session.py` (read by Section 5) | 30 min, architecture |
| `FILE_KEYSTORE_PBKDF2_ITERATIONS` | 600_000 | `keys.py` | OWASP 2024 |
| `FILE_KEYSTORE_SALT_BYTES` | 16 | `keys.py` | AES-GCM recommendation |
| `FILE_KEYSTORE_AEAD_NONCE_BYTES` | 12 | `keys.py` | GCM standard |
| `FILE_KEYSTORE_KEK_BYTES` | 32 | `keys.py` | AES-256 |
| `ORG_SLUG_MAX_LENGTH` | 64 | `org_slug.py` | Filesystem-safe short-ID length |
| `DOSSIER_VALIDITY_DAYS` | 90 | Architecture constant (re-exported) | M11 |
| `CHAIN_VERIFY_FAST_TAIL_ENTRIES` | 100 | `audit.py` | Runtime check window |
| `KEYCHAIN_SERVICE_TEMPLATE` | `com.goldenquill.tilth.{slug}` | `keys.py` | Per-org scoping |
| `LEDGER_HMAC_TRAILER_KEY_ID_TEMPLATE` | `tilth.ledger.{name}.hmac.v1` | `audit.py` | v2 — per-ledger HMAC trailer key id |
| `HMAC_KEY_ROTATION_GRACE_SECONDS` | 5 | `session.py` | v2 — reduced from 60 s per Red Team [MEDIUM] |
| `ADMIN_RISK_DAY_COUNTER_PATH_TEMPLATE` | `admin_risk.counts.{YYYY-MM-DD}.json` | `admin_risk.py` | v2 — compact day counter |
| `NONCE_REGISTRY_PATH_TEMPLATE` | `keys/{slug}/.nonce_registry.jsonl` | `keys.py` | v2 — AES-GCM nonce uniqueness |
| `RLIMIT_CORE_VALUE` | 0 | `boot.py` | v2 — core-dump suppression for passphrase hygiene |
| `SIGNAL_HANDLER_KEY_ZERO_FIRST` | True | `session.py` | v2 — handler zeroes HMAC bytearray before any I/O |
| `LEDGER_TRAILER_VERIFY_AT_BOOT` | True | `audit.py` | v2 — always fail-closed on trailer mismatch at boot |
| `LEDGER_WATERMARKS_PATH_TEMPLATE` | `watermarks/ledger_watermarks.json` | `audit.py` | v3 — persistent baseline for ledger freshness (HIGH-1) |
| `LEDGER_ROTATION_SIZE_LIMIT_BYTES` | 100 * 1024 * 1024 | `audit.py` | v3 — rotate ledger at 100 MiB; segments chained by prev_hash + watermark segment_index (LOW-5) |
| `BOOT_CLOCK_HISTORY_PATH_TEMPLATE` | `clock/boot_clock_history.jsonl` | `boot.py`, `degradation_log.py` | v3 — tamper-evident (boot_epoch_ns, wall_at_boot_utc) record for M13 rollback detection (HIGH-2) |
| `CLOCK_ROLLBACK_TOLERANCE_SECONDS` | 300 | `degradation_log.py` | v3 — 5-min NTP slop allowance before wall-clock regression fires BypassClockRollbackDetected |
| `NONCE_REGISTRY_SIZE_LIMIT_BYTES` | 10 * 1024 * 1024 | `keys.py` | v3 — rotate nonce registry at 10 MiB (MEDIUM-1) |
| `NONCE_REGISTRY_ROTATION_PATH_TEMPLATE` | `keys/{slug}/.nonce_registry.{seq}.jsonl` | `keys.py` | v3 — segment path after rotation |
| `NONCE_REGISTRY_ROLLING_HASH_ALG` | `sha3_512` | `keys.py` | v3 — per-segment trailer chain algorithm (LOW-1) |
| `KEYSTORE_CONTRACT_ENFORCEMENT` | `assert_returns_secretbytes` | `keys.py` | v3 — ABC `retrieve()` asserts subclass `_retrieve_raw()` returned bytearray, wraps in SecretBytes, raises `KeyStoreContractViolation` otherwise (HIGH-3) |
| `ADMIN_RISK_COUNTS_CACHE_HMAC_KEY_ID` | `tilth.ledger.admin_risk.counts.v3` | `admin_risk.py` | v3 — counter cache HMAC key id (MEDIUM-3 forge-resistance) |
| `M6_CROSS_FS_DOUBLE_CHECK` | True | `interrupted_state.py` | v3 — `st_dev` check both after tmp creation AND before rename (MEDIUM-2) |
| `SIGNAL_HANDLER_ONE_SHOT_FLAG` | `_shutting_down` | `session.py` | v3 — atomic `threading.Event` gates handler entry; second signal is no-op (LOW-2) |
| `LEDGER_WATERMARKS_HMAC_PATH_TEMPLATE` | `watermarks/ledger_watermarks.hmac` | `audit.py` | v4 — rolling SHA-3-512 HMAC trailer pinning watermark body; closes RT-v3 HIGH-1 (watermark-forge rollback) |
| `LEDGER_WATERMARKS_HMAC_KEY_ID` | `tilth.watermarks.hmac.v1` | `audit.py` | v4 — keystore key signing watermark HMAC; attacker without keystore access cannot forge |
| `LEDGER_WATERMARKS_LOCK_PATH_TEMPLATE` | `watermarks/ledger_watermarks.lock` | `audit.py` | v4 — fcntl lock gating body+HMAC atomic update (single held lock) |
| `BOOT_CLOCK_HISTORY_LOCK_PATH_TEMPLATE` | `clock/boot_clock_history.lock` | `degradation_log.py` | v4 — fcntl lock gating append+HMAC-recompute atomic block; closes RT-v3 MED-2 |
| `BOOT_CLOCK_HISTORY_HMAC_KEY_ID` | `tilth.clock.boot_history.hmac.v1` | `degradation_log.py` | v4 — keystore key signing boot_clock_history rolling HMAC trailer |
| `KEYSTORE_RETRIEVE_SEALED` | True | `keys.py` | v4 — `KeyStore.retrieve()` is `@typing.final` + `__init_subclass__` rejects overrides (RT-v3 HIGH-2 closure) |
| `NONCE_REGISTRY_SIZE_CHECK_PRE_GEN` | True | `keys.py` | v4 — size check runs BEFORE `os.urandom(12)`; rotation runs under same lock (RT-v3 MED-1 closure) |
| `SIGNAL_HANDLER_CHECKPOINT_LOCK_NONBLOCKING` | True | `session.py` | v4 — handler uses `_checkpoint_lock.acquire(blocking=False)`; on contention, skip checkpoint rather than deadlock (RT-v3 LOW-1 closure) |
| `SOVEREIGNTY_INIT_MARKER_PATH_TEMPLATE` | `sovereignty/init.marker` | `boot.py`, `audit.py` | v5 — one-time first-boot witness; presence + valid HMAC closes RT-v4 HIGH-1 first-boot-reset path |
| `SOVEREIGNTY_INIT_MARKER_HMAC_PATH_TEMPLATE` | `sovereignty/init.marker.hmac` | `boot.py`, `audit.py` | v5 — HMAC-SHA3-512 trailer over canonical JSON of init marker body |
| `SOVEREIGNTY_INIT_MARKER_LOCK_PATH_TEMPLATE` | `sovereignty/init.marker.lock` | `boot.py` | v5 — fcntl lock gating the single first-boot write (body + HMAC atomic) |
| `SOVEREIGNTY_INIT_MARKER_HMAC_KEY_ID` | `tilth.sovereignty.init.hmac.v1` | `boot.py`, `audit.py` | v5 — keystore key signing init-marker HMAC; attacker without keystore cannot forge first-boot witness |
| `SOVEREIGNTY_INIT_MARKER_VERSION` | 1 | `boot.py`, `audit.py` | v5 — schema version in both body and HMAC trailer; any future schema change is a separate audit round |
| `LOCK_FILE_OPEN_FLAGS` | `os.O_RDWR \| os.O_CREAT \| os.O_NOFOLLOW` | `audit.py`, `keys.py`, `boot.py`, `session.py`, `interrupted_state.py` | v5 — every `*.lock` file open MUST pass these flags via `safe_open_lock_file`; closes RT-v4 MED-1 symlink-swap |
| `LOCK_FILE_POST_OPEN_INODE_CHECK` | True | `safe_open_lock_file` helper | v5 — post-open `os.fstat(fd).st_ino == os.lstat(path).st_ino` invariant; catches O_NOFOLLOW-bypassing inode swap between open and lstat |
| `LOCK_FILE_POST_OPEN_UID_CHECK` | True | `safe_open_lock_file` helper | v5 — post-open `os.fstat(fd).st_uid == os.getuid()` invariant; belt-and-suspenders against directory-permission misconfiguration |

---

## 9. Boot sequence (exact ordering, fail-closed at every step) — v3 adds boot_clock_history append (step 2.5) and ledger watermark verification (step 7c); v4 adds watermark HMAC verification (step 7c.0 — runs before body is trusted); v5 adds sovereignty init marker verification (step 7c.0a) and first-boot write (step 7c.0b)

`boot.boot_envelope` runs the following in order. Any failure halts with a fail-closed exit. No step may be skipped.

1. **Platform detection.** `platform.system()` — `Darwin` → macOS branch; `Linux` → Linux branch. Anything else → `UnsupportedPlatform`. v0.1 does not target Windows.
2. **v2 — Core-dump suppression.** `resource.setrlimit(resource.RLIMIT_CORE, (0, 0))`. Prevents the kernel from writing a core file on segfault; closes Red Team [MEDIUM] BT4 crash-log leak vector before any key material enters process memory. Must run BEFORE keystore operations.
2.5. **v3 — boot_clock_history append (HIGH-2).** `platform_boot.read_boot_epoch_ns()` returns the current OS boot epoch (`sysctl kern.boottime` on macOS; `/proc/stat btime` on Linux). Read `boot_clock_history.jsonl` + its rolling HMAC-SHA3-512 trailer; verify trailer. If the trailer is missing and the file is empty, this is a legitimate first-boot — initialize. If the trailer is missing and the file is non-empty → `F-ADM-09 BootClockHistoryTrailerMissing`, hard abort. If the trailer verifies, check: (a) current `wall_at_boot_utc` must be ≥ `max(wall_at_boot_utc) - CLOCK_ROLLBACK_TOLERANCE_SECONDS` in history (NTP slop allowed); a larger regression → `F-ADM-09 BootClockHistoryRollback`. (b) If `read_boot_epoch_ns()` matches an existing entry's `boot_epoch_ns` byte-for-byte, this process is running under a boot that was already recorded — do not append (idempotency). Otherwise, append a new canonical-JSON line `{"boot_epoch_ns": <int>, "wall_at_boot_utc": "<ISO-8601>", "prev_hash": "<hex>"}` and update the rolling HMAC trailer. The append is O_APPEND single-syscall; the trailer recompute is a full-file hash.
3. **Repo root sanity.** `repo_root` must exist, be a directory, contain `router.yaml`, and contain an `orgs/` subdirectory. Otherwise → `RepoRootInvalid`.
4. **KeyStore resolution.** `resolve_keystore()` returns a concrete KeyStore or raises fail-closed. If `FileKeyStore`, this step also performs the v2 passphrase-hygiene sequence: read env var into bytearray, derive KEK, zero bytearray, `del os.environ["TILTH_FILE_KEYSTORE_PASSPHRASE"]`.
5. **Operator identity probe.** `keystore.retrieve("operator.identity.v1")` returns a pre-provisioned operator-identity bytearray; absence → `OperatorNotProvisioned` (operator must run the onboarding runbook once). The identity is trusted because the keystore is trusted (per §0 trust boundary); documented as such in §10 F6.
6. **Router integrity verify.** `verify_router_integrity(repo_root, keystore)` — see 4.4.
7. **Ledger boot checks.** Three phases per ledger (v3 adds 7c watermark verification):
   - (7a) `verify_ledger_hmac_trailer(path, hmac_path, key_id)` for both `admin_risk.*` and `degradation.*`. A missing or mismatched trailer hard-aborts BEFORE any chain walk. Mismatch → `LedgerHMACTrailerMismatch`. Missing → `LedgerHMACTrailerMissing`.
   - (7b) `admin_risk.verify_chain(fast=False)`, `degradation_log.verify_chain(fast=False)`. Any chain corruption → hard abort with line number.
   - (7c.0) **v4 — Watermark HMAC integrity verification (RT-v3 HIGH-1 closure).** `verify_watermarks_integrity(watermarks_path, hmac_path, "tilth.watermarks.hmac.v1")`. Runs FIRST, before any value from the watermark is trusted. If body exists but HMAC file does not (or vice-versa) → `F-ADM-10 WatermarkHmacMissing`. If both exist but the HMAC does not verify the canonical JSON of the body → `F-ADM-10 WatermarkHmacMismatch`. If both are absent and both ledgers are empty — proceed to step 7c.0a for the init-marker consistency check (v5 refines the "legitimate first boot" decision).
   - (7c.0a) **v5 — Sovereignty init marker verification (RT-v4 HIGH-1 closure).** `verify_sovereignty_init_marker(marker_path, hmac_path, keystore, key_id, ledger_states)`. Three outcomes: (a) both init.marker + init.marker.hmac present and HMAC verifies → return the marker body; step 7c.0b is SKIPPED; proceed to step 7c with watermark freshness verification. (b) both absent AND every ledger has zero entries AND every watermark body is absent AND `boot_clock_history.jsonl` either has exactly one entry (the one just appended in step 2.5) OR is still empty at this instant → legitimate first-boot signal; proceed to step 7c.0b. (c) any other combination → fail-closed per §6.5 F-ADM-11 / F-ADM-12. Specifically: marker XOR hmac present → `F-ADM-11 SovereigntyInitMarkerMissing`; both present but HMAC verifies false → `F-ADM-12 SovereigntyInitMarkerMismatch`; both absent but ledgers or watermarks non-empty → `F-ADM-12 SovereigntyInitMarkerMismatch` (RT-v4 HIGH-1 first-boot-reset attack signature).
   - (7c.0b) **v5 — First-boot init-marker write (RT-v4 HIGH-1 closure, one-time only).** Reached ONLY if step 7c.0a returned the legitimate-first-boot signal. Call `_write_sovereignty_init_marker_first_boot(...)` (§4.9a) to write init.marker + init.marker.hmac under `init.marker.lock` in a single held `fcntl.LOCK_EX` block; O_NOFOLLOW + fstat inode check on the lock file. After successful write, every subsequent boot will follow outcome (a) in step 7c.0a. If the first-boot write crashes between the marker rename and the HMAC rename, the next boot hits outcome (c) → `F-ADM-11`, operator ceremony (§4.9a recovery) required before retry.
   - (7c) **v3 — Ledger watermark freshness verification (HIGH-1).** `verify_ledger_freshness(ledger_name, current_last_seq_id, current_last_trailer_hmac_hex)`. Reads `watermarks/ledger_watermarks.json` (now known-HMAC-valid from step 7c.0). If the file is missing and this is a first-boot (both ledgers empty) — initialize. If missing with non-empty ledgers → `F-ADM-08 LedgerWatermarkMissing`. If `current_last_seq_id < watermark.last_seq_id` → `F-ADM-08 LedgerWatermarkRegression` (ledger+HMAC pair was rolled back). If `current_last_seq_id == watermark.last_seq_id` AND `current_last_trailer_hmac_hex != watermark.last_trailer_hmac_hex` → `F-ADM-08 LedgerWatermarkRegression` (partial rollback where a forged trailer-reuse attempt produces the same seq but a different trailer content). On success, re-serialize the watermark with the current values + `wall_at_write_utc = now_utc` via the tmp+rename atomic-write pattern (same cross-fs double-check as §4.5) AND recompute the `ledger_watermarks.hmac` under the same `watermarks/ledger_watermarks.lock` held-lock (v4 atomicity invariant).
8. **v2 — Orphan-key sweep.** Walk KeyStore for `tilth.session.*.hmac.*` entries whose matching `Session` file is not `ACTIVE`. Zero each; write one `crash_recovered` event per orphan to `degradation.jsonl`. **v2 — runs BEFORE INTERRUPTED-session detection** so a live key belonging to a non-ACTIVE session cannot sit in the keystore during the operator-prompt window. Addresses Red Team [MEDIUM] "orphan-key sweep runs after interrupted-session detection."
9. **Interrupted-session detect.** `detect_interrupted(repo_root)`:
   - None → proceed to step 10.
   - Found → raise `OperatorDecisionRequired(session=...)`. Caller (Section 5 CLI) prompts operator. Because step 8 already ran, the HMAC key for the interrupted session is already zeroed; the operator's decision to `resume` or `discard` only affects the on-disk payload, not the keystore.
10. **Org slug resolution.** `canonical_slug(slug_arg)`; `ensure_slug_available(slug)`. v2 applies the whitespace-strip + lossy-transliteration rejection from §4.3.
11. **Return `SovereigntyEnvelope` handle.** The handle carries `keystore`, `repo_root`, `operator_id`, `platform`, resolved `slug`, and a reference to the cached `RouterManifest`.

**Why the orphan-key sweep moves ahead of INTERRUPTED detection in v2:** v1 left a window between "boot detects INTERRUPTED" and "operator decides resume-or-discard" during which the keystore still held a live HMAC key for the interrupted session. An attacker who could trigger SIGTERM could extract that key during the window. v2's re-ordering means the key is gone from the keystore before the operator prompt even fires; the trade-off is that a `resume` decision must re-issue a fresh HMAC key, which is a feature, not a bug — the architecture treats a SIGTERM as a trust boundary for the session key.

After boot, the caller (Section 5's CLI) proceeds to `start_session(...)`, which is where RFA + PROJECT_CONTEXT get bound.

---

## 10. Findings and open questions (for audit to confirm or refute)

### F1 — Admin-risk ledger / register namespace disambiguation (MINOR, documentation)

The v4 architecture (Law 4, H) names a single "admin-risk ledger." The code repo as of 2026-04-16 carries two files that both claim that territory:

- `logician/registers/admin_risk_register.json` — the LIVE flagged-terms register (term-scoped schema, 18 entries).
- `logician/registers/architectural_risk_register.json` — the NEW architectural-residuals register created at v4 lock (ADM-A-001 cheap-domain bypass, ADM-A-002 M13 normalization drift).

Section 1 introduces a *third* artifact: `sovereignty/ledgers/admin_risk.jsonl`, which is the append-only EVENT LOG of admin-risk ACTIONS (substitutions applied at draft-time, bypass authorizations issued). The three are not duplicates:

| File | Kind | Purpose |
|---|---|---|
| `admin_risk_register.json` | Reference (lookup) | "What terms are flagged and how should they be substituted?" |
| `architectural_risk_register.json` | Reference (lookup) | "What architectural-level residual risks are accepted and under what compensating controls?" |
| `admin_risk.jsonl` | Event log (append-only) | "What substitutions were actually applied, and by whom, and when?" |

Recommendation: update the v4 architecture text in a future revision to use three distinct names — `admin_risk_terms_register`, `architectural_risk_register`, `admin_risk_ledger` — so the conflation does not grow. This is a documentation finding, not a blocking architectural one. Section 1 proceeds with the three distinct artifacts.

### F2 — macOS BT2 equivalence claim (MINOR, audit input)

The architecture's BT2 language says "atomic bind-mount or equivalent." Section 1 claims the macOS implementation (canonical-path + `O_NOFOLLOW` + inode snapshot + symlink walk) is "equivalent." The audit panel should confirm that this meets the architectural intent for the trusted-operator threat model. If the panel judges that only a true kernel mount namespace satisfies BT2, then v0.1 dev on macOS is out of compliance and Josh's dev loop has to move to Linux or the BT2 requirement is explicitly relaxed for macOS dev.

Section 1's position: equivalence holds for the v0.1 trusted-operator threat model. A hostile process running with the same uid as the Tilth process has the keyring anyway — the attack surface we are closing is path-level trickery and race conditions, not an adversary with arbitrary syscall capability. Linux bind-mount ships on Phase 2's production clients.

### F3 — File-keystore journal-level erasure (MINOR, documented limitation)

APFS (macOS) and ext4 (Linux) both defer file deletion through journaling layers that may retain zero-overwritten content in the journal for some time after `unlink`. Section 1's FileKeyStore documents this limitation: the zero+unlink path is best-effort, and operators who want stronger guarantees should use Keychain (APFS Data Protection) or the Phase-2 HSM path. The audit panel should confirm that this limitation is an acceptable v0.1 posture.

### F4 — Signal-handler reentrance under rapid SIGTERM+SIGINT (MINOR, tested)

Python signal handlers are not reentrant-safe in the general case, and a SIGTERM arriving during a SIGINT handler could corrupt the checkpoint. Section 1's handler uses `signal.siginterrupt(SIGTERM, False)` and a threading lock around the checkpoint write; `test_session_checkpoint_atomic_under_signal_race` exercises this. Audit panel should confirm test coverage is sufficient.

### F5 — Keychain service naming collision across operators (QUESTION for audit)

The Keychain service template `com.goldenquill.tilth.{slug}` ties keys to the org slug but does not include an operator identifier. On a single-operator Mac Mini this is fine. On a hypothetical multi-operator device (Phase 2+), two operators working on the same client org would collide. Section 1 proposal: document this as a Phase 2 concern and pin the v0.1 template as above. Audit panel confirm or propose alternative (`com.goldenquill.tilth.{operator_id}.{slug}` — at cost of longer service names and more plumbing).

### F6 — Operator-identity probe trust-root documentation (MINOR, documentation)

Section 1 derives `operator_id` from `pwd.getpwuid(os.geteuid()).pw_name` (macOS/Linux) at `boot_envelope()` time. Red Team v1 (LOW) noted that this is trusted on face value — a hostile local process running as the same uid could call `boot_envelope` with forged identity context. Within the v0.1 trusted-operator threat model this is acceptable (any process running as Josh's uid already has Keychain access on macOS and filesystem access on Linux), but the assumption should be documented explicitly so Phase 2 multi-operator work inherits the right mental model.

Section 1's position: operator-identity probe trust-root is *the uid that owns the Python process*. This is not defended against same-uid hostile processes. Section 1 annotates this in §5.5 and in the `OperatorContext` dataclass docstring. The audit panel should confirm that (a) the documentation is explicit enough and (b) the boundary is correctly drawn for the trusted-operator model.

### F7 — v3 / v4 / v5 HIGH closures summary (closure confirmations requested from audit panel)

v3 closed Red Team v2 HIGH-2 and HIGH-3 fully. Red Team v3 re-audit found that v3 HIGH-1 closure was PARTIAL (the watermark file itself was not MAC-protected — an attacker with file-write capability could roll ledger + .hmac + watermark together to an older self-consistent snapshot). v4 closed this residual plus a new HIGH (KeyStore subclass-override bypass). Red Team v4 re-audit found that v4 had a new HIGH — first-boot reset via ledger truncation + watermark deletion reaches the "legitimate first-boot" path (RT-v4 HIGH-1). v5 closes this with the sovereignty init marker.

| Red Team ID | Finding | v3 state | v4 closure | Where it lives |
|---|---|---|---|---|
| RT-v2 HIGH-1 | Ledger-rollback via HMAC-trailer reuse — attacker swaps a matched (ledger, .hmac) pair for an older snapshot | PARTIAL (watermark monotonicity check added, but watermark file not MAC-bound; simultaneous rollback of all three files evades detection) | FULL — new `ledger_watermarks.hmac` rolling trailer signed with `tilth.watermarks.hmac.v1` keystore key; boot-sequence step 7c.0 verifies trailer BEFORE body is trusted; `F-ADM-10` fail-closed on mismatch or missing | §5.6 `verify_watermarks_integrity`, §9 step 7c.0, §6.5 F-ADM-10 |
| RT-v2 HIGH-2 | M13 bypass via wall-clock rollback + process-restart | FULL (v3) | UNCHANGED v3 closure holds; v4 adds RT-v3 MED-2 hardening via single-held-lock atomic append | §2.6, §4.8, §9 step 2.5, §6.5 F-ADM-09 / F-DEG-03 |
| RT-v2 HIGH-3 | SecretBytes contract violation — `KeyStore.retrieve` emits raw `bytes` | FULL (v3 hoisted wrap into ABC) | UNCHANGED v3 closure + SEALED in v4 — `@typing.final` decorator + `__init_subclass__` contract enforcement prevents accidental or malicious subclass override of `retrieve()` | §3.11 `KeyStore.__init_subclass__`, §6.6 F-KEY-10 |
| RT-v3 HIGH-1 | Watermark-forge rollback — simultaneous replacement of ledger + .hmac + `ledger_watermarks.json` with older self-consistent snapshot (v3's watermark was not MAC-bound) | NEW FINDING | FULL — see row 1 above; dedicated HMAC trailer on watermark file | §5.6, §9 step 7c.0, §6.5 F-ADM-10 |
| RT-v3 HIGH-2 | KeyStore subclass-override bypass — Python permits overriding concrete `retrieve()`, a subclass returning raw `bytes` bypasses `SecretBytes` wrap | NEW FINDING | FULL — `@typing.final` (documentary / linter-level) + `__init_subclass__` class-definition-time check that scans `cls.__dict__` for `retrieve` and raises `KeyStoreContractViolation` | §3.11 `KeyStore.__init_subclass__`, §6.6 F-KEY-10 |
| RT-v4 HIGH-1 | First-boot reset — attacker truncates all ledgers + deletes watermarks → v4 boot treats as legitimate first-boot and silently re-initializes | NEW FINDING (v4) | FULL — sovereignty init marker `sovereignty/init.marker` + `init.marker.hmac` signed with `tilth.sovereignty.init.hmac.v1`; written once at first boot, verified at every boot; "legitimate first-boot" state now distinguishable from "attacker wiped state" | §2.7b, §3.11b, §4.9a, §9 step 7c.0a + 7c.0b, §6.5 F-ADM-11 + F-ADM-12 |

Audit panel should confirm: (a) the watermark HMAC trailer design closes RT-v3 HIGH-1 at blueprint level (concrete schema, boot-sequence ordering, failure mode, tests); (b) the sealed-`retrieve` design closes RT-v3 HIGH-2 at blueprint level — `__init_subclass__` runs at class-definition time so a malicious subclass raises before it can be instantiated; (c) the boot verifier ordering (7a trailer → 7b chain → 7c.0 watermark HMAC → 7c.0a init-marker verify → 7c.0b first-boot init-marker write → 7c watermark body freshness) is correct; (d) the sovereignty init marker closes RT-v4 HIGH-1 at blueprint level — attacker without keystore cannot forge marker, attacker who deletes marker is caught by ledgers-or-watermarks-non-empty mismatch.

### F8 — Contested Red Team v2 findings (REJECTED with justification, audit panel may overturn)

v3 explicitly rejects the following Red Team v2 contests. Audit panel may overturn; Section 1's position is documented here for the record.

| RT v2 ID | Red Team position | v3 rejection rationale | Where documented |
|---|---|---|---|
| F1 namespace disambiguation (RT contest: "rename before lock") | Three distinct files that all use the phrase "admin-risk" should be renamed to disambiguate | Three files have three distinct purposes; disambiguation is DOCUMENTATION (table in §10 F1), not a blueprint-blocking rename. A rename would cascade into Section 4 rubric lookups and Section 5 routing contracts. | §10 F1 |
| F2 macOS BT2 equivalence (RT contest: "formal proof missing") | The claim that canonical-path + O_NOFOLLOW + inode snapshot + post-open fstat is equivalent to Linux bind-mount needs a formal proof | Equivalence is claimed ONLY within the stated trusted-operator threat model. A formal proof of equivalence against arbitrary threat models is not a blueprint-level requirement. The v3 trust boundary is re-stated in §5.2. | §5.2 |
| F3 FileKeyStore journal erase (RT contest: "limitation → fix") | APFS/ext4 journal-level residue should be fixed, not just documented | Documented operator guidance: use Keychain (APFS Data Protection) or Phase-2 HSM for stronger journal guarantees. FileKeyStore is the fallback provider; the limitation is inherent to journaling filesystems and is acceptable in v0.1. | §5.4, §10 F3 |
| F5 Keychain operator_id (RT contest: "multi-operator docs insufficient") | Service template should include operator_id even in v0.1 | v0.1 is single-operator Mac Mini. Adding operator_id now is YAGNI plumbing; Phase 2 multi-operator work is where this becomes meaningful. Documented as Phase 2 concern. | §10 F5 |
| M1 URL-hash re-verify (RT contest: "URL stored in envelope never re-fetched") | The RFA's URL string should be re-fetched and re-hashed | Out of model. The envelope is a trusted-operator artifact; operator editing the envelope is out of scope. The content-hash check (F-RFA-01) is the integrity anchor; URL-string drift is surfaced via `reverify_rfa` (§4.1). | §4.1 |

### F9 — RT-v3 MEDIUM / LOW closures (v4 hardening, confirmations requested)

Red Team v3 raised two in-scope MEDIUMs and one reliability LOW in addition to the two HIGHs handled in §10 F7. v4 accepts all three as hardening. One LOW (ledger-segment splice) was rejected with expanded documentation; justification included.

| Red Team v3 ID | Severity | Finding | v4 closure | Where it lives |
|---|---|---|---|---|
| RT-v3 MED-1 | MEDIUM | Nonce-registry rotation timing race — attacker fills registry to just under 10 MiB then triggers rotation exactly as a new nonce is being written; rotation fails (disk-full) while nonce is already generated, causing DoS via F-KEY-09 | Size check moved BEFORE `os.urandom(12)` under the same fcntl lock; if at/above limit, trigger rotation first; rotation is atomic (`tmp → rename`) under the same lock; if rotation itself fails, raise `NonceRegistryRotationFailed` (F-KEY-09) BEFORE any nonce is minted so no nonce is orphaned | §5.4 `FileKeyStore.generate_nonce`, §6.6 F-KEY-09 |
| RT-v3 MED-2 | MEDIUM | Boot-clock-history atomic append race — between `write()` of the new line and recomputation of the rolling HMAC trailer, a same-uid process or a crash could interpose a forged entry that ends up covered by the new HMAC | Single fcntl exclusive lock held across append + fsync + HMAC recompute + trailer tmp-write + rename + second fsync; never released between write and HMAC commit; documented as §4.8 atomicity invariant | §4.8 `append_boot_clock_record`, §7.14 atomic append tests |
| RT-v3 LOW-1 | LOW | Signal-handler deadlock — handler acquires `_checkpoint_lock` after zeroing HMAC key; if checkpoint thread holds the lock and is blocked on I/O, handler blocks forever | Non-blocking `_checkpoint_lock.acquire(blocking=False)` in the signal handler; on failure, skip checkpoint and proceed directly to key zeroization and `os._exit` — guarantees the handler always terminates | §4.6 M7 signal handler |
| RT-v3 LOW-2 | LOW (REJECTED) | Ledger-segment splice attack — attacker forges a new segment with `prev_hash` pointing to an old segment | REJECTED. Per-segment HMAC trailer is signed with the STABLE keystore key `tilth.ledger.{name}.hmac.v1` (never rotated per segment). An attacker without the keystore key cannot produce a trailer that verifies. Red Team's own escape hatch ("unless the segment key is rotated per segment") is already the design — the key is stable, not rotated, and the attacker lacks it. Documented explicitly in §5.6 | §5.6 segment-chain documentation |

Audit panel should confirm: (a) the nonce-registry pre-generation size check correctly bounds registry size under disk pressure; (b) the single-held-lock discipline on boot_clock_history closes the write→HMAC window for both hostile-interposition (same-uid) and crash-mid-append (non-hostile) scenarios; (c) the non-blocking signal-handler lock is correct (no deadlock, no race with `_shutting_down` flag); (d) the rejection of RT-v3 LOW-2 is correctly anchored in the stable-key invariant.

### F9b — Red Team v4 finding closures (v5 hardening) and out-of-model rejections (confirmations requested)

Red Team v4 returned REQUIRES_MAJOR_MITIGATIONS with three HIGH, one MEDIUM, and one LOW finding. v5 accepts the two in-scope findings (one HIGH + the MEDIUM) and rejects three out-of-model (two HIGH + the LOW). The trusted-operator threat model stated at the top of this section (§0 header, paragraph "Trusted-operator threat-model boundary") places same-uid hostile code explicitly out-of-scope. Each rejection below cites that boundary and explains why closure would require expanding the threat model rather than patching the blueprint.

Operator confirmation anchor: Josh Inklovich confirmed 2026-04-16 ("we aren't claiming to be resistant to intentional user-inserted issues"). Recorded in memory `feedback_topology_is_identity.md`-adjacent note; see §10 F9b rejections 1–3 below for the specific application.

| Red Team v4 ID | Severity | Finding | v5 disposition | Where it lives |
|---|---|---|---|---|
| RT-v4 HIGH-1 | HIGH | First-boot reset — attacker truncates all ledgers to zero lines AND deletes `ledger_watermarks.json` + `ledger_watermarks.hmac`; v4 boot treats as legitimate first-boot and silently re-initializes with an empty audit trail | **ACCEPTED; CLOSED AT BLUEPRINT.** New `sovereignty/init.marker` + `init.marker.hmac` signed with keystore key `tilth.sovereignty.init.hmac.v1`. Written once at first boot, verified at every boot. The "legitimate first-boot" state is now distinguishable from "attacker wiped state" by presence-or-absence of the marker. Attacker without keystore cannot forge a valid marker; attacker who deletes the marker too is caught by cross-reference to `boot_clock_history.jsonl` (non-empty → marker should exist; also HMAC-sealed so attacker cannot truncate it either). See §2.7b, §3.11b, §4.9a, §9 steps 7c.0a + 7c.0b, §7.15 tests. | §4.9a, §9 step 7c.0a + 7c.0b, §6.5 F-ADM-11 + F-ADM-12 |
| RT-v4 MED-1 | MEDIUM | Symlink attack on lock files — attacker pre-plants a symlink at `ledger_watermarks.lock` (or any other sovereignty lock file) pointing to a file the attacker controls; Tilth's `open()` call follows the link, operates on the wrong inode, locking invariants silently broken | **ACCEPTED; CLOSED AT BLUEPRINT.** Every lock-file open in `pipeline/sovereignty/` goes through `safe_open_lock_file` (§3.11c), which passes `O_NOFOLLOW` to `os.open` (ELOOP on symlink) and performs a post-open `fstat(fd).st_ino == lstat(path).st_ino` inode equality check (catches inode swap between open and lstat) plus a post-open `st_uid == getuid()` check (belt-and-suspenders against directory-permission misconfig). See §3.11c, §7.15 tests. | §3.11c, §6.7 F-ISO-07, §8 constants `LOCK_FILE_*` |
| RT-v4 HIGH-2 | HIGH (REJECTED — OUT-OF-MODEL) | KeyStore `retrieve()` bypass via metaclass `StripRetrieveMeta` that deletes `"retrieve"` from `cls.__dict__` before `__init_subclass__` runs, OR runtime monkey-patch `KeyStore.retrieve = lambda self, kid: b'FAKE'` | **REJECTED.** Both attack paths require executing arbitrary Python code inside the Tilth process — either via an `import` of a malicious module (the metaclass route) or direct attribute assignment on the `KeyStore` class (the monkey-patch route). Under the trusted-operator threat model, same-uid code injection is explicitly OUT-OF-SCOPE (§0 header). An attacker who can run arbitrary Python as Tilth's uid has keyring access anyway — sealing `retrieve` against hostile code would require moving the retrieval path into a C extension with private symbol linkage, a v0.1 non-goal. The `__init_subclass__` + `@typing.final` seal IS the contract for well-behaved code. Closing the out-of-model hostile-code-injection path is deferred to a future threat-model expansion, not a v0.1 Section 1 blueprint gap. | §3.11 v5 trust-boundary note |
| RT-v4 HIGH-advisory-lock | HIGH (REJECTED — OUT-OF-MODEL) | `fcntl.LOCK_EX` is advisory on POSIX — a same-uid hostile process that opens `ledger_watermarks.json` (or any other lock-protected file) WITHOUT calling `fcntl.flock`/`fcntl.lockf` is not blocked by Tilth's lock and can corrupt the file concurrently | **REJECTED.** Bypass requires a same-uid process that deliberately skips the advisory lock. Under the trusted-operator threat model, same-uid concurrent writers are OUT-OF-SCOPE (§0 header) — the threat model is designed for single-operator single-process Tilth running under an operator-owned uid. Offline tampering by a different-uid actor (or a no-uid attacker with file-write via filesystem misconfiguration) lands on an inconsistent body+HMAC pair on next boot and is caught by `F-ADM-10 WatermarkHmacMismatch` — already in-model and closed. A true mandatory lock would require either filesystem mount options (`mand` on Linux + `chmod g+s,g-x`) that are not portable, fragile, and not part of v0.1's OS contract; or a kernel-level atomic file-open-plus-lock primitive that POSIX does not provide. Not a v0.1 blueprint gap. | §0 trust-model header, §10 F9b |
| RT-v4 LOW-1 | LOW (REJECTED — OUT-OF-MODEL) | Signal-handler lock-contention DoS — a same-uid process acquires `_checkpoint_lock` and holds it; Tilth receives SIGTERM, handler tries non-blocking acquire, fails, skips checkpoint, exits — attacker forces checkpoint-skip on every shutdown | **REJECTED.** Requires a same-uid process holding `_checkpoint_lock` adversarially. Same-uid adversary is OUT-OF-SCOPE (§0 header). Also bounded: the checkpoint-skip path is explicitly the non-blocking-lock fallback (v4 RT-v3 LOW-1 closure) and the handler still zeroes HMAC keys and exits cleanly. Loss of checkpoint on hostile SIGTERM is bounded at 30 s of in-flight draft state — the same loss as any ungraceful crash — and is acceptable for the v0.1 threat model. | §4.6 M7 handler (v4 closure text), §10 F9b |

**Red Team v4's own threat-model-expansion proposals** (C-extension `retrieve`, mandatory locks, separate privilege-dropping worker process) are **not accepted** for v0.1. They are noted as Phase 2+ hardening options if the threat model expands to cover same-uid hostile processes. Adding them now would re-open the Section 1 architectural lock (v4 LOCKED 2026-04-16) because the isolation surface changes qualitatively.

Audit panel should confirm: (a) the sovereignty init marker correctly closes RT-v4 HIGH-1 at blueprint level; (b) O_NOFOLLOW + fstat closes RT-v4 MED-1 at blueprint level; (c) the out-of-model rejections of RT-v4 HIGH-2, RT-v4 HIGH-advisory-lock, and RT-v4 LOW-1 are correctly anchored in the trusted-operator threat model — specifically that expanding coverage to same-uid hostile code is a threat-model expansion decision (operator-level), not a Section 1 blueprint gap.

---

## 11. What Section 1 deliberately does NOT implement

- **Source-tag grep verification (S9 / BT10).** Section 4 (Logician) reads the RFA envelope from Section 1 and does the grep-check. Section 1 provides the hash-verified RFA + canonical path; it does not read claim tags.
- **Claim-evidence map sign-overwrite (BT7).** Section 4.
- **USER_DATA conversation-anchor integrity (BT9).** Section 4 owns the conversation log; Section 1 owns the session HMAC key that signs it.
- **Cross-family runtime routing decisions (Section 5).** Section 1 provides `assert_cross_family` and `verify_router_integrity`; Section 5 calls them on every dispatch.
- **Per-session / per-org provider quotas (BT5).** Section 5.
- **Rails-report composition and signing (BT13).** Section 4.
- **Channel F pre-flight allowlist (BT12).** Section 3.
- **Operator onboarding runbook.** Out of scope for Section 1 as a *module*; the onboarding *process* references Section 1 but is an operator-facing document (`/docs/onboarding.md`), not Section 1 code.
- **GUI affordances** (per-section panels, reframe button, token-bloat banner, claim-evidence map viewer, rails dashboard). Phase 2+ per memory `project_future_gui.md`.

---

## 12. Dependencies

**Python:** 3.11 or later (`hashlib.sha3_512`, `dataclasses(kw_only=True)`).

**Third-party packages:**

| Package | Version pin | Used for |
|---|---|---|
| `cryptography` | `>=42,<44` | AES-GCM, PBKDF2 (`hashlib.pbkdf2_hmac` is adequate for PBKDF2-SHA3-512; `cryptography` provides AES-GCM) |
| `PyYAML` | `>=6.0,<7` | `router.yaml` parsing |
| `pytest` | `>=8,<9` | Test runner |
| `pytest-asyncio` | `>=0.23,<0.24` | Async-adjacent tests (not core) |
| `hypothesis` | `>=6,<7` | Property / fuzz tests |

No `anthropic`, `groq`, `openai`, `google-genai`, `httpx` etc. — Section 1 has zero network surface.

**Platform binaries:** `security` (macOS, stdlib), `git` (any), `unshare` + `mount` (Linux production clients only).

**Supply-chain posture for v0.1:** `pip-tools` pinned lockfile (`requirements.lock`); `pip install --require-hashes`. Signature-based verification of Python packages deferred to Phase 2 per the stated trust boundary.

---

## 13. Audit request (for the Thesis Team) — v5 re-audit

**v5 context.** v4 received Editor READY_TO_LOCK, Judge PASS 100/100, Red Team **REQUIRES_MAJOR_MITIGATIONS** with 3 NEW HIGH + 1 MEDIUM + 1 LOW. Operator (Josh Inklovich) confirmed 2026-04-16 that same-uid hostile code and same-uid concurrent writers are explicitly out-of-scope ("we aren't claiming to be resistant to intentional user-inserted issues"). v5 accepts the two in-scope findings (RT-v4 HIGH-1 first-boot reset, RT-v4 MED-1 symlink-on-lock-file) and rejects three out-of-model findings (RT-v4 HIGH-2 metaclass/monkey-patch, RT-v4 HIGH-advisory-lock same-uid concurrent writer, RT-v4 LOW-1 signal-handler DoS via same-uid lock holder) with explicit trust-model citation in §10 F9b. Synthesis is documented in `17_synthesis_v4.md`. Reviewers must decide whether v5 closes the in-scope Red Team v4 findings without introducing new ones, AND whether the out-of-model rejections are correctly anchored in the stated threat model.

This is the fifth Thesis Team round. The CLAUDE.md Autonomy Rule ("don't loop revisions more than 3 times without human input") was triggered at v5; the operator confirmed the v5 scope before drafting.

Reviewers:
- **Editor (Llama 3.3 70B).** Clarity, consistency, gaps. Is Section 1's scope still contained after the v5 growth (~3,850 → ~3,910 LoC)? Do the new artifacts (`sovereignty/init.marker`, `sovereignty/init.marker.hmac`, `sovereignty/init.marker.lock`) integrate cleanly alongside watermarks and boot_clock_history without overlap? Does the `safe_open_lock_file` helper (§3.11c) correctly centralize the O_NOFOLLOW + fstat discipline across every lock-file site in Section 1? Are the new failure-mode codes (F-ADM-11, F-ADM-12, F-ISO-07) distinct from v1/v2/v3/v4 codes and fail-closed? Are the v5 additions to §7.15 (~10 new tests under 2 categories plus documentation closure) coherent with the v4 test suite and map to the accepted Red Team v4 findings? Is the out-of-model rejection language in §10 F9b specific enough that the three rejected findings cannot be quietly reopened in a future round without re-examining the threat model?
- **Judge (Qwen 3 32B).** Score v5 against the blueprint rubric. Specifically — does the sovereignty init marker design close Red Team v4 HIGH-1 (first-boot reset) at blueprint level (concrete schema in §2.7b, interfaces in §3.11b, implementation sketch in §4.9a, boot-sequence steps 7c.0a + 7c.0b in §9, failure modes F-ADM-11 and F-ADM-12 in §6.5, tests in §7.15)? Does the `safe_open_lock_file` helper close Red Team v4 MED-1 (symlink on lock file) at blueprint level? Are the out-of-model rejections of RT-v4 HIGH-2 (metaclass), RT-v4 HIGH-advisory-lock (same-uid writer), and RT-v4 LOW-1 (same-uid signal DoS) correctly scoped by the trusted-operator threat model as stated in §0 and referenced throughout §10 F9b? Are the new constants (`SOVEREIGNTY_INIT_MARKER_*`, `LOCK_FILE_*`) pinned with values AND rationales? Are the v4→v5 fix closures complete (`v5_fix_closure` should have 1 HIGH + 1 MEDIUM = 2 entries as `closed_at_blueprint`, 3 entries as `rejected_out_of_model` with threat-model citations, 1 entry for the v4 LOW-2 rejection preserved as `rejected_out_of_model`)?
- **Red Team (GPT-OSS 120B).** Re-attack v5 specifically looking for (a) whether the init-marker fix genuinely closes RT-v4 HIGH-1 (first-boot reset) — can you forge a valid `init.marker.hmac` without access to `tilth.sovereignty.init.hmac.v1`? Can you exploit a race between the marker body rename and the HMAC rename (step 7c.0b)? Can you exploit a first-boot-reset attack by wiping the init marker AND the boot_clock_history together — does the cross-reference in §2.7b `boot_clock_history_seq_at_init` hold up? Can you force a "legitimate first-boot" via the step 7c.0a outcome (b) path by manipulating boot_clock_history to look first-boot-like while leaving ledgers non-empty? (b) whether the `safe_open_lock_file` helper closes RT-v4 MED-1 — can you bypass O_NOFOLLOW via a TOCTOU where a symlink appears between the file tool's directory listing and the `os.open` call? Can you exploit the post-open fstat check by swapping inodes between fstat and the caller's first read/write? (c) whether any v5 addition re-opens a v1/v2/v3/v4 attack path. (d) Is the trust-model boundary language in §10 F9b specific enough, or can an attack be crafted that LOOKS like one of the rejected findings but is actually in-scope (i.e., does not require same-uid code injection)? Out-of-model attacks (compromised operator keyring, hostile OS, physical seizure, same-uid hostile process) remain out of scope; flag them as `[OUT_OF_MODEL]` and do not let them block lock. You MAY contest the out-of-model rejections in §10 F9b — if you do, articulate a specific attack path that works within the trusted-operator threat model (no same-uid code injection assumed) and propose a blueprint-level fix. A naked restatement of the v4 attack does not count.

**Specific asks for v5:**

1. Does v5 close Red Team v4 HIGH-1 (first-boot reset via truncate-ledgers + delete-watermarks) at blueprint level? The `sovereignty/init.marker` + `init.marker.hmac` pair in §2.7b, the `verify_sovereignty_init_marker` + `_write_sovereignty_init_marker_first_boot` interfaces in §3.11b, the implementation sketches in §4.9a, boot-sequence steps 7c.0a + 7c.0b in §9, failure modes F-ADM-11 and F-ADM-12 in §6.5, and tests `test_first_boot_writes_init_marker_and_hmac`, `test_first_boot_reset_attack_truncate_ledgers_delete_watermarks_blocked`, `test_init_marker_hmac_forge_without_key_rejected`, etc. in §7.15 are the fix. Is the `boot_clock_history_seq_at_init` cross-reference in the marker body load-bearing? Does the "both absent but ledgers non-empty → F-ADM-12" branch in §3.11b correctly catch the attacker who wipes BOTH init marker AND watermarks?
2. Does v5 close Red Team v4 MED-1 (symlink swap on lock files) at blueprint level? The `safe_open_lock_file` helper in §3.11c, failure mode F-ISO-07 in §6.7, and tests `test_safe_open_lock_file_rejects_symlink`, `test_safe_open_lock_file_rejects_swapped_inode_post_open`, `test_every_lock_site_uses_safe_open_lock_file` in §7.15 are the fix. Is the post-open fstat-vs-lstat inode equality check placed correctly in the helper (i.e., does it catch a TOCTOU between `os.open` with O_NOFOLLOW and a subsequent path-to-inode resolution)? Is the "every lock site uses safe_open_lock_file" test a reliable invariant, or does it need to be statically enforced via a linter rule?
3. Are the three out-of-model rejections in §10 F9b correctly anchored in the trusted-operator threat model?
   - **RT-v4 HIGH-2 metaclass/monkey-patch bypass of `__init_subclass__`:** requires executing attacker-controlled Python in the Tilth process. Same-uid code injection is explicitly out-of-scope (§0 header). Correct to reject?
   - **RT-v4 HIGH-advisory-lock same-uid concurrent writer:** requires a same-uid process to deliberately open a lock target without calling `fcntl.flock`/`lockf`. Same-uid concurrent writers are out-of-scope. Offline tampering by a different-uid or no-uid actor is caught on next boot by the HMAC trailer (already in-model). Correct to reject?
   - **RT-v4 LOW-1 signal handler lock-contention DoS:** requires a same-uid process holding `_checkpoint_lock` adversarially. Bounded at 30 s, same-uid out-of-scope. Correct to reject?
4. Do any of the v5 additions re-open a v1/v2/v3/v4 attack? Specifically — does the init marker introduce a new tampering surface (answer: same operator-trust scope, and attacker lacks `tilth.sovereignty.init.hmac.v1` key)? Does the `safe_open_lock_file` helper's post-open fstat check introduce a new race (answer: no — the fd is already open against the inode; even if the path is swapped, the fd is pinned)?
5. Does v5 preserve the F1–F8 rejections from v2–v4, and is the new F9b (v5 closures + v4 rejections) internally consistent with the F9 language (v3 MED/LOW closures + LOW-2 rejection)?
6. Is the trust-model boundary language in §10 F9b specific enough that a future Red Team round cannot easily re-open any of these three rejections without articulating an attack that works WITHOUT same-uid code injection or same-uid concurrent write access?

If the three-seat panel returns unanimous LOCK / READY_TO_LOCK / PASS with no in-scope HIGH findings, Section 1 v5 is promoted to the locked canonical file at `pipeline/blueprint/v0.1/section_1_sovereignty_envelope.md`, the status header flips from `DRAFT v5` to `LOCKED v0.1 2026-04-16`, and Section 2 (RFA and Claim-Evidence Layer) begins in a fresh chat per memory `feedback_window_change_discipline.md`. If any reviewer returns UNSAFE / FAIL / NOT_READY with in-scope HIGHs, the operator is re-consulted before v6 is drafted (second autonomy-rule trigger).

Reference artifacts for reviewers:
- `01_editor_audit.md` — v1 Editor audit
- `02_judge_score.json` — v1 Judge score
- `03_judge_score.json` — v1 Judge score (second pass, full-rubric version)
- `04_red_team_challenge.md` — v1 Red Team UNSAFE verdict
- `05_synthesis_v1.md` — v1 synthesis, accept/reject table, v2 scope
- `section_1_v2.md` — v2 draft
- `06_editor_audit_v2.md` — v2 Editor READY_TO_LOCK
- `07_judge_score_v2.json` — v2 Judge PASS 100/100
- `08_red_team_challenge_v2.md` — v2 Red Team REQUIRES_MAJOR_MITIGATIONS (3 NEW HIGH)
- `09_synthesis_v2.md` — v2 synthesis, accept/reject table, v3 scope
- `section_1_v3.md` — v3 draft
- `10_editor_audit_v3.md` — v3 Editor READY_TO_LOCK
- `11_judge_score_v3.json` — v3 Judge PASS 100/100
- `12_red_team_challenge_v3.md` — v3 Red Team REQUIRES_MAJOR_MITIGATIONS (2 NEW HIGH + 2 MED + 2 LOW)
- `13_synthesis_v3.md` — v3 synthesis, accept/reject table, v4 scope
- `section_1_v4.md` — v4 draft
- `14_editor_audit_v4.md` — v4 Editor READY_TO_LOCK
- `15_judge_score_v4.json` — v4 Judge PASS 100/100
- `16_red_team_challenge_v4.md` — v4 Red Team REQUIRES_MAJOR_MITIGATIONS (3 HIGH + 1 MED + 1 LOW)
- `17_synthesis_v4.md` — v4 synthesis, accept/reject table, v5 scope + operator-confirmation anchor
- `section_1_v5.md` — this file
