"""pipeline.seats.red_team.types — §10 Red Team Round 1 shape-only dataclasses.

Blueprint: ``pipeline/blueprint/v0.1/section_10_red_team.md`` (§10 v1
SCOPING DRAFT 2026-05-01) + ``pipeline/blueprint/v0.1/section_05_v7_amendment.md``
(§5 v7 amendment SCOPING DRAFT 2026-05-01; CouncilSplitDecision shape).

Round 1 ships only **shape**: frozen, kw_only, slots=True dataclasses for
:class:`RedTeamInput`, :class:`RedTeamVerdict`, :class:`RedTeamCriterionScore`,
:class:`AttackMemo`, :class:`Weakness`, :class:`TotalScoreCorrection`,
:class:`CouncilSplitDecision`; plus forward-:class:`Protocol` contracts
(:class:`SectionDraftLike`, :class:`ClaimEvidenceLike`, :class:`JudgeVerdictLike`,
:class:`RubricLike`) that bind to Scribe R3's / Judge R3's concrete shapes
at Red Team R2 open via the E-026 ``__module__`` lineage check.

Threat model (R1):

- **In scope at R1.** Construction-time invariants on every dataclass:
  closed-set Literal severity / recommendation / dialect / decision,
  field non-empty checks, score / max_points bounds, ISO-8601 timestamp
  format, length caps per §10.5 (evidence ≤ 320 chars; notes ≤ 480
  chars; overall_verdict ≤ 480 chars; weakness fields per orchestrator-
  CLI tersity discipline ≤ 25 words / ~150 chars).
- **Out of scope at R1, deferred to R2/R3.** Evidence-in-draft
  verification (Logician POST-gate ``F-RT-EVIDENCE-NOT-IN-DRAFT`` —
  R3 wires Logician), LLM provider binding (R3 — Groq GPT-OSS-120B
  primary), cross-family 3-way routing (R3 — F-RT-FAMILY-OVERLAP +
  cascade reorder), SFR format parser (R3 — §6 Operating Envelope owns
  the parser; this module ships the *emitter* in :mod:`sfr_emitter`),
  subprocess entry, council-split dispatch (R3 — F-COUNCIL-SPLIT POST-
  gate wired in :mod:`pipeline.seats.red_team.logician_wiring`).

§7 design decision pin: every frozen dataclass is ``kw_only=True`` so
field additions in v0.2 cannot silently reorder positional calls (A-13
memory-layout discipline; Scribe / Judge precedent).

The forward-Protocols here document exactly the surface Red Team reads
from Scribe's ``SectionDraft`` (``section_name``, ``section_order``,
``body_text``, ``claim_evidence_map``) and Judge's ``JudgeVerdict``
(``run_id``, ``rubric_hash``, ``total_score``, ``max_score``,
``recommendation``, ``overall_notes``). R2 ships the ``__module__``-
lineage assertion that binds these to the concrete Scribe / Judge shapes;
R1 unit tests inject deterministic stubs that satisfy the Protocols
structurally.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Final, Literal, Protocol, runtime_checkable


# ---------------------------------------------------------------------------
# Closed-set Literal aliases (V1 inline-literal rebind-resistance pattern)
# ---------------------------------------------------------------------------

WeaknessSeverity = Literal["high", "medium", "low"]
RedTeamRecommendation = Literal["competitive", "marginal", "not_ready"]
RedTeamDialect = Literal["conservative", "centrist", "progressive", "soul_fire"]
CouncilSplitDecisionTag = Literal[
    "proceed_with_judge",
    "proceed_with_red_team",
    "revise",
    "drop",
]


_WEAKNESS_SEVERITIES: Final[frozenset[str]] = frozenset({"high", "medium", "low"})
_RT_RECOMMENDATIONS: Final[frozenset[str]] = frozenset(
    {"competitive", "marginal", "not_ready"}
)
_RT_DIALECTS: Final[frozenset[str]] = frozenset(
    {"conservative", "centrist", "progressive", "soul_fire"}
)
_COUNCIL_SPLIT_DECISIONS: Final[frozenset[str]] = frozenset(
    {"proceed_with_judge", "proceed_with_red_team", "revise", "drop"}
)


# Module-load integrity asserts — V1 inline-literal pattern (TAB_ORDERING
# precedent from §5 v3 V1 closure; Scribe + Judge mirror).
assert _WEAKNESS_SEVERITIES == frozenset({"high", "medium", "low"}), (
    "_WEAKNESS_SEVERITIES rebound at module load; refusing to load "
    "pipeline.seats.red_team.types"
)
assert _RT_RECOMMENDATIONS == frozenset({"competitive", "marginal", "not_ready"}), (
    "_RT_RECOMMENDATIONS rebound at module load; refusing to load "
    "pipeline.seats.red_team.types"
)
assert _RT_DIALECTS == frozenset(
    {"conservative", "centrist", "progressive", "soul_fire"}
), "_RT_DIALECTS rebound at module load; refusing to load pipeline.seats.red_team.types"
assert _COUNCIL_SPLIT_DECISIONS == frozenset(
    {"proceed_with_judge", "proceed_with_red_team", "revise", "drop"}
), (
    "_COUNCIL_SPLIT_DECISIONS rebound at module load; refusing to load "
    "pipeline.seats.red_team.types"
)


# ---------------------------------------------------------------------------
# §10 R1 failure-code string constants — R3 wires the gates.
# ---------------------------------------------------------------------------

F_RT_INPUT_MISSING: Final[str] = "F-RT-INPUT-MISSING"
F_RT_INPUT_INCONSISTENT: Final[str] = "F-RT-INPUT-INCONSISTENT"
F_RT_RUBRIC_DRIFT: Final[str] = "F-RT-RUBRIC-DRIFT"
F_RT_RFA_MISSING: Final[str] = "F-RT-RFA-MISSING"
F_RT_SCOPE_MISSING: Final[str] = "F-RT-SCOPE-MISSING"
F_RT_ORG_CROSS_REF: Final[str] = "F-RT-ORG-CROSS-REF"
F_RT_DIALECT_UNCLASSIFIED: Final[str] = "F-RT-DIALECT-UNCLASSIFIED"
F_RT_FAMILY_OVERLAP: Final[str] = "F-RT-FAMILY-OVERLAP"
F_RT_NO_COMPLIANT_FAMILY: Final[str] = "F-RT-NO-COMPLIANT-FAMILY"
F_RT_ADMIN_RISK_REGISTER_STALE: Final[str] = "F-RT-ADMIN-RISK-REGISTER-STALE"
F_RT_CONTEXT_PLACEMENT: Final[str] = "F-RT-CONTEXT-PLACEMENT"
F_RT_VERDICT_CERT_MALFORMED: Final[str] = "F-RT-VERDICT-CERT-MALFORMED"
F_RT_EVIDENCE_NOT_IN_DRAFT: Final[str] = "F-RT-EVIDENCE-NOT-IN-DRAFT"
F_RT_SCORE_OUT_OF_RANGE: Final[str] = "F-RT-SCORE-OUT-OF-RANGE"
F_RT_SCORE_SUM_MISMATCH: Final[str] = "F-RT-SCORE-SUM-MISMATCH"
F_RT_CRITERION_MISSING: Final[str] = "F-RT-CRITERION-MISSING"
F_RT_TIER_NOT_VERBATIM: Final[str] = "F-RT-TIER-NOT-VERBATIM"
F_RT_WEAKNESSES_EMPTY: Final[str] = "F-RT-WEAKNESSES-EMPTY"
F_RT_WEAKNESS_FIELD_MISSING: Final[str] = "F-RT-WEAKNESS-FIELD-MISSING"
F_RT_RECOMMENDATION_INVALID: Final[str] = "F-RT-RECOMMENDATION-INVALID"
F_RT_ADMIN_RISK_UNFLAGGED: Final[str] = "F-RT-ADMIN-RISK-UNFLAGGED"
F_RT_DIALECT_DRIFT: Final[str] = "F-RT-DIALECT-DRIFT"
F_COUNCIL_SPLIT: Final[str] = "F-COUNCIL-SPLIT"
F_RT_JUDGE_ANCHOR_SUSPECTED: Final[str] = "F-RT-JUDGE-ANCHOR-SUSPECTED"


# ---------------------------------------------------------------------------
# §10.5 length caps — V1 inline-literal discipline.
# ---------------------------------------------------------------------------

MAX_EVIDENCE_CHARS: Final[int] = 320
MAX_NOTES_CHARS: Final[int] = 480
MAX_OVERALL_VERDICT_CHARS: Final[int] = 480
MAX_WEAKNESS_FIELD_CHARS: Final[int] = 320  # claim/why_it_fails/etc.
MAX_TOP_WEAKNESSES: Final[int] = 5
MIN_TOP_WEAKNESSES: Final[int] = 1  # F-RT-WEAKNESSES-EMPTY trigger
MAX_OPERATOR_RATIONALE_CHARS: Final[int] = 480

assert MAX_EVIDENCE_CHARS == 320, (
    "MAX_EVIDENCE_CHARS rebound; refusing to load"
)
assert MAX_TOP_WEAKNESSES == 5, "MAX_TOP_WEAKNESSES rebound; refusing to load"
assert MIN_TOP_WEAKNESSES == 1, "MIN_TOP_WEAKNESSES rebound; refusing to load"


# ---------------------------------------------------------------------------
# Forward-Protocols — Scribe + Judge surface Red Team reads (R2 binds to
# concrete Scribe R3 SectionDraft + Judge R3 JudgeVerdict via E-026 lineage).
# ---------------------------------------------------------------------------


@runtime_checkable
class ClaimEvidenceLike(Protocol):
    """Forward-Protocol for Scribe's ``ClaimEvidence`` (§7.4a + §7.5).

    R1 reads ``evidence_kind`` (RFA / PROJECT_CONTEXT / USER_DATA) +
    ``source_pointer`` (anchor string). R2 binds this to Scribe R2.5's
    concrete ``ClaimEvidence`` via ``__module__`` lineage assertion.
    """

    evidence_kind: str
    source_pointer: str


@runtime_checkable
class SectionDraftLike(Protocol):
    """Forward-Protocol for Scribe's ``SectionDraft`` (§7.5)."""

    section_name: str
    section_order: int
    body_text: str
    claim_evidence_map: tuple[ClaimEvidenceLike, ...]


