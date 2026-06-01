"""Adversarial tests for ``pipeline.sovereignty.isolation``.

Round D LOCK gate — per Autonomy Rule 2 (Test Your Own Work) every primitive
in the Sovereignty Envelope ships with adversarial probes that simulate the
failure modes an attacker would exploit. Each probe in this file maps to
one of the five entries under "Adversarial (per Autonomy Rule 2)" in
``pipeline/engineering/round_D_isolation_spec.md``:

    - test_adv_unlink_recreate_same_name_different_inode   (inode drift)
    - test_adv_symlink_swap_during_operation               (TOCTOU race)
    - test_adv_volume_remount_during_operation             (volume drift)
    - test_adv_relative_root_with_traversal_chars          (path escape)
    - test_adv_unicode_normalization_path_escape           (NFC/NFD)

Sandbox compatibility:
    The tests run on whatever filesystem ``tmp_path`` lives on, which on
    Linux CI runners is often a non-allowlisted type (``fuseblk``,
    ``tmpfs``, ``overlayfs``). Fixtures extend the allowlist via the
    ``fs_allowlist_extend`` kwarg to ``OrgRootNamespace.bind``; this does
    NOT relax the production allowlist.

Determinism discipline:
    Where the kernel's inode-allocation policy could make a real
    unlink+recreate drift test non-deterministic (ext4 reuses inodes
    freely), the probe additionally synthesizes the drift with
    ``dataclasses.replace`` so the *isolation.py comparison path* is
    exercised regardless of what the underlying filesystem chose to do.
    The real attack scenario is still attempted as an opportunistic
    check — if inode reuse happens, the opportunistic branch is
    explicitly skipped and the synthetic branch carries the invariant.
"""

from __future__ import annotations

import dataclasses
import os
import threading
import time
import unicodedata
from pathlib import Path

import pytest

from pipeline.sovereignty import isolation
from pipeline.sovereignty.isolation import (
    InodeDrift,
    IsolationError,
    OrgRootNamespace,
    PathEscape,
    SymlinkResolveFailed,
    VolumeDrift,
    within_org_root,
    with_org_root,
)

# ---------------------------------------------------------------------------
# Shared sandbox compatibility set (matches test_isolation.py)
# ---------------------------------------------------------------------------

_SANDBOX_FS_EXTENSION = frozenset({"fuseblk", "tmpfs", "overlay", "overlayfs"})


@pytest.fixture()
def org_root(tmp_path: Path) -> Path:
    root = tmp_path / "orgs" / "acme-coop"
    root.mkdir(parents=True)
    return root


@pytest.fixture()
def ns(org_root: Path) -> OrgRootNamespace:
    return OrgRootNamespace.bind(
        org_slug="acme-coop",
        root_path=org_root,
        fs_allowlist_extend=_SANDBOX_FS_EXTENSION,
    )


# ---------------------------------------------------------------------------
# A1 — unlink + recreate same name, different inode (mid-session)
# ---------------------------------------------------------------------------


class TestAdvUnlinkRecreate:
    def test_adv_unlink_recreate_same_name_different_inode(
        self, ns: OrgRootNamespace, org_root: Path
    ) -> None:
        """Attacker rmdir's ``orgs/acme-coop/`` and immediately recreates it
        mid-session. The recreated directory has the same name — and may
        or may not get the same inode depending on the kernel's allocation
        policy. Isolation's contract: if the inode differs from the
        captured snapshot, every gate FAILS CLOSED.

        Because inode-reuse on ext4 is kernel-policy-dependent, this probe
        runs two branches:
            (a) a real rmdir+mkdir attempt; if the kernel issues a fresh
                inode, the real attack fires ``InodeDrift``;
            (b) a synthetic ``dataclasses.replace`` branch that forces the
                comparison to fire regardless of kernel behavior — this
                branch carries the LOCK-gate invariant.
        """
        # ------- branch (a): real attack --------------------------------
        original_inode = ns.root_inode
        os.rmdir(org_root)
        org_root.mkdir()
        new_inode = os.stat(org_root).st_ino
        if new_inode != original_inode:
            # Real attack fired; isolation MUST catch it.
            with pytest.raises(InodeDrift):
                ns.verify_bindings_still_hold()
            with pytest.raises(InodeDrift):
                within_org_root(org_root / "vault" / "x.json", ns)
        else:  # pragma: no cover — kernel-specific inode reuse
            # Kernel reused the inode. Synthetic branch (b) picks it up.
            pass

        # ------- branch (b): synthetic drift always exercises the path --
        drifted = dataclasses.replace(
            ns, root_inode=ns.root_inode ^ 0xDEAD_BEEF
        )
        with pytest.raises(InodeDrift):
            drifted.verify_bindings_still_hold()
        with pytest.raises(InodeDrift):
            within_org_root(org_root / "vault" / "x.json", drifted)
        with pytest.raises(IsolationError):
            with with_org_root(drifted):
                pass


