# Spec card — §2 Round K Capstone (integration + BT property tests + §7 test suite)

**STATUS:** DRAFT (awaiting LOCK)

**Blueprint anchor:** `pipeline/blueprint/v0.1/section_02_vault_topology.md` v7.1 (LOCKED 2026-04-19)
**Architecture anchor:** `pipeline/architecture/v0.1/tilth_architecture_locked.md` v7 A1-A12 (LOCKED 2026-04-19)
**Round:** §2 Round K — Section-2 capstone integration + BT property tests + cross-module fuzz
**Spec-card version:** v1
**Date:** 2026-04-22
**Precedent rounds:** §2 Batch 1/2/3 per-module LOCKs (11/11 code rows at `LOCKED (cycle-1 or remediation-cycle-1, 5/5 PASS)` or better as of Batch 3 Phase 2 CLOSEOUT 2026-04-22). §1 Round J capstone (LOCKED 2026-04-21) is the pattern this round mirrors.

---

## Purpose

Section 2 Vault is built module-by-module across Batch 1 (schemas/layout/identity_tuple/uuid_floor/metadata_homogenizer), Batch 2 (gate_and_open + remediation), Batch 3 (atomic_freeze + vault_query_skill + research_db_query_skill Phase-1, vault_write + compound_txn + mirror_verify Phase-2). All 11 code rows in the §2 ledger are at `LOCKED (cycle-1 or remediation-cycle-1, 5/5 PASS)` as of 2026-04-22. Round K is the **integration capstone**: verify the 19 §2 modules compose correctly as a vault-topology + enforcement envelope; verify the blueprint-tracked (BT) property invariants hold end-to-end; establish the §7 test-suite discipline at §2 scope (cross-module integration, boot-sequence property fuzz, BT14 property matrix).

This round does NOT write new §2 code. It writes the integration test surface that documents §2's whole-section coherence and that §4 Logician Group 7 amendment enforcement will consume as its §2-substrate precondition.

Promotes §2 from LOCKED-per-module (11/11 code rows) to **LOCKED-as-a-whole-section** (Round K capstone verdict).

## Scope

**§2-owned BTs** (per blueprint §2 line 101): **BT14.a–g.1** — eight subfamilies. Round K writes property tests for all eight.

Blueprint row mapping (§2.5.1 – §2.5.8):

- **BT14.a** — per-org `vault/init.marker` write + HMAC + verify (`init_marker.py`).
- **BT14.b** — Vault-owned skill enumeration (hard-coded allowlist: `vault-query`, `research-db-query`, `vault-write`; exposed via `fd_broker.py` + `vault_query_skill.py` + `research_db_query_skill.py` + `vault_write.py`).
- **BT14.c** — Cedar policy location under `vault_shared/cedar/{org_isolation,fd_issuance,write_gate}.cedar`; loaded by `m15_ledger.py` `cedar_policy_loader.load_all()`.
- **BT14.d** — `vault_shared/` signed commits via `m15_ledger.py` seed-manifest verify + `atomic_freeze.py` freeze.
- **BT14.e** — PRE-gate direct-FS failure semantics (`direct_fs_prohibition.py` + `kernel_copy_denylist.py` + `shm_memfd_denial.py`).
- **BT14.f** — per-org `init.marker` ceremony ordering (`init_marker.py` ceremony: floor → shared-init → per-org init).
- **BT14.g** — `(volume_uuid, fs_file_id)` identity tuple resolver + 4-field compare with `mount_id` and `fs_type` (`identity_tuple.py`); re-captured inside `mirror_verify.py` and `freeze_vault_shared` per Batch 3 Phase 2 defence-in-depth.
- **BT14.g.1** — stable-UUID floor PRE-gate (`uuid_floor.py`); `apfs`/`ext4`/`btrfs`/`zfs`/`xfs` allowlist; tmpfs/overlayfs/FUSE rejected.

**Out of scope** (owned by other sections):
- BT1-BT4, BT6, BT8 → Section 1 (covered by §1 Round J capstone 2026-04-21).
- BT5 per-session provider quota / back-off → Section 5.
- BT7 atomic claim-evidence sign-overwrite → Section 4.
- BT9 USER_DATA conversation-anchor integrity → Section 4.
- BT10 grep-check windowing → Section 4.
- BT11 cross-org dossier reference policy → Section 4.
- BT12 Channel F domain preflight → Section 3.
- BT13 rails report signing → Section 4.

