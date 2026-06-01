"""F-LOGICIAN-FACT-DRIFT — POST-gate on Scribe drafts (numeric claims).

Catches numeric drift and fabricated quantitative claims. Complements
Law 5 verbatim-substring (string credentials) and F-LOGICIAN-FABRICATED-ORG
(organisations) by enforcing that every quantitative claim Scribe makes
traces to an operator-validated entry in the Key Facts Register (KFR).

Doctrine
--------
Bad numbers in a grant are not a quality problem — they are an
audit-finding, clawback, "you lied to a federal agency" problem.
Worst-case cost is orders of magnitude higher than narrative drift. The
system cannot be trustworthy if its quantitative substrate is freeform.

Example catch
-------------
Scribe drafts "FIT Farms LLC enrolled 247 students in 2025-26" but the
KFR entry ``enrollment_2025_2026`` has ``value: 231``. Gate fires
``F-LOGICIAN-FACT-DRIFT`` with both values shown and DENIES promotion.

Pipeline
--------
1. **Load.** Read ``orgs/<org>/key_facts_register.yaml``. Validate
   schema. Empty/missing register → FAIL with reason ``kfr_missing``.
2. **Extract.** Parse Scribe draft for numeric claims:
   - Regex finds bare numbers (``247``, ``1,247``, ``4.2``,
     ``4,287,000``); excludes years and regulation citations via
     denylist filter.
   - For each number, take the sentence containing it as context;
     extract subject-tokens (content words ≥4 chars, stopword-filtered)
     from the sentence.
   - Unit token = token immediately following the number, when present.
3. **Filter.** Keep KFR facts whose ``value`` parses as numeric AND
   whose temporal window overlaps the grant funding period:
   ``fact.when.as_of <= grant_funding_period.end`` AND
   (``fact.when.expiry is None`` OR ``fact.when.expiry >=
   grant_funding_period.start``).
4. **Match.** For each claim, compute Jaccard token overlap between
   claim's subject-tokens and each candidate fact's
   ``content_words(who) ∪ content_words(what)``. Best match by highest
   Jaccard ≥ ``MATCH_JACCARD_THRESHOLD`` (default 0.45). No match →
   FAIL with reason ``kfr_no_match``.
5. **Verify.** For matched (claim, fact) pairs:
   - ``delta_pct = abs(claim_value - fact_value) / fact_value * 100``
   - effective_threshold = ``fact.display_tolerance_pct``
   - ``delta_pct > effective_threshold`` → FAIL with
     ``kfr_value_drift``, both values surfaced.
6. **Verdict.** Zero failures → PASS with per-claim trace. Any failure
   → FAIL with full findings list.

Properties
----------
- **Deterministic:** YAML load + regex + Decimal arithmetic + Jaccard +
  enum filtering. Zero LLM tokens.
- **Fail-closed:** unmatched / drifted → FAIL. M13 bypass (audited).
- **No spaCy required for v0.2.A.** Subject-token extraction uses the
  same content-word extractor as the spine-drift gate. spaCy POS
  augmentation is queued for v0.2.B-C if real-world false-positive
  rates show subject-token noise.

Spec card
---------
``pipeline/engineering/spec_cards/logician_fact_drift_kfr_gate.md`` v1,
2026-05-08.

Blueprint anchor
----------------
``pipeline/blueprint/v0.1/section_04_logician.md`` — Logician POST-gate
battery; Law 5 (Applicant Brings Substance) quantitative-claim sibling
to F-LOGICIAN-FABRICATED-ORG.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Final, Literal, Mapping, Optional, Union

# --------------------------------------------------------------------------
# Public failure code + tunables
# --------------------------------------------------------------------------

F_LOGICIAN_FACT_DRIFT: Final[str] = "F-LOGICIAN-FACT-DRIFT"

# Jaccard threshold for matching a numeric claim to a KFR fact.
# English plural/inflection variation is handled via 5-char prefix stemming
# inside ``_stem_token`` before set comparison — so "students" / "student",
# "enrolls" / "enrollment", etc. converge.
# Empirical floor: 0.30 catches realistic claim/fact pairs while still
# rejecting unrelated topics. 0.70 (spec-card original guess) was too
# strict without proper morphology.
MATCH_JACCARD_THRESHOLD: Final[float] = 0.30

# Token stemming length — collapse "students" / "student" / "studying"
# down to "stude" so trivial morphology doesn't break Jaccard match.
_STEM_PREFIX_LEN: Final[int] = 5

# v0.2.B — POS tags kept when spaCy is available. NOUN/PROPN are the
# meaningful subject carriers; ADJ retains modifiers like "operating",
# "regenerative" that often disambiguate which fact the claim concerns.
# Verbs, adverbs, determiners, conjunctions are filtered out — they add
# noise to the Jaccard union without contributing matchable signal.
_KEEP_POS: Final[frozenset[str]] = frozenset({"NOUN", "PROPN", "ADJ"})

# Default value-tolerance: 0% (exact match required) unless the fact
# specifies its own ``display_tolerance_pct``.
DEFAULT_VALUE_TOLERANCE_PCT: Final[float] = 0.0

# Confidence + projection_or_actual closed enums
_VALID_CONFIDENCE: Final[frozenset[str]] = frozenset({"HIGH", "MEDIUM", "LOW"})
_VALID_PROJ_ACTUAL: Final[frozenset[str]] = frozenset({"projection", "actual"})

# Stopword set + min length: identical to spine-drift to keep behavior
# consistent across gates.
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
_MIN_CONTENT_WORD_LEN: Final[int] = 4

# Regex for bare numbers: integers with optional thousands separator
# and optional decimal. Negative lookahead/behind keep it from grabbing
# fragments of larger tokens. Matches: 247, 1,247, 4.2, 4,287,000.
_NUMBER_RE: Final[re.Pattern[str]] = re.compile(
    r"(?<![\d.])(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)(?![\d])"
)

# Years to filter out — anything matching a 4-digit number in the
# 1900-2099 range without a thousands separator.
_YEAR_RE: Final[re.Pattern[str]] = re.compile(r"^(19|20)\d{2}$")

# Sentence split — same lightweight regex used in fabricated-org gate.
_SENTENCE_SPLIT_RE: Final[re.Pattern[str]] = re.compile(r"(?<=[.!?])\s+")


# --------------------------------------------------------------------------
# Reason tags
# --------------------------------------------------------------------------

_REASON_NO_MATCH: Final[str] = "kfr_no_match"
_REASON_VALUE_DRIFT: Final[str] = "kfr_value_drift"
_REASON_TEMPORAL_INVALID: Final[str] = "kfr_temporal_invalid"
_REASON_KFR_MISSING: Final[str] = "kfr_missing"
_REASON_SCHEMA_ERROR: Final[str] = "kfr_schema_error"


# --------------------------------------------------------------------------
# Dataclasses
# --------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True, slots=True)
class TemporalWindow:
    period: str
    as_of: date
    expiry: Optional[date] = None

    def __post_init__(self) -> None:
        if not self.period.strip():
            raise ValueError("TemporalWindow.period is empty")
        if self.expiry is not None and self.expiry <= self.as_of:
            raise ValueError(
                f"TemporalWindow.expiry ({self.expiry}) must be after "
                f"as_of ({self.as_of})"
            )


@dataclass(frozen=True, kw_only=True, slots=True)
class ValidationBlock:
    confirmed_by: str
    confirmed_at: date
    source_doc: str
    source_doc_hash: Optional[str] = None

    def __post_init__(self) -> None:
        for attr in ("confirmed_by", "source_doc"):
            if not getattr(self, attr).strip():
                raise ValueError(f"ValidationBlock.{attr} is empty")


@dataclass(frozen=True, kw_only=True, slots=True)
class KfrFact:
    """One Key Facts Register entry."""

    id: str
    who: str
    what: str
    when: TemporalWindow
    where: str
    why: str
    how: str
    value: Union[Decimal, str]
    unit: str
    projection_or_actual: str
    validation: ValidationBlock
    confidence: str
    display_tolerance_pct: float = DEFAULT_VALUE_TOLERANCE_PCT
    notes: str = ""

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("KfrFact.id is empty")
        if self.confidence not in _VALID_CONFIDENCE:
            raise ValueError(
                f"KfrFact[{self.id}].confidence={self.confidence!r} not in "
                f"{sorted(_VALID_CONFIDENCE)}"
            )
        if self.projection_or_actual not in _VALID_PROJ_ACTUAL:
            raise ValueError(
                f"KfrFact[{self.id}].projection_or_actual={self.projection_or_actual!r} "
                f"not in {sorted(_VALID_PROJ_ACTUAL)}"
            )
        if self.display_tolerance_pct < 0:
            raise ValueError(
                f"KfrFact[{self.id}].display_tolerance_pct must be >= 0"
            )

    @property
    def is_numeric(self) -> bool:
        """True when value is a Decimal — fact is matchable to numeric claims."""
        return isinstance(self.value, Decimal)


@dataclass(frozen=True, kw_only=True, slots=True)
class KeyFactsRegister:
    schema_version: str
    org_slug: str
    facts: tuple[KfrFact, ...]

    def numeric_facts(self) -> tuple[KfrFact, ...]:
        return tuple(f for f in self.facts if f.is_numeric)

    def fact_by_id(self, fact_id: str) -> Optional[KfrFact]:
        for f in self.facts:
            if f.id == fact_id:
                return f
        return None


@dataclass(frozen=True, kw_only=True, slots=True)
class NumericClaim:
    """One number-bearing claim extracted from Scribe draft text."""

    number: Decimal
    raw_token: str               # original "247" / "1,247" / "4.2"
    unit_token: str              # next word after number (e.g. "students")
    subject_tokens: frozenset[str]  # content words from the claim's sentence
    sentence: str
    char_offset: int             # position in source text


@dataclass(frozen=True, kw_only=True, slots=True)
class FactDriftFinding:
    """One drift incident — operator-actionable."""

    claim_token: str             # raw number text from draft
    claim_value: Decimal
    claim_sentence: str
    nearest_fact_id: Optional[str]
    nearest_fact_value: Optional[Decimal]
    delta_pct: Optional[float]
    reason_tag: str
    detail: str


@dataclass(frozen=True, kw_only=True, slots=True)
class FactDriftGateResult:
    verdict: Literal["PASS", "FAIL"]
    failure_code: Optional[str] = None
    findings: tuple[FactDriftFinding, ...] = ()
    claim_count_extracted: int = 0
    claim_count_drifted: int = 0
    schema_error: Optional[str] = None


# --------------------------------------------------------------------------
# Exceptions
# --------------------------------------------------------------------------

class KfrSchemaError(Exception):
    """YAML parse or schema-shape violation in KFR file."""


# --------------------------------------------------------------------------
# Lazy spaCy loader (v0.2.B — POS-tagged subject extraction)
# --------------------------------------------------------------------------

# Module-level cache for spaCy nlp object. Mirrors fabricated-org gate
# pattern; both gates lazy-load to avoid forcing spaCy onto callers that
# don't need it. None means "not loaded yet"; False means "load attempted
# and failed — don't retry within process".
_NLP_CACHE: list[Any] = [None]
_NLP_LOAD_ERROR: list[Optional[str]] = [None]


def _try_load_spacy() -> tuple[Any, Optional[str]]:
    """Return (nlp, None) on success, (None, error_message) on failure.

    Caches both success and failure within the process.
    """
    if _NLP_CACHE[0] is not None and _NLP_CACHE[0] is not False:
        return _NLP_CACHE[0], None
    if _NLP_CACHE[0] is False:
        return None, _NLP_LOAD_ERROR[0]

    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
    except ImportError as exc:
        _NLP_CACHE[0] = False
        _NLP_LOAD_ERROR[0] = f"spacy not installed: {exc}"
        return None, _NLP_LOAD_ERROR[0]
    except OSError as exc:
        _NLP_CACHE[0] = False
        _NLP_LOAD_ERROR[0] = (
            f"en_core_web_sm not installed: {exc}. "
            f"Run `python -m spacy download en_core_web_sm`."
        )
        return None, _NLP_LOAD_ERROR[0]
    except Exception as exc:  # pragma: no cover  (defensive: spacy internal)
        _NLP_CACHE[0] = False
        _NLP_LOAD_ERROR[0] = f"spacy.load raised {type(exc).__name__}: {exc}"
        return None, _NLP_LOAD_ERROR[0]

    _NLP_CACHE[0] = nlp
    return nlp, None


# --------------------------------------------------------------------------
# Token / number helpers
# --------------------------------------------------------------------------

def _stem_token(tok: str) -> str:
    """Crude 5-char prefix stemmer.

    Maps plural/inflection variants to the same prefix:
    ``students`` / ``student`` / ``studying`` → ``stude``;
    ``enrolls`` / ``enrollment`` / ``enrolled`` → ``enrol``.
    Tokens shorter than the prefix length pass through unchanged.

    Crude but deterministic and language-agnostic-ish; sufficient for
    matching grant-domain English claims to KFR who/what tokens. If
    field experience shows over-merging (false positives) or
    under-merging (missed matches), swap in a real stemmer (e.g.,
    Snowball) at v0.2.B.
    """
    return tok[:_STEM_PREFIX_LEN] if len(tok) > _STEM_PREFIX_LEN else tok


def _content_words(text: str) -> frozenset[str]:
    """Stemmed content-word extraction (regex-only fallback).

    Drops stopwords + tokens shorter than :data:`_MIN_CONTENT_WORD_LEN`,
    then maps each surviving token through :func:`_stem_token` so
    morphological variants converge before set comparison.
    """
    if not text:
        return frozenset()
    raw = re.findall(r"[A-Za-z][A-Za-z0-9'-]+", text.lower())
    return frozenset(
        _stem_token(tok) for tok in raw
        if len(tok) >= _MIN_CONTENT_WORD_LEN and tok not in _STOPWORDS
    )


def _content_words_pos(text: str, nlp: Any) -> frozenset[str]:
    """v0.2.B — POS-filtered content-word extraction via spaCy.

    Same stemming + stopword + min-length filter, plus POS-tag filter:
    keeps only NOUN / PROPN / ADJ tokens (see :data:`_KEEP_POS`). This
    drops verbs, adverbs, determiners, etc. that pollute the Jaccard
    denominator without adding matchable signal.

    Caller is responsible for passing a loaded spaCy ``nlp`` object.
    Use :func:`_try_load_spacy` to lazily acquire one with caching.
    """
    if not text:
        return frozenset()
    try:
        doc = nlp(text)
    except Exception:  # noqa: BLE001
        # spaCy parse failure → fall back to regex extraction
        return _content_words(text)
    return frozenset(
        _stem_token(tok.lower_) for tok in doc
        if tok.pos_ in _KEEP_POS
        and len(tok.text) >= _MIN_CONTENT_WORD_LEN
        and tok.lower_ not in _STOPWORDS
        # Token text must be alphabetic-leading (drops numeric tokens
        # which spaCy sometimes tags NUM and would pass otherwise).
        and tok.text[0].isalpha()
    )


def _parse_number_token(token: str) -> Optional[Decimal]:
    """Parse '247' / '1,247' / '4.2' / '4,287,000' to Decimal. None on fail."""
    try:
        cleaned = token.replace(",", "")
        return Decimal(cleaned)
    except (InvalidOperation, ValueError):
        return None


def _is_year_token(token: str) -> bool:
    """True if token is a bare 4-digit year (no thousands separator)."""
    return bool(_YEAR_RE.match(token.replace(",", "")) and "," not in token)


def _split_sentences(text: str) -> list[tuple[str, int]]:
    """Return list of (sentence_text, char_offset_in_source)."""
    if not text:
        return []
    out: list[tuple[str, int]] = []
    cursor = 0
    for sent in _SENTENCE_SPLIT_RE.split(text):
        idx = text.find(sent, cursor)
        if idx >= 0:
            out.append((sent, idx))
            cursor = idx + len(sent)
    return out


def _next_word_after(text: str, end_idx: int) -> str:
    """Return the next word-like token after index *end_idx* (lowercase)."""
    tail = text[end_idx:].lstrip()
    m = re.match(r"[A-Za-z%$][A-Za-z0-9'-]*", tail)
    if not m:
        # Currency symbols and percentage fall through:
        m2 = re.match(r"[%$€£]", tail)
        if m2:
            return m2.group(0)
        return ""
    return m.group(0).lower()


def extract_numeric_claims(
    text: str,
    *,
    nlp: Any = None,
) -> tuple[NumericClaim, ...]:
    """Extract all numeric claims from *text*.

    Filters out:
    - Years (1900-2099 4-digit bare).
    - Numbers inside regulation citations.

    Subject-token extraction (v0.2.B):
    - When *nlp* is supplied (or auto-loaded successfully), uses spaCy
      POS tagging via :func:`_content_words_pos` — keeps only NOUN /
      PROPN / ADJ tokens. Tighter, less noisy.
    - Otherwise falls back to regex-only :func:`_content_words`. Same
      stemmer, broader inclusion.

    Pass ``nlp=False`` (sentinel) to force regex fallback even if spaCy
    is installed — useful for tests that want deterministic non-spaCy
    output.
    """
    if not text:
        return ()

    # Resolve the subject-token extractor (POS-aware vs regex fallback)
    use_pos = False
    pos_nlp: Any = None
    if nlp is not None and nlp is not False:
        pos_nlp = nlp
        use_pos = True
    elif nlp is None:
        # Default: try to lazily acquire spaCy. Silently fall back on miss.
        loaded, _err = _try_load_spacy()
        if loaded is not None:
            pos_nlp = loaded
            use_pos = True

    claims: list[NumericClaim] = []
    sentences = _split_sentences(text)

    for m in _NUMBER_RE.finditer(text):
        token = m.group(1)
        if _is_year_token(token):
            continue
        # Find the sentence containing this number
        offset = m.start()
        host_sentence = ""
        for sent, sent_off in sentences:
            if sent_off <= offset < sent_off + len(sent):
                host_sentence = sent
                break

        # Skip numbers in regulation citations. We check both:
        # - "Section <num>" / "Title <num>" / "Subpart <num>" — citation
        #   keyword immediately precedes the number;
        # - "<num> CFR" / "<num> USC" / "<num> U.S.C." — number is the
        #   leading title-number of a regulation reference.
        window_start = max(0, offset - 30)
        prefix = text[window_start:offset]
        suffix = text[offset + len(token) : offset + len(token) + 12]

        prefix_citation = re.search(
            r"(?:Title|Section|Subpart|Part|Chapter|Article)\s+$",
            prefix,
            re.IGNORECASE,
        )
        if prefix_citation:
            continue

        suffix_citation = re.match(
            r"\s+(?:CFR|USC|U\.S\.C\.?)\b",
            suffix,
            re.IGNORECASE,
        )
        if suffix_citation:
            continue

        value = _parse_number_token(token)
        if value is None:
            continue

        unit_token = _next_word_after(text, m.end())
        if use_pos:
            subject_tokens = _content_words_pos(host_sentence, pos_nlp)
        else:
            subject_tokens = _content_words(host_sentence)

        claims.append(NumericClaim(
            number=value,
            raw_token=token,
            unit_token=unit_token,
            subject_tokens=subject_tokens,
            sentence=host_sentence.strip(),
            char_offset=offset,
        ))

    return tuple(claims)


# --------------------------------------------------------------------------
# YAML loader
# --------------------------------------------------------------------------

def _coerce_date(value: Any, source: Path, field_name: str) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError as exc:
            raise KfrSchemaError(
                f"{source}: {field_name} unparseable: {exc}"
            ) from exc
    raise KfrSchemaError(
        f"{source}: {field_name} must be ISO date string or datetime; got "
        f"{type(value).__name__}"
    )


def _coerce_optional_date(value: Any, source: Path, field_name: str) -> Optional[date]:
    if value is None:
        return None
    return _coerce_date(value, source, field_name)


def _parse_value(raw: Any) -> Union[Decimal, str]:
    """Parse KFR `value` field — Decimal when numeric, str otherwise."""
    if isinstance(raw, Decimal):
        return raw
    if isinstance(raw, (int, float)):
        return Decimal(str(raw))
    if isinstance(raw, str):
        # Try Decimal parse; fall through to str on failure
        try:
            return Decimal(raw.replace(",", "").replace("_", ""))
        except InvalidOperation:
            return raw
    return str(raw)


def _parse_kfr_fact(raw: Any, source: Path) -> KfrFact:
    if not isinstance(raw, dict):
        raise KfrSchemaError(
            f"{source}: KFR entries must be mappings, got {type(raw).__name__}"
        )

    when_raw = raw.get("when", {})
    if not isinstance(when_raw, dict):
        raise KfrSchemaError(f"{source}: KfrFact.when must be a mapping")
    try:
        when = TemporalWindow(
            period=str(when_raw.get("period", "")).strip(),
            as_of=_coerce_date(when_raw.get("as_of"), source, "when.as_of"),
            expiry=_coerce_optional_date(when_raw.get("expiry"), source, "when.expiry"),
        )
    except ValueError as exc:
        raise KfrSchemaError(f"{source}: {exc}") from exc

    val_raw = raw.get("validation", {})
    if not isinstance(val_raw, dict):
        raise KfrSchemaError(f"{source}: KfrFact.validation must be a mapping")
    try:
        validation = ValidationBlock(
            confirmed_by=str(val_raw.get("confirmed_by", "")).strip(),
            confirmed_at=_coerce_date(val_raw.get("confirmed_at"), source, "validation.confirmed_at"),
            source_doc=str(val_raw.get("source_doc", "")).strip(),
            source_doc_hash=str(val_raw["source_doc_hash"]).strip() if val_raw.get("source_doc_hash") else None,
        )
    except ValueError as exc:
        raise KfrSchemaError(f"{source}: {exc}") from exc

    try:
        return KfrFact(
            id=str(raw.get("id", "")).strip(),
            who=str(raw.get("who", "")).strip(),
            what=str(raw.get("what", "")).strip(),
            when=when,
            where=str(raw.get("where", "")).strip(),
            why=str(raw.get("why", "")).strip(),
            how=str(raw.get("how", "")).strip(),
            value=_parse_value(raw.get("value")),
            unit=str(raw.get("unit", "")).strip(),
            projection_or_actual=str(raw.get("projection_or_actual", "")).strip(),
            validation=validation,
            confidence=str(raw.get("confidence", "")).strip(),
            display_tolerance_pct=float(raw.get("display_tolerance_pct", DEFAULT_VALUE_TOLERANCE_PCT)),
            notes=str(raw.get("notes", "")).strip(),
        )
    except ValueError as exc:
        raise KfrSchemaError(f"{source}: {exc}") from exc


def load_kfr(path: Path) -> KeyFactsRegister:
    """Load and validate a KFR YAML file.

    Raises :class:`KfrSchemaError` on parse/schema failure.
    Raises :class:`FileNotFoundError` when *path* doesn't exist.
    """
    try:
        import yaml
    except ImportError as exc:
        raise KfrSchemaError(f"PyYAML required: {exc}") from exc

    if not path.exists():
        raise FileNotFoundError(f"KFR file not found: {path}")

    try:
        raw_text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise KfrSchemaError(f"{path}: read failed: {exc}") from exc

    try:
        data = yaml.safe_load(raw_text)
    except yaml.YAMLError as exc:
        raise KfrSchemaError(f"{path}: YAML parse error: {exc}") from exc

    if not isinstance(data, dict):
        raise KfrSchemaError(
            f"{path}: top-level must be a mapping, got {type(data).__name__}"
        )

    schema_version = str(data.get("schemaVersion", "")).strip()
    if not schema_version:
        raise KfrSchemaError(f"{path}: schemaVersion is required")

    org_slug = str(data.get("org_slug", "")).strip()
    if not org_slug:
        raise KfrSchemaError(f"{path}: org_slug is required")

    facts_raw = data.get("facts", [])
    if not isinstance(facts_raw, list):
        raise KfrSchemaError(f"{path}: facts must be a list")

    facts = tuple(_parse_kfr_fact(f, path) for f in facts_raw)

    # Detect duplicate ids
    seen: dict[str, int] = {}
    for i, f in enumerate(facts):
        if f.id in seen:
            raise KfrSchemaError(
                f"{path}: duplicate fact id={f.id!r} at indices "
                f"{seen[f.id]} and {i}"
            )
        seen[f.id] = i

    return KeyFactsRegister(
        schema_version=schema_version,
        org_slug=org_slug,
        facts=facts,
    )


# --------------------------------------------------------------------------
# Match + verify helpers
# --------------------------------------------------------------------------

def _temporal_overlap(
    fact: KfrFact,
    grant_start: date,
    grant_end: date,
) -> bool:
    """True when fact's temporal window overlaps the grant funding period."""
    if fact.when.as_of > grant_end:
        return False
    if fact.when.expiry is not None and fact.when.expiry < grant_start:
        return False
    return True


