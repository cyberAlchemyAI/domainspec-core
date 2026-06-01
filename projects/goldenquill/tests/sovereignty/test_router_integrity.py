"""Unit + adversarial tests for pipeline.sovereignty.router_integrity.

Section 1 Round H. Covers §2.7 RouterManifest + §3.10 verify_router_integrity
+ §3.10.1 orthogonality vs §4 boot-time git-sig gate + §4.4 M5 cross-family
+ §6.4 F-RTR-01..04 + §7.7 named tests.

Named tests per §7.7 / blueprint lines 2494-2496 + 2665-2667:

* ``test_m5_router_integrity_fail_closed_unsigned`` — signature_missing
* ``test_m5_router_integrity_fail_closed_tampered`` — signature_mismatch
* ``test_m5_router_integrity_yaml_semantic_equivalent`` — whitespace/key-order
  reorder that parses to the same content round-trips to the same canonical
  bytes (positive test — canonicalization is robust).
* ``test_m5_cross_family_violation_raised``
* ``test_router_integrity_hmac_binds_to_git_commit_sha`` — changing HEAD
  without re-signing → commit-binding mismatch.

Plus E-001 arg-type gates, RouterManifest persistence, git_unavailable
path, and empty/garbled signature file handling.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

from pipeline.sovereignty import (
    SecretBytes,
    hmac_sha3_512,
    sha3_512_hex,
)
from pipeline.sovereignty.keys import KeyStore
from pipeline.sovereignty.router_integrity import (
    ROUTER_HMAC_KEY_ID,
    CrossFamilyViolation,
    RouterHMACMismatch,
    RouterIntegrityError,
    RouterManifest,
    RouterYAMLParseError,
    assert_cross_family,
    canonicalize_router_yaml_bytes,
    verify_router_integrity,
)

# ---------------------------------------------------------------------------
# Test key material + minimal KeyStore double
# ---------------------------------------------------------------------------

_HMAC_KEY = bytes(range(64))  # deterministic 64-byte key


class _StubKeyStore(KeyStore):
    """Minimal KeyStore for tests — returns a bytearray of the fixed HMAC key.

    Subclasses KeyStore and overrides only `_retrieve_raw` (the sealed
    `retrieve()` path wraps our bytearray in a fresh SecretBytes on each
    call, per §3.11 v3 HIGH-3 contract).
    """

    def __init__(self, *, key_bytes: bytes = _HMAC_KEY, missing: bool = False) -> None:
        self._key_bytes = key_bytes
        self._missing = missing

    def _retrieve_raw(self, key_id: str) -> bytearray:
        if self._missing:
            raise KeyError(f"key {key_id!r} not present")
        return bytearray(self._key_bytes)

    def store(self, *, key_id: str, key_bytes, purpose: str) -> None:  # pragma: no cover
        raise NotImplementedError

    def rotate(self, key_id: str) -> str:  # pragma: no cover
        raise NotImplementedError

    def zero(self, key_id: str) -> None:  # pragma: no cover
        raise NotImplementedError

    def exists(self, key_id: str) -> bool:
        return not self._missing

    def provider(self) -> str:
        return "stub"


# ---------------------------------------------------------------------------
# Git fixture
# ---------------------------------------------------------------------------


def _run_git(repo: Path, *args: str) -> str:
    env = os.environ.copy()
    env.setdefault("GIT_AUTHOR_NAME", "Tester")
    env.setdefault("GIT_AUTHOR_EMAIL", "tester@example.com")
    env.setdefault("GIT_COMMITTER_NAME", "Tester")
    env.setdefault("GIT_COMMITTER_EMAIL", "tester@example.com")
    result = subprocess.run(
        ["git", *args], cwd=str(repo), capture_output=True, check=True,
        env=env, timeout=15,
    )
    return result.stdout.decode("utf-8", errors="replace").strip()


@pytest.fixture
def git_repo(tmp_path: Path) -> Path:
    """Init a git repo in tmp_path with one empty commit so HEAD resolves."""
    _run_git(tmp_path, "init", "-q", "-b", "main")
    _run_git(tmp_path, "commit", "--allow-empty", "-m", "init", "-q")
    return tmp_path


def _sign_router(repo: Path, router_yaml_bytes: bytes, key: bytes = _HMAC_KEY) -> tuple[str, str]:
    """Write router.yaml + router.yaml.sig. Returns (canonical_sha, commit_sha)."""
    (repo / "router.yaml").write_bytes(router_yaml_bytes)
    canonical = canonicalize_router_yaml_bytes(router_yaml_bytes)
    router_yaml_sha = sha3_512_hex(canonical).digest_hex
    commit_sha = _run_git(repo, "rev-parse", "HEAD")
    sig = hmac_sha3_512(key, (router_yaml_sha + commit_sha).encode("ascii")).hex()
    (repo / "router.yaml.sig").write_text(sig + "\n", encoding="utf-8")
    return router_yaml_sha, commit_sha


_BASE_ROUTER_YAML = b"""\
version: 1
tilth:
  scout:
    primary: ollama/mistral:7b
    family: mistral
  scribe:
    primary: anthropic/claude-opus-4-7
    family: anthropic
