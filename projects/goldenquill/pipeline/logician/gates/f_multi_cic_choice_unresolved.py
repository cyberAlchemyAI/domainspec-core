"""F-MULTI-CIC-CHOICE-UNRESOLVED — multi-CIC select-one composition resolution.

PRE-gate at order 6.7. Fires at seat-configuration resolution time, per-grant,
when a multi-CIC applicant has primitives requiring select-one resolution
(Language Register / narrative voice / tone) without operator selection in
``match_overrides:`` for the active grant. Fail-closed.

Authority: ``pipeline/architecture/v0.1/architecture_v7_0_8_amendment.md``
§4.3 + §7 (LOCKED 2026-05-08, Cycle-1 RT-04 fix).

Composition modes (per v7.0.8 §7)
---------------------------------
- ``union`` — additive primitives (Search Vocabulary, Evidence Schema)
- ``most-stringent`` — posture primitives (Reporting Rhythm)
- ``select-one-per-grant`` — choice primitives (Language Register, narrative
  voice, tone). Operator must select per-grant via ``match_overrides:`` block.
  This gate enforces that requirement at seat-config resolution time.

Recovery: operator edits the active grant's PROJECT_CONTEXT
``match_overrides:`` block to specify the chosen value for each unresolved
select-one primitive. Pipeline resumes.

Subcode
-------
- ``F-MULTI-CIC-CHOICE-UNRESOLVED.{primitive_name}`` — names the unresolved
  primitive, e.g., ``F-MULTI-CIC-CHOICE-UNRESOLVED.language_register``
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from pipeline.types import CUSTOMER_IDENTITY_CATEGORY_VALUES


GATE_ID = "F-MULTI-CIC-CHOICE-UNRESOLVED"
PRE_GATE_ORDER = 6.7

# Primitives whose composition mode is select-one-per-grant. This list is the
# authoritative inventory from v7.0.8 §7's primitive-to-mode mapping table.
SELECT_ONE_PRIMITIVES: tuple[str, ...] = (
    "language_register",
    "narrative_voice",
    "tone",
)


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MultiCICChoiceFinding:
    """One unresolved select-one primitive for a multi-CIC org × grant."""

    primitive_name: str
    cic_active: tuple[str, ...]
    cic_value_per_active: dict[str, str]
    detail: str


@dataclass(frozen=True)
class MultiCICChoiceResult:
    """Result of running F-MULTI-CIC-CHOICE-UNRESOLVED at seat-config time.

    ``passed=True`` means either single-CIC org (gate not applicable) OR
    multi-CIC with all select-one primitives resolved → seat config proceeds.
    """

    passed: bool
    findings: tuple[MultiCICChoiceFinding, ...]


# ---------------------------------------------------------------------------
# Injected dependencies
# ---------------------------------------------------------------------------


@runtime_checkable
class CICPrimitivesReaderCallable(Protocol):
    """Returns the value each active CIC declares for a given primitive.

    For input ``(["food_systems", "educator"], "language_register")``, returns
    e.g. ``{"food_systems": "agricultural-plainspoken", "educator": "academic-formal"}``.

    The values come from the per-CIC operational profile cards
    (TILTH-CIC-01..06). Caller (gate runner) has them pre-resolved.
    """

    def __call__(
        self, cic_active: list[str], primitive_name: str
    ) -> dict[str, str]: ...


@runtime_checkable
class MatchOverrideReaderCallable(Protocol):
    """Returns the operator-set override for a primitive on a specific grant,
    or ``None`` if not set.

    Looks up ``orgs/<slug>/PROJECT_CONTEXT.md::match_overrides[grant_id][primitive_name]``.
    """

    def __call__(
        self, org_slug: str, grant_id: str, primitive_name: str
    ) -> str | None: ...


# ---------------------------------------------------------------------------
# Gate entry point
# ---------------------------------------------------------------------------


def run(
    *,
    org_slug: str,
    grant_id: str,
    cic_active: list[str],
    cic_primitives_reader: CICPrimitivesReaderCallable,
    match_override_reader: MatchOverrideReaderCallable,
) -> MultiCICChoiceResult:
    """Check every select-one primitive for resolution.

    For single-CIC orgs (``len(cic_active) == 1``), the gate is a no-op (no
    composition is happening; the single CIC's value applies directly).

    For multi-CIC orgs, for each select-one primitive:
      1. Read the value each active CIC declares for that primitive.
      2. If all CICs declare the same value, no resolution needed → pass.
      3. If values differ AND no operator override set → finding.
      4. If values differ AND operator override set → resolved → pass.
    """
    # Validate CIC IDs (defense-in-depth; F-CIC-CLC-MATCH-NULL also catches)
    invalid = [c for c in cic_active if c not in CUSTOMER_IDENTITY_CATEGORY_VALUES]
    if invalid:
        # Don't double-fire — F-CIC-CLC-MATCH-NULL handles this.
        return MultiCICChoiceResult(passed=True, findings=())

    if len(cic_active) <= 1:
        # Single-CIC: no composition; gate inapplicable.
        return MultiCICChoiceResult(passed=True, findings=())

    findings: list[MultiCICChoiceFinding] = []

    for primitive_name in SELECT_ONE_PRIMITIVES:
        per_cic_values = cic_primitives_reader(cic_active, primitive_name)

        # Same value across all active CICs → no resolution needed
        unique_values = set(per_cic_values.values())
        if len(unique_values) <= 1:
            continue

        # Values differ → need operator override
        override = match_override_reader(org_slug, grant_id, primitive_name)
        if override is None or override == "":
            findings.append(
                MultiCICChoiceFinding(
                    primitive_name=primitive_name,
                    cic_active=tuple(cic_active),
                    cic_value_per_active=dict(per_cic_values),
                    detail=(
                        f"primitive {primitive_name!r} has differing values "
                        f"across active CICs ({per_cic_values}); operator "
                        f"override missing for grant {grant_id!r}; set "
                        f"match_overrides[{grant_id!r}][{primitive_name!r}] "
                        "in PROJECT_CONTEXT to resolve"
                    ),
                )
            )

    return MultiCICChoiceResult(
        passed=len(findings) == 0,
        findings=tuple(findings),
    )
