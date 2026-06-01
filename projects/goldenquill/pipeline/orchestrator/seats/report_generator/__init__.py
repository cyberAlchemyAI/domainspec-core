"""Report Generator seat module — §14 Report Generator v1 SPEC LOCK + WS-J Slice 2.

Per §14 v1 LOCK 2026-05-10, Report Generator is a TRACK in §5 v8
(``report_mode``), NOT a brand-new agent slot in the seat roster. The
five council seats (Scribe / Editor / Judge / Red Team / Logician) run
on report_mode with different prompt templates and the proposal-
commitments rubric.

This module hosts:

* Per-sub-section composer entry points (5 sub-sections at v0.2 first ship)
  — exported from :mod:`pipeline.orchestrator.seats.report_generator.composers`
  per WS-J Slice 2 (LANDED 2026-05-11).
* Claim-evidence-map authoring helpers (Slice 1 LANDED — see
  :mod:`.claim_evidence_map`).
* Cedar engine bootstrap + Python evaluator (Slice 2 LANDED — see
  :mod:`._cedar_bootstrap`).

Slice 1 → Slice 2 transition: the per-sub-section ``compose_*`` callables
are no longer NotImplementedError skeletons. The dispatch table here
points at the realized composer functions in the ``composers/`` subtree.
Per the WS-J Slice 2 handoff: "preserve the module-load integrity assert
at lines 117-125" — the closed-set + count asserts stay intact; the
function bodies are now substantive.
"""

from __future__ import annotations

from typing import Final

from .composers.beneficiary_section import compose_beneficiary_section
from .composers.financial_summary import compose_financial_summary
from .composers.metrics_table import compose_metrics_table
from .composers.narrative import compose_narrative
from .composers.photo_gallery import compose_photo_gallery


# Closed set of sub-section names per §14.6 (v0.2 first ship).
SUB_SECTIONS_V0_2: Final[frozenset[str]] = frozenset(
    {
        "narrative",
        "metrics_table",
        "financial_summary",
        "photo_gallery",
        "beneficiary_section",
    }
)


# Per-sub-section composer dispatch table — used by `pipeline.orchestrator.tracks.report_mode`
# to route per-sub-section composition requests.
_SUB_SECTION_COMPOSERS: Final[dict[str, object]] = {
    "narrative": compose_narrative,
    "metrics_table": compose_metrics_table,
    "financial_summary": compose_financial_summary,
    "photo_gallery": compose_photo_gallery,
    "beneficiary_section": compose_beneficiary_section,
}

# Module-load integrity assert per §5 v8 V1 inline-literal rebind-resistance pattern.
# If a contributor extends SUB_SECTIONS_V0_2 or _SUB_SECTION_COMPOSERS with a
# new sub-section AND fails to update the audit trail at §14.6, the assert
# below catches the drift at module load.
assert SUB_SECTIONS_V0_2 == frozenset(_SUB_SECTION_COMPOSERS.keys()), (
    "§14.6 sub-section closed set drift detected: SUB_SECTIONS_V0_2 must equal "
    "_SUB_SECTION_COMPOSERS.keys() — a §14 spin is required to extend the closed "
    "set per §14 v1 LOCK contract."
)
assert len(SUB_SECTIONS_V0_2) == 5, (
    "§14.6 sub-section count rebind-resistance: SUB_SECTIONS_V0_2 must be exactly "
    "5 entries at v0.2 first ship per §14 v1 LOCK contract."
)


__all__ = [
    "SUB_SECTIONS_V0_2",
    "compose_beneficiary_section",
    "compose_financial_summary",
    "compose_metrics_table",
    "compose_narrative",
    "compose_photo_gallery",
]
