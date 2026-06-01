# Blueprint Section 2 — Vault Topology + Enforcement Envelope (v4, 2026-04-17)

**Status:** DRAFT v4 — fourth Thesis Team round. v1 round closed: Editor=READY_TO_LOCK, Judge=PASS 100/100, Red Team=REQUIRES_MAJOR_MITIGATIONS (12 HIGH + 12 MED + 5 LOW + 1 ARCHITECTURAL + 3 out-of-model). v2 round closed: Editor=READY_TO_LOCK, Judge=PASS 100/100, Red Team=REQUIRES_MINOR_FIXES (4 v1-HIGH PARTIAL + 6 new findings). v3 round closed: Editor=READY_TO_LOCK, Judge=PASS 100/100, Red Team=REQUIRES_MINOR_FIXES (0 Bucket-A, 4 Bucket-B, 4 Bucket-C — see `05_synthesis_v3.md`). Operator elected "spin v4 with the four Bucket-B hardenings applied" so that the Section 2 substrate feeding into Sections 3+ has zero known-but-deferred items rather than four filed follow-ups. This v4 applies G-01 (extended Unicode forbidden-category set), G-02 (signal-mask around HMAC-pipe read/close), G-03 (explicit import-and-argv construction invariant + AST checker extension for dynamic imports), G-04 (`_TILTH_AUDIT_PASSED` environment scrub at wrapper startup). Each is a narrow ≤ 5-line edit under an existing failure code — no new failure codes, no new §8 constants, no new mechanisms, no architectural amendments. ARCH-01 remains filed against v5-r8 at `pipeline/validation/architecture_v0.1_findings_from_section_02/ARCH-01.md` and is NOT patched in v4. Audit artefacts: `pipeline/validation/blueprint_section_02_2026-04-17/{02_editor_audit_v{1,2,3}.md, 03_judge_score_v{1,2,3}.json, 04_red_team_challenge_v{1,2,3}.md, 05_synthesis_v{1,2,3}.md}`.

Authored against Tilth architecture v0.1 = v5-r8 LOCKED 2026-04-17 (`pipeline/architecture/v0.1/tilth_architecture_locked.md`). Operator (Josh Inklovich) confirmed outline + three pre-commits 2026-04-17:
- **α primary control** = (i) Cedar-gated, Vault-owned-skill-only FD issuance broker + (ii) per-seat mount namespace (Linux) / per-seat sandbox profile (macOS). (iii) LSM hook on `open*` family noted as v2 deepening, not v0.1.
- **M15.2.1 atomic verify-and-freeze** = mount-namespace switch primary on Linux; verified-and-pinned Merkle root primary on macOS; copy-on-verify snapshot reserved for filesystems where snapshots are cheap (APFS on macOS, btrfs/zfs on Linux) and used only as a defence-in-depth layer.
- **macOS `copyfile(3)`** = vault-routed wrapper rather than library-level deny, on the reasoning that blanket deny breaks legitimate system-library call sites and forces every caller to be patched.

