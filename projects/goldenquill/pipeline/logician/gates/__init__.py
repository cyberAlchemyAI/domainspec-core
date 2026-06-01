"""Section 4 — Logician per-gate modules (v2.2 Wave 1 / Wave 2 / Wave 3).

Gates operate on in-memory verdict dicts with no external deps beyond
the §4 v2.1 gate-runner invocation surface. Each gate is a pure-Python
deterministic predicate: zero LLM tokens, fail-closed, returns a frozen
kw-only dataclass result. Callers (gate_runner / pipeline orchestrator) are
responsible for persisting structured failure records to
``pipeline/metrics/session_log.jsonl`` — gate modules never touch disk.

Blueprint anchor: ``pipeline/blueprint/v0.1/section_04_logician.md`` v2.1
(current LOCK); v2.2 delta rows for F-AMDT-01 / F-AMDT-02 / F-AMDT-03 /
F-AMDT-04 / F-AMDT-05 / F-AMDT-06 / F-AMDT-07 / F-AMDT-08 / F-AMDT-09 /
F-AMDT-10 / F-AMDT-11 / F-AMDT-12.
"""

from __future__ import annotations

from pipeline.logician.gates._protocols import (
    AuditArtifactReaderCallable,
    ClockProtocol,
    DailyLogReaderCallable,
    DeprecationFeedReaderCallable,
    DeprecationRegisterReaderCallable,
    ExternalManifestReaderCallable,
    FileExistsCallable,
    HashBytesCallable,
    LedgerHashReaderCallable,
    LockHistoryReaderCallable,
    PinnedHashReaderCallable,
    PriorChainHeadReaderCallable,
    RouterConfigReaderCallable,
    RouterYamlReaderCallable,
    ScriptMetadataReaderCallable,
    SignatureVerifyCallable,
    StanzaReaderCallable,
)
from pipeline.logician.gates.f_bootstrap_reuse import (
    F_AMDT_01,
    BootstrapReuseDetail,
    BootstrapReuseResult,
    check_bootstrap_reuse,
)
from pipeline.logician.gates.f_committee_degradation_timeout import (
    CommitteeDegradationTimeoutDetail,
    CommitteeDegradationTimeoutResult,
    ESCALATE_THRESHOLD_DAYS,
    EVENT_CLOCK_SKEW_WARN,
    EVENT_ESCALATE,
    EVENT_READER_FAIL,
    EVENT_SUSPEND,
    EVENT_WARN,
    F_AMDT_08,
    F_AMDT_08_ESCALATE,
    F_AMDT_08_READER_FAIL,
    F_AMDT_08_SUSPEND,
    SUSPEND_THRESHOLD_DAYS,
    WARN_THRESHOLD_DAYS,
    check_committee_degradation_timeout,
)
from pipeline.logician.gates.f_amendment_self_reference_detect import (
    F_AMDT_07,
    F_AMDT_07_AUTHOR_COLLISION,
    SelfReferenceDetail,
    SelfReferenceResult,
    check_amendment_self_reference,
)
from pipeline.logician.gates.f_daily_log_lock_block_missing import (
    F_AMDT_12,
    F_AMDT_12_MALFORMED,
    F_AMDT_12_MISSING,
    F_AMDT_12_READER_FAIL,
    DailyLogBlockDetail,
    DailyLogBlockResult,
    check_daily_log_lock_block,
)
from pipeline.logician.gates.f_degradation_stanza_precedence import (
    EVENT_CARVEOUT_GRANTED,
    EVENT_KIND_PROMOTION,
    EVENT_KIND_STANZA,
    EVENT_PRECEDENCE_MIXED,
    F_AMDT_11,
    F_AMDT_11_DEADLOCK_CARVEOUT_VIOLATION,
    F_AMDT_11_PRECEDENCE_EMPTY,
    F_AMDT_11_READER_FAIL,
    StanzaPrecedenceDetail,
    StanzaPrecedenceResult,
    check_degradation_stanza_precedence,
)
from pipeline.logician.gates.f_deprecation_exemption_reuse import (
    F_AMDT_06,
    DeprecationExemptionDetail,
    DeprecationExemptionResult,
    check_deprecation_exemption_reuse,
)
from pipeline.logician.gates.f_deprecation_register_staleness import (
    EVENT_AMBIGUOUS,
    EVENT_CLOCK_SKEW_REGISTER_AHEAD,
    EVENT_MISSING,
    EVENT_NOT_DEPRECATED_OVERRIDE,
    EVENT_STALE,
    F_AMDT_09,
    F_AMDT_09_AMBIGUOUS,
    F_AMDT_09_MISSING,
    F_AMDT_09_READER_FAIL,
    F_AMDT_09_STALE,
    STALENESS_WINDOW_HOURS,
    DeprecationRegisterStalenessDetail,
    DeprecationRegisterStalenessResult,
    check_deprecation_register_staleness,
)
from pipeline.logician.gates.f_sdk_precedent_reuse import (
    EVENT_REUSE,
    F_AMDT_04,
    F_AMDT_04_AMBIGUOUS,
    F_AMDT_04_READER_FAIL,
    F_AMDT_04_REUSE,
    SdkPrecedentReuseDetail,
    SdkPrecedentReuseResult,
    check_sdk_precedent_reuse,
)
from pipeline.logician.gates.f_rollback_script_integrity import (
    F_AMDT_05,
    RollbackScriptIntegrityDetail,
    RollbackScriptIntegrityResult,
    check_rollback_script_integrity,
)
from pipeline.logician.gates.f_router_integrity_multi_source import (
    F_AMDT_10,
    F_AMDT_10_CHAIN_BREAK,
    F_AMDT_10_EXTERNAL,
    F_AMDT_10_PAIR,
    F_AMDT_10_READER_FAIL,
    F_AMDT_10_SIGNATURE,
    RouterIntegrityDetail,
    RouterIntegrityResult,
    check_router_integrity_multi_source,
)
from pipeline.logician.gates.f_verdict_blocking_missing import (
    F_AMDT_02,
    BlockingMissingDetail,
    BlockingMissingResult,
    check_verdict_blocking,
)
from pipeline.logician.gates.f_verdict_citation_missing import (
    F_AMDT_03,
    CitationMissingDetail,
    CitationMissingResult,
    DimensionCitationFailure,
    DraftReaderCallable,
    check_verdict_citations,
)
from pipeline.logician.gates.f_logician_fabricated_org import (
    DEFAULT_ALLOWLIST_FIELDS,
    DEFAULT_FUZZY_THRESHOLD,
    F_LOGICIAN_FABRICATED_ORG,
    FabricatedOrgFinding,
    FabricatedOrgGateResult,
    build_org_allowlist,
    check_fabricated_orgs,
    extract_org_entities,
)
from pipeline.logician.gates.f_logician_spine_drift import (
    DEFAULT_KEYWORD_RECALL_THRESHOLD,
    F_LOGICIAN_SPINE_DRIFT,
    CrossSectionAnchor,
    NarrativeSpine,
    SmartOutcomeShape,
    SpineDriftFinding,
    SpineDriftGateResult,
    SpineFraming,
    SpineSchemaError,
    check_spine_drift,
    load_spine,
)
from pipeline.logician.gates.f_logician_fact_drift import (
    DEFAULT_VALUE_TOLERANCE_PCT,
    F_LOGICIAN_FACT_DRIFT,
    MATCH_JACCARD_THRESHOLD,
    FactDriftFinding,
    FactDriftGateResult,
    KeyFactsRegister,
    KfrFact,
    KfrSchemaError,
    NumericClaim,
    TemporalWindow,
    ValidationBlock,
    check_fact_drift,
    extract_numeric_claims,
    load_kfr,
)

