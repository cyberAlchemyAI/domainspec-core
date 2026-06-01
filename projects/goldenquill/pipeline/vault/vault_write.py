"""Single-entry ``vault_write`` dispatcher. [§3.5, §4.10, §4.10.4, §4.10.6]

Three commit modes share one envelope:

* ``overwrite`` — last-writer-wins atomic replace (tmp → fsync → rename).
* ``write-if-absent`` — kernel-atomic exclusive create; EEXIST raises
  :class:`VaultWriteExists`.
* ``append-cas`` — compare-and-swap append; callers must present the
  SHA-3-512 of the current file bytes, or the empty-hash for absent files.

All three run inside a single ``fcntl.LOCK_EX`` on the org's
``.write.lock``. All three use Section 1's atomic-flush pattern
(tmp-in-same-dir → fsync → rename → parent-dir-fsync).

Cedar integration: an optional ``cedar_decide`` callback runs BEFORE the lock
is acquired. When provided, a denied decision raises
:class:`CedarSection4WritePathDenied` without touching the filesystem. The
real Cedar wiring lands in Round S (fd_broker); this module simply honours
the hook so the interface is stable.

Belt-and-suspenders §4.10.4 + §4.10.6 gates (v7.1, Batch 3 remediation):
After Cedar returns ``permit`` (or when no cedar_decide is supplied —
treated as Cedar-absent permit at v0.1), the dispatcher:

1. §4.10.4 step 4.5 — type-validates ``intent`` / ``path`` / ``write_mode``
   via :func:`isinstance` checks; failure raises
   :class:`CedarSection4WritePathDenied` with ``type_error=<T>`` carried on
   the exception (does NOT propagate ``TypeError`` — closes v6 Red Team
   CRIT-01 / CRIT-02 uncaught-TypeError path).
2. §4.10.4 step 5 — looks up ``intent`` in the hard-coded
   :data:`POST_GATE_ALLOWLIST`; unknown intent →
   ``reason=post_gate_unknown_intent``.
3. §4.10.4 step 6 — asserts ``str(path).startswith(expected_path_prefix)``;
   mismatch → ``reason=post_gate_path_mismatch``.
4. §4.10.4 step 7 — asserts ``write_mode`` is in the allowlist entry's
   ``permitted_modes``; mismatch → ``reason=post_gate_mode_mismatch``.
5. §4.10.6 kind-class hard-gate — reads ``kind_class`` from the allowlist
   entry and rejects the two crossed combinations:
   * ``kind_class == "COMPOUND"`` and ``txn_token is None`` →
     :class:`VaultCompoundProtocolViolation` with
     ``sub_reason="compound_intent_without_txn_token"``.
   * ``kind_class == "SIMPLE"`` and ``txn_token is not None`` →
     :class:`VaultCompoundProtocolViolation` with
     ``sub_reason="simple_intent_with_txn_token"``.
6. Only then proceeds to :func:`.write.lock` acquisition.

The v0.1 implementation is intentionally portable (Linux + macOS). It uses
``os.link`` + ``os.unlink`` as a portable shim for ``renameat2(RENAME_NOREPLACE)``
/ ``renamex_np(RENAME_EXCL)`` — on both supported kernels ``link`` is
kernel-atomic and returns EEXIST on collision. The renameat2 path is
reachable when available for a future pin.
"""

from __future__ import annotations

import errno
import fcntl
import hashlib
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Final, Optional

from pipeline.vault.error_codes import (
    CedarSection4WritePathDenied,
    VaultCASHeadMismatch,
    VaultCompoundProtocolViolation,
    VaultCrossOrgAccess,
    VaultWriteDenied,
    VaultWriteExists,
)

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_02_vault_topology.md": {
        "version": "v7.1",
        "hash_sha3_512_prefix16": "83a898275a4cf0a1",
        "sections_implemented": [
            "§3.5 vault_write single-entry dispatcher (overwrite / write-if-absent / append-cas)",
            "§4.10 atomic-flush commit primitive (tmp → fsync → rename → parent-dir-fsync)",
            "§4.10.4 post-gate path-allowlist belt-and-suspenders hook",
            "§4.10.6 dispatcher kind-class hard-gate + path-level lock scope (SIMPLE path)",
        ],
    },
    "section_02_v7_2_amendment.md": {
        "version": "v7.2-DRAFT",
        "sections_implemented": [
            "§2.13 POST_GATE_ALLOWLIST seven SIMPLE operational sub-kind rows",
        ],
    },
}

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

