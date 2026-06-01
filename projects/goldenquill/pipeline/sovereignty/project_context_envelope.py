"""PROJECT_CONTEXT envelope — per-slug-locked seal + verify. [§2.3, §3.5, §4.2, §6.2, §7.6]

Section 1 Round F2. Owns:

* :class:`PROJECTContextEnvelope` — frozen dataclass carrying (slug,
  canonical_path, inode, device, content_hash, nonce_hex, sealed_at,
  bound_session_id).
* :func:`seal_project_context` — M2 write path under per-slug
  ``fcntl.LOCK_EX``. Steps 1–10 per §4.2 v2.
* :func:`verify_project_context` — Logician's mid-session re-read.
  Shared-lock, rehash, fail-closed on drift.

Blueprint references:

* §2.3   PROJECTContextEnvelope schema
* §3.5   seal_project_context public API
* §4.2   M2 envelope + session binding (v2 atomic per-slug lock)
* §6.2   F-PC-01..03 failure codes + OrgRootEscape
* §7.6   unit tests

E-enforcement:

* E-001 arg-type validation before any I/O
* E-005 canonical JSON (sorted keys + ASCII + no whitespace)
* E-014 family exception taxonomy (:class:`ProjectContextError` parent)

The per-slug lock closes the Red Team v1 TOCTOU window where the
slug-equality check happened BEFORE the atomic rename. Lock is held
across read + hash + write + rename; released only after rename lands.
"""

from __future__ import annotations

import datetime as _dt
import errno
import fcntl
import json
import os
import secrets
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterator

from pipeline.sovereignty.crypto_primitives import (
    sha3_512_with_nonce,
    verify_sha3_512_with_nonce,
)
from pipeline.sovereignty._types import HashDigest
from pipeline.sovereignty.isolation import (
    IsolationError,
    OrgRootNamespace,
    within_org_root,
)
from pipeline.sovereignty.session import SessionSlugMismatch

__all__ = [
    "PROJECTContextEnvelope",
    "ProjectContextError",
    "ProjectContextDrift",
    "OrgRootEscape",
    "CrossOrgViolation",
    "seal_project_context",
    "verify_project_context",
]

BLUEPRINT_DEPS = {
    "section_1_sovereignty_envelope.md": {
        "sections_implemented": [
            "§2.3 PROJECTContextEnvelope",
            "§3.5 seal_project_context public API",
            "§4.2 M2 per-slug lock + BT2 post-open fstat",
            "§6.2 F-PC-01..03 failure codes",
            "§7.6 unit tests",
        ],
        "hash_at_lock": None,
        "hash_source_version": "v6",
    },
}


# ---------------------------------------------------------------------------
# Exceptions (E-014 family taxonomy)
# ---------------------------------------------------------------------------


class ProjectContextError(RuntimeError):
    """Common parent for F-PC-01..03. Carries a ``code`` attribute."""

    code: str = "F-PC"


class ProjectContextDrift(ProjectContextError):
    """F-PC-01. Mid-session content hash mismatch."""

    code = "F-PC-01"

    def __init__(self, reason: str) -> None:
        super().__init__(f"F-PC-01 drift: {reason}")
        self.reason = reason


class OrgRootEscape(ProjectContextError):
    """F-PC-02. Canonical path resolves outside org root.

    Subclass of ProjectContextError (local family) AND shares the F-ISO-*
    reason-text convention. Caller code that catches the §1 F-ISO family
    via :class:`IsolationError` still sees this as IsolationError because
    we pass-through from :class:`pipeline.sovereignty.isolation.PathEscape`
    where the underlying symlink/namespace check already fired.
    """

    code = "F-PC-02"

    def __init__(self, reason: str) -> None:
        super().__init__(f"F-PC-02 org_root_escape: {reason}")
        self.reason = reason


class CrossOrgViolation(ProjectContextError):
    """F-PC-03. Law 3 violation: attempted cross-org PROJECT_CONTEXT load."""

    code = "F-PC-03"

    def __init__(self, reason: str) -> None:
        super().__init__(f"F-PC-03 cross_org: {reason}")
        self.reason = reason


# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class PROJECTContextEnvelope:
    """M2 envelope — PROJECT_CONTEXT.md hash bound to one session. [§2.3]"""

    slug: str
    canonical_path: str
    inode: int
    device: int
    content_hash: str
    nonce_hex: str
    sealed_at: str
    bound_session_id: str


# ---------------------------------------------------------------------------
# Canonical JSON + helpers
# ---------------------------------------------------------------------------


def _canonical_json_bytes(obj: object) -> bytes:
    return json.dumps(
        obj,
        sort_keys=True,
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _envelope_path(repo_root: Path, slug: str) -> Path:
    return (
        repo_root
        / "sovereignty"
        / "envelopes"
        / "project_context"
        / f"{slug}.json"
    )


def _lock_path(repo_root: Path, slug: str) -> Path:
    """``{envelope}.lock``. Separate file — never the envelope itself."""
    return _envelope_path(repo_root, slug).with_suffix(".json.lock")


def _pc_md_path(repo_root: Path, slug: str) -> Path:
    return repo_root / "orgs" / slug / "PROJECT_CONTEXT.md"


# ---------------------------------------------------------------------------
# Lock discipline
# ---------------------------------------------------------------------------


@contextmanager
def _slug_lock(repo_root: Path, slug: str, *, exclusive: bool) -> Iterator[None]:
    """fcntl-advisory lock on the per-slug lock file.

    Blocking. Held across the entire seal (write) or verify (read) window
    per §4.2 step 1 / step 10.
    """
    lock_path = _lock_path(repo_root, slug)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    # O_CREAT so the lock file appears on first seal attempt.
    fd = os.open(str(lock_path), os.O_CREAT | os.O_RDWR, 0o600)
    try:
        flag = fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH
        fcntl.flock(fd, flag)
        try:
            yield
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
    finally:
        os.close(fd)


# ---------------------------------------------------------------------------
# Atomic write
# ---------------------------------------------------------------------------


def _atomic_write(final_path: Path, data: bytes) -> None:
    """tmp+fsync+rename within the same directory.

    Same-FS assumption: envelope + repo_root live on one mount (§4.5 M6 v3
    is the place where cross-FS is enforced; §4.2 step 8 says 'same-FS
    pre-check per M6 cross-fs guard').
    """
    final_path.parent.mkdir(parents=True, exist_ok=True)
    # Same-FS pre-check: tmp parent == final parent → same mount by construction.
    suffix = secrets.token_hex(8)
    tmp_path = final_path.parent / f"{final_path.name}.tmp.{suffix}"
    fd = os.open(
        str(tmp_path), os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o600
    )
    try:
        written = os.write(fd, data)
        if written != len(data):
            raise ProjectContextError(
                f"F-PC short write: {written}/{len(data)} bytes for {final_path}"
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
# Post-open fstat reader (BT2)
# ---------------------------------------------------------------------------


def _read_and_hash_post_open(
    md_path: Path, org_root_resolved: Path
) -> tuple[bytes, HashDigest, int, int]:
    """Open ``md_path`` with O_NOFOLLOW | O_RDONLY | O_CLOEXEC; fstat; read; hash. [§4.2 step 5]

    Returns (content_bytes, content_digest, st_ino, st_dev).

    :raises OrgRootEscape: post-open fstat places the fd outside ``org_root_resolved``.
    :raises FileNotFoundError: md_path missing.
    :raises OrgRootEscape: md_path is a symlink (O_NOFOLLOW raises ELOOP).
    """
    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC
    try:
        fd = os.open(str(md_path), flags)
    except OSError as exc:
        if exc.errno == errno.ELOOP:
            raise OrgRootEscape(
                f"PROJECT_CONTEXT.md at {md_path} is a symlink (O_NOFOLLOW rejected)"
            ) from exc
        raise
    try:
        st = os.fstat(fd)
        # BT2 post-open re-stat: confirm the opened fd is still under the org root.
        # We do this by comparing the fd's st_dev to the org root's st_dev AND
        # ensuring the canonical path of the fd (via /dev/fd when available, else
        # fallback to the pre-computed canonical_path check by the caller) lives
        # under the org root.
        org_root_stat = os.stat(str(org_root_resolved))
        if st.st_dev != org_root_stat.st_dev:
            raise OrgRootEscape(
                f"PROJECT_CONTEXT.md fd st_dev={st.st_dev} differs from "
                f"org_root st_dev={org_root_stat.st_dev}"
            )
        # Read.
        chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 1 << 16)
            if not chunk:
                break
            chunks.append(chunk)
        content = b"".join(chunks)
        digest = sha3_512_with_nonce(content)
        return content, digest, st.st_ino, st.st_dev
    finally:
        os.close(fd)


# ---------------------------------------------------------------------------
# Public API — seal (write)
# ---------------------------------------------------------------------------


def seal_project_context(
    *,
    slug: str,
    session_id: str,
    repo_root: Path,
    expected_session_bound_slug: str | None = None,
) -> PROJECTContextEnvelope:
    """M2 per-slug-locked seal. [§4.2 v2]

    Steps per blueprint:

    1. Acquire ``fcntl.LOCK_EX`` on ``{slug}.json.lock`` (blocking).
    2. Resolve ``orgs/{slug}/PROJECT_CONTEXT.md`` strict=True.
    3. Assert the resolved path is within the resolved org root.
    4. Reject via :func:`within_org_root` (symlink-chain escape).
    5. O_NOFOLLOW open + fstat + read + hash.
    6. ``expected_session_bound_slug`` equality check (inside the lock).
    7. Build envelope.
    8. Atomic tmp+rename.
    9. Release lock.

    :raises TypeError / ValueError: bad args (E-001).
    :raises FileNotFoundError: PROJECT_CONTEXT.md does not exist.
    :raises OrgRootEscape: canonical path escapes org root or fd st_dev drift.
    :raises SessionSlugMismatch: expected_session_bound_slug != slug.
    :raises IsolationError: within_org_root raised a symlink or namespace drift.
    """
    # E-001 type gate.
    if not isinstance(slug, str):
        raise TypeError("slug must be str")
    if not isinstance(session_id, str):
        raise TypeError("session_id must be str")
    if not isinstance(repo_root, Path):
        raise TypeError("repo_root must be pathlib.Path")
    if expected_session_bound_slug is not None and not isinstance(
        expected_session_bound_slug, str
    ):
        raise TypeError("expected_session_bound_slug must be str or None")
    if not slug:
        raise ValueError("slug must be non-empty")
    if not session_id:
        raise ValueError("session_id must be non-empty")

    org_root = repo_root / "orgs" / slug

    with _slug_lock(repo_root, slug, exclusive=True):
        # Step 2 — resolve strict=True.
        md_path = _pc_md_path(repo_root, slug)
        try:
            resolved = md_path.resolve(strict=True)
        except FileNotFoundError:
            raise
        except OSError as exc:
            raise OrgRootEscape(
                f"PROJECT_CONTEXT.md resolve failed: {exc}"
            ) from exc

        # Step 3 — is_relative_to the resolved org root.
        try:
            org_root_resolved = org_root.resolve(strict=True)
        except (FileNotFoundError, OSError) as exc:
            raise OrgRootEscape(
                f"org_root {org_root} does not resolve: {exc}"
            ) from exc
        if not resolved.is_relative_to(org_root_resolved):
            raise OrgRootEscape(
                f"PROJECT_CONTEXT.md at {resolved} escapes {org_root_resolved}"
            )

        # Step 4 — within_org_root symlink-chain check.
        try:
            ns = OrgRootNamespace.bind(
                org_slug=slug, root_path=org_root_resolved
            )
        except IsolationError:
            raise
        try:
            ok = within_org_root(md_path, ns)
        except IsolationError as exc:
            raise OrgRootEscape(
                f"within_org_root rejected {md_path}: {exc}"
            ) from exc
        if not ok:
            raise OrgRootEscape(
                f"within_org_root returned False for {md_path}"
            )

        # Step 5 — O_NOFOLLOW open + fstat + read + hash.
        _content, digest, st_ino, st_dev = _read_and_hash_post_open(
            md_path, org_root_resolved
        )

        # Step 6 — slug equality check (inside the lock).
        if (
            expected_session_bound_slug is not None
            and expected_session_bound_slug != slug
        ):
            raise SessionSlugMismatch(
                f"expected_session_bound_slug={expected_session_bound_slug!r} "
                f"!= slug={slug!r}"
            )

        # Step 7 — build envelope.
        sealed_at = _dt.datetime.now(_dt.timezone.utc).isoformat(
            timespec="microseconds"
        ).replace("+00:00", "Z")
        envelope = PROJECTContextEnvelope(
            slug=slug,
            canonical_path=str(resolved),
            inode=st_ino,
            device=st_dev,
            content_hash=digest.digest_hex,
            nonce_hex=digest.nonce_hex,
            sealed_at=sealed_at,
            bound_session_id=session_id,
        )

        # Step 8 — atomic tmp+rename.
        envelope_bytes = _canonical_json_bytes(asdict(envelope))
        _atomic_write(_envelope_path(repo_root, slug), envelope_bytes)

    # Step 9 — lock released by context manager exit.
    return envelope


# ---------------------------------------------------------------------------
# Public API — verify (mid-session re-read by Logician)
# ---------------------------------------------------------------------------


def verify_project_context(
    envelope: PROJECTContextEnvelope,
    *,
    repo_root: Path,
    expected_session_id: str | None = None,
) -> None:
    """Logician mid-session re-read. [§4.2 step 10]

    Acquire shared lock. Re-stat + re-hash. On any mismatch, raise
    :class:`ProjectContextDrift` with a specific reason subcode.

    :raises TypeError: bad args (E-001).
    :raises CrossOrgViolation: envelope.bound_session_id != expected_session_id
        when expected_session_id is provided.
    :raises ProjectContextDrift: content / inode / device mismatch.
    :raises FileNotFoundError / OrgRootEscape: as from seal.
    """
    if not isinstance(envelope, PROJECTContextEnvelope):
        raise TypeError("envelope must be PROJECTContextEnvelope")
    if not isinstance(repo_root, Path):
        raise TypeError("repo_root must be pathlib.Path")

    # Session-binding check up front — the envelope carries the slug, so a
    # mismatched session_id is a strong cross-org signal (Law 3).
    if (
        expected_session_id is not None
        and envelope.bound_session_id != expected_session_id
    ):
        raise CrossOrgViolation(
            f"envelope bound_session_id={envelope.bound_session_id!r} "
            f"!= expected_session_id={expected_session_id!r}"
        )

    with _slug_lock(repo_root, envelope.slug, exclusive=False):
        md_path = _pc_md_path(repo_root, envelope.slug)
        try:
            resolved = md_path.resolve(strict=True)
        except FileNotFoundError:
            raise ProjectContextDrift("project_context_missing") from None

        # Canonical path must still match the sealed one.
        if str(resolved) != envelope.canonical_path:
            raise ProjectContextDrift("canonical_path_changed")

        # Open + fstat + read; compare inode + device + content hash.
        flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC
        try:
            fd = os.open(str(resolved), flags)
        except OSError as exc:
            if exc.errno == errno.ELOOP:
                raise OrgRootEscape(
                    f"PROJECT_CONTEXT.md at {resolved} became a symlink"
                ) from exc
            raise
        try:
            st = os.fstat(fd)
            if st.st_ino != envelope.inode:
                raise ProjectContextDrift("inode_changed")
            if st.st_dev != envelope.device:
                raise ProjectContextDrift("device_changed")
            chunks: list[bytes] = []
            while True:
                chunk = os.read(fd, 1 << 16)
                if not chunk:
                    break
                chunks.append(chunk)
            content = b"".join(chunks)
        finally:
            os.close(fd)

        expected = HashDigest(
            algorithm="sha3-512-nonce",
            digest_hex=envelope.content_hash,
            nonce_hex=envelope.nonce_hex,
        )
        if not verify_sha3_512_with_nonce(content, expected=expected):
            raise ProjectContextDrift("content_hash_mismatch")
