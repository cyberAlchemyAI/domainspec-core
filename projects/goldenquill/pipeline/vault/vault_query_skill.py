"""Vault-owned first-class read skill. [§3.3 + §2.9]

Round Q' — thin consumer of :class:`pipeline.vault.fd_broker.FDBroker`.
Mints a per-request nonce, submits a :class:`FDBrokerRequest` with
``requester_skill="vault-query"``, reads the granted FD to bytes, and
returns ``(bytes, IdentityTuple)``.

Denials from the broker (unknown skill, nonce replay, post-gate veto,
path-escape, missing file) are re-raised as :class:`VaultAccessDenied`
with the broker's ``denial_reason`` string preserved in the message so
the caller can react deterministically.
"""

from __future__ import annotations

import os
import secrets
from typing import Final

from pipeline.vault.error_codes import VaultAccessDenied
from pipeline.vault.fd_broker import FDBroker
from pipeline.vault.schemas import FDBrokerRequest, IdentityTuple

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_02_vault_topology.md": {
        "version": "v7.1",
        "hash_sha3_512_prefix16": "83a898275a4cf0a1",
        "sections_implemented": [
            "§3.3 vault-query first-class read skill (thin FDBroker consumer)",
            "§2.7 FDBrokerRequest mint + per-request nonce",
        ],
    },
}

_REQUESTER_SKILL: str = "vault-query"
_READ_CHUNK_BYTES: int = 65_536


def vault_read(
    *,
    path: str,
    session_id: str,
    slug: str,
    broker: FDBroker,
    intent: str = "read",
) -> tuple[bytes, IdentityTuple]:
    """Read ``path`` under the Vault root through the FD broker.

    :returns: ``(content_bytes, identity_tuple_of_opened_file)``.
    :raises TypeError: E-001 arg-type violation.
    :raises ValueError: empty ``path``.
    :raises VaultAccessDenied: broker denied the request; the denial
        reason is surfaced verbatim in the exception message.
    """
    if not isinstance(path, str):
        raise TypeError(f"path must be str, got {type(path).__name__}")
    if not isinstance(session_id, str):
        raise TypeError(
            f"session_id must be str, got {type(session_id).__name__}"
        )
    if not isinstance(slug, str):
        raise TypeError(f"slug must be str, got {type(slug).__name__}")
    if not isinstance(broker, FDBroker):
        raise TypeError(
            f"broker must be FDBroker, got {type(broker).__name__}"
        )
    if not isinstance(intent, str):
        raise TypeError(f"intent must be str, got {type(intent).__name__}")
    if path == "":
        raise ValueError("path must be non-empty")

    request = FDBrokerRequest(
        requester_skill=_REQUESTER_SKILL,
        requester_pid=os.getpid(),
        requester_session_id=session_id,
        requester_org_slug=slug,
        requested_path=path,
        intent=intent,
        nonce_hex=secrets.token_hex(32),
    )
    response, fd = broker.request_fd(request)
    if not response.granted or fd is None:
        raise VaultAccessDenied(
            f"vault-query denied for {path!r}: {response.denial_reason}"
        )
    try:
        chunks: list[bytes] = []
        while True:
            buf = os.read(fd, _READ_CHUNK_BYTES)
            if not buf:
                break
            chunks.append(buf)
        return b"".join(chunks), response.identity_tuple
    finally:
        broker.release_fd(fd)


__all__ = ["vault_read"]