EMPTY_SHA3_512_HEX: str = hashlib.sha3_512(b"").hexdigest()

WRITE_MODES: frozenset[str] = frozenset({"overwrite", "write-if-absent", "append-cas"})

_HASH_CHUNK_BYTES = 64 * 1024


# ---------------------------------------------------------------------------
# §4.10.4 post-gate path-allowlist (v7.1, 7 entries: 5 SIMPLE + 2 COMPOUND)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class PostGateAllowlistEntry:
    """One row of the §4.10.4 v7.1 static post-gate allowlist.

    Two mutually-exclusive path-check shapes are supported:

    * ``vault_relative_prefix`` — SIMPLE rows and the COMPOUND
      ``index-amendment-audit-append`` row. The dispatcher strips the
      ``org_vault_root`` from the caller's absolute ``path`` and the remainder
      must :meth:`str.startswith` this prefix (always terminates in ``/``
      for directory-scoped rows; exact file name for the shared-ledger row).
    * ``repo_relative_regex_str`` — COMPOUND ``index-update`` row only.
      The dispatcher :func:`re.search` es the compiled regex against the
      absolute ``str(path)``; the positional ``v{N}.json`` placeholder is
      captured by ``\\d+`` in the regex.
    """

    vault_relative_prefix: Optional[str]
    repo_relative_regex_str: Optional[str]
    permitted_modes: frozenset[str]
    kind_class: str
    required_intents: Optional[tuple[str, ...]]


_KIND_CLASS_SIMPLE: Final[str] = "SIMPLE"
_KIND_CLASS_COMPOUND: Final[str] = "COMPOUND"

