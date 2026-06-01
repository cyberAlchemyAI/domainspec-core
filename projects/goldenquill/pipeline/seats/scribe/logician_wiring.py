"""pipeline.seats.scribe.logician_wiring — R3 Scribe PRE/POST gate assembly.

Spec card: ``pipeline/engineering/spec_cards/section_07_scribe_round_3_seat_entry_and_wiring.md``
§6 (PRE/POST gate wiring).

R3 authors pure *assemblers*. The predicates themselves live in
``pipeline.logician.pre_gate`` / ``pipeline.logician.post_gate`` /
``pipeline.logician.cedar_eval`` / ``pipeline.logician.source_tag_verify``
/ ``pipeline.logician.conversation_log``. This module wires Scribe-specific
F-SCRIBE-* codes over those predicates via injected Protocol seams (E-017)
and fires inline deterministic checks for envelope-local invariants
(dialect closed set, program registry, snapshot freshness, section-limit
consistency, activity exhaustiveness, dialect drift, dialect-induced
identity, numeric-verbatim).

Disciplines:

- **V1 inline-literal rebind-resistance.** Snapshot-age ceiling 24.0h
  inline at the PRE-gate check site (the constant in
  ``admin_risk_adapter`` is human-reading only).
- **E-017 injected seams.** Every cross-module Logician call is a
  Protocol callable — production wires to the real module, tests inject
  deterministic stubs.
- **Law 2 Scribe-owned.** ``F-SCRIBE-INELIGIBLE-ACTIVITY`` is checked
  locally against ``SectionDraft.eligible_activity_map`` — NOT delegated
  to a generic Law 2 gate.
- **Fail-closed.** Every trip raises :class:`.seat.ScribeGateFailed`
  with ``failure_code`` + ``trigger`` + ``evidence``; the seat catches
  and emits structured stderr.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Final, Mapping, Protocol, Sequence

from pipeline.seats.scribe.admin_risk_adapter import (
    AdminRiskRegister,
    F_SCRIBE_ADMIN_RISK_HIGH_UNAPPROVED,
    F_SCRIBE_ADMIN_RISK_REGISTER_STALE,
    F_SCRIBE_ADMIN_RISK_UNFLAGGED,
    AdminRiskHighUnapproved,
    verify_draft_flags_or_raise,
)
from pipeline.seats.scribe.dialect import (
    detect_dialect_drift,
    detect_dialect_induced_identity,
)
from pipeline.seats.scribe.program_templates import KNOWN_PROGRAMS
from pipeline.seats.scribe.section_draft import (
    AdminRiskFlag,
    ClaimEvidence,
    ConversationAnchor,
    EligibleActivityMatch,
    SectionDraft,
)
from pipeline.seats.scribe.seat import (
    F_SCRIBE_CONVERSATION_ANCHOR_INVALID,
    F_SCRIBE_DIALECT_DRIFT,
    F_SCRIBE_DIALECT_INDUCED_IDENTITY,
    F_SCRIBE_DIALECT_UNCLASSIFIED,
    F_SCRIBE_INELIGIBLE_ACTIVITY,
    F_SCRIBE_ORG_CROSS_REF,
    F_SCRIBE_OVERLOOKED_EXPENSE_UNRESOLVED,
    F_SCRIBE_PARAPHRASED_NUMERIC,
    F_SCRIBE_SCOPE_MISSING,
    F_SCRIBE_SECTION_OVER_LIMIT_UNFLAGGED,
    F_SCRIBE_TEMPLATE_DRIFT,
    F_SCRIBE_TEMPLATE_UNKNOWN,
    F_SCRIBE_UNSOURCED_CLAIM,
    ScribeEnvelope,
    ScribeGateFailed,
)
from pipeline.seats.scribe.smart import check_numeric_verbatim

# ---------------------------------------------------------------------------
# KGIE tri-state + dialect closed-set constants
# ---------------------------------------------------------------------------

# Dialects the envelope is allowed to carry. Mirrors
# ``dialect._DIALECT_VALID``; restated here so this module needs no
# private-name import.
_VALID_FUNDER_DIALECTS: Final[frozenset[str]] = frozenset(
    {"conservative", "centrist", "progressive", "soul_fire"}
)


# ---------------------------------------------------------------------------
# Protocol seams (E-017)
# ---------------------------------------------------------------------------


class CedarCrossOrgCheck(Protocol):
    """Cedar ``org_isolation`` policy evaluator.

    Returns the list of *foreign* org slugs detected in the compiled
    prompt or project_context — an empty list is PASS. Implementation
    typically delegates to
    ``pipeline.logician.cedar_eval.evaluate_cross_org_dossier``.
    """

    def __call__(
        self,
        *,
        envelope_org_slug: str,
        compiled_prompt: str,
        project_context: Mapping[str, Any],
    ) -> tuple[str, ...]: ...


class KgieStatusGetter(Protocol):
    """Retrieve the envelope's KGIE preflight status without Scribe having
    to carry the full KgiePreflightResult through the JSON envelope.

    Production wires a stub that reads from ``envelope.project_context``;
    tests inject fixed tri-state strings.
    """

    def __call__(self, *, envelope: ScribeEnvelope) -> str: ...


class RfaDriftCheck(Protocol):
    """Verify the RFA file content hash matches the envelope's pinned hash.

    Returns True on drift (F-SCRIBE-RFA-DRIFT). False on match.
    """

    def __call__(self, *, envelope: ScribeEnvelope) -> bool: ...


class TemplateDriftCheck(Protocol):
    """Verify the program-template content hash matches the envelope's pin.

    Returns True on drift (F-SCRIBE-TEMPLATE-DRIFT). False on match.
    """

    def __call__(self, *, envelope: ScribeEnvelope) -> bool: ...


class SourceTagVerify(Protocol):
    """Verify every ClaimEvidence source_pointer resolves + the claim_text
    appears byte-near in the cited source.

    Returns tuple of *unsourced* claim texts — empty tuple is PASS.
    Production delegates to ``pipeline.logician.source_tag_verify``.
    """

    def __call__(
        self,
        *,
        claim_evidence_map: tuple[ClaimEvidence, ...],
        project_context: Mapping[str, Any],
        rfa_body_text: str,
        conversation_log: Mapping[str, str],
    ) -> tuple[str, ...]: ...


class ConversationAnchorVerify(Protocol):
    """Verify a ``ConversationAnchor``'s turn-ordinal + prefix hash against
    the run-scoped append-only conversation log. Returns True on mismatch
    (F-SCRIBE-CONVERSATION-ANCHOR-INVALID), False on match.
    """

    def __call__(
        self, *, anchor: ConversationAnchor, run_id: str
    ) -> bool: ...


class EvidenceTextProvider(Protocol):
    """Return concatenated evidence text for numeric-verbatim cross-check.

    Production concatenates ``rfa.body + project_context.serialized +
    conversation_log.serialized``; tests inject fixed strings.
    """

    def __call__(self, *, envelope: ScribeEnvelope) -> str: ...


class IdentityClaimProvider(Protocol):
    """Return the identity-claim tuple stashed in envelope.project_context
    (R1 shape). Returns empty tuple when absent.
    """

    def __call__(self, *, envelope: ScribeEnvelope) -> tuple[Any, ...]: ...


# ---------------------------------------------------------------------------
# Assembly result shapes
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class PreGateAssembly:
    """Report of which F-codes the PRE-gate assembly checked and passed.

    Emitted on success (all checks PASS). On any failure, the assembler
    raises :class:`ScribeGateFailed` and this dataclass is not produced.
    """

    run_id: str
    org_slug: str
    codes_checked: tuple[str, ...]


@dataclass(frozen=True, kw_only=True, slots=True)
class PostGateAssembly:
    """Report of which F-codes the POST-gate assembly checked and passed."""

    run_id: str
    org_slug: str
    codes_checked: tuple[str, ...]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _raise_scribe(
    *, failure_code: str, trigger: str, evidence: Mapping[str, Any]
) -> None:
    """Construct + raise ScribeGateFailed with required kwargs."""
    raise ScribeGateFailed(
        failure_code=failure_code, trigger=trigger, evidence=evidence
    )


def _budget_section_needs_expenses_check(section_name: str) -> bool:
    """Return True iff the section is the RFA's budget section.

    Matches against common RFA naming — ``"budget"``, ``"budget
    narrative"``, ``"project budget"`` — case-insensitive substring.
    """
    lower = section_name.lower().strip()
    return "budget" in lower


# ---------------------------------------------------------------------------
# PRE-gate assembler
# ---------------------------------------------------------------------------


def assemble_scribe_pre_gate(
    *,
    envelope: ScribeEnvelope,
    admin_risk_register: AdminRiskRegister,
    cedar_cross_org_check: CedarCrossOrgCheck,
    kgie_status_getter: KgieStatusGetter,
    rfa_drift_check: RfaDriftCheck,
    template_drift_check: TemplateDriftCheck,
) -> PreGateAssembly:
    """Scribe PRE-gate: runs BEFORE the Anthropic dispatch.

    Raises :class:`ScribeGateFailed` on any F-SCRIBE-* trip; seat catches
    and emits structured stderr + exit 2.

    Checks (order is canonical):

    1. ``F-SCRIBE-ORG-CROSS-REF`` via Cedar ``org_isolation``.
    2. KGIE tri-state: ``fail`` → ``F-SCRIBE-KGIE-FAIL``.
    3. ``F-SCRIBE-RFA-DRIFT`` via session-manifest hash compare.
    4. ``F-SCRIBE-SCOPE-MISSING`` when KGIE ``needs_operator_input`` AND
       no operator-override dialect (operator hasn't acknowledged scope).
    5. ``F-SCRIBE-DIALECT-UNCLASSIFIED`` — envelope.funder_dialect in
       closed set (enforced at envelope construction, re-checked
       defensively here).
    6. ``F-SCRIBE-TEMPLATE-UNKNOWN`` — program_code ∈ KNOWN_PROGRAMS.
    7. ``F-SCRIBE-TEMPLATE-DRIFT`` via file-system hash compare.
    8. ``F-SCRIBE-ADMIN-RISK-REGISTER-STALE`` — 24.0h ceiling.
    """
    # Check 1 — Cedar org-isolation.
    foreign_slugs = cedar_cross_org_check(
        envelope_org_slug=envelope.org_slug,
        compiled_prompt=envelope.compiled_prompt,
        project_context=envelope.project_context,
    )
    if foreign_slugs:
        _raise_scribe(
            failure_code=F_SCRIBE_ORG_CROSS_REF,
            trigger="cedar_org_isolation_tripped",
            evidence={
                "envelope_org_slug": envelope.org_slug,
                "foreign_slugs": list(foreign_slugs),
            },
        )

    # Check 2 — KGIE tri-state.
    kgie_status = kgie_status_getter(envelope=envelope)
    if kgie_status == "fail":
        _raise_scribe(
            failure_code="F-SCRIBE-KGIE-FAIL",
            trigger="kgie_status_fail",
            evidence={"kgie_status": kgie_status},
        )
    # needs_operator_input is NOT a failure — it's the OQ surface path.
    # It becomes F-SCRIBE-SCOPE-MISSING only when paired with no operator
    # signal in envelope.operator_override_dialect (check 4 below).

    # Check 3 — RFA drift.
    if rfa_drift_check(envelope=envelope):
        _raise_scribe(
            failure_code="F-SCRIBE-RFA-DRIFT",
            trigger="rfa_hash_mismatch",
            evidence={"run_id": envelope.run_id},
        )

    # Check 4 — scope-missing (KGIE needs_operator_input + no override).
    if (
        kgie_status == "needs_operator_input"
        and envelope.operator_override_dialect is None
    ):
        _raise_scribe(
            failure_code=F_SCRIBE_SCOPE_MISSING,
            trigger="kgie_needs_operator_input_without_override",
            evidence={
                "kgie_status": kgie_status,
                "operator_override_dialect": None,
            },
        )

    # Check 5 — dialect closed-set (defensive; envelope invariant already
    # enforces, but a caller may construct envelope via
    # ``object.__setattr__`` and slip a value past construction).
    if envelope.funder_dialect not in _VALID_FUNDER_DIALECTS:
        _raise_scribe(
            failure_code=F_SCRIBE_DIALECT_UNCLASSIFIED,
            trigger="funder_dialect_not_in_closed_set",
            evidence={
                "funder_dialect": envelope.funder_dialect,
                "valid": sorted(_VALID_FUNDER_DIALECTS),
            },
        )

    # Check 6 — program template known.
    if envelope.program_code not in KNOWN_PROGRAMS:
        _raise_scribe(
            failure_code=F_SCRIBE_TEMPLATE_UNKNOWN,
            trigger="program_code_not_in_known_programs",
            evidence={
                "program_code": envelope.program_code,
                "known": sorted(KNOWN_PROGRAMS),
            },
        )

    # Check 7 — template-content drift.
    if template_drift_check(envelope=envelope):
        _raise_scribe(
            failure_code=F_SCRIBE_TEMPLATE_DRIFT,
            trigger="program_template_hash_mismatch",
            evidence={"program_code": envelope.program_code},
        )

    # Check 8 — admin-risk snapshot freshness.
    # 24.0h ceiling is INLINE LITERAL (V1 rebind-resistance). The constant
    # ``admin_risk_adapter.SNAPSHOT_AGE_HOURS_CEILING`` is human-reading only.
    if envelope.admin_risk_snapshot_age_hours > 24.0:
        _raise_scribe(
            failure_code=F_SCRIBE_ADMIN_RISK_REGISTER_STALE,
            trigger="admin_risk_snapshot_age_exceeds_24h",
            evidence={
                "snapshot_age_hours": envelope.admin_risk_snapshot_age_hours,
                "ceiling_hours": 24.0,
            },
        )
    # Belt-and-suspenders: if the register loader returned a snapshot
    # whose declared age mismatches the envelope, surface the envelope's
    # value (the source-of-truth per session manifest).
    if admin_risk_register.snapshot_age_hours > 24.0:
        _raise_scribe(
            failure_code=F_SCRIBE_ADMIN_RISK_REGISTER_STALE,
            trigger="admin_risk_register_load_returned_stale_snapshot",
            evidence={
                "loader_age_hours": admin_risk_register.snapshot_age_hours,
                "ceiling_hours": 24.0,
            },
        )

    return PreGateAssembly(
        run_id=envelope.run_id,
        org_slug=envelope.org_slug,
        codes_checked=(
            F_SCRIBE_ORG_CROSS_REF,
            "F-SCRIBE-KGIE-FAIL",
            "F-SCRIBE-RFA-DRIFT",
            F_SCRIBE_SCOPE_MISSING,
            F_SCRIBE_DIALECT_UNCLASSIFIED,
            F_SCRIBE_TEMPLATE_UNKNOWN,
            F_SCRIBE_TEMPLATE_DRIFT,
            F_SCRIBE_ADMIN_RISK_REGISTER_STALE,
        ),
    )


# ---------------------------------------------------------------------------
# POST-gate assembler
# ---------------------------------------------------------------------------


def _check_section_over_limit_consistency(sd: SectionDraft) -> bool:
    """Return True iff over_limit_flag is consistent with limit vs count.

    Matches the ``SectionDraft.__post_init__`` invariant for
    words/characters; `pages` cap is template-specific and skipped.
    """
    if sd.rfa_section_limit is None:
        return not sd.over_limit_flag
    limit = sd.rfa_section_limit
    if limit.limit_kind == "words":
        expected = sd.word_count > limit.limit_value
    elif limit.limit_kind == "characters":
        expected = sd.character_count > limit.limit_value
    else:  # pages — template-specific chars-per-page; SectionDraft does
           # not enforce this, so we treat `over_limit_flag` as authoritative
        return True
    return sd.over_limit_flag == expected


def _check_activity_map_exhaustive(sd: SectionDraft) -> list[EligibleActivityMatch]:
    """Return list of EligibleActivityMatch entries violating Law 2.

    Invariant: if ``matched_rfa_activity is None``, ``scope_check_flag``
    MUST be True. Construction already enforces this — this walker catches
    any violation that slipped through ``object.__setattr__``.
    """
    bad: list[EligibleActivityMatch] = []
    for match in sd.eligible_activity_map:
        if match.matched_rfa_activity is None and not match.scope_check_flag:
            bad.append(match)
    return bad


def _check_anchor_pointers(
    claim_evidence_map: tuple[ClaimEvidence, ...],
    conversation_anchor: ConversationAnchor | None,
) -> list[str]:
    """Return list of invalid source_pointer strings.

    A ``USER_DATA:`` source_pointer must match the run's
    ``conversation_anchor.as_source_pointer()`` exactly — other USER_DATA
    anchors require their own ConversationAnchor entry (not modeled at R3).
    RFA / PROJECT_CONTEXT pointers pass through (their resolution is the
    SourceTagVerify callable's job).
    """
    bad: list[str] = []
    for ev in claim_evidence_map:
        if ev.evidence_kind != "USER_DATA":
            continue
        if conversation_anchor is None:
            bad.append(ev.source_pointer)
            continue
        if ev.source_pointer != conversation_anchor.as_source_pointer():
            bad.append(ev.source_pointer)
    return bad


def assemble_scribe_post_gate(
    *,
    envelope: ScribeEnvelope,
    section_drafts: tuple[SectionDraft, ...],
    admin_risk_flags: tuple[AdminRiskFlag, ...],
    admin_risk_register: AdminRiskRegister,
    source_tag_verify: SourceTagVerify,
    conversation_anchor_verify: ConversationAnchorVerify,
    evidence_text_provider: EvidenceTextProvider,
    identity_claim_provider: IdentityClaimProvider,
    rfa_body_text: str = "",
    conversation_log: Mapping[str, str] | None = None,
) -> PostGateAssembly:
    """Scribe POST-gate: runs AFTER the Anthropic dispatch, before stdout.

    Raises :class:`ScribeGateFailed` on any F-SCRIBE-* trip.

    Checks (order is canonical):

    1. ``F-SCRIBE-UNSOURCED-CLAIM`` via ``source_tag_verify``.
    2. ``F-SCRIBE-PARAPHRASED-NUMERIC`` via ``check_numeric_verbatim``.
    3. ``F-SCRIBE-DIALECT-INDUCED-IDENTITY`` via closed-set proxy table.
    4. ``F-SCRIBE-CONVERSATION-ANCHOR-INVALID`` via run-log hash.
    5. ``F-SCRIBE-ADMIN-RISK-UNFLAGGED`` + ``F-SCRIBE-ADMIN-RISK-HIGH-
       UNAPPROVED`` via ``verify_draft_flags_or_raise``.
    6. ``F-SCRIBE-DIALECT-DRIFT`` via closed-set vocabulary check.
    7. ``F-SCRIBE-SECTION-OVER-LIMIT-UNFLAGGED`` via cross-walk.
    8. ``F-SCRIBE-OVERLOOKED-EXPENSE-UNRESOLVED`` (budget sections only —
       the envelope's single-section-per-invoke design means this fires
       only when the current section is the budget).
    9. ``F-SCRIBE-INELIGIBLE-ACTIVITY`` — Law 2 Scribe-owned walker over
       ``SectionDraft.eligible_activity_map``.

    Out of scope at R3 (codes exist as constants for §5 R5+ revision-loop;
    NOT advertised in ``codes_checked``):

    - ``F-SCRIBE-SMART-INVENTED-METRIC`` — distinct trip semantics (relevance-
      pointer set) from #2 numeric-verbatim; lands once SMART-relevance
      pointer table binds to SectionDraft surface.
    - ``F-SCRIBE-EVALUATION-CRITERION-MISSING`` — full-draft exhaustiveness
      gate; cannot fire on single-section invocation.
    """
    conv_log = conversation_log or {}
    identity_claims = identity_claim_provider(envelope=envelope)
    evidence_text = evidence_text_provider(envelope=envelope)

    # Accumulate a single pass per section to avoid re-scanning the body.
    for sd in section_drafts:
        # Check 1 — unsourced claim verification.
        unsourced = source_tag_verify(
            claim_evidence_map=sd.claim_evidence_map,
            project_context=envelope.project_context,
            rfa_body_text=rfa_body_text,
            conversation_log=conv_log,
        )
        if unsourced:
            _raise_scribe(
                failure_code=F_SCRIBE_UNSOURCED_CLAIM,
                trigger="source_tag_verify_unsourced",
                evidence={
                    "section_name": sd.section_name,
                    "unsourced_claims": list(unsourced),
                },
            )

        # Check 2 — numeric-verbatim invariant over body vs evidence.
        missing_numeric = check_numeric_verbatim(sd.body_text, evidence_text)
        if missing_numeric:
            _raise_scribe(
                failure_code=F_SCRIBE_PARAPHRASED_NUMERIC,
                trigger="numeric_token_not_in_evidence",
                evidence={
                    "section_name": sd.section_name,
                    "missing_tokens": list(missing_numeric),
                },
            )

        # Check 3 — dialect-induced identity closed set.
        induced_proxies = detect_dialect_induced_identity(
            sd.body_text,
            sd.draft_dialect,
            identity_claims,  # type: ignore[arg-type]
        )
        if induced_proxies:
            _raise_scribe(
                failure_code=F_SCRIBE_DIALECT_INDUCED_IDENTITY,
                trigger="dialect_identity_proxy_without_claim",
                evidence={
                    "section_name": sd.section_name,
                    "draft_dialect": sd.draft_dialect,
                    "proxies": list(induced_proxies),
                },
            )

        # Check 6 — dialect drift (vocabulary from other dialects).
        drift = detect_dialect_drift(sd.body_text, sd.draft_dialect)
        if drift:
            _raise_scribe(
                failure_code=F_SCRIBE_DIALECT_DRIFT,
                trigger="foreign_dialect_vocabulary_present",
                evidence={
                    "section_name": sd.section_name,
                    "declared_dialect": sd.draft_dialect,
                    "foreign_phrases": list(drift),
                },
            )

        # Check 7 — section-over-limit consistency.
        if not _check_section_over_limit_consistency(sd):
            _raise_scribe(
                failure_code=F_SCRIBE_SECTION_OVER_LIMIT_UNFLAGGED,
                trigger="over_limit_flag_inconsistent_with_count_vs_limit",
                evidence={
                    "section_name": sd.section_name,
                    "over_limit_flag": sd.over_limit_flag,
                    "word_count": sd.word_count,
                    "character_count": sd.character_count,
                    "rfa_section_limit": (
                        {
                            "limit_kind": sd.rfa_section_limit.limit_kind,
                            "limit_value": sd.rfa_section_limit.limit_value,
                        }
                        if sd.rfa_section_limit is not None
                        else None
                    ),
                },
            )

        # Check 8 — budget-section overlooked-expenses.
        if _budget_section_needs_expenses_check(sd.section_name):
            # Advisory form: drafter adds an inline
            # "[OVERLOOKED-EXPENSES-RESOLVED]" marker. Absent marker =
            # fail-closed. Marker absence is deterministic.
            if "[OVERLOOKED-EXPENSES-RESOLVED]" not in sd.body_text:
                _raise_scribe(
                    failure_code=F_SCRIBE_OVERLOOKED_EXPENSE_UNRESOLVED,
                    trigger="budget_section_missing_resolved_marker",
                    evidence={"section_name": sd.section_name},
                )

        # Check 11 — Scribe-owned Law 2 ineligible-activity walker.
        bad_activities = _check_activity_map_exhaustive(sd)
        if bad_activities:
            _raise_scribe(
                failure_code=F_SCRIBE_INELIGIBLE_ACTIVITY,
                trigger="unmatched_activity_without_scope_check_flag",
                evidence={
                    "section_name": sd.section_name,
                    "activities": [m.activity_phrase for m in bad_activities],
                },
            )

        # Check 4 — conversation-anchor USER_DATA pointer shape + run-log
        # hash match. ``claim_evidence_map`` entries with
        # ``evidence_kind == "USER_DATA"`` must pair with a valid anchor.
        # The envelope's conversation_log_anchor string is the canonical
        # shape; parse-or-fail.
        conversation_anchor = _parse_envelope_conversation_anchor(envelope)
        bad_pointers = _check_anchor_pointers(
            sd.claim_evidence_map, conversation_anchor
        )
        if bad_pointers:
            _raise_scribe(
                failure_code=F_SCRIBE_CONVERSATION_ANCHOR_INVALID,
                trigger="user_data_source_pointer_does_not_match_envelope_anchor",
                evidence={
                    "section_name": sd.section_name,
                    "bad_pointers": bad_pointers,
                },
            )
        if conversation_anchor is not None:
            if conversation_anchor_verify(
                anchor=conversation_anchor, run_id=envelope.run_id
            ):
                _raise_scribe(
                    failure_code=F_SCRIBE_CONVERSATION_ANCHOR_INVALID,
                    trigger="conversation_anchor_hash_mismatch",
                    evidence={
                        "section_name": sd.section_name,
                        "run_id": envelope.run_id,
                        "turn_ordinal": conversation_anchor.turn_ordinal,
                    },
                )

    # Check 5 — admin-risk scan + HIGH-unapproved gate.
    # Scan the concatenated body of every section; the HIGH-unapproved
    # check is deterministic over ``admin_risk_flags``.
    concatenated_body = "\n\n".join(sd.body_text for sd in section_drafts)
    identity_claim_terms = tuple(
        c.claim for c in identity_claims if hasattr(c, "claim")
    )
    try:
        verify_draft_flags_or_raise(
            draft_body=concatenated_body,
            declared_flags=admin_risk_flags,
            register=admin_risk_register,
            funder_dialect=envelope.funder_dialect,
            identity_claim_terms=identity_claim_terms,
            auto_substitute_low_enabled=False,
        )
    except AdminRiskHighUnapproved as exc:
        _raise_scribe(
            failure_code=F_SCRIBE_ADMIN_RISK_HIGH_UNAPPROVED,
            trigger="high_severity_flag_not_applicant_approved",
            evidence={"exception": str(exc)},
        )
    except RuntimeError as exc:
        # admin_risk_adapter raises RuntimeError with F-SCRIBE-ADMIN-RISK-
        # UNFLAGGED embedded in its message; route through the canonical
        # F-code we've already pinned.
        message = str(exc)
        if F_SCRIBE_ADMIN_RISK_UNFLAGGED in message:
            _raise_scribe(
                failure_code=F_SCRIBE_ADMIN_RISK_UNFLAGGED,
                trigger="medium_or_high_severity_term_without_declared_flag",
                evidence={"exception": message},
            )
        raise

    # codes_checked reports which F-codes the assembler ACTUALLY enforces
    # at R3. Two §7 codes are out-of-scope at R3 by spec card §6 design and
    # therefore NOT advertised here:
    #
    # - F-SCRIBE-SMART-INVENTED-METRIC: shares the numeric-verbatim walker
    #   with F-SCRIBE-PARAPHRASED-NUMERIC (§7.6 SMART vs §7 generic numeric);
    #   distinct trip semantics (relevance-pointer set vs body-vs-evidence)
    #   land at the §5 R5+ revision-loop level once the SMART-relevance
    #   pointer table is bound to the SectionDraft surface.
    # - F-SCRIBE-EVALUATION-CRITERION-MISSING: full-draft exhaustiveness
    #   gate; cannot fire on a single-section invocation. Lands at §5 R5+
    #   when the multi-section draft accumulator is in scope.
    return PostGateAssembly(
        run_id=envelope.run_id,
        org_slug=envelope.org_slug,
        codes_checked=(
            F_SCRIBE_UNSOURCED_CLAIM,
            F_SCRIBE_PARAPHRASED_NUMERIC,
            F_SCRIBE_DIALECT_INDUCED_IDENTITY,
            F_SCRIBE_DIALECT_DRIFT,
            F_SCRIBE_SECTION_OVER_LIMIT_UNFLAGGED,
            F_SCRIBE_OVERLOOKED_EXPENSE_UNRESOLVED,
            F_SCRIBE_INELIGIBLE_ACTIVITY,
            F_SCRIBE_CONVERSATION_ANCHOR_INVALID,
            F_SCRIBE_ADMIN_RISK_UNFLAGGED,
            F_SCRIBE_ADMIN_RISK_HIGH_UNAPPROVED,
        ),
    )


# ---------------------------------------------------------------------------
# Envelope conversation-anchor parsing
# ---------------------------------------------------------------------------


def _parse_envelope_conversation_anchor(
    envelope: ScribeEnvelope,
) -> ConversationAnchor | None:
    """Parse ``envelope.conversation_log_anchor`` → ConversationAnchor.

    Envelope carries the anchor as the compact string
    ``"USER_DATA:<run_id>:<turn_ordinal>:<sha3_512_prefix32>"``. Returns
    None when no anchor is set. Raises ScribeGateFailed(F-SCRIBE-
    CONVERSATION-ANCHOR-INVALID) on malformed shape.
    """
    raw = envelope.conversation_log_anchor
    if raw is None:
        return None
    parts = raw.split(":")
    if len(parts) != 4 or parts[0] != "USER_DATA":
        _raise_scribe(
            failure_code=F_SCRIBE_CONVERSATION_ANCHOR_INVALID,
            trigger="envelope_anchor_malformed_shape",
            evidence={"raw": raw},
        )
    _, run_id_raw, turn_raw, prefix = parts
    try:
        turn_ordinal = int(turn_raw)
    except ValueError:
        _raise_scribe(
            failure_code=F_SCRIBE_CONVERSATION_ANCHOR_INVALID,
            trigger="envelope_anchor_turn_ordinal_not_int",
            evidence={"raw": raw, "turn_raw": turn_raw},
        )
    if run_id_raw != envelope.run_id:
        _raise_scribe(
            failure_code=F_SCRIBE_CONVERSATION_ANCHOR_INVALID,
            trigger="envelope_anchor_run_id_mismatch",
            evidence={
                "envelope_run_id": envelope.run_id,
                "anchor_run_id": run_id_raw,
            },
        )
    try:
        return ConversationAnchor(
            run_id=run_id_raw,
            turn_ordinal=turn_ordinal,
            sha3_512_prefix32=prefix,
        )
    except ValueError as exc:
        _raise_scribe(
            failure_code=F_SCRIBE_CONVERSATION_ANCHOR_INVALID,
            trigger="envelope_anchor_prefix_malformed",
            evidence={"raw": raw, "error": str(exc)},
        )
        # unreachable — _raise_scribe raises
        return None


__all__ = [
    # Protocol seams
    "CedarCrossOrgCheck",
    "KgieStatusGetter",
    "RfaDriftCheck",
    "TemplateDriftCheck",
    "SourceTagVerify",
    "ConversationAnchorVerify",
    "EvidenceTextProvider",
    "IdentityClaimProvider",
    # Result shapes
    "PreGateAssembly",
    "PostGateAssembly",
    # Assemblers
    "assemble_scribe_pre_gate",
    "assemble_scribe_post_gate",
]
