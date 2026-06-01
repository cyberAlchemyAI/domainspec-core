"""pipeline.seats.scribe.admin_risk_adapter — §7.11 admin-risk register consumption.

Spec card: ``pipeline/engineering/spec_cards/section_07_scribe_round_3_seat_entry_and_wiring.md``
§5 (admin-risk integration).

Consumes the canonical register at
``pipeline/institutional_memory/admin_risk_register.yaml`` (v2.2 APPROVED
2026-04-21) via an injected loader callable — NEVER raw ``open()``.

Two-axis dialect discipline (§5.2):

- Federal axis: ``severity`` ∈ {RED / YELLOW / GREEN} → HIGH / MEDIUM / LOW.
- Progressive axis: ``progressive_register`` ∈ {AVOID / OK / EXPECTED /
  PREFERRED}. Optional field — default ``OK`` when absent (legacy entry).

Flag-routing (§5.3):

- LOW (federal) + auto-substitute-allowed policy → silent substitution.
  Auto-substitute is a per-call policy flag, NOT a per-entry pre-approval
  (register v2.2 lacks a ``pre_approved`` field).
- MEDIUM or AVOID → always flag; POST-gate enforces presence of
  ``[ADMIN-RISK:...]`` comment.
- HIGH → always flag AND hard-block finalize until operator approves.

Applicant-identity overlay: when ``KgiePreflightResult.identity_claims``
matches the funder register, identity-affirming language flips from
flagged to EXPECTED/PREFERRED (no flag emitted).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any, Callable, Final, Iterable, Mapping, Protocol, Sequence

from pipeline.seats.scribe.section_draft import AdminRiskFlag, AdminRiskSeverity
from pipeline.seats.scribe.dialect import Dialect

# -- Failure-code constants. --
F_SCRIBE_ADMIN_RISK_REGISTER_STALE: Final[str] = "F-SCRIBE-ADMIN-RISK-REGISTER-STALE"
F_SCRIBE_ADMIN_RISK_UNFLAGGED: Final[str] = "F-SCRIBE-ADMIN-RISK-UNFLAGGED"
F_SCRIBE_ADMIN_RISK_HIGH_UNAPPROVED: Final[str] = "F-SCRIBE-ADMIN-RISK-HIGH-UNAPPROVED"
F_SCRIBE_ADMIN_RISK_REGISTER_MALFORMED: Final[str] = (
    "F-SCRIBE-ADMIN-RISK-REGISTER-MALFORMED"
)

# -- Snapshot-age ceiling (§7.16; V1 — human-reading only, dispatch inlines 24.0). --
SNAPSHOT_AGE_HOURS_CEILING: Final[float] = 24.0

# -- Severity mapping (register YAML → AdminRiskSeverity literal value). --
# ``AdminRiskSeverity`` is ``Literal["low","medium","high"]`` (see
# ``section_draft.py``), NOT an enum; use the literal string values.
_SEVERITY_YAML_TO_ENUM: Final[Mapping[str, AdminRiskSeverity]] = {
    "RED": "high",
    "YELLOW": "medium",
    "GREEN": "low",
}

# -- Progressive-register values. --
_VALID_PROGRESSIVE_REGISTER: Final[frozenset[str]] = frozenset(
    {"AVOID", "OK", "EXPECTED", "PREFERRED"}
)

# -- Per-CLC register values (architecture v7.0.12 §1.2). --
# Same enum as progressive_register, but keyed off CLC slug not political axis.
# v7.0.12 retires the four-axis political enum; CLC-keyed register state is the
# sanctioned replacement. Per-CLC defaults to AVOID for any CLC slug not listed
# on the entry's per_clc_register map (architecture v7.0.12 §1.2 "safest default").
_VALID_PER_CLC_REGISTER: Final[frozenset[str]] = frozenset(
    {"AVOID", "OK", "EXPECTED", "PREFERRED"}
)

# Closed set of CapitalLogicCard slugs per pipeline/types/identity_capital.py
# + admin_risk_register.schema.json $defs.capital_logic_card_slug (v7.0.8 / v7.0.12).
_VALID_CLC_SLUGS: Final[frozenset[str]] = frozenset(
    {
        "public_purpose_works",
        "catalytic_change",
        "operating_capacity",
        "research_evidence",
        "market_access",
        "credit_underwriting",
        "sponsorship_corporate",
        "shared_assets",
    }
)


# -- Exceptions. --


class AdminRiskRegisterStale(RuntimeError):
    """Snapshot age exceeds 24h ceiling. F-SCRIBE-ADMIN-RISK-REGISTER-STALE."""


class AdminRiskRegisterMalformed(RuntimeError):
    """Register YAML parse / shape / severity-mapping failure."""


class AdminRiskHighUnapproved(RuntimeError):
    """HIGH-severity flag without operator approval at finalize."""


# -- E-017 Protocols. --


class RegisterLoadCallable(Protocol):
    """Vault-primitive-gated register loader.

    Returns the top-level register mapping (``{"version": ..., "entries": [...]}``).
    """

    def __call__(self, *, register_path: str) -> Mapping[str, Any]: ...


# -- Shapes. --


@dataclass(frozen=True, kw_only=True, slots=True)
class AdminRiskEntry:
    """One canonicalized register entry.

    ``progressive_register`` is the retired v2.x dialect-axis field; per
    architecture v7.0.12 §1.2 (LOCKED 2026-05-16T14:00:00Z) it has been
    replaced by ``per_clc_register``. Legacy v2.x entries still carry it;
    new v2.4 / v3.0 entries omit it and populate ``per_clc_register``
    instead. Both fields are read here during the operator's v2.x → v3.0
    transition window so Scribe Phase-0 can serve both shapes without a
    fail-closed crash on legacy data.

    ``per_clc_register`` is a tuple of ``(clc_slug, register_value)`` pairs
    (frozen-dataclass-compatible). Empty tuple = AVOID-everywhere safest
    default per v7.0.12 §1.2. Use :func:`acceptable_under_clc` to look up
    a value safely.
    """

    term: str
    severity: AdminRiskSeverity
    progressive_register: str  # legacy v2.x axis; "AVOID" | "OK" | "EXPECTED" | "PREFERRED"
    suggested_substitutions: tuple[str, ...]
    context: str
    variants: tuple[str, ...]
    per_clc_register: tuple[tuple[str, str], ...] = ()
    """Per-CLC register state per architecture v7.0.12 §1.2.

    Tuple of ``(clc_slug, register_value)`` pairs. Empty = AVOID-everywhere.
    Values are validated against ``_VALID_PER_CLC_REGISTER``; slugs against
    ``_VALID_CLC_SLUGS`` (the closed set of 8 CapitalLogicCard slugs).
    """

    def __post_init__(self) -> None:
        if not self.term:
            raise ValueError("term must be non-empty")
        if self.progressive_register not in _VALID_PROGRESSIVE_REGISTER:
            raise ValueError(
                f"progressive_register must be one of "
                f"{sorted(_VALID_PROGRESSIVE_REGISTER)}; got {self.progressive_register!r}"
            )
        # Validate per_clc_register pairs (v7.0.12 §1.2).
        for pair in self.per_clc_register:
            if not (isinstance(pair, tuple) and len(pair) == 2):
                raise ValueError(
                    f"per_clc_register entries must be 2-tuples of "
                    f"(clc_slug, register_value); got {pair!r}"
                )
            clc, val = pair
            if clc not in _VALID_CLC_SLUGS:
                raise ValueError(
                    f"per_clc_register slug must be one of "
                    f"{sorted(_VALID_CLC_SLUGS)}; got {clc!r}"
                )
            if val not in _VALID_PER_CLC_REGISTER:
                raise ValueError(
                    f"per_clc_register value must be one of "
                    f"{sorted(_VALID_PER_CLC_REGISTER)}; got {val!r}"
                )


@dataclass(frozen=True, kw_only=True, slots=True)
class AdminRiskRegister:
    """Loaded register snapshot."""

    version: str
    entries: tuple[AdminRiskEntry, ...]
    snapshot_sha3_512: str
    snapshot_age_hours: float

    def __post_init__(self) -> None:
        if not self.version:
            raise ValueError("version must be non-empty")
        if len(self.snapshot_sha3_512) != 128:
            raise ValueError("snapshot_sha3_512 must be 128-hex")
        if self.snapshot_age_hours < 0:
            raise ValueError("snapshot_age_hours must be non-negative")


# -- Register load + parse. --


def parse_admin_risk_register(
    *,
    raw_mapping: Mapping[str, Any],
    snapshot_sha3_512: str,
    snapshot_age_hours: float,
) -> AdminRiskRegister:
    """Parse already-loaded YAML mapping into frozen AdminRiskRegister."""
    version = raw_mapping.get("version")
    if not isinstance(version, (str, int, float)):
        raise AdminRiskRegisterMalformed(
            f"{F_SCRIBE_ADMIN_RISK_REGISTER_MALFORMED}: missing/invalid 'version' field"
        )
    version_str = str(version)
    entries_raw = raw_mapping.get("entries")
    if not isinstance(entries_raw, list) or not entries_raw:
        raise AdminRiskRegisterMalformed(
            f"{F_SCRIBE_ADMIN_RISK_REGISTER_MALFORMED}: missing/empty 'entries' array"
        )
    entries: list[AdminRiskEntry] = []
    for i, e in enumerate(entries_raw):
        if not isinstance(e, Mapping):
            raise AdminRiskRegisterMalformed(
                f"{F_SCRIBE_ADMIN_RISK_REGISTER_MALFORMED}: entry #{i} is not a mapping"
            )
        term = e.get("term")
        if not isinstance(term, str) or not term:
            raise AdminRiskRegisterMalformed(
                f"{F_SCRIBE_ADMIN_RISK_REGISTER_MALFORMED}: entry #{i} missing 'term'"
            )
        severity_yaml = e.get("severity")
        if severity_yaml not in _SEVERITY_YAML_TO_ENUM:
            raise AdminRiskRegisterMalformed(
                f"{F_SCRIBE_ADMIN_RISK_REGISTER_MALFORMED}: entry #{i} 'severity' "
                f"invalid: {severity_yaml!r}; must be RED/YELLOW/GREEN"
            )
        severity = _SEVERITY_YAML_TO_ENUM[severity_yaml]
        progressive_register = e.get("progressive_register", "OK")
        if progressive_register not in _VALID_PROGRESSIVE_REGISTER:
            raise AdminRiskRegisterMalformed(
                f"{F_SCRIBE_ADMIN_RISK_REGISTER_MALFORMED}: entry #{i} "
                f"'progressive_register' invalid: {progressive_register!r}"
            )
        alternatives_raw = e.get("alternatives", [])
        if not isinstance(alternatives_raw, list):
            raise AdminRiskRegisterMalformed(
                f"{F_SCRIBE_ADMIN_RISK_REGISTER_MALFORMED}: entry #{i} "
                f"'alternatives' must be list"
            )
        alternatives = tuple(
            a for a in alternatives_raw if isinstance(a, str) and a.strip()
        )
        variants_raw = e.get("variants", [])
        if not isinstance(variants_raw, list):
            raise AdminRiskRegisterMalformed(
                f"{F_SCRIBE_ADMIN_RISK_REGISTER_MALFORMED}: entry #{i} "
                f"'variants' must be list"
            )
        variants = tuple(v for v in variants_raw if isinstance(v, str) and v.strip())
        context = e.get("context", "") or ""
        # per_clc_register (v7.0.12 §1.2). Optional; default empty tuple = AVOID-everywhere.
        raw_per_clc = e.get("per_clc_register")
        if raw_per_clc is None:
            per_clc_pairs: tuple[tuple[str, str], ...] = ()
        elif isinstance(raw_per_clc, Mapping):
            collected: list[tuple[str, str]] = []
            for clc, val in raw_per_clc.items():
                if not (isinstance(clc, str) and isinstance(val, str)):
                    raise AdminRiskRegisterMalformed(
                        f"{F_SCRIBE_ADMIN_RISK_REGISTER_MALFORMED}: entry #{i} "
                        f"'per_clc_register' has non-string key/value: "
                        f"({clc!r}, {val!r})"
                    )
                if clc not in _VALID_CLC_SLUGS:
                    raise AdminRiskRegisterMalformed(
                        f"{F_SCRIBE_ADMIN_RISK_REGISTER_MALFORMED}: entry #{i} "
                        f"'per_clc_register' has unknown CLC slug: {clc!r}"
                    )
                if val not in _VALID_PER_CLC_REGISTER:
                    raise AdminRiskRegisterMalformed(
                        f"{F_SCRIBE_ADMIN_RISK_REGISTER_MALFORMED}: entry #{i} "
                        f"'per_clc_register[{clc}]' invalid: {val!r}"
                    )
                collected.append((clc, val))
            per_clc_pairs = tuple(sorted(collected))
        else:
            raise AdminRiskRegisterMalformed(
                f"{F_SCRIBE_ADMIN_RISK_REGISTER_MALFORMED}: entry #{i} "
                f"'per_clc_register' must be a mapping if present"
            )
        entries.append(
            AdminRiskEntry(
                term=term,
                severity=severity,
                progressive_register=progressive_register,
                suggested_substitutions=alternatives,
                context=str(context),
                variants=variants,
                per_clc_register=per_clc_pairs,
            )
        )
    return AdminRiskRegister(
        version=version_str,
        entries=tuple(entries),
        snapshot_sha3_512=snapshot_sha3_512,
        snapshot_age_hours=snapshot_age_hours,
    )


def load_admin_risk_register(
    *,
    register_loader: RegisterLoadCallable,
    register_path: str,
    snapshot_age_hours: float,
    fail_closed_on_stale: bool = True,
) -> AdminRiskRegister:
    """Vault-gated register load + parse.

    Raises:
        AdminRiskRegisterStale: when fail_closed_on_stale and age > 24h.
        AdminRiskRegisterMalformed: parse / shape failure.
    """
    if fail_closed_on_stale and snapshot_age_hours > 24.0:  # inline literal V1
        raise AdminRiskRegisterStale(
            f"{F_SCRIBE_ADMIN_RISK_REGISTER_STALE}: snapshot age "
            f"{snapshot_age_hours}h exceeds 24h ceiling"
        )
    raw = register_loader(register_path=register_path)
    # Compute canonical sha3_512 over the raw payload (for audit).
    import json as _json

    try:
        canonical_bytes = _json.dumps(
            raw, separators=(",", ":"), sort_keys=True, default=str
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise AdminRiskRegisterMalformed(
            f"{F_SCRIBE_ADMIN_RISK_REGISTER_MALFORMED}: raw register not "
            f"JSON-serializable: {exc}"
        ) from exc
    snapshot_sha3_512 = hashlib.sha3_512(canonical_bytes).hexdigest()
    return parse_admin_risk_register(
        raw_mapping=raw,
        snapshot_sha3_512=snapshot_sha3_512,
        snapshot_age_hours=snapshot_age_hours,
    )


# -- Flag routing. --


# Funder-dialect → federal-or-progressive axis selector. ``Dialect`` is
# ``Literal["conservative","centrist","progressive","soul_fire"]`` — plain
# strings at runtime, not an enum.
_FEDERAL_DIALECTS: Final[frozenset[str]] = frozenset(
    {"conservative", "centrist"}
)
_PROGRESSIVE_DIALECTS: Final[frozenset[str]] = frozenset(
    {"progressive", "soul_fire"}
)


def _dialect_is_progressive(dialect: Dialect) -> bool:
    return dialect in _PROGRESSIVE_DIALECTS


def _entry_matches_in_text(entry: AdminRiskEntry, text: str) -> list[str]:
    """Return list of matched surface forms (term + variants) found in text.

    Case-insensitive substring match; whitespace-normalized. Surface form
    (original-case from the text) is returned if you want it — here we
    return the register form for canonicity.
    """
    matches: list[str] = []
    lower_text = text.lower()
    for form in (entry.term, *entry.variants):
        if form.lower() in lower_text:
            matches.append(form)
    return matches


def _identity_overlay_applies(
    *, entry: AdminRiskEntry, identity_claim_terms: Iterable[str]
) -> bool:
    """Applicant-identity overlay: entry term matches a claimed identity."""
    entry_lower = entry.term.lower()
    for claim in identity_claim_terms:
        if entry_lower in claim.lower() or claim.lower() in entry_lower:
            return True
    return False


def _make_flag(entry: AdminRiskEntry) -> AdminRiskFlag:
    """Construct a pending AdminRiskFlag from a matched register entry."""
    proposed = (
        entry.suggested_substitutions[0]
        if entry.suggested_substitutions
        else None
    )
    return AdminRiskFlag(
        term=entry.term,
        severity=entry.severity,
        proposed_substitution=proposed,
        applicant_approved=False,
    )


def route_flag_for_match(
    *,
    entry: AdminRiskEntry,
    funder_dialect: Dialect,
    identity_claim_terms: Iterable[str],
    auto_substitute_low_enabled: bool,
) -> AdminRiskFlag | None:
    """Decide whether a match becomes a flag, and at what status.

    Returns None if the match is silently allowed (LOW auto-substitute with
    policy flag OR identity overlay to EXPECTED/PREFERRED).
    """
    # Identity overlay: flip to PREFERRED — no flag.
    if _identity_overlay_applies(
        entry=entry, identity_claim_terms=identity_claim_terms
    ):
        return None

    is_progressive = _dialect_is_progressive(funder_dialect)

    # Progressive axis: EXPECTED/PREFERRED under progressive funder → no flag.
    if is_progressive and entry.progressive_register in ("EXPECTED", "PREFERRED"):
        return None

    # Progressive AVOID → always flag regardless of federal severity.
    if entry.progressive_register == "AVOID":
        return _make_flag(entry)

    # Federal severity path. AdminRiskSeverity is a Literal — compare strings.
    sev = entry.severity
    if sev == "high":
        return _make_flag(entry)
    if sev == "medium":
        return _make_flag(entry)
    # LOW (GREEN).
    if auto_substitute_low_enabled and entry.suggested_substitutions:
        return None  # silent substitution upstream at compile-time
    return _make_flag(entry)


def scan_draft_for_admin_risk(
    *,
    draft_body: str,
    register: AdminRiskRegister,
    funder_dialect: Dialect,
    identity_claim_terms: Iterable[str] = (),
    auto_substitute_low_enabled: bool = False,
) -> tuple[AdminRiskFlag, ...]:
    """Walk register entries against draft; return flags to emit."""
    identity_list = list(identity_claim_terms)
    flags: list[AdminRiskFlag] = []
    seen_terms: set[str] = set()
    for entry in register.entries:
        surface_matches = _entry_matches_in_text(entry, draft_body)
        if not surface_matches:
            continue
        if entry.term in seen_terms:
            continue
        flag = route_flag_for_match(
            entry=entry,
            funder_dialect=funder_dialect,
            identity_claim_terms=identity_list,
            auto_substitute_low_enabled=auto_substitute_low_enabled,
        )
        if flag is not None:
            flags.append(flag)
            seen_terms.add(entry.term)
    return tuple(flags)


def verify_draft_flags_or_raise(
    *,
    draft_body: str,
    declared_flags: Sequence[AdminRiskFlag],
    register: AdminRiskRegister,
    funder_dialect: Dialect,
    identity_claim_terms: Iterable[str] = (),
    auto_substitute_low_enabled: bool = False,
) -> None:
    """POST-gate helper: ensure draft's declared flags cover scan results.

    Raises:
        RuntimeError(F-SCRIBE-ADMIN-RISK-UNFLAGGED): scan found MEDIUM+ term
            not in declared_flags.
        AdminRiskHighUnapproved(F-SCRIBE-ADMIN-RISK-HIGH-UNAPPROVED): a HIGH
            flag lacks status == "approved".
    """
    expected = scan_draft_for_admin_risk(
        draft_body=draft_body,
        register=register,
        funder_dialect=funder_dialect,
        identity_claim_terms=identity_claim_terms,
        auto_substitute_low_enabled=auto_substitute_low_enabled,
    )
    declared_by_term = {f.term: f for f in declared_flags}
    for expected_flag in expected:
        if expected_flag.severity == "low":
            continue
        if expected_flag.term not in declared_by_term:
            raise RuntimeError(
                f"{F_SCRIBE_ADMIN_RISK_UNFLAGGED}: term {expected_flag.term!r} "
                f"at severity {expected_flag.severity} present in draft "
                f"without declared AdminRiskFlag"
            )
    for flag in declared_flags:
        if flag.severity == "high" and not flag.applicant_approved:
            raise AdminRiskHighUnapproved(
                f"{F_SCRIBE_ADMIN_RISK_HIGH_UNAPPROVED}: HIGH-severity term "
                f"{flag.term!r} has applicant_approved=False; "
                f"operator approval required"
            )


# ---------------------------------------------------------------------------
# CLC-axis dialect routing (architecture v7.0.12 §1.2 sanctioned read path)
# ---------------------------------------------------------------------------
#
# v7.0.12 retires the four-axis political enum and replaces ``progressive_register``
# with ``per_clc_register`` (CLC slug → AVOID|OK|EXPECTED|PREFERRED). The default
# for any CLC slug not listed on the entry's per_clc_register is AVOID per §1.2
# "safest default."
#
# Scribe Phase-0 reads the workspace register against the active opportunity-CLC
# pair (Wave 2 close-synthesis §CC-1 unblock). The entry point is
# :func:`scan_draft_for_admin_risk_clc` which takes ``active_clc`` and emits
# flags using per_clc_register semantics instead of the retired progressive_register
# semantics. The legacy :func:`scan_draft_for_admin_risk` is preserved for
# pre-v3.0 routing call-sites until the operator's v2.x → v3.0 scrub completes.


def acceptable_under_clc(
    *, entry: AdminRiskEntry, clc: str
) -> str:
    """Return AVOID|OK|EXPECTED|PREFERRED for ``entry`` under the given CLC.

    Implements v7.0.12 §1.2 default semantics: any CLC not present in the
    entry's per_clc_register defaults to AVOID. Use this helper for all
    routing decisions on the CLC axis.

    Raises ``ValueError`` if ``clc`` is not one of the 8 canonical
    CapitalLogicCard slugs (fail-closed; do NOT silently accept unknown CLCs).
    """
    if clc not in _VALID_CLC_SLUGS:
        raise ValueError(
            f"clc must be one of {sorted(_VALID_CLC_SLUGS)}; got {clc!r}"
        )
    for slug, val in entry.per_clc_register:
        if slug == clc:
            return val
    return "AVOID"


def term_acceptable_under_clc(
    *, register: AdminRiskRegister, term: str, clc: str
) -> str:
    """Lookup a term in the register and return its AVOID|OK|EXPECTED|PREFERRED
    state under the given CLC.

    Per architecture v7.0.12 §1.2: the only sanctioned read path for
    CLC-axis dialect-routing decisions. Direct ``entry.per_clc_register``
    field access by seat code is forbidden — forces all routing decisions
    through this audit chain.

    Term lookup is case-insensitive. If the term is absent from the register
    entirely, returns ``"NOT_FLAGGED"`` (the only non-enum sentinel — terms
    not in the register are simply unflagged, distinct from AVOID).
    """
    if clc not in _VALID_CLC_SLUGS:
        raise ValueError(
            f"clc must be one of {sorted(_VALID_CLC_SLUGS)}; got {clc!r}"
        )
    needle = term.strip().lower()
    if not needle:
        raise ValueError("term must be non-empty")
    for entry in register.entries:
        if entry.term.lower() == needle:
            return acceptable_under_clc(entry=entry, clc=clc)
        for v in entry.variants:
            if v.lower() == needle:
                return acceptable_under_clc(entry=entry, clc=clc)
    return "NOT_FLAGGED"


def _route_flag_for_match_clc(
    *,
    entry: AdminRiskEntry,
    active_clc: str,
    identity_claim_terms: Iterable[str],
    auto_substitute_low_enabled: bool,
) -> AdminRiskFlag | None:
    """CLC-axis flag-routing parallel to :func:`route_flag_for_match`.

    Identity overlay still applies. The dialect-axis decision is keyed off
    per_clc_register[active_clc] (defaulting to AVOID per v7.0.12 §1.2)
    instead of progressive_register.

    PREFERRED / EXPECTED under the active CLC → no flag. AVOID always flags.
    OK falls through to federal severity. LOW + auto-substitute-enabled →
    silent substitution upstream.
    """
    if _identity_overlay_applies(
        entry=entry, identity_claim_terms=identity_claim_terms
    ):
        return None

    clc_state = acceptable_under_clc(entry=entry, clc=active_clc)

    if clc_state in ("EXPECTED", "PREFERRED"):
        return None
    if clc_state == "AVOID":
        return _make_flag(entry)

    # OK: fall through to federal severity (same path as the legacy router).
    sev = entry.severity
    if sev == "high":
        return _make_flag(entry)
    if sev == "medium":
        return _make_flag(entry)
    # LOW (GREEN).
    if auto_substitute_low_enabled and entry.suggested_substitutions:
        return None
    return _make_flag(entry)


def scan_draft_for_admin_risk_clc(
    *,
    draft_body: str,
    register: AdminRiskRegister,
    active_clc: str,
    identity_claim_terms: Iterable[str] = (),
    auto_substitute_low_enabled: bool = False,
) -> tuple[AdminRiskFlag, ...]:
    """CLC-keyed parallel to :func:`scan_draft_for_admin_risk`.

    Per architecture v7.0.12 §1.2: this is the sanctioned Scribe Phase-0
    admin-risk scan entry point on the CLC axis. Activated by the active
    (CIC × opportunity-CLC) pair — caller passes the opportunity's CLC slug
    as ``active_clc``.

    Behaviour mirrors :func:`scan_draft_for_admin_risk` except dialect-axis
    decisions consult ``per_clc_register[active_clc]`` instead of
    ``progressive_register``.

    Raises ``ValueError`` if ``active_clc`` is not one of the 8 canonical
    CapitalLogicCard slugs.
    """
    if active_clc not in _VALID_CLC_SLUGS:
        raise ValueError(
            f"active_clc must be one of {sorted(_VALID_CLC_SLUGS)}; "
            f"got {active_clc!r}"
        )
    identity_list = list(identity_claim_terms)
    flags: list[AdminRiskFlag] = []
    seen_terms: set[str] = set()
    for entry in register.entries:
        surface_matches = _entry_matches_in_text(entry, draft_body)
        if not surface_matches:
            continue
        if entry.term in seen_terms:
            continue
        flag = _route_flag_for_match_clc(
            entry=entry,
            active_clc=active_clc,
            identity_claim_terms=identity_list,
            auto_substitute_low_enabled=auto_substitute_low_enabled,
        )
        if flag is not None:
            flags.append(flag)
            seen_terms.add(entry.term)
    return tuple(flags)


__all__ = [
    # Shapes
    "AdminRiskEntry",
    "AdminRiskRegister",
    # Protocols
    "RegisterLoadCallable",
    # Load / parse
    "parse_admin_risk_register",
    "load_admin_risk_register",
    # Flag routing (legacy progressive-axis)
    "route_flag_for_match",
    "scan_draft_for_admin_risk",
    "verify_draft_flags_or_raise",
    # Flag routing (CLC-axis per v7.0.12 §1.2)
    "acceptable_under_clc",
    "term_acceptable_under_clc",
    "scan_draft_for_admin_risk_clc",
    # Exceptions
    "AdminRiskRegisterStale",
    "AdminRiskRegisterMalformed",
    "AdminRiskHighUnapproved",
    # Failure codes
    "F_SCRIBE_ADMIN_RISK_REGISTER_STALE",
    "F_SCRIBE_ADMIN_RISK_UNFLAGGED",
    "F_SCRIBE_ADMIN_RISK_HIGH_UNAPPROVED",
    "F_SCRIBE_ADMIN_RISK_REGISTER_MALFORMED",
    # Constants
    "SNAPSHOT_AGE_HOURS_CEILING",
]
