"""M15 signed-commit discipline for ``vault_shared/``. [§4.6 + §9 steps 6 + 9]

Round T entry points (callers in §9 boot order):

* :func:`verify_seed_manifest` (§9 step 6) — read
  ``vault_shared/seed_manifest.json`` + ``seed_manifest.sig``, run the
  operator-signature primitive over the canonical
  ``(head_hash, m15_ledger_head)`` payload, verify the manifest's
  ``m15_ledger_head`` matches the caller-provided current ledger head, then
  delegate to :func:`pipeline.vault.mirror_verify.freeze_vault_shared` to
  pin the Merkle root over the seed partition.
* :func:`cedar_policy_loader_load_all` (§9 step 9) — read every
  ``cedar/*.cedar`` text under the (frozen) seed partition, defence-in-depth
  re-hash against ``VaultSharedFrozenRoot``, and return the policy texts
  keyed by relative path. Section 4 Logician is the consumer.

Operator-signature primitive injected as a :type:`SignatureVerifier`
``Callable[[bytes, str], bool]`` so this module does not bind to a specific
keystore in v0.1 (Round Q Cedar-stub pattern; Round S signature-injection
pattern; engineering lesson E-017).

Out of scope (deferred):

* M15.3 ``commit_cedar`` operator workflow (HIGH-severity admin_risk re-type).
  This is an operator-tooling round, not a boot-path concern.
* Privileged broker-bootstrap FD acquisition for seed re-reads. Round R
  vault_boot capstone wires that in; Round T uses Path-based reads because
  the broker is itself bootstrapping at §9 step 6.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, fields, is_dataclass
from pathlib import Path
from typing import Any, Callable, Final


BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_02_vault_topology.md": {
        "version": "v7.1",
        "hash_sha3_512_prefix16": "83a898275a4cf0a1",
        "sections_implemented": [
            "§4.6 M15 signed-commit discipline for vault_shared/",
            "§9 step 6 verify_seed_manifest — operator-signature + ledger-head bind",
            "§9 step 9 cedar_policy_loader_load_all — frozen-root defence-in-depth",
            "§6.9 F-M15-01 / F-M15-02 / F-M15-03 failure codes",
            "§6.12 F-CEDAR-01 policy-load failure code",
        ],
    },
}

from pipeline.vault.error_codes import (
    F_CEDAR_01,
    F_M15_02,
    F_M15_03,
    CedarError,
    M15Error,
)
from pipeline.vault.mirror_verify import (
    VaultSharedFrozenRoot,
    freeze_vault_shared,
)
from pipeline.vault.schemas import (
    IdentityTuple,
    SeedFile,
    VaultSharedSeedManifest,
)


# ---------------------------------------------------------------------------
# Exception family
# ---------------------------------------------------------------------------


class SeedManifestSignatureInvalid(M15Error):
    """Operator signature over (head_hash, m15_ledger_head) does not verify."""

    code = F_M15_02


class SeedManifestLedgerHeadDrift(M15Error):
    """Manifest m15_ledger_head does not match the current ledger head."""

    code = F_M15_03


class CedarPolicyLoadFailed(CedarError):
    """Cedar policy file missing, content drifted, or unreadable post-freeze."""

    code = F_CEDAR_01


# ---------------------------------------------------------------------------
# Type aliases
# ---------------------------------------------------------------------------


SignatureVerifier = Callable[[bytes, str], bool]
"""Operator-signature primitive.