# ---------------------------------------------------------------------------
# v0.2 / WS-L gate families (architecture v7.0.4 KFR + v7.0.5 Funder Intel +
# v7.0.7 Classification dormant primitives + v2.7 Uploader). Wired into the
# package surface here; full registration in §4 v2.x amendment per WS-L.
# ---------------------------------------------------------------------------

# Funder Intel family (v7.0.5 §5; LOCKED 2026-05-10 row 179)
from pipeline.logician.gates.f_match_db_cross_org import (
    F_MATCH_DB_CROSS_ORG,
    MatchDbCrossOrgResult,
    check_match_db_cross_org,
)
from pipeline.logician.gates.f_vector_ns_mismatch import (
    F_VECTOR_NS_MISMATCH,
    PER_ORG_NAMESPACE_PREFIXES,
    WORKSPACE_SCOPED_NAMESPACES,
    VectorNsMismatchResult,
    check_vector_ns_mismatch,
)
from pipeline.logician.gates.f_channel_g_cross_org_leak import (
    F_CHANNEL_G_CROSS_ORG_LEAK,
    ChannelGLeakResult,
    check_channel_g_cross_org_leak,
)
from pipeline.logician.gates.f_channel_g_sanitization_bypass import (
    F_CHANNEL_G_SANITIZATION_BYPASS,
    SanitizationBypassResult,
    check_channel_g_sanitization_bypass,
)
from pipeline.logician.gates.f_match_db_consent_tier_violation import (
    CONSENT_TIER_SIGNATURE_KIND,
    F_MATCH_DB_CONSENT_TIER_VIOLATION,
    PERMITTED_CONSENT_TIERS,
    ConsentTierViolationResult,
    check_match_db_consent_tier_violation,
)
from pipeline.logician.gates.f_funder_corpus_stale import (
    DEFAULT_STALE_THRESHOLD_DAYS,
    F_FUNDER_CORPUS_STALE,
    FUNDER_TYPE_STALE_THRESHOLD_DAYS,
    FunderCorpusStaleResult,
    check_funder_corpus_stale,
)
from pipeline.logician.gates.f_funder_corpus_integrity import (
    F_FUNDER_CORPUS_INTEGRITY,
    FunderCorpusIntegrityResult,
    check_funder_corpus_integrity,
)

# KFR family residuals (v7.0.4 §1.1 / §3.2 / §4.4 / §5.2 / §5.3 / §7.2;
# WS-L Slice 2 LANDED 2026-05-10)
from pipeline.logician.gates.f_extractor_fabrication import (
    F_EXTRACTOR_FABRICATION,
    MODE_AWARD_INGEST,
    MODE_BULK_INGEST,
    MODE_INCREMENTAL_INGEST,
    PERMITTED_MODES as EXTRACTOR_PERMITTED_MODES,
    PERMITTED_SUBSTRATES as EXTRACTOR_PERMITTED_SUBSTRATES,
    SUBSTRATE_DOCX,
    SUBSTRATE_MARKDOWN,
    SUBSTRATE_PDF,
    CandidateFact,
    ExtractorFabricationResult,
    check_extractor_fabrication,
)
from pipeline.logician.gates.f_extractor_award_signature_invalid import (
    F_EXTRACTOR_AWARD_SIGNATURE_INVALID,
    F_EXTRACTOR_AWARD_SIGNATURE_INVALID_AWARD,
    F_EXTRACTOR_AWARD_SIGNATURE_INVALID_PROPOSAL,
    AwardSignatureLeg,
    AwardSignatureResult,
    check_extractor_award_signature_invalid,
)
from pipeline.logician.gates.f_kfr_signature_validation import (
    AUDIT_CHAIN_KIND_INITIAL,
    AUDIT_CHAIN_KIND_SP0_REVIEW,
    AUDIT_CHAIN_PERMITTED_KINDS,
    F_KFR_AUDIT_CHAIN_BROKEN,
    F_KFR_SIGNATURE_INVALID,
    KEY_ROTATION_MARKER_KIND,
    KeyringEntry,
    KfrSignatureValidationResult,
    check_kfr_audit_chain_broken,
    check_kfr_signature_invalid,
)
from pipeline.logician.gates.f_logician_fact_tolerance_drift import (
    F_LOGICIAN_FACT_TOLERANCE_DRIFT,
    LEDGER_KIND_WIDEN,
    LEDGER_KIND_WIDEN_RECONFIRM,
    TYPE_DEFAULT_TOLERANCE_PCT,
    FactToleranceDriftResult,
    check_fact_tolerance_drift,
)
from pipeline.logician.gates.f_logician_fact_needed_required import (
    F_LOGICIAN_FACT_NEEDED_REQUIRED,
    NEEDED_STATUS_VALUES,
    FactNeededRequiredResult,
    NeededFactGap,
    check_fact_needed_required,
)
from pipeline.logician.gates.f_benchmark_contains_per_org_ref import (
    DEFAULT_VALUE_TOLERANCE_PCT as BENCHMARK_DEFAULT_VALUE_TOLERANCE_PCT,
    F_BENCHMARK_CONTAINS_PER_ORG_REF,
    F_BENCHMARK_CONTAINS_PER_ORG_REF_PATH,
    F_BENCHMARK_CONTAINS_PER_ORG_REF_VALUE,
    BenchmarkPerOrgRefResult,
    PerOrgValueProbe,
    check_benchmark_contains_per_org_ref,
)

