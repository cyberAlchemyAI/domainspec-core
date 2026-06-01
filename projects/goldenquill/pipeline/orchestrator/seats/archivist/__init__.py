#!/usr/bin/env python3
"""
Archivist support agent — between-cycle preservation surface.

Per Blueprint §15: long-running curation work between grant cycles. Archivist proposes;
operator confirms every change. Archivist NEVER auto-applies a single mutation to KFR /
Funder Intel DB / Match DB / lessons.json / Benchmarks Register canonical state — the
autonomy boundary is structural and is enforced by F-ARCHIVIST-AUTO-APPLY-ATTEMPTED.

Two cadences: weekly tick (light — KFR expiry / pending-facts queue / Match DB delta /
lessons append) and quarterly review (heavy — Funder Intel promotion-or-drop / Match DB
outcome rollup / Benchmarks Register freshness / lessons.json proposed diffs).

Substrate: NONE at v0.2 (operator-driven manual cadence; no LLM invocation). v1.x
substrate: FAISS or Chroma + bge-large-en-v1.5 + Pydantic AI tool composition + small
local Mistral 7B class LLM. Always-local routing per v7.0.7. Per-substrate read goes
through Vault read intent wrappers (F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT enforcement).

Logician gates owned (per §15.9 — 5 codes; predicate stubs at v0.2; live Cedar/Python at
v1.x via §4 v2.x amendment):
  F-ARCHIVIST-CROSS-ORG-LEAK            (PRE + POST — per-org / workspace digest scope)
  F-ARCHIVIST-LESSON-INSTANCE-LEAK      (PRE — pattern-vs-instance lesson discipline)
  F-ARCHIVIST-AUTO-APPLY-ATTEMPTED      (PRE — three-layer auto-apply defense)
  F-ARCHIVIST-CADENCE-DRIFT             (PRE — informational at v0.2; HIGH+FAIL_CLOSED at v1.x per RT-10)
  F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT (PRE-substrate-read — NEW from RT-11 closure)

v0.2 SPEC LOCK 2026-05-10. Module skeleton authored at LOCK ceremony. v1.x amendment
realizes the LLM tool composition + scheduled-task wiring + Cedar/Python predicate bodies.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal


# Timezone-aware UTC factory. Per §11/§12 convention.
def _utc_now() -> datetime:
    """Return a timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# Cadence literals — two cadences per §15.6 (weekly + quarterly)
# Quarterly further routes to quarterly_workspace OR quarterly_per_org per §15.4.2 split
# ---------------------------------------------------------------------------

ArchivistCadence = Literal["weekly", "quarterly"]
ArchivistQuarterlyMode = Literal["quarterly_workspace", "quarterly_per_org"]


# ---------------------------------------------------------------------------
# Input contracts (per §15.4) — frozen kw_only per Tilth convention
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class ArchivistWeeklyInput:
    """Weekly tick input bundle. Per §15.4.1."""
    run_id: str
    org_slug: str
    kfr_register_path: str
    match_database_path: str
    lessons_json_path: str
    lookback_window_days: int = 7
    invoked_at_utc: datetime = field(default_factory=_utc_now)
    cadence: ArchivistCadence = "weekly"


@dataclass(frozen=True, kw_only=True)
class ArchivistQuarterlyWorkspaceInput:
    """Quarterly workspace cadence input bundle. Per §15.4.2.A."""
    run_id: str
    funder_intel_register_path: str
    benchmarks_register_path: str
    freshness_threshold_days: int = 90
    invoked_at_utc: datetime = field(default_factory=_utc_now)
    cadence: ArchivistCadence = "quarterly"
    quarterly_mode: ArchivistQuarterlyMode = "quarterly_workspace"


