"""pipeline.seats.scribe.dialect — §7.8 dialect code-switching primitives.

Blueprint §7 Scribe v1.1.1 §7.8 + §7.2 Law 5 LOCKED 2026-04-21. Pure data
+ pure predicates over draft text. Zero I/O, zero LLM, zero
external-package imports.

§7.8 pins four dialects (conservative / centrist / progressive / soul_fire)
with closed-set vocabulary tables. Vocabulary changes surface framing
ONLY — never substance. R3 Logician POST-gates ``F-SCRIBE-DIALECT-DRIFT``
and ``F-SCRIBE-DIALECT-INDUCED-IDENTITY`` consume the helpers below.

§7.2 Law 5 — ``DIALECT_IDENTITY_PROXY_TABLE`` is the §0.5 v7 row 124
closed-set of dialect-keyed identity-proxy phrases. A match requires a
corresponding ``KgiePreflightResult.identity_claims`` entry.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Final, Literal, Mapping

from pipeline.seats.scribe.types import IdentityClaim


Dialect = Literal["conservative", "centrist", "progressive", "soul_fire"]

_DIALECT_VALID: Final[frozenset[str]] = frozenset(
    {"conservative", "centrist", "progressive", "soul_fire"}
)


# §7.8 — closed-set vocabulary per dialect. Case-insensitive substring
# match is the drift-detection basis.
DIALECT_VOCABULARY: Final[Mapping[Dialect, frozenset[str]]] = MappingProxyType(
    {
        "conservative": frozenset(
            {
                "production efficiency",
                "economic impact",
                "market competitiveness",
                "return on investment",
                "food security",
            }
        ),
        "centrist": frozenset(
            {
                "balanced growth",
                "community resilience",
                "evidence-based",
                "public-private partnership",
            }
        ),
        "progressive": frozenset(
            {
                "equity",
                "food sovereignty",
                "environmental justice",
                "climate resilience",
                "community self-determination",
            }
        ),
        "soul_fire": frozenset(
            {
                "land rematriation",
                "ancestral knowledge",
                "healing justice",
                "community power",
                "liberation",
            }
        ),
    }
)


# §7.2 Law 5 — dialect-identity-proxy table. A phrase present in a draft
# under ``declared_dialect == key`` implies an identity claim whose text
# or label contains the mapped claim-label token. R3 POST-gate
# ``F-SCRIBE-DIALECT-INDUCED-IDENTITY`` checks this against
# ``KgiePreflightResult.identity_claims``.
#
# Keys are dialects; values are (phrase → implied_identity_claim_label)
# mappings. Both layers are frozen.
DIALECT_IDENTITY_PROXY_TABLE: Final[
    Mapping[Dialect, Mapping[str, str]]
] = MappingProxyType(
    {
        "conservative": MappingProxyType({}),
        "centrist": MappingProxyType({}),
        "progressive": MappingProxyType(
            {
                "historically marginalized": "marginalized-community",
                "historically excluded": "marginalized-community",
                "first-generation": "first-generation",
            }
        ),
        "soul_fire": MappingProxyType(
            {
                "my grandmother taught me": "ancestral-knowledge",
                "my grandmother taught us": "ancestral-knowledge",
                "elder wisdom": "ancestral-knowledge",
                "ancestral wisdom": "ancestral-knowledge",
                "ancestral lands": "ancestral-knowledge",
                "ancestral knowledge": "ancestral-knowledge",
                "indigenous knowledge": "indigenous-practitioner",
                "land back": "indigenous-practitioner",
            }
        ),
    }
)


def detect_dialect_drift(
    text: str,
    declared_dialect: Dialect,
) -> tuple[str, ...]:
    """§7.8 pin — return phrases from dialects OTHER than ``declared_dialect``
    present in ``text``.

    Empty tuple = no drift. Non-empty tuple = R3 POST-gate
    ``F-SCRIBE-DIALECT-DRIFT`` firing basis. Document-order preserved
    across dialects; duplicates dropped.
    """
    if declared_dialect not in _DIALECT_VALID:
        raise ValueError(
            f"detect_dialect_drift: declared_dialect must be one of "
            f"{sorted(_DIALECT_VALID)}; got {declared_dialect!r}."
        )
    if not isinstance(text, str) or not text:
        return ()
    found: list[str] = []
    seen: set[str] = set()
    lower = text.lower()
    for dialect, vocab in DIALECT_VOCABULARY.items():
        if dialect == declared_dialect:
            continue
        for phrase in sorted(vocab):  # deterministic order within a dialect
            if phrase.lower() in lower and phrase not in seen:
                found.append(phrase)
                seen.add(phrase)
    return tuple(found)


def detect_dialect_induced_identity(
    text: str,
    declared_dialect: Dialect,
    identity_claims: tuple[IdentityClaim, ...],
) -> tuple[str, ...]:
    """§7.2 Law 5 — return dialect-identity-proxy phrases present in text
    whose implied identity-label is NOT matched by any element of
    ``identity_claims``.

    Empty tuple = no induced-identity violation. Non-empty tuple = R3
    POST-gate ``F-SCRIBE-DIALECT-INDUCED-IDENTITY`` firing basis.

    Matching policy: the implied label token is case-insensitive-substring
    compared against each claim's ``claim`` text. Any claim match clears
    the phrase.
    """
    if declared_dialect not in _DIALECT_VALID:
        raise ValueError(
            f"detect_dialect_induced_identity: declared_dialect must be one "
            f"of {sorted(_DIALECT_VALID)}; got {declared_dialect!r}."
        )
    proxy_map = DIALECT_IDENTITY_PROXY_TABLE[declared_dialect]
    if not proxy_map or not isinstance(text, str) or not text:
        return ()
    claim_texts_lower = tuple(c.claim.lower() for c in identity_claims)
    violations: list[str] = []
    lower = text.lower()
    for phrase, implied_label in proxy_map.items():
        if phrase.lower() not in lower:
            continue
        label_lower = implied_label.lower()
        if not any(label_lower in ct for ct in claim_texts_lower):
            violations.append(phrase)
    return tuple(violations)


def select_default_dialect() -> Dialect:
    """§7.8 default — ``"conservative"`` / USDA Standard.

    R3 reads per-funder classification from the session manifest and falls
    back to this default when no classification is present and no operator
    override is supplied.
    """
    return "conservative"


__all__ = [
    "Dialect",
    "DIALECT_VOCABULARY",
    "DIALECT_IDENTITY_PROXY_TABLE",
    "detect_dialect_drift",
    "detect_dialect_induced_identity",
    "select_default_dialect",
]