# Uploader family (v2.7 SCOPING DRAFT; WS-F in-flight Audit #1; modules
# already on disk pending re-convergence at WS-F LOCK)
from pipeline.logician.gates.f_uploader_package_incomplete import (
    F_UPLOADER_PACKAGE_INCOMPLETE,
    PackageIncompleteResult,
    check_uploader_package_incomplete,
)
from pipeline.logician.gates.f_uploader_format_mismatch import (
    F_UPLOADER_FORMAT_MISMATCH,
    check_uploader_format_mismatch,
)
from pipeline.logician.gates.f_uploader_autosubmit_attempted import (
    F_UPLOADER_AUTOSUBMIT_ATTEMPTED,
    check_uploader_autosubmit_attempted,
)
from pipeline.logician.gates.f_uploader_signature_missing import (
    F_UPLOADER_SIGNATURE_MISSING,
    SignatureMissingResult,
    check_uploader_signature_missing,
)
from pipeline.logician.gates.f_uploader_signature_mismatch import (
    F_UPLOADER_SIGNATURE_MISMATCH,
    check_uploader_signature_mismatch,
)
from pipeline.logician.gates.f_uploader_content_mutation import (
    F_UPLOADER_CONTENT_MUTATION,
    check_uploader_content_mutation,
)
from pipeline.logician.gates.f_uploader_input_inconsistent import (
    F_UPLOADER_INPUT_INCONSISTENT,
    check_uploader_input_inconsistent,
)
from pipeline.logician.gates.f_uploader_rfa_missing import (
    F_UPLOADER_RFA_MISSING,
    check_uploader_rfa_missing,
)
from pipeline.logician.gates.f_uploader_org_cross_ref import (
    F_UPLOADER_ORG_CROSS_REF,
    OrgCrossRefResult,
    check_uploader_org_cross_ref,
)
from pipeline.logician.gates.f_uploader_attachment_missing import (
    F_UPLOADER_ATTACHMENT_MISSING,
    check_uploader_attachment_missing,
)
from pipeline.logician.gates.f_uploader_attachment_tampered import (
    F_UPLOADER_ATTACHMENT_TAMPERED,
    check_uploader_attachment_tampered,
)

# F-CLASS-* dormant primitives (v7.0.7 §5.1; LOCKED 2026-05-10 row 180;
# WS-L Slice 3 LANDED 2026-05-10) — twelve primitives across seven
# modules; consolidated per the v2.2 F-AMDT-08/09/10/11 sub-code-collapse
# precedent.
from pipeline.logician.gates.f_class_register import (
    F_CLASS_REGISTER_HASH_MISMATCH,
    F_CLASS_REGISTER_MISSING,
    F_CLASS_REGISTER_SIGNATURE_INVALID,
    F_CLASS_REGISTER_UNSIGNED,
    SIGN_OFF_HASH_CLASS_KEY,
    SIGN_OFF_HASH_FIELDS_KEY,
    SIGN_OFF_KEY,
    ClassRegisterResult,
    check_class_register_hash_mismatch,
    check_class_register_missing,
    check_class_register_signature_invalid,
    check_class_register_unsigned,
)
from pipeline.logician.gates.f_class_outbound_boundary import (
    CLASS_CONFIDENTIAL as OUTBOUND_CLASS_CONFIDENTIAL,
    CLASS_OPERATOR_FLAGGED as OUTBOUND_CLASS_OPERATOR_FLAGGED,
    CLASS_PUBLIC as OUTBOUND_CLASS_PUBLIC,
    CLASS_SHAREABLE as OUTBOUND_CLASS_SHAREABLE,
    ClassifiedValue,
    F_CLASS_CLOUD_RECEIVED_CONFIDENTIAL,
    F_CLASS_CLOUD_RECEIVED_OPAQUE_SLOT_FILLED,
    F_CLASS_HIGH_STAKES_FLAG_LEAK,
    F_CLASS_SLOT_ID_NON_OPAQUE,
    OutboundBoundaryResult,
    SlotPosition,
    check_class_cloud_received_confidential,
    check_class_cloud_received_opaque_slot_filled,
    check_class_high_stakes_flag_leak,
    check_class_slot_id_non_opaque,
)
from pipeline.logician.gates.f_class_routing_indeterminate import (
    CallInput,
    F_CLASS_ROUTING_INDETERMINATE,
    PERMITTED_CLASSES as ROUTING_PERMITTED_CLASSES,
    RoutingIndeterminateResult,
    check_class_routing_indeterminate,
)
from pipeline.logician.gates.f_class_new_fact_unclassified import (
    F_CLASS_NEW_FACT_UNCLASSIFIED,
    IncrementalFact,
    NewFactUnclassifiedResult,
    PENDING_OPERATOR_REVIEW,
    check_class_new_fact_unclassified,
)
from pipeline.logician.gates.f_class_per_grant_override import (
    F_CLASS_PER_GRANT_OVERRIDE_UNSIGNED,
    PER_GRANT_SP0_SIGNATURE_KEY,
    PerGrantOverrideResult,
    check_class_per_grant_override_unsigned,
)
from pipeline.logician.gates.f_class_router_template_signature import (
    F_CLASS_ROUTER_TEMPLATE_SIGNATURE_INVALID,
    RouterTemplateSignatureResult,
    check_class_router_template_signature_invalid,
)
from pipeline.logician.gates.f_class_coverage_incomplete import (
    CoverageEntry,
    CoverageIncompleteResult,
    F_CLASS_COVERAGE_INCOMPLETE,
    REQUIRED_F_CLASS_CODES,
    check_class_coverage_incomplete,
)
from pipeline.logician.gates.f_class_voice_confidential_cloud_stt import (
    F_CLASS_VOICE_CONFIDENTIAL_CLOUD_STT,
    POSTURE_LOCAL_ONLY,
    POSTURE_PUBLIC_FRONTIER,
    POSTURE_SPLIT_CONTEXT,
    VoiceConfidentialCloudSttResult,
    check_voice_confidential_cloud_stt,
)

