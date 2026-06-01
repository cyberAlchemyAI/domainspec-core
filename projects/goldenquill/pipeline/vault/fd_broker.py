"""Vault-owned-skill FD issuance broker. [§2.7 + §2.9 + §3.4]

v0.1 scope (Round Q): in-process broker that accepts :class:`FDBrokerRequest`
payloads, enforces the two-skill allowlist, checks nonce uniqueness, runs a
default-allow Cedar stub, invokes the optional Logician post-gate hook, and
opens a FD through :func:`gate_and_open`. The caller receives the FD directly
(no ``SCM_RIGHTS`` transport in v0.1 — seats run in-process).

Deferred past v0.1 (out-of-scope for this round, explicitly noted):

* ``SCM_RIGHTS`` FD transport over Unix domain sockets + peer-PID auth.
* Cedar policy loader + signed-manifest enforcement (default-allow for v0.1).
* Wrapper-hash re-verify at exec-time.
* Nonce persistence — the in-process set is lost on broker restart, which is
  safe because a restart invalidates every outstanding session anyway.

Allowlist invariants (§2.9):

* ``FD_BROKER_ALLOWED_SKILLS`` is a :class:`frozenset` hard-coded in this
  module. There is no dynamic registration — adding a new Vault-owned skill
  requires editing this constant + an M15 commit + a Section-2 re-lock.
* ``requester_skill`` not in the allowlist → F-FD-01 / denied response.
"""

from __future__ import annotations

import os
import secrets
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Final, Optional


BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_02_vault_topology.md": {
        "version": "v7.1",
        "hash_sha3_512_prefix16": "83a898275a4cf0a1",
        "sections_implemented": [
            "§2.7 FD broker responsibility scope",
            "§2.9 FD broker allowlist invariants",
            "§3.4 FD broker public interface",
            "§6.8 F-FD-01 / F-FD-02 / F-FD-03 failure codes (v0.1 scope)",
        ],
    },
}

from pipeline.vault.error_codes import F_FD_01, F_FD_02, F_FD_03, FDBrokerError
from pipeline.vault.gate_and_open import gate_and_open
from pipeline.vault.identity_tuple import (
    IdentityTupleUnavailable,
    resolve_identity_tuple,
)
from pipeline.vault.schemas import FDBrokerRequest, FDBrokerResponse, IdentityTuple

# ---------------------------------------------------------------------------
# Constants (§8 pins)
# ---------------------------------------------------------------------------

FD_BROKER_ALLOWED_SKILLS: frozenset[str] = frozenset(
    {"vault-query", "research-db-query"}
)
FD_BROKER_ALLOWED_INTENTS: frozenset[str] = frozenset(
    {"read", "write", "execute", "read-wrapper"}
)
NONCE_TTL_SECONDS: int = 300
NONCE_REGISTRY_MAX_ENTRIES: int = 65_536


# ---------------------------------------------------------------------------
# Exception family
# ---------------------------------------------------------------------------


class FdBrokerUnknownSkill(FDBrokerError):
    code = F_FD_01


class FdBrokerNonceReplayed(FDBrokerError):
    code = F_FD_02


class FdBrokerCedarVeto(FDBrokerError):
    code = F_FD_03


class FdBrokerPostGateVeto(FDBrokerError):
    code = F_FD_03


# ---------------------------------------------------------------------------
# Internal denial helper
# ---------------------------------------------------------------------------


