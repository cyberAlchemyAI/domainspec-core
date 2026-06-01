"""Router integrity — HMAC-SHA3-512 over canonicalized router.yaml bytes + git HEAD SHA.

Section 1 Round H. Owns:

* :class:`RouterManifest` — §2.7 schema frozen dataclass.
* :class:`RouterIntegrityError` (+ ``RouterHMACMismatch`` /
  ``RouterYAMLParseError`` / ``RouterCommitShaMismatch``) — §6.4 F-RTR-*.
* :func:`verify_router_integrity` — §3.10 runtime-load HMAC gate; orthogonal
  to §4 Logician's boot-time git-sig gate (§3.10.1).
* :func:`assert_cross_family` — §4.4 M5 runtime cross-family predicate
  (author_family != reviewer_family).

Blueprint references:

* §2.7   RouterManifest schema
* §3.10  verify_router_integrity signature
* §3.10.1 orthogonality clarification vs §4 git-sig gate (v6 amendment)
* §4.4   M5 router-integrity + cross-family invariant
* §6.4   F-RTR-01..04 failure codes
* §7.7   unit tests (test_m5_*)
* §8     ROUTER_HMAC_KEY_ID = "router.signing.hmac.v1"

E-enforcement:

* E-001 arg-type validation before any I/O
* E-005 canonical JSON / canonical YAML for hash input (yaml.safe_dump(load))
* E-014 family exception taxonomy (:class:`RouterIntegrityError` parent)

v0.1 scope (deferred):

* §2 Vault-mediated read — current implementation reads via direct
  ``Path.read_bytes()``; Round I boot.py can swap in ``vault.vault_read``
  once §2 Vault ships. Blueprint §3.10.1 calls this out explicitly.
* Section-5 call-site integration of ``assert_cross_family`` — Section 1
  only exports the predicate.
"""

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

import yaml

from pipeline.sovereignty.crypto_primitives import (
    SecretBytes,
    constant_time_equal,
    hmac_sha3_512,
    sha3_512_hex,
)
from pipeline.sovereignty.keys import KeyStore

__all__ = [
    "ROUTER_HMAC_KEY_ID",
    "RouterManifest",
    "RouterIntegrityError",
    "RouterHMACMismatch",
    "RouterYAMLParseError",
    "RouterCommitShaMismatch",
    "CrossFamilyViolation",
    "assert_cross_family",
    "canonicalize_router_yaml_bytes",
    "verify_router_integrity",
]

BLUEPRINT_DEPS = {
    "section_1_sovereignty_envelope.md": {
        "sections_implemented": [
            "§2.7 RouterManifest",
            "§3.10 + §3.10.1 verify_router_integrity",
            "§4.4 M5 router-integrity + cross-family",
            "§6.4 F-RTR-01..04",
            "§7.7 unit tests",
        ],
        "hash_at_lock": None,
        "hash_source_version": "v6",
    },
}

ROUTER_HMAC_KEY_ID: str = "router.signing.hmac.v1"


# ---------------------------------------------------------------------------
# Exceptions (E-014 family taxonomy)
# ---------------------------------------------------------------------------


class RouterIntegrityError(RuntimeError):
    """Common parent for F-RTR-01..04. Carries a ``code`` attribute and
    a ``reason`` attribute (one of ``signature_missing`` /
    ``signature_mismatch`` / ``git_unavailable`` /
    ``keystore_key_missing`` / ``commit_sha_mismatch`` / ``yaml_parse_error``).
    """

    code: str = "F-RTR"

    def __init__(self, reason: str, *args) -> None:
        super().__init__(f"F-RTR {reason}", *args)
        self.reason = reason


class RouterHMACMismatch(RouterIntegrityError):
    """F-RTR-02. HMAC-SHA3-512 over canonicalized bytes does not match sig."""

    code = "F-RTR-02"


class RouterYAMLParseError(RouterIntegrityError):
    """Canonicalization failed because router.yaml is not parseable."""

    code = "F-RTR-02"


class RouterCommitShaMismatch(RouterIntegrityError):
    """The sig was HMAC'd against a different commit SHA than the runtime HEAD."""

    code = "F-RTR-02"


class CrossFamilyViolation(RuntimeError):
    """§4.4 M5 runtime invariant: author_family == reviewer_family."""

    code = "F-RTR-CROSS-FAMILY"

    def __init__(self, *, author_family: str, reviewer_family: str) -> None:
        super().__init__(
            f"F-RTR cross-family violation: author={author_family!r} "
            f"reviewer={reviewer_family!r}"
        )
        self.author_family = author_family
        self.reviewer_family = reviewer_family


# ---------------------------------------------------------------------------
# Dataclass (§2.7)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class RouterManifest:
    """§2.7 schema. Frozen. Produced by :func:`verify_router_integrity`."""

    router_yaml_sha: str
    commit_sha: str
    signed_by_key_id: str
    signature_hex: str
    verified_at: str


