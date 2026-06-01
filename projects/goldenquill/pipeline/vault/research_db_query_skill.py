"""Vault-owned first-class research-DB read skill. [§3.3 + §2.9]

Round Q' — thin wrapper over the FD broker scoped to
``vault_shared/research_db/``. The caller passes a ``key`` (entry-relative
path under the research-DB root); the skill prepends the canonical
``vault_shared/research_db/`` prefix and delegates to the broker with
``requester_skill="research-db-query"``.

Cross-org safety: the research DB lives under ``vault_shared/``, which is
deliberately shared across orgs. To prevent a caller from smuggling a
cross-org path through this skill — e.g. ``key="orgs/other/vault/leak.json"``
— the key is validated **before** the broker call:

* absolute paths are rejected;
* ``..`` anywhere in the key is rejected;
* the ``orgs/`` prefix is rejected (belongs to the org-scoped read path,
  not the research DB);
* ``vault_shared/`` / ``research_db/`` prefixes are rejected (layering
  violation — the skill prepends its own prefix, so the caller must not
  include it).
"""

from __future__ import annotations

import os
import secrets
from typing import Final

from pipeline.vault.error_codes import VaultAccessDenied, VaultCrossOrgAccess
from pipeline.vault.fd_broker import FDBroker
from pipeline.vault.schemas import FDBrokerRequest, IdentityTuple

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_02_vault_topology.md": {
        "version": "v7.1",
        "hash_sha3_512_prefix16": "83a898275a4cf0a1",
        "sections_implemented": [
            "§3.3 research-db-query first-class read skill (vault_shared/research_db scope)",
            "§2.7 FDBrokerRequest mint + per-request nonce",
            "§2.9 on-disk layout (vault_shared/research_db/ partition)",
            "§4.10.4 post-gate path-allowlist hook (cross-org denial via forbidden-prefix list)",
        ],
    },
}

_REQUESTER_SKILL: str = "research-db-query"
_RESEARCH_DB_PREFIX: str = "vault_shared/research_db/"
_READ_CHUNK_BYTES: int = 65_536

_FORBIDDEN_KEY_PREFIXES: tuple[str, ...] = (
    "orgs/",
    "vault_shared/",
    "research_db/",
    "/",
)


def _validate_key(key: str) -> None:
    if not isinstance(key, str):
        raise TypeError(f"key must be str, got {type(key).__name__}")
    if key == "":
        raise ValueError("key must be non-empty")
    if ".." in key.split("/"):
        raise VaultCrossOrgAccess(
            f"research-db key contains path-escape: {key!r}"
        )
    for prefix in _FORBIDDEN_KEY_PREFIXES:
        if key.startswith(prefix):
            raise VaultCrossOrgAccess(
                f"research-db key has forbidden prefix {prefix!r}: {key!r}"
            )


def research_db_read(
    *,
    key: str,
    session_id: str,
    slug: str,
    broker: FDBroker,
) -> tuple[bytes, IdentityTuple]:
    """Read ``key`` under the research DB root through the FD broker.

    :returns: ``(content_bytes, identity_tuple_of_opened_file)``.
    :raises TypeError: E-001 arg-type violation.
    :raises ValueError: empty ``key``.
    :raises VaultCrossOrgAccess: key violates the research-DB layering.
    :raises VaultAccessDenied: broker denied the request; the denial
        reason is surfaced verbatim in the exception message.
    """
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
    _validate_key(key)

    request = FDBrokerRequest(
        requester_skill=_REQUESTER_SKILL,
        requester_pid=os.getpid(),
        requester_session_id=session_id,
        requester_org_slug=slug,
        requested_path=_RESEARCH_DB_PREFIX + key,
        intent="read",
        nonce_hex=secrets.token_hex(32),
    )
    response, fd = broker.request_fd(request)
    if not response.granted or fd is None:
        raise VaultAccessDenied(
            f"research-db-query denied for {key!r}: {response.denial_reason}"
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


__all__ = ["research_db_read"]
