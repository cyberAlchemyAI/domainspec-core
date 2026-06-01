"""pipeline.seats.scribe.kgie — §7.4 KGIE preflight predicate.

Blueprint §7 Scribe v1.1.1 LOCKED 2026-04-21, §7.4. Pure deterministic
predicate — zero Vault I/O, zero filesystem reads, zero LLM calls.

Input:
- ``rfa``: an already-constructed :class:`RfaExtractedRecord` (Phase 0 output).
- ``project_context``: mapping parsed from ``orgs/<slug>/PROJECT_CONTEXT.md``.
  Expected shape documented in the helper bodies below; operator-hand-populated
  at v0.1, parser at v0.2.
- ``operator_affirmations``: mapping from RFA key_term → affirmation literal.
  Missing keys → ``"unanswered"``.
- ``clock``: injected-callable (E-017) returning timezone-aware utc datetime.

Output: :class:`KgiePreflightResult` with ``status`` ∈ {pass, fail,
needs_operator_input}. Caller inspects ``status``; Logician PRE-gate
``F-SCRIBE-KGIE-FAIL`` reads ``status == "fail"``.

Policy: this predicate NEVER raises on missing data. "No data" routes to
``needs_operator_input``. "Invalid data" routes to ``fail``. Raising would
conflate the two and violate the §7.4 tri-state pin.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable, Mapping

from pipeline.seats.scribe.types import (
    ExperienceSummary,
    GeographyRecord,
    IdentityClaim,
    KeywordAffirmation,
    KeywordCheck,
    KgiePreflightResult,
    RfaExtractedRecord,
)

# ---------------------------------------------------------------------------
# Public clock type alias — injected-callable seam per E-017.
# ---------------------------------------------------------------------------

ClockFn = Callable[[], datetime]


def _default_utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


# ---------------------------------------------------------------------------
# Private per-dimension builders
# ---------------------------------------------------------------------------


def _build_keyword_checks(
    rfa: RfaExtractedRecord,
    project_context: Mapping[str, Any],
    operator_affirmations: Mapping[str, KeywordAffirmation],
    needed: list[str],
) -> tuple[KeywordCheck, ...]:
    """K — one check per RFA key_term. Missing affirmation → needs_input."""
    checks: list[KeywordCheck] = []
    for term in rfa.key_terms:
        raw = operator_affirmations.get(term, "unanswered")
        # Defensive: coerce unknown values to "unanswered" rather than
        # allowing KeywordCheck.__post_init__ to raise. The KGIE predicate
        # never raises on bad data; it routes the gap into needed_fields.
        if raw not in ("affirmed", "not_applicable_with_reason", "unanswered"):
            raw = "unanswered"
        affirm: KeywordAffirmation = raw  # type: ignore[assignment]
        source: str | None = None
        na_reason: str | None = None
        if affirm == "affirmed":
            # Source inferred from project_context: look for a field that
            # mentions the term. Operator supplies the pointer explicitly
            # via project_context["keyword_sources"][term] when available;
            # otherwise we use a synthetic trace anchor.
            sources_map = project_context.get("keyword_sources", {})
            src = sources_map.get(term) if isinstance(sources_map, Mapping) else None
            source = str(src) if src else f"PROJECT_CONTEXT:keyword_sources:{term}"
        elif affirm == "not_applicable_with_reason":
            reasons_map = project_context.get("keyword_na_reasons", {})
            reason = (
                reasons_map.get(term) if isinstance(reasons_map, Mapping) else None
            )
            # If reason is missing, degrade to unanswered — never construct
            # an invalid KeywordCheck.
            if not reason:
                affirm = "unanswered"
            else:
                na_reason = str(reason)
        if affirm == "unanswered":
            needed.append(f"kgie.K:{term}")
        checks.append(
            KeywordCheck(
                term=term,
                applicant_affirmation=affirm,
                source=source,
                na_reason=na_reason,
            )
        )
    return tuple(checks)


def _build_geography_record(
    rfa: RfaExtractedRecord,
    project_context: Mapping[str, Any],
    needed: list[str],
) -> GeographyRecord:
    """G — state / county / zones / Justice40 from project_context.location."""
    loc = project_context.get("location", {})
    if not isinstance(loc, Mapping):
        loc = {}

    state_raw = loc.get("state")
    state = str(state_raw).upper() if state_raw else ""
    if len(state) != 2 or not state.isalpha():
        needed.append("kgie.G:state")
        state = "ZZ"  # sentinel; paired with match=False below

    county_raw = loc.get("county")
    county = str(county_raw).strip() if county_raw else ""
    if not county:
        needed.append("kgie.G:county")
        county = "UNKNOWN"

    zone_tags_raw = loc.get("zone_tags", ())
    if isinstance(zone_tags_raw, (list, tuple)):
        zone_tags = tuple(str(z) for z in zone_tags_raw)
    else:
        zone_tags = ()

    justice40 = loc.get("justice40_tract")
    justice40_tract: str | None = (
        str(justice40) if justice40 else None
    )

    # rfa_geographic_match: True iff state is in RFA's allowed zones (when
    # enumerated in RFA.key_terms["allowed_states"] or similar). At v0.1 the
    # operator supplies this via project_context["rfa_geographic_match"] as
    # a boolean. Missing → default False (honest); missing AND state unknown
    # → needed_fields already carries the gap.
    match_raw = project_context.get("rfa_geographic_match", None)
    rfa_match = bool(match_raw) if match_raw is not None else False
    if match_raw is None and "kgie.G:state" not in needed:
        needed.append("kgie.G:rfa_geographic_match")

    return GeographyRecord(
        state=state,
        county=county,
        zone_tags=zone_tags,
        justice40_tract=justice40_tract,
        rfa_geographic_match=rfa_match,
    )


def _build_identity_claims(
    rfa: RfaExtractedRecord,
    project_context: Mapping[str, Any],
    needed: list[str],
) -> tuple[tuple[IdentityClaim, ...], bool]:
    """I — identity_affirmations from project_context.

    Returns ``(claims, has_identity_gap)``. ``has_identity_gap`` is True iff
    any claim lacks a source_field — Law 5 fail condition.
    """
    affirmations = project_context.get("identity_affirmations", ())
    if not isinstance(affirmations, (list, tuple)):
        return ((), False)

    claims: list[IdentityClaim] = []
    has_gap = False
    for entry in affirmations:
        if not isinstance(entry, Mapping):
            continue
        claim_text_raw = entry.get("claim")
        if not claim_text_raw:
            continue
        claim_text = str(claim_text_raw)
        source_field = str(entry.get("source_field", "") or "")
        priority_points_raw = entry.get("rfa_priority_points", 0)
        try:
            priority_points = int(priority_points_raw)
        except (TypeError, ValueError):
            priority_points = 0
            needed.append(f"kgie.I:{claim_text}:priority_points")
        if priority_points < 0:
            priority_points = 0
        if not source_field.strip():
            has_gap = True
        claims.append(
            IdentityClaim(
                claim=claim_text,
                source_field_in_project_context=source_field,
                rfa_priority_points=priority_points,
            )
        )
    return (tuple(claims), has_gap)


def _build_experience_summary(
    project_context: Mapping[str, Any],
    needed: list[str],
) -> tuple[ExperienceSummary, bool]:
    """E — experience fields. Critical-gap = 0 years AND no certs AND no partners."""
    exp = project_context.get("experience", {})
    if not isinstance(exp, Mapping):
        exp = {}

    years_raw = exp.get("years_operating")
    try:
        years = int(years_raw) if years_raw is not None else 0
    except (TypeError, ValueError):
        years = 0
        needed.append("kgie.E:years_operating")
    if years < 0:
        years = 0

    production = exp.get("production_metrics", {})
    if not isinstance(production, Mapping):
        production = {}
    production_map = {str(k): str(v) for k, v in production.items()}

    prior_grants_raw = project_context.get("prior_grants", ())
    if isinstance(prior_grants_raw, (list, tuple)):
        prior_grants = tuple(str(g) for g in prior_grants_raw)
    else:
        prior_grants = ()

    certs_raw = exp.get("certifications", ())
    certifications = (
        tuple(str(c) for c in certs_raw)
        if isinstance(certs_raw, (list, tuple))
        else ()
    )

    partners_raw = exp.get("partnerships", ())
    partnerships = (
        tuple(str(p) for p in partners_raw)
        if isinstance(partners_raw, (list, tuple))
        else ()
    )

    # E critical gap: newly-founded entity with no credentials AND no
    # partnerships. Per spec-card OQ-4, threshold pinned at v0.1: zero-year
    # operation WITHOUT certifications AND WITHOUT partnerships = fail.
    has_critical_gap = (
        years == 0
        and len(certifications) == 0
        and len(partnerships) == 0
        and len(prior_grants) == 0
    )

    summary = ExperienceSummary(
        years_operating=years,
        production_metrics=production_map,
        prior_grants=prior_grants,
        certifications=certifications,
        partnerships=partnerships,
    )
    return (summary, has_critical_gap)


# ---------------------------------------------------------------------------
# Public predicate
# ---------------------------------------------------------------------------


def kgie_preflight(
    rfa: RfaExtractedRecord,
    project_context: Mapping[str, Any],
    operator_affirmations: Mapping[str, KeywordAffirmation],
    *,
    clock: ClockFn = _default_utc_now,
) -> KgiePreflightResult:
    """Run KGIE preflight over an extracted RFA + project context.

    Pure function — no I/O, no globals mutation. Deterministic under a
    fixed ``clock`` callable.

    Status dispatch (§7.4 pin):
    - ``"needs_operator_input"`` — any gap in needed_fields.
    - ``"fail"`` — no gaps but evidence invalid (missing identity source,
      E critical gap, or RFA geographic mismatch).
    - ``"pass"`` — every dimension present and valid.
    """
    needed: list[str] = []

    keyword_checks = _build_keyword_checks(
        rfa, project_context, operator_affirmations, needed
    )
    geography = _build_geography_record(rfa, project_context, needed)
    identities, has_identity_gap = _build_identity_claims(
        rfa, project_context, needed
    )
    experience, has_experience_gap = _build_experience_summary(
        project_context, needed
    )

    if needed:
        status = "needs_operator_input"
    elif (
        has_identity_gap
        or has_experience_gap
        or not geography.rfa_geographic_match
    ):
        status = "fail"
    else:
        status = "pass"

    return KgiePreflightResult(
        status=status,
        keywords_checked=keyword_checks,
        geography_verified=geography,
        identity_claims=identities,
        experience_summary=experience,
        needed_fields=tuple(needed),
        preflight_at_utc=clock(),
    )


__all__ = ["ClockFn", "kgie_preflight"]