# ---------------------------------------------------------------------------
# Canonicalization (§4.4 step 2)
# ---------------------------------------------------------------------------


def canonicalize_router_yaml_bytes(router_yaml_bytes: bytes) -> bytes:
    """Produce canonical bytes for HMAC input. [§4.4 step 2]

    Step 1: strip BOM, normalize line endings to ``\\n``, strip trailing
    whitespace per line.
    Step 2: ``yaml.safe_load`` + ``yaml.safe_dump(..., sort_keys=True,
    default_flow_style=False)`` + UTF-8 encode. Round-trip through the YAML
    parser so whitespace/key-order drift that parses to the same content
    produces the same canonical bytes — prevents whitespace-only tamper
    attacks.

    :raises RouterYAMLParseError: if YAML parse or dump fails.
    :raises TypeError: if arg is not bytes.
    """
    if not isinstance(router_yaml_bytes, (bytes, bytearray)):
        raise TypeError("router_yaml_bytes must be bytes")

    raw = bytes(router_yaml_bytes)
    # Strip BOM.
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    text = raw.decode("utf-8", errors="strict")
    # Normalize line endings + strip trailing whitespace per line.
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").split("\n")]
    normalized = "\n".join(lines).lstrip("\n")

    try:
        parsed = yaml.safe_load(normalized)
    except yaml.YAMLError as exc:
        raise RouterYAMLParseError(
            "yaml_parse_error", f"router.yaml could not be parsed: {exc}"
        ) from exc

    try:
        reserialized = yaml.safe_dump(
            parsed, sort_keys=True, default_flow_style=False, allow_unicode=True
        )
    except yaml.YAMLError as exc:
        raise RouterYAMLParseError(
            "yaml_parse_error",
            f"router.yaml could not be canonicalized: {exc}",
        ) from exc

    return reserialized.encode("utf-8")


# ---------------------------------------------------------------------------
# Cross-family invariant (§4.4 M5 runtime check)
# ---------------------------------------------------------------------------


def assert_cross_family(author_family: str, reviewer_family: str) -> None:
    """§4.4 M5 runtime invariant. Raises :class:`CrossFamilyViolation` if
    the two families are equal.

    Families are strings like ``"anthropic"``, ``"openai"``, ``"groq"``,
    ``"google"``. Section 5 (Pipeline) calls this on every seat dispatch;
    Section 1 only provides the predicate.

    :raises TypeError: if either arg is not str.
    :raises CrossFamilyViolation: on equality.
    """
    if not isinstance(author_family, str):
        raise TypeError("author_family must be str")
    if not isinstance(reviewer_family, str):
        raise TypeError("reviewer_family must be str")
    if author_family == reviewer_family:
        raise CrossFamilyViolation(
            author_family=author_family, reviewer_family=reviewer_family
        )


# ---------------------------------------------------------------------------
# Git HEAD resolution
# ---------------------------------------------------------------------------


