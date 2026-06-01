"""F-ROUTER-INTEGRITY-MULTI-SOURCE (F-AMDT-10) — PRE-gate on router.yaml promotion.

EN-003 Cycle 4 Red Team finding C4-NEW-02: the existing same-commit pair
rule ("changes to ``router.yaml`` MUST co-commit with
``router_integrity.pinned.json``") is defeated by a single malicious commit
touching both files. A repo-write adversary crafts one commit that updates
``router.yaml`` and simultaneously rewrites the pinned hashes to match.
Text-level closure cannot bind an in-repo pair rule to external integrity.

This gate adds a third independent integrity source — an out-of-repo
HMAC-chained manifest signed per-update with a key held outside the repo.
A valid router.yaml promotion now requires agreement across three sources:

1. The live ``router.yaml`` bytes, hashed via the injected
   :class:`HashBytesCallable` (SHA3-512).
2. The ``router_yaml_sha3_512`` field of
   ``router_integrity.pinned.json``.
3. The external manifest's ``chain_head_hash`` + a valid Ed25519
   signature + a chain-continuity link to the prior manifest row.

No single-commit mutation inside the repo can satisfy all three.

The gate fires as a PRE-gate on the *promotion request* (diff against
last-known-good, or write-lock release on ``router.yaml``). Gates never
import ``hashlib``, ``cryptography``, or parse YAML — every external
input flows through a ``@runtime_checkable`` Protocol.

Blueprint anchor: ``pipeline/blueprint/v0.1/section_04_logician.md`` v2.1
(parent LOCK); v2.2 wave-3 delta row for F-AMDT-10.

Semantics (spec card v1, 2026-04-20):

* Any reader raises → FAIL fail-closed with ``reader_error`` populated;
  ``check_failed = "reader_fail"``.
* ``router_yaml_reader`` return not ``bytes`` → FAIL.
* ``hash_bytes`` return not ``str`` / empty → FAIL.
* ``pinned_hash_reader`` return not ``dict`` OR missing/empty/non-str
  ``router_yaml_sha3_512`` → FAIL.
* ``external_manifest_reader`` return not ``dict`` OR missing/non-str
  ``chain_head_hash``/``prior_chain_head_hash`` OR missing/non-bytes
  ``signature``/``signed_payload_bytes`` OR empty ``chain_head_hash`` →
  FAIL. ``prior_chain_head_hash`` is permitted to be the empty string on
  the bootstrap row (validated against ``prior_chain_head_reader()``
  returning ``None``).
* ``prior_chain_head_reader`` return neither ``None`` nor ``str`` → FAIL.
* Pair mismatch (live_hash ≠ pinned_hash) → FAIL with
  ``check_failed = "pair"``.
* External mismatch (chain_head_hash ≠ live_hash) → FAIL with
  ``check_failed = "external"``.
* Signature invalid (strict ``is True`` identity) → FAIL with
  ``check_failed = "signature"``.
* Chain break: bootstrap case requires current ``prior_chain_head_hash``
  to be ``""``; non-bootstrap requires it to equal the prior row's
  ``chain_head_hash`` → FAIL with ``check_failed = "chain_break"``.
* PASS only when all four substantive checks succeed.

Checks run in order (pair → external → signature → chain). The first
failure short-circuits — each failure class is independently actionable
by the operator, so a combined "all-four-failed" record is not emitted.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional

from pipeline.logician.gates._protocols import (
    ExternalManifestReaderCallable,
    HashBytesCallable,
    PinnedHashReaderCallable,
    PriorChainHeadReaderCallable,
    RouterYamlReaderCallable,
    SignatureVerifyCallable,
)


F_AMDT_10: Final[str] = "F-AMDT-10"
F_AMDT_10_PAIR: Final[str] = "F-AMDT-10-PAIR"
F_AMDT_10_EXTERNAL: Final[str] = "F-AMDT-10-EXTERNAL"
F_AMDT_10_SIGNATURE: Final[str] = "F-AMDT-10-SIGNATURE"
F_AMDT_10_CHAIN_BREAK: Final[str] = "F-AMDT-10-CHAIN-BREAK"
F_AMDT_10_READER_FAIL: Final[str] = "F-AMDT-10-READER-FAIL"


_CHECK_PAIR: Final[str] = "pair"
_CHECK_EXTERNAL: Final[str] = "external"
_CHECK_SIGNATURE: Final[str] = "signature"
_CHECK_CHAIN_BREAK: Final[str] = "chain_break"
_CHECK_READER_FAIL: Final[str] = "reader_fail"


_REASON_ROUTER_YAML_READER_RAISED: Final[str] = "router_yaml_reader_raised"
_REASON_ROUTER_YAML_NOT_BYTES: Final[str] = "router_yaml_not_bytes"
_REASON_HASH_BYTES_RAISED: Final[str] = "hash_bytes_raised"
_REASON_LIVE_HASH_NOT_STR: Final[str] = "live_hash_not_str"
_REASON_LIVE_HASH_EMPTY: Final[str] = "live_hash_empty"
_REASON_PINNED_READER_RAISED: Final[str] = "pinned_hash_reader_raised"
_REASON_PINNED_NOT_DICT: Final[str] = "pinned_hash_not_dict"
_REASON_PINNED_FIELD_MISSING: Final[str] = "pinned_router_yaml_sha3_512_missing_or_empty"
_REASON_MANIFEST_READER_RAISED: Final[str] = "external_manifest_reader_raised"
_REASON_MANIFEST_NOT_DICT: Final[str] = "external_manifest_not_dict"
_REASON_MANIFEST_CHAIN_HEAD_MISSING: Final[str] = "manifest_chain_head_hash_missing_or_empty"
_REASON_MANIFEST_SIGNATURE_NOT_BYTES: Final[str] = "manifest_signature_not_bytes"
_REASON_MANIFEST_PAYLOAD_NOT_BYTES: Final[str] = "manifest_signed_payload_bytes_not_bytes"
_REASON_MANIFEST_PRIOR_NOT_STR: Final[str] = "manifest_prior_chain_head_hash_not_str"
_REASON_PUBLIC_KEY_NOT_BYTES: Final[str] = "public_key_not_bytes"
_REASON_SIGNATURE_VERIFY_RAISED: Final[str] = "signature_verify_raised"
_REASON_PRIOR_READER_RAISED: Final[str] = "prior_chain_head_reader_raised"
_REASON_PRIOR_RETURN_INVALID: Final[str] = "prior_chain_head_return_invalid"
_REASON_PAIR_MISMATCH: Final[str] = "live_hash_mismatches_pinned"
_REASON_EXTERNAL_MISMATCH: Final[str] = "manifest_chain_head_mismatches_live"
_REASON_SIGNATURE_INVALID: Final[str] = "signature_verify_returned_false"
_REASON_CHAIN_BREAK_BOOTSTRAP_NONEMPTY: Final[str] = "bootstrap_prior_chain_head_hash_nonempty"
_REASON_CHAIN_BREAK_MISMATCH: Final[str] = "prior_chain_head_hash_mismatches_prior_reader"


@dataclass(frozen=True, kw_only=True)
class RouterIntegrityDetail:
    """Structured failure / pass record.

    ``reason_tag`` is always populated. ``check_failed`` is one of
    ``"pair"``, ``"external"``, ``"signature"``, ``"chain_break"``,
    ``"reader_fail"``, or an empty string on PASS. ``reader_error`` is
    non-empty only for fail-closed reader/verifier exceptions.
    """

    reason_tag: str
    check_failed: str
    reader_error: Optional[str]
    live_hash: str
    pinned_hash: str
    manifest_chain_head: str


@dataclass(frozen=True, kw_only=True)
class RouterIntegrityResult:
    success: bool
    failure_code: Optional[str]
    detail: Optional[RouterIntegrityDetail]


def _clip_error(exc: BaseException) -> str:
    """Produce a ≤500-char error tag for ``reader_error`` records."""

    return f"{type(exc).__name__}: {exc}"[:500]


def _fail(
    *,
    failure_code: str,
    reason_tag: str,
    check_failed: str,
    live_hash: str = "",
    pinned_hash: str = "",
    manifest_chain_head: str = "",
    reader_error: Optional[str] = None,
) -> RouterIntegrityResult:
    return RouterIntegrityResult(
        success=False,
        failure_code=failure_code,
        detail=RouterIntegrityDetail(
            reason_tag=reason_tag,
            check_failed=check_failed,
            reader_error=reader_error,
            live_hash=live_hash,
            pinned_hash=pinned_hash,
            manifest_chain_head=manifest_chain_head,
        ),
    )


def _ok(*, live_hash: str, pinned_hash: str, manifest_chain_head: str) -> RouterIntegrityResult:
    return RouterIntegrityResult(
        success=True,
        failure_code=None,
        detail=RouterIntegrityDetail(
            reason_tag="ok",
            check_failed="",
            reader_error=None,
            live_hash=live_hash,
            pinned_hash=pinned_hash,
            manifest_chain_head=manifest_chain_head,
        ),
    )


def check_router_integrity_multi_source(
    *,
    router_yaml_reader: RouterYamlReaderCallable,
    pinned_hash_reader: PinnedHashReaderCallable,
    external_manifest_reader: ExternalManifestReaderCallable,
    prior_chain_head_reader: PriorChainHeadReaderCallable,
    signature_verify: SignatureVerifyCallable,
    hash_bytes: HashBytesCallable,
    public_key: bytes,
) -> RouterIntegrityResult:
    """PRE-gate F-ROUTER-INTEGRITY-MULTI-SOURCE (F-AMDT-10).

    Verifies three-source agreement on a router.yaml promotion:
    (1) live file hash, (2) pinned hash, (3) external HMAC-chained
    manifest with Ed25519 signature and chain continuity.
    """

    if not isinstance(public_key, bytes):
        return _fail(
            failure_code=F_AMDT_10_READER_FAIL,
            reason_tag=_REASON_PUBLIC_KEY_NOT_BYTES,
            check_failed=_CHECK_READER_FAIL,
        )

    # Source 1 — router.yaml bytes + live hash
    try:
        yaml_bytes = router_yaml_reader()
    except Exception as exc:
        return _fail(
            failure_code=F_AMDT_10_READER_FAIL,
            reason_tag=_REASON_ROUTER_YAML_READER_RAISED,
            check_failed=_CHECK_READER_FAIL,
            reader_error=f"router_yaml_reader: {_clip_error(exc)}",
        )
    if not isinstance(yaml_bytes, bytes):
        return _fail(
            failure_code=F_AMDT_10_READER_FAIL,
            reason_tag=_REASON_ROUTER_YAML_NOT_BYTES,
            check_failed=_CHECK_READER_FAIL,
        )

    try:
        live_hash = hash_bytes(yaml_bytes)
    except Exception as exc:
        return _fail(
            failure_code=F_AMDT_10_READER_FAIL,
            reason_tag=_REASON_HASH_BYTES_RAISED,
            check_failed=_CHECK_READER_FAIL,
            reader_error=f"hash_bytes: {_clip_error(exc)}",
        )
    if not isinstance(live_hash, str):
        return _fail(
            failure_code=F_AMDT_10_READER_FAIL,
            reason_tag=_REASON_LIVE_HASH_NOT_STR,
            check_failed=_CHECK_READER_FAIL,
        )
    if live_hash == "":
        return _fail(
            failure_code=F_AMDT_10_READER_FAIL,
            reason_tag=_REASON_LIVE_HASH_EMPTY,
            check_failed=_CHECK_READER_FAIL,
        )

    # Source 2 — pinned hash record
    try:
        pinned = pinned_hash_reader()
    except Exception as exc:
        return _fail(
            failure_code=F_AMDT_10_READER_FAIL,
            reason_tag=_REASON_PINNED_READER_RAISED,
            check_failed=_CHECK_READER_FAIL,
            live_hash=live_hash,
            reader_error=f"pinned_hash_reader: {_clip_error(exc)}",
        )
    if not isinstance(pinned, dict):
        return _fail(
            failure_code=F_AMDT_10_READER_FAIL,
            reason_tag=_REASON_PINNED_NOT_DICT,
            check_failed=_CHECK_READER_FAIL,
            live_hash=live_hash,
        )
    raw_pinned = pinned.get("router_yaml_sha3_512")
    if not isinstance(raw_pinned, str) or raw_pinned == "":
        return _fail(
            failure_code=F_AMDT_10_READER_FAIL,
            reason_tag=_REASON_PINNED_FIELD_MISSING,
            check_failed=_CHECK_READER_FAIL,
            live_hash=live_hash,
        )
    pinned_hash: str = raw_pinned

    # Source 3 — external manifest
    try:
        manifest = external_manifest_reader()
    except Exception as exc:
        return _fail(
            failure_code=F_AMDT_10_READER_FAIL,
            reason_tag=_REASON_MANIFEST_READER_RAISED,
            check_failed=_CHECK_READER_FAIL,
            live_hash=live_hash,
            pinned_hash=pinned_hash,
            reader_error=f"external_manifest_reader: {_clip_error(exc)}",
        )
    if not isinstance(manifest, dict):
        return _fail(
            failure_code=F_AMDT_10_READER_FAIL,
            reason_tag=_REASON_MANIFEST_NOT_DICT,
            check_failed=_CHECK_READER_FAIL,
            live_hash=live_hash,
            pinned_hash=pinned_hash,
        )
    raw_head = manifest.get("chain_head_hash")
    if not isinstance(raw_head, str) or raw_head == "":
        return _fail(
            failure_code=F_AMDT_10_READER_FAIL,
            reason_tag=_REASON_MANIFEST_CHAIN_HEAD_MISSING,
            check_failed=_CHECK_READER_FAIL,
            live_hash=live_hash,
            pinned_hash=pinned_hash,
        )
    manifest_head: str = raw_head
    raw_sig = manifest.get("signature")
    if not isinstance(raw_sig, bytes):
        return _fail(
            failure_code=F_AMDT_10_READER_FAIL,
            reason_tag=_REASON_MANIFEST_SIGNATURE_NOT_BYTES,
            check_failed=_CHECK_READER_FAIL,
            live_hash=live_hash,
            pinned_hash=pinned_hash,
            manifest_chain_head=manifest_head,
        )
    raw_payload = manifest.get("signed_payload_bytes")
    if not isinstance(raw_payload, bytes):
        return _fail(
            failure_code=F_AMDT_10_READER_FAIL,
            reason_tag=_REASON_MANIFEST_PAYLOAD_NOT_BYTES,
            check_failed=_CHECK_READER_FAIL,
            live_hash=live_hash,
            pinned_hash=pinned_hash,
            manifest_chain_head=manifest_head,
        )
    raw_prior = manifest.get("prior_chain_head_hash")
    if not isinstance(raw_prior, str):
        return _fail(
            failure_code=F_AMDT_10_READER_FAIL,
            reason_tag=_REASON_MANIFEST_PRIOR_NOT_STR,
            check_failed=_CHECK_READER_FAIL,
            live_hash=live_hash,
            pinned_hash=pinned_hash,
            manifest_chain_head=manifest_head,
        )
    manifest_prior: str = raw_prior

    # Check 1 — pair (live == pinned)
    if live_hash != pinned_hash:
        return _fail(
            failure_code=F_AMDT_10_PAIR,
            reason_tag=_REASON_PAIR_MISMATCH,
            check_failed=_CHECK_PAIR,
            live_hash=live_hash,
            pinned_hash=pinned_hash,
            manifest_chain_head=manifest_head,
        )

    # Check 2 — external (manifest head == live)
    if manifest_head != live_hash:
        return _fail(
            failure_code=F_AMDT_10_EXTERNAL,
            reason_tag=_REASON_EXTERNAL_MISMATCH,
            check_failed=_CHECK_EXTERNAL,
            live_hash=live_hash,
            pinned_hash=pinned_hash,
            manifest_chain_head=manifest_head,
        )

    # Check 3 — signature (strict is True)
    try:
        sig_raw = signature_verify(raw_payload, raw_sig, public_key)
    except Exception as exc:
        return _fail(
            failure_code=F_AMDT_10_READER_FAIL,
            reason_tag=_REASON_SIGNATURE_VERIFY_RAISED,
            check_failed=_CHECK_READER_FAIL,
            live_hash=live_hash,
            pinned_hash=pinned_hash,
            manifest_chain_head=manifest_head,
            reader_error=f"signature_verify: {_clip_error(exc)}",
        )
    if sig_raw is not True:
        return _fail(
            failure_code=F_AMDT_10_SIGNATURE,
            reason_tag=_REASON_SIGNATURE_INVALID,
            check_failed=_CHECK_SIGNATURE,
            live_hash=live_hash,
            pinned_hash=pinned_hash,
            manifest_chain_head=manifest_head,
        )

    # Check 4 — chain continuity (head-to-prior)
    try:
        prior_head = prior_chain_head_reader()
    except Exception as exc:
        return _fail(
            failure_code=F_AMDT_10_READER_FAIL,
            reason_tag=_REASON_PRIOR_READER_RAISED,
            check_failed=_CHECK_READER_FAIL,
            live_hash=live_hash,
            pinned_hash=pinned_hash,
            manifest_chain_head=manifest_head,
            reader_error=f"prior_chain_head_reader: {_clip_error(exc)}",
        )
    if prior_head is None:
        if manifest_prior != "":
            return _fail(
                failure_code=F_AMDT_10_CHAIN_BREAK,
                reason_tag=_REASON_CHAIN_BREAK_BOOTSTRAP_NONEMPTY,
                check_failed=_CHECK_CHAIN_BREAK,
                live_hash=live_hash,
                pinned_hash=pinned_hash,
                manifest_chain_head=manifest_head,
            )
    elif not isinstance(prior_head, str):
        return _fail(
            failure_code=F_AMDT_10_READER_FAIL,
            reason_tag=_REASON_PRIOR_RETURN_INVALID,
            check_failed=_CHECK_READER_FAIL,
            live_hash=live_hash,
            pinned_hash=pinned_hash,
            manifest_chain_head=manifest_head,
        )
    elif manifest_prior != prior_head:
        return _fail(
            failure_code=F_AMDT_10_CHAIN_BREAK,
            reason_tag=_REASON_CHAIN_BREAK_MISMATCH,
            check_failed=_CHECK_CHAIN_BREAK,
            live_hash=live_hash,
            pinned_hash=pinned_hash,
            manifest_chain_head=manifest_head,
        )

    return _ok(
        live_hash=live_hash,
        pinned_hash=pinned_hash,
        manifest_chain_head=manifest_head,
    )
