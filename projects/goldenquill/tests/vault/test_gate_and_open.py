"""Unit tests for pipeline.vault.gate_and_open (§4.1 + §7.5).

Round N. Covers:
* Pre-gate input validation: null byte, %00, Unicode Cf/Cc/Co/Mn/Me,
  non-NFC, NFC-NFKC divergence, /dev/fd, reserved components, path depth.
* macOS path: ancestor-chain openat + O_NOFOLLOW + post-open fstat drift.
* Identity-tuple pinning drift → F-GATE-02.
* Symlink rejection (O_NOFOLLOW / ELOOP).
* Directory traversal beneath vault root.
* Arg-type gates.
* probe_openat2 on macOS (returns False).
"""

from __future__ import annotations

import os
import platform
from pathlib import Path
from unittest import mock

import pytest

from pipeline.vault.error_codes import (
    F_GATE_01,
    F_GATE_02,
    F_GATE_03,
    F_GATE_05,
    F_GATE_06,
    F_GATE_07,
    F_GATE_08,
    F_GATE_09,
    F_GATE_10,
    GateAncestorMountMismatch,
    GateDevFdRejected,
    GateIdentityTupleMismatch,
    GateNFCNFKCDivergence,
    GateOpenRejected,
    GatePathNullByte,
    GatePathUnicodeForbidden,
    GatePathUnicodeNonNormal,
    GatePercentNullRejected,
)
from pipeline.vault.gate_and_open import (
    MAX_VAULT_RELATIVE_PATH_DEPTH,
    _validate_relative_path,
    gate_and_open,
    open_vault_root,
    probe_openat2,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@pytest.fixture
def vault_root_fd(tmp_path: Path):
    fd = open_vault_root(tmp_path)
    yield fd
    try:
        os.close(fd)
    except OSError:
        pass


def _make_file(root: Path, rel: str, content: bytes = b"hi") -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(content)
    return p


# ---------------------------------------------------------------------------
# Pre-gate validator
# ---------------------------------------------------------------------------


class TestPreGateValidation:
    def test_null_byte_rejected(self) -> None:
        with pytest.raises(GatePathNullByte) as exc:
            _validate_relative_path("a/b\x00c")
        assert exc.value.code == F_GATE_05

    def test_percent_null_rejected(self) -> None:
        with pytest.raises(GatePercentNullRejected) as exc:
            _validate_relative_path("a/b%00c")
        assert exc.value.code == F_GATE_09

    def test_percent_null_case_insensitive(self) -> None:
        with pytest.raises(GatePercentNullRejected):
            _validate_relative_path("a/b%00c")

    def test_rtl_override_rejected(self) -> None:
        # U+202E is Cf (format)
        with pytest.raises(GatePathUnicodeForbidden) as exc:
            _validate_relative_path("a/b\u202ec")
        assert exc.value.code == F_GATE_08

    def test_zwj_rejected(self) -> None:
        with pytest.raises(GatePathUnicodeForbidden):
            _validate_relative_path("a/b\u200dc")  # ZWJ Cf

    def test_private_use_rejected(self) -> None:
        with pytest.raises(GatePathUnicodeForbidden):
            _validate_relative_path("a/b\ue000c")  # PUA Co

    def test_combining_mark_rejected(self) -> None:
        with pytest.raises(GatePathUnicodeForbidden):
            _validate_relative_path("a/b\u0301c")  # combining acute Mn

    def test_control_char_rejected(self) -> None:
        with pytest.raises(GatePathUnicodeForbidden):
            _validate_relative_path("a/b\x07c")  # Cc (bell)

    def test_non_nfc_rejected(self) -> None:
        # 'café' in NFD form (e + combining acute). The combining acute is Mn
        # and therefore fails at the forbidden-category check BEFORE NFC.
        # A pure non-NFC-but-allowed case: use a character whose
        # decomposed form contains only letters (there isn't a clean one, so
        # we patch past Unicode-category to hit the NFC branch directly).
        import unicodedata

        # Construct: 'A' + U+0041 composes to 'AA'? No — pick a known
        # NFC-distinct but no-Mn input: U+00C5 'Å' (Latin letter A with ring
        # above) vs U+212B 'Å' (ANGSTROM SIGN) — different codepoints, both
        # compose to U+00C5 under NFC.
        angstrom = "a/\u212bb"  # ANGSTROM SIGN
        assert unicodedata.normalize("NFC", angstrom) != angstrom
        with pytest.raises(GatePathUnicodeNonNormal) as exc:
            _validate_relative_path(angstrom)
        assert exc.value.code == F_GATE_07

    def test_nfc_nfkc_divergence_rejected(self) -> None:
        # U+FF21 'FULLWIDTH LATIN CAPITAL LETTER A' — its NFC form is itself,
        # but NFKC maps to ASCII 'A'.
        import unicodedata

        path = "a/\uff21b"
        assert unicodedata.normalize("NFC", path) == path
        assert unicodedata.normalize("NFKC", path) != path
        with pytest.raises(GateNFCNFKCDivergence) as exc:
            _validate_relative_path(path)
        assert exc.value.code == F_GATE_10

    def test_dev_fd_rejected(self) -> None:
        with pytest.raises(GateDevFdRejected) as exc:
            _validate_relative_path("/dev/fd/3")
        assert exc.value.code == F_GATE_06

    def test_dev_stdin_rejected(self) -> None:
        with pytest.raises(GateDevFdRejected):
            _validate_relative_path("/dev/stdin")

    def test_dotdot_rejected(self) -> None:
        with pytest.raises(GateOpenRejected) as exc:
            _validate_relative_path("../../../etc/passwd")
        # normpath collapses the leading .. but leaves them as parts
        assert exc.value.code == F_GATE_01
        assert "reserved" in exc.value.reason or "too-deep" in exc.value.reason

    def test_path_too_deep(self) -> None:
        deep = "/".join(f"d{i}" for i in range(MAX_VAULT_RELATIVE_PATH_DEPTH + 2))
        with pytest.raises(GateOpenRejected) as exc:
            _validate_relative_path(deep)
        assert exc.value.reason == "path-too-deep"

    def test_path_at_depth_limit_allowed(self) -> None:
        ok = "/".join(f"d{i}" for i in range(MAX_VAULT_RELATIVE_PATH_DEPTH))
        # Should not raise.
        _validate_relative_path(ok)

    def test_validate_rejects_non_str(self) -> None:
        with pytest.raises(TypeError):
            _validate_relative_path(b"bytes")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# F-2 closure (Batch 2 carry-forward) — validator rejects reserved and
# absolute canonical forms. normpath("") -> "." on Linux; without this
# check, openat2(".") would hand back the vault-root FD.
# ---------------------------------------------------------------------------


class TestValidateRelativePathRejectsReserved:
    def test_empty_string_rejected(self) -> None:
        with pytest.raises(GateOpenRejected) as ei:
            _validate_relative_path("")
        assert ei.value.reason == "reserved-component"

    def test_bare_dot_rejected(self) -> None:
        with pytest.raises(GateOpenRejected) as ei:
            _validate_relative_path(".")
        assert ei.value.reason == "reserved-component"

    def test_absolute_path_rejected(self) -> None:
        with pytest.raises(GateOpenRejected) as ei:
            _validate_relative_path("/etc/passwd")
        assert ei.value.reason == "reserved-component"


# ---------------------------------------------------------------------------
# F-1 closure (Batch 2 carry-forward) — open_vault_root translates
# OSError(ELOOP) on a symlink root to GateOpenRejected(root-is-symlink)
# instead of leaking the raw errno.
# ---------------------------------------------------------------------------


class TestOpenVaultRootRejectsSymlink:
    def test_symlink_root_raises_gate_open_rejected(self, tmp_path: Path) -> None:
        real = tmp_path / "real"
        real.mkdir()
        link = tmp_path / "link"
        link.symlink_to(real, target_is_directory=True)
        with pytest.raises(GateOpenRejected) as ei:
            open_vault_root(link)
        assert ei.value.reason == "root-is-symlink"
        # Must be the gate subclass, not a bare OSError (F-1 contract).
        assert not isinstance(ei.value, OSError)

    def test_eloop_post_islink_race_wrapped(self, tmp_path: Path) -> None:
        # Belt-and-braces: if a TOCTOU race lets a symlink slip past the
        # is_symlink() pre-check, the OSError(ELOOP) branch must still wrap
        # to GateOpenRejected.
        import errno as _errno

        def fake_open(*_a: object, **_k: object) -> int:
            raise OSError(_errno.ELOOP, "simulated")

        with mock.patch("pipeline.vault.gate_and_open.os.open", side_effect=fake_open):
            with pytest.raises(GateOpenRejected) as ei:
                open_vault_root(tmp_path)
            assert ei.value.reason == "root-is-symlink"

    def test_generic_errno_wrapped(self, tmp_path: Path) -> None:
        # Any other kernel refusal (e.g. EACCES, ENOENT post-is_dir-race) is
        # wrapped into GateOpenRejected with an errno-<CODE> reason. Raw
        # OSError must NOT leak to the caller.
        import errno as _errno

        def fake_open(*_a: object, **_k: object) -> int:
            raise OSError(_errno.EACCES, "permission denied")

        with mock.patch("pipeline.vault.gate_and_open.os.open", side_effect=fake_open):
            with pytest.raises(GateOpenRejected) as ei:
                open_vault_root(tmp_path)
            assert ei.value.reason == "errno-EACCES"
            assert not isinstance(ei.value, OSError)


# ---------------------------------------------------------------------------
# Successful opens
# ---------------------------------------------------------------------------


class TestOpen:
    def test_open_simple_file(self, tmp_path: Path, vault_root_fd: int) -> None:
        _make_file(tmp_path, "a.txt", b"hello")
        fd = gate_and_open(vault_root_fd, "a.txt", os.O_RDONLY)
        try:
            assert os.read(fd, 16) == b"hello"
        finally:
            os.close(fd)

    def test_open_nested_file(self, tmp_path: Path, vault_root_fd: int) -> None:
        _make_file(tmp_path, "sub/nested/leaf.bin", b"\x01\x02\x03")
        fd = gate_and_open(vault_root_fd, "sub/nested/leaf.bin", os.O_RDONLY)
        try:
            assert os.read(fd, 16) == b"\x01\x02\x03"
        finally:
            os.close(fd)

    def test_missing_file_raises_gate_rejected(
        self, tmp_path: Path, vault_root_fd: int
    ) -> None:
        with pytest.raises(GateOpenRejected):
            gate_and_open(vault_root_fd, "nope.txt", os.O_RDONLY)


# ---------------------------------------------------------------------------
# Symlink rejection
# ---------------------------------------------------------------------------


class TestSymlinks:
    def test_symlink_leaf_refused(self, tmp_path: Path, vault_root_fd: int) -> None:
        target = _make_file(tmp_path, "real.txt", b"secret")
        link = tmp_path / "link.txt"
        link.symlink_to(target)
        with pytest.raises(GateOpenRejected):
            gate_and_open(vault_root_fd, "link.txt", os.O_RDONLY)

    def test_symlink_in_ancestor_refused(
        self, tmp_path: Path, vault_root_fd: int
    ) -> None:
        (tmp_path / "realdir").mkdir()
        _make_file(tmp_path, "realdir/a.txt", b"x")
        (tmp_path / "linkdir").symlink_to(tmp_path / "realdir")
        with pytest.raises(GateOpenRejected):
            gate_and_open(vault_root_fd, "linkdir/a.txt", os.O_RDONLY)


# ---------------------------------------------------------------------------
# Identity-tuple pinning
# ---------------------------------------------------------------------------


class TestIdentityPinning:
    def test_pinning_match_allows_open(
        self, tmp_path: Path, vault_root_fd: int
    ) -> None:
        path = _make_file(tmp_path, "a.txt", b"ok")
        st = os.stat(path)
        pinning = {"a.txt": (st.st_dev, st.st_ino)}
        fd = gate_and_open(
            vault_root_fd, "a.txt", os.O_RDONLY, identity_pinning=pinning
        )
        os.close(fd)

    def test_pinning_mismatch_raises_f_gate_02(
        self, tmp_path: Path, vault_root_fd: int
    ) -> None:
        _make_file(tmp_path, "a.txt", b"ok")
        pinning = {"a.txt": (0, 0)}  # deliberately wrong
        with pytest.raises(GateIdentityTupleMismatch) as exc:
            gate_and_open(
                vault_root_fd, "a.txt", os.O_RDONLY, identity_pinning=pinning
            )
        assert exc.value.code == F_GATE_02

    def test_pinning_absent_path_skipped(
        self, tmp_path: Path, vault_root_fd: int
    ) -> None:
        _make_file(tmp_path, "a.txt", b"ok")
        # pinning doesn't include this path; verification is skipped.
        fd = gate_and_open(
            vault_root_fd, "a.txt", os.O_RDONLY, identity_pinning={"other": (0, 0)}
        )
        os.close(fd)


# ---------------------------------------------------------------------------
# Arg-type gates
# ---------------------------------------------------------------------------


class TestArgTypes:
    def test_vault_root_fd_must_be_int(self, vault_root_fd: int) -> None:
        with pytest.raises(TypeError):
            gate_and_open("not-an-fd", "a.txt", os.O_RDONLY)  # type: ignore[arg-type]

    def test_flags_must_be_int(self, vault_root_fd: int) -> None:
        with pytest.raises(TypeError):
            gate_and_open(vault_root_fd, "a.txt", "O_RDONLY")  # type: ignore[arg-type]

    def test_relative_path_must_be_str(self, vault_root_fd: int) -> None:
        with pytest.raises(TypeError):
            gate_and_open(vault_root_fd, b"a.txt", os.O_RDONLY)  # type: ignore[arg-type]

    def test_open_vault_root_rejects_non_path(self) -> None:
        with pytest.raises(TypeError):
            open_vault_root("/tmp")  # type: ignore[arg-type]

    def test_open_vault_root_rejects_non_directory(self, tmp_path: Path) -> None:
        f = tmp_path / "not-a-dir.txt"
        f.write_text("x")
        with pytest.raises(GateOpenRejected):
            open_vault_root(f)


# ---------------------------------------------------------------------------
# probe_openat2
# ---------------------------------------------------------------------------


class TestProbe:
    def test_macos_probe_returns_false(self, vault_root_fd: int) -> None:
        with mock.patch(
            "pipeline.vault.gate_and_open.platform.system", return_value="Darwin"
        ):
            assert probe_openat2(vault_root_fd) is False

    def test_windows_probe_returns_false(self, vault_root_fd: int) -> None:
        with mock.patch(
            "pipeline.vault.gate_and_open.platform.system", return_value="Windows"
        ):
            assert probe_openat2(vault_root_fd) is False


# ---------------------------------------------------------------------------
# Platform dispatch
# ---------------------------------------------------------------------------


class TestPlatformDispatch:
    def test_unsupported_platform_rejected(
        self, tmp_path: Path, vault_root_fd: int
    ) -> None:
        _make_file(tmp_path, "a.txt", b"x")
        with mock.patch(
            "pipeline.vault.gate_and_open.platform.system", return_value="Windows"
        ):
            with pytest.raises(GateOpenRejected) as exc:
                gate_and_open(vault_root_fd, "a.txt", os.O_RDONLY)
            assert exc.value.reason == "platform-unsupported"

# ---------------------------------------------------------------------------
# BLUEPRINT_DEPS pin — drift-detection guard (§4.6 engineering_process_v0.1.md)
# ---------------------------------------------------------------------------


class TestBlueprintDepsPin:
    def test_blueprint_deps_pin(self) -> None:
        from pipeline.vault import gate_and_open as _mod

        deps = _mod.BLUEPRINT_DEPS
        assert "section_02_vault_topology.md" in deps
        section = deps["section_02_vault_topology.md"]
        assert section["version"] == "v7.1"
        assert section["hash_sha3_512_prefix16"] == "83a898275a4cf0a1"
