"""BT9 conversation-log primitives + USER_DATA anchor verifier. [§2.5 + §4.6.4]

Append-only signed log of conversation utterances per session. Each entry is
SHA3-512 hash-chained from genesis (``prev_entry_hash = "0" * 128``) and signed
by Logician's BT6-rotated session key.

Round 4 ships pure-function primitives only:

* ``ConversationLogEntry`` frozen kw_only dataclass (§2.5).
* Canonical-bytes / hash / serialise / parse helpers.
* ``verify_chain(entries) -> ChainVerifyResult`` — walks forward from genesis,
  detecting chain breaks (``F-BT9-01``), append-races (``F-BT9-03``), and
  hash recomputation mismatches.
* ``build_appended_entry(...)`` — pure constructor that takes a signer
  callable, threads ``prev_entry_hash``, computes ``entry_hash``, and signs
  the canonical body.
* ``verify_user_data_anchor(...)`` — §4.6.4 four-step verifier returning a
  frozen ``AnchorVerifyResult``. Signature math is delegated to a
  ``SessionKeyVerifier`` Protocol per E-017 (injected callable pattern); the
  module itself has zero coupling to Section 1's BT6 catalog or Section 2's
  ``vault_read``.

Round 6 capstone wires this into §4.4.1 step 4 POST-gate after
``vault_read(intent="conversation-log-verify-read")`` loads the cited file.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Optional, Protocol, runtime_checkable


# ---------------------------------------------------------------------------
# Failure-code constants (§6.2 / §6.4)
# ---------------------------------------------------------------------------


F_BT9_01: str = "F-BT9-01"  # chain_break
F_BT9_02: str = "F-BT9-02"  # session_key_retired (INFO — BT6 rotation audit)
F_BT9_03: str = "F-BT9-03"  # append_race

F_POST_05_INVALID: str = "F-POST-05.conversation_anchor_invalid"
F_POST_05_MISSING_ENTRY: str = "F-POST-05.conversation_anchor_missing_entry"
F_POST_05_SUPERSEDED: str = "F-POST-05.conversation_anchor_superseded"
F_POST_05_WRONG_KEY: str = "F-POST-05.conversation_anchor_wrong_key"


VALID_SPEAKERS: frozenset[str] = frozenset(
    {"operator", "scribe", "scout", "editor", "judge", "logician"}
)

GENESIS_PREV_HASH: str = "0" * 128
_SHA3_HEX_LEN: int = 128


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class ConversationLogChainBroken(RuntimeError):
    """Raised when the on-disk chain fails recomputation. Code: F-BT9-01."""

    code: str = F_BT9_01

    def __init__(self, detail: str) -> None:
        super().__init__(detail)
        self.detail: str = detail


class ConversationLogAppendRace(RuntimeError):
    """Raised when two entries share a ``seq_id`` (concurrent append). F-BT9-03."""

    code: str = F_BT9_03

    def __init__(self, detail: str) -> None:
        super().__init__(detail)
        self.detail: str = detail


# ---------------------------------------------------------------------------
# Frozen dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class ConversationLogEntry:
    """USER_DATA trust-root anchor (§2.5)."""

    seq_id: int
    utc_timestamp: str
    session_id: str
    org_slug: str
    speaker: str
    content: str
    content_hash: str
    prev_entry_hash: str
    entry_hash: str
    session_key_signature: bytes
    corrects: Optional[str] = None  # entry_hash of superseded entry, per §4.6.4 step 4


@dataclass(frozen=True, kw_only=True)
class ChainVerifyResult:
    """Result of walking the on-disk chain forward from genesis."""

    chain_intact: bool
    head_seq_id: Optional[int]
    failure_code: Optional[str]
    failure_detail: str


@dataclass(frozen=True, kw_only=True)
class AnchorVerifyResult:
    """§4.6.4 verifier outcome for a USER_DATA claim."""

    tag: str  # "USER_DATA" | "UNSOURCED"
    verify_result: str  # "PASS" | "FAIL"
    verify_method: str  # "conversation_anchor" | "unresolved"
    verify_detail: str
    matched_seq_id: Optional[int]
    matched_entry_hash: Optional[str]
    failure_code: Optional[str]


# ---------------------------------------------------------------------------
# SessionKeyVerifier Protocol (E-017 injected-callable pattern)
# ---------------------------------------------------------------------------


@runtime_checkable
class SessionKeyVerifier(Protocol):
    """Resolves ``ConversationLogEntry.session_key_signature`` to a status.

    Returns one of:

    * ``"ACTIVE"`` — entry signed by a key in the current session's BT6
      catalog (signature math also passes). Anchor verify proceeds.
    * ``"RETIRED"`` — entry signed by a key that was active earlier in the
      current session and has since rotated (BT6). Treated as PASS for the
      anchor (the key was active during the session) but Round 6 capstone
      may emit ``F-BT9-02`` as an INFO/audit signal.
    * ``"WRONG_KEY"`` — signed by a key not in the current session's
      catalog. Maps to ``F-POST-05.conversation_anchor_wrong_key``.
    * ``"INVALID"`` — signature math fails. Maps to
      ``F-POST-05.conversation_anchor_invalid``.
    """

    def verify_entry(self, entry: ConversationLogEntry) -> str: ...


# ---------------------------------------------------------------------------
# Hash + canonical helpers
# ---------------------------------------------------------------------------


def compute_content_hash(content: str) -> str:
    """SHA3-512 hex digest of ``content.encode("utf-8")`` (128 hex chars)."""

    if not isinstance(content, str):
        raise TypeError(f"content must be str, got {type(content).__name__}")
    return hashlib.sha3_512(content.encode("utf-8")).hexdigest()


def _entry_canonical_bytes(
    *,
    seq_id: int,
    utc_timestamp: str,
    session_id: str,
    org_slug: str,
    speaker: str,
    content_hash: str,
    prev_entry_hash: str,
    corrects: Optional[str],
) -> bytes:
    """Canonical-JSON bytes used to compute ``entry_hash``.

    The entry_hash is computed over the body BEFORE entry_hash and
    session_key_signature are filled in, per the convention used elsewhere
    in §4 (admin_risk ledger, claim-evidence map).
    """

    body = {
        "seq_id": int(seq_id),
        "utc_timestamp": utc_timestamp,
        "session_id": session_id,
        "org_slug": org_slug,
        "speaker": speaker,
        "content_hash": content_hash,
        "prev_entry_hash": prev_entry_hash,
        "corrects": corrects,
    }
    return json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")


def compute_entry_hash(
    *,
    seq_id: int,
    utc_timestamp: str,
    session_id: str,
    org_slug: str,
    speaker: str,
    content_hash: str,
    prev_entry_hash: str,
    corrects: Optional[str] = None,
) -> str:
    """SHA3-512 hex over the canonical body (excludes entry_hash + signature)."""

    return hashlib.sha3_512(
        _entry_canonical_bytes(
            seq_id=seq_id,
            utc_timestamp=utc_timestamp,
            session_id=session_id,
            org_slug=org_slug,
            speaker=speaker,
            content_hash=content_hash,
            prev_entry_hash=prev_entry_hash,
            corrects=corrects,
        )
    ).hexdigest()


def signing_payload(entry: ConversationLogEntry) -> bytes:
    """Bytes the session-key signer should HMAC over.

    Composed of the canonical body (matches what entry_hash hashes) PLUS the
    entry_hash itself. This binds the signature to the chain position.
    """

    body = _entry_canonical_bytes(
        seq_id=entry.seq_id,
        utc_timestamp=entry.utc_timestamp,
        session_id=entry.session_id,
        org_slug=entry.org_slug,
        speaker=entry.speaker,
        content_hash=entry.content_hash,
        prev_entry_hash=entry.prev_entry_hash,
        corrects=entry.corrects,
    )
    return body + b"|" + entry.entry_hash.encode("ascii")


# ---------------------------------------------------------------------------
# Serialisation
# ---------------------------------------------------------------------------


def serialise_entry_line(entry: ConversationLogEntry) -> str:
    """Canonical-JSON line representation (newline-terminated).

    Stored format on disk under
    ``orgs/{slug}/vault/conversations/{session_id}.jsonl``.
    """

    payload = {
        "seq_id": int(entry.seq_id),
        "utc_timestamp": entry.utc_timestamp,
        "session_id": entry.session_id,
        "org_slug": entry.org_slug,
        "speaker": entry.speaker,
        "content": entry.content,
        "content_hash": entry.content_hash,
        "prev_entry_hash": entry.prev_entry_hash,
        "entry_hash": entry.entry_hash,
        "session_key_signature": entry.session_key_signature.hex(),
        "corrects": entry.corrects,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"


def parse_entry_line(line: str) -> ConversationLogEntry:
    """Round-trip companion to :func:`serialise_entry_line`."""

    if not isinstance(line, str):
        raise TypeError(f"line must be str, got {type(line).__name__}")
    obj = json.loads(line)
    return ConversationLogEntry(
        seq_id=int(obj["seq_id"]),
        utc_timestamp=str(obj["utc_timestamp"]),
        session_id=str(obj["session_id"]),
        org_slug=str(obj["org_slug"]),
        speaker=str(obj["speaker"]),
        content=str(obj["content"]),
        content_hash=str(obj["content_hash"]),
        prev_entry_hash=str(obj["prev_entry_hash"]),
        entry_hash=str(obj["entry_hash"]),
        session_key_signature=bytes.fromhex(obj["session_key_signature"]),
        corrects=(None if obj.get("corrects") is None else str(obj["corrects"])),
    )


def parse_log_text(text: str) -> tuple[ConversationLogEntry, ...]:
    """Parse a JSONL conversation log into a tuple of entries (in file order)."""

    if not isinstance(text, str):
        raise TypeError(f"text must be str, got {type(text).__name__}")
    if not text.strip():
        return ()
    entries: list[ConversationLogEntry] = []
    for raw in text.splitlines():
        if not raw.strip():
            continue
        entries.append(parse_entry_line(raw))
    return tuple(entries)


# ---------------------------------------------------------------------------
# Chain verification (forward walk from genesis)
# ---------------------------------------------------------------------------


def verify_chain(
    entries: tuple[ConversationLogEntry, ...] | list[ConversationLogEntry],
) -> ChainVerifyResult:
    """Walk forward from genesis, asserting per-entry hash + chain invariants.

    Returns a frozen :class:`ChainVerifyResult` carrying ``chain_intact``,
    the head ``seq_id`` (or ``None`` if zero entries / break before any
    valid head), and a failure code from :data:`F_BT9_01` / :data:`F_BT9_03`
    when relevant.
    """

    seq_seen: set[int] = set()
    expected_seq = 1
    expected_prev = GENESIS_PREV_HASH
    head_seq_id: Optional[int] = None

    for idx, entry in enumerate(entries):
        if not isinstance(entry, ConversationLogEntry):
            return ChainVerifyResult(
                chain_intact=False,
                head_seq_id=head_seq_id,
                failure_code=F_BT9_01,
                failure_detail=f"entry[{idx}] is not ConversationLogEntry",
            )
        if entry.seq_id in seq_seen:
            return ChainVerifyResult(
                chain_intact=False,
                head_seq_id=head_seq_id,
                failure_code=F_BT9_03,
                failure_detail=f"replayed seq_id {entry.seq_id} at index {idx}",
            )
        if entry.seq_id != expected_seq:
            return ChainVerifyResult(
                chain_intact=False,
                head_seq_id=head_seq_id,
                failure_code=F_BT9_01,
                failure_detail=(
                    f"seq_id gap at index {idx}: expected {expected_seq}, "
                    f"got {entry.seq_id}"
                ),
            )
        if entry.prev_entry_hash != expected_prev:
            return ChainVerifyResult(
                chain_intact=False,
                head_seq_id=head_seq_id,
                failure_code=F_BT9_01,
                failure_detail=(
                    f"prev_entry_hash mismatch at seq_id {entry.seq_id}"
                ),
            )
        recomputed = compute_entry_hash(
            seq_id=entry.seq_id,
            utc_timestamp=entry.utc_timestamp,
            session_id=entry.session_id,
            org_slug=entry.org_slug,
            speaker=entry.speaker,
            content_hash=entry.content_hash,
            prev_entry_hash=entry.prev_entry_hash,
            corrects=entry.corrects,
        )
        if recomputed != entry.entry_hash:
            return ChainVerifyResult(
                chain_intact=False,
                head_seq_id=head_seq_id,
                failure_code=F_BT9_01,
                failure_detail=(
                    f"entry_hash recompute mismatch at seq_id {entry.seq_id}"
                ),
            )
        if entry.content_hash != compute_content_hash(entry.content):
            return ChainVerifyResult(
                chain_intact=False,
                head_seq_id=head_seq_id,
                failure_code=F_BT9_01,
                failure_detail=(
                    f"content_hash mismatch at seq_id {entry.seq_id}"
                ),
            )

        seq_seen.add(entry.seq_id)
        head_seq_id = entry.seq_id
        expected_prev = entry.entry_hash
        expected_seq += 1

    return ChainVerifyResult(
        chain_intact=True,
        head_seq_id=head_seq_id,
        failure_code=None,
        failure_detail="",
    )


# ---------------------------------------------------------------------------
# Append (pure)
# ---------------------------------------------------------------------------


def build_appended_entry(
    *,
    prior_entries: tuple[ConversationLogEntry, ...] | list[ConversationLogEntry],
    utc_timestamp: str,
    session_id: str,
    org_slug: str,
    speaker: str,
    content: str,
    signer,  # callable: bytes -> bytes
    corrects: Optional[str] = None,
) -> ConversationLogEntry:
    """Construct the next signed entry given prior entries + a signer callable.

    The ``signer`` receives :func:`signing_payload`'s bytes and must return
    the HMAC signature bytes. No filesystem I/O — Round 6 capstone wires
    this into ``vault_write(intent="conversation-append")``.
    """

    if speaker not in VALID_SPEAKERS:
        raise ValueError(
            f"speaker must be one of {sorted(VALID_SPEAKERS)}, got {speaker!r}"
        )
    if not isinstance(content, str):
        raise TypeError(f"content must be str, got {type(content).__name__}")
    if not callable(signer):
        raise TypeError("signer must be a callable bytes -> bytes")

    if not prior_entries:
        seq_id = 1
        prev_entry_hash = GENESIS_PREV_HASH
    else:
        last = prior_entries[-1]
        seq_id = last.seq_id + 1
        prev_entry_hash = last.entry_hash

    content_hash = compute_content_hash(content)
    entry_hash = compute_entry_hash(
        seq_id=seq_id,
        utc_timestamp=utc_timestamp,
        session_id=session_id,
        org_slug=org_slug,
        speaker=speaker,
        content_hash=content_hash,
        prev_entry_hash=prev_entry_hash,
        corrects=corrects,
    )

    unsigned = ConversationLogEntry(
        seq_id=seq_id,
        utc_timestamp=utc_timestamp,
        session_id=session_id,
        org_slug=org_slug,
        speaker=speaker,
        content=content,
        content_hash=content_hash,
        prev_entry_hash=prev_entry_hash,
        entry_hash=entry_hash,
        session_key_signature=b"",
        corrects=corrects,
    )
    signature = signer(signing_payload(unsigned))
    if not isinstance(signature, (bytes, bytearray)):
        raise TypeError(
            f"signer must return bytes, got {type(signature).__name__}"
        )

    return ConversationLogEntry(
        seq_id=seq_id,
        utc_timestamp=utc_timestamp,
        session_id=session_id,
        org_slug=org_slug,
        speaker=speaker,
        content=content,
        content_hash=content_hash,
        prev_entry_hash=prev_entry_hash,
        entry_hash=entry_hash,
        session_key_signature=bytes(signature),
        corrects=corrects,
    )


# ---------------------------------------------------------------------------
# §4.6.4 USER_DATA anchor verifier
# ---------------------------------------------------------------------------


def _find_anchor_entry(
    entries: tuple[ConversationLogEntry, ...],
    *,
    claim_text: str,
    case_sensitive: bool,
) -> Optional[ConversationLogEntry]:
    """Return the first entry whose ``content`` contains ``claim_text``."""

    if case_sensitive:
        for entry in entries:
            if claim_text in entry.content:
                return entry
        return None
    needle = claim_text.lower()
    for entry in entries:
        if needle in entry.content.lower():
            return entry
    return None


def _is_superseded(
    entries: tuple[ConversationLogEntry, ...],
    *,
    anchor_index: int,
    anchor_entry_hash: str,
) -> bool:
    """True iff any later entry has ``corrects == anchor_entry_hash``."""

    for entry in entries[anchor_index + 1 :]:
        if entry.corrects == anchor_entry_hash:
            return True
    return False


def verify_user_data_anchor(
    *,
    claim_text: str,
    log_text: str,
    expected_session_id: str,
    expected_org_slug: str,
    signature_verifier: SessionKeyVerifier,
    case_sensitive: bool = True,
) -> AnchorVerifyResult:
    """§4.6.4 four-step USER_DATA anchor verifier.

    Steps:

    1. Parse the log and verify chain integrity (``F-BT9-01`` / ``F-BT9-03``
       on break → fail with :data:`F_POST_05_INVALID`).
    2. Locate the entry whose ``content`` contains ``claim_text`` as a
       substring (case sensitivity per ``case_sensitive`` kwarg). Miss →
       :data:`F_POST_05_MISSING_ENTRY`.
    3. Resolve the entry's ``session_key_signature`` via
       ``signature_verifier``. ``WRONG_KEY`` → :data:`F_POST_05_WRONG_KEY`.
       ``INVALID`` → :data:`F_POST_05_INVALID`.
    4. Reject if any later entry's ``corrects`` field points at the
       anchor's ``entry_hash`` → :data:`F_POST_05_SUPERSEDED`.
    """

    if not isinstance(claim_text, str):
        raise TypeError(
            f"claim_text must be str, got {type(claim_text).__name__}"
        )
    if not isinstance(log_text, str):
        raise TypeError(
            f"log_text must be str, got {type(log_text).__name__}"
        )
    if not isinstance(expected_session_id, str):
        raise TypeError("expected_session_id must be str")
    if not isinstance(expected_org_slug, str):
        raise TypeError("expected_org_slug must be str")

    entries = parse_log_text(log_text)
    if not entries:
        return AnchorVerifyResult(
            tag="UNSOURCED",
            verify_result="FAIL",
            verify_method="unresolved",
            verify_detail="conversation log is empty",
            matched_seq_id=None,
            matched_entry_hash=None,
            failure_code=F_POST_05_MISSING_ENTRY,
        )

    chain_result = verify_chain(entries)
    if not chain_result.chain_intact:
        return AnchorVerifyResult(
            tag="UNSOURCED",
            verify_result="FAIL",
            verify_method="unresolved",
            verify_detail=(
                f"chain verify failed ({chain_result.failure_code}): "
                f"{chain_result.failure_detail}"
            ),
            matched_seq_id=None,
            matched_entry_hash=None,
            failure_code=F_POST_05_INVALID,
        )

    # Reject log whose entries do not match the expected session + org.
    for entry in entries:
        if entry.session_id != expected_session_id:
            return AnchorVerifyResult(
                tag="UNSOURCED",
                verify_result="FAIL",
                verify_method="unresolved",
                verify_detail=(
                    f"entry seq_id {entry.seq_id} session_id "
                    f"{entry.session_id!r} != expected "
                    f"{expected_session_id!r}"
                ),
                matched_seq_id=None,
                matched_entry_hash=None,
                failure_code=F_POST_05_INVALID,
            )
        if entry.org_slug != expected_org_slug:
            return AnchorVerifyResult(
                tag="UNSOURCED",
                verify_result="FAIL",
                verify_method="unresolved",
                verify_detail=(
                    f"entry seq_id {entry.seq_id} org_slug "
                    f"{entry.org_slug!r} != expected "
                    f"{expected_org_slug!r}"
                ),
                matched_seq_id=None,
                matched_entry_hash=None,
                failure_code=F_POST_05_INVALID,
            )

    anchor = _find_anchor_entry(
        entries, claim_text=claim_text, case_sensitive=case_sensitive
    )
    if anchor is None:
        return AnchorVerifyResult(
            tag="UNSOURCED",
            verify_result="FAIL",
            verify_method="unresolved",
            verify_detail="no log entry contains claim_text as substring",
            matched_seq_id=None,
            matched_entry_hash=None,
            failure_code=F_POST_05_MISSING_ENTRY,
        )

    sig_status = signature_verifier.verify_entry(anchor)
    if sig_status == "INVALID":
        return AnchorVerifyResult(
            tag="UNSOURCED",
            verify_result="FAIL",
            verify_method="unresolved",
            verify_detail=(
                f"session_key signature INVALID at seq_id {anchor.seq_id}"
            ),
            matched_seq_id=anchor.seq_id,
            matched_entry_hash=anchor.entry_hash,
            failure_code=F_POST_05_INVALID,
        )
    if sig_status == "WRONG_KEY":
        return AnchorVerifyResult(
            tag="UNSOURCED",
            verify_result="FAIL",
            verify_method="unresolved",
            verify_detail=(
                f"entry seq_id {anchor.seq_id} signed by key not active in "
                f"current session"
            ),
            matched_seq_id=anchor.seq_id,
            matched_entry_hash=anchor.entry_hash,
            failure_code=F_POST_05_WRONG_KEY,
        )
    if sig_status not in {"ACTIVE", "RETIRED"}:
        return AnchorVerifyResult(
            tag="UNSOURCED",
            verify_result="FAIL",
            verify_method="unresolved",
            verify_detail=(
                f"signature_verifier returned unknown status {sig_status!r}"
            ),
            matched_seq_id=anchor.seq_id,
            matched_entry_hash=anchor.entry_hash,
            failure_code=F_POST_05_INVALID,
        )

    anchor_index = entries.index(anchor)
    if _is_superseded(
        entries, anchor_index=anchor_index, anchor_entry_hash=anchor.entry_hash
    ):
        return AnchorVerifyResult(
            tag="UNSOURCED",
            verify_result="FAIL",
            verify_method="unresolved",
            verify_detail=(
                f"entry seq_id {anchor.seq_id} superseded by later "
                f"entry with corrects={anchor.entry_hash}"
            ),
            matched_seq_id=anchor.seq_id,
            matched_entry_hash=anchor.entry_hash,
            failure_code=F_POST_05_SUPERSEDED,
        )

    detail = "anchor verified"
    if sig_status == "RETIRED":
        detail = "anchor verified (signing key BT6-retired — INFO F-BT9-02)"

    return AnchorVerifyResult(
        tag="USER_DATA",
        verify_result="PASS",
        verify_method="conversation_anchor",
        verify_detail=detail,
        matched_seq_id=anchor.seq_id,
        matched_entry_hash=anchor.entry_hash,
        failure_code=None,
    )


__all__ = [
    "F_BT9_01",
    "F_BT9_02",
    "F_BT9_03",
    "F_POST_05_INVALID",
    "F_POST_05_MISSING_ENTRY",
    "F_POST_05_SUPERSEDED",
    "F_POST_05_WRONG_KEY",
    "VALID_SPEAKERS",
    "GENESIS_PREV_HASH",
    "ConversationLogChainBroken",
    "ConversationLogAppendRace",
    "ConversationLogEntry",
    "ChainVerifyResult",
    "AnchorVerifyResult",
    "SessionKeyVerifier",
    "compute_content_hash",
    "compute_entry_hash",
    "signing_payload",
    "serialise_entry_line",
    "parse_entry_line",
    "parse_log_text",
    "verify_chain",
    "build_appended_entry",
    "verify_user_data_anchor",
]
