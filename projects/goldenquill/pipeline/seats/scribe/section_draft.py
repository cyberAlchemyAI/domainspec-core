"""pipeline.seats.scribe.section_draft — §7.5 + §7.2 Law 1 + §7.11 + §7.4a shapes.

Blueprint §7 Scribe v1.1.1 §7.5 LOCKED 2026-04-21. Pure data. Zero I/O at
R2 — composition + atomic persistence land at R3 (seat.py subprocess
entry + §2 Vault dispatcher).

Ships the eight Scribe-owned nested shapes that compose the per-section
output contract:

- :class:`SectionLimit` — word / character / page cap (§7.3 sub-shape).
- :class:`ClaimEvidence` — §7.2 Law 1 claim→source entry (§0.5 v7 row 124).
- :class:`EligibleActivityMatch` — §7.5 v1.1 Law 2 POST-gate support
  (§0.5 v7 row 126).
- :class:`AdminRiskFlag` — §7.11 severity-tiered term-flag entry
  (§0.5 v7 row 125).
- :class:`ScopeCheckComment` — §7.2 Law 2 scope-drift inline comment.
- :class:`ConversationAnchor` — §7.4a USER_DATA canonical anchor shape
  (§0.5 v7 row 127).
- :class:`SectionDraft` — §7.5 canonical per-section output contract
  (§0.5 v7 row 120).
- :class:`CompressedSectionDraft` — §7.10 compliant-version wrapper.

Invariants (construction-time):

- ``SectionLimit.limit_value`` is a positive int.
- ``ClaimEvidence.evidence_kind`` is closed over {RFA, PROJECT_CONTEXT,
  USER_DATA} (§7.2 Law 1 three-site trace).
- ``AdminRiskFlag.severity`` is closed over {low, medium, high} (§7.11).
- ``ConversationAnchor.sha3_512_prefix32`` is exactly 32 lowercase-hex
  chars (§7.4a v1.1 width — 128-bit birthday-bound floor per Red Team R-1
  narrow-fix).
- ``SectionDraft.section_order`` is >= 1.
- ``SectionDraft.over_limit_flag`` is True iff a ``rfa_section_limit`` is
  set AND the applicable count exceeds the limit (consistency check
  against :mod:`pipeline.seats.scribe.compress` helpers).
- ``SectionDraft.word_count`` and ``character_count`` match the body
  text under :func:`pipeline.seats.scribe.compress.count_words` /
  :func:`.count_characters`.
- ``CompressedSectionDraft.source_uncut_draft_sha3_512`` is 128 hex
  chars; ``compression_rationale`` is non-empty.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Final, Literal

from pipeline.seats.scribe.compress import count_characters, count_words
from pipeline.seats.scribe.dialect import Dialect


# ---------------------------------------------------------------------------
# Closed-set enumerations (V1 rebind-resistance via inline-literal frozensets)
# ---------------------------------------------------------------------------

EvidenceKind = Literal["RFA", "PROJECT_CONTEXT", "USER_DATA"]

_EVIDENCE_KIND_VALID: Final[frozenset[str]] = frozenset(
    {"RFA", "PROJECT_CONTEXT", "USER_DATA"}
)

AdminRiskSeverity = Literal["low", "medium", "high"]

_ADMIN_RISK_SEVERITY_VALID: Final[frozenset[str]] = frozenset(
    {"low", "medium", "high"}
)

LimitKind = Literal["words", "characters", "pages"]

_LIMIT_KIND_VALID: Final[frozenset[str]] = frozenset(
    {"words", "characters", "pages"}
)


_SHA3_512_HEX_LEN: Final[int] = 128
_CONVERSATION_ANCHOR_PREFIX_HEX_LEN: Final[int] = 32  # §7.4a v1.1 width
_HEX_CHARS: Final[frozenset[str]] = frozenset("0123456789abcdef")


def _is_lowercase_hex(s: str) -> bool:
    return len(s) > 0 and all(ch in _HEX_CHARS for ch in s)


# ---------------------------------------------------------------------------
# SectionLimit
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class SectionLimit:
    """§7.3 nested shape — section cap (limit_kind + positive limit_value)."""

    limit_kind: LimitKind
    limit_value: int

    def __post_init__(self) -> None:
        if self.limit_kind not in _LIMIT_KIND_VALID:
            raise ValueError(
                f"SectionLimit.limit_kind must be one of "
                f"{sorted(_LIMIT_KIND_VALID)}; got {self.limit_kind!r}."
            )
        if self.limit_value <= 0:
            raise ValueError(
                f"SectionLimit.limit_value must be a positive int; got "
                f"{self.limit_value!r}."
            )


# ---------------------------------------------------------------------------
# ClaimEvidence (§0.5 v7 row 124; §7.2 Law 1)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class ClaimEvidence:
    """§7.2 Law 1 claim→source entry — one per factual claim in body_text.

    ``evidence_kind`` + ``source_pointer`` together identify the source
    byte-range / project-context field / conversation-anchor backing the
    claim. R3 POST-gate ``F-SCRIBE-UNSOURCED-CLAIM`` walks each entry and
    grep-verifies the claim against the cited source.
    """

    claim_text: str
    evidence_kind: EvidenceKind
    source_pointer: str

    def __post_init__(self) -> None:
        if not isinstance(self.claim_text, str) or not self.claim_text.strip():
            raise ValueError("ClaimEvidence.claim_text must be non-empty.")
        if self.evidence_kind not in _EVIDENCE_KIND_VALID:
            raise ValueError(
                f"ClaimEvidence.evidence_kind must be one of "
                f"{sorted(_EVIDENCE_KIND_VALID)}; got {self.evidence_kind!r}."
            )
        if not isinstance(self.source_pointer, str) or not self.source_pointer.strip():
            raise ValueError(
                "ClaimEvidence.source_pointer must be non-empty — every Law 1 "
                "claim requires an addressable source."
            )


# ---------------------------------------------------------------------------
# EligibleActivityMatch (§0.5 v7 row 126; §7.5 v1.1 Law 2 Scribe-owned)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class EligibleActivityMatch:
    """§7.5 v1.1 — one entry per proposed project activity in body_text.

    ``matched_rfa_activity`` resolves against
    :attr:`RfaExtractedRecord.eligible_project_activities` when the Scribe
    seat can make an unambiguous match; otherwise ``None`` AND
    ``scope_check_flag == True`` (surfaces as ``[SCOPE-CHECK]`` in
    ``ScopeCheckComment``). R3 POST-gate ``F-SCRIBE-INELIGIBLE-ACTIVITY``
    walks this tuple and rejects the draft if any match is ``None`` with
    ``scope_check_flag == False`` (silent mismatch).
    """

    activity_phrase: str
    matched_rfa_activity: str | None
    scope_check_flag: bool

    def __post_init__(self) -> None:
        if not isinstance(self.activity_phrase, str) or not self.activity_phrase.strip():
            raise ValueError(
                "EligibleActivityMatch.activity_phrase must be non-empty."
            )
        if self.matched_rfa_activity is not None and not self.matched_rfa_activity.strip():
            raise ValueError(
                "EligibleActivityMatch.matched_rfa_activity must be None or a "
                "non-empty string (whitespace-only is not a valid RFA activity)."
            )
        # Invariant: if matched is None, scope_check_flag must be True —
        # no silent scope-drift allowed. Conversely, a matched activity
        # may still carry a scope-check flag if Scribe wants operator
        # review (e.g., broad match that could be tightened); that is
        # permitted.
        if self.matched_rfa_activity is None and not self.scope_check_flag:
            raise ValueError(
                f"EligibleActivityMatch({self.activity_phrase!r}): unmatched "
                f"activity (matched_rfa_activity is None) requires "
                f"scope_check_flag=True — silent scope-drift violates §7.2 "
                f"Law 2."
            )


# ---------------------------------------------------------------------------
# AdminRiskFlag (§0.5 v7 row 125; §7.11)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class AdminRiskFlag:
    """§7.11 — one entry per admin-risk-register term matched in body_text.

    ``applicant_approved`` is False by default at draft time; the operator
    toggles via the review loop. Severity-tiered routing per §7.11:
    LOW (auto-sub allowed with pre-approval), MEDIUM (always flag), HIGH
    (flag + hard-block finalize). R3 POST-gate
    ``F-SCRIBE-ADMIN-RISK-HIGH-UNAPPROVED`` trips on finalize attempt with
    any HIGH-severity flag + applicant_approved=False.
    """

    term: str
    severity: AdminRiskSeverity
    proposed_substitution: str | None
    applicant_approved: bool

    def __post_init__(self) -> None:
        if not isinstance(self.term, str) or not self.term.strip():
            raise ValueError("AdminRiskFlag.term must be non-empty.")
        if self.severity not in _ADMIN_RISK_SEVERITY_VALID:
            raise ValueError(
                f"AdminRiskFlag.severity must be one of "
                f"{sorted(_ADMIN_RISK_SEVERITY_VALID)}; got {self.severity!r}."
            )
        if (
            self.proposed_substitution is not None
            and not self.proposed_substitution.strip()
        ):
            raise ValueError(
                "AdminRiskFlag.proposed_substitution must be None or a "
                "non-empty string."
            )


# ---------------------------------------------------------------------------
# ScopeCheckComment
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class ScopeCheckComment:
    """§7.2 Law 2 inline `[SCOPE-CHECK]` note for operator review.

    Typically paired with an :class:`EligibleActivityMatch` whose
    ``scope_check_flag`` is True. Decoupled shape so Scribe may add
    comments that are not activity-bound (e.g., RFA-scope overlap
    observations at the prompt level).
    """

    activity_phrase: str
    comment: str

    def __post_init__(self) -> None:
        if not isinstance(self.activity_phrase, str) or not self.activity_phrase.strip():
            raise ValueError("ScopeCheckComment.activity_phrase must be non-empty.")
        if not isinstance(self.comment, str) or not self.comment.strip():
            raise ValueError("ScopeCheckComment.comment must be non-empty.")


# ---------------------------------------------------------------------------
# ConversationAnchor (§0.5 v7 row 127; §7.4a v1.1)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class ConversationAnchor:
    """§7.4a USER_DATA:<run_id>:<turn_ordinal>:<sha3_512_prefix32>.

    32-hex prefix width pins 128-bit birthday-bound floor per v1.1 narrow
    fix. Full 512-bit hash lives in the run-scoped append-only
    conversation log at ``orgs/<slug>/conversations/<run_id>.log.jsonl``;
    the anchor's compact reference uses the 32-hex prefix.
    """

    run_id: str
    turn_ordinal: int
    sha3_512_prefix32: str

    def __post_init__(self) -> None:
        if not isinstance(self.run_id, str) or not self.run_id.strip():
            raise ValueError("ConversationAnchor.run_id must be non-empty.")
        if self.turn_ordinal < 0:
            raise ValueError(
                f"ConversationAnchor.turn_ordinal must be >= 0; got "
                f"{self.turn_ordinal!r}."
            )
        if len(self.sha3_512_prefix32) != _CONVERSATION_ANCHOR_PREFIX_HEX_LEN:
            raise ValueError(
                f"ConversationAnchor.sha3_512_prefix32 must be "
                f"{_CONVERSATION_ANCHOR_PREFIX_HEX_LEN} hex chars; got "
                f"{len(self.sha3_512_prefix32)!r}."
            )
        if not _is_lowercase_hex(self.sha3_512_prefix32):
            raise ValueError(
                "ConversationAnchor.sha3_512_prefix32 must be lowercase hex."
            )

    def as_source_pointer(self) -> str:
        """Return the canonical ``USER_DATA:<...>`` string for a
        :class:`ClaimEvidence.source_pointer` field.
        """
        return (
            f"USER_DATA:{self.run_id}:{self.turn_ordinal}:"
            f"{self.sha3_512_prefix32}"
        )


# ---------------------------------------------------------------------------
# SectionDraft (§0.5 v7 row 120; §7.5 canonical per-section output contract)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class SectionDraft:
    """§7.5 — one per RFA-required section in the standard 13-section layout.

    Composed of the per-§ nested shapes: claim/evidence, activity/scope,
    admin-risk, and dialect pin. R3 seat subprocess emits a tuple of
    these on stdout; §8 Editor and §9 Judge consume the section-ordered
    manifest under ``orgs/<slug>/drafts/<run_id>/sections/*.json``.

    Invariants at construction:

    - ``section_order >= 1``.
    - ``word_count == count_words(body_text)`` and
      ``character_count == count_characters(body_text)``.
    - If ``rfa_section_limit`` is set: ``over_limit_flag`` reflects the
      words-or-characters comparison (pages caps are computed by the
      compress helper at the seat layer; R2 only checks words/characters
      here).
    - ``drafted_at_utc`` is timezone-aware.
    - Every :class:`EligibleActivityMatch` with ``scope_check_flag=True``
      should have a corresponding :class:`ScopeCheckComment` with the
      same ``activity_phrase`` (soft invariant — R3 POST-gate enforces;
      R2 does not reject construction on the orphan case).
    """

    section_name: str
    section_order: int
    body_text: str
    word_count: int
    character_count: int
    rfa_section_limit: SectionLimit | None
    over_limit_flag: bool
    claim_evidence_map: tuple[ClaimEvidence, ...]
    eligible_activity_map: tuple[EligibleActivityMatch, ...]
    admin_risk_flags: tuple[AdminRiskFlag, ...]
    scope_check_comments: tuple[ScopeCheckComment, ...]
    draft_dialect: Dialect
    drafted_at_utc: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.section_name, str) or not self.section_name.strip():
            raise ValueError("SectionDraft.section_name must be non-empty.")
        if self.section_order < 1:
            raise ValueError(
                f"SectionDraft.section_order must be >= 1; got "
                f"{self.section_order!r}."
            )
        if not isinstance(self.body_text, str):
            raise ValueError("SectionDraft.body_text must be a string.")
        expected_words = count_words(self.body_text)
        if self.word_count != expected_words:
            raise ValueError(
                f"SectionDraft.word_count={self.word_count!r} does not match "
                f"count_words(body_text)={expected_words!r}."
            )
        expected_chars = count_characters(self.body_text)
        if self.character_count != expected_chars:
            raise ValueError(
                f"SectionDraft.character_count={self.character_count!r} does "
                f"not match count_characters(body_text)={expected_chars!r}."
            )
        if self.drafted_at_utc.tzinfo is None:
            raise ValueError(
                "SectionDraft.drafted_at_utc must be timezone-aware."
            )
        # over_limit_flag consistency for words/characters caps. "pages"
        # caps are seat-layer responsibility because pages-per-body depends
        # on template-specific chars_per_page; R2 skips the pages branch.
        if self.rfa_section_limit is not None:
            limit = self.rfa_section_limit
            if limit.limit_kind == "words":
                actual_over = expected_words > limit.limit_value
                if self.over_limit_flag != actual_over:
                    raise ValueError(
                        f"SectionDraft.over_limit_flag={self.over_limit_flag!r} "
                        f"does not match word-count-vs-limit comparison "
                        f"({expected_words} vs {limit.limit_value})."
                    )
            elif limit.limit_kind == "characters":
                actual_over = expected_chars > limit.limit_value
                if self.over_limit_flag != actual_over:
                    raise ValueError(
                        f"SectionDraft.over_limit_flag={self.over_limit_flag!r} "
                        f"does not match character-count-vs-limit comparison "
                        f"({expected_chars} vs {limit.limit_value})."
                    )
            # limit_kind == "pages": R2 trusts the seat's computed flag;
            # no shape-level consistency check.
        else:
            if self.over_limit_flag:
                raise ValueError(
                    "SectionDraft.over_limit_flag must be False when "
                    "rfa_section_limit is None."
                )


# ---------------------------------------------------------------------------
# CompressedSectionDraft (§7.10)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class CompressedSectionDraft:
    """§7.10 compliant-version wrapper — pairs a compressed
    :class:`SectionDraft` with the full-byte hash of the uncut source
    draft + operator-visible compression rationale tuple.

    Scribe never emits only the compressed version; both are returned
    per §7.10 — operator decides which is submitted.
    """

    compressed_draft: SectionDraft
    source_uncut_draft_sha3_512: str
    compression_rationale: tuple[str, ...]

    def __post_init__(self) -> None:
        if len(self.source_uncut_draft_sha3_512) != _SHA3_512_HEX_LEN:
            raise ValueError(
                f"CompressedSectionDraft.source_uncut_draft_sha3_512 must be "
                f"{_SHA3_512_HEX_LEN} hex chars; got "
                f"{len(self.source_uncut_draft_sha3_512)!r}."
            )
        if not _is_lowercase_hex(self.source_uncut_draft_sha3_512):
            raise ValueError(
                "CompressedSectionDraft.source_uncut_draft_sha3_512 must be "
                "lowercase hex."
            )
        if len(self.compression_rationale) == 0:
            raise ValueError(
                "CompressedSectionDraft.compression_rationale must be "
                "non-empty (at least one rationale entry)."
            )
        for i, entry in enumerate(self.compression_rationale):
            if not isinstance(entry, str) or not entry.strip():
                raise ValueError(
                    f"CompressedSectionDraft.compression_rationale[{i}] must "
                    f"be a non-empty string; got {entry!r}."
                )
        # Soft invariant: the compressed draft should NOT itself be
        # over-limit. Enforced here for R2; R3 seat may re-prompt if a
        # single-pass compression fails to reach under-limit.
        if self.compressed_draft.over_limit_flag:
            raise ValueError(
                "CompressedSectionDraft.compressed_draft must not carry "
                "over_limit_flag=True — the compressed version is by "
                "definition under the RFA cap."
            )


__all__ = [
    # Closed-set enumerations
    "EvidenceKind",
    "AdminRiskSeverity",
    "LimitKind",
    # Shapes
    "SectionLimit",
    "ClaimEvidence",
    "EligibleActivityMatch",
    "AdminRiskFlag",
    "ScopeCheckComment",
    "ConversationAnchor",
    "SectionDraft",
    "CompressedSectionDraft",
]
