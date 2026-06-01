"""Section 2 Vault on-disk data-structure schemas.

Every schema is a frozen, keyword-only dataclass. Canonical JSON serialization
uses ``canonical_json_bytes`` from :mod:`pipeline.sovereignty.audit` so
whitespace- or key-order-only differences cannot evade HMAC binding.

Blueprint §2.1–§2.10 (section_02_vault_topology.md).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final, Optional


BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_02_vault_topology.md": {
        "version": "v7.1",
        "hash_sha3_512_prefix16": "83a898275a4cf0a1",
        "sections_implemented": [
            "§2.1 IdentityTuple",
            "§2.2 StableUUIDFloor",
            "§2.3 VaultInitMarker",
            "§2.4 VaultSharedSeedManifest + SeedFile",
            "§2.5 TrustRootMirrorManifest",
            "§2.6 ProcessWrapperManifest",
            "§2.7 FDBrokerRequest + FDBrokerResponse",
            "§2.8 SeccompFilterManifest + SandboxProfileManifest",
            "§2.10 StagedWrite + CompoundTxnState (Option-B compound-txn backfill)",
            "§3.6 SectionLockMarker (handshake artefact)",
        ],
    },
}


# ---------------------------------------------------------------------------
# §2.1 IdentityTuple
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class IdentityTuple:
    volume_uuid: str
    fs_file_id: str
    mount_id: str
    fs_type: str
    captured_at: str


# ---------------------------------------------------------------------------
# §2.2 StableUUIDFloor
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class StableUUIDFloor:
    fs_type: str
    volume_uuid: str
    accepted: bool
    rejection_reason: str
    evaluated_at: str


# ---------------------------------------------------------------------------
# §2.3 VaultInitMarker
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class VaultInitMarker:
    scope: str
    slug: str
    created_at: str
    created_under_uuid: str
    identity_tuple: IdentityTuple
    operator_id: str
    section_lock_hash: str


# ---------------------------------------------------------------------------
# §2.4 VaultSharedSeedManifest + SeedFile
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class SeedFile:
    relative_path: str
    content_hash: str
    size_bytes: int
    mode: int
    identity_tuple: IdentityTuple


@dataclass(frozen=True, kw_only=True)
class VaultSharedSeedManifest:
    head_hash: str
    files: tuple[SeedFile, ...]
    committed_at: str
    committed_by: str
    m15_ledger_head: str
    signature: str


# ---------------------------------------------------------------------------
# §2.5 TrustRootMirrorManifest
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class TrustRootMirrorManifest:
    mirror_path: str
    content_hash: str
    identity_tuple: IdentityTuple
    m15_ledger_head: str
    operator_signature: str
    signed_at: str
    immutability_flag_set: bool


# ---------------------------------------------------------------------------
# §2.6 ProcessWrapperManifest
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class ProcessWrapperManifest:
    platform: str
    wrapper_path: str
    content_hash: str
    identity_tuple: IdentityTuple
    m15_ledger_head: str
    mode: int


# ---------------------------------------------------------------------------
# §2.7 FDBrokerRequest / FDBrokerResponse
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class FDBrokerRequest:
    requester_skill: str
    requester_pid: int
    requester_session_id: str
    requester_org_slug: str
    requested_path: str
    intent: str
    nonce_hex: str


@dataclass(frozen=True, kw_only=True)
class FDBrokerResponse:
    granted: bool
    denial_reason: str
    fd_count: int
    issued_at: str
    identity_tuple: IdentityTuple
    cedar_decision_id: str


# ---------------------------------------------------------------------------
# §2.8 SeccompFilterManifest / SandboxProfileManifest
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class SeccompFilterManifest:
    platform: str
    filter_bpf_hash: str
    denied_syscalls: tuple[str, ...]
    m15_ledger_head: str
    operator_signature: str


@dataclass(frozen=True, kw_only=True)
class SandboxProfileManifest:
    platform: str
    profile_text_hash: str
    denied_primitives: tuple[str, ...]
    m15_ledger_head: str
    operator_signature: str


# ---------------------------------------------------------------------------
# §2.10 StagedWrite + CompoundTxnState (Option-B compound-txn backfill)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class StagedWrite:
    intent: str
    path: str
    data: bytes
    data_sha3_512: str
    data_len: int
    expected_current_file_hash: Optional[str]
    write_mode: str
    staged_at_monotonic_ns: int


@dataclass(frozen=True, kw_only=True)
class CompoundTxnState:
    txn_kind: str
    txn_token: str
    session_id: str
    created_at_monotonic_ns: int
    staged_writes: tuple[StagedWrite, ...] = ()
    pre_commit_bytes: tuple[tuple[str, Optional[bytes]], ...] = ()


# ---------------------------------------------------------------------------
# §3.6 SectionLockMarker (handshake artefact)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class SectionLockMarker:
    version: str
    locked_at: str
    locked_by: str
    architecture_head_hash: str
    blueprint_content_hash: str
    m15_ledger_head: str
    operator_signature: str
    section: str = "02-vault-topology"


__all__ = [
    "IdentityTuple",
    "StableUUIDFloor",
    "VaultInitMarker",
    "SeedFile",
    "VaultSharedSeedManifest",
    "TrustRootMirrorManifest",
    "ProcessWrapperManifest",
    "FDBrokerRequest",
    "FDBrokerResponse",
    "SeccompFilterManifest",
    "SandboxProfileManifest",
    "StagedWrite",
    "CompoundTxnState",
    "SectionLockMarker",
]
