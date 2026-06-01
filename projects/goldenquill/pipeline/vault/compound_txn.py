"""Option-B compound-transaction dispatcher. [§2.10 + §3.5 + §4.10.5-7]

v0.1 scope: offers ``begin`` / ``stage_write`` / ``commit`` / ``abort``
primitives for COMPOUND intents. Section 5 (Pipeline) is the only caller
surface in v0.1; Scout and Logician never touch these primitives directly.

Design invariants (Option-B LOCK 2026-04-19):

* ``StagedWrite`` and ``CompoundTxnState`` are frozen dataclasses; the
  in-memory tables live in the dispatcher's address space and are never
  serialized to disk.
* ``staged_writes`` is a :class:`tuple` — no ``.append`` surface; any
  addition returns a new ``CompoundTxnState`` with the extended tuple.
* Hash-at-stage-time: ``StagedWrite.data_sha3_512`` is pinned when the
  write is staged. The commit-side predicate reads the stored hash; no
  re-hash window exists.
* Runtime integrity check at commit entry: every staged record must be a
  :class:`StagedWrite` instance, or :class:`VaultCompoundIntegrityError`
  fires.
* Session cap: at most ``MAX_ACTIVE_COMPOUND_TXNS_PER_SESSION`` transactions
  may be open for a given session concurrently.
* Size cap: sum of ``data_len`` across staged writes + ``pre_commit_bytes``
  may not exceed ``MAX_COMPOUND_TXN_BYTES``.

The dispatcher takes the org's ``.compound.lock`` at ``commit`` time so
the persist hook's file writes serialize against all SIMPLE
``vault_write`` calls on the same org (both acquire the same
``fcntl.LOCK_EX``). ``begin``/``stage`` hold only in-memory records and
use the ``_session_counts`` table to enforce the per-session cap, so a
session may legitimately open up to
``MAX_ACTIVE_COMPOUND_TXNS_PER_SESSION`` concurrent compound txns before
any of them reaches commit.
"""

from __future__ import annotations

import fcntl
import hashlib
import os
import secrets
import time
from dataclasses import replace
from pathlib import Path
from typing import Final, Optional

from pipeline.vault.error_codes import (
    VaultCompoundCapExceeded,
    VaultCompoundIntegrityError,
    VaultCompoundOversize,
    VaultCompoundProtocolViolation,
)
from pipeline.vault.schemas import CompoundTxnState, StagedWrite

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_02_vault_topology.md": {
        "version": "v7.1",
        "hash_sha3_512_prefix16": "83a898275a4cf0a1",
        "sections_implemented": [
            "§2.10 StagedWrite + CompoundTxnState (Option-B compound-txn dispatcher)",
            "§3.5 compound-txn primitives (begin / stage_write / commit / abort)",
            "§4.10.5 COMPOUND sub-kind registry",
            "§4.10.6 dispatcher kind-class hard-gate (COMPOUND path)",
            "§4.10.7 compound-transaction life-cycle semantics (all-or-nothing)",
            "§8 compound-txn constants (session cap, stage caps, TTL, undo-snapshot cap)",
        ],
    },
}

# ---------------------------------------------------------------------------
# Constants (§8 pins, copied verbatim for v0.1)
# ---------------------------------------------------------------------------

TXN_TOKEN_ENTROPY_BYTES: int = 32
# §8: v7.1 corrected to 1 per LOCKED blueprint (was 8 in pre-remediation code).
MAX_ACTIVE_COMPOUND_TXNS_PER_SESSION: int = 1
# §8: 128 MiB stage-time cap on sum(len(sw.data) for sw in staged_writes).
# F-VAULT-24.compound_txn_cap_exceeded on overflow.
MAX_STAGED_BYTES_PER_TXN: int = 134_217_728  # 128 MiB
# §8: 8-write stage-time count cap. F-VAULT-24.compound_txn_cap_exceeded on overflow.
MAX_STAGED_WRITES_PER_TXN: int = 8
# §8: 64 MiB commit-time cap on sum(len(b) for _, b in pre_commit_bytes) — undo
# snapshot retained for §4.10.7.5. F-VAULT-COMPOUND-OVERSIZE on overflow. Half the
# stage cap by design (undo is backward-looking and historically smaller).
MAX_COMPOUND_TXN_BYTES: int = 67_108_864  # 64 MiB
# §8: 10-minute txn TTL (was 60s in pre-remediation code).
COMPOUND_TXN_TTL_SECONDS: int = 600

COMPOUND_TXN_KINDS: frozenset[str] = frozenset(
    {"index-update", "index-amendment-audit-append"}
)


# ---------------------------------------------------------------------------
# Dispatcher state (in-process)
# ---------------------------------------------------------------------------