def _git_rev_parse_head(repo_root: Path) -> str:
    """Return the 40-char git HEAD SHA for ``repo_root``.

    :raises RouterIntegrityError: if git is unavailable or the call fails.
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(repo_root),
            capture_output=True,
            check=False,
            timeout=10,
        )
    except FileNotFoundError as exc:
        raise RouterIntegrityError(
            "git_unavailable", f"git binary not found: {exc}"
        ) from exc
    except subprocess.TimeoutExpired as exc:
        raise RouterIntegrityError(
            "git_unavailable", f"git rev-parse timed out: {exc}"
        ) from exc
    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace").strip()
        raise RouterIntegrityError(
            "git_unavailable",
            f"git rev-parse HEAD failed (rc={result.returncode}): {stderr}",
        )
    sha = result.stdout.decode("ascii", errors="replace").strip()
    if len(sha) < 7 or not all(c in "0123456789abcdef" for c in sha.lower()):
        raise RouterIntegrityError(
            "git_unavailable", f"git rev-parse HEAD returned bad SHA: {sha!r}"
        )
    return sha


# ---------------------------------------------------------------------------
# Public API — verify_router_integrity
# ---------------------------------------------------------------------------


def _iso_utc_now() -> str:
    import datetime as _dt

    return (
        _dt.datetime.now(_dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def verify_router_integrity(
    *,
    repo_root: Path,
    keystore: KeyStore,
    session_id: str | None = None,
) -> RouterManifest:
    """§3.10 runtime-load HMAC gate over ``router.yaml`` + git HEAD SHA.

    Steps (§4.4):

    1. Read ``repo_root/router.yaml``.
    2. Canonicalize via :func:`canonicalize_router_yaml_bytes`.
    3. Compute ``router_yaml_sha = sha3_512(canonical_bytes)``.
    4. Resolve ``commit_sha`` via ``git rev-parse HEAD`` run in ``repo_root``.
    5. Read ``router.yaml.sig`` (hex HMAC-SHA3-512); absent → F-RTR-01.
    6. Load ``router.signing.hmac.v1`` from the keystore.
    7. Compute expected = ``hmac_sha3_512(key, router_yaml_sha || commit_sha)``.
    8. ``constant_time_equal`` against stored sig; mismatch → F-RTR-02.
    9. Persist :class:`RouterManifest` to
       ``sovereignty/router/manifest.{session_id}.json`` (or
       ``manifest.latest.json`` when session_id is None).
    10. Return the manifest.

    :raises TypeError: bad args (E-001).
    :raises FileNotFoundError: router.yaml does not exist.
    :raises RouterIntegrityError: signature_missing / signature_mismatch /
        git_unavailable / keystore_key_missing / yaml_parse_error.
    """
    if not isinstance(repo_root, Path):
        raise TypeError("repo_root must be pathlib.Path")
    if not isinstance(keystore, KeyStore):
        raise TypeError("keystore must be a KeyStore instance")
    if session_id is not None and not isinstance(session_id, str):
        raise TypeError("session_id must be str or None")

    router_yaml_path = repo_root / "router.yaml"
    sig_path = repo_root / "router.yaml.sig"

    # Step 1 — read router.yaml.
    if not router_yaml_path.is_file():
        raise FileNotFoundError(f"router.yaml missing at {router_yaml_path}")
    router_yaml_bytes = router_yaml_path.read_bytes()

    # Step 2 — canonicalize (may raise RouterYAMLParseError).
    canonical = canonicalize_router_yaml_bytes(router_yaml_bytes)

    # Step 3 — sha3_512 over canonical bytes.
    router_yaml_sha = sha3_512_hex(canonical).digest_hex

    # Step 4 — git rev-parse HEAD.
    commit_sha = _git_rev_parse_head(repo_root)

    # Step 5 — read signature file.
    if not sig_path.is_file():
        raise RouterIntegrityError(
            "signature_missing",
            f"router.yaml.sig missing at {sig_path}",
        )
    try:
        sig_hex = sig_path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise RouterIntegrityError(
            "signature_missing",
            f"router.yaml.sig unreadable at {sig_path}: {exc}",
        ) from exc
    if not sig_hex:
        raise RouterIntegrityError(
            "signature_missing",
            f"router.yaml.sig is empty at {sig_path}",
        )
    if len(sig_hex) != 128 or not all(
        c in "0123456789abcdefABCDEF" for c in sig_hex
    ):
        raise RouterIntegrityError(
            "signature_mismatch",
            f"router.yaml.sig is not a 128-char hex HMAC (len={len(sig_hex)})",
        )

    # Step 6 — load HMAC key from keystore. KeyStore.retrieve is sealed and
    # returns SecretBytes; we zero it via the context manager on exit.
    try:
        key_secret: SecretBytes = keystore.retrieve(ROUTER_HMAC_KEY_ID)
    except Exception as exc:
        raise RouterIntegrityError(
            "keystore_key_missing",
            f"keystore.retrieve({ROUTER_HMAC_KEY_ID!r}) failed: {exc}",
        ) from exc

    # Step 7 — compute expected HMAC over (router_yaml_sha || commit_sha).
    with key_secret as ks:
        key_bytes = bytes(ks.view())
        message = (router_yaml_sha + commit_sha).encode("ascii")
        expected_sig = hmac_sha3_512(key_bytes, message)

    # Step 8 — constant-time compare.
    if not constant_time_equal(
        expected_sig.hex().encode("ascii"), sig_hex.lower().encode("ascii")
    ):
        raise RouterHMACMismatch(
            "signature_mismatch",
            "router.yaml HMAC does not match router.yaml.sig",
        )

    # Step 9 — persist the manifest.
    manifest = RouterManifest(
        router_yaml_sha=router_yaml_sha,
        commit_sha=commit_sha,
        signed_by_key_id=ROUTER_HMAC_KEY_ID,
        signature_hex=sig_hex.lower(),
        verified_at=_iso_utc_now(),
    )
    _persist_manifest(repo_root, manifest, session_id=session_id)
    return manifest


def _persist_manifest(
    repo_root: Path, manifest: RouterManifest, *, session_id: str | None
) -> None:
    out_dir = repo_root / "sovereignty" / "router"
    out_dir.mkdir(parents=True, exist_ok=True)
    name = f"manifest.{session_id}.json" if session_id else "manifest.latest.json"
    out_path = out_dir / name
    body = {
        "router_yaml_sha": manifest.router_yaml_sha,
        "commit_sha": manifest.commit_sha,
        "signed_by_key_id": manifest.signed_by_key_id,
        "signature_hex": manifest.signature_hex,
        "verified_at": manifest.verified_at,
    }
    data = (
        json.dumps(body, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
        + "\n"
    )
    tmp = out_path.with_suffix(out_path.suffix + f".tmp.{os.getpid()}")
    tmp.write_text(data, encoding="utf-8")
    os.replace(str(tmp), str(out_path))