"""


# ---------------------------------------------------------------------------
# canonicalize_router_yaml_bytes
# ---------------------------------------------------------------------------


class TestCanonicalize:
    def test_basic_roundtrip_deterministic(self) -> None:
        out1 = canonicalize_router_yaml_bytes(_BASE_ROUTER_YAML)
        out2 = canonicalize_router_yaml_bytes(_BASE_ROUTER_YAML)
        assert out1 == out2

    def test_bom_stripped(self) -> None:
        with_bom = b"\xef\xbb\xbf" + _BASE_ROUTER_YAML
        assert canonicalize_router_yaml_bytes(with_bom) == canonicalize_router_yaml_bytes(_BASE_ROUTER_YAML)

    def test_crlf_normalized(self) -> None:
        crlf = _BASE_ROUTER_YAML.replace(b"\n", b"\r\n")
        assert canonicalize_router_yaml_bytes(crlf) == canonicalize_router_yaml_bytes(_BASE_ROUTER_YAML)

    def test_trailing_whitespace_stripped(self) -> None:
        padded = _BASE_ROUTER_YAML.replace(b"version: 1\n", b"version: 1   \n")
        assert canonicalize_router_yaml_bytes(padded) == canonicalize_router_yaml_bytes(_BASE_ROUTER_YAML)

    def test_reordered_keys_same_hash(self) -> None:
        """§7.7 positive: key reorder that parses to the same mapping must
        canonicalize to the same bytes."""
        reordered = b"""\
tilth:
  scribe:
    family: anthropic
    primary: anthropic/claude-opus-4-7
  scout:
    family: mistral
    primary: ollama/mistral:7b