``verify(payload_bytes, signature_str) -> True`` iff the signature is a valid
operator signature over the canonical payload bytes. Implementations are
expected to be pure (no I/O, no global state); they are called once per
``verify_seed_manifest`` invocation.
"""


# ---------------------------------------------------------------------------
# Disk readers
# ---------------------------------------------------------------------------


def load_seed_manifest(manifest_path: Path) -> VaultSharedSeedManifest:
    """Parse ``seed_manifest.json`` into :class:`VaultSharedSeedManifest`.

    Raises ``OSError`` / ``FileNotFoundError`` on read errors,
    ``json.JSONDecodeError`` on malformed JSON, and ``KeyError`` /
    ``TypeError`` on shape errors. The dataclass constructors enforce the
    rest of the per-field invariants.
    """
    if not isinstance(manifest_path, Path):
        raise TypeError(
            f"manifest_path must be pathlib.Path, got {type(manifest_path).__name__}"
        )
    raw = manifest_path.read_text(encoding="utf-8")
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise TypeError(
            f"seed manifest root must be a JSON object, got {type(payload).__name__}"
        )
    files_payload = payload["files"]
    if not isinstance(files_payload, list):
        raise TypeError("seed manifest 'files' must be a JSON array")
    seed_files = tuple(_seed_file_from_dict(item) for item in files_payload)
    return VaultSharedSeedManifest(
        head_hash=str(payload["head_hash"]),
        files=seed_files,
        committed_at=str(payload["committed_at"]),
        committed_by=str(payload["committed_by"]),
        m15_ledger_head=str(payload["m15_ledger_head"]),
        signature=str(payload["signature"]),
    )


def _seed_file_from_dict(item: Any) -> SeedFile:
    if not isinstance(item, dict):
        raise TypeError("seed manifest 'files' entries must be JSON objects")
    identity = item["identity_tuple"]
    if not isinstance(identity, dict):
        raise TypeError("SeedFile.identity_tuple must be a JSON object")
    return SeedFile(
        relative_path=str(item["relative_path"]),
        content_hash=str(item["content_hash"]),
        size_bytes=int(item["size_bytes"]),
        mode=int(item["mode"]),
        identity_tuple=IdentityTuple(
            volume_uuid=str(identity["volume_uuid"]),
            fs_file_id=str(identity["fs_file_id"]),
            mount_id=str(identity["mount_id"]),
            fs_type=str(identity["fs_type"]),
            captured_at=str(identity["captured_at"]),
        ),
    )


def load_signature(signature_path: Path) -> str:
    """Read ``seed_manifest.sig`` as text, stripping surrounding whitespace."""
    if not isinstance(signature_path, Path):
        raise TypeError(
            f"signature_path must be pathlib.Path, got {type(signature_path).__name__}"
        )
    return signature_path.read_text(encoding="utf-8").strip()


# ---------------------------------------------------------------------------
# Canonical signature payload
# ---------------------------------------------------------------------------


def serialize_signature_payload(*, head_hash: str, m15_ledger_head: str) -> bytes:
    """Canonical bytes signed by the operator over the seed manifest.

    Sorted-key, no-whitespace JSON of ``{"head_hash": ..., "m15_ledger_head":
    ...}`` — UTF-8 encoded. Both the operator-side committer and the
    boot-side verifier MUST produce identical bytes; otherwise the signature
    will not verify.
    """
    if not isinstance(head_hash, str):
        raise TypeError(f"head_hash must be str, got {type(head_hash).__name__}")
    if not isinstance(m15_ledger_head, str):
        raise TypeError(
            f"m15_ledger_head must be str, got {type(m15_ledger_head).__name__}"
        )
    payload = {"head_hash": head_hash, "m15_ledger_head": m15_ledger_head}
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


# ---------------------------------------------------------------------------
# verify_seed_manifest — §9 step 6
# ---------------------------------------------------------------------------


def verify_seed_manifest(
    *,
    manifest_path: Path,
    signature_path: Path,
    vault_shared_root: Path,
    current_ledger_head: str,
    verify_signature: SignatureVerifier,
) -> VaultSharedFrozenRoot:
    """§9 step 6 — verify seed manifest + freeze.

    Order (fail-closed at every step):

    1. Type gates on every parameter.
    2. Load manifest + signature from disk.
    3. Run the operator signature primitive over canonical
       ``(head_hash, m15_ledger_head)``. Failure or exception →
       :class:`SeedManifestSignatureInvalid` (F-M15-02).
    4. Verify ``manifest.m15_ledger_head`` matches ``current_ledger_head``.
       Mismatch → :class:`SeedManifestLedgerHeadDrift` (F-M15-03).
    5. Delegate to :func:`mirror_verify.freeze_vault_shared` for content +
       Merkle pin. Failures from that path raise their own M15Error /
       MirrorError children (F-M15-01 / F-MIRROR-02 chain).
    """
    if not isinstance(manifest_path, Path):
        raise TypeError(
            f"manifest_path must be pathlib.Path, got {type(manifest_path).__name__}"
        )
    if not isinstance(signature_path, Path):
        raise TypeError(
            f"signature_path must be pathlib.Path, got {type(signature_path).__name__}"
        )
    if not isinstance(vault_shared_root, Path):
        raise TypeError(
            f"vault_shared_root must be pathlib.Path, got {type(vault_shared_root).__name__}"
        )
    if not isinstance(current_ledger_head, str):
        raise TypeError(
            f"current_ledger_head must be str, got {type(current_ledger_head).__name__}"
        )
    if not callable(verify_signature):
        raise TypeError("verify_signature must be callable")

    manifest = load_seed_manifest(manifest_path)
    signature = load_signature(signature_path)

    payload = serialize_signature_payload(
        head_hash=manifest.head_hash,
        m15_ledger_head=manifest.m15_ledger_head,
    )
    try:
        signature_ok = bool(verify_signature(payload, signature))
    except Exception as exc:
        raise SeedManifestSignatureInvalid(
            f"signature verifier raised {type(exc).__name__}: {exc}"
        ) from exc
    if not signature_ok:
        raise SeedManifestSignatureInvalid(
            "operator signature over seed manifest did not verify"
        )

    if manifest.m15_ledger_head != current_ledger_head:
        raise SeedManifestLedgerHeadDrift(
            f"manifest m15_ledger_head {manifest.m15_ledger_head!r} does not "
            f"match current ledger head {current_ledger_head!r}"
        )

    return freeze_vault_shared(
        manifest=manifest, vault_shared_root=vault_shared_root
    )


# ---------------------------------------------------------------------------
# cedar_policy_loader_load_all — §9 step 9
# ---------------------------------------------------------------------------


_CEDAR_PREFIX = "cedar/"
_CEDAR_SUFFIX = ".cedar"


def cedar_policy_loader_load_all(
    *,
    frozen_root: VaultSharedFrozenRoot,
    vault_shared_root: Path,
) -> dict[str, str]:
    """§9 step 9 — load every top-level ``cedar/*.cedar`` policy text.

    Reads each file from disk (post-freeze defence-in-depth re-read), checks
    that SHA-3-512 of the bytes matches the pinned ``content_hashes_hex``
    entry in ``frozen_root``, and returns ``{relative_path: text}``. Nested
    ``cedar/sub/*.cedar`` entries are carried in the frozen root for routing
    purposes but not surfaced here; Section 4 Logician routes nested
    categories explicitly.

    Any of:
      * Cedar file missing on disk
      * Cedar file unreadable
      * Cedar file content drifted from the pinned hash
      * Cedar file decodes to non-UTF-8
    raises :class:`CedarPolicyLoadFailed` (F-CEDAR-01) and aborts boot.
    """
    if not isinstance(frozen_root, VaultSharedFrozenRoot):
        raise TypeError(
            f"frozen_root must be VaultSharedFrozenRoot, got {type(frozen_root).__name__}"
        )
    if not isinstance(vault_shared_root, Path):
        raise TypeError(
            f"vault_shared_root must be pathlib.Path, got {type(vault_shared_root).__name__}"
        )

    out: dict[str, str] = {}
    for rel in frozen_root.seed_paths:
        if not rel.startswith(_CEDAR_PREFIX):
            continue
        if not rel.endswith(_CEDAR_SUFFIX):
            continue
        # Top-level only: exactly one path segment after "cedar/".
        if "/" in rel[len(_CEDAR_PREFIX):]:
            continue

        target = vault_shared_root / rel
        if not target.is_file():
            raise CedarPolicyLoadFailed(
                f"Cedar policy missing on disk post-freeze: {rel}"
            )
        try:
            raw = target.read_bytes()
        except OSError as exc:
            raise CedarPolicyLoadFailed(
                f"Cedar policy unreadable: {rel}: {exc}"
            ) from exc

        expected_hash = frozen_root.content_hashes_hex.get(rel)
        if expected_hash is None:
            # Should be unreachable — every seed_paths entry has a hash.
            raise CedarPolicyLoadFailed(
                f"Cedar policy {rel} has no pinned content hash in frozen root"
            )
        actual_hash = hashlib.sha3_512(raw).hexdigest()
        if actual_hash != expected_hash:
            raise CedarPolicyLoadFailed(
                f"Cedar policy content drifted post-freeze: {rel} "
                f"expected={expected_hash[:16]}… actual={actual_hash[:16]}…"
            )

        try:
            out[rel] = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise CedarPolicyLoadFailed(
                f"Cedar policy {rel} is not valid UTF-8: {exc}"
            ) from exc

    return out


__all__ = [
    "CedarPolicyLoadFailed",
    "SeedManifestLedgerHeadDrift",
    "SeedManifestSignatureInvalid",
    "SignatureVerifier",
    "cedar_policy_loader_load_all",
    "load_seed_manifest",
    "load_signature",
    "serialize_signature_payload",
    "verify_seed_manifest",
]