@dataclass(frozen=True, kw_only=True)
class ArchivistQuarterlyPerOrgInput:
    """Quarterly per-org cadence input bundle. Per §15.4.2.B."""
    run_id: str
    org_slug: str
    kfr_register_path: str
    match_database_path: str
    reports_dir: str
    lookback_window_quarters: int = 4
    invoked_at_utc: datetime = field(default_factory=_utc_now)
    cadence: ArchivistCadence = "quarterly"
    quarterly_mode: ArchivistQuarterlyMode = "quarterly_per_org"


# ---------------------------------------------------------------------------
# Digest entry schemas (per §15.5)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class KfrRefreshDigestEntry:
    """Single KFR refresh proposal entry. Per §15.5.0 + §15.5.1."""
    digest_id: str
    archivist_run_id: str
    cadence: Literal["weekly", "quarterly"]
    proposed_at_utc: datetime
    proposed_action: Literal["mark_stale", "mark_pending_refresh", "propose_archive", "propose_supersede"]
    source_substrate_path: str
    source_entry_id: str
    rationale: str


@dataclass(frozen=True, kw_only=True)
class MatchDbLessonsDeltaEntry:
    """Single Match DB lessons-delta proposal entry. Per §15.5.0 + §15.5.1."""
    digest_id: str
    archivist_run_id: str
    cadence: Literal["weekly", "quarterly"]
    proposed_at_utc: datetime
    proposed_action: Literal["surface_pattern", "propose_action_state_change", "mark_for_review"]
    source_substrate_path: str
    source_entry_id: str
    pattern_summary: str  # Pattern-level only per F-ARCHIVIST-LESSON-INSTANCE-LEAK; instance-level FORBIDDEN
    rationale: str


@dataclass(frozen=True, kw_only=True)
class FunderIntelQuarterlyEntry:
    """Single Funder Intel quarterly digest entry. Per §15.5.0 + §15.5.2."""
    digest_id: str
    archivist_run_id: str
    proposed_at_utc: datetime
    proposed_action: Literal["mark_stale", "propose_promotion", "propose_drop", "integrity_check_failed"]
    funder_id: str
    source_substrate_path: str
    source_entry_id: str
    rationale: str


@dataclass(frozen=True, kw_only=True)
class LessonsProposalEntry:
    """Single lessons.json proposed-patch entry. Per §15.5.0 + §15.5.2."""
    digest_id: str
    archivist_run_id: str
    proposed_at_utc: datetime
    proposed_lesson_text: str  # Pattern-level only per F-ARCHIVIST-LESSON-INSTANCE-LEAK
    source_lesson_refs: list[str] = field(default_factory=list)
    rationale: str = ""


# ---------------------------------------------------------------------------
# State (per Rule 1 Save State Always)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class ArchivistState:
    """Persistent state per Archivist cadence run. Saved on success AND failure per Rule 1."""
    run_id: str
    org_slug: str | None  # populated for per-org cadences; None for workspace cadences
    cadence: ArchivistCadence
    quarterly_mode: ArchivistQuarterlyMode | None  # populated for quarterly cadences
    invoked_at_utc: datetime
    cadence_completed: bool
    digest_entries_produced: int
    digest_entries_rejected: int
    failure_reason: str | None = None  # populated when cadence_completed=False
    failure_detail: str | None = None


# ---------------------------------------------------------------------------
# Gate result envelope
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class GateResult:
    """Result of a Logician gate check. Per §11/§12 convention."""
    passed: bool
    code: str | None = None
    sub_tag: str | None = None
    detail: str | None = None

    @classmethod
    def PASS(cls) -> "GateResult":
        return cls(passed=True)

    @classmethod
    def FAIL(cls, *, code: str, sub_tag: str | None = None, detail: str | None = None) -> "GateResult":
        return cls(passed=False, code=code, sub_tag=sub_tag, detail=detail)


# ---------------------------------------------------------------------------
# Cadence dispatcher — §15.6 entry point
# ---------------------------------------------------------------------------


_CADENCE_DISPATCHER: dict[ArchivistCadence, str] = {
    "weekly": "weekly_tick",
    "quarterly": "quarterly_review",
}