Round K touches §1 only through its existing §3.2 consumer surface (`within_org_root`, `canonical_path`, `reserved_slug_guard`, `hmac_audit_writer`, `atomic_flush`, `safe_open_lock_file`, `per_session_hmac_key`, `nonce_registry.reserve`, `sovereignty_init_marker_verify`, `boot_clock_history.last_boot_wall_ns`). §4/§5 are not consumed — Round K is §2-internal composition.

## Integration test surface (cross-module)

Round K tests exercise the full §2 public surface as a single vault-boot + compound-txn lifecycle. Each test exercises ≥3 §2 modules in a single path.

### K.1 Boot sequence + compound-txn lifecycle (calls all 19 §2 modules end-to-end)

Per blueprint §9 — the 12-step Vault boot sequence (with 2a kernel probe, 11a snapshot prune, 11b cache prune, 11.5 seat-launch pin):

1. §1 init complete (consumed as precondition; §1 Round J primitives).
2. `uuid_floor.enforce(vault_root)` — BT14.g.1 PRE-gate.
2a. `gate_and_open.probe_openat2()` — Linux kernel floor 5.6; macOS skip.
3. `identity_tuple.capture_mount_table()` — per-boot snapshot.
4. `trust_root_mirror.verify()` via `mirror_verify.py` — immutability + content-hash + identity-tuple + manifest-signature + clock-rollback.
5. `init_marker.verify_shared()` — BT14.d shared-init verify.
6. `m15_ledger.verify_seed_manifest()` — per-seed-file identity-tuple re-capture + 4-field compare (Batch 3 Phase 2 defence-in-depth).
7. `atomic_freeze.apply()` — Linux mount-namespace switch / macOS Merkle-pin + APFS snapshot.
8. `process_wrapper.verify_manifest()` — 8a freeze-first, 8b broker-FD hash, 8c mode 0o550.
9. `m15_ledger.cedar_policy_loader.load_all()` — policy text + hash verify.
10. `fd_broker.start()` — Unix-domain socket, post-gate hook registration.
11. `init_marker.verify_org(slug)` — BT14.a + BT14.f per-org init + ceremony ordering.
11a. `atomic_freeze.prune_snapshots(retention=3)`.
11b. `cached_opportunities.prune(retention_days=90)`.
11.5. Seat-launch ordering pin (C-05 v3 invariant).
12. `VaultBootResult(success=True, …)` returned.

Layered on top:

13. `vault_write(intent=SIMPLE, txn_token=None, …)` — v7 allowlisted intent via `vault_write.py` dispatcher → §4.10.4 POST_GATE_ALLOWLIST + §4.10.6 kind-class gate.
14. `begin_compound_txn(txn_kind="index_amendment", session_id=…)` → `vault_write(intent=COMPOUND, txn_token=…)` × 2 → `commit_compound_txn(…)` → atomic persist under path-level lock.
15. `abort_compound_txn(…)` — §4.10.7.3 five-step lock-release order; §4.12 deep-inspect admin-risk append.

Eight integration classes, one per boot phase family:

- **K.1.a** — floor + kernel-primitive probe (steps 2, 2a).
- **K.1.b** — mount-table + mirror verify (steps 3, 4).
- **K.1.c** — shared-init + seed-manifest verify (steps 5, 6).
- **K.1.d** — atomic-freeze + process-wrapper verify (steps 7, 8).
- **K.1.e** — Cedar policy load + FD broker online (steps 9, 10).
- **K.1.f** — per-org init + snapshot/cache prune + seat-launch pin (steps 11, 11a, 11b, 11.5, 12).
- **K.1.g** — SIMPLE `vault_write` dispatcher composition (step 13): 5 SIMPLE intents × `txn_token=None` round-trip + 2 COMPOUND-class rejection at SIMPLE-entry + type-preamble.
- **K.1.h** — compound-txn lifecycle (steps 14, 15): `begin → stage → commit` happy path + `begin → stage → abort` path + TTL-sweep force-abort + crash-between-persists recovery via `COMPOUND_RECOVERY_SCAN_LINES=16`.

Each integration class: ≥5 adversarial cases (inject tampered mirror / tampered seed / wrapper-hash drift / freeze-failure / Cedar-load-failure / broker-socket-bind-failure / org-init-absent / txn-integrity-anomaly; verify fail-closed propagation, verify no partial state leaks, verify ledger hash-chain intact).