def _jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _best_fact_match(
    claim: NumericClaim,
    candidates: tuple[KfrFact, ...],
) -> tuple[Optional[KfrFact], float]:
    """Find the highest-Jaccard fact for *claim*. Returns (fact, jaccard)."""
    if not candidates:
        return None, 0.0
    best_fact: Optional[KfrFact] = None
    best_jac = 0.0
    for fact in candidates:
        fact_tokens = _content_words(fact.who) | _content_words(fact.what)
        jac = _jaccard(claim.subject_tokens, fact_tokens)
        if jac > best_jac:
            best_jac = jac
            best_fact = fact
    return best_fact, best_jac


def _verify_value(
    claim_value: Decimal,
    fact: KfrFact,
) -> tuple[bool, float]:
    """Return (passes, delta_pct).

    `passes` is True when delta_pct <= fact.display_tolerance_pct.
    """
    if not isinstance(fact.value, Decimal):
        return False, 100.0  # non-numeric fact shouldn't reach here, defensive
    if fact.value == 0:
        # Zero-value reference: any nonzero claim diverges
        delta_pct = 0.0 if claim_value == 0 else 100.0
    else:
        delta = abs(claim_value - fact.value) / fact.value * 100
        delta_pct = float(delta)
    return delta_pct <= fact.display_tolerance_pct, delta_pct


