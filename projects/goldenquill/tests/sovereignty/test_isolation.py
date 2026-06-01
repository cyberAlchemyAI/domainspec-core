"""Unit tests for ``pipeline.sovereignty.isolation``.

Round D gate. Probes every happy-path and documented failure mode of
``OrgRootNamespace``, ``within_org_root``, ``with_org_root``, and the
Phase-0 bind-mount stub. Adversarial tests live in
``test_isolation_adversarial.py``.

Sandbox note: this test suite extends ``FILESYSTEM_ALLOWLIST`` with the
CI-runner filesystem types (``fuseblk``, ``tmpfs``) via the
``fs_allowlist_extend`` argument so the tests run green on every
supported dev/CI surface. Production deployments never pass that
argument.
"""

from __future__ import annotations

import dataclasses
import os
import stat as _stat
from pathlib import Path

import pytest

from pipeline.sovereignty import isolation
from pipeline.sovereignty.isolation import (
    FILESYSTEM_ALLOWLIST,
    InodeDrift,
    IsolationError,
    OrgRootGate,
    OrgRootNamespace,
    PathEscape,
    SymlinkResolveFailed,
    UnsupportedFilesystem,
    VolumeDrift,
    create_bind_mount_namespace,
    within_org_root,
    with_org_root,
)

# ---------------------------------------------------------------------------
# Fixtures + helpers
# ---------------------------------------------------------------------------


#: Detected fs type of the pytest tmp_path family. Computed once; the suite
#: extends the isolation allowlist with this value so namespace construction
#: succeeds on any runner (Linux fuseblk, container tmpfs, macOS apfs).
_SANDBOX_FS_EXTENSION = frozenset({"fuseblk", "tmpfs", "overlay", "overlayfs"})


@pytest.fixture()
def org_root(tmp_path: Path) -> Path:
    """Create a directory that looks like ``orgs/<slug>/`` and return it."""
    root = tmp_path / "orgs" / "acme-coop"
    root.mkdir(parents=True)
    return root


@pytest.fixture()
def ns(org_root: Path) -> OrgRootNamespace:
    """A bound namespace for the ``acme-coop`` root."""
    return OrgRootNamespace.bind(
        org_slug="acme-coop",
        root_path=org_root,
        fs_allowlist_extend=_SANDBOX_FS_EXTENSION,
    )


# ---------------------------------------------------------------------------
# Construction  [§5.1 + E-001 + E-002]
# ---------------------------------------------------------------------------