**≥15 integration tests × 8 classes × adversarial expansion ≈ ≥30 integration test methods floor** (∼60 with parametric expansion).

### K.2 Per-BT property tests (≥12 per BT; 8 BTs × 12 = ≥96 property tests floor)

**BT14.a — Per-org init marker write + HMAC + verify.** Property: every `vault/init.marker` write produces a canonical-JSON body + rolling SHA-3-512 HMAC signed with `tilth.vault.init.hmac.v1`. Property: marker verify round-trips byte-identically for every valid operator_id. Adversarial: HMAC tamper (flip one byte) → verify fails; marker body tamper → HMAC fails; wrong keystore key → fails; missing `.hmac` sidecar → fails. Property: `scope="org"` markers always carry non-empty `slug`; `scope="shared"` markers always have `slug=""`.

**BT14.b — Vault-owned skill enumeration.** Property: `FDBrokerRequest.requester_skill` is exactly one of the hard-coded set `{"vault-query", "research-db-query", "vault-write"}`; any other value → denied at dispatcher preamble. Property: the enumeration constant is immutable at module-load time (frozen tuple / `Final[tuple[str, ...]]`). Adversarial: monkeypatch the enumeration set → AST-lint R7 catches at module-scope (Final preflight sentinel), or runtime re-load check denies.

**BT14.c — Cedar policy location.** Property: all three policies (`org_isolation.cedar`, `fd_issuance.cedar`, `write_gate.cedar`) live under `vault_shared/cedar/` and are loaded by `m15_ledger.cedar_policy_loader.load_all()`. Property: each file's content hash matches the seed manifest entry; drift → `F-CEDAR-01` / `F-CEDAR-02`. Adversarial: policy file outside `vault_shared/cedar/` → rejected; policy file present but not in seed manifest → tamper-evidence PRE-gate abort.

**BT14.d — `vault_shared/` signed commits.** Property: `VaultSharedSeedManifest.head_hash` equals the Merkle root over the files tuple; each `SeedFile.content_hash` is byte-identical to the on-disk canonical bytes. Property: manifest `signature` verifies against operator keyring. Property: every `vault_shared/` file not path-keyed as cache (`cached_opportunities/`, `research_db/` except `research_db/seed/`, any `/_cache/` suffix) appears in `files`. Adversarial: cache-partition seepage (file under `cached_opportunities/` appearing in seed manifest) → reject; seed file missing from manifest → `F-M15-01`; signature tamper → `F-M15-03`.

**BT14.e — PRE-gate direct-FS failure semantics.** Property: any non-vault-owned-skill path touch (io_uring, eBPF, `process_vm_readv`, `SCM_RIGHTS` outside the sanctioned broker pattern, `open_by_handle_at`, `pidfd_getfd`) → `F-DIRECT-{01,02,03,04,05}`. Property: kernel-copy denylist (`copy_file_range`, `sendfile`, `splice`, `tee`, `vmsplice`, `clonefile`, `fcopyfile`) → `F-VAULT-07` or `F-SECCOMP-*`. Property: `shm_open` / `memfd_create` / `mq_open` → `F-SECCOMP-07` (v0.1 option a). Adversarial: fuzz syscall numbers against the seccomp filter; every denied primitive surfaces a specific failure code, never silently fails.

**BT14.f — Per-org `init.marker` ceremony.** Property: ordering is floor → shared-init-verify → per-org-init-write. Property: attempting per-org init without shared-init present → `F-INIT-02`. Property: re-running ceremony on an existing per-org init is idempotent (verify only, no re-write). Adversarial: crash mid-ceremony (after floor, before shared-init verify) → next boot reconstructs from ledger tail `COMPOUND_RECOVERY_SCAN_LINES=16` without leaving partial state.

**BT14.g — Identity-tuple resolver + 4-field compare.** Property: `(volume_uuid, fs_file_id, mount_id, fs_type)` tuple uniquely identifies a file across remounts on the same volume; inode alone insufficient. Property: mount-table drift between capture and re-capture triggers cache eviction + re-capture. Property: 4-field compare inside `mirror_verify.freeze_vault_shared` Step 2 (Batch 3 Phase 2) → any field mismatch → `F-M15-01 SeedFileIdentityDrift`. Adversarial: bind-mount swap between capture and read (preserves content hash) → identity tuple drift detected; hard-link to a different volume (preserves inode) → `volume_uuid` mismatch; rename across mount boundaries → `mount_id` mismatch; fs type change (e.g., loopback remount) → `fs_type` mismatch.

