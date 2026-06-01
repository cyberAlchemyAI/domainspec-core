"""pipeline.seats.scribe — §7 Scribe grant-writing seat.

Blueprint anchor: ``pipeline/blueprint/v0.1/section_07_scribe.md`` **v1.1.1
LOCKED 2026-04-21**. Companion amendment:
``section_00_5_section_07_scribe_amendment.md`` (§0.5 v7 LOCKED 2026-04-21;
rows 118-158 register Scribe primitives).

Spec-card governance:

- Parent card: ``pipeline/engineering/spec_cards/section_7_council_seats_pipeline_modules.md``
- Round 1 (LOCKED 2026-04-21): ``section_07_scribe_round_1_types_and_kgie.md``
  ``types.py`` (Phase 0 + KGIE dataclasses) + ``kgie.py`` (pure deterministic
  preflight predicate). Zero-LLM, zero-network, zero-subprocess.
- Round 2 (LOCKED 2026-04-21): SMART generator (§7.6), overlooked-expenses
  walker (§7.7), funder-dialect code-switch (§7.8), program-template loader
  (§7.9). All deterministic shapers over R1 types.
- Round 2.5 (LOCKED 2026-04-22): SectionDraft composition shapes (§7.5) +
  compress counters (§7.10). Closes R3 soft prerequisite.
- Round 3 (this tranche): ``seat.py`` subprocess entry, Anthropic provider
  via ``pipeline.providers.anthropic`` (``provider_anthropic.py``),
  admin-risk register integration (``admin_risk_adapter.py``, §7.11), PRE /
  POST gate wiring (``logician_wiring.py``).

Import discipline (AST-lint R2 guard at parent ``pipeline.seats``):

- Seats may import from ``pipeline.logician`` (gate-code constants and
  exception classes) and ``pipeline.vault`` (draft + conversation-log
  persistence via the write dispatcher).
- Seats may NOT import from ``pipeline.loop`` — orchestration calls into
  seats via ``seat_runner.invoke_seat``, never the other way around.
- R3 adds subprocess boundary (seat.py main-entry) + Anthropic HTTPS egress
  via ``pipeline.providers.anthropic`` (provider_anthropic.py) + BYOK key
  fetch via injected ``KeyRetrieveCallable``. All outside those three
  channels remains stdlib + intra-package.

Five Operating Laws enforcement (see §7.2):

- Law 1 (RFA source of truth) — ``claim_evidence_map`` shape pinned at R2.5;
  R3 POST-gate ``F-SCRIBE-UNSOURCED-CLAIM`` verifies each claim's
  source_pointer resolves to RFA / PROJECT_CONTEXT / USER_DATA anchor.
- Law 2 (no boundary drift) — ``eligible_activity_map`` pinned at R2.5; R3
  POST-gate ``F-SCRIBE-INELIGIBLE-ACTIVITY`` (Scribe-owned, not generic
  Law-2) catches unmatched-without-flag invariant breaks.
- Law 3 (org isolation) — R3 PRE-gate ``F-SCRIBE-ORG-CROSS-REF`` via Cedar
  cross-org dossier evaluator injected at ``CedarCrossOrgCheck`` seam.
- Law 4 (apolitical sector language) — R2 dialect detector + R3 admin-risk
  register adapter + POST-gates ``F-SCRIBE-DIALECT-DRIFT`` /
  ``F-SCRIBE-DIALECT-INDUCED-IDENTITY`` /
  ``F-SCRIBE-ADMIN-RISK-{UNFLAGGED,HIGH-UNAPPROVED,REGISTER-STALE,…}``.
- Law 5 (applicant brings the substance) — R1 KGIE preflight predicate
  first-layer; R3 PRE-gate ``F-SCRIBE-KGIE-FAIL`` + ``F-SCRIBE-SCOPE-MISSING``
  wires fail-closed + operator-input branches.

Cross-family rigor: Scribe production binding = Anthropic per
``router.yaml``; downstream Editor / Judge / Red Team are non-Anthropic by
§D.2/D.3/D.4 architecture invariants.
"""

from __future__ import annotations

from typing import Final

