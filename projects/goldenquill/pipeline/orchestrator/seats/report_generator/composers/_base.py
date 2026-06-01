"""Shared Protocol + helper substrate for §14 Report Generator composers.

Per §14 v1 LOCKED 2026-05-10 + WS-J Slice 2 handoff (2026-05-11). This
module centralizes:

* The injected-Protocol shapes the composers consume (Vault read intent
  callable, Scribe drafting callable, clock, hash).
* The deterministic ``claim_id`` derivation per §14.5.1 / §14.6.x
  invariant (``compute_claim_id`` re-derivable at audit time).
* The composer-level ``ComposerError`` exception class.

Per OQ-S2-01 default: ``ScribeProtocol`` is the single generic
``compose_section(spec, sources) -> drafted_text`` callable. Per-sub-
section specs are carried via :class:`ScribeFieldSpec`.

No substrate I/O is performed in this module — callers inject. NO
``open()`` calls. NO direct ``cryptography`` / ``hashlib`` imports
(callers inject the ``hash_bytes`` callable).
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from dataclasses import dataclass, field
from typing import Any, Final, Mapping, Optional, Protocol, runtime_checkable


# ---------------------------------------------------------------------------
# Injected Protocols
# ---------------------------------------------------------------------------


@runtime_checkable
class VaultReadIntentCallable(Protocol):
    """Injected Vault read intent.

    ``__call__(*, kind, path, **kwargs) -> dict | list | object`` returns
    pre-parsed content for the substrate ``kind`` + ``path`` combination
    (operational-data sub-kind file, proposal_commitments.yaml,
    reporting_template.yaml, KFR register row, etc.).

    The composer never calls ``open()`` against vault paths; the read
    intent is the only sanctioned route per R-REPORT-VAULT-INTENT-
    REQUIRED (Slice 3 AST-lint).

    Exceptions from the read intent propagate to the composer; the
    composer returns ``ComposerError`` to the caller (track runner)
    which surfaces the failure through the F-REPORT-* gate machinery.
    """

    def __call__(self, *, kind: str, path: str, **kwargs: object) -> object: ...


@runtime_checkable
class ScribeProtocol(Protocol):
    """Injected Scribe drafting callable (per OQ-S2-01 default).

    ``__call__(*, spec, sources) -> drafted_text`` returns the drafted
    text for ``spec.field_name`` against the supplied ``sources`` list.
    The Scribe implementation is provided by the seat-level Scribe
    wiring; this Protocol is the composer-side contract.

    Implementations MUST be deterministic with respect to ``spec`` +
    ``sources`` content (no LLM randomness leaks into Logician's gate
    inputs at the composer layer; Scribe-side LLM-substrate calls are
    Scribe's own discipline).
    """

    def __call__(
        self,
        *,
        spec: "ScribeFieldSpec",
        sources: tuple[Mapping[str, object], ...],
    ) -> str: ...


@runtime_checkable
class ClockCallable(Protocol):
    """Injected clock callable returning current UTC ISO-8601 string.

    ``__call__() -> str`` — composer uses the returned timestamp for
    ``authored_at_utc`` + ``consent_tier_history_at_read_utc`` etc.
    Default implementation: ``datetime.datetime.now(tz=UTC).isoformat()``
    with ``+00:00`` → ``Z`` substitution. Tests inject deterministic
    fixed-clock callables.
    """

    def __call__(self) -> str: ...


@runtime_checkable
class HashBytesCallable(Protocol):
    """Injected hash callable.

    ``__call__(data: bytes) -> str`` returns lowercase-hex SHA3-512
    digest. The composer uses this to compute
    ``source_content_sha3_512`` + ``caption_text_sha3_512`` for each
    claim source. Defaults to
    :func:`pipeline.orchestrator.seats.report_generator._canonical.compute_sha3_512_hex`.
    """

    def __call__(self, data: bytes) -> str: ...


# ---------------------------------------------------------------------------
# Scribe field spec (per OQ-S2-01)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class ScribeFieldSpec:
    """Per-field drafting spec passed to :class:`ScribeProtocol`.

    The sub-section composer assembles per-field specs by walking the
    operator-captured ``reporting_template.yaml``
    ``required_fields_per_sub_section`` entry. Fields:

    * ``sub_section`` — one of ``SUB_SECTIONS_V0_2``.
    * ``field_name`` — funder's required field name (e.g.
      ``"accomplishments_narrative"``).
    * ``max_length_chars`` — funder cap; Scribe truncates / refines if
      drafted text exceeds.
    * ``required_min_length_chars`` — funder floor.
    * ``kind`` — ``"narrative"`` | ``"structured_table"`` | ``"gallery"`` |
      ``"beneficiary_block"``.
    * ``column_specs`` — for ``structured_table`` kind: per-column field
      specs (name + required flag).
    * ``extras`` — opaque additional spec (e.g. variance thresholds)
      passed-through to Scribe.
    """

    sub_section: str
    field_name: str
    kind: str
    max_length_chars: Optional[int] = None
    required_min_length_chars: Optional[int] = None
    column_specs: tuple[Mapping[str, object], ...] = field(default_factory=tuple)
    extras: Mapping[str, object] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Composer error
# ---------------------------------------------------------------------------


class ComposerError(Exception):
    """Composer-level invariant violation.

    Raised when a composer fails an internal contract before returning
    (e.g. an empty PROMOTED-set for a sub-section that requires at least
    one). The track runner / orchestrator catches and routes to the
    F-REPORT-* gate machinery.
    """


# ---------------------------------------------------------------------------
# Deterministic claim_id derivation (per §14.5.1 invariant)
# ---------------------------------------------------------------------------


_CLAIM_ID_PREFIX: Final[str] = "CLAIM-"
# 16 hex chars after the prefix — long enough that birthday-collision on
# any realistic per-draft claim count is < 1e-15.
_CLAIM_ID_HASH_LEN: Final[int] = 16
# Re-use the same content-token re from _entailment._content_tokens so
# the "claim_keyword_hash" extracted here is consistent with the
# entailment gate's view.
_CLAIM_KEYWORD_TOKEN_RE: Final[re.Pattern[str]] = re.compile(r"[a-z0-9]+", re.ASCII)


def _claim_keyword_hash(claim_text: str) -> str:
    """Stable content-token-derived hash for ``claim_id`` derivation.

    NFC normalize → lowercase → extract alphanumeric tokens → sort →
    join → SHA3-512 → first 16 hex chars. Deterministic; whitespace +
    punctuation insensitive.
    """
    nfc = unicodedata.normalize("NFC", claim_text).lower()
    tokens = sorted(_CLAIM_KEYWORD_TOKEN_RE.findall(nfc))
    joined = "|".join(tokens).encode("utf-8")
    return hashlib.sha3_512(joined).hexdigest()[:_CLAIM_ID_HASH_LEN]


def compute_claim_id(
    *,
    sub_section: str,
    paragraph_index: int,
    sentence_index: int,
    claim_text: str,
) -> str:
    """Compute the deterministic ``claim_id`` per §14.5.1 invariant.

    Format:
    ``CLAIM-<sub_section>-p<paragraph_index>-s<sentence_index>-<keyword_hash>``

    All components are re-derivable at audit time — the same draft text
    in the same sub-section / paragraph / sentence position produces the
    same ``claim_id``. Hashing reduces ``claim_text`` to a stable
    content-signature.

    Per RT-C2-02 closure (commitment_id-style safe-identifier regex
    audit), the resulting string conforms to ``^[A-Z0-9_-]+$``.
    """
    if sub_section is None or not isinstance(sub_section, str) or not sub_section:
        raise ValueError("sub_section must be a non-empty string")
    if not isinstance(paragraph_index, int) or paragraph_index < 0:
        raise ValueError(f"paragraph_index must be int >= 0; got {paragraph_index!r}")
    if not isinstance(sentence_index, int) or sentence_index < 0:
        raise ValueError(f"sentence_index must be int >= 0; got {sentence_index!r}")
    if not isinstance(claim_text, str):
        raise TypeError(f"claim_text must be str; got {type(claim_text).__name__}")
    # Upper-case the sub_section so the resulting id matches the
    # commitment_id safe-identifier regex.
    sub_upper = sub_section.upper().replace("_", "-")
    keyword_hash = _claim_keyword_hash(claim_text).upper()
    return f"{_CLAIM_ID_PREFIX}{sub_upper}-P{paragraph_index}-S{sentence_index}-{keyword_hash}"


# ---------------------------------------------------------------------------
# Sentence splitter (composer-side; Scribe-side splitting may differ)
# ---------------------------------------------------------------------------


_SENTENCE_SPLIT_RE: Final[re.Pattern[str]] = re.compile(r"(?<=[.!?])\s+")


def split_paragraph_into_sentences(paragraph: str) -> list[str]:
    """Naive sentence splitter for composer claim-id derivation.

    Splits on sentence-terminal punctuation followed by whitespace. The
    composer uses the resulting sentence indices for deterministic
    ``claim_id`` derivation. Empty / whitespace-only sentences are
    filtered out.

    Per §14 v1 LOCK: the composer-side splitter is deliberately simple
    — claim_id is derived at compose time and audited at finalize time
    using the same splitter. Whitespace-stable.
    """
    if not paragraph:
        return []
    pieces = _SENTENCE_SPLIT_RE.split(paragraph.strip())
    return [p.strip() for p in pieces if p.strip()]


def split_text_into_paragraphs(text: str) -> list[str]:
    """Split a markdown text block into paragraphs (double-newline boundary)."""
    if not text:
        return []
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


# ---------------------------------------------------------------------------
# Helpers used across composers
# ---------------------------------------------------------------------------


def utc_now_isoformat_default() -> str:
    """Default clock implementation — UTC ISO-8601 with ``Z`` suffix."""
    from datetime import datetime, timezone

    return datetime.now(tz=timezone.utc).isoformat().replace("+00:00", "Z")


def default_hash_bytes(data: bytes) -> str:
    """Default :class:`HashBytesCallable` — SHA3-512 lowercase-hex."""
    return hashlib.sha3_512(data).hexdigest()


def encode_for_hash(value: Any) -> bytes:
    """Encode a value to canonical bytes for hashing.

    * ``bytes`` → as-is
    * ``str`` → UTF-8
    * ``dict | list | int | float | bool | None`` → canonical JSON
    * Everything else → ``str()`` then UTF-8 (last-resort)

    Used by composers to compute ``source_content_sha3_512`` over the
    pre-parsed source row dicts the read intent returns.
    """
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode("utf-8")
    # Canonical JSON via the seat's canonical bytes helper (no float; the
    # Decimal mandate per v7.0.4-M1 keeps the JSON encoder safe).
    from .._canonical import canonical_json_bytes

    return canonical_json_bytes(value)


__all__ = [
    "ClockCallable",
    "ComposerError",
    "HashBytesCallable",
    "ScribeFieldSpec",
    "ScribeProtocol",
    "VaultReadIntentCallable",
    "compute_claim_id",
    "default_hash_bytes",
    "encode_for_hash",
    "split_paragraph_into_sentences",
    "split_text_into_paragraphs",
    "utc_now_isoformat_default",
]