_QUARTERLY_SUBMODE_DISPATCHER: dict[ArchivistQuarterlyMode, str] = {
    "quarterly_workspace": "quarterly_workspace_review",
    "quarterly_per_org": "quarterly_per_org_review",
}


def list_registered_cadences() -> list[str]:
    """Return the registered cadence names.

    Per §15.6.0 cadence summary table — exactly two cadences register at v0.2 LOCK
    (weekly + quarterly). The quarterly cadence further routes to quarterly_workspace OR
    quarterly_per_org per §15.4.2 split — those are submodes of quarterly, not separate
    top-level cadences.
    """
    return sorted(_CADENCE_DISPATCHER.keys())


def list_registered_quarterly_submodes() -> list[str]:
    """Return the registered quarterly submode names.

    Per §15.4.2 split — exactly two quarterly submodes register at v0.2 LOCK
    (quarterly_workspace + quarterly_per_org).
    """
    return sorted(_QUARTERLY_SUBMODE_DISPATCHER.keys())


def get_cadence_handler_name(cadence: ArchivistCadence) -> str:
    """Return the name of the handler for a given cadence."""
    if cadence not in _CADENCE_DISPATCHER:
        raise ValueError(
            f"Unknown Archivist cadence '{cadence}'. Available: {sorted(_CADENCE_DISPATCHER)}"
        )
    return _CADENCE_DISPATCHER[cadence]


def get_quarterly_submode_handler_name(submode: ArchivistQuarterlyMode) -> str:
    """Return the name of the handler for a given quarterly submode."""
    if submode not in _QUARTERLY_SUBMODE_DISPATCHER:
        raise ValueError(
            f"Unknown Archivist quarterly submode '{submode}'. Available: {sorted(_QUARTERLY_SUBMODE_DISPATCHER)}"
        )
    return _QUARTERLY_SUBMODE_DISPATCHER[submode]


# ---------------------------------------------------------------------------
# Predicate stubs (per §15.9 — 5 owned gates)
#
# All predicates raise NotImplementedError at v0.2 LOCK per the spec-only disposition.
# The §4 v2.x amendment realizes the Cedar/Python predicate bodies at v1.x.
# ---------------------------------------------------------------------------


def f_archivist_cross_org_leak(
    *,
    cadence_input: ArchivistWeeklyInput | ArchivistQuarterlyWorkspaceInput | ArchivistQuarterlyPerOrgInput,
) -> GateResult:
    """F-ARCHIVIST-CROSS-ORG-LEAK predicate stub. Per §15.9.1.

    Sub-tags: .symlink_escape, .path_outside_org, .unconfirmed_substrate_read,
    .workspace_digest_per_org_content, .aggregate_insufficient_orgs (NEW per RT-06 closure).

    v0.2: skeleton stub raising NotImplementedError. v1.x: live Cedar/Python predicate via
    §4 v2.x amendment.
    """
    raise NotImplementedError(
        "§15.9.1 predicate scaffold — v0.2 SPEC LOCK; v1.x amendment realizes."
    )


def f_archivist_lesson_instance_leak(
    *,
    proposed_lesson_text: str,
    org_index_path: str,
    funder_intel_register_path: str,
) -> GateResult:
    """F-ARCHIVIST-LESSON-INSTANCE-LEAK predicate stub. Per §15.9.2.

    Three-layer detection per RT-07 closure: Unicode NFKC + NER + regex.
    Sub-tags: .client_name_present, .funder_specific_with_client,
    .reason_attributable_to_specific_outcome, .ner_entity_match (NEW), .unicode_homoglyph (NEW).

    v0.2: skeleton stub. v1.x: live three-layer predicate.
    """
    raise NotImplementedError(
        "§15.9.2 predicate scaffold — v0.2 SPEC LOCK; v1.x amendment realizes."
    )