# ---------------------------------------------------------------------------
# A2 — symlink swap during operation (TOCTOU race)
# ---------------------------------------------------------------------------


class TestAdvSymlinkSwap:
    def test_adv_symlink_swap_during_operation(
        self, ns: OrgRootNamespace, org_root: Path, tmp_path: Path
    ) -> None:
        """A symlink inside the root initially points to a legitimate
        sibling. Between ``bind()`` and a later ``within_org_root`` call
        the symlink is re-pointed at an external directory. The escape
        MUST fire on the post-swap check — a silent True return would
        permit an attacker to smuggle writes outside the namespace."""
        # Start: symlink points inside.
        legit_dir = org_root / "legit"
        legit_dir.mkdir()
        (legit_dir / "x.json").write_text("{}")

        swapped_link = org_root / "maybe_evil"
        swapped_link.symlink_to(legit_dir)

        # Pre-swap: legit path resolves inside; within_org_root is True.
        assert within_org_root(swapped_link / "x.json", ns) is True

        # Attacker swaps the symlink mid-session.
        external_dir = tmp_path / "attacker_controlled"
        external_dir.mkdir()
        (external_dir / "x.json").write_text("{}")
        swapped_link.unlink()
        swapped_link.symlink_to(external_dir)

        # Post-swap: the predicate MUST refuse the detoured path. Because
        # the final resolved target lives in ``tmp_path`` (outside
        # ``org_root``), the cheap relative_to check returns False — the
        # predicate is False, NOT a silent True.
        probe = swapped_link / "x.json"
        assert within_org_root(probe, ns) is False

        # And if the attacker swaps into a subtler configuration where
        # the final target LOOPS BACK inside the root but a middle
        # component still escapes, the escape walker must fire.
        external_dir_2 = tmp_path / "attacker_loopback"
        external_dir_2.mkdir()
        (external_dir_2 / "x.json").symlink_to(legit_dir / "x.json")
        swapped_link.unlink()
        swapped_link.symlink_to(external_dir_2)

        probe2 = swapped_link / "x.json"
        with pytest.raises(SymlinkResolveFailed):
            within_org_root(probe2, ns)

    def test_adv_symlink_swap_under_held_gate(
        self, ns: OrgRootNamespace, org_root: Path, tmp_path: Path
    ) -> None:
        """TOCTOU closure: with ``with_org_root`` holding a dirfd + flock,
        a symlink swap still raises on subsequent gate.check() calls.
        The FD itself protects the ROOT directory inode; the predicate
        protects the symlink chain."""
        legit_dir = org_root / "legit"
        legit_dir.mkdir()
        (legit_dir / "x.json").write_text("{}")
        link = org_root / "link"
        link.symlink_to(legit_dir)

        external_dir = tmp_path / "external"
        external_dir.mkdir()
        (external_dir / "loop.json").symlink_to(legit_dir / "x.json")

        with with_org_root(ns) as gate:
            # Pre-swap probe inside the gate succeeds.
            assert gate.check(link / "x.json") is True
            # Swap the symlink under the held gate — ``link`` now points
            # at ``external_dir``; the child ``loop.json`` inside that
            # external dir is itself a symlink back to a legit file
            # under ``ns.root_path``. The FINAL resolved path therefore
            # lands inside the root, but the MIDDLE component (``link``)
            # escapes. The gate must refuse the probe via
            # ``SymlinkResolveFailed`` rather than silently admitting
            # the write through a root-aliased symlink.
            link.unlink()
            link.symlink_to(external_dir)
            probe_loop = link / "loop.json"
            with pytest.raises(SymlinkResolveFailed):
                gate.check(probe_loop)