**v2 changelog summary** (authoritative map to §X.Y where each Bucket-A fix lands):
- A-01 (HIGH-01, openat2 ENOSYS silent fallback) → §4.1 Linux, §8 kernel floor, §6.2 `F-GATE-01` refined
- A-02 (HIGH-02, macOS ancestor-walk TOCTOU) → §4.1 macOS post-open mount-id re-verify
- A-03 (HIGH-03, prctl PR_SET_DUMPABLE re-enable) → §4.3 seccomp extension, §6.6 `F-SECCOMP-04`
- A-04 (HIGH-04, dup*/dup2/dup3 restore stdio) → §4.3 seccomp + sandbox, §6.6 `F-SECCOMP-05/F-SANDBOX-03`
- A-05 (HIGH-05, SCM_RIGHTS marker guessability) → §4.3 per-connection HMAC, §6.8 `F-FD-05`
- A-06 (HIGH-06, DYLD_INSERT_LIBRARIES clear) → §4.3 macOS env-mutation deny, §6.6 `F-SANDBOX-04`
- A-07 (HIGH-07, wrapper-hash race) → §4.5 reordered, §9 boot step 8 → 8a/8b/8c
- A-08 (HIGH-09, security.*/system.* xattrs) → §4.2 strip-all, §6.1 `F-VAULT-05`
- A-09 (HIGH-10, APFS snapshot DoS) → §4.7 retention, §8 `COV_SNAPSHOT_RETENTION_COUNT=3`, §6.10 `F-FREEZE-04`
- A-10 (HIGH-11, openbyid_np / F_GETPATH on macOS) → §4.3 macOS sandbox extension, §6.7 `F-DIRECT-02`
- A-11 (HIGH-12, mach_ports_lookup omission) → §4.8 enumeration hardening, §6.1 `F-VAULT-06`
- A-12 (MED-02, null-byte injection) → §4.1 explicit reject, §6.2 `F-GATE-05`
- A-13 (MED-05, io_uring fd inheritance) → §4.4 bootstrap invariant, §6.7 `F-DIRECT-03`
- A-14 (MED-06, broker socket hijack) → §4.3 socket protection, §6.8 `F-FD-06`
- A-15 (MED-07, /dev/fd/* bypass) → §4.1 macOS reject, §6.2 `F-GATE-06`
- A-16 (MED-08, proc_pidfdinfo) → §4.3 macOS sandbox extension, §6.7 `F-DIRECT-04`
- A-17 (MED-09, hard-link identity-tuple fool) → §4.3 canonical-path prefix check, §6.8 `F-FD-07`
- A-18 (MED-10, copyfile destination unchecked) → §4.3 macOS wrapper gates destination, §6.1 `F-VAULT-07`
- B-03 (MED-03, Unicode NFC/NFKC mismatch) → §4.1 broker NFC-normalize ingress
- B-05 (LOW-02, broker DoS backpressure) → §8 `EAGAIN` return contract
- B-06 (LOW-03, cache retention unenforced) → §9 boot step 11b cache prune
- ARCH-01 (trusted-operator nsenter gap) → filed against v5-r8; NOT patched in v2; §10 records as residual.

**v3 changelog summary** (authoritative map for the v2-synthesis Bucket-A residuals; every fix is narrow-scope and blueprint-level):
- C-01 (v2-HIGH-04 PARTIAL, `fcntl(F_DUPFD_*)` re-dup bypass of seccomp `dup*` deny) → §4.3 seccomp extension, §6.6 `F-SECCOMP-06`
- C-02 (v2-HIGH-10 PARTIAL, macOS `NSURL` bookmark resolves file-id without the denied primitives) → §4.3 macOS sandbox extension, §6.7 `F-DIRECT-05`
- C-03 (v2-HIGH-12 PARTIAL, Unicode format-control characters + percent-encoded null-byte not filtered) → §4.1 `_validate_relative_path` extension, §6.2 `F-GATE-08` / `F-GATE-09`
- C-04 (v2-new-B, HMAC key startup-pipe FD inheritable by forked children) → §4.3 broker setup + §4.5 M14.4.1 seat-start close-pipe step; tightens `F-FD-05`
- C-05 (v2-new-C, bootstrap `io_uring` created between pre-exec audit and `execve`) → §4.4 M14.3.1 ordering invariant, §9 boot step 11.5 explicit; tightens `F-DIRECT-03`
- C-06 (v2-new-D, NFC-validated path diverges under NFKC normalization downstream) → §4.1 `_validate_relative_path` NFC∧NFKC-stable check, §6.2 `F-GATE-10`
- v2-HIGH-09 PARTIAL (snapshot retention DoS under external holds) → Bucket B, NOT patched (remains surfaced via `F-FREEZE-04`); §10 F-OQ-06 stands.
- v2-new-A (bind-mount via privileged helper) → Bucket C, ARCH-01 restatement; NOT patched.
- v2-new-E (network-FS immutability no-op) → Bucket C, already covered by UUID floor; NOT patched.

**v4 changelog summary** (authoritative map for the v3-synthesis Bucket-B hardenings; no new failure codes or §8 constants):
- G-01 (RT-v3 C-03 Co/Mn/Me visual-spoofing) → §4.1 `_validate_relative_path` — extend `_UNICODE_FORBIDDEN_CATEGORIES` from `{Cf, Cc}` to `{Cf, Cc, Co, Mn, Me}`; rejects Private-Use Area + combining-mark codepoints so rails-report display cannot be fooled by path components that normalize identically but render identically to unrelated base glyphs. Same `F-GATE-08`; one-line additive edit.
- G-02 (RT-v3 C-04 signal-handler fork) → §4.5 M14.4.1 step 3 — wrap the HMAC-pipe `os.read` + `os.close` pair in `signal.pthread_sigmask(SIG_BLOCK, …)` / `SIG_UNBLOCK` so no signal handler can fire between the read and the close. Same `F-FD-05`; three-line additive edit.
- G-03 (RT-v3 C-05 lazy-import side effects) → §4.5 M14.4.1 invariant note — all `import` statements and all `os.execve` argv objects are constructed BEFORE step 8 (the final audit); no lazy import or expression on the post-audit path. §7.16 — extend the AST checker to flag `importlib.import_module` / `__import__` / dynamic `getattr`-imports reachable between the audit call site and `execve`. Same `F-DIRECT-03` (amended wording already covers the invariant); documentation + checker extension.
- G-04 (RT-v3 C-05 pre-set sentinel) → §4.5 M14.4.1 step 1 — at the very top of the wrapper, `os.environ.pop("_TILTH_AUDIT_PASSED", None)` removes any operator- or parent-injected sentinel before anything else in the wrapper runs, preventing a poisoned-environment launch from passing the runtime sentinel check. Same `F-DIRECT-03`; one-line additive edit.

**Parent architecture:** `pipeline/architecture/v0.1/tilth_architecture_locked.md` (v5-r8 LOCKED 2026-04-17). v4 preserved at `tilth_architecture_locked_v4_2026-04-16.md`; full v5 arc and per-round audits at `pipeline/validation/architecture_v5_2026-04-16/`.

**This section's job:** Specify the HOW for the Vault substrate and its enforcement envelope — the boundary where seat processes meet the filesystem. Section 1 writes the sovereignty primitives; Section 2 arranges the filesystem those primitives operate on and wires the kernel-level controls that prevent a seat from reaching outside the Vault. If this section is wrong, org isolation is wrong, Law 3 is wrong, and the sovereignty promise evaporates.

**Sections this section owns (from the architecture):**
- **Mechanisms:** M14 Vault access discipline (M14.1 atomic gate-and-open, M14.2 metadata homogenization, M14.2.1 kernel-mediated-copy denylist, M14.3 direct-FS prohibition with sub-mechanisms M14.3.1 io_uring, M14.3.2 eBPF + `perf_event_open`, M14.3.3 `SCM_RIGHTS` / `pidfd_getfd`, M14.4 crash-handler discipline with sub-mechanisms M14.4.1 ancillary suppression, M14.4.2 process-creation wrapper, M14.4.3 shm/memfd denial, M14.4.4 wrapper signed-commit discipline). M15 signed-commit discipline for `vault_shared/` seed YAML, Cedar policies, process wrappers, and Section 2 lock marker (M15.1 seed-vs-cache partition, M15.2 read-only freeze, M15.2.1 atomic verify-and-freeze, M15.3 Cedar-change HIGH-severity ledger discipline).
- **Blueprint-tracked:** BT14.a–g.1 (per-org init marker, Vault-owned skill enumeration, Cedar policy location, `vault_shared/` signed commits, PRE-gate direct-FS failure, per-org `init.marker` ceremony, `(volume UUID, FS file ID)` identity tuple, stable-UUID floor).
- **v5-r8 amendments:** α complete-mediation (M14.2.1) primary-control choice, β macOS Mach-IPC principle-level deny profile, γ N.4.2 trust-root mirror hardening, O.5.m SCM_RIGHTS from Vault-owned skill (v2 deferral annotated), O.5.n snapshot-aware mount-over guard (v2 deferral annotated).
- **Boundary artefacts:** Section 2 lock marker contract for N.4.1 (v0.1 does not operate during temporal-bridge window) and N.4.2 (operator-signed lock marker + M15 ledger commit + trust-root mirror).

**Sections this section does NOT own:** Router binding and sovereignty primitives (Section 1). Scout discovery surface, Channel A-F ingest, Brave Search BYOK envelope (Section 3 — Scout). Cedar policy authoring, policy enforcement decisions, claim-evidence map, rails report (Section 4 — Logician). Section 2 wires the Cedar loader but does not write policy text. Pipeline choreography, inter-seat routing, council orchestration, M13 bypass authorization UI (Section 5 — Pipeline). Every write Section 2 produces is verified by Section 4 on read; Section 2 writes, Section 4 verifies.

**Trusted-operator threat-model boundary (stated up front, referenced throughout):**

Section 2 trusts the operator's keyring (same trust root as Section 1), signed commits to `vault_shared/` on the operator's keyring, operator-signed N.4.2 lock markers, and the operator's hardware physical integrity. Section 2 does NOT trust seat-process code (every seat is treated as potentially-compromised; the envelope assumes the seat will attempt path trickery, symlink plants, watermark rollback, and non-privileged file-write escapes), LLM outputs, web-fetched content prior to Section 1 materialization, or any process sharing the seat's uid that the operator did not start themselves.

**In-scope threats (v0.1):** path trickery (`..` traversal, symlink plants, magic-link traversal, relative-path escape, null-byte injection, Unicode normalization attacks), watermark rollback at mirror, non-privileged file-write by a seat reaching outside its org root, seat attempting to read another org's Vault contents, seat attempting to write to `vault_shared/` during runtime, seat attempting to open a file via a primitive not mediated by the Vault-owned skill (io_uring, eBPF, `process_vm_readv`, `SCM_RIGHTS` fd-passing, `open_by_handle_at`, `pidfd_getfd`), seat attempting to read watermarked state via a copy primitive that bypasses the read gate (`copy_file_range`, `sendfile`, `splice`, `tee`, `vmsplice`, `clonefile`, `fcopyfile`), and seat attempting to escalate via Mach IPC on macOS (`task_for_pid`, `host_get_special_port`, `bootstrap_port` reparenting, `mach_port_insert_right`).

**Out-of-scope threats (v0.1):** same-uid hostile code that the operator deliberately started (architecture §K; trusted-operator), compromised operator keyring, hostile OS kernel, physical device seizure, side-channel attacks (timing, cache, power) — O.5.a/b reserved for v2. Multi-client shared hardware under a single Golden Quill instance is A3 = v2; A1 (single-client-per-Golden-Quill) and A2 (operator dev multi-client under A4 trusted-operator) are the only v0.1 preflight configurations. Temporal-bridge operation (N.4.1) is explicitly out-of-scope for v0.1 — Section 2 defines what the N.4.2 lock marker must contain so Section 5 pipeline start can refuse to launch during the window.

**v0.1 constraints:**
- Runs on Josh's M1 Mac Mini 8 GB dev. Everything in this section must fit comfortably in that envelope. Production target is 32 GB+; if v0.1 runs on 8 GB it flies on 32 GB.
- Headless only. No UI. No web server. No WebSocket.
- BYOK only. No Anthropic-hosted key material. No third-party key escrow.
- Fail-closed. Every failure path halts the pipeline cleanly rather than silently degrading. The one allowed "degraded" state (M13 review-seat bypass) is Section 1's responsibility; Section 2 treats M13 as an opaque flag that Section 4 reads.
- Single-client-per-Golden-Quill (A1). A2 operator-dev multi-client is permitted because A4 (operator-trusted) covers the same-uid concurrent-writer concern.

---

## 1. Module inventory

All modules live at `pipeline/vault/` relative to the repo root. Section 2 ships as a Python package importable as `from pipeline.vault import <name>`. Most modules have no runtime LLM dependency; the two first-class Vault-owned skills (`vault-query`, `research-db-query`) are skill-backed but their invocation surface is Python — the skill is the policy, the module is the enforcement.

| # | Module | Lines (target) | Owns |
|---|---|---|---|
| 1 | `__init__.py` | ~40 | Public API surface, version pin, module-level boot guard |
| 2 | `layout.py` | ~220 | `VaultLayout` — canonical paths for `orgs/{slug}/vault/…`, `vault_shared/…`, `~/.tilth/logician_trust_root/…`; reserved-slug guard (delegated to Section 1's topology but re-verified at Vault layer); path-keyed partition of seed vs cache under `vault_shared/` |
| 3 | `init_marker.py` | ~180 | BT14.a + BT14.f — per-org `vault/init.marker` write + HMAC + verify; per-Vault `vault_shared/init.marker`; ceremony ordering (floor check → shared-init verify → per-org init write) |
| 4 | `identity_tuple.py` | ~200 | BT14.g — `(volume UUID, FS file ID)` tuple resolver; macOS (`statfs.f_fsid` + `getattrlist` `ATTR_CMN_FILEID`); Linux (`statx` with `STATX_MNT_ID` + `stx_ino`); cache eviction when mount table changes |
| 5 | `uuid_floor.py` | ~140 | BT14.g.1 — stable-UUID floor PRE-gate; APFS / ext4+UUID / btrfs / zfs / xfs accepted; tmpfs / overlayfs-on-tmpfs / FUSE (non-allowlisted) = PRE-gate abort |
| 6 | `gate_and_open.py` | ~360 | M14.1 — atomic gate-and-open. Linux: `openat2(RESOLVE_NO_SYMLINKS | RESOLVE_NO_MAGICLINKS | RESOLVE_BENEATH)`. macOS: `open(O_NOFOLLOW)` + post-open `fstat` + ancestor-chain `openat` verification. Both platforms: identity-tuple re-check against the Vault pinning table |
| 7 | `metadata_homogenizer.py` | ~260 | M14.2 — timestamp floor, size-bucket enforcement, xattr strip on materialization, path-name scrubbing for cache pages |
| 8 | `kernel_copy_denylist.py` | ~280 | M14.2.1 — enumerates the denied primitive family; installs seccomp filter (Linux) / `sandbox_init` profile (macOS); provides the vault-routed wrapper for `copyfile(3)` on macOS |
| 9 | `direct_fs_prohibition.py` | ~240 | M14.3 — PRE-gate failure detector when a non-vault-owned skill touches the filesystem outside the broker; io_uring deny (M14.3.1), eBPF + `perf_event_open` deny (M14.3.2), `SCM_RIGHTS` / `pidfd_getfd` deny (M14.3.3) |
| 10 | `crash_handler.py` | ~220 | M14.4 + M14.4.1 — crash-handler routed through Vault-owned write; exit-without-write if Vault-owned skill is unreachable; `RLIMIT_CORE=0`, stdio → `/dev/null`, `atexit` disabled, OS crash-reporter opt-out |
| 11 | `process_wrapper.py` | ~340 | M14.4.2 + M14.4.4 — process-creation wrapper for seat launch; systemd unit (Linux), launchd plist (macOS), fallback shell wrapper; signed-commit hash re-verify at exec; `vault_shared/process_wrappers/` read-only remount coordinator |
| 12 | `shm_memfd_denial.py` | ~120 | M14.4.3 — seccomp deny `shm_open` + `memfd_create` + `mq_open` (v0.1 option a only; option b — tmpfs unsharing — deferred to v2) |
| 13 | `fd_broker.py` | ~400 | α primary control — Cedar-gated, Vault-owned-skill-only FD issuance broker; only process that holds a raw inode FD; serves FDs to seats via `SCM_RIGHTS` from this process (the ONE sanctioned caller, architecture §O.5.m noted); Cedar policy loader plugs in here |
| 14 | `mount_namespace.py` | ~280 | α secondary control (Linux) — per-seat mount namespace preparation; `unshare(CLONE_NEWNS)` with private propagation; bind-mounts the org Vault subtree read-write and `vault_shared/` read-only; refuses to start if namespace support is missing |
| 15 | `sandbox_profile.py` | ~240 | α secondary control (macOS) — per-seat `sandbox_init(2)` profile; deny Mach-IPC primitives (β); deny privileged file ops outside the issued FDs; profile text loaded from `vault_shared/sandbox_profiles/` (M15 signed) |
| 16 | `mach_ipc_deny.py` | ~160 | β macOS — principle-level Mach-IPC deny enumeration; generates the sandbox-profile fragment consumed by `sandbox_profile.py`; deny list = `mach_msg_trap` send-right to privileged ports, `task_for_pid`, `host_get_special_port`, `host_set_special_port`, `mach_port_insert_right`, `bootstrap_port` reparenting, `clonefile`, `clonefileat`, `fcopyfile`, `copyfile(3)` (routed via wrapper, not denied) |
| 17 | `trust_root_mirror.py` | ~300 | γ N.4.2 — `~/.tilth/logician_trust_root/` mirror verifier; `chattr +i` / `chflags uchg` on mirror file + directory + grandparent; post-open `fstat` (st_dev, st_ino) against signed manifest; signed-manifest format (operator signature + M15-ledger-head hash + identity tuple) |
| 18 | `m15_ledger.py` | ~340 | M15 signed-commit discipline; ledger head read; hash re-verify for `vault_shared/` seed; ledger commit for Cedar-policy changes (HIGH-severity + operator re-type via Section 1's `admin_risk` bridge); append-only commit history |
| 19 | `atomic_freeze.py` | ~280 | M15.2.1 — atomic verify-and-freeze mechanism. Linux primary: mount-namespace switch + `mount --bind -o remount,ro`. macOS primary: verified-and-pinned Merkle root over `vault_shared/` with freeze carried in an in-process immutable snapshot reference. Snapshot-based defence-in-depth via APFS snapshot / btrfs subvol / zfs clone, guarded by O.5.n snapshot-aware mount-over check (v2-deferred for the stronger guard) |
| 20 | `vault_query_skill.py` | ~260 | Vault-owned first-class skill — read path; exposes `vault_read(path, intent)`; all reads go through `fd_broker.request_fd()`; returns materialized content with metadata homogenized |
| 21 | `research_db_query_skill.py` | ~220 | Vault-owned first-class skill — research-DB read path; thin layer over `vault_query_skill` plus research-DB index; honours org isolation by rejecting cross-org index keys |
| 22 | `vault_write.py` | ~300 | Vault-owned write path; only callers allowed are `crash_handler.py`, `fd_broker.py` ceremony paths, and Section 5 pipeline's save-on-success / save-on-failure hook; all writes are atomic (tmp → fsync → rename) inside an `fcntl.LOCK_EX` on `vault/.write.lock`; cross-org writes PRE-gate abort |
| 23 | `boot.py` | ~280 | Vault boot sequence: UUID floor → mirror verify → M15 seed verify → atomic freeze → wrapper hash verify → FD broker online → seat launch authorized |

Total target: ~5,400 lines. Larger than Section 1 because Section 2 has to enumerate the OS-level envelope on two platforms and the cross-cutting denylists are verbose by nature. Still small enough to hold in one developer's head; `layout.py` + `boot.py` together are the two files a new reviewer should start with.

**Split rationale:** `fd_broker.py`, `mount_namespace.py`, and `sandbox_profile.py` are three files because α is a primary control with two platform implementations; factoring the broker out of the namespace/profile modules lets the broker be tested against an in-process fake that does not touch the kernel. `kernel_copy_denylist.py` is separate from `shm_memfd_denial.py` because the denylists are conceptually distinct (copy family vs. shared-memory family) even though both are seccomp/`sandbox_init` filters; keeping them separate lets the seccomp filter be assembled by composition rather than one monolithic blob. `mach_ipc_deny.py` is separate from `sandbox_profile.py` because Mach-IPC deny is the principle-level β amendment and the enumeration needs to be inspectable on its own — reviewers should be able to diff the Mach deny list without reading the whole sandbox profile.

---

## 2. Data-structure schemas + on-disk layout

All schemas live as Python `dataclasses.dataclass(frozen=True, kw_only=True)`. JSON serialization via `dataclasses.asdict` + `json.dumps(..., sort_keys=True, separators=(",", ":"))` for deterministic hashing. Timestamps UTC, ISO-8601, suffix `Z`. Hashes hex-encoded SHA-3-512 (128 chars). Identity tuples carried as `(volume_uuid_hex, fs_file_id_hex)` pairs.

### 2.1 `IdentityTuple`

```python
@dataclass(frozen=True, kw_only=True)
class IdentityTuple:
    volume_uuid: str          # 32 hex chars (UUID of the filesystem volume)
    fs_file_id: str           # hex — macOS: ATTR_CMN_FILEID; Linux: stx_ino (with STATX_MNT_ID as volume anchor)
    mount_id: str             # hex — Linux statx STATX_MNT_ID; macOS fsid.val[0]:fsid.val[1]
    fs_type: str              # "apfs" | "ext4" | "btrfs" | "zfs" | "xfs"
    captured_at: str          # UTC ISO-8601
```

**Invariant:** `(volume_uuid, fs_file_id)` together uniquely identify a file across mount remounts on the same volume; inode alone is insufficient (BT14.g restates this — inode collisions across volumes are common, and a remount can change the inode number while the file stays the same on some filesystems). `mount_id` is carried alongside for diagnostic symmetry with the Linux `STATX_MNT_ID` field and macOS `f_fsid` pair.

### 2.2 `StableUUIDFloor`

```python
@dataclass(frozen=True, kw_only=True)
class StableUUIDFloor:
    fs_type: str
    volume_uuid: str
    accepted: bool            # True if fs_type is in the allowlist
    rejection_reason: str     # empty if accepted; otherwise e.g. "tmpfs-not-allowed"
    evaluated_at: str
```

**Invariant:** `accepted = True` ⟺ `fs_type ∈ {"apfs", "ext4", "btrfs", "zfs", "xfs"}` AND `volume_uuid` parses as a non-zero UUID. Overlayfs is accepted only if the lowerdir and upperdir both sit on an allowlisted filesystem AND the operator has signed an allowlist entry for this specific mount path (v0.1: not supported; PRE-gate abort). tmpfs is rejected unconditionally — ephemeral volumes cannot hold watermarks.

### 2.3 `VaultInitMarker`

```python
@dataclass(frozen=True, kw_only=True)
class VaultInitMarker:
    scope: str                # "shared" | "org"
    slug: str                 # "" for shared, org slug for per-org
    created_at: str
    created_under_uuid: str   # volume_uuid at creation
    identity_tuple: IdentityTuple  # captured at creation for this marker file itself
    operator_id: str          # keychain identifier
    section_lock_hash: str    # SHA-3-512 hex of the Section 2 lock marker at creation
```

Paired with `…/init.marker.hmac` — rolling SHA-3-512 HMAC over canonical JSON of the marker body, signed with keystore key `tilth.vault.init.hmac.v1`. Scope `"shared"` lives at `vault_shared/init.marker`; scope `"org"` lives at `orgs/{slug}/vault/init.marker`. Shared init must exist and verify before any per-org init is written.

### 2.4 `VaultSharedSeedManifest`

```python
@dataclass(frozen=True, kw_only=True)
class VaultSharedSeedManifest:
    head_hash: str                     # SHA-3-512 hex of the Merkle root over all seed files
    files: tuple[SeedFile, ...]        # ordered, canonical-path-sorted
    committed_at: str
    committed_by: str                  # operator_id from keyring
    m15_ledger_head: str               # ledger head hash at commit time
    signature: str                     # operator signature over head_hash + m15_ledger_head

@dataclass(frozen=True, kw_only=True)
class SeedFile:
    relative_path: str                 # under vault_shared/
    content_hash: str                  # SHA-3-512 hex of canonical file bytes (LF, no trailing whitespace)
    size_bytes: int
    mode: int                          # stat mode masked to 0o7777
    identity_tuple: IdentityTuple      # captured at commit time
```

**Invariant:** The seed manifest is the source of truth for what's frozen read-only after boot. Every file under `vault_shared/` that is NOT path-keyed as cache (see §2.9 on-disk layout) MUST appear in `files`. Any seat-observed file under `vault_shared/` that is not in the seed manifest and not in a cache partition is a PRE-gate failure — the Vault treats it as tamper evidence.

### 2.5 `TrustRootMirrorManifest`

```python
@dataclass(frozen=True, kw_only=True)
class TrustRootMirrorManifest:
    mirror_path: str                   # absolute, typically ~/.tilth/logician_trust_root/router.yaml
    content_hash: str                  # SHA-3-512 hex of canonical file bytes
    identity_tuple: IdentityTuple
    m15_ledger_head: str               # ledger head hash at manifest creation
    operator_signature: str            # operator signature over (content_hash, identity_tuple, m15_ledger_head)
    signed_at: str
    immutability_flag_set: bool        # True ⟺ chattr +i (Linux) or chflags uchg (macOS) succeeded on the file + directory + grandparent
```

**Invariant:** On every boot, Section 2 (a) re-fetches the identity tuple of the mirror file, (b) recomputes its content hash, (c) re-reads the manifest, (d) verifies the manifest's operator signature, (e) compares manifest.content_hash against the recomputed hash and manifest.identity_tuple against the freshly-captured tuple. Mismatch at (e) = `F-MIRROR-01 TrustRootMirrorIdentityMismatch` or `F-MIRROR-02 TrustRootMirrorContentMismatch`. Manifest signature fails = `F-MIRROR-03 TrustRootMirrorSignatureMismatch`. Immutability flag absent on any of the three targets (file, directory, grandparent) at boot = `F-MIRROR-04 TrustRootMirrorImmutabilityMissing`. All four are fail-closed.

### 2.6 `ProcessWrapperManifest`

```python
@dataclass(frozen=True, kw_only=True)
class ProcessWrapperManifest:
    platform: str                     # "linux-systemd" | "macos-launchd" | "fallback-shell"
    wrapper_path: str                 # under vault_shared/process_wrappers/
    content_hash: str
    identity_tuple: IdentityTuple
    m15_ledger_head: str
    mode: int                         # must be 0o550 (r-x, owner only can read+execute; group can execute)
```

**Invariant:** The wrapper is an M15-signed artefact. After PRE-gate verify succeeds, `vault_shared/process_wrappers/` is remounted read-only (Linux) or the directory is `chflags uchg`'d (macOS). Immediately before each seat-launch, the Logician (Section 4 consumer) re-reads the wrapper file via `fd_broker.request_fd()` and recomputes `content_hash`; mismatch = `F-WRAPPER-01 WrapperHashMismatchAtExec` = seat-launch refused.

### 2.7 `FDBrokerRequest` / `FDBrokerResponse`

```python
@dataclass(frozen=True, kw_only=True)
class FDBrokerRequest:
    requester_skill: str               # "vault-query" | "research-db-query" | "vault-write"
    requester_pid: int
    requester_session_id: str          # Section 1 session binding
    requester_org_slug: str
    requested_path: str                # org-root-relative or vault_shared-relative
    intent: str                        # "read" | "write" | "execute"
    nonce_hex: str                     # 32 bytes, per-request

@dataclass(frozen=True, kw_only=True)
class FDBrokerResponse:
    granted: bool
    denial_reason: str                 # "" if granted
    fd_count: int                      # 1 on grant, 0 on deny
    issued_at: str
    identity_tuple: IdentityTuple      # captured when the FD was opened by the broker
    cedar_decision_id: str             # for audit trail
```

**Invariant:** Only the broker process ever holds a raw inode FD. Seats receive FDs via `SCM_RIGHTS` on a Unix domain socket (architecture §O.5.m identifies this as the ONE sanctioned use of `SCM_RIGHTS`; all other `SCM_RIGHTS` traffic is denied by seccomp). The FD is opened AFTER a Cedar decision says "allow", pinned by identity tuple, and closed on the broker side immediately after transmission — the broker holds no dangling FDs. Request nonces are recorded in Section 1's nonce registry to prevent replay.

### 2.8 `SeccompFilterManifest` / `SandboxProfileManifest`

```python
@dataclass(frozen=True, kw_only=True)
class SeccompFilterManifest:
    platform: str                      # "linux"
    filter_bpf_hash: str               # SHA-3-512 hex of the compiled BPF program bytes
    denied_syscalls: tuple[str, ...]   # canonical syscall names, sorted
    m15_ledger_head: str
    operator_signature: str

@dataclass(frozen=True, kw_only=True)
class SandboxProfileManifest:
    platform: str                      # "macos"
    profile_text_hash: str             # SHA-3-512 hex of the SBPL text (canonical LF, no trailing whitespace)
    denied_primitives: tuple[str, ...] # "mach_msg_trap-send", "task_for_pid", "clonefile", etc.
    m15_ledger_head: str
    operator_signature: str
```

**Invariant:** Both filter and profile are M15-signed. The Linux seccomp filter is compiled once at wrapper-bake time; its BPF hash is recorded in the manifest. At seat launch, `process_wrapper.py` re-compiles the filter and compares the BPF hash against the manifest — mismatch aborts launch. On macOS, the sandbox profile text is hashed directly; drift = `F-SANDBOX-01 SandboxProfileHashMismatch`.

### 2.9 On-disk layout

All paths absolute, relative to the operator's home where applicable. Trailing slashes denote directories.

```
<repo-root>/
├── orgs/
│   ├── ORG_INDEX.md
│   ├── _TEMPLATE/                           (blank PROJECT_CONTEXT, no vault)
│   └── {slug}/
│       ├── PROJECT_CONTEXT.md
│       └── vault/
│           ├── init.marker                  (VaultInitMarker JSON)
│           ├── init.marker.hmac
│           ├── .write.lock                  (fcntl LOCK_EX target; empty file)
│           ├── subscribed_feeds/            (per-org subscribed feed snapshots)
│           ├── project_context/             (sealed envelopes per session)
│           ├── drafts/                      (per-RFA draft directories)
│           ├── contracts/                   (signed engagement docs)
│           ├── audit/                       (append-only per-org audit ledger, per §4.4 below)
│           └── state/                       (interrupted-state checkpoints, consumed by Section 5)
├── vault_shared/
│   ├── init.marker
│   ├── init.marker.hmac
│   ├── seed_manifest.json                   (VaultSharedSeedManifest, M15-signed)
│   ├── seed_manifest.sig                    (operator signature)
│   ├── cedar/
│   │   ├── org_isolation.cedar
│   │   ├── fd_issuance.cedar
│   │   ├── write_gate.cedar
│   │   └── policy_head.json                 (ledger head at policy last-commit)
│   ├── process_wrappers/
│   │   ├── linux-systemd/tilth-seat@.service
│   │   ├── macos-launchd/com.tilth.seat.plist
│   │   └── fallback-shell/seat-launch.sh
│   ├── sandbox_profiles/                    (macOS SBPL text, per seat kind)
│   ├── seccomp_filters/                     (Linux BPF bytecode, per seat kind)
│   ├── cached_opportunities/                (Scout cache partition — MUTABLE, not in seed manifest)
│   ├── research_db/                         (research DB — MUTABLE index; read-only seed under research_db/seed/)
│   └── sources/                             (M15-signed source material references — seed)
└── ~/.tilth/
    └── logician_trust_root/
        ├── router.yaml                      (mirror of repo-root router.yaml, chattr +i / chflags uchg)
        ├── manifest.json                    (TrustRootMirrorManifest)
        └── manifest.sig                     (operator signature)
```

**Seed vs cache partition (M15.1):** Under `vault_shared/`, paths matching these prefixes are **CACHE** (mutable, excluded from seed manifest, not frozen by atomic freeze): `cached_opportunities/`, `research_db/` (except `research_db/seed/` which is seed), and any subdirectory explicitly path-keyed with suffix `/_cache/`. Everything else under `vault_shared/` is SEED and MUST be listed in `seed_manifest.json`. The partition is path-keyed (no content inspection needed at boot).

**Reserved slugs:** The org slug `_shared`, `_template`, `_TEMPLATE`, `init`, `audit`, `logician`, `tilth`, and `.tilth` are rejected by `layout.py`'s slug guard (Section 1's `org_slug.py` does the primary canonicalization; Section 2 re-verifies to prevent drift).

---

## 3. Interfaces in / out

### 3.1 `pipeline.vault.__init__`

Public re-exports:
- `VaultLayout`, `VaultBootResult`
- `fd_broker.request_fd`, `fd_broker.release_fd`
- `vault_read`, `vault_write`, `research_db_read`
- `verify_trust_root_mirror`, `verify_vault_shared_seed`, `verify_process_wrapper`
- Failure-code constants (`F-VAULT-*`, `F-GATE-*`, `F-MIRROR-*`, `F-WRAPPER-*`, `F-UUID-*`, `F-SECCOMP-*`, `F-SANDBOX-*`, `F-CEDAR-*`)

No LLM calls, no network. Every function is either deterministic Python, a seccomp-bpf assemble, a `sandbox_init` call, a `mount` / `unshare` syscall, or a signed-manifest verify.

### 3.2 Primitives consumed from Section 1

Section 2 calls into Section 1 for:
- `within_org_root(path, slug)` — canonical-path + inode-snapshot TOCTOU closure (Section 1 `isolation.py`).
- `canonical_path(path)` — symlink-resolved path (Section 1 `topology.py`).
- `reserved_slug_guard(slug)` — slug rule enforcement (Section 1 `org_slug.py`).
- `hmac_audit_writer(ledger_path, payload)` — append-only HMAC-chained write (Section 1 `audit.py`).
- `atomic_flush(tmp, final)` — tmp → fsync → rename atomic (Section 1 `interrupted_state.py`).
- `safe_open_lock_file(path)` — O_NOFOLLOW + post-open fstat against parent readdir (Section 1 `isolation.py`).
- `per_session_hmac_key(session_id)` — Section 1 `session.py`.
- `nonce_registry.reserve(nonce_hex)` — prevents FD-broker request replay (Section 1 `keys.py`).
- `sovereignty_init_marker_verify()` — gates every boot (Section 1 `audit.py`).
- `boot_clock_history.last_boot_wall_ns()` — used to detect clock-rollback at mirror-verify time (Section 1 `audit.py`).

Section 1 does NOT import from Section 2. The dependency is one-way.

### 3.3 Surfaces offered to Section 3 (Scout)

- `vault_read(path, intent="read", session_id, slug)` → `bytes` + `IdentityTuple`. Scout reads cached opportunities, subscribed feeds, research DB entries through this function.
- `research_db_read(key, session_id, slug)` → `bytes` + `IdentityTuple`. Thin wrapper; enforces cross-org key rejection.
- `vault_write(path, bytes_, intent="write", session_id, slug)` → acknowledgement record. Scout writes verified opportunities through this path ONLY; never touches the filesystem directly. Cross-org write = PRE-gate abort.

### 3.4 Surfaces offered to Section 4 (Logician)

- `cedar_policy_loader.load(category)` → policy source text + M15 head hash. Logician reads Cedar text for its enforcement engine; Section 2 guarantees the text matches the signed manifest.
- `fd_broker_register_post_gate(hook)` → binds a Logician callback that is invoked AFTER a Cedar "allow" decision but BEFORE the FD is issued. The hook can veto; veto = FD issuance refused.
- `seccomp_manifest.head()` / `sandbox_profile_manifest.head()` → exposes the M15-signed manifest for Logician to include in its rails report.
- `direct_fs_prohibition.pre_gate_detector(path, caller)` → returns a failure code if a non-vault-owned skill touched the filesystem. Logician consumes this in its PRE-gate sweep.

### 3.5 Surfaces offered to Section 5 (Pipeline)

- `save_on_success(session_id, slug, payload)` → routes through `vault_write` with intent="state-success".
- `save_on_failure(session_id, slug, payload, reason)` → routes through `vault_write` with intent="state-failure".
- `seat_launch(seat_kind, session_id, slug)` → prepares mount namespace (Linux) or sandbox profile (macOS), verifies wrapper hash, brings FD broker online for this seat, exec's the wrapper. Returns PID on success; raises `F-WRAPPER-01` / `F-SECCOMP-02` / `F-SANDBOX-01` / `F-NS-01` on failure.

### 3.6 N.4.1 / N.4.2 lock-marker contract

Section 2 defines the canonical lock-marker format at `vault_shared/section_02.lock.json`:

```python
@dataclass(frozen=True, kw_only=True)
class SectionLockMarker:
    section: str = "02-vault-topology"
    version: str                       # e.g., "v1"
    locked_at: str
    locked_by: str                     # operator_id from keyring
    architecture_head_hash: str        # SHA-3-512 of the architecture file at lock time
    blueprint_content_hash: str        # SHA-3-512 of this blueprint file at lock time
    m15_ledger_head: str
    operator_signature: str
```

- **N.4.1:** v0.1 does not operate during the temporal-bridge window. Section 5 pipeline-start reads `section_02.lock.json` and refuses to launch if any of (a) signature invalid, (b) architecture_head_hash drifted from current architecture file, (c) m15_ledger_head not in the current ledger. The pipeline does not try to bridge or reconcile — it aborts and asks the operator to produce a new lock after re-audit.
- **N.4.2:** The lock marker is the operator-signed handshake. It lives under `vault_shared/` (therefore M15-signed). Trust-root mirror (§2.5) is the separate, stronger artefact that survives `vault_shared/` corruption.

---

## 4. Mechanism implementations

### 4.1 M14.1 — Atomic gate-and-open

**Intent:** Every file open inside the Vault must resolve path components, symlinks, and magic links in a single kernel-atomic operation so that no attacker can swap a path component between resolve and open.

**Pre-gate input validation (both platforms, performed before any syscall):**
```python
import unicodedata
import urllib.parse

# Unicode General_Category "Cf" is format controls (RIGHT-TO-LEFT OVERRIDE U+202E,
# zero-width joiner/non-joiner U+200C/U+200D, Mongolian vowel separator U+180E,
# BOM U+FEFF, ...). "Cc" is C0/C1 control characters. "Co" is Private-Use Area
# (U+E000-U+F8FF, U+F0000-U+FFFFD, U+100000-U+10FFFD) — application-defined glyphs
# with no fixed visual semantics; a downstream font/renderer can map them to
# anything, so rails-report display cannot be trusted to distinguish them from
# legitimate path components. "Mn"/"Me" are non-spacing/enclosing combining marks
# — a base letter plus a visually-invisible combining mark has the same
# apparent form as the base letter alone, so rails-report display of a vault
# path cannot be trusted to reveal such components. None of Cf/Cc/Co/Mn/Me
# belong in a legitimate vault path. (G-01, v4: Co/Mn/Me added — security is
# provided by codepoint-level resolution, but rails-report display integrity
# requires rejecting visually-ambiguous categories as well.)
_UNICODE_FORBIDDEN_CATEGORIES = {"Cf", "Cc", "Co", "Mn", "Me"}

def _validate_relative_path(relative_path: str) -> str:
    # A-12: null-byte injection reject (before any path split).
    if "\x00" in relative_path:
        raise VaultOpenRejected(path=relative_path, reason="path-contains-null", code="F-GATE-05")

    # C-03 (v3): percent-encoded null-byte (%00) reject — some API callers decode URL
    # escapes late; if anything downstream decodes %00 into \x00, the earlier \x00
    # check gets bypassed. Reject BEFORE any decoding step.
    if "%00" in relative_path.lower():
        raise VaultOpenRejected(path=relative_path, reason="path-contains-percent-null", code="F-GATE-09")

    # C-03 (v3, extended G-01 v4): Unicode format-control / control-character /
    # private-use / combining-mark reject. RIGHT-TO-LEFT OVERRIDE, zero-width
    # joiner/non-joiner, private-use codepoints (which the renderer can map to
    # anything), and non-spacing/enclosing combining marks (which are visually
    # invisible on a base letter) can all make two visually-identical paths
    # differ in resolution OR make a legitimate-looking rails-report hide a
    # different path from the operator. Reject any path containing a character
    # in General_Category Cf (format), Cc (control), Co (private use),
    # Mn (non-spacing mark), or Me (enclosing mark).
    for ch in relative_path:
        if unicodedata.category(ch) in _UNICODE_FORBIDDEN_CATEGORIES:
            raise VaultOpenRejected(
                path=relative_path,
                reason=f"path-unicode-forbidden-category-{unicodedata.category(ch)}-{ord(ch):04x}",
                code="F-GATE-08",
            )

    # B-03: Unicode normalization pin. Incoming path must be byte-for-byte identical
    # to its NFC form.
    if unicodedata.normalize("NFC", relative_path) != relative_path:
        raise VaultOpenRejected(path=relative_path, reason="path-unicode-nonnormal", code="F-GATE-07")

    # C-06 (v3): NFC-NFKC divergence reject. NFC-equal strings can still differ under
    # NFKC (compatibility decomposition), e.g. fullwidth 'Å' vs ASCII 'Å'. If a
    # downstream library does its own NFKC resolution, it may open a different file
    # than we validated. Reject paths whose NFC form differs from their NFKC form.
    if unicodedata.normalize("NFC", relative_path) != unicodedata.normalize("NFKC", relative_path):
        raise VaultOpenRejected(path=relative_path, reason="path-nfc-nfkc-divergence", code="F-GATE-10")

    # A-15 (macOS-primary, belt-and-suspenders on Linux): reject /dev/fd synthetic paths.
    canon = os.path.normpath(relative_path)
    if canon.startswith(("/dev/fd/", "/dev/stdin", "/dev/stdout", "/dev/stderr")):
        raise VaultOpenRejected(path=relative_path, reason="dev-fd-synthetic", code="F-GATE-06")
    return canon
```

**Linux (primary):**
```python
import os

RESOLVE_FLAGS = (
    os.RESOLVE_NO_SYMLINKS
    | os.RESOLVE_NO_MAGICLINKS
    | os.RESOLVE_BENEATH
)

def gate_and_open(vault_root_fd: int, relative_path: str, flags: int) -> int:
    relative_path = _validate_relative_path(relative_path)  # null, NFC, /dev/fd
    how = {
        "flags": flags | os.O_CLOEXEC,
        "mode": 0,
        "resolve": RESOLVE_FLAGS,
    }
    # openat2 is invoked via ctypes against the openat2 syscall (SYS_openat2 = 437)
    fd = _openat2_syscall(vault_root_fd, relative_path, how)
    if fd == -errno.ENOSYS:
        # A-01: kernel < 5.6. NO fallback. Abort boot-time or request-time.
        raise VaultOpenRejected(
            path=relative_path,
            reason="openat2-unavailable",
            code="F-GATE-01",
            detail="kernel < 5.6; Tilth v0.1 requires openat2; upgrade kernel.",
        )
    if fd < 0:
        raise VaultOpenRejected(path=relative_path, errno=-fd, code="F-GATE-01")
    return fd
```
- `vault_root_fd` is an FD obtained once at boot, after `mount_namespace.py` has switched into the per-seat namespace.
- **Kernel floor (v2 pin):** Linux 5.6 or later. The boot-time probe (§9 step 2a) runs `openat2` on a test file and aborts with `F-GATE-01 openat2-unavailable` if `ENOSYS` is returned. No fallback path exists. Rationale: the weak-fallback pattern observed in v1 allowed path-trickery escape on older kernels; v2 closes this by refusing to boot.
- `RESOLVE_BENEATH` guarantees that `relative_path` cannot escape `vault_root_fd` via `..`. `RESOLVE_NO_SYMLINKS` rejects any symlink component. `RESOLVE_NO_MAGICLINKS` rejects `/proc/*/fd/*` magic-link traversal.
- Post-open, the FD's `statx(..., STATX_BASIC_STATS | STATX_MNT_ID, ...)` is compared against the Vault pinning table for this org — mismatch = `F-GATE-02 GateIdentityTupleMismatch`.

**macOS (primary):**
```python
import os

def gate_and_open(vault_root_fd: int, relative_path: str, flags: int) -> int:
    relative_path = _validate_relative_path(relative_path)  # null, NFC, /dev/fd
    parts = relative_path.split("/")
    # A-02: keep every ancestor FD open across the walk, so we can re-stat and
    # re-verify after the leaf is opened. This defeats the TOCTOU window where
    # a bind-mount-over the parent could make the leaf resolve to an attacker
    # file while the ancestor check still passes.
    ancestor_fds: list[int] = [os.dup(vault_root_fd)]
    ancestor_tuples_pre: list[tuple[int, int]] = []
    for i, name in enumerate(parts[:-1]):
        if name in ("", ".", ".."):
            _close_all(ancestor_fds)
            raise VaultOpenRejected(path=relative_path, reason="reserved-component", code="F-GATE-01")
        next_fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=ancestor_fds[-1])
        _fstat_and_check(next_fd, expected_parent=ancestor_fds[-1])
        # Capture the ancestor's (st_dev, st_ino) BEFORE descending.
        pre_stat = os.fstat(next_fd)
        ancestor_tuples_pre.append((pre_stat.st_dev, pre_stat.st_ino))
        ancestor_fds.append(next_fd)
    leaf = parts[-1]
    fd = os.open(leaf, flags | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=ancestor_fds[-1])
    # A-02: post-open re-stat of every ancestor FD. If any ancestor's
    # (st_dev, st_ino) changed between the initial capture and now, a mount-over
    # occurred mid-walk. The ancestor FDs are still valid (kernel holds them
    # open across mounts), so re-fstat sees the CURRENT inode behind each fd.
    for idx, (pre_dev, pre_ino) in enumerate(ancestor_tuples_pre):
        post_stat = os.fstat(ancestor_fds[idx + 1])
        if (post_stat.st_dev, post_stat.st_ino) != (pre_dev, pre_ino):
            os.close(fd)
            _close_all(ancestor_fds)
            raise VaultOpenRejected(
                path=relative_path,
                reason="ancestor-mount-over",
                code="F-GATE-03",
                detail=f"ancestor[{idx+1}] drift: {pre_dev}:{pre_ino} -> "
                       f"{post_stat.st_dev}:{post_stat.st_ino}",
            )
    _fstat_and_check_identity(fd, expected_tuple=_lookup_pinning(relative_path))
    _close_all(ancestor_fds)
    return fd
```
- `openat2` is not available on macOS; the ancestor-chain `openat` walk plus `O_NOFOLLOW` at every step, **plus** the post-open re-stat of every ancestor FD (A-02), is the closest approximation to atomic resolution.
- `_fstat_and_check` verifies that the opened FD's `st_dev` matches the parent FD's `st_dev` (prevents cross-mount substitution) and that `st_ino` is not zero.
- `_fstat_and_check_identity` verifies `(st_dev, st_ino)` against the Vault pinning table for this org, keyed by canonical relative path.
- **Residual caveat (ARCH-01):** if the operator's own shell with `CAP_SYS_ADMIN` enters the seat's mount namespace via `nsenter` and performs a `mount(2)` between the broker's pinning capture and the seat's read, this re-verify cannot catch it. That gap is architectural, not blueprint-level; see §10 and `pipeline/validation/architecture_v0.1_findings_from_section_02/ARCH-01.md`.

**Failure modes:**
- `F-GATE-01 GateOpenRejected` — kernel refused the open (ENOTDIR, ELOOP, EACCES, etc.), or Linux `openat2` returned `ENOSYS` (kernel < 5.6; NO fallback), or a reserved-component (`""`, `.`, `..`) was seen in the walk.
- `F-GATE-02 GateIdentityTupleMismatch` — file opened but identity tuple drifted from pinning table.
- `F-GATE-03 GateAncestorMountMismatch` — macOS post-open ancestor re-stat detected drift (§4.1 A-02); alternate trigger: `st_dev` change during walk.
- `F-GATE-04 GateMagicLinkRejected` — Linux `RESOLVE_NO_MAGICLINKS` fired on `/proc/*/fd/*` traversal.
- `F-GATE-05 GatePathNullByte` — `\x00` in the incoming relative path (A-12).
- `F-GATE-06 GateDevFdRejected` — canonical path begins with `/dev/fd/` or `/dev/stdin|stdout|stderr` (A-15).
- `F-GATE-07 GatePathUnicodeNonNormal` — incoming path not byte-identical to its NFC form (B-03).

All are fail-closed: the open returns no FD; the caller gets an exception; Section 4 logs the failure via Section 1's HMAC audit writer.

### 4.2 M14.2 — Metadata homogenization

**Intent:** Seat-visible file metadata (mtime, ctime, atime, size, path name) MUST NOT leak information that could be used to fingerprint the operator's working cadence or to correlate organization data across boundaries.

**Mechanism:**
- **Timestamp floor:** Every materialized file served to a seat has its `st_mtime` and `st_ctime` projected to the most-recent second-boundary before the Vault-boot wall-clock. Access time is suppressed entirely (seats get `st_atime == st_mtime`).
- **Size bucketing (for cache pages only):** Files served from `cached_opportunities/` and `research_db/` caches are padded on-the-wire to the next bucket in `{4 KiB, 64 KiB, 1 MiB, 16 MiB, 256 MiB}`. Seed files are served at true size (they are M15-signed and re-verifiable; padding would break re-verification). **Known residual leakage:** the bucket choice itself leaks the size-class of the underlying file (an attacker who reads a cached file learns whether it was < 4 KiB, < 64 KiB, etc.). Constant-time per-file padding (same padded size for every cache page regardless of content) is the O.5.a v2 hardening target and remains correctly deferred; v0.1 treats size-class leakage as in-scope under the trusted-operator threat model because a seat that can already read a cache page it's authorized to see gains only size-class information, not content it wasn't already authorized to access.
- **Xattr strip (A-08, all namespaces):** Every FD handed to a seat has all four xattr namespaces stripped before hand-off — `user.*`, `trusted.*`, `security.*`, `system.*` (Linux) and all Finder/Spotlight/quarantine xattrs (macOS). The broker iterates `listxattr`, then calls `removexattr` for each key, then asserts `listxattr` returns an empty list. If any xattr remains at hand-off time, the FD is closed and the request fails with `F-VAULT-05 VaultXattrStripIncomplete`. There is no allowlist in v0.1; any xattr handed through would be a leak of operator-scoped metadata (e.g., SELinux labels, POSIX ACLs, macOS quarantine marks) across the sovereignty boundary.
- **Path-name scrubbing for cache pages:** Cache files are served under their content-hash as filename; original filenames are never exposed to the seat.

**Linux implementation:** metadata homogenization is applied by the FD broker between `openat2` and FD hand-off — the broker wraps each outgoing FD in an `io_uring`-free proxy that overrides `fstat`/`fstatat` results via a small per-FD shadow table. Since seats' io_uring is denied (§4.5.1), and `fstat` is routed through libc, this is sufficient. Xattr strip uses `listxattr(fd, NULL, 0)` to size, `listxattr(fd, buf, size)` to enumerate, then `fremovexattr(fd, key)` for each, across all four namespaces. Unit test `test_metadata_homogenizer_strips_all_namespaces` asserts empty `listxattr` on every broker-issued FD.

**macOS implementation:** same mechanism; `fstat` / `fstatat` results are overridden by the FD broker's shadow table. Xattr strip uses `flistxattr` / `fremovexattr` with `XATTR_NOFOLLOW`. `copyfile(3)` wrapper (§4.4) also scrubs xattrs by default — but the broker is the authoritative stripper; the wrapper is belt-and-suspenders.

### 4.3 M14.2.1 — Kernel-mediated-copy denylist

**Intent:** Prevent seats from reading (or exfiltrating) file content via copy primitives that bypass the homogenization layer by operating at the kernel level on raw FDs rather than going through `read()`.

**Linux denylist (seccomp filter, compiled at wrapper-bake, loaded by `process_wrapper.py` before exec):**
- `copy_file_range` (SYS_copy_file_range, 326)
- `sendfile` / `sendfile64` (40 / 239)
- `splice` (275)
- `tee` (276)
- `vmsplice` (278)
- `process_vm_readv` (310)
- `process_vm_writev` (311)
- `perf_event_open` (298)
- `sendmsg` / `recvmsg` when the ancillary type is `SCM_RIGHTS` — v2 replaces v1's static setsockopt magic marker (A-05) with a **per-connection HMAC-SHA-256 tag** derived from `HMAC(broker_session_secret, request_nonce || seat_euid || socket_cookie)`. The broker verifies the tag in userspace **before** calling `recvmsg(..., MSG_CMSG_CLOEXEC)`. The seccomp filter continues to deny any `sendmsg`/`recvmsg` with `msg_controllen > 0` from a non-broker peer; the HMAC adds application-level authentication so that a seat guessing the seccomp-level marker cannot forge a handoff. The broker session secret is 32 random bytes generated at broker start, stored only in broker address space, never logged, never handed to a seat. Verification failure → `F-FD-05 SCMRightsAuthFailed`.
  - **C-04 (v3) per-connection HMAC key delivery — startup-pipe FD hygiene:** the per-seat HMAC key (§8 `FD_BROKER_HMAC_KEY_LENGTH_BYTES = 32`) is delivered from broker to seat over an anonymous `pipe2(O_CLOEXEC | O_DIRECT)` pair created in the broker; the seat inherits only the read-end. To close the forked-child leak path identified in v2, v3 pins three ordering invariants: (1) the broker creates the pipe with `O_CLOEXEC` at `pipe2()` time (no window where the FD is not `FD_CLOEXEC`-marked); (2) the seat wrapper, immediately after reading the 32 key bytes, calls `close(startup_pipe_fd)` BEFORE any further code path that might `fork(2)` — this is part of the §4.5 M14.4.1 seat-start sequence; (3) the seat wrapper additionally calls `fcntl(startup_pipe_fd, F_SETFD, FD_CLOEXEC)` as a belt-and-suspenders against any clone between pipe-create and the explicit close. The seat process is sandbox-restricted so that post-key-read `fork*` / `clone*` / `posix_spawn` are all denied via seccomp / sandbox profile; together with the explicit `close()`, no child of the seat can ever observe the key. Key material never appears in environment variables, command-line arguments, `/proc/self/environ`, `/proc/self/cmdline`, or `ps(1)` output.
- **A-03 (prctl PR_SET_DUMPABLE):** `prctl` seccomp-filtered — any invocation with `arg0 == PR_SET_DUMPABLE` (4) or `arg0 == PR_SET_PTRACER` (0x59616d61) is denied with `SECCOMP_RET_KILL_PROCESS`. Other `prctl` ops used by CPython at startup (`PR_SET_NAME`, `PR_GET_NAME`, `PR_SET_NO_NEW_PRIVS`) remain allowed. The seccomp-bpf filter checks `arg0` via `BPF_LD|BPF_W|BPF_ABS` on `offsetof(seccomp_data, args[0])`. Emits `F-SECCOMP-04 SeccompPrctlDumpableDenied`.
- **A-04 (dup/dup2/dup3):** `dup`, `dup2`, `dup3` seccomp-denied after wrapper redirects stdio. The wrapper sets a process-wide flag via `prctl(PR_SET_NO_NEW_PRIVS)` and then loads a seccomp filter that treats `dup*` as `SECCOMP_RET_KILL_PROCESS`. Rationale: after wrapper has redirected FDs 0/1/2 to `/dev/null` and set `FD_CLOEXEC` on every other FD, the seat has no legitimate reason to duplicate an FD except via the broker's `SCM_RIGHTS` path. Denying `dup*` closes the stdio-restore attack. Emits `F-SECCOMP-05 SeccompDupDenied`.
- **C-01 (v3) `fcntl(F_DUPFD*)` closure:** seccomp filter is extended with an argument-inspecting rule on `fcntl(fd, cmd, arg)`: if `cmd ∈ {F_DUPFD, F_DUPFD_CLOEXEC}` → `SECCOMP_RET_KILL_PROCESS`. Rationale: v2 closed `dup/dup2/dup3` but left `fcntl(F_DUPFD_*)` as an alternate path to duplicate an FD; a seat could use it to restore stdio or to escape the broker's sole-caller guarantee on `SCM_RIGHTS` FDs. The filter inspects `args[1]` and emits `F-SECCOMP-06 SeccompFcntlDupDenied`. The `fcntl` allowlist (for `F_GETFL`, `F_SETFL`, `F_GETFD`, `F_SETFD`, `F_GETPATH`-on-broker-FD) continues to be enforced; only the `F_DUPFD*` commands are killed. macOS sandbox mirrors with `(deny file-fcntl (fcntl-command F_DUPFD F_DUPFD_CLOEXEC))`, emitting `F-SECCOMP-06` (cross-platform; sandbox failure path unified under the same code).
- `shm_open` (implemented as `openat` with a specific path prefix — also denied here for the copy-family case) / `memfd_create` (319) — see §4.5.3.
- `open_by_handle_at` (304) + implicit `CAP_DAC_READ_SEARCH` — denied.
- `io_uring_setup` (425), `io_uring_enter` (426), `io_uring_register` (427) — see §4.5.1.

**macOS denylist (`sandbox_init(2)` profile, loaded by `process_wrapper.py` via `sandbox-exec`):**
- `clonefile` / `clonefileat` — denied outright.
- `fcopyfile` — denied outright.
- `copyfile(3)` — routed via `vault-routed wrapper` (the operator-accepted choice). The wrapper lives at `vault_shared/process_wrappers/macos-launchd/copyfile_wrapper.dylib`, interposed via `DYLD_INSERT_LIBRARIES`. **v2 hardening:**
  - **Source validation (unchanged):** the source FD must be broker-issued; the wrapper holds a broker-issued FD table and rejects any source FD not in that table.
  - **A-18 destination gating:** the wrapper performs a full `_validate_relative_path` + ancestor-chain walk against the destination path (same as §4.1 macOS), so that `copyfile(src_broker_fd, "/tmp/evil", ...)` is rejected with `F-VAULT-07 VaultCopyfileDestinationOutsideVault`. The destination's canonical resolved path MUST sit beneath the org's `vault_root` or `cached_opportunities/` subtree.
  - **A-17 identity re-check at copy time:** the wrapper calls `fcntl(src_fd, F_GETPATH, buf)` **and** `fstat(src_fd)` immediately before the copy; the resolved path AND identity tuple must both match what the broker captured at FD issuance. Renaming or hard-linking the source after issuance → `F-FD-07 FDHardlinkOutsideVault`.
  - **Belt: hard-link creation denied at sandbox:** `(deny file-link* (subpath "/"))` except within the org's own vault subtree. Hard-linking vault content outside the vault is denied at the sandbox layer in addition to being caught by the broker's canonical-path check.
  - **A-06 DYLD interposer enforcement:** the sandbox profile adds `(deny process-exec* (env-override-any "DYLD_INSERT_LIBRARIES" "DYLD_LIBRARY_PATH" "DYLD_FALLBACK_LIBRARY_PATH" "DYLD_FALLBACK_FRAMEWORK_PATH" "DYLD_IMAGE_SUFFIX" "DYLD_INSERT_OVERRIDE" "DYLD_FORCE_FLAT_NAMESPACE"))`, which denies any `execve`, `posix_spawn`, or `posix_spawnp` that would clear, alter, or re-inject DYLD-family environment variables. Additionally, the wrapper library's `__attribute__((constructor))` initializer asserts that `_dyld_image_count()` returns a count consistent with the wrapper being loaded — if the constructor detects the wrapper was not loaded into this process, it aborts with `SIGTERM` (child process dies immediately; parent receives `F-SANDBOX-04 SandboxDYLDBypassDetected`).
- **Mach-IPC primitives — see §4.8 β (v2 extended deny list).**
- **A-10 (openbyid_np):** `openbyid_np` explicitly denied in sandbox profile via `(deny syscall-unix (syscall-number SYS_openbyid_np))`. Additionally, `fcntl(F_GETPATH)` is denied on any FD whose owner (per broker table) is not the seat's own process (seats may `F_GETPATH` on broker-issued FDs — they learn nothing new; but not on arbitrary FDs). Emits `F-DIRECT-02 MacosOpenbyidDenied`.
- **C-02 (v3) `NSURL` bookmark closure:** Foundation's `NSURL` bookmark resolution (`URLByResolvingBookmarkData:` / `CFURLCreateByResolvingBookmarkData`) reaches the kernel via `getattrlistbulk`, `fsgetpath`, and a Mach-service lookup of `com.apple.FileCoordinationHelper` — not via `openbyid_np`, so the A-10 sandbox rule alone does not cover it. The v3 sandbox profile adds: `(deny mach-lookup (global-name "com.apple.CoreServices.coreservicesd"))`, `(deny mach-lookup (global-name "com.apple.FileCoordinationHelper"))`, and `(deny file* (subpath "/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/"))` to block the bookmark-resolver helper daemons. Additionally `(deny iokit-open (iokit-user-client-class "IOHIDEventSystemUserClient"))` blocks the alternate CF-URL persistence path. A Vault-owned skill that needs a persistent file reference MUST use the broker's `(canonical_path, identity_tuple)` handle; bookmarks are explicitly not a Vault primitive. Emits `F-DIRECT-05 MacosNSURLBookmarkDenied`.
- **A-16 (proc_pidfdinfo):** `proc_pidfdinfo`, `proc_pidinfo`, `proc_pid_rusage` added to macOS sandbox deny list. These are the macOS equivalents of Linux `/proc/*/fd/*` enumeration and allow a seat to enumerate or duplicate FDs from other processes. Emits `F-DIRECT-04 MacosProcPidInfoDenied`.
- **Legacy (still enforced):** `open_by_handle_at` equivalent on macOS is `openbyid_np`; denied (now called out explicitly per A-10).

**FD broker hardening (A-05, A-14, A-17, both platforms):**
- **A-14 (broker socket hijack):** broker socket is created at `orgs/{slug}/vault/.broker.sock` (Linux) or `~/.tilth/sessions/{session_id}/broker.sock` (macOS), **not** `/tmp`. Immediately after `bind()`:
  1. `chmod(socket, 0o700)`.
  2. `chown(socket, operator_euid, operator_egid)`.
  3. Linux: `chattr +i` on the socket inode (via `ioctl FS_IOC_SETFLAGS` on the parent directory's FD — socket inode immutability works on ext4, xfs, btrfs; zfs requires the equivalent `chflags`). macOS: `chflags uchg`.
  4. On every `accept(2)`, broker verifies `SO_PEERCRED.euid == operator_euid` (Linux) / `LOCAL_PEEREPID + proc_pidinfo` (macOS). Mismatch → `F-FD-06 BrokerSocketPeerMismatch`, connection closed, ledger-logged.
- **A-17 (hard-link identity-tuple fool):** At FD issuance, broker captures `(canonical_path, st_dev, st_ino)` via `fcntl(F_GETPATH)` (macOS) / `readlink("/proc/self/fd/N")` (Linux). The canonical path MUST resolve under `orgs/{slug}/vault/` or the allowed cache subtree. A file that shares `(st_dev, st_ino)` with a vault file but whose canonical path is elsewhere (hard-linked out) → rejected with `F-FD-07 FDHardlinkOutsideVault`. Additionally, hard-link creation outside vault is denied at the sandbox profile level (macOS) and via seccomp `linkat`/`link` filtering on Linux when the destination dirfd/path resolves outside the org subtree.
- **A-05 (SCM_RIGHTS marker):** see Linux denylist above; broker HMAC-verifies every `recvmsg(SCM_RIGHTS)` peer.

**Failure modes:**
- `F-SECCOMP-01 SeccompFilterCompileFailure` — filter BPF compile failed at wrapper bake.
- `F-SECCOMP-02 SeccompFilterHashMismatch` — filter compiled at exec does not match manifest hash.
- `F-SECCOMP-03 SeccompSyscallRejected` — seat attempted a denied syscall; SIGSYS delivered, seat terminates (the seccomp action is `SECCOMP_RET_KILL_PROCESS` for denied syscalls in v0.1).
- `F-SECCOMP-04 SeccompPrctlDumpableDenied` — `prctl(PR_SET_DUMPABLE, …)` or `prctl(PR_SET_PTRACER, …)` attempted (A-03).
- `F-SECCOMP-05 SeccompDupDenied` — `dup`/`dup2`/`dup3` attempted after wrapper stdio redirect (A-04).
- `F-SANDBOX-01 SandboxProfileHashMismatch` — macOS profile text hash drift.
- `F-SANDBOX-02 SandboxProfileApplyFailure` — `sandbox_init` returned non-zero.
- `F-SANDBOX-03 SandboxDupDenied` — macOS sandbox denied `dup*` (A-04, mirror of F-SECCOMP-05).
- `F-SANDBOX-04 SandboxDYLDBypassDetected` — wrapper constructor saw itself missing in a child process (A-06).

### 4.4 M14.3 — Direct-FS prohibition family

**Intent:** Any filesystem access from a seat that bypasses the Vault-owned skill layer is a PRE-gate failure — detected, logged, and (where the kernel permits) prevented before it completes.

**Detection path:** Seats do not hold raw filesystem access capability. The per-seat mount namespace (Linux) restricts their visible filesystem to the bind-mounted org Vault (read-write) plus `vault_shared/` (read-only) plus `/dev/null`, `/dev/urandom`, and `/proc/self/*` (with `/proc/*/fd/*` magic-link-denied via seccomp). The per-seat sandbox profile (macOS) denies file-read/write outside the seat's allowed subtree. Attempting to `open` anything outside = `F-DIRECT-01 DirectFSAccessDetected`.

**M14.3.1 io_uring denial:** `io_uring_setup` seccomp-denied; the syscall returns `ENOSYS` to the seat. This denies the entire io_uring surface, including the SQE-based path traversals that bypass `openat2` RESOLVE flags. v2 may relax this if a vault-owned io_uring broker is built; v0.1 blanket denies.

**A-13 bootstrap invariant (NEW in v2):** The bootstrap process (parent of all seats) MUST NOT create or hold any `io_uring` FD at any point during or after Vault-boot. If a seat inherits a bootstrap-held io_uring FD across `fork`/`execve`, the seat could issue `io_uring_enter`/`io_uring_register` on the inherited FD without ever calling the seccomp-denied `io_uring_setup`. Enforcement:
1. **Pre-exec audit:** just before `execve(seat_binary)`, `process_wrapper.py` enumerates `/proc/self/fd/` (Linux) or `proc_pidinfo(PROC_PIDFDINFO)` (macOS) and asserts that no FD resolves to a pathname containing `[io_uring]` or `io_uring:*`. Any hit → `F-DIRECT-03 IoUringFDInherited` → seat launch refused.
2. **Static invariant:** the bootstrap binary is written to NOT use `io_uring` anywhere in its codepath. A lint rule in CI greps the bootstrap for `io_uring_setup` / `io_uring_enter` / `io_uring_register` / `liburing` imports; any hit fails CI.
3. **Runtime guard:** the wrapper sets `FD_CLOEXEC` on every FD numbered ≥ 3 before exec (Python default), so even if a stray io_uring FD somehow existed in the bootstrap, it would close across exec. The `CLOEXEC` sweep plus the pre-exec audit is belt-and-suspenders.
4. **C-05 (v3) audit→execve ordering invariant:** the pre-exec audit (item 1) must be the FINAL code path executed by `process_wrapper.py` before `execve(2)`. No syscalls — in particular, no `io_uring_setup`, `eventfd`, `timerfd_create`, `signalfd`, `userfaultfd`, `pidfd_open`, `memfd_create`, `socket`, `pipe*`, `epoll_create*`, `inotify_init*`, `open*`, or any other FD-creating primitive — may run between the audit and the `execve`. Enforced at three levels: (a) the code is arranged so that the audit is textually the last statement before the `os.execve(...)` call, with no intervening Python expressions that could trigger implicit syscalls; (b) a static-analysis assertion in §7.16 parses `process_wrapper.py`'s AST and fails CI if any non-`execve` syscall wrapper is reachable on the post-audit path; (c) at runtime, immediately after the audit, the wrapper sets a sentinel environment variable `_TILTH_AUDIT_PASSED=1` in its own `os.environ`, then calls `execve` — the sandbox/seccomp loader in the seat checks for the sentinel and refuses to initialise if it is absent (detecting a `process_wrapper.py` build where the audit was skipped). Any violation → `F-DIRECT-03 IoUringFDInherited` (wording amended in v3 to cover the audit-to-execve race, not only inherited-FD cases).

**M14.3.2 eBPF + `perf_event_open` denial:** `bpf(2)` seccomp-denied (all commands). `perf_event_open(2)` seccomp-denied. Tracing subsystems (`tracefs`, `/sys/kernel/debug/tracing`) are not mounted in the seat namespace. This closes the eBPF-based side channels and the perf-event side channels.

**M14.3.3 `SCM_RIGHTS` / `pidfd_getfd` denial:** `SCM_RIGHTS` is denied for all seat-originated `sendmsg` / `recvmsg` calls (see §4.3). `pidfd_getfd(2)` is seccomp-denied. This closes the FD-passing side channels. The single sanctioned caller — the FD broker — runs as a separate process in a separate namespace (its own, not the seat's), not subject to the seat's seccomp filter, and uses a setsockopt magic-marker socket to pass FDs to seats via `SCM_RIGHTS` on the ONE sanctioned path.

**Architecture §O.5.m deferral:** The SCM_RIGHTS-from-Vault-owned-skill pattern is acknowledged in architecture v5-r8 as a v2 hardening target — the v0.1 implementation uses the broker-side-effect pattern (broker is trusted, runs outside seat namespace). v2 will harden the broker's privileged position with additional constraints (HSM-backed authenticated path between broker and seat). v0.1 does NOT attempt to pre-implement v2.

### 4.5 M14.4 — Crash-handler discipline

**Intent:** A crashing seat must NOT leave ancillary artefacts on disk (core dumps, tmp files, shm segments) that either expose organization data or create attack surface for the next seat.

**M14.4 primary:** Crash-handler routed through Vault-owned write. If the handler can reach the Vault-owned skill, it writes an incident record via `vault_write(…, intent="crash")`. If not, it exits without writing — a missing crash record is preferable to a leaked one.

**M14.4.1 ancillary suppression at seat-start:** `process_wrapper.py` sets before `execve`, in this exact order:
1. **G-04 (v4) sentinel-environment scrub + `RLIMIT_CORE`.** As the very first wrapper action, `os.environ.pop("_TILTH_AUDIT_PASSED", None)` removes any caller-injected value of the C-05 runtime sentinel, so that the sentinel can only ever be set by the wrapper's own post-audit code in step 8 (never inherited from the operator's shell, a parent orchestrator, or a surrounding systemd/launchd unit-environment). This scrub is unconditional and idempotent; the `None` default makes it a no-op when the variable is absent. Immediately after the scrub, `setrlimit(RLIMIT_CORE, (0, 0))` — no core dumps.
2. stdio redirected: `dup2(open("/dev/null", O_RDWR), 0); dup2(…, 1); dup2(…, 2)` — no stdout/stderr leakage. Performed **before** loading the seccomp filter in step 6, because the filter denies further `dup*` (A-04) after load.
3. **C-04 (v3) HMAC startup-pipe read-and-close, with G-02 (v4) signal-mask guard.** The wrapper blocks the full synchronous-signal set before touching the startup pipe: `signal.pthread_sigmask(signal.SIG_BLOCK, set(range(1, signal.NSIG)) - {signal.SIGKILL, signal.SIGSTOP})` is called immediately before the `os.read`. Inside this blocked window, `os.read(startup_pipe_fd, FD_BROKER_HMAC_KEY_LENGTH_BYTES)` reads the 32 HMAC key bytes from the broker-created pipe (the read-end is the only FD the seat inherits from the broker beyond stdio), and `os.close(startup_pipe_fd)` runs immediately after — with signals still blocked. Only once the pipe FD is gone from the process does the wrapper call `signal.pthread_sigmask(signal.SIG_UNBLOCK, …)` to restore the inherited mask. This guarantees no signal handler (including one inherited from the bootstrap) can fire between the read and the close to observe or duplicate the pipe FD; it also removes the window in which a fork-calling handler could fire and inherit the FD. This step is ordered BEFORE the FD_CLOEXEC sweep in step 4 and BEFORE seccomp load in step 7 so that the close is unconditional (neither `close` nor the pipe-FD read is denied at this point). The close happens BEFORE the wrapper performs any `fork`/`clone`/`posix_spawn` (there are no such calls in the wrapper's post-read path; any future drift is caught by the §7.16 static-analysis assertion that forbids fork-family calls between step 3 and `execve`). The key bytes are stored in a module-scope `bytes` object; the wrapper does NOT pass them via env/argv, and relies on the seat's own initialisation to pick them out of a well-known inherited slot (per-process memory, not visible to any child because the seat is sandbox-denied from forking post-seccomp).
4. `FD_CLOEXEC` set on every FD ≥ 3 (iterates `/proc/self/fd/`; macOS iterates `proc_pidinfo`). Combined with the bootstrap io_uring invariant (A-13) and the C-04 explicit-close in step 3, this guarantees no FD leaks across `execve` except the three redirected stdio FDs.
5. `atexit` handlers disabled: Python's `sys.unraisablehook` set to a no-op; `signal.signal(SIGTERM, …)` set to `os._exit(1)` without `atexit` call.
6. OS crash-reporter opt-out:
   - Linux: `echo 0 > /proc/sys/kernel/core_pattern` NOT done (that's global); instead, `prctl(PR_SET_DUMPABLE, 0)` set — process cannot be ptraced, core dumped, or have its `/proc/self/mem` read. **A-03:** `prctl(PR_SET_DUMPABLE, 1)` and `prctl(PR_SET_PTRACER, …)` are then seccomp-denied (§4.3), so a seat cannot later re-enable dumpability.
   - macOS: `setrlimit(RLIMIT_CORE, 0)` + `prctl` equivalent is missing, but the sandbox profile denies file creation under `/cores/` and `/Library/Logs/DiagnosticReports/`. `dup*` is also denied via sandbox profile (A-04) to mirror Linux.
7. seccomp filter loaded (Linux) / sandbox profile applied (macOS). After this point, `dup*`, `prctl(PR_SET_DUMPABLE)`, `prctl(PR_SET_PTRACER)`, `fcntl(F_DUPFD*)` (C-01), and the full kernel-copy/Mach-IPC deny lists are enforced.
8. **C-05 (v3) final pre-execve audit.** The bootstrap io_uring FD-inheritance audit (see §4.4 M14.3.1 item 1) runs HERE, as the last step before `execve`, with no intervening syscalls. See §9 step 11.5 for the boot-sequence placement.
9. `execve(seat_binary)`.

**G-03 (v4) import-and-argv construction invariant.** All `import` statements in `process_wrapper.py` and every object that is referenced in the `os.execve(path, argv, env)` call — specifically every element of `argv` and every value in `env` — MUST be constructed before step 8 (the audit) begins. Concretely: (a) `process_wrapper.py` does all its imports at module top; lazy imports, `importlib.import_module(...)`, `__import__(...)`, and dynamic `getattr(module, name)` resolution are forbidden anywhere in the file, not just on the post-audit path. (b) `argv` and `env` are assembled into concrete `list[str]` / `dict[str, str]` objects earlier in the wrapper (alongside the signature-verified wrapper-manifest read at step 5 area) and are not reconstructed, reformatted, or lazily interpolated after step 7. (c) No object reachable from `argv` or `env` has a `__repr__`, `__str__`, or `__index__` method that performs I/O or a syscall — these elements are plain `str` / `bytes` / `dict` primitives, never user-defined classes. The §7.16 AST checker (see below) enforces (a) and part of (b); a code-review invariant + a mypy stubs assertion enforce (c). This invariant is why step 8's audit can be treated as final even though CPython's argument-list evaluation runs between the audit and the `execve` syscall: no evaluation can trigger a hidden import or I/O because every referenced object is already a materialized primitive.

**M14.4.2 process-creation wrapper:** Every seat is launched via one of:
- **Linux:** `systemd-run --scope --unit=tilth-seat-{session}-{slug}-{seat_kind}` with a unit file at `vault_shared/process_wrappers/linux-systemd/tilth-seat@.service`. Unit spec:
  - `CapabilityBoundingSet=` (empty — no capabilities).
  - `NoNewPrivileges=yes`.
  - `SystemCallFilter=` (loads the seccomp manifest's BPF bytecode by path).
  - `PrivateMounts=yes`, `PrivateNetwork=yes` (except for seats that need network — Scout only; others blanket-deny), `PrivateTmp=yes`.
  - `ProtectSystem=strict`, `ProtectHome=tmpfs` except for the bind-mounted Vault subtree.
  - `MemoryDenyWriteExecute=yes`, `RestrictAddressFamilies=AF_UNIX` (plus `AF_INET` / `AF_INET6` for Scout only, via an overriding drop-in).
- **macOS:** `launchctl submit` (or direct `launchd` plist install) with a plist at `vault_shared/process_wrappers/macos-launchd/com.tilth.seat.plist`. Plist spec:
  - `SandboxProfile` pointing to the per-seat SBPL under `vault_shared/sandbox_profiles/{seat_kind}.sbpl`.
  - `UserName` = operator uid (same-uid — architecture A4 trusted-operator).
  - `EnvironmentVariables` = minimal (no `DYLD_*`, no `PATH` beyond `/usr/bin:/bin`).
- **Fallback shell:** `vault_shared/process_wrappers/fallback-shell/seat-launch.sh` — used only when systemd / launchd are unavailable (e.g., tests). The shell script `setrlimit`s, `prctl`s, loads the seccomp filter via `libseccomp`'s `seccomp_load` wrapper, and `exec`s the seat. Not considered production-grade; Section 4 Logician's rails report flags any seat launched via the fallback as "reduced-confidence envelope".

**M14.4.3 shm/memfd denial:** `shm_open`, `memfd_create`, `mq_open` seccomp-denied at seat level. v0.1 uses option (a) only (blanket deny). Option (b) — unshared tmpfs + shm namespace — deferred to v2 (it's more permissive and needs its own mount-namespace wiring which v0.1 does not have the budget to test across three OSes).

**M14.4.4 wrapper signed-commit discipline (v2 reordered per A-07):** The three wrapper files are M15-signed artefacts under `vault_shared/process_wrappers/`. v1's order (hash → remount) created a race window where a privileged bootstrap process could swap the wrapper file between the hash compute and the remount. v2 closes the window by **freezing the directory first, then verifying against the now-immutable file bytes.**

At Vault boot, `process_wrapper.py` performs these steps in this strict order:
1. **Freeze first.** `vault_shared/process_wrappers/` is made immutable:
   - **Linux:** bind-mount `-o remount,ro` on the directory. If this fails, boot aborts with `F-WRAPPER-03 WrapperRemountFailed`. No verification is attempted on a writable directory.
   - **macOS:** `chflags uchg` on the directory and on each wrapper file. Failure → `F-WRAPPER-03`.
2. **Re-confirm mount state.** `statvfs(dir).f_flag` has `ST_RDONLY` set (Linux); or `getattrlist(dir, ATTR_CMN_FLAGS)` shows `UF_IMMUTABLE` (macOS). Mismatch → `F-WRAPPER-03`.
3. **Read through broker.** For each wrapper file, `fd_broker.request_fd(path, intent="read-wrapper")` (Vault-owned read path, privileged bootstrap mode). The FD is valid only for this bootstrap operation and is closed immediately after step 5.
4. **Hash.** Recompute SHA-3-512 hex from the broker-issued FD bytes. Because the directory is already read-only, a concurrent swap is impossible — the kernel refuses the write.
5. **Compare.** Check against `ProcessWrapperManifest.content_hash`. Mismatch → `F-WRAPPER-01 WrapperHashMismatchAtBoot`; boot aborts.
6. **Mode check.** `WRAPPER_FILE_MODE = 0o550` (§8). Mode drift → `F-WRAPPER-04 WrapperExecutionBit`; boot aborts.

Immediately before each seat-launch (not just at boot), Logician (Section 4) re-reads the wrapper file hash via `fd_broker.request_fd()` — this catches the case where the operator's storage was corrupted mid-day between Vault-boot and seat-launch (e.g., disk bitflip against a still-readable inode). The directory remains read-only; re-hash just confirms the stored content. Mismatch at exec-time = `F-WRAPPER-02 WrapperHashMismatchAtExec` = seat-launch refused.

**Why this order defeats A-07:** a privileged bootstrap cannot write to a read-only bind mount / immutable directory. The hash is computed on bytes the kernel has made physically unwriteable. Any attempt to replace the file between step 1 and step 5 fails at the kernel layer with `EROFS` (Linux) or `EPERM` (macOS), and the bootstrap is flagged via the ledger.

### 4.6 M15 — Signed-commit discipline for `vault_shared/`

**Intent:** Every file under `vault_shared/` that is not explicitly cache must be verifiable against an operator-signed manifest committed to the M15 ledger.

**Mechanism:** At boot, `m15_ledger.py`:
1. Reads `vault_shared/seed_manifest.json` and `vault_shared/seed_manifest.sig`.
2. Reads the ledger head hash from Section 1's sovereignty ledger (`sovereignty/ledgers/m15_commits.jsonl.hmac` trailer).
3. Verifies the operator signature over `(head_hash, m15_ledger_head)` using the operator's public key (from keyring).
4. For each file in `files`:
   - Re-opens via `fd_broker.request_fd()` (broker is bootstrapping; has a privileged startup mode that permits seed verification).
   - Computes SHA-3-512 of canonical bytes.
   - Compares against `SeedFile.content_hash` and `SeedFile.identity_tuple`.
5. If all files verify, the seed is accepted. Atomic freeze (§4.7) is invoked. If ANY file fails, boot aborts with `F-M15-01 SeedManifestFileMismatch`.

**M15.1 seed-vs-cache partition:** Enforced by path-prefix check before adding files to the seed manifest scan. The partition is static and path-keyed — no content inspection. This prevents a bogus file planted under `cached_opportunities/` from being interpreted as seed.

**M15.2 read-only freeze after verify:** See §4.7.

**M15.3 Cedar-change HIGH-severity ledger discipline:** Any change to `vault_shared/cedar/*.cedar` requires:
1. Operator edits the file in a separate working copy.
2. Operator runs `m15_ledger.py commit_cedar` which computes the new head hash, writes a HIGH-severity entry to Section 1's `admin_risk.py` ledger (requires operator re-type confirmation per Law 4 discipline), and signs the new seed manifest.
3. The old manifest is retained in history; the new manifest takes effect on next Vault-boot (not at runtime — Cedar policy is immutable during a seat session, enforced by the read-only freeze).

**Failure modes:**
- `F-M15-01 SeedManifestFileMismatch` — any seed file fails content-hash or identity-tuple check.
- `F-M15-02 SeedManifestSignatureMismatch` — operator signature over manifest invalid.
- `F-M15-03 SeedManifestLedgerHeadMismatch` — manifest `m15_ledger_head` not present in current ledger.
- `F-M15-04 CedarCommitWithoutRetype` — Cedar change committed without the HIGH-severity re-type confirmation (should be unreachable; included for completeness).

### 4.7 M15.2.1 — Atomic verify-and-freeze

**Intent:** The verify-then-freeze transition must be atomic from the seat's perspective — no seat can observe `vault_shared/` in a partially-verified state, and no write can occur between verification and freeze.

**Linux primary mechanism (mount-namespace switch):**
1. Bootstrap process (the parent of all seat processes) creates a new mount namespace via `unshare(CLONE_NEWNS)` and marks it private (`mount --make-rprivate /`).
2. Inside the new namespace, `vault_shared/` is unmounted from its current read-write location and re-mounted at the same path with `-o ro,nosuid,nodev,noexec` from the original block device.
3. Seed verification runs (§4.6) against the now-read-only view.
4. If verification passes, the namespace is preserved for seat children; they inherit it via `fork`. If verification fails, the namespace is torn down and Vault-boot aborts.
5. Seats cannot remount `vault_shared/` read-write because they lack `CAP_SYS_ADMIN` in their (further restricted) namespace.

**macOS primary mechanism (verified-and-pinned Merkle root):**
1. The Merkle root over all `vault_shared/` seed files is computed during §4.6 step 4.
2. The root is stored in an in-process immutable frozen dataclass (`VaultSharedFrozenRoot`) held by the Vault-boot process.
3. Every subsequent `fd_broker.request_fd()` for a path under `vault_shared/` re-walks the Merkle path — the broker holds the inclusion-proof structure and re-verifies per-request.
4. Per-seat sandbox profiles deny write to `vault_shared/` outside `cached_opportunities/` and `research_db/`. macOS sandbox cannot directly enforce read-only at a path level for all children, but the broker's per-request re-verification catches any write that leaked through.
5. Defence-in-depth: on APFS, an APFS snapshot of `vault_shared/` is taken at boot; the snapshot is read-only by design; the broker opens from the snapshot root for any seed file. O.5.n's snapshot-aware mount-over guard (v2-deferred) will tighten this further.

**Copy-on-verify snapshot (defence-in-depth, both platforms):**
- Linux btrfs / zfs: take a subvolume snapshot (`btrfs subvolume snapshot -r`) or clone (`zfs clone`) of `vault_shared/` at boot; broker reads from the snapshot. If the underlying volume is corrupted mid-run, the snapshot still serves verified seed.
- Linux ext4/xfs: snapshots are not native; CoV is skipped; primary (mount-namespace) carries the load.
- macOS APFS: snapshot as above.
- The snapshot is not the primary — primary is mount-ns or Merkle-pin. CoV is a belt-and-suspenders layer that handles specific ephemeral-storage failure modes.

**A-09 snapshot retention policy (NEW in v2):** On every successful boot, before creating a new CoV snapshot, `atomic_freeze.apply()` enforces a **retention count of `COV_SNAPSHOT_RETENTION_COUNT = 3`** (§8). The policy is:
1. Enumerate existing Tilth-tagged snapshots under the target filesystem:
   - macOS APFS: `tmutil listlocalsnapshots /` filtered to snapshots whose label starts with `com.tilth.vault_shared.`.
   - Linux btrfs: `btrfs subvolume list -s -r <mount>` filtered by name prefix `tilth-vault-shared-`.
   - Linux zfs: `zfs list -H -t snapshot -o name` filtered by suffix `@tilth-vault-shared-*`.
2. Sort by creation timestamp descending.
3. **If count ≥ 3, delete the oldest until count = 2**, so the new snapshot brings the total to 3.
   - macOS: `tmutil deletelocalsnapshots <date>` for each expired label.
   - btrfs: `btrfs subvolume delete -C <subvol>`.
   - zfs: `zfs destroy <snapshot>`.
4. Create the new snapshot with label `com.tilth.vault_shared.{session_id}.{iso8601}` / `tilth-vault-shared-{session_id}-{iso8601}`.
5. If retention-cleanup fails (e.g., APFS snapshot pinned by Time Machine), boot emits `F-FREEZE-04 CovSnapshotRetentionExceeded` and degrades to primary-only (mount-ns Linux / Merkle-pin macOS). CoV degradation is NOT fatal because primary carries the load; the operator gets a warning in the rails report and must investigate.

Rationale for `N=3`: (a) current + one rollback window + one long-session holdover; (b) APFS per-snapshot metadata is ~1 MB amortized over `vault_shared/` size ~30 MB, so three snapshots cost ~90 MB which is acceptable on the M1 8 GB target; (c) operator can manually bump the constant per-org via a governance edit of `ProcessWrapperManifest` for long-running forensic sessions. Raising `N` beyond 10 requires an architecture audit (disk-exhaustion threat shifts).

**Failure modes:**
- `F-FREEZE-01 FreezeMountNamespaceFailed` — Linux `unshare` or remount failed.
- `F-FREEZE-02 FreezeMerklePinLost` — macOS frozen-root dataclass released mid-run (should be unreachable; indicates a bug).
- `F-FREEZE-03 FreezeSnapshotCreationFailed` — CoV snapshot creation errored; degrades to primary-only (not fatal if primary succeeded).
- `F-FREEZE-04 CovSnapshotRetentionExceeded` — A-09 retention cleanup failed; CoV defence-in-depth disabled this session; primary must carry the load.

### 4.8 β — macOS Mach-IPC principle-level deny

**Intent:** Prevent seat processes from acquiring Mach IPC rights that would allow escape from the sandbox profile.

**Enumerated deny list (principle-level — the sandbox profile denies the primitive, not every syscall that might touch it). v2 (A-11) extends the list to close port-enumeration and port-rights-manipulation gaps:**
- **`mach_msg_trap` with `MACH_PORT_RIGHT_SEND` to privileged ports** — denies sending messages to any port not in the seat's allowed bootstrap-map. Privileged ports include the host port, the task port of other processes, the clock port, the set-special-port interface, and the I/O Kit master port. Specifically denied as sandbox rules: `(deny mach-lookup (global-name "com.apple.system.opendirectoryd.api"))`, `(deny mach-lookup (global-name "com.apple.distributed_notifications.2"))`, `(deny mach-priv-host-port)`, `(deny mach-priv-task-port)`.
- **`task_for_pid`** — denies the seat's ability to obtain a Mach task port for any other process. `(deny mach-task-lookup)`.
- **`host_get_special_port` / `host_set_special_port`** — denies the seat's ability to obtain or modify host-special ports (e.g., `HOST_PRIV_PORT`, `HOST_AUDIT_CONTROL_PORT`). `(deny mach-host-priv)` and `(deny mach-host-special-port)`.
- **`mach_port_insert_right`** — denies the seat's ability to insert a send right for a port name received from another process into its own port namespace. `(deny mach-port-insert-right)` (implemented via `sysctl kern.securelevel` enforcement plus sandbox rule).
- **`bootstrap_port` reparenting** — denies the seat's ability to replace its bootstrap port via `task_set_bootstrap_port`. `(deny mach-task-set-bootstrap-port)`.
- **A-11 port-enumeration primitives (NEW in v2):** v1 denied send-rights and task-port lookups but left enumeration primitives open. An attacker who can enumerate ports can stage a multi-step attack even without send rights. v2 denies:
  - `mach_ports_lookup` → `(deny mach-port-lookup (global-name-regex #"^.*"))` with an allowlist for the seat's bootstrap port only.
  - `mach_port_allocate` → `(deny mach-port-allocate)` — seats cannot create new ports.
  - `mach_port_destroy` → `(deny mach-port-destroy)` — seats cannot destroy inherited ports.
  - `mach_port_mod_refs` → `(deny mach-port-mod-refs)` — seats cannot manipulate port rights refcounts.
  - `mach_msg_trap` with `MACH_PORT_RIGHT_RECEIVE` or `MACH_PORT_RIGHT_SEND_ONCE` to any port other than the allowlisted broker port → `(deny mach-ipc-receive)` with narrow allowlist.
  - `mach_port_request_notification` → `(deny mach-port-request-notification)` — denies dead-name and port-destroyed notification plumbing.
- **Principle expressed:** the seat's Mach namespace is the minimum set of ports needed to run CPython and to talk to the broker — everything else is denied. Any port interaction not explicitly allowed → `F-VAULT-06 MachPortOperationDenied`.
- **`clonefile` / `clonefileat` / `fcopyfile`** — denies the copy primitives outright (see §4.3).
- **`copyfile(3)`** — routed via the vault-owned wrapper (see §4.3 macOS).

**Why principle-level, not enumeration:** The architecture v5-r8 §β requires principle-level deny because an exhaustive enumeration of every syscall that touches Mach IPC is (a) brittle against Darwin kernel version drift and (b) incomplete — the primitive set is what matters, not the specific syscall numbers. `sandbox_init` profiles are expressed in terms of primitives (mach-lookup, mach-task-lookup, etc.), which is precisely what the deny list above uses.

**Manifest:** `SandboxProfileManifest.denied_primitives` lists the primitive names (canonical, sorted). `SandboxProfileManifest.profile_text_hash` pins the SBPL text. Both are M15-signed.

### 4.9 γ — N.4.2 trust-root mirror hardening

**Intent:** The Logician trust root (mirror of `router.yaml`) must survive file-write attacks at `vault_shared/`, because the Logician is the last line of defence and its own trust anchor cannot live inside the artefact it's supposed to guard.

**Mechanism:**
1. **Mirror location:** `~/.tilth/logician_trust_root/router.yaml`. This path is outside the repo-root, outside `vault_shared/`, and under the operator's home directory. It is created at initial setup (a one-time operator ceremony) and re-verified at every boot.
2. **Immutability flag:** At setup and on every boot-verify:
   - **Linux:** `chattr +i /path/to/file`, `chattr +i /path/to/dir`, `chattr +i /path/to/~/.tilth`. The immutable flag requires `CAP_LINUX_IMMUTABLE` to clear — seat processes lack this capability in their namespace, and the operator's normal shell does too (requires `sudo` / explicit capability grant).
   - **macOS:** `chflags uchg /path/to/file /path/to/dir /path/to/~/.tilth`. The user-immutable flag requires `chflags nouchg` (by the owner) plus, in certain contexts, SIP exemption. Seat processes cannot clear the flag from within their sandbox profile.
3. **Post-open `fstat` identity-tuple verification:** On every boot, Section 2 opens the mirror file via `safe_open_lock_file(mirror_path)` (Section 1), then `fstat`s it, captures `(st_dev, st_ino)`, and compares against `TrustRootMirrorManifest.identity_tuple`. Any drift = `F-MIRROR-01`.
4. **Signed-manifest format:** `TrustRootMirrorManifest` carries:
   - `mirror_path` (absolute)
   - `content_hash` (SHA-3-512 hex of canonical bytes)
   - `identity_tuple` (volume UUID + FS file ID, captured at manifest creation)
   - `m15_ledger_head` (ledger head hash at manifest creation — this ties mirror to the same trust root as `vault_shared/`)
   - `operator_signature` over the canonical JSON of `(content_hash, identity_tuple, m15_ledger_head)` using the operator's keyring.
5. **Clock-rollback sanity check:** Section 1's `boot_clock_history.last_boot_wall_ns()` is read; if the current boot wall-clock is earlier than the last-recorded boot wall-clock minus `CLOCK_ROLLBACK_TOLERANCE_SECONDS` (Section 1 constant, 300 s), mirror-verify is rejected as `F-MIRROR-05 TrustRootMirrorClockRollback` even if content and identity tuples match — the operator may need to investigate whether the system clock was attacked.

**Why outside `vault_shared/`:** If an attacker gains write access to `vault_shared/` but not to `~/.tilth/`, they cannot tamper with the mirror. If they gain access to both, the operator's hardware is fully compromised and v0.1 makes no promise — this is the architecture §K sovereignty-promise boundary.

---

## 5. Blueprint-tracked implementations (BT14.a–g.1)

### 5.1 BT14.a — Per-org init marker

Implemented in `init_marker.py`. On first write for a given org slug:
1. Verify stable-UUID floor (BT14.g.1) for the filesystem containing `orgs/{slug}/vault/`.
2. Verify `vault_shared/init.marker` exists and its HMAC verifies (shared init must precede per-org init).
3. Generate `VaultInitMarker(scope="org", slug=slug, …)` with current identity tuple.
4. Write canonical JSON to `orgs/{slug}/vault/init.marker` via Section 1's `atomic_flush`.
5. Compute HMAC using key `tilth.vault.init.hmac.v1` from the keyring; write `…/init.marker.hmac` atomically.
6. Record the write to Section 1's sovereignty ledger.

Verification on every subsequent boot:
1. Read both marker + hmac files via `safe_open_lock_file`.
2. Verify HMAC signature.
3. Verify `marker.identity_tuple` against the current identity tuple of the marker file itself — drift indicates the marker was moved or the volume was remounted.
4. Verify `marker.created_under_uuid` against the current volume UUID — drift indicates a volume-UUID change (physical disk swap).

Failure modes: `F-INIT-01` marker missing, `F-INIT-02` HMAC mismatch, `F-INIT-03` identity drift, `F-INIT-04` volume-UUID drift.

### 5.2 BT14.b — Vault-owned skill enumeration

The two first-class Vault-owned skills are hard-coded in `fd_broker.py`:
- `vault-query` — implemented by `vault_query_skill.py`.
- `research-db-query` — implemented by `research_db_query_skill.py`.

Any FD broker request from a `requester_skill` not in this set is denied with `F-FD-01 UnknownVaultOwnedSkill`. There is no dynamic registration — adding a new Vault-owned skill requires a code change + M15 commit + re-lock of Section 2.

### 5.3 BT14.c — Cedar policy location

Cedar policies live at `vault_shared/cedar/`:
- `org_isolation.cedar` — enforces Law 3 (no cross-org reads or writes).
- `fd_issuance.cedar` — governs which skills can request which paths at which intents.
- `write_gate.cedar` — governs which skills can call `vault_write` for which paths.

Loaded by `m15_ledger.py cedar_policy_loader`. Verified against `VaultSharedSeedManifest`. Text is opaque to Section 2 (Section 4 Logician is the policy-authoring layer); Section 2 only guarantees integrity and availability.

### 5.4 BT14.d — `vault_shared/` signed commits

See §4.6. Every seed file listed in `VaultSharedSeedManifest.files`, manifest operator-signed, ledger-head tied via M15.

### 5.5 BT14.e — PRE-gate direct-FS failure semantics

See §4.4. When a seat process attempts any of the denied primitives:
- Linux seccomp: `SECCOMP_RET_KILL_PROCESS` — seat receives SIGSYS, terminates, parent (systemd-run scope) records exit. Failure propagates as `F-DIRECT-01 DirectFSAccessDetected` in the Section 1 sovereignty ledger.
- macOS sandbox: `deny` on the primitive returns the denied syscall's natural error (usually `EPERM`); the seat can handle the error, but the sandbox violation is logged to `log show --predicate 'subsystem == "com.apple.sandbox"'` and Section 2's audit consumer parses sandbox violations at seat exit. Failure propagates as `F-DIRECT-01` in the sovereignty ledger.

### 5.6 BT14.f — Per-org `init.marker` ceremony

The ceremony is the strict ordering of steps in §5.1. Ordering:
1. Stable-UUID floor (BT14.g.1).
2. Shared init verification (`vault_shared/init.marker`).
3. Per-org marker write.
4. Sovereignty ledger commit.

Any step failure aborts the ceremony; Vault rejects writes to the new org's vault until the ceremony completes.

### 5.7 BT14.g — Identity-tuple implementation

In `identity_tuple.py`:
- **macOS:** `os.statvfs(path)` gives `f_fsid` as a 64-bit value; combined with `getattrlist(path, ATTR_CMN_FILEID, …)` to produce the `(volume_uuid, fs_file_id)` pair. The volume UUID is read once at boot from `diskutil info -plist /` → `VolumeUUID` and cached.
- **Linux:** `statx(dirfd, path, 0, STATX_BASIC_STATS | STATX_MNT_ID, …)` gives `stx_mnt_id` (the volume anchor) and `stx_ino` (the file ID). The volume UUID is read once at boot from `blkid` or `/sys/block/…/dm/uuid` and cached.
- **Cache eviction:** When the mount table changes (detected via `/proc/self/mountinfo` on Linux, `DAUnregisterDiskAppeared` on macOS), the identity-tuple cache is flushed and every Vault-pinning-table entry is re-verified on next access.

### 5.8 BT14.g.1 — Stable-UUID floor

In `uuid_floor.py`:
- **Allowlist:** `apfs`, `ext4`, `btrfs`, `zfs`, `xfs`.
- **Rejection list:** `tmpfs`, `overlayfs` (unless both lowerdir and upperdir are on allowlisted filesystems AND an operator allowlist entry exists — v0.1: not supported), `fuse.*` (any FUSE filesystem), `hfs+` (lacks stable UUID semantics), `ntfs`, `vfat` / `msdos`, `nfs` / `cifs` / `smb`.
- **Check runs:** At Vault boot, before any seed verification. At every per-org init-marker write. At every mount-table-change event (for re-verification).
- **Failure:** `F-UUID-01 StableUUIDFloorAbort` — Vault boot refuses to proceed. The abort message names the fs_type and the mount path so the operator can move Vault data to a supported filesystem.

---

## 6. Failure modes + fail-closed recovery

Every failure code is (a) emitted from a named code path, (b) recorded in Section 1's sovereignty ledger via `hmac_audit_writer`, (c) fail-closed (no degraded-run fallback; degraded-run is Section 1's M10 only), (d) surfaced to Section 4 Logician's rails report.

### 6.1 Vault-access-related (F-VAULT-*)
- `F-VAULT-01 VaultReadUnauthorized` — Cedar `allow` failed at broker; seat gets empty response, seat pipeline aborts.
- `F-VAULT-02 VaultWriteUnauthorized` — same for write; write refused.
- `F-VAULT-03 VaultSkillNotOwned` — caller is not `vault-query`, `research-db-query`, or `vault-write`.
- `F-VAULT-04 VaultOrgMismatch` — request's slug does not match the seat's bound slug. Org-isolation violation.
- `F-VAULT-05 VaultXattrStripIncomplete` — FD handed to seat still had xattrs after strip pass (A-08).
- `F-VAULT-06 MachPortOperationDenied` — sandbox denied a Mach port primitive in the extended A-11 deny list.
- `F-VAULT-07 VaultCopyfileDestinationOutsideVault` — macOS copyfile wrapper saw destination path resolving outside the org vault subtree (A-18).

### 6.2 Gate-and-open-related (F-GATE-*)
- `F-GATE-01 GateOpenRejected` — see §4.1. Sub-reasons: kernel refused (ENOTDIR / ELOOP / EACCES), `openat2-unavailable` (Linux kernel < 5.6, no fallback, A-01), or reserved-component seen in walk.
- `F-GATE-02 GateIdentityTupleMismatch` — see §4.1.
- `F-GATE-03 GateAncestorMountMismatch` — macOS ancestor-walk post-open re-stat detected drift, or `st_dev` change during walk (A-02).
- `F-GATE-04 GateMagicLinkRejected` — Linux RESOLVE_NO_MAGICLINKS fired.
- `F-GATE-05 GatePathNullByte` — relative path contained `\x00` (A-12).
- `F-GATE-06 GateDevFdRejected` — canonical path begins with `/dev/fd/` or `/dev/std{in,out,err}` (A-15).
- `F-GATE-07 GatePathUnicodeNonNormal` — incoming path differs from its NFC form (B-03).
- `F-GATE-08 PathUnicodeForbiddenCategoryRejected` (C-03, v3; G-01 extended v4) — incoming path contains a Unicode codepoint in `General_Category` `Cf` (format control, e.g., U+202E RIGHT-TO-LEFT OVERRIDE, U+200C ZERO WIDTH NON-JOINER, U+200D ZERO WIDTH JOINER, U+2066–U+2069 bidi isolates), `Cc` (C0/C1 control), `Co` (Private-Use Area), `Mn` (non-spacing combining mark), or `Me` (enclosing combining mark). `_validate_relative_path()` rejects before any open. HIGH — defeats visual-impersonation path-trickery that bypasses NFC equality AND defeats rails-report display-integrity bypasses where combining marks or private-use glyphs render as a visually different path.
- `F-GATE-09 PathPercentEncodedNullRejected` (C-03, v3) — incoming path contains a percent-encoded null (`%00`, case-insensitive). A downstream URL-style decoder could turn this back into `\x00` and truncate the path after `_validate_relative_path()` has already accepted. HIGH.
- `F-GATE-10 PathNFCNFKCDivergence` (C-06, v3) — `unicodedata.normalize("NFC", p) != unicodedata.normalize("NFKC", p)`. A library that performs its own NFKC resolution (e.g., a URL library, some Python FS shims) could open a different file than the validator checked. HIGH.

### 6.3 Mirror-related (F-MIRROR-*)
- `F-MIRROR-01 TrustRootMirrorIdentityMismatch` — see §4.9.
- `F-MIRROR-02 TrustRootMirrorContentMismatch` — see §4.9.
- `F-MIRROR-03 TrustRootMirrorSignatureMismatch` — see §4.9.
- `F-MIRROR-04 TrustRootMirrorImmutabilityMissing` — see §4.9.
- `F-MIRROR-05 TrustRootMirrorClockRollback` — see §4.9.

### 6.4 Wrapper-related (F-WRAPPER-*)
- `F-WRAPPER-01 WrapperHashMismatchAtBoot` — §4.5 M14.4.4.
- `F-WRAPPER-02 WrapperHashMismatchAtExec` — §4.5 M14.4.4.
- `F-WRAPPER-03 WrapperRemountFailed` — `vault_shared/process_wrappers/` could not be remounted read-only / `chflags uchg`'d. Vault-boot refuses.
- `F-WRAPPER-04 WrapperExecutionBit` — wrapper mode is not `0o550`. Boot refuses.

### 6.5 UUID / floor (F-UUID-*)
- `F-UUID-01 StableUUIDFloorAbort` — see §5.8.
- `F-UUID-02 VolumeUUIDDrift` — volume UUID at mount differs from pinned UUID in a manifest.

### 6.6 Seccomp / sandbox (F-SECCOMP-*, F-SANDBOX-*)
- See §4.3 for enumeration. All fail-closed at seat-launch; the seat never runs.
- `F-SECCOMP-06 FDDuplicationViaFcntlDenied` (C-01, v3) — Linux seat attempted `fcntl(fd, F_DUPFD, …)` or `fcntl(fd, F_DUPFD_CLOEXEC, …)`. The seccomp filter denies these commands (argument-inspecting rule on the second argument); kernel returns `EPERM` and the audit is written. HIGH — the fcntl-based duplication would otherwise re-open a stdio FD after the dup*-deny path was locked. The macOS sandbox equivalent tightens `process-fork-and-exec` and denies `file-issue-extension` paths that would allow the same fan-out; the same failure code is raised with a `platform=darwin` tag.

### 6.7 Direct-FS (F-DIRECT-*)
- `F-DIRECT-01 DirectFSAccessDetected` — §4.4 + §5.5.
- `F-DIRECT-02 MacOSOpenByIDDenied` (A-10) — macOS sandbox blocked `openbyid_np` / `fsgetpath` / `F_GETPATH` on an FD whose path was not broker-issued. The seat had presumably obtained a file-id by scanning and tried to resolve it directly. Logged at HIGH; seat terminated.
- `F-DIRECT-03 BootstrapIoUringLeak` (A-13 + C-05 v3) — pre-exec audit of `/proc/self/fd/` found an `io_uring` instance in the bootstrap process that would have been inheritable by the seat, OR the C-05 audit→execve ordering invariant was violated (syscall detected between audit and `execve`, or `_TILTH_AUDIT_PASSED` sentinel missing when sandbox/seccomp loader initialises). Vault-boot aborts before `execve` rather than risk inheritance. v3 wording amended from v2 (which covered only inherited FDs) to also cover post-audit FD creation races.
- `F-DIRECT-04 MacOSProcPidInfoDenied` (A-16) — macOS sandbox blocked `proc_pidfdinfo` / `proc_pidinfo`. The seat attempted an FD→path reverse lookup on another process's FDs. Logged at HIGH; seat terminated.
- `F-DIRECT-05 MacOSNSURLBookmarkDenied` (C-02, v3) — macOS sandbox blocked a `mach-lookup` to `com.apple.CoreServices.coreservicesd` / `com.apple.FileCoordination` / `com.apple.FileProvider.LandingPoint`, or the `NSURLBookmarkResolutionWithoutMountingKey` resolution codepath. The seat attempted to resolve an `NSURL` bookmark to a file-id, bypassing the §4.3 deny on `openbyid_np` / `fsgetpath` / `F_GETPATH`. HIGH; seat terminated.

### 6.8 FD broker (F-FD-*)
- `F-FD-01 UnknownVaultOwnedSkill` — §5.2.
- `F-FD-02 FDRequestReplay` — broker detected a repeated nonce in Section 1's nonce registry.
- `F-FD-03 FDIssuanceCedarVeto` — Cedar denied at post-gate hook.
- `F-FD-04 FDTransmissionFailed` — SCM_RIGHTS send failed (broker socket closed, peer died).
- `F-FD-05 FDBrokerAuthenticationFailed` (A-05) — per-connection HMAC-SHA-256 challenge-response failed. Either the seat did not possess the per-seat key, the key was rotated mid-connection, or a third process attempted to impersonate a seat. Broker closes the socket; seat aborts.
- `F-FD-06 FDBrokerSocketIntegrityFailed` (A-14) — broker socket is missing the expected `chattr +i` (Linux) or `chflags uchg` (macOS) flag, OR `SO_PEERCRED` / `LOCAL_PEERCRED` on accept returned a credential outside the allowlist (bound seat PID, Vault bootstrap PID). Broker refuses to serve; Vault-boot aborts at the broker-online step.
- `F-FD-07 FDPathEscapeDetected` (A-17) — canonical-path prefix check at FD hand-out found that the resolved path does not start with `orgs/{bound_slug}/vault/`. Broker closes the FD without transmitting it; request rejected. Used as the tripwire for a race in which a bind-mount landed between the path-resolve step and the post-open re-stat; the re-stat must also fail independently, but `F-FD-07` catches the cases where re-stat happens to match by coincidence.

### 6.9 M15 (F-M15-*)
- `F-M15-01` through `F-M15-04` per §4.6.

### 6.10 Namespace / freeze (F-NS-*, F-FREEZE-*)
- `F-NS-01 MountNamespaceUnavailable` — Linux kernel lacks mount-namespace support OR operator UID cannot `unshare(CLONE_NEWNS)`. Vault-boot refuses.
- `F-NS-02 MountNamespacePreparationFailed` — `mount --make-rprivate` or bind-mount failed.
- `F-FREEZE-01` through `F-FREEZE-03` per §4.7.
- `F-FREEZE-04 SnapshotRetentionCleanupFailed` (A-09) — APFS / btrfs / zfs retention cleanup failed to prune snapshots beyond `COV_SNAPSHOT_RETENTION_COUNT` (§8 = 3). Logged at MEDIUM; Vault-boot proceeds but rails report surfaces the residual snapshots so operator can intervene. Unbounded snapshot accumulation is a disk-use problem, not a confidentiality problem.

### 6.11 Init-marker (F-INIT-*)
- `F-INIT-01` through `F-INIT-04` per §5.1.

### 6.12 Cedar (F-CEDAR-*)
- `F-CEDAR-01 CedarPolicyLoadFailed` — policy text could not be parsed.
- `F-CEDAR-02 CedarPolicyHashMismatch` — policy text hash drift from seed manifest.
- `F-CEDAR-03 CedarEvaluationError` — runtime evaluation raised; fail-closed as deny.

**Recovery for every code:** Log to sovereignty ledger, surface to rails report, abort the current operation. Section 4 Logician decides whether the whole pipeline aborts or just the current seat terminates; Section 2 does not make that choice. Section 2's job is to ensure the failure is detected and clean.

---

## 7. Test criteria

### 7.1 Unit — `layout`
- `VaultLayout.org_path(slug)` returns the canonical path under `orgs/`.
- Reserved-slug guard rejects `_shared`, `_template`, `_TEMPLATE`, `init`, `audit`, `logician`, `tilth`, `.tilth`.
- Seed-vs-cache partition correctly classifies sample paths.

### 7.2 Unit — `init_marker`
- First-write ceremony creates marker + HMAC with correct ordering.
- HMAC signed with `tilth.vault.init.hmac.v1` from keyring.
- Verification rejects missing marker, mismatched HMAC, drifted identity tuple, drifted volume UUID.

### 7.3 Unit — `identity_tuple`
- macOS returns non-zero `(volume_uuid, fs_file_id)` for a regular file.
- Linux returns non-zero `(stx_mnt_id, stx_ino)` for a regular file.
- Cache eviction triggers on mount-table change.

### 7.4 Unit — `uuid_floor`
- APFS, ext4 with UUID, btrfs, zfs, xfs accepted.
- tmpfs, overlayfs-on-tmpfs, fuse rejected with correct `rejection_reason`.

### 7.5 Unit — `gate_and_open`
- Linux: `openat2` with RESOLVE flags opens a valid Vault-internal path.
- Linux: kernel without `openat2` (simulated via `ENOSYS` probe) → `F-GATE-01 openat2-unavailable`; no fallback attempted (A-01 regression).
- Linux: symlink component → ELOOP → `F-GATE-01`.
- Linux: `../escape` → ELOOP/EXDEV → `F-GATE-01`.
- Linux: `/proc/self/fd/0` magic-link → `F-GATE-04`.
- macOS: ancestor-chain walk succeeds for a valid path.
- macOS: symlink at any component → `F-GATE-01`.
- macOS: mount-over mid-walk → `F-GATE-03`; post-open re-stat of ancestor FDs must trigger the failure (A-02 regression, not the pre-walk stat).
- Path with embedded null byte `foo\0bar` → `F-GATE-05` before any syscall issues (A-12).
- Path `/dev/fd/0` / `/dev/fd/1` → `F-GATE-06` at relative-path validation; does not reach `openat` (A-15).
- Path with NFD-encoded Unicode component (e.g. `é` as `e` + combining acute) → `F-GATE-07` at relative-path validation; the NFC-only rule is enforced pre-syscall (B-03).
- Path with U+202E RIGHT-TO-LEFT OVERRIDE anywhere in any component → `F-GATE-08` (C-03 v3 regression).
- Path with U+200C / U+200D / U+2066–U+2069 → `F-GATE-08`.
- Path with embedded `%00` / `%2500` percent-encoding → `F-GATE-09` (C-03 v3 regression).
- Path with NFC-stable form that differs from NFKC (e.g., `ﬁ` ligature U+FB01 vs `fi` ASCII) → `F-GATE-10` (C-06 v3 regression).

### 7.6 Unit — `metadata_homogenizer`
- Materialized file has mtime projected to boot-second-boundary.
- Cache page padded to nearest bucket in `{4 KiB, 64 KiB, 1 MiB, 16 MiB, 256 MiB}`.
- Xattrs stripped.

### 7.7 Unit — `kernel_copy_denylist`
- Seccomp filter compiled at wrapper-bake has denied-syscalls set matching manifest.
- Filter BPF hash reproducible (same source text → same hash).
- macOS sandbox profile denies `clonefile`, `fcopyfile`; `copyfile(3)` routed through wrapper.

### 7.8 Unit — `fd_broker`
- Request from unknown skill → `F-FD-01`.
- Request with reused nonce → `F-FD-02`.
- Cedar post-gate veto → `F-FD-03`.
- Successful request returns exactly one FD, identity tuple captured at open time.
- Connection from a process that does not possess the per-seat HMAC key → HMAC challenge fails → `F-FD-05` (A-05 regression).
- Broker socket with cleared immutability flag at boot → `F-FD-06` refuses to serve.
- `SO_PEERCRED` / `LOCAL_PEERCRED` returning a PID outside the bound-seat/bootstrap allowlist → `F-FD-06`.
- Injection of a mount-over between path-resolve and post-open re-stat: if the re-stat happens to match by coincidence, the canonical-path prefix check at hand-out must still trip → `F-FD-07` (A-17 regression).
- Broker at `FD_BROKER_MAX_OUTSTANDING_REQUESTS` returns `EAGAIN` to the seat; seat retries with backoff (B-05 regression — backpressure contract is documented, not a failure code).
- HMAC startup-pipe FD hygiene (C-04 v3): broker creates pipe with `O_CLOEXEC`; seat reads 32 bytes and immediately `close()`s; a subsequent `fork()` inside the wrapper (simulated via test harness) cannot inherit the pipe FD. The test parent-process confirms `/proc/self/fd/` in the child contains no read-end of the key pipe.
- Belt-and-suspenders: `fcntl(pipe_fd, F_GETFD)` shows `FD_CLOEXEC` set BEFORE the explicit `close()`.

### 7.9 Unit — `trust_root_mirror`
- Verify passes for a freshly-signed mirror.
- Verify fails F-MIRROR-01 / -02 / -03 / -04 / -05 for the corresponding corruption.

### 7.10 Unit — `process_wrapper`
- Wrapper mode validated as `0o550`.
- Exec-time re-hash runs against the wrapper's current bytes.
- systemd unit file parses as valid systemd syntax.
- launchd plist parses as valid Apple plist.

### 7.11 Unit — `m15_ledger`
- Seed manifest verification succeeds for a valid commit.
- Any single-file corruption → `F-M15-01`.
- Signature corruption → `F-M15-02`.
- Ledger head drift → `F-M15-03`.

### 7.12 Integration — full Vault boot sequence
- Clean boot: UUID floor → mirror verify → M15 seed verify → atomic freeze → wrapper hash verify → FD broker online → seat-launch authorized. All pass.
- Tampered mirror: boot aborts at mirror-verify with `F-MIRROR-*`.
- Tampered seed: boot aborts at M15-verify with `F-M15-01`.
- Tampered wrapper at boot: `F-WRAPPER-01`.
- Tampered wrapper between boot and seat-launch: `F-WRAPPER-02`.

### 7.13 Integration — seat isolation
- Seat-A in org-A cannot read `orgs/{org-B}/vault/`.
- Seat-A cannot `openat2` any path outside its bind-mounted subtree.
- Seat-A cannot `connect` to any network except via Scout's overriding drop-in.
- Seat-A cannot `shm_open` / `memfd_create`.
- Seat-A cannot `io_uring_setup`.
- Seat-A cannot `sendmsg` with SCM_RIGHTS.
- Seat-A cannot `task_for_pid` (macOS) or `ptrace` (Linux).
- Seat-A cannot `prctl(PR_SET_DUMPABLE, 1)` or `prctl(PR_SET_PTRACER, …)` (A-03 regression).
- Seat-A cannot `dup` / `dup2` / `dup3` any FD (A-04 regression — seccomp denies; macOS sandbox denies `file-issue-extension`).
- Seat-A cannot call `openbyid_np` / `fsgetpath` / `F_GETPATH` (macOS; A-10 regression → `F-DIRECT-02`).
- Seat-A cannot call `proc_pidfdinfo` / `proc_pidinfo` (macOS; A-16 regression → `F-DIRECT-04`).
- Seat-A cannot call `mach_port_allocate` / `mach_port_destroy` / `mach_msg_trap` (A-11 regression → `F-VAULT-06`).
- Seat-A launched as child of a bootstrap with a leaked `io_uring` FD must fail at the pre-exec `/proc/self/fd/` audit (A-13 regression → `F-DIRECT-03`).
- Seat-A attempted `fcntl(fd, F_DUPFD, 10)` or `fcntl(fd, F_DUPFD_CLOEXEC, 10)` after seccomp load → `EPERM` + `F-SECCOMP-06` (C-01 v3 regression). A test seat that tries to restore a closed stdio FD via fcntl-dup must fail.
- Seat-A attempted to resolve an `NSURL` bookmark via `[NSURL URLByResolvingBookmarkData:...]` on macOS → sandbox denies `mach-lookup com.apple.CoreServices.coreservicesd` / `com.apple.FileCoordination` / `com.apple.FileProvider.LandingPoint` → `F-DIRECT-05` (C-02 v3 regression).
- Seat-A `process_wrapper.py` with a synthetic syscall (test-only `os.pipe()` or `socket.socket()`) inserted between the pre-exec audit and `execve` must be rejected by the §7.16 static-analysis corpus and by the runtime sentinel check → `F-DIRECT-03` (C-05 v3 regression, amended wording).
- Seat-A forked from a wrapper where the HMAC startup pipe was NOT explicitly closed → the child observes the read-end of the pipe and can read residual key bytes. The regression corpus includes a test-only wrapper variant with the close omitted; the test harness must detect the inheritance and fail CI (C-04 v3 regression).
- Seat-A cannot mutate `DYLD_*` environment variables and re-exec itself (A-06 regression); if the wrapper is invoked without the interposer visible, the wrapper's constructor aborts before any payload runs (→ `F-SANDBOX-04`).
- Seat-A `copyfile(3)` with a destination path outside the bound slug's vault subtree → `F-VAULT-07` (A-18 regression).

### 7.14 Property / fuzz
- Path-trickery corpus: `..`, `../..`, `./foo/../bar`, `foo/./bar`, `foo//bar`, `foo\0bar`, `foo%2Fbar`, Unicode normalization attacks (`é` in NFC vs NFD), right-to-left override marks, trailing slashes. All must resolve to either a valid Vault path or `F-GATE-01`; never to an out-of-Vault path.
- Symlink corpus: symlink-to-parent-dir, symlink-to-root, symlink-loop, dangling symlink, absolute-target symlink. All must yield `F-GATE-01`.
- Magic-link corpus: `/proc/self/fd/0`, `/proc/1/fd/1`, `/proc/self/exe`, `/proc/self/root`. Linux must yield `F-GATE-04`; macOS lacks the magic-link surface but the equivalent `/dev/fd/*` must be denied by sandbox.

### 7.15 Performance smoke (M1 8 GB dev target)
- `gate_and_open` cold path: < 5 ms P99.
- `gate_and_open` warm path: < 1 ms P99.
- Full Vault-boot (UUID floor → seed verify → freeze → broker online): < 2 s on a 100-file seed.
- FD broker request-to-issuance round-trip: < 3 ms P99.
- Mount-namespace preparation (Linux): < 50 ms on M1 (virtualized Linux).
- Sandbox profile application (macOS): < 100 ms.

### 7.16 Red-team regression corpus
Captured in `pipeline/vault/tests/redteam_corpus/`, at least one test per failure code from §6. On any failure-code emission, the regression test confirms the code surfaced correctly in the rails report.

**C-05 static-analysis assertion (v3):** a CI step parses `process_wrapper.py` with `ast` and walks from the pre-exec audit call site to the `os.execve` call site; any `ast.Call` node on that path whose callable resolves to an FD-creating primitive (open/openat/pipe/pipe2/socket/socketpair/eventfd/timerfd_create/signalfd/userfaultfd/pidfd_open/memfd_create/io_uring_setup/epoll_create/epoll_create1/inotify_init/inotify_init1/dup/dup2/dup3/accept/accept4/fork/clone/posix_spawn*) fails the build with `CI-PROC-WRAPPER-AUDIT-ORDER`. The assertion runs as part of the pre-commit hook and the CI lint stage.

**G-03 (v4) dynamic-import + dynamic-attribute assertion:** the same AST parser adds two invariants over the entire `process_wrapper.py` module, not just the post-audit region: (a) no `ast.Call` whose callable resolves (by dotted-name lookup) to `importlib.import_module`, `importlib.__import__`, `builtins.__import__`, `importlib.util.spec_from_file_location`, or `importlib.util.module_from_spec` may appear anywhere in the module; (b) no `ast.Call` whose callable is `getattr(...)` with a non-`ast.Constant` second argument may appear on the path between the step 7 seccomp-load call site and the `os.execve` call site (this catches `getattr(mod, dyn_name)(...)` dispatch that would hide a lookup behind a dynamic name the static analyser cannot resolve). Violations fail the build with `CI-PROC-WRAPPER-DYN-IMPORT` or `CI-PROC-WRAPPER-DYN-GETATTR` respectively. Rationale: closes the RT-v3 C-05 attack path where a lazy import or an indirect `getattr`-dispatched function call could trigger a hidden syscall on the post-audit path even while the direct-syscall audit passes. The assertion runs in the same CI pass as the C-05 audit-order check.

**C-04 fork-family denial assertion (v3):** the same CI parser asserts that, between the HMAC startup-pipe `close()` call site and the `execve` call site, there is NO reachable `fork` / `clone` / `posix_spawn*` call. This is in addition to the sandbox/seccomp runtime deny, and catches the case where a refactor inadvertently introduces a child-spawning path between key-read and exec.

---

## 8. Concrete numbers (pinned)

- `NONCE_REGISTRY_ENTRY_SIZE_BYTES` — 64 (32 bytes request nonce + 32 bytes response nonce, hex-encoded when serialized).
- `FD_BROKER_REQUEST_TIMEOUT_MS` — 50. Beyond this, the broker cancels the request and returns `F-FD-04`.
- `MAX_VAULT_RELATIVE_PATH_DEPTH` — 12. A path with more than 12 `/`-separated components under `orgs/{slug}/vault/` is rejected at `gate_and_open` with `F-GATE-01 path-too-deep`.
- `METADATA_HOMOGENIZATION_SIZE_BUCKETS` — `(4096, 65536, 1048576, 16777216, 268435456)` — exact bytes for 4 KiB, 64 KiB, 1 MiB, 16 MiB, 256 MiB.
- `TRUST_ROOT_MIRROR_REVERIFY_INTERVAL_SECONDS` — 86400 (24 h). If the last mirror verify was longer ago than this at pipeline-start (e.g., a long-running orchestrator process), re-verify unconditionally before the next seat-launch.
- `M15_SEED_VERIFY_CACHE_TTL` — 0. Seed verification is done every boot; no cross-boot cache.
- `CLOCK_ROLLBACK_TOLERANCE_SECONDS` — 300 (5 min). Same value as Section 1's `boot_clock_history` tolerance.
- `VAULT_BOOT_TIMEOUT_SECONDS` — 10. Beyond this, boot aborts with `F-BOOT-TIMEOUT`.
- `SEAT_LAUNCH_TIMEOUT_SECONDS` — 5. Mount-namespace prep + sandbox profile apply + seccomp load + exec must complete within 5 s.
- `FD_BROKER_MAX_OUTSTANDING_REQUESTS` — 64. Prevents a seat from DoS'ing the broker by issuing unbounded concurrent requests.
- `WRAPPER_FILE_MODE` — `0o550` (owner r-x, group r-x, others none). Anything else at boot = `F-WRAPPER-04`.
- `SEED_MANIFEST_MAX_FILES` — 10000. Safety ceiling; current `vault_shared/` seed is ~30 files, so this is headroom, not a constraint.
- `CACHED_OPPORTUNITIES_RETENTION_DAYS` — 90. Entries older than 90 days in `cached_opportunities/` are eligible for eviction by a Section 5 housekeeping task (not Section 2's job; Section 2 only enforces that cache is mutable and seed is not).
- `LINUX_KERNEL_FLOOR_VERSION` — `5.6` (A-01). Section 2 **refuses to boot** on a kernel that reports `< 5.6` from `uname(2)` OR that returns `ENOSYS` for an `openat2(…, {RESOLVE_NO_SYMLINKS|RESOLVE_NO_MAGICLINKS|RESOLVE_BENEATH})` probe on a trusted in-vault path. There is no legacy-`openat` fallback. The probe runs at boot step 2a (§9) before any confidentiality-carrying FD is issued. Rationale: every downside of `openat2` unavailability lands in the trusted-operator threat model's in-scope list.
- `COV_SNAPSHOT_RETENTION_COUNT` — 3 (A-09). At Vault boot, atomic-freeze takes a CoV snapshot (APFS / btrfs / zfs); snapshots older than the most recent 3 for the tilth-owned dataset are pruned via `tmutil deletelocalsnapshots` (macOS) / `btrfs subvolume delete` / `zfs destroy`. Retention-cleanup failure emits `F-FREEZE-04` (MEDIUM) and surfaces to rails report; Vault-boot still proceeds because accumulated snapshots are a disk-use problem, not a confidentiality problem.
- `FD_BROKER_BACKPRESSURE_ERROR` — `EAGAIN` (B-05). When `FD_BROKER_MAX_OUTSTANDING_REQUESTS` is reached, the broker returns `EAGAIN` on the next request. Seats MUST implement exponential backoff starting at `FD_BROKER_BACKOFF_INITIAL_MS = 10` doubling up to `FD_BROKER_BACKOFF_MAX_MS = 500`. This is a contract, not a failure code; persistent `EAGAIN` past `FD_BROKER_REQUEST_TIMEOUT_MS` becomes `F-FD-04` at the seat.
- `FD_BROKER_HMAC_KEY_LENGTH_BYTES` — 32 (A-05). Each seat's per-connection HMAC-SHA-256 key is 32 bytes generated by `secrets.token_bytes(32)` at seat-launch, passed to the seat via the seccomp-gated startup pipe (anonymous fd), never via env or argv.
- `FD_BROKER_SOCKET_MODE` — `0o700` (A-14). Socket permissions at `orgs/{slug}/vault/.broker.sock`; `chattr +i` (Linux) / `chflags uchg` (macOS) applied after bind.

---

## 9. Vault boot sequence (exact ordering, fail-closed at every step)

1. **Section 1 init complete.** Caller (Section 5 pipeline-start) has already run Section 1's boot sequence: sovereignty init marker verified, ledger watermarks verified, boot_clock_history appended, per-session HMAC key loaded.
2. **Stable-UUID floor check.** `uuid_floor.enforce(vault_root)`. Fails → `F-UUID-01`, Vault-boot aborts.
2a. **Kernel-primitive probe (Linux only).** `gate_and_open.probe_openat2()`:
   - Read `uname(2)` release; refuse below `LINUX_KERNEL_FLOOR_VERSION` (§8 = 5.6).
   - Issue an `openat2(vault_root_fd, ".", {O_PATH|O_DIRECTORY}, {RESOLVE_NO_SYMLINKS|RESOLVE_NO_MAGICLINKS|RESOLVE_BENEATH})` probe.
   - `ENOSYS` → `F-GATE-01 openat2-unavailable`, Vault-boot aborts. No legacy `openat` fallback (A-01).
   - macOS: skip; the ancestor-chain walk is the only supported primitive.
3. **Mount-table snapshot.** `identity_tuple.capture_mount_table()` — cached for duration of boot; used for every subsequent identity-tuple verification.
4. **Trust-root mirror verify.** `trust_root_mirror.verify()`:
   - Re-read mirror file via `safe_open_lock_file`.
   - Verify immutability flag on file + dir + grandparent.
   - Re-compute content hash.
   - Re-capture identity tuple.
   - Verify manifest signature.
   - Verify clock rollback.
   - Any failure → `F-MIRROR-*`, Vault-boot aborts.
5. **Vault-shared init marker verify.** `init_marker.verify_shared()`. Fails → `F-INIT-*`, Vault-boot aborts.
6. **M15 seed manifest verify.** `m15_ledger.verify_seed()`:
   - Read manifest + signature.
   - Verify signature against keyring.
   - Verify `m15_ledger_head` is current ledger head.
   - For each seed file, re-open via temporary privileged broker bootstrap, re-hash, re-capture identity tuple, compare.
   - Any failure → `F-M15-*`, Vault-boot aborts.
7. **Atomic verify-and-freeze.** `atomic_freeze.apply()`:
   - Linux: `unshare(CLONE_NEWNS)`, `mount --make-rprivate /`, re-mount `vault_shared/` read-only inside namespace.
   - macOS: compute Merkle root over seed, pin to immutable dataclass, APFS-snapshot `vault_shared/` (defence-in-depth).
   - Failure → `F-FREEZE-*`, Vault-boot aborts.
8. **Wrapper hash verify at boot (freeze-first ordering, A-07).** `process_wrapper.verify_manifest()`:
   - **8a. Freeze the wrapper directory FIRST.** Remount `vault_shared/process_wrappers/` read-only on Linux (`mount -o remount,ro,bind`) or `chflags uchg` on macOS on the directory itself. Failure → `F-WRAPPER-03`, Vault-boot aborts. This ordering closes the TOCTOU window where an attacker could swap a wrapper file between the hash check and the freeze.
   - **8b. Verify each wrapper file's hash through the broker's privileged bootstrap FD** (not via fresh `open`, which could race a bind-mount post-freeze-failure). For each wrapper, re-read via the already-open directory FD, re-hash, compare against `ProcessWrapperManifest.content_hash`.
   - **8c. Verify mode is `0o550`** via `fstatat(dir_fd, name, …, AT_SYMLINK_NOFOLLOW)`.
   - Any mismatch in 8b or 8c → `F-WRAPPER-01` / `F-WRAPPER-04`, Vault-boot aborts.
9. **Cedar policy load.** `m15_ledger.cedar_policy_loader.load_all()`:
   - Read every `.cedar` file under `vault_shared/cedar/`.
   - Compare each against its entry in the seed manifest.
   - Load into Logician's Cedar engine (Section 4 consumer).
   - Failure → `F-CEDAR-01` / `F-CEDAR-02`, Vault-boot aborts.
10. **FD broker online.** `fd_broker.start()`:
    - Create Unix domain socket at `/tmp/tilth-fd-broker-{session_id}.sock` (Linux) or `/var/folders/*/T/tilth-fd-broker-{session_id}.sock` (macOS).
    - Bind, listen, accept in background thread.
    - Register Cedar post-gate hook.
    - Write broker-online marker to sovereignty ledger.
11. **Per-org init verification (for the bound slug).** `init_marker.verify_org(slug)`. If the marker does not exist, Vault-boot triggers the first-write ceremony (§5.1). Failure → `F-INIT-*`.
11a. **Snapshot retention prune (B-06/A-09).** `atomic_freeze.prune_snapshots(retention=COV_SNAPSHOT_RETENTION_COUNT)`:
    - Enumerate tilth-tagged snapshots on the vault_root dataset (APFS via `tmutil listlocalsnapshots` filtered on `tilth.vault.` prefix; btrfs via `btrfs subvolume list` with tag path; zfs via `zfs list -t snapshot` with tag).
    - Retain the most recent `COV_SNAPSHOT_RETENTION_COUNT` (§8 = 3).
    - Delete older entries via the platform primitive.
    - Failure → `F-FREEZE-04` (MEDIUM); boot proceeds, rails report surfaces the residuals.
11b. **Cache prune (B-06).** `cached_opportunities.prune(retention_days=CACHED_OPPORTUNITIES_RETENTION_DAYS)`:
    - Section 5 housekeeping is the canonical owner; Section 2 exposes the capability but does not force it at every boot.
    - If a `prune_on_boot=true` flag is set in the VaultSharedSeedManifest, Section 2 dispatches the Section 5 task synchronously. Otherwise, skip.
    - Failure is non-fatal; seats that need cache access will get fresh entries.
11.5. **Seat-launch ordering pin (C-05 v3).** The Vault boot does not itself `execve` a seat, but the boot-sequence contract declares that every subsequent seat-launch via `process_wrapper.py` MUST end with the pre-exec audit immediately followed by `execve`, with no intervening syscalls (see §4.4 M14.3.1 item 4 and §4.5 M14.4.1 step 8). This is a boot-level invariant — any seat launched through a wrapper build that violates the ordering is refused (`F-DIRECT-03`). The invariant is enforced by the §7.16 C-05 static-analysis assertion and by the `_TILTH_AUDIT_PASSED` runtime sentinel.
12. **Vault boot complete.** Return `VaultBootResult(success=True, session_id=…, vault_root_fd=…, fd_broker_endpoint=…)`. Section 5 pipeline proceeds to first seat-launch.

**Timeout:** Total sequence must complete within `VAULT_BOOT_TIMEOUT_SECONDS` (§8 = 10 s). Soft-target is <2 s on M1 8 GB; hard-timeout catches hung IO or stuck signature verification.

---

## 10. Findings and open questions (for audit to confirm or refute)

### F-OQ-01 — α primary recommendation
The outline pre-commit accepted Cedar-gated FD broker + per-seat mount-namespace (Linux) / sandbox profile (macOS) as α primary. v0.1 does NOT deploy an LSM hook on the `open*` family. **Question for audit:** does the blueprint evidence sufficient coverage from broker + namespace alone, given the trusted-operator threat model's in-scope list? Is there a specific in-scope attack vector not covered without an LSM hook?

### F-OQ-02 — `copyfile(3)` wrapper vs. library-level deny
The outline pre-commit accepted the vault-routed wrapper approach. **Question for audit:** is the `DYLD_INSERT_LIBRARIES` interposition approach robust against a seat process that `execve`s a child with different `DYLD_` environment? (The per-seat sandbox profile denies arbitrary `execve` except for a fixed whitelist, so the child case should be closed by composition, but the audit should confirm.)

### F-OQ-03 — M15.2.1 primary per platform
Linux = mount-namespace switch; macOS = Merkle-pin; CoV-snapshot as defence-in-depth on supported filesystems. **Question for audit:** is the mount-namespace switch's reliance on `CAP_SYS_ADMIN` at the bootstrap process level consistent with the broader v0.1 privilege posture? (The operator's normal shell lacks `CAP_SYS_ADMIN`, so the bootstrap must be specifically launched with that capability — via `setcap` on the bootstrap binary, which is itself an M15-signed artefact.)

### F-OQ-04 — Concrete numbers in §8
Numbers are best-effort estimates tuned to M1 8 GB dev. **Operator confirm or override.** In particular: `FD_BROKER_REQUEST_TIMEOUT_MS=50`, `MAX_VAULT_RELATIVE_PATH_DEPTH=12`, `CACHED_OPPORTUNITIES_RETENTION_DAYS=90`.

### F-OQ-05 — Fallback shell wrapper acceptable for v0.1?
§4.5 lists a `fallback-shell/seat-launch.sh` as a third process-creation wrapper. It's flagged as "reduced-confidence envelope" by Logician's rails report. **Question for audit:** should v0.1 refuse to launch seats via the fallback shell at all, given A1 (single-client-per-Golden-Quill)? The fallback is primarily for tests; production seats always have systemd or launchd available.

### F-OQ-06 — APFS snapshot retention discipline
§4.7 Linux CoV snapshots are ephemeral (session-lifetime). APFS snapshots persist until explicitly deleted. **Question for audit:** what's the retention policy — release on session end, keep N most recent, keep until operator prunes? Proposal: release on session end via `tmutil deletelocalsnapshots` for Tilth-tagged snapshots, to prevent unbounded disk use.

### F-OQ-07 — Cross-org init-marker propagation
If a new org is added mid-session, can its init marker be written without re-booting the Vault? Current design: no. Adding an org triggers a Vault re-boot because the seat bound-slug is pinned at seat-launch. **Question for audit:** is this acceptable? Adding an org is a low-frequency operator action, so "re-boot the Vault" seems fine, but the audit should confirm no pipeline state is lost.

### F-OQ-08 — Architectural finding triggers
Per handoff discipline: if an audit finding against Section 2 requires editing v5-r8, the finding is written as a finding against the architecture. **Question for audit:** do any of the current audit pass findings rise to architectural level, or are they all Section-2-internal? The author's pre-read of the architecture suggests this blueprint is fully inside the v5-r8 envelope; any finding that wants to cross the architecture boundary should be flagged explicitly.

### F-OQ-09 — ARCH-01 residual exposure (operator-shared mount-namespace escape)
The v1 Red Team (GPT-OSS 120B) identified that the trusted-operator threat model in v5-r8 Section B does not explicitly forbid the operator from entering a seat's mount namespace via `nsenter(1)` or from issuing `mount(2)` inside a shared namespace. Under such operator-adjacent attacks, `RESOLVE_BENEATH` and post-open mount-id re-verify can be defeated by an attacker who times a bind-mount between the Vault's capture of identity tuples and the seat's first file read.

Section 2 v2 implements every blueprint-level hardening available inside the α/β/γ envelope (post-open re-stat, canonical-prefix check at hand-out, broker socket immutability, `SO_PEERCRED` allowlist, bind-mount-aware freeze ordering). None defeats a privileged operator shell that enters the seat namespace between broker's capture and seat's first read.

**Residual disposition:** filed as `pipeline/validation/architecture_v0.1_findings_from_section_02/ARCH-01.md` against v5-r8. Per standing handoff discipline: v5-r8 is LOCKED and is not re-opened in place; ARCH-01 waits for the next architecture audit round. Section 2's job on this finding is done — all blueprint-level mitigations are in v2. **Question for audit:** confirm this is the correct disposition (file against architecture, not patch Section 2), or identify a Section-2-internal mitigation the author missed.

### v2-deferred items (carry-forward, not re-litigated)
- O.5.a — constant-time padding for FD-broker responses.
- O.5.b — CPU-cache flush on seat exit.
- O.5.c — IPC timing boundary between broker and seat.
- O.5.d — HSM-backed keyring for broker-to-seat authenticated channel.
- O.5.e — seccomp-enforced eBPF deny (v0.1 denies at seccomp; v2 adds defense-in-depth LSM).
- O.5.f — seccomp-enforced shm deny plus unshared tmpfs shm namespace (v0.1 option (a) only).
- O.5.g — readahead-channel hardening.
- O.5.h — mmap + msync flush-channel hardening.
- O.5.i — FUSE allowlist with operator-signed mount entries.
- O.5.j — tracefs isolation (v0.1: not mounted in seat namespace, which is sufficient under A1+A4).
- O.5.k — `/proc/fd` enumeration hiding.
- O.5.l — `open_by_handle_at` handle enumeration hiding.
- **O.5.m — `SCM_RIGHTS` from Vault-owned skill** (v0.1 uses the single sanctioned broker pattern; v2 hardens with HSM-backed auth).
- **O.5.n — snapshot-aware mount-over guard** (v0.1 takes APFS snapshots; v2 adds the snapshot UUID / ZFS gen / btrfs subvol-gen consistency check at mount-over time).

### Governance-only residuals (carry-forward, not re-litigated)
- ADM-A-001 — cheap-domain cross-domain diversity bypass. Governance captures operator discipline; no technical mitigation in v0.1.
- ADM-A-002 — M13 bypass normalization drift. Governance captures operator discipline; M13 bypass accounting is Section 1's job, not Section 2's.

---

## 11. What Section 2 deliberately does NOT implement

- **UI, dashboard, rendering.** Headless only (v0.1 constraint).
- **Cross-client multi-org on a single Golden Quill** (A3 = v2). A1 single-client-per-GQ is the v0.1 configuration; A2 operator-dev multi-client is allowed only under A4 trusted-operator.
- **Temporal-bridge operation** (N.4.1). v0.1 refuses to launch during the bridge window; Section 2's lock marker defines what Section 5 checks.
- **Supply-chain signing of Python packages.** Out-of-model for v0.1 (architecture §K). Pinned lockfile only.
- **Hostile-OS resistance.** Trusted-operator threat model puts OS compromise out-of-scope.
- **Side-channel resistance (timing, cache, power).** O.5.a/b/c are v2 hardening targets.
- **Multi-factor operator authentication at keyring access.** Single-factor operator keyring is the v0.1 root of trust.
- **Distributed / clustered Vault.** Single-node Golden Quill only.
- **Network-mounted `vault_shared/` or `~/.tilth/`.** NFS / CIFS / SMB rejected by UUID floor.

---

## 12. Dependencies

- **Section 1 (Sovereignty Envelope)** — consumed for crypto primitives, keystore, session lifecycle, atomic flush, nonce registry, `within_org_root`, canonical path resolver, reserved-slug guard, HMAC audit-chain writer, safe lock-file open, boot_clock_history, sovereignty init marker.
- **Operating system facilities** — Linux: `openat2`, `statx`, `unshare`, `mount`, seccomp BPF, `prctl`, systemd. macOS: `openat` + `O_NOFOLLOW`, `getattrlist`, `statfs`, `sandbox_init` + `sandbox-exec`, `chflags`, `DYLD_INSERT_LIBRARIES`, launchd, `diskutil`.
- **Python runtime** — CPython 3.11+ for `os.open` with `dir_fd`, `os.statvfs`, `os.statx` (via ctypes on Linux), `fcntl`.
- **ctypes** — used for syscalls not in the `os` module (`openat2`, `statx`, `bpf`, `sandbox_init`).
- **libseccomp** — for seccomp filter assembly (Linux); `python-libseccomp` package.
- **cryptography** — for SHA-3-512, HMAC, signature verification (operator signatures over manifests).
- **Operator keyring** — macOS Keychain / Linux Secret Service / `FileKeyStore` fallback (Section 1 `keys.py`). Keys: `tilth.vault.init.hmac.v1`, `tilth.operator.signing.v1` (public key for manifest verification).

No network dependencies. No LLM calls. No external services.

---

## 13. Audit request (for the Thesis Team) — v4 round

**Context for auditors:** v1→v3 history summarised at the top of this file. v3 met the formal PASS condition (Editor=READY_TO_LOCK, Judge=100/100, Red Team=REQUIRES_MINOR_FIXES with 0 Bucket-A items, 4 Bucket-B items, 4 Bucket-C items). The operator explicitly elected to spin v4 applying the four Bucket-B hardenings (G-01..G-04) so that Section 2's downstream-facing substrate (Sections 3+, v0.2 planning, M15 ledger interpretation) has zero known-but-deferred items rather than four filed follow-ups. This is a discipline choice about what a "locked" section should mean, not a correctness claim about v3 being unsafe — v3 was already PASS-eligible.

v4 edits in scope:
- G-01 — §4.1 `_validate_relative_path`: extend `_UNICODE_FORBIDDEN_CATEGORIES` from `{Cf, Cc}` to `{Cf, Cc, Co, Mn, Me}` and widen the `F-GATE-08` reason-tag to include category. No new failure code.
- G-02 — §4.5 M14.4.1 step 3: wrap the HMAC-pipe `os.read` + `os.close` in `signal.pthread_sigmask(SIG_BLOCK, …)` / `SIG_UNBLOCK`. No new failure code.
- G-03 — §4.5 M14.4.1 invariant paragraph after step 9 + §7.16 AST-checker extension for dynamic imports (`CI-PROC-WRAPPER-DYN-IMPORT`) and dynamic getattr (`CI-PROC-WRAPPER-DYN-GETATTR`). No new failure code.
- G-04 — §4.5 M14.4.1 step 1 preamble: `os.environ.pop("_TILTH_AUDIT_PASSED", None)` as very first wrapper action. No new failure code.

v4 NON-scope: no new mechanisms (M14.* / M15.* families unchanged), no new BT items, no new §8 constants, no changes to Cedar policy or broker protocol, no architectural amendments. ARCH-01 remains filed against v5-r8.

**Editor (clarity, v4):**
- Are the v3→v4 deltas discoverable? Can a reader match each G-item to its §4 edit site and (where applicable) its §7.16 AST-checker extension in under 60 s?
- Is the G-02 pthread_sigmask window (block before read, unblock after close) tightly scoped so that the mask-change cannot itself race with a signal that would widen the window?
- Is the G-03 invariant paragraph consistent with the existing C-04 fork-family denial assertion and the C-05 audit-order assertion (are the three AST assertions non-overlapping and jointly exhaustive for the step-7-to-`execve` window)?
- Is G-04's placement (very first wrapper action, before `setrlimit(RLIMIT_CORE)`) unambiguous in the revised step 1? Could a reader misread it as "step 0" vs. "step 1a" and get the ordering wrong?
- Do any of G-01..G-04 regress a v1/v2/v3 protection (e.g., does widening `_UNICODE_FORBIDDEN_CATEGORIES` break any legitimate path the v1/v2 audits accepted)?

**Judge (scoring, v4):** Score v4 against the v0.1 rubric. v1/v2/v3 all scored 100/100; v4 adds mitigations under existing failure codes without removing or amending any mechanism, so the expected outcome is re-PASS at 100/100. Verify specifically that:
- The G-01..G-04 edits land where the v3 changelog says they land, and no other edits snuck in.
- §6 failure-code inventory is unchanged (same codes, F-GATE-08 reason-tag widened).
- §7.16 gains two new CI assertions but does not alter existing ones.
- §8 concrete numbers are byte-identical to v3.
- ARCH-01 disposition is byte-identical to v3.

**Red Team (adversarial, v4):** re-run the v3 corpus against v4 + attack the new G-fixes:
- G-01 Co/Mn/Me rejection: are there other Unicode General_Categories that can produce visual spoofing (e.g., `Sk` modifier symbols, `Pc` connector punctuation, `Lm` modifier letters)? If yes, severity + reachability.
- G-02 pthread_sigmask window: can a signal delivered BEFORE the `SIG_BLOCK` call (but queued) fire after the mask change due to delivery semantics? Is there a `sigsuspend`-style edge case that re-opens the window? Could a real-time signal bypass the mask?
- G-03 dynamic-import/getattr AST assertion: can a refactor introduce a side-effecting primitive that the AST checker cannot resolve statically but that is not `importlib.import_module`, `__import__`, or `getattr(mod, dyn)`? (e.g., `operator.attrgetter('f')(mod)()`? `types.ModuleType(...)`? `exec('...')`?)
- G-04 env-pop: can a parent process re-inject `_TILTH_AUDIT_PASSED` between the pop and the step 8 audit via `prctl(PR_SET_CHILD_SUBREAPER)` + signal-driven env manipulation? (Spoiler: no, but confirm.)
- Regression: does G-01's widened reject set break any legitimate org slug or vault relative path currently in scope (the Section 1 slug grammar and the scan/Cedar reserved-slug set)?

Also re-confirm that the v3 carry-forward classifications (H-01 through H-04 in `05_synthesis_v3.md`) remain Bucket-C at v4, and that the v2-HIGH-09 / v2-new-A / v2-new-E classifications remain stable.

**Out-of-scope for v4 Red Team:** ARCH-01, v2-HIGH-09 (snapshot retention availability), v2-new-A (bind-mount = ARCH-01 restatement), v2-new-E (network-FS UUID-floor covered). These were all classified correctly at v2 and v3; do not re-surface.

**Operator (final gate, v4):** Confirm the v4 changelog accurately enumerates the four G-items and nothing else. Confirm no new §8 constants, no new failure codes, no new mechanisms. Confirm ARCH-01 disposition unchanged from v3. If Editor READY_TO_LOCK + Judge ≥ 85/100 (zero mechanism/BT gaps) + Red Team ∈ {READY_TO_LOCK, REQUIRES_MINOR_FIXES with Bucket B/C only}, Section 2 v4 locks. Given the four-round history (Editor READY ×3 already; Judge 100 ×3 already), the critical-path check is Red Team's verdict on the v4 additions specifically.

---

*End Section 2 v4 — DRAFT for audit (v4 round).*