def f_archivist_auto_apply_attempted(
    *,
    attempted_write_path: str,
    attempted_call_site: str,
) -> GateResult:
    """F-ARCHIVIST-AUTO-APPLY-ATTEMPTED predicate stub. Per §15.9.3.

    Three-layer defense: AST-lint + runtime dispatcher + Cedar policy.
    Sub-tags: .ast_lint_violation, .runtime_dispatcher_violation, .cedar_policy_denied,
    .subprocess_canonical_cli_invocation (NEW per RT-01), .foreign_file_write_helper_import
    (NEW per RT-02), .principal_spoofing_detected (NEW per RT-03).

    v0.2: skeleton stub. v1.x: live three-layer enforcement. AST-lint level R-ARCHIVIST-NO-CANONICAL-MUTATE
    is realized at §4 v2.x amendment compile-time AST scan.
    """
    raise NotImplementedError(
        "§15.9.3 predicate scaffold — v0.2 SPEC LOCK; v1.x amendment realizes."
    )


def f_archivist_cadence_drift(
    *,
    current_invocation_at_utc: datetime,
    prior_state_path: str | None,
    cadence: ArchivistCadence,
) -> GateResult:
    """F-ARCHIVIST-CADENCE-DRIFT predicate stub. Per §15.9.4.

    v0.2: informational-only (no scheduled cadence to drift from; operator decides when).
    v1.x: severity=HIGH + action=FAIL_CLOSED per RT-10 closure.

    Sub-tags: .weekly_drift, .quarterly_workspace_drift, .quarterly_per_org_drift.

    v0.2: skeleton stub. v1.x: live predicate with v1.x severity binding.
    """
    raise NotImplementedError(
        "§15.9.4 predicate scaffold — v0.2 SPEC LOCK; v1.x amendment realizes."
    )


def f_archivist_read_without_vault_intent(
    *,
    attempted_read_path: str,
    attempted_call_site: str,
) -> GateResult:
    """F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT predicate stub. Per §15.9.5.

    NEW from Cycle 1 RT-11 closure. Three-layer enforcement: AST-lint + runtime guard +
    Vault read intent signature self-check.

    Sub-tags: .raw_open_call, .generic_helper_import, .vault_intent_signature_invalid.

    Every substrate read attempt by Archivist MUST go through the appropriate Vault read
    intent wrapper (vault_read_intent_kfr / vault_read_intent_funder_intel /
    vault_read_intent_match_db / vault_read_intent_lessons / vault_read_intent_benchmarks /
    vault_read_intent_archivist_state); reads via raw open() or generic file-read helpers
    fail-closed.

    v0.2: skeleton stub. v1.x: live three-layer enforcement.
    """
    raise NotImplementedError(
        "§15.9.5 predicate scaffold — v0.2 SPEC LOCK; v1.x amendment realizes."
    )


# ---------------------------------------------------------------------------
# Module exports
# ---------------------------------------------------------------------------


__all__ = [
    # Cadence dispatch
    "ArchivistCadence",
    "ArchivistQuarterlyMode",
    "list_registered_cadences",
    "list_registered_quarterly_submodes",
    "get_cadence_handler_name",
    "get_quarterly_submode_handler_name",
    # Input contracts
    "ArchivistWeeklyInput",
    "ArchivistQuarterlyWorkspaceInput",
    "ArchivistQuarterlyPerOrgInput",
    # Digest entry schemas
    "KfrRefreshDigestEntry",
    "MatchDbLessonsDeltaEntry",
    "FunderIntelQuarterlyEntry",
    "LessonsProposalEntry",
    # State + gate envelopes
    "ArchivistState",
    "GateResult",
    # Predicate stubs (5 owned gates per §15.9)
    "f_archivist_cross_org_leak",
    "f_archivist_lesson_instance_leak",
    "f_archivist_auto_apply_attempted",
    "f_archivist_cadence_drift",
    "f_archivist_read_without_vault_intent",
]
