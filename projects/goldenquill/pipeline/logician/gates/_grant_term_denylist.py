"""pipeline.logician.gates._grant_term_denylist — grant-domain false-positive
denylist for spaCy NER ORG suppression.

Pattern source
--------------
Adapted from MIT-licensed `linkedin_ssi_booster`
(github.com/samjd-zz/linkedin_ssi_booster, ``services/console_grounding/
_gate_helpers.py:289-321``). Their ``_CONCEPT_ABBREVS`` + ``_TECH_VERSION_PREFIXES``
suppression pattern catches spaCy NER false-positives where common
abbreviations (``LLM``, ``S3``, ``OAuth``) and tech-version strings
("Java 21") get tagged ``ORG``. We reuse the *pattern* with grant-domain
content.

Why this exists before the gate that consumes it
-------------------------------------------------
The future ``F-LOGICIAN-FABRICATED-ORG`` gate (queued, not yet built) will
extract ``ORG`` entities from a Scribe draft via spaCy NER and verify each
appears in ``orgs/<slug>/PROJECT_CONTEXT.md``. Without an upstream denylist,
the gate would emit false positives for every grant draft that says "USDA
NIFA", "Title VII", "7 CFR 1.1", "VAPG", "501(c)(3)", etc. — these are
agency abbreviations, regulation citations, program acronyms, and
entity-type strings that spaCy's general-domain NER mislabels as
organisations.

This module is **data + predicates only**. It ships zero gate logic. When
the fabricated-ORG gate lands it will import the predicates and apply them
upstream of its PROJECT_CONTEXT cross-check.

Categories (frozensets)
-----------------------
1. Federal agency abbreviations (USDA, NIFA, NRCS, EPA, etc.) — separate
   set so a future gate can decide policy (skip-by-default vs require
   PROJECT_CONTEXT membership).
2. Grant program abbreviations (VAPG, REAP, EQIP, SARE, AFRI, SCBGP, etc.)
3. Sector / demographic / entity-type abbreviations (SDA, MTVC, BIPOC,
   501c3, L3C, etc.)
4. Ag / food / regen-ag concept abbreviations (FSMA, GAP, IPM, HACCP, ROC)
5. Workforce / education abbreviations (WIOA, TANF, STEM, MWBE)
6. Generic-tech concept abbreviations (AI, LLM, API, SDK) — common in
   workforce-of-the-future and eco-art draft contexts.

Categories (regex patterns)
---------------------------
- ``Title VII`` / ``Section 9007`` / ``Subpart B`` etc.
- ``7 CFR 1.1`` / ``2 CFR 200`` / ``7 USC 6502``
- ``Pub. L. 117-58`` / ``Public Law 117-58``
- ``FY 2026`` / ``FY26`` / ``FY-2026``
- ``RFA-26-XXX`` / ``NOFO-...`` / ``FOA-...`` / ``BAA-...``
- ``501(c)(3)`` / ``501(c)(6)`` etc.

Sovereignty / dependency posture
--------------------------------
Pure-Python frozensets + ``re.compile`` patterns. Zero deps beyond stdlib.
No spaCy import here — spaCy lives in the future gate that consumes these
predicates, not in the denylist module itself. Keeps the substrate
locked-stdlib (``pyproject.toml`` § ``[project]``).

Extension points
----------------
The denylist is starter content. Expected to grow as Logician sees
field-data false positives. Add to the frozenset literal below — every
addition is a single-line diff with no behavioural side effects elsewhere
(the predicates union the sets at module load).
"""

from __future__ import annotations

import re
from typing import Final

# --------------------------------------------------------------------------
# Federal agency abbreviations
#
# Kept as a separate set from the main denylist so a future gate can choose
# policy: short-circuit-skip (federal agencies are the funder, never a
# fabricated partnership) OR require PROJECT_CONTEXT to enumerate funders
# explicitly. The denylist module takes no position; it exposes the data.
# --------------------------------------------------------------------------

_FEDERAL_AGENCY_ABBREVS: Final[frozenset[str]] = frozenset({
    # USDA family
    "USDA", "NIFA", "NRCS", "FSA", "RBS", "RD", "FNS", "AMS", "ARS", "ERS",
    "FAS", "APHIS", "FSIS", "OSEC", "REE", "OCE", "OCIO",
    # Other cabinet-level departments
    "HUD", "EPA", "DOL", "DOE", "DOI", "DHS", "DOT", "ED", "HHS", "VA",
    # Independent / specialized federal
    "SBA", "NSF", "NIH", "USAID", "BLM", "USFS", "USFWS", "NOAA", "NPS",
    "FEMA", "CDC", "FDA", "NEA", "NEH", "IMLS",
    # Treasury / financial
    "IRS", "OFAC", "FinCEN", "CDFI",
    # International (cross-border regen-ag work)
    "FAO", "UNDP", "UNESCO", "WHO", "AAFC",
})

# --------------------------------------------------------------------------
# Grant / program abbreviations (USDA + adjacent)
#
# Programs are *not* organisations even when spaCy NER labels them ``ORG``.
# These belong in the main denylist — the fabricated-ORG gate should
# unconditionally skip them.
# --------------------------------------------------------------------------