def _iso_utc_now() -> str:
    import datetime

    return (
        datetime.datetime.now(datetime.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _sentinel_identity_tuple(captured_at: str) -> IdentityTuple:
    """Identity tuple stamped on denial responses.

    v0.1 denials return a non-optional IdentityTuple so every response shape
    matches the blueprint (§2.7). The sentinel's zeroed fields make it
    trivially distinguishable from a real tuple.
    """
    return IdentityTuple(
        volume_uuid="00" * 16,
        fs_file_id="00" * 8,
        mount_id="00" * 8,
        fs_type="denied",
        captured_at=captured_at,
    )


# ---------------------------------------------------------------------------
# Broker
# ---------------------------------------------------------------------------


PostGateHook = Callable[[FDBrokerRequest], bool]
Clock = Callable[[], float]


class FDBroker:
    """Per-process FD issuance broker.

    Instantiated once per Vault boot. Holds the nonce registry + optional
    Logician post-gate hook. Not thread-safe; the Vault boot sequence wraps
    any concurrent seat launches behind its own serialization.
    """

    def __init__(
        self,
        *,
        vault_root_fd: int,
        vault_root_path: Path,
        post_gate_hook: Optional[PostGateHook] = None,
        clock: Optional[Clock] = None,
    ) -> None:
        if not isinstance(vault_root_fd, int):
            raise TypeError(
                f"vault_root_fd must be int, got {type(vault_root_fd).__name__}"
            )
        if not isinstance(vault_root_path, Path):
            raise TypeError(
                f"vault_root_path must be pathlib.Path, got "
                f"{type(vault_root_path).__name__}"
            )
        if post_gate_hook is not None and not callable(post_gate_hook):
            raise TypeError("post_gate_hook must be callable or None")
        if clock is not None and not callable(clock):
            raise TypeError("clock must be callable or None")
        self._vault_root_fd: int = vault_root_fd
        self._vault_root_path: Path = vault_root_path
        self._post_gate_hook: Optional[PostGateHook] = post_gate_hook
        self._clock: Clock = clock or time.monotonic
        # nonce_hex -> registered_at_monotonic
        self._nonces: dict[str, float] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register_post_gate(self, hook: PostGateHook) -> None:
        if not callable(hook):
            raise TypeError("hook must be callable")
        self._post_gate_hook = hook

    # ------------------------------------------------------------------
    # request_fd
    # ------------------------------------------------------------------

    def request_fd(
        self, request: FDBrokerRequest
    ) -> tuple[FDBrokerResponse, Optional[int]]:
        if not isinstance(request, FDBrokerRequest):
            raise TypeError(
                "request must be FDBrokerRequest, got "
                f"{type(request).__name__}"
            )
        self._prune_nonces()
        issued_at = _iso_utc_now()

        # 1) Skill allowlist
        if request.requester_skill not in FD_BROKER_ALLOWED_SKILLS:
            return (
                self._deny(
                    issued_at,
                    f"unknown-skill:{request.requester_skill!r}",
                ),
                None,
            )

        # 2) Intent allowlist
        if request.intent not in FD_BROKER_ALLOWED_INTENTS:
            return (
                self._deny(issued_at, f"invalid-intent:{request.intent!r}"),
                None,
            )

        # 3) Basic session/slug sanity
        if not request.requester_session_id:
            return self._deny(issued_at, "empty-session-id"), None
        if not request.requester_org_slug:
            return self._deny(issued_at, "empty-org-slug"), None

        # 4) Nonce replay
        if request.nonce_hex in self._nonces:
            return self._deny(issued_at, "nonce-replay"), None

        # 5) Cedar stub — default allow; mint a synthetic decision_id for
        #    audit-trail continuity with the future policy-loader-backed path.
        cedar_decision_id = secrets.token_hex(16)

        # 6) Post-gate hook (Logician veto)
        if self._post_gate_hook is not None:
            try:
                allowed = bool(self._post_gate_hook(request))
            except Exception as exc:  # hook misbehavior = veto, don't leak FD
                return (
                    self._deny(
                        issued_at,
                        f"post-gate-hook-raised:{type(exc).__name__}",
                    ),
                    None,
                )
            if not allowed:
                return self._deny(issued_at, "post-gate-veto"), None

        # 7) Open the FD
        open_flags = os.O_RDONLY
        if request.intent == "write":
            open_flags = os.O_RDWR
        try:
            fd = gate_and_open(
                self._vault_root_fd, request.requested_path, open_flags
            )
        except Exception as exc:
            return (
                self._deny(
                    issued_at,
                    f"gate-open-rejected:{type(exc).__name__}",
                ),
                None,
            )

        # 8) Capture identity tuple of the opened file
        try:
            abs_path = self._vault_root_path / request.requested_path
            identity = resolve_identity_tuple(abs_path)
        except IdentityTupleUnavailable as exc:
            # Close the FD so we don't leak
            try:
                os.close(fd)
            except OSError:
                pass
            return (
                self._deny(
                    issued_at, f"identity-tuple-unavailable:{exc}"
                ),
                None,
            )

        # 9) Record nonce + return
        self._nonces[request.nonce_hex] = self._clock()
        response = FDBrokerResponse(
            granted=True,
            denial_reason="",
            fd_count=1,
            issued_at=issued_at,
            identity_tuple=identity,
            cedar_decision_id=cedar_decision_id,
        )
        return response, fd

    # ------------------------------------------------------------------
    # release_fd
    # ------------------------------------------------------------------

    def release_fd(self, fd: int) -> None:
        if not isinstance(fd, int):
            raise TypeError(f"fd must be int, got {type(fd).__name__}")
        try:
            os.close(fd)
        except OSError:
            # Idempotent: already-closed is a no-op from the caller's POV.
            pass

    # ------------------------------------------------------------------
    # internals
    # ------------------------------------------------------------------

    def _prune_nonces(self) -> None:
        if not self._nonces:
            return
        now = self._clock()
        cutoff = now - NONCE_TTL_SECONDS
        stale = [n for n, t in self._nonces.items() if t < cutoff]
        for n in stale:
            self._nonces.pop(n, None)
        # Cap runaway growth if a caller floods unique nonces.
        if len(self._nonces) > NONCE_REGISTRY_MAX_ENTRIES:
            # Drop the oldest half.
            oldest = sorted(self._nonces.items(), key=lambda kv: kv[1])
            keep_from = len(oldest) // 2
            self._nonces = dict(oldest[keep_from:])

    def _deny(self, issued_at: str, reason: str) -> FDBrokerResponse:
        return FDBrokerResponse(
            granted=False,
            denial_reason=reason,
            fd_count=0,
            issued_at=issued_at,
            identity_tuple=_sentinel_identity_tuple(issued_at),
            cedar_decision_id="",
        )


__all__ = [
    "FD_BROKER_ALLOWED_INTENTS",
    "FD_BROKER_ALLOWED_SKILLS",
    "NONCE_REGISTRY_MAX_ENTRIES",
    "NONCE_TTL_SECONDS",
    "FDBroker",
    "FdBrokerCedarVeto",
    "FdBrokerNonceReplayed",
    "FdBrokerPostGateVeto",
    "FdBrokerUnknownSkill",
    "PostGateHook",
]