from pipeline.seats.scribe.admin_risk_adapter import (
    F_SCRIBE_ADMIN_RISK_HIGH_UNAPPROVED,
    F_SCRIBE_ADMIN_RISK_REGISTER_MALFORMED,
    F_SCRIBE_ADMIN_RISK_REGISTER_STALE,
    F_SCRIBE_ADMIN_RISK_UNFLAGGED,
    SNAPSHOT_AGE_HOURS_CEILING,
    AdminRiskEntry,
    AdminRiskHighUnapproved,
    AdminRiskRegister,
    AdminRiskRegisterMalformed,
    AdminRiskRegisterStale,
    RegisterLoadCallable,
    load_admin_risk_register,
    parse_admin_risk_register,
    route_flag_for_match,
    scan_draft_for_admin_risk,
    verify_draft_flags_or_raise,
)
from pipeline.seats.scribe.compress import (
    count_characters,
    count_pages,
    count_words,
    is_over_limit,
)
from pipeline.seats.scribe.dialect import (
    DIALECT_IDENTITY_PROXY_TABLE,
    DIALECT_VOCABULARY,
    Dialect,
    detect_dialect_drift,
    detect_dialect_induced_identity,
    select_default_dialect,
)
from pipeline.seats.scribe.kgie import ClockFn, kgie_preflight
from pipeline.seats.scribe.logician_wiring import (
    CedarCrossOrgCheck,
    ConversationAnchorVerify,
    EvidenceTextProvider,
    IdentityClaimProvider,
    KgieStatusGetter,
    PostGateAssembly,
    PreGateAssembly,
    RfaDriftCheck,
    SourceTagVerify,
    TemplateDriftCheck,
    assemble_scribe_post_gate,
    assemble_scribe_pre_gate,
)
from pipeline.seats.scribe.overlooked_expenses import (
    DEFAULT_CHECKLIST,
    ExpenseStatus,
    OverlookedExpenseEntry,
    OverlookedExpensesWalk,
    build_default_checklist_walk,
    build_walk,
    is_finalizable,
)
from pipeline.seats.scribe.program_templates import (
    KNOWN_PROGRAMS,
    ProgramTemplate,
    build_known_template,
    compute_template_sha3_512,
)
from pipeline.seats.scribe.provider_anthropic import (
    F_SCRIBE_BYOK_MISSING,
    F_SCRIBE_PAYLOAD_CEILING,
    F_SCRIBE_PROVIDER_MALFORMED,
    F_SCRIBE_SEMANTIC_FAILURE,
    F_SCRIBE_TRANSPORT_FAILURE,
    AnthropicBinding,
    AnthropicBYOKMissing,
    AnthropicCallCallable,
    AnthropicPayloadCeiling,
    AnthropicProviderMalformed,
    AnthropicResponse,
    AnthropicSemanticFailure,
    AnthropicTransportFailure,
    HttpPostCallable,
    KeyRetrieveCallable,
    SleepFn,
    call_anthropic_scribe,
    estimate_prompt_tokens,
    load_scribe_binding_from_router_mapping,
)
from pipeline.seats.scribe.seat import (
    ENVELOPE_VERSION_V1,
    EXIT_GATE_FAIL,
    EXIT_INTERNAL_ERROR,
    EXIT_OK,
    F_SCRIBE_CONVERSATION_ANCHOR_INVALID,
    F_SCRIBE_DIALECT_DRIFT,
    F_SCRIBE_DIALECT_INDUCED_IDENTITY,
    F_SCRIBE_DIALECT_UNCLASSIFIED,
    F_SCRIBE_ENVELOPE_MALFORMED,
    F_SCRIBE_EVALUATION_CRITERION_MISSING,
    F_SCRIBE_INELIGIBLE_ACTIVITY,
    F_SCRIBE_ORG_CROSS_REF,
    F_SCRIBE_OVERLOOKED_EXPENSE_UNRESOLVED,
    F_SCRIBE_PARAPHRASED_NUMERIC,
    F_SCRIBE_SCOPE_MISSING,
    F_SCRIBE_SECTION_OVER_LIMIT_UNFLAGGED,
    F_SCRIBE_SMART_INVENTED_METRIC,
    F_SCRIBE_TEMPLATE_DRIFT,
    F_SCRIBE_TEMPLATE_UNKNOWN,
    F_SCRIBE_UNSOURCED_CLAIM,
    RESULT_VERSION_V1,
    AdminRiskRegisterFetch,
    PostGateCallable,
    PreGateCallable,
    ResponseParseCallable,
    ScribeEnvelope,
    ScribeEnvelopeMalformed,
    ScribeGateFailed,
    ScribeResult,
    decode_envelope,
    encode_result,
    run_seat,
)
from pipeline.seats.scribe.section_draft import (
    AdminRiskFlag,
    AdminRiskSeverity,
    ClaimEvidence,
    CompressedSectionDraft,
    ConversationAnchor,
    EligibleActivityMatch,
    EvidenceKind,
    LimitKind,
    ScopeCheckComment,
    SectionDraft,
    SectionLimit,
)
from pipeline.seats.scribe.smart import (
    VIOLATION_MISSING_ACHIEVABILITY,
    VIOLATION_MISSING_MEASUREMENT,
    VIOLATION_MISSING_OBJECTIVE,
    VIOLATION_MISSING_OUTCOME,
    VIOLATION_MISSING_TIMELINE,
    VIOLATION_NO_RELEVANCE_POINTER,
    SmartObjective,
    check_numeric_verbatim,
    extract_numeric_tokens,
    validate_smart_objective,
)
from pipeline.seats.scribe.types import (
    DateTimeWithTimezone,
    EvaluationCriterion,
    ExperienceSummary,
    F_SCRIBE_KGIE_FAIL,
    F_SCRIBE_PHASE_0_MISSING,
    F_SCRIBE_RFA_DRIFT,
    F_SCRIBE_RFA_MISSING,
    GeographyRecord,
    IdentityClaim,
    KeywordAffirmation,
    KeywordCheck,
    KgiePreflightResult,
    KgieStatus,
    MatchRequirement,
    RfaExtractedRecord,
    SectionSpec,
)