# --------------------------------------------------------------------------
# Public entry point
# --------------------------------------------------------------------------

def check_fact_drift(
    *,
    draft_text: str,
    kfr_path: Path,
    grant_funding_period: tuple[date, date],
    match_jaccard_threshold: float = MATCH_JACCARD_THRESHOLD,
    nlp: Any = None,
) -> FactDriftGateResult:
    """POST-gate F-LOGICIAN-FACT-DRIFT.

    Args:
        draft_text: Scribe draft body.
        kfr_path: Path to ``orgs/<org>/key_facts_register.yaml``.
        grant_funding_period: (start, end) date pair — used for temporal
            validity of KFR facts.
        match_jaccard_threshold: Minimum Jaccard ratio for claim→fact
            match. Default :data:`MATCH_JACCARD_THRESHOLD`.
        nlp: Optional spaCy ``nlp`` object — for test injection or to
            force a specific model. When None (default), lazy-loads
            ``en_core_web_sm`` and uses POS-tagged subject extraction;
            silently falls back to regex content-words on load failure.
            Pass ``False`` (sentinel) to skip spaCy entirely.

    Returns:
        :class:`FactDriftGateResult`. Empty draft → PASS with zero counts.
        Missing KFR / schema error → FAIL.
    """
    if not draft_text or not draft_text.strip():
        return FactDriftGateResult(verdict="PASS")

    grant_start, grant_end = grant_funding_period
    if grant_start > grant_end:
        return FactDriftGateResult(
            verdict="FAIL",
            failure_code=F_LOGICIAN_FACT_DRIFT,
            schema_error=f"grant_funding_period invalid: {grant_start} > {grant_end}",
            findings=(
                FactDriftFinding(
                    claim_token="",
                    claim_value=Decimal(0),
                    claim_sentence="",
                    nearest_fact_id=None,
                    nearest_fact_value=None,
                    delta_pct=None,
                    reason_tag=_REASON_SCHEMA_ERROR,
                    detail=f"grant_funding_period.start ({grant_start}) > end ({grant_end})",
                ),
            ),
        )

    # 1) Load KFR
    try:
        kfr = load_kfr(kfr_path)
    except FileNotFoundError:
        return FactDriftGateResult(
            verdict="FAIL",
            failure_code=F_LOGICIAN_FACT_DRIFT,
            findings=(
                FactDriftFinding(
                    claim_token="",
                    claim_value=Decimal(0),
                    claim_sentence="",
                    nearest_fact_id=None,
                    nearest_fact_value=None,
                    delta_pct=None,
                    reason_tag=_REASON_KFR_MISSING,
                    detail=f"KFR file not found: {kfr_path}",
                ),
            ),
        )
    except KfrSchemaError as exc:
        return FactDriftGateResult(
            verdict="FAIL",
            failure_code=F_LOGICIAN_FACT_DRIFT,
            schema_error=str(exc),
            findings=(
                FactDriftFinding(
                    claim_token="",
                    claim_value=Decimal(0),
                    claim_sentence="",
                    nearest_fact_id=None,
                    nearest_fact_value=None,
                    delta_pct=None,
                    reason_tag=_REASON_SCHEMA_ERROR,
                    detail=str(exc),
                ),
            ),
        )

    # 2) Extract claims (threading nlp seam — None auto-loads, False skips)
    claims = extract_numeric_claims(draft_text, nlp=nlp)
    if not claims:
        return FactDriftGateResult(
            verdict="PASS",
            claim_count_extracted=0,
        )

    # 3) Filter facts by temporal validity + numericness
    candidate_facts = tuple(
        f for f in kfr.numeric_facts()
        if _temporal_overlap(f, grant_start, grant_end)
    )

    findings: list[FactDriftFinding] = []

    for claim in claims:
        # 4) Match
        best_fact, jaccard = _best_fact_match(claim, candidate_facts)
        if best_fact is None or jaccard < match_jaccard_threshold:
            findings.append(FactDriftFinding(
                claim_token=claim.raw_token,
                claim_value=claim.number,
                claim_sentence=claim.sentence,
                nearest_fact_id=best_fact.id if best_fact else None,
                nearest_fact_value=best_fact.value if (best_fact and best_fact.is_numeric) else None,
                delta_pct=None,
                reason_tag=_REASON_NO_MATCH,
                detail=(
                    f"jaccard={jaccard:.2f} < threshold={match_jaccard_threshold:.2f}"
                    if best_fact else "no candidate KFR facts in temporal window"
                ),
            ))
            continue

        # 5) Verify value
        passes, delta_pct = _verify_value(claim.number, best_fact)
        if not passes:
            findings.append(FactDriftFinding(
                claim_token=claim.raw_token,
                claim_value=claim.number,
                claim_sentence=claim.sentence,
                nearest_fact_id=best_fact.id,
                nearest_fact_value=best_fact.value if best_fact.is_numeric else None,
                delta_pct=delta_pct,
                reason_tag=_REASON_VALUE_DRIFT,
                detail=(
                    f"draft={claim.number}, KFR.value={best_fact.value}, "
                    f"delta={delta_pct:.2f}% > tolerance={best_fact.display_tolerance_pct}%"
                ),
            ))

    if findings:
        return FactDriftGateResult(
            verdict="FAIL",
            failure_code=F_LOGICIAN_FACT_DRIFT,
            findings=tuple(findings),
            claim_count_extracted=len(claims),
            claim_count_drifted=len(findings),
        )

    return FactDriftGateResult(
        verdict="PASS",
        claim_count_extracted=len(claims),
        claim_count_drifted=0,
    )


__all__ = [
    "F_LOGICIAN_FACT_DRIFT",
    "MATCH_JACCARD_THRESHOLD",
    "DEFAULT_VALUE_TOLERANCE_PCT",
    "TemporalWindow",
    "ValidationBlock",
    "KfrFact",
    "KeyFactsRegister",
    "NumericClaim",
    "FactDriftFinding",
    "FactDriftGateResult",
    "KfrSchemaError",
    "load_kfr",
    "extract_numeric_claims",
    "check_fact_drift",
]