POST_GATE_ALLOWLIST: Final[dict[str, PostGateAllowlistEntry]] = {
    "claim-evidence-write": PostGateAllowlistEntry(
        vault_relative_prefix="claim_evidence/",
        repo_relative_regex_str=None,
        permitted_modes=frozenset({"write-if-absent"}),
        kind_class=_KIND_CLASS_SIMPLE,
        required_intents=None,
    ),
    "admin-risk-append": PostGateAllowlistEntry(
        vault_relative_prefix="admin_risk/",
        repo_relative_regex_str=None,
        permitted_modes=frozenset({"append-cas"}),
        kind_class=_KIND_CLASS_SIMPLE,
        required_intents=None,
    ),
    "conversation-log-append": PostGateAllowlistEntry(
        vault_relative_prefix="conversation_log/",
        repo_relative_regex_str=None,
        permitted_modes=frozenset({"overwrite", "append-cas"}),
        kind_class=_KIND_CLASS_SIMPLE,
        required_intents=None,
    ),
    "rails-report-write": PostGateAllowlistEntry(
        vault_relative_prefix="rails_reports/",
        repo_relative_regex_str=None,
        permitted_modes=frozenset({"overwrite"}),
        kind_class=_KIND_CLASS_SIMPLE,
        required_intents=None,
    ),
    "lessons-delta-append": PostGateAllowlistEntry(
        vault_relative_prefix="lessons_delta/",
        repo_relative_regex_str=None,
        permitted_modes=frozenset({"append-cas"}),
        kind_class=_KIND_CLASS_SIMPLE,
        required_intents=None,
    ),
    # §4.10.5 COMPOUND sub-kind registry — v0.1 has exactly one kind
    # (``index_amendment``) that requires both entries below.
    "index-update": PostGateAllowlistEntry(
        vault_relative_prefix=None,
        repo_relative_regex_str=(
            r"pipeline/blueprint/v0\.1/section_00_5_interface_index\.v\d+\.json$"
        ),
        permitted_modes=frozenset({"write-if-absent"}),
        kind_class=_KIND_CLASS_COMPOUND,
        required_intents=("index-update", "index-amendment-audit-append"),
    ),
    "index-amendment-audit-append": PostGateAllowlistEntry(
        # Shared ledger file under org vault; exact-path match.
        vault_relative_prefix="admin_risk/ledger.jsonl",
        repo_relative_regex_str=None,
        permitted_modes=frozenset({"append-cas"}),
        kind_class=_KIND_CLASS_COMPOUND,
        required_intents=("index-update", "index-amendment-audit-append"),
    ),
    # ----- v7.2 §2.13 (DRAFT) — operational-data SIMPLE sub-kinds -----
    # Each sub-kind owns its `operational/<sub_kind>/` subtree; modes are
    # uniformly `write-if-absent` so the audit trail is unforgeable per the
    # v7.2 amendment §1 rationale.
    "operational-metrics-write": PostGateAllowlistEntry(
        vault_relative_prefix="operational/metrics/",
        repo_relative_regex_str=None,
        permitted_modes=frozenset({"write-if-absent"}),
        kind_class=_KIND_CLASS_SIMPLE,
        required_intents=None,
    ),
    "operational-financials-write": PostGateAllowlistEntry(
        vault_relative_prefix="operational/financials/",
        repo_relative_regex_str=None,
        permitted_modes=frozenset({"write-if-absent"}),
        kind_class=_KIND_CLASS_SIMPLE,
        required_intents=None,
    ),
    "operational-photos-write": PostGateAllowlistEntry(
        vault_relative_prefix="operational/photos/",
        repo_relative_regex_str=None,
        permitted_modes=frozenset({"write-if-absent"}),
        kind_class=_KIND_CLASS_SIMPLE,
        required_intents=None,
    ),
    "operational-narrative-write": PostGateAllowlistEntry(
        vault_relative_prefix="operational/narratives/",
        repo_relative_regex_str=None,
        permitted_modes=frozenset({"write-if-absent"}),
        kind_class=_KIND_CLASS_SIMPLE,
        required_intents=None,
    ),
    "operational-timeline-write": PostGateAllowlistEntry(
        vault_relative_prefix="operational/timeline/",
        repo_relative_regex_str=None,
        permitted_modes=frozenset({"write-if-absent"}),
        kind_class=_KIND_CLASS_SIMPLE,
        required_intents=None,
    ),
    "operational-beneficiary-write": PostGateAllowlistEntry(
        vault_relative_prefix="operational/beneficiaries/",
        repo_relative_regex_str=None,
        permitted_modes=frozenset({"write-if-absent"}),
        kind_class=_KIND_CLASS_SIMPLE,
        required_intents=None,
    ),
    "operational-attachment-write": PostGateAllowlistEntry(
        vault_relative_prefix="operational/attachments/",
        repo_relative_regex_str=None,
        permitted_modes=frozenset({"write-if-absent"}),
        kind_class=_KIND_CLASS_SIMPLE,
        required_intents=None,
    ),
    # §17 WPFA cycle_receipt sub-kind — LOCKED 2026-05-11 row 205.
    "operational-cycle-receipt-write": PostGateAllowlistEntry(
        vault_relative_prefix="operational/cycle_receipts/",
        repo_relative_regex_str=None,
        permitted_modes=frozenset({"write-if-absent"}),
        kind_class=_KIND_CLASS_SIMPLE,
        required_intents=None,
    ),
}


def _path_matches_entry(
    path: Path, entry: PostGateAllowlistEntry, org_vault_root: Path
) -> bool:
    """Return True iff ``path`` matches ``entry``'s path-shape.

    Matches the blueprint §4.10.4 step 6 ``path.startswith(expected_prefix)``
    semantics while letting callers pass absolute :class:`pathlib.Path`
    objects whose vault root is a test-time ``tmp_path``.
    """
    p_str = str(path)
    if entry.vault_relative_prefix is not None:
        root_str = str(org_vault_root)
        needle = root_str.rstrip(os.sep) + os.sep
        if not p_str.startswith(needle):
            return False
        rel = p_str[len(needle):]
        return rel.startswith(entry.vault_relative_prefix)
    if entry.repo_relative_regex_str is not None:
        return re.search(entry.repo_relative_regex_str, p_str) is not None
    return False


# ---------------------------------------------------------------------------
# Return type
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class VaultWriteAck:
    """Return value from ``vault_write`` on success.

    Carries enough state for callers to reason about what committed without
    re-reading the file.
    """

    mode: str
    path: str
    committed: bool
    post_commit_hash: str
    pre_append_hash: Optional[str] = None
    existing_content_hash: Optional[str] = None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _hash_file_bytes(path: Path) -> str:
    if not path.exists():
        return EMPTY_SHA3_512_HEX
    h = hashlib.sha3_512()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(_HASH_CHUNK_BYTES)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def _atomic_flush(tmp: Path, final: Path) -> None:
    with open(tmp, "rb+") as fh:
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(str(tmp), str(final))
    parent_fd = os.open(str(final.parent), os.O_RDONLY)
    try:
        os.fsync(parent_fd)
    finally:
        os.close(parent_fd)