# BLUEPRINT_DEPS — engineering-process §4.6 hash-pinned citation block.
# Hashes computed 2026-04-22 at R3 landing. L-015 sweep currently scoped to
# ``pipeline.vault``; citation block is rendered in the canonical shape so a
# future scope-expansion picks up Scribe cleanly.
BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_07_scribe.md": {
        "version": "v1.1.1",
        "hash_sha3_512_prefix16": "e793055d257ae56b",
        "sections_implemented": [
            "§7.3 RfaExtractedRecord (Phase 0 shape)",
            "§7.4 KgiePreflightResult (KGIE preflight contract)",
            "§7.4a ConversationAnchor (USER_DATA source pointer)",
            "§7.5 SectionDraft + nested shapes (canonical output contract)",
            "§7.6 SmartObjective + numeric-verbatim helpers",
            "§7.7 OverlookedExpensesWalk + default 11-item checklist",
            "§7.8 Dialect vocabulary + drift / induced-identity detectors",
            "§7.9 ProgramTemplate + KNOWN_PROGRAMS registry (8 programs)",
            "§7.10 compress counters + is_over_limit predicate",
            "§7.11 AdminRiskFlag + admin-risk register adapter (R3)",
            "§7.12 Scribe subprocess entry + Anthropic provider binding (R3)",
            "§7.13 F-SCRIBE-* failure-code family (23 codes at R3)",
        ],
    },
    "section_00_5_section_07_scribe_amendment.md": {
        "version": "§0.5 v7",
        "hash_sha3_512_prefix16": "b99312d9a3ba3527",
        "sections_implemented": [
            "§A rows 118 (rfa_extracted_record schema)",
            "§A rows 119 (kgie_preflight_result schema)",
            "§A rows 120 (smart_objective schema)",
            "§A rows 121 (overlooked_expenses_walk schema)",
            "§A rows 122 (program_template schema)",
            "§A rows 123 (DIALECT_VOCABULARY closed-set)",
            "§A rows 124 (DIALECT_IDENTITY_PROXY_TABLE closed-set + ClaimEvidence schema)",
            "§A rows 125 (AdminRiskFlag schema)",
            "§A rows 126 (EligibleActivityMatch schema)",
            "§A rows 127 (ConversationAnchor schema)",
            "§A rows 132 (F-SCRIBE-RFA-MISSING failure code)",
            "§A rows 133 (F-SCRIBE-RFA-DRIFT failure code)",
            "§A rows 134 (F-SCRIBE-PHASE-0-MISSING failure code)",
            "§A rows 135 (F-SCRIBE-KGIE-FAIL failure code)",
            "§A rows 154 (scribe.pre_gate.kgie_pass.v1)",
        ],
    },
    "section_04_logician.md": {
        "version": "v2.1",
        "hash_sha3_512_prefix16": "b7e5439cac97b2fe",
        "sections_implemented": [
            "§4.2.1 PRE-gate slot table (8 Scribe PRE-gate F-codes wired at R3)",
            "§4.2.2 POST-gate slot table (11 Scribe POST-gate F-codes wired at R3)",
        ],
    },
    "section_06_operating_envelope.md": {
        "version": "v1-r1",
        "hash_sha3_512_prefix16": "f4a55d9650489531",
        "sections_implemented": [
            "§6.3 Anthropic provider tokenizer bound + payload-ceiling discipline",
            "§6.11 compiled_prompt_shell_sha3_512 envelope→result passthrough",
            "§6.13 24.0h admin-risk snapshot-age ceiling (inline-literal)",
        ],
    },
    "section_05_pipeline.md": {
        "version": "v6",
        "hash_sha3_512_prefix16": "feb5928491e4dc40",
        "sections_implemented": [
            "§4.1 step 4 seat-invocation contract (subprocess entry, A-v1-13 minimal-env)",
            "§5.7 structured stderr single-line JSON on gate-trip",
        ],
    },
    "section_02_vault_topology.md": {
        "version": "v7.1",
        "hash_sha3_512_prefix16": "83a898275a4cf0a1",
        "sections_implemented": [
            "§2.4 conversation_log kind-class (§7.4a anchor persistence target)",
        ],
    },
}

