"""Shared runtime-checkable Protocols for §4 Logician v2.2 Wave 2 + Wave 3 gates.

Each gate in the wave-2 / wave-3 sets depends on one or more of the callables
defined here. Centralising them guarantees:

* A single canonical contract for readers across ``lock_history.v1.jsonl``,
  the daily-log stream, ``router.yaml``, audit-artifact JSON, rollback-script
  metadata, ledger-hash tip, and Ed25519 signature verification.
* Symmetric injection sites at the call layer — the gate_runner or pipeline
  orchestrator constructs one concrete implementation per reader and passes
  it into any gate that needs it.
* No direct file / YAML / JSON / crypto I/O inside gate code (AST-lint R3 is
  the module-load banner; these Protocols are the *only* sanctioned route).

All Protocols are ``@runtime_checkable`` so test doubles (plain callables or
lambdas matching the signature) pass ``isinstance()`` checks at the caller
layer. See E-017 (``project_impl_round_s_locked.md``) for the injected-
callable pattern that originated this style.

Blueprint anchor: ``pipeline/blueprint/v0.1/section_04_logician.md`` v2.1
(parent LOCK); v2.2 wave-2 delta rows for F-AMDT-01 / F-AMDT-06 /
F-AMDT-07 / F-AMDT-12; v2.2 wave-3 delta rows for F-AMDT-05 /
F-AMDT-08 / F-AMDT-09 / F-AMDT-10 / F-AMDT-11.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional, Protocol, runtime_checkable


# ---------------------------------------------------------------------------
# LockHistoryReaderCallable — gates #1 (F-AMDT-01), #12 (F-AMDT-12 via caller)
# ---------------------------------------------------------------------------


@runtime_checkable
class LockHistoryReaderCallable(Protocol):
    """Returns the full parsed contents of ``lock_history.v1.jsonl``.

    Each returned element is one row (a ``dict`` — the gate does not assume a
    more specific type and validates fields it consumes on read). The reader
    is responsible for any JSONL parsing, encoding, and malformed-line
    handling at the boundary. Raising from the reader is the fail-closed
    signal to consuming gates — a gate must DENY on reader exception rather
    than conflate "empty history" with "read failure".
    """

    def __call__(self) -> list[dict]: ...


# ---------------------------------------------------------------------------
# AuditArtifactReaderCallable — gate #6 (F-AMDT-06)
# ---------------------------------------------------------------------------


@runtime_checkable
class AuditArtifactReaderCallable(Protocol):
    """Reads and parses a cross-family audit artifact (markdown + JSON body).

    Returns a ``dict`` whose shape matches the EN-001 / EN-003 audit round
    convention: at minimum a top-level ``"red_team_verdict"`` key carrying
    the blocking flag + findings, and optionally a ``"cycle_fixes"`` list
    where each entry carries ``finding_id``, ``fix_description``,
    ``closure_evidence`` fields.

    Raising signals fail-closed to the gate; the gate does not distinguish
    between "not found" and "parse error" at this seam — both DENY.
    """

    def __call__(self, path: str) -> dict: ...


# ---------------------------------------------------------------------------
# FileExistsCallable — gate #6 (F-AMDT-06)
# ---------------------------------------------------------------------------


@runtime_checkable
class FileExistsCallable(Protocol):
    """Boolean existence check for a filesystem path.

    The gate does not call ``os.path.exists`` or ``pathlib.Path.exists``
    directly — the injected callable is the only sanctioned route. A ``True``
    return means the artifact is read-able by the subsequent reader; a
    ``False`` return is a clean DENY (no read attempted).
    """

    def __call__(self, path: str) -> bool: ...


# ---------------------------------------------------------------------------
# RouterConfigReaderCallable — gate #7 (F-AMDT-07 v1 + v1.1)
# ---------------------------------------------------------------------------


@runtime_checkable
class RouterConfigReaderCallable(Protocol):
    """Returns a pre-digested family-name view of ``router.yaml``.

    The gate does NOT parse YAML. The caller constructs a plain ``dict`` with
    already-extracted family-name fields:

    ::

        {
          "judge_primary_family": "google",
          "code_reviewer_1": {"primary_family": "openai",
                               "fallback_family": "openai"},
          "code_reviewer_2": {"primary_family": "alibaba",
                               "fallback_family": "alibaba"},
          "code_reviewer_3": {"primary_family": "meta",
                               "fallback_family": "meta"},
          "code_reviewer_4": {"primary_family": "openai_oss",
                               "fallback_family": "openai_oss"},
          "code_reviewer_5": {"primary_family": "moonshot",
                               "fallback_family": "google"},
        }

    Family names are canonical lowercase strings. The gate enforces exact
    string equality — it does not case-fold or normalise Unicode.
    """

    def __call__(self) -> dict: ...


# ---------------------------------------------------------------------------
# DailyLogReaderCallable — gate #12 (F-AMDT-12)
# ---------------------------------------------------------------------------


@runtime_checkable
class DailyLogReaderCallable(Protocol):
    """Returns the text of ``daily_logs/{date_iso}.md`` or ``None``.

    ``None`` signals "file does not exist" — an explicit, fail-closed signal
    distinct from an empty string (which would mean a zero-byte log does
    exist). Raising is the fail-closed signal for read errors distinct from
    non-existence (permission denied, decode error).
    """

    def __call__(self, date_iso: str) -> Optional[str]: ...


# ---------------------------------------------------------------------------
# ClockProtocol — gate #12 (F-AMDT-12), shared forward with gates #8/#9/#11
# ---------------------------------------------------------------------------


@runtime_checkable
class ClockProtocol(Protocol):
    """Injected UTC clock. Gates never call ``datetime.now(UTC)`` directly."""

    def now_utc(self) -> datetime: ...


# ---------------------------------------------------------------------------
# SignatureVerifyCallable — gates #5 (F-AMDT-05), #10 (F-AMDT-10), #11 (F-AMDT-11)
# ---------------------------------------------------------------------------


@runtime_checkable
class SignatureVerifyCallable(Protocol):
    """Injected Ed25519 signature verifier.

    Signature contract: ``signature_verify(message_bytes, signature, public_key)``
    returns ``True`` when ``signature`` is a valid Ed25519 signature over
    ``message_bytes`` under ``public_key``, ``False`` otherwise.

    Gates never import ``cryptography``, ``nacl``, or any other crypto library
    directly — the injected callable is the only sanctioned route (E-011
    crypto-agility envelope; AST-lint R3 LOGICIAN_OPEN_BAN supplemented by
    R1 LOGICIAN_IMPORT_BAN on ``hashlib`` at gate load).

    A non-boolean return is treated as failure by the caller (gate applies
    strict ``is True`` identity on the returned value). Raising from the
    verifier is the fail-closed signal — the gate DENIES and records the
    exception class name in ``reader_error``.
    """

    def __call__(
        self,
        message_bytes: bytes,
        signature: bytes,
        public_key: bytes,
    ) -> bool: ...


# ---------------------------------------------------------------------------
# LedgerHashReaderCallable — gate #5 (F-AMDT-05)
# ---------------------------------------------------------------------------


@runtime_checkable
class LedgerHashReaderCallable(Protocol):
    """Returns the current HMAC-SHA3-512 hash at the ``lock_history.v1.jsonl``
    ledger head, as a lowercase hex string.

    The caller (gate_runner or pipeline orchestrator) materialises the ledger
    hash by walking the HMAC-chain over committed rows; the gate only
    consumes the tip. Empty-string return is permitted (degenerate case:
    empty ledger) and treated as a valid string by the gate; the pin
    comparison then succeeds only if the script was authored against an
    empty-ledger tip too. Raising is the fail-closed signal.
    """

    def __call__(self) -> str: ...


# ---------------------------------------------------------------------------
# ScriptMetadataReaderCallable — gate #5 (F-AMDT-05)
# ---------------------------------------------------------------------------


@runtime_checkable
class ScriptMetadataReaderCallable(Protocol):
    """Returns parsed metadata for a registered rollback script.

    At minimum the returned dict must carry ``ledger_hash_at_pin: str`` —
    the exact ledger-head hash the script was authored against. Additional
    fields (``author_timestamp_utc``, ``amendment_id``, etc.) are permitted
    but not consumed by the gate. Missing ``ledger_hash_at_pin`` is a DENY
    signal (structural contract failure).

    The reader is responsible for locating the metadata (sidecar ``.meta``
    file, central manifest row, etc.) — the gate never parses the script
    file itself. Raising is the fail-closed signal.
    """

    def __call__(self, script_path: str) -> dict: ...


# ---------------------------------------------------------------------------
# Router integrity Protocols — gate #10 (F-AMDT-10)
# ---------------------------------------------------------------------------


@runtime_checkable
class RouterYamlReaderCallable(Protocol):
    """Returns raw bytes of the current ``router.yaml`` file.

    The gate computes the live SHA3-512 hash of the return value via the
    injected :class:`HashBytesCallable` — it never parses YAML. Raising is
    the fail-closed signal.
    """

    def __call__(self) -> bytes: ...


@runtime_checkable
class PinnedHashReaderCallable(Protocol):
    """Returns parsed ``router_integrity.pinned.json`` content.

    At minimum the returned dict must carry ``router_yaml_sha3_512: str`` —
    the pinned hash of the last-known-good ``router.yaml``. Missing or
    non-string value is a DENY signal. Raising is the fail-closed signal.
    """

    def __call__(self) -> dict: ...


@runtime_checkable
class ExternalManifestReaderCallable(Protocol):
    """Returns the HMAC-chained router-integrity manifest head row.

    The returned dict must carry:

    * ``chain_head_hash: str`` — hash of the current router.yaml as recorded
      by the external manifest.
    * ``signature: bytes`` — Ed25519 signature over ``signed_payload_bytes``.
    * ``prior_chain_head_hash: str`` — pointer to the prior row's
      ``chain_head_hash`` (empty string ``""`` permitted only on the
      bootstrap row).
    * ``signed_payload_bytes: bytes`` — the exact bytes the signature
      covers. The manifest author is responsible for canonicalization; the
      gate does not re-canonicalize.

    The manifest file lives **outside the repo** (operator-controlled path)
    so a repo-write adversary cannot tamper with it. Raising is the
    fail-closed signal.
    """

    def __call__(self) -> dict: ...


@runtime_checkable
class PriorChainHeadReaderCallable(Protocol):
    """Returns the prior manifest row's ``chain_head_hash`` or ``None``.

    ``None`` signals "bootstrap row — no prior exists"; the gate then
    requires the current row's ``prior_chain_head_hash`` to be the empty
    string. A non-``None`` return must equal the current row's
    ``prior_chain_head_hash`` or the chain is broken (DENY
    ``F-AMDT-10-CHAIN-BREAK``). Raising is the fail-closed signal.
    """

    def __call__(self) -> Optional[str]: ...


# ---------------------------------------------------------------------------
# HashBytesCallable — gate #10 (F-AMDT-10)
# ---------------------------------------------------------------------------


@runtime_checkable
class HashBytesCallable(Protocol):
    """Injected SHA3-512 digest function.

    Gates never import ``hashlib`` (AST-lint R1 LOGICIAN_IMPORT_BAN). The
    injected callable returns a lowercase hex string. Raising is the
    fail-closed signal.
    """

    def __call__(self, data: bytes) -> str: ...


# ---------------------------------------------------------------------------
# StanzaReaderCallable — gate #11 (F-AMDT-11)
# ---------------------------------------------------------------------------


@runtime_checkable
class StanzaReaderCallable(Protocol):
    """Returns the F-AMDT-08 operator sign-off stanza text from the daily
    log for ``date_iso``, or ``None`` if no stanza is present.

    The reader is responsible for locating the stanza block inside the daily
    log markdown — the gate consumes raw stanza text and tokenises directive
    keywords inline. ``None`` signals "no stanza today" (clean no-op PASS
    for the stanza-check event). Raising is the fail-closed signal.
    """

    def __call__(self, date_iso: str) -> Optional[str]: ...


# ---------------------------------------------------------------------------
# Deprecation register + feed Protocols — gate #9 (F-AMDT-09)
# ---------------------------------------------------------------------------


@runtime_checkable
class DeprecationRegisterReaderCallable(Protocol):
    """Returns parsed rows of ``pipeline/vault_shared/deprecation_register.jsonl``.

    Each row is a ``dict`` with at minimum ``affected_model: str`` and one of
    ``deprecated: bool`` / ``not_deprecated: bool``. Current rows also carry
    ``registered_at_iso8601: str`` and optionally ``evidence_url: str``. The
    reader is responsible for JSONL parsing, encoding, and malformed-line
    handling at the boundary. Raising is the fail-closed signal.
    """

    def __call__(self) -> list[dict]: ...


@runtime_checkable
class DeprecationFeedReaderCallable(Protocol):
    """Returns the cached provider-announcement record for ``affected_model``,
    or ``None`` if the model is not in any cached feed.

    Return shape (when not ``None``):

    * ``announcement_iso8601: str`` — when the provider publicly announced
      the deprecation (UTC).
    * ``deprecation_effective_iso8601: str`` — when the deprecation takes
      effect (optional; falls back to announcement time).
    * ``source_url: str`` — permalink to the announcement (audit trail).

    The cache snapshot is produced out-of-band (feed-ingestion cron); the
    gate trusts it as presented. Raising is the fail-closed signal.
    """

    def __call__(self, affected_model: str) -> Optional[dict]: ...