# CIC × CLC orthogonality family (v7.0.8 LOCKED 2026-05-08 row 175) uses a
# different export convention (GATE_ID + run() rather than F_* + check_*) and
# is outside WS-L scope — tests import those gates directly from their
# modules; not wired into the package __init__ surface.

# ---------------------------------------------------------------------------
# WS-L Slice 4 — v7.0.4-M1 corrective gate family (LANDED 2026-05-10).
# Architecture v7.0.4-M1 §10 lists the nineteen failure codes; this block
# imports each gate's surface so the package __init__.py exposes them.
# ---------------------------------------------------------------------------

from pipeline.logician.gates.f_kfr_yaml_construct_forbidden import (
    F_KFR_YAML_CONSTRUCT_FORBIDDEN,
    YamlConstructForbiddenResult,
    check_kfr_yaml_construct_forbidden,
)
from pipeline.logician.gates.f_kfr_canonical_signature_invalid import (
    F_KFR_CANONICAL_SIGNATURE_INVALID,
    CanonicalSignatureResult,
    check_kfr_canonical_signature_invalid,
)
from pipeline.logician.gates.f_kfr_legacy_accept_re_enabled_unsigned import (
    F_KFR_LEGACY_ACCEPT_RE_ENABLED_UNSIGNED,
    LEDGER_KIND_LEGACY_RE_ENABLE,
    LegacyAcceptReEnabledResult,
    check_kfr_legacy_accept_re_enabled_unsigned,
)
from pipeline.logician.gates.f_kfr_path_symlink_forbidden import (
    F_KFR_PATH_SYMLINK_FORBIDDEN,
    PathSymlinkForbiddenResult,
    check_kfr_path_symlink_forbidden,
)
from pipeline.logician.gates.f_kfr_tag_modified import (
    F_KFR_TAG_MODIFIED,
    LEDGER_KIND_TAG_MODIFIED,
    TRACKED_TAG_FIELDS,
    TagModifiedResult,
    check_kfr_tag_modified,
    compute_tag_set_hash,
)
from pipeline.logician.gates.f_kfr_duplicate_key import (
    COMPOSITE_KEY_BYTE_LEN,
    F_KFR_DUPLICATE_KEY,
    DuplicateKeyResult,
    check_kfr_duplicate_key,
    compute_composite_key,
)
from pipeline.logician.gates.f_derivation_ast_forbidden_node import (
    F_DERIVATION_AST_FORBIDDEN_NODE,
    AstForbiddenNodeResult,
    check_derivation_ast_forbidden_node,
)
from pipeline.logician.gates.f_derivation_runtime_arithmetic_error import (
    F_DERIVATION_RUNTIME_ARITHMETIC_ERROR,
    SUB_TAG_DIVIDE_BY_ZERO,
    SUB_TAG_INVALID_OPERATION,
    SUB_TAG_OTHER,
    SUB_TAG_OVERFLOW,
    DerivationArithmeticErrorResult,
    check_derivation_runtime_arithmetic_error,
    classify_arithmetic_error,
)
from pipeline.logician.gates.f_benchmark_cross_check_audit_missing import (
    F_BENCHMARK_CROSS_CHECK_AUDIT_MISSING,
    CrossCheckAuditResult,
    check_benchmark_cross_check_audit_missing,
)
from pipeline.logician.gates.f_benchmark_seeding_source_unauthorized import (
    F_BENCHMARK_SEEDING_SOURCE_UNAUTHORIZED,
    SeedingSourceUnauthorizedResult,
    check_benchmark_seeding_source_unauthorized,
)
from pipeline.logician.gates.f_benchmark_seeding_allowlist_signature_invalid import (
    F_BENCHMARK_SEEDING_ALLOWLIST_SIGNATURE_INVALID,
    AllowlistSignatureResult,
    check_benchmark_seeding_allowlist_signature_invalid,
)
from pipeline.logician.gates.f_currency_float_in_comparison import (
    F_CURRENCY_FLOAT_IN_COMPARISON,
    CurrencyFloatResult,
    check_currency_float_in_comparison,
)
from pipeline.logician.gates.f_currency_context_omitted import (
    F_CURRENCY_CONTEXT_OMITTED,
    CurrencyContextOmittedResult,
    check_currency_context_omitted,
)
from pipeline.logician.gates.f_currency_context_mismatch import (
    F_CURRENCY_CONTEXT_MISMATCH,
    CurrencyContextMismatchResult,
    check_currency_context_mismatch,
)
from pipeline.logician.gates.f_currency_decimal_context_drift import (
    F_CURRENCY_DECIMAL_CONTEXT_DRIFT,
    CurrencyContextDriftResult,
    check_currency_decimal_context_drift,
)
from pipeline.logician.gates.f_currency_unit_mismatch import (
    F_CURRENCY_UNIT_MISMATCH,
    CurrencyUnitMismatchResult,
    check_currency_unit_mismatch,
)
from pipeline.logician.gates.f_award_ingest_attn_unverified import (
    F_AWARD_INGEST_ATTN_UNVERIFIED,
    LEDGER_KIND_AWARD_INGEST_ATTESTATION,
    AwardAttestationResult,
    check_award_ingest_attn_unverified,
)
from pipeline.logician.gates.f_intake_telemetry_leak import (
    CONFIDENTIAL_FIELD_NAMES,
    F_INTAKE_TELEMETRY_LEAK,
    IntakeTelemetryLeakResult,
    check_intake_telemetry_leak,
)
from pipeline.logician.gates.f_intake_logfire_stub_missing import (
    F_INTAKE_LOGFIRE_STUB_MISSING,
    IntakeLogfireStubResult,
    check_intake_logfire_stub_missing,
)