class CompoundTxnDispatcher:
    """Per-process compound-transaction coordinator.

    Instantiated once per Vault boot. Holds the active-txn table and the
    per-txn lock-FDs. Thread-safe under GIL — all mutations are short and
    the broker wraps any long-running compound txn in a per-org
    ``.write.lock`` that serializes across threads anyway.
    """

    def __init__(self, *, compound_lock_path: Path) -> None:
        if not isinstance(compound_lock_path, Path):
            raise TypeError("compound_lock_path must be pathlib.Path")
        self._compound_lock_path: Path = compound_lock_path
        self._active: dict[str, CompoundTxnState] = {}
        self._session_counts: dict[str, int] = {}
        self._lock_fds: dict[str, int] = {}

    # ------------------------------------------------------------------
    # begin
    # ------------------------------------------------------------------

    def begin(
        self,
        *,
        txn_kind: str,
        session_id: str,
    ) -> str:
        if not isinstance(txn_kind, str):
            raise TypeError("txn_kind must be str")
        if not isinstance(session_id, str):
            raise TypeError("session_id must be str")
        if txn_kind not in COMPOUND_TXN_KINDS:
            raise VaultCompoundProtocolViolation(
                f"unknown txn_kind {txn_kind!r}; "
                f"expected one of {sorted(COMPOUND_TXN_KINDS)}"
            )
        if self._session_counts.get(session_id, 0) >= (
            MAX_ACTIVE_COMPOUND_TXNS_PER_SESSION
        ):
            raise VaultCompoundCapExceeded(
                f"session {session_id!r} already has "
                f"{MAX_ACTIVE_COMPOUND_TXNS_PER_SESSION} open compound txns"
            )
        token = secrets.token_urlsafe(TXN_TOKEN_ENTROPY_BYTES)
        self._active[token] = CompoundTxnState(
            txn_kind=txn_kind,
            txn_token=token,
            session_id=session_id,
            created_at_monotonic_ns=time.monotonic_ns(),
            staged_writes=(),
            pre_commit_bytes=(),
        )
        self._session_counts[session_id] = (
            self._session_counts.get(session_id, 0) + 1
        )
        return token

    # ------------------------------------------------------------------
    # stage
    # ------------------------------------------------------------------

    def stage_write(
        self,
        *,
        txn_token: str,
        session_id: str,
        intent: str,
        path: str,
        data: bytes,
        write_mode: str = "overwrite",
        expected_current_file_hash: Optional[str] = None,
    ) -> None:
        if not isinstance(txn_token, str):
            raise TypeError("txn_token must be str")
        state = self._require_active(txn_token, session_id)
        self._check_ttl(state)
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes|bytearray")
        staged = StagedWrite(
            intent=intent,
            path=path,
            data=bytes(data),
            data_sha3_512=hashlib.sha3_512(bytes(data)).hexdigest(),
            data_len=len(data),
            expected_current_file_hash=expected_current_file_hash,
            write_mode=write_mode,
            staged_at_monotonic_ns=time.monotonic_ns(),
        )
        new_state = replace(state, staged_writes=state.staged_writes + (staged,))
        self._check_stage_caps(new_state)
        self._active[txn_token] = new_state

    # ------------------------------------------------------------------
    # commit
    # ------------------------------------------------------------------

    def commit(
        self,
        *,
        txn_token: str,
        session_id: str,
        persist: "CommitPersistHook",
    ) -> tuple[StagedWrite, ...]:
        state = self._require_active(txn_token, session_id)
        self._check_ttl(state)
        self._runtime_integrity_check(state)
        # §4.10.7.3 step 2: undo-snapshot 64 MiB cap. Caller (Section 5 or
        # the persist hook) may have populated pre_commit_bytes via
        # ``dataclasses.replace`` before invoking commit; we re-validate
        # defensively here. F-VAULT-COMPOUND-OVERSIZE on overflow.
        self._check_pre_commit_bytes_cap(state)
        # Acquire the org-level .compound.lock only now — commit is the
        # serialization point against SIMPLE vault_write on the same org.
        self._compound_lock_path.parent.mkdir(parents=True, exist_ok=True)
        lock_fd = os.open(
            str(self._compound_lock_path),
            os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW,
            0o600,
        )
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        self._lock_fds[txn_token] = lock_fd
        try:
            persist(state)
        except Exception:
            self._teardown(txn_token, session_id)
            raise
        committed = state.staged_writes
        self._teardown(txn_token, session_id)
        return committed

    # ------------------------------------------------------------------
    # abort
    # ------------------------------------------------------------------

    def abort(
        self,
        *,
        txn_token: str,
        session_id: str,
        reason: str,
    ) -> None:
        if not isinstance(reason, str):
            raise TypeError("reason must be str")
        # abort must be idempotent on missing txn_token: if the commit path
        # already tore down, a follow-up abort is a no-op with a protocol
        # violation raised so callers can detect double-abort.
        if txn_token not in self._active:
            raise VaultCompoundProtocolViolation(
                f"abort on unknown txn_token"
            )
        self._require_active(txn_token, session_id)  # session-binding check
        self._teardown(txn_token, session_id)

    # ------------------------------------------------------------------
    # internals
    # ------------------------------------------------------------------

    def _require_active(
        self, txn_token: str, session_id: str
    ) -> CompoundTxnState:
        state = self._active.get(txn_token)
        if state is None:
            raise VaultCompoundProtocolViolation(
                "txn_token not active"
            )
        if state.session_id != session_id:
            raise VaultCompoundProtocolViolation(
                "session_id does not match txn's originating session"
            )
        return state

    def _check_ttl(self, state: CompoundTxnState) -> None:
        elapsed_ns = time.monotonic_ns() - state.created_at_monotonic_ns
        if elapsed_ns > COMPOUND_TXN_TTL_SECONDS * 1_000_000_000:
            # Tear the txn down and raise. Caller must re-begin.
            self._teardown(state.txn_token, state.session_id)
            from pipeline.vault.error_codes import VaultCompoundTTLExpired

            raise VaultCompoundTTLExpired(
                f"compound txn {state.txn_token[:8]}… exceeded "
                f"{COMPOUND_TXN_TTL_SECONDS}s TTL"
            )

    def _check_stage_caps(self, state: CompoundTxnState) -> None:
        """§4.10.7.2 stage-time caps (F-VAULT-24.compound_txn_cap_exceeded).

        Distinct from :meth:`_check_pre_commit_bytes_cap` which enforces the
        §8 ``MAX_COMPOUND_TXN_BYTES`` undo-snapshot cap at commit time.
        """
        if len(state.staged_writes) > MAX_STAGED_WRITES_PER_TXN:
            raise VaultCompoundCapExceeded(
                f"compound txn staged-writes count {len(state.staged_writes)} "
                f"exceeds cap {MAX_STAGED_WRITES_PER_TXN}"
            )
        total = sum(sw.data_len for sw in state.staged_writes)
        if total > MAX_STAGED_BYTES_PER_TXN:
            raise VaultCompoundCapExceeded(
                f"compound txn staged bytes {total} exceed "
                f"cap {MAX_STAGED_BYTES_PER_TXN}"
            )

    def _check_pre_commit_bytes_cap(self, state: CompoundTxnState) -> None:
        """§4.10.7.3 step 2 — undo-snapshot 64 MiB cap.

        Called from ``commit`` after the persist hook has populated
        ``pre_commit_bytes``. F-VAULT-COMPOUND-OVERSIZE on overflow.
        """
        total = sum(
            len(b) for _, b in state.pre_commit_bytes if b is not None
        )
        if total > MAX_COMPOUND_TXN_BYTES:
            raise VaultCompoundOversize(
                f"compound txn pre_commit_bytes {total} exceed "
                f"cap {MAX_COMPOUND_TXN_BYTES}"
            )

    def _runtime_integrity_check(self, state: CompoundTxnState) -> None:
        if type(state).__name__ != "CompoundTxnState":
            raise VaultCompoundIntegrityError(
                "txn state is not a CompoundTxnState"
            )
        for sw in state.staged_writes:
            if type(sw).__name__ != "StagedWrite":
                raise VaultCompoundIntegrityError(
                    "staged write is not a StagedWrite"
                )
            # Re-verify the pinned hash covers the pinned bytes; a mutation
            # attempt would show up here even though the dataclass is frozen.
            actual = hashlib.sha3_512(sw.data).hexdigest()
            if actual != sw.data_sha3_512:
                raise VaultCompoundIntegrityError(
                    "staged data hash drift from pinned record"
                )

    def _teardown(self, txn_token: str, session_id: str) -> None:
        self._active.pop(txn_token, None)
        lock_fd = self._lock_fds.pop(txn_token, None)
        if lock_fd is not None:
            try:
                fcntl.flock(lock_fd, fcntl.LOCK_UN)
            finally:
                try:
                    os.close(lock_fd)
                except OSError:
                    pass
        count = self._session_counts.get(session_id, 0)
        if count > 0:
            self._session_counts[session_id] = count - 1


# ---------------------------------------------------------------------------
# Public typing helper
# ---------------------------------------------------------------------------

from typing import Callable, Protocol


class CommitPersistHook(Protocol):
    def __call__(self, state: CompoundTxnState) -> None: ...


__all__ = [
    "COMPOUND_TXN_KINDS",
    "COMPOUND_TXN_TTL_SECONDS",
    "MAX_ACTIVE_COMPOUND_TXNS_PER_SESSION",
    "MAX_COMPOUND_TXN_BYTES",
    "MAX_STAGED_BYTES_PER_TXN",
    "MAX_STAGED_WRITES_PER_TXN",
    "TXN_TOKEN_ENTROPY_BYTES",
    "CommitPersistHook",
    "CompoundTxnDispatcher",
]
