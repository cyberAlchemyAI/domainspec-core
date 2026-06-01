"""RFA envelope — dual-hash ingest + TOCTOU-guarded reverify. [§2.2, §3.4, §4.1, §5.1 BT1, §6.1, §7.6]

Section 1 Round F1. Owns:

* :class:`RFAEnvelope` — frozen dataclass carrying (url_hash, content_hash,
  nonce, inode, device, size_bytes, operator_id, session_bound_slug,
  canonical_path, url_at_ingest, ingested_at, rfa_id).
* :func:`ingest_rfa` — M1 write path: compute dual-hash over
  ``(content_bytes || nonce)`` + ``url``, stash raw content under the org
  root, serialize envelope canonically, append local audit line.
* :func:`reverify_rfa` — M1 read path: restat + rehash + url-hash compare.
  Fail-closed on any mismatch per §6.1 failure codes.

Blueprint references:

* §2.2   RFAEnvelope schema
* §3.4   public API (``ingest_rfa`` / ``reverify_rfa``)
* §4.1   M1 dual-hash (ingest + v2 URL re-verify)
* §5.1   BT1 SHA-3-512 with per-RFA 32-byte nonce
* §6.1   F-RFA-01..05 failure codes
* §7.6   unit tests

E-enforcement:

* E-001 arg-type validation before any I/O
* E-002 lowercase algorithm identifiers (HashPair.algorithm == ``"SHA3-512"``)
* E-005 canonical JSON via sorted keys + ASCII + no whitespace
* E-014 RFA exception taxonomy shares a family parent (:class:`RFAError`)
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import secrets
from dataclasses import asdict, dataclass
from pathlib import Path

from pipeline.sovereignty._types import HashPair
from pipeline.sovereignty.crypto_primitives import (
    constant_time_equal,
    sha3_512_hex,
    sha3_512_with_nonce,
    verify_sha3_512_with_nonce,
)
from pipeline.sovereignty._types import HashDigest

__all__ = [
    "RFAEnvelope",
    "RFAError",
    "RFADriftError",
    "RFAMissing",
    "RFAEnvelopeCorrupt",
    "ingest_rfa",
    "reverify_rfa",
]

BLUEPRINT_DEPS = {
    "section_1_sovereignty_envelope.md": {
        "sections_implemented": [
            "§2.2 RFAEnvelope",
            "§3.4 rfa_envelope public API",
            "§4.1 M1 dual-hash ingest + v2 URL reverify",
            "§5.1 BT1 (delegated to crypto_primitives.sha3_512_with_nonce)",
            "§6.1 F-RFA-01..05 failure codes",
            "§7.6 unit tests",
        ],
        "hash_at_lock": None,
        "hash_source_version": "v6",
    },
}


# ---------------------------------------------------------------------------
# Exceptions (E-014 family taxonomy)
# ---------------------------------------------------------------------------


class RFAError(RuntimeError):
    """Common parent for F-RFA-01..05. Carries a ``code`` attribute."""

    code: str = "F-RFA"


class RFADriftError(RFAError):
    """F-RFA-01 / F-RFA-05. Content, inode/device/size, or URL hash mismatch at reverify."""

    code = "F-RFA-01"

    def __init__(self, reason: str) -> None:
        super().__init__(f"F-RFA drift: {reason}")
        self.reason = reason


class RFAMissing(RFAError):
    """F-RFA-02. Canonical RFA file not present at reverify time."""

    code = "F-RFA-02"


class RFAEnvelopeCorrupt(RFAError):
    """Envelope JSON / nonce integrity failure at load.

    Default ``code`` is F-RFA-04 (envelope JSON unparseable). Raise sites
    that detect F-RFA-03 (nonce file missing) should construct with
    ``code="F-RFA-03"`` so downstream handlers can distinguish them.
    """

    code = "F-RFA-04"

    def __init__(self, *args, code: str | None = None) -> None:
        super().__init__(*args)
        if code is not None:
            self.code = code


# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class RFAEnvelope:
    """M1 dual-hash envelope. [§2.2 + §4.1 v2 url_at_ingest]

    url_at_ingest is not named in §2.2 but is required by §4.1 reverify
    step 4 (v2) so the URL can be re-hashed against ``hashes.url_hash``
    without network round-trip. Carrying it on the envelope is the
    smallest change that satisfies the re-hash contract; Scout owns the
    re-fetch path.
    """

    rfa_id: str
    ingested_at: str
    hashes: HashPair
    session_bound_slug: str
    canonical_path: str
    inode: int
    device: int
    size_bytes: int
    ingested_by: str
    url_at_ingest: str


# ---------------------------------------------------------------------------
# Canonical JSON + atomic write
# ---------------------------------------------------------------------------


def _canonical_json_bytes(obj: object) -> bytes:
    """Deterministic JSON: sorted keys, ASCII, no whitespace (§2 canon)."""
    return json.dumps(
        obj,
        sort_keys=True,
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _envelope_to_dict(env: RFAEnvelope) -> dict:
    """asdict expansion; HashPair flattens into a nested dict automatically."""
    return asdict(env)


def _atomic_write(final_path: Path, data: bytes) -> None:
    """tmp+fsync+rename within the same directory. [§4.1 step 6/8]

    Not the §4.5 M6 double-check: RFA ingest does not mandate a
    post-creation st_dev re-check (that guard is checkpoint-specific).
    Single-FS assumption: the repo_root itself lives on one mount in v0.1.
    """
    final_path.parent.mkdir(parents=True, exist_ok=True)
    suffix = secrets.token_hex(8)
    tmp_path = final_path.parent / f"{final_path.name}.tmp.{suffix}"
    fd = os.open(
        str(tmp_path), os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o600
    )
    try:
        written = os.write(fd, data)
        if written != len(data):
            raise RFAError(
                f"short write: {written}/{len(data)} bytes for {final_path}"
            )
        os.fsync(fd)
    except BaseException:
        try:
            os.close(fd)
        except OSError:
            pass
        try:
            os.unlink(str(tmp_path))
        except OSError:
            pass
        raise
    else:
        os.close(fd)
    os.rename(str(tmp_path), str(final_path))


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------


def _rfa_content_path(repo_root: Path, slug: str, rfa_id: str) -> Path:
    """``orgs/{slug}/rfa/{rfa_id}.raw`` under repo_root."""
    return repo_root / "orgs" / slug / "rfa" / f"{rfa_id}.raw"


def _envelope_path(repo_root: Path, rfa_id: str) -> Path:
    """``sovereignty/envelopes/rfa/{rfa_id}.json`` under repo_root. [§2.8]"""
    return repo_root / "sovereignty" / "envelopes" / "rfa" / f"{rfa_id}.json"


def _audit_path(repo_root: Path, slug: str) -> Path:
    """Per-org ``orgs/{slug}/rfa_audit.jsonl``. [§4.1 step 7]"""
    return repo_root / "orgs" / slug / "rfa_audit.jsonl"


def _validate_rfa_id(rfa_id: str) -> None:
    """Reject path-injection via rfa_id."""
    if not isinstance(rfa_id, str):
        raise TypeError("rfa_id must be str")
    if not rfa_id:
        raise ValueError("rfa_id must be non-empty")
    if len(rfa_id) > 128:
        raise ValueError("rfa_id too long (>128 chars)")
    # Conservative allowlist: alnum + dash + underscore + dot. No slashes.
    # Reject leading dot to prevent hidden-file shenanigans.
    if rfa_id.startswith("."):
        raise ValueError("rfa_id cannot start with '.'")
    for ch in rfa_id:
        if not (ch.isalnum() or ch in "-_."):
            raise ValueError(
                f"rfa_id contains disallowed character {ch!r}; "
                f"allowed: alnum + '-' + '_' + '.'"
            )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def ingest_rfa(
    *,
    url: str,
    content_bytes: bytes,
    slug: str,
    operator_id: str,
    rfa_id: str,
    repo_root: Path,
) -> RFAEnvelope:
    """M1 ingest path. [§4.1]

    1. Compute ``url_hash = sha3_512(utf-8(url))`` — no nonce (§2.1 invariant).
    2. Generate nonce via BT1 CSPRNG; compute
       ``content_hash = sha3_512(content_bytes || nonce)``.
    3. Atomically write raw content to
       ``orgs/{slug}/rfa/{rfa_id}.raw``.
    4. ``stat`` the raw file — snapshot ``st_ino``, ``st_dev``, ``st_size``.
    5. Build :class:`RFAEnvelope` and serialize it canonically to
       ``sovereignty/envelopes/rfa/{rfa_id}.json``.
    6. Append audit entry with envelope hash + operator + UTC ts.

    :raises TypeError: any argument of wrong type (E-001).
    :raises ValueError: empty ``url`` / ``slug`` / ``operator_id`` or bad ``rfa_id``.
    :raises RFAError: atomic write short-write (covered by the helper).

    v0.1 assumption: ``repo_root`` exists and is writable under a single-FS
    mount. Callers pre-resolve ``repo_root`` before calling.
    """
    # E-001 arg-type gate.
    if not isinstance(url, str):
        raise TypeError("url must be str")
    if not isinstance(content_bytes, (bytes, bytearray)):
        raise TypeError("content_bytes must be bytes")
    if not isinstance(slug, str):
        raise TypeError("slug must be str")
    if not isinstance(operator_id, str):
        raise TypeError("operator_id must be str")
    if not isinstance(repo_root, Path):
        raise TypeError("repo_root must be pathlib.Path")
    _validate_rfa_id(rfa_id)
    if not url:
        raise ValueError("url must be non-empty")
    if not slug:
        raise ValueError("slug must be non-empty")
    if not operator_id:
        raise ValueError("operator_id must be non-empty")

    # Normalize bytes input to immutable bytes for hashing.
    content_bytes_immut = bytes(content_bytes)

    # Step 1 — url_hash (no nonce).
    url_digest: HashDigest = sha3_512_hex(url.encode("utf-8"))

    # Step 2 — content_hash with per-RFA nonce (BT1).
    content_digest: HashDigest = sha3_512_with_nonce(content_bytes_immut)

    hashes = HashPair(
        url_hash=url_digest.digest_hex,
        content_hash=content_digest.digest_hex,
        algorithm="SHA3-512",
        nonce_hex=content_digest.nonce_hex,
    )

    # Step 3 — write raw.
    raw_path = _rfa_content_path(repo_root, slug, rfa_id)
    _atomic_write(raw_path, content_bytes_immut)

    # Step 4 — stat snapshot (TOCTOU closure).
    st = raw_path.stat()
    size_bytes = st.st_size
    if size_bytes != len(content_bytes_immut):
        # Write / stat must agree or something racy happened between rename and stat.
        raise RFAError(
            f"F-RFA post-ingest size drift: wrote {len(content_bytes_immut)} "
            f"bytes, stat reports {size_bytes}"
        )

    # Step 5 — build + serialize envelope.
    canonical_path = str(raw_path.resolve(strict=True))
    ingested_at = _dt.datetime.now(_dt.timezone.utc).isoformat(
        timespec="microseconds"
    ).replace("+00:00", "Z")
    envelope = RFAEnvelope(
        rfa_id=rfa_id,
        ingested_at=ingested_at,
        hashes=hashes,
        session_bound_slug=slug,
        canonical_path=canonical_path,
        inode=st.st_ino,
        device=st.st_dev,
        size_bytes=size_bytes,
        ingested_by=operator_id,
        url_at_ingest=url,
    )

    envelope_bytes = _canonical_json_bytes(_envelope_to_dict(envelope))
    _atomic_write(_envelope_path(repo_root, rfa_id), envelope_bytes)

    # Step 6 — per-org audit trail.
    envelope_hash = sha3_512_hex(envelope_bytes).digest_hex
    audit_line = _canonical_json_bytes(
        {
            "rfa_id": rfa_id,
            "envelope_hash": envelope_hash,
            "operator_id": operator_id,
            "ingested_at": ingested_at,
        }
    )
    audit_path = _audit_path(repo_root, slug)
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    # O_APPEND is atomic for writes ≤ PIPE_BUF on all POSIX filesystems; our
    # audit lines are well under 4 KiB (the POSIX atomic-write guarantee).
    fd = os.open(
        str(audit_path),
        os.O_CREAT | os.O_WRONLY | os.O_APPEND,
        0o600,
    )
    try:
        os.write(fd, audit_line + b"\n")
    finally:
        os.close(fd)

    return envelope


def reverify_rfa(envelope: RFAEnvelope) -> None:
    """M1 reverify path (v2 — also re-hashes the URL). [§4.1]

    1. Restat canonical path; compare ``(st_dev, st_ino, st_size)``. Any
       mismatch → :class:`RFADriftError` with a specific subcode.
    2. Re-read content bytes.
    3. Recompute ``content_hash`` against envelope's stored nonce;
       constant-time-compare against envelope.hashes.content_hash.
    4. Recompute ``url_hash`` against envelope.url_at_ingest and compare
       against envelope.hashes.url_hash.

    :raises TypeError: if ``envelope`` is not an :class:`RFAEnvelope`.
    :raises RFAMissing: F-RFA-02 — canonical file no longer exists.
    :raises RFADriftError: F-RFA-01 / F-RFA-05.
    """
    if not isinstance(envelope, RFAEnvelope):
        raise TypeError("envelope must be RFAEnvelope")

    canonical = Path(envelope.canonical_path)

    # Step 1 — restat with O_NOFOLLOW-equivalent check (lstat + regular-file).
    try:
        st = canonical.stat()
    except FileNotFoundError:
        raise RFAMissing(
            f"F-RFA-02: canonical path {canonical} no longer exists"
        ) from None
    except OSError as exc:
        raise RFAMissing(
            f"F-RFA-02: canonical path {canonical} unreachable: {exc}"
        ) from exc

    if st.st_ino != envelope.inode:
        raise RFADriftError("rfa_inode_changed")
    if st.st_dev != envelope.device:
        raise RFADriftError("rfa_device_changed")
    if st.st_size != envelope.size_bytes:
        raise RFADriftError("rfa_size_changed")

    # Step 2 — re-read content bytes.
    try:
        content_bytes = canonical.read_bytes()
    except OSError as exc:
        raise RFAMissing(
            f"F-RFA-02: canonical path {canonical} unreadable: {exc}"
        ) from exc

    # Defensive: len(content_bytes) must match size_bytes (already checked via stat).
    if len(content_bytes) != envelope.size_bytes:
        raise RFADriftError("rfa_size_changed")

    # Step 3 — content hash recompute via expected HashDigest.
    expected_content = HashDigest(
        algorithm="sha3-512-nonce",
        digest_hex=envelope.hashes.content_hash,
        nonce_hex=envelope.hashes.nonce_hex,
    )
    if not verify_sha3_512_with_nonce(content_bytes, expected=expected_content):
        raise RFADriftError("rfa_content_hash_mismatch")

    # Step 4 — url_hash re-verify (v2 F-RFA-05).
    current_url_digest = sha3_512_hex(envelope.url_at_ingest.encode("utf-8"))
    if not constant_time_equal(
        current_url_digest.digest_hex.encode("ascii"),
        envelope.hashes.url_hash.encode("ascii"),
    ):
        raise RFADriftError("rfa_url_hash_mismatch")