__all__ = [
    # Phase 0 shapes
    "RfaExtractedRecord",
    "MatchRequirement",
    "EvaluationCriterion",
    "SectionSpec",
    "DateTimeWithTimezone",
    # KGIE shapes
    "KgiePreflightResult",
    "KgieStatus",
    "KeywordAffirmation",
    "KeywordCheck",
    "GeographyRecord",
    "IdentityClaim",
    "ExperienceSummary",
    # KGIE predicate
    "kgie_preflight",
    "ClockFn",
    # §7.13 R1+R2 failure-code constants
    "F_SCRIBE_RFA_MISSING",
    "F_SCRIBE_RFA_DRIFT",
    "F_SCRIBE_PHASE_0_MISSING",
    "F_SCRIBE_KGIE_FAIL",
    # §7.6 SMART
    "SmartObjective",
    "validate_smart_objective",
    "extract_numeric_tokens",
    "check_numeric_verbatim",
    "VIOLATION_MISSING_OBJECTIVE",
    "VIOLATION_MISSING_OUTCOME",
    "VIOLATION_MISSING_MEASUREMENT",
    "VIOLATION_MISSING_TIMELINE",
    "VIOLATION_MISSING_ACHIEVABILITY",
    "VIOLATION_NO_RELEVANCE_POINTER",
    # §7.7 Overlooked-expenses
    "ExpenseStatus",
    "DEFAULT_CHECKLIST",
    "OverlookedExpenseEntry",
    "OverlookedExpensesWalk",
    "build_walk",
    "build_default_checklist_walk",
    "is_finalizable",
    # §7.8 Dialect
    "Dialect",
    "DIALECT_VOCABULARY",
    "DIALECT_IDENTITY_PROXY_TABLE",
    "detect_dialect_drift",
    "detect_dialect_induced_identity",
    "select_default_dialect",
    # §7.9 Program templates
    "ProgramTemplate",
    "KNOWN_PROGRAMS",
    "compute_template_sha3_512",
    "build_known_template",
    # §7.10 compress counters
    "count_words",
    "count_characters",
    "count_pages",
    "is_over_limit",
    # §7.5 SectionDraft + nested shapes
    "SectionDraft",
    "SectionLimit",
    "ClaimEvidence",
    "EligibleActivityMatch",
    "AdminRiskFlag",
    "ScopeCheckComment",
    "ConversationAnchor",
    "CompressedSectionDraft",
    "EvidenceKind",
    "AdminRiskSeverity",
    "LimitKind",
    # R3 — Scribe subprocess seat entry
    "run_seat",
    "ScribeEnvelope",
    "ScribeResult",
    "ScribeEnvelopeMalformed",
    "ScribeGateFailed",
    "decode_envelope",
    "encode_result",
    "ENVELOPE_VERSION_V1",
    "RESULT_VERSION_V1",
    "EXIT_OK",
    "EXIT_INTERNAL_ERROR",
    "EXIT_GATE_FAIL",
    "PreGateCallable",
    "PostGateCallable",
    "ResponseParseCallable",
    "AdminRiskRegisterFetch",
    # R3 — Anthropic provider binding
    "AnthropicBinding",
    "AnthropicResponse",
    "call_anthropic_scribe",
    "load_scribe_binding_from_router_mapping",
    "estimate_prompt_tokens",
    "AnthropicBYOKMissing",
    "AnthropicPayloadCeiling",
    "AnthropicTransportFailure",
    "AnthropicSemanticFailure",
    "AnthropicProviderMalformed",
    "AnthropicCallCallable",
    "HttpPostCallable",
    "KeyRetrieveCallable",
    "SleepFn",
    # R3 — Admin-risk adapter
    "AdminRiskRegister",
    "AdminRiskEntry",
    "scan_draft_for_admin_risk",
    "load_admin_risk_register",
    "parse_admin_risk_register",
    "route_flag_for_match",
    "verify_draft_flags_or_raise",
    "AdminRiskRegisterMalformed",
    "AdminRiskRegisterStale",
    "AdminRiskHighUnapproved",
    "RegisterLoadCallable",
    "SNAPSHOT_AGE_HOURS_CEILING",
    # R3 — Logician wiring (PRE + POST assemblers + Protocol seams)
    "assemble_scribe_pre_gate",
    "assemble_scribe_post_gate",
    "PreGateAssembly",
    "PostGateAssembly",
    "CedarCrossOrgCheck",
    "KgieStatusGetter",
    "RfaDriftCheck",
    "TemplateDriftCheck",
    "SourceTagVerify",
    "ConversationAnchorVerify",
    "EvidenceTextProvider",
    "IdentityClaimProvider",
    # R3 — Provider + seat + wiring + adapter F-SCRIBE-* failure-code constants
    "F_SCRIBE_BYOK_MISSING",
    "F_SCRIBE_PAYLOAD_CEILING",
    "F_SCRIBE_TRANSPORT_FAILURE",
    "F_SCRIBE_SEMANTIC_FAILURE",
    "F_SCRIBE_PROVIDER_MALFORMED",
    "F_SCRIBE_ENVELOPE_MALFORMED",
    "F_SCRIBE_ORG_CROSS_REF",
    "F_SCRIBE_SCOPE_MISSING",
    "F_SCRIBE_DIALECT_UNCLASSIFIED",
    "F_SCRIBE_TEMPLATE_UNKNOWN",
    "F_SCRIBE_TEMPLATE_DRIFT",
    "F_SCRIBE_UNSOURCED_CLAIM",
    "F_SCRIBE_PARAPHRASED_NUMERIC",
    "F_SCRIBE_DIALECT_DRIFT",
    "F_SCRIBE_DIALECT_INDUCED_IDENTITY",
    "F_SCRIBE_CONVERSATION_ANCHOR_INVALID",
    "F_SCRIBE_SECTION_OVER_LIMIT_UNFLAGGED",
    "F_SCRIBE_OVERLOOKED_EXPENSE_UNRESOLVED",
    "F_SCRIBE_SMART_INVENTED_METRIC",
    "F_SCRIBE_EVALUATION_CRITERION_MISSING",
    "F_SCRIBE_INELIGIBLE_ACTIVITY",
    "F_SCRIBE_ADMIN_RISK_UNFLAGGED",
    "F_SCRIBE_ADMIN_RISK_HIGH_UNAPPROVED",
    "F_SCRIBE_ADMIN_RISK_REGISTER_STALE",
    "F_SCRIBE_ADMIN_RISK_REGISTER_MALFORMED",
    # Blueprint pin
    "BLUEPRINT_DEPS",
]