_PROGRAM_ABBREVS: Final[frozenset[str]] = frozenset({
    # USDA grants — production / value-add
    "VAPG", "LFPP", "FMPP", "FINI", "GUSNIP", "MPPEP", "DRP",
    # USDA grants — energy / rural development
    "REAP", "REDLG", "RBDG", "RBIG", "RBOG", "SEARCH",
    # USDA — conservation
    "EQIP", "CSP", "CRP", "FRPP", "ACEP", "RCPP", "CIG", "WLFW", "WHIP",
    # USDA — research / extension
    "SARE", "AFRI", "SBIR", "STTR", "OREI",
    # USDA — specialty / local / underserved
    "SCBGP", "CFP", "BFRDP", "OASDVFR", "SDFR", "FOTO",
    # Workforce / community development
    "WIOA", "TANF", "CDBG", "EDA",
})

# --------------------------------------------------------------------------
# Sector / demographic / entity-type abbreviations
# --------------------------------------------------------------------------

_DEMOGRAPHIC_ABBREVS: Final[frozenset[str]] = frozenset({
    # Producer / community designations
    "SDA", "MTVC", "BIPOC", "LMI", "CCC", "FCIC",
    # Entity types — community / mission
    "CBO", "NGO", "MWBE", "DBE", "WBE", "MBE",
    # Tax / legal entity types
    # NOTE: '501(c)(3)' matches via the punctuation-normalize predicate
    # (see is_grant_concept_token) and via the _501C_RE regex.
    "501c3", "501c6", "L3C", "B-Corp", "S-Corp", "C-Corp",
    "LLC", "LLP", "PLLC", "EIN",
    # Education / workforce
    "STEM", "STEAM", "GED", "ESL", "ELL", "IEP",
})

# --------------------------------------------------------------------------
# Ag / food / regen-ag concept abbreviations
# --------------------------------------------------------------------------

_AG_CONCEPT_ABBREVS: Final[frozenset[str]] = frozenset({
    # Food safety / standards
    "FSMA", "HACCP", "GAP", "GMP", "GHP", "GACP",
    # Crop / soil / pest practices
    "IPM", "ITM", "ROC", "SOM", "CEC", "SHI", "AWC", "NOP", "GMO",
    # Insurance / risk
    "WFRP", "NAP",
})

# --------------------------------------------------------------------------
# Generic-tech concept abbreviations (preserved from upstream pattern)
# --------------------------------------------------------------------------

_GENERIC_CONCEPT_ABBREVS: Final[frozenset[str]] = frozenset({
    # AI / ML
    "AI", "ML", "DL", "NLP", "LLM", "LLMs", "RAG", "AGI",
    # API / web / data
    "API", "APIs", "SDK", "CLI", "UI", "UX", "DB", "SQL", "NoSQL",
    "REST", "gRPC", "OAuth", "JWT", "HTTPS", "HTTP",
    "GraphQL", "OpenAPI", "JSON", "YAML", "XML", "CSV",
    # Business / accounting
    "ESG", "CSR", "DEI", "DEIA", "KPI", "ROI", "NPV", "IRR",
    "TAM", "SAM", "SOM", "FTE", "P&L", "YOY", "CAGR", "ARR", "MRR",
})

# --------------------------------------------------------------------------
# Aggregate denylist (single-token lookup)
#
# Federal agencies are intentionally NOT included — the consuming gate may
# want different policy for "agency mention" vs "concept mention".
# --------------------------------------------------------------------------

_GRANT_CONCEPT_DENYLIST: Final[frozenset[str]] = (
    _PROGRAM_ABBREVS
    | _DEMOGRAPHIC_ABBREVS
    | _AG_CONCEPT_ABBREVS
    | _GENERIC_CONCEPT_ABBREVS
)

# Case-folded variant for punctuation-normalized lookup. Built once at
# module load. Used so '501(C)(6)' (operator capitalises differently than
# the canonical '501c6') still matches.
_GRANT_CONCEPT_DENYLIST_CASEFOLDED: Final[frozenset[str]] = frozenset(
    m.casefold() for m in _GRANT_CONCEPT_DENYLIST
)

# --------------------------------------------------------------------------
# Citation / regulation regex patterns
# --------------------------------------------------------------------------

# "Title VII", "Section 9007", "Subpart B", "Part 200", "Article III".
# Third group accepts: number (200), Roman numeral (VII), or single uppercase
# letter (B) — Subparts in CFR are typically lettered.
_TITLE_SECTION_RE: Final[re.Pattern[str]] = re.compile(
    r"^(Title|Section|Subpart|Part|Chapter|Article)\s+"
    r"(\d+|[IVXLCDM]+|[A-Z])\b",
    re.IGNORECASE,
)

# "7 CFR 1.1", "2 CFR 200", "7 USC 6502", "7 U.S.C. 6502".
# Trailing lookahead (not \b) — \b can't fire between two non-word chars
# (e.g. "." then " ") which is exactly what "U.S.C." gives us.
_CFR_USC_RE: Final[re.Pattern[str]] = re.compile(
    r"^\d+\s+(CFR|USC|U\.S\.C\.?)(?=\s|$)",
    re.IGNORECASE,
)