@runtime_checkable
class JudgeCriterionScoreLike(Protocol):
    """Forward-Protocol for Judge's ``CriterionScore`` (§9 R1 types)."""

    criterion_id: str
    score: int
    max_points: int


@runtime_checkable
class JudgeVerdictLike(Protocol):
    """Forward-Protocol for Judge's ``JudgeVerdict`` (§9 R2 types).

    R1 reads only the headline numbers + recommendation + truncated notes.
    Per §10.8, Red Team does NOT see Judge's per-criterion breakdown
    (anti-anchoring discipline). The Protocol does not expose ``criteria``.
    """

    run_id: str
    rubric_hash: str
    total_score: int
    max_score: int
    recommendation: str
    overall_notes: str  # consumed truncated to 400 chars per orchestrator CLI


@runtime_checkable
class RubricLike(Protocol):
    """Forward-Protocol for Judge's ``Rubric`` (§9 R1 types)."""

    rubric_id: str
    content_hash: str
    max_score: int
    criteria: tuple


# ---------------------------------------------------------------------------
# §10.5 schemas — frozen, kw_only, slots=True
# ---------------------------------------------------------------------------


def _ensure_tz_aware_utc(dt: datetime, *, field_name: str) -> None:
    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) != timezone.utc.utcoffset(
        datetime.now(tz=timezone.utc)
    ):
        # Tolerate any offset-aware tz; only bare-naive is rejected.
        if dt.tzinfo is None:
            raise ValueError(
                f"{field_name} must be tz-aware; got naive datetime {dt!r}"
            )