**BT14.g.1 — Stable-UUID floor.** Property: `accepted=True` ⟺ `fs_type ∈ {"apfs","ext4","btrfs","zfs","xfs"}` AND `volume_uuid` parses as non-zero UUID. Property: tmpfs rejected unconditionally. Property: overlayfs rejected in v0.1 (reserved for v2 operator-signed-allowlist). Property: FUSE non-allowlisted rejected. Adversarial: spoofed volume_uuid = all-zeros → rejected; fs_type string tamper (e.g., "APFS" uppercase) → rejected if not canonical; overlayfs-on-tmpfs → rejected because lowerdir is tmpfs.

### K.3 Full boot-sequence parametric fuzz

Single harness: given a clean vault root, boot Tilth through all 19 §2 modules N times with N distinct org slugs (N parametrized over `[2, 8, 16, 32]`). Verify:

- Every boot produces a `VaultBootResult(success=True, …)` with distinct `session_id`.
- Every boot's audit ledger hash-chain terminates at a valid trailer HMAC.
- Every boot's identity-tuple mount-table snapshot is captured exactly once and reused across downstream steps.
- No cross-org file access attempts succeed (Law 3 mechanical: seat-A in org-A cannot read `orgs/org-B/vault/`).
- Atomic-freeze retains snapshots for the most recent `COV_SNAPSHOT_RETENTION_COUNT=3` orgs; older entries pruned.
- `vault_write` called across all 5 SIMPLE + 2 COMPOUND intents per org round-trips byte-identically.
- `begin_compound_txn` per org stages ≤ `MAX_STAGED_WRITES_PER_TXN=8` under `MAX_STAGED_BYTES_PER_TXN=128 MiB` (stage-cap bounds enforced via `monkeypatch` to `1024` bytes for RAM-safe test).
- Compound-txn `commit_compound_txn` succeeds under `MAX_COMPOUND_TXN_BYTES=64 MiB` undo-snapshot cap (monkeypatched to `1024` for RAM-safe test).

Counted as a single parameterized test class with ≥ N bootstraps per run.

### K.4 §7 test-suite packaging

The §7 test suite (per §2 blueprint §7 scope definition) becomes the canonical §2 test harness. Round K packages:

- `tests/vault/conftest.py` — fixture library (clean vault root, operator keypair, sample `VaultSharedSeedManifest`, sample `IdentityTuple`, `CapstoneKeyStore` pattern, `SnapshotProvider` stub, `FDBroker` stub, `isolate_active_runtime`-equivalent seam).
- `tests/vault/test_section_2_integration.py` — K.1 boot sequence + compound-txn lifecycle integration tests.
- `tests/vault/test_section_2_bt_properties.py` — eight BT14 property test classes (K.2).
- `tests/vault/test_section_2_boot_sequence_property.py` — N-vault parametric fuzz harness (K.3).

## Dependencies

- All §2 Batch 1/2/3 per-module LOCKs complete (11/11 rows as of 2026-04-22 Batch 3 Phase 2 CLOSEOUT).
- §1 Round J capstone LOCKED 2026-04-21 — Round K consumes §1 primitives via the frozen §3.2 consumer surface.
- §4 Logician runtime not consumed — Round K only references Cedar policy file hashes at blueprint-stated paths.
- §5 Pipeline runtime not consumed — Round K mocks `session_id` at fixture layer.
- AST-lint R1-R7 clean on all four test files.
- `pyproject.toml` Python pin `>=3.11` + `.venv` 3.14 — run via `scripts/run_tests.sh` or `.venv/bin/python3 -m pytest`.

## Done definition

1. All 4 test files written with ≥96 property tests across the eight §2-owned BTs (≥12 per BT) + ≥30 integration tests (K.1) + parametric fuzz harness (K.3).
2. ≥95% coverage on every §2 module via the union of per-module + cross-module tests.
3. AST-lint R1-R7 exit 0 on all test files.
4. Full suite green (baseline 5206 pass per Batch 3 Phase 2 CLOSEOUT; Round K adds ≥150 tests → suite should clear 5356+).
5. Code Thesis Committee 5/5 PASS cycle-1 on the Round K capstone surface — OR self-LOCK per §1 Round J + §3 Scout R5-R9 + §5 Pipeline R3-R12 compositional-round precedent (test-only round composing already-LOCKED primitives; every consumed module has independent committee LOCK on record).
6. Operator signs — **§2 capstone LOCKED-as-a-whole**. Promotes all of Section 2 from LOCKED-per-module to LOCKED-as-a-whole-section.
7. Canonical daily_log LOCK block per gate #12 discipline; §0.5 paired-commit rows (4 test files as Index entries); `lock_history.v1.jsonl` row with `lock_class: "code"`, `scope: "Section 2 capstone — integration + BT14 property matrix + boot-sequence parametric fuzz + §7 test suite"`.
8. MEMORY.md prepend + `memory/project_impl_section_2_round_k_capstone_locked.md`; blueprint §2 v7.1 header status line amended to include "§2 LOCKED-as-a-whole 2026-04-YY".

