"""pipeline.seats.red_team — §10 Red Team adversarial-review seat.

Blueprint: ``pipeline/blueprint/v0.1/section_10_red_team.md`` (§10 v1
SCOPING DRAFT 2026-05-01) + ``pipeline/blueprint/v0.1/section_05_v7_amendment.md``
(§5 v7 amendment SCOPING DRAFT 2026-05-01) + companion §0.5 §10 amendment.

Round 1 (this tranche): types + attack_memo composer + SFR three-block
emitter. Pure-deterministic; zero LLM, zero network, zero subprocess.

Future rounds:

- **Round 2** — full evidence-in-draft POST pre-check + cross-rubric
  hierarchy support (parent vs subcriteria) + ``__module__`` lineage
  binding to Scribe R3 ``SectionDraft`` and Judge R3 ``JudgeVerdict``.
- **Round 3** — ``seat.py`` subprocess entry, Groq GPT-OSS-120B / Anthropic
  fallback / OpenAI gpt-5.1 escalation provider binding, Logician PRE/POST
  gate wiring (notably ``F-RT-EVIDENCE-NOT-IN-DRAFT``, ``F-RT-FAMILY-OVERLAP``
  3-way distinct, ``F-COUNCIL-SPLIT`` POST-gate routing, M13 escape valve).

Cross-family rigor (§10.7): Red Team production binding = Groq GPT-OSS-120B
primary / Anthropic fallback / OpenAI gpt-5.1 escalation per ``router.yaml``.
Strict 3-way distinct: Red Team's resolved family MUST differ from BOTH
Scribe's resolved family AND Judge's resolved family. Cascade reorder skips
any family already landed by Scribe or Judge.
"""

from __future__ import annotations

from pipeline.seats.red_team.attack_memo import (
    RT_ANCHOR_SUSPECTED_THRESHOLD,
    RT_DISAGREEMENT_THRESHOLD,
    assert_evidence_in_drafts,
    compose_red_team_verdict,
    detect_council_split,
    detect_judge_anchor_suspected,
)
from pipeline.seats.red_team.sfr_emitter import (
    CONCLUSION_HEADING,
    PREMISES_HEADING,
    TRACE_HEADING,
    emit_sfr_certificate,
    parse_recommendation_from_sfr,
    parse_total_score_from_sfr,
)
from pipeline.seats.red_team.types import (
    F_COUNCIL_SPLIT,
    F_RT_ADMIN_RISK_REGISTER_STALE,
    F_RT_ADMIN_RISK_UNFLAGGED,
    F_RT_CONTEXT_PLACEMENT,
    F_RT_CRITERION_MISSING,
    F_RT_DIALECT_DRIFT,
    F_RT_DIALECT_UNCLASSIFIED,
    F_RT_EVIDENCE_NOT_IN_DRAFT,
    F_RT_FAMILY_OVERLAP,
    F_RT_INPUT_INCONSISTENT,
    F_RT_INPUT_MISSING,
    F_RT_JUDGE_ANCHOR_SUSPECTED,
    F_RT_NO_COMPLIANT_FAMILY,
    F_RT_ORG_CROSS_REF,
    F_RT_RECOMMENDATION_INVALID,
    F_RT_RFA_MISSING,
    F_RT_RUBRIC_DRIFT,
    F_RT_SCOPE_MISSING,
    F_RT_SCORE_OUT_OF_RANGE,
    F_RT_SCORE_SUM_MISMATCH,
    F_RT_TIER_NOT_VERBATIM,
    F_RT_VERDICT_CERT_MALFORMED,
    F_RT_WEAKNESS_FIELD_MISSING,
    F_RT_WEAKNESSES_EMPTY,
    MAX_EVIDENCE_CHARS,
    MAX_NOTES_CHARS,
    MAX_OPERATOR_RATIONALE_CHARS,
    MAX_OVERALL_VERDICT_CHARS,
    MAX_TOP_WEAKNESSES,
    MAX_WEAKNESS_FIELD_CHARS,
    MIN_TOP_WEAKNESSES,
    AttackMemo,
    ClaimEvidenceLike,
    CouncilSplitDecision,
    CouncilSplitDecisionTag,
    JudgeCriterionScoreLike,
    JudgeVerdictLike,
    RedTeamCriterionScore,
    RedTeamDialect,
    RedTeamInput,
    RedTeamRecommendation,
    RedTeamVerdict,
    RubricLike,
    SectionDraftLike,
    TotalScoreCorrection,
    Weakness,
    WeaknessSeverity,
)


__all__ = [
    # Closed-set Literals
    "WeaknessSeverity",
    "RedTeamRecommendation",
    "RedTeamDialect",
    "CouncilSplitDecisionTag",
    # Schemas
    "Weakness",
    "AttackMemo",
    "RedTeamCriterionScore",
    "TotalScoreCorrection",
    "RedTeamVerdict",
    "RedTeamInput",
    "CouncilSplitDecision",
    # Forward-Protocols
    "ClaimEvidenceLike",
    "SectionDraftLike",
    "JudgeCriterionScoreLike",
    "JudgeVerdictLike",
    "RubricLike",
    # Failure-code constants
    "F_COUNCIL_SPLIT",
    "F_RT_ADMIN_RISK_REGISTER_STALE",
    "F_RT_ADMIN_RISK_UNFLAGGED",
    "F_RT_CONTEXT_PLACEMENT",
    "F_RT_CRITERION_MISSING",
    "F_RT_DIALECT_DRIFT",
    "F_RT_DIALECT_UNCLASSIFIED",
    "F_RT_EVIDENCE_NOT_IN_DRAFT",
    "F_RT_FAMILY_OVERLAP",
    "F_RT_INPUT_INCONSISTENT",
    "F_RT_INPUT_MISSING",
    "F_RT_JUDGE_ANCHOR_SUSPECTED",
    "F_RT_NO_COMPLIANT_FAMILY",
    "F_RT_ORG_CROSS_REF",
    "F_RT_RECOMMENDATION_INVALID",
    "F_RT_RFA_MISSING",
    "F_RT_RUBRIC_DRIFT",
    "F_RT_SCOPE_MISSING",
    "F_RT_SCORE_OUT_OF_RANGE",
    "F_RT_SCORE_SUM_MISMATCH",
    "F_RT_TIER_NOT_VERBATIM",
    "F_RT_VERDICT_CERT_MALFORMED",
    "F_RT_WEAKNESS_FIELD_MISSING",
    "F_RT_WEAKNESSES_EMPTY",
    # Length caps
    "MAX_EVIDENCE_CHARS",
    "MAX_NOTES_CHARS",
    "MAX_OPERATOR_RATIONALE_CHARS",
    "MAX_OVERALL_VERDICT_CHARS",
    "MAX_TOP_WEAKNESSES",
    "MAX_WEAKNESS_FIELD_CHARS",
    "MIN_TOP_WEAKNESSES",
    # Composer + helpers
    "RT_ANCHOR_SUSPECTED_THRESHOLD",
    "RT_DISAGREEMENT_THRESHOLD",
    "assert_evidence_in_drafts",
    "compose_red_team_verdict",
    "detect_council_split",
    "detect_judge_anchor_suspected",
    "emit_sfr_certificate",
    "parse_recommendation_from_sfr",
    "parse_total_score_from_sfr",
    # SFR block headings
    "PREMISES_HEADING",
    "TRACE_HEADING",
    "CONCLUSION_HEADING",
]