version: 1
"""
        assert canonicalize_router_yaml_bytes(reordered) == canonicalize_router_yaml_bytes(_BASE_ROUTER_YAML)

    def test_bad_yaml_raises_parse_error(self) -> None:
        with pytest.raises(RouterYAMLParseError) as exc:
            canonicalize_router_yaml_bytes(b"{:\n  broken: [unclosed\n")
        assert exc.value.reason == "yaml_parse_error"
        assert exc.value.code == "F-RTR-02"

    @pytest.mark.parametrize("bad", [None, "string", 42, [b"x"]])
    def test_type_error_on_non_bytes(self, bad) -> None:
        with pytest.raises(TypeError):
            canonicalize_router_yaml_bytes(bad)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# verify_router_integrity happy path + persistence
# ---------------------------------------------------------------------------


class TestVerifyHappyPath:
    def test_returns_manifest_and_persists(self, git_repo: Path) -> None:
        router_sha, commit_sha = _sign_router(git_repo, _BASE_ROUTER_YAML)
        store = _StubKeyStore()

        manifest = verify_router_integrity(repo_root=git_repo, keystore=store)

        assert isinstance(manifest, RouterManifest)
        assert manifest.router_yaml_sha == router_sha
        assert manifest.commit_sha == commit_sha
        assert manifest.signed_by_key_id == ROUTER_HMAC_KEY_ID
        assert len(manifest.signature_hex) == 128
        assert manifest.verified_at.endswith("Z")

        out = git_repo / "sovereignty" / "router" / "manifest.latest.json"
        assert out.is_file()
        body = json.loads(out.read_text(encoding="utf-8"))
        assert body["router_yaml_sha"] == router_sha
        assert body["commit_sha"] == commit_sha
        assert body["signed_by_key_id"] == ROUTER_HMAC_KEY_ID

    def test_session_id_writes_distinct_manifest(self, git_repo: Path) -> None:
        _sign_router(git_repo, _BASE_ROUTER_YAML)
        verify_router_integrity(
            repo_root=git_repo, keystore=_StubKeyStore(), session_id="sess-abc"
        )
        out = git_repo / "sovereignty" / "router" / "manifest.sess-abc.json"
        assert out.is_file()

    def test_whitespace_reorder_still_verifies(self, git_repo: Path) -> None:
        """Whitespace-only tamper to router.yaml AFTER signing still verifies
        because canonicalization absorbs the drift."""
        _sign_router(git_repo, _BASE_ROUTER_YAML)
        noisy = _BASE_ROUTER_YAML.replace(b"version: 1\n", b"version: 1   \n")
        (git_repo / "router.yaml").write_bytes(noisy)
        # Should not raise.
        verify_router_integrity(repo_root=git_repo, keystore=_StubKeyStore())


# ---------------------------------------------------------------------------
# Fail-closed paths (§7.7 named tests)
# ---------------------------------------------------------------------------


class TestFailClosed:
    def test_m5_router_integrity_fail_closed_unsigned(self, git_repo: Path) -> None:
        """§7.7 — absent router.yaml.sig → signature_missing."""
        (git_repo / "router.yaml").write_bytes(_BASE_ROUTER_YAML)
        with pytest.raises(RouterIntegrityError) as exc:
            verify_router_integrity(repo_root=git_repo, keystore=_StubKeyStore())
        assert exc.value.reason == "signature_missing"

    def test_m5_router_integrity_fail_closed_tampered(self, git_repo: Path) -> None:
        """§7.7 — flip a content byte in router.yaml post-sign → mismatch."""
        _sign_router(git_repo, _BASE_ROUTER_YAML)
        tampered = _BASE_ROUTER_YAML.replace(
            b"ollama/mistral:7b", b"ollama/malware:7b"
        )
        (git_repo / "router.yaml").write_bytes(tampered)
        with pytest.raises(RouterHMACMismatch) as exc:
            verify_router_integrity(repo_root=git_repo, keystore=_StubKeyStore())
        assert exc.value.reason == "signature_mismatch"
        assert exc.value.code == "F-RTR-02"

    def test_m5_router_integrity_yaml_semantic_equivalent(self, git_repo: Path) -> None:
        """§7.7 — reordering keys (semantically identical) still verifies."""
        _sign_router(git_repo, _BASE_ROUTER_YAML)
        reordered = b"""\
tilth:
  scribe:
    family: anthropic
    primary: anthropic/claude-opus-4-7
  scout:
    family: mistral
    primary: ollama/mistral:7b