## Test criteria

- K.2: ≥12 property tests per BT × 8 BTs = **≥96 floor**.
- K.1: ≥15 integration tests × 8 classes (families) with ≥5 adversarial cases each parametrically ≈ **≥30 integration test methods floor**.
- K.3: parametric fuzz harness across N ∈ {2, 8, 16, 32} org slugs = **single parameterized class, ≥58 individual test instances**.
- Total floor: **≥150 tests**. E-024 capstone-shape multiplier 1.3× target ≈ 195 tests. §1 Round J landed 214 tests at 1.26× — comparable target.
- E-026 formal: use `__module__` lineage checks, not identity, for any cross-module Protocol lineage assertion.
- Stage/undo-cap RAM-safety: use `monkeypatch.setattr(_compound_txn_mod, "MAX_STAGED_BYTES_PER_TXN", 1024)` and analogous for `MAX_COMPOUND_TXN_BYTES` — mirrors Batch 3 Phase 2 compound_txn remediation discipline.
- Deterministic hash ops: canonical bytes recipe `json.dumps(obj, sort_keys=True, separators=(",",":"), ensure_ascii=False).encode("utf-8")` → SHA-3-512; no alternative encodings.
- `@dataclass(frozen=True, kw_only=True)` requirement — Python 3.10+; any `.venv` drift surfaced as collection-error, not test failure.

## §0.5 paired-commit rows

| Row | Content |
|-----|---------|
| Tests | `tests/vault/conftest.py` |
| Tests | `tests/vault/test_section_2_integration.py` |
| Tests | `tests/vault/test_section_2_bt_properties.py` |
| Tests | `tests/vault/test_section_2_boot_sequence_property.py` |
| Lock history | `pipeline/engineering/lock_history.v1.jsonl` — Round K capstone row; `lock_class: "code"`; `scope: "Section 2 capstone — integration + BT14 property matrix + boot-sequence parametric fuzz + §7 test suite"` |
| Blueprint | Update §2 v7.1 header status line to include "§2 LOCKED-as-a-whole 2026-04-YY" |
| Memory | `memory/project_impl_section_2_round_k_capstone_locked.md` + MEMORY.md prepend |
| Daily log | Canonical LOCK block per gate #12 |

## Coupling

- **Downstream unlock:** §2 capstone LOCK-as-a-whole unblocks §4 Logician Group 7 amendment enforcement (last §2-substrate precondition). With §2 LOCKED-as-a-whole and §4 v2.1 LOCKED, §4 Group 7 can consume both as stable inputs.
- **§1 Round J precedent:** Round K mirrors §1 Round J verbatim in shape; the `tests/vault/` directory receives the same four-file capstone layout (`conftest.py` + `_integration.py` + `_bt_properties.py` + `_boot_sequence_property.py`).
- **Batch 3 Phase 2 inheritance:** Round K inherits the identity-tuple re-capture defence-in-depth landed in `mirror_verify.py` Phase 2 — the K.1.b + K.2 BT14.g tests exercise this new path directly.
- **Self-LOCK candidacy:** Round K is test-only; every module it composes has an independent 5/5 PASS committee LOCK on record. §1 Round J + §3 Scout R5-R9 + §5 Pipeline R3-R12 all self-LOCKed under analogous compositional-round precedent. Round K is a strong self-LOCK candidate with the same rationale. Committee dispatch remains available if operator prefers belt-and-suspenders.

---

*Spec card v1 — 2026-04-22 — §2 Round K capstone. Promotes §2 LOCKED-per-module → LOCKED-as-a-whole-section. Dispatched immediately on spec-card LOCK — §2 Batch 3 Phase 2 CLOSEOUT + §1 Round J capstone both land the precondition set.*