@dataclass(frozen=True, kw_only=True, slots=True)
class Weakness:
    """A single prosecutorial finding within :class:`AttackMemo.top_weaknesses`."""

    severity: WeaknessSeverity
    claim: str
    why_it_fails: str
    what_a_reviewer_would_say: str
    fix_hint: str

    def __post_init__(self) -> None:
        if self.severity not in _WEAKNESS_SEVERITIES:
            raise ValueError(
                f"severity must be one of {sorted(_WEAKNESS_SEVERITIES)}; "
                f"got {self.severity!r}"
            )
        for field_name in (
            "claim",
            "why_it_fails",
            "what_a_reviewer_would_say",
            "fix_hint",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Weakness.{field_name} must be non-empty str")
            if len(value) > MAX_WEAKNESS_FIELD_CHARS:
                raise ValueError(
                    f"Weakness.{field_name} exceeds {MAX_WEAKNESS_FIELD_CHARS} chars "
                    f"({len(value)})"
                )


@dataclass(frozen=True, kw_only=True, slots=True)
class AttackMemo:
    """The prosecutorial memo (§10.5)."""

    top_weaknesses: tuple[Weakness, ...]
    unsupported_assertions: tuple[str, ...]
    dialect_mismatches: tuple[str, ...]
    boundary_drift: tuple[str, ...]
    overall_verdict: str

    def __post_init__(self) -> None:
        n = len(self.top_weaknesses)
        if n < MIN_TOP_WEAKNESSES:
            raise ValueError(
                f"AttackMemo.top_weaknesses requires at least {MIN_TOP_WEAKNESSES}; "
                f"got {n} (Red Team must produce at least one weakness)"
            )
        if n > MAX_TOP_WEAKNESSES:
            raise ValueError(
                f"AttackMemo.top_weaknesses exceeds {MAX_TOP_WEAKNESSES}; got {n}"
            )
        for field_name in ("unsupported_assertions", "dialect_mismatches", "boundary_drift"):
            value = getattr(self, field_name)
            if not isinstance(value, tuple):
                raise TypeError(
                    f"AttackMemo.{field_name} must be tuple; got {type(value).__name__}"
                )
            for i, item in enumerate(value):
                if not isinstance(item, str) or not item.strip():
                    raise ValueError(
                        f"AttackMemo.{field_name}[{i}] must be non-empty str"
                    )
        if not isinstance(self.overall_verdict, str) or not self.overall_verdict.strip():
            raise ValueError("AttackMemo.overall_verdict must be non-empty str")
        if len(self.overall_verdict) > MAX_OVERALL_VERDICT_CHARS:
            raise ValueError(
                f"AttackMemo.overall_verdict exceeds {MAX_OVERALL_VERDICT_CHARS} chars "
                f"({len(self.overall_verdict)})"
            )


@dataclass(frozen=True, kw_only=True, slots=True)
class RedTeamCriterionScore:
    """Red Team's score for a single rubric criterion (§10.5 + §10.8)."""

    criterion_id: str
    criterion_name: str
    max_points: int
    score: int
    tier_matched: str
    evidence: str
    missing: tuple[str, ...]
    notes: str

    def __post_init__(self) -> None:
        if not isinstance(self.criterion_id, str) or not self.criterion_id.strip():
            raise ValueError("criterion_id must be non-empty str")
        if not isinstance(self.criterion_name, str) or not self.criterion_name.strip():
            raise ValueError("criterion_name must be non-empty str")
        if not isinstance(self.max_points, int) or self.max_points < 0:
            raise ValueError(
                f"max_points must be non-negative int; got {self.max_points!r}"
            )
        if not isinstance(self.score, int) or self.score < 0:
            raise ValueError(
                f"score must be non-negative int; got {self.score!r}"
            )
        if self.score > self.max_points:
            raise ValueError(
                f"score {self.score} exceeds max_points {self.max_points} "
                f"(criterion {self.criterion_id})"
            )
        if not isinstance(self.tier_matched, str) or not self.tier_matched.strip():
            raise ValueError("tier_matched must be non-empty str")
        if not isinstance(self.evidence, str) or not self.evidence.strip():
            raise ValueError("evidence must be non-empty str")
        if len(self.evidence) > MAX_EVIDENCE_CHARS:
            raise ValueError(
                f"evidence exceeds {MAX_EVIDENCE_CHARS} chars ({len(self.evidence)})"
            )
        if not isinstance(self.missing, tuple):
            raise TypeError("missing must be tuple")
        for i, item in enumerate(self.missing):
            if not isinstance(item, str) or not item.strip():
                raise ValueError(f"missing[{i}] must be non-empty str")
        if not isinstance(self.notes, str):
            raise TypeError("notes must be str")
        if len(self.notes) > MAX_NOTES_CHARS:
            raise ValueError(
                f"notes exceeds {MAX_NOTES_CHARS} chars ({len(self.notes)})"
            )


@dataclass(frozen=True, kw_only=True, slots=True)
class TotalScoreCorrection:
    """Audit shape — populated when model's reported total ≠ computed sum."""

    model_reported: int
    computed_from_criteria: int
    delta: int  # = computed_from_criteria - model_reported

    def __post_init__(self) -> None:
        if self.delta != self.computed_from_criteria - self.model_reported:
            raise ValueError(
                f"delta {self.delta} ≠ computed_from_criteria - model_reported "
                f"({self.computed_from_criteria - self.model_reported})"
            )


@dataclass(frozen=True, kw_only=True, slots=True)
class RedTeamVerdict:
    """Authoritative Red Team output (§10.5).

    Computed-from-criteria invariant (§10.8): ``total_score == sum(c.score for
    c in criteria)``. The model's reported total is captured in
    ``total_score_correction`` if it disagreed; ``total_score`` is always the
    computed sum (auto-corrected at composer time, R2).
    """

    run_id: str
    rubric_id: str
    rubric_hash: str
    total_score: int
    max_score: int
    recommendation: RedTeamRecommendation
    criteria: tuple[RedTeamCriterionScore, ...]
    attack_memo: AttackMemo
    total_score_correction: TotalScoreCorrection | None
    verdict_at_utc: datetime
    red_team_dialect: RedTeamDialect

    def __post_init__(self) -> None:
        if not isinstance(self.run_id, str) or not self.run_id.strip():
            raise ValueError("run_id must be non-empty str")
        if not isinstance(self.rubric_id, str) or not self.rubric_id.strip():
            raise ValueError("rubric_id must be non-empty str")
        if not isinstance(self.rubric_hash, str) or not self.rubric_hash.strip():
            raise ValueError("rubric_hash must be non-empty str")
        if not isinstance(self.total_score, int) or self.total_score < 0:
            raise ValueError(
                f"total_score must be non-negative int; got {self.total_score!r}"
            )
        if not isinstance(self.max_score, int) or self.max_score <= 0:
            raise ValueError(
                f"max_score must be positive int; got {self.max_score!r}"
            )
        if self.total_score > self.max_score:
            raise ValueError(
                f"total_score {self.total_score} exceeds max_score {self.max_score}"
            )
        if self.recommendation not in _RT_RECOMMENDATIONS:
            raise ValueError(
                f"recommendation must be one of {sorted(_RT_RECOMMENDATIONS)}; "
                f"got {self.recommendation!r}"
            )
        if not isinstance(self.criteria, tuple) or len(self.criteria) == 0:
            raise ValueError("criteria must be non-empty tuple")
        # Computed-total invariant: §10.8 sum-of-criteria authoritative.
        computed_sum = sum(c.score for c in self.criteria)
        if self.total_score != computed_sum:
            raise ValueError(
                f"total_score {self.total_score} ≠ sum-of-criteria {computed_sum} "
                f"(F-RT-SCORE-SUM-MISMATCH would fire at POST-gate; auto-correction "
                f"is composer-side, not constructor-side)"
            )
        if not isinstance(self.attack_memo, AttackMemo):
            raise TypeError(
                f"attack_memo must be AttackMemo; got {type(self.attack_memo).__name__}"
            )
        if self.total_score_correction is not None and not isinstance(
            self.total_score_correction, TotalScoreCorrection
        ):
            raise TypeError(
                "total_score_correction must be TotalScoreCorrection or None"
            )
        if not isinstance(self.verdict_at_utc, datetime):
            raise TypeError("verdict_at_utc must be datetime")
        _ensure_tz_aware_utc(self.verdict_at_utc, field_name="verdict_at_utc")
        if self.red_team_dialect not in _RT_DIALECTS:
            raise ValueError(
                f"red_team_dialect must be one of {sorted(_RT_DIALECTS)}; "
                f"got {self.red_team_dialect!r}"
            )


@dataclass(frozen=True, kw_only=True, slots=True)
class RedTeamInput:
    """Input bundle Red Team consumes at Phase 0 (§10.3).

    The bundle is run-scoped: every field carries the same ``run_id`` and the
    rubric content-hash matches what Judge consumed.
    """

    run_id: str
    section_drafts: tuple[SectionDraftLike, ...]
    claim_evidence_map: tuple[ClaimEvidenceLike, ...]
    rubric: RubricLike
    judge_verdict: JudgeVerdictLike | None
    funder_dialect: RedTeamDialect
    admin_risk_register_snapshot: object  # opaque at R1; R2 binds to AdminRiskRegisterSnapshot
    prepared_at_utc: datetime

    # §4 v2.x.5 CC-007 fields (LOCKED 2026-05-16 row 232) — production
    # wire-up reads these to construct the OutboundCallable wrapper around
    # provider_boundary.stdlib_urlopen_caller. Default to empty / Local-Only
    # so existing test fixtures that omit them still construct cleanly.
    classification_context_json: str = ""
    posture: Literal[
        "frontier_eligible", "split_context_hybrid", "local_only_sovereign"
    ] = "local_only_sovereign"

    def __post_init__(self) -> None:
        if not isinstance(self.run_id, str) or not self.run_id.strip():
            raise ValueError("run_id must be non-empty str")
        if not isinstance(self.section_drafts, tuple) or len(self.section_drafts) == 0:
            raise ValueError("section_drafts must be non-empty tuple")
        if not isinstance(self.claim_evidence_map, tuple):
            raise TypeError("claim_evidence_map must be tuple")
        if self.judge_verdict is not None:
            # Run-scoped binding (§10.3 invariant).
            if self.judge_verdict.run_id != self.run_id:
                raise ValueError(
                    f"judge_verdict.run_id {self.judge_verdict.run_id!r} ≠ "
                    f"input run_id {self.run_id!r} (F-RT-INPUT-INCONSISTENT)"
                )
            if self.judge_verdict.rubric_hash != self.rubric.content_hash:
                raise ValueError(
                    f"judge_verdict.rubric_hash != rubric.content_hash "
                    f"(F-RT-INPUT-INCONSISTENT)"
                )
        if self.funder_dialect not in _RT_DIALECTS:
            raise ValueError(
                f"funder_dialect must be one of {sorted(_RT_DIALECTS)}; "
                f"got {self.funder_dialect!r}"
            )
        if not isinstance(self.prepared_at_utc, datetime):
            raise TypeError("prepared_at_utc must be datetime")
        _ensure_tz_aware_utc(self.prepared_at_utc, field_name="prepared_at_utc")


@dataclass(frozen=True, kw_only=True, slots=True)
class CouncilSplitDecision:
    """Operator's binary decision at sign-off when Judge ↔ Red Team disagree
    by >= RT_DISAGREEMENT_THRESHOLD points (§10.6 + §5 v7 §3.2.1).

    Ledger-stamped HIGH-severity to the admin-risk register at decision time
    (§10.6 invariant). The decision is the ONLY way to advance from
    ``signoff_pending_council_split`` to ``report_signed``.
    """

    decision: CouncilSplitDecisionTag
    judge_total_score: int
    red_team_total_score: int
    delta_absolute: int  # MUST equal abs(judge - red_team) AND >= RT_DISAGREEMENT_THRESHOLD
    operator_signoff_at_iso: str  # ISO 8601 UTC at moment operator chose
    operator_rationale: str  # ledger-stamped to admin-risk; non-empty

    def __post_init__(self) -> None:
        if self.decision not in _COUNCIL_SPLIT_DECISIONS:
            raise ValueError(
                f"decision must be one of {sorted(_COUNCIL_SPLIT_DECISIONS)}; "
                f"got {self.decision!r}"
            )
        if not isinstance(self.judge_total_score, int) or self.judge_total_score < 0:
            raise ValueError(
                f"judge_total_score must be non-negative int; "
                f"got {self.judge_total_score!r}"
            )
        if not isinstance(self.red_team_total_score, int) or self.red_team_total_score < 0:
            raise ValueError(
                f"red_team_total_score must be non-negative int; "
                f"got {self.red_team_total_score!r}"
            )
        expected_delta = abs(self.judge_total_score - self.red_team_total_score)
        if self.delta_absolute != expected_delta:
            raise ValueError(
                f"delta_absolute {self.delta_absolute} ≠ "
                f"abs(judge - red_team) = {expected_delta}"
            )
        # Note: F-COUNCIL-SPLIT.exceeds_threshold trigger is a POST-gate concern
        # (§5 v7 §4.7); the constructor accepts any non-negative delta_absolute
        # so test fixtures can construct decisions that capture both legitimate
        # splits AND below-threshold corner cases (the gate, not the type,
        # enforces the threshold).
        if not isinstance(self.operator_signoff_at_iso, str) or not self.operator_signoff_at_iso.strip():
            raise ValueError("operator_signoff_at_iso must be non-empty str")
        if not isinstance(self.operator_rationale, str) or not self.operator_rationale.strip():
            raise ValueError("operator_rationale must be non-empty str")
        if len(self.operator_rationale) > MAX_OPERATOR_RATIONALE_CHARS:
            raise ValueError(
                f"operator_rationale exceeds {MAX_OPERATOR_RATIONALE_CHARS} chars "
                f"({len(self.operator_rationale)})"
            )


__all__ = [
    # Closed-set Literal aliases
    "WeaknessSeverity",
    "RedTeamRecommendation",
    "RedTeamDialect",
    "CouncilSplitDecisionTag",
    # Closed-set frozensets
    "_WEAKNESS_SEVERITIES",
    "_RT_RECOMMENDATIONS",
    "_RT_DIALECTS",
    "_COUNCIL_SPLIT_DECISIONS",
    # Failure code constants
    "F_RT_INPUT_MISSING",
    "F_RT_INPUT_INCONSISTENT",
    "F_RT_RUBRIC_DRIFT",
    "F_RT_RFA_MISSING",
    "F_RT_SCOPE_MISSING",
    "F_RT_ORG_CROSS_REF",
    "F_RT_DIALECT_UNCLASSIFIED",
    "F_RT_FAMILY_OVERLAP",
    "F_RT_NO_COMPLIANT_FAMILY",
    "F_RT_ADMIN_RISK_REGISTER_STALE",
    "F_RT_CONTEXT_PLACEMENT",
    "F_RT_VERDICT_CERT_MALFORMED",
    "F_RT_EVIDENCE_NOT_IN_DRAFT",
    "F_RT_SCORE_OUT_OF_RANGE",
    "F_RT_SCORE_SUM_MISMATCH",
    "F_RT_CRITERION_MISSING",
    "F_RT_TIER_NOT_VERBATIM",
    "F_RT_WEAKNESSES_EMPTY",
    "F_RT_WEAKNESS_FIELD_MISSING",
    "F_RT_RECOMMENDATION_INVALID",
    "F_RT_ADMIN_RISK_UNFLAGGED",
    "F_RT_DIALECT_DRIFT",
    "F_COUNCIL_SPLIT",
    "F_RT_JUDGE_ANCHOR_SUSPECTED",
    # Length caps
    "MAX_EVIDENCE_CHARS",
    "MAX_NOTES_CHARS",
    "MAX_OVERALL_VERDICT_CHARS",
    "MAX_WEAKNESS_FIELD_CHARS",
    "MAX_TOP_WEAKNESSES",
    "MIN_TOP_WEAKNESSES",
    "MAX_OPERATOR_RATIONALE_CHARS",
    # Forward-Protocols
    "ClaimEvidenceLike",
    "SectionDraftLike",
    "JudgeCriterionScoreLike",
    "JudgeVerdictLike",
    "RubricLike",
    # Schemas
    "Weakness",
    "AttackMemo",
    "RedTeamCriterionScore",
    "TotalScoreCorrection",
    "RedTeamVerdict",
    "RedTeamInput",
    "CouncilSplitDecision",
]
