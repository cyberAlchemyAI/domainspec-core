"""pipeline.cards.validators — Phase 4 self-validation helpers.

Per blueprint §18.11 Phase 4 (Self-Validation). Each draft card must
pass these checks before review handback:

  - schema_completeness_check — every required field present.
  - source_provenance_completeness_check — every claim has a source_citation.
  - no_hardcoded_cic_clc_coupling_check — defense in depth against F-CARDS-COUPLING-VIOLATION-EXTENSION.
  - no_private_customer_data_check — defense in depth against F-CARDS-PRIVATE-DATA-IN-CARD.
  - no_unsourced_numeric_win_rate_claims_check — defense in depth.
  - no_unsupported_program_claims_check.
  - no_excessive_copied_source_text_check.
  - no_production_load_if_unsigned_check.

These helpers are research-time tooling for card authors (Paul's research
skill in Phase D). They run client-side before review handback, separate from
the runtime Logician gates which run at loader time.

DRAFT at v0.1 LOCK candidate state. Body landings graduate LIVE at v0.2 first
wave alongside Phase D research pipeline activation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal, Mapping, Sequence


# --- ValidationResult shape --------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class ValidationFinding:
    """One validator finding."""
    check: str                    # e.g., "schema_completeness", "no_hardcoded_coupling"
    severity: Literal["INFO", "WARN", "FAIL"]
    field_path: str               # card field path or "" if global
    message: str


@dataclass(frozen=True, kw_only=True)
class ValidationReport:
    """Aggregated Phase 4 self-validation report."""
    card_path: str
    card_axis: Literal["CIC", "CLC", "MATRIX"]
    findings: tuple[ValidationFinding, ...]

    @property
    def passed(self) -> bool:
        return not any(f.severity == "FAIL" for f in self.findings)

    @property
    def fail_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "FAIL")

    @property
    def warn_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "WARN")


def validate_card(
    *,
    card_body: Mapping[str, object],
    card_path: str,
    card_axis: Literal["CIC", "CLC", "MATRIX"],
) -> ValidationReport:
    """Run all Phase 4 self-validation checks. Returns ValidationReport.

    Body graduates LIVE at v0.2 first wave per architecture v7.0.11 §5.
    """

    raise NotImplementedError(
        "validate_card body graduates LIVE at v0.2 first wave alongside Phase D "
        "research pipeline activation per architecture v7.0.11 §5."
    )


# --- Individual check shells -------------------------------------------------

def check_schema_completeness(
    *,
    card_body: Mapping[str, object],
    card_axis: Literal["CIC", "CLC", "MATRIX"],
) -> Sequence[ValidationFinding]:
    """Check that every required schema field is present and non-empty."""
    raise NotImplementedError("graduates v0.2 first wave")


def check_source_provenance_completeness(
    *,
    card_body: Mapping[str, object],
) -> Sequence[ValidationFinding]:
    """Check that every claim has a source_citation field set (no '_note: NEEDED' markers)."""
    raise NotImplementedError("graduates v0.2 first wave")


def check_no_hardcoded_coupling(
    *,
    card_body: Mapping[str, object],
    card_axis: Literal["CIC", "CLC", "MATRIX"],
) -> Sequence[ValidationFinding]:
    """Defense-in-depth check against F-CARDS-COUPLING-VIOLATION-EXTENSION.
    Scans top-level keys against the FORBIDDEN_FIELD_REGISTRY in
    pipeline.logician.gates.f_cards_coupling_violation_extension.
    """
    raise NotImplementedError("graduates v0.2 first wave")


def check_no_private_customer_data(
    *,
    card_body: Mapping[str, object],
) -> Sequence[ValidationFinding]:
    """Defense-in-depth check against F-CARDS-PRIVATE-DATA-IN-CARD.
    Scans for org_slug, client_name, EIN, UEI, addresses, named individuals,
    private cycle IDs.
    """
    raise NotImplementedError("graduates v0.2 first wave")


def check_no_unsourced_numeric_win_rate_claims(
    *,
    card_body: Mapping[str, object],
) -> Sequence[ValidationFinding]:
    """Any numeric win-rate or success-percentage claim must have a
    source_citation. Unsourced numerics fail Phase 4.
    """
    raise NotImplementedError("graduates v0.2 first wave")


def check_no_unsupported_program_claims(
    *,
    card_body: Mapping[str, object],
) -> Sequence[ValidationFinding]:
    """Any reference to a named federal/state/foundation program must have a
    source_citation pointing to the program's official documentation.
    """
    raise NotImplementedError("graduates v0.2 first wave")


def check_no_excessive_copied_source_text(
    *,
    card_body: Mapping[str, object],
    similarity_threshold: float = 0.8,
) -> Sequence[ValidationFinding]:
    """Defense against authorship laundering — card content should be
    extracted/summarized, not copied verbatim from primary sources.
    """
    raise NotImplementedError("graduates v0.2 first wave")