# ---------------------------------------------------------------------------
# Data Collector gate family (WS-I §13 v1 LOCKED 2026-05-10 rows 196/197).
# Eight gates total: 6 graduated from §4 v2.x §5.1 HORIZON to live PRE/POST at
# §13 LOCK; 2 NEW added at Cycle 1 RT-28 (BENEFICIARY-CONSENT-TIER) + Cycle 2
# RT-C2-02 (OPT-OUT-PROPAGATION-FAILED). Predicate bodies realized in WS-I
# Code phase 2026-05-10 (this LOCK cycle's slice 1).
# ---------------------------------------------------------------------------
from pipeline.logician.gates.f_datacollector_consent_missing import (
    F_DATACOLLECTOR_CONSENT_MISSING,
    ConsentMissingResult,
    check_config_signature as check_datacollector_config_signature,
    check_config_value_ranges as check_datacollector_config_value_ranges,
    check_consent_missing as check_datacollector_consent_missing,
    check_send_time_consent_drift as check_datacollector_send_time_consent_drift,
)
from pipeline.logician.gates.f_datacollector_opt_out_active import (
    F_DATACOLLECTOR_OPT_OUT_ACTIVE,
    OptOutActiveResult,
    check_opt_out_active as check_datacollector_opt_out_active,
)
from pipeline.logician.gates.f_datacollector_frequency_cap_exceeded import (
    F_DATACOLLECTOR_FREQUENCY_CAP_EXCEEDED,
    FrequencyCapResult,
    check_frequency_cap_exceeded as check_datacollector_frequency_cap_exceeded,
)
from pipeline.logician.gates.f_datacollector_pii_leak_in_outbound import (
    F_DATACOLLECTOR_PII_LEAK_IN_OUTBOUND,
    PiiLeakResult,
)
from pipeline.logician.gates.f_datacollector_kfr_drift import (
    F_DATACOLLECTOR_KFR_DRIFT,
    KfrDriftResult,
    check_kfr_drift as check_datacollector_kfr_drift,
)
from pipeline.logician.gates.f_datacollector_inbound_classification_unset import (
    F_DATACOLLECTOR_INBOUND_CLASSIFICATION_UNSET,
    check_inbound_classification_unset as check_datacollector_inbound_classification_unset,
)
from pipeline.logician.gates.f_datacollector_beneficiary_consent_tier import (
    F_DATACOLLECTOR_BENEFICIARY_CONSENT_TIER,
    check_beneficiary_consent_tier as check_datacollector_beneficiary_consent_tier,
)
from pipeline.logician.gates.f_datacollector_opt_out_propagation_failed import (
    F_DATACOLLECTOR_OPT_OUT_PROPAGATION_FAILED,
    check_opt_out_propagation_failed as check_datacollector_opt_out_propagation_failed,
)

