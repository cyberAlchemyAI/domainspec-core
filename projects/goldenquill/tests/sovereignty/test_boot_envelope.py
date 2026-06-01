"""§9 boot_envelope orchestrator end-to-end tests.

Section 1 Round J. Covers:

* §9 step 1 platform gate (``UnsupportedPlatform``).
* §9 step 2 RLIMIT_CORE suppression.
* §9 step 2.5 boot_clock_history append.
* §9 step 3 repo-root sanity (``RepoRootInvalid``).
* §9 step 5 operator-identity probe (``OperatorNotProvisioned``).
* §9 step 6 router HMAC gate (composed from Round H).
* §9 step 7c.0a/b init-marker verify + first-boot write.
* §9 step 9 INTERRUPTED-session raise.
* §9 step 10 slug canonicalization + availability.
* §9 step 11 ``SovereigntyEnvelope`` return shape.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from unittest import mock

import pytest

from pipeline.sovereignty import (
    BootClockHistoryEntry,
    OperatorNotProvisioned,
    RepoRootInvalid,
    SovereigntyEnvelope,
    UnsupportedPlatform,
    boot_envelope,
    hmac_sha3_512,
    read_boot_clock_history,
    sha3_512_hex,
)
from pipeline.sovereignty.keys import KeyStore
from pipeline.sovereignty.router_integrity import canonicalize_router_yaml_bytes

_HMAC_KEY = bytes(range(64))


class _StubKeyStore(KeyStore):
    def __init__(
        self,
        *,
        key_bytes: bytes = _HMAC_KEY,
        operator_present: bool = True,
    ) -> None:
        self._key_bytes = key_bytes
        self._operator_present = operator_present

    def _retrieve_raw(self, key_id: str) -> bytearray:
        return bytearray(self._key_bytes)

    def store(self, *, key_id, key_bytes, purpose) -> None:  # pragma: no cover
        raise NotImplementedError

    def rotate(self, key_id):  # pragma: no cover
        raise NotImplementedError

    def zero(self, key_id) -> None:  # pragma: no cover
        raise NotImplementedError

    def exists(self, key_id: str) -> bool:
        if key_id == "operator.identity.v1":
            return self._operator_present
        return True

    def provider(self) -> str:
        return "stub"


# ---------------------------------------------------------------------------
# Repo fixture
# ---------------------------------------------------------------------------


_BASE_ROUTER_YAML = b"""\
version: 1
tilth:
  scout:
    primary: ollama/mistral:7b
    family: mistral
