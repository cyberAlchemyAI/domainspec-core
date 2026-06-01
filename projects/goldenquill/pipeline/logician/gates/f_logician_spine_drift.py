"""F-LOGICIAN-SPINE-DRIFT — POST-gate on Scribe + Editor outputs.

Catches narrative drift across Scribe sections and Editor edits. Enforces
that operator-approved strategic framings — locked at SP1 after KGIE
preflight — survive every drafting and editing pass intact.

Doctrine
--------
Nothing in Tilth is automated end-to-end. Defining human-in-the-mix stop
points is a critical component of the system, not a nice-to-have. Time
saved by stopping and tightening language to create accurate outputs is
far greater than the time required to remediate a memory contaminated
with bad data downstream.

Example catch
-------------
Operator locks framing-001 "Worker-owned cooperative scaling regenerative
mushroom production" at SP1. Scribe drafts Section 1 with this framing.
Editor R2 cleans Section 1 prose and silently weakens the framing to
"Mushroom production cooperative." Gate fires
``F-LOGICIAN-SPINE-DRIFT`` and DENIES Editor's edit.

Pipeline
--------
1. **Load.** Read ``orgs/<org>/grants/<grant_id>/spine.locked.yaml``.
   Validate schema. Missing file → FAIL with reason ``spine_missing``.
2. **Anchor lookup.** For *section_id*, find the ``CrossSectionAnchor``
   that references it. If none: PASS (gate is silent for unanchored
   sections).
3. **Framing recall.** For each framing-id required by the anchor's
   ``methods_must_mirror`` / ``outcomes_must_mirror`` /
   ``budget_justification_must_cite`` lists, compute keyword recall
   against the section text. If recall < 0.6 (default): FAIL with
   reason ``spine_framing_weak``.
4. **Anti-contradiction.** Scan section for explicit negation patterns
   targeting framing keywords. Hit: FAIL with reason
   ``spine_framing_contradicted``.
5. **Dialect register.** Compare section_dialect against
   ``spine.dialect_register``. Mismatch: FAIL with reason
   ``spine_dialect_drift``.
6. **Admin-risk avoid-list.** Scan section for any term in
   ``spine.admin_risk_terms_avoid``. Hit: FAIL with reason
   ``spine_admin_risk_violation``.

Properties
----------
- **Deterministic:** YAML load + token-set ops + regex negation +
  enum compare = fully deterministic. Zero LLM tokens.
- **Fail-closed:** any drift → FAIL. M13 bypass available, audited.
- **No spaCy / NER required.** Token extraction is regex + content-word
  matching. Lighter than fabricated-org / fact-drift.

Spec card
---------
``pipeline/engineering/spec_cards/logician_spine_drift_gate.md`` v1,
2026-05-08.

Blueprint anchor
----------------
``pipeline/blueprint/v0.1/section_04_logician.md`` — Logician POST-gate
battery; Law 4 (Funder-Attractive Framing) deterministic enforcement
layer.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Final, Iterable, Literal, Mapping, Optional


# --------------------------------------------------------------------------
# Public failure code + tunables
# --------------------------------------------------------------------------

F_LOGICIAN_SPINE_DRIFT: Final[str] = "F-LOGICIAN-SPINE-DRIFT"

DEFAULT_KEYWORD_RECALL_THRESHOLD: Final[float] = 0.6

# Closed enum mirrored from pipeline.seats.scribe.dialect — restated here
# to avoid a private-name import. Keep in sync.
_VALID_DIALECTS: Final[frozenset[str]] = frozenset(
    {"conservative", "centrist", "progressive", "soul_fire"}
)

# Stopword set for content-word extraction. Conservative — drops obvious
# function words. Not exhaustive English stopwords; the goal is keyword
# discrimination, not English-major linguistics. Operators can always
# tune the recall threshold per spine.
_STOPWORDS: Final[frozenset[str]] = frozenset({
    "a", "an", "the", "and", "or", "but", "of", "to", "in", "on",
    "at", "for", "with", "from", "by", "as", "is", "are", "was",
    "were", "be", "been", "being", "have", "has", "had", "do",
    "does", "did", "will", "would", "could", "should", "may",
    "might", "must", "can", "this", "that", "these", "those",
    "it", "its", "their", "them", "they", "we", "our", "us",
    "you", "your", "he", "she", "his", "her", "him", "i", "my",
    "me", "if", "then", "than", "so", "such", "into", "through",
    "across", "between", "above", "below", "after", "before",
    "during", "while", "when", "where", "why", "how", "what",
    "which", "who", "whom", "whose", "all", "any", "each",
    "every", "some", "none", "both", "either", "neither",
    "not", "no", "nor", "yes", "very", "more", "most", "less",
    "least", "many", "much", "few", "several", "other", "another",
    "same", "different",
})

# Minimum content-word length — drops single-letter and common 2-3 char
# function words that escape the stopword list (e.g., "us", "we", "as").
_MIN_CONTENT_WORD_LEN: Final[int] = 4

# Anti-contradiction phrase prefixes. We construct full patterns at check
# time by interpolating each framing keyword. Conservative regex — fires
# on explicit negation only, not on subtle weakening.
_NEGATION_CUES: Final[tuple[str, ...]] = (
    r"not\s+(?:a|an|the)?\s*",
    r"outside\s+(?:of\s+)?(?:a|an|the)?\s*",
    r"reject(?:s|ed|ing)?\s+(?:a|an|the)?\s*",
    r"opposite\s+of\s+(?:a|an|the)?\s*",
    r"contrary\s+to\s+(?:a|an|the)?\s*",
    r"(?:non|anti)[-\s]+",
)

# --------------------------------------------------------------------------
# Reason tags
# --------------------------------------------------------------------------

_REASON_SPINE_MISSING: Final[str] = "spine_missing"
_REASON_FRAMING_WEAK: Final[str] = "spine_framing_weak"
_REASON_FRAMING_CONTRADICTED: Final[str] = "spine_framing_contradicted"
_REASON_DIALECT_DRIFT: Final[str] = "spine_dialect_drift"
_REASON_ADMIN_RISK_VIOLATION: Final[str] = "spine_admin_risk_violation"
_REASON_SCHEMA_ERROR: Final[str] = "spine_schema_error"

ReasonTag = Literal[
    "spine_missing",
    "spine_framing_weak",
    "spine_framing_contradicted",
    "spine_dialect_drift",
    "spine_admin_risk_violation",
    "spine_schema_error",
]


# --------------------------------------------------------------------------
# Dataclasses
# --------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True, slots=True)
class SpineFraming:
    """One funder-attractive framing inside a locked spine."""

    id: str
    claim: str
    rationale: str
    rfa_anchor: str
    # Derived at load time — content words ≥4 chars in claim, lowercased.
    keywords: frozenset[str]


@dataclass(frozen=True, kw_only=True, slots=True)
class SmartOutcomeShape:
    primary: str
    secondary: Optional[str] = None
    tertiary: Optional[str] = None


@dataclass(frozen=True, kw_only=True, slots=True)
class CrossSectionAnchor:
    """Anchor binding a section_id to required framing-ids."""

    section_id: str
    methods_must_mirror: tuple[str, ...] = ()
    outcomes_must_mirror: tuple[str, ...] = ()
    budget_justification_must_cite: tuple[str, ...] = ()

    def required_framing_ids(self) -> frozenset[str]:
        """Union of all three mirroring lists — what this section must reflect."""
        return frozenset(
            self.methods_must_mirror
            + self.outcomes_must_mirror
            + self.budget_justification_must_cite
        )


@dataclass(frozen=True, kw_only=True, slots=True)
class NarrativeSpine:
    """Operator-locked per-grant narrative spine."""

    grant_id: str
    locked_at: datetime
    locked_by: str
    version: int
    funder_attractive_framings: tuple[SpineFraming, ...]
    dialect_register: str
    admin_risk_terms_in_use: tuple[str, ...]
    admin_risk_terms_avoid: tuple[str, ...]
    smart_outcome_shape: SmartOutcomeShape
    strategic_emphasis: Mapping[str, Any] = field(default_factory=dict)
    cross_section_anchors: tuple[CrossSectionAnchor, ...] = ()
    keyword_recall_threshold: float = DEFAULT_KEYWORD_RECALL_THRESHOLD

    def __post_init__(self) -> None:
        if not self.grant_id.strip():
            raise ValueError("NarrativeSpine.grant_id must be non-empty")
        if self.locked_at.tzinfo is None:
            raise ValueError("NarrativeSpine.locked_at must be timezone-aware")
        if self.version < 1:
            raise ValueError(
                f"NarrativeSpine.version must be >= 1; got {self.version!r}"
            )
        if self.dialect_register not in _VALID_DIALECTS:
            raise ValueError(
                f"NarrativeSpine.dialect_register={self.dialect_register!r} "
                f"not in {sorted(_VALID_DIALECTS)}"
            )
        if not (0.0 < self.keyword_recall_threshold <= 1.0):
            raise ValueError(
                f"NarrativeSpine.keyword_recall_threshold must be in (0, 1]; "
                f"got {self.keyword_recall_threshold!r}"
            )

    def framing_by_id(self, framing_id: str) -> Optional[SpineFraming]:
        for f in self.funder_attractive_framings:
            if f.id == framing_id:
                return f
        return None

    def anchor_for_section(self, section_id: str) -> Optional[CrossSectionAnchor]:
        for a in self.cross_section_anchors:
            if a.section_id == section_id:
                return a
        return None


@dataclass(frozen=True, kw_only=True, slots=True)
class SpineDriftFinding:
    """One drift incident with full operator-actionable context."""

    framing_id: Optional[str]    # None for non-framing failures
    section_id: str
    reason_tag: str
    detail: str                   # missing keywords / contradiction / hit term


@dataclass(frozen=True, kw_only=True, slots=True)
class SpineDriftGateResult:
    """POST-gate verdict."""

    verdict: Literal["PASS", "FAIL"]
    failure_code: Optional[str] = None
    findings: tuple[SpineDriftFinding, ...] = ()
    section_id: str = ""
    framings_checked: int = 0
    schema_error: Optional[str] = None  # populated on yaml/schema parse fail


# --------------------------------------------------------------------------
# Exceptions
# --------------------------------------------------------------------------

class SpineSchemaError(Exception):
    """YAML parse or schema-shape violation in spine file."""


# --------------------------------------------------------------------------
# Core helpers
# --------------------------------------------------------------------------

def _extract_keywords(text: str) -> frozenset[str]:
    """Return the set of content-word tokens (lowercased) in *text*.

    Content words = ≥ :data:`_MIN_CONTENT_WORD_LEN` chars, alphanumeric +
    apostrophe + hyphen, NOT in :data:`_STOPWORDS`.
    """
    if not text:
        return frozenset()
    raw = re.findall(r"[A-Za-z][A-Za-z0-9'-]+", text.lower())
    return frozenset(
        tok for tok in raw
        if len(tok) >= _MIN_CONTENT_WORD_LEN and tok not in _STOPWORDS
    )


def _section_token_set(section_text: str) -> frozenset[str]:
    """Same content-word extraction, applied to section body."""
    return _extract_keywords(section_text)


def _check_anti_contradiction(
    section_text: str,
    keywords: Iterable[str],
) -> Optional[str]:
    """Return a detail string when section explicitly contradicts a keyword.

    Builds a regex per keyword: ``(<negation_cue>)<keyword>``. First hit
    wins; returns the matched substring as the detail. Returns None when
    no contradiction detected.
    """
    section_lower = section_text.lower()
    for kw in keywords:
        kw_pat = re.escape(kw)
        for cue in _NEGATION_CUES:
            full_pat = re.compile(cue + kw_pat, re.IGNORECASE)
            m = full_pat.search(section_lower)
            if m:
                # Find the original-case substring for the operator finding
                orig_idx = section_lower.find(m.group(0))
                if orig_idx >= 0:
                    return section_text[orig_idx : orig_idx + len(m.group(0))]
                return m.group(0)
    return None


def _check_admin_risk_avoid(
    section_text: str,
    avoid_terms: Iterable[str],
) -> Optional[str]:
    """Return the first avoid-term substring detected, else None.

    Case-insensitive substring match, word-boundaried (avoid matching
    "DEI" inside "DEIcide" etc.).
    """
    section_lower = section_text.lower()
    for term in avoid_terms:
        if not term.strip():
            continue
        # Word-boundaried so partial-token matches don't fire (DEI ≠ DEIcide)
        pat = re.compile(rf"\b{re.escape(term.lower())}\b")
        m = pat.search(section_lower)
        if m:
            return term
    return None


# --------------------------------------------------------------------------
# YAML loader
# --------------------------------------------------------------------------

def _parse_datetime(value: Any, source: Path, field_name: str) -> datetime:
    """Coerce YAML datetime to tz-aware datetime; raise on unparseable input."""
    if isinstance(value, datetime):
        if value.tzinfo is None:
            raise SpineSchemaError(
                f"{source}: {field_name} must be timezone-aware"
            )
        return value
    if isinstance(value, str):
        try:
            dt = datetime.fromisoformat(value)
        except ValueError as exc:
            raise SpineSchemaError(
                f"{source}: {field_name} unparseable: {exc}"
            ) from exc
        if dt.tzinfo is None:
            raise SpineSchemaError(
                f"{source}: {field_name} must be timezone-aware"
            )
        return dt
    raise SpineSchemaError(
        f"{source}: {field_name} must be ISO-8601 string or datetime; "
        f"got {type(value).__name__}"
    )


def _parse_framing(raw: Any, source: Path) -> SpineFraming:
    if not isinstance(raw, dict):
        raise SpineSchemaError(
            f"{source}: framing entries must be mappings, got "
            f"{type(raw).__name__}"
        )
    fid = str(raw.get("id", "")).strip()
    claim = str(raw.get("claim", "")).strip()
    rationale = str(raw.get("rationale", "")).strip()
    rfa_anchor = str(raw.get("rfa_anchor", "")).strip()
    if not all((fid, claim, rationale, rfa_anchor)):
        raise SpineSchemaError(
            f"{source}: framing requires id, claim, rationale, rfa_anchor — "
            f"got id={fid!r}"
        )
    return SpineFraming(
        id=fid,
        claim=claim,
        rationale=rationale,
        rfa_anchor=rfa_anchor,
        keywords=_extract_keywords(claim),
    )


def _parse_anchor(raw: Any, source: Path) -> CrossSectionAnchor:
    if not isinstance(raw, dict):
        raise SpineSchemaError(
            f"{source}: cross_section_anchors entries must be mappings"
        )
    section_id = str(raw.get("section_id", "")).strip()
    if not section_id:
        raise SpineSchemaError(
            f"{source}: cross_section_anchors entry missing section_id"
        )

    def _str_tuple(key: str) -> tuple[str, ...]:
        val = raw.get(key, [])
        if val is None:
            return ()
        if not isinstance(val, list):
            raise SpineSchemaError(
                f"{source}: anchor.{key} must be a list (or null), got "
                f"{type(val).__name__}"
            )
        out: list[str] = []
        for item in val:
            s = str(item).strip()
            if not s:
                raise SpineSchemaError(
                    f"{source}: anchor.{key} contains empty string"
                )
            out.append(s)
        return tuple(out)

    return CrossSectionAnchor(
        section_id=section_id,
        methods_must_mirror=_str_tuple("methods_must_mirror"),
        outcomes_must_mirror=_str_tuple("outcomes_must_mirror"),
        budget_justification_must_cite=_str_tuple("budget_justification_must_cite"),
    )


def load_spine(path: Path) -> NarrativeSpine:
    """Load and validate a spine YAML file.

    Raises :class:`SpineSchemaError` on any parse / shape failure.
    Raises :class:`FileNotFoundError` when *path* doesn't exist.
    """
    try:
        import yaml
    except ImportError as exc:
        raise SpineSchemaError(
            f"PyYAML required for spine loading: {exc}"
        ) from exc

    if not path.exists():
        raise FileNotFoundError(f"spine file not found: {path}")

    try:
        raw_text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SpineSchemaError(f"{path}: read failed: {exc}") from exc

    try:
        data = yaml.safe_load(raw_text)
    except yaml.YAMLError as exc:
        raise SpineSchemaError(f"{path}: YAML parse error: {exc}") from exc

    if not isinstance(data, dict):
        raise SpineSchemaError(
            f"{path}: top-level must be a mapping, got {type(data).__name__}"
        )

    grant_id = str(data.get("grant_id", "")).strip()
    if not grant_id:
        raise SpineSchemaError(f"{path}: grant_id is required")

    locked_by = str(data.get("locked_by", "")).strip()
    if not locked_by:
        raise SpineSchemaError(f"{path}: locked_by is required")

    locked_at = _parse_datetime(data.get("locked_at"), path, "locked_at")

    version_raw = data.get("version", 1)
    if not isinstance(version_raw, int):
        raise SpineSchemaError(
            f"{path}: version must be an integer, got {type(version_raw).__name__}"
        )

    framings_raw = data.get("funder_attractive_framings", [])
    if not isinstance(framings_raw, list) or not framings_raw:
        raise SpineSchemaError(
            f"{path}: funder_attractive_framings must be a non-empty list"
        )
    framings = tuple(_parse_framing(f, path) for f in framings_raw)

    dialect_register = str(data.get("dialect_register", "")).strip()
    if dialect_register not in _VALID_DIALECTS:
        raise SpineSchemaError(
            f"{path}: dialect_register={dialect_register!r} not in "
            f"{sorted(_VALID_DIALECTS)}"
        )

    def _str_list(key: str) -> tuple[str, ...]:
        val = data.get(key, [])
        if val is None:
            return ()
        if not isinstance(val, list):
            raise SpineSchemaError(
                f"{path}: {key} must be a list (or null)"
            )
        return tuple(str(s).strip() for s in val if str(s).strip())

    admin_risk_terms_in_use = _str_list("admin_risk_terms_in_use")
    admin_risk_terms_avoid = _str_list("admin_risk_terms_avoid")

    smart_raw = data.get("smart_outcome_shape", {})
    if not isinstance(smart_raw, dict):
        raise SpineSchemaError(
            f"{path}: smart_outcome_shape must be a mapping"
        )
    primary = str(smart_raw.get("primary", "")).strip()
    if not primary:
        raise SpineSchemaError(
            f"{path}: smart_outcome_shape.primary is required"
        )
    smart = SmartOutcomeShape(
        primary=primary,
        secondary=str(smart_raw.get("secondary") or "") or None,
        tertiary=str(smart_raw.get("tertiary") or "") or None,
    )

    strategic_emphasis = data.get("strategic_emphasis", {}) or {}
    if not isinstance(strategic_emphasis, dict):
        raise SpineSchemaError(
            f"{path}: strategic_emphasis must be a mapping"
        )

    anchors_raw = data.get("cross_section_anchors", []) or []
    if not isinstance(anchors_raw, list):
        raise SpineSchemaError(
            f"{path}: cross_section_anchors must be a list"
        )
    anchors = tuple(_parse_anchor(a, path) for a in anchors_raw)

    threshold = data.get("keyword_recall_threshold", DEFAULT_KEYWORD_RECALL_THRESHOLD)
    if not isinstance(threshold, (int, float)):
        raise SpineSchemaError(
            f"{path}: keyword_recall_threshold must be numeric"
        )

    try:
        return NarrativeSpine(
            grant_id=grant_id,
            locked_at=locked_at,
            locked_by=locked_by,
            version=version_raw,
            funder_attractive_framings=framings,
            dialect_register=dialect_register,
            admin_risk_terms_in_use=admin_risk_terms_in_use,
            admin_risk_terms_avoid=admin_risk_terms_avoid,
            smart_outcome_shape=smart,
            strategic_emphasis=strategic_emphasis,
            cross_section_anchors=anchors,
            keyword_recall_threshold=float(threshold),
        )
    except ValueError as exc:
        raise SpineSchemaError(f"{path}: {exc}") from exc


# --------------------------------------------------------------------------
# Public entry point
# --------------------------------------------------------------------------

def check_spine_drift(
    *,
    section_text: str,
    section_id: str,
    section_dialect: str,
    spine_path: Path,
) -> SpineDriftGateResult:
    """POST-gate F-LOGICIAN-SPINE-DRIFT.

    Args:
        section_text: Scribe (or Editor)-produced section body.
        section_id: Canonical section identifier (e.g. "1.A.2").
        section_dialect: Caller's classified dialect for this section.
            Must be in the closed dialect enum or "unknown" (low-
            confidence classifications skip the dialect check).
        spine_path: Path to ``orgs/<org>/grants/<grant_id>/spine.locked.yaml``.

    Returns:
        :class:`SpineDriftGateResult`. On structural failure (missing file,
        YAML parse, schema mismatch) returns FAIL with reason ``spine_missing``
        or ``spine_schema_error``.
    """
    # 1) Load spine
    try:
        spine = load_spine(spine_path)
    except FileNotFoundError:
        return SpineDriftGateResult(
            verdict="FAIL",
            failure_code=F_LOGICIAN_SPINE_DRIFT,
            findings=(
                SpineDriftFinding(
                    framing_id=None,
                    section_id=section_id,
                    reason_tag=_REASON_SPINE_MISSING,
                    detail=f"spine file not found: {spine_path}",
                ),
            ),
            section_id=section_id,
        )
    except SpineSchemaError as exc:
        return SpineDriftGateResult(
            verdict="FAIL",
            failure_code=F_LOGICIAN_SPINE_DRIFT,
            findings=(
                SpineDriftFinding(
                    framing_id=None,
                    section_id=section_id,
                    reason_tag=_REASON_SCHEMA_ERROR,
                    detail=str(exc),
                ),
            ),
            section_id=section_id,
            schema_error=str(exc),
        )

    findings: list[SpineDriftFinding] = []

    # 2) Anchor lookup — gate is silent on unanchored sections
    anchor = spine.anchor_for_section(section_id)
    framings_checked = 0

    if anchor is not None:
        section_tokens = _section_token_set(section_text)

        for framing_id in sorted(anchor.required_framing_ids()):
            framing = spine.framing_by_id(framing_id)
            if framing is None:
                # Anchor references a framing that doesn't exist in spine —
                # schema error masquerading as drift, surface clearly.
                findings.append(SpineDriftFinding(
                    framing_id=framing_id,
                    section_id=section_id,
                    reason_tag=_REASON_SCHEMA_ERROR,
                    detail=(
                        f"cross_section_anchors[section_id={section_id}] "
                        f"references framing_id={framing_id!r} not in "
                        f"funder_attractive_framings"
                    ),
                ))
                continue

            framings_checked += 1
            if not framing.keywords:
                # Framing claim too short to extract content words —
                # treat as PASS for this framing (operator's clue to
                # write a denser claim).
                continue

            # 3) Framing recall
            matched = framing.keywords & section_tokens
            recall = len(matched) / len(framing.keywords)
            if recall < spine.keyword_recall_threshold:
                missing = sorted(framing.keywords - section_tokens)
                findings.append(SpineDriftFinding(
                    framing_id=framing.id,
                    section_id=section_id,
                    reason_tag=_REASON_FRAMING_WEAK,
                    detail=(
                        f"keyword recall {recall:.2f} < threshold "
                        f"{spine.keyword_recall_threshold:.2f}; "
                        f"missing: {missing}"
                    ),
                ))
                continue

            # 4) Anti-contradiction
            contradicted = _check_anti_contradiction(
                section_text, framing.keywords
            )
            if contradicted is not None:
                findings.append(SpineDriftFinding(
                    framing_id=framing.id,
                    section_id=section_id,
                    reason_tag=_REASON_FRAMING_CONTRADICTED,
                    detail=f"detected negation: '{contradicted}'",
                ))

    # 5) Dialect register check — runs regardless of anchor presence
    if section_dialect and section_dialect != "unknown":
        if section_dialect != spine.dialect_register:
            findings.append(SpineDriftFinding(
                framing_id=None,
                section_id=section_id,
                reason_tag=_REASON_DIALECT_DRIFT,
                detail=(
                    f"section dialect={section_dialect!r} != "
                    f"spine.dialect_register={spine.dialect_register!r}"
                ),
            ))

    # 6) Admin-risk avoid-list — runs regardless of anchor presence
    if spine.admin_risk_terms_avoid:
        hit = _check_admin_risk_avoid(section_text, spine.admin_risk_terms_avoid)
        if hit is not None:
            findings.append(SpineDriftFinding(
                framing_id=None,
                section_id=section_id,
                reason_tag=_REASON_ADMIN_RISK_VIOLATION,
                detail=f"avoid-list term in section: '{hit}'",
            ))

    if findings:
        return SpineDriftGateResult(
            verdict="FAIL",
            failure_code=F_LOGICIAN_SPINE_DRIFT,
            findings=tuple(findings),
            section_id=section_id,
            framings_checked=framings_checked,
        )
    return SpineDriftGateResult(
        verdict="PASS",
        section_id=section_id,
        framings_checked=framings_checked,
    )


__all__ = [
    "F_LOGICIAN_SPINE_DRIFT",
    "DEFAULT_KEYWORD_RECALL_THRESHOLD",
    "CrossSectionAnchor",
    "NarrativeSpine",
    "SmartOutcomeShape",
    "SpineFraming",
    "SpineDriftFinding",
    "SpineDriftGateResult",
    "SpineSchemaError",
    "load_spine",
    "check_spine_drift",
]
