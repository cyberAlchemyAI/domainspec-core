# Round D — `isolation.py` Spec Card

**Section:** 1 (Sovereignty Envelope)
**Module:** `pipeline/sovereignty/isolation.py`
**Dependencies:** Round B (`topology.py`), Round A (`crypto_primitives.py`, `_types.py`)
**Filed:** 2026-04-19
**Status:** Spec draft — awaiting Round C LOCK-internal before kickoff

---

## Purpose

Implements org-root namespace isolation per blueprint §1 + §2 v7.1 + SOUL.md Law 3 (Org Isolation). Enforces that every file operation inside `orgs/<org>/` cannot escape to another org's root, with TOCTOU closure.

## Primitives

### `OrgRootNamespace`

Dataclass binding an org to its root path + resolved inode snapshot.

Fields (all kw_only):
- `org_slug: str` — validated via `org_slug.validate()`
- `root_path: pathlib.Path` — absolute; resolved to real path at construction
- `root_inode: int` — captured at construction; used for inode-stability check
- `volume_uuid: str` — filesystem volume UUID; guards against cross-volume escape
- `created_at: datetime` — UTC, immutable

Invariants:
- `root_path.is_absolute()` and `root_path.exists()` at construction
- `root_path.stat().st_ino == root_inode` (re-check at every gate)
- Filesystem type per §5.1 allowlist (`apfs` / `ext4` / `btrfs` / `zfs` / `xfs`)
- Rejects `tmpfs`, `overlayfs` (except signed-allowlist), `fuse.*`, `hfs+`, `ntfs`, `vfat`, `nfs`, `cifs`, `smb`

### `within_org_root(path: Path, ns: OrgRootNamespace) -> bool`

Predicate. Returns True iff `path` (after symlink resolution + canonical-form) is strictly descended from `ns.root_path` AND the root's inode still matches `ns.root_inode`.

Implementation:
- macOS: `os.path.realpath()` + `pathlib.Path.resolve(strict=True)` + `.samefile()` check against root
- Linux: `openat2(RESOLVE_NO_SYMLINKS | RESOLVE_NO_MAGICLINKS | RESOLVE_BENEATH)` when kernel ≥ 5.6 (per provisioning manifest §2.2 `LINUX_KERNEL_FLOOR_VERSION`)

Failure modes (all fail-closed):
- `F-ISOLATION-INODE-DRIFT` — root inode changed (mount swap, rename, unlink+recreate)
- `F-ISOLATION-VOLUME-DRIFT` — volume UUID changed (remount, filesystem swap)
- `F-ISOLATION-PATH-ESCAPE` — resolved path is not under root
- `F-ISOLATION-SYMLINK-RESOLVE-FAIL` — symlink chain did not resolve strictly

### `with_org_root(ns: OrgRootNamespace)` — context manager

Opens the org root with `os.open(root, O_DIRECTORY | O_NOFOLLOW | O_CLOEXEC)`, takes an `fcntl.flock` on the directory FD, and yields a closure function `check(path)` that re-verifies `within_org_root` at call time using the held FD. On exit, releases the flock.

Used by the `gate_and_open` primitive in Section 2 for TOCTOU-safe writes.

### Linux bind-mount stub

Phase-0 stub: `create_bind_mount_namespace(ns)` that documents the intended Linux Mount Namespace approach without implementing it. Real implementation deferred to Section 2 Vault implementation where process isolation is wired. Stub returns a `NotImplementedError` with a clear pointer to the v0.2 bind-mount work item.

## Test surface (Round D LOCK gate)

Per Round A's E-001..E-004 lessons as pre-checks:
- `test_ns_construction_validates_slug`
- `test_ns_rejects_relative_path`
- `test_ns_rejects_disallowed_fs`
- `test_ns_captures_inode_at_construction`
- `test_within_org_root_ascends_symlink_correctly`
- `test_within_org_root_rejects_dotdot_escape`
- `test_within_org_root_rejects_cross_root_symlink`
- `test_within_org_root_detects_inode_drift`
- `test_within_org_root_detects_volume_drift`
- `test_with_org_root_holds_flock`
- `test_with_org_root_closure_re_verifies_at_call`
- `test_bind_mount_stub_raises_with_pointer`

Adversarial (per Autonomy Rule 2):
- `test_adv_unlink_recreate_same_name_different_inode` (mid-session)
- `test_adv_symlink_swap_during_operation` (TOCTOU race)
- `test_adv_volume_remount_during_operation`
- `test_adv_relative_root_with_traversal_chars`
- `test_adv_unicode_normalization_path_escape`

## BT property tests (feed Round J)

- BT2: every path write under an `OrgRootNamespace` resolves to a descendant of the root, even under concurrent rename
- BT3: inode drift always causes fail-closed, never silent recovery

## Provisioning manifest delta

No new Python deps (stdlib `os`, `pathlib`, `fcntl`). Round C's `cryptography` lib is not needed here. Document macOS Keychain vs Linux `openat2` difference in §2.2.

## Handoff

Ready for Claude Code implementation after Round C LOCK-internal. One CC window should produce module + tests + adversarial tests in ~2-3 hour session on Mac Mini 8GB. Committee dispatch in a separate window.
