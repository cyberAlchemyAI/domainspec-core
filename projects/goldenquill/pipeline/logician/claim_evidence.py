"""Claim-evidence map dataclasses + canonical-JSON assembler. [§4.4 + §4.5]

This is the §4 Logician Round 2 floor: the frozen kw_only dataclasses
(`SourceRef`, `ClaimEntry`, `ClaimEvidenceMap`, `SignedClaimEvidenceMap`),
the canonical-byte-identical assembler (§7.5), and id/hash helpers.

The full BT10 grep-windowed verifier (§4.6) lands in Round 3; the S11c lock
verifier (§4.7) in Round 5; the gate-runner capstone that wires PRE-gate +
POST-gate + Cedar in Round 6. This module deliberately does NOT verify
sources or sign maps — that is Round 5/6 territory. It produces the artifact
shape and guarantees that a given (claim-tuple, metadata) pair always
canonicalises to the same bytes regardless of input order.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Iterable, Optional


# ---------------------------------------------------------------------------
# Pinned constants (blueprint §8.1)
# ---------------------------------------------------------------------------


GENERATOR_VERSION: str = "s4-v1"

TAGS: frozenset[str] = frozenset({"DOC_SOURCED", "USER_DATA", "UNSOURCED"})

SOURCE_KINDS: frozenset[str] = frozenset(
    {
        "RFA",
        "PROJECT_CONTEXT",
        "ENTITY_DOSSIER",
        "RUBRIC_LIBRARY",
        "LESSONS",
        "CONVERSATION_LOG",
    }
)

VERIFY_METHODS: frozenset[str] = frozenset(
    {
        "grep_windowed_pm2",
        "grep_windowed_pm5_fallback",
        "conversation_anchor",
        "unresolved",
    }
)

_ID_TRUNCATE: int = 24
_SHA3_HEX_LEN: int = 128


# ---------------------------------------------------------------------------
# Frozen dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class SourceRef:
    source_kind: str
    canonical_path: str
    inode: int
    content_hash: str
    grep_string: Optional[str]
    window_size_sentences: Optional[int]


@dataclass(frozen=True, kw_only=True)
class ClaimEntry:
    claim_id: str
    draft_offset: int
    claim_text: str
    tag: str
    source_ref: Optional[SourceRef]
    verify_method: str
    verify_result: str
    verify_detail: str
    rigor_breach_flag: bool


@dataclass(frozen=True, kw_only=True)
class ClaimEvidenceMap:
    map_id: str
    draft_hash: str
    rfa_hash: str
    session_id: str
    org_slug: str
    rfa_url_hash: str
    entries: tuple[ClaimEntry, ...]
    unsourced_count: int
    hard_block_count: int
    rigor_breach_active: bool
    generated_at_utc: str
    generator_version: str


@dataclass(frozen=True, kw_only=True)
class SignedClaimEvidenceMap:
    map: ClaimEvidenceMap
    content_hash: str
    signature: bytes
    operator_key_id: str
    signed_at_utc: str


# ---------------------------------------------------------------------------
# Id + hash helpers (sha3_512 truncated to 24 hex chars per §2.1)
# ---------------------------------------------------------------------------


def _canonical_json_bytes(obj: object) -> bytes:
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def compute_claim_id(*, draft_hash: str, draft_offset: int, claim_text: str) -> str:
    payload = {
        "draft_hash": draft_hash,
        "draft_offset": draft_offset,
        "claim_text": claim_text,
    }
    digest = hashlib.sha3_512(_canonical_json_bytes(payload)).hexdigest()
    return digest[:_ID_TRUNCATE]


def compute_map_id(*, draft_hash: str, rfa_hash: str, session_id: str) -> str:
    payload = {
        "draft_hash": draft_hash,
        "rfa_hash": rfa_hash,
        "session_id": session_id,
    }
    digest = hashlib.sha3_512(_canonical_json_bytes(payload)).hexdigest()
    return digest[:_ID_TRUNCATE]


# ---------------------------------------------------------------------------
# Assembler — §4.4.1 step 9
# ---------------------------------------------------------------------------


def _validate_claim(entry: ClaimEntry) -> None:
    if entry.tag not in TAGS:
        raise ValueError(f"unknown tag: {entry.tag!r}")
    if entry.verify_method not in VERIFY_METHODS:
        raise ValueError(f"unknown verify_method: {entry.verify_method!r}")
    if entry.tag == "UNSOURCED":
        if entry.source_ref is not None:
            raise ValueError(
                f"claim {entry.claim_id} tagged UNSOURCED must have source_ref=None"
            )
    else:
        if entry.source_ref is None:
            raise ValueError(
                f"claim {entry.claim_id} tagged {entry.tag} requires a source_ref"
            )
        if entry.source_ref.source_kind not in SOURCE_KINDS:
            raise ValueError(
                f"claim {entry.claim_id} source_kind {entry.source_ref.source_kind!r} unknown"
            )


def assemble_claim_evidence_map(
    *,
    draft_hash: str,
    rfa_hash: str,
    session_id: str,
    org_slug: str,
    rfa_url_hash: str,
    claims: tuple[ClaimEntry, ...],
    rigor_breach_active: bool,
    generated_at_utc: str,
    hard_block_count: int = 0,
) -> ClaimEvidenceMap:
    if not isinstance(claims, tuple):
        raise TypeError(
            f"claims must be a tuple of ClaimEntry, got {type(claims).__name__}"
        )
    for c in claims:
        if not isinstance(c, ClaimEntry):
            raise TypeError(f"claim must be ClaimEntry, got {type(c).__name__}")
        _validate_claim(c)
    if not isinstance(hard_block_count, int) or hard_block_count < 0:
        raise ValueError(f"hard_block_count must be non-negative int")

    sorted_entries = tuple(sorted(claims, key=lambda e: e.claim_id))
    unsourced_count = sum(1 for e in sorted_entries if e.tag == "UNSOURCED")
    map_id = compute_map_id(
        draft_hash=draft_hash, rfa_hash=rfa_hash, session_id=session_id
    )
    return ClaimEvidenceMap(
        map_id=map_id,
        draft_hash=draft_hash,
        rfa_hash=rfa_hash,
        session_id=session_id,
        org_slug=org_slug,
        rfa_url_hash=rfa_url_hash,
        entries=sorted_entries,
        unsourced_count=unsourced_count,
        hard_block_count=hard_block_count,
        rigor_breach_active=rigor_breach_active,
        generated_at_utc=generated_at_utc,
        generator_version=GENERATOR_VERSION,
    )


# ---------------------------------------------------------------------------
# Canonicalisation — §7.5 byte-identical
# ---------------------------------------------------------------------------


def _map_to_dict(m: ClaimEvidenceMap) -> dict:
    return {
        "map_id": m.map_id,
        "draft_hash": m.draft_hash,
        "rfa_hash": m.rfa_hash,
        "session_id": m.session_id,
        "org_slug": m.org_slug,
        "rfa_url_hash": m.rfa_url_hash,
        "entries": [_entry_to_dict(e) for e in m.entries],
        "unsourced_count": m.unsourced_count,
        "hard_block_count": m.hard_block_count,
        "rigor_breach_active": m.rigor_breach_active,
        "generated_at_utc": m.generated_at_utc,
        "generator_version": m.generator_version,
    }


def _entry_to_dict(e: ClaimEntry) -> dict:
    return {
        "claim_id": e.claim_id,
        "draft_offset": e.draft_offset,
        "claim_text": e.claim_text,
        "tag": e.tag,
        "source_ref": _source_ref_to_dict(e.source_ref) if e.source_ref else None,
        "verify_method": e.verify_method,
        "verify_result": e.verify_result,
        "verify_detail": e.verify_detail,
        "rigor_breach_flag": e.rigor_breach_flag,
    }


def _source_ref_to_dict(s: SourceRef) -> dict:
    return {
        "source_kind": s.source_kind,
        "canonical_path": s.canonical_path,
        "inode": s.inode,
        "content_hash": s.content_hash,
        "grep_string": s.grep_string,
        "window_size_sentences": s.window_size_sentences,
    }


def canonical_map_bytes(m: ClaimEvidenceMap) -> bytes:
    """Deterministic JSON bytes — sort_keys + tight separators + utf-8."""
    return _canonical_json_bytes(_map_to_dict(m))


def compute_content_hash(m: ClaimEvidenceMap) -> str:
    """sha3_512 hex digest over canonical_map_bytes(m)."""
    return hashlib.sha3_512(canonical_map_bytes(m)).hexdigest()


def verify_canonical_idempotent(payload: bytes) -> bool:
    """F-BT7-01: re-serialising parsed JSON yields identical bytes.

    True iff payload is canonical (sort_keys + tight separators + utf-8) and
    a parse → re-emit round-trip produces byte-identical output.
    """
    try:
        parsed = json.loads(payload)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return False
    re_emit = _canonical_json_bytes(parsed)
    return re_emit == payload