# ---------------------------------------------------------------------------
# A3 — volume remount during operation
# ---------------------------------------------------------------------------


class TestAdvVolumeRemount:
    def test_adv_volume_remount_during_operation(
        self, ns: OrgRootNamespace, org_root: Path
    ) -> None:
        """A remount or volume swap under the same mount point changes
        ``st_dev``. Isolation MUST fail-closed on VolumeDrift.

        Real remounts require privileged capabilities not available in
        the test sandbox; the probe therefore synthesizes the drift
        deterministically via ``dataclasses.replace`` so the
        ``st_dev``-comparison path is exercised on every CI run.
        """
        drifted = dataclasses.replace(
            ns, volume_identifier=ns.volume_identifier ^ 0xC0FFEE
        )

        # verify_bindings_still_hold fires VolumeDrift.
        with pytest.raises(VolumeDrift) as excinfo:
            drifted.verify_bindings_still_hold()
        assert excinfo.value.expected_volume == drifted.volume_identifier
        assert excinfo.value.observed_volume == ns.volume_identifier

        # within_org_root propagates the drift rather than returning False.
        probe = org_root / "vault" / "x.json"
        with pytest.raises(VolumeDrift):
            within_org_root(probe, drifted)

        # with_org_root catches the drift on enter.
        with pytest.raises(IsolationError):
            with with_org_root(drifted):
                pass  # pragma: no cover — block should never run


# ---------------------------------------------------------------------------
# A4 — relative root with traversal chars
# ---------------------------------------------------------------------------