# "Pub. L. 117-58", "Public Law 117-58"
_PUB_LAW_RE: Final[re.Pattern[str]] = re.compile(
    r"^(Pub\.?\s*L\.?|Public\s+Law)\s+\d+",
    re.IGNORECASE,
)

# "FY 2026", "FY26", "FY-2026"
_FY_RE: Final[re.Pattern[str]] = re.compile(
    r"^FY[\s-]?(20)?\d{2}\b",
    re.IGNORECASE,
)

# "RFA-26-XXX", "NOFO 26-...", "FOA-25-...", "BAA-...", "RFI-...", "RFP-..."
_RFA_NOFO_RE: Final[re.Pattern[str]] = re.compile(
    r"^(RFA|NOFO|FOA|BAA|RFI|RFP)[\s-]?\d",
    re.IGNORECASE,
)

# "501(c)(3)", "501(c)(6)" etc.
_501C_RE: Final[re.Pattern[str]] = re.compile(
    r"^501\s*\(\s*c\s*\)\s*\(\s*\d+\s*\)$",
    re.IGNORECASE,
)


# --------------------------------------------------------------------------
# Public predicates
# --------------------------------------------------------------------------

def _normalize_punctuation(text: str) -> str:
    """Strip whitespace, parens, periods for abbreviation lookup.

    ``501(c)(3)`` → ``501c3``. ``Pub. L.`` → ``PubL``. Used so denylist
    members stored bare (``501c3``) match the punctuated forms a draft
    actually contains (``501(c)(3)``).
    """
    return re.sub(r"[\s.()]+", "", text)


def is_grant_concept_token(text: str) -> bool:
    """Return True if *text* is a known grant-domain abbreviation/concept.

    A True result means downstream NER ORG checks should *skip* this token —
    it is not an organisation name even if spaCy NER tagged it ``ORG``.

    Matches:
    - bare form (``USDA``, ``VAPG``, ``LLM``)
    - punctuation-normalised form (``501(c)(3)`` → ``501c3``)
    - multi-word strings where every token is a known concept
      (``USDA NIFA`` → both tokens hit; ``USDA NRCS`` → both tokens hit)

    Federal agency abbreviations are *not* matched by this predicate — use
    :func:`is_federal_agency` for that. The split lets a future gate apply
    different policy to agency mentions vs program mentions.
    """
    if not text:
        return False

    stripped = text.strip()

    if stripped in _GRANT_CONCEPT_DENYLIST:
        return True

    # Punctuation-stripped + case-folded lookup. Handles '501(C)(6)' →
    # '501c6' regardless of operator capitalisation.
    normalised = _normalize_punctuation(stripped).casefold()
    if normalised in _GRANT_CONCEPT_DENYLIST_CASEFOLDED:
        return True

    tokens = stripped.split()
    if len(tokens) > 1 and all(
        tok in _GRANT_CONCEPT_DENYLIST
        or _normalize_punctuation(tok).casefold()
        in _GRANT_CONCEPT_DENYLIST_CASEFOLDED
        for tok in tokens
    ):
        return True

    return False


def is_federal_agency(text: str) -> bool:
    """Return True if *text* is a known US federal agency abbreviation.

    Used by callers that want to apply distinct policy to agency mentions
    (the funder is implicitly known) vs program / concept mentions.
    Multi-word inputs match if every token is a known agency
    (``USDA NRCS`` → True).
    """
    if not text:
        return False

    stripped = text.strip()

    if stripped in _FEDERAL_AGENCY_ABBREVS:
        return True

    tokens = stripped.split()
    if len(tokens) > 1 and all(
        tok in _FEDERAL_AGENCY_ABBREVS for tok in tokens
    ):
        return True

    return False


def is_regulation_citation(text: str) -> bool:
    """Return True if *text* matches a regulation / statute / citation pattern.

    Handles ``Title VII``, ``Section 9007``, ``Subpart B``, ``7 CFR 1.1``,
    ``Pub. L. 117-58``, ``FY 2026``, ``RFA-26-001``, ``501(c)(3)``.
    """
    if not text:
        return False

    stripped = text.strip()

    return any(
        pat.match(stripped)
        for pat in (
            _TITLE_SECTION_RE,
            _CFR_USC_RE,
            _PUB_LAW_RE,
            _FY_RE,
            _RFA_NOFO_RE,
            _501C_RE,
        )
    )


def is_grant_domain_non_org(text: str) -> bool:
    """Convenience predicate — True when the candidate is *definitely not* an org.

    Single entry point for the future fabricated-ORG gate. Returns True iff
    the input is a denylist concept OR a regulation/citation pattern.
    Federal agencies are deliberately excluded — the gate may want to flag
    agency mentions absent from PROJECT_CONTEXT (operator should declare
    funders explicitly).
    """
    return is_grant_concept_token(text) or is_regulation_citation(text)


__all__ = [
    "is_grant_concept_token",
    "is_federal_agency",
    "is_regulation_citation",
    "is_grant_domain_non_org",
]
