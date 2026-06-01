"""F-LOGICIAN-FABRICATED-ORG — POST-gate on Scribe drafts.

Catches fabricated organisation names in Scribe output. Complements the
existing Law 5 verbatim-substring gate (which catches fabricated
credentials / data as literal strings) by targeting a specific failure
mode: invented partnerships and collaborations that name real-sounding
organisations not present in PROJECT_CONTEXT.md.

Example catch
-------------
Scribe drafts "in partnership with Penn State Extension" but Penn State
Extension is not listed in the client's PROJECT_CONTEXT.md partners,
collaborators, or fiscal-sponsor fields. Gate fires
``F-LOGICIAN-FABRICATED-ORG`` and DENIES promotion.

Pipeline
--------
1. **Extract.** spaCy NER (``en_core_web_sm``) extracts all ``ORG``
   entities from Scribe draft text.
2. **Denylist filter.** Each extracted ORG is run through
   ``pipeline.logician.gates._grant_term_denylist`` predicates. Concept
   tokens (VAPG, LLM, 501c3) and citation patterns (Title VII, 7 CFR 1.1)
   are dropped — they are not orgs even when spaCy NER labels them ORG.
3. **Allowlist build.** Walk PROJECT_CONTEXT mapping for known org names —
   applicant, partners, collaborators, fiscal sponsor, subawardees,
   letters-of-support, prior partners. Optionally union with
   ``rfa_issuer`` (the funder agency, always a valid mention) and the
   federal-agency frozenset from the denylist module
   (auto_allow_federal_agencies, default True).
4. **Fuzzy set-membership.** Each surviving ORG must appear in the
   allowlist within Levenshtein ratio ≥ 0.85 (default; configurable).
   Lowercase + whitespace-collapse normalisation applied to both sides.
5. **Verdict.** Any ORG that fails membership → DENY with
   ``F-LOGICIAN-FABRICATED-ORG`` and the per-finding sentence context +
   nearest-allowlist match for operator review.

Properties
----------
- **Deterministic:** spaCy NER is a fixed model + seeded; rapidfuzz
  Levenshtein is deterministic. Zero LLM tokens.
- **Fail-closed:** unmatched ORG → DENY. Operator override is via the
  M13 bypass mechanism (audited), not silent suppression.
- **Lazy deps:** ``spacy`` and ``rapidfuzz`` import inside the entry
  function; module imports cleanly without them. Missing dep → DENY with
  reason ``dependency_unavailable``.
- **Pure-Python denylist:** the upstream concept-token / regulation-
  citation filter requires no model, so denylist refinement does not
  block on spaCy availability.

Spec card
---------
``pipeline/engineering/spec_cards/logician_fabricated_org_ner_gate.md``
v1, 2026-05-06.

Blueprint anchor
----------------
``pipeline/blueprint/v0.1/section_04_logician.md`` — Logician POST-gate
battery; Law 5 (Applicant Brings Substance) complementary surface.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final, Iterable, Literal, Mapping, Optional

from pipeline.logician.gates._grant_term_denylist import (
    is_federal_agency,
    is_grant_domain_non_org,
)

# --------------------------------------------------------------------------
# Public failure code + tunables
# --------------------------------------------------------------------------

F_LOGICIAN_FABRICATED_ORG: Final[str] = "F-LOGICIAN-FABRICATED-ORG"

DEFAULT_FUZZY_THRESHOLD: Final[float] = 0.85

# Project-context fields walked for org-name allowlist build. Operators
# can override via the explicit `allowlist_fields` arg; this default
# matches the v0.1 PROJECT_CONTEXT.md schema commonly populated by
# operators per CLAUDE.md guidance.
DEFAULT_ALLOWLIST_FIELDS: Final[tuple[str, ...]] = (
    "applicant_name",
    "applicant_legal_name",
    "applicant_org",
    "applicant",
    "partners",
    "collaborators",
    "subawardees",
    "sub_awardees",
    "fiscal_sponsor",
    "letters_of_support",
    "prior_partners",
    "matching_partners",
    "host_organization",
    "host_org",
    "funder",
)


# --------------------------------------------------------------------------
# Reason tags
# --------------------------------------------------------------------------

_REASON_FABRICATED_ORG: Final[str] = "fabricated_org_detected"
_REASON_DEPENDENCY_UNAVAILABLE: Final[str] = "dependency_unavailable"
_REASON_MODEL_LOAD_FAILED: Final[str] = "spacy_model_load_failed"


# --------------------------------------------------------------------------
# Result dataclasses
# --------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class FabricatedOrgFinding:
    """One ungrounded ORG mention with its sentence context."""

    org_name: str               # as extracted by spaCy NER
    sentence_context: str       # the sentence containing the ORG mention
    nearest_match: Optional[str]  # closest allowlist entry (if ratio > 0.5)
    match_ratio: float          # Levenshtein ratio to nearest allowlist entry


@dataclass(frozen=True, kw_only=True)
class FabricatedOrgGateResult:
    """POST-gate verdict."""

    verdict: Literal["PASS", "FAIL"]
    failure_code: Optional[str] = None
    reason_tag: Optional[str] = None
    findings: tuple[FabricatedOrgFinding, ...] = ()
    org_count_extracted: int = 0
    org_count_after_denylist: int = 0
    org_count_ungrounded: int = 0
    dependency_error: Optional[str] = None  # populated when a dep import failed


# --------------------------------------------------------------------------
# Lazy spaCy + rapidfuzz hookup
# --------------------------------------------------------------------------

# Module-level cache for the spaCy nlp object. None means "not loaded yet";
# False means "load attempted and failed — don't retry within this process".
# We use a tuple-cell pattern for thread-safety-ish (not strict, but
# adequate for the single-process subprocess design).
_NLP_CACHE: list[Any] = [None]
_NLP_LOAD_ERROR: list[Optional[str]] = [None]


def _try_load_spacy() -> tuple[Any, Optional[str]]:
    """Return (nlp, None) on success, (None, error_message) on failure.

    Tries ``spacy.load("en_core_web_sm")``. Caches both success and
    failure within the process — repeated calls within one Logician run
    don't pay the load cost twice and don't retry a known-broken install.
    """
    if _NLP_CACHE[0] is not None and _NLP_CACHE[0] is not False:
        return _NLP_CACHE[0], None
    if _NLP_CACHE[0] is False:
        return None, _NLP_LOAD_ERROR[0]

    try:
        import spacy  # noqa: F401  (lazy import per substrate-locked policy)
    except ImportError as exc:
        _NLP_CACHE[0] = False
        _NLP_LOAD_ERROR[0] = (
            f"spacy not installed: {exc}. "
            f"Install via `pip install 'tilth[fabricated_org]'` "
            f"(or add spacy>=3.7 + rapidfuzz>=3.0 to environment)."
        )
        return None, _NLP_LOAD_ERROR[0]

    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
    except OSError as exc:
        _NLP_CACHE[0] = False
        _NLP_LOAD_ERROR[0] = (
            f"en_core_web_sm model not installed: {exc}. "
            f"Run `python -m spacy download en_core_web_sm`."
        )
        return None, _NLP_LOAD_ERROR[0]
    except Exception as exc:  # pragma: no cover  (defensive: spacy internal failure)
        _NLP_CACHE[0] = False
        _NLP_LOAD_ERROR[0] = f"spacy.load raised {type(exc).__name__}: {exc}"
        return None, _NLP_LOAD_ERROR[0]

    _NLP_CACHE[0] = nlp
    return nlp, None


def _try_import_rapidfuzz() -> tuple[Any, Optional[str]]:
    """Return (rapidfuzz_ratio_fn, None) on success, (None, err) on failure."""
    try:
        from rapidfuzz import fuzz
    except ImportError as exc:
        return None, f"rapidfuzz not installed: {exc}"
    return fuzz.ratio, None


# --------------------------------------------------------------------------
# Core helpers
# --------------------------------------------------------------------------

def _normalise_org(text: str) -> str:
    """Lowercase + collapse whitespace + strip leading/trailing punctuation."""
    if not text:
        return ""
    lowered = text.lower().strip()
    # Collapse internal whitespace
    parts = lowered.split()
    collapsed = " ".join(parts)
    # Strip terminal punctuation common in NER output
    return collapsed.strip(".,;:!?'\"()[]{}")


def _walk_for_org_names(value: Any) -> Iterable[str]:
    """Yield org-name strings from a project_context field value.

    Handles:
    - bare string ("FIT Farms LLC")
    - list of strings (["FIT Farms LLC", "MycoSymbiotics Coop"])
    - list of dicts with `name` or `org_name` key
      ([{"name": "FIT Farms LLC", "role": "applicant"}, ...])
    - dict with `name` / `org_name` key
    """
    if value is None:
        return
    if isinstance(value, str):
        s = value.strip()
        if s:
            yield s
        return
    if isinstance(value, Mapping):
        for key in ("name", "org_name", "organization", "organisation"):
            if key in value and isinstance(value[key], str):
                s = value[key].strip()
                if s:
                    yield s
                    return  # one name per dict
        return
    if isinstance(value, (list, tuple)):
        for item in value:
            yield from _walk_for_org_names(item)
        return
    # Other types ignored — booleans, numbers, dataclasses without
    # explicit name fields are not org names by convention.


def build_org_allowlist(
    project_context: Mapping[str, Any],
    *,
    rfa_issuer: Optional[str] = None,
    auto_allow_federal_agencies: bool = True,
    fields: Optional[tuple[str, ...]] = None,
) -> frozenset[str]:
    """Build the normalised org-name allowlist from PROJECT_CONTEXT mapping.

    Walks the configured fields, collects org names, and returns a
    frozenset of normalised forms (lowercased + whitespace-collapsed +
    terminal-punctuation-stripped).

    Args:
        project_context: parsed PROJECT_CONTEXT data (matches the
            ScribeEnvelope.project_context shape).
        rfa_issuer: optional RFA-issuing agency name. Auto-added to the
            allowlist — the funder is always a valid mention.
        auto_allow_federal_agencies: when True (default), every federal
            agency abbreviation in the denylist's
            ``_FEDERAL_AGENCY_ABBREVS`` set is auto-allowed. Disable for
            strict-mode runs that require explicit operator declaration
            of every agency mentioned.
        fields: which top-level keys of project_context to walk.
            Defaults to :data:`DEFAULT_ALLOWLIST_FIELDS`.
    """
    allow: set[str] = set()
    use_fields = fields if fields is not None else DEFAULT_ALLOWLIST_FIELDS

    for field_name in use_fields:
        if field_name in project_context:
            for raw in _walk_for_org_names(project_context[field_name]):
                norm = _normalise_org(raw)
                if norm:
                    allow.add(norm)

    if rfa_issuer:
        norm = _normalise_org(rfa_issuer)
        if norm:
            allow.add(norm)

    if auto_allow_federal_agencies:
        # Import here so the agency set is available without exposing the
        # private name; we use the predicate plus a curated list. Simpler:
        # add the public predicate's domain by enumerating common funder
        # agency mentions via the predicate at evaluation time.
        # NOTE: we don't expand all 32 abbreviations into the allowlist
        # here; instead, the gate applies `is_federal_agency` as a check
        # alongside the allowlist lookup. See `check_fabricated_orgs`.
        pass

    return frozenset(allow)


def extract_org_entities(
    text: str,
    *,
    nlp: Any = None,
) -> tuple[str, ...]:
    """Extract ORG entities from *text* via spaCy NER.

    Returns the list of ORG strings as spaCy tagged them (original case
    preserved). Pass ``nlp=`` for test injection — when None, lazy-loads
    ``en_core_web_sm`` via :func:`_try_load_spacy`.

    Raises :class:`RuntimeError` when spaCy or the model is unavailable.
    Callers should guard with :func:`_try_load_spacy` first if they want
    a soft-fail path.
    """
    if not text:
        return ()

    if nlp is None:
        nlp, err = _try_load_spacy()
        if nlp is None:
            raise RuntimeError(err or "spacy load failed")

    doc = nlp(text)
    return tuple(ent.text for ent in doc.ents if ent.label_ == "ORG")


def _split_into_sentences(text: str) -> list[str]:
    """Lightweight sentence split — used to attach sentence-context to findings.

    spaCy can do this but we want a stdlib path so the helper is callable
    even when spaCy is unavailable (defensive).
    """
    if not text:
        return []
    # Period/!/? followed by whitespace — same shape as the regex used in
    # SSI-booster reference implementation. Conservative; doesn't handle
    # 'Dr.' / 'Inc.' etc. perfectly but good enough for finding context.
    import re
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s for s in sentences if s.strip()]


def _find_sentence_for(text: str, target: str) -> str:
    """Return the first sentence in *text* containing *target* (case-insensitive)."""
    sentences = _split_into_sentences(text)
    target_lower = target.lower()
    for sent in sentences:
        if target_lower in sent.lower():
            return sent.strip()
    return ""  # ORG not found in any sentence (shouldn't happen post-NER)


def _nearest_match(
    org_norm: str,
    allowlist: frozenset[str],
    *,
    ratio_fn: Any,
) -> tuple[Optional[str], float]:
    """Return (best_match, ratio) where ratio is 0-1 Levenshtein."""
    if not allowlist:
        return None, 0.0
    best_match: Optional[str] = None
    best_ratio = 0.0
    for entry in allowlist:
        # rapidfuzz returns 0-100; normalise to 0-1.
        r = ratio_fn(org_norm, entry) / 100.0
        if r > best_ratio:
            best_ratio = r
            best_match = entry
    return best_match, best_ratio


# --------------------------------------------------------------------------
# Public entry point
# --------------------------------------------------------------------------

def check_fabricated_orgs(
    *,
    draft_text: str,
    project_context: Mapping[str, Any],
    rfa_issuer: Optional[str] = None,
    fuzzy_threshold: float = DEFAULT_FUZZY_THRESHOLD,
    auto_allow_federal_agencies: bool = True,
    allowlist_fields: Optional[tuple[str, ...]] = None,
    nlp: Any = None,
    ratio_fn: Any = None,
) -> FabricatedOrgGateResult:
    """POST-gate F-LOGICIAN-FABRICATED-ORG.

    Args:
        draft_text: Scribe draft body to scan.
        project_context: parsed PROJECT_CONTEXT mapping (matches
            ``ScribeEnvelope.project_context`` shape).
        rfa_issuer: optional RFA-issuing agency name (auto-allowed).
        fuzzy_threshold: Levenshtein ratio floor for allowlist match.
            Default 0.85 per spec card.
        auto_allow_federal_agencies: skip federal agency mentions
            (USDA, NRCS, EPA, etc.) without requiring PROJECT_CONTEXT
            membership. Default True; disable for strict mode.
        allowlist_fields: override the project_context keys walked for
            org names. Defaults to :data:`DEFAULT_ALLOWLIST_FIELDS`.
        nlp: optional spaCy nlp object — for test injection. When None,
            lazy-loads ``en_core_web_sm``.
        ratio_fn: optional fuzzy ratio function (signature: str, str → 0-100).
            For test injection. When None, uses ``rapidfuzz.fuzz.ratio``.

    Returns:
        :class:`FabricatedOrgGateResult` with verdict + findings list.
        Empty draft → PASS with zero counts.
    """
    if not draft_text or not draft_text.strip():
        return FabricatedOrgGateResult(verdict="PASS")

    # Lazy-load deps. On failure: FAIL with dependency_unavailable.
    if nlp is None:
        nlp, nlp_err = _try_load_spacy()
        if nlp is None:
            return FabricatedOrgGateResult(
                verdict="FAIL",
                failure_code=F_LOGICIAN_FABRICATED_ORG,
                reason_tag=_REASON_DEPENDENCY_UNAVAILABLE,
                dependency_error=nlp_err,
            )
    if ratio_fn is None:
        ratio_fn, fz_err = _try_import_rapidfuzz()
        if ratio_fn is None:
            return FabricatedOrgGateResult(
                verdict="FAIL",
                failure_code=F_LOGICIAN_FABRICATED_ORG,
                reason_tag=_REASON_DEPENDENCY_UNAVAILABLE,
                dependency_error=fz_err,
            )

    # 1. NER extraction
    try:
        all_orgs = extract_org_entities(draft_text, nlp=nlp)
    except RuntimeError as exc:
        return FabricatedOrgGateResult(
            verdict="FAIL",
            failure_code=F_LOGICIAN_FABRICATED_ORG,
            reason_tag=_REASON_MODEL_LOAD_FAILED,
            dependency_error=str(exc),
        )

    if not all_orgs:
        return FabricatedOrgGateResult(
            verdict="PASS",
            org_count_extracted=0,
        )

    # 2. Denylist filter — drop concept tokens + citations
    survivors_after_denylist: list[str] = [
        org for org in all_orgs if not is_grant_domain_non_org(org)
    ]

    # 3. Build allowlist
    allowlist = build_org_allowlist(
        project_context,
        rfa_issuer=rfa_issuer,
        auto_allow_federal_agencies=auto_allow_federal_agencies,
        fields=allowlist_fields,
    )

    # 4. Allowlist check (with fuzzy threshold + federal-agency short-circuit)
    findings: list[FabricatedOrgFinding] = []
    for org in survivors_after_denylist:
        # Auto-allow federal agencies when configured
        if auto_allow_federal_agencies and is_federal_agency(org):
            continue

        org_norm = _normalise_org(org)
        if not org_norm:
            continue  # NER returned blank — nothing to verify

        # Direct membership
        if org_norm in allowlist:
            continue

        # Fuzzy membership
        nearest, ratio = _nearest_match(org_norm, allowlist, ratio_fn=ratio_fn)
        if ratio >= fuzzy_threshold:
            continue

        # Ungrounded — record finding
        findings.append(FabricatedOrgFinding(
            org_name=org,
            sentence_context=_find_sentence_for(draft_text, org),
            nearest_match=nearest if ratio >= 0.5 else None,
            match_ratio=ratio,
        ))

    if findings:
        return FabricatedOrgGateResult(
            verdict="FAIL",
            failure_code=F_LOGICIAN_FABRICATED_ORG,
            reason_tag=_REASON_FABRICATED_ORG,
            findings=tuple(findings),
            org_count_extracted=len(all_orgs),
            org_count_after_denylist=len(survivors_after_denylist),
            org_count_ungrounded=len(findings),
        )

    return FabricatedOrgGateResult(
        verdict="PASS",
        org_count_extracted=len(all_orgs),
        org_count_after_denylist=len(survivors_after_denylist),
        org_count_ungrounded=0,
    )


__all__ = [
    "F_LOGICIAN_FABRICATED_ORG",
    "DEFAULT_FUZZY_THRESHOLD",
    "DEFAULT_ALLOWLIST_FIELDS",
    "FabricatedOrgFinding",
    "FabricatedOrgGateResult",
    "build_org_allowlist",
    "extract_org_entities",
    "check_fabricated_orgs",
]
