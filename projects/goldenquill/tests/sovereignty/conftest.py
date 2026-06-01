"""Shared fixtures for §1 Round J capstone tests.

Round J packages a cross-module test surface that exercises the full
§1 public API as a single boot → session → RFA → PROJECT_CONTEXT →
ledger lifecycle. The fixtures below mirror the pattern established
by :mod:`tests.sovereignty.test_boot_envelope`'s ``_StubKeyStore`` +
git-init ``repo`` fixture, promoted here so the three Round J test
files reuse one definition.

Per spec card `pipeline/engineering/spec_cards/section_1_round_j_capstone.md`
J.4 bullet 4 ("fixture library — clean vault, operator keypair,
sample RFA, sample PROJECT_CONTEXT").
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Iterator

import pytest

from pipeline.sovereignty import (
    hmac_sha3_512,
    sha3_512_hex,
)
from pipeline.sovereignty.keys import KeyStore
from pipeline.sovereignty.router_integrity import canonicalize_router_yaml_bytes


# ---------------------------------------------------------------------------
# Canonical HMAC-key constants
# ---------------------------------------------------------------------------

# 64-byte router-signing key (matches test_boot_envelope.py canonical pattern).
CAPSTONE_HMAC_KEY: bytes = bytes(range(64))

# Ledger HMAC keys (admin_risk + degradation per-ledger; plus watermarks).
# 32-byte minimum per sovereignty.crypto_primitives._DEFAULT_MIN_HMAC_KEY_BYTES.
CAPSTONE_LEDGER_KEY: bytes = b"L" * 32
CAPSTONE_WATERMARKS_KEY: bytes = b"W" * 32
CAPSTONE_DEGRADATION_KEY: bytes = b"D" * 32

# Base router.yaml used by _write_signed_router. Same shape as
# test_boot_envelope.py so verify_router_integrity accepts the manifest.
CAPSTONE_BASE_ROUTER_YAML: bytes = (
    b"version: 1\n"
    b"tilth:\n"
    b"  scout:\n"
    b"    primary: ollama/mistral:7b\n"
    b"    family: mistral\n"
)


# ---------------------------------------------------------------------------
# KeyStore stub (promoted from test_boot_envelope.py)
# ---------------------------------------------------------------------------


class CapstoneKeyStore(KeyStore):
    """Minimal ``KeyStore`` suitable for §1 end-to-end integration tests.

    Serves a single key buffer for every key_id request (same shape as
    ``_StubKeyStore`` in tests.sovereignty.test_boot_envelope). ``exists``
    reports True for every key EXCEPT when ``operator_present=False`` and
    the probed id is ``operator.identity.v1`` — the boot_envelope F-BOOT-
    OPERATOR gate.

    Session HMAC lifecycle (store / zero / retrieve) is implemented so
    ``start_session`` / ``end_session`` / ``sign_health_tuple`` / rotate
    all work end-to-end.
    """

    def __init__(
        self,
        *,
        key_bytes: bytes = CAPSTONE_HMAC_KEY,
        operator_present: bool = True,
    ) -> None:
        self._default_bytes = key_bytes
        self._operator_present = operator_present
        self._store: dict[str, bytearray] = {}

    # --- Required overrides -------------------------------------------------

    def _retrieve_raw(self, key_id: str) -> bytearray:
        stored = self._store.get(key_id)
        if stored is not None:
            return bytearray(stored)
        return bytearray(self._default_bytes)

    def store(self, *, key_id: str, key_bytes, purpose: str) -> None:
        self._store[key_id] = bytearray(bytes(key_bytes))

    def rotate(self, key_id: str) -> str:
        return key_id

    def zero(self, key_id: str) -> None:
        buf = self._store.get(key_id)
        if buf is not None:
            for i in range(len(buf)):
                buf[i] = 0
            del self._store[key_id]

    def exists(self, key_id: str) -> bool:
        if key_id == "operator.identity.v1":
            return self._operator_present
        return True

    def provider(self) -> str:
        return "capstone-stub"


# ---------------------------------------------------------------------------
# Git-init helpers
# ---------------------------------------------------------------------------


def run_git(repo: Path, *args: str) -> str:
    """Run a git command inside ``repo``; return stripped stdout.

    Uses a pinned author/committer so every commit hashes deterministically
    for a given repo seed. Mirrors ``tests.sovereignty.test_boot_envelope``'s
    ``_run_git``.
    """
    env = os.environ.copy()
    env.setdefault("GIT_AUTHOR_NAME", "Tester")
    env.setdefault("GIT_AUTHOR_EMAIL", "tester@example.com")
    env.setdefault("GIT_COMMITTER_NAME", "Tester")
    env.setdefault("GIT_COMMITTER_EMAIL", "tester@example.com")
    result = subprocess.run(
        ["git", *args],
        cwd=str(repo),
        capture_output=True,
        check=True,
        env=env,
        timeout=15,
    )
    return result.stdout.decode("utf-8", errors="replace").strip()


def write_signed_router(
    repo: Path,
    *,
    yaml_bytes: bytes = CAPSTONE_BASE_ROUTER_YAML,
    hmac_key: bytes = CAPSTONE_HMAC_KEY,
) -> None:
    """Write ``router.yaml`` + ``router.yaml.sig`` under ``repo``.

    The signature is
    ``hmac_sha3_512(hmac_key, router_sha_hex + commit_sha_hex)`` per Round H.
    """
    (repo / "router.yaml").write_bytes(yaml_bytes)
    canonical = canonicalize_router_yaml_bytes(yaml_bytes)
    router_sha = sha3_512_hex(canonical).digest_hex
    commit_sha = run_git(repo, "rev-parse", "HEAD")
    sig = hmac_sha3_512(
        hmac_key,
        (router_sha + commit_sha).encode("ascii"),
    ).hex()
    (repo / "router.yaml.sig").write_text(sig + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Core fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def capstone_repo(tmp_path: Path) -> Path:
    """A freshly-initialised clean Tilth vault.

    Layout after the fixture returns:

    * git-initialised, one empty ``init`` commit on ``main``
    * ``orgs/`` directory present (empty)
    * ``router.yaml`` + ``router.yaml.sig`` (HMAC-signed under
      ``CAPSTONE_HMAC_KEY``)

    This is the pre-boot state consumed by :func:`boot_envelope`.
    """
    run_git(tmp_path, "init", "-q", "-b", "main")
    run_git(tmp_path, "commit", "--allow-empty", "-m", "init", "-q")
    (tmp_path / "orgs").mkdir()
    write_signed_router(tmp_path)
    return tmp_path


@pytest.fixture
def capstone_keystore() -> CapstoneKeyStore:
    """Default keystore used by the majority of capstone tests.

    Reports ``operator.identity.v1`` present so boot_envelope clears
    the F-BOOT-OPERATOR gate; serves the canonical 64-byte
    ``CAPSTONE_HMAC_KEY`` for router-signature verification.
    """
    return CapstoneKeyStore()


@pytest.fixture
def capstone_ledger_keys() -> dict[str, bytes]:
    """Per-ledger HMAC keys the capstone tests hand to record_* APIs."""
    return {
        "admin_risk": CAPSTONE_LEDGER_KEY,
        "degradation": CAPSTONE_DEGRADATION_KEY,
        "watermarks": CAPSTONE_WATERMARKS_KEY,
    }


@pytest.fixture
def capstone_slug() -> str:
    """Default org slug used by the integration fixtures."""
    return "mycosymbiotics"


@pytest.fixture
def capstone_org_dir(capstone_repo: Path, capstone_slug: str) -> Path:
    """Provision an ``orgs/<slug>/`` directory with a canonical
    ``PROJECT_CONTEXT.md``.

    The body is deliberately minimal so tests that mutate it can
    observe drift without fighting the hashing.
    """
    org_dir = capstone_repo / "orgs" / capstone_slug
    org_dir.mkdir(parents=True, exist_ok=True)
    (org_dir / "PROJECT_CONTEXT.md").write_text(
        "# PROJECT_CONTEXT — mycosymbiotics\n\nseed: 1\n",
        encoding="utf-8",
    )
    return org_dir


@pytest.fixture
def capstone_rfa_bytes() -> bytes:
    """Deterministic RFA content used in ingest/reverify paths."""
    return b"# Sample RFA\n\nfunder: Test Foundation\nceiling: $50000\n"


@pytest.fixture
def capstone_rfa_url() -> str:
    """Stable URL for ingest_rfa; url_hash invariance is a BT1 property."""
    return "https://grants.example.gov/sample/RFA-2026-TEST-0001"


# ---------------------------------------------------------------------------
# Misc. helpers (function-scope, imported by test modules)
# ---------------------------------------------------------------------------


def isolate_active_runtime() -> Iterator[None]:
    """Clear the module-global session runtime before and after a test.

    Some integration tests start and end sessions; if an earlier test
    left the ``_active_runtime`` slot bound (e.g. after a failure), the
    next ``start_session`` call would raise ``SessionAlreadyActive``.
    Not auto-applied — test modules that need it opt in explicitly.
    """
    from pipeline.sovereignty import session as _session

    _session._set_active_runtime(None)
    yield
    _session._set_active_runtime(None)