class TestOrgRootNamespaceBind:
    def test_happy_path_binds_canonical_slug_and_captures_inode(
        self, org_root: Path
    ) -> None:
        ns = OrgRootNamespace.bind(
            org_slug="acme-coop",
            root_path=org_root,
            fs_allowlist_extend=_SANDBOX_FS_EXTENSION,
        )
        assert ns.org_slug == "acme-coop"
        assert ns.root_path == org_root.resolve(strict=True)
        assert ns.root_inode == org_root.stat().st_ino
        assert ns.volume_identifier == org_root.stat().st_dev
        assert ns.fs_type  # non-empty string
        assert ns.created_at.tzinfo is not None  # UTC

    def test_bind_rejects_non_str_slug(self, org_root: Path) -> None:
        with pytest.raises(TypeError, match="org_slug must be str"):
            OrgRootNamespace.bind(
                org_slug=42,  # type: ignore[arg-type]
                root_path=org_root,
                fs_allowlist_extend=_SANDBOX_FS_EXTENSION,
            )

    def test_bind_rejects_non_path_root(self) -> None:
        with pytest.raises(TypeError, match="root_path must be pathlib.Path"):
            OrgRootNamespace.bind(
                org_slug="acme-coop",
                root_path="/tmp",  # type: ignore[arg-type]
                fs_allowlist_extend=_SANDBOX_FS_EXTENSION,
            )

    def test_bind_rejects_non_canonical_slug(self, org_root: Path) -> None:
        # Upper-case is non-canonical; canonical_slug would lower it.
        with pytest.raises(ValueError, match="is not canonical"):
            OrgRootNamespace.bind(
                org_slug="ACME_Coop",
                root_path=org_root,
                fs_allowlist_extend=_SANDBOX_FS_EXTENSION,
            )

    def test_bind_rejects_relative_root_path(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # monkeypatch.chdir auto-restores cwd at test teardown. Plain
        # os.chdir leaks the new cwd into subsequent tests in the same
        # worker, breaking any test that reads files via relative paths.
        monkeypatch.chdir(tmp_path)
        (tmp_path / "orgs" / "x").mkdir(parents=True)
        with pytest.raises(PathEscape, match="root_path_not_absolute"):
            OrgRootNamespace.bind(
                org_slug="x",
                root_path=Path("orgs/x"),
                fs_allowlist_extend=_SANDBOX_FS_EXTENSION,
            )

    def test_bind_rejects_nonexistent_root(self, tmp_path: Path) -> None:
        ghost = tmp_path / "nope"
        with pytest.raises(PathEscape, match="root_path_unresolvable"):
            OrgRootNamespace.bind(
                org_slug="x",
                root_path=ghost,
                fs_allowlist_extend=_SANDBOX_FS_EXTENSION,
            )

    def test_bind_rejects_root_that_is_a_regular_file(self, tmp_path: Path) -> None:
        f = tmp_path / "notadir.txt"
        f.write_text("", encoding="utf-8")
        with pytest.raises(PathEscape, match="root_path_not_a_directory"):
            OrgRootNamespace.bind(
                org_slug="x",
                root_path=f,
                fs_allowlist_extend=_SANDBOX_FS_EXTENSION,
            )

    def test_bind_rejects_disallowed_filesystem(self, org_root: Path) -> None:
        """When NO extension is passed, the sandbox fs (e.g. fuseblk) is rejected."""
        # If the sandbox fs happens to be in the core allowlist (apfs, ext4,
        # btrfs, zfs, xfs), skip — there's nothing to reject.
        detected = isolation._detect_fs_type(org_root.resolve(strict=True))
        if detected in FILESYSTEM_ALLOWLIST:
            pytest.skip(f"sandbox fs {detected} is on the core allowlist")
        with pytest.raises(UnsupportedFilesystem):
            OrgRootNamespace.bind(
                org_slug="acme-coop",
                root_path=org_root,
                # no fs_allowlist_extend
            )

    def test_bind_frozen_dataclass_rejects_mutation(self, ns: OrgRootNamespace) -> None:
        with pytest.raises(Exception):  # FrozenInstanceError or dataclass error
            ns.org_slug = "other"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# verify_bindings_still_hold  [§6.7 drift detection]
# ---------------------------------------------------------------------------


class TestVerifyBindingsStillHold:
    def test_no_drift_returns_quietly(self, ns: OrgRootNamespace) -> None:
        ns.verify_bindings_still_hold()  # must not raise

    def test_inode_drift_raises_inode_drift(self, ns: OrgRootNamespace) -> None:
        """A synthetic namespace whose recorded inode differs from the
        filesystem's current inode triggers InodeDrift. (We synthesize the
        drift with ``dataclasses.replace`` because ext4 is free to reuse
        inodes after rmdir+mkdir — the semantic being tested is the
        comparison, not the kernel's inode-allocation policy.)"""
        drifted = dataclasses.replace(ns, root_inode=ns.root_inode ^ 0xDEAD)
        with pytest.raises(InodeDrift):
            drifted.verify_bindings_still_hold()

    def test_missing_root_raises_inode_drift(self, ns: OrgRootNamespace) -> None:
        os.rmdir(ns.root_path)
        with pytest.raises(InodeDrift):
            ns.verify_bindings_still_hold()

    def test_volume_drift_raises_volume_drift(
        self, ns: OrgRootNamespace
    ) -> None:
        """Same synthesis trick for volume_identifier drift."""
        drifted = dataclasses.replace(
            ns, volume_identifier=ns.volume_identifier ^ 0xBEEF
        )
        with pytest.raises(VolumeDrift):
            drifted.verify_bindings_still_hold()

    def test_inode_drift_carries_both_inode_values(
        self, ns: OrgRootNamespace
    ) -> None:
        drifted = dataclasses.replace(ns, root_inode=ns.root_inode ^ 0xDEAD)
        try:
            drifted.verify_bindings_still_hold()
        except InodeDrift as exc:
            assert exc.expected_inode == drifted.root_inode
            assert exc.observed_inode == ns.root_inode
            assert exc.expected_inode != exc.observed_inode


# ---------------------------------------------------------------------------
# within_org_root predicate
# ---------------------------------------------------------------------------


class TestWithinOrgRoot:
    def test_inside_path_returns_true(self, ns: OrgRootNamespace) -> None:
        inside = ns.root_path / "vault" / "claim_evidence" / "x.json"
        assert within_org_root(inside, ns) is True

    def test_outside_path_returns_false(
        self, ns: OrgRootNamespace, tmp_path: Path
    ) -> None:
        outside = tmp_path / "other_org" / "x.json"
        assert within_org_root(outside, ns) is False

    def test_nonexistent_child_still_returns_true(
        self, ns: OrgRootNamespace
    ) -> None:
        """Predicate supports the 'can I create this?' use case."""
        ghost = ns.root_path / "vault" / "claim_evidence" / "does_not_exist.json"
        assert not ghost.exists()
        assert within_org_root(ghost, ns) is True

    def test_dotdot_escape_returns_false(
        self, ns: OrgRootNamespace, tmp_path: Path
    ) -> None:
        escape = ns.root_path / ".." / "other_org" / "x.json"
        assert within_org_root(escape, ns) is False

    def test_symlink_to_sibling_inside_root_ok(
        self, ns: OrgRootNamespace
    ) -> None:
        (ns.root_path / "real").mkdir()
        (ns.root_path / "real" / "target.json").write_text("{}")
        link = ns.root_path / "link.json"
        link.symlink_to(ns.root_path / "real" / "target.json")
        assert within_org_root(link, ns) is True

    def test_symlink_to_outside_root_raises(
        self, ns: OrgRootNamespace, tmp_path: Path
    ) -> None:
        external = tmp_path / "external.json"
        external.write_text("{}")
        link = ns.root_path / "evil.json"
        link.symlink_to(external)
        # The link itself, when resolved, is outside — relative_to check
        # returns False, NOT raises. The symlink escape only raises if the
        # resolved path happens to be inside the root but some intermediate
        # symlink pointed outside. This branch is exercised below.
        assert within_org_root(link, ns) is False

    def test_intermediate_symlink_escape_raises_symlink_resolve_failed(
        self, ns: OrgRootNamespace, tmp_path: Path
    ) -> None:
        """An intermediate symlink that detours outside the root raises
        SymlinkResolveFailed even when the final resolved path happens
        to land back inside."""
        external_dir = tmp_path / "detour"
        external_dir.mkdir()
        # Create a symlink from inside the ns root that points to external_dir
        # AND a file inside external_dir that symlinks back to a legit
        # location inside ns.root — the resolved path lands inside, but
        # a MIDDLE component (the first symlink) escapes.
        (ns.root_path / "target_dir").mkdir()
        legit_file = ns.root_path / "target_dir" / "x.json"
        legit_file.write_text("{}")
        (external_dir / "loop_back.json").symlink_to(legit_file)
        bad_link_dir = ns.root_path / "escaped"
        bad_link_dir.symlink_to(external_dir)
        probe = bad_link_dir / "loop_back.json"
        with pytest.raises(SymlinkResolveFailed):
            within_org_root(probe, ns)

    def test_drift_during_call_fails_closed(
        self, ns: OrgRootNamespace
    ) -> None:
        """If the namespace has drifted (synthesized here via
        ``dataclasses.replace``), the predicate raises drift rather than
        silently returning False."""
        drifted = dataclasses.replace(ns, root_inode=ns.root_inode ^ 0xFADE)
        probe = ns.root_path / "x.json"
        with pytest.raises(InodeDrift):
            within_org_root(probe, drifted)

    def test_type_gate_rejects_non_path(self, ns: OrgRootNamespace) -> None:
        with pytest.raises(TypeError, match="path must be pathlib.Path"):
            within_org_root("/tmp/x", ns)  # type: ignore[arg-type]

    def test_type_gate_rejects_non_ns(self, tmp_path: Path) -> None:
        with pytest.raises(TypeError, match="ns must be OrgRootNamespace"):
            within_org_root(tmp_path, ns="not-a-namespace")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# with_org_root context manager
# ---------------------------------------------------------------------------


class TestWithOrgRoot:
    def test_yields_gate_with_live_fd(self, ns: OrgRootNamespace) -> None:
        with with_org_root(ns) as gate:
            assert isinstance(gate, OrgRootGate)
            assert gate.ns is ns
            assert gate.fd > 0
            # fd must be usable — fstat should agree with the root's stat
            st = os.fstat(gate.fd)
            assert _stat.S_ISDIR(st.st_mode)
            assert st.st_ino == ns.root_inode

    def test_fd_is_closed_on_exit(self, ns: OrgRootNamespace) -> None:
        with with_org_root(ns) as gate:
            fd = gate.fd
        # After exit, fd should be closed — fstat raises EBADF
        with pytest.raises(OSError):
            os.fstat(fd)

    def test_gate_check_returns_bool(self, ns: OrgRootNamespace) -> None:
        inside = ns.root_path / "claim_evidence" / "x.json"
        with with_org_root(ns) as gate:
            assert gate.check(inside) is True

    def test_exception_inside_block_still_releases_fd_and_lock(
        self, ns: OrgRootNamespace
    ) -> None:
        captured_fd = None
        with pytest.raises(RuntimeError, match="block-internal"):
            with with_org_root(ns) as gate:
                captured_fd = gate.fd
                raise RuntimeError("block-internal")
        assert captured_fd is not None
        with pytest.raises(OSError):
            os.fstat(captured_fd)

    def test_blocking_false_on_uncontested_returns_gate(
        self, ns: OrgRootNamespace
    ) -> None:
        with with_org_root(ns, blocking=False) as gate:
            assert gate.fd > 0

    def test_drift_between_bind_and_enter_is_caught(
        self, ns: OrgRootNamespace
    ) -> None:
        """A synthetically drifted namespace raises IsolationError on enter."""
        drifted = dataclasses.replace(ns, root_inode=ns.root_inode ^ 0xFADE)
        with pytest.raises(IsolationError):
            with with_org_root(drifted):
                pass

    def test_missing_root_on_enter_raises(
        self, ns: OrgRootNamespace
    ) -> None:
        """If the root has been rmdir'd, os.open fails and the CM raises."""
        os.rmdir(ns.root_path)
        with pytest.raises((OSError, IsolationError)):
            with with_org_root(ns):
                pass

    def test_type_gate_rejects_non_ns(self) -> None:
        with pytest.raises(TypeError, match="ns must be OrgRootNamespace"):
            with with_org_root("not-a-ns"):  # type: ignore[arg-type]
                pass


# ---------------------------------------------------------------------------
# Phase-0 bind-mount stub
# ---------------------------------------------------------------------------


class TestBindMountStub:
    def test_raises_not_implemented_with_clear_pointer(
        self, ns: OrgRootNamespace
    ) -> None:
        with pytest.raises(NotImplementedError) as excinfo:
            create_bind_mount_namespace(ns)
        # Must point at the v0.2 work item so readers don't have to hunt.
        assert "v0.2" in str(excinfo.value) or "round_E_vault_fs_spec" in str(
            excinfo.value
        )


# ---------------------------------------------------------------------------
# Filesystem-allowlist behaviour
# ---------------------------------------------------------------------------


class TestFilesystemAllowlist:
    def test_core_allowlist_is_frozenset_of_lowercase_names(self) -> None:
        assert isinstance(FILESYSTEM_ALLOWLIST, frozenset)
        for fs in FILESYSTEM_ALLOWLIST:
            assert fs == fs.lower()
        # Exactly the five §5.1 filesystems.
        assert FILESYSTEM_ALLOWLIST == frozenset({"apfs", "ext4", "btrfs", "zfs", "xfs"})

    def test_env_var_extension_is_honored(
        self, org_root: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # Skip if sandbox fs is already on the core allowlist.
        detected = isolation._detect_fs_type(org_root.resolve(strict=True))
        if detected in FILESYSTEM_ALLOWLIST:
            pytest.skip(f"sandbox fs {detected} is on the core allowlist")
        # Without env var, construction fails.
        monkeypatch.delenv(
            isolation.TILTH_ISOLATION_FS_ALLOWLIST_EXTEND_ENV, raising=False
        )
        with pytest.raises(UnsupportedFilesystem):
            OrgRootNamespace.bind(org_slug="acme-coop", root_path=org_root)
        # With env var, construction succeeds.
        monkeypatch.setenv(
            isolation.TILTH_ISOLATION_FS_ALLOWLIST_EXTEND_ENV,
            ",".join(_SANDBOX_FS_EXTENSION),
        )
        ns = OrgRootNamespace.bind(org_slug="acme-coop", root_path=org_root)
        assert ns.fs_type  # non-empty


# ---------------------------------------------------------------------------
# BLUEPRINT_DEPS sanity
# ---------------------------------------------------------------------------


def test_blueprint_deps_declared() -> None:
    assert "section_1_sovereignty_envelope.md" in isolation.BLUEPRINT_DEPS
    decl = isolation.BLUEPRINT_DEPS["section_1_sovereignty_envelope.md"]
    assert decl["hash_source_version"] == "v6"
    assert isinstance(decl["sections_implemented"], list)
    assert any("§1 row 7" in s for s in decl["sections_implemented"])
    assert any("§4.13 Law 3" in s for s in decl["sections_implemented"])