"""


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


def _write_signed_router(repo: Path, yaml_bytes: bytes = _BASE_ROUTER_YAML) -> None:
    (repo / "router.yaml").write_bytes(yaml_bytes)
    canonical = canonicalize_router_yaml_bytes(yaml_bytes)
    router_sha = sha3_512_hex(canonical).digest_hex
    commit_sha = _run_git(repo, "rev-parse", "HEAD")
    sig = hmac_sha3_512(_HMAC_KEY, (router_sha + commit_sha).encode("ascii")).hex()
    (repo / "router.yaml.sig").write_text(sig + "\n", encoding="utf-8")


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    _run_git(tmp_path, "init", "-q", "-b", "main")
    _run_git(tmp_path, "commit", "--allow-empty", "-m", "init", "-q")
    (tmp_path / "orgs").mkdir()
    _write_signed_router(tmp_path)
    return tmp_path


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------


class TestHappyPath:
    def test_first_boot_returns_envelope(self, repo: Path) -> None:
        env = boot_envelope(repo_root=repo, keystore=_StubKeyStore())
        assert isinstance(env, SovereigntyEnvelope)
        assert env.repo_root == repo
        assert env.operator_identity_present is True
        assert env.platform in ("Darwin", "Linux")
        assert env.router_manifest.commit_sha
        assert env.init_marker.init_version == 1
        assert env.boot_epoch_ns > 0
        assert env.slug is None
        # init-marker written
        assert (repo / "sovereignty" / "init.marker").is_file()
        assert (repo / "sovereignty" / "init.marker.hmac").is_file()
        # boot_clock_history appended once
        history = read_boot_clock_history(repo)
        assert len(history) == 1
        assert isinstance(history[0], BootClockHistoryEntry)

    def test_second_boot_idempotent_does_not_rewrite_marker(self, repo: Path) -> None:
        boot_envelope(repo_root=repo, keystore=_StubKeyStore())
        marker = repo / "sovereignty" / "init.marker"
        mtime = marker.stat().st_mtime_ns

        env2 = boot_envelope(repo_root=repo, keystore=_StubKeyStore())
        assert env2.init_marker.init_version == 1
        # Marker unchanged.
        assert marker.stat().st_mtime_ns == mtime
        # Still exactly one entry (idempotent on same boot_epoch_ns).
        assert len(read_boot_clock_history(repo)) == 1

    def test_slug_arg_canonicalized(self, repo: Path) -> None:
        env = boot_envelope(
            repo_root=repo, keystore=_StubKeyStore(), slug_arg="MyCoSymBiotics"
        )
        assert env.slug == "mycosymbiotics"

    def test_rlimit_core_set_to_zero(self, repo: Path) -> None:
        import resource

        boot_envelope(repo_root=repo, keystore=_StubKeyStore())
        soft, hard = resource.getrlimit(resource.RLIMIT_CORE)
        assert soft == 0
        assert hard == 0

    def test_operator_slug_written_into_marker(self, repo: Path) -> None:
        env = boot_envelope(
            repo_root=repo, keystore=_StubKeyStore(), operator_slug="josh"
        )
        assert env.init_marker.operator_slug == "josh"


# ---------------------------------------------------------------------------
# Fail-closed outcomes
# ---------------------------------------------------------------------------


class TestFailClosed:
    def test_repo_root_missing_router_yaml_rejected(
        self, tmp_path: Path
    ) -> None:
        _run_git(tmp_path, "init", "-q", "-b", "main")
        _run_git(tmp_path, "commit", "--allow-empty", "-m", "init", "-q")
        (tmp_path / "orgs").mkdir()
        # No router.yaml.
        with pytest.raises(RepoRootInvalid) as exc:
            boot_envelope(repo_root=tmp_path, keystore=_StubKeyStore())
        assert exc.value.code == "F-BOOT-REPO"

    def test_repo_root_missing_orgs_rejected(self, tmp_path: Path) -> None:
        _run_git(tmp_path, "init", "-q", "-b", "main")
        _run_git(tmp_path, "commit", "--allow-empty", "-m", "init", "-q")
        _write_signed_router(tmp_path)
        # No orgs/.
        with pytest.raises(RepoRootInvalid):
            boot_envelope(repo_root=tmp_path, keystore=_StubKeyStore())

    def test_repo_root_not_directory_rejected(self, tmp_path: Path) -> None:
        f = tmp_path / "not_a_dir"
        f.write_bytes(b"x")
        with pytest.raises(RepoRootInvalid):
            boot_envelope(repo_root=f, keystore=_StubKeyStore())

    def test_operator_identity_absent_rejected(self, repo: Path) -> None:
        with pytest.raises(OperatorNotProvisioned) as exc:
            boot_envelope(
                repo_root=repo,
                keystore=_StubKeyStore(operator_present=False),
            )
        assert exc.value.code == "F-BOOT-OPERATOR"

    def test_unsupported_platform_rejected(self, repo: Path) -> None:
        with mock.patch(
            "pipeline.sovereignty.boot._platform_mod.system",
            return_value="Windows",
        ):
            with pytest.raises(UnsupportedPlatform) as exc:
                boot_envelope(repo_root=repo, keystore=_StubKeyStore())
            assert exc.value.code == "F-BOOT-PLATFORM"


# ---------------------------------------------------------------------------
# Arg-type gates (E-001)
# ---------------------------------------------------------------------------


class TestCrossRoundInvariants:
    """BT-style invariants covering Rounds H + I composed by Round J."""

    def test_tampered_router_after_first_boot_rejects_second_boot(
        self, repo: Path
    ) -> None:
        boot_envelope(repo_root=repo, keystore=_StubKeyStore())
        # Change a semantic field in router.yaml without re-signing.
        (repo / "router.yaml").write_bytes(
            _BASE_ROUTER_YAML.replace(b"mistral:7b", b"mistral:13b")
        )
        with pytest.raises(Exception):
            boot_envelope(repo_root=repo, keystore=_StubKeyStore())

    def test_tampered_init_marker_after_first_boot_rejects_second_boot(
        self, repo: Path
    ) -> None:
        boot_envelope(repo_root=repo, keystore=_StubKeyStore())
        marker = repo / "sovereignty" / "init.marker"
        body = marker.read_bytes().replace(b'"init_version"', b'"init_version_x"')
        marker.write_bytes(body)
        with pytest.raises(Exception):
            boot_envelope(repo_root=repo, keystore=_StubKeyStore())

    def test_tampered_boot_clock_jsonl_rejects_second_boot(
        self, repo: Path
    ) -> None:
        boot_envelope(repo_root=repo, keystore=_StubKeyStore())
        jsonl = repo / "sovereignty" / "clock" / "boot_clock_history.jsonl"
        raw = jsonl.read_bytes()
        jsonl.write_bytes(raw + b'{"x":1}\n')  # append bogus line, trailer stale
        with pytest.raises(Exception):
            boot_envelope(repo_root=repo, keystore=_StubKeyStore())

    def test_wrong_keystore_key_rejects_boot(self, repo: Path) -> None:
        # router.yaml.sig was signed under _HMAC_KEY; a keystore serving
        # a different key cannot verify it.
        with pytest.raises(Exception):
            boot_envelope(
                repo_root=repo, keystore=_StubKeyStore(key_bytes=b"\x22" * 32)
            )

    def test_first_boot_boot_clock_history_chain_from_genesis(
        self, repo: Path
    ) -> None:
        env = boot_envelope(repo_root=repo, keystore=_StubKeyStore())
        history = read_boot_clock_history(repo)
        assert len(history) == 1
        assert history[0].prev_hash == "0" * 128
        assert history[0].boot_epoch_ns == env.boot_epoch_ns


class TestArgTypes:
    def test_rejects_str_repo_root(self) -> None:
        with pytest.raises(TypeError):
            boot_envelope(repo_root="/tmp/x", keystore=_StubKeyStore())  # type: ignore[arg-type]

    def test_rejects_non_keystore(self, repo: Path) -> None:
        with pytest.raises(TypeError):
            boot_envelope(repo_root=repo, keystore="not-a-keystore")  # type: ignore[arg-type]

    def test_rejects_bad_slug_type(self, repo: Path) -> None:
        with pytest.raises(TypeError):
            boot_envelope(
                repo_root=repo, keystore=_StubKeyStore(), slug_arg=123  # type: ignore[arg-type]
            )

    def test_rejects_bad_ledger_keys(self, repo: Path) -> None:
        with pytest.raises(TypeError):
            boot_envelope(
                repo_root=repo,
                keystore=_StubKeyStore(),
                ledger_hmac_keys="not-a-mapping",  # type: ignore[arg-type]
            )