def _write_tmp(tmp: Path, payload: bytes) -> None:
    with open(tmp, "wb") as fh:
        fh.write(payload)
        fh.flush()
        os.fsync(fh.fileno())


def _within_org_root(path: Path, org_vault_root: Path) -> bool:
    try:
        path.resolve().relative_to(org_vault_root.resolve())
        return True
    except ValueError:
        return False


# ---------------------------------------------------------------------------
# §4.10.4 post-gate allowlist check + §4.10.6 kind-class hard-gate
# ---------------------------------------------------------------------------


def _post_gate_check(
    *,
    intent: object,
    path: object,
    slug: str,
    write_mode: object,
    txn_token: Optional[str],
    org_vault_root: Path,
) -> None:
    """Run §4.10.4 steps 4.5-7 and the §4.10.6 kind-class hard-gate.

    Raises :class:`CedarSection4WritePathDenied` on allowlist / prefix /
    mode / type-validation failure. Raises
    :class:`VaultCompoundProtocolViolation` on kind-class gate failure.

    Type-checked post-Cedar in addition to :func:`_validate_args` (which
    runs pre-Cedar). The belt-and-suspenders pattern closes the window
    where a refactor of ``_validate_args`` could unintentionally let a
    non-``str`` ``intent`` reach the allowlist lookup. Per blueprint
    §4.10.4 step 4.5 the type-error surface is a
    :class:`CedarSection4WritePathDenied` — not a :class:`TypeError` — so
    the caller's failure path is the rails-report path, not the generic
    broker handler.
    """
    # §4.10.4 step 4.5 — type-validation preamble (defence-in-depth).
    if not isinstance(intent, str):
        raise CedarSection4WritePathDenied(
            f"post-gate intent is not str (got {type(intent).__name__})",
            attempted_path=str(path) if isinstance(path, (str, Path)) else repr(path),
            attempted_intent=repr(intent),
            reason="post_gate_unknown_intent",
            type_error=type(intent).__name__,
        )
    if not isinstance(path, Path):
        raise CedarSection4WritePathDenied(
            f"post-gate path is not pathlib.Path (got {type(path).__name__})",
            attempted_path=repr(path),
            attempted_intent=intent,
            reason="post_gate_path_mismatch",
            type_error=type(path).__name__,
        )
    if not isinstance(write_mode, str):
        raise CedarSection4WritePathDenied(
            f"post-gate write_mode is not str (got {type(write_mode).__name__})",
            attempted_path=str(path),
            attempted_intent=intent,
            reason="post_gate_mode_mismatch",
            type_error=type(write_mode).__name__,
        )
    # §4.10.4 step 5 — intent-in-allowlist check (deny-by-default on unknown).
    entry = POST_GATE_ALLOWLIST.get(intent)
    if entry is None:
        raise CedarSection4WritePathDenied(
            f"post-gate denied: intent {intent!r} not in allowlist",
            attempted_path=str(path),
            attempted_intent=intent,
            reason="post_gate_unknown_intent",
        )
    # §4.10.4 step 6 — path-prefix check.
    if not _path_matches_entry(path, entry, org_vault_root):
        raise CedarSection4WritePathDenied(
            f"post-gate denied: path {path} does not match allowlist "
            f"entry for intent {intent!r}",
            attempted_path=str(path),
            attempted_intent=intent,
            reason="post_gate_path_mismatch",
        )
    # §4.10.4 step 7 — write_mode-in-permitted-modes check.
    if write_mode not in entry.permitted_modes:
        raise CedarSection4WritePathDenied(
            f"post-gate denied: write_mode {write_mode!r} not in "
            f"{sorted(entry.permitted_modes)} for intent {intent!r}",
            attempted_path=str(path),
            attempted_intent=intent,
            reason="post_gate_mode_mismatch",
        )
    # §4.10.6 kind-class hard-gate.
    if entry.kind_class == _KIND_CLASS_COMPOUND and txn_token is None:
        raise VaultCompoundProtocolViolation(
            f"§4.10.6 gate: COMPOUND intent {intent!r} requires txn_token",
            sub_reason="compound_intent_without_txn_token",
        )
    if entry.kind_class == _KIND_CLASS_SIMPLE and txn_token is not None:
        raise VaultCompoundProtocolViolation(
            f"§4.10.6 gate: SIMPLE intent {intent!r} rejects txn_token",
            sub_reason="simple_intent_with_txn_token",
        )


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------