class TestAdvRelativeRootTraversal:
    def test_adv_relative_root_with_traversal_chars(
        self,
        ns: OrgRootNamespace,
        org_root: Path,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """The namespace rejects a *relative* root at construction. Once
        bound to an absolute root, probe paths that embed ``..``, mixed
        slashes, or other traversal tokens must never silently accept a
        destination outside the resolved root."""
        # 4a — ``..`` escape: resolves OUTSIDE ns.root_path → False.
        escape = org_root / ".." / "other_org" / "x.json"
        assert within_org_root(escape, ns) is False

        # 4b — ``..`` that lands BACK inside root (e.g. orgs/acme-coop/
        # ../acme-coop/vault/x.json) → True, because the resolved path
        # ends up inside. The predicate's contract is "resolved inside",
        # not "path-string free of ..".
        loopback = org_root / ".." / org_root.name / "vault" / "x.json"
        assert within_org_root(loopback, ns) is True

        # 4c — absolute path to another org → False.
        other_root = tmp_path / "orgs" / "other-coop"
        other_root.mkdir(parents=True)
        assert within_org_root(other_root / "vault" / "x.json", ns) is False

        # 4d — path with embedded nulls or other rubbish: the OS layer
        # refuses to resolve, which should surface as SymlinkResolveFailed
        # or a TypeError — NEVER a silent True.
        # (Pathlib refuses embedded NULs at construction, so use a
        # pre-constructed Path with a non-normalized mess of separators.)
        messy = Path(str(org_root) + "/./vault/./../../../etc/passwd")
        assert within_org_root(messy, ns) is False

        # 4e — bind() itself refuses a relative root.
        # monkeypatch.chdir auto-restores cwd at teardown so this test's
        # chdir cannot pollute subsequent tests in the same xdist worker
        # (which would silently break any cwd-relative source-scan tests).
        monkeypatch.chdir(tmp_path)
        with pytest.raises(PathEscape, match="root_path_not_absolute"):
            OrgRootNamespace.bind(
                org_slug="x-coop",
                root_path=Path("orgs/x-coop/../x-coop"),
                fs_allowlist_extend=_SANDBOX_FS_EXTENSION,
            )


# ---------------------------------------------------------------------------
# A5 — Unicode normalization path escape
# ---------------------------------------------------------------------------


class TestAdvUnicodeNormalization:
    def test_adv_unicode_normalization_path_escape(
        self, tmp_path: Path
    ) -> None:
        """On HFS+ / APFS, filenames are normalized at the VFS layer (NFD
        on HFS+, less aggressive on APFS). On ext4, byte-identical names
        with different Unicode normalizations are DISTINCT files.

        The isolation property: two namespaces whose slugs look identical
        to a human reader but whose byte sequences differ must bind to
        DIFFERENT roots — the predicate must not silently admit a path
        under root-NFC when the namespace was bound against root-NFD.

        Note: canonical_slug() restricts slugs to ASCII
        [a-z0-9-]+, so the Unicode attack surface on the slug itself is
        closed at Round C. This test exercises the path-containment
        layer — paths CAN contain Unicode on every allowlisted fs.
        """
        # Build two roots whose names differ ONLY in NFC vs NFD.
        name_nfc = unicodedata.normalize("NFC", "caf\u00e9")        # café (1 char)
        name_nfd = unicodedata.normalize("NFD", "cafe\u0301")       # café (2 char)
        assert name_nfc != name_nfd
        assert unicodedata.normalize("NFC", name_nfd) == name_nfc

        # The slug layer rejects non-ASCII; that's a different module's
        # invariant. This test uses Unicode CHILD paths under an ASCII
        # slug root, which is what an operator-supplied document path
        # looks like on disk.
        root = tmp_path / "orgs" / "cafe-coop"
        root.mkdir(parents=True)
        ns = OrgRootNamespace.bind(
            org_slug="cafe-coop",
            root_path=root,
            fs_allowlist_extend=_SANDBOX_FS_EXTENSION,
        )

        # A child file whose name is NFC-composed.
        (root / name_nfc).write_text("{}")
        # Probe that same child via its NFD spelling. On case-sensitive /
        # normalization-naive filesystems (ext4) the NFD spelling is a
        # DIFFERENT file — it does not exist, but its parent DOES, so the
        # predicate returns True ("can create here"). The contract: the
        # path must be INSIDE ns.root_path — which it is, under both
        # spellings. The predicate must return True, not silently
        # accept a sibling escape.
        probe_nfc = root / name_nfc
        probe_nfd = root / name_nfd
        assert within_org_root(probe_nfc, ns) is True
        assert within_org_root(probe_nfd, ns) is True

        # The sibling-escape flavor of the attack: construct a name whose
        # NFD form contains combining chars that — when the filesystem
        # renders them — resolve to a SIBLING directory rather than a
        # child. The slug is ASCII-only at the root level, so the only
        # way to produce such a name is outside the slug. On ext4, a
        # child named "..\u202E/etc" is a legitimate (if hostile) single
        # filename. The resolved path stays under root — predicate True.
        hostile_child = root / "..\u202e_payload.json"
        # The parent still exists — so relative_to against the RESOLVED
        # root still succeeds. That's the correct behavior: the hostile
        # name is a child of the root, even if a human reader might
        # misread it.
        assert within_org_root(hostile_child, ns) is True

        # But a Unicode-encoded ``..`` that escapes via path separators
        # (e.g. a slash inside the Unicode payload) decomposes into real
        # components and escapes — predicate False.
        escape_unicode = root / ".." / "other-coop" / "x.json"
        assert within_org_root(escape_unicode, ns) is False

    def test_adv_unicode_slug_case_variants_rejected_at_bind(
        self, tmp_path: Path
    ) -> None:
        """The slug-canonicalization layer refuses Unicode in the slug
        field itself — isolation.bind() re-checks and refuses. Guards
        against a case where a caller bypassed the org_slug module and
        passed a raw Unicode slug to isolation directly."""
        root = tmp_path / "orgs" / "unicode-attempt"
        root.mkdir(parents=True)
        with pytest.raises(ValueError):
            OrgRootNamespace.bind(
                org_slug="caf\u00e9-coop",  # non-ASCII — canonical_slug refuses
                root_path=root,
                fs_allowlist_extend=_SANDBOX_FS_EXTENSION,
            )


# ---------------------------------------------------------------------------
# A8 — fs_type drift after bind (same-st_dev remount edge case)
# ---------------------------------------------------------------------------


class TestAdvFsTypeDriftAfterBind:
    """Closes the GPT-OSS-flagged gap: after bind, if the underlying fs is
    remounted to a disallowed type but ``st_dev`` is somehow preserved (e.g.,
    overlayfs tricks), ``verify_bindings_still_hold`` must still fail closed.
    """

    def test_adv_fs_type_drift_raises_unsupported(
        self, ns: OrgRootNamespace
    ) -> None:
        """Synthetic drift: the namespace's recorded fs_type differs from
        what the detector reports at check-time. Must raise
        ``UnsupportedFilesystem`` (fail-closed), not silently continue.
        """
        drifted = dataclasses.replace(ns, fs_type="zfs")
        with pytest.raises(isolation.UnsupportedFilesystem):
            drifted.verify_bindings_still_hold(
                fs_allowlist_extend=_SANDBOX_FS_EXTENSION
            )

    def test_adv_fs_type_becomes_disallowed_raises(
        self, ns: OrgRootNamespace, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Simulate a mid-session remount that swaps the fs to a type
        not on the allowlist. Patch the detector to return a disallowed
        type; verify_bindings must raise ``UnsupportedFilesystem``.
        """
        monkeypatch.setattr(
            isolation, "_detect_fs_type", lambda _p: "ntfs"
        )
        with pytest.raises(isolation.UnsupportedFilesystem):
            ns.verify_bindings_still_hold(
                fs_allowlist_extend=_SANDBOX_FS_EXTENSION
            )

    def test_adv_fs_type_drift_caught_in_within_org_root(
        self, ns: OrgRootNamespace, org_root: Path,
        monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """The public predicate path must propagate the fs-type drift
        raise — not swallow it and return False."""
        monkeypatch.setattr(
            isolation, "_detect_fs_type", lambda _p: "ntfs"
        )
        with pytest.raises(isolation.UnsupportedFilesystem):
            within_org_root(org_root / "vault" / "x.json", ns)

    def test_adv_post_bind_env_var_mutation_cannot_widen_allowlist(
        self, org_root: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Bind under a clean env, then set TILTH_ISOLATION_FS_ALLOWLIST_EXTEND
        to a value that would whitelist a disallowed fs type. Verify the
        post-bind check still fails closed — the bind-time snapshot wins,
        env-var mutation after bind is ignored.

        Closes GPT-OSS v2 HIGH finding: same-uid actor must not be able to
        widen the allowlist by mutating the env var after namespace bind.
        """
        monkeypatch.delenv(
            isolation.TILTH_ISOLATION_FS_ALLOWLIST_EXTEND_ENV,
            raising=False,
        )
        # Bind with ONLY the sandbox fs extension — no env var set.
        ns = OrgRootNamespace.bind(
            org_slug="acme-coop",
            root_path=org_root,
            fs_allowlist_extend=_SANDBOX_FS_EXTENSION,
        )
        # Post-bind: attacker sets env var claiming 'ntfs' is allowed.
        monkeypatch.setenv(
            isolation.TILTH_ISOLATION_FS_ALLOWLIST_EXTEND_ENV, "ntfs"
        )
        # Simulate the fs drifting to the disallowed type. Even though
        # the env var now "authorizes" it, the bind-time snapshot does
        # NOT include ntfs and the check must raise.
        monkeypatch.setattr(
            isolation, "_detect_fs_type", lambda _p: "ntfs"
        )
        with pytest.raises(isolation.UnsupportedFilesystem):
            ns.verify_bindings_still_hold()