__all__ = [
    "AuditArtifactReaderCallable",
    "BlockingMissingDetail",
    "BlockingMissingResult",
    "BootstrapReuseDetail",
    "BootstrapReuseResult",
    "CitationMissingDetail",
    "CitationMissingResult",
    "ClockProtocol",
    "CommitteeDegradationTimeoutDetail",
    "CommitteeDegradationTimeoutResult",
    "DailyLogBlockDetail",
    "DailyLogBlockResult",
    "DailyLogReaderCallable",
    "DeprecationExemptionDetail",
    "DeprecationExemptionResult",
    "DeprecationFeedReaderCallable",
    "DeprecationRegisterReaderCallable",
    "DeprecationRegisterStalenessDetail",
    "DeprecationRegisterStalenessResult",
    "DimensionCitationFailure",
    "DraftReaderCallable",
    "ESCALATE_THRESHOLD_DAYS",
    "EVENT_AMBIGUOUS",
    "EVENT_CARVEOUT_GRANTED",
    "EVENT_CLOCK_SKEW_REGISTER_AHEAD",
    "EVENT_CLOCK_SKEW_WARN",
    "EVENT_ESCALATE",
    "EVENT_KIND_PROMOTION",
    "EVENT_KIND_STANZA",
    "EVENT_MISSING",
    "EVENT_NOT_DEPRECATED_OVERRIDE",
    "EVENT_PRECEDENCE_MIXED",
    "EVENT_READER_FAIL",
    "EVENT_REUSE",
    "EVENT_STALE",
    "EVENT_SUSPEND",
    "EVENT_WARN",
    "ExternalManifestReaderCallable",
    "F_AMDT_01",
    "F_AMDT_02",
    "F_AMDT_03",
    "F_AMDT_04",
    "F_AMDT_04_AMBIGUOUS",
    "F_AMDT_04_READER_FAIL",
    "F_AMDT_04_REUSE",
    "F_AMDT_05",
    "F_AMDT_06",
    "F_AMDT_07",
    "F_AMDT_07_AUTHOR_COLLISION",
    "F_AMDT_08",
    "F_AMDT_08_ESCALATE",
    "F_AMDT_08_READER_FAIL",
    "F_AMDT_08_SUSPEND",
    "F_AMDT_09",
    "F_AMDT_09_AMBIGUOUS",
    "F_AMDT_09_MISSING",
    "F_AMDT_09_READER_FAIL",
    "F_AMDT_09_STALE",
    "F_AMDT_10",
    "F_AMDT_10_CHAIN_BREAK",
    "F_AMDT_10_EXTERNAL",
    "F_AMDT_10_PAIR",
    "F_AMDT_10_READER_FAIL",
    "F_AMDT_10_SIGNATURE",
    "F_AMDT_11",
    "F_AMDT_11_DEADLOCK_CARVEOUT_VIOLATION",
    "F_AMDT_11_PRECEDENCE_EMPTY",
    "F_AMDT_11_READER_FAIL",
    "F_AMDT_12",
    "F_AMDT_12_MALFORMED",
    "F_AMDT_12_MISSING",
    "F_AMDT_12_READER_FAIL",
    "FileExistsCallable",
    "HashBytesCallable",
    "LedgerHashReaderCallable",
    "LockHistoryReaderCallable",
    "PinnedHashReaderCallable",
    "PriorChainHeadReaderCallable",
    "RollbackScriptIntegrityDetail",
    "RollbackScriptIntegrityResult",
    "SdkPrecedentReuseDetail",
    "SdkPrecedentReuseResult",
    "RouterConfigReaderCallable",
    "RouterIntegrityDetail",
    "RouterIntegrityResult",
    "RouterYamlReaderCallable",
    "ScriptMetadataReaderCallable",
    "STALENESS_WINDOW_HOURS",
    "SelfReferenceDetail",
    "SelfReferenceResult",
    "SUSPEND_THRESHOLD_DAYS",
    "SignatureVerifyCallable",
    "StanzaPrecedenceDetail",
    "StanzaPrecedenceResult",
    "StanzaReaderCallable",
    "WARN_THRESHOLD_DAYS",
    "check_amendment_self_reference",
    "check_bootstrap_reuse",
    "check_committee_degradation_timeout",
    "check_daily_log_lock_block",
    "check_degradation_stanza_precedence",
    "check_deprecation_exemption_reuse",
    "check_deprecation_register_staleness",
    "check_rollback_script_integrity",
    "check_router_integrity_multi_source",
    "check_sdk_precedent_reuse",
    "check_verdict_blocking",
    "check_verdict_citations",
    # F-LOGICIAN-FABRICATED-ORG (v0.2 spec card)
    "DEFAULT_ALLOWLIST_FIELDS",
    "DEFAULT_FUZZY_THRESHOLD",
    "F_LOGICIAN_FABRICATED_ORG",
    "FabricatedOrgFinding",
    "FabricatedOrgGateResult",
    "build_org_allowlist",
    "check_fabricated_orgs",
    "extract_org_entities",
    # F-LOGICIAN-SPINE-DRIFT (v0.2 spec card)
    "DEFAULT_KEYWORD_RECALL_THRESHOLD",
    "F_LOGICIAN_SPINE_DRIFT",
    "CrossSectionAnchor",
    "NarrativeSpine",
    "SmartOutcomeShape",
    "SpineDriftFinding",
    "SpineDriftGateResult",
    "SpineFraming",
    "SpineSchemaError",
    "check_spine_drift",
    "load_spine",
    # F-LOGICIAN-FACT-DRIFT (v0.2 spec card)
    "DEFAULT_VALUE_TOLERANCE_PCT",
    "F_LOGICIAN_FACT_DRIFT",
    "MATCH_JACCARD_THRESHOLD",
    "FactDriftFinding",
    "FactDriftGateResult",
    "KeyFactsRegister",
    "KfrFact",
    "KfrSchemaError",
    "NumericClaim",
    "TemporalWindow",
    "ValidationBlock",
    "check_fact_drift",
    "extract_numeric_claims",
    "load_kfr",
    # ---- Funder Intel family (v7.0.5; WS-L) ----
    "CONSENT_TIER_SIGNATURE_KIND",
    "ChannelGLeakResult",
    "ConsentTierViolationResult",
    "DEFAULT_STALE_THRESHOLD_DAYS",
    "F_CHANNEL_G_CROSS_ORG_LEAK",
    "F_CHANNEL_G_SANITIZATION_BYPASS",
    "F_FUNDER_CORPUS_INTEGRITY",
    "F_FUNDER_CORPUS_STALE",
    "F_MATCH_DB_CONSENT_TIER_VIOLATION",
    "F_MATCH_DB_CROSS_ORG",
    "F_VECTOR_NS_MISMATCH",
    "FUNDER_TYPE_STALE_THRESHOLD_DAYS",
    "FunderCorpusIntegrityResult",
    "FunderCorpusStaleResult",
    "MatchDbCrossOrgResult",
    "PER_ORG_NAMESPACE_PREFIXES",
    "PERMITTED_CONSENT_TIERS",
    "SanitizationBypassResult",
    "VectorNsMismatchResult",
    "WORKSPACE_SCOPED_NAMESPACES",
    "check_channel_g_cross_org_leak",
    "check_channel_g_sanitization_bypass",
    "check_funder_corpus_integrity",
    "check_funder_corpus_stale",
    "check_match_db_consent_tier_violation",
    "check_match_db_cross_org",
    "check_vector_ns_mismatch",
    # ---- Uploader family (v2.7 SCOPING DRAFT; WS-F in-flight) ----
    "F_UPLOADER_ATTACHMENT_MISSING",
    "F_UPLOADER_ATTACHMENT_TAMPERED",
    "F_UPLOADER_AUTOSUBMIT_ATTEMPTED",
    "F_UPLOADER_CONTENT_MUTATION",
    "F_UPLOADER_FORMAT_MISMATCH",
    "F_UPLOADER_INPUT_INCONSISTENT",
    "F_UPLOADER_ORG_CROSS_REF",
    "F_UPLOADER_PACKAGE_INCOMPLETE",
    "F_UPLOADER_RFA_MISSING",
    "F_UPLOADER_SIGNATURE_MISMATCH",
    "F_UPLOADER_SIGNATURE_MISSING",
    "OrgCrossRefResult",
    "PackageIncompleteResult",
    "SignatureMissingResult",
    "check_uploader_attachment_missing",
    "check_uploader_attachment_tampered",
    "check_uploader_autosubmit_attempted",
    "check_uploader_content_mutation",
    "check_uploader_format_mismatch",
    "check_uploader_input_inconsistent",
    "check_uploader_org_cross_ref",
    "check_uploader_package_incomplete",
    "check_uploader_rfa_missing",
    "check_uploader_signature_mismatch",
    "check_uploader_signature_missing",
    # ---- KFR family residuals (v7.0.4; WS-L Slice 2) ----
    "AUDIT_CHAIN_KIND_INITIAL",
    "AUDIT_CHAIN_KIND_SP0_REVIEW",
    "AUDIT_CHAIN_PERMITTED_KINDS",
    "AwardSignatureLeg",
    "AwardSignatureResult",
    "BENCHMARK_DEFAULT_VALUE_TOLERANCE_PCT",
    "BenchmarkPerOrgRefResult",
    "CandidateFact",
    "EXTRACTOR_PERMITTED_MODES",
    "EXTRACTOR_PERMITTED_SUBSTRATES",
    "ExtractorFabricationResult",
    "F_BENCHMARK_CONTAINS_PER_ORG_REF",
    "F_BENCHMARK_CONTAINS_PER_ORG_REF_PATH",
    "F_BENCHMARK_CONTAINS_PER_ORG_REF_VALUE",
    "F_EXTRACTOR_AWARD_SIGNATURE_INVALID",
    "F_EXTRACTOR_AWARD_SIGNATURE_INVALID_AWARD",
    "F_EXTRACTOR_AWARD_SIGNATURE_INVALID_PROPOSAL",
    "F_EXTRACTOR_FABRICATION",
    "F_KFR_AUDIT_CHAIN_BROKEN",
    "F_KFR_SIGNATURE_INVALID",
    "F_LOGICIAN_FACT_NEEDED_REQUIRED",
    "F_LOGICIAN_FACT_TOLERANCE_DRIFT",
    "FactNeededRequiredResult",
    "FactToleranceDriftResult",
    "KEY_ROTATION_MARKER_KIND",
    "KeyringEntry",
    "KfrSignatureValidationResult",
    "LEDGER_KIND_WIDEN",
    "LEDGER_KIND_WIDEN_RECONFIRM",
    "MODE_AWARD_INGEST",
    "MODE_BULK_INGEST",
    "MODE_INCREMENTAL_INGEST",
    "NEEDED_STATUS_VALUES",
    "NeededFactGap",
    "PerOrgValueProbe",
    "SUBSTRATE_DOCX",
    "SUBSTRATE_MARKDOWN",
    "SUBSTRATE_PDF",
    "TYPE_DEFAULT_TOLERANCE_PCT",
    "check_benchmark_contains_per_org_ref",
    "check_extractor_award_signature_invalid",
    "check_extractor_fabrication",
    "check_fact_needed_required",
    "check_fact_tolerance_drift",
    "check_kfr_audit_chain_broken",
    "check_kfr_signature_invalid",
    # ---- F-CLASS-* dormant primitives (v7.0.7 §5.1; WS-L Slice 3) ----
    "CallInput",
    "ClassRegisterResult",
    "ClassifiedValue",
    "CoverageEntry",
    "CoverageIncompleteResult",
    "F_CLASS_CLOUD_RECEIVED_CONFIDENTIAL",
    "F_CLASS_CLOUD_RECEIVED_OPAQUE_SLOT_FILLED",
    "F_CLASS_COVERAGE_INCOMPLETE",
    "F_CLASS_HIGH_STAKES_FLAG_LEAK",
    "F_CLASS_NEW_FACT_UNCLASSIFIED",
    "F_CLASS_PER_GRANT_OVERRIDE_UNSIGNED",
    "F_CLASS_REGISTER_HASH_MISMATCH",
    "F_CLASS_REGISTER_MISSING",
    "F_CLASS_REGISTER_SIGNATURE_INVALID",
    "F_CLASS_REGISTER_UNSIGNED",
    "F_CLASS_ROUTER_TEMPLATE_SIGNATURE_INVALID",
    "F_CLASS_ROUTING_INDETERMINATE",
    "F_CLASS_SLOT_ID_NON_OPAQUE",
    "F_CLASS_VOICE_CONFIDENTIAL_CLOUD_STT",
    "IncrementalFact",
    "NewFactUnclassifiedResult",
    "OUTBOUND_CLASS_CONFIDENTIAL",
    "OUTBOUND_CLASS_OPERATOR_FLAGGED",
    "OUTBOUND_CLASS_PUBLIC",
    "OUTBOUND_CLASS_SHAREABLE",
    "OutboundBoundaryResult",
    "PENDING_OPERATOR_REVIEW",
    "PER_GRANT_SP0_SIGNATURE_KEY",
    "POSTURE_LOCAL_ONLY",
    "POSTURE_PUBLIC_FRONTIER",
    "POSTURE_SPLIT_CONTEXT",
    "PerGrantOverrideResult",
    "REQUIRED_F_CLASS_CODES",
    "ROUTING_PERMITTED_CLASSES",
    "RouterTemplateSignatureResult",
    "RoutingIndeterminateResult",
    "SIGN_OFF_HASH_CLASS_KEY",
    "SIGN_OFF_HASH_FIELDS_KEY",
    "SIGN_OFF_KEY",
    "SlotPosition",
    "VoiceConfidentialCloudSttResult",
    "check_class_cloud_received_confidential",
    "check_class_cloud_received_opaque_slot_filled",
    "check_class_coverage_incomplete",
    "check_class_high_stakes_flag_leak",
    "check_class_new_fact_unclassified",
    "check_class_per_grant_override_unsigned",
    "check_class_register_hash_mismatch",
    "check_class_register_missing",
    "check_class_register_signature_invalid",
    "check_class_register_unsigned",
    "check_class_router_template_signature_invalid",
    "check_class_routing_indeterminate",
    "check_class_slot_id_non_opaque",
    "check_voice_confidential_cloud_stt",
    # ---- WS-L Slice 4 (v7.0.4-M1 corrective family) ----
    "AllowlistSignatureResult",
    "AstForbiddenNodeResult",
    "AwardAttestationResult",
    "CONFIDENTIAL_FIELD_NAMES",
    "COMPOSITE_KEY_BYTE_LEN",
    "CanonicalSignatureResult",
    "CrossCheckAuditResult",
    "CurrencyContextDriftResult",
    "CurrencyContextMismatchResult",
    "CurrencyContextOmittedResult",
    "CurrencyFloatResult",
    "CurrencyUnitMismatchResult",
    "DerivationArithmeticErrorResult",
    "DuplicateKeyResult",
    "F_AWARD_INGEST_ATTN_UNVERIFIED",
    "F_BENCHMARK_CROSS_CHECK_AUDIT_MISSING",
    "F_BENCHMARK_SEEDING_ALLOWLIST_SIGNATURE_INVALID",
    "F_BENCHMARK_SEEDING_SOURCE_UNAUTHORIZED",
    "F_CURRENCY_CONTEXT_MISMATCH",
    "F_CURRENCY_CONTEXT_OMITTED",
    "F_CURRENCY_DECIMAL_CONTEXT_DRIFT",
    "F_CURRENCY_FLOAT_IN_COMPARISON",
    "F_CURRENCY_UNIT_MISMATCH",
    "F_DERIVATION_AST_FORBIDDEN_NODE",
    "F_DERIVATION_RUNTIME_ARITHMETIC_ERROR",
    "F_INTAKE_LOGFIRE_STUB_MISSING",
    "F_INTAKE_TELEMETRY_LEAK",
    "F_KFR_CANONICAL_SIGNATURE_INVALID",
    "F_KFR_DUPLICATE_KEY",
    "F_KFR_LEGACY_ACCEPT_RE_ENABLED_UNSIGNED",
    "F_KFR_PATH_SYMLINK_FORBIDDEN",
    "F_KFR_TAG_MODIFIED",
    "F_KFR_YAML_CONSTRUCT_FORBIDDEN",
    "IntakeLogfireStubResult",
    "IntakeTelemetryLeakResult",
    "LEDGER_KIND_AWARD_INGEST_ATTESTATION",
    "LEDGER_KIND_LEGACY_RE_ENABLE",
    "LEDGER_KIND_TAG_MODIFIED",
    "LegacyAcceptReEnabledResult",
    "PathSymlinkForbiddenResult",
    "SUB_TAG_DIVIDE_BY_ZERO",
    "SUB_TAG_INVALID_OPERATION",
    "SUB_TAG_OTHER",
    "SUB_TAG_OVERFLOW",
    "SeedingSourceUnauthorizedResult",
    "TRACKED_TAG_FIELDS",
    "TagModifiedResult",
    "YamlConstructForbiddenResult",
    "check_award_ingest_attn_unverified",
    "check_benchmark_cross_check_audit_missing",
    "check_benchmark_seeding_allowlist_signature_invalid",
    "check_benchmark_seeding_source_unauthorized",
    "check_currency_context_mismatch",
    "check_currency_context_omitted",
    "check_currency_decimal_context_drift",
    "check_currency_float_in_comparison",
    "check_currency_unit_mismatch",
    "check_derivation_ast_forbidden_node",
    "check_derivation_runtime_arithmetic_error",
    "check_intake_logfire_stub_missing",
    "check_intake_telemetry_leak",
    "check_kfr_canonical_signature_invalid",
    "check_kfr_duplicate_key",
    "check_kfr_legacy_accept_re_enabled_unsigned",
    "check_kfr_path_symlink_forbidden",
    "check_kfr_tag_modified",
    "check_kfr_yaml_construct_forbidden",
    "classify_arithmetic_error",
    "compute_composite_key",
    "compute_tag_set_hash",
    # ---- Data Collector family (§13 v1 LOCKED 2026-05-10 rows 196/197;
    # WS-I Code phase 2026-05-10) ----
    "ConsentMissingResult",
    "F_DATACOLLECTOR_BENEFICIARY_CONSENT_TIER",
    "F_DATACOLLECTOR_CONSENT_MISSING",
    "F_DATACOLLECTOR_FREQUENCY_CAP_EXCEEDED",
    "F_DATACOLLECTOR_INBOUND_CLASSIFICATION_UNSET",
    "F_DATACOLLECTOR_KFR_DRIFT",
    "F_DATACOLLECTOR_OPT_OUT_ACTIVE",
    "F_DATACOLLECTOR_OPT_OUT_PROPAGATION_FAILED",
    "F_DATACOLLECTOR_PII_LEAK_IN_OUTBOUND",
    "FrequencyCapResult",
    "KfrDriftResult",
    "OptOutActiveResult",
    "PiiLeakResult",
    "check_datacollector_beneficiary_consent_tier",
    "check_datacollector_config_signature",
    "check_datacollector_config_value_ranges",
    "check_datacollector_consent_missing",
    "check_datacollector_frequency_cap_exceeded",
    "check_datacollector_inbound_classification_unset",
    "check_datacollector_kfr_drift",
    "check_datacollector_opt_out_active",
    "check_datacollector_opt_out_propagation_failed",
    "check_datacollector_send_time_consent_drift",
]