def vault_write(
    path: Path,
    bytes_: bytes,
    intent: str,
    session_id: str,
    slug: str,
    *,
    org_vault_root: Path,
    write_lock_path: Path,
    write_mode: str = "overwrite",
    expected_current_file_hash: Optional[str] = None,
    txn_token: Optional[str] = None,
    cedar_decide: Optional[Callable[[str, Path, str], bool]] = None,
) -> VaultWriteAck:
    """Single-entry vault-write dispatcher.

    :param path: final target path (absolute). Must resolve under
        ``org_vault_root``.
    :param bytes_: payload to write (``overwrite`` / ``write-if-absent``) or
        append (``append-cas``).
    :param intent: stable intent string (e.g. ``"claim-evidence-write"``).
    :param session_id: caller session id (propagated to Cedar).
    :param slug: org slug (propagated to Cedar + used for the lock file).
    :param org_vault_root: absolute path to ``orgs/{slug}/vault/``.
    :param write_lock_path: path to the org's ``.write.lock`` file.
    :param write_mode: one of :data:`WRITE_MODES`.
    :param expected_current_file_hash: required for ``append-cas``; forbidden
        otherwise.
    :param txn_token: bearer token from :mod:`pipeline.vault.compound_txn`.
        MUST be ``None`` for SIMPLE-class intents; MUST be supplied for
        COMPOUND-class intents (§4.10.6 hard-gate).
    :param cedar_decide: optional callback ``(intent, path, slug) -> allowed``.
    :raises VaultWriteDenied: Cedar veto.
    :raises CedarSection4WritePathDenied: §4.10.4 post-gate allowlist /
        path-prefix / write-mode / type-validation mismatch.
    :raises VaultCompoundProtocolViolation: §4.10.6 kind-class hard-gate
        mismatch (SIMPLE+txn_token or COMPOUND-without-txn_token).
    :raises VaultCrossOrgAccess: path resolved outside the org vault root.
    :raises VaultWriteExists: ``write-if-absent`` and the target exists.
    :raises VaultCASHeadMismatch: ``append-cas`` and the head hash differs.
    """
    _validate_args(
        path=path,
        bytes_=bytes_,
        intent=intent,
        session_id=session_id,
        slug=slug,
        org_vault_root=org_vault_root,
        write_lock_path=write_lock_path,
        write_mode=write_mode,
        expected_current_file_hash=expected_current_file_hash,
    )

    if cedar_decide is not None and not cedar_decide(intent, path, slug):
        raise VaultWriteDenied(
            f"Cedar denied write of intent={intent!r} to {path}"
        )

    # Cross-org check precedes the post-gate so a path outside the org
    # vault root always surfaces as ``F-VAULT-04`` (and never as
    # ``F-CEDAR-SECTION4-WRITE-PATH-DENIED.post_gate_path_mismatch``). The
    # two codes index distinct alert classes on the rails report; collapsing
    # them would hide operational signal.
    if not _within_org_root(path, org_vault_root):
        raise VaultCrossOrgAccess(
            f"path {path} is outside org vault root {org_vault_root}"
        )

    # §4.10.4 + §4.10.6 belt-and-suspenders post-gate (runs whether Cedar
    # explicitly permitted OR was absent at v0.1 — absence is treated as
    # permit, matching the pre-v7.1 behaviour of this module).
    _post_gate_check(
        intent=intent,
        path=path,
        slug=slug,
        write_mode=write_mode,
        txn_token=txn_token,
        org_vault_root=org_vault_root,
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_dir = org_vault_root / ".tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    tmp_path = tmp_dir / f"{intent}.{os.getpid()}.{session_id}.part"

    write_lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_fd = os.open(
        str(write_lock_path),
        os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW,
        0o600,
    )
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        if write_mode == "overwrite":
            return _commit_overwrite(path, bytes_, tmp_path)
        if write_mode == "write-if-absent":
            return _commit_write_if_absent(path, bytes_, tmp_path)
        if write_mode == "append-cas":
            assert expected_current_file_hash is not None  # validated above
            return _commit_append_cas(
                path, bytes_, tmp_path, expected_current_file_hash
            )
        raise AssertionError(f"unhandled write_mode {write_mode!r}")
    finally:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
        finally:
            os.close(lock_fd)
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass


# ---------------------------------------------------------------------------
# Arg-type validation (E-001)
# ---------------------------------------------------------------------------


def _validate_args(
    *,
    path: Path,
    bytes_: bytes,
    intent: str,
    session_id: str,
    slug: str,
    org_vault_root: Path,
    write_lock_path: Path,
    write_mode: str,
    expected_current_file_hash: Optional[str],
) -> None:
    if not isinstance(path, Path):
        raise TypeError(f"path must be pathlib.Path, got {type(path).__name__}")
    if not isinstance(bytes_, (bytes, bytearray)):
        raise TypeError(
            f"bytes_ must be bytes|bytearray, got {type(bytes_).__name__}"
        )
    if not isinstance(intent, str):
        raise TypeError(f"intent must be str, got {type(intent).__name__}")
    if not isinstance(session_id, str):
        raise TypeError(f"session_id must be str")
    if not isinstance(slug, str):
        raise TypeError("slug must be str")
    if not isinstance(org_vault_root, Path):
        raise TypeError("org_vault_root must be pathlib.Path")
    if not isinstance(write_lock_path, Path):
        raise TypeError("write_lock_path must be pathlib.Path")
    if write_mode not in WRITE_MODES:
        raise ValueError(
            f"write_mode must be in {sorted(WRITE_MODES)}, got {write_mode!r}"
        )
    if write_mode == "append-cas":
        if expected_current_file_hash is None:
            raise ValueError(
                "append-cas requires expected_current_file_hash"
            )
        if not isinstance(expected_current_file_hash, str):
            raise TypeError("expected_current_file_hash must be str")
    else:
        if expected_current_file_hash is not None:
            raise ValueError(
                f"expected_current_file_hash forbidden for "
                f"write_mode={write_mode!r}"
            )


# ---------------------------------------------------------------------------
# Commit routines
# ---------------------------------------------------------------------------


def _commit_overwrite(final: Path, payload: bytes, tmp: Path) -> VaultWriteAck:
    _write_tmp(tmp, payload)
    _atomic_flush(tmp, final)
    return VaultWriteAck(
        mode="overwrite",
        path=str(final),
        committed=True,
        post_commit_hash=hashlib.sha3_512(payload).hexdigest(),
    )


def _commit_write_if_absent(
    final: Path, payload: bytes, tmp: Path
) -> VaultWriteAck:
    _write_tmp(tmp, payload)
    try:
        os.link(str(tmp), str(final))
    except FileExistsError:
        existing_hash = _hash_file_bytes(final)
        raise VaultWriteExists(
            f"write-if-absent collision at {final}"
        ) from None
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            raise VaultWriteExists(
                f"write-if-absent collision at {final}"
            ) from exc
        raise
    # Parent-dir fsync for durability.
    parent_fd = os.open(str(final.parent), os.O_RDONLY)
    try:
        os.fsync(parent_fd)
    finally:
        os.close(parent_fd)
    return VaultWriteAck(
        mode="write-if-absent",
        path=str(final),
        committed=True,
        post_commit_hash=hashlib.sha3_512(payload).hexdigest(),
    )


def _commit_append_cas(
    final: Path,
    payload: bytes,
    tmp: Path,
    expected_hash: str,
) -> VaultWriteAck:
    expected_norm = expected_hash.lower() if expected_hash else EMPTY_SHA3_512_HEX
    if expected_norm == "":
        expected_norm = EMPTY_SHA3_512_HEX
    current_hash = _hash_file_bytes(final)
    if current_hash.lower() != expected_norm:
        raise VaultCASHeadMismatch(
            f"append-cas head mismatch at {final}",
            expected_current_file_hash=expected_norm,
            actual_current_file_hash=current_hash,
        )
    # Build combined payload: old bytes + new bytes.
    if final.exists():
        old = final.read_bytes()
    else:
        old = b""
    combined = old + payload
    _write_tmp(tmp, combined)
    _atomic_flush(tmp, final)
    return VaultWriteAck(
        mode="append-cas",
        path=str(final),
        committed=True,
        post_commit_hash=hashlib.sha3_512(combined).hexdigest(),
        pre_append_hash=current_hash,
    )


__all__ = [
    "EMPTY_SHA3_512_HEX",
    "POST_GATE_ALLOWLIST",
    "PostGateAllowlistEntry",
    "WRITE_MODES",
    "VaultWriteAck",
    "vault_write",
]