version: 1
"""
        (git_repo / "router.yaml").write_bytes(reordered)
        # Should verify — canonicalization makes these hash-equivalent.
        verify_router_integrity(repo_root=git_repo, keystore=_StubKeyStore())

    def test_tampered_signature_byte_flip(self, git_repo: Path) -> None:
        """Flip a byte in the stored sig → mismatch."""
        _sign_router(git_repo, _BASE_ROUTER_YAML)
        sig_path = git_repo / "router.yaml.sig"
        sig = sig_path.read_text(encoding="utf-8").strip()
        flipped = ("a" if sig[0] != "a" else "b") + sig[1:]
        sig_path.write_text(flipped, encoding="utf-8")
        with pytest.raises(RouterHMACMismatch):
            verify_router_integrity(repo_root=git_repo, keystore=_StubKeyStore())

    def test_router_integrity_hmac_binds_to_git_commit_sha(self, git_repo: Path) -> None:
        """§7.7 — commit binding. Re-signing at commit A then advancing HEAD
        to commit B without re-signing → mismatch (sig was bound to A)."""
        _sign_router(git_repo, _BASE_ROUTER_YAML)
        # Advance HEAD.
        (git_repo / "unrelated.txt").write_text("x", encoding="utf-8")
        _run_git(git_repo, "add", "unrelated.txt")
        _run_git(git_repo, "commit", "-m", "advance", "-q")
        with pytest.raises(RouterHMACMismatch) as exc:
            verify_router_integrity(repo_root=git_repo, keystore=_StubKeyStore())
        assert exc.value.reason == "signature_mismatch"

    def test_empty_signature_file_rejected(self, git_repo: Path) -> None:
        _sign_router(git_repo, _BASE_ROUTER_YAML)
        (git_repo / "router.yaml.sig").write_text("", encoding="utf-8")
        with pytest.raises(RouterIntegrityError) as exc:
            verify_router_integrity(repo_root=git_repo, keystore=_StubKeyStore())
        assert exc.value.reason == "signature_missing"

    def test_malformed_signature_rejected(self, git_repo: Path) -> None:
        """Non-hex / wrong-length sig → signature_mismatch."""
        _sign_router(git_repo, _BASE_ROUTER_YAML)
        (git_repo / "router.yaml.sig").write_text("not-a-hex-sig\n", encoding="utf-8")
        with pytest.raises(RouterIntegrityError) as exc:
            verify_router_integrity(repo_root=git_repo, keystore=_StubKeyStore())
        assert exc.value.reason == "signature_mismatch"

    def test_missing_router_yaml_raises_filenotfound(self, git_repo: Path) -> None:
        with pytest.raises(FileNotFoundError):
            verify_router_integrity(repo_root=git_repo, keystore=_StubKeyStore())

    def test_keystore_missing_key_raises_rtr(self, git_repo: Path) -> None:
        _sign_router(git_repo, _BASE_ROUTER_YAML)
        with pytest.raises(RouterIntegrityError) as exc:
            verify_router_integrity(
                repo_root=git_repo, keystore=_StubKeyStore(missing=True)
            )
        assert exc.value.reason == "keystore_key_missing"

    def test_parse_error_surfaces_as_router_integrity_error(self, git_repo: Path) -> None:
        """Garbled router.yaml + any sig → RouterYAMLParseError (subclass of
        RouterIntegrityError)."""
        (git_repo / "router.yaml").write_bytes(b"{: bad yaml [unclosed\n")
        (git_repo / "router.yaml.sig").write_text("00" * 64, encoding="utf-8")
        with pytest.raises(RouterIntegrityError) as exc:
            verify_router_integrity(repo_root=git_repo, keystore=_StubKeyStore())
        assert exc.value.reason == "yaml_parse_error"

    def test_no_git_repo_raises_git_unavailable(self, tmp_path: Path) -> None:
        """Dir with router.yaml + sig but no .git → git rev-parse fails."""
        (tmp_path / "router.yaml").write_bytes(_BASE_ROUTER_YAML)
        (tmp_path / "router.yaml.sig").write_text("a" * 128, encoding="utf-8")
        with pytest.raises(RouterIntegrityError) as exc:
            verify_router_integrity(repo_root=tmp_path, keystore=_StubKeyStore())
        assert exc.value.reason == "git_unavailable"


# ---------------------------------------------------------------------------
# E-001 arg-type gates
# ---------------------------------------------------------------------------


class TestArgTypes:
    def test_repo_root_must_be_path(self) -> None:
        with pytest.raises(TypeError):
            verify_router_integrity(
                repo_root="/not/a/path", keystore=_StubKeyStore()  # type: ignore[arg-type]
            )

    def test_keystore_must_be_keystore(self, git_repo: Path) -> None:
        with pytest.raises(TypeError):
            verify_router_integrity(
                repo_root=git_repo, keystore="not-a-keystore"  # type: ignore[arg-type]
            )

    def test_session_id_must_be_str_or_none(self, git_repo: Path) -> None:
        _sign_router(git_repo, _BASE_ROUTER_YAML)
        with pytest.raises(TypeError):
            verify_router_integrity(
                repo_root=git_repo,
                keystore=_StubKeyStore(),
                session_id=123,  # type: ignore[arg-type]
            )


# ---------------------------------------------------------------------------
# Cross-family invariant (§4.4 M5 runtime)
# ---------------------------------------------------------------------------


class TestAssertCrossFamily:
    def test_m5_cross_family_violation_raised(self) -> None:
        """§7.7 — equal families → CrossFamilyViolation."""
        with pytest.raises(CrossFamilyViolation) as exc:
            assert_cross_family("anthropic", "anthropic")
        assert exc.value.author_family == "anthropic"
        assert exc.value.reviewer_family == "anthropic"

    def test_distinct_families_pass(self) -> None:
        assert_cross_family("anthropic", "groq")
        assert_cross_family("openai", "google")

    @pytest.mark.parametrize("bad", [None, 42, b"anthropic", ["anthropic"]])
    def test_type_errors(self, bad) -> None:
        with pytest.raises(TypeError):
            assert_cross_family(bad, "anthropic")  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            assert_cross_family("anthropic", bad)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Exception taxonomy (E-014)
# ---------------------------------------------------------------------------


class TestExceptionTaxonomy:
    def test_all_router_errors_descend_from_parent(self) -> None:
        assert issubclass(RouterHMACMismatch, RouterIntegrityError)
        assert issubclass(RouterYAMLParseError, RouterIntegrityError)

    def test_catching_parent_catches_all(self, git_repo: Path) -> None:
        """E-014 — callers only need the parent to handle the family."""
        (git_repo / "router.yaml").write_bytes(_BASE_ROUTER_YAML)
        try:
            verify_router_integrity(repo_root=git_repo, keystore=_StubKeyStore())
        except RouterIntegrityError as exc:
            assert exc.reason == "signature_missing"
        else:
            pytest.fail("expected RouterIntegrityError")

    def test_cross_family_violation_has_code(self) -> None:
        assert CrossFamilyViolation.code == "F-RTR-CROSS-FAMILY"


# ---------------------------------------------------------------------------
# §3.10.1 orthogonality smoke — manifest does NOT depend on any §4 gate
# ---------------------------------------------------------------------------


class TestOrthogonality:
    def test_verify_does_not_touch_section_4_state(self, git_repo: Path) -> None:
        """§3.10.1 — §1 runtime-load HMAC gate is orthogonal to §4 boot-time
        git-sig gate. verify_router_integrity writes only to
        sovereignty/router/ and never to §4's boot state dirs."""
        _sign_router(git_repo, _BASE_ROUTER_YAML)
        verify_router_integrity(repo_root=git_repo, keystore=_StubKeyStore())
        # Only the manifest dir should exist under sovereignty/.
        sovereignty_dir = git_repo / "sovereignty"
        assert sovereignty_dir.is_dir()
        subdirs = {p.name for p in sovereignty_dir.iterdir()}
        assert subdirs == {"router"}
